# -*- coding: utf-8 -*-
"""关卡主视图：三端 -> 统一认证中心(关卡A/关卡B) -> 通过/拒绝回环"""
import sys
from xml.sax.saxutils import escape

def esc(s):
    return escape(str(s)).replace("&amp;#xa;", "&#xa;")

cells, edges = [], []
_n = [1]

def nid():
    _n[0] += 1
    return "c%d" % _n[0]

def node(x, y, w, h, label, style, parent="1"):
    i = nid()
    cells.append('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s">'
                 '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
                 % (i, esc(label), style, parent, x, y, w, h))
    return i

def edge(src, dst, label="", style=None, pts=None, pins=""):
    e = ('<mxCell id="%s" value="%s" style="%s" edge="1" parent="1" source="%s" target="%s">'
         '<mxGeometry relative="1" as="geometry">' % (nid(), esc(label), (style or NORM) + pins, src, dst))
    if pts:
        e += '<Array as="points">' + "".join('<mxPoint x="%d" y="%d"/>' % p for p in pts) + '</Array>'
    edges.append(e + '</mxGeometry></mxCell>')

# ---------- 样式 ----------
NORM = ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "endArrow=block;endSize=8;strokeColor=#333333;fontColor=#333333;labelBackgroundColor=#ffffff;")
DENY = ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "endArrow=block;endSize=8;dashed=1;strokeColor=#b85450;fontColor=#b85450;labelBackgroundColor=#ffffff;")
OK   = ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "endArrow=block;endSize=8;strokeColor=#82b366;fontColor=#3f7a2a;labelBackgroundColor=#ffffff;")
DATA = ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "endArrow=open;endSize=10;dashed=1;strokeColor=#666666;fontColor=#666666;labelBackgroundColor=#ffffff;")

BLUE  = "rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#1f3b63;"
GREEN = "rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#2f5520;"
YELB  = "rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#7a5c00;"
DIAY  = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#7a5c00;"
DIAR  = "rhombus;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontColor=#7a1f1b;"
RED   = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontColor=#7a1f1b;"
ORNG  = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontColor=#7c4a00;"
WHITEP= "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#9673a6;fontColor=#4a2a6b;"
TEXTC = "text;html=1;align=left;verticalAlign=middle;fontSize=13;fontStyle=1;fontColor=#555555;"
NOTE  = ("shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#fff2cc;strokeColor=#d6b656;"
         "align=left;spacingLeft=6;fontSize=11;fontColor=#5a4500;")
CYL   = ("shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=14;"
         "fillColor=#ffffff;strokeColor=#666666;fontColor=#333333;fontSize=11;")
CONT_A = ("swimlane;html=1;startSize=30;collapsible=0;resizeParent=0;fillColor=#e1d5e7;"
          "swimlaneFillColor=#ffffff;strokeColor=#9673a6;strokeWidth=2;fontStyle=1;fontColor=#5c2d91;"
          "fontSize=13;align=left;spacingLeft=8;")
CONT_B = ("swimlane;html=1;startSize=30;collapsible=0;resizeParent=0;fillColor=#ffe6cc;"
          "swimlaneFillColor=#fffaf3;strokeColor=#d79b00;strokeWidth=3;fontStyle=1;fontColor=#7c4a00;"
          "fontSize=13;align=left;spacingLeft=8;")
CONT_N = ("swimlane;html=1;startSize=30;collapsible=0;resizeParent=0;fillColor=#fde7e7;"
          "swimlaneFillColor=#ffffff;strokeColor=#b85450;strokeWidth=2;dashed=1;fontStyle=1;"
          "fontColor=#7a1f1b;fontSize=13;align=left;spacingLeft=8;")
AUTH_C = ("swimlane;html=1;startSize=34;collapsible=0;resizeParent=0;fillColor=#e1d5e7;"
          "swimlaneFillColor=#fbf9fd;strokeColor=#7b4bb5;strokeWidth=3;fontStyle=1;fontColor=#4a2a6b;"
          "fontSize=16;align=center;")

