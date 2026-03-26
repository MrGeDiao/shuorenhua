# Claude Code 安装

## 先说结论

Claude Code 这类环境里，最稳的做法不是指望“丢进去就自动识别”，而是：

1. 把 skill 文件放到约定目录
2. 在 `CLAUDE.md` 里明确写出触发条件和适用边界

这样比一句模糊的“遵循反模式规则”更可靠。

---

## 方式 1：项目级（推荐）

### 1. 复制 skill 文件

```bash
mkdir -p .claude/skills/shuorenhua
cp SKILL.md .claude/skills/shuorenhua/
cp -r references .claude/skills/shuorenhua/
```

### 2. 在 `CLAUDE.md` 里写清楚怎么触发

推荐写法：

```markdown
## 写作风格
当任务涉及“去 AI 味”“说人话”“自然一点”“别像模板”这类改写时，优先遵循 `.claude/skills/shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出默认不套这个 skill。
```

这样能解决两个问题：
- 让触发条件更明确
- 避免误伤技术内容

---

## 方式 2：全局

如果你希望多个项目共用：

```bash
mkdir -p ~/.claude/skills/shuorenhua
cp SKILL.md ~/.claude/skills/shuorenhua/
cp -r references ~/.claude/skills/shuorenhua/
```

但即便放到全局目录，也建议在项目的 `CLAUDE.md` 里补一条简短说明，不要完全依赖隐式发现。

---

## 这个 skill 在 Claude Code 里怎么理解更对

`SKILL.md` 不是词表大全，而是入口判断文件。它负责：
- 识别场景：`chat / status / docs / public-writing`
- 识别 Tier：`Tier 1 / Tier 2 / Tier 3`
- 判断改写档位：`minimal / standard / aggressive`

`references/` 才是补充层：
- 短语
- 结构
- 边界
- 微操作
- 禁改表

所以推荐用法是：
- 默认先让 Claude 参考 `SKILL.md`
- 碰到复杂重写、误杀边界或风格争议时，再补读 `references/`

---

## 使用示例

你可以直接说：

```text
用说人话规则改写这段文本。
```

也可以更具体：

```text
把这段 status 更新按说人话规则轻改，保留术语和系统主语，不要改成口语闲聊体。
```

后者通常更稳，因为它同时给了：
- 场景
- 改写强度
- 禁改边界

---

## 验证

测试一句典型 AI 腔：

```text
在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。
```

如果输出不再保留 `打造 / 赋能 / 不容忽视 / 关键议题` 这些套话，同时还保持原意，就说明接好了。
