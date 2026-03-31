# v1.5 Todo

- [x] 备份旧版 `SKILL.md` 和 `tasks/todo.md` 到 `/tmp/stop-slop-zh-backup`
- [x] 重写 `SKILL.md`，把主文档收敛为入口决策、流程、档位、Tier、输出合同和导航
- [x] 新增 `references/operation-manual.md`，把高频问题写成可执行的微操作协议
- [x] 新增 `references/scene-guardrails.md`，补齐 `chat / status / docs / public-writing` 的禁改项
- [x] 新增 `references/boundary-cases.md`，补边界样例用于静态回归
- [x] 校验主文档是否覆盖：场景判定、禁改项、档位默认映射、Tier、回读检查、输出合同
- [x] 校验引用文件是否覆盖：6 类动作、4 个核心场景、4+ 组边界案例

## Retrospective

- 这次仓库位于 `Downloads`，当前会话对子进程读取旧文件受 macOS 权限限制；为避免盲改，先做了 `/tmp` 备份，再重建 v1.5 文件。

## Review follow-up

- [x] 修正 `SKILL.md` 中 `Tier` 与 `minimal / standard / aggressive` 的语义冲突
- [x] 在 `SKILL.md` 补回单文件安装可执行的最小规则集
- [x] 补全 `SKILL.md` 对 `phrases / severity / structures` 的导航，避免默认流程丢规则

## Fix current review findings

- [x] 恢复 `SKILL.md` frontmatter 的中文触发描述，避免 skill 自动触发能力回退
- [x] 调整 `SKILL.md` 的单文件模式和默认流程表述，避免把 `references/` 说成纯增强层
- [x] 修正 `references/operation-manual.md` 中与词表冲突的替换词
- [x] 复核 diff，确认三个 review finding 都被覆盖

## Static benchmark review

- [x] 复读 `evals/benchmark.md`，按 SF / SNF 梳理当前规则需要覆盖的能力点
- [x] 对照 `SKILL.md` 和 `references/` 静态判断每条 benchmark 的覆盖状态与风险
- [x] 汇总静态通过率、残余风险和建议修补点

## v1.4.1 hardening and release

- [x] 补齐 5 个静态风险点：SF-08、SF-16、SNF-05、SNF-09、SNF-11
- [x] 复核规则间的一致性，避免新增误杀或自相矛盾
- [x] 更新 `CHANGELOG.md`，整理 v1.4.1 发布说明
- [x] 提交修复并推送 `main`
- [x] 创建并推送 `v1.4.1` tag

## v1.4.3 pattern-first intake hardening

- [x] 把“模式优先、词条兜底、变体归并”的原则写进主规则和参考文档
- [x] 补充“调试腔 / 暴力动作腔 / 主动出击腔 / 总结提示腔”的变体归并说明
- [x] 新增 benchmark，用例覆盖“现有模式变体不必逐词入库”和“真人语境不误杀”
- [x] 增加一份自动化 intake 方案文档，定义样本收集、归类、入库建议和人工确认流程
- [x] 运行相关检查并复核 diff

## v1.4.4 eval sync and automation prompt

- [x] 运行最新 `benchmark.md` 评测，并归档新结果
- [x] 同步 README / CHANGELOG / 结果文件的评测口径
- [x] 把 intake 方案落成可直接复用的 automation prompt 模板
- [x] 新增 `.gitignore` 忽略 `.DS_Store`
- [x] 复核 diff 和仓库状态

## v1.4.3 release

- [ ] 把 `Unreleased` 和 `v1.4.4` 口径收回到 `v1.4.3`
- [ ] 重命名评测结果文件并同步 README / CHANGELOG 引用
- [ ] 提交 release 对齐变更
- [ ] fast-forward `main` 到发布提交并推送
- [ ] 创建并推送 `v1.4.3` tag

## v1.5 plan

### Scope

- [x] 把 `v1.5` 范围收敛到 3 个主交付：评测矩阵升级、无源引用处理策略、标注模式
- [x] 明确本版不做的事：不继续大规模扩词表，不做平台绑定，不做自动改仓库的 automation，不把 intake automation 正式产品化
- [x] 写清每个主交付的落地文件和“完成即发布”的验收标准
- [x] 把 `intake pilot` 降级为发布前验证项，不阻塞 `v1.5` 主线交付

### Acceptance criteria

- [x] `Benchmark matrix` 完成标准：`evals/benchmark.md` 新增长文本、混合病灶、上下文依赖样本，并补充更明确的通过口径
- [x] `Unsourced citation policy` 完成标准：`SKILL.md` 和 `references/operation-manual.md` 对三种处理模式、场景默认策略和边界写法保持一致
- [x] `Annotation mode` 完成标准：`SKILL.md`、`references/examples.md` 和至少一个安装文档都能说明“只标问题”怎么用
- [x] `Release` 完成标准：评测结果、README、CHANGELOG 口径一致，且全量 diff 无明显范围漂移

### Execution order

- [x] Phase 1：补完 `unsourced citation` 的 benchmark 覆盖和结果口径，只动规则与评测，不碰安装文档
- [x] Phase 2：落 `annotation mode` 的输出合同、示例和最小安装说明，先只覆盖 Codex 入口
- [x] Phase 3：按新 benchmark 做静态复核并补 `annotation mode` 抽样验证，更新结果文件，确认 `SF-05` 一类样本按新口径记分
- [x] Phase 4：同步 README / CONTRIBUTING / CHANGELOG，收拢文档口径并做发布前 diff review

### File map

