# Changelog

## [2.4.1] - 2026-09-12 — 示例层不再教补造原文没有的信息

> 本版是 patch：规则正文一行未动，只修 references 示例层的「补造数据」问题。旧示例教的是「说人话 = 补具体数字」——人话版里的日活 1200、94%、800ms→120ms、CVE 编号、Stanford 2023 全是原文没有的，与 `SKILL.md` 保真合同「不新增事实」直接矛盾。修法统一为**改原文，让人话版的每个事实都能回指**，人话版多数不动。
> 验收范围是**全量 120 条双席位交叉判分**（另加 HUMAN 10 篇纯脚本统计），两席位 L1 硬约束失败均为 0。这轮同时补上 v2.2.1 起欠的全量基线，并作为 v2.5.0 减法的「改造前」快照。完整证据见 `evals/results-v2.4.1.md`。

### Added

- HUMAN 长文 residual 对照新增 2 篇固定 revision 的中文原作：一篇技术文档写作规范（Public Domain），一篇开源项目进展报告（CC BY-SA 4.0）。两篇都只做机械抽取，不作生成式改写。
- HUMAN cohort 增至 10 篇、9 个作者组；其中历史文本 3 篇、现代公开文本 7 篇，中文原作 8 篇、英译中 2 篇。direct 场景现覆盖 `docs`、`public-writing`、`status`。

### Changed

- HUMAN 代表性门禁恢复为普通阻塞检查，移除 v2.4.0 为收集期临时保留的 `known-gap` 放行通道。
- README 恢复为面向新读者的短结构，只保留项目用途、使用方式、规则边界和评测结论；版本实验过程继续放在评测记录和 changelog，不再占用 README 主流程。
- `positive-style.md` 2.5 补充：语域一致也包括时代感，当下的第一人称口语文里混进上世纪报刊散文腔或 2000 年代博客腔按语域错配处理，怀旧题材、年代小说和刻意复古放行。这类词多数不是 AI 高频词，不进词表，按主语域判断。观察来自 #14。
- **示例层不再教补造原文没有的信息。** 改动文件：`references/examples.md`、`references/structures.md`、`references/scene-packs.md`、`references/positive-style.md`。手法是把人话版里原文没有的事实放回原文、用原文本来的包装裹住，人话版多数不动；说明文字里的「加了具体数据」「换成具体数据」「用具体改动代替抽象描述」一类表述全部改掉，改成「把原文埋在包装里的 X 拎出来」。
  - `examples.md`：示例 1/2/3/4/6/7 与 English Example 1/2 的 AI 版补回人话版已有的事实；示例 4 的真实产品名换成虚构名称，避免公开仓库出现关于真实产品的假跑分；English Example 2 删掉 CVE 编号（原文不给编号，改写也不补）；标注模式示例 A 的原文补一句作者自己的事实，默认改写从元评论改成改写文本。文件头加一句总说明。
  - `structures.md`：第 12 条无源引用的 ✅ 从「补 Stanford 2023 来源」改为 `rewrite-safe` 整条删除 / `audit-only` 标缺来源两档——替作者编来源本身就违反「不要补虚构来源」；第 5、6、13、21 条去掉 ✅ 里补造的百分比与数值；另有 9 处同类问题按同一手法处理（第 1、3、4、11、14、16、17、19、24、25 条）。
  - `scene-packs.md`：README、release-note、issue-reply 三节的 Before 补入 After 已有的信息，forum-post 的 After 换成不补事实也不留二元骨架的版本；release-note 加一行「原文真的没有任何变更信息时，按本节规定改成提示补具体变更，不编」。
  - `positive-style.md`：§2 开头框定「更好 / 不够好」是两种写法的对照而非改写前后；§4 三组 A/B/C 的原文补入「更像人」档已用的事实，并去掉原文没有的因果与动作。三档结构保留。

### Verification status

- 验收范围：**全量 120 条盲测 · 双席位 · 双向交叉判分**。改写与判分席位均为 Claude Opus 5（`claude-opus-5` / firstParty）与 Grok 4.6（`grok-4.6-build`）。候选 `61062b89c06a`，基线 `d2d0ce2`。36 次调用（上限 40），有效 33 次。
- **两席位 L1 硬约束失败均为 0/120。** 8 批长文硬下限失败 0、目标下警告 0。
- SNF 误杀：Claude 2/57 = 3.5%、Grok 1/56 = 1.8%，均为不涉编造或受保护片段破坏的普通误杀。SF 风格通过 Claude 53/63、Grok 51/63；22 条 ⚠️ 全部是「清理不彻底 / 动作不完整」，零保真类失败。
- 发布门槛只判受影响面子集 36 条：门槛 1（子集内 L1 = 0）与门槛 2（子集内 SNF 误杀 < 10%，两席位均 0/7）达成；门槛 3 不适用（本版无新增或修订用例）；门槛 4 按席位报告，Claude 席位 SF 通过率较 v2.3.1 r4 低 9.3 个百分点，解释见结果页 §4——用例集 111→120、判官更换、单席位→双席位三个变量同时变化，且回退全部落在 ⚠️ 而非 ❌。
- 四条锚点：SF-39、SF-16、SF-37 两席位硬约束与风格双通过；SF-07 两席位硬约束通过（都没有把抽象关系具体化成实现声明），Grok 风格列 ⚠️。
- Grok 隔离修复（`--tools ''` + `--system-prompt-override`）首次实跑验证通过：16 次 Grok 调用全部通过 provenance 校验、零工具事件。
- `hard_metrics.py --human-stats`：10 篇全部通过 manifest、正文哈希、许可、年代、语言、作者组和 direct 场景检查，代表性门禁通过。
- `check_repo.py`：120 条用例、20 个场景样本、10 篇 HUMAN、24 个锚点、89 个链接和 3 组词表全部通过。42 项单测通过。
- 不迁移 v2.4.0 的实跑数据：references 改动使候选 ID 从 `9f83b9c456a4` 变为 `61062b89c06a`，旧验收数据按设计作废。
- `SKILL.md` 第 119 行 `实现了效率的提升 → 快了多少、省了几个人` 与 `operation-manual.md` 同源的一处，本版按范围不动，留给 v2.5.0 的规则收敛。

## [2.4.0] - 2026-08-29 — 技术术语按词义放行、FAQ 条件顺序

> 发布口径：本版是**收缩版**。原候选把七类改动打包，13 轮 remediation、54 次外部调用未通过任何一轮完整验收；2026-08-29 收缩为只保留直接回应 #5 的两条规则改动，其余移出留给 v2.5。验收范围是**受影响面 34 条，不是全量 120 条**，判分方式是逐条静态复核而非模型交叉判分。门槛 1、2 达成；**门槛 3（新增用例双模型达标）待维护者判定**——Grok 通过，Claude 两次运行中一次通过、一次漏清 SF-62 的一处包装。完整证据见 `evals/results-v2.4.0.md`。

### Changed

- No-touch 按词在句子里的具体技术含义或明确项目约定保护，不再因为文本是 README、发布说明或评测报告、或者相邻有命令和数字，就把周围的包装表达一起放行。被讨论的词、引用原文和没有附术语表的正常技术词仍然保留。回应 #5。
- `闭环` 拆成三个义项分别处理：表示工作完成时还原为完成了什么并保留完成范围，表示反馈流程时保留原有关系，`闭环反馈 / 闭环控制` 等实际技术用法保留。
- protected spans 区分逐字保护与含义保护：数值、名称、标识符、正式术语和引用原文按字面保留；状态、实验结果、条件与比较关系按含义保留，非正式叙述里的包装措辞仍可等义改写。
- FAQ 的“尽早给结论或动作”不得把原有执行前条件和警告挪到操作之后，真实的事后检查和失败分支也不改成前置步骤，不补原文没有的操作；结构调整仍受 scope 限制。这是规则澄清，旧规则小样未复现流程破坏。

### Added

- 9 条正反回归（2 SF + 7 SNF），benchmark 共 120 条（63 SF + 57 SNF）；另冻结 6 条不同领域的任务内侧测，不计入公开分母。
- 补登记 v2.3.1 r4/r5 评测索引，保留历史失败与未完成的第二模型判分。

### Verification status

- 双席位改写各 34 条：Claude Opus 5（`claude-opus-5` / firstParty）与 Grok 4.6（`grok-4.6-build`）。7 次调用全部有效、无重试；每次均校验实际模型、单轮、零工具、显式输入逐字一致、输出与持久会话一致。
- 两席位 L1 硬约束失败 0；硬判 34 条全解析，长文硬下限失败 0，protected spans 无漂移。
- SNF 误杀：Claude 0/23，Grok 1/23（SNF-28，v2.3.1 的 r4 与 r8 均记录过同一条，不是本版引入）。本版新增 7 条 SNF 两席位均零误杀。
- SF 两席位各 10/11。三处失败点完全互补，没有一条是两个模型同时失败：SF-61 Claude 通过 / Grok 警告，SF-62 Grok 通过 / Claude 波动，SNF-28 Claude 通过 / Grok 误杀。
- SF-62 是 #5 的原始素材：Claude 第一次漏清「判分仅闭环」，第二次在完全相同的冻结输入下两处包装均清除。两次事实层都完整，属执行波动而非稳定失败，两次结果都记录在案。
- 未跑全量 120 条，不据此声称全量无回归。

### Notes

- 本版范围已于 2026-08-29 收缩：抽象主张保留、否定范围保护、主动出击腔交付保留、scope 拆句边界，以及 `examples.md` / `positive-style.md` / `structures.md` / `operation-manual.md` 的示例重写移出本版，留给 v2.5 单独验收。原因与旧候选实跑记录见 `evals/run-manifest.md`。
- 由此，旧候选复核出的 SF-07 抽象关系丢失、SF-39 否定关系漂移，以及 r8 实测的 SF-16 决定因素降级、SF-37 条件式下一步被换成新前置要求，本版都不修复，继续作为已知问题记录；它们在 v2.3.1 已经存在，不是本版引入。
- `dist/shuorenhua-mini.md` 未修改，不宣传其包含本版规则澄清。

### Fixed

- `check_repo.py` 把 HUMAN 代表性门禁（direct 场景缺 docs/status，语料收集中）从失败降为**已知缺口**：照常打印 `⚠️ [known-gap/...]`，不再以退出码 1 阻塞 CI。该通道仅此一处、语料收齐后随门禁通过一并移除；其余任何检查失败仍返回退出码 1。修复 v2.3.1 发布提交（`b779335`）在 GitHub Actions 上的红叉。

## [2.3.1] - 2026-08-21 — mini 分发、Scene Packs、HUMAN 对照与全量基线刷新

> 发布口径（维护者 2026-08-21 决定）：以 **Opus 单席位**收口。r4 Opus 侧全量达门槛（硬约束失败 0、SNF 误杀 0/50、SF 57/61）；DeepSeek 撤出正式席位（真实 L1 B-74 + run-to-run 方差）；Grok 4.6 换席补跑的改写与硬判干净、判分仅 1/7 批闭环（评测通道不稳定），作为辅助证据记录，完整第二席位补跑留给后续版本。详见 `evals/results-v2.3.1.md`。

### Added

- 新增 1,500 字符以内的自包含 `dist/shuorenhua-mini.md`，并把安装口径统一为 mini / lite / full 三档。
- 新增 API reference、FAQ 等 Scene Packs；benchmark 扩到 **111 条（61 SF + 50 SNF）**，盲测输入、映射、批次和计数锚点同步。
- 新增 8 篇 HUMAN 长文 residual 对照：5 篇现代公开文本、3 篇历史原作，其中 2 篇明确标为英译中。逐篇保留固定 revision、归属、CC BY 2.5 / CC BY-SA 4.0、固定版权政策证据、抽取说明和 AI 来源依据；正文及其改编不适用根目录 MIT。

### Changed

- `hard_metrics.py` 增加 HUMAN manifest、长度/句数/SHA256、目录双向对账、许可/许可证据、固定 revision/UTC 时间、AI 依据、作者组/时代/原始语言分层与分布报告；历史/现代各至少 3 篇，翻译稿不超过三分之一。场景代表性只统计 direct，proxy 只作 report-only 假阳性参照，不进 benchmark 分母。
- 保真回读改为按子句/事实要素建账并做双向核对，显式保护范围、条件、否定、情态、完成态、方向和强度；避免清理整行姿态时顺带删条件，也避免把“潜力/可能”补成已实现关系。
- 新增固定 MediaWiki wikitext 抽取器与单测，避免旧 revision 在渲染时混入当前模板内容。
- `check_repo.py` 增加 HUMAN 发布检查和 plugin / marketplace 元数据结构、版本一致性检查。

### Fixed

- 修复 `references/structures.md` §20（标点腔）的计数单位自相矛盾：原「检测」子句按破折号**符号**数计数（「单段两处以上 `——`」），「保留条件」按插入语**组**数计数（「全段仅一处」），中文成对插入语（`……——插入——……`，两个符号构成一处）对两个子句给出相反判定。三个模型在同一用例（SNF-34 / B-15）上按不同子句判定产生分歧，证明这是规则文本缺陷而非模型幻觉。现统一为按**插入处**计数，并补成对插入的放行示例。Opus r4 对该用例的行为（放行）在修复前后同为正确，全量基线不受影响，无需重跑。

### Tested

