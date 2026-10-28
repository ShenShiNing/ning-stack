# Continuity

Read the section for the transition at hand. Reuse existing artifacts rather than rebuilding their history.

## Decision trail

For unattended, multi-phase, or measured work, use `scripts/trail.py` to record decisions with evidence pointers; ordinary attended work needs no trail. It writes TSV: `run-start`, `note`, and `run-end`. Timing spans use [Learning](learning.md), Timing.

Log consequential forks, verified units, pivots/reverts, and blockers, not every action. Append corrections; each new session or owner starts a new run naming inherited runs. Keep logs outside the repo in the project's artifact location. Before handoff, confirm entries describe real actions and evidence resolves. A trail preserves context; it does not establish correctness by itself.

## Long or unattended run

Keep whole-goal acceptance and a task graph in existing durable records: verifiable units, blocking edges, claims/worker handles, and evidence pointers. Reuse harness task state; a ready unit is unblocked and unclaimed. Start with the riskiest unknown; use baselines for improvement claims.

Claim and dispatch the ready frontier within project concurrency limits using fresh workers and [Delivery's briefs](../delivery.md#stage-0-frame). Serialize conflicting writes; reuse workers only for needed live state. Communicate through artifact pointers and concise completion reports; steer only changes affecting active work.

Verify artifacts before marking a unit done, update dependencies, and dispatch newly ready work. Recover failed/stalled units from evidence. Account for in-flight work and unaccepted results before waiting or concluding; avoid status pings and interrupt-resume chains.

Use supported completion/recovery wakeups within authorization and required turn-ending rules; no improvised pollers. If unavailable, report the resume trigger and recovery gap. Continue until verified whole-goal completion or explicit pause. With no ready units, wait for in-flight work or replan; report genuine blockers and link the trail.

## Pause and Handoff

On an explicit pause, reach a safe boundary, start no new work, and stop nested work you own before preserving task edits in a task-branch commit; label an incomplete tree. A session transition alone preserves active worker handles and the supported resume trigger without changing a live worker's checkout. Neither grants permission to publish.

Leave a short note outside the repo: intent, current branch/worktree, decisions, verified/open items, next action and flow/stage, artifact pointers, and gotchas. Redact sensitive data. Report what is durable and where the next session starts.

## Pickup

Read the resume note, recent decision points, and relevant source. Reconcile branch, diff, landed commits, open findings, worker results awaiting acceptance, and next runnable units; name the resume point. Do not repeat completed investigation. Inherited claims used at a gate must resolve to real evidence and pass [Evidence](evidence.md), Reuse on the current head/base. Route remaining work to its flow.

## Takeover

Read the original request, PR/thread, findings, later corrections, and actual code including uncommitted work. Preserve intended behavior, not an inherited implementation by default.

For a replacement PR, import original commits and add fixes separately; honor an explicitly requested in-place or stacked continuation. Preserve authorship and co-author trailers, credit contributors and link the original, retaining verified human credit through a squash. Do not alter or close the original without authorization.

Check the current base and competing work as in Modernize. Independently verify the original failure and relevant workflows, then resume [Delivery](../delivery.md) at Stage 1. Report inherited, changed, verified, and credited work.

## Modernize

Read the old PR's intent, author, head/base, discussion, findings, and diff. Fetch current refs and inspect intervening changes to contracts, ownership, schemas, and dependencies; check whether the work is already solved or would restore something deliberately removed.

Choose before pushing:

- **Modernize:** goal and shape remain useful. Update on a safe branch, resolve by current intent, compare range-diff, prove affected behavior, and use `--force-with-lease` against the observed head when authorized.
- **Rework:** goal useful, shape obsolete. Propose the smallest rewrite; implement only if authorized.
- **Close:** superseded or not worth its cost. Give evidence; close only if authorized.

Report disposition, conceptual conflicts, proof, and remaining decisions. Modernization alone does not authorize merging.

## Backlog

For requested triage, read each issue and prior decisions, search for an existing solution or duplicate, and verify its claim. Recommend category/state with evidence. A ready item needs acceptance, key interfaces, exclusions, and current/desired behavior; a needs-info item needs established facts and specific questions. Use durable concepts, not line numbers.

Follow explicit state overrides; otherwise confirm the proposed triage disposition before changing tracker state. Posting, labels, and closures require authorization and project conventions, including AI attribution. An already assigned implementation follows delivery rather than asking for triage approval again.
