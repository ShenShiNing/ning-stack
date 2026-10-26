# Evidence

Read the relevant section: Tests, Ladder, Blast radius, Reuse, Numbers, or Verification harness. Risk classes and routine proof live in [Delivery](../delivery.md).

## Tests

Test observable behavior through public interfaces, at the highest existing seam that reproduces the risk. For behavior changes, observe a meaningful failure before the fix and work one red-to-green vertical slice at a time. Related assertions in one scenario belong together.

- Each new test catches a distinct current risk. Reuse coverage instead of repeating an assertion across layers.
- Prefer literal expectations, worked examples, or specification examples over recomputing the implementation's answer.
- Mock existing external boundaries (network, provider, clock), not private collaborators. A refactor that preserves behavior should preserve tests.
- If no honest seam reproduces the bug, report the gap instead of adding a shallow test for confidence.
- Visual-only changes use captures. Mechanical changes may rely on existing tests when project rules permit. Deleting tests requires the coverage decision in [Cleanup](../cleanup.md).
- Mutation proof, when needed, runs in a disposable copy; verify the intended mutation actually landed.

## Ladder

Evidence levels: **1** assertion, **2** source pointer, **3** traced path, **4** executed check, **5** real running surface. Record where proof stops. Missing or inconclusive proof is an open gap; mocked tests do not establish a user-experience claim.

## Blast radius

For R2 or an uncertain change, identify the safety fact and investigate what the diff hides: downstream callers, schemas and wire formats, dependency source and patches, resource lifetime, timing, and shared setup. Follow the risks this change actually introduces; irrelevant database or build checks add no proof.

Prove the load-bearing safety fact with an executable check (level 4); a user-experience claim needs the real surface. Record confirmed risks and cleared cases with evidence.

## Reuse

Record head and base with check and review results; record patch identity when carrying them across a rebase. Link existing output rather than copying it into another document.

1. Inspect the old-to-new base delta before deciding: patch files and dependencies, public contracts, lockfiles and build/type config, shared fixtures, resources, and CI inputs. Clean textual application is not proof of compatibility.
2. Rebase for a conflict, an interaction, or a project gate. Unrelated base changes do not require a rebase or a new review.
3. Carry review and local proof only when the patch is identical (range-diff or patch ids) and no base interaction changes their assumptions. Changed behavior gets incremental review; changed inputs get affected checks. Inspect interactions even when the patch is unchanged.
4. CI is per head: an earlier green run never substitutes for checks required on the new head.

## Numbers

Before claiming a speedup, inspect the measurement code, production settings, machine load, and the end-to-end path. Count errors and completed work, confirm work ran inside the timed region, and identify the limiter. Compare equally tuned cases, at least five alternating runs per side; report median, range, unit, and count. Overlapping spread, an unknown limiter, or mismatched settings makes the conclusion inconclusive. A requested ballpark may use one run, explicitly labelled.

For sustained optimization: reproduce the complaint, freeze a realistic measurement harness and correctness gate, record a baseline, and test one mechanism per iteration. Keep changes only when improvement exceeds noise and correctness holds; revert failed attempts and record why. On a plateau, change the hypothesis rather than relax acceptance. Workflow task comparisons use [Learning](learning.md), Timing; elapsed child-task time alone is not model latency.

## Verification harness

Build a project-local helper only when agents repeatedly improvise verification of the same real surface. Reuse existing launch and test infrastructure first. A useful helper can launch in a safe environment, check readiness, drive stable handles, capture real outcomes, and clean up only what it started. Keep a small feature map of paths and gotchas; run the helper end to end before relying on it.

When the app changes, check the map against source and run the affected journeys. Report product regressions instead of hiding them in harness updates. Respect project browser and infrastructure limits.