- `python3 automation/check_repo.py`：结构计数为 **111 用例 / 20 样本 / HUMAN 8 篇 / 24 锚点 / 98 链接 / 3 词表**；预期退出 1，HUMAN direct 场景仍缺 `docs` 和 `status`——维护者决定如实记录、随版发布，继续收集，收齐后关闭门禁。
- HUMAN：8 篇均达到 1,000 汉字 / 12 句门槛；3 篇历史 + 5 篇现代，6 篇中文原作 + 2 篇英译中，7 个作者组。句长 CV 与连词密度按总体、场景、长度桶输出；小样本没有稳定同场景分离证据，不设新阈值。
- L1 修复侧测：先冻结 14 条非近邻 held-out，再由 first-party Opus 5 与 Grok 4.6 独立执行，28/28 无 L1；纯姿态 4/4 被清理，no-op 4/4 放行。两个历史失败题的 targeted 复跑为 4/4 保真通过，但不覆盖旧全量失败，也不替代完整新全量基线。
- targeted：Opus mini 6/6；Scene Pack 7 通过 / 1 个 L2 警告 / 0 L1，新增 SNF 误杀 0/4。DeepSeek Scene Pack 同为 7/1/0；B-26 的“没有先直接回答”在多模型上复现，保留为 L2。
- 全量（新规则 r4）：Opus 与 DeepSeek 改写均 111/111，双向 judge 14/14 批全部闭环；长文硬下限失败 0。Opus 侧：SF 通过 57/61（余 4 条 L2 警告）、硬约束失败 0、SNF 误杀 0/50。DeepSeek 侧：SF 通过 48/61、硬约束失败 2、SNF 误杀 2/50。
- 旧两条 L1 修复验证：B-39 的“高峰期流量”适用条件与 B-95 的 potential 抽象层级在 r4 全量中两模型均通过，与 held-out 28/28 一致。
- r5 换席补跑（Grok 4.6，辅助证据）：改写 7/7 批 111/111、L0 干净；`hard_metrics.py --run` 长文硬下限失败 0、目标下警告 0，保护片段报警仅 1 条（B-77 整条删除所致）；Opus judge 的 B-65–80 批闭环：硬约束失败 0、SNF 误杀 0/6、SF 风格通过 7/10（⚠️ 3）。其余 6 批 judge 因评测通道不稳定（Opus judge worker 并发异常终止）未产出；维护者 2026-08-21 决定收敛，不再重试。
- 复核更正：原判 B-57 / SNF-49 的硬约束失败不成立，降为 L0 回显不完整；B-15 / SNF-34 的失败归因从「DeepSeek 单方规则应用缺陷」更正为「规则缺陷导致的判定分歧」（即上文 Fixed 项）。

### 席位决定（维护者 2026-08-20 / 08-21）

- DeepSeek V4 Pro 撤出正式席位，r4 成绩原样保留为辅助证据。依据（主线程复核后口径）：B-74 / SF-08 把“一个目标”替换成“这个产品”，指代对象漂移，预期逐字禁止该动作，为真实 L1；B-33 / SF-38 主病灶词「掰扯清楚」未清（真实 SF ❌）；受控诊断（两次同条件独立复跑，不进正式分母）显示**同条件两次运行输出不同**——B-33 为 2/3 失败且出现单次推理内自相矛盾，B-74 为 1/3 失败。单次全量结果不可复现，对要求 L1=0 的正式基线属结构性问题，且独立于 B-15 的规则缺陷。Opus 同用例全过。
- Grok 4.6 补跑第二席位（r5）：改写与硬判完整且干净，判分仅 1/7 批闭环，不作为发布门槛席位。
- Codex 5.6 Sol 因额度耗尽记“未参与”，未用其他 Codex 模型替代。
- mini 6 条：Opus 侧 r3 6/6 有效沿用；DeepSeek 侧 3/6 格式失败随撤席不再补跑。

## [2.3.0] - 2026-08-14 — 篇章级病灶 + 项目规则优先级 + 抒情词与量化保真

> 原规划的 v2.3.0 与 v2.4.0 合并为一个对外版本 v2.3.0。

### Fixed

- 修复 benchmark 总数跨过 100 后的盲测编号格式失配。`make_blind.py` 原先按总数位数扩宽，103 条会把全部编号改成 `B-001…B-103`；`hard_metrics.py` 与历史批次名仍按 `B-01…B-99, B-100…` 解析，导致正常批次运行把 B-01–B-99 全部报成缺输出。95 条评测集阶段两处格式恰好同为两位，扩到 103 条时才暴露。生成器现固定以两位为最小宽度，跨 100 后自然扩位；`B65-103` 实测期望 39 条、生成物 39 条、缺失 0、多出 0，另用 B33-48 完整批次实跑 `hard_metrics.py`，16 条全部解析、无缺输出。
- `check_repo` 目前不检查 `make_blind.py` 与 `hard_metrics.py` 的跨文件编号格式契约，本版只记录为后续检查缺口，不继续扩范围。

### Added

- `SKILL.md` 的 No-touch 规则明确：用户当前要求与项目 style guide / 术语表优先于通用规则，项目正式术语和稳定团队表达不能仅因命中词表被改写。
- `references/phrases-zh.md` 补 `洞察 / 赛道 / 协同 / 卡点 / 联动` 5 个代表词及逐条误杀边界；`赛道` 只补单词条，不改 v2.3.0 的借喻场判据。Tier 2 新增 12 个抒情词代表项，按同段密度、搭配对象与文学场景判断，实体描写和用户明确要求的抒情语体放行。
- `hard_metrics.py` residual 层新增 `「」/『』` 高亮短语候选计数，只报数、不判死、不影响退出码。103 条实测中 SF / SNF 的中位数与 p90 都是 0、max 都是 3：SF-55 是自造高亮，SNF-44 是人物对白，原始计数不可分，故不照抄上游「一篇 3 处以上」、不设阈值。
- 保真合同新增量化歧义边界，`operation-manual.md` 增加 §15 五段式操作协议。改写侧默认不替原文选择数量关系；`docs / status` 走 `audit-only`，`chat / public-writing` 只有在量化说法不承担关键信息时才允许压缩，任何情况下不得补基数、年份、期限或测量结果。
- benchmark 扩到 **103 条（57 SF + 46 SNF）**：新增 SF-54–57、SNF-43–46，覆盖新补词、项目术语覆盖、抒情词抽象 / 实体对照组、量化歧义的 public-writing / docs 动作，以及正确百分点、百分比、单位与基数的数字防误杀。盲测输入、映射表、README、run-eval 分母、批次表与计数锚点同步。

### Tested

- `python3 automation/check_repo.py` 通过：**103 用例 / 20 样本 / 24 锚点 / 94 链接 / 3 词表**；盲测生成物 103 条同步。
- `python3 automation/eval/hard_metrics.py --calibrate` 实跑：高亮短语候选 SF max 3 / SNF max 3，两组中位数与 p90 均为 0，负结论已同步到脚本 docstring 与运行说明。
- 静态误杀扫描：5 个新补词在 SNF 46 条中零命中；量化歧义模式在 SNF 46 条中零命中；抒情词只命中设计好的实体 / 小说对照组 SNF-44。
- `python3 -m py_compile automation/check_repo.py automation/eval/hard_metrics.py automation/eval/make_blind.py` 与 `git diff --check` 均通过。
- **targeted 跨模型盲测（新增 8 条）**：Codex CLI `gpt-5.6-sol` 与 Claude Code `--model opus` 独立盲改写、双向交叉判分。两组均为 L1 硬失败 0、SNF 误杀 0/4、无 `❌`；Codex 输出 SF 2/4 `✅` + 2/4 `⚠️`，Claude 输出 SF 1/4 `✅` + 3/4 `⚠️`。SF-55 两模型都清掉目标抒情词和自造高亮，但仍有较淡的抽象隐喻，作为 L2 已知弱点记录；SF-56 的保守 audit-only 路径是 benchmark 明写的 `⚠️`，均未擅自推导新比例。
- **第一阶段新增 11 条影响面回归**：两组均为 L1 硬失败 0、SNF 误杀 0/5、无 `❌`；Codex 输出 SF 6/6，Claude 输出 SF 5/6，唯一 `⚠️` 仍为已知的 SF-52 借喻清理不彻底，没有发现合并批次的新规则引入回归。
- **数字准入与 annotation mode 自检**：SNF-45 / SNF-46 两模型整体放行，4/4 与 5/5 protected spans 全部逐字保留；Codex / Claude 对新增词条和抒情词规则段的自检均为建议改写项 0。完整结果见 `evals/results-v2.3.0.md` §9–§10，运行元数据见 `evals/run-manifest.md`。

### 第一阶段：篇章级病灶 + residual 统计层 + 标点腔长文覆盖

这一阶段原本计划单独发布，后来与上面的项目规则、词表和量化保真任务一起收进 v2.3.0。下面保留详细改动和当时的验证记录。