TOP_IN=";entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
BOT_IN=";entryX=0.5;entryY=1;entryDx=0;entryDy=0;"
LEFT_IN=";entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
RIGHT_IN=";entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
LEFT_IN7=";entryX=0;entryY=0.7;entryDx=0;entryDy=0;"
LEFT_IN3=";entryX=0;entryY=0.3;entryDx=0;entryDy=0;"
TOP_OUT=";exitX=0.5;exitY=0;exitDx=0;exitDy=0;"
BOT_OUT=";exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
RIGHT_OUT=";exitX=1;exitY=0.5;exitDx=0;exitDy=0;"
LEFT_OUT=";exitX=0;exitY=0.5;exitDx=0;exitDy=0;"

# ---------- 标题 ----------
cells.append('<mxCell id="title" value="管理后台 · 门户端 · 设备端  共用一个统一认证中心 —— 登录与访问业务交互图" '
             'style="text;html=1;align=left;verticalAlign=middle;fontSize=24;fontStyle=1;fontColor=#262626;" '
             'vertex="1" parent="1"><mxGeometry x="80" y="36" width="1700" height="44" as="geometry"/></mxCell>')

# ---------- 左列：两个浏览器端 ----------
admin  = node(140, 140, 340, 90, "管理后台入口&#xa;管理端用户 · 管理端角色", BLUE)
portal = node(140, 280, 340, 90, "门户端入口&#xa;门户用户 · 门户角色", GREEN)
err    = node(180, 660, 320, 90, "登录失败：&#xa;账号或密码错误", YELB)

# ---------- 认证中心容器 ----------
auth = node(650, 140, 940, 910, "统一认证中心（三端共用同一登录页与同一套关卡）", AUTH_C)
ask      = node(110, 110, 220, 110, "是否已登录？", DIAY, parent=auth)
login    = node(70, 290, 300, 70, "统一登录页 · 输入账号密码", WHITEP, parent=auth)
gateA    = node(40, 400, 360, 300, "关卡 A · 身份认证与授权处理", CONT_A, parent=auth)
identity = node(30, 55, 300, 70, "身份认证&#xa;识别用户身份", WHITEP, parent=gateA)
authorize= node(30, 175, 300, 70, "授权处理&#xa;授权确认（需授权的请求）", WHITEP, parent=gateA)
gateB    = node(520, 300, 340, 210, "关卡 B · 账号准入", CONT_B, parent=auth)
admit    = node(50, 55, 240, 110, "该账号是否属于目标应用&#xa;允许登录的账号范围？", DIAR, parent=gateB)
deliver  = node(70, 800, 300, 70, "交付授权结果", WHITEP, parent=auth)

# ---------- 准入拒绝区（红虚线容器） ----------
zone = node(150, 1005, 440, 320, "准入拒绝 → 提示 → 更换账号（不离开登录页）", CONT_N)
p_deny = node(30, 40, 380, 90, "当前账号无权登录该应用，&#xa;请使用对应端的账号", RED, parent=zone)
p_switch = node(30, 170, 380, 90, "更换对应端账号&#xa;重新登录", ORNG, parent=zone)

# ---------- 右列：数据与结果 ----------
db     = node(1650, 340, 320, 100, "账号与准入规则数据库&#xa;账号 · 角色 · 应用归属 · 准入规则", CYL)
redis  = node(1650, 710, 320, 100, "Redis&#xa;登录会话 · 访问临时状态", CYL)
res    = node(1650, 1180, 420, 230, "回到最初访问目标（换号后恢复原始请求）",
              "swimlane;html=1;startSize=30;collapsible=0;fillColor=#d5e8d4;swimlaneFillColor=#ffffff;"
              "strokeColor=#82b366;strokeWidth=2;fontStyle=1;fontColor=#2f5520;fontSize=13;align=left;spacingLeft=8;")
end_admin  = node(30, 55, 360, 60, "进入管理后台（原目标）", GREEN, parent=res)
end_portal = node(30, 135, 360, 60, "进入门户端（原目标）", GREEN, parent=res)

