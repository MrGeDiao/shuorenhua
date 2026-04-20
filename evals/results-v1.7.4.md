# v1.7.4 评测结果

> 复核时间：2026-04-20
> 复核方式：静态 benchmark 复核（读规则文件逐项推理；等同于 CHANGELOG 历次 smoke test 的口径）
> 评测集：`evals/benchmark.md`（54 条：31 SF + 23 SNF）+ `evals/real-samples.md`（14 条整段样本）

> **追溯说明**：`v1.7.2` 和 `v1.7.3` 发布时没有单独归档 `results-*.md` 文件。本份 `results-v1.7.4.md` 追溯性地覆盖 `v1.7.1 → v1.7.4` 之间的评测演进，并固化 `v1.7.4` 新增的两条回归护栏。

## 通过率

| 指标 | 结果 | 目标 |
|------|------|------|
| SF 通过率 | 31/31 (100%) | > 90% ✅ |
| SNF 误杀率 | 0/23 (0%) | < 10% ✅ |
| code-context | 7/7 (100%) | 只改注释 / docstring / commit message ✅ |
| mixed | 2/2 (100%) | 只改有问题的正文 ✅ |
| Residual Audit | 3/3 (100%) | 第二遍只做轻量修正 ✅ |
| 接住体语境判断 | 3/3 (100%) | `SF-31` 命中姿态层，`SNF-22 / SNF-23` 放行技术语境 ✅ |

## 自 v1.7.1 以来的 benchmark 增量

| 版本 | 新增用例 | 作用 |
|------|----------|------|
| v1.7.2 | — (未动 benchmark.md，新增 `real-samples.md` 12 条) | 引入整段真实样本，补 benchmark 的"结构清晰但不像真实素材"短板 |
| v1.7.3 | `SF-31`（chat：过度接住 + 心理判断 + 身份认证式夸奖）；`real-samples.md` 扩到 14 条（含 `RS-14` 社区标题 / 宣言腔） | 把 Claude Opus 4.7 / GPT-5.4 共有的"接住体"姿态链固化为用例 |
| v1.7.4 | `SNF-22`（code-context：接住突发请求）、`SNF-23`（docs：限流网关稳稳接住上游峰值请求） | 回归护栏：防止未来改规则时误杀"接住请求 / 流量"的技术语境 |

## Should Fix 详情

