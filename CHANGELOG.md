# Changelog

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

## [1.8.1] - 2026-04-27 — Knowledge Architecture / 项目知识架构收口

### Changed
- `README.md` 更新项目状态和快速开始入口，把公开信息架构收口到当前已发布能力
- `install/codex.md` 和 `evals/run-eval.md` 切换到当前 Codex CLI 的 `codex exec` 用法，避免旧命令继续作为主入口传播
- `install/chatgpt.md` 去掉易漂移的 reference 文件数量，改为按目录上传完整知识文件

### Framing
- 本版定位为项目知识架构收口：让新用户能从 README 进入使用路径，让评测和安装入口保持同一套事实基线
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
