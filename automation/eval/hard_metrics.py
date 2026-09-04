#!/usr/bin/env python3
"""eval harness 零依赖硬判与 residual 统计。

v2.2.0：字数留存率 / 破折号密度 / protected spans 粗核（规格见旧 roadmap §6）。
v2.3.0：新增句长 CV / 连词密度 / 名词化 / 借喻场统计与 benchmark 标定模式。
v2.3.0 合并批次：residual 层新增「」/『』高亮短语候选计数，继续只报数不判死。
v2.3.1：增加 HUMAN 长文 manifest 校验与分布输出；只做 residual 对照，不进判分。
合并版 v2.3.0 标定实测（SF 57 / SNF 46）：候选数两组中位数与 p90 均为 0、
max 均为 3；SF-55 是自造高亮，SNF-44 是人物对白，原始计数不可分，
因此不设阈值、不影响退出码。
定位：把 judge 模型能被脚本替掉的判定项拿出来硬判——降成本、提稳定性。
判死 vs 报警：字数留存率与破折号密度按 run-eval.md 既有口径直接判过/不过；
protected spans 粗核只报警不判死，缺失留给 judge 复核（粗核是正则匹配，
不判定语义改写是否保真）。

用法（仓库根目录）：
    python3 automation/eval/hard_metrics.py --run tasks/current/eval-runs/<日期>-<版本>/
        # 扫批次目录：自动配对原文本（evals/benchmark-blind.md）与各模型输出，
        # 逐条计算，输出 <目录>/hard-metrics.md 报告和 <目录>/hard-metrics.json
    python3 automation/eval/hard_metrics.py --pair <原文本文件> <改后文本文件>
        # 单条对照：输出可读结果
    python3 automation/eval/hard_metrics.py --stdin <原文本文件>
        # 原文本从文件读，改后文本从 stdin 读；输出可读结果
    python3 automation/eval/hard_metrics.py --pair A.md B.md --report-json
        # 输出单行 JSON，供 automation/eval/README.md 的管道用法拼接 judge 输入
    python3 automation/eval/hard_metrics.py --human-stats evals/human-corpus.jsonl
        # 严格校验 HUMAN manifest 与正文，并输出不含正文的 residual 分布
    python3 automation/eval/hard_metrics.py --calibrate
        # 标定 benchmark SF/SNF + 8–12 篇 HUMAN 对照；缺 manifest 或 cohort 不全退出 2
    python3 automation/eval/hard_metrics.py --calibrate --benchmark-only
        # 采集期显式跳过 HUMAN，只看 benchmark 诊断分布；不算发布标定

退出码：--run 模式任一长文用例留存率低于硬下限 0.85 时退出码为 1；
批次不完整（零用例批次 / 缺输出）时退出码为 2（报告不可信）；
缺文件、格式异常等自身错误退出码为 2；其余为 0。
"""

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# 长文用例判据口径来自 evals/run-eval.md「Long-form / in-place」：
# 字数留存率目标 >= 0.90，硬下限 0.85
RETENTION_TARGET = 0.90
RETENTION_FLOOR = 0.85

# 场景标签里标了 long 的用例按长文判据处理；这个信号同时写死在
# benchmark-blind.md 的标题行里，不依赖 benchmark.md 的预期字段
LONG_TAG = re.compile(r"\blong\b")


def batch_expected_ids(batch):
    """从批次名解析期望覆盖的用例编号集。

    支持 `B01-16`（盲测区间）与旧口径 `SF43-45-SNF34-35`（v1.9.2 回放，
    多个前缀+区间段）。非区间命名（如 targeted-*）返回 None。
    """
    segments = re.split(r"-", batch)
    groups = []  # [(prefix, lo, hi)]
    i = 0
    while i < len(segments):
        seg = segments[i]
        m = re.fullmatch(r"([A-Za-z]*)(\d+)", seg)
        if not m:
            return None
        prefix = m.group(1).upper()
        num = int(m.group(2))
        if i + 1 < len(segments) and re.fullmatch(r"\d+", segments[i + 1]):
            lo, hi = num, int(segments[i + 1])
            if lo > hi:
                return None
            groups.append((prefix, lo, hi))
            i += 2
        else:
            groups.append((prefix, num, num))
            i += 1
    if not groups:
        return None
    ids = set()
    for prefix, lo, hi in groups:
        if prefix in ("", "B"):
            ids.update(f"B-{n:02d}" for n in range(lo, hi + 1))
        else:
            ids.update(f"{prefix}-{n}" for n in range(lo, hi + 1))
    return ids

# 保护片段粗核：数字（含单位）、版本号、路径、反引号片段、带小数的百分比、
# 中英文时间表达、英文缩略词。只做逐字存在检查，不做语义判定。
TOKEN_PATTERNS = [
    (r"`[^`\n]+`", "反引号片段"),
    # 中文紧贴场景（「耗时20ms」「共20人」）没有 \b 边界：数字侧用 ASCII 负向断言，
    # 中文（CJK）不算 word char，汉字贴数字也能命中；单位表把 CJK 单位也列进来。
    (r"(?<![0-9A-Za-z_])\d+(?:\.\d+)?\s*(?:ms|s|h|天|小时|分钟|秒|%|MB|GB|KB|倍|次|人|台|个|条|篇|年|月|日|版本|万|k)(?![0-9A-Za-z_])", "数字+单位"),
    (r"(?<![0-9A-Za-z_])\d+(?:\.\d+)?(?![0-9A-Za-z_])", "数字"),
    # 版本号：中文紧贴（「版本v1.8.0」）用负向字符断言替代 \b
    (r"(?<![0-9A-Za-z])v?\d+\.\d+\.\d+(?:[-+][\w.]+)?(?![0-9A-Za-z])", "版本号"),
    (r"(?:^|[\s(/])(?:[\w-]+/){1,}[\w./-]+", "路径"),
    (r"\b[A-Za-z_][A-Za-z0-9_]*[a-z][A-Za-z0-9_]*(?:[A-Z][a-z0-9]*){2,}\b", "英文标识符"),
    (r"\b(?:[a-z]+_){1,}[a-z][a-z0-9_]*\b", "英文标识符"),
    (r"\b(?:p95|p99|max_connections|handleBurst|Request|iOS|API|URL|DB|HTTP|CLI|Redis|Dijkstra|GitHub|Linux)\b", "英文缩略词/术语"),
    (r"\d{4}[-年]\d{1,2}(?:[-月]\d{1,2}日?)?", "日期"),
]

def parse_cases(root):
    """从 benchmark 语料解析用例：(编号, 场景, 原文)。

    盲测标题 `### B-xx | 场景` 从 evals/benchmark-blind.md 读；
    旧口径 `### SF-xx | 场景 | 描述` / `### SNF-xx | ...`（v1.9.2 回放）
    从 evals/benchmark.md 读。两个语料都解析并合并，编号体系互不冲突。
    """
    cases = []

    def parse_file(path, head):
        text = path.read_text(encoding="utf-8")
        current = None
        for line in text.splitlines():
            m = head.match(line)
            if m:
                current = {"id": m.group(1), "scene": m.group(2).strip(), "quote": []}
                cases.append(current)
                continue
            if current is not None and (line.startswith(">") or not line.strip()):
                current["quote"].append(line)

    blind = root / "evals" / "benchmark-blind.md"
    if blind.exists():
        parse_file(blind, re.compile(r"^### (B-\d+) \| (.+)$"))
    bench = root / "evals" / "benchmark.md"
    if bench.exists():
        parse_file(bench, re.compile(r"^### (SF-\d+|SNF-\d+) \| ([^|]+)"))
    if not cases:
        print("hard_metrics: evals/benchmark-blind.md 与 evals/benchmark.md 都没有可解析用例", file=sys.stderr)
        sys.exit(2)
    out = []
    for c in cases:
        quote = "\n".join(c["quote"]).strip("\n")
        if not quote:
            print(f"hard_metrics: {c['id']} 在 benchmark-blind.md 中没有解析到引用块", file=sys.stderr)
            sys.exit(2)
        out.append((c["id"], c["scene"], quote))
    return out


def extract_blocks(text):
    """从模型输出里切出每条用例的 处理结果 正文。

    返回 {盲测编号: 正文}。B-xx 标题后的「处理结果：」以下到下一个
    B-xx 标题之间的内容都算正文；处理结果内的 Markdown 标题是被测
    文本的一部分，必须保留。
    """
    lines = text.splitlines()
    blocks = {}
    pending_id = None
    in_result = False
    buf = []
    for line in lines:
        # 模型可能给整篇输出加 blockquote 前缀（`> ## B-01`），识别标题时先剥
        line_stripped = line[2:] if line.startswith("> ") else line
        # 兼容两代标题：盲测 B-xx 与旧口径 SF-xx / SNF-xx（v1.9.2 回放）
        m = re.match(r"^## (B-\d+|SF-\d+|SNF-\d+)$", line_stripped)
        if m:
            if pending_id is not None and buf:
                blocks.setdefault(pending_id, []).extend(buf)
            pending_id = m.group(1)
            in_result = False
            buf = []
            continue
        if pending_id is None:
            continue
        # 处理结果 行也可能带 blockquote 前缀（`> 处理结果：`），剥前缀后再识别
        if re.match(r"^处理结果(?:（[^）]*）)?[:：]", line_stripped):
            in_result = True
            rest = line_stripped.split("：", 1)[1] if "：" in line_stripped else (
                line_stripped.split(":", 1)[1] if ":" in line_stripped else ""
            )
            if rest.strip():
                buf.append(rest)
            continue
        if in_result and re.match(r"^判定链[:：]", line):
            continue
        if in_result:
            buf.append(line)
    if pending_id is not None and buf:
        blocks.setdefault(pending_id, []).extend(buf)
    return {k: "\n".join(v) for k, v in blocks.items()}


