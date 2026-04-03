# v1.6 Todo — 规则边界补强

> 目标：补齐 v1.5 在实际使用中暴露的 4 个规则盲区，不扩词表、不加新功能、不改架构。

## Scope

本版只做：
- 补代码上下文 benchmark
- Tier 2 长度归一化
- 混合场景 worked example
- 中英混排句指引

本版不做：
- 不扩词表
- 不加新输出模式
- 不做 automation / intake
- 不改 SKILL.md 主流程

## 迭代计划

### P0 — 补代码上下文 benchmark ✅

**为什么优先**：skill 的主要分发渠道是代码编辑器（Claude Code、Cursor、Codex），但 37 条 benchmark 全是纯散文，零条覆盖代码注释、docstring、commit message。这是最大的实际盲区。

**交付物**：
- [x] `evals/benchmark.md` 新增 3 条 SF（SF-22 docstring / SF-23 commit message / SF-24 英文代码注释）
- [x] `evals/benchmark.md` 新增 2 条 SNF（SNF-17 正常技术注释 / SNF-18 正常 commit message）
- [x] 覆盖矩阵补上 `code-context` 列
- [x] 同步 `evals/run-eval.md` 的 case 数量（SF 24 / SNF 18 / 总 42）
- [x] 评测标准补 `code-context` 样本额外要求

**验收标准**：新增样本能被现有规则正确处理（SF 改掉、SNF 放行），不需要改规则本身。如果发现现有规则覆盖不了，再回来补规则。

**涉及文件**：
- `evals/benchmark.md`
- `evals/run-eval.md`

---

### P1 — Tier 2 长度归一化 ✅

**为什么做**：Tier 3 有按文本长度归一化的密度阈值（短文本 3+、中等 5+、长文本按占比），但 Tier 2 的"同段 2+"是绝对数字。500 字段落出现 2 个"然而""此外"可能完全合理，30 字句子连用 2 个就很明显。不一致会导致长段落误杀。

**交付物**：
- [x] `references/severity.md` Tier 2 小节加长度参考：短段落（< 100 字/词）2+、长段落（≥ 100 字/词）3+
- [x] `references/severity.md` 决策流程图同步更新
- [x] `SKILL.md` Tier 2 描述同步更新
- [x] 确认 SNF-03 在新规则下仍然放行

**涉及文件**：
- `references/severity.md`
- `SKILL.md`

---

### P2 — 混合场景 worked example ✅

**为什么做**：`scene-guardrails.md` 的"混合场景处理"只有 3 行原则，没有具体案例。中文技术写作经常混场景（博客嵌复盘、status 引用公开说明），实操时不知道怎么判。

**交付物**：
- [x] `references/boundary-cases.md` 新增案例 9：技术博客嵌事故复盘
  - 完整展示：判主场景（public-writing）→ 识别次场景（docs 复盘）→ 主场景 standard 改写 + 次场景误杀防护保留
  - 含原文、场景判断过程、推荐改法、改写理由、不该改的点

**涉及文件**：
- `references/boundary-cases.md`

---

### P3 — 中英混排句指引 ✅

**为什么做**：中文技术写作大量出现句内英文（"这是一个 paradigm shift"），当前规则按语言分词表但没有混排指引。实操时不确定英文词该查 `phrases-en` 还是按中文句子语境判断。

**交付物**：
- [x] `references/severity.md` 误杀防护新增第 11 条：中英混排句中的英文词按实际语义判断，附正反两个例子
- [x] `SKILL.md` 单文件兜底规则同步加一行说明

**涉及文件**：
- `references/severity.md`
- `SKILL.md`

---

## Release checklist

- [x] 全部 P0-P3 完成后，跑一轮完整 benchmark 静态复核（5 条新用例均被现有规则覆盖）
- [x] 同步 README / CHANGELOG 的 benchmark 数量和版本号
- [x] 确认新增内容没有和现有规则冲突（code review MEDIUM 已修）
- [ ] 提交并打 tag
