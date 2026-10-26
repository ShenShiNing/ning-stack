---
name: ning-stack
description: Ning's engineering workflow for design, end-to-end delivery, debt cleanup, and architecture reassessment. Use when specifying or shipping work, driving a PR, cleaning a codebase, reviewing its architecture, or resuming a task.
---

# ning-stack

Build complex things as simply as possible. One owner carries each outcome; independent review and evidence earn the finish.

## Project rules

Read the project's `AGENTS.md` / `CLAUDE.md` and the references relevant to this task. They supply product constraints, design authority, architecture, safe environments, commands, model roles, and merge policy.

Apply harness and tool rules, then the user's task instructions, then project rules, then this stack. Identify a conflict when it changes the route. Existing authorization carries forward; this skill grants none. Optional project preferences belong in a short `ning-stack` section of `AGENTS.md`.

## Route

Read the matching flow and follow its conditional pointers; other methods stay unloaded.

| Request | Read |
| --- | --- |
| Explain or investigate a question | [Investigation](references/methods/investigation.md); answer read-only |
| Decide a new capability's behavior | [Design](references/design.md) |
| Ship a feature, fix, refactor, or PR | [Delivery](references/delivery.md) |
| Remove dead code, stale comments, excess tests, or other debt | [Cleanup](references/cleanup.md) |
| Reassess logical or physical architecture | [Optimization](references/optimization.md) |
| Resume, pause, hand off, take over, or work unattended | [Continuity](references/methods/continuity.md) |
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
