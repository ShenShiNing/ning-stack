# ning-stack

My personal software engineering workflow, packaged as one agent skill for Claude Code and Codex. It draws extensively from Matt Pocock's skills, Lauren Tan's pstack, and Theo Browne's tstack, adapted to how I work.

Build complex things as simply as possible. Keep one owner accountable, bring me consequential decisions, and prove the result on the real artifact.

## How I work

- One request owner carries the work to its agreed finish line. One implementer owns each coherent slice through review and CI fixes.
- Investigate observable facts before asking questions. Bring consequential product choices together, with a recommendation and its trade-offs.
- Use the smallest design that meets the current need. Additional tests, comments, abstractions, and options must address a concrete risk or reduce existing complexity.
- Run focused local checks, open a ready PR, and run independent review alongside CI. Batch fixes and evaluate the merge gate on the final commit.
- Keep reviewers independent and read-only. Assess requirements and engineering standards separately.
- Match verification to risk. Reuse evidence only while its assumptions remain valid.

## Four flows

| Flow | Purpose | Reference |
| --- | --- | --- |
| Design | Understand the existing system, resolve consequential choices, shape the implementation, and agree on a brief or specification. | [Design](references/design.md) |
| Delivery | Carry an agreed change through implementation, proof, independent review, and the requested finish line. | [Delivery](references/delivery.md) |
| Cleanup | Remove debt, dead code, stale comments, and unnecessary tests against explicit standards, with evidence for each change. | [Cleanup](references/cleanup.md) |
| Optimization | Reassess logical and physical architecture, including the premises behind earlier decisions. Keeping the current design is a valid outcome. | [Optimization](references/optimization.md) |

## Load only what the task needs

`SKILL.md` contains shared rules and routing. An ordinary change loads the delivery flow; specialist methods are loaded when their conditions apply.

- [Investigation](references/methods/investigation.md): understand behavior and rationale, diagnose difficult bugs, compare designs, and divide independent investigations.
- [Review](references/methods/review.md): Spec and Standards assessments, findings ledgers, and bounded review rounds. Cross-model interrogation and council are available for consequential disputes or explicit requests.
- [Evidence](references/methods/evidence.md): proof by risk, test quality, blast radius, evidence reuse, measurements, and reusable verification tools.
- [Continuity](references/methods/continuity.md): decision trails, unattended work, pause and resume, handoffs, takeovers, old PRs, and backlogs.
- [Learning](references/methods/learning.md): structural fixes for recurring mistakes, retrospectives, and stage timing.

Small changes use an inline frame and existing check output. Separate specs, decomposition checklists, and decision trails are conditional; a findings ledger starts only when a finding exists. Review rounds have a ceiling, not a required count. Competing designs and review panels stay conditional.

## Install

The repository root is the skill directory.

```bash
# Claude Code
git clone https://github.com/ShenShiNing/ning-stack ~/.claude/skills/ning-stack

# Codex
git clone https://github.com/ShenShiNing/ning-stack "${CODEX_HOME:-$HOME/.codex}/skills/ning-stack"
```

To use both, keep one clone and link it into the other skill directory. Automatic discovery is enabled; you can also invoke `ning-stack` explicitly.

## Use it in a project

No setup or activation step is required. The skill reads the project's existing `AGENTS.md`, `CLAUDE.md`, and referenced instructions for product constraints, safe environments, design authority, architecture, commands, model roles, and merge requirements.

The order of authority is: harness and tool rules, explicit instructions for the task, project rules, then ning-stack. If an existing project rule conflicts, follow it and identify the conflict. Replacing that rule is a deliberate project change.

A project may add a short preferences section to `AGENTS.md`:

```markdown
## ning-stack
- Default finish line: ready
- Reviewer: an independent model from a different family, medium effort
- Focused checks: `npm test -- <files>`, `npm run typecheck`
- Broader checks for persistence changes: `npm run test:integration`
```

Keep project-specific constraints and operating procedures in the project.

## Validate

The only helper script, `scripts/trail.py`, records decision notes and explicit run/span timing. Spans can overlap. Its report distinguishes elapsed time, active wall time, and overlapping phase totals.

Tests use the Python standard library:

```bash
python3 -m unittest discover -s tests
```

GitHub Actions runs the same tests on pushes and pull requests.

## Measure the improvement

The intended improvements are shorter handoffs, continuous ownership, focused checks, concurrent review and CI, and retesting based on actual impact. No speedup has been measured or promised.

Compare several tasks of similar scope and risk. Record stage timing and rework. A delegated task's elapsed time includes its investigation, coding, and checks; it is not a measurement of model latency alone.

## Sources

Methods are adapted from the upstream projects below. The [source map](docs/provenance.md) records what was retained, changed, and made conditional. Raw upstream skill files are not runtime dependencies.

| Source | Author | Main contributions | License notice |
| --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/main) | Matt Pocock | Decision-frontier interviews, domain modeling, deep modules, prototypes, specifications, vertical tickets, TDD, diagnosis, Spec/Standards review, architecture exploration, handoffs, triage, wayfinding, and retrospectives. | [MIT](LICENSES/mattpocock-skills.txt) |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) | Lauren Tan | Investigation, design shaping, competing designs, adversarial review, bounded parallel work, blast-radius proof, benchmark discipline, structural correction, continuity, cleanup, and verification tools. | [MIT](LICENSES/pstack.txt) |
| [tstack](https://github.com/t3dotgg/tstack/tree/main) | Theo Browne | Full-send/full-stop finish lines, Sol review loops, concise PRs, event-driven PR supervision, attributed comments, takeovers, modernization, and council. | [MIT](LICENSES/tstack.txt) |

Local adaptations include single-owner defaults, conditional multi-model work, review concurrent with CI, impact-based severity, and preserving ambiguous constraint comments until their purpose is understood. Provider-specific names and worker machinery are resolved through the active harness rather than copied from upstream.

## License

[MIT](LICENSE). Original upstream copyright and permission notices are retained in `LICENSES/`.
