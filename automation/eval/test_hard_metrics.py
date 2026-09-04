#!/usr/bin/env python3
"""hard_metrics HUMAN manifest 的零依赖回归测试。"""

import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).with_name("hard_metrics.py")
SPEC = importlib.util.spec_from_file_location("hard_metrics", MODULE_PATH)
hard_metrics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(hard_metrics)

CHECK_REPO_PATH = MODULE_PATH.parents[1] / "check_repo.py"
CHECK_SPEC = importlib.util.spec_from_file_location("check_repo", CHECK_REPO_PATH)
check_repo = importlib.util.module_from_spec(CHECK_SPEC)
CHECK_SPEC.loader.exec_module(check_repo)


class HumanCorpusTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "evals" / "human-corpus").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def body(self, marker="甲"):
        sentence = f"这是{marker}组作者亲手写下的一段完整叙述，句子里有具体动作、对象、时间顺序和自然停顿，没有为了测试临时拼接模型套话。"
        return "\n\n".join("".join(f"{sentence}{i}。" for i in range(5)) for _ in range(5))

    def entry(self, cid, filename, body, **overrides):
        path = self.root / "evals" / "human-corpus" / filename
        path.write_text(body, encoding="utf-8")
        data = {
            "id": cid,
            "path": path.relative_to(self.root).as_posix(),
            "scene": "public-writing",
            "genre": "essay",
            "era": "modern",
            "origin_language": "zh-original",
            "representation_role": "direct",
            "author_group": "owner-a",
            "source_type": "owner",
            "source_url": "",
            "source_revision": "",
            "source_revision_at": "",
            "source_title": "",
            "source_author": "",
            "license": "repository-owner-authorized",
            "license_url": "",
            "license_evidence_url": "",
            "modifications": "none",
            "consent_evidence": "owner approved repository redistribution on 2026-08-19",
            "written_at": "2024",
            "fixed_revision_at": "2021-01-01",
            "ai_assisted": "no",
            "ai_evidence": "written before generative AI; no model rewrite",
            "deidentified": True,
            "added_on": "2026-08-19",
            "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "withdrawn": False,
        }
        data.update(overrides)
        if data["source_type"] == "open" and not data["source_revision"]:
            data["source_revision"] = "revision-1"
        if data["source_type"] == "open" and not data["source_revision_at"]:
            data["source_revision_at"] = "2021-01-01T00:00:00Z"
        return data

    def write_manifest(self, entries):
        manifest = self.root / "evals" / "human-corpus.jsonl"
        manifest.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in entries) + "\n", encoding="utf-8")
        return manifest

    def test_valid_manifest_reports_scene_author_and_length(self):
        first = self.entry("HUMAN-01", "HUMAN-01.txt", self.body("甲"))
        second = self.entry(
            "HUMAN-02",
            "HUMAN-02.txt",
            self.body("乙"),
            scene="docs",
            genre="technical-note",
            author_group="open-b",
            source_type="open",
            source_url="https://example.org/article",
            source_title="公开文章",
            source_author="示例作者",
            license="CC BY 4.0",
            license_url="https://creativecommons.org/licenses/by/4.0/",
            license_evidence_url="https://example.org/article#license",
            consent_evidence="source page declares CC BY 4.0",
        )
        records = hard_metrics.load_human_corpus(self.root, self.write_manifest([first, second]))
        report = hard_metrics.human_corpus_report(records)

        self.assertEqual(report["active"], 2)
        self.assertEqual(report["withdrawn"], 0)
        self.assertEqual(report["overall"]["cv_eligible"], 2)
        self.assertEqual(set(report["by_scene"]), {"docs", "public-writing"})
        self.assertEqual(report["author_groups"], {"open-b": 1, "owner-a": 1})
        self.assertEqual(report["eras"], {"modern": 2})
        self.assertEqual(report["origin_languages"], {"zh-original": 2})
        self.assertEqual(report["representation_roles"], {"direct": 2})
        self.assertEqual(report["direct_scenes"], ["docs", "public-writing"])
        self.assertEqual(report["missing_direct_scenes"], ["status"])

    def test_missing_provenance_field_is_error(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body())
        item.pop("license")
        manifest = self.write_manifest([item])

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "缺字段: license"):
            hard_metrics.load_human_corpus(self.root, manifest)

    def test_unknown_manifest_field_is_error(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body(), reviewer_note="不在合同里")

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "未定义字段: reviewer_note"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_hash_mismatch_is_error(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body(), sha256="0" * 64)

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "sha256 不匹配"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_open_source_needs_verifiable_url(self):
        item = self.entry(
            "HUMAN-01",
            "HUMAN-01.txt",
            self.body(),
            source_type="open",
            source_title="公开文章",
            source_author="示例作者",
            license="CC BY 4.0",
            license_url="https://creativecommons.org/licenses/by/4.0/",
            license_evidence_url="https://example.org/article#license",
            consent_evidence="source page declares CC BY 4.0",
        )

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "open 条目必须给出"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_open_source_rejects_non_redistributable_license(self):
        item = self.entry(
            "HUMAN-01",
            "HUMAN-01.txt",
            self.body(),
            source_type="open",
            source_url="https://example.org/article",
            source_title="公开文章",
            source_author="示例作者",
            license="all-rights-reserved",
            consent_evidence="none",
        )

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "license 不在允许集合"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_open_source_accepts_public_domain_with_canonical_evidence(self):
        item = self.entry(
            "HUMAN-01",
            "HUMAN-01.txt",
            self.body(),
            source_type="open",
            source_url="https://example.org/work?oldid=123",
            source_title="历史作品",
            source_author="示例作者",
            license="Public Domain",
            license_url="https://creativecommons.org/publicdomain/mark/1.0/",
            license_evidence_url="https://example.org/work?oldid=123",
            consent_evidence="source page declares Public Domain",
        )

        records = hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

        self.assertEqual(records[0]["license"], "Public Domain")

    def test_open_source_requires_license_and_ai_evidence(self):
        missing_license_evidence = self.entry(
            "HUMAN-01",
            "HUMAN-01.txt",
            self.body(),
            source_type="open",
            source_url="https://example.org/article",
            source_title="公开文章",
            source_author="示例作者",
            license="CC BY-SA 4.0",
            license_url="https://creativecommons.org/licenses/by-sa/4.0/",
            consent_evidence="source page declares CC BY-SA 4.0",
        )
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "license_evidence_url"):
            hard_metrics.load_human_corpus(
                self.root, self.write_manifest([missing_license_evidence])
            )

        missing_ai_evidence = dict(missing_license_evidence)
        missing_ai_evidence.update(
            {
                "license_evidence_url": "https://example.org/article#license",
                "ai_evidence": "",
            }
        )
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "ai_evidence"):
            hard_metrics.load_human_corpus(
                self.root, self.write_manifest([missing_ai_evidence])
            )

        generic_deed_only = dict(missing_ai_evidence)
        generic_deed_only.update(
            {
                "ai_evidence": "written before generative AI; no model rewrite",
                "license_evidence_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            }
        )
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "逐篇作品证据"):
            hard_metrics.load_human_corpus(
                self.root, self.write_manifest([generic_deed_only])
            )

    def test_open_source_rejects_fake_cc_version_and_consent_placeholder(self):
        fake_version = self.entry(
            "HUMAN-01",
            "HUMAN-01.txt",
            self.body(),
            source_type="open",
            source_url="https://example.org/article",
            source_title="公开文章",
            source_author="示例作者",
            license="CC BY 9.9",
            consent_evidence="source page declares CC BY 9.9",
        )
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "license 不在允许集合"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([fake_version]))

        placeholder = self.entry(
            "HUMAN-01",
            "HUMAN-01.txt",
            self.body(),
            source_type="open",
            source_url="https://example.org/article",
            source_title="公开文章",
            source_author="示例作者",
            license="CC BY 4.0",
            license_url="https://creativecommons.org/licenses/by/4.0/",
            license_evidence_url="https://example.org/article#license",
            consent_evidence="pending approval",
        )
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "必须逐字对应"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([placeholder]))

    def test_active_entry_requires_completed_privacy_check(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body(), deidentified=False)

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "deidentified=true"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_open_source_requires_complete_attribution(self):
        missing_author = self.entry(
            "HUMAN-01",
            "HUMAN-01.txt",
            self.body(),
            source_type="open",
            source_url="https://example.org/article",
            source_title="公开文章",
            source_author="",
            license="CC BY 4.0",
            license_url="https://creativecommons.org/licenses/by/4.0/",
            license_evidence_url="https://example.org/article#license",
            consent_evidence="source page declares CC BY 4.0",
        )
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "source_title/source_author"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([missing_author]))

        wrong_license_url = dict(missing_author)
        wrong_license_url.update({"source_author": "示例作者", "license_url": "https://example.org/license"})
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "license_url 必须是"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([wrong_license_url]))

        missing_change_notice = dict(wrong_license_url)
        missing_change_notice.update({
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "modifications": "",
        })
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "modifications"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([missing_change_notice]))

    def test_body_path_must_stay_in_corpus_directory(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body())
        item["path"] = "evals/not-corpus.txt"

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "path 必须精确为"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_invalid_path_is_wrapped_as_corpus_error(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body())
        item["path"] = "evals/human-corpus/bad\0path.txt"

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "path 无法解析"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_corpus_directory_cannot_be_symlink(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body())
        corpus = self.root / "evals" / "human-corpus"
        target = self.root / "elsewhere"
        target.mkdir()
        (target / "HUMAN-01.txt").write_text(self.body(), encoding="utf-8")
        (corpus / "HUMAN-01.txt").unlink()
        corpus.rmdir()
        corpus.symlink_to(target, target_is_directory=True)

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "目录及其父目录不能是 symlink"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_duplicate_id_is_error(self):
        first = self.entry("HUMAN-01", "HUMAN-01.txt", self.body("甲"))
        second = self.entry("HUMAN-01", "HUMAN-02.txt", self.body("乙"), author_group="owner-b")

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "重复 id"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([first, second]))

    def test_too_short_or_too_few_sentences_is_error(self):
        short = "这是一篇太短的文字。" * 12
        item = self.entry("HUMAN-01", "HUMAN-01.txt", short)

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "低于 1000"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_long_single_sentence_hits_sentence_gate(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", "汉" * 1001 + "。")

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "低于 12"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_duplicate_body_hash_is_error(self):
        body = self.body()
        first = self.entry("HUMAN-01", "HUMAN-01.txt", body)
        second = self.entry("HUMAN-02", "HUMAN-02.txt", body, author_group="owner-b")

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "正文重复"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([first, second]))

    def test_unregistered_body_file_is_error(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body())
        (self.root / "evals" / "human-corpus" / "HUMAN-99.txt").write_text(
            self.body("未登记"), encoding="utf-8"
        )

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "manifest 未登记文件: HUMAN-99.txt"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_release_cohort_requires_eight_open_sources_and_representative_groups(self):
        owner_only = [
            self.entry(f"HUMAN-{i:02d}", f"HUMAN-{i:02d}.txt", self.body(str(i)))
            for i in range(1, 9)
        ]
        records = hard_metrics.load_human_corpus(self.root, self.write_manifest(owner_only))
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "必须全部来自可核验公开来源"):
            hard_metrics.validate_human_cohort(records)

        open_cohort = []
        for i in range(1, 9):
            overrides = {
                "scene": ("docs", "public-writing", "status")[i % 3],
                "era": "historical" if i <= 3 else "modern",
                "origin_language": "translated-from-en" if i <= 2 else "zh-original",
                "source_type": "open",
                "source_url": f"https://example.org/article-{i}",
                "source_title": f"公开文章 {i}",
                "source_author": f"示例作者 {i}",
                "license": "CC BY-SA 4.0",
                "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
                "license_evidence_url": f"https://example.org/article-{i}#license",
                "consent_evidence": "source page declares CC BY-SA 4.0",
                "fixed_revision_at": "2021-01-01",
                "author_group": f"open-{i % 3}",
            }
            open_cohort.append(self.entry(f"HUMAN-{i:02d}", f"HUMAN-{i:02d}.txt", self.body(f"m{i}"), **overrides))
        valid = hard_metrics.load_human_corpus(self.root, self.write_manifest(open_cohort))
        self.assertEqual(len(hard_metrics.validate_human_cohort(valid)), 8)

    def test_mediawiki_revision_and_real_date_are_required(self):
        item = self.entry(
            "HUMAN-01",
            "HUMAN-01.txt",
            self.body(),
            source_type="open",
            source_url="https://zh.wikinews.org/w/index.php?title=Example&oldid=123",
            source_revision="124",
            source_title="公开文章",
            source_author="示例作者",
            license="CC BY 2.5",
            license_url="https://creativecommons.org/licenses/by/2.5/",
            license_evidence_url="https://zh.wikinews.org/w/index.php?title=Wikinews%3A%E7%89%88%E6%9D%83%E4%BF%A1%E6%81%AF&oldid=262628",
            consent_evidence="source page declares CC BY 2.5",
        )
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "oldid 必须与 source_revision 一致"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

        item["source_revision"] = "123"
        item["fixed_revision_at"] = "2021-99-99"
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "fixed_revision_at 不是有效日期"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

        item["fixed_revision_at"] = "2021-01-02"
        item["source_revision_at"] = "2021-01-01T23:59:59Z"
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "必须与 source_revision_at"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

        item["fixed_revision_at"] = "2021-01-01"
        item["license_evidence_url"] = "https://zh.wikinews.org/w/index.php?title=Example&oldid=262628"
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "固定版权政策 revision"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

        item["license_evidence_url"] = "https://zh.wikinews.org/w/index.php?title=Wikinews%3A%E7%89%88%E6%9D%83%E4%BF%A1%E6%81%AF&oldid=262628"
        item["source_revision"] = "abc"
        item["source_url"] = "https://zh.wikinews.org/w/index.php?title=Example&oldid=abc"
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "source_revision 必须是正整数"):
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

    def test_release_cohort_rejects_era_imbalance_or_translation_dominance(self):
        base = [
            {
                "withdrawn": False,
                "source_type": "open",
                "author_group": f"author-{i % 3}",
                "scene": ("docs", "public-writing", "status")[i % 3],
                "era": "historical" if i < 3 else "modern",
                "origin_language": "zh-original",
            }
            for i in range(8)
        ]

        historical_only = [dict(record, era="historical") for record in base]
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "现代文本至少需要 3 篇"):
            hard_metrics.validate_human_cohort(historical_only)

        translation_heavy = [
            dict(record, origin_language="translated-from-en" if i < 3 else "zh-original")
            for i, record in enumerate(base)
        ]
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "翻译文本不得超过 active cohort 的三分之一"):
            hard_metrics.validate_human_cohort(translation_heavy)

    def test_release_cohort_rejects_too_few_documents(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body())
        records = hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "8–12"):
            hard_metrics.validate_human_cohort(records)

    def test_release_cohort_rejects_too_many_documents(self):
        records = [{"withdrawn": False} for _ in range(13)]

        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "8–12"):
            hard_metrics.validate_human_cohort(records)

    def test_release_cohort_rejects_narrow_author_or_scene_coverage(self):
        base = [
            {
                "withdrawn": False,
                "source_type": "open",
                "era": "historical" if i < 3 else "modern",
                "origin_language": "zh-original",
                "author_group": f"author-{i % 3}",
                "scene": ("docs", "public-writing", "status")[i % 3],
                "representation_role": "direct",
            }
            for i in range(8)
        ]

        narrow_authors = [dict(record, author_group="same-author") for record in base]
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "至少需要 3 个作者组"):
            hard_metrics.validate_human_cohort(narrow_authors)

        missing_status = [
            dict(record, scene="docs" if record["scene"] == "status" else record["scene"])
            for record in base
        ]
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "缺少代表性场景: status"):
            hard_metrics.validate_human_representativeness(missing_status)

        proxy_status = [
            dict(record, representation_role="proxy" if record["scene"] == "status" else "direct")
            for record in base
        ]
        with self.assertRaisesRegex(hard_metrics.HumanCorpusError, "direct 样本缺少代表性场景: status"):
            hard_metrics.validate_human_representativeness(proxy_status)

    def test_human_body_cannot_reappear_anonymously_in_benchmark(self):
        records = [{"id": "HUMAN-01", "text": "第一段。\n第二段。", "manifest_line": 1}]
        cases = [("SF-99", "public-writing", "> 第一段。  \n> 第二段。")]

        duplicates = check_repo.human_benchmark_duplicates(records, cases, hard_metrics.strip_blockquote)

        self.assertEqual([(item[0]["id"], item[1]) for item in duplicates], [("HUMAN-01", ["SF-99"])])

    def test_withdrawn_entry_keeps_id_but_needs_no_body(self):
        active = self.entry("HUMAN-01", "HUMAN-01.txt", self.body())
        withdrawn = dict(active)
        withdrawn.update({
            "id": "HUMAN-02",
            "path": "",
            "sha256": "",
            "withdrawn": True,
            "consent_evidence": "withdrawn by author on 2026-08-20",
        })
        report = hard_metrics.human_corpus_report(
            hard_metrics.load_human_corpus(self.root, self.write_manifest([active, withdrawn]))
        )

        self.assertEqual(report["active"], 1)
        self.assertEqual(report["withdrawn"], 1)

    def test_text_report_includes_required_distribution_bounds(self):
        item = self.entry("HUMAN-01", "HUMAN-01.txt", self.body())
        report = hard_metrics.human_corpus_report(
            hard_metrics.load_human_corpus(self.root, self.write_manifest([item]))
        )
        stdout = io.StringIO()

        with mock.patch("sys.stdout", stdout):
            hard_metrics.print_human_report(report)

        rendered = stdout.getvalue()
        self.assertIn("| CV n | CV min | CV 中位 | CV p90 | CV max |", rendered)
        self.assertIn("| 连词 n | 连词 min | 连词中位 | 连词 p90 | 连词 max |", rendered)

    def test_cli_rejects_multiple_primary_modes(self):
        stderr = io.StringIO()
        with mock.patch("sys.argv", ["hard_metrics.py", "--calibrate", "--human-stats", "missing.jsonl"]):
            with mock.patch("sys.stderr", stderr):
                code = hard_metrics.main()

        self.assertEqual(code, 2)
        self.assertIn("只能选一种", stderr.getvalue())

    def test_human_stats_cli_accepts_valid_release_cohort(self):
        entries = []
        for i in range(1, 9):
            overrides = {}
            if i >= 5:
                overrides = {
                    "source_type": "open",
                    "era": "historical" if i <= 3 else "modern",
                    "origin_language": "translated-from-en" if i <= 2 else "zh-original",
                    "source_url": f"https://example.org/article-{i}",
                    "source_title": f"公开文章 {i}",
                    "source_author": f"示例作者 {i}",
                    "license": "CC BY 4.0",
                    "license_url": "https://creativecommons.org/licenses/by/4.0/",
                    "license_evidence_url": f"https://example.org/article-{i}#license",
                    "consent_evidence": "source page declares CC BY 4.0",
                    "fixed_revision_at": "2021-01-01",
                    "author_group": f"open-{i % 3}",
                }
            else:
                overrides = {
                    "scene": ("docs", "public-writing", "status")[i % 3],
                    "source_type": "open",
                    "era": "historical" if i <= 3 else "modern",
                    "origin_language": "translated-from-en" if i <= 2 else "zh-original",
                    "source_url": f"https://example.org/article-{i}",
                    "source_title": f"公开文章 {i}",
                    "source_author": f"示例作者 {i}",
                    "license": "CC BY 4.0",
                    "license_url": "https://creativecommons.org/licenses/by/4.0/",
                    "license_evidence_url": f"https://example.org/article-{i}#license",
                    "consent_evidence": "source page declares CC BY 4.0",
                    "fixed_revision_at": "2021-01-01",
                    "author_group": f"open-{i % 3}",
                }
            entries.append(
                self.entry(
                    f"HUMAN-{i:02d}",
                    f"HUMAN-{i:02d}.txt",
                    self.body(f"cli{i}"),
                    **overrides,
                )
            )
        manifest = self.write_manifest(entries)
        stdout = io.StringIO()

        fake_module_path = self.root / "automation" / "eval" / "hard_metrics.py"
        with mock.patch.object(hard_metrics, "__file__", str(fake_module_path)):
            with mock.patch("sys.argv", ["hard_metrics.py", "--human-stats", str(manifest)]):
                with mock.patch("sys.stdout", stdout):
                    code = hard_metrics.main()

        self.assertEqual(code, 0)
        self.assertIn("active 8 篇", stdout.getvalue())
        self.assertIn("| CV n | CV min | CV 中位 | CV p90 | CV max |", stdout.getvalue())

    def test_plugin_versions_must_match(self):
        plugin_dir = self.root / ".claude-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "plugin.json").write_text(
            json.dumps({"name": "shuorenhua", "version": "2.3.1"}), encoding="utf-8"
        )
        (plugin_dir / "marketplace.json").write_text(
            json.dumps({
                "metadata": {"version": "2.3.0"},
                "plugins": [{"name": "shuorenhua", "version": "2.3.1"}],
            }),
            encoding="utf-8",
        )
        issues = []

        with mock.patch.object(check_repo, "ROOT", self.root):
            check_repo.check_meta(issues)

        self.assertTrue(any("版本不一致" in issue for issue in issues))

    def test_plugin_metadata_schema_errors_are_reported(self):
        plugin_dir = self.root / ".claude-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "plugin.json").write_text(
            json.dumps({"name": "shuorenhua", "version": "2.3.1"}), encoding="utf-8"
        )
        (plugin_dir / "marketplace.json").write_text(
            json.dumps({"metadata": None, "plugins": []}), encoding="utf-8"
        )
        issues = []

        with mock.patch.object(check_repo, "ROOT", self.root):
            check_repo.check_meta(issues)

        self.assertTrue(any("metadata 必须是 object" in issue for issue in issues))

    def test_plugin_top_level_and_name_schema_errors_are_reported(self):
        plugin_dir = self.root / ".claude-plugin"
        plugin_dir.mkdir()
        plugin_path = plugin_dir / "plugin.json"
        marketplace_path = plugin_dir / "marketplace.json"
        marketplace_path.write_text(
            json.dumps({"metadata": {"version": "2.3.1"}, "plugins": []}), encoding="utf-8"
        )

        plugin_path.write_text("[]", encoding="utf-8")
        top_level_issues = []
        with mock.patch.object(check_repo, "ROOT", self.root):
            check_repo.check_meta(top_level_issues)
        self.assertTrue(any("顶层 JSON 必须是 object" in issue for issue in top_level_issues))

        plugin_path.write_text("null", encoding="utf-8")
        null_issues = []
        with mock.patch.object(check_repo, "ROOT", self.root):
            check_repo.check_meta(null_issues)
        self.assertTrue(any("顶层 JSON 必须是 object" in issue for issue in null_issues))

        plugin_path.write_text(json.dumps({"version": "2.3.1"}), encoding="utf-8")
        name_issues = []
        with mock.patch.object(check_repo, "ROOT", self.root):
            check_repo.check_meta(name_issues)
        self.assertTrue(any("name 必须是非空字符串" in issue for issue in name_issues))

    def test_cli_rejects_json_calibration_until_implemented(self):
        stderr = io.StringIO()
        with mock.patch("sys.argv", ["hard_metrics.py", "--calibrate", "--report-json"]):
            with mock.patch("sys.stderr", stderr):
                code = hard_metrics.main()

        self.assertEqual(code, 2)
        self.assertIn("暂不支持", stderr.getvalue())

    def test_extract_blocks_preserves_headings_inside_result(self):
        output = """## B-01

处理结果：
## v1.8.0 Release Highlights

- 保留版本号。

## B-02

处理结果：
## FAQ

先回答问题。
"""

        blocks = hard_metrics.extract_blocks(output)

        self.assertIn("## v1.8.0 Release Highlights", blocks["B-01"])
        self.assertIn("## FAQ", blocks["B-02"])
        self.assertNotIn("B-02", blocks["B-01"])


