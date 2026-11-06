# -*- coding: utf-8 -*-
"""静态检查：标签是否溢出容器、盒子是否互相重叠（浏览器截图不可用时的替代自检）"""
import re, sys, unicodedata
import xml.etree.ElementTree as ET

path = sys.argv[1]
tree = ET.parse(path)
root = tree.getroot()

cells = {}
for c in root.iter("mxCell"):
    cells[c.get("id")] = c

def geom(c):
    g = c.find("mxGeometry")
    if g is None:
        return None
    return (float(g.get("x", 0)), float(g.get("y", 0)),
            float(g.get("width", 0)), float(g.get("height", 0)))

def font_size(style):
    m = re.search(r"fontSize=(\d+)", style or "")
    return int(m.group(1)) if m else 12

def text_width(s, fs):
    w = 0.0
    for ch in s:
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            w += fs * 1.0
        elif ch == " ":
            w += fs * 0.3
        else:
            w += fs * 0.55
    return w

problems = []

# 1) 标签溢出检查
for cid, c in cells.items():
    if c.get("vertex") != "1":
        continue
    g = geom(c)
    if not g:
        continue
    x, y, w, h = g
    label = c.get("value", "")
    if not label or label.startswith("<"):
        continue
    style = c.get("style", "")
    if "text;" in style:
        need = font_size(style) * 1.4
    else:
        fs = font_size(style)
        txt = label.replace("&#xa;", "\n").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        lines = 0
        maxw = 0
        for seg in txt.split("\n"):
            tw = text_width(seg, fs)
            maxw = max(maxw, tw)
            lines += max(1, int(tw / max(1, w - 16)) + (1 if tw % max(1, w - 16) else 0))
        need = lines * fs * 1.35 + 14
        if tw > 0:
            if maxw > w - 12 and lines == 1 and "\n" not in txt:
                problems.append("WIDE  %-10s 宽%.0f 文本%.0f  %s" % (cid, w, maxw, txt[:34]))
        if need > h + 2:
            problems.append("TALL  %-10s 高%.0f 需%.0f (%d行)  %s" % (cid, h, need, lines, txt[:34]))

# 2) 同层兄弟盒子重叠检查（仅同 parent 的 vertex）
from collections import defaultdict
byparent = defaultdict(list)
for cid, c in cells.items():
    if c.get("vertex") == "1" and geom(c):
        byparent[c.get("parent")].append((cid, geom(c)))

for parent, items in byparent.items():
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][1], items[j][1]
            ox = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
            oy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
            if ox > 1 and oy > 1:
                problems.append("OVERLAP parent=%s %s x %s  (%.0f x %.0f)" %
                                (parent, items[i][0], items[j][0], ox, oy))

print("checked %d vertices" % sum(len(v) for v in byparent.values()))
if problems:
    for p in problems:
        print(p)
else:
    print("OK: 无标签溢出、无同层重叠")
