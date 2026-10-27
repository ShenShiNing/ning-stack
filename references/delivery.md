# Delivery

One request owner carries the finish line. One slice owner keeps a coherent change through review and CI fixes; the request owner may implement it directly. Delegate for a real need: isolation, another model or expertise, independent write sets, or context limits. Follow project model and concurrency rules. Reviewers are independent and read-only; children never launch review trees or watch PRs.

## Stage 0: Frame

State acceptance, finish line, and risk in the existing progress note. A small task needs only a few lines. Split only if work is genuinely independent; name ownership, blocking steps, and shared state when a split is needed. Give each child a standalone brief: goal, owned paths, acceptance, finish line, PR policy and authorization limits, proof, and report with evidence and head SHA.

**Finish line:** `local` = committed, proven, and reviewed when required; `ready` = PR passes its gate, left unmerged; `merged` = merged after the gate. User instructions win, then the project default, otherwise `ready`.

- `full send` selects merged; `full stop` selects ready. Both authorize this task's pushes, own-branch `--force-with-lease`, and proof methods such as running the app or captures, subject to harness and project limits. Full send also authorizes the gated merge. Production, data deletion, closing PRs, and other branches are outside these grants.
- For full stop, disable auto-merge and leave merge queues before other work; recheck before each push and handoff. Never merge, enqueue, enable auto-merge, or delegate a merge. Any ready finish leaves auto-merge off.

| Risk | Local proof |
| --- | --- |
| R0 prose: no code, config, or build consumes it | scoped format and link checks |
| R1 bounded behavior or wiring unchanged public capabilities | relevant tests or reproduction, affected type and lint checks |
| R2 shared semantics or contracts, security, state, concurrency, lifecycle, persistence, broad tooling, or unknown impact | R1 plus checks for the actual affected risks; read [Evidence](methods/evidence.md), Blast radius |

Classify instructions and operational documents by what consuming them changes, not their extension. Escalate when impact grows. Project gates still apply; a scheduled full run never substitutes for required pre-merge proof.

For R2 or changes to releases, persisted data, or access controls, include recovery in the existing frame: the signal that reveals a regression, how to stop its impact or recover, and any data or external effects left after a code revert. Prove the recovery mechanism in a safe environment where feasible; otherwise name the unverified part. Irreversible steps and recovery actions retain their own authorization requirements.

## Stage 1: Ground

Use the harness-owned isolated checkout from the freshly fetched default branch. Preserve the user's primary checkout and unrelated work. Read the owner and callers; reuse an agreed brief's grounding. A bug needs a failing reproduction before a fix. Use [Investigation](methods/investigation.md) for a hard bug, unfamiliar subsystem, or decision whose rationale must be revisited.

Proceed when the changed behavior, owning seam, and applicable constraints are clear.

## Stage 2: Change and prove

Make the smallest change meeting acceptance. For behavior changes, use red-to-green vertical slices at an existing public seam. A test must catch a distinct current risk; pure visual changes use before/after captures. Mechanical refactors may use existing coverage when project rules permit. Read [Evidence](methods/evidence.md), Tests when writing or removing tests.

Run the framed proof. Stop when acceptance and relevant risks are covered. Keep commands and results tied to the tested head and base. For reused evidence or a moving base, read Evidence, Reuse.

## Stage 3: Publish, or finish locally

Commit coherent changes. For `local`, apply the review policy below to the local committed diff, fix real findings, and report without pushing or requiring remote CI.

Otherwise check for an existing PR, push, and open one ready PR. Follow the project's title/body convention: problem, change, evidence, model and harness; carry any framed recovery guidance into the body and scan for private details. Follow the project's PR registration and supervision rules. A child's last line reports PR URL, head, checks, and review state.

## Stage 4: Review and CI together

Apply [Review](methods/review.md), Scope, including its narrow mechanical-document exemption. When review is required, launch one fresh reviewer against the pushed head while CI runs on that same head. That method defines the brief, severity, and round budget. A stricter project ordering governs when present.

## Stage 5: Fix loop

The slice owner checks findings against the source: fix a real defect, disagree with evidence, or decline a nit or unrelated scope with a reason. Keep unresolved findings, including older bot comments, until resolved on the current head. Track findings only when there are findings.

Batch fixes into one push per round. Distinguish product failures from infrastructure flakes; rerun an established flake once. Re-run affected proof and current-head CI. A fresh review covers open findings, behavioral fixes, or new scope; format and comment edits alone need no new round. Earlier conclusions carry only under Evidence, Reuse. An exhausted budget is not approval.

## Stage 6: Finish gate

Fetch and evaluate the latest head:

1. Proof and any required independent review cover its behavior; no unresolved blocker, should, or human request for changes remains. Check required GitHub approvals separately from the agent verdict.
2. Required checks pass on this head. Local proof cannot replace a required remote check.
3. No merge conflict. Inspect base changes affecting this patch or its dependencies, contracts, and shared resources, even without conflicts. Rebase for an interaction, conflict, or project requirement; then renew affected proof and review. See Evidence, Reuse.

For a GitHub PR, run `scripts/gate.py --repo OWNER/REPO --pr NUMBER --head REVIEWED_SHA --finish ready|merged` from the skill directory before finishing. Supply project check names with `--require-check NAME` when needed; see the [README](../README.md#validate). A pass covers only the helper's observable conditions, not the review or authorization decision.

For merged, use the configured merge method with the head pinned (`--match-head-commit` or equivalent), then confirm merge. For ready, leave the PR open with auto-merge off. If a gate cannot be met, report the blocker and ask only for the decision needed; preserve the PR unmerged.

## Stage 7: Close out and waiting

Report acceptance, proof, review outcome, PR or local finish, and gaps. Clean up only this task's worktree and branch when safe. Unwatch before handoff. Record recurring debt for cleanup, a changed architectural premise for optimization, and observed process friction for [Learning](methods/learning.md); do not expand the delivered task into those follow-ups without authorization.

When waiting, use harness completion events and the PR watcher, owned by the request thread. Follow instructions to end the turn after registering a watcher. Without a watcher, check only at harness-permitted decision points; otherwise report the exact pending gate. No polling loops or watcher agents.

**Special entries:** read [Continuity](methods/continuity.md) for takeover, modernization, pickup, unattended work, or backlogs. For performance measurements, read Evidence, Numbers; for workflow trials, read [Learning](methods/learning.md), Timing.
