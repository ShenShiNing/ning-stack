# Investigation

Questions stay read-only. Read the method that answers the question; an investigation is not permission to change the system.

## How

Read narrow areas directly and explain runtime flow, ownership, concepts, and source pointers. For broad work, use [Parallel exploration](#parallel-exploration) when independent questions benefit from delegation, then synthesize once. State useful assumptions and proceed with the smallest useful scope.

## Why

Anchor the current code, then trace meaningful history through blame, renames, commits, PR discussion, and relevant ADRs. Stop a narrow inquiry when a clear rationale answers it. Widen to issues, docs, chat, or observability only while uncertainty remains or a deep audit is requested. Defensive guards, retries, flags, and thresholds warrant looking for the motivating incident.

Separate sourced facts, reasonable inference, competing hypotheses, and unknowns. Record searched sources, empty results, and access gaps when they matter to confidence; an unreachable source is not a negative result. Before a change, turn the rationale into Preserve / Change / Avoid / Risk constraints.

## Diagnose

1. Build a tight feedback loop that exercises the user's real failure: test, request, replay, fixture, or minimal harness. Observe the failure before theorizing. Pin time/data and isolate state where useful; improve reproduction rate for intermittent failures. If no honest reproduction is possible, report attempts and the missing access or instrumentation.
2. Minimize until the remaining inputs and steps are load-bearing. Confirm this is the reported failure.
3. Rank falsifiable hypotheses. Each probe tests one prediction and changes one variable; use a debugger or targeted logs at distinguishing boundaries. For regressions, measure and bisect.
4. Fix the first wrong state, with a regression test at a seam that reaches it ([Evidence](evidence.md), Tests). Watch red become green and rerun the original reproduction.
5. Remove temporary probes and harnesses; record the confirmed cause and proof.

After two failed fixes sharing a premise, test that premise before trying a third. Redact secrets from evidence and keep credentials out of code.

## Competing designs

Use only for irreversible, contested, or unprecedented choices. Set a task-specific rubric (for example locality, interface depth, migration cost), then produce at least two structurally different whole designs. Separate authors/model families are useful when their independence earns the cost; otherwise sketch sequentially yourself.

Compare against the rubric, choose one base, and borrow only parts that preserve one coherent model. Convergence supports a shared shape; wide divergence calls for reframing, not averaging. Verify the chosen artifact and explain the selection and rejected trade-offs. A second judge is optional.

## Parallel exploration

Use for independent questions or coverage slices that each need substantial context. Declare the expected artifact and done condition; partition scope or declare how a race will be judged before starting. Give each explorer a standalone goal, exact slice, verification method, and report format. Measurement and verification results identify the SHAs they cover.

Consolidate `PASS`, `ISSUES`, or `BLOCKED` results with evidence and gaps. Missing, unpinned, or failed work is a gap, never a pass. Writers need separate isolated workspaces within project limits; read-only explorers do not consume implementer slots.