- [x] `Phase 1` 主要修改：`SKILL.md`、`references/operation-manual.md`、`references/scene-guardrails.md`、`evals/benchmark.md`、`evals/run-eval.md`
- [x] `Phase 2` 主要修改：`SKILL.md`、`references/examples.md`、`install/codex.md`
- [x] `Phase 3` 主要修改：`evals/results-v1.5.0.md`、`evals/run-eval.md`
- [x] `Phase 4` 主要修改：`README.md`、`CONTRIBUTING.md`、`CHANGELOG.md`

### Phase 1 detail

- [x] 给 `evals/benchmark.md` 增加英文无源引用样本，覆盖 `studies show / experts say`
- [x] 再补一条中文无源引用样本，覆盖 `数据显示 / 业内人士认为`
- [x] 明确 `SF-05`、新增样本和长文本样本的记分方式：什么情况下记 `✅`，什么情况下记 `⚠️`
- [x] 检查 `SKILL.md`、`operation-manual`、`scene-guardrails` 是否都把 `docs/status -> audit-only`、`chat/public-writing -> rewrite-safe` 写一致
- [x] 同步 `evals/run-eval.md` 的 case 数量、说明和 mixed 样本注意事项

### Phase 2 detail

- [x] 在 `SKILL.md` 加一个独立的 `annotation mode` 小节，不和默认改写合同混在一起
- [x] 约定最小输出格式：`问题族 / 触发点 / 建议动作 / 是否建议改写`
- [x] 在 `references/examples.md` 新增 3 组对照：同一文本分别展示 `annotation mode` 与默认改写结果
- [x] 在 `install/codex.md` 增加最小可复制示例，说明什么时候用 `annotation mode`
- [x] 回读 examples，确认标注模式不会把引用、术语、系统主语误当成问题

### Phase 3 detail

- [x] 按更新后的 benchmark 做静态复核，并补 `annotation mode` 抽样验证
- [x] 生成新的结果文件，优先命名为 `results-v1.5.0.md`
- [x] 在结果文件里单列 `无源引用` 相关样本，说明 `⚠️` 是“不能编事实”而不是规则漏判
- [x] 复核 benchmark 总数、SF 通过率、SNF 误杀率，确保 README 和结果文件不会再口径漂移

### Phase 4 detail

- [x] 更新 `README.md` 的“规模 / 评测 / 设计”段落，加入 `annotation mode` 和新的 benchmark 规模
- [x] 更新 `CONTRIBUTING.md`，补“什么时候该加 benchmark，什么时候只该补操作手册”
- [x] 更新 `CHANGELOG.md`，按 `Added / Changed / Tested` 记完整
- [x] 做一次全量 diff review，只看范围漂移、口径冲突、未同步计数
- [ ] 评估 `intake pilot` 是否作为 `v1.5.x` 跟进；不在这版 release 阻塞

### 1. Benchmark matrix hardening

- [x] 重构 `evals/benchmark.md`，把用例按 `chat / status / docs / public-writing` 和 `short / long / mixed` 两个维度整理
- [x] 新增长段落和混合病灶样本：同段多类问题叠加、局部 AI 腔、真人文本夹少量网络语或工程术语
- [x] 新增多轮对话或上下文依赖样本，验证规则不会只会做“单句题”
- [x] 给 benchmark 增加更明确的通过口径：哪些是必须改写，哪些允许只标注风险不重写

### 2. Unsourced citation policy

- [x] 在 `SKILL.md` 明确三种处理模式：`rewrite-safe`、`audit-only`、`rewrite-with-placeholder`
- [x] 在 `references/operation-manual.md` 补一节“无源引用怎么处理”，分别说明默认动作、保留条件和回读检查
- [x] 为 `研究表明 / 数据显示 / 业内人士认为 / studies show` 这类句型补充中英文 benchmark
- [x] 明确各场景默认策略：`docs` 和 `status` 更保守，`public-writing` 允许更直接删掉姿态层
- [x] 复核 `SF-05` 相关结果，确认以后不会把“不能编事实”误记成规则失败

### 3. Annotation mode

- [x] 在 `SKILL.md` 增加“标注模式”输出合同：只标问题，不直接改写
- [x] 约定标注模式最小输出字段：问题族、触发原因、建议动作、是否建议改写
- [x] 在 `references/examples.md` 补 3 组示例：同一段文本分别展示“标注模式”和“改写模式”
- [x] 更新安装文档，说明什么时候该用标注模式，什么时候直接改写
- [x] 用 benchmark 抽样验证标注模式不会把术语、引用和真人具体叙事误判成问题

### 4. Intake pilot

- [ ] 按现有 [tasks/automation-intake.md](/Users/zhangqi/Downloads/stop-slop-zh/tasks/automation-intake.md) 跑一轮手工 intake 试点，收集至少 10 条社区样本
- [ ] 用试点结果验证“已覆盖 / 变体归并 / 候选新模式”三档结论是否够用
- [ ] 如果试点里反复出现同一类样本，优先补 benchmark 或 `operation-manual`，不要直接堆词表
- [ ] 把试点结论整理成一份可复用模板，供后续 automation 或人工 intake 直接套用
- [ ] 如果主线交付已完成再做；若版本节奏吃紧，可顺延到 `v1.5.x`

### 5. Release

- [x] 重新跑评测并输出新结果文件，确保 README / CHANGELOG / results 口径一致
- [x] 更新 `README.md`，把 `v1.5` 的新增能力讲清楚：更强评测、无源引用策略、标注模式
- [x] 更新 `CONTRIBUTING.md`，补充“什么时候应该加 benchmark，什么时候只是变体归并”
- [x] 更新 `CHANGELOG.md`，整理 `v1.5` 发布说明
- [x] 复核全量 diff，确认主文档、参考文档、benchmark、结果文件之间没有口径漂移
- [x] 完成发布前检查：评测、diff review、最终文案核对
