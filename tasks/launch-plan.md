# 说人话：宣传与冷启动方案

> 更新时间：2026-04-13
> 当前状态：已在 X 和 Linux.do 发过首波内容，后续曝光没有接上。

---

## 核心判断

你现在最缺的不是"再发一次链接"，而是 **第二波叙事素材**。

单纯转发仓库链接，用户很难理解它和普通 prompt 有什么不同。第二轮曝光之前，先补齐 4 样东西：

1. README 已重写（已完成）
2. 至少 3 组能秒懂的 before / after
3. 一条征集 bad cases 的入口
4. 一个明确的版本升级点（v1.7.1 二次审稿）

---

## 30 天目标

不要只盯 star。

### 质量目标

- 拿到 20-30 条真实 bad cases
- 收到 5-10 条用户真实使用反馈
- 积累 5 条以上可公开展示的真实 before / after

### 分发目标

- 至少被 2-4 个 skill / agent 目录收录
- 完成第二轮 X 帖子和 Linux.do 跟进帖
- 建立一个可复用的发帖节奏

### 数据目标（保守）

- star：+50-150
- issues / discussions：至少 5 个真实样本反馈
- 外部目录收录：2-4 个

---

## 3 条传播主线

### 主线 A：中文 AI 写作有自己独特的病灶

不只是 `赋能 / 闭环`，现在还有工程师表演腔、小红书 AI 腔、narrator 腔。英文项目很少专门解决中文这些问题。

适合：X、Linux.do

### 主线 B：这不是乱润色，它有边界和误杀防护

docs / status / code-context 默认保守。benchmark 分 should-fix 和 should-not-fix。不只是"改得更好看"，而是"该改的改，不该改的别碰"。

适合：GitHub README、Release、目录提交

### 主线 C：下一步不是堆词表，而是做二次审稿和 voice 拟合

当前版本能做基础清理，下一步要解决"改完还是有轻微 AI 味"。

适合：开发日志、跟进帖、征集反馈

---

## 渠道优先级与具体动作

### P0：GitHub 仓库本身

所有外部流量最后都会落到这里，先把这里搞好。

**已完成**：
- [x] README 重写（恢复个性、对比表、致谢、社区链接）

**待完成**：
- [ ] 更新 repo topics，建议用这些：
  ```
  agent-skill, codex, claude-code, chatgpt, prompt-engineering,
  ai-writing, anti-slop, chinese, rewriting, developer-tools, text-quality
  ```
- [ ] 开一个 pinned issue：`征集"改完还是有 AI 味"的案例`
  ```
  标题：征集 bad cases：改完还是像 AI？贴出来我改规则

  你用过说人话改写文本吗？如果改完还是有 AI 味，把原文和改写结果贴在这里。

  请附上：
  1. 原文（或片段）
  2. 你用的工具和模式（Codex / Claude Code / ChatGPT，lite / full）
  3. 哪里你觉得还是不自然
  4. 有什么内容是不能改的（术语、代码、引用等）

  每一条真实 case 都会推动下一个版本更准。
  ```
- [ ] 最新 release note 写清楚 v1.7.0 具体加了什么（已有 CHANGELOG，同步到 GitHub Release 页面）
- [ ] CHANGELOG 看起来在持续维护（已满足）

---

### P0：X（推特）

你已经发过一次，第二波不要再发"项目发布了"。发 **洞察 + 案例 + 请求反馈**，分 3 条发，不要塞进 1 条。

**帖子 1：洞察帖**

```
最近中文 AI 写作里最烦的，已经不只是"赋能、闭环"这种 old slop 了。

现在模型开始说：
- 收窄
- 根因坐实
- 稳稳兜住
- 落盘
- 收口

看起来像 SRE 在写 incident review，实际上只是帮你改个 README。

我做了个中文优先的 skill，专门清这些"表演感"和模板感：
https://github.com/MrGeDiao/shuorenhua

不是为了骗 detector，重点是：
- 去 AI 味
- 保事实和术语
- docs / code-context 默认更保守

如果你有"改完还是一股 AI 味"的案例，欢迎直接贴给我。
```

