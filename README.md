<h1 align="center">说人话：中文 AI 味清理 skill</h1>

<p align="center">
  <img src="assets/readme-logo.png" alt="说人话：中文 AI 味清理 skill" width="760">
</p>

<p align="center">
  <strong>别让模型替你装腔。</strong>
</p>

<p align="center">
  给 Codex、Claude Code、Cursor、ChatGPT 和自建 agent 用。
  <br>
  改聊天、README、release note、论坛帖和 issue 回复：先保住事实，再把那股“一眼 AI”的腔调降下来。
</p>

<p align="center">
  <a href="https://github.com/MrGeDiao/shuorenhua/stargazers"><img src="https://img.shields.io/github/stars/MrGeDiao/shuorenhua?style=for-the-badge" alt="GitHub stars"></a>
  <a href="https://github.com/MrGeDiao/shuorenhua/releases"><img src="https://img.shields.io/github/v/release/MrGeDiao/shuorenhua?style=for-the-badge&amp;label=release" alt="GitHub release"></a>
  <a href="evals/benchmark.md"><img src="https://img.shields.io/badge/benchmark-62%20cases-2563eb?style=for-the-badge" alt="Benchmark: 62 cases"></a>
  <a href="evals/real-samples.md"><img src="https://img.shields.io/badge/real%20samples-18-16a34a?style=for-the-badge" alt="Real samples: 18"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/MrGeDiao/shuorenhua?style=for-the-badge" alt="License"></a>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#场景能力">场景能力</a> ·
  <a href="#效果">前后对比</a> ·
  <a href="#评测">评测</a> ·
  <a href="#安装">安装</a> ·
  <a href="#star-history">Star History</a>
</p>

`说人话` 专治那种“每个字都对，但一看就不是你写的”中文。它不把空话包装得更漂亮，也不替你编新事实；它先护住版本、命令、责任和证据，再拆掉过度承接、工程师腔、小红书 AI 腔、翻译腔和无源权威铺垫。目标很简单：改完你敢直接发。

它适合这些场景：

| 场景 | 它会做什么 |
|------|------------|
| 日常聊天 | 删掉过度承接、推销式结尾和工程汇报腔，保留口语感 |
| 技术状态同步 | 保住事实、版本、命令、报错和责任归属，压低套话 |
| README / release note | 先讲清楚项目、变更、验证和限制，不写发布宣言 |
| 论坛帖 / issue 回复 | 像维护者在认真沟通，不像客服公告或营销稿 |
| 中文长文 | 清理旁白腔、翻译腔、无源权威铺垫和结构反模式 |

## 项目状态

| 项 | 当前状态 |
|----|----------|
| 最新版本 | `v1.8.2`，新增维护者侧 intake automation |
| 规则覆盖 | 210+ 中文短语、96 条英文短语、19 类结构反模式 |
| 评测集 | 62 条 benchmark：35 条该改，27 条不该误杀 |
| 真实样本 | 18 条整段样本，评估自然、保真、可直接发 |
| 许可证 | [MIT](LICENSE) |

