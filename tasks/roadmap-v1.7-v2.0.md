# 版本迭代清单

> 更新时间：2026-04-13
> 当前版本：v1.7.0（已发布）

---

## 当前状态

v1.7.0 已经做了两件基础工作：

- **Positive Style Contract** — 定义"更像人"的正向目标，不只是删套话
- **Protected Spans** — 改写前先保护数字、日期、引用、命令、参数、报错等不能动的内容

还没做的：

- Residual Audit（二次审稿）
- Voice Calibration（声音拟合）
- Real Sample Eval Pack（真实样本评测）
- Scene Packs（子场景细分）
- Bad-case 公开收集机制

---

## v1.7.1 — 二次审稿

**目标**：解决"第一遍改完还是有轻微 AI 味"的问题。

**时间**：2026-04 第 3 周

**做什么**：

- [x] ~~Positive Style Contract~~ *(v1.7.0 已完成)*
- [x] ~~Protected Spans~~ *(v1.7.0 已完成)*
- [ ] 把回读拆成两步：保真回读 + 残留味回读
- [ ] 残留味回读只查 5 件事：开场残留、总结残留、narrator 残留、空泛判断残留、句长过匀
- [ ] 第二遍只做轻量修正，不重写全文
- [ ] `docs / status` 场景第二遍默认更保守
- [ ] 新增 3 条 benchmark：第二遍应该帮忙的场景
- [ ] 新增 2 条 benchmark：第二遍应该克制的场景
- [ ] 补 2 组 before/after 示例（一遍 vs 两遍的差异）

**改哪些文件**：

- `SKILL.md`
- `references/operation-manual.md`
- `references/examples.md`
- `evals/benchmark.md`
- `CHANGELOG.md`

**验收**：

- 对 AI 味重的文本，两遍结果比一遍更自然
- 对保守场景文本，不会因为第二遍而被过度口语化

---

## v1.7.2 — 真实样本评测

**目标**：评测不只看规则命中，还要看"改完能不能直接发"。

**时间**：2026-04 第 4 周

**做什么**：

- [ ] 创建 `evals/real-samples.md`
- [ ] 首批收集 8-12 条真实样本，覆盖：
  - README 简介
  - GitHub release note
  - X 短帖
  - Linux.do 长帖
  - issue 回复
  - commit message
  - docstring
  - 开发进度同步
- [ ] 每条样本记录：原文、场景、为什么像 AI、不该改坏什么、推荐改法
- [ ] 新增 3 个评分维度：`自然 / 保真 / 可直接发`，5 分制
- [ ] 从真实样本里挑 5 条以上可以放进 README 或 release note 的展示素材

**改哪些文件**：

- `evals/real-samples.md`（新建）
- `README.md`（如果有好的新示例）
- `CHANGELOG.md`

**验收**：

- 至少 5 条样本质量足够好，可以作为长期回归资产
- 能发现 synthetic benchmark 抓不到的问题

---

## v1.7.3 — 入口打通 + 文档对齐

**目标**：让外部用户更容易上手，建立反馈闭环。

**时间**：2026-05 第 1 周

**做什么**：

- [ ] 所有 install 文档统一 `lite` vs `full` 的说明
- [ ] 加一个"我应该用哪种模式"的选择矩阵
- [ ] 新增 `.github/ISSUE_TEMPLATE/bad-case.md`，字段：原文、场景、期望语气、哪里像 AI、哪里不能改
- [ ] 开一个 pinned issue：征集"改完还是有 AI 味"的案例
- [ ] 真实样本包从 8-12 条扩到 20+ 条
- [ ] 从用户反馈里拉 5+ 条真实 bad case（不只是自己写的）

**改哪些文件**：

- `install/*.md`
- `.github/ISSUE_TEMPLATE/bad-case.md`（新建）
- `evals/real-samples.md`
- `README.md`
- `CHANGELOG.md`

**验收**：

- 用户能看懂什么时候用 lite、什么时候用 full
- 外部贡献者有清晰的提交入口

---

## v1.8 — Voice Calibration + 子场景

**目标**：从"去 AI 味"进化到"更像你自己"。

**前置条件**：v1.7.x 稳定，Positive Style / Protected Spans / Residual Audit 都经过真实样本验证。

**时间**：2026-05 第 2-4 周

**做什么**：

### Voice Calibration Lite

- [ ] 新增 `references/voice-calibration.md`
- [ ] 用户提供 2-3 段自己的文字样本后，提取风格信号：
  - 句长波动
  - 口语度
  - 标点习惯
  - 连接方式
  - 主语偏好
  - 语气强弱
- [ ] 只拟合风格信号，不复制用户原文
- [ ] 明确禁止：模仿名人、品牌、公众人物
- [ ] 补 before/after 示例（有样本 vs 无样本的差异）
- [ ] 补 benchmark：更像用户但不抄袭

### Scene Packs

- [ ] 把 `public-writing` 拆成子场景，先做最常用的 4 个：
  - `README`
  - `release-note`
  - `forum-post`
  - `issue-reply`
- [ ] 每个子场景有独立的改写约束和示例
- [ ] 新增 `references/scene-packs.md` 或扩展 `scene-guardrails.md`

### 结构化输出（可选）

- [ ] 评估是否值得给 agent 做一个结构化输出 schema
- [ ] 如果做，保持 opt-in，不影响默认的一次性改写

**验收**：

- 提供 voice 样本后，结果比不提供时更接近用户风格
- 子场景的改写比大场景更贴合实际用途
- 没有引入幻觉或事实漂移

---

## v2.0 — 从仓库到产品

**目标**：让 `说人话` 从一个 skill 仓库变成一个有辨识度的中文开发者工具项目。

**时间**：2026-06

**做什么**：

- [ ] 更完整的示例页（按场景分类的改写前后对照）
- [ ] 面向更多平台的安装文档（Copilot、Windsurf、其他 agent）
- [ ] bad-case 征集机制常态化（定期整理、发 release 回应）
- [ ] 提交到 2-4 个 skill / agent 目录
- [ ] 建立固定的发布节奏（每 2-3 周一个小版本）
- [ ] 英文 README 或英文简介，方便国际开发者理解

**验收**：

- 项目被至少 2 个外部目录收录
- 有稳定的外部 bad case 提交
- 发布节奏至少持续 3 个版本

---

## 一条线看完

| 版本 | 核心词 | 状态 |
|------|--------|------|
| v1.7.0 | Positive Style + Protected Spans | 已发布 |
| v1.7.1 | 二次审稿 | 待开发 |
| v1.7.2 | 真实样本评测 | 待开发 |
| v1.7.3 | 入口打通 + bad-case 收集 | 待开发 |
| v1.8 | Voice Calibration + 子场景 | 待规划 |
| v2.0 | 产品化 + 分发 | 待规划 |

### 一句话路线

- **现在**："能去掉很多 AI 套话，但还不够像具体的人在说话。"
- **v1.7 完成后**："在不丢事实的前提下，不只删 AI 味，还开始贴近真人表达。"
- **v1.8 完成后**："可以拟合用户自己的 voice，不同场景有不同的改法。"
- **v2.0**："中文优先的自然表达 rewrite protocol，不只是一个有趣的 skill 仓库。"