| 用例 | 场景 | Tier | 档位 | 结果 | 备注 |
|------|------|------|------|------|------|
| SF-01 | `chat` | Tier 1 | `minimal` | ✅ | 删开场套话、谄媚和教学腔，直接回答问题 |
| SF-02 | `status` | Tier 1 + Tier 2 | `standard` | ✅ | 去渲染层，不编造指标，允许明确"需补数据" |
| SF-03 | `public-writing` | Tier 1 | `standard` | ✅ | 商业黑话改回普通动作和结果 |
| SF-04 | `docs` | Tier 1 | `minimal` | ✅ | 去否定式列举和二元对比骨架 |
| SF-05 | `public-writing` | Tier 1 | `standard` | ✅ | 无源引用按 `rewrite-safe` 处理，不补假来源 |
| SF-06 | `chat` | Tier 1 | `minimal` | ✅ | 总结式收尾整段可删 |
| SF-07 | `docs` | Tier 1 + Tier 2 | `minimal` | ✅ | 英文 inflation / meta-commentary 清掉，保留文档语体 |
| SF-08 | `public-writing` | Tier 1 | `standard` | ✅ | 去碎句格式、金句感和拔高骨架 |
| SF-09 | `status` | Tier 1 + Tier 2 | `standard` | ✅ | 被动堆砌改回主动表达，不补假数据 |
| SF-10 | `public-writing` | Tier 1 | `standard` | ✅ | 英文 sycophantic opener 和 meta-commentary 全删 |
| SF-11 | `chat` | Tier 1 | `standard` | ✅ | 调试腔映射回正常动作表达 |
| SF-12 | `public-writing` | Tier 1 | `aggressive` | ✅ | 网感词密集，直接压回正常分享口气 |
| SF-13 | `public-writing` | Tier 1 | `standard` | ✅ | 去掉鸡汤结构和正能量收尾 |
| SF-14 | `chat` | Tier 1 + Tier 2 | `standard` | ✅ | 学术腔、网感、商业黑话、工程腔统一回单一口语 |
| SF-15 | `status` | Tier 2 + 结构问题 | `standard` | ✅ | 打破句长过匀，只做节奏层轻改 |
| SF-16 | `public-writing` | Tier 1 | `standard` | ✅ | 价值拔高骨架全部拆掉 |
| SF-17 | `chat` | Tier 1 | `standard` | ✅ | 变体归并生效，删庸医 / 暴力 / 调试姿态层 |
| SF-18 | `docs` | Tier 1 + Tier 2 | `minimal` | ✅ | 无源引用按 `audit-only`；点明缺来源，不伪装成已证实 |
| SF-19 | `chat` | Tier 1 | `standard` | ✅ | mixed 样本只改引号内正文，不动用户指令 |
| SF-20 | `public-writing` | Tier 1 | `standard` | ✅ | 英文无源引用按 `rewrite-safe` 处理 |
| SF-21 | `status` | Tier 1 | `minimal` | ✅ | 无源引用按 `audit-only`，明确缺来源 / 归属 |
| SF-22 | `docs` | Tier 1 | `minimal` | ✅ | `code-context`，只改 docstring，不动代码 |
| SF-23 | `status` | Tier 1 | `minimal` | ✅ | `code-context`，commit message 改回动作导向 |
| SF-24 | `docs` | Tier 1 | `minimal` | ✅ | `code-context`，只改注释，不动实现 |
| SF-25 | `status` | Tier 1 | `minimal` | ✅ | 日期、指标、人名、字段、时间点全部保真 |
| SF-26 | `docs` | Tier 1 | `minimal` | ✅ | 版本号、命令、报错、配置值全部保留 |
| SF-27 | `docs` | Tier 1 | `minimal` | ✅ | 只清理注释姿态层，事实型 spans 全保真 |
| SF-28 | `public-writing` | Tier 1 | `standard` | ✅ | Pass 1 保真后，Pass 2 只收 narrator 残留 |
| SF-29 | `chat` | Tier 1 | `minimal` | ✅ | Pass 2 只删开场残留和总结残留 |
| SF-30 | `status` | Tier 1 | `minimal` | ✅ | Pass 2 只删空泛判断，不把 `status` 写口语化 |
| SF-31 | `chat` | Tier 1 + Tier 2 | `standard` | ✅ | 接住体姿态链整层删：`我就在这里 / 不躲不藏 / 稳稳接住 / 你不是……你只是…… / 顶刊作者的素养` |

## Should NOT Fix 详情

| 用例 | 场景 | 误杀? | 理由 |
|------|------|-------|------|
| SNF-01 | `docs` | ✅ 未误杀 | 技术文档里的系统主语描述真实系统行为 |
| SNF-02 | `docs` | ✅ 未误杀 | RFC 原文引用应原样保留 |
| SNF-03 | `status` | ✅ 未误杀 | `然而` 单独出现，不构成 Tier 2 聚集 |
| SNF-04 | `docs` | ✅ 未误杀 | `leverage` 在金融语境里是标准术语 |
| SNF-05 | `docs` | ✅ 未误杀 | `navigates / traversing` 是图算法的字面技术动词 |
| SNF-06 | `status` | ✅ 未误杀 | 变更日志允许这种简洁硬语气 |
| SNF-07 | `chat` | ✅ 未误杀 | `重要 / 确保` 属于 Tier 3，低频使用合理 |
| SNF-08 | `docs` | ✅ 未误杀 | `赋能` 在这里是被讨论词，不是正文姿态词 |
| SNF-09 | `docs` | ✅ 未误杀 | 学术语体里的正常被动不该机械改成主动 |
| SNF-10 | `status` | ✅ 未误杀 | `status` 报告可合理使用第三人称团队叙述 |
| SNF-11 | `chat` | ✅ 未误杀 | 有参数、操作时长和结果，是正常真人 debug 对话 |
| SNF-12 | `public-writing` | ✅ 未误杀 | 有具体技术经历支撑的网络用语不算批量 AI 腔 |
| SNF-13 | `status` | ✅ 未误杀 | 纯技术报告语域一致，术语和数据都承载事实 |
| SNF-14 | `docs` | ✅ 未误杀 | 这里在讨论词条维护策略，被讨论词不能误杀 |
| SNF-15 | `docs` | ✅ 未误杀 | 长段技术复盘有具体参数、动作和结果，工程语汇应保留 |
| SNF-16 | `chat` | ✅ 未误杀 | mixed 样本里这些词是引用和讨论对象，不是正文姿态 |
| SNF-17 | `docs` | ✅ 未误杀 | 注释本身已经具体、直接且有参数 |
| SNF-18 | `status` | ✅ 未误杀 | commit message 已经具体、事实性强 |
| SNF-19 | `status` | ✅ 未误杀 | 时间、动作、数值、下一步已经足够直接 |
| SNF-20 | `docs` | ✅ 未误杀 | 第二遍不该为了节奏改写技术说明和配置项 |
| SNF-21 | `status` | ✅ 未误杀 | 第一遍已经够直接，第二遍应停手 |
| SNF-22 | `code-context` | ✅ 未误杀 | `接住` 宾语是 `突发请求`，有系统主语（`handleBurst`）和边界说明（`p99 突刺`、`令牌桶节流`），`phrases-zh.md:90` 明确放行 |
| SNF-23 | `docs` | ✅ 未误杀 | `稳稳接住` 宾语是 `上游峰值请求`，技术语境完整（`max_concurrency=256`、`429`、`gw.shed_rate`），`operation-manual.md:213` 的保留条件全满足 |