# ---------- 设备码流程（底部独立带） ----------
d1 = node(130, 1590, 280, 70, "设备端用户&#xa;设备发起设备授权申请", YELB)
d2 = node(490, 1590, 280, 70, "展示设备码&#xa;/ 验证地址", BLUE)
d3 = node(850, 1590, 280, 70, "用户在浏览器打开&#xa;设备验证页面", BLUE)
dev_grp = node(1210, 1530, 720, 170, "统一认证中心 · 设备码路径（同一套关卡 A / 关卡 B）",
               "swimlane;html=1;startSize=30;collapsible=0;fillColor=#e1d5e7;swimlaneFillColor=#fbf9fd;"
               "strokeColor=#7b4bb5;strokeWidth=2;fontStyle=1;fontColor=#4a2a6b;fontSize=13;align=left;spacingLeft=8;")
d4 = node(40, 60, 280, 70, "设备验证页&#xa;设备端账号登录", WHITEP, parent=dev_grp)
d5 = node(400, 60, 280, 70, "设备端账号准入检查", ORNG, parent=dev_grp)
d6 = node(2010, 1590, 280, 70, "用户确认设备授权", GREEN)
d7 = node(2370, 1590, 280, 70, "设备获得授权结果&#xa;继续后续业务操作", BLUE)

# ---------- 说明 ----------
node(130, 1800, 520, 130,
     "换号重登后恢复原始访问请求：最终进入用户&#xa;最初想访问的应用，而不是门户首页。", NOTE)
node(700, 1800, 560, 130,
     "反向场景：管理端账号访问门户端 → 被门户端准入规则&#xa;拒绝 → 换用门户端账号重新登录 → 重新准入通过 →&#xa;返回最初访问的门户页面。", NOTE)
node(1310, 1800, 520, 130,
     "设备码路径与浏览器登录共用同一个统一认证中心&#xa;与同一张准入规则库，另有独立的设备授权确认步骤。", NOTE)

# ---------- 连线 ----------
# 左列三端汇入认证中心
edge(admin, ask, "发起访问", NORM, pts=[(870, 185)], pins=RIGHT_OUT + TOP_IN)
edge(portal, ask, "发起访问", NORM, pts=[(640, 325), (640, 305)], pins=RIGHT_OUT + LEFT_IN)

# 关卡A：未登录 -> 登录页 -> 身份认证
edge(ask, login, "未登录", NORM, pins=BOT_OUT + TOP_IN)
edge(login, identity, "输入并提交", NORM, pins=BOT_OUT + TOP_IN)

# 身份认证 -> 关卡B
edge(identity, admit, "认证成功", NORM, pts=[(1140, 630), (1140, 550)], pins=RIGHT_OUT + LEFT_IN)
# 已登录免输密码 -> 关卡B
edge(ask, admit, "已登录 · 免输密码", NORM, pts=[(1340, 305)], pins=RIGHT_OUT + TOP_IN)

# 关卡B -> 关卡A 续（授权交付）
edge(admit, authorize, "准入通过", OK, pts=[(1340, 750)], pins=BOT_OUT + RIGHT_IN)
edge(authorize, deliver, "", NORM, pins=BOT_OUT + TOP_IN)

# 路径二：密码错误回环
edge(identity, err, "密码错误", DENY, pts=[(610, 630), (610, 705)], pins=LEFT_OUT + RIGHT_IN)
edge(err, login, "重新输入", DENY, pts=[(340, 451)], pins=TOP_OUT + LEFT_IN3)

# 关卡B 拒绝 -> 提示 -> 换号 -> 回登录页
edge(admit, p_deny, "不允许", DENY, pts=[(1560, 550), (1560, 900), (370, 900)], pins=RIGHT_OUT + TOP_IN)
edge(p_deny, p_switch, "更换账号", DENY, pins=BOT_OUT + TOP_IN)
edge(p_switch, login, "重新登录", DENY, pts=[(80, 1220), (80, 400)], pins=LEFT_OUT + ";entryX=0.25;entryY=0;entryDx=0;entryDy=0;")

