# Continuity

Read the section for the transition at hand. Reuse existing artifacts rather than rebuilding their history.

## Decision trail

For unattended, multi-phase, or measured work, use `scripts/trail.py` to record decisions with evidence pointers; ordinary attended work needs no trail. It writes TSV: `run-start`, `note`, and `run-end`. Timing spans use [Learning](learning.md), Timing.

Log consequential forks, verified units, pivots/reverts, and blockers, not every action. Append corrections; each new session or owner starts a new run naming inherited runs. Keep logs outside the repo in the project's artifact location. Before handoff, confirm entries describe real actions and evidence resolves. A trail preserves context; it does not establish correctness by itself.

## Long or unattended run

State acceptance, scope, and independently verifiable units once. Start with the riskiest unknown and use a baseline when claiming an improvement. Verify each unit, keep or revert it, and record why. Split only across real seams. Finish by checking the whole outcome, listing verified and open items, and linking the trail.

Continue until the finish line or a real blocker. Follow harness completion events and required turn-ending behavior; use no polling helpers.

## Pause and Handoff

On an explicit pause or a required session transition, reach a safe boundary and start no new work. Stop nested work you own if pausing. Preserve task edits in a task-branch commit, labelling an incomplete tree; pause itself grants no permission to publish.

Leave a short note outside the repo: intent, current branch/worktree, decisions, verified/open items, next action and flow/stage, artifact pointers, and gotchas. Redact sensitive data. Report what is durable and where the next session starts.

## Pickup

Read the resume note, recent decision points, and relevant source. Reconcile branch, diff, landed commits, and open findings; name the resume point. Do not repeat completed investigation. Inherited claims used at a gate must resolve to real evidence and pass [Evidence](evidence.md), Reuse on the current head/base. Route remaining work to its flow.

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
