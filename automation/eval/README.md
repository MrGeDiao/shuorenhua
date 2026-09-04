# Benchmark Eval Harness — 运行说明

> v1.9.0 起使用的模型实跑入口；2026-07-11 起改盲测口径（见下节）。
> Prompt 本体见 `./rewrite-prompt.md` 和 `./judge-prompt.md`。
> 这份 README 只解决"具体怎么跑一次"。

## 盲测口径（2026-07-11 起）

旧口径的问题：被测模型直接读 `evals/benchmark.md`，每条用例的 `预期` / `理由` 就在原文旁边，编号前缀（SF / SNF）和标题也暴露该改还是不该改——测出来的是 instruction-following，不是规则在陌生文本上的泛化。

现口径：

- 被测模型只读 `evals/benchmark-blind.md`：匿名编号（B-xx）、顺序打乱、只含场景和原文。
- judge 用 `evals/benchmark-map.md` 把 B-xx 映射回 SF/SNF 编号，再按 `benchmark.md` 的预期判分。
- 两个盲测文件由 `python3 automation/eval/make_blind.py` 生成（固定种子，可复现）；`benchmark.md` 用例增删后必须重跑，手改生成文件无效。
- 隔离靠 prompt 路径纪律约束，不是硬隔离；如需硬隔离，可在干净目录只放 `SKILL.md`、`references/`、`benchmark-blind.md` 再跑（v2.2.0 起 hard_metrics 需要 `evals/benchmark-blind.md` 解析原文，硬隔离目录须包含它）。

## 文件约定

工具本体（committed）：

| 角色 | 路径 |
|------|------|
| 被测模型改写 prompt | `automation/eval/rewrite-prompt.md` |
| 交叉判分 prompt | `automation/eval/judge-prompt.md` |
| 盲测生成脚本 | `automation/eval/make_blind.py` |
| 硬判脚本 | `automation/eval/hard_metrics.py` |
| 盲测输入（生成物） | `evals/benchmark-blind.md` |
| 盲测映射表（生成物） | `evals/benchmark-map.md` |
| 运行说明 | `automation/eval/README.md`（本文件） |

运行实例（local-only，`tasks/` 在 `.gitignore` 内）：

| 角色 | 路径 |
|------|------|
| Codex 改写输出 | `tasks/current/eval-runs/<YYYY-MM-DD>-codex/rewrite-<batch>.md` |
| Claude 改写输出 | `tasks/current/eval-runs/<YYYY-MM-DD>-claude/rewrite-<batch>.md` |
| Claude 判 Codex | `tasks/current/eval-runs/<YYYY-MM-DD>-judge/claude-judge-codex-<batch>.md` |
| Codex 判 Claude | `tasks/current/eval-runs/<YYYY-MM-DD>-judge/codex-judge-claude-<batch>.md` |

第一次使用前先建目录：

```bash
mkdir -p tasks/current/eval-runs/2026-06-18-codex \
  tasks/current/eval-runs/2026-06-18-claude \
  tasks/current/eval-runs/2026-06-18-judge
```

## 批次划分

默认按 7 批跑（盲测编号连续切段，每批 SF/SNF 天然混排）：

| batch | 区间 |
|-------|------|
| `B01-16` | B-01 到 B-16 |
| `B17-32` | B-17 到 B-32 |
| `B33-48` | B-33 到 B-48 |
| `B49-64` | B-49 到 B-64 |
| `B65-80` | B-65 到 B-80 |
| `B81-96` | B-81 到 B-96 |
| `B97-120` | B-97 到 B-120 |

新增或补跑用例可以单独成批：targeted 补跑先查 `benchmark-map.md` 找到对应 B 编号，按 B 编号下发给被测模型（不要把 SF/SNF 编号透给被测模型），输出命名可用 `targeted-vX.Y.Z`。历史批次（v1.9.x 的 `SF01-14` 等命名）是盲测前的旧口径，归档不改。

如果模型或供应商的上下文 / 输出限制跑不下 7 批之一，可以继续细拆，例如把 `B01-16` 拆成 `B01-08` 和 `B09-16`。文件名保持区间可读即可，最终汇总时按原区间合并。

