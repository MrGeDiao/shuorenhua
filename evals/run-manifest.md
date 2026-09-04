# 评测运行清单 | Run Manifest

> 2026-07-11 新增（发布前 deep review 反馈：外部读者无法核对实跑口径）。每次基线 / targeted 实跑在这里登记元数据；`results-*.md` 只放判分结论和硬指标，这里放"怎么跑出来的"。
> 原始模型输出在维护者本地 `tasks/current/eval-runs/`（gitignored），默认不入库；外部复现按 `automation/eval/README.md` 的命令自跑。
> 历史轮次按当时记录回填，缺项如实标「未记录」，从下一轮起按模板补齐。

## v1.9.0 全量双模型基线（2026-06-18）

- 评测集：`benchmark.md` @ v1.9.0（73 条：41 SF + 32 SNF）；仓库同期含 `real-samples.md` 19 条场景样本，本轮未纳入批跑（批次只覆盖 SF/SNF，无 RS-xx 运行记录）
- 口径：双模型交叉——Codex 改写 → Claude 判；Claude 改写 → Codex 判。盲测未启用（当时被测模型可见预期；盲测 2026-07-11 起才有）
- 被测 / 判分模型：Codex CLI（具体模型版本未记录）；Claude Code `--model opus`（Claude Opus 4.8，dated model id 未记录）
- CLI 版本：未记录
- 归档：`results-v1.9.0.md`（含 token / 成本 / 判分汇总）
- 原始输出：本地 `tasks/current/eval-runs/2026-06-18-{codex,claude,judge}/`（未入库）

## v1.9.1 targeted 单模型回归（2026-07-01）

- 评测集：`benchmark.md` @ v1.9.1（75 条：42 SF + 33 SNF）；范围 = v1.9.0 的 8 个边界用例 + #5 回归用例
- 口径：targeted 单模型回归 + 静态规则检查，非全量实跑
- 模型：具体版本未记录
- 归档：`results-v1.9.1.md`
- 原始输出：本地 `tasks/current/eval-runs/2026-07-01-v1.9.1-targeted/`（未入库）

## v1.9.2 targeted 交叉回归（2026-07-05）

- 评测集：`benchmark.md` @ v1.9.2（80 条：45 SF + 35 SNF）；范围 = 新增 5 条（SF-43/44/45、SNF-34/35）
- 口径：targeted 交叉回归（Codex 改写 + Claude 判读），非全量实跑
- 模型：具体版本未记录
- 归档：`results-v1.9.2.md`
- 原始输出：本地 `tasks/current/eval-runs/2026-07-05-v1.9.2-targeted/`（未入库）

## v2.0.0 盲测口径 smoke（2026-07-15）

- 评测集：`benchmark.md` @ v2.0.0（80 条：45 SF + 35 SNF）；范围 = B-01–08 流程 smoke + B-58/B-78 定向（SF-23/SF-15 预期修订专项），共 10 条
- 口径：盲测首跑（`benchmark-blind.md` 生成于 2026-07-15 工作区，种子 20260711）；目的 = 端到端流程验证 + 保真合同专项，非基线，判分结果不计入版本指标
- 被测模型：Codex CLI（盲改写；模型版本未记录）
- judge 模型：Codex 同线程自判一份（偏离交叉惯例，留档对照）+ Claude Code（Claude Fable 5，`claude-fable-5`）按固定配对补做独立交叉判分
- CLI 版本：codex 未记录 / claude 2.1.210
- 结论：格式合同全对齐（B 编号标题、四项判定链、三列判分表、汇总四件套）；B-58/B-78 输出无编造数据或技术选型，SF-15/SF-23 修订后合同端到端生效；判分汇总（交叉判）SF 3/7 ✅、SNF 误杀 0/3、❌ 无
- 已知缺口：`make_blind.py` 不传递 benchmark J 节的节级 scope 指令（SF-39 保长度 / SF-40 in-place），被测模型只见 `public-writing / long` 会按默认 bounded 处理；修掉之前 judge 对这两条不因 scope 判定记 ❌，修法待 v2.1.0 评估
- 原始输出：`tasks/current/eval-runs/2026-07-15-smoke/`（未入库）

## v2.1.0 全量盲测 + targeted 多模型回归（2026-07-23）

- 评测集：`benchmark.md` @ v2.1.0（82 条：46 SF + 36 SNF）；范围 = 82 条全量 + 10 条核心 targeted + 6 条共同问题最终 targeted
- 口径：全量双模型交叉（Codex 改写 → Claude 判；Claude 改写 → Codex 判）；盲测 = 是（种子 `20260711`）；Grok / Gemini 只作 targeted 模型差异诊断
- 被测模型：Codex CLI `gpt-5.6-sol`；Claude Code `opus→claude-opus-4-8`；Grok `grok-4.5→grok-4.5-build`；Agy `gemini-3.6-flash-medium→Gemini 3.6 Flash (Medium)`
- judge 模型：Claude Code `claude-opus-4-8` 判 Codex；Codex CLI `gpt-5.6-sol` 判 Claude / Grok / Gemini
- CLI 版本：codex 0.145.0 / claude 2.1.218 / grok 0.2.111 / agy 1.1.5
- 全量结果：Codex SF 38/46、SNF 误杀 1/36；Claude SF 26/46、SNF 误杀 1/36；全量发生在最终 6 条共享问题修复前，修复后只重跑 targeted
- 核心 targeted：Codex SF 9/9、SNF 误杀 0/1；Claude SF 6/9、SNF 误杀 0/1
- provenance：三体 live doctor 全绿；Grok session verifier 与 Agy conversation verifier 均通过；Grok targeted 因 B-11 标题前夹过程叙述而不计正式 harness 分数
- 最终入口合同微测：对齐 `SKILL.md` / rewrite prompt / README 后补跑 B-11 + B-61；Codex 与 Claude 均按新合同处理无源数字与 bounded 删除清单，不重算全量分数
- 归档：`results-v2.1.0.md`
- 原始输出：`tasks/current/eval-runs/2026-07-23-v2.1.0-{targeted,full,final-targeted}/`（未入库）

