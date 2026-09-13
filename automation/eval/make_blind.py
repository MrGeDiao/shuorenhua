#!/usr/bin/env python3
"""从 evals/benchmark.md 生成盲测输入 benchmark-blind.md 和映射表 benchmark-map.md。

为什么要盲测（2026-07-11 deep review 结论）：benchmark.md 每条用例自带
`预期` / `理由`，等于把答案递给被测模型；编号前缀（SF / SNF）和标题里的
病灶描述本身也暴露「该改还是不该改」。实跑要测的是规则在陌生文本上的
行为，所以被测模型只能看到：匿名编号 + 场景 + 原文，顺序按固定种子打乱。

用法：在仓库根目录运行 `python3 automation/eval/make_blind.py`。
benchmark.md 用例增删后必须重跑本脚本；手改生成文件无效，会被覆盖。
"""

import random
import re
import sys
from pathlib import Path

# 固定种子保证同一用例集合可复现；换种子或增删用例都会重排盲测编号，
# 跨版本批次必须查当版 benchmark-map.md，不能直接沿用旧 B 编号
SEED = 20260711

# rubric 标签白名单：SF 必须是预期/Expected，SNF 必须是理由/Reason，
# 其他粗体标签视为格式漂移，宁可挂掉也不静默生成错误盲测集
RUBRIC_LABELS = {"SF": ("预期", "Expected"), "SNF": ("理由", "Reason")}


def parse_cases(text):
    """切出每条用例：(编号, 场景, 输入引用块)。预期/理由之前只允许引用行。"""
    parts = re.split(r"(?m)^### (?=(?:SF|SNF)-\d)", text)
    cases = []
    for chunk in parts[1:]:
        lines = chunk.splitlines()
        fields = [f.strip() for f in lines[0].split("|")]
        if len(fields) != 3:
            sys.exit(f"标题行不是「编号 | 场景 | 说明」三段式: {lines[0]!r}")
        cid, scene, _title = fields
        kind = cid.split("-")[0]
        input_lines = []
        rubric_seen = False
        for ln in lines[1:]:
            if ln.startswith("**"):
                m = re.match(r"\*\*([^*]+)\*\*", ln)
                label = m.group(1) if m else None
                if label not in RUBRIC_LABELS[kind]:
                    sys.exit(f"{cid}: rubric 标签 {label!r} 不在 {kind} 允许集 {RUBRIC_LABELS[kind]} 内，benchmark 格式漂移或用例写错")
                rubric_seen = True
                break
            if ln.startswith("### ") or ln.startswith("## "):
                break
            if ln.startswith(">") or not ln.strip():
                input_lines.append(ln)
            else:
                sys.exit(f"{cid}: 预期/理由之前出现非引用行，人工确认格式后再调脚本: {ln!r}")
        quote = "\n".join(input_lines).strip("\n")
        if not quote:
            sys.exit(f"{cid}: 没有解析到输入引用块")
        if not rubric_seen:
            sys.exit(f"{cid}: 没有找到预期/理由字段")
        cases.append((cid, scene, quote))
    ids = [c[0] for c in cases]
    if len(ids) != len(set(ids)):
        sys.exit("用例编号有重复")
    return cases


def render_outputs(root):
    """生成两份盲测文件的文本，不写盘。"""
    src = root / "evals" / "benchmark.md"
    cases = parse_cases(src.read_text(encoding="utf-8"))

    sf = sum(1 for c in cases if c[0].startswith("SF-"))
    snf = len(cases) - sf

    order = list(range(len(cases)))
    random.Random(SEED).shuffle(order)

    # 盲测文件头保持极简：不提生成来源、种子、映射表和 benchmark.md——
    # 隔离目前只靠 prompt 纪律，不给被测模型「答案文件就在旁边」的提示
    # 盲测号固定以 2 位为最小宽度：B-01…B-99，跨过 100 后自然变成 B-100。
    # hard_metrics.batch_expected_ids() 和历史批次名都使用同一格式；如果按总数
    # 把全部旧编号扩成 3 位，B-001 会与批次期望的 B-01 失配。
    width = 2
    blind = [
        "# 盲测输入 | Blind Benchmark Input",
        "",
        f"> 共 {len(cases)} 条。按「说人话」规则处理每条用例的引用块文本：该改就改，不改时返回完整原文。",
        "> 输出合同见 `automation/eval/rewrite-prompt.md`。",
        "",
    ]
    maprows = [
        "# 盲测映射表 | Blind Map",
        "",
        f"> 由 `automation/eval/make_blind.py` 从 `benchmark.md` 生成（种子 {SEED}）；本文件和 `benchmark-blind.md` 都是生成物，手改无效，重跑脚本会覆盖。",
        "> judge 判分前用本表把盲测编号映射回 `benchmark.md` 用例编号。",
        "> ⚠️ 被测模型禁止读取本文件。",
        f"> 共 {len(cases)} 条 = {sf} SF + {snf} SNF。",
        "",
        "| 盲测编号 | 用例编号 | 场景 |",
        "|----------|----------|------|",
    ]
    for i, idx in enumerate(order, 1):
        cid, scene, quote = cases[idx]
        bid = f"B-{i:0{width}d}"
        blind += [f"### {bid} | {scene}", "", quote, ""]
        maprows.append(f"| {bid} | {cid} | {scene} |")

    return cases, "\n".join(blind).rstrip() + "\n", "\n".join(maprows) + "\n"


def main():
    args = sys.argv[1:]
    if args not in ([], ["--check"]):
        sys.exit("用法：python3 automation/eval/make_blind.py [--check]")

    root = Path(__file__).resolve().parents[2]
    cases, blind, mapping = render_outputs(root)
    outputs = {
        root / "evals" / "benchmark-blind.md": blind,
        root / "evals" / "benchmark-map.md": mapping,
    }
    if args == ["--check"]:
        stale = [
            path.relative_to(root).as_posix()
            for path, expected in outputs.items()
            if not path.is_file() or path.read_bytes() != expected.encode("utf-8")
        ]
        if stale:
            sys.exit(
                "盲测生成物陈旧或缺失，重跑 python3 automation/eval/make_blind.py："
                + ", ".join(stale)
            )
        print(f"盲测生成物检查 OK：{len(cases)} 条")
        return

    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
    sf = sum(1 for c in cases if c[0].startswith("SF-"))
    snf = len(cases) - sf
    print(f"生成完成：{len(cases)} 条（{sf} SF + {snf} SNF）→ evals/benchmark-blind.md, evals/benchmark-map.md")


if __name__ == "__main__":
    main()
