# 维护工具

## 仓库检查

在仓库根目录运行 `python3 automation/check_repo.py`，检查用例与编号、盲测同步、相对链接、版本元数据、HUMAN 语料元数据，以及运行清单的文件与链接闭合。README badge 存在时校验其数字，不要求固定宣传文案。

旧词表的统计检查读取冻结历史副本并核验哈希，不约束新版运行规则。脚本检查仓库结构与元数据，不判定文章质量或来源真伪。

## 编辑评测

见 [eval/README.md](eval/README.md)。新版使用薄 runner 与逐题 JSON，保留输入、输出、失败与复核证据；历史 Markdown 指标脚本另留作复查。

## 社区反馈

把原文、用户要求、实际输出与来源说明保存在 `tasks/current/intake/`，按 [intake.md](intake.md) 整理。可使用 [提示模板](intake-prompt.md)，只处理本次提供的材料；不自动创建周期任务。

整理产物和过程笔记放在 gitignored 的 `tasks/`。先确认具体失败，再决定补回归或改编辑边界，不默认扩词表。

## Star 曲线

`gen_star_history.py` 读取本仓库公开 stargazer 时间戳生成 SVG；现有 GitHub workflow 将曲线更新到 `star-data` 分支。它与改写运行包和质量评测无关。手动运行方式：

```bash
python3 automation/gen_star_history.py /tmp/star-growth.svg
```

需要已登录的 gh CLI。新版本尚未发布时，不提前增加发版标记。