## v2.1.0 Fable 结构修复后双列协议 smoke（2026-07-23）

- 评测集：`benchmark.md` @ v2.1.0（82 条：46 SF + 36 SNF）；范围 = B-05 / B-13 / B-19 / B-40 / B-45 / B-55（SF-36 / SF-05 / SF-40 / SF-42 / SF-18 / SNF-34）
- 口径：复用 Fable 结构修复后生成的双模型盲改写，在最终 judge 协议上重新交叉判分；目的 = 验证 audit-only、方向认证、L3 可接受集与 SNF/L1 分列，不替代 82 条全量
- 被测模型：Codex CLI `gpt-5.6-sol`；Claude Code `opus→claude-opus-4-8`
- judge 模型：Claude Code `claude-opus-4-8` 判 Codex；Codex CLI `gpt-5.6-sol` 判 Claude
- CLI 版本：codex 0.145.0 / claude 2.1.218
- 结果：两边 L1 硬约束失败均为 0，SF 均为 5/5；Claude 输出 SNF 误杀 0/1，Codex 输出在 SNF-34 发生普通标点误杀 1/1。新版协议把后者稳定判为「硬约束 ✅、SNF 误杀 ❌」，没有再误算成 L1
- 归档：`results-v2.1.0.md` §6
- 原始输出：`tasks/current/eval-runs/2026-07-23-v2.1.0-rc-verify/`（未入库）

## v2.1.0 最终 82 条全量（2026-07-23）

- 评测集：`benchmark.md` @ v2.1.0（82 条：46 SF + 36 SNF）；范围 = B-01–82，五批完整运行
- 行为合同 diff-id：`41da53fc8f7db08140d695ecc838002186a516ad`；冻结后只追加结果归档，不改规则、benchmark 或 prompt
- 口径：双模型盲改写 + 固定交叉判分；Codex 改写 → Claude 判，Claude 改写 → Codex 判；judge 使用硬约束 / 风格或 SNF 误杀双列协议
- 被测模型：Codex CLI `gpt-5.6-sol`；Claude Code `opus→claude-opus-4-8`
- judge 模型：Claude Code `claude-opus-4-8` 判 Codex；Codex CLI `gpt-5.6-sol` 判 Claude
- CLI 版本：codex 0.145.0 / claude 2.1.218
- 完整性：两套改写均 82/82；两套 judge 均 82/82；无缺号、重复或 L0 作废批次
- Codex 结果：L1 失败 0；L2 41/43；L3 3/3；旧口径 SF 44/46；SNF 误杀 1/36
- Claude 结果：L1 失败 1（SF-27 / B-48）；L2 30/43；L3 3/3；旧口径 SF 33/46；SNF 误杀 3/36
- L1 争议审计：Claude 审计建议只记第二列，Codex 审计建议记 L1；按 `SKILL.md` 信息留存硬指标与 `protected-spans.md` 的 code-context 真实行为保护，最终维持 L1 ❌
- 发布判断：SNF 均 <10%，但 Claude 存在 1 个 L1 失败；正式 v2.1.0 不达门槛
- 归档：`results-v2.1.0.md` §7
- 原始输出：`tasks/current/eval-runs/2026-07-23-v2.1.0-final-full-41da53f/`（未入库）

## v2.1.0 关系保真修复后正式版验证（2026-07-23）

- 评测集：`benchmark.md` @ v2.1.0（82 条：46 SF + 36 SNF）；范围 = Codex / Claude 各一轮 B-01–82 + Claude 一次预先声明的完整稳定性确认轮
- 行为合同 diff-id：`d8408ce9edad998cba0cefcbc6372e84f3f07fb2`；确认轮前后未改规则、benchmark、blind 输入或 prompt
- 口径：82 条盲改写 + 双列 judge；Codex 输出由 Claude Opus 4.8 判。Claude 首轮 B-01–16 由 Codex 判，Codex CLI 随后触发用量上限（提示 2026-07-30 11:25 恢复），B-17–82 与确认轮改由 Grok 4.5 按同一 judge prompt 独立判分
- 被测模型：Codex CLI `gpt-5.6-sol`；Claude Code `opus→claude-opus-4-8`
- judge 模型：Claude Code `claude-opus-4-8`；Codex CLI `gpt-5.6-sol`（仅 Claude 首轮 B-01–16）；Grok `grok-4.5`（替代其余 Claude 输出 judge）
- CLI 版本：codex 0.145.0 / claude 2.1.218；Grok 当前默认模型清单确认 `grok-4.5`
- 完整性：Codex 全量、Claude 首轮、Claude 确认轮的改写与 judge 均为 82/82；无缺号或重复
- Codex 结果：L1 失败 0；L2 37/43；L3 3/3；旧口径 SF 40/46；SNF 误杀 2/36
- Claude 首轮：L1 失败 1（SF-07 / B-71）；L2 36/43；L3 3/3；旧口径 SF 39/46；SNF 误杀 3/36
- Claude 确认轮：不改规则后完整重跑；L1 失败 0；L2 36/43；L3 3/3；旧口径 SF 39/46；SNF 误杀 1/36
- targeted：B-53 / B-65 双模型 L1 均为 0；SF-12 残留单个 `避坑` 按分层记 L2 `⚠️`，不阻塞发布
- 发布判断：Codex 全量与 Claude 确认轮均满足 L1=0、SNF<10%；正式 v2.1.0 可发布。Claude 首轮 SF-07 失败作为随机不服从证据并列保留，不宣称所有运行全绿
- 归档：`results-v2.1.0.md` §8
- 原始输出：`tasks/current/eval-runs/2026-07-23-v2.1.0-release-final-d8408ce/`、`tasks/current/eval-runs/2026-07-23-v2.1.0-release-confirmation-d8408ce/`（未入库）