**帖子 2：案例帖**（隔 2-3 天发）

```
这类句子现在特别常见：

"我已经把差异收窄了，根因基本坐实，接下来稳稳把问题兜住，落盘之后就能收口了。"

正常人其实会说：

"我已经把排查范围缩小了，原因也基本确认了。接下来再排查一轮，把结论记下来就行。"

我在做一个中文 rewrite skill，专门处理这种工程师表演腔：
https://github.com/MrGeDiao/shuorenhua
```

**帖子 3：征集帖**（再隔 2-3 天）

```
做「说人话」这个去 AI 味 skill 以来，收到最多的反馈是：改完还是有轻微 AI 味。

所以下一版（v1.7.1）准备加二次审稿：第一遍清理套话，第二遍专门扫残留的模板感和过匀节奏。

如果你手里有这种 case——改完还是不够自然——直接贴给我，或者去 issue 里提：
https://github.com/MrGeDiao/shuorenhua/issues

真实 bad case 比 star 更有价值。
```

**英文帖**（可选，发一条即可）

```
AI writing slop in Chinese is not just "empower / leverage / cutting-edge".

Newer models produce a weird engineer-performance tone:
- narrow the diff
- root cause is basically locked
- hold the core path
- land it, close the loop

I built a Chinese-first rewrite skill for this:
https://github.com/MrGeDiao/shuorenhua

Goal: reduce AI writing patterns, preserve facts and technical context, stay conservative in docs / code-context.

Would love real bad cases if you have any.
```

---

### P0：Linux.do

Linux.do 适合发长帖，不要重复首发内容，发一个"做了一段时间后的反思"。

**帖子结构**：

```
标题：做「说人话」一个月后，我发现去 AI 味最难的不是删套话

正文：

## 我为什么做这个

[简短回顾，1-2 段]

## 做了一个月后我发现的真实问题

1. 删套话容易，删完还是像 AI 才是真正的难点
2. 工程师表演腔比商业黑话更难处理——因为它长得像正常技术讨论
3. 只靠"不能说什么"只能得到更干净的文本，不一定更像人
4. 代码场景（docstring、commit message）最容易误杀

## 目前做到什么程度

- 210+ 中文短语、96 英文短语、19 类结构反模式
- 46 条 benchmark，SF 通过率 100%，误杀率 0%
- 支持 Codex、Claude Code、ChatGPT、Cursor
- 新加了 Positive Style Contract 和 Protected Spans

## 接下来要做什么

- v1.7.1：二次审稿——第一遍清理后再扫一遍残留味
- v1.7.2：真实样本评测——不只看规则命中，还看能不能直接发
- v1.8：Voice Calibration——拟合用户自己的表达风格

## 最需要你们帮忙的

贴 bad case。

如果你用过之后发现改完还是像 AI，把原文和结果贴在评论里或者去 GitHub issue：
https://github.com/MrGeDiao/shuorenhua/issues

真实样本比 star 更能推动下一版。

项目地址：https://github.com/MrGeDiao/shuorenhua
```

---

### P1：Skill / Agent 目录提交

等 README 和 pinned issue 都就位后，提交到目录。

**统一提交材料**：

| 字段 | 内容 |
|------|------|
| 项目名 | 说人话 (shuorenhua) |
| 中文一句话 | 中文优先的自然表达 rewrite skill，减少 AI 模板感，保留事实、术语和技术上下文 |
| 英文一句话 | Chinese-first rewrite skill that removes AI writing patterns while preserving facts, terminology, and technical context |
| 标签 | writing, editing, developer-tools, skill, prompt, chinese, codex, claude-code |
| 核心特点 | benchmark, annotation mode, unsourced citation handling, code-context safe |
| 仓库链接 | https://github.com/MrGeDiao/shuorenhua |
| 最强示例 | 工程师腔 before/after |

**目标目录**：

