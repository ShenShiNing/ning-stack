# ning-stack

我的个人工程工作流，打包成一个 agent skill，Claude Code 和 Codex 都能用。和 tstack、pstack 一样，它写的是我自己的做事方式；方法大量取自 Matt Pocock 的 skills、pstack 和 tstack，按我的习惯改写、取舍后放在本仓库里。

English summary: my personal workflow as one agent skill, covering four flows (design, delivery, cleanup, optimization) and the specialist methods behind them. Methods are adapted from Matt Pocock's skills, pstack and tstack at pinned revisions (MIT, see `LICENSES/`).

## 我的工作方式

- 用尽量简单的方式做复杂的东西。
- 每个结果只有一个 owner：接到请求的线程负责到终点线，一个实现者负责一段代码直到所有评审和 CI 修复做完。评审者独立、只读，每轮都是新任务。
- 证据先于结论：先做能变红的复现，再修；结论都标明是实测、推断还是猜测。
- 能观察到的事实由 agent 自己去查。只有影响产品、所有权或不可逆的决定才问我，并且一次问完、附上推荐答案。
- 评审和 CI 并行：先做定向本地证明，开 ready PR，在同一个 head 上同时启动评审和 CI，修复按轮批量推送，最后在最新 head 上过合并门禁。
- 验证深度看真实风险，不靠一套固定的全量流程。额外的测试、注释和抽象都要说得出当前的理由。

## 四条流程

| 流程 | 用途 | 文件 |
| --- | --- | --- |
| 设计 | 新能力：先读源码，按“前沿”分轮对齐决策，在模块缝上定形状，产物大小按执行需要来定 | `references/design.md` |
| 交付 | 从请求走到 `local`、`ready` 或 `merged`：定框、接地、改动与证明、发布、评审与 CI 并行、修复循环、合并门禁 | `references/delivery.md` |
| 清理 | 按成文标准去掉死代码、过时注释、多余测试，每项删除都要有证据 | `references/cleanup.md` |
| 优化 | 重估逻辑与物理架构，按摩擦选点深挖；保留现状也是合法结论 | `references/optimization.md` |

## 短路径与专项方法

`SKILL.md` 只放共享规则和路由，每次只读命中的那个流程文件。专项方法只在触发条件满足时加载：

- `references/methods/investigation.md`：how / why 溯源、诊断难缠的 bug、竞争设计、并行探索。
- `references/methods/review.md`：单评审者的两轴评审、分级与账本、轮次预算；跨模型质询和 council 只在有争议或我要求时用。
- `references/methods/evidence.md`：置信阶梯、按风险分级的证明、blast radius、证据复用、性能数字核查、验证工具。
- `references/methods/continuity.md`：决策轨迹、长时间无人值守运行、暂停、接续、交接、接管、旧 PR 现代化、积压分诊。
- `references/methods/learning.md`：同类错误结构化根治、retro、分阶段计时。

普通的小改动只会走 `SKILL.md` 加上交付流程这一条路，不会触发设计赛跑、多评审或长程规划。

## 安装

把仓库放进 skill 目录即可，仓库根目录就是这个 skill：

```bash
# Claude Code
git clone https://github.com/ShenShiNing/ning-stack ~/.claude/skills/ning-stack

# Codex
git clone https://github.com/ShenShiNing/ning-stack "${CODEX_HOME:-$HOME/.codex}/skills/ning-stack"
```

两边都要用的话，克隆一份，再从另一个目录做符号链接。skill 默认可以自动发现，也可以显式调用 `ning-stack`。

## 在项目里使用

不需要先配置或激活。skill 会读取项目现有的 `AGENTS.md` / `CLAUDE.md`，以及它们指向的文档，从中拿产品和环境约束：checkout 与数据安全、设计权威、架构规则、检查命令、CI 和合并约定、模型分工。优先级从高到低是：harness 与工具规则、我对当前任务的明确指令、项目规则、ning-stack。遇到冲突时按项目规则办，并在报告里写明依据的是哪条。

项目可以在 `AGENTS.md` 里加一小段偏好，没有就用默认值。例如：

```markdown
## ning-stack
- Default finish line: ready
- Reviewer: a different model family from the implementer, medium effort
- Focused checks: `npm test -- <files>`, `npm run typecheck`
- Broad checks for wide changes: `npm run test:integration`
```

真实项目的约束和偏好留在项目自己的仓库里，不放进本 skill。

## 验证

`scripts/trail.py` 是唯一的脚本：记录决策轨迹和分阶段计时（显式的 run、span 起止事件，span 可以重叠；报告给出活动墙钟时间，也就是各 span 的并集，以及会互相重叠的各阶段合计）。测试只用 Python 标准库：

```bash
python3 -m unittest discover -s tests
```

GitHub Actions（`.github/workflows/test.yml`）在每次 push 和 PR 上跑同一组测试。

## 关于速度

这套流程想缩短的是关键路径：连续的 owner、按需拆分、定向证明、评审与 CI 并行、按真实风险决定重测。这些都是设计意图，**没有实测过提速倍数**。想比较新旧流程，就用 `trail.py` 在多个同类任务上记录各阶段，委派任务的耗时不要当成模型本身的延迟。

## 来源

方法改写自下面三个仓库的固定版本，原始文件不随本包分发，运行时也不会读取。逐项的取舍、改写和触发条件见 `references/provenance.md`。

| 来源 | 作者 | 固定版本 | 主要采纳 | 许可 |
| --- | --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2) | Matt Pocock | `5beb35b040e3de97e54fa9e386d7e42d15c295c2` | grilling 的前沿分轮、domain-modeling、codebase-design 的深模块词汇、prototype、to-spec / to-tickets、tdd、diagnosing-bugs、code-review 两轴、improve-codebase-architecture、handoff、triage、wayfinder、retro | MIT，`LICENSES/mattpocock-skills.txt` |
| [cursor/plugins](https://github.com/cursor/plugins/tree/99b609a72323b70204eab407c622f436e858e112/pstack)（pstack） | Lauren Tan | `99b609a72323b70204eab407c622f436e858e112` | how / why、architect、arena、interrogate、swarm、blast-radius、benchmark-checklist、correct、show-me-your-work、figure-it-out，feature、hillclimb、session-pickup、pause-safely 这几个 playbook，no-comments 的一部分，验证工具的创建与维护 | MIT，`LICENSES/pstack.txt` |
| [t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/7de017b3fc9d50c03cf3ecb98fb71e0ca65a78bd) | Theo Browne | `7de017b3fc9d50c03cf3ecb98fb71e0ca65a78bd` | full-send / full-stop、sol-loop、file-pr、babysit-pr、leaving-pr-comments、takeover、modernize、council | MIT，`LICENSES/tstack.txt` |

主要改动：默认的多代理分流（每轮两个评审子代理、七个 why 调查者、实现阶段强制 arena）改成单 agent 默认、按条件升级；评审从“push 之前”挪到“PR 开出后与 CI 并行”；去掉 Cursor 专用的模型名、子代理类型和云端 worker；含义不明的注释保留并列出，而不是直接删。

## 许可

MIT，见 `LICENSE`。上游许可声明原文保存在 `LICENSES/`。
