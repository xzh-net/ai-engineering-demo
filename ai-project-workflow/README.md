# ai-project-workflow

> 业务图的规格化生产与维护 · 入口与约定见 [AGENTS.md](AGENTS.md)

## 1. 业务设计说明书

- [统一认证中心业务流程图](docs/business/统一认证中心业务设计说明书.md) — 三端共用一个认证中心，身份认证/授权/账号准入三环节分离，换号后回到最初访问目标
- [统一消息中心订阅推送业务流程图](docs/business/统一消息中心订阅推送业务设计说明书.md) — 订阅授权与触达准入两关卡，含配额延迟重试与换账号不串订阅（模拟演练稿，图尚未生成）

---

## 2. 图源与产物

- [gen-iam-flow.py](docs/diagrams/gen-iam-flow.py) — 图的坐标与文案唯一权威，命名配对 `gen-<标识>.py` ↔ `<标识>.drawio`
- [iam-flow.drawio](docs/diagrams/iam-flow.drawio) — 生成产物，三硬校验通过（0 错误 / 0 警告 / 0 交叉 / 0 重叠），禁止手改

---

## 3. 画图能力（项目级 skill `business-flow-draw`）

- [SKILL.md](.opencode/skills/business-flow-draw/SKILL.md) — 改图工作流、硬性禁止与依赖说明
- [flowchart-guidelines.md](.opencode/skills/business-flow-draw/references/flowchart-guidelines.md) — 线型语义、配色、走线硬规则
- [diagram-checklist.md](.opencode/skills/business-flow-draw/references/diagram-checklist.md) — 三道硬门槛 + 软检查判据 + 排错表
- [business-flow-template.md](.opencode/skills/business-flow-draw/templates/business-flow-template.md) — 业务设计说明书撰写模板
