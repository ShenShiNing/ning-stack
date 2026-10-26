# Cleanup

Remove real debt against explicit current standards, with evidence for every deletion, and ship it through delivery.

Contents: Scope · Standards · Find candidates · Evidence per class · Decide · Ship · Recurring classes.

## Scope

Take the area the user names. Otherwise pick hotspots: walk a good stretch of `git log` for files and directories that keep changing, and weight recent churn, because cleanup pays back where the next changes land. State the scope and a budget (number of candidates or PRs) before scanning.

## Standards

Cleanup measures against written, current standards, never taste. Collect them first and cite them per finding:

- The project's coding standards and agent instructions, architecture documents and active ADRs.
- Reference projects the project names, compared at a recorded revision.
- Tool output the project already runs (unused-code gates, lint, typecheck, test scope tools).

A standard that is itself stale or wrong is an optimization finding, not something to silently bypass.

## Find candidates

- **Dead code**: unused exports, files, branches, flags, parameters, compatibility layers for removed data (pre-launch projects get a hard cut, not shims), and duplicate ways of doing one thing.
- **Comments**: narration that restates code, outdated explanations, commented-out code, phase markers in scripts, stale TODOs, and lint or type suppressions.
- **Tests**: dead tests nothing runs, implementation-coupled tests (mock internals, assert private shape, verify through a side channel), tautological tests (expected value recomputed the way the code does), and the same assertion repeated across layers.
- **Docs and instructions**: lines that no longer change behavior, restate the environment, or contradict current code.

## Evidence per class

Get each deletion's safety fact as far down the confidence ladder ([methods/evidence.md](methods/evidence.md), Ladder) as is cheap, and record where it stopped.

**Code.** No caller by symbol search, plus the places search misses: string and dynamic references, config, generated code, routes, public packages, scripts, wire formats and stored data, indirect test inputs. Prefer the project's unused-code tool output. If the code looks intentional but unused, read its history (`why` method) before deleting: a planned feature in flight is not dead.

**Comments.** Keep a comment that carries a real constraint the code and types cannot express: a non-obvious why, an external or legal obligation, a tooling directive, a public-contract note. Delete narration and restatement. A comment claiming a constraint (`do not remove`, `must stay in sync with X`) gets checked: if the constraint is real and cheap to encode as a type, test or lint, offer that encoding; otherwise keep it. When intent stays ambiguous after a history check, keep it and list it as open rather than deleting on doubt. A suppression that hides a correctness or safety issue is a finding to fix, not a comment to tidy.

**Tests.** Classify before touching:

- Delete: dead tests nothing runs, assertions on pure shape or private structure, tautologies, and exact duplicates of an assertion kept at a higher seam.
- Rewrite: a test that guards real behavior through the wrong seam. Move the assertion to the interface first, then remove the old test, so unique coverage never drops.
- Keep: unique live behavior coverage, and any regression, concurrency, authorization or failure-path test whose value is uncertain but whose miss would be costly. Doubt keeps it.

Mutation or negative proof (break the behavior in a disposable copy of the workspace, never the working source, and confirm which tests go red) only when a consequential deletion is still uncertain after reading. Never for every deletion.

## Decide

Present the candidate list grouped by class, each with its standard, its evidence level, and a verdict: delete, rewrite, encode, keep-with-reason, or open. Deletions with level 3 or better evidence and no product effect proceed under the user's cleanup request. Anything that changes observable behavior or a public contract goes back to the user first.

Done when every candidate in scope has a verdict, or the budget is spent and the remainder is listed.

## Ship

Each cleanup PR has one theme so review stays fast. Go through [delivery.md](delivery.md) as R1, or R2 when deletions touch shared infrastructure, test setup, public contracts or data. The PR body lists each deletion with its evidence pointer and the kept-with-reason items.

## Recurring classes

When the same class of debt shows up twice, remove the cause, not just the instances: the levels and proof rule are in [methods/learning.md](methods/learning.md), Correct.
