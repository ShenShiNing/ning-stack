# Continuity

Read the section for the transition at hand. Reuse existing artifacts rather than rebuilding their history.

## Continue

For multi-task or multi-session work, keep remaining outcomes, blocking dependencies, owners, worker handles, and evidence pointers in existing progress records. Refer to the runtime's live task state rather than copying it into a second registry. Give bounded execution tasks an outcome they can finish; the request owner keeps whole-goal acceptance and cross-task decisions.

After a result or context recovery, reconcile what is ready, active, returned but unaccepted, accepted, or blocked. A completed run is a returned result; accept its outcome only after checking the artifact and required proof. Tests or other checks still running remain pending work with an owner and a recoverable handle.

Before waiting or closing out, account for every unfinished outcome. Continue authorized, unblocked work within resource and harness turn-ending rules; a blocked workstream leaves independent work runnable. Stop at the agreed finish line, explicit pause, or genuine blockers, naming any partial completion and remaining gaps.

For each external wait, verify the supported resume trigger and who receives its result before claiming automatic continuation. An ended runner is not a subscription. If no supported trigger exists, report the exact pending condition, manual resume action, and automatic-continuation gap; keep independent work moving where permitted. Scheduling, polling, and recovery actions retain their existing authorization limits.

## Decision trail

Use existing progress notes for decisions and evidence pointers. When an append-only or measured record is useful, `scripts/trail.py` writes TSV: `run-start`, `note`, and `run-end`. Timing spans use [Learning](learning.md), Timing.

In a trail, log consequential forks, verified units, pivots/reverts, and blockers, not every action. Append corrections; each new session or owner starts a new run naming inherited runs. Keep logs outside the repo in the project's artifact location. Before handoff, confirm entries describe real actions and evidence resolves. A trail preserves context; it does not establish correctness by itself.

## Pause and Handoff

On explicit pause, start no new work and bring owned execution to a safe preserved boundary under the user's stop instructions. Preserve task edits and label incomplete work; keep active work in its current checkout.

When replacing an owner, the old owner stops accepting work, preserves WIP and pending checks, and accounts for every owned writer. The successor starts writing only after old writers are confirmed stopped or explicitly transferred with a single owner. If the old owner is unavailable, verify actual task and checkout state; unresolved writer ownership remains a handoff gap. Context compaction alone preserves live worker handles and pending results, without stopping or relaunching them.

Leave a short note outside the repo: intent, branch/worktree, decisions, verified/open items, active tasks and pending results, next action and flow/stage, and artifact pointers. Redact sensitive data. Report what is durable and where the next session starts.

## Pickup

Read the resume note, recent decision points, and relevant source. Reconcile branch, diff, landed commits, open findings, worker results awaiting acceptance, and next runnable units; name the resume point and apply Continue. Do not repeat completed investigation. Inherited claims used at a gate must resolve to real evidence and pass [Evidence](evidence.md), Reuse on the current head/base. Route remaining work to its flow.

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