## v2.2.1 targeted 回归（2026-08-06）

- 评测集：`benchmark.md` @ v2.2.1（84 条：47 SF + 37 SNF）；范围 = B-12 / B-38（SF-47 / SNF-37）
- 口径：targeted 双模型交叉；盲测 = 是（`benchmark-blind.md` 2026-08-06 用固定种子重新生成）
- 被测模型：codex-cli 0.146.1（Codex 侧）/ Claude Opus 5 冷启动 subagent（Claude 侧）
- judge 模型：Codex 判 Claude 改写、Claude 判 Codex 改写（r2 轮双向交叉）
- CLI 版本：codex 0.146.1 / claude 2.1.222
- 已知偏差：本轮在 Claude Agent SDK 宿主环境下跑，凭证由宿主托管、不落盘（`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` 已设，无 `~/.claude/.credentials.json`），从 shell 另起的 `claude` 子进程拿不到 token（报 `Not logged in`，非账号问题）。Claude 侧因此改用冷启动 subagent，文件访问纪律与 CLI 口径一致（只给 `SKILL.md` + `references/` + `benchmark-blind.md`，不给含预期的文件）；同模型（Opus 5），但与历史轮次的 `claude --print` 进程路径不完全可比
- 结果：四轮迭代（r1 因用例卡阈值边界作废 / r2 / r3 出现由本版改动引入的回归 / r4 修复）；L1 硬失败 0（全轮）；SNF 误杀 0；SF-47 终轮 Claude ✅、Codex ⚠️（L2，不阻塞）
- 归档：`results-v2.2.1.md`
- 原始输出：`tasks/current/eval-runs/2026-08-06-{codex,claude,judge}/`（未入库）

## v2.2.1 影响面回归 7 条（2026-08-06）

- 评测集：`benchmark.md` @ v2.2.1（84 条：47 SF + 37 SNF）；范围 = B-12 / B-15 / B-25 / B-53 / B-54 / B-63 / B-79（SF-47 / SF-16 / SF-39 / SF-04 / SNF-29 / SF-40 / SNF-30）
- 口径：targeted 双模型交叉；盲测 = 是；选样依据 = 全库扫描后按新密度阈值行为会改变的全部用例（15 条含骨架，7 条达阈值），非抽样
- 被测模型：codex-cli 0.146.1 / Claude Opus 5 冷启动 subagent
- judge 模型：Codex 判 Claude、Claude 判 Codex（双向）
- CLI 版本：codex 0.146.1 / claude 2.1.222
- 结果：L1 硬失败 0（双侧）；**SNF 误杀 0/2（双侧）**；L2 口径 Codex 判 Claude 1/4、Claude 判 Codex 2/4；L3（SF-40）双侧 ✅
- 结论：新密度判据未引入误杀，也未造成「该改的反而不改」；两条 ⚠️ 的成因分别是词表层漏改与预期骨架覆盖不全，与第 1 条无关
- 归档：`results-v2.2.1.md` §7
- 原始输出：`tasks/current/eval-runs/2026-08-06-{codex,claude,judge}/*regression7*`（未入库）

## v2.3.0 targeted + 影响面跨模型盲测（2026-08-07）

- 评测集：`benchmark.md` @ v2.3.0（95 条：53 SF + 42 SNF）；范围 = 新增 11 条（SF-48–53 / SNF-38–42）+ 影响面 6 条（SF-32 / SNF-11 / SNF-12 / SNF-26 / SNF-29 / SNF-30）
- 口径：三路盲测 + 交叉判分；盲测 = 是（`benchmark-blind.md` 由固定种子 20260711 在 2026-08-07 生成，指纹 `5e930eff…`，全程未再生成）。三条路径均只读 `SKILL.md` / `references/` / `benchmark-blind.md`，看不到预期与映射
- 被测路径：Codex CLI 0.147.0（`gpt-5.6-sol`，reasoning `max`）；Claude Opus 5（Agent `model: opus` 冷启动）；Agent SDK 冷启动（`gpt-5.6-sol[1m]`，与 Codex 同模型不同执行路径）
- judge 路径：Codex 判 Claude（targeted + 影响面）；Claude 判 Codex（targeted）；Codex 判 SDK、SDK 判 Codex（targeted + 影响面）。judge 均在改写完成后才读预期
- 运行时间线：Claude 路径最初因订阅额度耗尽 + 宿主托管凭证不下发给 shell 子进程（`claude --print` 报 `Not logged in`）无法运行，先出了一版 Codex/SDK 同模型双路结论；额度恢复后在同一份未改动的规则与 blind 输入上补跑 Claude 路径，SDK 结果保留为同模型跨执行路径证据
- targeted 结果：四组判分硬约束失败均为 0、SNF 误杀均为 0/5；Claude 改写 SF **6/6**，Codex 与 SDK 改写均 5/6（⚠️ 均为 SF-52）；三对对照组全部判对；无 ❌
- SF-52 结论：Claude 路径全部还原本义并通过，证明第 25 条默认动作可达成；Codex / SDK 的 ⚠️ 属模型执行不彻底，不改预期、不加用例例外
- 影响面结果：三组判分硬约束失败 0；SF 1/1；SNF 误杀 0/5；无 ⚠️ / ❌。两条 long/in-place 无删句、并句、重排；三条具体经历 SNF 未被装饰性细节规则误杀
- 硬判：六份输出全部解析完整，长文硬下限失败 0；本轮据 Claude judge 反馈修掉一处报告措辞缺陷（非 in-place 长文一律被称作「bounded 长文」）
- 归档：`results-v2.3.0.md`
- 原始输出：`tasks/current/eval-runs/2026-08-07-v2.3.0-targeted/`（未入库）

