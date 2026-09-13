#!/usr/bin/env python3
"""检查仓库结构、计数、链接、用例编号和元数据是否同步。"""

import html
import hashlib
import json
import re
import subprocess
import sys
import traceback
import types
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "tasks", "assets"}
SKIP_FILES = {"evals/run-manifest.md", "CHANGELOG.md"}

# 展示形式不属于数据契约：README 可以删 badge；存在时数字须来自语料。
BADGE_COUNTS = (
    (r"benchmark-(\d+)%20cases", "total"),
    (r'alt="Benchmark: (\d+) cases"', "total"),
    (r"scenario%20samples-(\d+)", "rs"),
    (r'alt="Scenario samples: (\d+)"', "rs"),
)

CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}

LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^)\s]+)")
HTML_LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)")
CASE_ID_RE = re.compile(r"\b(?:SF|SNF|RS)-\d+\b")
FUTURE_ID_RE = re.compile(r"新增从\s+((?:SF|SNF|RS)-\d+)\s+起")


def line_number(text, offset):
    return text.count("\n", 0, offset) + 1


def add_issue(issues, path, line, check_id, message):
    issues.append(f"{path}:{line} [{check_id}] {message}")


def read_text(relative, issues, check_id):
    try:
        return (ROOT / relative).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        add_issue(issues, relative, "-", check_id, f"无法读取：{exc}")
        return None


def check_blind_sync(issues):
    script = ROOT / "automation" / "eval" / "make_blind.py"
    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    if result.returncode:
        for message in output.splitlines() or [f"退出码 {result.returncode}"]:
            add_issue(issues, "automation/eval/make_blind.py", "-", "blind-sync", message)
    elif output:
        print(output)


def check_counts(issues):
    benchmark = read_text("evals/benchmark.md", issues, "counts")
    samples = read_text("evals/real-samples.md", issues, "counts")
    if benchmark is None or samples is None:
        return None, None, None, None, 0

    case_matches = list(re.finditer(r"^### ((SF|SNF)-\d+) \|", benchmark, re.MULTILINE))
    rs_matches = list(re.finditer(r"^#{2,4} (RS-\d+)\b", samples, re.MULTILINE))
    if not case_matches:
        add_issue(issues, "evals/benchmark.md", "-", "counts", "没有解析到 benchmark 用例标题")
    if not rs_matches:
        add_issue(issues, "evals/real-samples.md", "-", "counts", "没有解析到 RS 样本标题")
    for relative, matches in (("evals/benchmark.md", case_matches), ("evals/real-samples.md", rs_matches)):
        ids = [match.group(1) for match in matches]
        if len(ids) != len(set(ids)):
            add_issue(issues, relative, "-", "counts", "用例编号重复")

    sf = sum(match.group(2) == "SF" for match in case_matches)
    snf = len(case_matches) - sf
    expected = {"total": len(case_matches), "sf": sf, "snf": snf, "rs": len(rs_matches)}
    anchor_count = 0
    relative = "README.md"
    text = read_text(relative, issues, "counts") or ""
    for pattern, source in BADGE_COUNTS:
        matches = list(re.finditer(pattern, text))
        anchor_count += len(matches)
        for match in matches:
            actual = int(match.group(1))
            if actual != expected[source]:
                add_issue(
                    issues,
                    relative,
                    line_number(text, match.start()),
                    "counts",
                    f"计数应为 {expected[source]}，实际为 {actual}",
                )
    return case_matches, rs_matches, sf, snf, anchor_count


def markdown_files(issues):
    files = []
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT)
        relative_text = relative.as_posix()
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if relative_text in SKIP_FILES or (
            relative.parent.as_posix() == "evals" and relative.name.startswith("results-")
        ):
            continue
        try:
            files.append((relative_text, path.read_text(encoding="utf-8")))
        except (OSError, UnicodeError) as exc:
            add_issue(issues, relative_text, "-", "links", f"无法读取：{exc}")
    return files


def strip_inline_code(line):
    return re.sub(r"(`+)[^`]*?\1", "", line)


def local_target(target):
    target = html.unescape(target.strip())
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if target.startswith(("//", "#")) or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
        return None
    return unquote(target.split("#", 1)[0].split("?", 1)[0]) or None


