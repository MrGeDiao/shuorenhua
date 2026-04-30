# Community Sample Intake — 运行说明

> 维护者本地工具的运行入口。
> 协议规范（什么是 intake、为什么做）见 `./intake.md`，prompt 本体见 `./intake-prompt.md`。
> 这份 README 只解决"具体怎么跑一次"。

## 什么时候跑

- 公开讨论（X / Linux.do / V2EX / 知乎 / Reddit 等）出现一批新的 AI 姿态链
- 怀疑现有词表可能没收住，但又不确定是变体还是新模式
- 触发条件全集见 `CONTRIBUTING.md` 「维护者：Community Observation Intake」一节

## 文件约定

工具本体（committed）：

| 角色 | 路径 |
|------|------|
| 协议规范 | `automation/intake.md` |
| Prompt 本体 | `automation/intake-prompt.md` |
| 运行说明 | `automation/README.md`（本文件） |

运行实例（local-only，`tasks/` 在 `.gitignore` 内）：

| 角色 | 路径 |
|------|------|
| 输入（本轮样本批次） | `tasks/current/intake/inbox/<YYYY-MM-DD>.md` |
| 输出（本轮 intake 报告） | `tasks/current/intake/reports/<YYYY-MM-DD>-intake.md` |

输入文件每条样本带"来源 / 原文 / 提交者备注"三栏，越接近原始观察越好。dryrun 参考样本和 expected baseline 见仓库内 commit 历史里 v1.8.2 的相关引用。

## 一条命令跑完

在仓库根目录执行（替换日期）：

```bash
codex exec -C . -s read-only --ephemeral \
  -o tasks/current/intake/reports/2026-05-01-intake.md \
  '你正在执行说人话仓库的 intake automation。

请完整读取 ./automation/intake-prompt.md，按其中 text 代码块里的 prompt 行事。该 prompt 已固定：要先读哪些 reference、如何按"已覆盖 / 变体归并 / 候选新模式"三档归类、强约束（默认不要建议加词条；不要把被讨论词、引用词、真人具体叙事误判成 AI 腔），以及最终输出格式。

本轮样本批次在 ./tasks/current/intake/inbox/2026-05-01.md。

请直接输出最终的 intake 报告，按 prompt 推荐的格式（本轮样本数 / 已覆盖 / 变体归并 / 候选新模式 / 建议动作 / 一句总判断），不要附加任何过程叙述或 meta 评论。'
```

关键参数说明：

- `-C .` — 让 codex 把仓库根作为工作目录，prompt 里的相对路径才能解析
- `-s read-only` — 沙箱锁死成只读，强约束"不自动改仓库"用沙箱兜一次底
- `--ephemeral` — 不持久化 session，单次任务即跑即弃
- `-o <报告路径>` — 直接把模型最终输出落到 reports 目录，不依赖 stdout 复制粘贴

> `tasks/current/intake/inbox/` 和 `reports/` 这两个目录在 `.gitignore` 内，第一次用前手动 `mkdir -p` 一次即可。

## 跑完之后

报告里只会出现四类建议动作：`无动作 / 补 benchmark / 补 operation-manual / 考虑新增词条或结构`。

- 默认假设：本轮**不需要**直接改仓库
- 如果建议是 `补 benchmark`：人工评估后再去改 `evals/benchmark.md`
- 如果建议是 `补 operation-manual`：人工评估后再去改 `references/operation-manual.md`
- 如果建议是 `考虑新增词条或结构`：先观察 2-3 轮，确认是否反复出现，再考虑入库
- 任何动作都**不应该**由 intake 自动完成；这一层是建议，不是落库

## Prompt 调坏了怎么办

如果哪天改 `intake-prompt.md` 让报告偏离 spec 推荐格式（6 段都缺、问题族归类乱、被讨论词被误判成 AI 腔），就说明 prompt 调坏了——回滚或重新校准。校准时建议先准备一份覆盖三档结论 + 两类陷阱（被讨论词、技术语境放行）的合成样本批次作为 expected baseline，跑完比对。
