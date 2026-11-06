---
name: business-flow-draw
description: 创建或修改 draw.io 业务流程图 / 泳道图 / 时序图，按业务设计说明书生成可编辑的 .drawio。触发词：按设计说明书改图、按规格说明书改图、业务流程图、业务交互图、画泳道图、时序图、改图、draw.io 图、生成图表。
---

# 业务流程图绘制与维护

产出**可编辑的 `.drawio`**，不是图片。业务内容以项目内的业务设计说明书为准，
通用画图规则以本 skill 的 references 为准。

## 何时用

- 用户要求"按设计说明书改图 / 画业务流程图 / 生成 draw.io 图"
- 需要维护 `docs/diagrams/` 下的既有图

## 工作流

1. **读业务**：`docs/business/<图名>业务设计说明书.md` —— 业务对错、禁则、验收软检查判据
2. **读规范**：`references/flowchart-guidelines.md` —— 线型语义、配色、走线约束
3. **改图源**：只改 `docs/diagrams/gen-*.py`（文案/坐标/样式/连线），**禁止手改 `.drawio`**
4. **生成**：`python3 docs\diagrams\gen-<标识>.py docs\diagrams\<标识>.drawio`（同标识配对）
5. **校验**：按 `references/diagram-checklist.md` 跑硬门槛三条
6. **收尾**：业务有变动 → 同步更新业务设计说明书与其中的变更记录

## 硬性禁止

- 禁止直接编辑 `.drawio`（会被下次生成覆盖）
- 禁止画入技术细节：接口路径、类名、框架名、Filter、Handler、Token 内部实现
- 禁止把本应独立的两个判断合并成一个判断框（业务说明书会指明哪些必须独立）

## 依赖

- **全局 `drawio-skill`**：提供 `.drawio` XML 规范、样式词汇、`validate.py` 几何校验
- 本 skill：提供项目化的流程、验收清单、业务说明书模板

## 关键约定

- **坐标与文案只写在 `gen-*.py`**，说明书中不复制坐标表（避免两份不同步）
- 容器内子节点用**相对坐标**，连线 waypoint 用**页面绝对坐标**
- 菱形进出必须用顶点锚点（上 `0.5/0`、下 `0.5/1`、左 `0/0.5`、右 `1/0.5`）
