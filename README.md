# stop-slop-zh

**中英双语 AI 写作去味技能** | Bilingual AI writing de-slop skill

消除 AI 生成文本中的套话、机械结构、虚假主语、被动堆砌和情绪渲染。按场景分档改写，避免过度矫正。

Remove throat-clearing, formulaic structures, false agency, passive stacking, and emotional inflation from AI-generated text. Scene-based intensity routing prevents over-correction.

## 为什么需要这个？ | Why?

AI 生成的文本有明显的模式：开场铺垫、二元对比、三件套列举、"赋能""助力""打造"等黑话、无源引用、总结式收尾。这些模式在中文和英文中都存在，但中文还有额外的翻译腔和互联网黑话问题。

多数主流去 AI 味工具（[humanizer](https://github.com/blader/humanizer)、[stop-slop](https://github.com/hardikpandya/stop-slop)）主要覆盖英文。本项目填补中文空白，并在以下方面做了改进：

| 特性 | stop-slop | humanizer | **stop-slop-zh** |
|------|-----------|-----------|-----------------|
| 中文禁用短语表 | - | - | ✅ 140+ 条 |
| 互联网黑话（赋能/闭环/抓手） | - | - | ✅ |
| 翻译腔检测 | - | - | ✅ |
| 场景分流 | - | - | ✅ 4 场景 × 3 档位 |
| 严重度分级 | - | - | ✅ 3 级 + 误杀防护 |
| 无源引用检测 | - | - | ✅ |
| 英文禁用短语 | ✅ | ✅ | ✅ |
| 结构反模式 | ✅ | 部分 | ✅ 13 种 |
| 改写示例 | ✅ | ✅ | ✅ 中英双语 |

## 快速开始 | Quick Start

### 一键下载

```bash
git clone https://github.com/MrGeDiao/stop-slop-zh.git
```

### Claude Code

```bash
# 方式 1：复制到项目
mkdir -p .claude/skills/stop-slop-zh
cp -r stop-slop-zh/SKILL.md stop-slop-zh/references/ .claude/skills/stop-slop-zh/

# 方式 2：复制到全局
mkdir -p ~/.claude/skills/stop-slop-zh
cp -r stop-slop-zh/SKILL.md stop-slop-zh/references/ ~/.claude/skills/stop-slop-zh/
```

详见 [install/claude-code.md](install/claude-code.md)。

### Cursor / Windsurf

```bash
cp stop-slop-zh/SKILL.md .cursor/rules/stop-slop.md
```

详见 [install/cursor.md](install/cursor.md)。

### ChatGPT / 其他

将 `SKILL.md` 内容粘贴到 System Prompt 或 Custom Instructions 中。

详见 [install/chatgpt.md](install/chatgpt.md)。

## 核心设计 | Design

### 场景分流

不同文本类型需要不同的改写强度：

| 场景 | 档位 | 说明 |
|------|------|------|
| chat（即时消息） | minimal | 只砍 Tier 1 套话，保留口语感 |
| status（技术摘要） | standard | 砍套话 + 渲染词，允许系统主语 |
| docs（文档） | standard | 技术表达优先 |
| public-writing（博客/社交媒体） | aggressive | 全规则 + 两遍制 |

### 10 条规则

1. 砍掉开场废话
2. 打破公式化结构
3. 优先用人或具体事物做主语（启发式）
4. 要具体，不要渲染
5. 适时对读者说话（启发式）
6. 调节节奏
7. 信任读者智商
8. 砍掉金句感
9. 消灭谄媚和元评论
10. 用最简单的动词

### 3 级严重度

- **Tier 1**：默认替换（"赋能""delve""serves as"）
- **Tier 2**：同段聚集 2+ 个时标记（"然而""此外""nuanced"）
- **Tier 3**：全文密度高时标记（"重要""significant"）

附误杀防护规则：引用原文、术语定义、代码/配置、行业标准术语、技术描述中的系统主语。

## 效果对比 | Before & After

### 中文

**改写前：**
> 在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。数据显示，采用该方案的团队生产力实现了显著提升。总而言之，这款工具必将成为推动行业发展的重要力量。

**改写后：**
> AI 工具很多，真正能帮开发者把活做快、做稳的并不多。用过这套方案的团队，开发节奏明显快了，代码返工也少了。它未必会一夜之间改写整个行业，但至少说明了一件事：软件开发的工作流，已经开始换轨。

### English

**Before:**
> It's worth noting that this framework serves as a testament to the transformative potential of modern architecture patterns. The system leverages cutting-edge microservices to foster seamless collaboration across teams.

**After:**
> This framework shows what modern architecture patterns can do in practice. It uses microservices to help teams collaborate across service boundaries with less friction.

更多示例见 [references/examples.md](references/examples.md)。

## 文件结构 | Structure

```
stop-slop-zh/
├── SKILL.md               # 核心规则 + 工作流 + 评分框架
├── references/
│   ├── phrases-zh.md       # 中文禁用短语（140+ 条，含互联网黑话）
│   ├── phrases-en.md       # 英文禁用短语（130+ 条）
│   ├── structures.md       # 13 种跨语言结构反模式
│   ├── examples.md         # 中英文改写示例
│   └── severity.md         # 3 级严重度 + 误杀防护
├── evals/
│   └── benchmark.md        # 评测集：该改的 + 不该误杀的
├── install/                # 各平台安装说明
│   ├── claude-code.md
│   ├── cursor.md
│   └── chatgpt.md
├── CONTRIBUTING.md         # 贡献指南
├── LICENSE                 # MIT
└── CHANGELOG.md
```

## 致谢 | Credits

本项目融合了以下开源项目的精华：

- [humanizer](https://github.com/blader/humanizer) (10.5k stars) — 25 种 AI 模式分类
- [stop-slop](https://github.com/hardikpandya/stop-slop) (2.2k stars) — 8 规则 + 评分框架
- [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) (13.5k stars) — 中文去 AI 味
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — 3 级严重度
- [beautiful_prose](https://github.com/SHADOWPR0/beautiful_prose) — 正面风格契约

## 许可 | License

[MIT](LICENSE)
