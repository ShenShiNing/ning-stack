#!/usr/bin/env python3
"""Read-only finish gate for a GitHub PR, using an authenticated `gh`.

  gate.py --repo OWNER/REPO --pr NUMBER --head FULL_SHA --finish ready|merged
          [--require-check NAME ...] [--allow-no-checks]

Prints PASS and exits 0, or prints each failed condition and exits 1. It never
changes remote state and never retries. The result is a snapshot: the final
merge must still pin the head, and review, authorization and queue decisions
stay with the caller. Required checks are GitHub's required-check policy plus
any --require-check names; names add to the policy and never waive it.
"""

import argparse
import json
import subprocess
import sys
from urllib.parse import quote

VIEW_FIELDS = "headRefOid,baseRefName,state,isDraft,autoMergeRequest"
CHECK_FIELDS = "name,bucket,state"
NO_CHECKS = ("no required checks reported", "no checks reported")


class GateError(Exception):
    pass


def gh(*args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise GateError(f"gh could not run: {error}") from error


def parse_json(result: subprocess.CompletedProcess, what: str):
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise GateError(f"{what}: unreadable response") from error


def snapshot(repo: str, pr: str) -> dict:
    result = gh("pr", "view", pr, "-R", repo, "--json", VIEW_FIELDS)
    if result.returncode != 0:
        raise GateError(f"pr view failed: {result.stderr.strip()}")
    data = parse_json(result, "pr view")
    if not isinstance(data, dict) or not all(
        isinstance(data.get(key), str) and data[key] for key in ("headRefOid", "baseRefName")
    ):
        raise GateError("pr view: missing headRefOid or baseRefName")
    if not isinstance(data.get("state"), str) or not isinstance(data.get("isDraft"), bool):
        raise GateError("pr view: missing state or isDraft")
    if "autoMergeRequest" not in data:
        raise GateError("pr view: missing autoMergeRequest")
    return data


def declared_checks(repo: str, branch: str) -> set[str]:
    base = f"repos/{repo}/branches/{quote(branch, safe='')}/protection"
    result = gh("api", "--method", "GET", base)
    if result.returncode:
        try:
            error = json.loads(result.stdout)
        except json.JSONDecodeError:
            error = {}
        if not isinstance(error, dict) or error.get("message") != "Branch not protected" or str(error.get("status")) != "404":
            raise GateError(f"branch protection query failed: {result.stderr.strip()}")
        classic = {"required_status_checks": None}
    else:
        classic = parse_json(result, "branch protection")
    if not isinstance(classic, dict) or "required_status_checks" not in classic:
        raise GateError("branch protection: missing required status check policy")
    policy = classic["required_status_checks"]
    contexts = [] if policy is None else policy.get("contexts") if isinstance(policy, dict) else None
    if not isinstance(contexts, list) or not all(isinstance(c, str) and c for c in contexts):
        raise GateError("branch protection: missing required contexts")
    names = set(contexts)
    result = gh("api", "--method", "GET",
                f"repos/{repo}/rules/branches/{quote(branch, safe='')}?per_page=100",
                "--paginate", "--slurp")
    if result.returncode:
        raise GateError(f"branch rules query failed: {result.stderr.strip()}")
    pages = parse_json(result, "branch rules")
    if not isinstance(pages, list) or not all(isinstance(page, list) for page in pages):
        raise GateError("branch rules: expected paginated lists")
    for rule in (rule for page in pages for rule in page):
        if not isinstance(rule, dict) or not isinstance(rule.get("type"), str):
            raise GateError("branch rules: missing rule type")
        if rule["type"] == "workflows":
            raise GateError("required workflow policy needs separate verification")
        if rule["type"] == "required_status_checks":
            params = rule.get("parameters")
            checks = params.get("required_status_checks") if isinstance(params, dict) else None
            if not isinstance(checks, list):
                raise GateError("branch rules: missing required status checks")
            for check in checks:
                context = check.get("context") if isinstance(check, dict) else None
                if not isinstance(context, str) or not context:
                    raise GateError("branch rules: missing check context")
                names.add(context)
    return names


def collect_checks(repo: str, pr: str, only_required: bool) -> list[dict]:
    flags = ["--required"] if only_required else []
    result = gh("pr", "checks", pr, "-R", repo, *flags, "--json", CHECK_FIELDS)
    # gh exits 8 while checks are pending and 1 when some failed, still printing JSON.
    if result.returncode in (0, 1, 8) and result.stdout.strip():
        rows = parse_json(result, "pr checks")
        if not isinstance(rows, list):
            raise GateError("pr checks: expected a list")
        return rows
    if result.returncode == 1 and any(text in result.stderr for text in NO_CHECKS):
        return []
    raise GateError(f"pr checks failed (exit {result.returncode}): {result.stderr.strip()}")


def failing(rows: list[dict], label: str) -> list[str]:
    problems = []
    for entry in rows:
        name = entry.get("name") if isinstance(entry, dict) else None
        bucket = entry.get("bucket") if isinstance(entry, dict) else None
        if not isinstance(name, str) or not isinstance(bucket, str) or not isinstance(entry.get("state"), str):
            problems.append(f"{label} check has missing fields: {entry!r}")
        elif bucket != "pass" or entry["state"] != "SUCCESS":
            problems.append(f"{label} check {name} is {bucket}")
    return problems


def evaluate(args: argparse.Namespace) -> list[str]:
    problems = []
    before = snapshot(args.repo, args.pr)
    declared = declared_checks(args.repo, before["baseRefName"])
    required = collect_checks(args.repo, args.pr, only_required=True)
    named = args.require_check
    everything = collect_checks(args.repo, args.pr, only_required=False) if named else []
    after = snapshot(args.repo, args.pr)
    if before["baseRefName"] != after["baseRefName"]:
        problems.append("PR base changed during checks")

    for label, pr in (("before", before), ("after", after)):
        if pr["headRefOid"] != args.head:
            problems.append(f"head {pr['headRefOid']} {label} checks is not the reviewed head {args.head}")
        if pr["state"] != "OPEN":
            problems.append(f"PR is not open ({pr['state']}) {label} checks")
        if pr["isDraft"]:
            problems.append(f"PR is a draft {label} checks")
        if args.finish == "ready" and pr["autoMergeRequest"] is not None:
            problems.append(f"auto-merge is enabled {label} checks")

    problems += failing(required, "required")
    reported = {row["name"] for row in required
                if isinstance(row, dict) and isinstance(row.get("name"), str)}
    for name in sorted(declared - reported):
        problems.append(f"required check {name} has not reported")
    for name in named:
        matching = [entry for entry in everything if isinstance(entry, dict) and entry.get("name") == name]
        if not matching:
            problems.append(f"required check {name} is missing")
        problems += failing(matching, "named")
    if not required and not named and not args.allow_no_checks:
        problems.append("no required checks: name them with --require-check or pass --allow-no-checks")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--finish", required=True, choices=["ready", "merged"])
    parser.add_argument("--require-check", action="append", default=[])
    parser.add_argument("--allow-no-checks", action="store_true")
    args = parser.parse_args()
    try:
        problems = evaluate(args)
    except GateError as error:
        problems = [str(error)]
    if problems:
        print("\n".join(f"FAIL: {problem}" for problem in problems))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
