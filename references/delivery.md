# Delivery

Take a change from request to its **finish line** with one owner, focused proof, and an independent review that runs beside CI instead of before it.

Contents: Roles · Stage 0 Frame · Stage 1 Ground · Stage 2 Change and prove · Local finish · Stage 3 Publish · Stage 4 Review and CI together · Stage 5 Fix loop · Stage 6 Merge gate · Stage 7 Close out · Waiting · Special entries.

## Roles

- **Request owner**: the thread that received the request. Owns the finish line, the user conversation, ongoing PR supervision and watching, and the merge gate. It reads children's artifacts (diff, proof output, ledger) instead of repeating their investigation or checks, and re-runs something only when the evidence is missing, does not match the head, or does not cover the claim.
- **Slice owner**: one implementer per coherent code slice, from first edit through every review and CI fix of that slice. When the request owner fits the work in its own context, with the right model and an isolated checkout, it is the slice owner. A slice owner never launches reviewers or a review tree of its own.
- **Reviewer**: independent and read-only, a fresh task per round. Method: [methods/review.md](methods/review.md).
- **Runner**: executes supplied commands and reports; it does not diagnose.

Models and effort per role follow the project's instructions; an explicit user choice wins for that task. When a requested model or provider is unavailable, report it and stop that role rather than substituting.

## Stage 0: Frame

Write down, in a few lines:

1. **Acceptance**: the observable behavior that means done, as a falsifiable predicate.
2. **Finish line**: `local` (committed on a branch, reviewed, nothing pushed), `ready` (PR open, merge gate passing, unmerged), or `merged`. Use the user's words; `full stop` means ready and `full send` means merged. Otherwise the project's default, else `ready`.
   - A `full send` or `full stop` request grants, for this task only: pushing and `--force-with-lease` on the task's own branch, and the test methods proof needs without asking first (running the app, browser or device checks, captures); `full send` adds the merge once the gate passes. Rules about how to test still apply. Production changes, data deletion, closing PRs, or touching other branches stay outside the grant.
   - `full stop` never merges, enqueues or enables auto-merge, and never delegates those. Before any push or other work on an existing PR, turn off its auto-merge and remove it from any merge queue; recheck before each push and before handoff, and report what you changed.
   - Under either phrase the user is not watching: stay active through the stages (see Waiting).
3. **Risk class**, which sets proof depth and review budget:
   - **R0 prose**: docs and comments that no test, script, build or config reads.
   - **R1 bounded**: behavior inside a module, or wiring existing public capabilities across modules without changing their semantics, with known and bounded impact.
   - **R2 wide**: changes shared semantics, ownership or contracts; touches auth or security, concurrency or lifecycle, migrations or stored data, or broad tooling (build, test or CI infrastructure); or has unknown impact.
   - Escalate the class the moment a change reaches further than framed; never lower it mid-flight.
4. **Shape of the work**, the throughput checkpoint. Answer each line; `n/a: <reason>` is valid.
   - Blocking first steps (repro, prefactor, migration) that gate everything else.
   - Independent workstreams: disjoint files or artifacts that could run in parallel.
   - Shared mutable state: split the target first; serialize only for a real invariant.
   - Smallest safe decomposition: usually one slice owner. Name why if more.

Split into several slice owners only for real independence: disjoint write sets that each produce a verifiable artifact, a part needing distinct expertise or model, an exploration whose output would swamp the owner's context, or a coverage partition (audits, matrices). Coupled code stays with one owner. Respect the project's concurrency limits. Each split brief stands alone: goal, scope and owned paths, acceptance, proof commands, and a report ending in `PASS`, `ISSUES` or `BLOCKED` with evidence and the head SHA. A missing result is a gap, never a pass.

Delegate the whole slice when the request thread must stay responsive, the work needs another provider, model or settings, or it needs a worktree only a delegate can get. Hand over what is already learned so the owner does not rebuild it: the request verbatim, the frame, file pointers, decisions and their reasons, the finish line, and the PR policy.

Done when the frame is written. For small work it is three lines in the thread, not a document.

## Stage 1: Ground

Work in an isolated checkout the harness owns, branched from the freshly fetched default branch. The user's primary checkout is theirs: no checkout, reset, pull, stash or discard there.

- **Bug**: build a feedback loop that goes red on the user's exact symptom before theorizing ([methods/investigation.md](methods/investigation.md), Diagnose).
- **Feature or refactor**: read the owning code and its callers. Name the data shape and the structure that organizes it (typed model, state machine, table) before writing logic. Reuse the design brief's grounding when there is one.
- **Unfamiliar subsystem**: one `how` pass; add a `why` pass when the change redefines ownership or reverses an old choice.

Done when you can state the seam the proof will cross and the current behavior there, with `file:line` or a red command.

## Stage 2: Change and prove

- Make the smallest change that meets acceptance. Fix the case that happened, not every case that could. Subtract dead weight first when it sits in the way.
- Behavior and logic changes run red to green at an existing seam, one vertical slice at a time ([methods/evidence.md](methods/evidence.md), Tests). A consequential new seam is a decision you report.
- Prove with the **focused set**: the reproduction now green, tests for touched modules, scoped typecheck and lint. R2 adds only the obligations its actual risk touches ([methods/evidence.md](methods/evidence.md), Proof by risk class).
- UI follows the project's design authority. Purely visual changes prove with before and after captures, not tests.
- Stop when acceptance and the risk-class proof are met. Extra tests, comments, guards, options or abstractions each need a current reason a reviewer would accept.

