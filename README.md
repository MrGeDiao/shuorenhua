# 说人话

> 我已经把差异**收窄**了，**根因**基本**坐实**，和我刚**抓到的现象**也**对上了**。接下来做一个**更硬的排除法**，**稳稳兜住**，**落盘**之后就能**收口**了。

这是 ChatGPT 5.4 跟你说的“人话”。没有一个正常人会这么聊天。

**说人话（shuorenhua）** 是一个给 AI 用的改写 skill：专门清理中文和英文里的模板感、表演感和 AI 套路，让输出更像真人在当前场景下说的话。

它不是简单的敏感词替换表。重点是三件事：
- 先判断场景：`chat / status / docs / public-writing`
- 再判断问题强度：`Tier 1 / Tier 2 / Tier 3`
- 最后才决定轻改、标准改，还是重写

该保留的也会保留：术语、系统主语、命令、字段名、正式公告语体、事故复盘表达，不会为了“像人”把技术文本改散。

## 它主要解决什么问题

旧的 AI 味你已经很熟了：`赋能`、`闭环`、`在当今快速发展的时代`。

新一波更烦，尤其是 GPT-5.x / Codex 这类模型会开始说一种“工程师表演腔”或者“SRE 中文”：
- `收窄`、`兜住`、`落盘`、`收口`
- `根因基本坐实了`
- `我先补一刀`
- `只要你回复我，我立马开始`

还有另一条支线是自媒体 / 小红书流水线：
- `姐妹们`
- `谁懂啊`
- `保姆级`
- `建议收藏`
- `狠狠提升`

真人当然也会偶尔说这些词，但 AI 的问题是：**密度太高、结构太整齐、语域乱跳，还爱表演执行力。**

## 这份 skill 现在有什么

- 中英文禁用短语表
- 结构反模式
- 严重度分级（Tier 1 / 2 / 3）
- 场景禁改表
- 微操作手册
- 边界案例集
- 改写示例

完整工作流已经从“规则列表”升级成“入口判断 + 按需补读 references”模式，更适合 Codex、Claude Code、OpenClaw 这类按 skill 逐层加载的环境。

## 效果

**改写前：**
> 在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。数据显示，采用该方案的团队生产力实现了显著提升。总而言之，这款工具必将成为推动行业发展的重要力量。

**改写后：**
> AI 工具很多，真正能帮开发者把活做快、做稳的并不多。用过这套方案的团队，开发节奏明显快了，代码返工也少了。

更多例子看 [references/examples.md](references/examples.md)。

## 评测

下面这组数字对应**当前公开归档的一次评测运行**（GPT-5.4 Codex，29 条测试用例：16 条该改 + 13 条不该误杀），不是每次文档更新都会同步重跑：

| 指标 | 结果 | 目标 |
|------|------|------|
| 该改的改了 | 14/15 (93%)，SF-16 待测 | > 90% ✅ |
| 不该改的没动 | 13/13 (100%) | 误杀 < 10% ✅ |

新增的工程师腔、小红书腔、语域混搭、句长均匀、边界误杀防护测试都已经补进来。当前公开归档结果见 [evals/results-v1.3.0.md](evals/results-v1.3.0.md)。

## 安装

```bash
git clone https://github.com/MrGeDiao/shuorenhua.git
```

常见安装方式：
- [Codex](install/codex.md)
- [OpenClaw](install/openclaw.md)
- [Claude Code](install/claude-code.md)
- [Cursor / Windsurf](install/cursor.md)
- [ChatGPT / 其他](install/chatgpt.md)

## 设计思路

### 1) 先判场景，不是一把梭

| 场景 | 默认档位 | 重点 |
|------|----------|------|
| `chat` | minimal | 只清理明显套话，保留口语感 |
| `status` | minimal / standard | 保时间线、动作、结果、风险 |
| `docs` | minimal | 保术语、系统主语、可检索性 |
| `public-writing` | standard | 保语域一致，不硬造洞见 |

### 2) 再判 Tier，不把所有词一刀切

- **Tier 1**：默认替换。命中后大概率直接删或改。
- **Tier 2**：单独可接受，聚集出现才处理。
- **Tier 3**：只在全文密度明显过高时处理。

### 3) 最后才决定改写力度

- **minimal**：轻改，去局部模板感
- **standard**：统一语域，处理结构问题
- **aggressive**：只在重度 AI 腔时启用，先保事实再重写

## 文件结构

```text
shuorenhua/
├── SKILL.md                         # 入口型主文档：场景 / Tier / 档位 / 输出合同
├── references/
│   ├── phrases-zh.md                # 中文禁用短语
│   ├── phrases-en.md                # 英文禁用短语
│   ├── structures.md                # 结构反模式
│   ├── severity.md                  # 严重度分级
│   ├── examples.md                  # 改写示例
│   ├── operation-manual.md          # 微操作手册
│   ├── scene-guardrails.md          # 场景禁改表
│   └── boundary-cases.md            # 边界案例 / 误杀防护
├── evals/
│   ├── benchmark.md                 # 评测集
│   ├── run-eval.md                  # 评测指令
│   └── results-v1.3.0.md            # 当前归档结果
├── install/                         # 各平台安装说明
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## 仓库里的名字怎么理解

- **仓库名 / 项目名**：`shuorenhua`
- **对外展示名**：说人话
- **兼容旧叫法**：如果你之前把它当成 `stop-slop-zh` 的中文分支，也没问题，但现在建议统一用 `shuorenhua / 说人话`

如果你在某些宿主里更喜欢沿用 `stop-slop` 这个 skill 名，也可以做本地映射；仓库本身建议统一叫“说人话”。

## 参与

想加新词、新结构、新评测用例，或者补误杀边界，先看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 致谢

- [humanizer](https://github.com/blader/humanizer) — AI 模式分类
- [stop-slop](https://github.com/hardikpandya/stop-slop) — 规则与评分框架
- [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 中文去 AI 味
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — 严重度分级
- [beautiful_prose](https://github.com/SHADOWPR0/beautiful_prose) — 正面风格契约

## 许可

[MIT](LICENSE)
