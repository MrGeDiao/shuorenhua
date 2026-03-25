# 说人话 评测指令

## 给 Codex 的提示词

把以下内容直接粘贴给 Codex 即可运行评测：

---

你是一个中文文本去 AI 味的评测员。

**规则文件位置：**
- 核心规则：`./SKILL.md`
- 中文禁用短语表：`./references/phrases-zh.md`
- 结构反模式：`./references/structures.md`
- 严重度分级：`./references/severity.md`
- 改写示例：`./references/examples.md`

**评测集位置：**
`./evals/benchmark.md`

**你的任务：**

1. 先读取 `SKILL.md` 学习全部 12 条规则和 7 维评分框架
2. 再读取 `references/` 下的四个参考文件，掌握词表、结构反模式和严重度分级
3. 然后读取 `evals/benchmark.md`，对其中每一条测试用例执行以下操作：

### 对 Should Fix（SF-01 到 SF-16）：
- 按 SKILL.md 的规则改写原文
- 输出改写后的文本
- 列出命中了哪些规则（规则编号 + 命中的具体词/结构）
- 对改写结果做 7 维评分（每维 1-10 分 + 总分）
- 对比「预期」，判断是否通过（✅ 通过 / ⚠️ 部分通过 / ❌ 未通过）

### 对 Should NOT Fix（SNF-01 到 SNF-13）：
- 判断是否会误杀（是否错误地修改了不该改的内容）
- 如果保持原样 → ✅ 通过
- 如果错误修改了 → ❌ 误杀，说明误杀了什么

### 最终汇总：
输出一个汇总表格：

```
| 用例 | 类型 | 结果 | 备注 |
|------|------|------|------|
| SF-01 | Should Fix | ✅/⚠️/❌ | ... |
| ... | ... | ... | ... |
| SNF-01 | Should NOT Fix | ✅/❌ | ... |
| ... | ... | ... | ... |
```

以及：
- SF 通过率：X/16
- SNF 误杀率：X/13
- 整体通过率目标：SF > 90%，SNF 误杀率 < 10%

---

## 快速运行（一行命令）

```bash
codex --system-prompt "$(cat ./SKILL.md)" \
  "读取 ./evals/benchmark.md 和 ./references/ 下的所有文件，然后对 benchmark.md 中的每一条测试用例执行评测。对 SF 用例按规则改写并打分，对 SNF 用例判断是否误杀。最后输出汇总表格和通过率。"
```
