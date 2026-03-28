# 说人话

> 我已经把差异**收窄**了，**根因**基本**坐实**，和我刚**抓到的现象**也**对上了**。接下来做一个**更硬的排除法**，**稳稳兜住**，**落盘**之后就能**收口**了。

这是 ChatGPT 5.4 跟你说的"人话"。没有一个正常人会这么聊天。

这个项目干的事：让 AI 输出的中文读起来像人写的。英文也管。

## GPT-5.x 的新一波口癖

旧的 AI 味你认识——"赋能""闭环""在当今快速发展的时代"。这些已经被骂了一年，新模型学乖了，换了一套。

GPT-5.4 和 Codex 开始说一种"SRE 中文"，把 debug 术语塞进日常对话。"兜底""压实""收敛""收束""锁住""口径""能吃""硬写"——像在写 incident report，但其实只是在帮你改个按钮颜色。

还学会了暴力表演执行力：**补一刀、狠狠干、拍脑门、揪出来**。你让它改个 CSS，它说"我先狠狠干一把"。

最让人血压升高的是这类：

> **要不要我**帮你把剩下的也改了？**只要你回复我**，**我立马开始**。**你就确认一点**，**你一回复我就**上手。

没人问你。做就做，别推销。这批新口癖的核心模式已经覆盖，变体不靠逐词硬收。

## 小红书 AI 腔也没放过

> 姐妹们！今天给大家**拆解**一个**保姆级干货**！**谁懂啊**，这个工具**狠狠**提升了我的效率！**建议收藏**！

真人用这些词是随机蹦一两个，AI 是六个连发。一眼机器。

## 规模

12 条规则。210+ 中文禁用短语。96 英文禁用短语。18 种结构反模式。7 维评分。按场景自动调强度，聊天时只动套话，写博客时全规则扫描，不会把正常的技术报告改得面目全非。

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
| 结构反模式 | ✅ | 部分 | 18 种 |

## 效果

**改写前：**
> 在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。数据显示，采用该方案的团队生产力实现了显著提升。总而言之，这款工具必将成为推动行业发展的重要力量。

**改写后：**
> AI 工具很多，真正能帮开发者把活做快、做稳的并不多。用过这套方案的团队，开发节奏明显快了，代码返工也少了。

更多示例见 [references/examples.md](references/examples.md)。

## 评测

最新一次评测基于 31 条测试用例（17 条该改 + 14 条不该误杀）：

| 指标 | 结果 | 目标 |
|------|------|------|
| 该改的改了 | 16/17 (94.1%) | > 90% ✅ |
| 不该改的没动 | 14/14 (100%) | 误杀 < 10% ✅ |

唯一的 ⚠️ 还是"研究表明……"那条。规则正确标记了需要补来源，但原文本身没有真实来源可补，不算规则失效。

新增的 2 条测试里，`SF-17` 验证了未逐词入库的变体也能被现有模式吸收，`SNF-14` 验证了讨论收词策略时不会误杀被引用词。

详见 [evals/results-v1.4.4.md](evals/results-v1.4.4.md)。

## 安装

```bash
git clone https://github.com/MrGeDiao/shuorenhua.git
```

最快的用法——Codex 一行命令：

```bash
codex --system-prompt "$(cat shuorenhua/SKILL.md)" "改写以下文本：..."
```

其他平台的安装说明：[Codex](install/codex.md) · [OpenClaw](install/openclaw.md) · [Claude Code](install/claude-code.md) · [Cursor / Windsurf](install/cursor.md) · [ChatGPT / 其他](install/chatgpt.md)

## 设计

四种场景，三种强度：

| 场景 | 强度 | 干什么 |
|------|------|--------|
| 聊天 | 轻 | 只砍套话，保留口语感 |
| 技术摘要 | 中 | 砍套话 + 渲染词，允许系统主语 |
| 文档 | 中 | 技术表达优先 |
| 博客/社交 | 重 | 全规则 + 两遍制 |

12 条规则：砍开场废话、打破公式结构、用具体主语、要具体不要渲染、适时对读者说话、调节节奏、信任读者、砍金句感、砍谄媚、用简单动词、语域别混搭、句长别均匀。

三级严重度——Tier 1 默认替换，Tier 2 聚集时改，Tier 3 密度高时改。附误杀防护：技术术语、引用原文、行业标准用语不动。

## 文件结构

```
shuorenhua/
├── SKILL.md               # 规则 + 工作流 + 评分
├── references/
│   ├── phrases-zh.md       # 中文禁用短语（210+ 条）
│   ├── phrases-en.md       # 英文禁用短语（96 条）
│   ├── structures.md       # 18 种结构反模式
│   ├── examples.md         # 改写示例
│   └── severity.md         # 严重度 + 误杀防护
├── evals/
│   ├── benchmark.md        # 评测集（31 条）
│   ├── run-eval.md         # Codex 评测指令
│   └── results-v1.4.4.md   # 最新评测结果
├── install/                # 各平台安装说明
├── CONTRIBUTING.md
├── LICENSE                 # MIT
└── CHANGELOG.md
```

## 参与

想加新词、新结构、新评测用例？看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 致谢

- [humanizer](https://github.com/blader/humanizer) — AI 模式分类
- [stop-slop](https://github.com/hardikpandya/stop-slop) — 规则 + 评分框架
- [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 中文去 AI 味
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — 严重度分级
- [beautiful_prose](https://github.com/SHADOWPR0/beautiful_prose) — 正面风格契约

## 社区

在 [Linux.do](https://linux.do) 发现这个项目？欢迎来聊。

## 许可

[MIT](LICENSE)
