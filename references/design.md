# Design

Reach agreement with the user on a new capability, grounded in the real source, and hand delivery a brief proportional to what the implementer needs. Not more.

Contents: Classify · Ground · Align · Domain · Shape · Prototype · Output · Long horizon.

## Classify

Pick the lightest path that fits, and say which one you took.

- **Covered**: an existing pattern, the project's design authority, or an agreed spec already answers how it should behave. No design round. Write the three-line frame from delivery Stage 0, cite what covers it, go to delivery.
- **Bounded**: one capability, a few open decisions, fits one session. Ground, one alignment round, inline brief.
- **Deep**: high uncertainty, a one-way door, contested ownership, or the user asks to be grilled. Ground, alignment in rounds until the frontier is empty, shaped design, written spec.
- **Foggy**: too big for one session and the route is not visible yet. Long horizon below.

## Ground

Facts are your job. Before asking the user anything:

- Read the code that owns the area and its callers. Use the `how` method ([methods/investigation.md](methods/investigation.md)) when the subsystem is unfamiliar; use `why` when the design would reverse or redraw an existing decision, so the old rationale becomes a constraint instead of a guess.
- Read the domain glossary and active ADRs for the area (wherever the project keeps them).
- Find prior art in the codebase: the nearest existing feature, test and UI pattern an agent would copy.

Done when you can describe the current behavior, the owning module, and the constraint set, each with a source pointer.

## Align

Map the open decisions as a **design tree**. The **frontier** is every decision whose prerequisites are settled.

1. Ask the whole frontier in one round. Number each question, give the options when there are any, and give your recommended answer, worded so "yes" accepts it.

   ```
   Q1. <title>: <question and options>
   Recommended: <answer and one-line reason>
   ```

2. Ask only what is the user's to decide: product behavior, scope, ownership across contexts, irreversible or costly choices. A fact you could observe goes to a lookup or a sketch, not the user. A reversible technical detail is yours: decide it and list it in the brief.
3. A question that depends on another question in the same round waits for a later round. While a lookup runs, ask the questions that do not depend on it.
4. Recompute the frontier from the answers and continue. Bounded designs usually close in one round; deep ones take as many as the tree needs.

Done when the frontier is empty and the user confirms the shared understanding for anything consequential. Do not act on a design before that confirmation.

## Domain

While aligning, keep the domain model honest:

- Challenge a term that conflicts with the glossary in the moment ("the glossary defines X as A; you seem to mean B").
- Replace vague or overloaded words with a canonical term.
- Stress relationships with concrete edge-case scenarios.
- Cross-check claims against code and surface contradictions.
- Update the owning glossary when a term resolves, with no implementation detail in it.
- Offer an ADR only when the choice is hard to reverse, surprising without context, and the result of a real trade-off. All three, or skip it.

## Shape

For anything that crosses a module seam:

1. **Write the caller's usage first**, then derive types, signatures and module placement from it. Sketch with unimplemented bodies when it helps.
2. Use the deep-module vocabulary: **module**, **interface** (everything a caller must know, including invariants, errors, ordering), **depth** (behavior per unit of interface), **seam**, **adapter**, **leverage**, **locality**. Apply the deletion test to each new module: if removing it makes complexity vanish, it was a pass-through; if that complexity reappears across callers, the module was earning its place. One adapter suggests hypothetical variability, while two can justify an adapter seam; a current ownership or lifecycle requirement can also justify a boundary without inventing alternative implementations.
3. Screen for the next contributor: an agent that sees only the files it opened, copies the nearest example and takes the shortest path that compiles. Prefer the shape where a change that looks right from one file is right for the repo.
4. Name the test seams: existing ones first, the highest seam possible, as few as possible. Each gets one line on what it catches and misses.
5. **Competing sketches** only for a one-way door, a contested shape, or no precedent in the codebase: produce at least two structurally different whole-shape sketches and pick by rubric (Competing designs in [methods/investigation.md](methods/investigation.md)). Contested and costly after that: run an adversarial cross-model review of the chosen sketch ([methods/review.md](methods/review.md), Interrogate). Established patterns skip both.

During delivery the sketch is the contract: a needed deviation is a signal to surface, not friction to absorb. When the same workaround shape recurs, unrelated edge cases need special branches, types need escape hatches, or callers must know internal rules, scrap the sketch and redesign as if the new constraint were there from day one, smaller before it grows.

## Prototype

When the answer is something you could observe, sketch it instead of asking.

- Question decides the shape. "Does this logic or state model feel right?" gets a single runnable file that drives the state through hard cases and shows full state after each action. "What should this look like?" first goes to the project's design authority; an uncovered UI is one static mock composed from existing patterns, presented, then stop for approval. Several variants only when no existing pattern fits.
- Throwaway from the start and marked as such, trivial to run, in-memory state, no polish or tests.
- Fold the validated decision into the brief. Keep the prototype out of the main branch.

## Output

Size the artifact to the execution, not to the idea.

- **Inline brief** (default): acceptance, decisions with reasons, ownership and seams, constraints, out of scope. Lives in the thread or the delivery child's prompt.
- **Spec**: only when several owners or sessions will execute it or the user asks. Sections: Problem (user's view), Solution (user's view), Key behaviors (numbered and testable, as many as the behavior needs and no more), Decisions (modules, interfaces, schema, contracts), Test seams, Out of scope. No file paths or code that will go stale, except a prototype snippet that encodes a decision more precisely than prose.
- **Tickets**: only when the work spans sessions or owners. Tracer-bullet vertical slices, each demoable alone and sized to one context, prefactoring first, each with its blocking edges. A wide mechanical refactor goes expand, migrate in batches, contract. Present the breakdown once for confirmation of granularity and edges.

Publishing a spec or tickets to the tracker needs the user's request or a standing authorization; otherwise keep them local and say where.

## Long horizon

For a foggy effort larger than one session, chart a **map**: the destination in one or two lines, standing notes, decisions so far (one line each, linking where the detail lives), **not yet specified** (the fog you can see but not phrase sharply), and out of scope. Each sharp question becomes a decision ticket typed research, prototype, grilling or task, with blocking edges; the frontier is the open, unblocked, unclaimed tickets. Resolve one decision ticket per session (research tickets may run in parallel), record the answer, graduate the fog it clears. The map plans; it hands off to delivery once nothing is left to decide. Keep the map local unless the user authorizes tracker publishing.
