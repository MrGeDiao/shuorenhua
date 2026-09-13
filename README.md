<h1 align="center">说人话：中文 AI 味清理 skill</h1>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" alt="说人话：中文 AI 味清理 skill — 先保信息，再谈风格" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/MrGeDiao/shuorenhua/stargazers"><img src="https://img.shields.io/github/stars/MrGeDiao/shuorenhua?style=for-the-badge&amp;label=stars" alt="GitHub stars"></a>
  <a href="https://github.com/MrGeDiao/shuorenhua/releases"><img src="https://img.shields.io/github/v/release/MrGeDiao/shuorenhua?style=for-the-badge&amp;label=release" alt="GitHub release"></a>
  <a href="evals/benchmark.md"><img src="https://img.shields.io/badge/benchmark-123%20cases-2563eb?style=for-the-badge" alt="Benchmark: 123 cases"></a>
  <a href="evals/real-samples.md"><img src="https://img.shields.io/badge/scenario%20samples-20-16a34a?style=for-the-badge" alt="Scenario samples: 20"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/MrGeDiao/shuorenhua?style=for-the-badge" alt="License"></a>
</p>

`说人话`是一个中文优先的文字编辑 skill，用来清理套话、重复铺垫和生硬句式。数字、条件、承诺和作者本来的意思要保留；正常文字可以不改。

适合改 README、Release Note、工作同步、issue 回复和个人文章，也支持英文与只标问题。它不判断文章是不是 AI 写的，不提供“AI 含量”或规避检测的保证。

**v2.5.0 已发布。** v2.4.1 的修复并入本版。Claude Opus 5 完成 136 条、Grok 4.6 完成 56 条定向验收；范围、结果与限制见[评测记录](evals/results-v2.5.0.md)。

## 怎么用

把原文交给支持加载 skill 的工具，然后说明要求：

```text
把这段去掉套话，保留信息和我的口气：……
只在句内改，不删句、不并句：……
只标问题，不改写：……
```

默认交完整改写稿，不附判定链和评分。不需要修改时返回原文；来源提示和删除建议放在正文后。

例如，原文是：

> 本次完成了对重试策略的调整。重试策略已经调整过了。重复请求从 24 次降到 7 次。

可以改成：

> 本次调整了重试策略，重复请求从 24 次降到 7 次。

但“得到批准后，我可以周五前交一版草案”里的条件、“可以”和交付动作都要留下，不能顺手改成确定承诺。更多对照见[示例](references/examples.md)。

## v2.5 改了什么

运行规则收为三个文件：[入口](SKILL.md)、[编辑边界](references/editing-guide.md)、[示例](references/examples.md)。两份参考按需读取。旧词表、场景包和固定多步流程退出运行包，完整快照留在[历史目录](evals/legacy-v2.4.1/)。

编辑按内容判断，不按词语命中次数替换。“闭环控制”、引用中的“赋能”、有意重复和真实对比都可以保留。原文只谈潜力或目标时，也不要求模型补出具体实现。

程序代码块（包括注释和文档字符串）默认逐字保留；只有用户明确点名修改注释或说明文字时才编辑相应部分，且不改程序行为。代码围栏里的普通文案仍可按要求清理。

来源处理有一项明确变化：“研究表明”没有附出处时，默认保留归属与论断，必要时在正文外提示缺来源。用户明确要求删除无源论断或指定 `rewrite-safe`，才按允许的范围处理；不能只删“研究表明”，把结论变成已核实的事实。

引号按用途判断：作为依据的原话、文献、规范、界面文字、正在定义的词，以及书名号里的标题和名称按原文保留。叙述中的讲话可以清理口头填充和重复，保留说话人的事实、判断和“可能”“我觉得”等情态；用户要求保留口述原貌时不改。

默认改写较保守：清理赘语和句法，保留背景、定位、程度与作者评价。心理、感受和安抚类陈述也先保留；明确要求删去这类内容时再处理。审稿模式可以指出问题，但不会替作者撤回判断。