- [ ] `awesome-agent-skills` 类仓库（搜 GitHub 找 2-3 个最活跃的）
- [ ] agent skill directory / registry 网站
- [ ] Codex / Claude Code 相关的 skill 合集
- [ ] 中文开发者工具合集

每个目录提交前确认：README 链接能打开、示例能看懂、有反馈入口。

---

### P1：其他社区（等第一轮反馈稳定后再做）

- V2EX — 发在"分享创造"节点
- 掘金 — 技术文章形式
- Reddit — r/LanguageTechnology 或 r/ChineseLanguage
- GitHub Discussions — 开自己仓库的 discussion

---

## 14 天动作表

| 时间 | 动作 | 产出 |
|------|------|------|
| Day 1 (4/14) | 更新 repo topics、开 pinned issue、发 GitHub Release v1.7.0 | 仓库基础面就位 |
| Day 2 (4/15) | 准备 3 组最强 before/after 素材 | 发帖素材备齐 |
| Day 3 (4/16) | 发 X 洞察帖（帖子 1） | 第二波曝光启动 |
| Day 5 (4/18) | 发 X 案例帖（帖子 2） | 工程师腔示例传播 |
| Day 6 (4/19) | 发 Linux.do 跟进长帖 | 深度反馈渠道 |
| Day 7 (4/20) | 发 X 征集帖（帖子 3） | bad case 收集启动 |
| Day 8 (4/21) | 选 2-3 个目录，准备提交材料 | 目录提交开始 |
| Day 9 (4/22) | 提交目录 PR / 表单 | 长尾入口建立 |
| Day 10 (4/23) | 发一个小版本或开发日志 | 项目活跃信号 |
| Day 12 (4/25) | 整理收到的 bad cases，回复提交者 | 反馈闭环 |
| Day 14 (4/27) | 阶段总结：拿到了多少反馈、哪些 case 最难、接下来做什么 | 下一轮素材 |

---

## GitHub Release v1.7.0 模板

发布到 GitHub Releases 页面：

```
## What changed

### Added
- Positive Style Contract：不只删 AI 套话，定义"更像人"的正向改写目标
- Protected Spans：改写前先保护数字、日期、引用、命令、参数、报错等不能动的内容
- 4 条新 benchmark（fact-preservation 相关）

### Changed
- SKILL.md 执行顺序改为先划 protected spans 再改写
- README 全文重写，恢复项目个性

## Why it matters

之前的版本更擅长"删掉 AI 味"，但删完有时还是太平、太匀、太像被清理过的模板。

这一版开始定义"改成什么样才算更像人"，同时把不能乱动的内容保护得更明确。

## Examples

**改写前**
> 在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。

**改写后**
> AI 工具很多，真正能帮开发者把活做快、做稳的并不多。这个项目做的，就是把模型写出来的套话和表演感压下去，让结果更像人写的。

## What's next

- v1.7.1：二次审稿（第一遍清理后再扫一遍残留味）
- v1.7.2：真实样本评测（不只看规则命中，还看能不能直接发）

如果你有"改完还是像 AI"的案例，欢迎贴到 issues。
```

---

## 版本更新帖模板（后续复用）

```
说人话 v{版本号} 更新了。

这次主要做了：
- {1}
- {2}
- {3}

重点不是多了多少功能，而是解决了：
{一个最实际的问题}

附一个例子：
{before / after}

项目地址：https://github.com/MrGeDiao/shuorenhua
```

---

## 最容易踩的坑

1. **只发链接** — 没人有义务自己理解你的项目，必须给一个最短路径的案例
2. **只谈"去 AI 味"，不谈边界** — 会被误认为 detector-bypass 工具
3. **只有技术亮点，没有反馈入口** — 曝光过去了也不会形成反馈闭环
4. **一次性把所有话说完** — 分 3-4 条帖子比 1 条长帖有效
5. **发完就沉默** — 一周没后续，项目会被默认"停更"
6. **只收 star 不收 case** — bad case 比 star 对迭代有用 10 倍
