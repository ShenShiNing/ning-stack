# Review

Independent review that finds real defects in the intended case and fights scope growth. One reviewer per round by default; heavier panels only when their trigger holds.

Contents: Standard round · Brief · Answering findings · Budget and stop · Interrogate · Council · Posting on a PR.

## Standard round

Used by delivery Stage 4 and every later round.

- The reviewer runs on the reviewer model the user or project names (a different model family from the implementer when available), as a fresh task each round, read-only: no edits, commits, pushes, PR comments or subagents. In T3 that is a new `delegate_task` per round; never a message to an earlier review thread.
- It reads the diff from the merge-base to the pinned head SHA, the surrounding code, and the brief. It covers two axes in separate sections, so one cannot mask the other:
  - **Spec**: what acceptance asked for that is missing, partial or wrong; behavior nobody asked for.
  - **Standards**: violations of the project's documented standards (cite the rule), plus the smell baseline as labelled judgement calls. A documented project standard overrides the baseline. Skip what tooling enforces.
- Smell baseline: mysterious name, duplicated code, feature envy, data clumps, primitive obsession, repeated switches, shotgun surgery, divergent change, speculative generality, message chains, middle man, refused bequest.

## Brief

Children get no history, so the brief stands alone:

```
Review only. Do not edit, commit, push, comment on the PR, or start subagents.
Repo: <path or URL>  Base: <merge-base sha>  Head: <head sha>
Intent: <one or two sentences>  Out of scope: <list>
Acceptance: <predicate>  Risk class: <R0|R1|R2>
Standards: <the project's standards files>
Proof so far: <commands and results>  CI: <state at launch>
Read: git diff <base>..<head> and surrounding code.
Find bugs, broken callers and mismatches with intent. Flag code, tests or guards the intent does not need.
Severity by impact on valid behavior and invariants, not by frequency: blocker = the intended case is wrong, or any reachable path can break authorization, security, data integrity, concurrency or resource safety; should = a real bug valid callers can hit; nit = style, speculative hardening, unneeded compatibility, small cost.
Reply:
VERDICT: APPROVE or CHANGES
## Spec
S1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion>
## Standards
T1 [blocker|should|nit] <file>:<line> <rule or smell>. Fix: <suggestion>
```

Later rounds add the ledger and the change since the last round, and ask for open ids and changed code only, each old id marked `resolved` or `still open: <reason>`.

## Answering findings

The slice owner checks each finding and its severity against the source. Severity follows impact: a rare path that breaks authorization, data, concurrency or resource safety still blocks; a cosmetic or speculative concern is a nit whatever its label. Scope stays fixed: a real risk outside the intent becomes a named follow-up, not silence.

- **Agree**: smallest fix; prefer deleting or narrowing over a new lock, cache, helper or option. One focused failing-then-passing test if the intent needs it.
- **Disagree**: the reason with evidence (`file:line`, test, output).
- **Decline**: out of scope or nit, one line, listed as a follow-up.

Keep a ledger row per finding: id, severity, outcome, evidence. Never agree just to end the loop. Review bots and the project's agentic reviewers get the same treatment: they catch real bugs and also file noise.

## Budget and stop

- Three rounds by default. Up to five for security, permissions, auth, data loss or state and concurrency while a blocker or should stays open with evidence, or when the user asks.
- Stop early when a round returns only nits.
- **Agreed**: APPROVE on the current behavior diff, nothing open at blocker or should, no concern of the owner's own.
- **Stuck**: a finding disputed after two exchanges, or budget spent. Show both sides in two or three lines each; the user decides. Budget end is not approval.
- A timeout, an error or no reply is not approval. Cancel, confirm it stopped, and start a fresh round with the ledger.

## Interrogate

For a contested design or a high-cost change before shipping, when reviewers on at least two model families are available.

1. Write the intent in one paragraph. If intent is unclear, ask the user first.
2. Give each reviewer the same brief, diff or sketch, and context, in parallel, read-only. Diversity comes from different model families, not assigned personas.
3. Merge findings that describe the same issue, noting which reviewers raised each. Independent agreement is the strongest signal.
4. Judge as the lead, not an aggregator. Each finding goes to **Act on** (blocks a real PR), **Consider** (legitimate, cost unclear, the user's call), **Noted** (valid, not actionable now) or **Dismissed** (wrong or missing context, with the reason). Close with an agreement map.

Deliver the verdict; do not auto-apply.

## Council

Only when the user says `council` or has designated it for a decision class. Three delegates, one strong model from each of three providers (the user's named members first), read-only, with the request and context. If three providers are not reachable, or a named member is unavailable, report it instead of substituting. For a code review ask each for a score out of 10 and record `no score` when none is given. Summarize useful findings, disagreements and next steps; a fresh review after fixes is a new round. Keep scope fixed across rounds. If the work has a PR, put the per-round score table in the PR description, never a comment.

## Posting on a PR

Only when the user or project authorizes posting. Every comment written on the user's behalf opens with a note callout, attribution inside, reply outside:

```md
> [!NOTE]
> 🤖 **<verified model name, or the harness name> responding on behalf of <user>**

<conclusion first, then the cited code, check or reproduction>
```

Separate verified fact from judgement, check the whole comment for secrets and private details, preview the Markdown, and confirm the returned comment URL. Resolve a thread only after its reply posted. PR descriptions and commit messages take no callout.