def strip_output_notes(text):
    """剥掉模型输出末尾的括号说明段（claude 在正文后附的 `（in-place：…）` 等）。

    特征：独立段落、整段以 `（` 开头 `）` 结尾、不是 `（待确认）` 删除清单。
    人工 wc -m 记录不算这些说明（对照 long-form-retention.txt：claude B-19 320、
    B-44 254 都是剥掉说明段后的正文长度）。
    """
    paras = text.split("\n\n")
    out = []
    for para in paras:
        s = para.strip()
        if s.startswith("（") and s.endswith("）") and not s.startswith("（待确认"):
            continue
        out.append(para)
    return "\n\n".join(out)


def count_chars(text, strip_markdown_prefix=False):
    """长文留存率口径：与既有人工 wc -m 一致，统计所有字符含空白。

    benchmark-blind.md 的原文是 blockquote（每行带 `> ` 前缀）；人工 wc -m
    记录的是去掉前缀后的正文（对照 long-form-retention.txt：B-02 231、B-19
    339、B-44 254、B-68 416）。模型输出侧剥掉 `> ` 前缀、末尾括号说明段
    和首尾空白再数。
    """
    lines = []
    for line in text.splitlines():
        if strip_markdown_prefix and line.startswith("> "):
            lines.append(line[2:])
        elif strip_markdown_prefix and line.startswith(">"):
            lines.append(line[1:])
        else:
            lines.append(line)
    text = "\n".join(lines)
    text = strip_output_notes(text)
    return len(text.strip("\n"))


def retained(tokens, text):
    """粗核：token 逐字出现在 text 里才算保留，大小写敏感、忽略空白差异。"""
    norm = re.sub(r"\s+", "", text)
    hits, missing = [], []
    for pat, label, raw in tokens:
        probe = re.sub(r"\s+", "", raw)
        if probe and probe in norm:
            hits.append((pat, label, raw))
        else:
            missing.append((pat, label, raw))
    return hits, missing


def dash_metrics(blocks_text, original):
    """破折号密度：原文本段数、原/改每段 —— 计数、输出首句是否仍以 —— 起手。

    首句起手 = 正文第一段的第一个句子以 `——` 开头（SF-43 判据之一）。
    只统计含 —— 的段；输出侧首句起手是「该改没改」的残留信号。
    """
    def segs(text):
        return [s for s in re.split(r"\n\s*\n", text) if s.strip()]

    def strip_quote_prefix(text):
        """剥 blockquote 前缀：模型输出与 benchmark-blind 原文都可能带 `> `。"""
        lines = []
        for line in text.splitlines():
            if line.startswith("> "):
                lines.append(line[2:])
            elif line.startswith(">"):
                lines.append(line[1:])
            else:
                lines.append(line)
        return "\n".join(lines)

    orig_segs = segs(strip_quote_prefix(original))
    new_segs = segs(strip_quote_prefix(blocks_text))
    orig_counts = [s.count("——") for s in orig_segs]
    new_counts = [s.count("——") for s in new_segs]

    def first_sentence(text):
        return re.split(r"(?<=[。！？.!?])", text, maxsplit=1)[0]

    orig_first_starts = False
    if orig_segs:
        orig_first_starts = first_sentence(orig_segs[0]).lstrip().startswith("——")

    new_first_starts = False
    if new_segs:
        new_first_starts = first_sentence(new_segs[0]).lstrip().startswith("——")

    return {
        "original_segments": len(orig_segs),
        "output_segments": len(new_segs),
        "original_per_segment": orig_counts,
        "output_per_segment": new_counts,
        "output_total_dashes": sum(new_counts),
        "original_first_sentence_starts_with_dash": orig_first_starts,
        "output_first_sentence_starts_with_dash": new_first_starts,
    }


# ---------------------------------------------------------------------------
# residual 统计层（v2.3.0）
# ---------------------------------------------------------------------------
# 定位：既有三项硬判都在「保真侧」——改写有没有改坏。这一层补「残留侧」：
# 改完读起来还像不像模型写的。判据全部不依赖词表，抓的是「换一套词继续做
# 同一件事」——词表拦不住换字，统计量拦得住。
#
# 全部只报警，不判死，不影响退出码。阈值由 --calibrate 在 evals/benchmark.md
# 的 SF（该改）/ SNF（不该改）两组语料上实测标定，不照抄外部经验值。
#
# v2.3.0 标定实测结论（`--calibrate`，SF 53 / SNF 42）：
#   - 句长变异系数：**标不了**。够 12 句的样本 SF 只有 2 条、SNF 零条。
#     标定它需要「人写长文」对照组，本仓库语料里一篇都没有（real-samples.md
#     的 5 条 long 全是 AI 味样本，没有反例）。缺口留给后续版本。
#   - 连词密度：**全局判据被实测否掉，不设阈值**。SNF 中位 5.26 / 千字高于
#     SF 中位 0.00，且 SNF max 81.08 高于 SF max 80.00——不该改的比该改的
#     密度还高。benchmark 里有一对同密度对照用例钉住这件事：SF-50
#     （public-writing 叙事）80.00 该删一半，SNF-39（docs 迁移说明）81.08
#     一个都不能删。原因是 docs / status 靠显性连词承担条件与因果。照抄
#     外部「每千字 7 个」的阈值会优先误伤不该改的文本，因此本层只输出
#     数值供人看，判定交给 structures.md 第 23 条的场景限定。
#   - 名词化 / 借喻场：区分度好，且 SNF 侧零误报。名词化 SF max 4（SF-48）、
#     SNF max 0；借喻场 SF max 5（SF-52）、SNF max 1（SNF-41 的三套名义命中
#     被字面用法排除表滤成一套，正是该用例要验的）。两项都只报数不判死。
#
# v2.3.0 合并批次标定实测结论（`--calibrate`，SF 57 / SNF 46）：
#   - 「」/『』高亮短语：**原始计数不可设阈值**。两组中位数与 p90 都是 0，
#     max 都是 3。SF-55 的 3 处是抽象概念上的自造高亮，SNF-44 的 3 处是小说
#     人物对白；同一个计数对应相反结论，照抄上游「一篇 3 处以上」会直接误伤。
#     因此脚本只机械统计候选，是否属于自造金句仍由人结合引用、正式术语和
#     文学场景判断，不设阈值、不影响退出码。

# 显性连词：中文小句靠语序和事理相接，连词密度高是英文式衔接的搬运痕迹
CONJUNCTIONS_ZH = (
    "因为", "所以", "但是", "然而", "同时", "此外", "而且", "并且",
    "因此", "不仅", "于是", "另外", "总之", "首先", "其次",
    # 条件连词同属显性衔接，是 if/then/otherwise 的搬运重灾区。
    # 单字「则」不收——「规则 / 准则 / 原则」误伤面太大。
    "如果", "否则",
)

# 动词名词化：`进行 / 实现 / 完成 / 开展 / 起到` 带一个动名词，句子变长信息没变
NOMINALIZATION_PATTERNS = (
    re.compile(r"进行(?:了|一次|一场|着)?[^。，！？\n]{0,10}(?:调整|优化|升级|分析|讨论|沟通|梳理|复盘|迭代|探索|尝试|思考|规划|布局|评估|排查|验证)"),
    re.compile(r"实现了?[^。，！？\n]{0,14}的?[^。，！？\n]{0,6}(?:提升|增长|突破|转变|跃升|落地|改善)"),
    re.compile(r"完成了?对[^。，！？\n]{0,16}的"),
    re.compile(r"起到了?[^。，！？\n]{0,12}的?作用"),
    re.compile(r"具有[^。，！？\n]{0,10}(?:意义|价值)"),
    re.compile(r"开展[^。，！？\n]{0,10}(?:工作|建设|研究|合作)"),
)

# 借喻场：同一段里从多套不相干的比喻系统借词，是用比喻替代说明的信号。
# 单套用得准没问题，多套混用才报警。
METAPHOR_FIELDS = {
    "道路竞赛": ("赛道", "跑道", "岔路", "十字路口", "终点线", "起跑线", "弯道超车"),
    "战争攻防": ("护城河", "壁垒", "厮杀", "血战", "阵地", "弹药", "突围", "打法"),
    "建筑灾害": ("坍塌", "崩塌", "地基", "支柱", "废墟", "基石"),
    "温度": ("降温", "升温", "冷却", "余温", "白热化", "点燃"),
    "仓储": ("仓库", "库存", "抽屉", "货架", "囤积"),
    "海洋航行": ("蓝海", "红海", "浪潮", "潮水", "灯塔", "彼岸", "风口"),
    "机器器官": ("齿轮", "引擎", "发动机", "血管", "骨架", "神经末梢"),
}

# 借喻词的字面用法排除：这些前缀出现时该词是技术术语或本义，不算借喻。
# 误伤防护优先——本仓库的判据默认宁可漏报不可误杀。
METAPHOR_LITERAL_PREFIX = {
    "引擎": ("搜索", "渲染", "游戏", "物理", "推荐", "规则", "模板", "查询", "存储"),
    "发动机": ("汽车", "飞机", "柴油", "航空"),
    "仓库": ("代码", "git", "Git", "远程", "本地", "私有", "镜像"),
    "库存": ("商品", "实际", "系统", "剩余"),
    "阵地": ("前沿",),
    "风口": ("出", "通", "进"),
    "打法": ("战术",),
}


def mask_non_prose(text):
    """屏蔽代码块、行内代码、链接目标、URL 和 HTML 标签，保留字符偏移与换行。

    用等长空格替换而不是删除：偏移不变，后续算行号和窗口距离才准。
    """
    def mask(match):
        return "".join("\n" if ch == "\n" else " " for ch in match.group())

    patterns = (
        re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL),
        re.compile(r"```.*?```", re.DOTALL),
        re.compile(r"`[^`\n]*`"),
        re.compile(r"\]\([^\n)]*\)"),
        re.compile(r"https?://[^\s)>]+"),
        re.compile(r"<[^>\n]+>"),
    )
    out = text
    for pattern in patterns:
        out = pattern.sub(mask, out)
    return out


