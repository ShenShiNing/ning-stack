# Investigation

Grounding methods: how code works, why it is shaped that way, why a bug happens, and how to compare designs. Questions stay read-only.

Contents: How · Why · Diagnose · Competing designs · Parallel exploration.

## How

Answers "how does X work", "where should this live", "which layer owns this".

- **Simple** (one module, a narrow question): explore and explain in one pass yourself.
- **Complex** (a subsystem across many files or services, a cross-cutting feature): split into two to four angles, each a distinct slice. Hand angles to read-only explorers only when their raw output would crowd your context; otherwise walk them in sequence. Synthesize once.
- When unsure, take the simple path. State your interpretation of a vague scope and proceed; the user can redirect.

Output sections, dropping any that do not apply: **Overview**, **Key concepts**, **How it works** (runtime flow), **Where things live** (`file:line` pointers), **Gotchas**. Senior-engineer onboarding level: a working mental model, not annotated source.

## Why

Answers design rationale, "why did we pick Y", regressions, and data-backed thresholds.

1. **Anchor the code**: paths and line ranges, key symbols, `git blame -L` for last touches, `git log --follow` through renames, PR numbers from subjects, and PR bodies and discussion for substantive commits (`gh pr view <n> --json title,body,comments,reviews`). Trace back past the latest commit; the current shape is usually an accretion.
2. **Scope the search before widening it.** State the question and what would settle it. A narrow why whose anchor already shows a clear rationale (commit message, PR body, ADR, comment) stops there. Widen category by category (issue tracker, docs and ADRs, chat, observability, error tracking, analytics) only while the answer is still open, or when the user asks for a deep historical audit. Record each category searched with its result, searched with nothing, or not searched and why. A null is an answer; an unreachable source is a gap, not a negative.
3. **Defensive code** (retries, timeouts, null guards, flags, rate limits): look specifically for the incident that motivated it.
4. **Write with confidence separated**: What we found (cited), What we can reasonably infer, Competing hypotheses, What we do not know, Sources consulted (one line per category searched, including empty ones).
5. When the question precedes a change, end with **Preserve / Change / Avoid / Risk** constraints.

## Diagnose

For a hard bug or a performance regression. The loop is the method; skip a phase only with a stated reason.

1. **Feedback loop.** Build one command that drives the real bug path and goes red on the user's exact symptom: a failing test at the seam that reaches it, an HTTP script, a CLI with a fixture, a replayed captured payload, a minimal harness, a fuzz loop, a bisection script, a differential run of old against new. Tighten it: faster, sharper assertion, deterministic (pin time, seed randomness, isolate files). Flaky bugs: raise the reproduction rate until it is debuggable. Done when the command is red-capable, deterministic, takes seconds, runs unattended, and you have run it and shown the redacted output. No loop, no theory: if you cannot build one, say what you tried and ask for access, a captured artifact or permission to instrument.
2. **Reproduce and minimise.** Confirm it is the user's failure, not a neighbor. Cut inputs, callers, config and steps one at a time until every remaining element is load-bearing.
3. **Hypothesise.** Three to five ranked, falsifiable hypotheses: "if X is the cause, changing Y makes it disappear". Show the ranking to the user if they are present; do not wait on it.
4. **Instrument.** Each probe tests one prediction; change one variable at a time. Prefer a debugger, then targeted logs at distinguishing boundaries, each tagged with a unique prefix such as `[DEBUG-a4f2]`. For performance, measure a baseline and bisect instead of logging.
5. **Fix and regression test** at a correct seam (see Tests in [evidence.md](evidence.md)): watch it fail, fix at the root cause, watch it pass, re-run the original loop.
6. **Clean up**: original repro green, the tag prefix grepped to zero, throwaway harnesses removed, and the confirmed hypothesis stated in the commit or PR.

Redact every secret in what you show; keep credentials in the environment. After two failed fixes that share one premise, write the premise down and test it directly before a third.

## Competing designs

For a one-way door, a contested shape, or a problem with no precedent. Established patterns skip this.

1. **Frame**: the artifact each candidate produces and a rubric of three to six gradeable criteria for this task (interface depth, locality, seam placement, migration cost, fit with existing patterns, agent-proofness). Candidates see the task, not the rubric.
2. **Generate at least two structurally different whole-shape candidates**, not point variations. With delegation available and worth the cost, give separate candidates the same prompt and separate output locations, ideally on different model families; otherwise draft them yourself, one at a time, each committed to before the next.
3. **Pick a base** by scoring every candidate per criterion, not by feel. A cross-judge on another model family is optional; disagreement with it means a biased pick or an ambiguous rubric, so reread both rationales.
4. **Graft** the one or two strongest parts of the losers by hand so the result keeps one mental model. Convergence is strong agreement: ship the shared shape. Wild divergence means the frame was under-specified: reframe, do not average.
5. **Verify** the result like any artifact.

Output: the chosen design, a short note naming the base and why, each graft and its source, rejections with reasons.

## Parallel exploration

When several independent questions or coverage slices would each fill a context:

1. State the done predicate and what comes back.
2. Choose the shape: partition into slices, or race identical briefs and declare the selection rule (first pass, rank all, best of) before starting.
3. Every brief stands alone: goal, scope, the exact slice, how to verify, what to report. Briefs that verify or measure name the exact SHAs and method, and results must record them.
4. Results report `PASS`, `ISSUES` (every provable issue, not only the first) or `BLOCKED`, with evidence. A missing or unpinned result is retried once, then recorded as a gap. A gap is not a pass.
5. Return one consolidated table, issue one-liners, and gaps.

Writers in parallel each get their own worktree, within the project's concurrency limits. Read-only explorers do not count toward it.
