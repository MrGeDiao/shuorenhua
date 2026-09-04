<h1 align="center">说人话：中文 AI 味清理 skill</h1>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" alt="说人话：中文 AI 味清理 skill — 先保信息，再谈风格" width="100%">
  </picture>
</p>

<p align="center">
  <strong>别让模型替你装腔。</strong>
</p>

<p align="center">
  <a href="https://github.com/MrGeDiao/shuorenhua/stargazers"><img src="https://img.shields.io/github/stars/MrGeDiao/shuorenhua?style=for-the-badge&amp;label=stars" alt="GitHub stars"></a>
  <a href="https://github.com/MrGeDiao/shuorenhua/releases"><img src="https://img.shields.io/github/v/release/MrGeDiao/shuorenhua?style=for-the-badge&amp;label=release" alt="GitHub release"></a>
  <a href="evals/benchmark.md"><img src="https://img.shields.io/badge/benchmark-120%20cases-2563eb?style=for-the-badge" alt="Benchmark: 120 cases"></a>
  <a href="evals/real-samples.md"><img src="https://img.shields.io/badge/scenario%20samples-20-16a34a?style=for-the-badge" alt="Scenario samples: 20"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/MrGeDiao/shuorenhua?style=for-the-badge" alt="License"></a>
</p>

<p align="center">
  <a href="#快速上手">快速上手</a> ·
  <a href="#改写原则与示例">改写原则</a> ·
  <a href="#规则与场景">规则与场景</a> ·
  <a href="#评测体系">评测</a> ·
  <a href="#安装方式">安装</a> ·
  <a href="#常见问题">FAQ</a>
</p>

`说人话` 是一个面向中文文本的改写 skill。主要用于清理 AI 起草内容中的模板套话、商业包装、工程师姿态腔、翻译腔和无依据的定性断言。适用于日常编写 README、Release Notes、工作同步、Issue 回复、论坛讨论及技术长文的开发者、维护者与写作者。

核心逻辑是**改写前先锁定事实**：原文中的数字指标、版本编号、命令参数、文件路径、因果条件与责任归属一律保留，只剔除多余的渲染与空洞铺垫。支持接入 Claude Code、Codex、Cursor、ChatGPT 及各类自建 Agent。

## 快速上手