def strip_blockquote(text):
    """剥 blockquote 前缀（benchmark 语料的引用块与模型输出都可能带 `> `）。

    与 dash_metrics 内的同名局部函数功能一致；那个是既有代码的闭包，这里
    单独提供模块级版本给 residual 层用，不改动原函数。
    """
    lines = []
    for line in text.splitlines():
        if line.startswith("> "):
            lines.append(line[2:])
        elif line.startswith(">"):
            lines.append(line[1:])
        else:
            lines.append(line)
    return "\n".join(lines)


def han_count(text):
    return len(re.findall(r"[一-鿿]", text))


def _non_overlapping(text, terms):
    """长词优先的不重叠匹配，返回 [(位置, 词)]。避免「因此」被「因」重复计数。"""
    matches, occupied = [], []
    for term in sorted(terms, key=len, reverse=True):
        for m in re.finditer(re.escape(term), text):
            start, end = m.span()
            if any(start < oe and end > os for os, oe in occupied):
                continue
            matches.append((start, term))
            occupied.append((start, end))
    return sorted(matches)


def sentence_length_cv(text, min_sentences=12):
    """句长变异系数：人写的长短句差距大，模型的句长彼此接近。

    返回 (cv, 句数)。句数不足时 cv 为 None——短文本上这个量没有意义，
    不做外推。
    """
    lengths = [
        han_count(m.group())
        for m in re.finditer(r"[^。！？!?\n]+[。！？!?]", text)
        if han_count(m.group()) >= 4
    ]
    if len(lengths) < min_sentences:
        return None, len(lengths)
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return None, len(lengths)
    variance = sum((v - mean) ** 2 for v in lengths) / len(lengths)
    return (variance ** 0.5) / mean, len(lengths)


def conjunction_density(text):
    """显性连词密度（每千字）。返回 (密度, 命中数, 汉字数)。"""
    han = han_count(text)
    if han == 0:
        return None, 0, 0
    hits = _non_overlapping(text, CONJUNCTIONS_ZH)
    return len(hits) * 1000.0 / han, len(hits), han


def nominalization_hits(text):
    """动词名词化命中。返回 [(位置, 命中片段)]。"""
    out = []
    for pattern in NOMINALIZATION_PATTERNS:
        for m in pattern.finditer(text):
            out.append((m.start(), m.group()))
    return sorted(out)


def metaphor_fields_hit(text, window=800):
    """借喻场统计：返回 (最大同窗口场数, 命中明细)。

    命中明细为 [(位置, 场名, 词)]。字面用法（搜索引擎、代码仓库）先排除。
    """
    hits = []
    for field, words in METAPHOR_FIELDS.items():
        for word in words:
            for m in re.finditer(re.escape(word), text):
                prefixes = METAPHOR_LITERAL_PREFIX.get(word, ())
                head = text[max(0, m.start() - 4):m.start()]
                if any(head.endswith(p) for p in prefixes):
                    continue
                hits.append((m.start(), field, word))
    hits.sort()
    best = 0
    for i, (start, _, _) in enumerate(hits):
        fields = {h[1] for h in hits[i:] if h[0] - start <= window}
        best = max(best, len(fields))
    return best, hits


def highlight_quote_hits(text):
    """「」/『』括起的短语候选。返回 [(位置, 内容)]。

    只收同一行 1–30 字符的短内容，排除大段引用；脚本无法可靠区分自造金句、
    正式术语和人物对白，因此这一项只提供 residual 观测，不直接判定。
    """
    hits = []
    for pattern in (r"「([^「」\n]{1,30})」", r"『([^『』\n]{1,30})』"):
        for match in re.finditer(pattern, text):
            hits.append((match.start(), match.group(1)))
    return sorted(hits)


def paragraph_metrics(text):
    """段落形状：段数、每段汉字数、每段句数。

    抓的是「少分段 / 段落过长」，方向与 structures 第 13、14 条的过度格式化相反。
    只报数，不设阈值：中文段落长度的正常分布还没实测过，不照搬英文来源的判据。

    连续的列表行之间没有空行，会并进同一段计数，因此另报 list_lines，
    让读数的人自己判断段落数字在这份文本上可不可信。
    """
    blocks = [b for b in re.split(r"\n\s*\n", text) if han_count(b) > 0]
    list_lines = sum(
        1 for line in text.splitlines()
        if re.match(r"\s*(?:[-*+]|\d+[.)])\s", line)
    )
    if not blocks:
        return {
            "paragraphs": 0,
            "han_per_paragraph": None,
            "max_paragraph_han": None,
            "sentences_per_paragraph": None,
            "list_lines": list_lines,
        }
    hans = [han_count(b) for b in blocks]
    counts = [len(re.findall(r"[^。！？!?\n]+[。！？!?]", b)) for b in blocks]
    return {
        "paragraphs": len(blocks),
        "han_per_paragraph": round(sum(hans) / len(blocks), 1),
        "max_paragraph_han": max(hans),
        "sentences_per_paragraph": round(sum(counts) / len(blocks), 2),
        "list_lines": list_lines,
    }


def residual_metrics(text):
    """一段文本的残留统计量。输入应为正文（调用方负责剥 blockquote）。"""
    prose = mask_non_prose(text)
    paras = paragraph_metrics(prose)
    cv, sentences = sentence_length_cv(prose)
    density, conj_hits, han = conjunction_density(prose)
    noms = nominalization_hits(prose)
    fields, field_hits = metaphor_fields_hit(prose)
    quotes = highlight_quote_hits(prose)
    quote_density = len(quotes) * 1000.0 / han if han else None
    return {
        "han": han,
        "sentences": sentences,
        "paragraphs": paras["paragraphs"],
        "han_per_paragraph": paras["han_per_paragraph"],
        "max_paragraph_han": paras["max_paragraph_han"],
        "sentences_per_paragraph": paras["sentences_per_paragraph"],
        "list_lines": paras["list_lines"],
        "sentence_cv": None if cv is None else round(cv, 4),
        "conjunction_per_1k": None if density is None else round(density, 2),
        "conjunction_hits": conj_hits,
        "nominalization": len(noms),
        "nominalization_samples": [s for _, s in noms[:4]],
        "metaphor_fields": fields,
        "metaphor_samples": sorted({w for _, _, w in field_hits})[:6],
        "highlight_quotes": len(quotes),
        "highlight_quote_per_1k": None if quote_density is None else round(quote_density, 2),
        "highlight_quote_samples": [s for _, s in quotes[:6]],
    }


def retention_status(ratio):
    if ratio >= RETENTION_TARGET:
        return "ok"
    if ratio >= RETENTION_FLOOR:
        return "warn"
    return "fail"


def normalize_text(t):
    """归一化：去空白、全角/半角括号差异，用于「声明 no-op 但正文没跟上」比对。"""
    norm = re.sub(r"\s+", "", t)
    norm = norm.replace("（", "(").replace("）", ")").replace("，", ",").replace("。", ".")
    return norm


def is_noop(output_text):
    """no-op 判定：输出以「保留原文」开头，或处理结果不含改写正文。

    no-op 用例不判留存率——模型判定不该改时输出说明即可，字数变短不代表误删；
    留存率口径只约束实际改写（替掉人工对长文改写用例的 wc -m）。
    """
    head = output_text.lstrip().split("\n", 1)[0]
    # --pair/--stdin 模式给的是完整模型输出，先剥「处理结果：」前缀再判断
    m = re.match(r"^处理结果(?:（[^）]*）)?[:：]\s*", head)
    if m:
        head = head[m.end():]
    return (
        head.startswith("保留原文")
        or head.startswith("保持原文")
        or head.startswith("保留原文：")
        or head.startswith("保持原文：")
    )