## v2.3.0 合并阶段 targeted 跨模型验收（2026-08-10 / 2026-08-12）

- 评测集：`benchmark.md` @ v2.3.0 合并版（103 条：57 SF + 46 SNF）；范围 = 合并阶段新增 8 条 + 第一阶段新增 11 条影响面回归
- 口径：自动化完整性 / residual 标定 / 静态误杀扫描 + 双模型盲改写 + 固定交叉判分；盲测快照不含预期与映射，judge 在改写完成后才读取完整 benchmark 与分层规则
- 新增 8 条盲测号：B-29 / B-34 / B-57 / B-61 / B-78 / B-81 / B-93 / B-98
- 影响面 11 条盲测号：B-14 / B-21 / B-45 / B-46 / B-50 / B-51 / B-56 / B-72 / B-86 / B-94 / B-102
- 冻结指纹：`SKILL.md` = `b407e30a…`；`benchmark-blind.md` = `db35cfd3…`；rewrite prompt = `df611269…`；judge prompt = `1822c7fb…`
- 被测模型：Codex CLI `gpt-5.6-sol`（reasoning `max`）；Claude Code `--model opus`（effort `max`）
- judge 模型：Claude 判 Codex 输出；Codex 判 Claude 输出
- CLI 版本：codex 0.147.0 / claude 2.1.228
- 自动化结果：`check_repo` 103 用例 / 20 样本 / 24 锚点 / 94 链接 / 3 词表；`py_compile` 与 `git diff --check` 通过
- 标定结论：`「」/『』` 候选数 SF / SNF 的中位数与 p90 均为 0、max 均为 3，原始计数不可分，不设阈值
- targeted 结果：两组 judge 的 L1 硬失败均为 0、SNF 误杀均为 0/4、无 `❌`；Codex 输出 SF 2/4 `✅` + 2/4 `⚠️`，Claude 输出 SF 1/4 `✅` + 3/4 `⚠️`
- 影响面结果：两组 judge 的 L1 硬失败均为 0、SNF 误杀均为 0/5、无 `❌`；Codex 输出 SF 6/6，Claude 输出 SF 5/6 + SF-52 `⚠️`
- 数字准入线：SNF-45 / SNF-46 两模型整体 no-op，protected spans 分别 4/4、5/5；歧义倍数没有被改成新关系
- annotation mode：Codex / Claude 均判定新增词条与抒情词规则段属于术语定义 / 被讨论对象，建议改写项 0
- 发布判断：达到现行门槛；SF-55 两模型均有 L2 残留，作为已知执行弱点记录，不阻塞发布
- 归档：`results-v2.3.0.md` §9–§10
- 原始输出：`tasks/current/eval-runs/2026-08-12-v2.4.0-final/`（未入库；目录名保留内部里程碑编号）

## v2.3.1 候选全量基线与 HUMAN 标定（2026-08-19 / 2026-08-20）

- 评测集：`benchmark.md` @ v2.3.1 候选（111 条：61 SF + 50 SNF）；全量范围 B-01–111，HUMAN 8 篇另作 residual 假阳性参照
- 口径：Opus 5 + DeepSeek V4 Pro 独立盲改写、计划双向交叉判分；冻结 blind SHA256 `79dedd4247e0df8a292a883a282e1d80214e0f6cc829a5855348b6a7e063acdd`
- 被测模型：Claude Code CLI 2.1.237 / first-party `claude-opus-5`；Cindy Host 实际计费回执 `deepseek-v4-pro[1m]`
- 完整性：DeepSeek rewrite 111/111；Opus rewrite 111/111。Opus B-97–111 在订阅恢复后用全新 first-party Opus 5 会话补齐，没有重跑已成功批次
- judge：DeepSeek→Opus 96/111，L1 失败 1（B-39 / SF-27），缺 B-97–111；Opus→DeepSeek 111/111，L1 失败 1（B-95 / SF-07），SF L2 44/58，SNF 误杀 1/50
- B-39 审计：输入、映射、预期与 frozen rule 都要求保留 fallback 适用条件“高峰期流量”；raw 与归一化输出一致，运行 rc=0、模型身份和执行链正常，判定为 Opus 模型执行失败
- 认证核验：2026-08-20 17:51:30 +08:00 的 `claude auth status` 仍退出 1，但实际 first-party Opus 请求成功；后续 8 个新会话的原始 JSON 均验证 `claude-opus-5` / `firstParty`。因此将 `auth status` 记为 CLI 2.1.237 假阴性，不再当作实际可用性证据
- DeepSeek 最后 judge 缺口：原 Cindy Host / Orca Worker 通道当前不可调；直接 Claude CLI 请求 `deepseek-v4-pro` 返回 404 `unrecognized_model`，未用其他模型代替
- HUMAN：8/8 active，全 open，7 个作者组；3 篇历史 + 5 篇现代，6 篇中文原作 + 2 篇英译中。6 篇是场景 proxy，direct 只有 2 篇 public-writing；`--human-stats` 与 `--calibrate` 通过，`check_repo.py` 按预期被 direct 缺 docs/status 阻塞。逐篇固定 revision/UTC 时间、来源、许可、许可证据、改动和 AI 依据见 `human-corpus.jsonl`
- 失败后修复侧测（2026-08-20）：先冻结 14 条 task-local held-out，再修改保真回读；first-party Opus 5 与 Grok 4.6 均为 L1 0/14，历史 B-39/B-95 targeted 两模型 4/4。Grok 由 Santi verifier 核对 `grok-4.6-build` + fingerprint；原始输出在 `tasks/current/eval-runs/2026-08-20-l1-generalization-r1/`。这不是正式全量追分，旧 L1 与 NOT release-ready 状态保留
- 发布判断：**NOT release-ready**。两个独立 L1 均使 L1=0 门槛失败；另有一批 DeepSeek judge 缺失。不改门槛、不移除用例、不追分重跑
- 归档：`results-v2.3.1.md`
- 原始输出：`tasks/current/eval-runs/2026-08-19-v2.3.1-{targeted-r3,full-r3}/`（未入库；Opus 早期 429 与 `auth status` 假阴性原件在 `full-r3/opus/raw/`）