默认使用 Codex 与 Claude 做双向交叉判分：

- Codex 改写 → Claude 判
- Claude 改写 → Codex 判

若运行环境不满足身份核验或输入隔离要求，可以换成另一个可核验模型；须在 run manifest 记录原因、实际模型和固定交叉方向。不能用设计审查充当盲测，也不能把未完成 judge 的席位称为正式双模型验证。

## 硬判（v2.2.0 起）

改写输出落盘后、跑判分前，先对每个运行目录跑一遍硬判脚本，把 judge 不再自己数的判定项（字数留存率、破折号密度、protected spans 粗核）批量算出来：

```bash
python3 automation/eval/hard_metrics.py --run tasks/current/eval-runs/<YYYY-MM-DD>-final/
```

- 扫 `<run-dir>/` 下所有 `rewrite-*.md`（按 `codex/`、`claude/` 子目录区分模型），自动配对 `evals/benchmark-blind.md` 原文逐条计算；旧口径批次（v1.9.2 的 `rewrite-SF43-45-SNF34-35.md` 命名）自动配对 `evals/benchmark.md` 的 SF/SNF 用例。
- 输出 `<run-dir>/hard-metrics.md`（可读报告）和 `<run-dir>/hard-metrics.json`（机器可读），两者都是运行产物，不入 commit。
- 长文留存率只对 `public-writing / long / in-place` 用例判定（目标 ≥ 0.90、硬下限 0.85）；bounded 长文与 no-op（保留原文）不适用留存率判据。任一用例低于硬下限时脚本退出码为 1。
- no-op 校验：声明保留原文的用例会核对「判定链有力度=no-op 证据」或「正文≈原文」；两者都没有（假 no-op）标 `noop_unverified` 并按实际留存率判，不让一句「保留原文」吞掉长文硬失败。正文附原文的 no-op 按 100% 记（包装字如「处理结果：/保持原文：」不计入分子）。
- 退出码：0 = 全部批次解析完整且无硬下限失败；1 = 有硬下限失败；2 = 自身错误或报告不可信（路径缺失、零用例批次、缺输出、单条缺文件等）。
- 破折号密度对单段 ≥ 4 处 `——` 或输出首句仍以 `——` 起手报警（SF-43 信号）。
- protected spans 粗核逐字检查数字、版本号、路径、反引号片段等（中文紧贴如 `耗时20ms`、`版本v1.8.0` 也能命中），缺失只报警不判死，交给 judge 复核（bounded 删除清单内的无源论断按规则删掉不算漂移）。

单条对照（调 prompt 或 debug 时用）：

```bash
python3 automation/eval/hard_metrics.py --pair <原文文件> <改后文件>
python3 automation/eval/hard_metrics.py --stdin <原文文件> < 改后.txt
python3 automation/eval/hard_metrics.py --pair <原文> <改后> --report-json --scene "public-writing / long / in-place"
```

单条模式自动剥模型输出里的 `## B-xx` 标题和「处理结果：」前缀，只对正文判；`--scene` 带上 `long / in-place` 标签时才会输出留存率判据（没有场景标签时留存为 `null`，只算破折号与粗核）。

判分时把 `hard-metrics.md` 的对应数字提供给 judge（见 `judge-prompt.md`），judge 不再自己数长文留存。

### residual 统计（v2.3.0 起）

`hard_metrics.py` 还可以单独查看篇章级残留形状：

```bash
python3 automation/eval/hard_metrics.py --residual 稿件.md
python3 automation/eval/hard_metrics.py --residual 稿件.md --report-json
python3 automation/eval/hard_metrics.py --calibrate
python3 automation/eval/hard_metrics.py --calibrate --benchmark-only
python3 automation/eval/hard_metrics.py --human-stats evals/human-corpus.jsonl
```

