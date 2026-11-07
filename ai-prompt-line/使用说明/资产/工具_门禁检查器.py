# -*- coding: utf-8 -*-
"""门禁检查器（V0.5 · 只读）

对目标项目跑四项门禁：AGENTS 结构、证据与项数、交叉引用、任务状态与断点。
只读：不修改任何文件；发现不过项即阻断（退出码 1）并指出病层。

用法：
    python 工具_门禁检查器.py --root <目标项目根>
    python 工具_门禁检查器.py            # 默认当前目录
"""

import argparse
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
JUDGE_VALUES = {"通过", "不通过", "待补测", "不适用"}
TASK_STATES = {"待开始", "进行中", "挂起", "已完成", "已放弃"}
SKIP_EVIDENCE = {"", "-", "—", "无", "N/A", "n/a"}


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def sections(text):
    """按 '### 1.2 xxx' 形式抽取编号章节正文。"""
    result, current = {}, None
    for line in text.splitlines():
        m = re.match(r"^#{2,4}\s+(?:§)?(\d+\.\d+)\b", line)
        if m:
            current = m.group(1)
            result[current] = []
        elif current is not None:
            if re.match(r"^#{1,4}\s", line):
                current = None
            else:
                result[current].append(line)
    return {k: "\n".join(v) for k, v in result.items()}


def table_after(lines, key):
    """找到包含 key 的行之后的第一张表，返回 (表头, 数据行)。"""
    for i, line in enumerate(lines):
        if key in line:
            for j in range(i, min(i + 40, len(lines))):
                if lines[j].strip().startswith("|"):
                    header = cells(lines[j])
                    rows, k = [], j + 2
                    while k < len(lines) and lines[k].strip().startswith("|"):
                        row = cells(lines[k])
                        if not re.match(r"^[\s|:－—-]+$", lines[k]):
                            rows.append(row)
                        k += 1
                    return header, rows
            return None, None
    return None, None


def col(header, *names):
    for i, h in enumerate(header):
        for n in names:
            if n in h:
                return i
    return None


def task_table(body):
    """优先找「任务状态表」标签；无标签时退化为 §1.6 内第一张含任务ID 的表。"""
    lines = body.splitlines()
    header, rows = table_after(lines, "任务状态表")
    if not header:
        header, rows = table_after(lines, "任务ID")
    return header, rows


def check_agents(root):
    probs = []
    path = os.path.join(root, "AGENTS.md")
    if not os.path.isfile(path):
        return ["项目根缺少 AGENTS.md（病层：项目根）"]
    text = read_text(path)
    secs = sections(text)
    for s in ("1.2", "1.3", "1.6", "1.7", "1.8"):
        if s not in secs:
            probs.append("AGENTS 缺 §%s（病层：项目 AGENTS；若模板亦缺则病在模板）" % s)
    body16 = secs.get("1.6", "")
    if body16:
        header, _rows = task_table(body16)
        if not header:
            probs.append("§1.6 未找到任务状态表（病层：项目 AGENTS）")
        else:
            need = ["任务ID", "类型", "目标", "状态", "验收判据", "证据", "更新日期"]
            missing = [n for n in need if col(header, n) is None]
            if missing:
                probs.append("§1.6 任务表缺字段 %s（病层：项目 AGENTS；模板契约）" % "、".join(missing))
        if "完整性四查" not in body16:
            probs.append("§1.6 缺完整性四查（病层：项目 AGENTS）")
        if "下一步" not in body16:
            probs.append("§1.6 缺下一步入口（病层：项目 AGENTS）")
    body18 = secs.get("1.8", "")
    if body18:
        for w in ("候选", "已确认", "已生效", "已否决"):
            if w not in body18:
                probs.append("§1.8 缺状态值「%s」（病层：项目 AGENTS）" % w)
    holders = [h for h in re.findall(r"\{[^{}\n]{1,24}\}", text)
               if not re.fullmatch(r"\{\d+\.\.\d+\}", h)]  # {1..5} 区间简写 = 合法速记，非占位
    for h in holders[:3]:
        probs.append("AGENTS 占位残留 %s（病层：项目 AGENTS；P1 生成自查不实）" % h)
    if len(holders) > 3:
        probs.append("AGENTS 占位残留共 %d 处（余略）" % len(holders))
    return probs


