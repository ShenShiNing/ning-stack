# Evidence

How to prove a change, how much proof a risk class needs, when earlier proof still counts, and how to trust a number.

Contents: Ladder · Proof by risk class · Tests · Blast radius · Reuse · Numbers · Verification harness.

## Ladder

For each fact a change's safety rests on, get it as far down this list as is cheap and say where it stopped:

1. Asserted. Worth nothing alone.
2. Pointed at: a real `file:line`, or the library's own source at the pinned version.
3. Walked: the failure path traced step by step and shown not to reach.
4. Ran: a script or test that calls the real code and fails loudly if the fact is false.
5. Reproduced in the running app on the real surface.

Green mocked tests do not prove a user experience. A verdict is `VERIFIED`, `NOT VERIFIED` or `INCONCLUSIVE`; inconclusive is not a pass. When something passes too easily, suspect the observation before the system.

## Proof by risk class

| Class | Local proof the slice owner runs | Review |
| --- | --- | --- |
| R0 prose | scoped formatter and link checks on the changed files | independent review, budget 3 |
| R1 bounded | repro green, tests of touched modules, scoped typecheck and lint | standard rounds, budget 3 |
| R2 wide | R1 plus the obligations its actual risks touch: integration tests only for data or persistence effects, a build only for build or packaging effects, wider typecheck for shared contracts, and a level 4 proof of the one safety fact | budget up to 5 for the listed risks; interrogate if contested |

CI runs whatever the project requires on the current head; a project gate is never bypassed or replaced by local proof. One owner per check: the slice owner owns local proof, CI owns its suites, and a scheduled full run is a safety net that never stands in for R2 proof before merge. Unknown impact is conservative: widen to the full relevant set when you cannot name what a change reaches.

## Tests

Tests prove behavior through public interfaces; they survive refactors because they do not care about internals.

- **Red before green**: write the failing test at an existing seam, watch it fail for the right reason, write only enough code to pass. If you force red by mutating code or a fixture, do it in a disposable copy and diff against the pristine source to prove the mutation landed.
- **Vertical slices**: one seam, one test, one minimal implementation per cycle; each test responds to what the last cycle taught. Writing all tests first verifies imagined behavior.
- **One scenario, related assertions**: a test may assert several observable consequences of one scenario.
- Avoid **implementation-coupled** tests (mocking internal collaborators, testing private methods, checking through a side channel instead of the interface) and **tautological** ones (expected values recomputed the way the code computes them; take them from a literal, a worked example or the spec).
- Mock only at boundaries the system already isolates (network, provider, clock), not internal collaborators.
- A bug without a correct seam (the only test would be too shallow to replay the real call pattern) is itself a finding: say so and leave the regression test out rather than adding false confidence.
- Purely visual changes prove with before and after captures, not tests.
- A new test needs a risk it uniquely catches. Do not repeat an assertion across layers.

## Blast radius

For a change you do not yet trust, or any R2 change, find what it breaks elsewhere before shipping.

1. Read the change, including what it now does that the diff does not spell out.
2. Find the one fact it is safe because of (often a single fact clears most risky cases). Spend the time here.
3. Look where symbol search stops: the library source at its pinned version and local patches, execution timing (microtasks, teardown), JSON shapes, database columns, wire formats, another language reading the same bytes, feature flags, code three hops downstream.
4. Give each risk a real likelihood and cost. Keep confirmed risks; list checked-and-cleared ones separately; a search that finds nothing is still an answer.
5. Prove the one fact at level 4 and paste the result. If you cannot, write `unproven`.

Hand back: what it does, the safety fact and its level, risks with `file:line` and how to check, cleared items, and the cheapest pre-merge check.

## Reuse

Pin identities every time you record evidence: head SHA, base SHA, patch id. Earlier evidence counts for a new head only while its assumptions hold.

