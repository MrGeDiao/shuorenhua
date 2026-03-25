# Changelog

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
