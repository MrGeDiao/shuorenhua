# v1.8.0 评测结果

> 复核时间：2026-04-24
> 复核方式：TDD 静态复核（先补 scene pack 回归用例，再写最小规则和接入点）
> 评测集：`evals/benchmark.md`（62 条：35 SF + 27 SNF）+ `evals/real-samples.md`（18 条整段样本）

## 通过率

| 指标 | 结果 | 目标 |
|------|------|------|
| SF 通过率 | 35/35 (100%) | > 90% ✅ |
| SNF 误杀率 | 0/27 (0%) | < 10% ✅ |
| Scene Packs | 8/8 (100%) | 4 SF + 4 SNF 全覆盖 ✅ |
| Real Samples | 18/18 可复核 | `保真` 和 `可直接发` 均可提升到 ≥ 4/5 ✅ |

## v1.8.0 增量

| 文件 | 增量 | 作用 |
|------|------|------|
| `evals/benchmark.md` | `SF-32` ~ `SF-35`，`SNF-24` ~ `SNF-27` | 用 TDD 先钉住 README、release note、forum post、issue reply 的正例和误杀边界 |
| `references/scene-packs.md` | 新增 4 个 scene pack | 把 `public-writing` 细分到可发布场景，不靠全局扩词表 |
| `SKILL.md` | 增加 scene pack 子场景入口 | 主流程先判大场景，再按发布目的收束语气 |
| `references/scene-guardrails.md` | 补分工说明 | 大场景边界仍由 guardrails 控制，scene packs 只做落地策略 |
| `evals/real-samples.md` | `RS-15` ~ `RS-18` | 用整段样本验证“改完能不能直接发” |

## Scene Pack 用例详情

| 用例 | 子场景 | 结果 | 备注 |
|------|--------|------|------|
| `SF-32` | `README` | ✅ | README intro 从价值口号改成“是什么、给谁用、解决什么问题” |
| `SF-33` | `release-note` | ✅ | release note 从发布宣言改成变更列表；缺 changelog 时不编数据 |
| `SF-34` | `forum-post` | ✅ | 社区帖保留维护者观察，去掉公告腔和方法论闭环 |
| `SF-35` | `issue-reply` | ✅ | issue 回复先确认问题和下一步，删客服式安抚 |
| `SNF-24` | `README` | ✅ 未误杀 | 已经直接的 README intro 保留术语和定位 |
| `SNF-25` | `release-note` | ✅ 未误杀 | 已经可扫描的 changelog 列表不改成故事 |
| `SNF-26` | `forum-post` | ✅ 未误杀 | 有具体经历支撑的社区帖保留口语感 |
| `SNF-27` | `issue-reply` | ✅ 未误杀 | 已经具体的维护回复不加寒暄 |

## Real Samples 复核

| 样本 | 场景 | 可直接发 | 备注 |
|------|------|----------|------|
| `RS-15` | `README` | ≥ 4/5 | README 第一段改成项目定位，不写愿景口号 |
| `RS-16` | `release-note` | ≥ 4/5 | release note 改成变更列表，保留版本号和文件名 |
| `RS-17` | `forum-post` | ≥ 4/5 | 社区帖保留维护者观察和口语，不改成公告 |
| `RS-18` | `issue-reply` | ≥ 4/5 | issue 回复保留维护动作，不做客服式安抚 |

## 关键口径

- Scene Packs 只细化 `public-writing` 的发布目的，不替代 `Protected Spans`、`Tier`、档位和 `Residual Audit`。
- README、release note、forum post、issue reply 四个场景的区别不是词表区别，而是发布目的区别：介绍项目、列变更、讲观察、回 issue。
- 本版不做 Voice Calibration / Voice Hints，不模仿名人、品牌或公众人物。
- 本版不做公开 bad-case 收集入口，继续留到 v2.0 和分发一起做。

## 摘要

v1.8.0 的主线不是继续扩词表，而是把 v1.7.x 已经稳定的规则落到可发布场景。新增 benchmark 先写失败边界，再用最小 Scene Packs 解释这些用例，最后用整段样本验证“可直接发”。这让 `public-writing` 从一个大场景，向 README、release note、forum post、issue reply 四个常用工作流落地。