## v2.3.1 r4 发布基线与 r5 辅助补跑（2026-08-20 / 2026-08-21，2026-08-27 补登记）

- 本节补齐索引，不重写前一节 r3 的失败；以 `results-v2.3.1.md` 的最终复核为准。
- r4：111 条（61 SF + 50 SNF），Opus 5 与 DeepSeek V4 Pro 独立改写均 111/111，双向 judge 14/14 批完成。Opus：L1 0、SNF 0/50、SF 57/61。DeepSeek 撤出正式席位：最终复核 L1 1（B-74）、SNF 1/50、SF 风格失败 1（B-33）；原始判分与撤销/改判原因均留在结果页。
- r5：Grok 4.6 改写 111/111、硬判完整；Opus→Grok 仅 B-65–80 批完成（L1 0、SNF 0/6、SF 7/10），其余6批未完成，Grok→Opus未启动。不能视为完整第二模型基线。
- 当时通道：Cindy Host / Orca Worker，Opus `claude-opus-5[1m]`、DeepSeek `deepseek-v4-pro[1m]`、Grok `xai/grok-4.6`；Grok 未完成判分系通道异常，不补造结果。
- 发布决定：维护者 2026-08-21 接受 Opus 单席位；HUMAN direct 缺 docs/status 随版公开，`check_repo` 后续已改为 known-gap。
- 归档：`results-v2.3.1.md` §4–§11。
- 原始输出：`tasks/current/eval-runs/2026-08-20-v2.3.1-full-r4/`、`tasks/current/eval-runs/2026-08-21-v2.3.1-full-r5-grok/`（未入库）。

## 登记模板（新一轮实跑照抄填写）

```markdown
## vX.Y.Z <全量基线|targeted 回归>（YYYY-MM-DD）

- 评测集：`benchmark.md` @ vX.Y.Z（N 条：a SF + b SNF）；范围 = <全量|用例列表>
- 口径：<双模型交叉|targeted>；盲测 = 是（benchmark-blind.md 生成于 <日期/commit>）
- 被测模型：<CLI + 确切模型版本，如 dated model id>
- judge 模型：<CLI + 确切模型版本>
- CLI 版本：codex <ver> / claude <ver>
- 归档：`results-vX.Y.Z.md`
- 原始输出：`tasks/current/eval-runs/<目录>`（未入库；如对外公开争议判定，摘录脱敏片段进归档）
```


## v2.4.0 候选：Grok全量续跑（2026-08-27）

- 基线：`cff0300071da7949b2041448bc7ae6ebc5041033`；本地候选分支 `codex/v2.4.0`，未发布，版本元数据仍2.3.1。
- 评测集：120条（63 SF + 57 SNF），保留旧111条并新增2 SF + 7 SNF。任务内18条（12条定向复现 + 6条侧测）不加入公开分母。
- 冻结指纹：SKILL `452ffadbc5208f11cc6095fa3c07a951ac0de511d5e14dc81efe5c7841d05968`；blind `d91620417690e9d33d9722a341dc04aee2c6e403e6bcd9473dc1f8644d2dac19`；rewrite prompt `332f34f0d44ee50f803b187e672d71f863abf4ac4009c3e5728c7c0d3f38985b`。
- 续跑原因：full-r1双方均无有效全量答案；Claude额度限制，Grok通道故障。用户明确只重跑Grok、暂不调用Claude。原失败回执保留，不是追分重跑。
- 被测模型：Grok CLI 1.0.5（5115b46bc909），请求 `grok-4.6`，七批实际均 `grok-4.6-build`。7个新会话，每批只给冻结规则/references/匿名输入；`--deny '*'` 会话级拒绝所有工具，实际持久记录均零工具调用/结果，fingerprint核验通过。
- CLI环境限制：仍注入通用工作规则和技能目录摘要；七批额外上下文在归一化cwd后相同，无评分预期或他人答案。prompt文件与full-r1字节一致；CLI实际输入仅移除末尾一个换行，其余字符一致。不宣称完全空白环境。
- 完整性：7/7批，120/120条，无缺号/重号。会话ID、原始JSON哈希、结束状态及上下文核验见本地 `completion-verification.json` 和各批 `provenance.txt`。
- 硬指标：长文4条，硬下限失败0、目标下警告0；破折号密度报警0；protected粗核15条/38片段。Codex逐条归因为14条有效保留原文说明、1条SF-20允许的无源论断整条删除；脚本结果未改写。
- 辅助初审：Codex重点核查20条并复核机械报警，发现SF-39/B-76否定关系漂移、SF-07/B-104抽象关系丢失；SF-08/B-80完成态疑点待判。不是正式全量判分，不据此给出全量L1数量、SF通过率或SNF误杀率。
- judge：正式方向仍为Claude判Grok、Grok判Claude；本次Claude未调用，两个方向均未完成。机械检查不能抵消语义失败，当前不能作为达标第二席位。
- 归档：[results-v2.4.0.md](./results-v2.4.0.md)。原始输出：主工作区本地 `tasks/current/eval-runs/2026-08-27-v2.4.0-grok-resume-r2/`；首轮失败 `2026-08-27-v2.4.0-full-r1/` 保留。


