import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "gate.py"
HEAD = "a" * 40
OTHER = "b" * 40

# A stand-in `gh` that replays canned answers. Each answer is used once, by the
# first unused entry whose `match` is a substring of the joined arguments.
FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
state_file = os.environ["FAKE_GH_STATE"]
state = json.load(open(state_file))
line = " ".join(sys.argv[1:])
state["calls"].append(line)
for answer in state["answers"]:
    if not answer.get("used") and answer["match"] in line:
        answer["used"] = True
        break
else:
    answer = {"code": 99, "stdout": "", "stderr": "unexpected call: " + line}
json.dump(state, open(state_file, "w"))
sys.stdout.write(answer["stdout"])
sys.stderr.write(answer["stderr"])
sys.exit(answer["code"])
"""


def view(head=HEAD, state="OPEN", draft=False, auto=None):
    return {
        "match": "pr view",
        "code": 0,
        "stdout": json.dumps(
            {"headRefOid": head, "state": state, "isDraft": draft, "autoMergeRequest": auto, "baseRefName": "main"}
        ),
        "stderr": "",
    }


def checks(match, rows, code=0):
    return {"match": match, "code": code, "stdout": json.dumps(rows), "stderr": ""}


def required(rows, code=0):
    return checks("--required", rows, code)


def all_checks(rows, code=0):
    return checks("pr checks 7 -R o/r --json", rows, code)


def row(name, bucket="pass", state="SUCCESS"):
    return {"name": name, "bucket": bucket, "state": state}


NO_REQUIRED = {
    "match": "--required",
    "code": 1,
    "stdout": "",
    "stderr": "no required checks reported on the 'feature' branch\n",
}


class Gate(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        root = Path(self.dir.name)
        gh = root / "gh"
        gh.write_text(FAKE_GH)
        gh.chmod(0o755)
        self.state = root / "state.json"

    def tearDown(self):
        self.dir.cleanup()

    def gate(self, answers, *extra, head=HEAD, finish="ready", policy=None, rules=None):
        contexts = policy if policy is not None else []
        answers = [
            checks("branches/main/protection", {"required_status_checks": {"contexts": contexts}}),
            checks("rules/branches/", [rules or []]),
            *answers,
        ]
        self.state.write_text(json.dumps({"answers": answers, "calls": []}))
        env = {
            **os.environ,
            "PATH": f"{self.dir.name}{os.pathsep}{os.environ['PATH']}",
            "FAKE_GH_STATE": str(self.state),
        }
        result = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), "--repo", "o/r", "--pr", "7",
             "--head", head, "--finish", finish, *extra],
            capture_output=True, text=True, env=env,
        )
        return result, json.loads(self.state.read_text())["calls"]

    def passes(self, answers, *extra, **kw):
        result, calls = self.gate(answers, *extra, **kw)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), "PASS")
        return calls

    def fails(self, answers, expect, *extra, **kw):
        result, _ = self.gate(answers, *extra, **kw)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("PASS", result.stdout)
        self.assertIn(expect, result.stdout + result.stderr)

    def test_good_result_only_reads(self):
        calls = self.passes([view(), required([row("build")]), view()])
        for call in calls:
            self.assertRegex(call, r"^(pr (view|checks) |api --method GET )")

    def test_never_reported_classic_requirement_cannot_pass(self):
        self.fails([view(), required([row("build")]), view()], "never-reported",
                   policy=["build", "never-reported"])

    def test_never_reported_ruleset_requirement_cannot_pass(self):
        rules = [{"type": "required_status_checks", "parameters": {
            "required_status_checks": [{"context": "never-reported"}]}}]
        self.fails([view(), required([row("build")]), view()], "never-reported", rules=rules)

    def test_allow_no_checks_cannot_waive_policy_access_errors(self):
        result, _ = self.gate([view(), required([]), view()], "--allow-no-checks")
        self.assertEqual(result.returncode, 0, result.stdout)
        data = json.loads(self.state.read_text())
        for answer in data["answers"]:
            answer.pop("used", None)
            if "/protection" in answer["match"]:
                answer.update(code=1, stdout="", stderr="HTTP 403: denied")
        self.state.write_text(json.dumps(data))
        env = {**os.environ, "PATH": f"{self.dir.name}{os.pathsep}{os.environ['PATH']}",
               "FAKE_GH_STATE": str(self.state)}
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), "--repo", "o/r", "--pr", "7",
                                 "--head", HEAD, "--finish", "ready", "--allow-no-checks"],
                                capture_output=True, text=True, env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("403", result.stdout)

    def test_stale_head(self):
        self.fails([view(head=OTHER), required([row("build")]), view(head=OTHER)], "head")

    def test_closed_and_draft_prs_fail(self):
        self.fails([view(state="CLOSED"), required([row("b")]), view(state="CLOSED")], "open")
        self.fails([view(draft=True), required([row("b")]), view(draft=True)], "draft")

    def test_ready_requires_auto_merge_off_but_merged_does_not(self):
        on = {"enabledBy": {"login": "x"}}
        answers = [view(auto=on), required([row("b")]), view(auto=on)]
        self.fails(answers, "auto-merge")
        self.passes(answers, finish="merged")

    def test_nonpassing_required_checks_fail_even_when_gh_returns_json(self):
        for bucket, state, code in [
            ("pending", "IN_PROGRESS", 8),
            ("fail", "FAILURE", 1),
            ("cancel", "CANCELLED", 1),
            ("skipping", "SKIPPED", 0),
        ]:
            with self.subTest(bucket):
                self.fails([view(), required([row("build"), row("test", bucket, state)], code), view()], "test")

    def test_same_name_passing_context_cannot_mask_failing_one(self):
        rows = [row("build"), row("build", "fail", "FAILURE")]
        self.fails([view(), required(rows, 1), view()], "build")

    def test_explicit_checks_supplement_required_policy(self):
        everything = [row("build"), row("e2e")]
        answers = [view(), required([row("build")]), all_checks(everything), view()]
        self.passes(answers, "--require-check", "e2e")
        missing = [view(), required([row("build")]), all_checks([row("build")]), view()]
        self.fails(missing, "e2e", "--require-check", "e2e")

    def test_explicit_checks_never_waive_a_failing_server_requirement(self):
        answers = [
            view(),
            required([row("build", "fail", "FAILURE")], 1),
            all_checks([row("build", "fail", "FAILURE"), row("e2e")], 1),
            view(),
        ]
        self.fails(answers, "build", "--require-check", "e2e")

    def test_no_required_policy_needs_names_or_flag(self):
        self.fails([view(), NO_REQUIRED, view()], "no required checks")
        self.passes([view(), NO_REQUIRED, view()], "--allow-no-checks")
        named = [view(), NO_REQUIRED, all_checks([row("e2e")]), view()]
        self.passes(named, "--require-check", "e2e")

    def test_allow_no_checks_never_waives_query_failure_or_failing_check(self):
        broken = {"match": "--required", "code": 1, "stdout": "", "stderr": "HTTP 502\n"}
        self.fails([view(), broken, view()], "502", "--allow-no-checks")
        failing = required([row("build", "fail", "FAILURE")], 1)
        self.fails([view(), failing, view()], "build", "--allow-no-checks")

    def test_malformed_responses_fail_closed(self):
        garbage = {"match": "--required", "code": 0, "stdout": "not json", "stderr": ""}
        self.fails([view(), garbage, view()], "checks")
        self.fails([view(), required([{"name": "build"}]), view()], "build")
        self.fails([view(), required({"name": "build"}), view()], "checks")
        no_head = {"match": "pr view", "code": 0, "stdout": "{}", "stderr": ""}
        self.fails([no_head, required([row("b")]), no_head], "pr view")

    def test_query_errors_fail_closed(self):
        broken = {"match": "pr view", "code": 1, "stdout": "", "stderr": "HTTP 404\n"}
        self.fails([broken], "404")

    def test_head_moving_between_snapshots_fails(self):
        self.fails([view(), required([row("build")]), view(head=OTHER)], "head")

    def test_auto_merge_enabled_between_snapshots_fails_ready(self):
        on = {"enabledBy": {"login": "x"}}
        self.fails([view(), required([row("build")]), view(auto=on)], "auto-merge")


if __name__ == "__main__":
    unittest.main()
