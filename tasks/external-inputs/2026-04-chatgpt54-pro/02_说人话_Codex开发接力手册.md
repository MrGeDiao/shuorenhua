# 说人话：Codex 开发接力手册

> 目的：让 Codex 或未来协作者可以接力继续开发 `shuorenhua`，而不是每次都从头理解项目。  
> 使用方式：把这份文档和仓库一起交给 Codex，要求它按本文档的优先级、边界和验收标准推进。

---

## 1. 项目接力目标

`说人话` 当前不是要“大改框架”，而是要围绕一个明确目标迭代：

> **在不损害事实、术语、责任主体的前提下，减少文本中的 AI 模板感和表演感，并逐步提升真人表达感。**

接力开发的重点不是继续无限堆词表，而是补齐以下缺口：

1. 正向风格能力不足
2. 缺少 voice calibration
3. 缺少 residual audit
4. 真实样本评测不足
5. `lite` 和 `full` 模式差异没有产品化表达清楚

---

## 2. 进入仓库后先读什么

Codex 接手时，必须先通读以下文件，再开始改任何规则：

1. `README.md`
2. `SKILL.md`
3. `CHANGELOG.md`
4. `CONTRIBUTING.md`
5. `evals/benchmark.md`
6. `references/operation-manual.md`
7. `references/structures.md`
8. `references/severity.md`
9. `references/scene-guardrails.md`
10. `references/examples.md`

如果当前分支没有其中某些文件，就以仓库现状为准，但不要凭空假设文件存在。

---

## 3. 开发铁律

## 3.1 先 benchmark，后规则

任何新增规则、改写策略、误杀防护，至少要满足下面一条：

- 补一个新的 should-fix case
- 补一个新的 should-not-fix case
- 补一个真实样本 before/after case

如果没有样本，只是“感觉可能更好”，先不要落库。

## 3.2 先模式，后词条

遇到新口癖时，优先问：

- 它是不是现有问题族的变体？
- 现有模式能不能吸收它？
- 是不是补 benchmark / examples / operation-manual 比直接补词更好？

只有在下列情况才新增词条：

- 高频复现
- 改变误杀边界
- 现有模式吸收不稳

## 3.3 不许编造事实

任何新能力都不能导致：

- 编造研究来源
- 补不存在的数据
- 补不存在的人名、公司、年份
- 把猜测写成已证实事实

## 3.4 保守文档优先

`docs / status / code-context` 是误杀高风险区。优化自然感时，优先保护：

- 术语
- 命令
- 参数
- 路径
- 引用
- 代码
- 日志
- 报错
- 责任主体

## 3.5 一次改动必须全链路同步

如果改了规则逻辑，最少同步以下内容：

- `SKILL.md`
- 对应的 `references/*.md`
- `README.md`
- `CHANGELOG.md`
- 至少一个 benchmark / example

不要出现“规则已经变了，但 README 和 examples 还是旧口径”的情况。

## 3.6 不要把项目带向“骗 detector”

项目的方向是自然表达，不是规避识别。新增文案、README、功能时，避开以下叙事：

- humanizer for detectors
- bypass AI detection
- make text undetectable
- fool GPT detectors

---

## 4. 当前推荐的开发顺序

### 第一优先级（P0）

1. `Voice Calibration Lite`
2. `Residual Audit / Two-pass`
3. `Protected Spans / Facts Ledger`
4. `Positive Style Contract`
5. `Real Sample Eval Pack`

### 第二优先级（P1）

6. `Scene Packs`
7. `Lite vs Full` 使用模式产品化
8. `Copilot / 更多平台安装文档`
9. `Bad-case intake 模板`
10. `README / examples 升级`

### 第三优先级（P2）

11. 目录提交素材
12. 社区协作机制
13. 轻量 workflow / structured output schema
14. 自动化评测脚本（如仓库后续需要）

---

## 5. P0 任务详细说明

## P0-01：Voice Calibration Lite

### 目标

当用户提供 2–3 段自己的文字样本时，`说人话` 不只“去 AI 味”，还应该尝试贴近用户自己的表达节奏。

### 行为要求

新增一个轻量规则层，提取但不死记下面这些特征：

- 句长波动
- 标点密度
- 口语度
- 常用连接方式
- 是否爱用第一人称 / 直接判断句
- 是否喜欢短句、顿号、破折号、括号补充

### 重要边界

- 不复制用户样本文字
- 不模仿名人、品牌、公众人物
- 不因为“更像用户”而新增原文没有的事实

### 建议新增文件