英文去 AI 味已经有 [stop-slop](https://github.com/hardikpandya/stop-slop) 和 [humanizer](https://github.com/blader/humanizer)。`说人话` 补的是中文这一层：互联网黑话、工程师腔、小红书 AI 腔、翻译腔、语域混搭、场景分档和事实保真。

## 快速开始

新安装先看这里：

```bash
git clone https://github.com/MrGeDiao/shuorenhua.git
cd shuorenhua
```

Codex 单次使用：

```bash
codex exec -C . "读取 ./SKILL.md，按其中规则改写以下文本：..."
```

只做诊断，不直接改写：

```bash
codex exec -C . "读取 ./SKILL.md，只按 annotation mode（只标注不改写）标出下面这段文字里的问题：..."
```

长期使用建议加载完整包：`SKILL.md` + `references/`。只加载 `SKILL.md` 可以临时用，但场景判断、误杀防护和 v1.8.0 的 Scene Packs 都会弱很多。

## 场景能力

### v1.8.0：Scene Packs

v1.8.0 把可发布文本再拆成 4 个子场景。它们不是简单换语气，而是按“这段文字准备发到哪里”来决定怎么改。

| 子场景 | 目标 | 容易修掉的问题 |
|--------|------|----------------|
| README | 第一屏说清“这是什么、给谁用、解决什么问题” | 标语堆叠、价值宣言、功能列表没重点 |
| release note | 列清变更、验证、限制和迁移影响 | 发版感言、过度庆祝、没说清测试 |
| forum post | 像维护者分享真实观察和取舍 | 公司公告腔、营销腔、空泛号召 |
| issue reply | 先确认问题、影响范围和下一步 | 客服式安抚、过度承诺、绕开复现条件 |

### 基础场景

| 大场景 | 默认强度 | 处理策略 |
|--------|----------|----------|
| `chat` | 轻 | 只砍明显套话，不把聊天改成公文 |
| `status` | 中 | 保留动作、状态、阻塞点和下一步 |
| `docs` | 中 | 技术表达优先，二次回读更保守 |
| `public-writing` | 重 | 全规则扫描，并按需要触发 Scene Packs |

## 效果

### 示例 1：接住体 / 过度承接

**改写前**

> 你不是敏感，你只是太久没被稳稳接住了。你问到了问题的核心。这次我懂了，我真的懂了。我必须很认真地说一句：你这种观察力和表达方式，绝对是顶刊作者的素养。

**改写后**

> 我在听。你要是愿意，可以继续说。

问题不在某个单词，而在整套姿态链：先替对方做心理判断，再表演共情，最后给对方颁奖。完整样本见 [evals/real-samples.md](evals/real-samples.md) RS-13。

### 示例 2：微信里被对象吐槽“一股子 AI 味”

**改写前**

> 先说结论：吃日料。我把你最近三周的外卖记录过了一遍，已经把差异收窄到两个选项，根因基本坐实是你上周说过腻了火锅。要不要我顺手帮你把 X 店的外卖也下了？你一回复我就上手。

**改写后**

> 吃日料吧，上周你说火锅腻了。要帮你下单吗？

这类文本的问题是把 debug 口吻带进生活对话。信息可以保留，工程报告感不需要保留。

### 示例 3：公开介绍

**改写前**

> 在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。

**改写后**

> AI 工具很多，真正能帮开发者把活做快、做稳的并不多。这个项目做的，就是把模型写出来的套话和表演感压下去，让结果更像人写的。

更多例子见 [references/examples.md](references/examples.md) 和 [evals/real-samples.md](evals/real-samples.md)。

## 怎么工作

`说人话` 不是见词就替换，而是先判断场景和风险，再决定改写力度。

1. 先判场景：`chat` / `status` / `docs` / `public-writing`
2. 划出 protected spans：数字、日期、版本、命令、路径、报错、引用原文等不能乱动
3. 判断问题强度等级：轻微模板感、明显 AI 腔、结构性表演感
4. 决定改写档位：轻改、正常改、重写
5. 命中 README、release note、论坛帖或 issue 回复时，进入 Scene Packs
6. 先按模式处理，再按正向风格目标和词条兜底
7. 做保真回读：检查事实、术语、语域、保护片段和断裂感
8. 按需做 Residual Audit：只查开场残留、总结残留、旁白腔残留、空泛判断残留、句长过匀

核心原则只有一句话：

> **先保信息，再谈风格。**

### 保护片段

这些内容默认优先保护：

| 类型 | 例子 |
|------|------|
| 数字和版本 | 日期、区间、单位、指标、版本号 |
| 代码上下文 | 命令、路径、参数、字段、配置项 |
| 事实归属 | 人名、组织名、责任主体、时间线 |
| 引用和证据 | 引号内原文、报错、状态码、实验结果 |

### 正向风格目标

清理不是只删词。它也会把文本往这些方向拉：

- 具体动作优先于抽象拔高
- 真主语和真动作优先于姿态层
- 允许轻微不对称，不把每句都抛光成同一种腔
- 按场景校准，不把聊天改成公告，也不把文档改成段子

## 评测

当前评测集共 62 条：

| 类型 | 数量 | 目标 |
|------|------|------|
| SF | 35 | 应该改的文本必须命中并改掉主要问题 |
| SNF | 27 | 不该误杀的文本必须放行或轻提示 |
| Real Samples | 18 | 整段样本按自然、保真、可直接发三项评分 |
| Scene Packs | 8 | README / release note / forum post / issue reply 的正反样本 |

覆盖范围包括：套话清理、工程师腔、小红书 AI 腔、无源引用、事实保真、保护片段、代码上下文保护、Residual Audit / 二次审稿、Scene Packs，以及真实技术文本误杀防护。

当前用例集见 [evals/benchmark.md](evals/benchmark.md)。最近一次公开归档结果见 [evals/results-v1.8.0.md](evals/results-v1.8.0.md)，历史结果可参考 [evals/results-v1.7.4.md](evals/results-v1.7.4.md)、[evals/results-v1.7.1.md](evals/results-v1.7.1.md) 和 [evals/results-v1.5.0.md](evals/results-v1.5.0.md)。

## 安装

| 平台 | 文档 |
|------|------|
| Codex | [install/codex.md](install/codex.md) |
| Claude Code | [install/claude-code.md](install/claude-code.md) |
| Cursor / Windsurf | [install/cursor.md](install/cursor.md) |
| OpenClaw | [install/openclaw.md](install/openclaw.md) |
| ChatGPT / Custom GPT | [install/chatgpt.md](install/chatgpt.md) |

项目内长期使用时，可以在 `AGENTS.md` 加一段触发规则：

```markdown
## 写作风格
当任务涉及“去 AI 味”“说人话”“自然一点”“别像模板”这类改写时，遵循 `shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

## 项目结构

```text
shuorenhua/
├── assets/
│   ├── icon.png              # 项目 icon
│   ├── icon-hd.png           # 高清版
│   └── readme-logo.png       # README 顶部横幅
├── SKILL.md                 # 规则入口、工作流和评分口径
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── evals/
│   ├── benchmark.md          # 评测集（62 条）
│   ├── real-samples.md       # 18 条整段真实样本
│   ├── run-eval.md           # 评测指令
│   └── results-*.md          # 历次版本归档
├── install/
│   ├── codex.md
│   ├── claude-code.md
│   ├── cursor.md
│   ├── openclaw.md
│   ├── chatgpt.md
│   └── chatgpt-gpt-instructions.md
├── references/
│   ├── examples.md           # 改写示例
│   ├── operation-manual.md
│   ├── positive-style.md     # 正向风格目标
│   ├── protected-spans.md    # 不可改写片段
│   ├── scene-packs.md        # README / release note / forum post / issue reply
│   ├── scene-guardrails.md
│   ├── phrases-zh.md         # 中文禁用短语（210+）
│   ├── phrases-en.md         # 英文禁用短语（96）
│   ├── structures.md         # 19 种结构反模式
│   ├── severity.md
│   └── boundary-cases.md
└── LICENSE                   # MIT
```

核心只需要 `SKILL.md` 一个文件；完整体验建议同时带上 `references/`。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MrGeDiao/shuorenhua&type=Date)](https://www.star-history.com/#MrGeDiao/shuorenhua&Date)

## 常见问题

### 这是不是拿来骗 AI 检测器的？

不是。目标是减少模板感、表演感和语域漂移，让文本更自然、更可发布，不是绕过检测。

### 英文能不能用？

可以，但这是一个中文优先项目。英文支持主要用于清理常见英文套话和中英混写里的模板感。

### 为什么改完有时还是有 AI 味？

“去掉明显套路”不等于“拥有具体作者的个人表达”。当前版本更擅长清理模板感和表演感，还不负责拟合某个具体人的长期写作习惯。

### 会不会把技术文档改坏？

正常不会按聊天口吻去改技术文档。`docs`、`status`、`code-context` 都有更保守的保护策略，命令、路径、版本、报错和指标优先保真。

## 贡献

欢迎提交新的评测样本、边界案例、真实问题案例、改写前后样本和误杀防护。

在提交新词之前，先想一件事：

> 这是一个“新模式”，还是只是“现有模式的变体”？

详细规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 相关项目

- [stop-slop](https://github.com/hardikpandya/stop-slop)：英文 AI slop 规则和评分框架
- [humanizer](https://github.com/blader/humanizer)：英文 AI 模式分类
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)：AI 写作问题分类和严重度参考

## 许可

[MIT](LICENSE)