def check_links(files, issues):
    checked = 0
    for relative, text in files:
        source = ROOT / relative
        in_fence = False
        for number, raw_line in enumerate(text.splitlines(), 1):
            if re.match(r"^\s*(```|~~~)", raw_line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            line = strip_inline_code(raw_line)
            targets = [match.group(1) for match in LINK_RE.finditer(line)]
            if relative == "README.md":
                targets += [match.group(1) for match in HTML_LINK_RE.finditer(line)]
            for target in targets:
                path_text = local_target(target)
                if path_text is None:
                    continue
                checked += 1
                destination = source.parent / path_text
                if not destination.exists():
                    add_issue(issues, relative, number, "links", f"相对链接目标不存在：{path_text}")
    return checked


def safe_relative_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return (not path.is_absolute() and ":" not in value
            and not any(part in ("", ".", "..") for part in value.split("/")))


def check_runtime_manifest(issues, root=None):
    """运行安装包由显式清单定义，不递归收集开发目录里的 SKILL。"""
    root = (root or ROOT).resolve()
    manifest = root / "runtime-files.json"
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        add_issue(issues, "runtime-files.json", "-", "runtime", f"无法读取运行清单：{exc}")
        return 0
    entries = payload.get("files") if isinstance(payload, dict) else None
    if not isinstance(entries, list) or not entries:
        add_issue(issues, "runtime-files.json", "-", "runtime", "files 必须是非空数组")
        return 0
    paths = {}
    for relative in entries:
        if not safe_relative_path(relative):
            add_issue(issues, "runtime-files.json", "-", "runtime", f"不安全的相对路径：{relative!r}")
            continue
        if relative in paths:
            add_issue(issues, "runtime-files.json", "-", "runtime", f"重复文件：{relative}")
            continue
        path = PurePosixPath(relative)
        if relative != "SKILL.md" and (path.parts[0] != "references" or path.name.lower() == "skill.md"):
            add_issue(issues, "runtime-files.json", "-", "runtime", f"运行包只允许根 SKILL.md 与 references 资料：{relative}")
        candidate = root / relative
        paths[relative] = candidate
        try:
            candidate.resolve().relative_to(root)
        except (ValueError, OSError, RuntimeError):
            add_issue(issues, relative, "-", "runtime", "运行文件通过符号链接越出仓库")
            continue
        if not candidate.is_file():
            add_issue(issues, relative, "-", "runtime", "清单文件不存在或不是普通文件")
        elif candidate.resolve() != candidate.absolute():
            add_issue(issues, relative, "-", "runtime", "运行文件及其父目录不能通过符号链接加载资料")
    if "SKILL.md" not in paths:
        add_issue(issues, "runtime-files.json", "-", "runtime", "清单必须包含根 SKILL.md 入口")
    references = root / "references"
    if references.is_symlink() or (references.exists() and not references.is_dir()):
        add_issue(issues, "references", "-", "runtime", "references 必须是仓库内的真实目录")
    if references.exists():
        for candidate in references.rglob("*"):
            relative = candidate.relative_to(root).as_posix()
            if candidate.is_symlink() and candidate.is_dir():
                add_issue(issues, relative, "-", "runtime", "references 不能通过目录符号链接隐式加载资料")
            elif candidate.is_file() or candidate.is_symlink():
                if relative not in paths:
                    add_issue(issues, relative, "-", "runtime", "references 文件未列入运行清单")
    for relative, candidate in paths.items():
        try:
            candidate.resolve().relative_to(root)
            if candidate.suffix.lower() != ".md" or not candidate.is_file():
                continue
        except (OSError, ValueError, RuntimeError):
            continue  # 上面的文件检查已报告路径失败。
        try:
            text = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            add_issue(issues, relative, "-", "runtime", f"运行文件无法读取：{exc}")
            continue
        in_fence = False
        for number, raw_line in enumerate(text.splitlines(), 1):
            if re.match(r"^\s*(```|~~~)", raw_line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            line = strip_inline_code(raw_line)
            targets = [match.group(1) for match in LINK_RE.finditer(line)]
            targets += [match.group(1) for match in HTML_LINK_RE.finditer(line)]
            targets += [match.group(1) for match in REFERENCE_LINK_RE.finditer(line)]
            for target in targets:
                local = local_target(target)
                if local is None:
                    continue
                destination = candidate.parent / local
                try:
                    packaged = destination.resolve().relative_to(root).as_posix()
                except (ValueError, OSError, RuntimeError):
                    packaged = None
                # 按实际目标核对，不能用 symlink 别名绕进开发目录。
                if packaged not in paths or not destination.is_file():
                    add_issue(issues, relative, number, "runtime", f"相对链接没有闭合到运行包：{target}")
    return len(paths)


def check_legacy_sources(issues):
    """历史基线只校验冻结字节，不约束新运行规则的文件结构。"""
    relative = "evals/legacy-v2.4.1/source-hashes.json"
    text = read_text(relative, issues, "legacy")
    if text is None:
        return
    try:
        hashes = json.loads(text)
    except ValueError as exc:
        add_issue(issues, relative, "-", "legacy", f"哈希清单无法解析：{exc}")
        return
    if not isinstance(hashes, dict) or not hashes:
        add_issue(issues, relative, "-", "legacy", "历史哈希清单必须是非空 object")
        return
    for source, expected in hashes.items():
        if not safe_relative_path(source) or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            add_issue(issues, relative, "-", "legacy", f"历史哈希条目无效：{source!r}")
            continue
        snapshot = ROOT / "evals/legacy-v2.4.1" / (source + ".txt")
        try:
            actual = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        except OSError as exc:
            add_issue(issues, relative, "-", "legacy", f"历史文件无法读取：{source}: {exc}")
            continue
        if actual != expected:
            add_issue(issues, relative, "-", "legacy", f"冻结历史字节已变化：{source}")


def check_case_ids(files, case_matches, rs_matches, issues):
    if case_matches is None or rs_matches is None:
        return
    valid = {match.group(1) for match in case_matches}
    valid.update(match.group(1) for match in rs_matches)
    for relative, text in files:
        # “新增从 RS-20 起”描述的是下一个可用编号，不是对现有用例的引用。
        future_spans = {match.span(1) for match in FUTURE_ID_RE.finditer(text)}
        for match in CASE_ID_RE.finditer(text):
            if match.span() in future_spans:
                continue
            if match.group(0) not in valid:
                add_issue(
                    issues,
                    relative,
                    line_number(text, match.start()),
                    "case-ids",
                    f"用例编号不存在：{match.group(0)}",
                )


def check_meta(issues):
    skill = read_text("SKILL.md", issues, "meta")
    if skill is not None:
        lines = skill.splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            add_issue(issues, "SKILL.md", 1, "meta", "frontmatter 不存在或未闭合")
        else:
            end = lines[1:].index("---") + 1
            metadata = {}
            for number, line in enumerate(lines[1:end], 2):
                match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
                if match:
                    metadata[match.group(1)] = (match.group(2).strip(), number)
            for key in ("name", "description"):
                value, number = metadata.get(key, ("", 1))
                if not value:
                    add_issue(issues, "SKILL.md", number, "meta", f"frontmatter 的 {key} 不能为空")

    payloads = {}
    for relative in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
        text = read_text(relative, issues, "meta")
        if text is None:
            continue
        try:
            payloads[relative] = json.loads(text)
        except json.JSONDecodeError as exc:
            add_issue(issues, relative, exc.lineno, "meta", f"JSON 无法解析：{exc.msg}")

    plugin = payloads.get(".claude-plugin/plugin.json")
    marketplace = payloads.get(".claude-plugin/marketplace.json")
    if ".claude-plugin/plugin.json" in payloads and not isinstance(plugin, dict):
        add_issue(issues, ".claude-plugin/plugin.json", 1, "meta", "顶层 JSON 必须是 object")
    if ".claude-plugin/marketplace.json" in payloads and not isinstance(marketplace, dict):
        add_issue(issues, ".claude-plugin/marketplace.json", 1, "meta", "顶层 JSON 必须是 object")
    if not isinstance(plugin, dict) or not isinstance(marketplace, dict):
        return
    plugin_name = plugin.get("name")
    plugin_version = plugin.get("version")
    if not isinstance(plugin_name, str) or not plugin_name:
        add_issue(issues, ".claude-plugin/plugin.json", 1, "meta", "name 必须是非空字符串")
        return
    metadata = marketplace.get("metadata")
    if not isinstance(metadata, dict):
        add_issue(issues, ".claude-plugin/marketplace.json", 1, "meta", "metadata 必须是 object")
        return
    marketplace_version = metadata.get("version")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        add_issue(issues, ".claude-plugin/marketplace.json", 1, "meta", "plugins 必须是数组")
        return
    matches = [entry for entry in entries if isinstance(entry, dict) and entry.get("name") == plugin_name]
    if len(matches) != 1:
        add_issue(
            issues,
            ".claude-plugin/marketplace.json",
            1,
            "meta",
            f"应有且只有一个 name={plugin_name!r} 的 plugin 条目，实际 {len(matches)} 个",
        )
        return
    entry_version = matches[0].get("version")
    if not isinstance(plugin_version, str) or not plugin_version:
        add_issue(issues, ".claude-plugin/plugin.json", 1, "meta", "version 必须是非空字符串")
    elif marketplace_version != plugin_version or entry_version != plugin_version:
        add_issue(
            issues,
            ".claude-plugin/marketplace.json",
            1,
            "meta",
            "版本不一致："
            f"plugin.json={plugin_version!r}, metadata={marketplace_version!r}, plugin entry={entry_version!r}",
        )


def normalized_corpus_body(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def human_benchmark_duplicates(records, cases, strip_blockquote):
    """返回 HUMAN 正文与 SF/SNF benchmark 正文的精确重复关系。"""
    benchmark = {}
    for cid, _, body in cases:
        if cid.startswith(("SF-", "SNF-")):
            benchmark.setdefault(normalized_corpus_body(strip_blockquote(body)), []).append(cid)
    return [
        (record, benchmark[normalized_corpus_body(record["text"])])
        for record in records
        if normalized_corpus_body(record["text"]) in benchmark
    ]


def check_human_corpus(issues):
    """校验 v2.3.1 必需的 HUMAN 语料、发布 cohort 与 benchmark 隔离。"""
    relative = "evals/human-corpus.jsonl"
    manifest = ROOT / relative
    if not manifest.exists():
        add_issue(issues, relative, "-", "human-corpus", "v2.3.1 发布要求 8–12 篇逐篇核验公开许可的 HUMAN 正文，manifest 缺失")
        return 0

    module = load_hard_metrics(issues)
    if module is None:
        return 0
    try:
        records = module.load_human_corpus(ROOT, manifest)
        active = module.validate_human_cohort(records)
    except module.HumanCorpusError as exc:
        add_issue(issues, relative, "-", "human-corpus", str(exc))
        return 0

    try:
        module.validate_human_representativeness(records)
    except module.HumanCorpusError as exc:
        add_issue(issues, relative, "-", "human-representativeness", str(exc))

    for target in ("evals/benchmark.md", "evals/benchmark-blind.md", "evals/benchmark-map.md"):
        text = read_text(target, issues, "human-corpus")
        if text is None:
            continue
        match = re.search(r"\bHUMAN-\d+\b", text)
        if match:
            add_issue(
                issues,
                target,
                line_number(text, match.start()),
                "human-corpus",
                "HUMAN 只作 residual 对照，不得进入 benchmark/blind/map",
            )

    try:
        cases = module.parse_cases(ROOT)
    except SystemExit:
        add_issue(issues, relative, "-", "human-corpus", "无法解析 benchmark 正文，不能验证 HUMAN 隔离")
        return 0
    for record, case_ids in human_benchmark_duplicates(active, cases, module.strip_blockquote):
        add_issue(
            issues,
            relative,
            record["manifest_line"],
            "human-corpus",
            f"{record['id']} 正文与 benchmark {', '.join(case_ids)} 完全重复；HUMAN 不得进入 rewrite/judge 分母",
        )
    return len(active)


# hard_metrics.py 的 residual 词表只服务历史统计，与冻结的旧规则对照。
# 新 skill 的运行结构和编辑质量不由这些历史词表约束。
def load_hard_metrics(issues):
    """直接编译源码取词表，不走 importlib 的字节码缓存。

    pyc 的失效判定依赖解释器版本与构建配置：timestamp-based 只看「秒级 mtime +
    文件大小」，同秒内的等长修改会被判成没变；hash-based 才看内容。本机 3.14 实测
    改内容即失效，但这是个防漂移的检查，不该把正确性押在 CI 那边的缓存策略上。
    """
    relative = "automation/eval/hard_metrics.py"
    path = ROOT / relative
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        add_issue(issues, relative, "-", "rule-tables", f"无法读取：{exc}")
        return None
    module = types.ModuleType("hard_metrics")
    module.__file__ = str(path)
    try:
        exec(compile(source, str(path), "exec"), module.__dict__)
    except Exception:  # noqa: BLE001 — 加载期任何异常都应报成检查失败
        # 只留最后几行：定位到出错的文件、行号和异常类型，不刷屏
        detail = " | ".join(traceback.format_exc().strip().splitlines()[-3:])
        add_issue(issues, relative, "-", "rule-tables", f"加载失败：{detail}")
        return None
    return module


def rule_section(text, number):
    return re.search(rf"^## {number}\. .*?(?=^## |\Z)", text, re.S | re.M)


def code_span_terms(line):
    terms = []
    for span in re.findall(r"`([^`]+)`", line):
        terms += [term.strip() for term in span.split("/") if term.strip()]
    return terms


def check_rule_tables(issues):
    module = load_hard_metrics(issues)
    relative = "evals/legacy-v2.4.1/references/structures.md.txt"
    text = read_text(relative, issues, "rule-tables")
    if module is None or text is None:
        return 0

    checked = 0

    # 第 25 条借喻场：正文「常见 N 套：A、B、……」与 METAPHOR_FIELDS 双向一致，
    # 且声明的数量词要和实际列出的套数对得上（加场时忘改数字也算漂移）。
    section = rule_section(text, 25)
    match = re.search(r"常见([一二三四五六七八九十]+)套：([^。]+)。", section.group()) if section else None
    if match is None:
        add_issue(issues, relative, "-", "rule-tables", "第 25 条找不到「常见 N 套：……」枚举，无法与 METAPHOR_FIELDS 对照")
    else:
        line = line_number(text, section.start() + match.start())
        doc_fields = [item.strip() for item in match.group(2).split("、") if item.strip()]
        code_fields = list(module.METAPHOR_FIELDS)
        if CN_NUM.get(match.group(1)) != len(doc_fields):
            add_issue(issues, relative, line, "rule-tables", f"第 25 条声称「{match.group(1)}套」，实际列了 {len(doc_fields)} 套")
        if set(doc_fields) != set(code_fields):
            add_issue(
                issues,
                relative,
                line,
                "rule-tables",
                f"第 25 条与 hard_metrics.METAPHOR_FIELDS 不一致："
                f"仅正文有 {sorted(set(doc_fields) - set(code_fields)) or '无'}，"
                f"仅脚本有 {sorted(set(code_fields) - set(doc_fields)) or '无'}",
            )
        checked += 1

    # 第 21 条名词化：正文列的空动词与 NOMINALIZATION_PATTERNS 的起手动词双向一致。
    # 范围只到起手动词，不含后面的动名词宾语（`优化 / 分析 / 梳理` 那批）：正文把宾语写在
    # 「检测」节且按举例列，脚本侧是穷举，两边口径本就不同，强行对账只会误报。
    section = rule_section(text, 21)
    match = re.search(r"\*\*模式\*\*：(.+)", section.group()) if section else None
    if match is None:
        add_issue(issues, relative, "-", "rule-tables", "第 21 条找不到「**模式**：」行，无法与 NOMINALIZATION_PATTERNS 对照")
    else:
        line = line_number(text, section.start() + match.start())
        doc_verbs = set(code_span_terms(match.group(1)))
        code_verbs = set()
        for pattern in module.NOMINALIZATION_PATTERNS:
            head = re.match(r"[一-鿿]+", pattern.pattern)
            if not head:
                continue
            verb = head.group()
            # `实现了?` / `完成了?对` 里的「了」是可选量词标记，不属于空动词本身
            if verb.endswith("了") and pattern.pattern[head.end() : head.end() + 1] == "?":
                verb = verb[:-1]
            code_verbs.add(verb)
        if doc_verbs != code_verbs:
            add_issue(
                issues,
                relative,
                line,
                "rule-tables",
                f"第 21 条与 hard_metrics.NOMINALIZATION_PATTERNS 的空动词不一致："
                f"仅正文有 {sorted(doc_verbs - code_verbs) or '无'}，"
                f"仅脚本有 {sorted(code_verbs - doc_verbs) or '无'}",
            )
        checked += 1

    # 第 23 条连词：正文是举例，只单向要求它列到的词脚本里都有。
    section = rule_section(text, 23)
    match = re.search(r"\*\*模式\*\*：(.+)", section.group()) if section else None
    if match is None:
        add_issue(issues, relative, "-", "rule-tables", "第 23 条找不到「**模式**：」行，无法与 CONJUNCTIONS_ZH 对照")
    else:
        missing = [term for term in code_span_terms(match.group(1)) if term not in module.CONJUNCTIONS_ZH]
        if missing:
            add_issue(
                issues,
                relative,
                line_number(text, section.start() + match.start()),
                "rule-tables",
                f"第 23 条正文列的连词不在 hard_metrics.CONJUNCTIONS_ZH 里：{missing}",
            )
        checked += 1

    return checked


def main():
    issues = []
    check_blind_sync(issues)
    case_matches, rs_matches, sf, snf, anchors = check_counts(issues)
    files = markdown_files(issues)
    links = check_links(files, issues)
    check_case_ids(files, case_matches, rs_matches, issues)
    check_meta(issues)
    runtime = check_runtime_manifest(issues)
    check_legacy_sources(issues)
    human = check_human_corpus(issues)
    tables = check_rule_tables(issues)

    if issues:
        print("\n".join(issues))
        print(f"check_repo: FAIL（{len(issues)} 个问题）")
        return 1
    total = sf + snf
    human_text = f" / HUMAN {human} 篇" if human else ""
    print(f"check_repo: OK（{total} 用例 / {len(rs_matches)} 样本{human_text} / {anchors} badge 计数 / {links} 链接 / {runtime} 运行文件 / {tables} 历史词表）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
