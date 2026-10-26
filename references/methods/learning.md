# Learning

Improve the environment and this workflow from evidence of real friction: repeated corrections, slow stages, missed checks. One-offs are not lessons.

Contents: Correct · Retro · Timing · Evolving this stack.

## Correct

When the user corrects the same class of mistake a second time, or cleanup finds the same debt twice, make the mistake impossible instead of adding prose.

1. **Find the classes**: read recent commits, reverts, review findings, agent instruction files and workaround comments; group mistakes. A class counts once it has happened twice.
2. **Fix each at the highest level that works**:
   1. Architecture: one owner per piece of state, one supported way per task, internals hidden so the wrong import fails, hand-synced lists replaced by one source, old ways deleted so nobody copies them.
   2. Types: make the bad state unrepresentable.
   3. A lint or check whose error names the file, type or function to use instead; if the pattern is already common, fail only on new additions.
   4. A behavior test (fix or delete tests that pass when behavior breaks or fail when only internals change).
   5. Docs or agent rules last, and only for judgement calls.
3. **Prove** each new check fails on a real past mistake; run the same command locally and in CI. An exception sits on the offending line with a reason, an expiry and a human's approval.
4. Keep a rule-to-enforcer table where the project keeps agent rules. A rule that was already written and still repeated gets an enforcer in the same change; a rule whose mistake can no longer happen is dropped.

Each enforcement change ships through [delivery.md](../delivery.md).

## Retro

When the user asks for a retrospective on a session, or a delivery overran its stages noticeably.

Read the primary sources (the session transcript or thread, PR history, the decision trail) and look for:

- **Navigation**: time lost finding information; would a pointer in an existing doc fix it?
- **Automated checks**: a mistake a lint, type, test or CI check could have caught. Read the repo's existing check commands and CI first: an existing but unwired or broken check is the finding.
- **Coding standards**: a rule the reviewer should enforce, or a stale one to drop. Mechanical rules become checks; only judgement calls go in standards prose.
- **Instruction files**: always-loaded lines that should move to a disclosed doc or a check; no-op instructions that do not change behavior.
- **Tool economy**: expensive or repeated tool calls that a script or better tool would replace.
- **Information access**: something the agent needed but could not see (logs, read-only service access).
- **Workflow stages**: a stage that waited without reducing risk (see Timing).

Present candidates by severity with evidence. Apply nothing to shared skills, instructions or global configuration without the user's approval of the specific edits.

## Timing

"Slow" gets measured before it gets fixed. Attribute time to stages, not to a model by reputation.

Record with `scripts/trail.py`, the same file as the decision trail:

```
trail.py run-start <file> <run>
trail.py start <file> <run> <span-id> <phase>
trail.py end <file> <run> <span-id>
trail.py run-end <file> <run>
trail.py report <file>
```

Spans may overlap, so review and CI waiting can run at once. `report` prints each run's elapsed time and **active wall** time (the union of its spans), then phase totals. Phase totals overlap and do not add up to wall time. Time between runs is never counted. Pass `--at <ISO time with offset>` to record a moment taken from task or CI metadata. Invalid order, negative spans and open runs fail loudly instead of producing a number.

| Phase | Starts | Ends |
| --- | --- | --- |
| `frame` | request received | Stage 0 written |
| `explore` | grounding starts | first edit |
| `write` | first edit | change complete before proof |
| `tests` | test authoring starts | tests written |
| `validate` | first local check | focused proof green |
| `handoff` | brief sent to a child or reviewer | child starts working |
| `child-task` | child starts | child returns |
| `review-wait` | review launched | verdict received |
| `ci-wait` | push | required checks finish |
| `fix` | finding or failure received | fix pushed |
| `merge` | gate evaluation | merged or ready |

Rules for drawing conclusions:

- `child-task` is the delegated task's whole elapsed time, including its own exploration, tool calls, tests and waits. It is not model latency. Attribute time to the model or provider only from usage, tool or SDK timing the harness exposes; otherwise that split is unknown.
- Compare like with like: the same task class and risk class, several tasks per side. One task is an anecdote.
- Report counts too: files read, tests added, checks run, review rounds. A stage can be slow because it did unnecessary work.
- Treat timing comparisons as measurements under [evidence.md](evidence.md), Numbers. No speedup claim without both sides measured.

## Evolving this stack

Change the stack only from evidence: a pattern seen in two or more sessions, a retro finding, or a correction class. A preference stated once and contradicted elsewhere is noise.

- A trivial correction (a stale fact, a sharper sentence) is a direct edit. A new section or method goes through skill-authoring practice: keep `SKILL.md` short, disclose detail by branch, prefer a leading word or a check over more prose, and remove lines that no longer change behavior.
- Update provenance when a method is added, adapted further or dropped.
- Never edit an installed copy in place to work around a problem mid-task; record the friction and fix the stack source.
