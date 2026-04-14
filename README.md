<p align="center">
  <img src="assets/icon.png" alt="说人话 icon" width="140">
</p>

<h1 align="center">说人话</h1>

<p align="center">
  把 AI 写出来的中文，改回当前场景里一个正常人会怎么说。
</p>

<p align="center">
  面向 Codex、Claude Code、ChatGPT 等工具的 rewrite skill。
  <br>
  重点处理中文 AI 味、工程师腔、小红书 AI 腔和翻译腔，也兼顾英文套话和结构反模式。
</p>

<p align="center">
  <a href="https://github.com/MrGeDiao/shuorenhua/stargazers"><img src="https://img.shields.io/github/stars/MrGeDiao/shuorenhua?style=social" alt="GitHub stars"></a>
  <a href="https://github.com/MrGeDiao/shuorenhua/releases"><img src="https://img.shields.io/github/v/release/MrGeDiao/shuorenhua" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/MrGeDiao/shuorenhua" alt="License"></a>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#效果">前后对比</a> ·
  <a href="#覆盖范围">覆盖范围</a> ·
  <a href="#怎么工作">工作方式</a> ·
  <a href="#项目结构">项目结构</a>
</p>

> 我已经把差异**收窄**了，**根因**基本**坐实**，和我刚**抓到的现象**也**对上了**。接下来做一个**更硬的排除法**，**稳稳兜住**，**落盘**之后就能**收口**了。

这是 AI 跟你说的“人话”。没有一个正常人会这么聊天。

`说人话` 不是敏感词替换器，也不是把句子润色得更华丽。它只做一件事：

> **把“像模型在表演写作”的文本，改回自然、可信、可发布的人话。**

## 一眼看懂

| 如果你遇到的是 | 它会怎么处理 |
|---|---|
| 套话太多、腔调太满 | 先砍姿态层，尽量保住信息层 |
| 工程师腔跑进日常表达 | 把 incident report 口吻拉回正常中文 |
| 小红书 AI 腔、翻译腔、宣传腔 | 压低模板感，不硬拗 voice |
| 文档、状态更新、代码上下文 | 优先保护事实、术语、参数和语域 |

## 它主要抓什么

旧的 AI 味你已经认识：`赋能`、`闭环`、`在当今快速发展的时代`。这些已经被骂了一年，新模型学乖了，换了一套。

现在更常见的是一种“会说黑话的实习经理”口吻：把 debug 术语塞进日常对话，把执行姿态演得很满，再顺手补一段推销式热情。

| 类型 | 常见表现 | 它会做什么 |
|------|----------|------------|
| 工程师腔 / SRE 腔 | `收窄` `坐实` `兜住` `收口` | 保留排查信息，去掉表演化术语 |
| 执行力表演 | `狠狠干` `补一刀` `拍脑门` `揪出来` | 改成具体动作，不演 |
| 推销式助手腔 | `只要你回复我我立马开始` | 去掉无效催促，直接办事 |
| 小红书 AI 腔 | `姐妹们` `保姆级` `谁懂啊` `狠狠` | 降低密度，保留场景需要的口语 |
| 翻译腔 / narrator 腔 | `基于……来……` `通过……进行……` | 改成更直接的中文句式 |

最让人血压升高的是这类：

> **要不要我**帮你把剩下的也改了？**只要你回复我**，**我立马开始**。**你就确认一点**，**你一回复我就**上手。

没人问你。做就做，别推销。这批新口癖已经全部收录。

## 效果

### 示例 1：公开介绍

**改写前**

> 在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。

**改写后**

> AI 工具很多，真正能帮开发者把活做快、做稳的并不多。这个项目做的，就是把模型写出来的套话和表演感压下去，让结果更像人写的。

### 示例 2：工程师腔

**改写前**

> 我已经把差异收窄了，根因基本坐实，和刚抓到的现象也对上了。接下来做一个更硬的排除法，稳稳把问题兜住，落盘之后就能收口了。

**改写后**

> 我已经把排查范围缩小了，原因也基本确认了，和刚看到的现象一致。接下来再排查一轮，把问题解决掉，结论记下来就行。

### 示例 3：只做诊断

```text
先不要改写，只按 annotation mode 标出下面这段文字里的问题：...
```

适合审稿、review，或者你还不想让 AI 直接替你改稿的时候。

更多示例见 [references/examples.md](references/examples.md)。

---

## 覆盖范围

210+ 中文短语。96 条英文短语。19 类结构反模式。按场景自动调强度：聊天时只动套话，写博客时全规则扫描，不会把正常的技术报告改得面目全非。

