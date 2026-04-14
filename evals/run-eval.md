# 说人话 评测指令

## 通用评测提示词

把以下内容直接粘贴给任意支持长上下文的模型即可运行评测：

---

你是一个"去 AI 味"规则的评测员。

**规则文件位置：**
- 核心入口：`./SKILL.md`
- Positive Style Contract：`./references/positive-style.md`
- Protected Spans：`./references/protected-spans.md`
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

1. 先读取 `SKILL.md`，理解主流程：场景判断 → protected spans → Tier 判断 → 改写档位 → 保真回读 → 残留味回读 → 输出合同
2. 再按需读取 `references/` 下的文件，补齐短语、结构、边界和误杀防护
3. 然后读取 `./evals/benchmark.md`，对其中每一条测试用例执行评测

### 对 Should Fix（SF-01 到 SF-30）：
- 先判断主场景（chat / status / docs / public-writing）和问题类型
- 判断改写档位（minimal / standard / aggressive）
- 回读先做保真回读；只有第一遍已经保住事实、但仍有明显残留味时，才再做 `Residual Audit`
- 第二遍固定只查 5 件事：开场残留、总结残留、narrator 残留、空泛判断残留、句长过匀
- 按规则处理原文：默认输出改写后的文本；如果该样本按 `audit-only` 通过，允许只输出缺来源 / 缺归属的风险说明，不强行给整段重写
- 列出命中项（问题类型 + 命中的具体词/结构）
- 判断是否通过（✅ 通过 / ⚠️ 部分通过 / ❌ 未通过），简短说明理由
- 对无源引用类 SF 用例，额外按场景判定：`public-writing / chat` 默认以删掉无证据权威铺垫为 `✅`；`docs / status` 默认以明确标注缺来源且不伪装成已证实为 `✅`
- 对 `Residual Audit` 类 SF 用例，额外检查第二遍是否只做轻量修正；如果为了抛光而重写全文、补新事实，或把 `status / docs` 写得更口语，记 `❌`

### 对 Should NOT Fix（SNF-01 到 SNF-21）：
- 判断这条文本为什么不该改
- 如果保持原样或只做最小无害调整 → ✅ 通过
- 如果错误修改了术语、系统主语、技术报告、引用原文、边界案例中的合理表达 → ❌ 误杀，说明误杀点

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
- SF 通过率：X/30
- SNF 误杀率：X/21
- 是否达到目标：SF > 90%，SNF 误杀率 < 10%

**注意：**
- 不要误伤系统主语、技术术语、学术被动、真人 debug 对话等已知边界
- `code-context` 样本只处理注释 / docstring / commit message 中的文字，不改动代码本身

---

## Codex 快速运行

```bash
codex --system-prompt "$(cat ./SKILL.md)" \
  "先读取 ./SKILL.md，再结合 ./references/ 下的相关文件，评测 ./evals/benchmark.md 中的所有用例。对 SF 用例先判断场景、Tier 和改写档位，再按规则处理并判断是否通过；回读先做保真回读，只有第一遍已经保住事实、但仍有明显残留味时，才再做 Residual Audit。Residual Audit 只查开场残留、总结残留、narrator 残留、空泛判断残留、句长过匀，且只允许轻量修正。默认输出改写结果，但对按 audit-only 通过的无源引用样本，允许只输出缺来源或缺归属的风险说明，不强行整段重写。无源引用类 SF 需要按场景判定：public-writing/chat 默认删掉无证据权威铺垫算通过，docs/status 默认明确标注缺来源且不伪装成已证实算通过。对 SNF 用例判断是否误杀。注意 mixed 样本只处理真正有问题的正文，不要改用户指令、引用和被讨论词。code-context 样本只改注释/docstring/commit message，不动代码。最后输出汇总表格、SF 通过率和 SNF 误杀率。"
```

## Claude Code 快速运行

在项目目录下启动 Claude Code，对话里直接说：

```text
读取 ./SKILL.md 和 ./references/ 下的所有文件，然后评测 ./evals/benchmark.md 中的所有用例。对 SF 用例先判断场景、Tier 和改写档位，再按规则处理并判断是否通过；回读先做保真回读，只有第一遍已经保住事实、但仍有明显残留味时，才再做 Residual Audit。Residual Audit 只查开场残留、总结残留、narrator 残留、空泛判断残留、句长过匀，且只允许轻量修正。默认输出改写结果，但对按 audit-only 通过的无源引用样本，允许只输出缺来源或缺归属的风险说明，不强行整段重写。无源引用类 SF 按场景判定：public-writing/chat 默认删掉无证据权威铺垫算通过，docs/status 默认明确标注缺来源且不伪装成已证实算通过。对 SNF 用例判断是否误杀。注意 mixed 样本只处理真正有问题的正文，不要改用户指令、引用和被讨论词。code-context 样本只改注释/docstring/commit message，不动代码。最后输出汇总表格、SF 通过率和 SNF 误杀率。
```

## 通用 LLM / API

如果用的是 ChatGPT、Claude Web、或其他 API：

1. 把上面"通用评测提示词"部分（两条横线之间）作为 system prompt 或首条消息
2. 把 `SKILL.md`、`references/` 下的文件和 `evals/benchmark.md` 的内容一起贴给模型
3. token 不够时，优先保留 `SKILL.md` + `benchmark.md` + `severity.md` + `boundary-cases.md`

注意：token 窗口较短的模型可能无法一次跑完 51 条，可以分批（先跑 SF，再跑 SNF）。
