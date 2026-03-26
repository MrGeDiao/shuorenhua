# 说人话 评测指令

## 评测前先统一理解

这份 skill 现在不是“12 条规则列表 + 评分表”那种扁平结构了。

更准确的评测顺序应该是：
1. 先用 `SKILL.md` 判断场景、Tier、档位和禁改边界
2. 再按需要补读 `references/` 里的词表、结构、边界案例和微操作手册
3. 最后对 benchmark 用例做改写或误杀判断

如果评测员一上来就把它当成固定词表替换器，结果会失真。

---

## 给 Codex 的提示词

把以下内容直接粘贴给 Codex 即可运行评测：

---

你是一个“去 AI 味”规则的评测员。

**规则文件位置：**
- 核心入口：`./SKILL.md`
- 中文禁用短语表：`./references/phrases-zh.md`
- 英文禁用短语表：`./references/phrases-en.md`
- 结构反模式：`./references/structures.md`
- 严重度分级：`./references/severity.md`
- 改写示例：`./references/examples.md`
- 微操作手册：`./references/operation-manual.md`
- 场景禁改表：`./references/scene-guardrails.md`
- 边界案例：`./references/boundary-cases.md`

**评测集位置：**
`./evals/benchmark.md`

**你的任务：**

1. 先读取 `SKILL.md`，理解它的主流程：场景判断、Tier 判断、改写档位、禁改边界、输出合同
2. 再按需读取 `references/` 下的文件，补齐短语、结构、边界和误杀防护
3. 然后读取 `./evals/benchmark.md`，对其中每一条测试用例执行评测

### 对 Should Fix（SF-01 到 SF-16）：
- 先判断这条用例的主场景（chat / status / docs / public-writing）
- 判断命中了哪些问题类型（例如：开场套话、总结式收尾、工程师腔、语域混搭、无源引用、二元对比骨架）
- 判断应该使用 `minimal / standard / aggressive` 哪个档位
- 按规则改写原文
- 输出改写后的文本
- 列出命中项（问题类型 + 命中的具体词/结构）
- 判断是否通过（✅ 通过 / ⚠️ 部分通过 / ❌ 未通过）
- 简短说明理由

### 对 Should NOT Fix（SNF-01 到 SNF-13）：
- 判断这条文本为什么不该改
- 如果保持原样或只做最小无害调整 → ✅ 通过
- 如果错误修改了术语、系统主语、技术报告、引用原文、边界案例中的合理表达 → ❌ 误杀
- 简短说明误杀点

### 最终汇总：
输出一个汇总表格：

```text
| 用例 | 类型 | 结果 | 备注 |
|------|------|------|------|
| SF-01 | Should Fix | ✅/⚠️/❌ | ... |
| ... | ... | ... | ... |
| SNF-01 | Should NOT Fix | ✅/❌ | ... |
| ... | ... | ... | ... |
```

并给出：
- SF 通过率：X/16
- SNF 误杀率：X/13
- 是否达到目标：SF > 90%，SNF 误杀率 < 10%

**注意：**
- 不要把所有改写都做成同一种腔调
- 不要为了“去 AI 味”而删掉关键事实
- 不要误伤系统主语、技术术语、学术被动、图算法字面动词、真人 debug 对话等已知边界

---

## 快速运行（一行命令）

```bash
codex --system-prompt "$(cat ./SKILL.md)" \
  "先读取 ./SKILL.md，再结合 ./references/ 下的相关文件，评测 ./evals/benchmark.md 中的所有用例。对 SF 用例先判断场景、Tier 和改写档位，再改写并判断是否通过；对 SNF 用例判断是否误杀。最后输出汇总表格、SF 通过率和 SNF 误杀率。"
```