def analyze_case(cid, scene, original, output_text, raw_output=None):
    """单条用例的硬判结果。

    raw_output：可选，完整输出文件文本，用于在判定链里查「力度=no-op」证据；
    缺省时退化用 output_text 本身。
    """
    # --pair/--stdin 常给完整模型输出（含 `## B-xx` 标题）。先尝试剥出「处理结果」
    # 正文；剥不出（纯正文）就原样用。raw_output 未提供时回填为剥前原文，
    # 保证判定链证据可用。
    if re.search(r"^#{1,3} ", output_text, re.MULTILINE):
        blocks = extract_blocks(output_text)
        target = blocks.get(cid) or next(
            (b for b in blocks.values() if b.strip()), ""
        )
        if target.strip():
            if raw_output is None:
                raw_output = output_text
            output_text = target
    char_orig = count_chars(original, strip_markdown_prefix=True)
    char_out = count_chars(output_text, strip_markdown_prefix=True)
    ratio = char_out / char_orig if char_orig else 1.0

    noop = is_noop(output_text)
    is_long = bool(LONG_TAG.search(scene))
    is_inplace_long = is_long and "in-place" in scene
    # 假 no-op 校验：声明保留原文时，要么判定链有「力度=no-op」的推理证据（judge 会复核），
    # 要么正文≈原文（归一化后长度不比原文短太多且原文字符基本都在）。
    # 两者都没有 → 标 noop_unverified，仍按长文判据计算，不让假 no-op 吞掉硬失败。
    noop_unverified = False
    if noop and is_inplace_long:
        verdict_text = raw_output or output_text
        chain_noop = re.search(r"力度\s*[:=]\s*no-?op", verdict_text) is not None
        norm_out = normalize_text(output_text)
        # benchmark-blind 原文带 `> ` blockquote 前缀，归一化前先剥掉
        stripped_orig = "\n".join(
            l[2:] if l.startswith("> ") else (l[1:] if l.startswith(">") else l)
            for l in original.splitlines()
        )
        norm_orig = normalize_text(stripped_orig)
        # 真 no-op 的输出要么是原文本身（正文连续包含归一化后的原文），
        # 要么有判定链「力度=no-op」佐证。假 no-op 只有一句「保留原文」的说明，
        # 原文不会连续出现 → 标 noop_unverified，仍按实际留存率判。
        body_ok = bool(norm_orig) and norm_orig in norm_out
        noop_ok = chain_noop or body_ok
        if not noop_ok:
            noop_unverified = True
        if noop_ok and body_ok:
            # 正文≈原文：留存率按 100% 记（与手工 wc -m 口径一致，
            # 「处理结果：/保持原文：」等包装字不计入分子）
            char_out = char_orig
            ratio = 1.0
    retention = None
    if is_inplace_long:
        status = "noop" if (noop and not noop_unverified) else retention_status(ratio)
        retention = {
            "original_chars": char_orig,
            "output_chars": char_out,
            "ratio": round(ratio, 4),
            "target": RETENTION_TARGET,
            "floor": RETENTION_FLOOR,
            "status": status,
            "noop_unverified": noop_unverified,
        }

    dm = dash_metrics(output_text, original)
    dashes_dense = (
        max(dm["output_per_segment"], default=0) >= 4
        or dm["output_first_sentence_starts_with_dash"]
    )

    tokens = []
    for pat, label in TOKEN_PATTERNS:
        for m in re.finditer(pat, original, re.MULTILINE):
            raw = m.group(0).strip()
            if raw and re.fullmatch(r"[\s\W_]+", raw):
                continue
            tokens.append((pat, label, raw, m.start(), m.end()))

    # 版本号优先：先剥掉完整版本跨度，避免「v1.8.0」再被裸数字拆成幽灵片段 8/8.0
    version_spans = []
    for pat, label in TOKEN_PATTERNS:
        if label != "版本号":
            continue
        for m in re.finditer(pat, original, re.MULTILINE):
            version_spans.append((m.start(), m.end()))
    if version_spans:
        kept = []
        for pat, label, raw, start, end in tokens:
            if any(s < end and start < e for s, e in version_spans if not (label == "版本号" and s == start and e == end)):
                continue
            kept.append((pat, label, raw, start, end))
        tokens = kept

    # 按位置覆盖去重：一个匹配完全落在更早（更长）匹配区间内时丢弃。
    # 例：`3.8%` 先被「数字+单位」匹配（0,4），`3` / `3.8` 落在其内 → 丢弃。
    # 模式顺序即优先级：数字+单位 > 版本号 > 路径 > 标识符 > 日期 > 数字。
    tokens.sort(key=lambda t: (t[3], -(t[4] - t[3])))
    deduped = []
    covered_until = -1
    for pat, label, raw, start, end in tokens:
        if start < covered_until:
            continue
        deduped.append((pat, label, raw))
        covered_until = max(covered_until, end)
    # no-op 用例也要跑粗核：模型说「保留原文」但实际改了数字/术语时，
    # 缺失报警能抓住假 no-op（留存率不判是因为输出是说明文字不是正文）
    hits, missing = retained(deduped, output_text)

    return {
        "case": cid,
        "scene": scene,
        "is_long": is_long,
        "retention": retention,
        "dashes": {
            "dense": dashes_dense,
            **dm,
        },
        "protected": {
            "total": len(deduped),
            "hit": len(hits),
            "missing": missing,
        },
        "noop": noop,
        "noop_unverified": noop_unverified,
    }


def summarize(result):
    """把单条结果变成 markdown 小节（run-eval.md 口径的判定）。"""
    lines = [f"### {result['case']} | {result['scene']}", ""]
    if result["is_long"] and not result["retention"]:
        # 非 in-place 的长文都走这一支：bounded、no-op 判定用例都在内。
        # 早期措辞一律写成「bounded 长文」，会让 judge 误以为用例被判成了 bounded
        # （v2.3.0 跨模型盲测中 judge 对 SNF-38 提出过这一点），改为按场景标签直述。
        lines.append(
            f"- 字数留存率：不适用（场景标签 `{result['scene'] or '未标注'}` 不含 in-place，"
            "run-eval.md 口径只对 in-place 长文判留存率）"
        )
    if result["retention"]:
        r = result["retention"]
        if r.get("noop_unverified"):
            lines.append(f"- 字数留存率：{r['output_chars']}/{r['original_chars']} = {r['ratio']:.1%}（⚠️ 声明保留原文但正文未跟上原文，按实际改写判：目标 ≥ {r['target']:.0%}，硬下限 {r['floor']:.0%}）→ **{r['status'].upper()}**")
        elif r["status"] == "noop":
            lines.append(f"- 字数留存率：{r['output_chars']}/{r['original_chars']} = {r['ratio']:.1%}（no-op：模型判定保留原文，留存率不判；数字仅供参考复核）")
        else:
            lines.append(f"- 字数留存率：{r['output_chars']}/{r['original_chars']} = {r['ratio']:.1%}（目标 ≥ {r['target']:.0%}，硬下限 {r['floor']:.0%}）→ **{r['status'].upper()}**")
        if r["status"] == "warn":
            lines.append("  - ⚠️ 低于目标，高于硬下限：符合 run-eval.md 的既有口径但需 judge 复核风格列")
        elif r["status"] == "fail":
            lines.append("  - ❌ 低于硬下限：长文误删并句重排风险，按 run-eval.md 记硬约束 ❌")
    d = result["dashes"]
    lines.append(f"- 破折号密度：原 {d['original_per_segment']} / 改 {d['output_per_segment']}；输出首句起手={d['output_first_sentence_starts_with_dash']}；总 {d['output_total_dashes']} 处")
    if d["dense"]:
        lines.append("  - ⚠️ 单段 ≥ 4 处或首句起手：命中 SF-43 破折号过密信号，需 judge 复核标点腔处理")
    p = result["protected"]
    lines.append(f"- protected spans 粗核：{p['hit']}/{p['total']} 保留")
    if p["missing"]:
        lines.append("  - ⚠️ 以下受保护片段在输出中未逐字找到（报警不判死，留给 judge 复核）：")
        for pat, label, raw in p["missing"]:
            lines.append(f"    - [{label}] `{raw}`")
    lines.append("")
    return "\n".join(lines)


