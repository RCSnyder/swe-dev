---
name: swe-dev-evidence-gated-loop-design
description: "A repeatable method for designing or auditing long-running coding-agent and autonomous-SDLC loops. Use when work needs explicit lifecycle states, source-bound evidence gates, semantic traceability, formal verification, durable recovery, authority controls, or bounded self-improvement. Not for ordinary one-shot coding tasks."
argument-hint: "[loop, autonomous workflow, SDLC, or self-improvement mechanism]"
---

# Evidence-Gated Loop Design

Use this skill to turn an autonomous-agent idea into a **small, explicit control design that can be tested**.

For novelty, literature, or architectural rationale, read [prior-art.md](./references/prior-art.md). Do not load that reference merely to complete an ordinary design.

## 0. Decide Whether A Loop Is Justified

Choose the smallest class that fits:

| Class | Use |
|---|---|
| 0 | One-shot/local/reversible: normal engineering, no loop framework |
| 1 | Repeated bounded task: goal + verifier + retry budget + stop |
| 2 | Long-running autonomy: durable state + gates + recovery + audit |
| 3 | Self-improving/high-impact: protected kernel + candidate admission + lineage |

Reject autonomy theater. If a deterministic script or CI job solves the problem, prefer it.

## 1. Write The Contract Before The Agents

Capture:

```text
Trigger:
Goal:
Authoritative state:
Allowed actions:
Budget:
Terminal states:
Escalation:
```

Then define:

```text
MUST NEVER:
MUST EVENTUALLY:
```

These are the first safety/liveness invariants.

A useful loop model is:

```text
L = trigger
  + goal
  + durable state
  + capabilities
  + verifier policy
  + recovery policy
  + budget
  + terminal states
  + authority policy
```

If one is consequential and implicit, the design is incomplete.

## 2. Convert Lifecycle Labels Into Claims

Replace vague labels:

```text
implemented
tested
reviewed
safe
ready
done
```

with claims that can be checked.

Example:

```text
AC-17:
"Malformed requests are rejected before persistence."
```

For each claim define an evidence contract:

```yaml
claim: AC-17
required_evidence:
  - kind: bug-contrast-test
  - kind: regression-suite
source_binding:
  commit: <hash>
  environment: <digest>
invalid_alternative:
  known_bad_state: <hash>
invalidation:
  - relevant_source_change
  - test_change
  - verifier_change
trust:
  verifier: <tool/version>
```

The exact schema can differ. Preserve the semantics.

## 3. Test Evidence Quality

Every evidence item should answer three questions.

### Admissibility
Is it fresh, reproducible, source-bound, and produced under the stated trust model?

### Discrimination
Would it reject the failure the claim is meant to exclude?

For repair work, a useful check is:

```text
known-bad state → should fail
candidate state → should pass
known-good/gold state → should pass, when available
```

A test that passes everywhere is not strong evidence of the repair.

### Semantic Reach
What does it actually prove?

Examples:

```text
compile success             → structural validity
test                        → covered behavior
property/fuzz/mutation      → broader behavioral evidence
SMT/model check             → stated formal property in its model
kernel-checked proof        → proposition under assumptions
field experiment/telemetry  → external outcome evidence
```

Never upgrade evidence beyond its semantic reach.

## 4. Build A Named State Machine

Example:

```text
INTAKE
→ SPECIFIED
→ EXECUTING
→ CANDIDATE
→ VERIFIED
→ RELEASE_READY
→ DEPLOYED
→ OBSERVED
→ CLOSED
```

Add explicit non-success states:

```text
BLOCKED
NEEDS_HUMAN
REJECTED
BUDGET_EXHAUSTED
QUARANTINED
ROLLED_BACK
SUPERSEDED
```

For each consequential transition specify:

```yaml
from:
to:
requires:
  evidence: []
  authority: []
freshness:
side_effect:
rollback:
on_failure:
```

The state store owns lifecycle truth. Agent text does not.

## 5. Create Stable Semantic Traceability

Use stable IDs only where the value survives lifecycle change:

```text
INTENT-*  high-level purpose
REQ-*     requirement
AC-*      acceptance criterion
SPEC-*    executable/formal specification
MODULE-*  implementation unit
TEST-*    empirical verifier
MODEL-*   formal model
PROOF-*   proof artifact
EVID-*    evidence receipt
DEPLOY-*  release/deployment
FIELD-*   observed-world hypothesis/evidence
```

Example:

```text
INTENT-2
  refined_by → REQ-12

REQ-12
  satisfied_by → AC-17

AC-17
  formalized_by → SPEC-9
  implemented_by → MODULE-8
  tested_by → TEST-91
  proved_by → PROOF-12
  observed_by → FIELD-6
```

The graph is operational when it supports:

- impact analysis;
- stale-evidence invalidation;
- selective re-verification;
- failure routing;
- release reconstruction.

Where practical, compare declared links against dependencies recovered from the artifacts.

## 6. Make Invalidation A First-Class Operation

Evidence is valid for a state, not forever.

Examples:

```text
Δ requirement
→ invalidate dependent specs
→ invalidate affected tests/proofs
→ block dependent release claims
```