## v2.4.0 候选：Claude改写与部分交叉判分续跑（2026-08-28）

- 规则、blind、预期及prompt：沿用上一节冻结版本，19项SHA256一致；原111条和新增9条均未改动。Grok的08-27有效120条输出直接复用，不重跑覆盖。
- Claude Code 2.1.247，`opus → claude-opus-5` / firstParty。7批120条改写及1批16条judge的持久会话答复均为Opus5；JSON另有少量Haiku辅助用量，单列于原始回执，不算第二答复席位。safe-mode、strict-mcp-config、tools空，实际零tool_use/tool_result。
- Grok CLI 1.0.5，`grok-4.6 → grok-4.6-build`。7批独立判Claude全部完成；会话级deny-all，结束状态、模型fingerprint、实际零工具记录及显式prompt一致性逐批核验。
- Claude改写：120/120；4条长文硬下限失败0、目标下警告0，破折号密度报警0。protected粗核2条/20片段：SF-59允许删除编造的30秒，SNF-37明确保留原文未回显；Codex复核不构成L1，原脚本结果保留。
- Grok判Claude：120/120，L1失败0；SF54/63、L2 51/60、L3 3/3；SNF误杀1/57（SNF-28）。新增9条：SF1/2（SF-62警告）、SNF0/7、L1=0。
- 旧111趋势：SF53/61、L2 50/58、L3 3/3、SNF1/50。相比v2.3.1有效r4的L2 54/58下降6.90个百分点；原判官DeepSeek与本次Grok、运行通道均不同，不作严格因果归因。旧警告3条保留、SF-53通过，新增旧题警告SF-18/24/28/52/61，详见结果页。
- Claude判Grok：仅B-17–32完成16/120；该局部L1=0、SF/L2 9/9、SNF0/7，不外推到未判104条。B-01–16与B-49–64返回会话额度限制，提示当地2026-08-28 06:00恢复；另外4批未启动。错误回执不是用例失败。
- 判分争议：SF-28预期把“首次导入最容易卡住”当成原文事实，与原文/保真合同有张力；本轮保留原始⚠️和冻结输入，未调分，留待主审。
- 分批策略：同一冻结轮可跨额度窗口完成。后续每阶段先运行最多2批Claude，验证保存；任一额度错误阻止新请求，已在途结果单独核验。只补未完成批次，最终双审留到judge完整后；不设未经授权的主审token/费用上限，未安排定时任务。
- 原始材料：主工作区 `tasks/current/eval-runs/2026-08-28-v2.4.0-claude-resume-r3/`，含 `judge-summary.json`、`claude-completion-verification.json`、逐批回执及 `claude-resume-checkpoint.json`。冻结模型原输出与judge输入均保留。
- 此阶段仍是未验收候选；当时Claude剩余6批判分与最终主审未补，第二正式席位未完成，不发布、不更新2.3.1版本元数据。[结果与限制](./results-v2.4.0.md)。


## v2.4.0 候选：剩余Claude判分完成（2026-08-28，r4）

- 用户再次确认额度恢复；按2批一阶段补6批104条，复用r3已完成16条，不重跑有效结果。Claude CLI 2.1.248，实际Opus5/firstParty不变；prompt文件逐字沿用，19项冻结文件不变。每批正文、输入、编号与零工具记录均核验。
- 双向判分完整性：Claude判Grok120/120，Grok判Claude120/120。两模型各120条原始改写不变。
- Grok原始判分：L1=0、SF53/63、L2 50/60、L3 3/3、SNF误杀0/57。新增9条SF2/2、SNF0/7；旧111条SF51/61、L2 48/58、SNF0/50。上一版Grok无完整基线，不计算同比。
- Codex复核：SF-39的“不是A”被改成“不只是A”，SF-07原有抽象关系整体丢失，纠正两处硬约束漏判。Grok复核L1=2、SF52/63、L2 49/60、L3 3/3、SNF0/57；旧111复核SF50/61、L2 47/58。原始judge不覆盖、不降门槛、不追分重跑。
- SF-08两模型均出现完成态表达，均维持原判并对称保留疑点；SF-28既有预期张力且相近输出获双向不同判分，不改原分。Claude全部指标沿用r3，无新增改写或调分。
- P-01定向与同源SF-62全量结果不一致：Claude全量仍有“判分仅闭环”残留。门槛1未过，门槛3不能仅凭定向小样认定满足；不扩写FAQ小样的证明范围。
- 完整对照证据已补齐，但Grok不是达标第二席位，候选未通过验收；既有保真要求未改，不能把失败直接归因新增规则。不发布、不更新元数据或安装软链。
- 原始回执、逐批验证、合并 `judge-summary.json` 与语义复核材料：主工作区 `tasks/current/eval-runs/2026-08-28-v2.4.0-claude-judge-resume-r4/`；最终双审记录另存本地过程材料。[完整结果](./results-v2.4.0.md)。

## v2.4.0 修复 r5：18条定向与修复双审（2026-08-28）

