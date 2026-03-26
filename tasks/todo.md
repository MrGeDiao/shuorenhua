# v1.5 Todo (next milestone)

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
