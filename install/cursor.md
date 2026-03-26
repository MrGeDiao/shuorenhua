# Cursor / Windsurf 安装

## 先说现实一点的结论

这类编辑器里的 rules / project instructions 能不能稳定触发，取决于具体版本和你项目里的其他规则。

所以不要把它理解成“复制进去就一定全自动生效”。更稳的做法是：
- 把 `SKILL.md` 放进项目规则目录
- 在项目说明里明确写出适用场景
- 把 `references/` 当按需补读资源，而不是默认全量灌入

---

## 方式 1：项目级 Rules

### Cursor

```bash
mkdir -p .cursor/rules
cp SKILL.md .cursor/rules/shuorenhua.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp SKILL.md .windsurf/rules/shuorenhua.md
```

如果你希望把参考文件也一起带上，再额外复制：

```bash
mkdir -p .cursor/rules/references
cp -r references/* .cursor/rules/references/
```

或 Windsurf 对应目录。

---

## 方式 2：全局 Rules / Instructions

如果你的编辑器支持全局 rules，也可以把 `SKILL.md` 放到全局配置里。

但建议只放 `SKILL.md`，不要一开始就把整个 `references/` 全塞进去。原因很简单：
- `SKILL.md` 已经能完成主判断
- `references/` 主要提升精度，不是每次都必须
- 全量塞入会抬高上下文成本，还可能和别的项目规则打架

---

## 推荐的项目说明写法

无论是 Cursor 还是 Windsurf，最好都在项目自己的说明文件里再补一句，明确它什么时候用。

例如：

```markdown
当任务涉及“去 AI 味”“说人话”“自然一点”“别像模板”这类改写时，优先参考 `shuorenhua` 规则。
对外文本优先按它处理；代码、日志、配置、命令输出默认不套这个规则。
```

这样比只放一个 rules 文件更稳。

---

## 这个 skill 的正确打开方式

不要把它当成单纯的“禁用词表”。

它现在的结构是：
- `SKILL.md`：入口判断
- `references/`：按需补细节

具体来说：
- 先判场景：`chat / status / docs / public-writing`
- 再判 Tier：`Tier 1 / Tier 2 / Tier 3`
- 再选强度：`minimal / standard / aggressive`

如果只是普通轻改，`SKILL.md` 往往就够。
如果是复杂文案、强 AI 腔、容易误杀的技术文本，再补读 `references/`。

---

## 验证

拿一句典型套话测试：

```text
用说人话规则改写：在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。
```

如果结果去掉了套话，但没把信息改空，说明规则基本接上了。