- 工作树：`shuorenhua-v2.4.0-remediation`；分支 `codex/v2.4.0-remediation`，基于 `cff0300071da7949b2041448bc7ae6ebc5041033`。规则快照 `f2e6303f2e48`，13项被测源码哈希保存于任务记录。
- 范围：新增9题（SF-62–63、SNF-51–57）+ SF-07、SF-39、SNF-28 + 6条任务内保护/泛化用例。18条全是已见回归，不是新盲测，不进120条公开分母。r1–r4失败与快照保留，题目、预期和门槛未改。
- 改写：两模型显式prompt相同168871字节；Claude Code 2.1.248 / `opus → claude-opus-5` / firstParty，session `1d65d2ea-56b0-486d-9048-c5211235c7ba`；Grok CLI 1.0.5 / `grok-4.6 → grok-4.6-build`，session `01a04807-de8a-7b90-8099-89db96b9937e`。
- 修复双审：同一修复差异与实际18条输出，prompt相同79124字节。Claude session `c72f7b1a-557f-4991-80ae-2c9af03ace1f`；Grok session `01a0480d-616e-7870-9584-ba4d7cdcf82d`。不是全量judge，不据此生成新全量分数。
- 4次调用均正常结束，实际模型、持久会话、显式输入与零工具通过核验。Grok fingerprint均为 `fp_08d0bc26c22b024e`。CLI附加上下文只记录指纹、未冻结；不声称完全一致的运行上下文或稳定性。
- Codex逐条复核与双审均未发现高置信硬失败；SF-62漏改本轮不再出现。Grok SF-07尾句省略仍保留歧义，不称18/18全风格通过。SF-39两侧12句/3段，字符留存98.8%/97.6%。
- 双审后仅同步评测指南和状态记录，13项被测source hashes仍匹配；42项单测、check_repo与diff检查通过。原线上仓库、旧候选与安装软链未动，元数据2.3.1。
- 维护者要求节省Claude额度：未启动新候选全量，无在途调用、无自动重试或自动续跑。当前修复可保留，但正式验收与发布尚未完成。原始产物见主工作区 `tasks/current/v2.4-remediation-20260828-r5/`。[结果与限制](./results-v2.4.0.md)。


## v2.4.0 范围收缩（2026-08-29 决定）

- 2026-08-27 至 08-29 的候选（`codex/v2.4.0`、`codex/v2.4.0-remediation`，最终候选 `29753b6ff697`）把 severity 第 6 项、FAQ 条件顺序、抽象主张保留、否定范围保护、issue-reply 删除例外、scope 拆句边界和全部示例重写打包在同一版里。r6 与 r8 两轮正式验收分别在 B65-80 首批和 B81-96 第六批确认 L1（SF-04 删限定词；SF-37 把条件式下一步换成新的前置要求、SF-16 把决定因素降为一般影响），随后 r9–r13 五轮只做规则修订与 harness 修复，没有任何一轮进入正式批次。
- 维护者 2026-08-29 决定收缩 v2.4 范围：只保留直接回应 #5 的 severity 第 6 项按词义放行，以及 FAQ 不得后移原有执行前条件和警告。抽象主张保留、否定范围保护、主动出击腔交付保留、scope 拆句边界，以及 `examples.md` / `positive-style.md` / `structures.md` / `operation-manual.md` 的示例重写全部移出本版，留给 v2.5 单独立项验收。
- 被移出的完整候选留存在本地任务材料 `tasks/current/v2.5-candidate-full-29753b6ff697.patch` 与 `tasks/current/v2.4-remediation-20260829-r13/snapshot/`，不在提交历史内。
- benchmark 不变：9 条新增（SF-62–63、SNF-51–57）全部落在收缩后的范围内，题目、预期、blind 顺序与 SHA256 `d91620417690e9d33d9722a341dc04aee2c6e403e6bcd9473dc1f8644d2dac19` 沿用首次改规则前的冻结版本，不重新生成。
- 旧候选 r6/r8 的实跑数据不迁移到本版：规则输入已变，不能复用作本版成绩，也不改写为通过。


## v2.4.0 收缩版：受影响面 34 条双席位改写（2026-08-29）

- 候选：分支 `codex/v2.4.0-minimal`，基线 `cff0300071da7949b2041448bc7ae6ebc5041033`，候选 ID `9f83b9c456a4`（13 项被测源码 SHA256 摘要前 12 位）。规则改动约 20 行，只有 severity 第 6 项按词义放行与 FAQ 条件顺序两条。
- 评测集：benchmark 120 条不变，blind SHA256 `d91620417690e9d33d9722a341dc04aee2c6e403e6bcd9473dc1f8644d2dac19` 沿用首次改规则前的冻结，未重新生成。
- **实跑范围是受影响面 34 条，不是全量 120 条。** 构成：本版新增 9 条（SF-62、SF-63、SNF-51–57）+ severity 收紧后误杀风险最高的 12 条 + FAQ 子场景既有题 4 条 + `闭环`/`收口` 波及的 SF 7 条 + 逐字与含义保护波及的数值题 2 条。分 3 批（M1 12 / M2 12 / M3 10），另有 M2 的一次复现观测 M2RUN2（12 条，prompt SHA256 与 M2 完全相同）。
- 被测模型：Claude Code 2.1.251，`opus → claude-opus-5` / firstParty；Grok CLI 1.0.5，`grok-4.6 → grok-4.6-build`，fingerprint `fp_08d0bc26c22b024e`。7 次调用全部有效、无重试，逐次校验实际模型、单轮、零工具、显式输入逐字一致、输出与持久会话一致。Grok 侧使用 `--tools ''` 加隔离 system prompt（此前 `--deny '*'` 不移除工具，导致 r9–r11 三轮输出与持久会话不一致而作废）。
- 判分方式：**逐条静态复核，不是模型交叉判分。** 依据是 r8 的先例——Grok judge 判 120 条给出 L1 = 0，静态复核抓出 SF-39 否定关系漂移与 SF-07 抽象关系丢失两个真 L1。复核记录见各批次目录的 `static-review.json` / `static-review-claude.json`。
- 硬指标：两席位 L1 硬约束失败 0；34 条全部解析，长文硬下限失败 0，protected spans 无漂移。Grok 侧 M2 的 7 条 protected 粗核报警逐条归因为「只写保留原文未重复正文」的假阳性，7 条均为 SNF 且 no-op 正确。
- 结果：SNF 误杀 Claude 0/23、Grok 1/23（SNF-28）；本版新增 7 条 SNF 两席位零误杀；SF 两席位各 10/11。三处失败点完全互补，无一条两个模型同时失败。
- 门槛：1 与 2 达成；4 已按模型分别记录；**门槛 3（新增或修订用例 targeted 双模型达标）待维护者判定**——Grok 通过，Claude 两次运行中一次通过、一次漏清 SF-62 的一处包装。
- 已知问题不在本版修复范围，继续记录：SF-07、SF-39、SF-16、SF-37 四条在 v2.3.1 已存在；SNF-28 的误杀在 r4 与 r8 亦有记录。
- 归档：[results-v2.4.0.md](./results-v2.4.0.md)。原始输出（未入库）：`tasks/current/v2.4.0-minimal-acceptance-20260829-{M1,M2,M3,M2RUN2}/`；冻结物与批次生成器在 `tasks/current/v2.4.0-minimal-freeze-20260829/`。


