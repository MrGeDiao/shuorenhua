# Benchmark Rewrite Prompt

把下面这段 prompt 直接用于模型实跑。它只负责让被测模型按规则处理指定盲测区间，不负责判分。

> 2026-07-11 起改盲测口径：被测模型只读 `evals/benchmark-blind.md`（匿名编号、乱序、无预期），不再读取 `benchmark.md` 和 `run-eval.md`——它们含预期与判分标准，被测模型读了本轮结果作废。

```text
你正在执行「说人话」benchmark 盲测改写实跑。你的任务是作为被测模型，按当前仓库规则处理指定区间的盲测用例，并输出稳定、可被 judge 对照的结果。

路径边界：
- 只使用当前工作目录里的 `./SKILL.md`、`./references/`、`./evals/benchmark-blind.md` 和 `./automation/eval/rewrite-prompt.md`。
- 禁止读取 `./evals/` 下除 `benchmark-blind.md` 外的任何文件：其余文件含预期与判分口径，读了本轮实跑作废。
- SKILL.md 第 6 步引用的「场景样本评测」在本轮实跑中跳过，不要读取。
- 不要读取或引用全局安装副本，例如 `~/.codex/skills/shuorenhua`、`~/.claude/skills/shuorenhua` 或其他仓库外路径。
- 如果某个全局 skill 被自动触发，也只能把它当作运行环境噪音；本轮实跑口径以当前工作目录文件为准。

开始前先读取：
- ./SKILL.md
- ./evals/benchmark-blind.md

再按需读取：
- ./references/positive-style.md
- ./references/protected-spans.md
- ./references/phrases-zh.md
- ./references/phrases-en.md
- ./references/structures.md
- ./references/severity.md
- ./references/examples.md
- ./references/operation-manual.md
- ./references/scene-guardrails.md
- ./references/scene-packs.md
- ./references/boundary-cases.md

输入会指定一个盲测区间，例如：
- B-01 到 B-16
- B-17 到 B-32
- B-33 到 B-48
- B-49 到 B-64
- B-65 到 B-80
- B-81 到 B-96
- B-97 到 B-120

每条用例的字段以 ./evals/benchmark-blind.md 为准：
- 标题行：盲测编号 / 场景
- 测试文本：标题后的引用块或代码块

处理要求：

1. 逐条处理指定区间内的所有用例，不要跳过、合并或增删编号。
2. 每条先输出判定链，再输出处理结果。改写前先在心里按子句 / 事实要素建立事实与关系账本，不要把整句整行只判成“事实”或“姿态”：记录实体类型、数字修饰对象、主体与各自动作 / 目标、目的、适用条件、风险、限制、实现关系，以及谓词的方向、完成态、强度和效果类型；删掉某个子句若会改变命题真值、适用范围或成立条件，就必须进入账本。不需要把账本单独输出。
3. 判定链固定包含四项，各用一个短语：
   - 场景：chat / status / docs / public-writing / code-context，必要时带 README / release-note / forum-post / issue-reply / api-reference / faq / long
   - Tier：Tier 1 / Tier 2 / Tier 3 / protected / not-fix
   - 力度：minimal / standard / aggressive / audit-only / no-op
   - scope：structural / bounded / in-place / not-applicable
4. 该改就改：默认输出改写结果；无源论断按规则属于 audit-only（例如 status/docs 场景的无源引用）时，对该论断输出风险说明，不要伪装成已证实事实。audit-only 只约束无源论断本身，同段其他病灶照常清理，不要整段只输出风险说明。
5. 按规则不该改的保持原文，并说明按哪条规则放行；如果只做最小无害调整，必须说明为什么没有误杀 protected spans、术语、引用或合理语境。
6. code-context 只处理注释、docstring 或 commit message，不改代码。
7. Scene Packs 先保大场景和 protected spans，再按 README / release-note / forum-post / issue-reply / api-reference / faq 的发布目的处理。API reference 的 method、path、字段、类型、约束、状态码、错误码和恢复动作不得漂移；FAQ 不得扩大问题范围、否定、期限和支持承诺，也不要把采访问答误判成 FAQ。
8. scope 判为 in-place 或 bounded 时，严格按 ./SKILL.md「3.5 Edit scope」的合同执行（in-place 不删句、不并句、不重排；bounded 的删除清单边界与无源论断例外以该节为准），不自行放宽或收紧。
9. 输出前做双向核对并检查命中项与处理结果是否一致：先从输入到账本逐项确认范围、条件、否定、情态、完成态、方向、强度、数量—对象和主体—目标都能在输出找回，再从输出回到输入确认每个关系都有原文依据。如果命中项写了“原文没有具体对象 / 能力 / 实现 / 依据”，处理结果不得再补出工具、产品、平台、功能、实现关系或指标；输出里的每个 `X 做 Y / X 基于 Y / X 处理 Y` 关系必须能回指原文同一谓词，不能把背景、主题或相邻句共现拼成新能力；同义改写不得改变谓词方向、完成态、强度或效果类型，例如不能把“已经改善”写成“涉及”，也不能把“提升效率”扩成“节省时间”；命中项列出的保护关系必须逐项保留。

输出格式必须严格如下：

## <盲测编号>

判定链：场景=<...>；Tier=<...>；力度=<...>；scope=<...>

命中项：
- <命中的问题类型、保护点或放行理由>

处理结果：
<改写稿、audit-only 风险说明、或保留原文说明>

禁止：
- 不要猜测或标注用例属于「该改」还是「不该改」的评测分类；按规则处理即可。
- 不要输出自评通过 / 部分通过 / 未通过；判分是 judge 的事。
- 不要跳过用例。
- 不要把多条用例合并到一个标题下。
- 不要改 `## <盲测编号>` 和 `判定链：场景=...；Tier=...；力度=...；scope=...` 这两个格式。
- 不要为了让结果更好看而编造原文没有的来源、数据、责任主体、命令、版本号或指标。
```