def active_workbook(root, agents_text):
    m = re.search(r"激活分册[：:]\s*`([^`]+\.md)`", agents_text)
    if not m:
        m = re.search(r"激活分册[：:]\s*([^\s，,|）)]+\.md)", agents_text)
    if not m:
        return None, "AGENTS §1.2 未写明激活分册路径（病层：项目 AGENTS）"
    raw = m.group(1).strip()
    cand = os.path.join(root, raw.replace("/", os.sep))
    if os.path.isfile(cand):
        return cand, None
    base = os.path.basename(raw)
    for dp, _dn, fn in os.walk(os.path.join(root, "docs", "工作流")):
        if base in fn:
            return os.path.join(dp, base), None
    return None, "激活分册 %s 不存在（病层：项目 AGENTS 指针 / 分册）" % base


def check_evidence(root, agents_text):
    probs, notes = [], []
    wb, err = active_workbook(root, agents_text)
    if err:
        return [err]
    wb_text = read_text(wb)
    wb_ids = set(re.findall(r"\bV-\d{1,3}\b", wb_text))
    if not wb_ids:
        return ["分册未找到 V-NN 验证项编号（病层：分册）"]
    rep_dir = os.path.join(root, "docs", "技术选型")
    reports = []
    if os.path.isdir(rep_dir):
        for f in os.listdir(rep_dir):
            if f.endswith(".md") and "选型验证报告" in f:
                p = os.path.join(rep_dir, f)
                reports.append((os.path.getmtime(p), p))
    if not reports:
        return ["未找到《选型验证报告》（docs/技术选型/*_选型验证报告.md）（病层：项目交付物缺失）"]
    rep = sorted(reports)[-1][1]
    text = read_text(rep)
    header, rows = table_after(text.splitlines(), "原始数据路径")
    if not header:
        return ["报告未找到证据表（需含「原始数据路径」表头）（病层：报告模板 / 报告）"]
    i_judge = col(header, "判定")
    i_raw = col(header, "原始数据")
    i_id = col(header, "编号", "验证项")
    if i_judge is None or i_raw is None:
        return ["证据表缺「判定」或「原始数据路径」列（病层：报告模板）"]
    if len(rows) != len(wb_ids):
        probs.append("证据表 %d 行 ≠ 分册验证项 %d 项（病层：报告漏项 / 分册编号）" % (len(rows), len(wb_ids)))
    rep_ids = set()
    for r in rows:
        rid = r[i_id] if i_id is not None and i_id < len(r) else ""
        found = re.findall(r"\bV-\d{1,3}\b", rid) or re.findall(r"\bV-\d{1,3}\b", " ".join(r))
        rep_ids.update(found)
        if i_judge is not None and i_judge < len(r):
            j = r[i_judge].strip().strip("*").strip()  # 剥 markdown 强调（**不适用** → 不适用），四值按语义比对
            if not any(j.startswith(v) for v in JUDGE_VALUES):
                probs.append("判定「%s」不在四值（病层：报告）" % (j or "空"))
            if j.startswith("通过"):
                raw = r[i_raw].strip().strip("`") if i_raw < len(r) else ""
                if raw in SKIP_EVIDENCE:
                    probs.append("通过项缺原始数据路径（病层：报告 / 验证记录）")
                else:
                    for token in re.findall(r"[^\s，,；;）)]+\.(?:csv|log|txt|json|xlsx|md)", raw):
                        token = token.strip("`")  # 反引号包裹的路径：剥引号后再判存在性
                        target = os.path.join(root, token.replace("/", os.sep))
                        if not os.path.exists(target):
                            probs.append("原始数据路径不存在：%s（病层：验证记录）" % token)
    if rep_ids:
        missing = sorted(wb_ids - rep_ids)
        extra = sorted(rep_ids - wb_ids)
        if missing:
            probs.append("报告缺验证项 %s（病层：报告漏项）" % "、".join(missing))
        if extra:
            probs.append("报告多出分册没有的验证项 %s（病层：报告 / 分册）" % "、".join(extra))
    notes.append("报告：%s；分册：%s" % (os.path.relpath(rep, root), os.path.relpath(wb, root)))
    return probs + notes