1. **Inspect the base delta first**: `git diff <old-base> <new-base> --stat`, then read what touches the patch's files, its dependencies (imports and importers of touched modules, lockfile, build and type config), contracts (schemas, migrations, wire formats, public APIs) and shared resources (test setup, CI files, environment). Do this even when a rebase would apply cleanly; a missing textual conflict proves nothing.
2. **Rebase only for a reason**: a conflict, an interaction found in step 1, or a gate that requires being up to date. Never rebase repeatedly for no benefit, and never re-review unrelated base history.
3. **Carry review and local proof** when the patch is identical (`git range-diff` or patch ids) and step 1 found no interaction. When the patch changed, re-review the changed hunks. When the base interacts, re-run the checks for that area and ask the reviewer about the interaction only.
4. **CI is per head**: a green run on an earlier head is history, never the required gate for a new head when the project requires current-head checks. Re-run the required jobs on the current head.

## Numbers

Before you report or act on a performance number (a before and after, a regression claim, a choice between options), write the claim in the words you would ship, read the measurement script, and check machine load (`uptime`, `nproc`). Then answer each with evidence:

1. **Why not double?** Name the limiter with a profiler run you do not report. If a change did not move the number, the limiter explains why.
2. **Was it tuned?** Both sides as production runs them: build mode, flags, pools, caches, data. Otherwise you compared configurations.
3. **Did it break limits?** Arithmetic against disk, network and cores. Removing a piece that takes 10% of the run gains at most about 11%.
4. **Did it error?** Count failures and check output correctness.
5. **Does it reproduce?** At least five runs per side, alternating; report median and range. A gap inside the run-to-run spread is no measurable difference.
6. **Does it matter?** Measure the end-to-end path a user waits on and report the micro result as a share of it.
7. **Did it happen?** Confirm the work ran inside the timed region.

Report: verdict first (faster, slower, no measurable difference, inconclusive), then number with unit, run count, range and limiter. Inconclusive when the limiter is unknown, a side was untuned, or questions 4 or 7 were not checked. A quick ballpark the user asked for may be one run, still checking 4 and 7 and saying it is one run.

**Improvement loop** for sustained work on one metric:

1. Reproduce the user's complaint with a realistic case; if none reproduces it, fix the repro first.
2. Fix the metric, the better direction, and a stop predicate pairing a target with a minimum attempt count.
3. Build the harness, prove it separates contrasting workloads, vet it with the questions above, make it print error and work counts, then freeze it. Record the baseline and a green regression gate.
4. One hypothesis per iteration, naming a mechanism. One change, one measurement, keep only past noise with the gate green, otherwise revert fully. Log every attempt in the decision trail ([continuity.md](continuity.md), Decision trail). One commit per kept win.
5. On a plateau, pivot category or combine near-misses before concluding. Correctness and simplicity outrank the number. Never relax the predicate to meet it.

## Verification harness

A project-local verification skill or script (launch, doctor, drive, evidence, cleanup, plus a feature map) pays off only when agents repeatedly need to drive the same real surface and keep improvising it. Not for a single change. When warranted:

- Answer from the repo, not the user: the surface, the documented run command and readiness signal, the existing harnesses to drive it, the evidence it can capture, and whether two instances can run side by side.
- **Launch** reaches a usable state from empty data; **Doctor** is a read-only health check run before driving and after any surprise; **Drive** uses real stable handles from this repo; **Evidence** follows the real user path and verifies side effects; **Cleanup** kills only what it started and keeps the evidence.
- Seed a feature map with the top few user-facing features: how to reach each, how to drive it, the end state that proves it, gotchas. Never weaken a journey to make it pass.
- Run it end to end once before handing it over; a harness never executed is a draft.
- Maintenance pass when the app has changed: index hygiene, a source read per feature for drift, then a live pass driving every feature. Outcome is `clean`, `changed` (one PR of proven doc or harness fixes) or `blocked`. Product regressions found this way are reported, never papered over in the map.

Respect the project's limits on browser suites and test infrastructure; a harness is a verification tool, not a new test suite.