## v2.4.1：全量 120 条双席位交叉判分（2026-09-04）

- 候选：分支 `codex/v2.4.1`，基线 `d2d0ce27da295581c3cf87a30ab65deb7d0ddfb8`，候选 ID `61062b89c06a`（13 项被测源码 SHA256 摘要前 12 位）。改动只在 references 示例层（`examples.md` / `structures.md` / `scene-packs.md` / `positive-style.md`，+72 / −67 行），**规则正文一行未动**。
- 评测集：benchmark 120 条不变，blind SHA256 `d91620417690e9d33d9722a341dc04aee2c6e403e6bcd9473dc1f8644d2dac19` 沿用同一冻结版本，未重新生成。v2.4.0 的验收数据因候选 ID 变化按设计作废，不迁移。
- **实跑范围是全量 120 条，双席位，双向交叉判分。** 分 8 批 × 15 条（B01-15、B16-30、…、B106-120），批次标签用真实区间，`hard_metrics.batch_expected_ids()` 逐批做区间完整性校验。这轮同时充当 v2.2.1 起欠的全量基线与 v2.5.0 减法的「改造前」快照。
- 被测模型：Claude Code 2.1.259，`opus → claude-opus-5` / firstParty；Grok CLI 1.0.13，`grok-4.6 → grok-4.6-build`，fingerprint 全部 `fp_08d0bc26c22b024e`。改写与判分均为双席位：Claude 判 Grok、Grok 判 Claude。
- 调用：36 次（预算上限 40），有效 33 次。三次无效均与被测规则无关——子进程 provider 环境（已在生成器修复）、一次 judge 少输出一行（L0 归一化）、一次 Grok API 传输错误；后两类按 HARNESS 规矩新建 `-r2` 目录重跑，失败目录保留。逐次校验实际模型、单轮、零工具、显式输入逐字一致、输出与持久会话一致。
- **Grok 隔离修复首次实跑验证通过**：r13 的 `--tools ''` + `--system-prompt-override` 此前从未实跑验证过（见 HARNESS「已知坑」）。本轮 16 次 Grok 调用全部通过 provenance 校验、零工具事件，该坑可销账。
- 硬指标：**两席位 L1 硬约束失败均为 0/120**。8 批长文硬下限失败 0、目标下警告 0。protected spans 粗核仅 B61-75 批 Grok 席位报 6 条，逐条归因为「no-op 只写保留原文未复述正文」的 L0 形态假阳性。
- 结果：SNF 误杀 Claude 2/57 = 3.5%（B-48 SNF-23、B-74 SNF-27）、Grok 1/56 = 1.8%（B-110 SNF-28），均为不涉编造或受保护片段破坏的普通误杀。SF 风格通过 Claude 53/63、Grok 51/63，22 条 ⚠️ 全部是「清理不彻底 / 动作不完整」，零保真类失败。
- 四条锚点：B-76 / SF-39、B-86 / SF-16、B-89 / SF-37 两席位全部硬约束与风格双通过；B-104 / SF-07 两席位硬约束通过，Grok 风格列 ⚠️（未交改写稿）。
- 门槛：本版无新增或修订用例，发布门槛只判受影响面子集 36 条——门槛 1（子集内 L1 = 0）与门槛 2（子集内 SNF 误杀 < 10%，两席位均 0/7）均达成；门槛 3 不适用；门槛 4 按席位报告，Claude 席位 SF 通过率较 v2.3.1 r4 低 9.3 个百分点，解释见结果页 §4（用例集 111→120、判官更换、单席位→双席位三个变量同时变化，且回退全部落在 ⚠️ 而非 ❌）。
- HUMAN：不进 rewrite/judge，只跑脚本。10 篇 active，代表性门禁**通过**（direct 4 篇覆盖 `docs` / `public-writing` / `status`），此前的已知缺口已由 `1cb6238` 补齐。分布数字见结果页 §7。
- 归档：[results-v2.4.1.md](./results-v2.4.1.md)。原始输出（未入库）：`tasks/current/v2.4.1-acceptance-20260904-*/`；冻结物、批次生成器与 HUMAN 统计在 `tasks/current/v2.4.1-freeze-20260904/`。
