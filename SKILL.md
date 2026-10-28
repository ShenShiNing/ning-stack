---
name: ning-stack
description: Compose engineering methods for investigation, design, delivery, review, verification, cleanup, architecture, and handoffs.
---

# ning-stack

Build complex things as simply as possible. One owner carries each outcome; independent review and evidence earn the finish.

Use a method for a focused request or combine the four flows for end-to-end work. Execution, delegation, and monitoring follow the active environment.

## Project rules

Read the project's `AGENTS.md` / `CLAUDE.md` and the references relevant to this task. They supply product constraints, design authority, architecture, safe environments, commands, model roles, and merge policy.

Apply harness and tool rules, then the user's task instructions, then project rules, then this stack. Identify a conflict when it changes the route. Existing authorization carries forward; this skill grants none. Optional project preferences belong in a short `ning-stack` section of `AGENTS.md`.

## Route

Choose by the requested outcome. Read a method directly for a focused request; load a flow for end-to-end work and follow only its relevant pointers.

| Request | Read |
| --- | --- |
| Explain or investigate a question | [Investigation](references/methods/investigation.md); answer read-only |
| Review a diff or assess a contested decision | [Review](references/methods/review.md); read-only |
| Assess tests, blast radius, measurement, or reusable proof | [Evidence](references/methods/evidence.md) |
| Prototype an unsettled behavior or interface | [Design, Prototype](references/design.md#prototype) |
| Decide a new capability's behavior | [Design](references/design.md) |
| Ship a feature, fix, refactor, or PR | [Delivery](references/delivery.md) |
| Remove dead code, stale comments, excess tests, or other debt | [Cleanup](references/cleanup.md) |
| Reassess logical or physical architecture | [Optimization](references/optimization.md) |
| Resume, hand off, take over, or triage a backlog | [Continuity](references/methods/continuity.md) |
| Diagnose workflow friction or measure delivery | [Learning](references/methods/learning.md) |

Design produces the brief delivery consumes. Cleanup and optimization ship through delivery.

## Shared decisions

- Look up facts yourself. Bring consequential product, ownership, and irreversible choices to the user together, with a recommendation. Decide reversible details yourself. Reuse settled decisions and seams.
- Show proof from the real artifact; distinguish observation from inference and uncertainty.
- A step, test, comment, abstraction, or option must address a current risk or reduce existing complexity. Decline work that does neither.
- Use existing progress notes, commits, check output, and PRs as records. Create a separate spec, checklist, ledger, or trail only when its flow needs one.
- Report the finish-line state, evidence, consequential decisions, and remaining gaps.

## Sources

Adapted from Matt Pocock's skills, Lauren Tan's pstack, and Theo Browne's tstack. Read the [source map](docs/provenance.md) only when updating the stack or checking attribution.