def analyze_run(root, run_dir):
    """扫批次目录：配对 benchmark-blind.md 原文与各模型输出，逐条硬判。"""
    run_dir = Path(run_dir)
    cases = parse_cases(root)
    by_id = {cid: (scene, quote) for cid, scene, quote in cases}

    if run_dir.is_dir():
        candidates = sorted(run_dir.rglob("rewrite-*.md"))
    elif run_dir.is_file():
        candidates = [run_dir]
    else:
        print(f"hard_metrics: 路径不存在：{run_dir}", file=sys.stderr)
        sys.exit(2)

    model_reports = {}
    report_paths = []
    file_results = {}
    problems = {}
    for path in candidates:
        m = re.search(r"rewrite-([A-Za-z0-9-]+)\.md$", path.name)
        if not m:
            continue
        batch = m.group(1)
        report_paths.append(path)
        blocks = extract_blocks(path.read_text(encoding="utf-8"))
        expected = batch_expected_ids(batch)
        actual_ids = set(blocks)
        if expected is None:
            # 非区间命名（targeted 补跑等）：以实际出现的标题为准
            target_ids = actual_ids
        else:
            target_ids = expected
        ignored = sorted(actual_ids - target_ids)
        results = []
        for cid in sorted(target_ids):
            scene, quote = by_id.get(cid, ("", ""))
            output_text = blocks.get(cid, "")
            if not output_text:
                results.append({
                    "case": cid, "scene": scene,
                    "is_long": bool(LONG_TAG.search(scene)),
                    "retention": None, "dashes": None, "protected": None,
                    "missing_output": True, "noop": False, "noop_unverified": False,
                })
                continue
            results.append(analyze_case(cid, scene, quote, output_text, path.read_text(encoding="utf-8")))

        retentions = [r["retention"] for r in results if r.get("retention")]
        fails = [r["case"] for r in results if r.get("retention") and r["retention"]["status"] == "fail"]
        warns = [r["case"] for r in results if r.get("retention") and r["retention"]["status"] == "warn"]
        dense = [
            (r["case"], max(r["dashes"]["output_per_segment"], default=0))
            for r in results if r.get("dashes") and r["dashes"]["dense"]
        ]
        missing_spans = [
            (r["case"], len(r["protected"]["missing"]))
            for r in results if r.get("protected") and r["protected"]["missing"]
        ]

        key = path.relative_to(run_dir).as_posix() if run_dir.is_dir() else path.name
        file_results[key] = results
        # 零用例批次 = 解析失败或命名不被识别（如旧口径 SF-xx），报告不完整，记硬错
        if len(results) == 0:
            problems.setdefault(key, []).append("零用例批次（文件名命名未被 Bxx-yy 识别或正文为空）")
        if any(r.get("missing_output") for r in results):
            problems.setdefault(key, []).append(
                f"缺输出：{', '.join(r['case'] for r in results if r.get('missing_output'))}"
            )
        model_reports[key] = {
            "batch": batch,
            "total_cases": len(results),
            "ignored_out_of_range": ignored,
            "missing_output": [r["case"] for r in results if r.get("missing_output")],
            "long_form": {
                "cases": len(retentions),
                "warn": warns,
                "fail": fails,
            },
            "dash_dense": dense,
            "protected_missing": missing_spans,
        }

    if not report_paths:
        print(f"hard_metrics: {run_dir} 下没有找到 rewrite-*.md 文件", file=sys.stderr)
        sys.exit(2)

    lines_out = [
        "# Hard Metrics — 硬判报告",
        "",
        f"> 由 `python3 automation/eval/hard_metrics.py --run {run_dir}` 生成。",
        "> 字数留存率与破折号密度按 `evals/run-eval.md` 既有口径判定；protected spans 粗核只报警不判死，缺失由 judge 复核。",
        "> 本报告是运行产物，不入 commit；需要时归档到 `tasks/` 下。",
        "",
        "## 汇总",
        "",
    ]
    total_fail, total_warn = 0, 0
    for key, rep in model_reports.items():
        lf = rep["long_form"]
        total_fail += len(lf["fail"])
        total_warn += len(lf["warn"])
    lines_out.append(f"- 长文硬下限失败 {total_fail} 条（{', '.join(c for rep in model_reports.values() for c in rep['long_form']['fail']) or '无'}）")
    lines_out.append(f"- 长文目标下警告 {total_warn} 条（{', '.join(c for rep in model_reports.values() for c in rep['long_form']['warn']) or '无'}）")
    lines_out.append("")
    for path in report_paths:
        key = path.relative_to(run_dir).as_posix() if run_dir.is_dir() else path.name
        rep = model_reports[key]
        lines_out += [f"## {key}", ""]
        lines_out.append(f"- 用例总数：{rep['total_cases']}")
        if rep.get("ignored_out_of_range"):
            lines_out.append(f"- ⚠️ 区间外标题（已忽略）：{', '.join(rep['ignored_out_of_range'])}")
        if rep["missing_output"]:
            lines_out.append(f"- ⚠️ 缺输出：{', '.join(rep['missing_output'])}")
        lf = rep["long_form"]
        if lf["cases"]:
            lines_out.append(f"- 长文用例 {lf['cases']} 条：硬下限失败 {len(lf['fail'])}（{', '.join(lf['fail']) or '无'}），目标下警告 {len(lf['warn'])}（{', '.join(lf['warn']) or '无'}）")
        else:
            lines_out.append("- 长文用例：0（本批次无 long 标签用例，留存率不判）")
        if rep["dash_dense"]:
            lines_out.append(f"- ⚠️ 破折号过密 {len(rep['dash_dense'])} 条：{', '.join(f'{cid}（{n} 处）' for cid, n in rep['dash_dense'])}")
        if rep["protected_missing"]:
            lines_out.append(f"- ⚠️ 保护片段缺失报警 {len(rep['protected_missing'])} 条：{', '.join(f'{cid}（{n} 项）' for cid, n in rep['protected_missing'])}")
        lines_out.append("")
        for res in file_results[key]:
            if res.get("missing_output"):
                lines_out.append(f"### {res['case']} | {res['scene']}")
                lines_out.append("")
                lines_out.append("- ⚠️ 缺输出：本用例在输出文件中没有解析到处理结果")
                lines_out.append("")
                continue
            lines_out.append(summarize(res))
        lines_out.append("")

    header = lines_out

    out_path = run_dir if run_dir.is_dir() else run_dir.parent
    md_path = out_path / "hard-metrics.md"
    json_path = out_path / "hard-metrics.json"
    md_path.write_text("\n".join(header).rstrip() + "\n", encoding="utf-8")
    json_path.write_text(
        json.dumps({"reports": model_reports, "cases": file_results}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"hard-metrics: {len(report_paths)} 个批次 → {md_path}, {json_path}")
    for name, probs in problems.items():
        for prob in probs:
            print(f"  ⚠️ {name}: {prob}")
    for name, rep in model_reports.items():
        lf = rep["long_form"]
        print(f"  {name}: {rep['total_cases']} 条, 长文 {lf['cases']} 条, 硬下限失败 {len(lf['fail'])}")
    # 退出码：硬下限失败=1；批次不完整（零用例/缺输出）这类报告不可信=2；其余=0
    if any(problems.values()):
        return 2
    return 1 if any(rep["long_form"]["fail"] for rep in model_reports.values()) else 0


def _percentile(values, q):
    """线性插值分位数。零依赖手写，与文件其余部分保持同一风格。"""
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    idx = (len(ordered) - 1) * q
    lo = int(idx)
    hi = min(lo + 1, len(ordered) - 1)
    frac = idx - lo
    return ordered[lo] * (1 - frac) + ordered[hi] * frac


class HumanCorpusError(ValueError):
    """HUMAN manifest 或正文不满足可复现统计合同。"""


HUMAN_REQUIRED_FIELDS = {
    "id",
    "path",
    "scene",
    "genre",
    "era",
    "origin_language",
    "representation_role",
    "author_group",
    "source_type",
    "source_url",
    "source_revision",
    "source_revision_at",
    "source_title",
    "source_author",
    "license",
    "license_url",
    "license_evidence_url",
    "modifications",
    "consent_evidence",
    "written_at",
    "fixed_revision_at",
    "ai_assisted",
    "ai_evidence",
    "deidentified",
    "added_on",
    "sha256",
    "withdrawn",
}
HUMAN_SCENES = {"chat", "status", "docs", "public-writing"}
HUMAN_ERAS = {"historical", "modern"}
HUMAN_ORIGIN_LANGUAGES = {"zh-original", "translated-from-en"}
HUMAN_REPRESENTATION_ROLES = {"direct", "proxy"}
HUMAN_SOURCE_TYPES = {"owner", "open"}
HUMAN_OPEN_LICENSES = {
    "CC0",
    "CC0 1.0",
    "CC BY 1.0",
    "CC BY 2.0",
    "CC BY 2.5",
    "CC BY 3.0",
    "CC BY 4.0",
    "CC BY-SA 1.0",
    "CC BY-SA 2.0",
    "CC BY-SA 2.5",
    "CC BY-SA 3.0",
    "CC BY-SA 4.0",
    "Public Domain",
    "written-permission",
}
HUMAN_CC_LICENSE_URLS = {
    "CC0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "CC0 1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "CC BY 1.0": "https://creativecommons.org/licenses/by/1.0/",
    "CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/",
    "CC BY 2.5": "https://creativecommons.org/licenses/by/2.5/",
    "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/",
    "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC BY-SA 1.0": "https://creativecommons.org/licenses/by-sa/1.0/",
    "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/",
    "CC BY-SA 2.5": "https://creativecommons.org/licenses/by-sa/2.5/",
    "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/",
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
    "Public Domain": "https://creativecommons.org/publicdomain/mark/1.0/",
}
HUMAN_MEDIAWIKI_LICENSE_EVIDENCE = {
    ("zh.wikinews.org", "CC BY 2.5"): ("Wikinews:版权信息", "262628"),
    ("zh.wikisource.org", "CC BY-SA 4.0"): ("Wikisource:版权信息", "2437011"),
}


def _inside_root(root, path):
    root = root.resolve()
    path = path.resolve()
    return path == root or root in path.parents


def load_human_corpus(root, manifest_path):
    """读取并严格校验 HUMAN JSONL；返回含统计元数据的记录。

    active 正文必须可随仓库再分发、明确未经过 AI 辅助、至少 1000 个汉字且
    当前句子解析器能识别至少 12 句。withdrawn 条目只保留编号和 provenance，
    不要求正文继续存在，也不进入分布。
    """
    root = Path(root).resolve()
    manifest = Path(manifest_path)
    if not manifest.is_absolute():
        manifest = root / manifest
    try:
        raw = manifest.read_text(encoding="utf-8")
    except OSError as exc:
        raise HumanCorpusError(f"无法读取 manifest {manifest}: {exc}") from exc

    corpus_dir_path = root / "evals" / "human-corpus"
    records, ids, paths, hashes = [], set(), set(), set()
    for line_no, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise HumanCorpusError(f"{manifest}:{line_no} 不是合法 JSON: {exc.msg}") from exc
        if not isinstance(item, dict):
            raise HumanCorpusError(f"{manifest}:{line_no} 每行必须是 JSON object")
        missing = sorted(HUMAN_REQUIRED_FIELDS - item.keys())
        if missing:
            raise HumanCorpusError(f"{manifest}:{line_no} 缺字段: {', '.join(missing)}")
        extra = sorted(item.keys() - HUMAN_REQUIRED_FIELDS)
        if extra:
            raise HumanCorpusError(f"{manifest}:{line_no} 未定义字段: {', '.join(extra)}")

        cid = item["id"]
        if not isinstance(cid, str) or not re.fullmatch(r"HUMAN-\d{2,}", cid):
            raise HumanCorpusError(f"{manifest}:{line_no} id 必须是 HUMAN-01 形式")
        if cid in ids:
            raise HumanCorpusError(f"{manifest}:{line_no} 重复 id: {cid}")
        ids.add(cid)

        for key in (
            "scene",
            "genre",
            "era",
            "origin_language",
            "representation_role",
            "author_group",
            "source_type",
            "license",
            "consent_evidence",
            "written_at",
            "ai_assisted",
            "ai_evidence",
            "added_on",
        ):
            if not isinstance(item[key], str) or not item[key].strip():
                raise HumanCorpusError(f"{manifest}:{line_no} {key} 必须是非空字符串")
        if item["scene"] not in HUMAN_SCENES:
            raise HumanCorpusError(f"{manifest}:{line_no} scene 不在允许集合: {item['scene']}")
        if item["era"] not in HUMAN_ERAS:
            raise HumanCorpusError(f"{manifest}:{line_no} era 不在允许集合: {item['era']}")
        if item["origin_language"] not in HUMAN_ORIGIN_LANGUAGES:
            raise HumanCorpusError(
                f"{manifest}:{line_no} origin_language 不在允许集合: {item['origin_language']}"
            )
        if item["representation_role"] not in HUMAN_REPRESENTATION_ROLES:
            raise HumanCorpusError(
                f"{manifest}:{line_no} representation_role 不在允许集合: {item['representation_role']}"
            )
        if item["source_type"] not in HUMAN_SOURCE_TYPES:
            raise HumanCorpusError(f"{manifest}:{line_no} source_type 只能是 owner/open")
        if not isinstance(item["deidentified"], bool) or not isinstance(item["withdrawn"], bool):
            raise HumanCorpusError(f"{manifest}:{line_no} deidentified/withdrawn 必须是 boolean")
        for key in (
            "source_url",
            "source_revision",
            "source_revision_at",
            "source_title",
            "source_author",
            "license_url",
            "license_evidence_url",
            "modifications",
            "fixed_revision_at",
        ):
            if not isinstance(item[key], str):
                raise HumanCorpusError(f"{manifest}:{line_no} {key} 必须是字符串")
        if item["source_type"] == "open" and not re.fullmatch(r"https?://\S+", item["source_url"]):
            raise HumanCorpusError(f"{manifest}:{line_no} open 条目必须给出 http(s) source_url")
        if item["source_type"] == "open" and not item["source_revision"].strip():
            raise HumanCorpusError(f"{manifest}:{line_no} open 条目必须给出 source_revision")
        if item["source_type"] == "open" and not item["source_revision_at"].strip():
            raise HumanCorpusError(f"{manifest}:{line_no} open 条目必须给出 source_revision_at")
        if item["source_type"] == "open" and not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}", item["fixed_revision_at"]
        ):
            raise HumanCorpusError(
                f"{manifest}:{line_no} open 条目 fixed_revision_at 必须是 YYYY-MM-DD"
            )
        if item["source_type"] == "owner" and item["fixed_revision_at"] and not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}", item["fixed_revision_at"]
        ):
            raise HumanCorpusError(
                f"{manifest}:{line_no} owner 条目 fixed_revision_at 应留空或使用 YYYY-MM-DD"
            )
        if item["fixed_revision_at"]:
            try:
                date.fromisoformat(item["fixed_revision_at"])
            except ValueError as exc:
                raise HumanCorpusError(
                    f"{manifest}:{line_no} fixed_revision_at 不是有效日期"
                ) from exc
        if item["source_revision_at"]:
            try:
                revision_time = datetime.fromisoformat(
                    item["source_revision_at"].replace("Z", "+00:00")
                )
            except ValueError as exc:
                raise HumanCorpusError(
                    f"{manifest}:{line_no} source_revision_at 不是有效 ISO 8601 时间"
                ) from exc
            if revision_time.tzinfo is None or revision_time.utcoffset() != timezone.utc.utcoffset(None):
                raise HumanCorpusError(
                    f"{manifest}:{line_no} source_revision_at 必须明确使用 UTC"
                )
            if item["fixed_revision_at"] != revision_time.date().isoformat():
                raise HumanCorpusError(
                    f"{manifest}:{line_no} fixed_revision_at 必须与 source_revision_at 的 UTC 日期一致"
                )
        if item["source_type"] == "open":
            source = urlparse(item["source_url"])
            evidence = urlparse(item["license_evidence_url"])
            if source.hostname in {"zh.wikinews.org", "zh.wikisource.org"}:
                oldids = parse_qs(source.query).get("oldid", [])
                evidence_oldids = parse_qs(evidence.query).get("oldid", [])
                if not re.fullmatch(r"[1-9]\d*", item["source_revision"]):
                    raise HumanCorpusError(
                        f"{manifest}:{line_no} MediaWiki source_revision 必须是正整数"
                    )
                if oldids != [item["source_revision"]]:
                    raise HumanCorpusError(
                        f"{manifest}:{line_no} MediaWiki source_url 的 oldid 必须与 source_revision 一致"
                    )
                expected_evidence = HUMAN_MEDIAWIKI_LICENSE_EVIDENCE.get(
                    (source.hostname, item["license"])
                )
                evidence_titles = parse_qs(evidence.query).get("title", [])
                if (
                    expected_evidence is None
                    or evidence.hostname != source.hostname
                    or evidence_titles != [expected_evidence[0]]
                    or evidence_oldids != [expected_evidence[1]]
                ):
                    raise HumanCorpusError(
                        f"{manifest}:{line_no} MediaWiki license_evidence_url 必须指向已核验的固定版权政策 revision"
                    )
        if item["source_type"] == "open" and (
            not item["source_title"].strip() or not item["source_author"].strip()
        ):
            raise HumanCorpusError(f"{manifest}:{line_no} open 条目必须给出 source_title/source_author 作归属")
        if item["source_type"] == "open" and item["license"] not in HUMAN_OPEN_LICENSES:
            raise HumanCorpusError(
                f"{manifest}:{line_no} open 条目 license 不在允许集合: {item['license']}"
            )
        if item["source_type"] == "open" and not re.fullmatch(
            r"https?://\S+", item["license_evidence_url"]
        ):
            raise HumanCorpusError(
                f"{manifest}:{line_no} open 条目必须给出 http(s) license_evidence_url"
            )
        if (
            item["source_type"] == "open"
            and item["license_evidence_url"] == item["license_url"]
        ):
            raise HumanCorpusError(
                f"{manifest}:{line_no} license_evidence_url 必须指向逐篇作品证据，不能只填通用 license_url"
            )
        if item["source_type"] == "owner" and item["license"] != "repository-owner-authorized":
            raise HumanCorpusError(
                f"{manifest}:{line_no} owner 条目 license 必须是 repository-owner-authorized"
            )
        if item["source_type"] == "owner" and item["license_url"]:
            raise HumanCorpusError(f"{manifest}:{line_no} owner 条目 license_url 应留空")
        if item["source_type"] == "owner" and item["license_evidence_url"]:
            raise HumanCorpusError(f"{manifest}:{line_no} owner 条目 license_evidence_url 应留空")
        if item["source_type"] == "open" and item["license"] in HUMAN_CC_LICENSE_URLS:
            expected_license_url = HUMAN_CC_LICENSE_URLS[item["license"]]
            if item["license_url"] != expected_license_url:
                raise HumanCorpusError(
                    f"{manifest}:{line_no} license_url 必须是 {expected_license_url}"
                )
        if item["source_type"] == "open" and item["license"] == "written-permission" and item["license_url"]:
            raise HumanCorpusError(f"{manifest}:{line_no} written-permission 的 license_url 应留空")
        if not item["withdrawn"] and not item["modifications"].strip():
            raise HumanCorpusError(f"{manifest}:{line_no} active 条目必须用 modifications 说明是否改动")
        evidence = item["consent_evidence"]
        if item["withdrawn"] and not re.fullmatch(
            r"withdrawn by author on \d{4}-\d{2}-\d{2}", evidence
        ):
            raise HumanCorpusError(f"{manifest}:{line_no} withdrawn consent_evidence 格式不合合同")
        if not item["withdrawn"] and item["source_type"] == "owner" and not re.fullmatch(
            r"owner approved repository redistribution on \d{4}-\d{2}-\d{2}", evidence
        ):
            raise HumanCorpusError(f"{manifest}:{line_no} owner consent_evidence 格式不合合同")
        if not item["withdrawn"] and item["source_type"] == "open" and item["license"] != "written-permission":
            if evidence != f"source page declares {item['license']}":
                raise HumanCorpusError(f"{manifest}:{line_no} 开放许可 consent_evidence 必须逐字对应 license")
        if not item["withdrawn"] and item["source_type"] == "open" and item["license"] == "written-permission":
            if not re.fullmatch(r"written permission archived at \S+ on \d{4}-\d{2}-\d{2}", evidence):
                raise HumanCorpusError(f"{manifest}:{line_no} written-permission consent_evidence 格式不合合同")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item["added_on"]):
            raise HumanCorpusError(f"{manifest}:{line_no} added_on 必须是 YYYY-MM-DD")

        record = dict(item)
        record["manifest_line"] = line_no
        if item["withdrawn"]:
            record.update({"text": None, "han": 0, "sentences": 0, "metrics": None})
            records.append(record)
            continue

        if item["ai_assisted"] != "no":
            raise HumanCorpusError(f"{manifest}:{line_no} active HUMAN 条目必须明确 ai_assisted=no")
        if not item["deidentified"]:
            raise HumanCorpusError(f"{manifest}:{line_no} active HUMAN 条目必须完成隐私检查并设 deidentified=true")
        if not isinstance(item["path"], str) or not item["path"].strip():
            raise HumanCorpusError(f"{manifest}:{line_no} active HUMAN 条目必须给出 path")
        try:
            rel = Path(item["path"])
            candidate = root / rel
            lexical_corpus_dir = corpus_dir_path
            if (root / "evals").is_symlink() or lexical_corpus_dir.is_symlink():
                raise HumanCorpusError(f"{manifest}:{line_no} HUMAN 目录及其父目录不能是 symlink")
            corpus_dir = lexical_corpus_dir.resolve()
            body_path = candidate.resolve()
        except HumanCorpusError:
            raise
        except (OSError, ValueError) as exc:
            raise HumanCorpusError(f"{manifest}:{line_no} path 无法解析: {item['path']}") from exc
        expected_rel = Path("evals") / "human-corpus" / f"{cid}.txt"
        if rel.is_absolute() or rel != expected_rel:
            raise HumanCorpusError(f"{manifest}:{line_no} path 必须精确为 {expected_rel.as_posix()}")
        if not _inside_root(corpus_dir, body_path):
            raise HumanCorpusError(f"{manifest}:{line_no} path 解析后越出 evals/human-corpus/: {item['path']}")
        if candidate.is_symlink():
            raise HumanCorpusError(f"{manifest}:{line_no} HUMAN 正文不能是 symlink: {item['path']}")
        try:
            rel_key = body_path.relative_to(root).as_posix()
        except ValueError as exc:
            raise HumanCorpusError(f"{manifest}:{line_no} path 解析后越出仓库: {item['path']}") from exc
        if rel_key in paths:
            raise HumanCorpusError(f"{manifest}:{line_no} 重复 path: {item['path']}")
        paths.add(rel_key)
        try:
            body_bytes = body_path.read_bytes()
            body = body_bytes.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            raise HumanCorpusError(f"{manifest}:{line_no} 无法读取 UTF-8 正文 {item['path']}: {exc}") from exc

        digest = hashlib.sha256(body_bytes).hexdigest()
        if not isinstance(item["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
            raise HumanCorpusError(f"{manifest}:{line_no} sha256 必须是 64 位小写十六进制")
        if digest != item["sha256"]:
            raise HumanCorpusError(f"{manifest}:{line_no} sha256 不匹配: {item['path']}")
        if digest in hashes:
            raise HumanCorpusError(f"{manifest}:{line_no} 正文重复（sha256）: {item['path']}")
        hashes.add(digest)

        metrics = residual_metrics(body)
        if metrics["han"] < 1000:
            raise HumanCorpusError(f"{manifest}:{line_no} {cid} 只有 {metrics['han']} 个汉字，低于 1000")
        if metrics["sentences"] < 12:
            raise HumanCorpusError(f"{manifest}:{line_no} {cid} 只识别到 {metrics['sentences']} 句，低于 12")
        record.update({"text": body, "han": metrics["han"], "sentences": metrics["sentences"], "metrics": metrics})
        records.append(record)

    try:
        body_files = sorted(path for path in corpus_dir_path.iterdir() if path.suffix == ".txt")
    except OSError as exc:
        raise HumanCorpusError(f"无法读取 HUMAN 正文目录 {corpus_dir_path}: {exc}") from exc
    unregistered = [path.name for path in body_files if path.stem not in ids]
    if unregistered:
        raise HumanCorpusError(
            "HUMAN 正文目录存在 manifest 未登记文件: " + ", ".join(unregistered)
        )

    if not records:
        raise HumanCorpusError(f"{manifest} 没有任何条目")
    if not any(not record["withdrawn"] for record in records):
        raise HumanCorpusError(f"{manifest} 没有 active HUMAN 正文")
    return records


def validate_human_cohort(records):
    """校验 v2.3.1 发布口径；采集期可只调用 load_human_corpus 检查单篇。"""
    active = [record for record in records if not record["withdrawn"]]
    if not 8 <= len(active) <= 12:
        raise HumanCorpusError(f"active HUMAN 正文应为 8–12 篇，实际 {len(active)} 篇")
    source_types = {record["source_type"] for record in active}
    if source_types != {"open"}:
        raise HumanCorpusError(
            f"v2.3.1 active HUMAN 正文必须全部来自可核验公开来源，实际 {sorted(source_types)}"
        )
    author_groups = {record["author_group"] for record in active}
    if len(author_groups) < 3:
        raise HumanCorpusError(
            f"active HUMAN 正文至少需要 3 个作者组，实际 {len(author_groups)} 个"
        )
    era_counts = Counter(record["era"] for record in active)
    if era_counts["historical"] < 3:
        raise HumanCorpusError("active HUMAN 历史文本至少需要 3 篇")
    if era_counts["modern"] < 3:
        raise HumanCorpusError("active HUMAN 现代文本至少需要 3 篇")
    translated = sum(
        record["origin_language"] == "translated-from-en" for record in active
    )
    if translated * 3 > len(active):
        raise HumanCorpusError("翻译文本不得超过 active cohort 的三分之一")
    return active


def validate_human_representativeness(records):
    """发布代表性门禁；proxy 可参与 residual，但不能替 direct 场景顶数。"""
    active = validate_human_cohort(records)
    required_scenes = {"docs", "public-writing", "status"}
    direct_scenes = {
        record["scene"] for record in active if record["representation_role"] == "direct"
    }
    missing_scenes = sorted(required_scenes - direct_scenes)
    if missing_scenes:
        raise HumanCorpusError(
            "active HUMAN direct 样本缺少代表性场景: " + ", ".join(missing_scenes)
        )
    return active


def _distribution(values):
    if not values:
        return {"n": 0, "min": None, "p10": None, "p25": None, "median": None, "p75": None, "p90": None, "max": None, "raw": []}
    return {
        "n": len(values),
        "min": min(values),
        "p10": _percentile(values, 0.10),
        "p25": _percentile(values, 0.25),
        "median": _percentile(values, 0.50),
        "p75": _percentile(values, 0.75),
        "p90": _percentile(values, 0.90),
        "max": max(values),
        "raw": sorted(values) if len(values) < 8 else [],
    }


def human_corpus_report(records):
    """生成不含正文的 HUMAN 统计报告。"""
    active = [record for record in records if not record["withdrawn"]]

    def group_report(items):
        cvs = [item["metrics"]["sentence_cv"] for item in items if item["metrics"]["sentence_cv"] is not None]
        conjs = [item["metrics"]["conjunction_per_1k"] for item in items if item["metrics"]["conjunction_per_1k"] is not None]
        return {
            "documents": len(items),
            "cv_eligible": len(cvs),
            "sentence_cv": _distribution(cvs),
            "conjunction_per_1k": _distribution(conjs),
        }

    scenes = sorted({item["scene"] for item in active})
    required_scenes = {"docs", "public-writing", "status"}
    direct_scenes = sorted(
        {item["scene"] for item in active if item["representation_role"] == "direct"}
    )
    buckets = {
        "1000-1499": [item for item in active if 1000 <= item["han"] < 1500],
        "1500-2999": [item for item in active if 1500 <= item["han"] < 3000],
        "3000+": [item for item in active if item["han"] >= 3000],
    }
    return {
        "active": len(active),
        "withdrawn": len(records) - len(active),
        "author_groups": dict(sorted(Counter(item["author_group"] for item in active).items())),
        "source_types": dict(sorted(Counter(item["source_type"] for item in active).items())),
        "eras": dict(sorted(Counter(item["era"] for item in active).items())),
        "origin_languages": dict(
            sorted(Counter(item["origin_language"] for item in active).items())
        ),
        "representation_roles": dict(
            sorted(Counter(item["representation_role"] for item in active).items())
        ),
        "direct_scenes": direct_scenes,
        "missing_direct_scenes": sorted(required_scenes - set(direct_scenes)),
        "overall": group_report(active),
        "by_scene": {scene: group_report([item for item in active if item["scene"] == scene]) for scene in scenes},
        "by_length": {name: group_report(items) for name, items in buckets.items()},
        "documents": [
            {
                "id": item["id"],
                "scene": item["scene"],
                "genre": item["genre"],
                "era": item["era"],
                "origin_language": item["origin_language"],
                "representation_role": item["representation_role"],
                "author_group": item["author_group"],
                "source_type": item["source_type"],
                "han": item["han"],
                "sentences": item["sentences"],
                "sha256": item["sha256"],
            }
            for item in active
        ],
    }


def _fmt_stat(value):
    return "-" if value is None else f"{value:.2f}"


def print_human_report(report):
    print("# HUMAN 长文 residual 对照\n")
    print(f"active {report['active']} 篇 / withdrawn {report['withdrawn']} 篇")
    print(
        f"作者组：{report['author_groups']}；来源：{report['source_types']}；"
        f"时代：{report['eras']}；原始语言：{report['origin_languages']}\n"
        f"代表性角色：{report['representation_roles']}\n"
    )
    if report["missing_direct_scenes"]:
        print(
            "代表性门禁：未通过；direct 样本缺 "
            + ", ".join(report["missing_direct_scenes"])
            + "（proxy 只进 residual，不顶场景数）。\n"
        )
    else:
        print(f"代表性门禁：通过；direct 场景 {', '.join(report['direct_scenes'])}。\n")
    print(
        "| 分组 | 文档 | CV n | CV min | CV 中位 | CV p90 | CV max | "
        "连词 n | 连词 min | 连词中位 | 连词 p90 | 连词 max |"
    )
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    rows = [("HUMAN", report["overall"])]
    rows.extend((f"scene:{name}", stats) for name, stats in report["by_scene"].items())
    rows.extend((f"length:{name}", stats) for name, stats in report["by_length"].items())
    for name, stats in rows:
        cv = stats["sentence_cv"]
        conj = stats["conjunction_per_1k"]
        print(
            f"| {name} | {stats['documents']} | {cv['n']} | "
            f"{_fmt_stat(cv['min'])} | {_fmt_stat(cv['median'])} | "
            f"{_fmt_stat(cv['p90'])} | {_fmt_stat(cv['max'])} | "
            f"{conj['n']} | {_fmt_stat(conj['min'])} | "
            f"{_fmt_stat(conj['median'])} | {_fmt_stat(conj['p90'])} | "
            f"{_fmt_stat(conj['max'])} |"
        )

    small = []
    for name, stats in rows:
        for metric in ("sentence_cv", "conjunction_per_1k"):
            raw = stats[metric]["raw"]
            if raw:
                small.append(f"- {name} / {metric}（n={len(raw)}）：{', '.join(_fmt_stat(v) for v in raw)}")
    if small:
        print("\n样本少于 8 的分组同时列原始值：\n")
        print("\n".join(small))


def calibrate(root, human_manifest=None, benchmark_only=False):
    """在 benchmark 与可用的 HUMAN 对照语料上实测 residual 分布。

    分组：`SF-xx` 是该改的 AI 味样本，`SNF-xx` 是不该改的正常样本，两组
    天然构成对照组。`B-xx` 是 SF/SNF 的盲测副本，计入会重复污染分布，排除。

    输出每组每个指标的样本数与分位数。HUMAN 只作长文假阳性对照，
    不进入 benchmark 判分；样本不足时只报告原始值，不据此硬设阈值。
    """
    cases = parse_cases(root)
    groups = {"SF": [], "SNF": []}
    for cid, scene, quote in cases:
        prefix = cid.split("-")[0]
        if prefix not in groups:
            continue
        groups[prefix].append((cid, scene, strip_blockquote(quote).strip()))

    if not groups["SF"] or not groups["SNF"]:
        print("hard_metrics: benchmark.md 没有解析到 SF/SNF 分组，无法标定", file=sys.stderr)
        return 2

    human_records = None
    if not benchmark_only:
        manifest = Path(human_manifest) if human_manifest else root / "evals" / "human-corpus.jsonl"
        if not manifest.is_absolute():
            manifest = root / manifest
        if not manifest.exists():
            print(
                f"hard_metrics: HUMAN manifest 不存在: {manifest}；只看 benchmark 请显式传 --benchmark-only",
                file=sys.stderr,
            )
            return 2
        try:
            human_records = load_human_corpus(root, manifest)
            validate_human_cohort(human_records)
        except HumanCorpusError as exc:
            print(f"hard_metrics: {exc}", file=sys.stderr)
            return 2
        groups["HUMAN"] = [
            (record["id"], record["scene"], record["text"])
            for record in human_records
            if not record["withdrawn"]
        ]

    title = "benchmark" if benchmark_only else "benchmark + HUMAN"
    print(f"# residual 判据标定（{title}）\n")
    sample_line = f"样本：SF {len(groups['SF'])} 条（该改）/ SNF {len(groups['SNF'])} 条（不该改）"
    if "HUMAN" in groups:
        sample_line += f" / HUMAN {len(groups['HUMAN'])} 篇（人写长文对照）"
    print(sample_line)
    print("B-xx 盲测副本已排除，避免同一文本重复计入分布。\n")

    collected = {}
    scene_collected = {}
    for name, items in groups.items():
        stats = {"cv": [], "conj": [], "nom": [], "field": [], "quote": []}
        for _, scene, body in items:
            m = residual_metrics(body)
            base_scene = scene.split("/", 1)[0].strip()
            scene_stats = scene_collected.setdefault(
                (name, base_scene), {"documents": 0, "cv": [], "conj": []}
            )
            scene_stats["documents"] += 1
            if m["sentence_cv"] is not None:
                stats["cv"].append(m["sentence_cv"])
                scene_stats["cv"].append(m["sentence_cv"])
            if m["conjunction_per_1k"] is not None and m["han"] >= 80:
                stats["conj"].append(m["conjunction_per_1k"])
                scene_stats["conj"].append(m["conjunction_per_1k"])
            if name != "HUMAN":
                stats["nom"].append(m["nominalization"])
                stats["field"].append(m["metaphor_fields"])
                stats["quote"].append(m["highlight_quotes"])
        collected[name] = stats

    labels = {
        "cv": "句长变异系数（句数 ≥ 12 才计）",
        "conj": "连词密度 每千字（汉字 ≥ 80 才计）",
        "nom": "名词化命中数 每条",
        "field": "同窗口借喻场数 每条",
        "quote": "「」/『』高亮短语候选数 每条",
    }
    for key, label in labels.items():
        print(f"## {label}\n")
        print("| 组 | n | p10 | p25 | 中位 | p75 | p90 | max |")
        print("|---|---|---|---|---|---|---|---|")
        names = groups if key in {"cv", "conj"} else ("SF", "SNF")
        for name in names:
            vals = collected[name][key]
            if not vals:
                print(f"| {name} | 0 | - | - | - | - | - | - |")
                continue
            cells = " | ".join(
                "-" if v is None else f"{v:.2f}"
                for v in (
                    _percentile(vals, 0.10),
                    _percentile(vals, 0.25),
                    _percentile(vals, 0.50),
                    _percentile(vals, 0.75),
                    _percentile(vals, 0.90),
                    max(vals),
                )
            )
            print(f"| {name} | {len(vals)} | {cells} |")
        print()

    print("## 句长 CV / 连词密度按主场景\n")
    print("| 组 | 主场景 | 文档 | CV 有效 | CV 中位 | CV p90 | 连词有效 | 连词中位 | 连词 p90 | 小样本原始值 |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for name in groups:
        scenes = sorted(scene for group, scene in scene_collected if group == name)
        for scene in scenes:
            stats = scene_collected[(name, scene)]
            cv = _distribution(stats["cv"])
            conj = _distribution(stats["conj"])
            raw = []
            if cv["raw"]:
                raw.append("CV=" + ",".join(f"{value:.2f}" for value in cv["raw"]))
            if conj["raw"]:
                raw.append("连词=" + ",".join(f"{value:.2f}" for value in conj["raw"]))
            print(
                f"| {name} | {scene} | {stats['documents']} | {cv['n']} | "
                f"{_fmt_stat(cv['median'])} | {_fmt_stat(cv['p90'])} | {conj['n']} | "
                f"{_fmt_stat(conj['median'])} | {_fmt_stat(conj['p90'])} | {'；'.join(raw) or '-'} |"
            )
    print("\n样本少于 8 的场景分组列出原始值；没有同场景分离证据时不设阈值。\n")

    print("## 逐条命中（名词化 / 借喻场 / 高亮短语非零项）\n")
    for name in ("SF", "SNF"):
        items = groups[name]
        for cid, scene, body in items:
            m = residual_metrics(body)
            if m["nominalization"] or m["metaphor_fields"] >= 2 or m["highlight_quotes"]:
                print(
                    f"- {cid}（{scene.strip()}）：名词化 {m['nominalization']}"
                    f"{'（' + '、'.join(m['nominalization_samples']) + '）' if m['nominalization_samples'] else ''}"
                    f"，借喻场 {m['metaphor_fields']}"
                    f"{'（' + '、'.join(m['metaphor_samples']) + '）' if m['metaphor_samples'] else ''}"
                    f"，高亮短语候选 {m['highlight_quotes']}"
                    f"{'（' + '、'.join(m['highlight_quote_samples']) + '）' if m['highlight_quote_samples'] else ''}"
                )
    if human_records:
        print("\n")
        print_human_report(human_corpus_report(human_records))
        print("\nHUMAN 只作 residual 假阳性参照，不进 benchmark rewrite/judge，也不单凭这批小样本设产品阈值。")
    return 0


def read_text_safe(path):
    """读文件，缺文件时打印错误并退出 2（自身错误口径）。"""
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as e:
        print(f"hard_metrics: 读文件失败 {path}: {e}", file=sys.stderr)
        sys.exit(2)


def single_pair(original_path, output_path, scene=""):
    """单条对照：原文本从文件读，改后文本从文件或 stdin 读。"""
    original = read_text_safe(original_path)
    if output_path == "-":
        output_text = sys.stdin.read()
    else:
        output_text = read_text_safe(output_path)
    cid = f"{Path(original_path).name} / {Path(output_path).name}"
    res = analyze_case(cid, scene, original, output_text)
    print(summarize(res).rstrip())
    return 0


def main():
    ap = argparse.ArgumentParser(description="说人话 eval harness 硬判与 residual 统计（v2.3.1）")
    ap.add_argument("--run", metavar="DIR", help="扫批次目录（含 rewrite-*.md），输出 hard-metrics 报告")
    ap.add_argument("--pair", nargs=2, metavar=("ORIG", "OUT"), help="单条对照：原文本文件 + 改后文本文件（- 表示 stdin）")
    ap.add_argument("--stdin", metavar="ORIG", help="原文本文件，改后文本从 stdin 读")
    ap.add_argument("--report-json", action="store_true", help="支持的模式改为输出 JSON；--pair 可供 judge 输入拼接")
    ap.add_argument("--scene", metavar="SCENE", default="", help="单条模式（--pair/--stdin）的用例场景标签，如 'public-writing / long / in-place'，用于长文留存判据")
    ap.add_argument("--residual", metavar="FILE", help="对单个文本算 residual 统计量（句长 CV / 连词密度 / 名词化 / 借喻场 / 「」高亮短语），只报警不判死；- 表示 stdin")
    ap.add_argument("--calibrate", action="store_true", help="在 benchmark SF/SNF 与 HUMAN 对照语料上实测 residual 分布")
    ap.add_argument("--human-manifest", metavar="FILE", help="--calibrate 使用的 HUMAN JSONL；不传则读取 evals/human-corpus.jsonl")
    ap.add_argument("--benchmark-only", action="store_true", help="仅与 --calibrate 合用：显式跳过 HUMAN，只看 benchmark 诊断分布")
    ap.add_argument("--human-stats", metavar="FILE", help="只校验 HUMAN JSONL 并输出 residual 分布，不运行 benchmark 标定")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[2]

    primary_modes = [args.run, args.pair, args.stdin, args.residual, args.calibrate, args.human_stats]
    if sum(value is not None and value is not False for value in primary_modes) > 1:
        print("hard_metrics: --run/--pair/--stdin/--residual/--calibrate/--human-stats 只能选一种", file=sys.stderr)
        return 2

    if args.human_manifest and not args.calibrate:
        print("hard_metrics: --human-manifest 只能与 --calibrate 一起使用", file=sys.stderr)
        return 2
    if args.benchmark_only and not args.calibrate:
        print("hard_metrics: --benchmark-only 只能与 --calibrate 一起使用", file=sys.stderr)
        return 2
    if args.benchmark_only and args.human_manifest:
        print("hard_metrics: --benchmark-only 不能与 --human-manifest 同时使用", file=sys.stderr)
        return 2
    if args.report_json and args.calibrate:
        print("hard_metrics: --calibrate 暂不支持 --report-json", file=sys.stderr)
        return 2

    if args.calibrate:
        return calibrate(root, args.human_manifest, args.benchmark_only)

    if args.human_stats:
        try:
            records = load_human_corpus(root, args.human_stats)
            validate_human_cohort(records)
        except HumanCorpusError as exc:
            print(f"hard_metrics: {exc}", file=sys.stderr)
            return 2
        report = human_corpus_report(records)
        if args.report_json:
            print(json.dumps(report, ensure_ascii=False))
        else:
            print_human_report(report)
        return 0

    if args.residual:
        text = sys.stdin.read() if args.residual == "-" else read_text_safe(args.residual)
        res = residual_metrics(strip_blockquote(text))
        if args.report_json:
            print(json.dumps(res, ensure_ascii=False))
        else:
            print(f"汉字数 {res['han']}，可计句数 {res['sentences']}")
            cv = res["sentence_cv"]
            print(f"- 句长变异系数：{'句数不足 12，不判' if cv is None else cv}")
            print(
                f"- 段落：{res['paragraphs']} 段，平均 {res['han_per_paragraph']} 字 / "
                f"{res['sentences_per_paragraph']} 句，最长 {res['max_paragraph_han']} 字"
                f"（列表行 {res['list_lines']}）"
            )
            print(f"- 连词密度：{res['conjunction_per_1k']} /千字（命中 {res['conjunction_hits']} 处）")
            print(f"- 名词化：{res['nominalization']} 处 {res['nominalization_samples']}")
            print(f"- 借喻场：{res['metaphor_fields']} 套 {res['metaphor_samples']}")
            print(f"- 「」/『』高亮短语候选：{res['highlight_quotes']} 处，{res['highlight_quote_per_1k']} /千字 {res['highlight_quote_samples']}")
        return 0

    if args.run:
        sys.exit(analyze_run(root, args.run))

    if args.pair:
        if args.report_json:
            original = read_text_safe(args.pair[0])
            output_text = (
                sys.stdin.read()
                if args.pair[1] == "-"
                else read_text_safe(args.pair[1])
            )
            res = analyze_case("pair", args.scene, original, output_text)
            print(json.dumps(res, ensure_ascii=False))
            return 0
        sys.exit(single_pair(args.pair[0], args.pair[1], args.scene))

    if args.stdin:
        original = read_text_safe(args.stdin)
        res = analyze_case("stdin", args.scene, original, sys.stdin.read())
        if args.report_json:
            print(json.dumps(res, ensure_ascii=False))
        else:
            print(summarize(res).rstrip())
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