Done when every changed behavior has proof you observed in this session, recorded as commands and outputs.

## Local finish

For the `local` finish line:

1. Commit in coherent units on the task branch.
2. Run review rounds against the local branch (merge-base to the committed head) with the same reviewer brief, budget and ledger as Stages 4 and 5; the slice owner fixes, then re-runs the focused proof the fixes touched.
3. Report: branch and head SHA, acceptance met, proof, review rounds and outcomes, declined follow-ups, unverified items. No push, CI, bot or merge requirement applies.

## Stage 3: Publish

1. Commit in coherent units with the project's message convention. If the branch was cut from a base that has since moved, inspect the base delta first ([methods/evidence.md](methods/evidence.md), Reuse) and rebase only for a conflict, an interaction, or a gate that requires it.
2. Check for an existing PR on the branch. Push, then open a ready (not draft) PR: title per the repository convention and saying why it matters; body opens with the user's problem in plain words, then the change, then evidence; end with the model and harness that wrote it. Scan title, body and attachments for secrets and private details.
3. In T3, whoever creates, takes over or pushes to a PR calls `link_pull_request` as its very next tool call, delegated children included. Ongoing supervision and watching belong to the request owner; children never watch. A child's last line is `PR <url>, head <sha>, checks and reviews <state>`.

R0 prose gets scoped formatter and link checks plus an independent review; any stricter gate the project requires for docs still applies.

## Stage 4: Review and CI together

When the PR head is pushed, start both, pinned to the same head SHA:

- **CI** runs whatever the project's workflow runs for a PR.
- **Review round 1**: a fresh reviewer task with the brief from [methods/review.md](methods/review.md), reading the diff from merge-base to the pinned head. Read-only; it posts on the PR only when the user or project authorizes it.

Then wait for events (see Waiting).

## Stage 5: Fix loop

The slice owner judges each event against the source:

- **Review finding**: agree and fix with the smallest change (prefer deleting or narrowing), disagree with evidence, or decline as nit or out of scope in one line.
- **CI failure**: tell a product failure from an infrastructure flake. Rerun a flake once; fix a product failure with a reproduction.
- **Bot or human comment**: same as a review finding.

Every unresolved finding stays in the ledger until it is fixed, answered with evidence, or shown obsolete against the current head. Timestamps only deduplicate notices; a new push never closes an older real issue.

Batch the fixes from one round with any CI fixes into one push. Then:

- CI re-runs on the new head.
- A new review round starts only when a blocker or should finding is open, or the fix changed behavior the last verdict did not cover. It covers the changed hunks and open finding ids. Comment, format and declined-nit fixes need no round.
- Re-run locally only the checks whose inputs the fix changed. A fix that reaches a new area re-frames its risk class.

When review growth exceeds the intent, cut back before pushing.

## Stage 6: Merge gate

Evaluate on the latest head SHA after a fresh fetch, every time; a wake is news, not a decision.

1. Proof covers every behavior change in the final diff.
2. The latest review verdict covers the current behavior diff, with no open blocker or should. A verdict or local proof from an earlier head carries over only under [methods/evidence.md](methods/evidence.md), Reuse.
3. Every required check is green on this head. A green run on an earlier head never stands in for current-head checks the project requires.
4. Every ledger entry is resolved; no human review requests changes.
5. Not conflicting. If behind, inspect the base commits since the last green run: when they touch the PR's files, dependencies, contracts or shared resources, rebase, push and go back through Stage 5. Follow any project rule that requires up to date.
6. Merge through the repository's configured method and gates, never a bypass, with the head SHA pinned (`--match-head-commit` or equivalent).

Then by finish line:

- `merged`: merge, confirm the merged state, close out.
- `ready`: leave it open with no auto-merge; report ready, waiting on a named human approval, or blocked with what was tried.
- An unmet gate you cannot fix: ask through the harness question tool with the PR link, blocker and options with a recommendation. Without a question tool, leave the PR unmerged and lead the reply with the question.

Before handing back or asking, unwatch every PR this thread watches.

## Stage 7: Close out

Clean up only this task's worktree and branch, never the primary checkout or shared resources. Report: PR link and merge commit (or ready verdict), proof, review rounds and outcomes, decisions made for the user, declined follow-ups, anything unverified.

## Waiting

Wait on events the active harness supports: its PR watcher (T3 `watch_pull_request`, owner thread only) and child completion notices. Where the harness has no watcher, query PR and check state yourself only at points the harness allows (on a wake, after a push, before deciding), never in a loop. If neither exists, hand back with a precise blocker: what is pending, on which head, and what to check next. Never build a polling loop, a sleep, or a helper agent to watch CI.

## Special entries

Read [methods/continuity.md](methods/continuity.md) for these and return at the stage they name.

- **Takeover** of a PR, branch or agent thread: credit preserved, handoff treated as context, resumes at Stage 1.
- **Modernize** an old PR: disposition first (modernize, rework, close), resumes at Stage 3 or stops at a recommendation.
- **Pickup** after a pause or compaction: resume point from the trail, no redo.
- **Unattended or long run**: keep a decision trail and stay active until the finish line or a real blocker.
- **Measured performance or metric work**: the improvement loop in [methods/evidence.md](methods/evidence.md), Numbers, inside Stage 2.
