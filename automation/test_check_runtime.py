"""运行包边界与数据计数检查；不依赖项目文案的固定段落。"""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check_repo


class RuntimePackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "references").mkdir()
        (self.root / "SKILL.md").write_text("# Skill\n[说明](references/guide.md)\n")
        (self.root / "references/guide.md").write_text("[返回](../SKILL.md)\n[官网](https://example.com/x)\n")
        self.files = ["SKILL.md", "references/guide.md"]

    def issues(self):
        (self.root / "runtime-files.json").write_text(json.dumps({"files": self.files}))
        issues = []
        check_repo.check_runtime_manifest(issues, self.root)
        return issues

    def test_closed_package_passes_without_loading_development_skills(self):
        (self.root / "tasks/history").mkdir(parents=True)
        (self.root / "tasks/history/SKILL.md").write_text("Historical working copy")
        self.assertEqual(self.issues(), [])

    def test_missing_manifest_file_fails(self):
        (self.root / "references/guide.md").unlink()
        self.assertTrue(any("文件不存在" in issue for issue in self.issues()))

    def test_traversal_and_development_entries_fail(self):
        for forbidden in ("../outside.md", "/absolute.md", "evals/SKILL.md", "tasks/SKILL.md", "references/SKILL.md"):
            with self.subTest(path=forbidden):
                self.files = ["SKILL.md", "references/guide.md", forbidden]
                self.assertTrue(self.issues())

    def test_unbundled_reference_link_fails_even_when_file_exists(self):
        (self.root / "README.md").write_text("Development document")
        (self.root / "references/guide.md").write_text("[更多](../README.md)\n")
        self.assertTrue(any("没有闭合" in issue for issue in self.issues()))

    def test_duplicate_manifest_entry_fails(self):
        self.files.append("references/guide.md")
        self.assertTrue(any("重复文件" in issue for issue in self.issues()))

    def test_unlisted_reference_file_fails(self):
        (self.root / "references/forgotten.md").write_text("Forgotten file")
        self.assertTrue(any("未列入" in issue for issue in self.issues()))

    def test_symlink_outside_repo_fails(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "guide.md"
            target.write_text("External")
            (self.root / "references/guide.md").unlink()
            (self.root / "references/guide.md").symlink_to(target)
            self.assertTrue(any("越出仓库" in issue for issue in self.issues()))

    def test_empty_manifest_and_missing_entry_fail(self):
        for files in ([], ["references/guide.md"]):
            with self.subTest(files=files):
                self.files = files
                self.assertTrue(self.issues())

    def test_entry_cannot_alias_internal_history(self):
        (self.root / "evals").mkdir()
        (self.root / "evals/history.txt").write_text("Historical instructions")
        (self.root / "SKILL.md").unlink()
        (self.root / "SKILL.md").symlink_to("evals/history.txt")
        self.assertTrue(any("不能通过符号链接" in issue for issue in self.issues()))

    def test_reference_style_links_are_checked(self):
        (self.root / "references/guide.md").write_text("[更多][details]\n\n[details]: ../README.md\n")
        self.assertTrue(any("没有闭合" in issue for issue in self.issues()))

    def test_unreadable_markdown_encoding_fails(self):
        (self.root / "references/guide.md").write_bytes(b"\xff")
        self.assertTrue(any("无法读取" in issue for issue in self.issues()))


class CountsTests(unittest.TestCase):
    def test_readme_prose_is_free_but_declared_badge_counts_must_match(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "evals").mkdir()
            (root / "evals/benchmark.md").write_text("### SF-01 | docs | 示例\n### SNF-01 | docs | 示例\n")
            (root / "evals/real-samples.md").write_text("### RS-01 任意文案\n")
            (root / "README.md").write_text("任意简短介绍，无固定标题或表格。")
            with patch.object(check_repo, "ROOT", root):
                issues = []
                check_repo.check_counts(issues)
                self.assertEqual(issues, [])
                (root / "README.md").write_text('![Benchmark](https://img.shields.io/badge/benchmark-99%20cases-blue)')
                check_repo.check_counts(issues)
                self.assertTrue(any("计数应为 2" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