- `--residual` 输出句长变异系数、段落形状、连词密度（每千字）、动词名词化命中、800 字窗口内借喻场数量，以及 `「」/『』` 括起的短语候选数。代码块、URL、frontmatter 等先用等长空格屏蔽，行号和字符偏移不漂。
- 段落形状（2026-09-04 加）报段数、每段平均汉字与句数、最长段汉字数，另单列列表行数。抓的是「少分段 / 段落过长」，方向与 `structures.md` 第 13、14 条的过度格式化相反；来源是 Anthropic 对新一代模型「sentences run longer and there are fewer paragraph breaks」的观察。**只报数，不设阈值**：中文段落长度的正常分布还没实测过，不照搬英文来源的判据。连续列表行之间没有空行，会并进同一段计数，所以列表行数要一起看——列表多的文本，段落数字会偏低偏长。
- `--calibrate` 在 `benchmark.md` 的 SF / SNF 与 HUMAN 对照组上实测分布，自动排除 B-xx 盲测副本；HUMAN manifest 缺失、不足 8 篇或来源不全时退出 2。采集期只想复看 benchmark，可显式加 `--benchmark-only`；这不是发布标定结果。
- `--human-stats` 严格校验 JSONL、逐篇许可/许可证据与归属元数据、固定 revision/UTC 时间、正文目录/SHA256、去重、隐私检查、AI 辅助状态及其依据、1,000 汉字、12 句、8–12 篇公开来源、至少 3 个作者组、历史/现代各至少 3 篇及翻译稿不超过三分之一，再按总体、场景和长度桶报告 HUMAN 分布，并单列时代、原始语言、direct/proxy 及缺失 direct 场景。`check_repo.py` 的发布代表性门禁只把 direct 计入 `docs / public-writing / status` 覆盖；proxy 仍可作 residual，但不能顶数。自动化能验证的是元数据合同，归属内容与授权证据真实性仍由维护者人工确认。HUMAN 不进 benchmark rewrite/judge；格式或授权元数据不完整退出 2。
- 五项目前都只报数、不判死、不影响退出码。v2.3.0 的 95 条标定给出一个明确负结论：连词密度不能设全局线——SNF 最高 81.08/千字，反而高于 SF 的 80.00；`docs` / `status` 里的连词常常承担真实条件和因果。规则侧因此只在 `public-writing` 叙事中按分布判断，见 `references/structures.md` 第 23 条。
- 合并版 v2.3.0 在 103 条（57 SF / 46 SNF）上的 `「」/『』` 候选计数同样给出负结论：两组中位数与 p90 都是 0，max 都是 3。SF-55 的 3 处是抽象概念上的自造高亮，SNF-44 的 3 处是小说人物对白；原始计数完全同值、结论相反，因此不照抄上游「一篇 3 处以上」，不设阈值。脚本只报候选数，引用、正式术语、对白和文学场景由人工复核。
- v2.3.1 增加 HUMAN manifest 与统计入口；在授权语料补齐、分布实际跑出之前，句长 CV 与分场景连词密度继续不设阈值。8–12 篇小样本也只用于观察假阳性，不宣称统计显著或泛化成人味检测器。

## 改写批

Codex 改写一批：

```bash
codex exec -C . -s read-only --ephemeral \
  -o tasks/current/eval-runs/<YYYY-MM-DD>-codex/rewrite-B01-16.md \
  '你正在执行说人话 benchmark 盲测改写实跑。

请完整读取 ./automation/eval/rewrite-prompt.md，按其中 text 代码块里的 prompt 行事。
只使用当前工作目录下的 ./SKILL.md、./references/ 和 ./evals/benchmark-blind.md；禁止读取 ./evals/ 下的其他文件，不要读取全局安装的 shuorenhua skill 副本。

本轮只处理 ./evals/benchmark-blind.md 中 B-01 到 B-16。
请直接输出最终结果，不要附加过程叙述。'
```

Claude 改写一批：

