"""仓库一致性检查的纯函数测试；不依赖仓库当前文案或文件系统。"""
import unittest

import check_repo


class LineNumberTests(unittest.TestCase):
    def test_newline_belongs_to_preceding_line(self):
        text = "甲\n乙\n"
        for offset, expected in ((0, 1), (1, 1), (2, 2), (3, 2), (4, 3)):
            with self.subTest(offset=offset):
                self.assertEqual(check_repo.line_number(text, offset), expected)

    def test_empty_text_and_offsets_beyond_end(self):
        self.assertEqual(check_repo.line_number("", 0), 1)
        self.assertEqual(check_repo.line_number("a\nb", 100), 2)

    def test_negative_offsets_follow_string_count_bounds(self):
        self.assertEqual(check_repo.line_number("a\nb\n", -1), 2)
        self.assertEqual(check_repo.line_number("a\nb\n", -100), 1)

    def test_only_line_feed_counts(self):
        self.assertEqual(check_repo.line_number("a\rb\r\nc", 7), 2)


class StripInlineCodeTests(unittest.TestCase):
    def test_removes_multiple_spans_without_changing_surrounding_text(self):
        self.assertEqual(check_repo.strip_inline_code("前 `code` 中 ``two`` 后"), "前  中  后")

    def test_empty_and_plain_text_are_unchanged(self):
        for text in ("", "普通文本", "unclosed `code"):
            with self.subTest(text=text):
                self.assertEqual(check_repo.strip_inline_code(text), text)

    def test_empty_span_is_removed(self):
        self.assertEqual(check_repo.strip_inline_code("a``b"), "ab")

    def test_matching_is_regex_based_rather_than_markdown_parsing(self):
        self.assertEqual(check_repo.strip_inline_code("``code```"), "`")
        self.assertEqual(check_repo.strip_inline_code("`a\nb`"), "")


class LocalTargetTests(unittest.TestCase):
    def test_local_paths_keep_relative_components(self):
        for target in ("guide.md", "../README.md", "/absolute.md", "./guide.md"):
            with self.subTest(target=target):
                self.assertEqual(check_repo.local_target(target), target)

    def test_strips_whitespace_angle_brackets_query_and_fragment(self):
        self.assertEqual(check_repo.local_target("  <docs/a b.md?view=1#part> \n"), "docs/a b.md")

    def test_decodes_html_before_removing_query(self):
        self.assertEqual(check_repo.local_target("docs/a&#32;b.md?x=1&amp;y=2"), "docs/a b.md")

    def test_percent_decoding_happens_after_query_and_fragment_removal(self):
        self.assertEqual(check_repo.local_target("a%23b%3Fc%20d.md#section"), "a#b?c d.md")
        self.assertEqual(check_repo.local_target("%23local"), "#local")
        self.assertEqual(check_repo.local_target("a+b.md"), "a+b.md")

    def test_empty_and_nonlocal_targets_are_ignored(self):
        for target in ("", " \t", "<>", "#part", "?query", "//example.com/a",
                       "https://example.com", "MAILTO:a@example.com", "git+ssh:x",
                       "custom.scheme-1:value", "C:/file.md", "&#35;part"):
            with self.subTest(target=target):
                self.assertIsNone(check_repo.local_target(target))

    def test_invalid_scheme_prefix_is_kept(self):
        for target in ("1scheme:value", "./file:name", "a%ZZ.md"):
            with self.subTest(target=target):
                self.assertEqual(check_repo.local_target(target), target)


class SafeRelativePathTests(unittest.TestCase):
    def test_accepts_nonempty_posix_components(self):
        for value in ("SKILL.md", "references/说明.md", ".hidden/file", "a/.../b", "a b", " "):
            with self.subTest(value=value):
                self.assertTrue(check_repo.safe_relative_path(value))

    def test_rejects_empty_or_nonstring_values(self):
        for value in ("", None, 0, False, [], {}, b"file.md"):
            with self.subTest(value=value):
                self.assertFalse(check_repo.safe_relative_path(value))

    def test_rejects_absolute_windows_and_colon_paths(self):
        for value in ("/file", "//host/file", "a\\b", "C:/file", "a/b:c"):
            with self.subTest(value=value):
                self.assertFalse(check_repo.safe_relative_path(value))

    def test_rejects_empty_dot_and_parent_components_before_normalization(self):
        for value in (".", "..", "./a", "a/.", "../a", "a/../b", "a//b", "a/"):
            with self.subTest(value=value):
                self.assertFalse(check_repo.safe_relative_path(value))