def check_links(root):
    probs = []
    all_names, md_files = set(), []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        all_names.update(fn)
        md_files += [os.path.join(dp, f) for f in fn if f.endswith(".md")]
    for p in md_files:
        text = read_text(p)
        for m in re.finditer(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
            link = m.group(1)
            if link.startswith(("http://", "https://", "mailto:")) or "{" in link:
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(p), link))
            if not os.path.exists(target):
                probs.append("断链 %s：%s（病层：项目文档）" % (os.path.relpath(p, root), link))
        for m in re.finditer(r"`([^`\n]+\.(?:md|py|drawio))`", text):
            name = os.path.basename(m.group(1).strip())
            if "{" in name or "*" in name or " " in name:
                continue
            if re.search(r"YYYY|MM|DD|阶段N|验证阶段工作流|\.\.\.", name):
                continue  # 命名约定词（分册命名本体/日期模式），不是实体文件
            if name.startswith(("模板_", "标准_", "工具_")) or re.match(r"^(R|P\d)_", name):
                continue  # 工具仓产物名，允许出现在项目文档里
            if name not in all_names:
                probs.append("引用了不存在的文件 %s（出处 %s，病层：项目文档）"
                             % (name, os.path.relpath(p, root)))
    return probs


def check_state(agents_text):
    probs = []
    body = sections(agents_text).get("1.6", "")
    if not body:
        return ["AGENTS 缺 §1.6（病层：项目 AGENTS）"]
    header, rows = task_table(body)
    if header:
        i_state = col(header, "状态")
        i_ev = col(header, "证据")
        i_id = col(header, "任务ID")
        for r in rows:
            rid = r[i_id] if i_id is not None and i_id < len(r) else "?"
            st = r[i_state].strip() if i_state is not None and i_state < len(r) else ""
            if st not in TASK_STATES:
                probs.append("任务 %s 状态「%s」不在五值（病层：项目 AGENTS）" % (rid, st or "空"))
            if st == "已完成" and i_ev is not None and i_ev < len(r):
                ev = r[i_ev].strip()
                if ev in SKIP_EVIDENCE:
                    probs.append("任务 %s 已完成但无证据（病层：项目 AGENTS / 验证记录）" % rid)
        suspended = set()
        for r in rows:
            if i_state is not None and i_state < len(r) and r[i_state].strip() == "挂起":
                suspended.add(r[i_id].strip() if i_id is not None and i_id < len(r) else "")
        hh, hrows = table_after(body.splitlines(), "阻塞任务ID")
        blocked = set()
        if hrows:
            bi = col(hh, "阻塞任务")
            for r in hrows:
                if bi is not None and bi < len(r):
                    blocked.update(re.findall(r"[VT]-\d{1,3}", r[bi]))
        for rid in sorted(suspended):
            if rid and rid not in blocked:
                probs.append("挂起任务 %s 未进挂起表（病层：项目 AGENTS）" % rid)
    nxt = re.search(r"下一步[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*任务ID[：:]\s*([^\n]*)", body)
    if not nxt:
        probs.append("§1.6 缺「下一步 · 任务ID」入口（病层：项目 AGENTS）")
    elif not nxt.group(1).strip():
        probs.append("§1.6 下一步任务ID为空（病层：项目 AGENTS）")
    return probs


def run(root):
    checks = []
    agents_path = os.path.join(root, "AGENTS.md")
    agents_text = read_text(agents_path) if os.path.isfile(agents_path) else ""
    checks.append(("AGENTS 结构完整性", check_agents(root)))
    if agents_text:
        checks.append(("证据与项数一致性", check_evidence(root, agents_text)))
        checks.append(("任务状态与断点", check_state(agents_text)))
    else:
        checks.append(("证据与项数一致性", ["缺少 AGENTS.md，无法定位分册（病层：项目根）"]))
        checks.append(("任务状态与断点", ["缺少 AGENTS.md，无法检查状态（病层：项目根）"]))
    checks.append(("交叉引用审计", check_links(root)))

    failed = 0
    print("门禁检查：%s" % root)
    for idx, (name, probs) in enumerate(checks, 1):
        # 末尾以"报告：/分册："开头的为定位信息，不算问题
        issues = [p for p in probs if not p.startswith(("报告：", "分册："))]
        notes = [p for p in probs if p.startswith(("报告：", "分册："))]
        if issues:
            failed += 1
            print("\n[%d/4] %s —— 阻断（%d 项）" % (idx, name, len(issues)))
            for p in issues:
                print("  - " + p)
        else:
            print("\n[%d/4] %s —— 通过" % (idx, name))
        for n in notes:
            print("  · " + n)
    if failed:
        print("\n结论：%d 项阻断，退出码 1（请按病层修复后重跑）" % failed)
        return 1
    print("\n结论：四项门禁全部通过，退出码 0")
    return 0


def main():
    ap = argparse.ArgumentParser(description="目标项目四项门禁检查（只读）")
    ap.add_argument("--root", default=".", help="目标项目根目录（默认当前目录）")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("目录不存在：%s" % root)
        return 2
    return run(root)


if __name__ == "__main__":
    sys.exit(main())
