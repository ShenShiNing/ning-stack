# Design

Agree on behavior and implementation shape, then give delivery the smallest brief it can execute.

## Classify

- **Covered:** an agreed spec, existing pattern, or design authority already answers the question. Cite it and go to delivery.
- **Bounded:** a capability fits one session. Ground it, resolve consequential choices, write an inline brief.
- **Deep:** uncertainty, irreversible choices, contested ownership, or explicit grilling warrants repeated alignment and a written spec.
- **Foggy:** the effort exceeds one session and the route is unclear. Use Long horizon below.

## Ground

Read the owner, callers, applicable glossary/ADRs, and the nearest feature, test, and UI precedent. Use [Investigation](methods/investigation.md), How for unfamiliar behavior and Why before reversing a decision. Proceed when current behavior, ownership, and constraints have source pointers. Look up observable facts yourself.

## Align

Ask only consequential product, scope, ownership, or irreversible choices. Decide reversible details yourself and carry settled answers forward.

Group currently answerable questions into one numbered round, each with options and a recommendation that “yes” can accept. Defer questions that depend on unanswered ones. Recompute this frontier after answers; stop when it is empty and the user confirms consequential choices. Do not implement those choices before agreement.

Challenge ambiguous terms against the glossary and concrete scenarios. Update resolved domain terms when project documentation rules call for it; discussion alone does not require a document. Offer an ADR when the choice is hard to reverse, surprising without context, and rests on a real trade-off.

## Shape

For a new or changed interface, sketch caller usage first. State ownership, data/state shape, errors, constraints, test seams, and where modules belong. Existing seams and established patterns need no new design round.

Prefer deep modules: little a caller must know, substantial behavior behind the interface. Apply the deletion test: if removing a module removes complexity, it is a pass-through; if complexity spreads across callers, it earns its place. A second real implementation or a present ownership/lifecycle need can justify an adapter; hypothetical variability cannot.

Use [Competing designs](methods/investigation.md) only for contested, irreversible, or unprecedented shapes. A still-contested costly choice may warrant [Interrogate](methods/review.md). During implementation, surface consequential departures from the agreed shape. Repeated workarounds, escape hatches, or caller knowledge of internals are reasons to revisit the sketch rather than accumulate exceptions.

## Prototype

Settle an empirical question with a throwaway, runnable sketch: minimal state, no polish or test suite, full state visible for logic experiments. UI follows project design authority first. For uncovered UI, compose one static mock from existing patterns, present it, and wait for approval; use several variants only if no pattern fits. Fold the decision into the brief and keep the prototype off main.

## Output

- **Inline brief, default:** acceptance, decisions and reasons, ownership/seams, constraints, exclusions.
- **Spec, multi-owner/session work or on request:** user problem and solution, testable behaviors, decisions, test seams, exclusions. Prefer durable concepts to paths or code that will drift; retain a prototype snippet when it precisely encodes a decision.
- **Tickets, work spanning owners/sessions:** independently demonstrable vertical slices sized to one context, prefactor first, blocking edges explicit. Confirm granularity and edges once. Migration strategy follows the project's data and hard-cut rules.

Tracker publication needs authorization; otherwise keep artifacts local and report their location.

## Long horizon

Keep a local map: destination, settled decisions with links, unresolved questions, and exclusions. Turn sharp questions into research, prototype, grilling, or implementation tickets with blocking edges. Work the unblocked frontier; resolve a coherent decision per session and update the map. Start delivery when the relevant decisions are settled. Publish the map only when authorized.