class CodeSpanTermsTests(unittest.TestCase):
    def test_splits_slashes_trims_terms_and_preserves_order_and_duplicates(self):
        self.assertEqual(check_repo.code_span_terms("正文 ` 甲 / 乙 /甲 ` 与 `丙`"),
                         ["甲", "乙", "甲", "丙"])

    def test_empty_segments_and_whitespace_terms_are_dropped(self):
        self.assertEqual(check_repo.code_span_terms("`/ a // \t / b /`"), ["a", "b"])
        self.assertEqual(check_repo.code_span_terms("` / / `"), [])

    def test_no_complete_nonempty_span_returns_no_terms(self):
        for text in ("", "普通文本 / terms", "`unclosed", "``"):
            with self.subTest(text=text):
                self.assertEqual(check_repo.code_span_terms(text), [])

    def test_regex_matches_inside_double_backticks_and_across_lines(self):
        self.assertEqual(check_repo.code_span_terms("``a/b``"), ["a", "b"])
        self.assertEqual(check_repo.code_span_terms("`a\nb`"), ["a\nb"])


class NormalizedCorpusBodyTests(unittest.TestCase):
    def test_normalizes_line_endings_and_trailing_whitespace(self):
        self.assertEqual(check_repo.normalized_corpus_body("\r\n甲  \r\n乙\t\r丙\r\n"), "甲\n乙\n丙")

    def test_strips_outer_whitespace_but_preserves_internal_layout(self):
        self.assertEqual(check_repo.normalized_corpus_body("  甲\n\n  乙  丙  \n  丁  "),
                         "甲\n\n  乙  丙\n  丁")

    def test_empty_and_whitespace_only_bodies_normalize_to_empty(self):
        for text in ("", " \t\r\n\n", "\u3000"):
            with self.subTest(text=text):
                self.assertEqual(check_repo.normalized_corpus_body(text), "")

    def test_splitlines_also_normalizes_other_line_separators(self):
        self.assertEqual(check_repo.normalized_corpus_body("甲\v乙\u2028丙"), "甲\n乙\n丙")


class HumanBenchmarkDuplicatesTests(unittest.TestCase):
    def test_matches_normalized_bodies_and_collects_ids_in_case_order(self):
        record = {"id": "HUMAN-1", "text": "\r\n甲  \r\n乙\t\n"}
        cases = [("SNF-02", "ignored", "> 甲\n> 乙"),
                 ("SF-01", "ignored", "> 甲  \r\n> 乙 ")]

        def strip_blockquote(body):
            return "\n".join(line.removeprefix("> ") for line in body.splitlines())

        result = check_repo.human_benchmark_duplicates([record], cases, strip_blockquote)
        self.assertEqual(result, [(record, ["SNF-02", "SF-01"])])
        self.assertIs(result[0][0], record)

    def test_filters_case_prefixes_before_calling_callback(self):
        bodies = []

        def strip_blockquote(body):
            bodies.append(body)
            return body

        cases = [(cid, None, cid) for cid in ("RS-01", "sf-01", "XSF-01", "SF-", "SNF-custom")]
        records = [{"text": cid} for cid, _, _ in cases]
        self.assertEqual(check_repo.human_benchmark_duplicates(records, cases, strip_blockquote),
                         [(records[3], ["SF-"]), (records[4], ["SNF-custom"])])
        self.assertEqual(bodies, ["SF-", "SNF-custom"])

    def test_preserves_record_order_and_repeated_case_ids(self):
        records = [{"text": "b"}, {"text": "a"}, {"text": "a"}]
        cases = [("SF-1", None, "a"), ("SF-1", None, "a"), ("SNF-2", None, "b")]
        self.assertEqual(check_repo.human_benchmark_duplicates(records, cases, lambda body: body),
                         [(records[0], ["SNF-2"]), (records[1], ["SF-1", "SF-1"]),
                          (records[2], ["SF-1", "SF-1"])])

    def test_matching_is_exact_after_normalization(self):
        records = [{"text": text} for text in ("a b", "A  b", "a\nb", "> a  b")]
        cases = [("SF-1", None, "a  b")]
        self.assertEqual(check_repo.human_benchmark_duplicates(records, cases, lambda body: body), [])

    def test_empty_inputs_and_normalized_empty_bodies(self):
        record = {"text": " \r\n"}
        cases = [("SF-1", None, "\t")]
        self.assertEqual(check_repo.human_benchmark_duplicates([], cases, lambda body: body), [])
        self.assertEqual(check_repo.human_benchmark_duplicates([record], [], lambda body: body), [])
        self.assertEqual(check_repo.human_benchmark_duplicates([record], cases, lambda body: body),
                         [(record, ["SF-1"])])


if __name__ == "__main__":
    unittest.main()
