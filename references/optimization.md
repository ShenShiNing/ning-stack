# Optimization

Reassess the whole codebase's architecture, logical and physical, and recommend what to change and what to keep, with evidence. Keeping the current architecture is a valid outcome.

Contents: Global map · Select · Investigate · Judge · Report · Hand off.

## Global map

Build one low-resolution map before going deep. Use the project's architecture documents, package manifests, entry points, the dependency graph and `git log` hotspots. Note for each item what it is, why it is that way (from ADRs or history), and whether code agrees.

**Logical architecture**

- Stack and runtime model: languages, frameworks, process and runtime boundaries, how work is scheduled and where state lives.
- Principles in force and where they are enforced (types, lint, checks, review only).
- Ownership: which module owns each piece of domain state and each capability; dependency direction.
- Data and state model: core types, persistence, contracts between processes and clients.
- Why and trade-offs: the decisions that shaped this (ADRs, history) and the premise each rests on.

**Physical architecture**

- Packages, modules and directories; entry points; where code of each kind is placed and why.
- Build, test and deploy units and how they map to the logical owners.

Done when the map covers every top-level package and runtime, each line with a source pointer, and the unknowns are named instead of guessed.

## Select

Choose one to three areas for deep investigation from evidence of friction, not from the map's completeness:

- Hotspots where one logical change forces scattered edits (shotgun surgery) or one module changes for unrelated reasons.
- Understanding one concept requires bouncing across many small modules; shallow modules whose interface is nearly as complex as their implementation.
- Bugs that had no correct test seam; areas hard to test through their current interface.
- Two ways of doing one thing; ownership claimed by two modules; layers that only pass through.
- A principle or ADR whose premise has changed (scale, product direction, stack, team, tooling).
- Repeated agent corrections in the area (see [methods/learning.md](methods/learning.md)).

The user's named direction overrides this selection.

## Investigate

For each selected area:

1. `how` over it and `why` over its current shape ([methods/investigation.md](methods/investigation.md)). The `why` output's Preserve, Change, Avoid and Risk set becomes the constraint list.
2. Apply the deletion test to each suspect module: would deleting it concentrate complexity, or just move it?
3. Check the premise of every rule or ADR the area leans on. Write the premise down and test it against today's facts. A changed premise is a reason to revisit; an inconvenient rule is not.
4. Sketch the deepened or moved shape in deep-module terms (module, interface, depth, seam, adapter, leverage, locality) and the domain's glossary terms. For a one-way door or a contested call, use competing sketches and a cross-model interrogation ([methods/review.md](methods/review.md), Interrogate).

## Judge

For each candidate, decide one of:

- **Keep**: the current shape earns its cost. Say why so the next review does not re-suggest it.
- **Deepen or move**: a concrete restructure, with the benefit in locality, leverage and testability, and the migration route (prefactor, expand, migrate in batches, contract; or a hard cut where the project has no data to preserve).
- **Revise the standard**: the principle or ADR is wrong for today. Propose a superseding ADR with the changed premise and evidence. Code that merely deviates from a sound norm is migration debt, named as such, never blessed by rewriting the norm.

Rate each change `Strong`, `Worth exploring` or `Speculative`, and name one top recommendation.

## Report

Lead with the top recommendation. Then the map summary (short), each candidate (files or modules, problem, proposal, benefits, cost and migration, strength, ADR conflicts), the kept items with reasons, and the unknowns. Use a visual when it makes graph-shaped structure clearer; follow the active harness's rendering rules.

Propose no code until the user picks a candidate.

## Hand off

The chosen candidate goes to [design.md](design.md) at Shape (its grounding is done), then to [delivery.md](delivery.md) as R2 work. Record a rejected candidate with a load-bearing reason as an ADR only when a future review would otherwise re-suggest it.
