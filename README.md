# 说人话

让 AI 写出来的东西像人写的。中英文都管。

你肯定见过这种文字:

> 在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。

一眼 AI。本项目就是干掉这种味道的。

## ChatGPT 5.4 又发明了一套新黑话

最近社区发现 ChatGPT 5.4 / Codex 开始说一种奇怪的"工程师中文"，像在写 postmortem，但其实只是在聊天：

> 我已经把差异**收窄**了，**根因**基本**坐实**，和我刚**抓到的现象**也**对上了**。接下来做一个**更硬的排除法**，**稳稳兜住**，**落盘**之后就能**收口**了。

说人话版本：

> 原因找到了：是缓存过期导致的。我把可能性排查了一遍，现在就剩这一个。

这些词:**砍一刀、兜住、落盘、收口、收窄、打掉问题、根因、偏硬、拆开看、接住、对上了、坐实等等**没有一个是正常人会在聊天里用的。本项目 v1.3 已经全部收录。

## 还有小红书 AI 腔

AI 模仿爆款文风也很容易穿帮：

> 姐妹们！今天给大家**拆解**一个**保姆级干货**！真的**绝绝子**！**谁懂啊**，这个工具**狠狠**提升了我的效率！**强烈建议收藏**！

真人用这些词是随机的，AI 是批量的。一眼就能看出来。

## 这个项目做了什么

12 条规则，200+ 中文禁用短语，130+ 英文禁用短语，18 种结构反模式，7 维评分。按场景自动调节强度，不会矫枉过正。

英文的去 AI 味工具已经有了（[stop-slop](https://github.com/hardikpandya/stop-slop)、[humanizer](https://github.com/blader/humanizer)），但中文一直是空白。这个项目补上了：

| 能力 | stop-slop | humanizer | **说人话** |
|------|-----------|-----------|-----------|
| 中文禁用短语 | - | - | ✅ 200+ 条 |
| 互联网黑话（赋能/闭环/抓手） | - | - | ✅ |
| 工程师腔（兜住/落盘/根因） | - | - | ✅ |
| 小红书 AI 腔（保姆级/绝绝子） | - | - | ✅ |
| 翻译腔 | - | - | ✅ |
| 语域混搭检测 | - | - | ✅ |
| 节奏量化 | - | - | ✅ |
| 场景分档 | - | - | ✅ 4 × 3 |
| 严重度分级 + 误杀防护 | - | - | ✅ |
| 英文禁用短语 | ✅ | ✅ | ✅ |
| 结构反模式 | ✅ | 部分 | ✅ 18 种 |

## 效果

**改写前：**
> 在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。数据显示，采用该方案的团队生产力实现了显著提升。总而言之，这款工具必将成为推动行业发展的重要力量。

**改写后：**
> AI 工具很多，真正能帮开发者把活做快、做稳的并不多。用过这套方案的团队，开发节奏明显快了，代码返工也少了。

更多示例见 [references/examples.md](references/examples.md)。

## 评测

用 GPT-5.4 Codex 跑了 28 条测试用例（15 条该改的 + 13 条不该误杀的）：

| 指标 | 结果 | 目标 |
|------|------|------|
| 该改的改了 | 14/15 (93%) | > 90% ✅ |
| 不该改的没动 | 13/13 (100%) | 误杀 < 10% ✅ |

唯一的 ⚠️ 是"研究表明……"那条——规则正确标记了需要补来源，但原文本身就没有真实来源可补，不算规则失效。

新增的 5 条测试（工程师腔、小红书腔、正能量收尾、语域混搭、句长均匀）全部一次通过。新增的 3 条误杀防护测试（真人 debug 对话、真人博主网络用语、纯技术报告）零误杀。

详见 [evals/results-v1.3.0.md](evals/results-v1.3.0.md)。

## 安装

### 下载

```bash
git clone https://github.com/MrGeDiao/shuorenhua.git
```

### Claude Code

```bash
# 项目级
mkdir -p .claude/skills/shuorenhua
cp -r shuorenhua/SKILL.md shuorenhua/references/ .claude/skills/shuorenhua/

# 全局
mkdir -p ~/.claude/skills/shuorenhua
cp -r shuorenhua/SKILL.md shuorenhua/references/ ~/.claude/skills/shuorenhua/
```

详见 [install/claude-code.md](install/claude-code.md)。

### Codex CLI

```bash
codex --system-prompt "$(cat shuorenhua/SKILL.md)" "改写以下文本：..."
```

详见 [install/codex.md](install/codex.md)。

### Cursor / Windsurf

```bash
cp shuorenhua/SKILL.md .cursor/rules/shuorenhua.md
```

详见 [install/cursor.md](install/cursor.md)。

### ChatGPT / 其他

把 `SKILL.md` 的内容粘贴到 System Prompt 或 Custom Instructions 里。

详见 [install/chatgpt.md](install/chatgpt.md)。

## 设计

**4 种场景，3 种强度：**

| 场景 | 强度 | 干什么 |
|------|------|--------|
| 聊天 | 轻 | 只砍套话，保留口语感 |
| 技术摘要 | 中 | 砍套话 + 渲染词，允许系统主语 |
| 文档 | 中 | 技术表达优先 |
| 博客/社交 | 重 | 全规则 + 两遍制 |

**12 条规则：**

1. 砍开场废话
2. 打破公式结构
3. 用具体主语
4. 要具体，不要渲染
5. 适时对读者说话
6. 调节节奏
7. 信任读者
8. 砍金句感
9. 砍谄媚
10. 用简单动词
11. 语域别混搭
12. 句长别均匀

**3 级严重度：** Tier 1 默认替换，Tier 2 聚集时改，Tier 3 密度高时改。附误杀防护——技术术语、引用原文、行业标准用语不改。

## 文件结构

```
shuorenhua/
├── SKILL.md               # 规则 + 工作流 + 评分
├── references/
│   ├── phrases-zh.md       # 中文禁用短语（200+ 条）
│   ├── phrases-en.md       # 英文禁用短语（130+ 条）
│   ├── structures.md       # 18 种结构反模式
│   ├── examples.md         # 改写示例
│   └── severity.md         # 严重度 + 误杀防护
├── evals/
│   ├── benchmark.md        # 评测集（28 条）
│   ├── run-eval.md         # Codex 评测指令
│   └── results-v1.3.0.md   # v1.3 评测结果
├── install/                # 各平台安装说明
├── CONTRIBUTING.md
├── LICENSE                 # MIT
└── CHANGELOG.md
```

## 参与

想加新词、新结构、新评测用例？看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 致谢

站在这些项目的肩膀上：

- [humanizer](https://github.com/blader/humanizer) — AI 模式分类
- [stop-slop](https://github.com/hardikpandya/stop-slop) — 规则 + 评分框架
- [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 中文去 AI 味
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — 严重度分级
- [beautiful_prose](https://github.com/SHADOWPR0/beautiful_prose) — 正面风格契约

## 许可

[MIT](LICENSE)