# 数据侧
edge(gateB, db, "查询账号归属 · 角色 · 应用准入规则", DATA, pts=[(1810, 500)],
     pins=";exitX=1;exitY=0.286;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;")
edge(deliver, redis, "写入登录会话 / 访问临时状态", DATA, pts=[(1650, 975)], pins=RIGHT_OUT + LEFT_IN)

# 通过 -> 回到原目标
edge(deliver, res, "回到最初访问目标", OK, pts=[(870, 1140), (1860, 1140)], pins=BOT_OUT + TOP_IN)

# 设备码流程（底部一条直线）
for a, b in ((d1, d2), (d2, d3), (d3, d4), (d4, d5), (d5, d6), (d6, d7)):
    edge(a, b, "", NORM, pins=RIGHT_OUT + LEFT_IN)

# ---------- 图例 ----------
rows = [("#333333", "s", "正常业务流（黑实线）"),
        ("#b85450", "d", "准入拒绝 · 提示 · 换号（红虚线）"),
        ("#82b366", "s", "准入通过 · 回到原目标（绿线）"),
        ("#666666", "d", "查询数据库 / Redis（灰虚线）"),
        ("#e1d5e7", "b", "关卡 A · 身份认证与授权处理"),
        ("#ffe6cc", "b", "关卡 B · 账号准入"),
        ("#dae8fc", "b", "角色 · 管理端用户 / 管理后台"),
        ("#d5e8d4", "b", "角色 · 门户用户 / 门户端"),
        ("#fff2cc", "b", "角色 · 设备端用户 / 设备端")]
lh = 30 + 24 * len(rows)
legs = ['<mxCell id="legend" value="图例" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;'
        'strokeColor=#666666;verticalAlign=top;fontSize=14;fontStyle=1;align=left;spacingLeft=8;" '
        'vertex="1" parent="1"><mxGeometry x="2150" y="140" width="440" height="%d" as="geometry"/></mxCell>' % lh]
for k, (color, kind, label) in enumerate(rows):
    yy = 34 + 24 * k
    if kind in ("s", "d"):
        dash = ";dashed=1" if kind == "d" else ""
        legs.append('<mxCell id="lg%d" value="" style="endArrow=block;endSize=6;strokeColor=%s%s;html=1;strokeWidth=2;" '
                    'edge="1" parent="legend"><mxGeometry relative="1" as="geometry">'
                    '<mxPoint as="sourcePoint" x="12" y="%d"/><mxPoint as="targetPoint" x="66" y="%d"/>'
                    '</mxGeometry></mxCell>' % (k, color, dash, yy + 8, yy + 8))
    else:
        legs.append('<mxCell id="lgb%d" value="" style="rounded=0;html=1;fillColor=%s;strokeColor=#999999;" '
                    'vertex="1" parent="legend"><mxGeometry x="14" y="%d" width="52" height="16" as="geometry"/>'
                    '</mxCell>' % (k, color, yy))
    legs.append('<mxCell id="lgt%d" value="%s" style="text;html=1;align=left;verticalAlign=middle;fontSize=12;" '
                'vertex="1" parent="legend"><mxGeometry x="80" y="%d" width="350" height="20" as="geometry"/>'
                '</mxCell>' % (k, esc(label), yy - 2))

# ---------- �装配 ----------
W, H = 2750, 1990
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="drawio" version="26.0.0">\n'
       '<diagram name="统一认证中心业务交互图">\n'
       '<mxGraphModel dx="1600" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
       'arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" pageHeight="%d">\n'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n' % (W, H))
xml += "".join(cells) + "\n" + "".join(edges) + "\n" + "".join(legs) + "\n"
xml += '</root></mxGraphModel></diagram></mxfile>\n'
open(sys.argv[1], "w", encoding="utf-8").write(xml)
print("wrote", sys.argv[1], len(xml), "bytes;", len(cells), "nodes,", len(edges), "edges")



