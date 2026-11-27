"""Kiểm cách đếm bằng dữ liệu giả tạm thời; không phải bằng chứng pain.

Chạy: python -B -m unittest discover -s scripts -p test_mine_chat.py -v
"""
import contextlib
import csv
from datetime import datetime, timedelta
import io
import json
from pathlib import Path
import tempfile
import unittest

import mine_chat


def question(code, second=0, latency=1, length=20, learner="TEST_LEARNER", video="TEST_VIDEO", **extra):
    asked = datetime(2026, 1, 1) + timedelta(seconds=second)
    row = {"id": code, "hv": learner, "channel": "video_question", "transcript": video, "kind": "question",
           "agent_id": "teaching_assistant", "asked_at": asked.isoformat(),
           "created_at": (asked + timedelta(seconds=latency)).isoformat(),
           "do_dai_cau_hoi": length, "do_dai_tra_loi": 100}
    row.update(extra)
    return row


class MiningTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "synthetic-test.csv"

    def write_rows(self, rows, delimiter=","):
        with self.path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=sorted(mine_chat.REQUIRED), delimiter=delimiter)
            writer.writeheader()
            writer.writerows(rows)
        return self.path

    def test_boundaries_filter_order_and_groups(self):
        self.write_rows([
            question("T3", 241, latency=0.5, length=11),
            question("T2", 120, latency=0.499, length=10),
            question("T1", 0, latency=0, length=2),
            question("T4", 121, learner="OTHER_LEARNER"),
            question("T5", 121, video="OTHER_VIDEO"),
            question("T6", 121, kind="answer"),
            question("T7", 121, agent_id="other_agent"),
        ], delimiter=";")
        report = mine_chat.analyze(self.path)
        self.assertEqual((report["total_rows"], report["questions"], report["learners"]), (7, 5, 2))
        self.assertEqual(report["short_questions"]["count"], 2)
        self.assertEqual(report["fast_responses"]["count"], 2)
        self.assertEqual(report["followups"]["count"], 1)
        self.assertEqual(report["followup_examples"], [{"previous_id": "T1", "current_id": "T2", "gap_s": 120}])
        self.assertEqual(len(report["source_sha256"]), 64)

    def test_zero_fast_responses_and_no_followups(self):
        self.write_rows([question("T1")])
        report = mine_chat.analyze(self.path)
        self.assertEqual(report["fast_responses"]["count"], 0)
        self.assertEqual(report["followups"]["count"], 0)
        self.assertEqual(report["fast_response_examples"], [])

    def test_invalid_records_fail_instead_of_changing_denominator(self):
        cases = [
            ([question("T1", latency=-1)], "phản hồi âm"),
            ([question("T1", length=-1)], "số nguyên không âm"),
            ([question("T1", length="abc")], "số nguyên không âm"),
            ([question("T1", hv="")], "thiếu hv"),
            ([question("T1", asked_at="invalid")], "ISO 8601"),
            ([question("T1"), question("T1")], "bị trùng"),
            ([question("T1", kind="answer")], "Không có câu hỏi"),
            ([question("T1", created_at="2026-01-01T00:00:01+00:00")], "múi giờ"),
        ]
        for rows, message in cases:
            with self.subTest(message=message):
                self.write_rows(rows)
                with self.assertRaisesRegex(ValueError, message):
                    mine_chat.analyze(self.path)

    def test_missing_column(self):
        self.path.write_text("id,kind\nT1,question\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Thiếu cột"):
            mine_chat.analyze(self.path)

    def test_missing_video_retains_totals_but_cannot_create_same_video_pair(self):
        self.write_rows([question("T1", latency=0.1, length=2, video=""),
                         question("T2", second=10, latency=0.1, length=2, video=""),
                         question("T3", second=20)])
        report = mine_chat.analyze(self.path)
        self.assertEqual(report["questions"], 3)
        self.assertEqual(report["short_questions"]["count"], 2)
        self.assertEqual(report["fast_responses"]["count"], 2)
        self.assertEqual(report["followups"]["count"], 0)
        self.assertEqual(report["followups"]["eligible_questions"], 1)
        self.assertEqual(report["data_quality"], {"missing_video_count": 2, "missing_video_ids": ["T1", "T2"],
                                                 "video_questions_missing_transcript": 2})

    def test_empty_filter_fields_fail_even_with_other_valid_rows(self):
        for field in ("kind", "agent_id"):
            with self.subTest(field=field):
                self.write_rows([question("GOOD"), question("BAD", **{field: ""})])
                with self.assertRaisesRegex(ValueError, "thiếu " + field):
                    mine_chat.analyze(self.path)

    def test_wrong_cell_count_is_rejected_before_filtering(self):
        self.write_rows([question("GOOD")])
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write("too,few,cells\n")
        with self.assertRaisesRegex(ValueError, "số ô không khớp"):
            mine_chat.analyze(self.path)

    def test_duplicate_headers_are_rejected(self):
        self.path.write_text("id,id\nA,B\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "cột bị trùng"):
            mine_chat.analyze(self.path)

    def test_session_question_cannot_form_video_pair_even_with_same_transcript(self):
        self.write_rows([question("V1", second=0),
                         question("SESSION", second=60, channel="session_question"),
                         question("V2", second=180)])
        report = mine_chat.analyze(self.path)
        self.assertEqual(report["questions"], 3)
        self.assertEqual(report["channels"], {"session_question": 1, "video_question": 2})
        self.assertEqual(report["video_only"]["questions"], 2)
        self.assertEqual(report["followups"]["count"], 0)

    def test_session_without_video_keeps_main_denominator_and_video_rate_separate(self):
        self.write_rows([question("V1", second=0), question("V2", second=60),
                         question("SESSION", second=70, channel="session_question", video="")])
        report = mine_chat.analyze(self.path)
        self.assertEqual(report["questions"], 3)
        self.assertEqual(report["followups"]["count"], 1)
        self.assertAlmostEqual(report["followups"]["percent"], 100 / 3)
        self.assertEqual(report["video_only"]["followup_percent"], 50)
        self.assertEqual(report["data_quality"]["video_questions_missing_transcript"], 0)

    def test_cli_outputs_no_learner_or_video_identifiers_and_writes_nothing(self):
        self.write_rows([question("T1", latency=0.1, length=2)])
        before = self.path.read_bytes()
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(mine_chat.main([str(self.path), "--json"]), 0)
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["fast_response_examples"][0]["id"], "T1")
        for private in ("TEST_LEARNER", "TEST_VIDEO"):
            self.assertNotIn(private, stdout.getvalue())
        self.assertEqual(before, self.path.read_bytes())
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_missing_file_has_clear_cli_failure(self):
        with contextlib.redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(mine_chat.main([str(self.path)]), 1)
        self.assertIn("Không thể phân tích", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