## 控制改动范围

| 要求 | 改动范围 |
|---|---|
| 自由调整 / `structural` | 可删、并、重排，保留有效信息和作者意图 |
| 保留结构 / `bounded` | 句内清理；整句删除只提建议，正文保留，不并句、不重排 |
| 只在原位改 / `in-place` | 不删句、不并句、不重排；要求保句数时也不拆句 |

用户要求优先。中文公开长文约 1000 字以上默认保留句段结构。`minimal / standard / aggressive` 仍可使用，只表示编辑幅度，不放宽保真要求。

## 安装

安装 full 时 只复制 [runtime-files.json](runtime-files.json) 列出的三个文件，保持相对目录。不要把 `evals/` 和 `tasks/` 放进 skill 扫描目录。仓库开发文件不会自动更新已安装副本。

| 用法 | 文件 |
|---|---|
| mini | [自包含短版](dist/shuorenhua-mini.md)，适合粘贴到单次对话 |
| lite | 只读 `SKILL.md`，遇到细节边界时可补参考 |
| full | `SKILL.md` 与两份参考文件 |

已有安装入口见 [Codex](install/codex.md)、[Claude Code](install/claude-code.md)、[Cursor / Windsurf](install/cursor.md)、[OpenClaw](install/openclaw.md)、[ChatGPT](install/chatgpt.md)。请按对应工具的说明安装；升级前先核对本地定制。

## 怎么验证

评测先看保真与任务是否完成，再看编辑是否有阅读收益。判据独立于 skill 文案，也不指定某个模型必须当判官。

主集 123 条，其中 65 条待改善文本、58 条正常文本；新增 3 条按引号用途判断的用例。已完成 Claude Opus 5 的 136 条和 Grok 4.6 的 56 条定向验收。信息与任务硬失败均为零，正向样本各有 5/7 条改善、2 条持平。Claude 正常文本误改为 0/58；Grok 只覆盖其中 11 条，未发现误改，不代表完整误改率。20 条场景样本与 10 篇 HUMAN 长文各自记录，不相加。新版使用冻结的中性请求和[编辑质量判据](evals/v2.5/criteria.md)，不要求模型删除某个指定句式。

发布要求包括信息与任务硬失败为零、正常文本误改率低于 10%，以及 7 条正向编辑样本至少 5 条有收益。脚本通过只证明结构和证据校验通过，不证明改写质量达标。

## 常见问题

**还会误改吗？** 会。尤其要核对否定范围、可能与承诺、作者判断和长文中的结构限制。欢迎附脱敏原文、请求与实际输出反馈。

**英文能用吗？** 可以。默认保留原文语言，重点仍是中文。不会为了避开某个英文词而改换事实。

**能模仿某个人的文风吗？** 本项目主要清理多余表达，保留原有口气。它没有针对特定作者做风格训练。

## 参与贡献

请用 [Bad Case 模板](.github/ISSUE_TEMPLATE/bad-case.md) 提供具体原文、编辑要求和输出；避免提交未授权聊天、密钥或个人隐私。新问题优先补可复现案例，是否需要加规则再看证据，见[贡献说明](CONTRIBUTING.md)。

## English

**shuorenhua** is a Chinese-first editing skill. It removes unnecessary wording while preserving facts, conditions, modality, attribution, and the writer’s voice. It also supports English and review-only requests. Version **2.5.0** rebuilds the editing rules; validation coverage and limitations are recorded separately. It is not an AI authorship detector.

## 相关项目

- [stop-slop](https://github.com/hardikpandya/stop-slop) — 英文冗余表达规则
- [humanizer](https://github.com/blader/humanizer) — 英文写作模式整理
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — AI 写作问题分类
- [speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw) — 繁体中文编辑规则

## Star 增长

[![说人话 star 增长曲线](https://raw.githubusercontent.com/MrGeDiao/shuorenhua/star-data/star-growth.svg)](https://github.com/MrGeDiao/shuorenhua/stargazers)

## 许可

[MIT](LICENSE)