## Real Samples 复核（v1.7.2 起）

`evals/real-samples.md` 14 条整段样本按 3 维打分（自然 / 保真 / 可直接发，各 5 分制）。v1.7.4 不在这批样本上继续扩量，延续 v1.7.3 的状态。

| 样本 | 场景 | 可直接发 | 备注 |
|------|------|----------|------|
| RS-01 ~ RS-12 | 混合 | ≥ 4/5 | 首批 v1.7.2 入库：README 简介、release note、X 短帖、Linux.do 长帖、issue 回复、commit message、docstring、开发进度同步、技术博客开头、微信对话、知乎长回答、混合场景 |
| RS-13 | `chat` | ≥ 4/5 | v1.7.3 新增：完整"接住体"样本（`稳稳接住 / 你不是……你只是…… / 顶刊作者的素养`），对齐 `SF-31` |
| RS-14 | `public-writing` | ≥ 4/5 | v1.7.3 新增：社区标题 / 宣言腔（`稳稳地接住所有人`），覆盖 Lite 模式的兜底口径 |

## 关键口径

- `SF-05`、`SF-20`：`public-writing / chat` 的无源引用按 `rewrite-safe` 计分。删掉无证据权威铺垫、不补假来源，即记 `✅`。
- `SF-18`、`SF-21`：`docs / status` 的无源引用按 `audit-only` 计分。明确指出缺来源或缺归属，不把原句伪装成已证实结论，即记 `✅`。
- `SF-28`、`SF-29`、`SF-30`：先做 Pass 1 保真回读，再做 Pass 2 Residual Audit。第二遍只删 narrator / 开场 / 总结 / 空泛判断等残留，不重写全文。
- `SF-31`：整组"接住体"姿态链（`过度接住 + 心理判断 + 身份认证式夸奖`）命中时整层删除，不能只删一两个词留空壳姿态。
- `SNF-22 / SNF-23`：`接住` 的判定优先看宾语。宾语是人 / 情绪 / 关系 / 需求 → 按姿态层处理；宾语是请求 / 流量 / 峰值 / 异常 → 回到技术语境判断，有系统主语、参数、结果时放行。
- 全部 `code-context` 样本都遵守"只动注释 / docstring / commit message，不动代码本体"。

## 摘要

- `v1.7.2` 把"是否像真人"从纯规则命中扩成 3 维打分（自然 / 保真 / 可直接发），用整段样本补 benchmark 的结构化短板。
- `v1.7.3` 没有继续扩词表，而是把"接住"从单词命中升级为按宾语判断的语境规则，并用 `SF-31` + `RS-13 / RS-14` 把 Claude Opus 4.7 / GPT-5.4 共有的姿态链固化为可回归的用例。
- `v1.7.4` 是对 v1.7.3 规则的**回归护栏补齐**：新增 `SNF-22 / SNF-23` 两条技术语境放行用例，防止未来改规则时把 `接住请求 / 接住流量 / 稳稳接住上游峰值请求` 一起误杀。两条新 SNF 在 v1.7.3 的现有规则下均按预期放行，不需要修改规则文件。
- 和 `v1.7.1` 相比，整个 v1.7.x 的脉络是"把真实信号分层评测"：合成 benchmark（规则命中）+ 整段真实样本（自然度）+ 回归护栏（误杀保护）。
