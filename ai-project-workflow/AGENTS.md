# AI 项目工作流 · 项目说明

本仓库 = 业务图（draw.io）的**业务规格 + 图源 + 产物**。业务说明是项目开发文档的一部分，
改图一律**按业务设计说明书执行**，不凭对话记忆。

## 目录职责

| 目录 | 职责 | 权威性 |
|---|---|---|
| `docs/business/` | 业务设计说明书（业务内容、决策、变更记录） | **业务唯一权威源** |
| `docs/diagrams/` | 图的源（`gen-*.py`）与产物（`*.drawio`） | **图的坐标/文案唯一权威源** |
| `.opencode/skills/business-flow-draw/` | 画图能力：规范、验收清单、说明书模板 | 通用能力，跨项目复用 |

## 改图约定

1. 先读 `docs/business/<图名>业务设计说明书.md` —— 业务对错以它为准
2. 只改 `docs/diagrams/gen-*.py`，**禁止手改 `.drawio`**（下次生成会被覆盖）
3. 通用 draw.io 规范（XML 格式、样式词汇、走线约束）见 skill `business-flow-draw`
   的 `references/flowchart-guidelines.md`；底层 XML 规则见已装的全局 `drawio-skill`
4. 图的坐标与文案**只存在于 `gen-*.py`**，说明书中不重复维护坐标表

## 构建命令

```powershell
python3 docs\diagrams\gen-<图名>.py docs\diagrams\<图名>.drawio
```

## 验证要求（硬门槛，三条全过才算交付）

```powershell
# 1. 生成日志必须 nodes>0 且 edges>0
# 2. 几何校验全 0（validate.py 属全局 drawio-skill）
python3 C:\Users\admin\.config\opencode\skills\drawio-skill\scripts\validate.py docs\diagrams\<图名>.drawio --score
# 3. 文字与重叠自检
python3 .opencode\skills\business-flow-draw\scripts\check-diagram.py docs\diagrams\<图名>.drawio
```

详见 skill 的 `references/diagram-checklist.md`（含软检查判据与排错表）。

## 待办

- [ ] **设备码登录流程图**：占位，尚未创建。当前设备码流程是主图底部的一条横带，拆出时需
      独立设计版面，并从主图移除该横带避免重复。