- `references/voice-calibration.md`

### 需要同步修改

- `SKILL.md`
- `README.md`
- `CHANGELOG.md`
- `references/examples.md`
- `evals/benchmark.md`（新增 voice 样本 case）

### 验收标准

- 给出同一段待改文本时，提供 voice 样本后的结果，与未提供样本版本相比，更接近样本的句长和语气
- 没有明显增加幻觉或事实漂移
- 不会过度模仿样本中的具体用词

---

## P0-02：Residual Audit / Two-pass

### 目标

解决“第一遍改完还是有轻微 AI 味”的问题。

### 行为要求

引入一个简短的第二遍自检流程，只检查下面几件事：

- 是否残留开场套话 / 总结腔 / narrator 腔
- 是否句长过于均匀
- 是否还存在空泛判断
- 是否改成了“很干净但太整齐”的答案风

### 推荐实现方式

在 `SKILL.md` 中把当前回读阶段拆成两个层次：

1. **保真回读**
2. **残留味回读**

### 重要边界

- 第二遍不是重写全文
- 第二遍只做轻量修正
- `docs / status` 默认更保守

### 需要同步修改

- `SKILL.md`
- `references/operation-manual.md`
- `README.md`
- `CHANGELOG.md`
- `references/examples.md`

### 验收标准

- 对已有 AI 味重文本，第二遍结果比第一遍更自然
- 对误杀高风险文本，不会因为第二遍而被过度口语化

---

## P0-03：Protected Spans / Facts Ledger

### 目标

让模型在追求自然时，更稳地保住事实和技术上下文。

### 行为要求

在改写前，先识别下列不可随意改写的片段：

- 数字
- 日期
- 人名 / 项目名 / 公司名
- 路径 / 文件名 / 参数名
- API / 字段名
- 命令
- 引用原文
- 代码块
- 报错文本
- 指标数据

### 建议新增文件

- `references/protected-spans.md`

### 需要同步修改

- `SKILL.md`
- `references/scene-guardrails.md`
- `README.md`
- `CHANGELOG.md`
- `evals/benchmark.md`（新增 protected spans case）

### 验收标准

- 复杂 docs/status/code-context 样本中，术语和关键事实更稳定
- 改写前后，数字、路径、参数和引用原文默认不漂移

---

## P0-04：Positive Style Contract

### 目标

补齐“不能说什么”之外的“改完应该像什么”。

### 行为要求

新增一份正向风格文档，明确鼓励以下特征：

- 说清楚动作和对象
- 少一点空洞总括
- 句长有轻微波动
- 允许口语，但不装
- 不追求油滑
- 不追求每句都像抛光过的模板
- 不解释“我现在要开始解释了”

### 建议新增文件

- `references/positive-style.md`

### 需要同步修改

- `SKILL.md`
- `README.md`
- `CHANGELOG.md`
- `references/examples.md`

### 验收标准

- 结果不只是“没黑话”，而是明显更具体
- 不会统一变成一种新的模板风格

---

## P0-05：Real Sample Eval Pack

### 目标

评测不只看规则命中，还要看“可发性”和“真人感”。

### 建议新增目录或文件

- `evals/real-samples.md`
- 或 `evals/real-samples/` 目录

### 样本类型建议

至少覆盖：

- README 简介
- GitHub release note
- X 短帖
- Linux.do 长帖
- issue 回复
- commit message
- docstring
- 开发进度同步
- 公开项目介绍

### 每条样本的记录字段

- 原文
- 场景
- 为什么像 AI
- 不该改坏什么
- 推荐结果
- 评估维度（自然 / 保真 / 可发）

### 验收标准

- 新版本发布时，可以展示 5–10 条真实样本对比
- 可以作为后续增长素材和 benchmark 资产复用

---

## 6. P1 任务详细说明

## P1-01：Scene Packs

把现在的 4 类大场景细分成更贴近真实使用的子场景：

- `forum-post`
- `X-post`
- `README`
- `release-note`
- `commit-message`
- `docstring`
- `issue-reply`

这样改写会更稳，因为“公开写作”这个类还是太大。

## P1-02：Lite vs Full 产品化

把下面这件事写得更清楚：

- `SKILL.md` = lite / fallback
- `SKILL.md + references/` = full mode

并在 README / install 文档里明确告诉用户：

- 什么情况下只用 lite
- 什么情况下必须上 full

## P1-03：Copilot / 更多平台文档

如果要扩大分发范围，建议补：

- `install/copilot.md`
- 其他 agent/editor 的接入说明