对标 [KKKKhazix/human-writing](https://github.com/KKKKhazix/human-writing)（生成侧中文写作 skill）后做的一轮吸收。它管「写」、本仓库管「改」，两边的病灶清单只有部分重叠；本版补的是它覆盖到而本仓库零命中的篇章级病灶，以及一处被对比照出来的内部规则冲突。它的一刀切禁令（禁冒号、禁破折号）和单级严重度未采纳——那套只服务创作场景，套到 `docs` / `release-note` / `code-context` 会崩。

#### Fixed

- **`references/severity.md` Tier 3 的默认处理与 `SKILL.md` 自相矛盾**。Tier 3 原本写「用同义词替换部分出现」，而 `SKILL.md` Core stance 明写「不用机械同义词替换表」。更要紧的是这个动作本身会引入新的 AI 味：`重要 → 关键 → 核心` 的换词轮换正是模型腔的来源之一（人写东西不怕重复关键词，模型才逐次换近义词）。等于规则库里有一条默认动作在教模型加重 AI 味。改为「删掉多余的那几次，或把其中一部分换成具体信息」，并在决策流程图同步。

#### Added

- `references/structures.md` 新增 5 条反模式，均为改动前全库 grep 零命中的缺口：
  - **21 动词名词化**：`进行了优化 / 实现了效率的提升 / 完成了对 X 的梳理 / 起到了 X 作用`。中文 AI 味的高频病灶，此前 `structures.md` 20 条与两张短语表都没有覆盖。
  - **22 同义词躲避**：同一对象在相邻几句里逐次升格换词（`修表 → 这门手艺 → 这项技能`）。这一条同时反向约束改写动作本身，与上面 Tier 3 的修复互为引用。
  - **23 连词过密**：**按实测数据限定了适用范围**，只在 `public-writing` 叙事文本上判，`docs / status / code-context` 不判，且不设全局密度阈值（理由见下方 Tested）。
  - **24 装饰性细节**：无来源且不改变后文的时间、天气、神态、物件。判据是两条同时成立，与第 16 条「假口语化」区分（那条抓硬塞流行语，这条抓伪造生活细节）。
  - **25 借喻场混用**：短距离内混用 3 套以上比喻系统（道路 / 战争 / 建筑 / 温度 / 仓储 / 海洋 / 机器）。
- `references/structures.md` 第 1 条补跨句与换字变体：`不是 A。而是 B`、`与其说 A，毋宁说 B`、`你以为 A，其实 B`、`回头才发现`、`大家都说 A，可真相是 B`、`答案恰恰相反`。**只补变体清单，判据和豁免口径不变**，仍走本条既有的密度阈值与豁免上限。
- `references/operation-manual.md` 新增 §10–§14（名词化 / 同义词躲避 / 连词过密 / 装饰性细节 / 借喻场混用），各含 `识别信号` / `默认动作` / `in-place 替代动作` / `保留条件` / `回读检查`；§11 的回读检查含一条针对 Tier 3 的反向自查。
- `references/operation-manual.md` 补三个操作化诊断手法：「Scope 与删除清单」补**压缩试验**（假设删掉三分之一，信息几乎不变即为注水，用来校准清单长度，不替代逐条判据）；§2 补**结尾删除测试**；§9 补**「换一个模型也能原样写出来」**的快速定位问句。
- `automation/eval/hard_metrics.py` 新增 residual 统计层与两个 CLI 模式：
  - `--residual FILE`：算句长变异系数、连词密度、名词化命中、借喻场数。全部只报数不判死，不影响退出码。
  - `--calibrate`：在 `evals/benchmark.md` 的 SF（该改）/ SNF（不该改）两组语料上跑分布，用于实测定阈值。B-xx 盲测副本已排除，避免同一文本重复计入。
  - 借喻场判据内置字面用法排除表（`搜索引擎` / `代码仓库` / `商品库存` 等不计），误伤防护优先。
  - 移植 `mask_non_prose()`：用等长空格屏蔽代码块、行内代码、链接目标、URL 和 HTML 标签，保留字符偏移与换行，行号和窗口距离才算得准。
- `references/phrases-zh.md` / `phrases-en.md` 顶部各加元规则：**清单是举例不是边界，管的是修辞动作不是字面**。换一套字继续做同一个动作仍算命中；反过来，列表里的词在当前句子承担实义时按误杀防护放行。
- `SKILL.md` 单文件 fallback 补两条（名词化还原、同义词躲避），Core stance 的「不用机械同义词替换表」补明「也不要为了躲重复而轮换同义词」。其余三条新病灶靠 `references/` 生效，不进 fallback，避免入口继续膨胀。
- `SKILL.md` 的 `annotation mode` 新增 `材料不足` 问题族，`references/examples.md` 配一组示例（示例 C，原示例 C 顺延为 D）。这是对标 human-writing「材料门槛」的**轻量替代出口**：它那套「开稿前先清点五件具体材料，不够就查、就问、就写短」属于生成侧，收进来会把本 skill 从改写侧拉走，因此本体不吸收；这里只保留一个判定出口——文本的问题是「没东西可写」而不是「话说得不对」时，能标出来。判据挂在本版新增的压缩试验上，边界写死三条：`建议动作` 只说删完还剩什么、缺哪一类材料，不替作者设计怎么去补；`材料不足` 不等于「不用改」，该清的姿态照常清，只是要同时说明改完会短很多；这个判断只在 `annotation mode` 出，默认改写模式仍然只交改写结果，不评价作者手里有没有东西可写。
- `automation/check_repo.py` 新增 `rule-tables` 检查：`hard_metrics.py` 的词表与 `references/structures.md` 正文对账。本版把借喻七场和名词化空动词硬编码进了脚本，同一判据从此有两处独立维护的清单，改一边忘另一边会静默漂移，而既有的四项检查（计数 / 链接 / 用例编号 / 元数据）都覆盖不到。**按正文的语义分级对账**：正文明说是完整枚举的双向核对（第 25 条「常见 N 套」↔ `METAPHOR_FIELDS`，含数量词与实际套数的一致性；第 21 条空动词 ↔ `NOMINALIZATION_PATTERNS` 的起手动词），正文按「清单是举例不是边界」写的只单向核对（第 23 条 ↔ `CONJUNCTIONS_ZH`，只要求正文列到的词脚本里有，不反向要求穷举）。分级是必要的——两张短语表的元规则刚写明清单是举例，检查若一律双向就会和它打架。

- `evals/benchmark.md` 扩到 **95 条（53 SF + 42 SNF）**，本节先列钉住第 21–25 条的 9 条，其中两对是对照组（标点腔长文的另 2 条见下一节）：
  - 新增 SF：`SF-48` 名词化（status）、`SF-49` 同义词躲避、`SF-50` 连词过密、`SF-51` 装饰性细节、`SF-52` 借喻场混用。
  - 新增 SNF：`SNF-38` 亲历叙事里的琐碎细节（long，SF-51 的对照组）、`SNF-39` 承担逻辑的连词密度（docs，SF-50 的对照组）、`SNF-40` 稳定术语里的名词结构、`SNF-41` 借喻词的字面用法与行业术语。
  - `评测标准` 新增「篇章级病灶」判分口径；覆盖矩阵、盲测生成物、各处计数锚点同步。
- `automation/eval/hard_metrics.py` 的连词表补条件连词 `如果` / `否则`（`if/then/otherwise` 的搬运重灾区）；单字 `则` 不收，`规则 / 准则 / 原则` 的误伤面太大。

**标点腔长文覆盖（原 v2.1.1 欠账）**

- `evals/benchmark.md` 新增 M 章节与第三对对照组：`SF-53`（`public-writing / long / bounded`，7 处破折号跨 4 段 + 2 句整句空话）与 `SNF-42`（文学摘录里承担刻意文体的破折号，6 处跨 4 段）。此前标点腔只有 short 覆盖（SF-43 / SNF-34），长文里破折号与 `bounded` 删除清单怎么交互没有钉住。SF-53 要求**两类动作分开走**：破折号是句内动作、句内改、不进删除清单；整句空话照常进清单。SNF-42 钉住判据顺序——**先查保留条件、再算密度**，引用体裁与刻意文体即使密度超标也放行。
- `references/scene-guardrails.md` 长文小节补一条：标点腔是句内动作，不进「建议删除（待确认）」清单，同段整句空话仍照常进清单，两类动作不因同段共现就混成一种处理。（`operation-manual.md` 不动——2026-07-07 已钉死 bounded 与场景的交互口径单源在 scene-guardrails。）
- `evals/real-samples.md` 新增 `RS-20`（工具推荐长帖，标点腔 + 装坦诚混合病灶，按四维评分），样本集 19 → 20 条。改法说明记了一条边界：价值拔高收尾换成有信息的适用边界，而不是直接删空——原文末段承担「给读者一个判断」的功能。
- `evals/benchmark.md` 评测标准新增「标点腔长文」判分口径。

#### Tested

- `python3 automation/check_repo.py` 通过：**95 用例 / 20 样本 / 24 锚点 / 94 链接 / 3 词表**（改动前 84 / 19 / 24 / 81，无词表检查）。`make_blind.py` 已重跑，盲测生成物 95 条同步。
- **`rule-tables` 做了反向验证**，五类漂移逐个注入后跑检查，全部抓到：正文加一套借喻场但脚本没同步、正文加场并改了数字但脚本没同步（数量词与实际套数各报一条）、正文改名词化空动词、正文补一个脚本没有的连词、脚本侧改场名而正文没同步。文档→脚本与脚本→文档两个方向都验过，注入的改动跑完即还原。第一轮实跑还真抓到一处自身缺陷：空动词抽取把 `实现了?` / `完成了?对` 里的可选量词「了」当成了动词的一部分，已修。
- **`rule-tables` 经外部模型 review 后又做了一轮加固**（DeepSeek V4 Flash，通过 Codex worker 跑）。它提的主要问题是 `importlib` 的字节码缓存可能让「同秒 + 同字节数」的脚本改动漏报。本机 Python 3.14 实测复现不了——连 `os.utime` 强行把源文件 mtime 与大小回设到与 pyc 记录完全一致，改动仍被抓到，说明这里走的是 hash-based 判定。但 pyc 的失效判定本就依赖解释器版本与构建配置（timestamp-based 只看秒级 mtime + 文件大小），**一个防漂移的检查不该把正确性押在 CI 那边的缓存策略上**，因此仍按建议改成直接 `compile` + `exec` 源码，绕开缓存。同时采纳另两条：加载失败改为附带 `traceback` 尾部（语法错误给出错行与 `SyntaxError` 说明，运行期异常给文件与行号，均已实测）；第 21 条的对账范围写进注释：只比对起手动词，不含动名词宾语，因为正文把宾语按举例列、脚本侧是穷举，口径不同，强行对账只会误报。未采纳它关于把 `是否建议改写` 改成 `是（有界）` 的建议：那会破坏该字段既有的 `是 / 否` 枚举；它据以立论的「示例 C 同时给了改写稿」其实是 `examples.md` 全章节的固定体例（A / B / D 各例都有这一栏），而「不要一边说只标问题一边偷偷输出重写版」在 `annotation mode` 的既有约束里已经写死。
- 修 `check_repo.py` 三处锚点脆弱写法：①`an (\d+)-case benchmark` 写死了冠词，95 的英文冠词是 `a`，改为 `\ban? (\d+)-case`；②`^### RS-(19)\b` 硬编码了样本编号，随 RS-20 更新为 20；③`v1\.8\.5 扩到 (\d+) 条。` 绑死在某个历史版本上，改为贪婪匹配最后一个「扩到 N 条。」，以后扩样本只改正文不用动正则。
- **residual 阈值标定结果为负，如实记录，不硬凑阈值**（`--calibrate`，SF 53 / SNF 42）：
  - **句长变异系数：标不了。** 够 12 句的样本 SF 仅 2 条、SNF 零条。标定它需要「人写长文」对照组，本仓库一篇都没有——`real-samples.md` 的 5 条 long 全是 AI 味样本，没有反例。判据保留在脚本里，不设阈值，缺口留给后续版本。
  - **连词密度：全局判据被实测否掉，不设阈值。** SNF 中位 5.26 / 千字高于 SF 的 0.00，且 **SNF max 81.08 高于 SF max 80.00——不该改的比该改的密度还高**。新增的 SF-50 / SNF-39 就是为这件事做的同密度对照对：同样 80 上下的密度，`public-writing` 叙事该删一半，`docs` 迁移说明一个都不能删。照抄外部「每千字 7 个」的阈值会优先误伤不该改的文本，故第 23 条定为场景限定 + 看分布不看总量。
  - **名词化 / 借喻场：区分度好，SNF 侧零误报。** 名词化 SF max 4（SF-48）、SNF max 0；借喻场 SF max 5（SF-52）、SNF max 1——SNF-41 的三套名义命中被字面用法排除表滤成一套（`代码仓库` / `搜索引擎` 正确放行），规则侧与脚本侧行为一致。
- **静态误杀检查：SNF 42 条对新增判据零命中**（名词化 max 0、借喻场 max 1 且未达 3 套报警线）。
- 覆盖度交叉验证：补用例前，`benchmark.md` 84 条仅 1 条命中名词化（SF-32），而 `real-samples.md` 19 条命中 4 条（RS-01 / RS-02 / RS-08 / RS-15），命中率 1.2% vs 21%，证实是 benchmark 对篇章级病灶覆盖不足而非判据无效；本版补的 9 条正是填这个缺口。
- 既有功能回归：`--pair`、`--stdin`、`--run` 参数与退出码语义未改动，`--pair` 抽测正常。
- **targeted 跨模型盲测（新增 11 条）**：三条独立路径——Codex CLI `gpt-5.6-sol`、Claude Opus 5、Agent SDK `gpt-5.6-sol[1m]`——互相交叉判分，共四组判分。全部硬约束失败 0、SNF 误杀 0/5，三对对照组（连词 / 装饰性细节 / 标点腔长文）在所有路径下一致判对，无 ❌。
- **SF-52 由跨模型对比得出明确结论**：Claude 改写 SF **6/6**，五套借喻全部还原本义；Codex 与 SDK 均 5/6，⚠️ 都落在 SF-52（`技术壁垒` 未还原、`点燃斗志` 只换成 `重振士气`）。这说明 `structures.md` 第 25 条的默认动作**可达成**，⚠️ 是模型执行不彻底而非规则过严。因此不改 benchmark 预期、不加单用例例外。
- **影响面回归 6 条**：全库 84 条既有用例脚本扫描只有 SF-32 命中新判据；另按风险选 SNF-26 / 11 / 12（具体经历与时间细节）和 SNF-29 / 30（long/in-place）。三组判分均为硬约束失败 0、SF 1/1、SNF 误杀 0/5，无 ⚠️ / ❌。
- 修 `hard_metrics.py` 一处报告措辞缺陷（Claude judge 判分时发现）：所有 `is_long` 且非 `in-place` 的用例被统一打印成「bounded 长文不适用留存率判据」，但这一支同时包含 bounded 用例与 no-op 判定用例（如 SNF-38），措辞会让 judge 误以为用例被判成 bounded。改为按实际场景标签直述。判定逻辑未变，不影响任何已有结论。
- 完整结果见 `evals/results-v2.3.0.md`，运行元数据与时间线见 `evals/run-manifest.md`。
- plugin / marketplace 版本元数据同步为 `2.3.0`。

## [2.2.1] - 2026-08-06 — 句式骨架密度判据

### Added
- `references/structures.md` 第 1 条「二元对比假戏剧」补齐 `检测` / `默认动作` / `保留条件` 三节，体例对齐第 20 条（破折号腔）。此前该条只有单句正反例，没有任何密度判据，跨段分布的同型骨架规则管不到——`evals/benchmark-tiers.md` 记录的 SF-40 降 L3 理由「操作手册只约束同段连续叠加」就是这个缺口的历史证据。
  - 长度归一阈值：< 300 字/词 2 处以上；300–1000 字/词 3 处以上；> 1000 字/词 平均每 300 字/词 1 处以上。计数口径明确为中文按字、英文按词、代码片段 / 路径 / 命令 / 版本号各计 1、标点空白不计（同 `severity.md` 体例）。
  - 变体计入：`不像 A，像 B`、`要的是 X，不是 Y`、`X 不行，Y 才行`，以及连续多条以否定收尾的列表项或表格行。
  - 豁免先剔除再计数，上限 2 处（术语定义 1 处 + 论证骨架 1 处）；超过 2 处都声称承担论证时不再逐条豁免。论证骨架的判据是「前半句是读者会真实持有的误解，且删掉后后文数据/结论/动作失去依据」，不是「读起来气势弱一点」。
  - 明确「只把 `不是 X，是 Y` 倒装成 `Y，不是 X` 不算完成降密度」。
- `evals/benchmark.md` 新增 `SF-47`（docs / long，同型骨架跨段密集，每句都带信息）与 `SNF-37`（docs / long，2 处对比未达阈值的下边界），评测集从 82 条扩为 84 条（47 SF + 37 SNF）；盲测输入和映射表已用固定种子重新生成。
- `evals/benchmark.md` 评测标准新增「句式骨架密度」样本口径。
- 新增 `evals/results-v2.2.1.md`，归档四轮 targeted 双模型盲测，含一次由本版改动引入、当轮发现并修复的回归。

### Changed
- `SKILL.md` Pass 2 第 5 项从「句长过匀」改为「节奏过匀」，补回 `positive-style.md` §2.3 和 `operation-manual.md` §9 早已写明、但漏抄进合同的「同抬手、同落点」，并纳入同型句式骨架密度。`SKILL.md` 是行为合同单源，此前模型实跑只按「句长」查，长短句交替的文本直接过关。
- `SKILL.md` Pass 2 轻量修正清单补一条对应动作：同型骨架超阈值时只改超出的那几处，换成中性连接或直接陈述。
- `references/structures.md` 第 18 条从「句长均匀」扩为「节奏单调」，分列句长均匀与句式骨架重复两个子信号；句长标准差数据（1.2 / 4.7+）原样保留。
- `references/operation-manual.md` §1 与 §7 的保留条件从只约束「同一段连续叠加」扩为同段 + 跨段全文密度两档，并引用第 1 条阈值；§9 残留清单同步改为「节奏过匀」，轻量修正与保留条件各补一条。
- `references/positive-style.md` §2.3 补句式骨架维度。
- `evals/run-eval.md` judge 口径三处「句长过匀」同步为「节奏过匀（句长 + 同型句式骨架密度）」；SF / SNF 分母改为 47 / 37。
- README、`evals/real-samples.md`、`automation/eval/README.md` 批次表同步到 84 条。

### Tested
- targeted 双模型盲测四轮（B-12 = SF-47、B-38 = SNF-37），Codex 侧走 `codex exec --sandbox read-only`，Claude 侧因宿主托管凭证不共享给 shell 子进程（非账号未登录）改用同模型冷启动 subagent，同样只给 `SKILL.md` / `references/` / `benchmark-blind.md`，不给预期。
- r2（阈值已加、豁免未剔除）：双侧均识别密度超标并降密度；Claude 改 2 处 ✅，Codex 改 3 处但抹平了一处豁免项，记 ⚠️。交叉判分 L1 失败 0、SNF 误杀 0。Claude 侧 judge 指出阈值与「保留 1–2 处」自相矛盾——短文里保留 2 处会被同一条规则再次判超标。
- r3（加「豁免先剔除」后）：**出现回归**，双侧对 SF-47 全部判 no-op。原因是「对比本身是论证骨架」缺可判定边界，任何带信息的对比都能套；且本版曾把 SF-40 的用例级例外「作者刻意用对比承载全文论点」误提升为通用豁免口。
- r4（豁免加上限 2 + 论证骨架加可判定判据 + 删除越界的通用豁免口）：回归修复。Claude 改满 2 处非豁免且未用倒装充数 ✅；Codex 改 1 处、留 1 处，记 ⚠️（L2，不阻塞）。双侧 SNF-37 均 no-op，0 误杀。
- L1 硬约束四轮全部 0 失败：`retry-guard`、`3 次`×3、`27 次`、`2026-04`、`9 倍` 与 SNF-37 的 19 项命令 / 权限 / 字段 / 阈值逐字保真。`hard_metrics.py --pair` 粗核：SF-47 7/7、SNF-37 19/19，破折号 0 处。
- SF-40 维持 L3 不变。本版只补通用规则，未移动任何用例层级（`benchmark-tiers.md` 防放水约束）。
- 影响面回归 7 条（B-12 / B-15 / B-25 / B-53 / B-54 / B-63 / B-79）双模型双向交叉：L1 硬失败 0，**SNF 误杀 0/2**。选样非抽样——全库 84 条扫描后确认 15 条含二元对比骨架、其中 7 条按新阈值行为会改变，其余 69 条对新规则是 no-op，因此未跑全量。
- 回归重点 SNF-29 / SNF-30（in-place 长文误杀防护）在新判据下均「名义命中」阈值，双侧四次运行全部 no-op，正文逐字 100% 保留；豁免上限未把节奏性重复与正常转场推进改写。
- 遗留观察：密度判据给了模型一个合法的停手点（SF-39 改到阈值之下即停，留下预期点名的另两处骨架）。本版不动，避免围着单个用例长例外。
- `python3 automation/eval/make_blind.py`、`python3 automation/check_repo.py` 通过（84 用例 / 19 样本 / 24 锚点 / 81 链接）。

## [2.2.0] - 2026-08-03 — eval harness 脚本硬判

### Added
- 新增 `automation/eval/hard_metrics.py`：零依赖硬判脚本（纯 Python 标准库），输入改写前后文本，输出三项硬指标：
  - 字数留存率：替掉人工 `wc -m` 步骤，只对 `public-writing / long / in-place` 用例判定，目标 ≥ 0.90、硬下限 0.85，低于硬下限按 run-eval.md 口径记硬约束失败；bounded 长文与 no-op（保留原文）用例不适用留存率判据。
  - 破折号密度：每段 `——` 计数 + 输出首句是否仍以 `——` 起手，命中 SF-43 破折号过密信号时报警。
  - protected spans 粗核：数字、版本号、路径、反引号片段、代码标识符等在输出中是否逐字存在；缺失只报警不判死，留给 judge 复核。
- `--run <dir>` 批量扫批次目录（自动区分 `codex/` / `claude/` 子目录并配对 `evals/benchmark-blind.md` 原文），输出 `hard-metrics.md` 报告和 `hard-metrics.json`；`--pair` / `--stdin` 支持单条对照，`--report-json` 供 judge 输入拼接。

### Changed
- `automation/eval/judge-prompt.md`：长文留存等硬指标改为「运行者提供 hard_metrics 报告数字」，judge 不再自己数，也不再估算；补充三项硬指标的口径说明（bounded / no-op 例外、破折号信号、粗核报警不判死）。
- `automation/eval/README.md`：新增「硬判」一节（运行命令、口径、产物、单条用法），文件约定表登记硬判脚本；移除 v2.2.0 硬判脚本相关的未来时态表述。

### Tested
- `--run tasks/current/eval-runs/2026-07-23-v2.1.0-final-full-41da53f/`：10 个批次（codex/claude 各 5）全部解析，无缺输出，退出码 0；`--run tasks/current/eval-runs/2026-07-05-v1.9.2-targeted/` 旧口径（SF/SNF 编号）5 条回放成功，退出码 0。
- 8 个长文用例（B-02 / B-19 / B-44 / B-68 × codex/claude）字数留存率与手工记录 `long-form-retention.txt` 逐条一致，零冲突：
  - 实际改写（B-19 / B-68）：codex 322/339=95.0%、403/416=96.9%；claude 320/339=94.4%、413/416=99.3%。
  - 保留原文（B-02 codex、B-44 两侧、B-02 claude）：按 no-op 口径不判留存率；其中正文附原文的按 100% 记（包装字如「处理结果：/保持原文：」不计入分子），claude B-02 只输出说明文字、靠判定链「力度=no-op」证据放行，并保留 80/231 供 judge 复核。
- 第二视角评审 P1 项已全部修复并复测：整篇 blockquote 输出（`> ## B-xx` + `> 处理结果：`）解析成功；中文紧贴数字/单位（`耗时20ms`、`共20人`、`版本v1.8.0`）正确命中，版本号先剥避免幽灵片段；假 no-op（声明保留原文但正文未附原文、无判定链证据）标 `noop_unverified` 并按实际留存率判 fail；`--pair` / `--stdin` 自动剥标题与「处理结果：」前缀，`--scene` 支持长文判据。
- 失败语义实测：路径不存在、无参调用、单条缺文件均退出码 2，不会静默通过。
- `python3 automation/check_repo.py` 通过。

## [2.1.0] - 2026-07-23 — 清完变泛 / README 使用入口

### Added
- `references/positive-style.md` 新增「清理后的落点」合同：有具体信息时必须落回原文；没有具体口径时允许变短，但不补事实、不用更泛的空话填空。
- `references/protected-spans.md` 增加时间范围与时间跨度保护，避免 `over the next decade` 等表达被改窄、改宽或模糊化。
- `references/operation-manual.md` 为二元对比和价值拔高补清理后泛化检查。
- `evals/benchmark.md` 新增 `SF-46` / `SNF-36`，评测集从 80 条扩为 82 条（46 SF + 36 SNF）；盲测输入和映射表已用固定种子重新生成。
- 新增 `evals/results-v2.1.0.md`，归档全量盲测、核心 targeted、多模型诊断和已知边界。
- README 增加 `npx skills add MrGeDiao/shuorenhua` 安装入口、检索关键词和现有能力模式地图。
- 新增 `evals/benchmark-tiers.md`：用例分层（硬约束 / 风格目标 / 风格观察）与发布门槛的单源；`SF-15` / `SF-40` / `SF-42` 风格判定降为观察层并逐条记录理由。

### Changed
- README、评测说明、场景样本说明和 eval harness 批次表同步到 82 条 benchmark。
- README 英文简介补充 `AI writing humanizer` 和 npx 安装入口，保持中文优先，不扩成全文英文化。
- `SF-39` / `SF-40` / `SNF-29` / `SNF-30` 的场景标签显式带上 `in-place`，让盲测输入保留原先只写在章节说明里的 scope 指令。
- `SF-41` / `SNF-31` / `SNF-32` 的场景标签显式带上 `bounded`；重写 `SF-26` 的否定式歧义输入，让姿态层处于真实正文语境。
- `SF-12` / `SF-13` / `SF-20` 的预期同步到“不编造、不变泛、时间跨度不漂移”的新合同。
- README scene pack、无源引用 mixed 段落和路径正确性认证补回读边界。
- `SKILL.md`、eval rewrite prompt 和 README 模式地图同步无源数字的入口合同：无法独立成立时删整条论断，不能去掉数字后留下更泛判断；`bounded` 允许整条无源论断连同依附其上的数字进入待确认清单。
- `automation/check_repo.py` 的 README 英文计数锚点跟随未发布版本的 `82-case benchmark` 文案更新。
- 修复三处合同冲突：eval prompt 与 run-eval 此前允许 audit-only 样本整段冻结（与操作手册矛盾，`SF-18` 不稳定的直接原因），改为只约束无源论断本身；`SKILL.md` 单文件兜底补「方向/进度认证不得降格成弱安抚」；`SF-05` 预期对齐 rewrite-safe 合同（此前仍是旧口径"删掉研究表明直接给数据"）。
- 发布门槛从「SF > 90% 且全模型统一」改为「硬约束失败 0 + SNF 误杀 < 10% + 本版 targeted 达标」，judge 判分拆成硬约束列与风格 / SNF 误杀列；旧口径 SF 通过率继续并列报告，用于历史对比。
- 收紧双列语义：第二列对 SF 记录风格、对 SNF 记录误杀；普通 SNF 误杀不再误算成 L1，只有涉及编造或受保护片段破坏时才同时记硬约束失败。
- 修复最终全量暴露的 code-context 保真缺口：真实运行行为、适用条件和边界明确归入 protected spans；SF-27 补写“高峰期流量”不能被相邻 504 指标替代，避免清姿态词时整行删掉独有条件。
- 补齐实体与关系保真：抽象方案不得擅自具体化成工具 / 产品，目标不能换指代，架构潜力不能改写成实现关系；SF-03 / SF-07 / SF-08 / SF-32 的预期同步明确这些既有 L1 边界。
- 进一步钉住配对关系：数字与所修饰对象、主体与各自动作 / 目标必须一起保留，不能把并列分句的对象归属合并，也不能从“两个团队”推断出团队更换顺序。
- 增加分析—输出一致性回读：先记实体 / 关系账本；如果模型已经判断原文缺具体对象、能力或实现，最终结果不得再补出工具、产品、平台或功能，避免“诊断说不编造、输出却具体化”的自相矛盾。
- 事实 / 关系账本补目的、适用条件、风险和限制：对象暂时抽象不等于没有信息，清掉“痛点”等套话时仍须保留“解决问题”这一目的关系。
- 禁止把同段共现拼成新能力：背景或主题提到 AI，不代表相邻的表达工具处理 AI 生成文本；输出中的能力 / 输入 / 实现关系必须能回指原文同一谓词。
- 保留断言粒度与谓词状态：删渲染词时不能把“已经提升 / 改善 / 加强”弱化成“涉及”，也不能把“提升效率”推演成“节省时间 / 成本”；SF-09 / SF-12 的既有预期同步写明这条 L1 边界。
- 单源化去重：`automation/eval/rewrite-prompt.md` 的 scope 条款改为指向 `SKILL.md` 3.5，不再复述 bounded 例外；`references/` 全部文件头部加「行为合同以 SKILL.md 为准」的从属声明。

### Tested
- `python3 automation/eval/make_blind.py` 生成 82 条（46 SF + 36 SNF）。
- `python3 automation/check_repo.py` 通过：82 用例 / 19 样本 / 24 锚点 / 69 链接。
- `npx skills add MrGeDiao/shuorenhua` 真实安装成功；测试生成物未留在仓库。
- 核心 10 条 targeted：Codex SF 9/9、SNF 0/1 误杀；Claude SF 6/9、SNF 0/1 误杀。Grok / Gemini 诊断与 provenance 见 `evals/results-v2.1.0.md`。
- 82 条全量盲测：Codex SF 38/46、SNF 误杀 1/36；Claude SF 26/46、SNF 误杀 1/36。SF 通过率未达到既定 `>90%`，本版不恢复 `model-tested` 文案，已知边界如实归档。
- 入口合同对齐后补跑 B-11 / B-61：Codex 与 Claude 均不再去掉无源数字后保留泛化论断，并允许整条无源论断进入 bounded 待确认清单。
- Fable 结构修复后补跑 6 条双模型交叉 judge：两边 L1 失败均为 0、SF 均为 5/5；普通 SNF 误杀被稳定拆成「硬约束 ✅、SNF 误杀 ❌」，双列协议不再把它误算成 L1。
- 最终 diff 上重跑 82 条全量：Codex L1 失败 0、L2 41/43、L3 3/3、SNF 误杀 1/36；Claude L1 失败 1（SF-27）、L2 30/43、L3 3/3、SNF 误杀 3/36。两边 SNF 均达标，但 Claude 的 L1 失败阻塞正式版；完整判分和争议审计见 `evals/results-v2.1.0.md` §7。
- 关系保真根因修复后的最终 diff `d8408ce9edad998cba0cefcbc6372e84f3f07fb2`：Codex 完整 82 条 L1 失败 0、L2 37/43、L3 3/3、SNF 误杀 2/36；Claude 首轮出现 SF-07 单个 L1，未改规则后按事先声明完整确认复跑，确认轮 L1 失败 0、L2 36/43、L3 3/3、SNF 误杀 1/36。两边满足正式发布门槛；失败轮与确认轮并列归档，不宣称所有运行全绿。Codex judge 用量耗尽后，Claude 输出的剩余判分由 Grok 4.5 按同一双列协议完成。

## [2.0.2] - 2026-07-22 — 仓库完整性硬检查

### Added
- 新增 `automation/check_repo.py`：零依赖检查盲测生成物同步、计数锚点、相对链接、用例编号引用和元数据，任一检查前提失效时直接失败。
- `automation/eval/make_blind.py` 新增 `--check` 模式，在内存生成并逐字节比对两份盲测文件；默认生成行为不变。
- 新增 GitHub Actions `check` workflow，在 main push 和 pull request 上运行 `python3 automation/check_repo.py`。

### Changed
- `CONTRIBUTING.md` 的 PR 规范补提交前自检命令和新增计数文案时登记 `ANCHORS` 的要求。
- `automation/README.md` 补仓库完整性硬检查的定位、命令和五项检查说明。

### Tested
1. 仓库根目录运行 `python3 automation/check_repo.py` 通过：80 用例 / 19 样本 / 24 锚点 / 59 链接。
2. 从 `automation/` 目录运行结果与根目录逐字一致，exit 0。
3. 默认运行 `make_blind.py` 后 `git diff --exit-code -- evals/` 通过，生成逻辑字节不变。
4. 删除 `benchmark-map.md` 一行映射后，`[blind-sync]` 正确报出该文件，exit 1。
5. 删除 benchmark 最后一条用例且不重跑生成脚本后，`[blind-sync]` 失败，`[counts]` 在 README 等多处报出 80/79 和 35/34 失配。
6. 把一条 benchmark 用例编号改成重复编号后，`[blind-sync]` 透传「用例编号有重复」，exit 1。
7. README benchmark 徽章 80 改 81 后，`[counts]` 定位到 `README.md:23`，exit 1。
8. 删除 README「当前评测集共 80 条」锚点后，`[counts]` 报预期命中 1 次、实际 0 次，fail-closed 生效。
9. 临时改名 `references/examples.md` 后，`[links]` 定位 README 和 SKILL.md 的断链，exit 1。
10. 在 `references/operation-manual.md` 插入 `SF-99` 后，`[case-ids]` 定位到新增行，exit 1。
11. 删除 SKILL.md frontmatter 的 `description` 后，`[meta]` 报字段为空，exit 1。
12. 在 `.claude-plugin/plugin.json` 插入尾逗号后，`[meta]` 定位 JSON 解析错误，exit 1。
13. workflow 按零依赖环境目检通过；CI 首跑待维护者 push 后在 Actions 页确认。

## [2.0.0] - 2026-07-15 — Plugin 一键安装 / 分发铺设

### Added
- Claude Code plugin 化：新增 `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`（单仓库自荐为自己的 marketplace），两条命令装完：`/plugin marketplace add MrGeDiao/shuorenhua` + `/plugin install shuorenhua@shuorenhua`。
- plugin 直接以仓库根目录 `SKILL.md` 作为唯一 skill（Claude Code 支持单 skill plugin 的根布局），不引入 `skills/` 包装目录，「规则文件不复制成两份」以零拷贝满足；Windows 安装无需额外配置。（2026-07-15 发布前修订：替换原符号链接包装方案）
- README 新增 `## English` 段：一段式项目说明 + plugin 安装命令，供目录收录和国际用户。

### Changed
- `install/claude-code.md`：plugin 安装提为方式 1（含重复安装提醒），原项目级 / 全局 / 软链方式顺延为方式 2-4，全部保留。
- README「30 秒上手」Claude Code 块换成两条 plugin 命令，手动安装移到安装文档。
- （2026-07-11 发布前修订）双模型实跑改盲测口径：新增 `automation/eval/make_blind.py`，从 `benchmark.md` 生成 `evals/benchmark-blind.md`（匿名编号 B-xx、固定种子乱序、不含预期）和 `evals/benchmark-map.md`（judge 用映射表）；旧口径被测模型直接读 `benchmark.md`，预期 / 理由和 SF/SNF 编号前缀等于把答案递给考生。`automation/eval/` 三份文件与 `run-eval.md` 口径同步，批次改按 B 编号切。
- （2026-07-11 发布前修订）`evals/real-samples.md` 更名「场景样本评测（高拟真合成）」（文件路径不变防断链）：样本是"观察归纳 + 合成"产物，旧名「真实样本评测」易被误读为真实用户样本；SKILL.md / README 引用文案同步。
- （2026-07-11 发布前修订）新增 `evals/run-manifest.md`：实跑元数据登记（评测集版本 / 模型 / 口径 / 原始输出位置），回填 v1.9.0–v1.9.2，历史缺项如实标「未记录」。

### Fixed（2026-07-11 / 2026-07-15 发布前 deep review）
- （2026-07-15）`evals/benchmark.md` SF-15 / SF-23 预期示例不再编造原文没有的数据与实现（"3 倍 / 2 秒 / 0.4 秒"、"LRU / Redis / 10k QPS"）：与下面 SF-02 / SF-09 同类修法，示例只用原文已有信息重组，对齐盲测 rewrite prompt「不得编造数据与指标」的保真合同。同类隐患一并处理：`references/positive-style.md` §2.3 节奏示例补「没有数据就只调句长，不编数」的边界；`evals/real-samples.md` RS-06 推荐改法标注作者视角（替别人改写时拿不到事实，只删空话不编细节）。
- `evals/benchmark.md` SF-02 / SF-09 预期不再要求"给具体数据"：两条原文本无数据，旧预期与 fact-preservation 冲突（results-v1.9.1 §3 已确认"不编造是对的"），改为对齐 v2.1.0 规格的"清理后的落点"合同——允许短而直白，不得编造、不得留更泛空话。
- `SKILL.md` 保真回读"补一条事实句"补上限定：只能用原文已有信息重组，找不到就不补，堵住诱导补写新事实的口子。
- README 六步流程第 3 步与 SKILL.md 对齐：Tier 表示命中强度，不直接等于改写力度（原文案"按命中强度定力度"与 SKILL.md "不要把 Tier 当作改写力度"相抵）。

### Tested
- `claude plugin validate . --strict` 通过（plugin + marketplace 清单）。
- 本机实测完整链路（2026-07-15 按无 symlink 布局复测）：`marketplace add`（本地路径）→ `install` → `claude plugin details` 确认 Skills (1) shuorenhua 被发现，安装缓存为整仓拷贝，根目录 `SKILL.md` 对 `references/`、`evals/` 的相对引用直接解析 → 卸载恢复原状。常驻成本以当前版本 `claude plugin details` 实测为准（估算值随 CLI 版本与计算口径漂移，同一工作区多次实测差异可达数量级，不记具体数字）。GitHub 远程安装路径待 push 后由维护者复测一次。
- 现有手动安装路径（cp / 软链）不受影响；plugin 与 skills 目录安装并存会重复触发，安装文档已写明先移除旧安装。
- 盲测口径 smoke（2026-07-15，登记见 `evals/run-manifest.md`）：B-01–08 + 定向 B-58/B-78 端到端跑通，Codex 盲改写 → Claude 按映射表交叉判分，改写输出与判分表的格式合同全对齐；B-58/B-78（即修订后的 SF-23/SF-15）无编造数据或技术选型。已知缺口：`make_blind.py` 不传递 J 节的节级 scope 指令，judge 对 SF-39/40 暂不因 scope 判定记 ❌，修法待 v2.1.0 评估。

### Notes
- 分发动作从原规划的 2026-08 提前：仓库流量 6 月中旬起跳变约 6 倍并保持平台期（详见 local metrics log），按 2026-06 迭代文档 §4 的加码条件执行。
- 目录提交材料包与维护者手动清单在 local tasks 工作区；提交前需逐目录现查收录方式。
- 第三方在线 demo（issue #4 提及）的评估与背书决策留给维护者，本版不代做。

## [1.9.2] - 2026-07-05 — Claude 5 口癖巡检 / 标点腔 pattern pack

### Added
- references/structures.md 新增第 20 类「标点腔（破折号过密）」：把英文 em-dash 习惯带进中文的跨模型现象，按密度和位置判（首句起手 / 单段两处以上 / 跨段承接），单次出现和标题连接符放行。来源：Claude 5 家族（2026-06-09 发布）触发的首次口癖巡检，Linux.do 三个线程的多方独立证词（含跨模型：Claude / DeepSeek / Kimi 2.6）+ 五个固定探针任务 5/5 复现；观察轮次已满足（Opus 4.7/4.8 存量记录、Fable 5 追踪、自探针印证各一轮）。
- evals/benchmark.md 新增 5 条（75 → 80，42 SF + 33 SNF → 45 SF + 35 SNF）：
  - SF-43：破折号过密的标点腔，改标点不丢信息
  - SF-44：装坦诚（诚实宣言 / 主动自曝换可信度），删姿态层但保留自曝的真信息
  - SF-45：自媒体爆款词同族变体（直接封神 / 炸裂了 / 重点来了 / 掰开揉碎），不需词表逐条收录也应命中
  - SNF-34：承担真实插入语的单次破折号与标题连接符不误杀
  - SNF-35：「有，而且」开头的真实应答不因起手式命中改平
- 新增 evals/results-v1.9.2.md，归档本版 5 条新用例的 targeted 交叉回归（Codex 改写 + Claude 判读）：SF 3/3，SNF 0/2 误杀。

### Changed
- references/operation-manual.md 变体归并：郑重预告族补「诚实宣言」（我必须诚实地说 / 说句实话）与「装坦诚」（说个真实变化 / 缺点也说一句）两组识别信号，明确只删姿态层、自曝的真信息必须保留；暴力动作腔补 `钉死`；主动出击腔补 `趁热`；语域混搭补「强行游戏化 / 职业化比喻」识别信号（刺客 / 奶妈式产品比喻）和中英混排技术词的放行边界。
- benchmark 计数同步为 80 条（45 SF + 35 SNF），README.md（含徽章与「20 类结构反模式」）、evals/run-eval.md、evals/real-samples.md、automation/eval/README.md 批次表、automation/intake*.md 同步更新。

### Tested
- Codex 按 automation/eval 口径改写本版 5 条新用例，Claude 判读（与 v1.9.1 方向互补的交叉口径）：SF-43/44/45 全部命中且保护点无损，SNF-34/35 明确 no-op 零误杀。
- 复核既有覆盖：收口 / 落盘 / 接住 / 砍一刀 / 抓手 / 顺手等社区点名词均已有规则，本轮零新词条，全部走结构与既有问题族吸收。

### Notes
- 触发器：Claude 5 家族发布（roadmap 口癖巡检机制首次实战）。GPT-5.5 本轮未收到足量中文样本，留待下轮。
- 「孤儿（包）」有技术语境放行的反方社区意见，按宾语判断先例处理，未入库，继续观察。
- 本版不动 SKILL.md 主流程；标点腔经 structures.md 被既有流程（模式优先，词表兜底）自然引用。

## [1.9.1] - 2026-07-01 — Feedback Intake / 门面勘误与 targeted 回归

### Added
- evals/benchmark.md 新增 SF-42：回应 #5 首条反馈，钉住 README / 自我宣传文本里的“做快、做稳”残味。
- evals/benchmark.md 新增 SNF-33：保护有指标支撑的“稳定”状态同步，避免把“稳”一刀切当坏词。
- 新增 evals/results-v1.9.1.md，归档本版 targeted 单模型回归；明确不替代 v1.9.0 的全量双模型实跑基线。

### Changed
- README 首页示例去掉“把活做快、做稳”，改成直接说明本项目清理哪些中文 AI 残味。
- references/phrases-zh.md 补一条带护栏的“做快、做稳 / 又快又稳 / 更快更稳”规则，并给既有“更稳 / 最稳 / 不稳”条目补误杀边界：只处理自我宣传、项目介绍、营销式 README；有真实主体、指标或稳定性结果时放行。
- benchmark 计数同步为 75 条（42 SF + 33 SNF），README.md、evals/run-eval.md、evals/real-samples.md 与 eval harness 批次说明同步更新。

### Tested
- Claude targeted rewrite 覆盖 v1.9.0 的 8 个边界用例 + 新增 SF-42 / SNF-33；Codex 按 evals/run-eval.md 口径人工判读。
- SF-42 通过：README 自我宣传残味被去掉，且没有换成“更可靠 / 更高效 / 价值闭环”等同族空话。
- SNF-33 通过：“稳定”挂在具体指标上被放行，没有误杀。
- 复查 v1.9.0 留下的 8 个边界用例，确认本版新增规则不借机扩大为长文、无源引用或 mixed 场景大修。

### Notes
- 本版不做 v2.0 的 Claude Code plugin、目录分发、README 英文段或第三方 demo 背书。
- 本版只做 targeted 单模型回归 + 人工判读，不替代 v1.9.0 的双模型实跑结果。

## [1.9.0] - 2026-06-18 — Eval Harness / 模型实跑评测

### Added
- 新增 `automation/eval/` 三件套：`rewrite-prompt.md`、`judge-prompt.md`、`README.md`，把 benchmark 改写和交叉判分流程固化成可复制命令。
- 新增 `evals/results-v1.9.0.md`，归档首轮完整双模型实跑结果、非绿用例点评、bounded 尾巴补跑和成本基线。
- `evals/benchmark.md` 新增 `SNF-32`：`bounded` 下商业黑话壳句不得与紧随其后的具体数据句合并，数据句必须逐字保留。

### Changed
- README 评测区切换为 v1.9.0 起的双模型实跑口径；静态走查退为发版前快速自查。
- benchmark 计数同步为 73 条（41 SF + 32 SNF），`evals/run-eval.md` 和 `evals/real-samples.md` 同步 SNF 32 口径。
- `evals/run-eval.md` 补充 bounded 防并句判分：壳句与紧随其后的数据句被合并成一句，记 `❌`。

### Tested
- 小样试跑 `SF-01–05 + SNF-01–03` 第二轮格式可用，改写输出与 judge 表格可逐条对照。
- 首轮完整实跑：Codex 改写由 Claude 判，SF 39/41，SNF 0/32 误杀；Claude Opus 4.8 改写由 Codex 判，SF 34/41，SNF 0/32 误杀。
- `SNF-32` 用同一套 harness 补跑：Codex 与 Claude 均 0/1 误杀，未并句，数据句保留。

### Notes
- 本版不改 `SKILL.md` 或 `references/` 的规则行为，只新增 eval harness、归档和防并句用例。
- 成本基线：Codex rewrite 6 runs 记录 input 1,218,624 / cached 784,384 / output 103,780 / reasoning 87,653；Codex judge 6 runs 记录 input 866,815 / cached 446,720 / output 41,710 / reasoning 32,856。Codex CLI 未提供稳定 cost / duration 字段。
- Claude 可回收记录：SF rewrite 三批 416.503s / $2.629105，judge 六批 375.170s / $2.922822；可回收小计 791.673s / $5.551927。Claude SNF rewrite 小批缺 CLI cost / duration，不手算进小计。实际模型确认为 `claude-opus-4-8`。

## [1.8.8] - 2026-06-10 — README v2

### Changed
- `README.md` 整体重排：before/after 三组示例前置；新增「30 秒上手」（Codex / Claude Code / ChatGPT 三入口 + annotation mode 一句话用法）；场景、力度、scope 压缩为三表一流程；issue #4 的 scope 实测过程折叠进 `<details>`。
- 横幅从位图换成手写 SVG（`assets/banner-light.svg` / `banner-dark.svg`），用 `<picture>` 适配 GitHub 亮暗主题：文字全部转矢量轮廓（字形来自 Noto Sans SC，SIL OFL 1.1），不依赖访问者系统字体，跨平台渲染一致；视觉改走「红笔审稿」方向——划掉的套话、红色句号、一枚「可直接发」印章。原 `assets/readme-logo.png` 保留未删。
- 移除项目状态表和项目结构文件树：版本信息由 release 徽章和 CHANGELOG 承担，规则覆盖数字并入评测区。
- 小节标题去掉版本号，避免随版本腐烂。

### Notes
- 本版只动 `README.md`、`assets/`（新增两个 banner SVG）与本文件，不改规则与评测；计数为实测同步（benchmark 72 条 = 41 SF + 31 SNF，real samples 19 条）。

## [1.8.7] - 2026-06-10 — Maintenance Surface 2 / 安装口径与 bounded 下沉

### Changed
- `install/claude-code.md` 重写：Claude Code 会按 `SKILL.md` frontmatter 的 description 自动发现并触发 skill，移除“不会自动发现、CLAUDE.md 说明不能省略”的过时断言；CLAUDE.md 触发说明降级为可选增强；新增软链接“跟随更新”安装方式。
- `install/` 全部平台文档补「长文改写的三档 scope」小节（structural / bounded / in-place 与长文默认值）——v1.8.6 的 scope 能力此前没有下沉到任何安装入口。
- `install/chatgpt-gpt-instructions.md` 执行流程补 scope 判断一行（需维护者手动同步到 Custom GPT 后台）。
- `references/examples.md` 新增 Bounded 双合同示例（正文 + 建议删除清单，合成文本，含「句内洗 vs 进清单」的边界说明）。
- `references/positive-style.md` 长文节奏边界补一句 bounded 口径：节奏句不进清单，进清单的必须是纯空句。

### Notes
- 本版不改 `SKILL.md` 与 `evals/`，是 v1.8.4 之后第二个维护面版本。
- 仓库杂项：移除空的 `docs/` 目录；`CLAUDE.md → AGENTS.md` 软链纳入版本控制，Claude Code 用户 clone 后直接生效。

## [1.8.6] - 2026-06-03 — Bounded Scope / 长文去味与保长度的中间态

针对 [#4](https://github.com/MrGeDiao/shuorenhua/issues/4) 复测反馈:v1.8.5 的 `in-place` 把长度接住了(实测 95–96%),但去 AI 味效果明显弱于 `structural`——长文里整句级的空话(无源引用、价值拔高收尾)在 `in-place` 下规则上删不掉,只会被软化保留。本版在 `structural` 和 `in-place` 之间补一个 `bounded` scope。

### Added
- `SKILL.md` 新增 `bounded` edit scope:`public-writing` 长文默认 scope。允许删"整句都是空话"的句子,但不直接删,而是进「建议删除(待确认)」清单交用户拍板;句内洗实句照常,不并句、不重排、不删承担节奏的重复。
- `evals/benchmark.md` 新增 2 条用例(70 → 72,40 SF + 30 SNF → 41 SF + 31 SNF):
  - `SF-41`:`bounded` 下整句空话(谄媚开场 / 无源引用 / 价值拔高收尾)进删除清单,带数字的实句和排比节奏句原样保留
  - `SNF-31`:`bounded` 删除清单不该混进实句或节奏句——带句首引导词(`说到底`)但实质是立场判断的句子,只能句内删引导词,整句不进清单
- `references/operation-manual.md` 顶部新增「Scope 与删除清单」一节,统一三档 scope 下"整句空话 vs 句首引导词"的处理,不在各类问题里重复。

### Changed
- 长 `public-writing` 默认 scope 从 `in-place` 改为 `bounded`(行为变化);`in-place` 退为用户明确要求"完全原样 / 一句都别删 / 严格保句数",或反馈 `bounded` 仍删多了时才用。
- `SKILL.md` 执行顺序第 5 步 scope 判断扩成三档;第 8 节回读把"字数留存"从硬指标降为参考,新增"信息留存"为硬指标——`bounded` 删整句空话会降字数,约束应落在"信息点可追溯"和"删除清单只含纯空句"上,不是字数。
- `README.md`、`evals/run-eval.md` 同步版本、计数(72)、scope 三档和默认值变化。

### Tested
- 2026-06-03 首次**模型实跑**(此前各版为静态复核):同一篇 1498 字合成长文,用现有 `SKILL.md`+`references/` 跑 `aggressive` 力度的 `structural` 和 `in-place`,Codex(gpt-5 家族)与 Claude(opus 家族)双交叉。
- 结果支撑本版动机:`in-place` 两个模型都把无源引用、价值拔高收尾**整句残留**(只软化铺垫),留存 95–96%;`structural` 都删掉这些整句空话,留存 80–83%。`bounded` 规则刚落地,实跑留待下一轮。
- 一处修正:`structural` 在两个强模型上并未腰斩(实测 -18%,非 issue #4 报告的 -39%),说明长文 `structural` 缩水程度依模型而定、不可控——这也是 `bounded` 把"删多少"交还用户的理由。

### Notes
- `bounded` 不是第四个力度档位,而是 scope 轴上介于 `structural` 和 `in-place` 之间的中间态;`minimal / standard / aggressive` 三档力度不变。
- 实跑成稿和对照存档在本地 `tasks/current/runs/`(local-only)。

## [1.8.5] - 2026-05-27 — In-place Scope / 长文保长度

针对 [#4](https://github.com/MrGeDiao/shuorenhua/issues/4) 反馈"长文被改完明显缩水"（约 1800 字 → minimal 约 1500 字 → aggressive 约 1000 字）。本版结论：问题不在三档力度，而在长文默认走 structural 动作时，删句、并句、重排段落会叠加。

### Added
- 新增 `in-place` edit scope，和 `minimal / standard / aggressive` 三档力度**正交**。`in-place` 下只做句内替换、删短语和降调，不默认删整句、并句或重排段落。它不是第四档力度，而是改写动作的边界。
- `evals/benchmark.md` 新增 4 条用例（66 → 70 条，38 SF + 28 SNF → 40 SF + 30 SNF）：
  - `SF-39`：长 `public-writing` 在 `in-place` 下应去掉拔高骨架，但保留字数、句数和关键转场
  - `SF-40`：多类骨架叠加时，`in-place` 应做句内替代，而不是删段落
  - `SNF-29`：重复短语承担长文节奏时，不应被当作水分误删
  - `SNF-30`：正常承接句挂在事实上下文里，不应被误杀为总结式收尾
- `evals/real-samples.md` 新增 `RS-19` 高拟真合成长文样本（不直接转录 issue #4 原文），并为 long-form 场景增加 `长度节奏` 评分维度。
- 新增 `evals/results-v1.8.5.md`，归档本轮静态复核。

### Changed
- `SKILL.md` 在执行顺序里加入 scope 判断，定义 `structural` / `in-place` 两种改写边界。默认走 `structural`；中文 `public-writing` 长文（约 1000 字以上）或用户明确要求保长度、保句数、保段落节奏时切到 `in-place`。
- `references/operation-manual.md` 给二元对比、总结式收尾、narrator 腔、价值拔高骨架四类骨架补 `in-place` 替代动作，保留原有 structural 默认动作不变。
- `references/positive-style.md` 和 `references/scene-guardrails.md` 加长文节奏边界：重复和转场不一定是水分，删之前先看它是不是在承担段落呼吸。
- `evals/run-eval.md` 同步 scope 判断和 70 条 benchmark 的评测范围。
- `README.md` 同步版本、计数和 In-place Scope 能力说明。

### Tested
- 静态复核 `SF-39` / `SF-40` / `SNF-29` / `SNF-30`：4 条新增 benchmark 都能被 `SKILL.md` + `references/operation-manual.md` 当前的 scope 规则解释。
- 静态复核 `RS-19`：推荐改法保留五段结构、三处时间锚点和关键转场，不把长文压成摘要。
- 没有跑模型实测。本版的"通过率"是静态走查口径，不是任何具体模型在线跑出来的结果——模型实跑留给后续轮次。

### Notes
- 本版不动 `minimal / standard / aggressive` 三档力度本身，也不新增第四档；调整集中在"动作边界"这一条新的正交轴上。
- `in-place` 不是凑字数。字数留存率（目标 ≥ 0.90，硬下限 0.85）是回读指标，真正约束的是不删整句、不并句、不重排段落。
- "约 1000 字"是这一轮反馈得到的工程默认值，不是稳定结论；后续需要更多真实长文 bad case 校准。

## [1.8.4] - 2026-05-17 — Maintenance Surface / 维护入口对齐

### Added
- 新增 `.github/ISSUE_TEMPLATE/bad-case.md`，给“改完还是像 AI”的反馈留一个结构化入口，固定收集原文、使用方式、场景、问题点、不可改坏内容和期望方向。
- `CONTRIBUTING.md` 新增 bad case 提交说明，明确脱敏和授权边界。

### Changed
- `README.md` 最新版本说明更新到 `v1.8.4`，并把 lite / full 的安装口径写清楚：lite 是只加载 `SKILL.md`，full 是 `SKILL.md` + `references/`。
- `install/` 下各平台安装文档统一 lite / full 表述，避免不同入口对“只放 `SKILL.md` 还是带 `references/`”给出相互矛盾的建议。

### Notes
- 本版不改 `SKILL.md`、`references/`、`evals/benchmark.md` 或评测口径；它是维护入口和分发准备版本，不是规则能力扩张。
- 本地 `tasks/current/roadmap-v1.8-v2.0.md` 已同步到当前维护状态；`tasks/` 仍保持 local-only，不进入公开发布面。

## [1.8.3] - 2026-05-09 — Community Intake Round 1 / 首次实战

### Added
- `evals/benchmark.md` 新增 4 条用例（62 → 66 条，35 SF + 27 SNF → 38 SF + 28 SNF）：
  - `SF-36`：路径正确性认证（`已经走在正确的路上了 / 走得很稳`），身份认证式夸奖在"对你的进度"维度上的延伸
  - `SF-37`：对人本身发证书（`说明你已经超越绝大部分人了 / 你已经具备做这件事的实力了`），SF-31 同族新变体
  - `SF-38`：庸医问诊腔变体（`掰扯清楚 / 彻底掰开说清楚`），归并到 `references/phrases-zh.md` 「庸医问诊腔」族
  - `SNF-28`：技术语境里的"落盘"放行（宾语是 `重构方案 / 三份文档` 这类具体技术对象），规则同 v1.7.3 的 `接住` 按宾语判断

### Changed
- `references/operation-manual.md` 4 处补充（按"模式优先、词条兜底"原则，主要规则更新落在 manual 边界，不新增 phrases-zh 词条）：
  - 5.2 节「过度接住 / 心理判断腔」补 `你现在的 X 很正常` 心理判断变体
  - 5.2 节补 `抱住 / 紧紧抱住 / 拥抱 / 实实在在的抱住你这种想法` 同类抚慰动词归并提示
  - 第 3 节「工程师腔」补 `落 X / 把 X 落下去 / 落到` 万能动词边界（按宾语区分姿态层 vs 技术对象）
  - 第 7 节「价值拔高骨架」补 `你看完会彻底开悟 / 看完就懂了 / 看完会震惊 / 看完不再 X` 承诺式收尾
- `evals/run-eval.md` 同步评测口径：SF 范围 → `01–38`，SNF 范围 → `01–28`，总数 → `66`
- `README.md` 同步状态徽章、状态表、评测表、项目结构里的 benchmark 数量（62 → 66），版本号 → `v1.8.3`
- `evals/real-samples.md` 同步 benchmark 计数（62 → 66）：元数据对比表（"benchmark vs real-samples 分工"）+ RS-10 推荐改法演示文本，样本本身和数量（18 条）不变
- `references/phrases-zh.md` 工程师腔族升级 `落盘 / 已经落下去` 两条已有词条为按宾语判断（沿用 v1.7.3 `接住` 的处理方式），让 SNF-28 在单加载词表的评测路径上也能正确放行；不新增词条

### Tested
- 2026-05-09 用 v1.8.2 引入的 intake automation 跑了首次真实 community intake：10 条样本批次 → 报告归类 `已覆盖 3 / 变体归并 13 / 候选新模式 2`，落到 `tasks/current/intake/reports/2026-05-09-intake.md`（local-only）
- intake 报告自身守住"已覆盖 → 无动作"边界：3 条已覆盖样本（包括接住体长版样板、元讨论保护、`You're absolutely right!`）全部按现有规则放行，没有被推到候选新模式
- 新增 4 条 benchmark 静态复核：在更新后的 `operation-manual.md` 下，SF-36/37/38 命中身份认证 / 庸医问诊腔规则；SNF-28 在工程师腔的"落 X 按宾语判断"新边界下应放行

### Notes
- 本版坚持 v1.8.2 intake 协议的"模式优先、词条兜底"：**不新增** `references/phrases-zh.md` 词条；只升级已有 `落盘 / 已经落下去` 两条的判断口径（同 v1.7.3 `接住`），其余规则更新落在 `operation-manual.md` 的边界说明上
- 2 个候选新模式（末尾二选一追问 / narrator 自夸式自我演绎）按 `automation/README.md:62-64` 协议，先记录在 intake 报告里观察 2-3 轮，确认是否反复出现再考虑入库；本版不立即落库
- 本轮 intake 也是 v1.8.2 工具链首次脱离 dryrun 跑真实社区样本，验证了"先 intake 报告 → 人工确认 → 才动文件"的工作流可走通
- 不动 `references/structures.md`、`SKILL.md`；`evals/real-samples.md` 仅做计数同步，样本本体和数量（18 条）不变；`references/phrases-zh.md` 仅升级 `落盘 / 已经落下去` 两条已有词条的判断口径，不新增词条

## [1.8.2] - 2026-05-01 — Intake Automation / 维护者侧反馈闭环

### Added
- 顶层新增 `automation/` 目录，作为维护者工具入口（committed）：
  - `automation/intake.md` — 协议规范
  - `automation/intake-prompt.md` — Codex prompt 本体
  - `automation/README.md` — 运行入口，含可复制粘贴的 `codex exec -C . -s read-only --ephemeral -o ...` 命令、文件命名约定、强约束说明
- 运行实例继续放在 `tasks/current/intake/inbox/` 和 `reports/`（`.gitignore` 内，本地工作目录），第一次用前 `mkdir -p` 即可
- dryrun 验证集（本地）：6 条合成样本覆盖三档结论 + 两类陷阱（被讨论词、技术语境放行），expected baseline 钉在 inbox 同目录下
- 真实样本 smoke（本地）：用 `evals/real-samples.md` 的 RS-14 接住体跑了一次，验证工具守住"已覆盖 → 无动作"边界

### Changed
- `CONTRIBUTING.md`「维护者：Community Observation Intake」末尾新增"自动化运行（v1.8.2 起）"小节，明确自动化只覆盖原 5 步里的第 2-3 步（抽象姿态链、判宾语 / 判场景），第 1、4、5 步仍需人工
- 公开路线图把原 v1.8.2「Feedback Loop / 反馈闭环」拆成两半：维护者侧 intake automation（本版）+ 外部 issue 模板 / pinned issue / bad-case 公开征集（顺延到 v2.0，理由和 v1.7.3 retro 一致）

### Tested
- 2026-05-01 跑了两轮 codex exec：第一轮 dryrun 6/6 命中 expected（已覆盖 3、变体归并 2、候选新模式 1），无误判被讨论词或技术语境放行；第二轮真实样本 smoke 1/1 标"已覆盖 → 无动作"
- 报告格式两轮都符合 spec 的 6 段：本轮样本数 / 已覆盖 / 变体归并 / 候选新模式 / 建议动作 / 一句总判断
- prompt 一轮通过，没有进入预设的"最多 2 轮微调"分支

### Notes
- 本版只动 intake 工具链 + 维护者文档，**没有改** `SKILL.md`、`references/*`、`evals/benchmark.md`、`evals/real-samples.md`、`README.md`，benchmark 总数仍为 62 条（35 SF + 27 SNF）
- 强约束遵循 spec 已固定的口径：报告默认不建议加词条、不自动改仓库；`-s read-only` 沙箱在 codex 层再保一道
- 不做 Codex Automation 调度（每周自动跑、自动开 issue）和外部 bad-case 征集入口，等 v2.0 配合分发一起做

## [1.8.1] - 2026-04-27 — Knowledge Architecture / 项目知识架构对齐

### Changed
- `README.md` 更新项目状态和快速开始入口，把公开信息架构对齐到当前已发布能力
- `install/codex.md` 和 `evals/run-eval.md` 切换到当前 Codex CLI 的 `codex exec` 用法，避免旧命令继续作为主入口传播
- `install/chatgpt.md` 去掉易漂移的 reference 文件数量，改为按目录上传完整知识文件

### Framing
- 本版定位为项目知识架构对齐：让新用户能从 README 进入使用路径，让评测和安装入口保持同一套事实基线
- 不改变 `SKILL.md`、`references/`、benchmark 判分口径或 Scene Packs 行为；`v1.8.1` 是采用路径和维护表面的升级，不是规则能力扩张

## [1.8.0] - 2026-04-24 — Scene Packs / 可直接发场景包

### Added
- 新增 `references/scene-packs.md`，把 `public-writing` 细分为 `README`、`release-note`、`forum-post`、`issue-reply` 四个可发布场景
- `evals/benchmark.md` 新增 8 条 scene pack 回归用例：`SF-32` ~ `SF-35` 覆盖该改场景，`SNF-24` ~ `SNF-27` 覆盖误杀防护
- `evals/real-samples.md` 新增 `RS-15` ~ `RS-18` 四条整段样本，分别覆盖 README intro、release note、forum post 和 issue reply
- 新增 `evals/results-v1.8.0.md`，归档本轮 TDD 静态复核结果

### Changed
- `SKILL.md` 在大场景判定后增加 Scene Packs 入口：先判 `public-writing`，再按发布目的细分
- `references/scene-guardrails.md` 明确分工：大场景边界仍由 guardrails 控制，scene packs 只做更细的落地策略
- benchmark 总数从 54 条（31 SF + 23 SNF）扩到 62 条（35 SF + 27 SNF）
- `README.md` 重构为正式项目首页：新增状态徽章、快速导航、v1.8.0 场景能力入口和 Star History
- 新增 `assets/icon-hd.png` 和 `assets/readme-logo.png`，在保留原 icon 元素的基础上补齐 README 横向品牌图

### Tested
- 2026-04-24 按 TDD 做静态复核：先补 `SF-32` ~ `SF-35` / `SNF-24` ~ `SNF-27`，再写最小 Scene Packs 和接入点
- 静态复核结果：SF 通过率 `35/35 (100%)`，SNF 误杀率 `0/27 (0%)`，Scene Packs `8/8 (100%)`
- 复核方式、用例详情和 real samples 评分口径见 `evals/results-v1.8.0.md`

### Notes
- v1.8.0 不做 Voice Calibration / Voice Hints，不模仿名人、品牌或公众人物
- 公开 bad-case 征集入口继续留到 v2.0，等项目有更多外部流量后再和分发一起做

## [1.7.4] - 2026-04-20 — Guardrails & Retro

### Added
- `evals/benchmark.md` 新增 `SNF-22`（code-context：技术语境里的接住突发请求）和 `SNF-23`（docs：限流网关稳稳接住上游峰值请求），作为 v1.7.3"接住"语境判断的**回归护栏**——防止未来改规则时把"接住请求 / 接住流量 / 稳稳接住上游峰值请求"一起误杀
- `evals/results-v1.7.4.md` 新增评测归档：追溯覆盖 v1.7.1 → v1.7.4 的 benchmark 增量（`SF-31`、`SNF-22`、`SNF-23`），补上 v1.7.2 / v1.7.3 当时没做的结果归档
- `CONTRIBUTING.md` 新增"维护者：Community Observation Intake"小节，把 v1.7.3 用过的"公开讨论 → 姿态链抽象 → 判宾语 / 判场景 → 双向补样本 → 升级规则"五步流程沉淀为可复用协议

### Changed
- benchmark 总数从 52 条（31 SF + 21 SNF）扩到 54 条（31 SF + 23 SNF）
- `README.md` 的评测口径（54 条）、最新归档链接（`results-v1.7.4.md`）、文件树里的 benchmark 条数（54）同步对齐
- `evals/real-samples.md` 顶部版本标记从"v1.7.2 新增"升级为"v1.7.2 新增（首批 12 条），v1.7.3 扩到 14 条"；内部 benchmark 对比表条数同步为 54

### Tested
- 2026-04-20 对 `SNF-22` / `SNF-23` 做静态复核：在 v1.7.3 现有规则下（`phrases-zh.md:88-90, 240-243`、`operation-manual.md:201, 213, 219`）两条 SNF 都按预期放行，**不需要修改规则文件**——这正是"先写回归测试再看规则"的 TDD 收尾
- 复核方式、通过率和用例详情见 `evals/results-v1.7.4.md`

### Notes
- v1.7.4 是 v1.7.x 的收尾版本，主旨是 **Guardrails（回归护栏）** + **Retro（追溯归档和方法论沉淀）**，不引入新能力也不扩词表
- 原 v1.7.3 roadmap 规划的"入口打通 + bad-case 收集"整体推迟到 v2.0，等项目有曝光后再配合分发一起做
- 后续路线已调整：v1.8.0 先做 Scene Packs / 可直接发场景包，Voice Hints Lite 推迟到 v1.9 评估

## [1.7.3] - 2026-04-17 — Community Intake / 接住体

### Added
- `evals/real-samples.md` 新增“社区观察：为什么‘接住体’一眼像 AI”区块，提炼 Linux.do / V2EX 公开讨论里的高频方法信号，并附公开链接作观察来源
- `references/boundary-cases.md` 新增案例 10：技术语境里的“接住请求”，明确 `接住` 不能按字面一刀切
- `evals/real-samples.md` 新增 `RS-14`（社区标题 / 宣言腔），覆盖 `稳稳地接住所有人` 这类标题式承接承诺

### Changed
- `references/phrases-zh.md`、`references/operation-manual.md` 把“接住”从单词命中升级为按宾语和场景判断：人/情绪/关系默认更可疑，请求/流量/峰值先回技术语境判断
- `SKILL.md` 的 Lite 模式兜底同步覆盖“过度接住 / 心理判断 / 身份认证式夸奖”，避免单文件模式和 Full 模式行为分裂
- `README.md` 同步补“姿态链优先”的解释，明确这类问题按模式处理，不按社区热词逐条追打
- 按最近公开讨论里的分布，这版也开始覆盖 Claude Opus 4.7 新冒出来的那批口癖；它在“我就在这里 / 稳稳接住 / 你不是……你只是……”这组姿态链上，已经越来越接近 GPT-5.4
- `evals/real-samples.md` 数量从 12 条更新为 14 条，`README.md` 评测口径同步对齐

### Tested
- 2026-04-17 做一轮“接住体”静态 smoke test：私聊安抚、社区标题、推销式结尾应命中；技术语境里的“接住峰值请求 / 流量”应放行
- `git diff --check` 通过

## [1.7.2] - 2026-04-17 — Real Sample Eval Pack

### Added
- 新增 `evals/real-samples.md`，首批 12 条整段样本，覆盖 README 简介、release note、X 短帖、Linux.do 长帖、GitHub issue 回复、commit message、Python docstring、开发进度同步、技术博客开头、微信对话、知乎长回答、混合场景
- 每条样本按统一模板记录：原文、场景、为什么像 AI、不该改坏什么、推荐改法、原文 3 维评分
- 新增 3 维评分体系：`自然 / 保真 / 可直接发`（5 分制），以"可直接发"为最终指标，`保真` 掉到 < 4 分即算退步
- 新增"高频 AI 句式分布"区块：汇总 2026-04 中文用户被吐槽最多的 AI 味句式（`要不要我顺手帮你`、`掰开揉碎`、`先说结论`、`直接封神`、`核心逻辑是` 等），用来指导样本构造
- `README.md` 示例 2 换成 `RS-11`（微信工程师腔溢出），还原"程序员一开口像在写工程报告"的尴尬瞬间

### Changed
- `README.md` 评测区补充 `real-samples.md` 12 条整段样本的说明，和 51 条 benchmark 并列
- `tasks/roadmap-v1.7-v2.0.md` v1.7.2 条目全部打勾

### Notes
- 首批为"观察归纳 + 合成"样本，不指向任何真人或真项目。之所以不直接引用真实帖子到公开仓库：未授权转录有归属和合规问题
- 真实样本收集机制留给后续版本，届时会补单独的提交流程和授权模板，再追加到本文件（目标 20+ 条）

## [1.7.1] - 2026-04-14 — Residual Audit / Two-pass

### Added
- `references/operation-manual.md` 新增 `Residual Audit / 二次审稿` 条目，固定第二遍只查 5 类残留：开场、总结、narrator、空泛判断、句长过匀
- `references/examples.md` 新增 2 组一遍 vs 两遍示例，并把英文 `two-pass demo` 改成不补新事实的版本
- `evals/benchmark.md` 新增 5 条二次审稿相关用例：`SF-28`、`SF-29`、`SF-30`、`SNF-20`、`SNF-21`

### Changed
- `SKILL.md` 把回读正式拆成两步：`保真回读 + Residual Audit`，并明确第二遍只允许轻量修正
- `SKILL.md` 补充场景保守策略：`docs / status / code-context` 的第二遍默认更克制，宁可停在第一遍也不为了“更像人”改失真
- `evals/run-eval.md` 同步评测口径：纳入 `Positive Style Contract` / `Protected Spans`，SF/SNF 范围更新到 `30 / 21`
- `README.md` 同步工作流和 benchmark 数量到 `51` 条

### Fixed
- `SKILL.md` frontmatter 去掉远端同步带来的 `metadata` 字段，调整为当前本地 skill 规范可稳定使用的形式

### Tested
- 2026-04-14 用 GPT-5.4 Codex 静态复核 `benchmark.md`（51 条）：SF 通过率 `30/30 (100%)`，SNF 误杀率 `0/21 (0%)`
- `Residual Audit` 新增 3 条正例（`SF-28`、`SF-29`、`SF-30`）和 2 条反误杀样本（`SNF-20`、`SNF-21`）全部通过

## [1.7.0] - 2026-04-13 — Positive Style Contract + Protected Spans

### Added
- 新增 `references/positive-style.md`，把“更像人”写成正向合同：强调具体动作、真实主语、轻微不对称节奏和分场景校准，不再只停留在“删套话”
- 新增 `references/protected-spans.md`，把数字、日期、名字、引用、命令、代码、参数、路径、报错、指标和责任归属整理成预检清单
- `evals/benchmark.md` 新增 4 条 fact-preservation 相关用例：`SF-25`、`SF-26`、`SF-27`、`SNF-19`

### Changed
- `references/scene-guardrails.md` 接入 `Protected Spans` 入口，按场景补充优先保留项
- `SKILL.md` 执行顺序改为先划 `protected spans` 再改写，回读项补 protected spans 检查，并加入 `Positive Style Contract` / `Protected Spans` 导航
- `README.md` 同步新增 `Protected spans` 和 `Positive Style Contract` 能力说明，更新 benchmark 数量和 `v1.7.0` 口径

### Notes
- 本次只落 `v1.7.0` 的基础层，不包含 `Residual Audit / Two-pass`、voice 拟合、real-sample pack 或 scene packs
## [1.6.1] - 2026-04-08 — ChatGPT Custom GPT 支持

### Added
- 新增 `install/chatgpt-gpt-instructions.md`，提供 Custom GPT 的 Instructions 文本，用户自建 GPT 时直接复制
- `install/chatgpt.md` 新增 Custom GPT 方案（推荐）和 Projects 方案，解决 Custom Instructions 1,500 字符放不下 `SKILL.md` 的问题（[#3](https://github.com/MrGeDiao/shuorenhua/issues/3)）

### Changed
- `install/chatgpt.md` 原有的 Custom Instructions 方案降级为备选，注明字符限制
- `README.md` 快速开始部分新增 ChatGPT Custom GPT 入口提示，平台链接更新为"ChatGPT / Custom GPT"

## [1.6.0] - 2026-04-03 — Code-context benchmark + rule boundary hardening

### Added
- `evals/benchmark.md` 扩到 42 条：新增 `code-context` 维度，补上 `SF-22`（docstring AI 腔）、`SF-23`（commit message AI 腔）、`SF-24`（英文代码注释 AI 腔）、`SNF-17`（正常技术注释）、`SNF-18`（正常 commit message）
- 覆盖矩阵新增 `code-context` 列，评测标准补 code-context 样本约束
- `references/boundary-cases.md` 新增案例 9：混合场景 worked example（技术博客嵌事故复盘），完整展示判主场景、识别次场景、分区处理的决策过程
- `references/severity.md` 误杀防护新增第 11 条：中英混排句中的英文词按实际语义判断，不机械套词表
- `SKILL.md` 单文件兜底规则同步补中英混排指引

### Changed
- `references/severity.md` Tier 2 新增长度归一化：短段落（< 100 字/词）同段 2+ 即标记，长段落（≥ 100 字/词）同段 3+ 再标记；决策流程图同步更新
- `SKILL.md` Tier 2 描述同步加长度参考
- `references/severity.md` Tier 2 定义段去掉写死的"2 个以上"，改为指向长度参考，数字来源收敛为一处
- `evals/run-eval.md` 更新 SF/SNF 范围、总 case 数（42）、评测提示词补 code-context 说明

## [1.5.0] - 2026-03-30 — Benchmark matrix + unsourced citation policy + annotation mode

### Added
- `evals/benchmark.md` 扩到 37 条：新增 `long / mixed / unsourced citation focus` 三类样本，补上 `SF-18`、`SF-19`、`SF-20`、`SF-21`、`SNF-15`、`SNF-16`
- `SKILL.md` 新增 `annotation mode` 输出合同，固定最小字段为 `问题族 / 触发点 / 建议动作 / 是否建议改写`
- `references/examples.md` 新增 3 组 `annotation mode` 对照示例
- 新增 `evals/results-v1.5.0.md`，归档本轮 benchmark 复核结果

### Changed
- `SKILL.md`、`references/operation-manual.md`、`references/scene-guardrails.md` 全部对齐为 3 种无源引用策略：`rewrite-safe`、`audit-only`、`rewrite-with-placeholder`
- `evals/run-eval.md` 从 Codex 专用改为平台无关，新增 Claude Code 快速运行和通用 LLM / API 评测说明
- `install/codex.md` 增加 `annotation mode` 的最小可复制用法
- `install/claude-code.md` 增加 `annotation mode` 用法和无源引用模式说明
- `install/openclaw.md` 增加 `annotation mode` 用法和无源引用模式说明
- `install/cursor.md` 增加 `annotation mode` 用法和无源引用模式说明
- `install/chatgpt.md` 增加 `annotation mode` 用法和无源引用模式说明
- `README.md` 安装部分新增 Claude Code 快速用法，annotation mode 示例覆盖 Codex 和 Claude Code；平台链接顺序调整为 Codex > Claude Code > OpenClaw > Cursor > ChatGPT
- `CONTRIBUTING.md` 更新到 `v1.5.0` 的 benchmark 规模、标注模式和维护策略

### Tested
- 2026-03-30 静态 benchmark 复核 `benchmark.md`（37 条）：SF 通过率 `21/21 (100%)`，SNF 误杀率 `0/16 (0%)`
- 2026-03-30 用 GPT-5.4 Codex 对 `SF-05`、`SF-21`、`SNF-01`、`SNF-16` 做 `annotation mode` 抽样验证，结果与新规则一致

## [1.4.3] - 2026-03-28 — Pattern-first intake hardening + eval sync

### Added
- 新增“模式变体归并”规则：遇到 `扒开 / 拽出来` 这类未逐词收录的说法，先并入现有问题族，不把词表当成穷举清单
- `evals/benchmark.md` 新增 2 条用例：`SF-17` 验证现有模式对未收录变体的吸收能力，`SNF-14` 验证讨论词条维护策略时不误杀被引用词
- 新增自动化 intake 方案文档，定义社区样本的收集、归类、建议输出和人工确认流程
- 新增 `tasks/automation-intake-prompt.md`，提供可直接复用的 automation prompt 模板

### Changed
- `SKILL.md`、`references/operation-manual.md`、`references/phrases-zh.md`、`CONTRIBUTING.md` 全部对齐为“模式优先、词条兜底”的维护策略
- `evals/run-eval.md` 和 README 的 benchmark 口径同步到最新用例数量

### Tested
- 2026-03-28 用 GPT-5.4 Codex 重新跑 `benchmark.md`（31 条）：SF 通过率 `16/17 (94.1%)`，SNF 误杀率 `0/14 (0%)`

## [1.4.2] - 2026-03-26 — 发布口径对齐 + 文档修正

### Changed
- `SKILL.md` frontmatter：`name` 从 `stop-slop-zh` 改为 `shuorenhua`，描述补"中英文"，H1 改为"说人话"
- `install/` 文档全面修正触发模型描述：删除"Claude Code 自动识别"和"OpenClaw 全量加载"等误导性说法，明确各平台的触发入口；统一补充验证示例
- `evals/run-eval.md`：补全缺失的 reference 文件列表（`phrases-en`、`operation-manual`、`scene-guardrails`、`boundary-cases`）；评测流程改为先判场景 / Tier / 档位

## [1.4.1] - 2026-03-26 — Skill workflow 修复 + benchmark 边界加固

### Added
- 新增 `references/operation-manual.md`，把二元对比、总结收尾、工程师腔、商业黑话、narrator 腔、语域混搭等问题写成可执行的微操作协议
- 新增 `references/scene-guardrails.md`，补齐 `chat / status / docs / public-writing` 的禁改项
- 新增 `references/boundary-cases.md`，加入系统主语、英文图算法字面动词、学术被动语态、具体证据支撑的真人 debug 对话等边界案例
- 新增“价值拔高骨架”规则，明确覆盖 `这不仅仅是……更是……`、`真正的 X 不是……而是……`、`最后比拼的是……`

### Changed
- `SKILL.md` 重写为入口型主文档：先做场景 / Tier / 档位判断，再按问题类型补读 `references/`
- 单文件模式改成明确兜底路径，不再暗示 `SKILL.md` 单独加载就等于完整模式
- `SKILL.md` frontmatter 恢复中文触发描述，降低 skill 自动触发失配风险

### Fixed
- 修正 `references/operation-manual.md` 中把 `对上了` 替换成 `对齐` 的规则冲突，改为 `核对`
- 为 `navigate` 在图算法 / 网络拓扑语境中的字面用法增加误杀防护
- 为学术或实验语体中的正常英文被动语态增加误杀防护
- 为带具体参数、操作和结果的真人工程师 debug 对话增加误杀防护
- 静态 benchmark 风险点补强：覆盖 SF-08、SF-16、SNF-05、SNF-09、SNF-11

## [1.4.0] - 2026-03-25 — GPT-5.x 新词入库 + Codex review 修复

### Added
- GPT-5.x / Codex 新口癖大批入库：庸医问诊腔（抠出来/揪出来、不靠猜）、暴力动作腔（补一刀、狠狠干、拍脑门、拍板）、AI 主动出击腔（要不要我、我立马开始、只要你回复我、顺手）等 30+ 条
- Tier 2 新增单音节命令词类别：补/接/核/进/顺/落/坏/跑
- SKILL.md 加入 repo 根目录，此前只在 Claude Code skill 目录
- SKILL.md v2.0.0：按处理方式分组（直接删除类 vs 替换为具体表达类），不按来源分类

### Changed
- README 全文重写：GPT-5.4 荒谬引文开头、血压升高类和暴力动词类专门示例
- 安装部分从 80 行缩到 13 行，详情推到 install/ 目录
- 短语计数统一为 bullet 数：中文 210+、英文 96（此前各文件数法不一致）
- phrases-en.md Tier 3 阈值对齐 severity.md（分段阈值替代 >3%）

### Fixed
- run-eval.md 硬编码本地路径改为相对路径
- 评测数据更新为 29 条（16 SF + 13 SNF），此前漏计 SF-16
- CHANGELOG、README、results、openclaw.md 数据全部对齐

## [1.3.0] - 2026-03-24 — 项目更名为「说人话」(shuorenhua)

### Renamed
- 项目名从 stop-slop-zh 更名为「说人话」(shuorenhua)
- README 全文重写，去掉 AI 味，加入 ChatGPT 5.4 工程师腔黑话作为传播亮点

### Tested
- GPT-5.4 Codex 评测：SF 通过率 14/15 (93%)，SF-16 待测；SNF 误杀率 0/13 (0%)
- 评测集扩展至 29 条（16 SF + 13 SNF）
- 评测结果归档：`evals/results-v1.3.0.md`

### Added
- 新规则 11：语域一致性检测 — 同段混搭 2+ 种语域（学术/口语/商业/工程/鸡汤）时标记
- 新规则 12：节奏量化检测 — 句长标准差锚点（AI ≈ 1.2 vs 人类 ≈ 4.7+）
- 新短语类别「工程师腔 / 调试腔」：稳稳兜住、落盘、收口、根因、打掉问题、收窄等 19 条
- 新短语类别「自媒体 / 小红书 AI 腔」：保姆级、绝绝子、谁懂啊、拆解、硬核等 17 条
- Tier 1 开场套话新增 5 条：不得不说、诚然、深入探讨、具体来说、更重要的是
- Tier 1 渲染性强调新增 7 条：毫不夸张、值得深思、令人深思、引发思考、颠覆性、范式转移等
- Tier 1 正能量收尾模板新类别：与其…不如…、只有…才能…、让我们拭目以待、未来可期
- Tier 1 过渡废话新增 4 条：本质上、核心在于、关键在于、由此可以看出
- Tier 2 连接词新增 5 条：恰恰、正是、无疑、由此可以看出、不外乎
- Tier 2 形容/修饰新增 3 条：可谓、堪称、追根溯源
- 结构反模式新增 5 种：#14 分条列点强迫症、#15 正能量收尾强迫症、#16 假口语化、#17 调试腔叙事、#18 句长均匀
- 评测集 SF 新增 5 条：SF-11 工程师腔、SF-12 小红书腔、SF-13 正能量收尾、SF-14 语域混搭、SF-15 句长均匀
- 评测集 SNF 新增 3 条：SNF-11 真人 debug 对话、SNF-12 真人博主网络用语、SNF-13 纯技术报告术语
- 误杀防护新增 2 条：技术报告中的工程术语、真人网络用语
- 改写示例新增 3 组：工程师腔、小红书腔、语域混搭

### Changed
- 5 维评分升级为 7 维评分：新增「语域」「具体」维度，每维增加量化锚点
- 评分阈值从 < 35 调整为 < 49（适配 7 维）
- 核心规则从 10 条扩展为 12 条
- severity.md Tier 1/Tier 2 典型词更新，反映新增分类
- phrases-zh.md 来源说明更新，加入 Linux.do / X / 即刻社区

## [1.2.0] - 2026-03-23

### Added
- Codex CLI installation guide (`install/codex.md`) with AGENTS.md, system prompt, and global instructions methods
- Codex quick start section in README

### Changed
- Moved Codex CLI content from `install/chatgpt.md` to dedicated `install/codex.md`

## [1.1.0] - 2026-03-23

### Added
- Scene-based routing: chat/status/docs/public-writing with minimal/standard/aggressive intensity levels
- Unsourced citation pattern detection (Chinese and English)
- 9 additional Chinese high-frequency AI phrases
- Misfire protection for technical system subjects
- Length-normalized thresholds for Tier 3 severity

### Changed
- Rules 3 (subject) and 5 (reader address) downgraded from hard constraints to heuristics
- Tier 1 severity: "always replace" changed to "replace by default, allow exceptions"
- Tier 3 severity: unified to length-normalized density thresholds
- Positive guidance: removed "allow tangents and half-formed thoughts", replaced with "allow casual tone without sacrificing completeness"
- Two-pass workflow now only enforced in aggressive mode

### Fixed
- Severity rules inconsistency between percentage-based and count-based thresholds
- Misfire protection now checked before Tier 1 replacement in decision flow

## [1.0.0] - 2026-03-23

### Added
- Initial release
- 10 core rules for AI writing pattern removal
- Bilingual banned phrase lists (Chinese 140+ entries, English 130+ entries)
- Chinese internet jargon coverage (赋能/闭环/抓手/etc.)
- Translation artifact detection (翻译腔)
- 13 cross-language structural anti-patterns
- 3-tier severity system with misfire protection
- 5-dimension self-evaluation scoring matrix
- Before/after examples in Chinese and English
- Two-pass workflow (rewrite + audit)