class ParagraphMetricsTests(unittest.TestCase):
    def test_counts_paragraphs_and_reports_longest(self):
        text = "第一段写了两句话。这是第二句。\n\n第二段只有一句。"

        m = hard_metrics.paragraph_metrics(text)

        self.assertEqual(m["paragraphs"], 2)
        self.assertEqual(m["max_paragraph_han"], hard_metrics.han_count("第一段写了两句话这是第二句"))
        self.assertEqual(m["sentences_per_paragraph"], 1.5)

    def test_single_dense_paragraph_is_one_paragraph(self):
        text = "".join(f"这是第{i}句话，写得不算短，但中间没有任何空行。" for i in range(12))

        m = hard_metrics.paragraph_metrics(text)

        self.assertEqual(m["paragraphs"], 1)
        self.assertEqual(m["han_per_paragraph"], float(m["max_paragraph_han"]))

    def test_blocks_without_han_are_not_paragraphs(self):
        text = "正文一段。\n\n   \n\n又一段正文。"

        self.assertEqual(hard_metrics.paragraph_metrics(text)["paragraphs"], 2)

    def test_empty_text_reports_zero_without_crashing(self):
        m = hard_metrics.paragraph_metrics("\n\n   \n")

        self.assertEqual(m["paragraphs"], 0)
        self.assertIsNone(m["han_per_paragraph"])
        self.assertIsNone(m["max_paragraph_han"])

    def test_list_lines_are_counted_separately(self):
        text = "开头一段。\n\n- 第一条\n- 第二条\n3. 第三条\n"

        m = hard_metrics.paragraph_metrics(text)

        self.assertEqual(m["list_lines"], 3)
        self.assertEqual(m["paragraphs"], 2)

    def test_residual_metrics_masks_code_block_out_of_paragraph_count(self):
        text = "说明文字一段。\n\n```\ncode_line_without_han()\n```\n\n收尾一段。"

        res = hard_metrics.residual_metrics(text)

        self.assertEqual(res["paragraphs"], 2)
        self.assertEqual(res["list_lines"], 0)


if __name__ == "__main__":
    unittest.main()
