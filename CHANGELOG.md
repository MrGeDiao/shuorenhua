# Changelog

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
- `SKILL.md` frontmatter 去掉远端同步带来的 `metadata` 字段，收口成当前本地 skill 规范可稳定使用的形式

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
