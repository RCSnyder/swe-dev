# Prior Art And Boundaries

Load this reference only when novelty, literature, architecture positioning, or research claims matter.

The method in this skill composes established ideas rather than claiming to invent each primitive.

## Established Or Substantial Adjacent Areas

- software assurance cases and structured claims/evidence;
- dynamic and runtime assurance;
- truth-maintenance and assumption-dependent reasoning;
- formal verification, refinement, model checking, proof-carrying code;
- requirements traceability and impact analysis;
- provenance and software-supply-chain attestations;
- policy-as-code, capability security, exact-action authorization;
- event sourcing and tamper-evident audit trails;
- safety cases, fault trees, recovery engineering, resilience;
- autonomous-agent governance and tool-call mediation;
- self-adaptive and self-modifying systems;
- continuous verification and incremental build/dependency invalidation;
- data lineage and change impact analysis.

Do not claim `assurance lineage`, `release gating`, `runtime policy`, `formal agent constraints`, `provenance`, or `self-evolving agents` as novel categories without careful current research.

## Synthesis Worth Testing

A narrower research/product hypothesis is that useful systems can compute a decision chain like:

```text
meaningful change
-> assurance applicability
-> preserved counterevidence
-> current epistemic state
-> corrective capacity
-> justified authority envelope
-> minimum next evidence / action
```

The potentially distinctive focus is **semantic applicability under change**: evidence can remain byte-identical while ceasing to justify a claim because the model, specification, verifier, scope, assumptions, or authority semantics changed.

Another useful hypothesis is **counterevidence-preserving evolution**: a successor should not become more trusted merely because the history that weakened its predecessor was dropped, summarized away, or merged incorrectly.

A third is **corrective-capacity-aware authority**: action scope should account not only for policy and current evidence, but whether independent timely correction remains constructible after the action.

These are hypotheses and design principles, not established universal laws.

## Useful External Building Blocks

When implementing a real system, prefer composition with existing standards/tools rather than replacing them:

- W3C PROV for provenance concepts;
- SLSA and in-toto for software artifact provenance/attestations;
- SACM or existing assurance-case representations where appropriate;
- TLA+/Apalache/Alloy/Lean/SMT/property tests for formal or behavioral evidence;
- OPA/Cedar/capability systems for enforcement and authority;
- OpenTelemetry/runtime telemetry for observations;
- supply-chain/data-lineage graphs for dependency facts.

The skill itself stays format-agnostic so it remains useful in ordinary Copilot/VS Code and other harnesses.
