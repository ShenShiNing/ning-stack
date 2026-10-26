# Review

One independent reviewer per round, fresh and read-only, on the user/project model (another family when available). No edits, commits, pushes, comments, or subagents. Each round starts a new reviewer task rather than messaging a previous reviewer.

## Standard round

Give the reviewer the repo, base and head SHAs, intent, acceptance, scope exclusions, risk class, applicable standards, existing proof, and CI state. It reads the diff and surrounding callers and reports:

```
VERDICT: APPROVE or CHANGES
## Spec
S1 [blocker|should|nit] file:line — missing, incorrect, or unrequested behavior; suggested fix.
## Standards
T1 [blocker|should|nit] file:line — violated rule or labelled design judgement; suggested fix.
```

Standards include correctness and the project's documented rules. Skip what tooling already enforces. Look for unnecessary tests, comments, compatibility, guards, and abstraction; assess names, duplication, coupling, scattered ownership, and shallow pass-through modules against current needs.

Severity follows impact on valid behavior, not frequency: **blocker** breaks the intended case or reachable security, authorization, data integrity, concurrency, or resource safety; **should** is a real bug valid callers can hit; **nit** is style, speculative hardening, or minor cost.

## Findings and stop

The slice owner verifies every finding. Agree and make the smallest fix, disagree with evidence, or decline a nit or unrelated scope with a reason. Preserve a row per finding (id, severity, outcome, evidence); create no empty ledger. An unresolved older finding survives a new push. Report a real out-of-scope risk as a follow-up.

A new round gets the ledger, responses, changed hunks, and any new base interaction; review only open findings and behavior the previous verdict did not cover. Mark old ids resolved or still open with reasons. Comment and format edits alone need no new round.

Stop on an approval covering the current behavior with no unresolved blocker or should; nits alone do not require another round. Three rounds is a ceiling, not a target. Up to five for concrete security, auth, data-loss, concurrency, or state risks while a real finding remains, or on request. After two unresolved exchanges or the budget, present the disagreement for the user's decision. Exhaustion, errors, timeouts, and silence are not approval; cancel a failed run before replacing it with a fresh task.

## Interrogate

Use for a contested design or high-cost change when two model families are available. Send the same intent, diff or sketch, and constraints to independent read-only reviewers. Merge duplicates, note agreement, and judge each finding: act, consider with the user, note for later, or dismiss with evidence. Present the verdict; do not auto-apply a panel's proposals.

## Council

Only on explicit request or a user-designated decision class. Three strong models from three providers, using named members first; report unavailable members rather than substitute. Keep scope fixed. For code reviews collect scores out of ten (or no score), useful findings, disagreements, and next steps. A fix gets a fresh round. If there is a PR, keep per-round scores in its description.

## Posting on a PR

Post only when authorized. Comments written for the user start with:

```md
> [!NOTE]
> 🤖 **<verified model or harness> responding on behalf of <user>**

<Conclusion, evidence, and reply>
```

Check facts, private details, and rendered Markdown; confirm the returned URL before resolving a thread. Descriptions and commit messages need no callout.
