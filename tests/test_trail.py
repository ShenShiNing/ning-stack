import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "trail.py"


class TrailCli(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.file = Path(self.dir.name) / "trail.tsv"

    def tearDown(self):
        self.dir.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-I", str(SCRIPT), *args],
            capture_output=True,
            text=True,
        )

    def ok(self, *args):
        result = self.run_cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def at(self, minute):
        return f"2026-01-01T10:{minute:02d}:00+08:00"

    def test_overlapping_spans_report_union_wall_time_and_overlapping_phase_totals(self):
        f = str(self.file)
        self.ok("run-start", f, "r1", "--at", self.at(0))
        self.ok("start", f, "r1", "review", "review-wait", "--at", self.at(10))
        self.ok("start", f, "r1", "ci", "ci-wait", "--at", self.at(10))
        self.ok("end", f, "r1", "review", "--at", self.at(30))
        self.ok("end", f, "r1", "ci", "--at", self.at(40))
        self.ok("run-end", f, "r1", "--at", self.at(50))

        out = self.ok("report", f)

        self.assertIn("run r1: elapsed 50.0 min, active wall 30.0 min", out)
        self.assertIn("review-wait\t20.0 min", out)
        self.assertIn("ci-wait\t30.0 min", out)
        self.assertIn("overlap", out)

    def test_offline_gap_between_runs_is_not_counted(self):
        f = str(self.file)
        self.ok("run-start", f, "a", "--at", "2026-01-01T09:00:00+08:00")
        self.ok("start", f, "a", "s1", "write", "--at", "2026-01-01T09:00:00+08:00")
        self.ok("end", f, "a", "s1", "--at", "2026-01-01T09:10:00+08:00")
        self.ok("run-end", f, "a", "--at", "2026-01-01T09:10:00+08:00")
        self.ok("run-start", f, "b", "--at", "2026-01-02T09:00:00+08:00")
        self.ok("start", f, "b", "s1", "write", "--at", "2026-01-02T09:00:00+08:00")
        self.ok("end", f, "b", "s1", "--at", "2026-01-02T09:05:00+08:00")
        self.ok("run-end", f, "b", "--at", "2026-01-02T09:05:00+08:00")

        out = self.ok("report", f)

        self.assertIn("all runs: elapsed 15.0 min, active wall 15.0 min", out)
        self.assertIn("write\t15.0 min", out)

    def test_end_before_start_is_rejected_and_not_written(self):
        f = str(self.file)
        self.ok("run-start", f, "r", "--at", self.at(0))
        self.ok("start", f, "r", "s", "explore", "--at", self.at(20))

        result = self.run_cli("end", f, "r", "s", "--at", self.at(10))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("before", result.stderr)
        self.assertEqual(len(self.file.read_text().splitlines()), 3)

    def test_end_of_unknown_span_is_rejected(self):
        f = str(self.file)
        self.ok("run-start", f, "r", "--at", self.at(0))

        result = self.run_cli("end", f, "r", "missing", "--at", self.at(5))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing", result.stderr)

    def test_run_cannot_end_before_a_completed_span(self):
        f = str(self.file)
        self.ok("run-start", f, "r", "--at", self.at(0))
        self.ok("start", f, "r", "s", "write", "--at", self.at(5))
        self.ok("end", f, "r", "s", "--at", self.at(20))

        result = self.run_cli("run-end", f, "r", "--at", self.at(10))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("before", result.stderr)
        self.assertEqual(len(self.file.read_text().splitlines()), 4)

    def test_report_flags_incomplete_runs_and_spans(self):
        f = str(self.file)
        self.ok("run-start", f, "r", "--at", self.at(0))
        self.ok("start", f, "r", "s", "validate", "--at", self.at(5))

        result = self.run_cli("report", f)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("incomplete", result.stderr)
        self.assertIn("s", result.stderr)

    def test_hand_edited_negative_span_fails_report(self):
        self.file.write_text(
            "ts\trun\tevent\tspan\tphase\tdecision\twhy\tevidence\tresult\n"
            f"{self.at(0)}\tr\trun-start\t\t\t\t\t\t\n"
            f"{self.at(9)}\tr\tstart\ts\twrite\t\t\t\t\n"
            f"{self.at(3)}\tr\tend\ts\t\t\t\t\t\n"
            f"{self.at(10)}\tr\trun-end\t\t\t\t\t\t\n"
        )

        result = self.run_cli("report", str(self.file))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("before", result.stderr)

    def test_notes_are_single_line_and_formula_safe(self):
        f = str(self.file)
        self.ok("run-start", f, "r", "--at", self.at(0))
        self.ok(
            "note", f, "r", "frame", "=HYPERLINK(1)", "two\nlines", "-1", "+ok\tthere", "--at", self.at(1)
        )

        rows = list(csv.DictReader(self.file.read_text().splitlines(), delimiter="\t"))
        note = rows[-1]

        self.assertEqual(note["event"], "note")
        self.assertEqual(note["decision"], "'=HYPERLINK(1)")
        self.assertEqual(note["why"], "two lines")
        self.assertEqual(note["evidence"], "'-1")
        self.assertEqual(note["result"], "'+ok there")

    def test_timestamp_without_offset_is_rejected(self):
        result = self.run_cli("run-start", str(self.file), "r", "--at", "2026-01-01T10:00:00")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("offset", result.stderr)


if __name__ == "__main__":
    unittest.main()
