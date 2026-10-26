---
name: ning-stack
description: Ning's engineering workflow for designing new capabilities, delivering code changes to a local, ready-PR or merged finish line, cleaning up debt (dead code, comments, excess tests), and reassessing architecture. Use when building or fixing something end to end, specifying work, driving or taking over a PR, running a cleanup, reviewing architecture, or resuming paused work.
---

# ning-stack

Build complex things as simply as possible. Every outcome has one **owner**, every claim has **evidence**, review is independent, and a step stays on the critical path only while it reduces a real risk.

## Project rules

Read the project's always-loaded instructions (`AGENTS.md`, `CLAUDE.md`) and the docs they point to for product and environment constraints: checkout and data safety, design authority, architecture rules, check commands, CI and merge conventions, model roles. This stack supplies the methods; the project supplies those facts.

Precedence, highest first: harness and tool rules, the user's explicit instruction for this task, the project's rules, this stack. When a project rule conflicts with a step here, follow the rule and say which one governed. A project may add a short `ning-stack` section with preferences (default finish line, reviewer model, focused and broad check commands); without one, use the defaults here.

## Route

| Request | Read |
| --- | --- |
| A question: how, why, should we, can X do Y | [methods/investigation.md](references/methods/investigation.md). Answer read-only; offer a change instead of making it. |
| A new capability, or behavior nobody has decided yet | [design.md](references/design.md) |
| A change to ship: feature, bug, refactor, PR work, takeover, rebase of an old PR | [delivery.md](references/delivery.md) |
| Remove debt: dead code, stale comments, redundant tests, sediment docs | [cleanup.md](references/cleanup.md) |
| Reassess logical or physical architecture | [optimization.md](references/optimization.md) |
| Resume, pause, hand off, run long and unattended, or work a backlog | [methods/continuity.md](references/methods/continuity.md) |
| Repeated corrections, workflow friction, stage timing | [methods/learning.md](references/methods/learning.md) |

Read only the row that matches. Flows chain: design ends in a brief that delivery consumes, and cleanup and optimization ship through delivery. Each flow file names the method files it needs and when.

## Shared rules

- **Facts are the agent's, decisions are the user's.** Look up anything observable. Settle an empirical fork by running or sketching it. Put consequential product, ownership and irreversible choices to the user once, with a recommendation. Decide reversible technical details yourself and list them in the report. A settled decision or an agreed seam stays settled.
- **Permissions come from the user or the project.** This stack grants none by itself. Publishing issues, posting comments, pushing, merging, deploying, installing and messaging each need the user's request, a standing project or user authorization, or a finish-line grant (`full send`, `full stop`, see delivery). An action already covered by one of those needs no second confirmation.
- **Prove on the real artifact.** Command output, a reproduction, a capture. Label every claim measured, inferred or guess in the sentence that makes it. Never hand the user a check you could run.
- **No is an acceptable answer.** When scope, an abstraction, a test or a review finding does not earn its place, say so with the reason.
- **Report** the finish-line state, the evidence, the decisions made on the user's behalf, and what remains unverified.

## Sources

Methods are adapted from Matt Pocock's skills, pstack, and tstack. [references/provenance.md](references/provenance.md) maps each source to what was kept and where; read it only when updating the stack or asked about sources.
