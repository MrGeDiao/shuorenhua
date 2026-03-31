# 说人话

> 我已经把差异**收窄**了，**根因**基本**坐实**，和我刚**抓到的现象**也**对上了**。接下来做一个**更硬的排除法**，**稳稳兜住**，**落盘**之后就能**收口**了。

这是 GPT-5.4 跟你说的"人话"。没有一个正常人会这么聊天。

**说人话**是一套规则，让 AI 输出的中文读起来像人写的。英文也管。装进你的 AI 编辑器，写出来的东西就不再一股 AI 味。

## 效果

**改写前：**
> 在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。数据显示，采用该方案的团队生产力实现了显著提升。总而言之，这款工具必将成为推动行业发展的重要力量。

**改写后：**
> AI 工具很多，真正能帮开发者把活做快、做稳的并不多。用过这套方案的团队，开发节奏明显快了，代码返工也少了。

**改写前（工程师腔）：**
> 我先把这个 bug **抠出来**看看**根因**，**稳稳兜住**之后**落盘**，**收口**之前再**补一刀**确认。

**改写后：**
> 我先定位这个 bug 的原因，修完之后写入日志，关单前再确认一次。

更多示例见 [references/examples.md](references/examples.md)。

## 快速开始

```bash
git clone https://github.com/MrGeDiao/shuorenhua.git
```

**Codex** — 一行命令：

```bash
codex --system-prompt "$(cat shuorenhua/SKILL.md)" "改写以下文本：..."
```

**Claude Code** — 把 skill 装进项目后直接对话：

```text
用说人话规则改写这段文本：...
```

**只想看哪里像 AI，不直接改？** 用 annotation mode：

```text
先不要改写，只按 annotation mode 标出下面这段文字里的问题：...
```

更多平台：[Codex](install/codex.md) · [Claude Code](install/claude-code.md) · [OpenClaw](install/openclaw.md) · [Cursor / Windsurf](install/cursor.md) · [ChatGPT / 其他](install/chatgpt.md)

## 它管什么

210+ 中文禁用短语，96 英文禁用短语，19 种结构反模式。分六大类：

| 类别 | 典型症状 |
|------|---------|
| 经典套话 | 在当今快速发展的时代、值得注意的是、总而言之 |
| 商业黑话 | 赋能、闭环、抓手、打造、降本增效 |
| 工程师腔 | 收窄、兜住、落盘、收口、根因、坐实 |
| 小红书腔 | 保姆级、绝绝子、谁懂啊、拆解、建议收藏 |
| 翻译腔 | 基于……来……、通过……进行……、被动堆砌 |
| 英文 slop | leverage、delve、it's worth noting、testament to |

还有：语域混搭检测、节奏量化（AI 句长标准差 ≈ 1.2，人类 ≈ 4.7+）、无源引用识别。

不管的：代码、日志、命令、配置、接口名、报错信息。

## 工作原理

**四种场景，三种强度：**

| 场景 | 默认强度 | 策略 |
|------|---------|------|
| 聊天 | 轻 | 只砍套话，保留口语感 |
| 技术摘要 | 轻–中 | 砍套话 + 渲染词，保留系统主语 |
| 文档 | 轻 | 术语优先，不改成口语 |
| 博客 / 社交 | 中 | 全规则扫描 |

**三级严重度：**
- **Tier 1**：默认替换（开场套话、商业黑话、工程师表演腔）
- **Tier 2**：聚集时改（高频连接词、渲染修饰词扎堆）
- **Tier 3**：密度高时改（常见词本身没问题，饱和了才处理）

**误杀防护**：技术术语、引用原文、系统主语、学术被动语态、真人 debug 对话——碰到这些不动。

**两种输出模式：**
- 默认直接给改写结果
- `annotation mode`：只标问题，不改写（适合审稿）

## 评测

37 条 benchmark（21 条该改 + 16 条不该动）：

| 指标 | 结果 | 目标 |
|------|------|------|
| 该改的改了 | 21/21 (100%) | > 90% ✅ |
| 不该改的没动 | 16/16 (0% 误杀) | < 10% ✅ |

覆盖 `short / long / mixed` 三类长度，含无源引用、annotation mode 抽样验证。详见 [evals/results-v1.5.0.md](evals/results-v1.5.0.md)。

## 对比

英文去 AI 味有 [stop-slop](https://github.com/hardikpandya/stop-slop) 和 [humanizer](https://github.com/blader/humanizer)，中文一直没有。

| 能力 | stop-slop | humanizer | **说人话** |
|------|-----------|-----------|-----------|
| 中文短语 | — | — | 210+ |
| 英文短语 | ✅ | ✅ | 96 |
| 结构反模式 | ✅ | 部分 | 19 种 |
| 场景分档 | — | — | 4 × 3 |
| 误杀防护 | — | — | ✅ |
| 标注模式 | — | — | ✅ |
| 工程师腔 / 小红书腔 | — | — | ✅ |

## AI 味图鉴

「赋能」「闭环」是旧的 AI 味。新模型换了一套。

**工程师表演腔** — GPT-5.4 开始说一种"SRE 中文"，把 debug 术语塞进日常对话。"兜底""压实""收敛""收束""锁住"——像在写 incident report，但其实只是在帮你改个按钮颜色。

**暴力执行力腔** — "补一刀""狠狠干""拍脑门""揪出来"。你让它改个 CSS，它说"我先狠狠干一把"。

**主动推销腔** — "要不要我帮你把剩下的也改了？""只要你回复我，我立马开始。"没人问你。做就做，别推销。

**小红书 AI 腔** — "姐妹们！今天给大家**拆解**一个**保姆级干货**！**谁懂啊**！**建议收藏**！"真人用这些词是随机蹦一两个，AI 是六个连发。

## 文件结构

```
shuorenhua/
├── SKILL.md               # 核心规则（单文件即可用）
├── references/             # 补充规则（精细改写时按需加载）
│   ├── phrases-zh.md       # 中文禁用短语（210+）
│   ├── phrases-en.md       # 英文禁用短语（96）
│   ├── structures.md       # 结构反模式（19 种）
│   ├── severity.md         # 严重度 + 误杀防护
│   ├── operation-manual.md # 微操作手册
│   ├── scene-guardrails.md # 场景禁改表
│   ├── boundary-cases.md   # 边界案例集
│   └── examples.md         # 改写示例 + annotation mode 示例
├── evals/                  # 评测
├── install/                # 各平台安装说明
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE                 # MIT
```

核心只需要 `SKILL.md` 一个文件。`references/` 让场景判断和误杀防护更准，按需加载。

## 参与

想加新词、新结构、新评测用例？看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 致谢

- [stop-slop](https://github.com/hardikpandya/stop-slop) — 规则 + 评分框架
- [humanizer](https://github.com/blader/humanizer) — AI 模式分类
- [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 中文去 AI 味
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — 严重度分级
- [beautiful_prose](https://github.com/SHADOWPR0/beautiful_prose) — 正面风格契约

## 社区

在 [Linux.do](https://linux.do) 发现这个项目？欢迎来聊。

## 许可

[MIT](LICENSE)
