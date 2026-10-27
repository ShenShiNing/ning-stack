# ning-stack

An engineering agent stack integrating and adapting the strengths of Matt Pocock's skills, Lauren Tan's pstack, and Theo Browne's tstack. It combines reusable engineering methods, four workflows that compose them, and small tools for observable checks. It works with Claude Code and Codex, with project and harness details supplied by adapters.

Build complex things as simply as possible. Keep one owner accountable, agree on consequential decisions with the user, and prove the result on the real artifact.

## What the stack contains

| Part | Role |
| --- | --- |
| Engineering methods | Investigation, diagnosis, domain and interface design, prototypes, specifications, testing, verification, review, architecture analysis, and continuity. Use them independently or together. |
| Four workflows | Design, delivery, cleanup, and optimization compose the methods around an outcome and finish line. |
| Executable tools | Decision and timing trails, plus a read-only GitHub PR gate. |
| Project and harness adapters | Supply product constraints, architecture, commands, model choices, permissions, and environment-specific tool calls. |

Matt's skills contribute decision clarity, deep modules, vertical slices, and behavior-focused tests. pstack contributes investigation, design exploration, blast-radius analysis, and structural correction. tstack contributes delivery finish lines, bounded review, PR supervision, and continuity. The [source map](docs/provenance.md) explains the adaptations.

## Principles

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

## Use a method or compose a workflow

`SKILL.md` is one discoverable entrypoint. A focused review or investigation goes straight to its method; an end-to-end change uses a workflow. Loading is conditional in both cases.

Ask the agent to use ning-stack to investigate a decision, prototype a state model, review a diff, audit test value, or resume work. These requests do not require a delivery cycle. Shipping code, publishing artifacts, or changing external state still requires the corresponding authorization.

- [Investigation](references/methods/investigation.md): understand behavior and rationale, diagnose difficult bugs, compare designs, and divide independent investigations.
- [Review](references/methods/review.md): Spec and Standards assessments, findings ledgers, and bounded review rounds. Cross-model interrogation and council are available for consequential disputes or explicit requests.
- [Evidence](references/methods/evidence.md): proof by risk, test quality, blast radius, evidence reuse, measurements, and reusable verification tools.
- [Continuity](references/methods/continuity.md): decision trails, unattended work, pause and resume, handoffs, takeovers, old PRs, and backlogs.
- [Learning](references/methods/learning.md): structural fixes for recurring mistakes, retrospectives, and stage timing.

Small changes use an inline frame and existing check output. Separate specs, decomposition checklists, and decision trails are conditional; a findings ledger starts only when a finding exists. Review rounds have a ceiling, not a required count. Meaning-preserving prose repairs may skip review when user/project rules allow; semantic changes to agent instructions and operating procedures retain it. Competing designs and review panels stay conditional.

## Connect the four flows

| Input | Flow | Outcome and next step |
| --- | --- | --- |
| A new capability or an unsettled requirement | Design | Agree acceptance and constraints; hand an inline brief, spec, or vertical tickets to Delivery. |
| An agreed feature, fix, or refactor | Delivery | Prove, review, and finish locally, ready, or merged. Record maintenance and learning findings without expanding the task. |
| Debt measured against current project standards | Cleanup | Keep, remove, rewrite, or encode with evidence; ship changes through Delivery. A disputed architectural premise goes to Optimization. |
| Architectural friction or a changed premise | Optimization | Keep the current choice or recommend a logical/physical restructure; an approved candidate goes through Design and Delivery. |

Learning feeds observed failures and friction back into these methods. Recurring maintenance uses an agreed scope, cadence, and action budget; schedules and external writes need authorization. Existing records carry the handoffs, so a small task does not need four documents or four separate agent sessions.

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

`scripts/trail.py` records decision notes and explicit run/span timing. Spans can overlap. Its report distinguishes elapsed time, active wall time, and overlapping phase totals.

`scripts/gate.py` is a read-only GitHub PR check using an authenticated GitHub CLI. Supply the full head SHA covered by your proof and review:

```bash
python3 scripts/gate.py --repo OWNER/REPO --pr 123 --head FULL_SHA --finish ready
```

It prints `PASS: remote state checks only`, lists the checked conditions and the remaining owner checks, or reports the failed conditions: head mismatch, closed/draft PR, auto-merge enabled for a ready finish, merge conflicts, unknown mergeability, GitHub `CHANGES_REQUESTED`, or required checks not passing. Both PR snapshots must report `MERGEABLE`; `UNKNOWN` blocks with a request to check again after calculation, without an internal retry loop. Missing or invalid state fields fail closed.

It reads classic branch protection and active branch rules to catch required checks that never reported, then queries their current results. The token must be able to read those policies. Use repeatable `--require-check NAME` for additional project checks. If there are no server requirements, supply project check names or explicitly confirm a no-check policy with `--allow-no-checks`. GitHub's explicit response that the plan does not offer protection counts as no server policy; it still requires an explicit project policy. Permission errors, other query failures, and missing evidence fail closed. Required-workflow rules need separate verification and block this helper.

It neither changes PR state nor merges. `reviewDecision` is only an extra veto: an empty value, `APPROVED`, or `REVIEW_REQUIRED` does not establish independent review or satisfy required approvals. Review acceptance, required GitHub approvals, authorization, queue state, base interactions, and the final pinned merge remain the owner's responsibility. A pass is a snapshot, not protection against later head, base, or review changes.

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