英文去 AI 味已经有 [stop-slop](https://github.com/hardikpandya/stop-slop) 和 [humanizer](https://github.com/blader/humanizer)，中文一直没有。这个项目补上了。

| 能力 | stop-slop | humanizer | **说人话** |
|------|-----------|-----------|-----------|
| 中文禁用短语 | - | - | 210+ 条 |
| 互联网黑话 | - | - | ✅ |
| 工程师腔 / SRE 腔 | - | - | ✅ |
| 小红书 AI 腔 | - | - | ✅ |
| 翻译腔 | - | - | ✅ |
| 语域混搭检测 | - | - | ✅ |
| 节奏量化 | - | - | ✅ |
| 场景分档 | - | - | 4 × 3 |
| 误杀防护 | - | - | ✅ |
| 英文禁用短语 | ✅ | ✅ | 96 条 |
| 结构反模式 | ✅ | 部分 | 19 种 |

---

## 怎么工作

`说人话` 不是见词就替换，而是先判断场景和风险，再决定改写力度。

1. 先判场景
2. 再划 protected spans，确认哪些内容不能动
3. 再判问题强度（Tier）
4. 再决定改写档位
5. 先按模式处理，再按正向目标和词条兜底
6. 先做保真回读：检查 protected spans、保真、语域、术语和断裂感
7. 再按需做 Residual Audit：只查开场残留、总结残留、narrator 残留、空泛判断残留、句长过匀

核心原则只有一句话：

> **先保信息，再谈风格。**

### 场景 × 强度

| 场景 | 强度 | 干什么 |
|------|------|--------|
| 聊天 | 轻 | 只砍套话，保留口语感 |
| 技术摘要 | 中 | 砍套话 + 渲染词，默认先保真，再决定要不要 second pass |
| 文档 | 中 | 技术表达优先，second pass 更保守 |
| 博客/社交 | 重 | 全规则 + Residual Audit |

### Protected Spans

改写前先保护这些不能乱动的内容：

- 数字、日期、区间、单位、版本号
- 人名、组织名、责任归属
- 引号内原文
- 命令、代码、路径、参数、字段、配置项
- 报错、状态码、指标和度量关系

### Positive Style Contract

不只删套话，也定义“更像人”的正向目标：

- 具体动作优先于抽象拔高
- 真主语和真动作优先于姿态层
- 允许轻微不对称，不把每句都抛光成同一种腔
- 按 `chat / status / docs / public-writing` 分场景校准

---

## 评测

当前 benchmark 共 51 条（30 条该改 + 21 条不该误杀）。

覆盖：套话清理、工程师腔、小红书 AI 腔、无源引用、fact preservation、protected spans、代码上下文保护、Residual Audit / 二次审稿，以及真实技术文本误杀防护。

当前用例集见 [evals/benchmark.md](evals/benchmark.md)。本轮结果见 [evals/results-v1.7.1.md](evals/results-v1.7.1.md)，历史归档可参考 [evals/results-v1.5.0.md](evals/results-v1.5.0.md)。

---

## 快速开始

```bash
git clone https://github.com/MrGeDiao/shuorenhua.git
```

### 方式 1：Codex 单次使用

```bash
codex --system-prompt "$(cat SKILL.md)" "改写以下文本：..."
```

只做诊断：

```bash
codex --system-prompt "$(cat SKILL.md)" "先不要改写，只按 annotation mode 标出下面这段文字里的问题：..."
```

### 方式 2：项目内长期使用（推荐）

把 `SKILL.md` 和 `references/` 放进项目，在 `AGENTS.md` 中声明触发条件：

```markdown
## 写作风格
当任务涉及"去 AI 味""说人话""自然一点""别像模板"这类改写时，遵循 `shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

### 方式 3：ChatGPT / Custom GPT / Projects

可以直接使用已有 GPT，也可以自建 Custom GPT，或者在 Project 里上传 `SKILL.md` + `references/`。详见 [install/chatgpt.md](install/chatgpt.md)。

### 其他平台

[Codex](install/codex.md) · [Claude Code](install/claude-code.md) · [Cursor / Windsurf](install/cursor.md) · [OpenClaw](install/openclaw.md) · [ChatGPT](install/chatgpt.md)

---

## Lite 模式和 Full 模式

### Lite 模式

只加载 `SKILL.md`。适合临时改一段话、快速验证、场景简单的时候。

### Full 模式

加载 `SKILL.md` + `references/`。适合 AI 味比较重、中英文混写、需要更稳的误杀防护和事实保真、docs / status / code-context 这些保守场景。

> `SKILL.md` 是兜底入口，不等于完整模式。只加载一个文件，效果会明显弱于完整模式。

---

## 它会优先改什么

### 常见会处理的

- `值得注意的是` `综上所述` `总的来说` `归根结底`
- `研究表明`（但没来源）
- `赋能 / 闭环 / 抓手`
- `收窄 / 坐实 / 兜住 / 收口`
- `姐妹们 / 保姆级 / 绝绝子 / 建议收藏`
- `Great question!` `Let's dive in!` `serves as a testament` `cutting-edge` `leverage`

### 常见不会乱动的

- 引用原文、RFC / 论文 / 规范里的原句
- 代码、命令、配置、日志、报错
- 参数名、字段名、路径
- 系统主语的正常技术描述
- 学术语体里的合理被动语态
- 有具体参数、动作和结果支撑的真实工程讨论

---

## 什么时候它效果会一般

### 1. 你只加载了 `SKILL.md`

能做基础清理，但不会有完整的场景判断和精细误杀防护。

### 2. 原文的问题不是"套话太多"，而是"没有作者自己的声音"

当前版本更擅长去掉明显 AI 痕迹，还不够擅长贴近"你本人会怎么说"。

### 3. 你在非常保守的场景里用它

技术文档、status、code-context 这些场景默认更克制，结果可能"更干净"但不一定"更活"。

### 4. 原文本身就太空

没有具体信息的文本，`说人话` 不会凭空替你发明细节。它最多能把空洞表达压低，但不能把没有内容的文本改成有内容。

---

## 无源引用处理

内置 3 种模式：

- `rewrite-safe` — 删掉无证据的权威铺垫
- `audit-only` — 只指出缺来源，不直接改
- `rewrite-with-placeholder` — 改写并标记需要补源

---

## 项目结构

```text
shuorenhua/
├── SKILL.md               # 规则 + 工作流 + 评分
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── evals/
│   ├── benchmark.md        # 评测集（51 条）
│   ├── run-eval.md         # 评测指令
│   ├── results-v1.3.0.md
│   ├── results-v1.4.3.md
│   └── results-v1.5.0.md
├── install/
│   ├── codex.md
│   ├── claude-code.md
│   ├── cursor.md
│   ├── openclaw.md
│   ├── chatgpt.md
│   └── chatgpt-gpt-instructions.md
├── references/
│   ├── examples.md         # 改写示例
│   ├── operation-manual.md
│   ├── positive-style.md   # 正向风格目标
│   ├── phrases-en.md       # 英文禁用短语（96 条）
│   ├── phrases-zh.md       # 中文禁用短语（210+ 条）
│   ├── protected-spans.md  # 不可改写片段
│   ├── scene-guardrails.md
│   ├── severity.md
│   ├── structures.md       # 19 种结构反模式
│   └── boundary-cases.md
└── LICENSE                 # MIT
```

核心只需要 `SKILL.md` 一个文件。`references/` 让场景判断、正向改写目标和事实保真更稳，按需加载。

---

## FAQ

### 这是不是拿来骗 AI detector 的？

不是。目标是减少模板感、表演感和语域漂移，让文本更自然、更可发布，不是绕过检测。

### 会不会把技术内容改坏？

默认不会。代码、参数、日志、命令、系统主语、术语、引用原文都在优先保护范围内。

### 英文能不能用？

可以，但这是一个 **中文优先** 项目。英文支持是有的，主要价值在中文场景。

### 为什么改完有时还是有 AI 味？

因为"去掉明显套路"不等于"拥有具体作者的 voice"。当前版本更擅长清理，不够擅长拟合你的个人表达，这也是后续迭代重点。

### 我应该什么时候用 annotation mode？

当你还不确定该不该改、想先 review 再决定、处在 docs / status 这种保守场景、或者怀疑有无源引用和误杀风险的时候。

---

## 贡献

欢迎提交新 benchmark、边界案例、真实 bad case、改写前后样本、新的误杀防护。

在提交新词之前，先想一件事：

> 这是一个"新模式"，还是只是"现有模式的变体"？

详细规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 致谢

- [humanizer](https://github.com/blader/humanizer) — AI 模式分类
- [stop-slop](https://github.com/hardikpandya/stop-slop) — 规则 + 评分框架
- [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 中文去 AI 味
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — 严重度分级

## 社区

在 [Linux.do](https://linux.do) 发现这个项目？欢迎来聊。

## 许可

[MIT](LICENSE)
