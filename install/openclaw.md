# OpenClaw 安装

手动升级时先用新的空目录收集运行文件，核对本地定制后再切换旧安装；仅覆盖入口会留下旧参考文件。下方复制命令面向首次安装或空目录。

本页对应 2.5.0 开发候选，尚未发布。远程安装入口仍提供已发布版本；测试候选时，请从本地候选源码目录复制文件。

## mini / lite / full 怎么选

- `mini`：把 `dist/shuorenhua-mini.md` 放进一次性 prompt 或 `SOUL.md` 的风格段；它没有 skill 元数据，不应冒充可自动发现的 skill。
- `lite`：只放 `SKILL.md`。适合 token 紧张或只做基础改写。
- `full`：放 `SKILL.md`、`references/editing-guide.md`、`references/examples.md` 三个文件。适合长期 workspace、对外文本、技术文档和需要查看编辑边界与改写对照的任务。

## 1. 把 skill 放进 workspace

```bash
mkdir -p workspace/skills/shuorenhua/references
cp SKILL.md workspace/skills/shuorenhua/
cp references/editing-guide.md references/examples.md workspace/skills/shuorenhua/references/
```

上面是 full 用法。token 紧张时只放 `SKILL.md` 也能完成基础改写；两份参考文件用于查看编辑边界与改写对照，按需读取。

## 2. 触发方式选一个

**方式 A：按需触发（默认）**

把文件放进 `workspace/skills/` 后，OpenClaw 会按 skill 的 `name` 和 `description` 判断何时启用。对话里说"用说人话规则改写"就能触发，不需要额外配置。

**方式 B：设为默认写作风格**

如果希望所有对外文本都自动套用，在 `workspace/SOUL.md` 中加：

```markdown
## 说人话
所有对外文本（消息、文档、摘要、公开写作）遵循 `skills/shuorenhua/SKILL.md` 的规则。
内部技术输出（代码、日志、配置）不受约束。
```

## 3. 同步到 VM

```bash
git add workspace/skills/shuorenhua
git commit -m "feat: add shuorenhua skill"
git push
```

VM 上 `git pull` 后即生效。如果 VM 配了自动拉取，push 之后直接就能用。

## 使用提示

如果你想先判断"哪里像 AI"，不要直接改稿：

```text
先不要改写，只按 annotation mode 标出下面这段文字里的问题：...
```

适合这几类场景：

- 你想先看这段话该不该改
- 你要做审稿或 review，不想直接替作者重写
- 你怀疑有无源引用、语域混搭或工程师腔，但还不想动正文

处理无源引用时，可以指定模式：

```text
用说人话规则改写这段文本，无源引用按 audit-only 处理。
```

默认保留无源论断及其归属，必要时在正文外提示缺来源。只有明确指定 `rewrite-safe` 或要求删除无源论断，才允许整条删除；`bounded` 只列删除建议，`in-place` 保留原句并提示。`audit-only` 标出来源缺口，其他内容照常编辑；`rewrite-with-placeholder` 按用户要求保留论证结构、标待补来源，不编出处。

## 编辑范围

默认做最小必要修改；中文公开长文约 1000 字以上默认保留句段结构。可以直接指定：

程序代码块（包括注释和文档字符串）默认逐字保留；只有用户明确点名修改注释或说明文字时才编辑相应部分，且不改程序行为。代码围栏里的普通文案仍可按用户要求编辑。

- `structural`：允许删、并、重排，仍须保留有效信息与作者意图。
- `bounded`：不直接删整句、不并句、不重排。纯空句可列“建议删除（待确认）”，正文暂时保留。
- `in-place`：不删句、不并句、不重排，只在句内替换或删修饰；要求保句数时也不拆句。

例如：“按 bounded 改，删除建议放在正文后。”这些范围不因编辑力度或来源处理方式而放宽。

## 手动检查

提交正文后，确认保留原文语言、事实、条件与作者立场。正常原文应完整返回，不只回复“保留原文”；只标问题时不应附替换全文。以下提示可用来检查是否加载，但不能代替效果评测。

```text
用说人话规则改写这段文本：值得注意的是，接口超时从 30 秒改为 60 秒。
```

可以去掉“值得注意的是”，但必须保留接口超时及 30 秒改为 60 秒的关系。