文档里重点说明：

- 怎么触发
- 哪些场景会生效
- 怎么验证是否接上了
- 怎样使用 annotation mode

## P1-04：Bad-case intake 机制

新增：

- `ISSUE_TEMPLATE`：提交 bad case
- `DISCUSSION_TEMPLATE`：征集真实样本
- 一个 pinned issue：`收集“改完还是有 AI 味”的案例`

让社区贡献不再只会“加词”，而是能贡献更有价值的真实样本。

---

## 7. 建议新增的仓库结构（未来态）

```text
shuorenhua/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── references/
│   ├── phrases-zh.md
│   ├── phrases-en.md
│   ├── structures.md
│   ├── severity.md
│   ├── operation-manual.md
│   ├── scene-guardrails.md
│   ├── positive-style.md
│   ├── voice-calibration.md
│   ├── protected-spans.md
│   └── examples.md
├── evals/
│   ├── benchmark.md
│   ├── real-samples.md
│   └── results-*.md
├── install/
│   ├── codex.md
│   ├── chatgpt.md
│   ├── copilot.md
│   └── ...
└── .github/
    ├── ISSUE_TEMPLATE/
    └── DISCUSSION_TEMPLATE/
```

---

## 8. Definition of Done（每次任务都要满足）

一个任务完成，至少要同时满足：

1. 规则逻辑已写进主文档
2. 边界与误杀风险写进参考文档
3. README 口径同步
4. CHANGELOG 有记录
5. 至少新增一个样本或 benchmark
6. 示例可复制，不只是抽象说明

如果这 6 条不同时满足，就不算真正完成。

---

## 9. Codex 的一次性接管 Prompt

下面这段可以直接作为一次性接管 prompt：

```text
你正在接手开源项目 shuorenhua。先完整阅读 README.md、SKILL.md、CHANGELOG.md、CONTRIBUTING.md、evals/benchmark.md，以及 references/ 下的所有规则文件。项目目标不是堆更多禁用词，而是在不损害事实、术语、责任主体的前提下，提高中文文本的自然表达度，减少 AI 模板感和表演感。

开发时遵守这些原则：
1. 先 benchmark，后规则；没有样本不要直接加规则。
2. 先模式，后词条；变体优先归并，不要机械扩词表。
3. 不编造事实、来源、数据、人物、年份。
4. docs/status/code-context 场景优先保守。
5. 每次规则变更都同步 README、CHANGELOG、examples 和至少一个 eval case。
6. 不把项目带向“骗 AI detector”的方向。

当前优先级：
P0：Voice Calibration Lite、Residual Audit、Protected Spans、Positive Style Contract、Real Sample Eval Pack。
请先输出一个执行计划，再按优先级逐项修改文件，并在每一步说明：
- 改了哪些文件
- 为什么这么改
- 新增了哪些 case
- 还有什么风险边界
```

---

## 10. Codex 的单任务 Prompt 模板

下面这段适合你以后一次只让 Codex 做一个任务：

```text
你现在只做 shuorenhua 的一个任务：{任务名}。

先阅读以下文件：
- SKILL.md
- README.md
- CHANGELOG.md
- evals/benchmark.md
- references/ 下与该任务相关的文件

任务目标：
{写清楚目标}

必须遵守：
1. 不编造事实
2. 不增加误杀风险而不写边界说明
3. 改规则必须同步 README 和 CHANGELOG
4. 至少新增一个 benchmark 或 example
5. 不要大面积重写无关文件

输出顺序：
1. 先给执行计划
2. 再修改文件
3. 再总结变更点
4. 最后列出新增的 benchmark / example 和剩余风险
```

---

## 11. 你作为作者最该盯住的 3 个点

Codex 可以帮你持续开发，但你自己最好始终盯住下面三件事：

### 1）有没有越来越像“规则越多越僵”

如果是，就说明负向约束太多，正向风格不够。

### 2）有没有越来越依赖“新词入库”

如果是，就说明模式抽象还不够。

### 3）有没有真实样本越来越少、抽象规则越来越多

如果是，项目会越来越像“聪明的文档”，而不是“好用的工具”。

---

## 12. 最后的开发判断

下一阶段最值钱的不是继续加 50 个新词，而是把下面这条链路打通：

> **真实 bad case → 新模式抽象 → 规则落地 → 边界防护 → benchmark / example → README / release 素材**

只要这条链路跑顺，`说人话` 就会进入一个可持续积累的状态。  
反过来，如果只是继续往词表里塞词，项目会很快碰到上限。
