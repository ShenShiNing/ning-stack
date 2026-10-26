# Continuity

Keep work coherent across time, agents and sessions: trails, long runs, pause and pickup, handoff, takeover, old PRs, and backlogs.

Contents: Decision trail · Long or unattended run · Pause · Pickup · Handoff · Takeover · Modernize · Backlog.

## Decision trail

A tab-separated log, one row per decision, for unattended, long, multi-phase or measurement work. Skip it for ordinary attended tasks.

- Write it only with `scripts/trail.py` from this skill: `run-start <file> <run>`, then `note <file> <run> <phase> <decision> <why> <evidence> <result>` per decision, and `run-end` when the run stops. It stamps the time, validates event order, keeps cells single-line and neutralizes spreadsheet-formula prefixes. Evidence is a pointer (SHA, PR, `file:line`, artifact path), never prose.
- Log forks taken, units completed with their verification result, pivots and reverts with the trigger, blockers, fixed gates. Not every action.
- Append-only: a wrong note is superseded by a new note, never edited. A pickup, replacement agent or new session opens its own run id, and its first note names the runs it did not write.
- Keep it out of the repository in the working directory or the OS temp directory. Attach or commit it only when a reviewer needs it to trust ambitious work.
- Before handing back, walk your rows against what actually happened: each maps to a real action, each evidence pointer resolves, and any unlogged fork that shaped the work is added.
- For high-stakes runs, if a second model family is available, have it read the trail and flag weak evidence, skipped verification and risky choices. The reply then ends with an Attention section naming that reviewer.
- Stage timing for workflow measurement uses the same log; see [learning.md](learning.md), Timing.

## Long or unattended run

For work the user steps away from, a multi-hour run, or a task no flow fits cleanly.

1. **Frame**: done as a falsifiable predicate, scope quantified (units and rough effort), rigor level biased high for one-way doors and wide blast radius. Present the framing once before a multi-hour run; reversible work proceeds without waiting.
2. **Design the run**: atomic units that each land independently, riskiest unknown first, verification harness and baseline before the work, fan-out only across real seams. Write the unit list down; it is what the user reviews.
3. **Loop**: each unit is an experiment. Hypothesis, smallest change, measure against the predicate on the real artifact, keep or revert, log a row. Verify each unit before the next.
4. **Hand back**: whole result checked against the predicate on the real product, the trail path, verified versus open items, and any recurring correction encoded as a check.

Stay active until the finish line or a real blocker; wait on watchers, not by ending the turn. Pause only on an explicit request.

## Pause

Only on an explicit pause, going offline, a restart, or imminent compaction. "Keep going" means do not pause.

1. Stop at a safe boundary: finish or back out of the current atomic step; start nothing new; cancel nested work you started.
2. Take no irreversible action to pause (no new PR or push unless one already exists).
3. Make it durable: commit uncommitted edits on the task branch as one `wip:` commit; note a broken tree in its body.
4. Write a resume note outside the repository: intent, progress and what is verified, current state, next steps, key files, gotchas, and a pointer to the trail if one exists.

Reply with where the loop stands, what is on disk versus only in context, the commits made, and the first action on resume.

## Pickup

Resuming your own or another agent's paused or compacted work.

1. Locate the trail: resume note, transcript, thread, branch or PR. Read the last messages and decision points first; parse a long transcript in a subagent when it would crowd your context.
2. Reconstruct state: branch and worktree, what landed (`git log`, diff against base), open items, decisions made. The trail is authoritative input; do not re-derive it.
3. Name the resume point. Do not re-run completed work or the prior repro from scratch.
4. Route the remainder to its flow and stage.
5. Before relying on an inherited claim at a gate, check it on the real artifact at the current head; a prior self-report is context, not proof.

## Handoff

When another session will continue. Write a note outside the repository: what the next session is for, the state, decisions, next steps, which flow and stage to resume at, and pointers to existing artifacts (issues, PRs, specs, commits) instead of copies. Redact secrets and personal data.

## Takeover

Taking over a PR, branch or agent thread to finish its goal.

- Read the source: PR, branch or thread, review findings, and the user's later corrections. Resolve it to the actual code at the current head, including uncommitted work. The handoff is context, not proof, and the existing implementation earns no defense.
- For a replacement PR, import the original commits onto a new branch and add fixes as separate commits. Honor an explicitly requested in-place or stacked continuation. Do not change the original PR or unrelated work without authorization.
- Preserve git authorship and co-author trailers; credit original contributors in the PR description and link the original PR. If it will be squashed, keep human credit in the merge commit with verified identities. Model attribution does not replace contributor credit.
- Modernize against the current base (below), simplify without dropping intended behavior, recheck the source PR for updates, and verify the original failure and realistic workflows independently.
- Continue in [delivery.md](../delivery.md) at Stage 1. Merge or close the original only when authorized. Report what was inherited, changed, verified and credited.

## Modernize

Updating an old PR: modernize the idea, not just the branch.

1. Record the PR's URL, state, base, head, author, checks and reviews; read body, issues, commits, threads and the full diff; state the smallest coherent goal it pursued.
2. Fetch the latest base and head; record the merge base. Inspect what landed on the base since divergence and search for competing or replacing PRs. Ask: already solved? APIs, types, schemas or boundaries changed? Ownership now claimed twice? Code deleted or simplified on purpose? Would landing it restore old behavior or create a second way? Is the benefit still worth the cost? No conflicts is not currency.
3. Choose a disposition before pushing anything:
   - **MODERNIZE**: goal useful, shape right. Rebase on a safe branch or disposable worktree, resolve conflicts by current intent and the base's newer invariants, compare with `git range-diff`, run focused checks, push with `--force-with-lease` against the observed head.
   - **REWORK**: goal useful, shape wrong. Describe the smallest credible rewrite and stop unless rework was requested.
   - **CLOSE**: superseded, obsolete or not worth its cost, with concrete evidence. Never close without permission.
4. Report the disposition first, then base changes, conceptual conflicts, push result, checks, and the remaining decision. Never merge as part of modernizing.

## Backlog

Only when the user asks to work an issue backlog or a single issue.

- For each item: read it fully including prior triage notes; check redundancy (search for an existing implementation by domain concept, report where you looked) and prior rejection; verify the claim (reproduce a bug) before shaping it.
- Recommend a category (bug, enhancement) and a state (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix) with reasons, and wait for direction. An explicit state override from the user is applied directly.
- A ready-for-agent outcome carries an agent brief: current behavior, desired behavior, acceptance criteria, key interfaces, out of scope, all durable (no line numbers). Needs-info carries what is established and specific questions.
- Posting comments, labels or closures needs the user's authorization; posted text opens with a line saying it was AI-generated during triage. The project's tracker conventions map state names to real labels.