```text
Δ implementation
→ invalidate affected behavioral/formal evidence
→ preserve unrelated evidence
```

```text
Δ verifier
→ invalidate evidence whose trust semantics changed
```

Keep old receipts for audit. Mark them stale; do not rewrite history.

## 7. Route Failures To The Responsible Layer

Use failure-directed recovery instead of generic retry.

| Observation | Route |
|---|---|
| build/type error | implementation |
| local regression | implementation/design |
| architecture cannot preserve invariant | design |
| proof exposes false/inadequate invariant | specification/design |
| formalization contradicts accepted examples | intent/specification |
| validation passes on known-bad state | verifier/test design |
| model/code behavior disagree | model/instrumentation |
| field behavior contradicts value hypothesis | discovery/intent |
| action lacks authority | authorization |
| retry repeats same state/strategy | stop/escalate/reframe |

Checkpoint at semantically meaningful boundaries. Recover from the earliest invalidated checkpoint.

## 8. Use A Verification Portfolio

Match verifier strength to risk.

```text
0 compile/type/lint
1 unit/integration/regression
2 property/fuzz/mutation/adversarial
3 executable contracts / SMT
4 model checking / temporal logic
5 kernel-checked proof
```

For proof-grounded work:

```text
requirement       → proposition/contract
architecture      → decomposition/interfaces/invariants
implementation    → witness/program
verification      → proof obligations
integration       → composition
release           → proof + empirical evidence bundle
```

Remember:

```text
code ⊨ spec
```

does not imply:

```text
spec = intended behavior
```

Challenge the intent-to-spec edge with examples, independent formalizations, counterexamples, metamorphic properties, or field evidence.

## 9. Control Authority At The Effect Boundary

Prompts are not access control.

Prefer:

```text
agent proposal
→ structured intent
→ policy + current-state check
→ capability/effect gate
→ external action
→ durable receipt
```

Use:

- least privilege;
- expiring/revocable capabilities;
- idempotency;
- replay protection;
- cancellation semantics;
- isolation;
- explicit irreversible-action policy.

For critical effects, enforcement must live outside the agent's editable reasoning path.

## 10. Budget And Stop

Track at least:

- wall time;
- model/tool cost;
- attempts;
- branches;
- external effects.

A retry is justified only if something material changed:

```text
new evidence
new hypothesis
new decomposition
new tool
new skill
new context
new authorization
```

Otherwise stop or escalate.

## 11. Add Self-Improvement Only When Needed

Name the mutable object:

```text
memory
skill
tool
workflow/scaffold
verifier
model
```

Use a transactional admission path:

```text
failure/opportunity
→ responsibility attribution
→ smallest justified mutation
→ candidate fork
→ historical regression
→ held-out evaluation
→ adversarial/safety checks
→ compare with incumbent
→ promote / reject / canary
→ retain lineage + rollback
```

Rules:

- preserve the incumbent;
- later is not automatically better;
- do not learn from impossible/invalid tasks as if they were skill failures;
- do not let a candidate alter the verifier or authority policy that judges its own admission;
- move slowly as mutations approach verifier, objective, or governance semantics.

## 12. Separate Repository Truth From World Truth

Repository evidence can establish:

- implementation conformance;
- proof validity;
- package consistency.

It cannot establish by itself:

- customer value;
- scientific truth;
- policy legitimacy;
- acceptable distribution of harms/benefits.

Where the loop is product- or world-facing, attach a falsifiable field hypothesis.

Example:

```text
AC-42:
  invariant:
    no accepted transaction is silently lost

  repository evidence:
    property tests + replay tests + proof

  field hypothesis:
    reconciliation incidents remain below threshold X

  invalidation:
    recurring real-world losses or contradictory support evidence
```

For scientific loops, also preserve an epistemic-process claim:

```text
hypothesis
  -> test
  -> evidence
  -> judgment
  -> commitment or belief revision
```

Require the trace to show evidence uptake, treatment of contradictory results,
and convergent or otherwise discriminating tests. Derive it from source-bound
event and tool records, and independently validate its nodes and edges against
those raw records; an agent explanation cannot be the sole evidence. A
successful result is not enough to establish that the process was scientifically
self-correcting. This distinction is motivated by Ríos-García et al.,
[arXiv:2604.18805v1](https://arxiv.org/abs/2604.18805v1); use the paper as a
process-audit signal, not as evidence that every scaffold fails in the same way.

For autonomous science, also read the [Scientific Loop Template](./references/scientific-loop-template.md).

## 13. Certify Relationships, Not Just Files

For multi-artifact releases, local validity is insufficient.

A professional release should be able to show:

```text
requirement version
→ interpretation/specification
→ implementation boundary
→ tests/proofs
→ exact source/toolchain receipts
→ release claim
→ built/deployed bytes
```

Treat contradictions among individually green artifacts as a release failure.

## Design Output

For a concrete design, read the [Loop Design Template](./references/loop-design-template.md)
and return only the sections that apply. Keep unanswered questions under
`Residual Risk`; do not silently assume them away.
