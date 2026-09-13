"""新协议保留产品正文，只检查结构与覆盖范围。"""
import json
import unittest

from protocol import ProtocolError, parse_response, summarize_judgments


class ProtocolTests(unittest.TestCase):
    def rewrite(self, rows):
        return json.dumps({"cases": rows}, ensure_ascii=False)

    def test_body_is_preserved_and_order_is_canonical(self):
        body = '## 标题\n\n```json\n{"a": 1}\n```\n\n（这是正文）\n保留原文。'
        response = self.rewrite([{"id": "B-02", "text": "另一条"}, {"id": "B-01", "text": body}])
        rows = parse_response(response, "rewrite", ["B-01", "B-02"])
        self.assertEqual(rows[0], {"id": "B-01", "text": body})

    def test_single_json_fence_is_accepted(self):
        raw = self.rewrite([{"id": "B-01", "text": "原文"}])
        self.assertEqual(parse_response('```json\n' + raw + '\n```', 'rewrite', ['B-01'])[0]['text'], '原文')

    def test_rejects_partial_duplicate_unknown_and_extra_fields(self):
        valid = {"id": "B-01", "text": "正文"}
        for rows in [[], [valid, valid], [{"id": "B-02", "text": "正文"}], [dict(valid, tier="1")]]:
            with self.subTest(rows=rows), self.assertRaises(ProtocolError):
                parse_response(self.rewrite(rows), "rewrite", ["B-01"])

    def test_rejects_non_json_duplicate_keys_and_wrappers(self):
        raw = self.rewrite([{"id": "B-01", "text": "正文"}])
        for bad in [raw + '\n说明', '说明\n' + raw, '```\n```json\n' + raw + '\n```\n```',
                    '{"cases": [], "cases": []}', '{"cases":[{"id":"B-01","text":"a","text":"b"}]}',
                    '{"cases": [], "score": NaN}']:
            with self.subTest(bad=bad), self.assertRaises(ProtocolError):
                parse_response(bad, "rewrite", ["B-01"])

    def test_judge_requires_evidence_and_valid_dimensions(self):
        row = dict(id="B-01", fidelity="fail", task="pass", quality="better", evidence="原文 2 人，输出 3 人")
        self.assertEqual(parse_response(self.rewrite([row]), "judge", ["B-01"]), [row])
        for change in [{"evidence": " "}, {"fidelity": "better"}, {"quality": "pass"}]:
            with self.assertRaises(ProtocolError):
                parse_response(self.rewrite([dict(row, **change)]), "judge", ["B-01"])

    def test_summary_keeps_review_and_quality_separate(self):
        rows = [dict(id="B-01", fidelity="pass", task="review", quality="worse", evidence="需复核"),
                dict(id="B-02", fidelity="fail", task="pass", quality="better", evidence="数字改变")]
        result = summarize_judgments(rows, ["B-01", "B-02"])
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["fidelity"], {"pass": 1, "fail": 1, "review": 0})
        self.assertEqual(result["task"]["review"], 1)
        self.assertEqual(result["quality"]["worse"], 1)
        with self.assertRaises(ProtocolError):
            summarize_judgments(rows[:1], ["B-01", "B-02"])


if __name__ == "__main__":
    unittest.main()
