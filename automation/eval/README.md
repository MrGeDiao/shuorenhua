# 运行评测

v2.5 分开检查编辑结果与运行证据。质量判据只有一份：[criteria.md](../../evals/v2.5/criteria.md)。运行包清单见 [runtime-files.json](../../runtime-files.json)，主集的中性请求与原文见 [suite.json](../../evals/v2.5/suite.json)。判分模型不固定为某个品牌。

## 准备一次运行

先冻结候选文件、原文、请求、模型、批次、预算和判据。改写输入不带 SF/SNF 标签或预期。`candidate_files` 只负责快照和哈希，**不会自动把文件内容注入模型**；需要加载的规则须实际放进 `instructions`。

以下是一个单题计划，保存到 `tasks/current/eval-runs/plan.json`。此例只是简单提示试跑，不代表 full skill：

```json
{
  "phase": "rewrite",
  "protocol": "shuorenhua-rewrite-v1",
  "provider": "claude",
  "model": "claude-opus-5",
  "instructions": "清理套话，保留信息和作者语气。不补事实。",
  "candidate_files": ["evals/v2.5/simple-prompt.md"],
  "cases": [{"id":"trial-01","source":"本次完成了对配置的检查。","request":"去掉套话，只给改写稿。"}],
  "batch_size": 1,
  "max_calls": 1
}
```

从仓库根目录执行：

```bash
python3 automation/eval/runner.py prepare tasks/current/eval-runs/plan.json --repo . --out tasks/current/eval-runs/trial
python3 automation/eval/runner.py run tasks/current/eval-runs/trial
python3 automation/eval/runner.py report tasks/current/eval-runs/trial
```

`prepare` 只创建新目录和冻结文件；`run` 才调用已登录的订阅 CLI。当前适配 `claude` 与 `grok`，显式模型 ID 要由本机可用模型确认，示例不保证其他机器具有权限。计划每批至多 15 题，默认超时 1200 秒，调用总数不得超过 `max_calls`；可用 `--max-new-calls 1` 一次只推进一批。

`instructions`、原文和请求会发送给所选提供方。CLI 禁用工具，校验单次输入、完整输出和精确 session；Claude 核对主 assistant 模型及 firstParty 用量，辅助计费另列；Grok 核对实际模型、fingerprint 与 signals。未由持久会话证实的隐藏系统上下文或辅助模型用途不声称已冻结。

## 判分与恢复

判分计划使用 `phase: judge`、`protocol: shuorenhua-judge-v1`，增加 `outputs`（ID 到完整输出的映射）和 `rubric`（实际判据全文）；`candidate_files` 冻结判据。不要只填一个文件路径让模型猜内容。

改写和判分均只交逐题 JSON，见[改写协议](rewrite-prompt.md)和[判分协议](judge-prompt.md)。协议、身份、缺题或工具调用不合规会停止运行。普通 judge 遇保真/任务的 fail 或 review 会停止后续批次；预先设置 `diagnostic: true` 可跑完诊断对照，但报告会标记 `non_release`。

`resume RUN` 离线汇总，不发模型请求。`resume RUN --revalidate-failed` 用当前验证器重新检查已有失败证据，新增审计记录，不覆盖原始验证。失败时已有的证据哈希必须保持一致；旧失败若没有哈希基线，会明确披露无法证明从首次失败起冻结。补录现有 CLI 结果可使用：

```bash
python3 automation/eval/runner.py resume RUN --batch 1 --raw output.json --transcript transcript.jsonl --completion completion.json
```

Grok 另需 `--signals signals.json`。只有原始 CLI JSON、退出记录和对应持久会话齐全才可验证。`run RUN --retry-failed` 是显式新调用，会建新 attempt 并消耗原预算；不因得分低自动重跑。成功批次复用前也会重验哈希。

`complete` 是覆盖与身份状态，`content_status` 是本批内容状态，二者都不代替发布裁决。发布还需要正常文本误改率、正向编辑收益、模式/留出文本和完整要求；review 未裁决、候选改过或覆盖不足时不能声称通过。

## 验证顺序

1. 独立判据与参考裁决先冻结，校准可用判官，记录漏报、误报和不确定项。
2. 同一模型对照简单提示、旧规则与新规则，匿名比较偏好并复核语义。
3. 候选定稿后跑完整主集、编辑模式与未参与写规则的留出文本。新请求需双模型证据。
4. 保存原始输出、原判和另外的复核记录；失败有据可查，不能用后一次覆盖首轮。

默认在 `tasks/current/` 存本地运行，公开结果页只发布必要范围、数字、限制与可复核例子。HUMAN 历史语料的 residual 统计、单独授权的长文改写、主集 123 题各自记录，不混分母。

## 本地检查与历史工具

```bash
python3 -m unittest discover -s automation/eval -p 'test_*.py'
python3 -m unittest discover -s automation -p 'test_check_runtime.py'
python3 automation/check_repo.py
```

旧 [hard_metrics.py](hard_metrics.py) 保留用于历史 Markdown 运行、字数和 residual 统计，不能直接解析新版 JSON 或充当语义判官。历史词表来自冻结归档，仅用于维持旧统计口径，不参与新运行规则。

旧主集原文、编号与映射保留；`make_blind.py` 的生成物仍可用于查阅。旧条目中的风格预期和 [benchmark-tiers.md](../../evals/benchmark-tiers.md) 不再是 v2.5 的判分权威。历史结果不回填新版成绩。
