# 说人话 (shuorenhua)

> Chinese-first rewrite skill for removing AI writing patterns while preserving facts, terminology, and technical context.

![GitHub stars](https://img.shields.io/github/stars/MrGeDiao/shuorenhua?style=social)
![GitHub release](https://img.shields.io/github/v/release/MrGeDiao/shuorenhua)
![License](https://img.shields.io/github/license/MrGeDiao/shuorenhua)

`说人话` 是一套给 Codex、Claude Code、ChatGPT 等工具使用的 rewrite skill。  
它不追求把文本改得更油滑，也不是简单的“敏感词替换器”。它做的事更明确：

> **把“像模型在表演写作”的文本，改回当前场景里一个正常人会怎么说。**

它主要处理：

- 开场套话
- 总结式收尾
- 商业黑话
- 工程师表演腔
- 小红书式 AI 腔
- narrator 腔
- 翻译腔
- 语域混搭
- 无源引用
- 句长过于均匀的模板感

同时尽量保住：

- 事实
- 术语
- 责任主体
- 代码、日志、命令、参数、路径等技术上下文

---

## 为什么会有这个项目

中文 AI 写作的问题，不只是 `赋能 / 闭环 / 值得注意的是` 这些老套话。

新模型还会写出另一类更隐蔽的“AI 味”：

- **工程师表演腔**：`收窄 / 根因 / 坐实 / 兜住 / 收口`
- **小红书 AI 腔**：`保姆级 / 绝绝子 / 建议收藏 / 划重点`
- **narrator 腔**：不停解释“我现在要开始解释了”
- **价值拔高骨架**：`不是……而是……`、`真正的 X 不是……而是……`
- **翻译腔**：`基于……来……`、`通过……进行……`

`说人话` 的目标不是把所有文本都改成口语，而是：

- 在 **chat** 里别端着
- 在 **status** 里别说套话
- 在 **docs** 里别假装有洞见
- 在 **public-writing** 里别写得像 AI 在发公告

---

## 它适合什么场景

- “去 AI 味”
- “自然一点”
- “别像模板”
- “别太像 ChatGPT”
- “先帮我看哪里不自然”
- “只标问题，不直接改写”
- “技术文案别太像 PR 稿”
- “公开帖别一眼 AI”

---

## 快速示例

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

更多示例见 `references/examples.md`。

---

## 当前能力

### 1. 中文优先的规则覆盖

- 210+ 中文短语
- 96 英文短语
- 19 类结构反模式

### 2. 场景路由

- `chat`
- `status`
- `docs`
- `public-writing`

### 3. 改写强度

- `minimal`
- `standard`
- `aggressive`

### 4. 标注模式

支持 `annotation mode`：

- 只指出问题
- 不直接重写全文
- 适合审稿和保守场景

### 5. 无源引用处理

内置 3 种模式：

- `rewrite-safe`
- `audit-only`
- `rewrite-with-placeholder`

### 6. code-context 保护

对以下内容默认更保守：

- 代码
- docstring
- 注释
- commit message
- 命令
- 配置
- 路径
- 参数名
- 报错信息

### 7. Protected spans

会先保护这些承载事实的片段，再决定怎么改写周围句子：

- 数字、日期、区间、单位、版本号
- 人名、组织名、责任归属
- 引号内原文
- 命令、代码、路径、参数、字段、配置项
- 报错、状态码、指标和度量关系

### 8. Positive Style Contract

不只删套话，也定义“更像人”的正向目标：

- 具体动作优先于抽象拔高
- 真主语和真动作优先于姿态层
- 允许轻微不对称，不把每句都抛光成同一种腔
- 按 `chat / status / docs / public-writing` 分场景校准

---

## 快速开始

## 方式 1：Codex 单次使用

```bash
codex --system-prompt "$(cat SKILL.md)" "改写以下文本：..."
```

只做诊断：

```bash
codex --system-prompt "$(cat SKILL.md)" "先不要改写，只按 annotation mode 标出下面这段文字里的问题：..."
```

## 方式 2：项目内长期使用（推荐）

把 `SKILL.md` 和 `references/` 放进项目，在 `AGENTS.md` 中声明触发条件。

例如：

```markdown
## 写作风格
当任务涉及“去 AI 味”“说人话”“自然一点”“别像模板”这类改写时，遵循 `shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

## 方式 3：ChatGPT / Custom GPT / Projects

如果你用 ChatGPT：

- 可以直接使用已有 GPT
- 也可以自建 Custom GPT
- 或者在 Project 里上传 `SKILL.md` + `references/`

详细说明见 `install/chatgpt.md`。

---

## Lite 模式和 Full 模式

### Lite 模式

只加载 `SKILL.md`。

适合：

- 临时改一段话
- 想快速验证是否接上
- 场景比较简单

### Full 模式

加载 `SKILL.md` + `references/`。

适合：

- AI 味比较重
- 中英文混写
- 需要更稳的误杀防护和事实保真
- docs / status / code-context
- 你想要更细的场景判断

> `SKILL.md` 是兜底入口，不等于完整模式。  
> 如果你只加载一个文件，效果可能会明显弱于完整模式。

---

## 它怎么工作

`说人话` 不是见词就替换，而是按下面的顺序处理：

1. 先判场景
2. 再划 protected spans，确认哪些内容不能漂
3. 再判问题强度（Tier）
4. 再决定改写档位
5. 先按模式处理，再按正向目标和词条兜底
6. 最后回读：检查 protected spans、保真、语域、术语和断裂感

核心原则只有一句话：

> **先保信息，再谈风格。**

---

## 它会优先改什么

### 常见会处理的内容

- `值得注意的是`
- `综上所述`
- `总的来说`
- `归根结底`
- `研究表明`（但没来源）
- `赋能 / 闭环 / 抓手`
- `收窄 / 坐实 / 兜住 / 收口`
- `姐妹们 / 保姆级 / 绝绝子 / 建议收藏`
- `Great question!`
- `Let's dive in!`
- `serves as a testament`
- `cutting-edge`
- `leverage`

### 常见不会乱动的内容

- 引用原文
- RFC / 论文 / 规范里的原句
- 代码、命令、配置、日志、报错
- 参数名、字段名、路径
- 系统主语的正常技术描述
- 学术语体里的合理被动语态
- 有具体参数、动作和结果支撑的真实工程讨论

---

## Benchmark

当前 benchmark 覆盖：

- `short`
- `long`
- `mixed`
- `code-context`

并分成两类：

- **Should Fix**：该改的必须改
- **Should Not Fix**：不该改的不能误杀

适合验证的能力包括：

- 套话清理
- 工程师腔
- 小红书 AI 腔
- 无源引用
- fact preservation / protected spans
- 代码上下文保护
- 真实技术文本误杀防护

当前仓库里的 benchmark 矩阵共有 `46` 条。
最新归档结果见：

- `evals/results-v1.5.0.md`

这个结果对应的是 `v1.5.0` 时的 `37` 条矩阵，记录为：

- SF 通过率：`21/21 (100%)`
- SNF 误杀率：`0/16 (0%)`

评测文件见：

- `evals/benchmark.md`
- `evals/run-eval.md`

---

## 什么时候它效果会一般

这是一个很重要的问题，建议直接写清楚。

### 1. 你只加载了 `SKILL.md`

这时它能做基础清理，但不会有完整的场景判断和精细误杀防护。

### 2. 原文的问题不是“套话太多”，而是“没有作者自己的声音”

当前版本更擅长去掉明显 AI 痕迹，还不够擅长贴近“你本人会怎么说”。

### 3. 你在非常保守的场景里用它

例如：

- 技术文档
- status
- code-context

这些场景默认会更克制，所以结果可能是“更干净”，但不一定会“更活”。

### 4. 原文本身就太空

如果原文没有具体信息，`说人话` 不会凭空替你发明细节。  
它最多能把空洞表达压低，但不能把没有内容的文本改成有内容。

---

## 项目结构

```text
shuorenhua/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── evals/
│   ├── benchmark.md
│   ├── results-v1.3.0.md
│   ├── results-v1.4.3.md
│   ├── results-v1.5.0.md
│   └── run-eval.md
├── install/
│   ├── codex.md
│   ├── claude-code.md
│   ├── cursor.md
│   ├── openclaw.md
│   ├── chatgpt.md
│   └── chatgpt-gpt-instructions.md
└── references/
    ├── examples.md
    ├── operation-manual.md
    ├── positive-style.md
    ├── phrases-en.md
    ├── phrases-zh.md
    ├── protected-spans.md
    ├── scene-guardrails.md
    ├── severity.md
    ├── structures.md
    └── boundary-cases.md
```

核心只需要 `SKILL.md` 一个文件。`references/` 让场景判断、正向改写目标和事实保真更稳，按需加载。

---

## v1.7.0 基础层

这一版先把两件基础工作补齐：

- `Positive Style Contract`：不只说“别写得像 AI”，也定义“更像人”该往哪里靠
- `Protected Spans`：先保护数字、日期、引用、命令、参数、报错和责任归属，再决定怎么改句子

这一步还是基础层，不等于已经做了 voice 拟合或 second pass 抛光。

---

## FAQ

### 这是不是拿来骗 AI detector 的？

不是。  
这个项目的目标是减少模板感、表演感和语域漂移，让文本更自然、更可发布，不是绕过检测。

### 会不会把技术内容改坏？

默认不会。  
代码、参数、日志、命令、系统主语、术语、引用原文都在优先保护范围内。

### 英文能不能用？

可以，但这是一个 **中文优先** 项目。  
英文支持是有的，但主要价值仍然在中文场景，尤其是中文互联网和工程写作里的 AI 腔。

### 为什么改完有时还是有 AI 味？

因为“去掉明显套路”不等于“拥有具体作者的 voice”。  
当前版本更擅长清理，不够擅长拟合你的个人表达，这也是后续迭代重点。

### 我应该什么时候用 annotation mode？

当你：

- 还不确定这段该不该改
- 想先 review 再决定
- 处在 docs / status 这种保守场景
- 怀疑有无源引用或误杀风险

---

## 贡献

欢迎提交：

- 新 benchmark
- 边界案例
- 真实 bad case
- 改写前后样本
- 新的误杀防护

在提交新词之前，优先先想一件事：

> 这是一个“新模式”，还是只是“现有模式的变体”？

详细规则见 `CONTRIBUTING.md`。

---

## License

MIT