```bash
claude --print --model opus \
  --name shuorenhua-eval-rewrite-B01-16 \
  --disallowedTools Edit Write \
  > tasks/current/eval-runs/<YYYY-MM-DD>-claude/rewrite-B01-16.md <<'EOF'
你正在执行说人话 benchmark 盲测改写实跑。

请完整读取 ./automation/eval/rewrite-prompt.md，按其中 text 代码块里的 prompt 行事。
只使用当前工作目录下的 ./SKILL.md、./references/ 和 ./evals/benchmark-blind.md；禁止读取 ./evals/ 下的其他文件，不要读取全局安装的 shuorenhua skill 副本。

本轮只处理 ./evals/benchmark-blind.md 中 B-01 到 B-16。
请直接输出最终结果，不要附加过程叙述。
EOF
```

其余批次只替换区间和输出文件名。

## 判分批

Claude 判 Codex 改写：

```bash
claude --print --model opus \
  --name shuorenhua-eval-judge-codex-B01-16 \
  --disallowedTools Edit Write \
  > tasks/current/eval-runs/<YYYY-MM-DD>-judge/claude-judge-codex-B01-16.md <<'EOF'
你正在执行说人话 benchmark 交叉判分。

请完整读取 ./automation/eval/judge-prompt.md，按其中 text 代码块里的 prompt 行事。
只使用当前工作目录下的 ./evals/、./SKILL.md、./references/ 和被测输出文件，不要读取全局安装的 shuorenhua skill 副本。

盲测区间：B-01 到 B-16
被测输出：./tasks/current/eval-runs/<YYYY-MM-DD>-codex/rewrite-B01-16.md

请直接输出判分表和汇总，不要重写被测输出。
EOF
```

Codex 判 Claude 改写：

```bash
codex exec -C . -s read-only --ephemeral \
  -o tasks/current/eval-runs/<YYYY-MM-DD>-judge/codex-judge-claude-B01-16.md \
  '你正在执行说人话 benchmark 交叉判分。

请完整读取 ./automation/eval/judge-prompt.md，按其中 text 代码块里的 prompt 行事。
只使用当前工作目录下的 ./evals/、./SKILL.md、./references/ 和被测输出文件，不要读取全局安装的 shuorenhua skill 副本。

盲测区间：B-01 到 B-16
被测输出：./tasks/current/eval-runs/<YYYY-MM-DD>-claude/rewrite-B01-16.md

请直接输出判分表和汇总，不要重写被测输出。'
```

其余批次只替换区间、被测输出和输出文件名。

## 小样试跑

调 prompt 时先跑小样，不要直接上全量：

```bash
mkdir -p tasks/current/eval-runs/<YYYY-MM-DD>-smoke

codex exec -C . -s read-only --ephemeral \
  -o tasks/current/eval-runs/<YYYY-MM-DD>-smoke/rewrite-B01-08.md \
  '请完整读取 ./automation/eval/rewrite-prompt.md，按其中 text 代码块里的 prompt 行事。
只使用当前工作目录下的 ./SKILL.md、./references/ 和 ./evals/benchmark-blind.md；禁止读取 ./evals/ 下的其他文件，不要读取全局安装的 shuorenhua skill 副本。

本轮只处理 ./evals/benchmark-blind.md 中 B-01 到 B-08。
请直接输出最终结果，不要附加过程叙述。'

claude --print --model opus \
  --name shuorenhua-eval-smoke-judge \
  --disallowedTools Edit Write \
  > tasks/current/eval-runs/<YYYY-MM-DD>-smoke/judge-B01-08.md <<'EOF'
请完整读取 ./automation/eval/judge-prompt.md，按其中 text 代码块里的 prompt 行事。
只使用当前工作目录下的 ./evals/、./SKILL.md、./references/ 和被测输出文件，不要读取全局安装的 shuorenhua skill 副本。

盲测区间：B-01 到 B-08
被测输出：./tasks/current/eval-runs/<YYYY-MM-DD>-smoke/rewrite-B01-08.md

请直接输出判分表和汇总，不要重写被测输出。
EOF
```

小样只看格式是否可对照：

- 每条改写输出都有 `## <编号>`。
- 每条都有固定判定链。
- judge 只输出固定三列表格。
- 汇总里有 SF 通过、SNF 误杀、⚠️ / ❌ 清单。

如果格式不顺，最多改 prompt 后再跑一轮；第二轮仍不顺就停下，不要继续全量。