- **网页直接体验（无需安装）**：使用 [说人话 GPT](https://chatgpt.com/g/g-6a5829b1163481919e1e45851f6bc709-shuo-ren-hua)（需 ChatGPT Plus / Pro），粘贴文本即可改写。
- **Claude Code**：在对话中执行以下命令安装插件：
  ```text
  /plugin marketplace add MrGeDiao/shuorenhua
  /plugin install shuorenhua@shuorenhua
  ```
  安装后输入「把这段去 AI 味」即可调用。手动安装及跟随更新说明见 [install/claude-code.md](install/claude-code.md)。
- **Codex**：克隆仓库后单次执行：
  ```bash
  git clone https://github.com/MrGeDiao/shuorenhua.git && cd shuorenhua
  codex exec -C . "读取 ./SKILL.md，按其中规则改写以下文本：……"
  ```
- **支持 `skills` 协议的 Agent**：
  ```bash
  npx skills add MrGeDiao/shuorenhua
  ```
- **仅审阅模式**：若只需排查问题而不希望直接修改正文，可在指令中附加「按 annotation mode 只标注不改写」。

更多接入方式（Cursor、Windsurf、OpenClaw 等）见[安装方式](#安装方式)。

## 改写原则与示例

去 AI 味的关键在于**在去杂质的同时不破坏原有事实链条**：

1. **数字与修饰绑定**：保留具体指标，不把「p95 延迟从 480ms 降至 160ms」粗暴概括为「明显优化」。
2. **事实关系不变**：不把「展示了云原生潜力」擅自改写为「已采用云原生架构」。
3. **要素完整**：条件、范围、否定、时态与强度均属于事实，不随语气一同删减。
4. **不脑补具体细节**：原文若只有抽象定性（如「提升效率」），不擅自推测扩充为「节省开发时间」。
5. **双向回读验证**：确保原文所有事实点在改写后均有对应，改写后的每个结论在原文均有出处。

### 改写对照

- **改写前**：
  > 本次优化在性能方面取得了显著成效，有效改善了接口响应问题，p95 延迟从 480ms 降到 160ms，充分体现了团队持续优化的能力。
- **过度删减（丢失事实）**：
  > 这次优化明显降低了接口延迟。*(丢失了 p95、480ms 与 160ms 核心指标)*
- **说人话改写**：
  > 这次优化把接口 p95 延迟从 480ms 降到 160ms。

此例对应评测集硬约束用例 [SF-46](evals/benchmark.md)。更多对比样本见 [references/examples.md](references/examples.md) 与 [evals/real-samples.md](evals/real-samples.md)，保护边界见 [references/protected-spans.md](references/protected-spans.md)。

## 规则与场景

执行流程固定：识别文本场景 → 锁定事实片段（数字/命令/责任主体）→ 判断问题强度 → 优先处理句式与段落结构（短语表仅作兜底）→ 双向保真回读 → 残留审计。

### 常见模式处理

| 识别信号 | 处理方式 | 示例 |
|---|---|---|
| 开场客套、总结提示 | 删除提示层，直接提供正文内容 | `好问题！让我来解释` → 直接回答 |
| 商业黑话、价值拔高 | 还原为具体操作；无实际信息则删除 | `赋能开发者` → 明确具体解决的操作 |
| 工程师姿态腔 | 替换为实际动作 | `把结论落盘` → `把结论写进文档` |
| 过度承接、情绪共情 | 删去评价与心理预设，聚焦客观事实 | `你不是敏感，你只是……` → 直接针对技术点回复 |
| 结构过满、翻译腔 | 简化连接词与从句嵌套，保留专业术语 | `基于……通过……来……` → 直陈动作与结果 |
| 动词名词化 | 还原为自然动词，保持统一指称 | `进行了优化` → `优化了` / `改了` |
| 无源权威断言 | 移除非自洽论断；技术文档中标注信息缺口 | 避免将无来源的 `40% 提升` 作为既定事实保留 |

完整边界定义见 [references/](references/)。

### 场景包（Scene Packs）

针对不同文体定制改写重心：

| 场景 | 改写重点 |
|---|---|
| **README** | 首屏快速说明项目用途、目标用户与解决的具体问题，避免空洞口号。 |
| **Release Note** | 明确罗列变更项、验证结果与使用限制，不写公关式发版宣言。 |
| **Forum Post** | 保留作者个人经历、技术判断与自然的社区讨论口吻。 |
| **Issue Reply** | 优先陈述复现情况、当前判断与下一步行动方案。 |
| **API Reference** | 严格保护 Endpoint、HTTP Method、参数字段、状态码及约束条件。 |
| **FAQ** | 优先给出明确结论；保留前置条件与风险警示，不后移步骤，不随意扩大承诺范围。 |

场景细则见 [references/scene-packs.md](references/scene-packs.md)。

### 长文力度控制（Scope）

针对篇幅较长的文本，可通过 `scope` 参数控制结构与句式的删改幅度：

- `structural`：允许跨句合并、删除与重排结构，适用于短文或明确要求大修的文稿。
- `bounded`（长文默认）：保留核心段落节奏，将疑似空话归入「建议删除（待确认）」清单，避免破坏结构。
- `in-place`：不删除整句，仅在句内做词汇替换与语气微调，严格保留原文排版。

演进记录与讨论见 [issue #4](https://github.com/MrGeDiao/shuorenhua/issues/4)，评测记录见 [evals/results-v1.8.6.md](evals/results-v1.8.6.md) 与 [evals/run-manifest.md](evals/run-manifest.md)。

## 评测体系

规则层覆盖 210+ 条中文短语、96 条英文短语及 25 类结构反模式。

### 数据集构成

当前评测集共 120 条：

| 类型 | 数量 | 目标 |
|------|------|------|
| SF | 63 | 应该改的文本要命中并处理主要问题 |
| SNF | 57 | 本来正常的文本应放行或只做轻提示 |
| 场景样本 | 20 | 整段样本按自然、保真、可直接发评分，长文另看长度节奏 |

120 条是主 benchmark，20 条场景样本单独评估，两者不相加。主 benchmark 含 21 条 Scene Pack 正反例、4 条 Long-form In-place 和 3 条 Bounded 样本。

- **HUMAN 长文对照（10 篇）**：涵盖 9 个作者组的中文原作与译作，用于长期观察自然写作中的假阳性（独立评估，不计入评测分母）。

### 验收门槛

| 级别 | 检查维度 | 判定标准 |
|---|---|---|
| **L1 硬约束** | 虚构事实、保护片段漂移、篡改归属、超出 scope | 必须为 0 失败（阻塞发布） |
| **SNF 误杀** | 对正常自然文本进行错误修改 | 误杀率低于 10%（阻塞发布） |
| **L2 风格目标** | 典型 AI 套路与冗余表达清理率 | 单独跟踪各模型清理趋势 |
| **L3 风格观察** | 编辑风格层面的合理差异表达 | 仅作记录，不设硬性门槛 |

评测通过匿名乱序的 [evals/benchmark-blind.md](evals/benchmark-blind.md) 配合硬指标校验脚本 `python3 automation/eval/hard_metrics.py --run <批次目录>/`（详见 [automation/eval/README.md](automation/eval/README.md)）运行。

最新发布验收数据见 [v2.4.1 评测记录](evals/results-v2.4.1.md)：全量 120 条双席位交叉判分，两席位 L1 违规均为 0，SNF 误杀 3.5% / 1.8%。上一版聚焦术语放行与 FAQ 警告保护的记录见 [v2.4.0 评测记录](evals/results-v2.4.0.md)，更早的全量基线见 [v2.3.1 评测记录](evals/results-v2.3.1.md)。

## 安装方式

### 平台指南

| 平台 | 接入文档 |
|---|---|
| Codex | [install/codex.md](install/codex.md) |
| Claude Code | [install/claude-code.md](install/claude-code.md) |
| Cursor / Windsurf | [install/cursor.md](install/cursor.md) |
| OpenClaw | [install/openclaw.md](install/openclaw.md) |
| ChatGPT / Custom GPT | [install/chatgpt.md](install/chatgpt.md) |

### 规格选择

| 入口 | 内容构成 | 适用场景 |
|---|---|---|
| **mini** | [`dist/shuorenhua-mini.md`](dist/shuorenhua-mini.md)（1,500 字符内，自包含） | 单次会话、Custom Instructions、上下文受限环境 |
| **lite** | `SKILL.md` 单文件 | 日常轻量改写与审稿 |
| **full** | `SKILL.md` + `references/` 完整规则集 | 长期工程项目、正式技术文档及防误杀要求高的场景 |

在团队工程项目中，可在 `AGENTS.md` 中配置规则引导 Agent 自动调用：

```markdown
## 写作风格
当任务涉及「去 AI 味」「说人话」「自然一点」「别像模板」这类改写时，遵循 `shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

## English

**shuorenhua (说人话)** is a Chinese-first rewrite skill for Codex, Claude Code, Cursor, ChatGPT, and custom agents. It removes common AI writing patterns in Chinese while protecting numbers, commands, attribution, conditions, and factual relations. The repo includes a 120-case benchmark, false-positive guards, scene-specific rules, and long-form scopes. The latest release is `v2.4.1`.

- **Claude Code**: Run `/plugin marketplace add MrGeDiao/shuorenhua` followed by `/plugin install shuorenhua@shuorenhua`.
- **Other Agents**: Run `npx skills add MrGeDiao/shuorenhua`.
- Detailed setup guides: [install/](install/).

<sub>关键词 / keywords：中文 AI 写作、中文 humanizer、去 AI 味、AI writing humanizer、Chinese writing style</sub>

## 常见问题

### 是否用于规避 AI 内容检测？
不是。该项目专注于清理文本中的模板化表达、公关腔调与生硬句式，提升可读性与准确度，不以绕过检测算法为设计目标。

### 是否支持英文文本改写？
支持，但以中文优化为主。英文规则主要用于清理常见英文套话以及中英文混排时的结构冗余。

### 为什么部分文本改写后仍感觉不够生动？
本工具定位为规则驱动的冗余清理与保真纠偏，侧重清除通用套路，不包含对特定作者个人文风的拟合。

### 处理技术文档时是否有误改风险？
在 `docs`、`status` 与 `code-context` 场景下采用更严格的保护策略，重点锁定命令、路径、版本、报错与性能数据。若在实际使用中发现误改，欢迎提交脱敏样本。

## 参与贡献

欢迎提交实际使用中遇到的 Bad Case、改写对照及误杀记录。

- 提交时请使用 [Bad Case 模板](.github/ISSUE_TEMPLATE/bad-case.md) 或直接提交至 [征集 Issue #5](https://github.com/MrGeDiao/shuorenhua/issues/5)。
- **注意脱敏**：请勿包含未授权对话、账号密钥、内部内网链接或个人隐私信息。
- 新增词条前请确认其代表了新的表达模式，而非已有规则的简单同义词。具体贡献规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 相关项目

- [stop-slop](https://github.com/hardikpandya/stop-slop) — 英文 AI 冗余表达规则与评估框架
- [humanizer](https://github.com/blader/humanizer) — 英文 AI 模式分类体系
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — AI 写作问题分类与严重度参考
- [speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw) — 繁体中文去 AI 味规则

## Star 增长

[![「说人话」star 增长曲线](https://raw.githubusercontent.com/MrGeDiao/shuorenhua/star-data/star-growth.svg)](https://github.com/MrGeDiao/shuorenhua/stargazers)

## 许可

[MIT](LICENSE)
