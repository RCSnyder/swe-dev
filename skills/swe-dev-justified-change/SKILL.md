---
name: swe-dev-justified-change
description: A harness-neutral method for deciding whether a proposed or completed change is still justified by current evidence. Maps changed semantic layers, invalidates stale assurance, preserves counterevidence, checks authority and corrective capacity, and identifies the minimum evidence or safer scope needed next. Use for migrations, successor releases, branch merges, durable agent changes, model/spec/verifier changes, or self-modification; not for routine local reversible edits.
argument-hint: [change, migration, successor, release, agent mutation, model/spec/verifier change, or consequential action]
---

# Justified Change

Use this skill when the difficult part of a change is **continuity of justification** rather than ordinary implementation correctness.

The core question is:

> Given what changed, which prior claims and evidence still apply, what became stale or contradicted, what authority is justified now, can we still correct the result if wrong, and what is the smallest credible next step?

This skill is deliberately harness-neutral. It works with VS Code Copilot, GitHub Copilot CLI, Claude Code, or another coding/research harness using ordinary repository inspection, tests, shell commands, documents, and available tools. It has no runtime dependency on CETLab, Open Pincery, or a particular policy engine.

For compact schemas and examples, read `references/change-contract.md`. For high-consequence recovery analysis, read `references/corrective-closure.md`. When a decision is blocked by uncertainty, read `references/evidence-planning.md`. Load `references/prior-art-and-boundaries.md` only when novelty, research positioning, or architectural comparison matters.

## 0. Decide Whether This Skill Is Justified

Do **not** use the full method for an ordinary change where all of the following are true:

- local scope;
- reversible;
- no durable external side effect;
- no inherited approval/certification/assurance whose applicability is in question;
- no model/specification/verifier/authority change;
- no long-lived autonomous actor whose future permissions depend on current evidence.

Use normal engineering: implement, test, review, ship.

Use this skill when one or more of these are true:

- the successor inherits claims or evidence from a predecessor;
- a migration or merge changes semantics while preserving identifiers;
- an assumption can expire at runtime;
- model/specification/verifier changes can alter what old evidence means;
- an agent or system changes itself or its decision process;
- the proposed action is high-impact, persistent, expensive, or difficult to reverse;
- authorization should narrow when evidence degrades;
- prior counterevidence must not be silently forgotten;
- recovery depends on multiple components that may share failure domains.

## 1. Establish The Predecessor And Successor

Write the transition explicitly:

```text
Predecessor:
Successor / proposed action:
Why now:
User / system intent:
Expected benefit:
Side effects:
Reversibility:
Time pressure / irreversibility horizon:
```

If there is no meaningful predecessor, treat the current baseline as the predecessor. Do not invent historical assurance that cannot be recovered from artifacts or user-provided facts.

A successful build or test of the successor does not by itself establish continuity with the predecessor.

## 2. Classify What Changed

Use the shallowest truthful change layer. Multiple layers may change.

```text
runtime         values, workload, environment, observed state
implementation  code, configuration, dependency implementation
architecture    boundaries, interfaces, topology, persistence/concurrency model
model           causal/world/system model used to reason about behavior
specification   requirements, invariants, acceptance semantics
verifier        tests, proof/checker semantics, evidence-production mechanism
governance      authority, policy, approval or capability semantics
meta-governance process that changes/verifies governance or verifier rules
```

Do not infer low depth merely from line count. A one-line policy/verifier change can be deeper than a thousand-line implementation change.

For every changed layer, ask:

1. What old proposition depended on the old meaning?
2. What evidence was produced under that meaning?
3. Does the evidence still discriminate the failure the claim was meant to exclude?
4. If not, what explicitly transports or replaces the claim?

## 3. Convert Trust Labels Into Claims

Replace labels such as:

```text
safe
ready
approved
verified
tested
compatible
healthy
trusted
```

with concrete propositions.

Bad:

```text
The migration is safe.
```

Better:

```text
CLAIM-17:
Every record accepted by schema v2 can be read by the v1 rollback binary during the 24-hour rollback window.
```

For each consequential claim capture:

```text
id:
statement:
scope:
assumptions:
sensitive_layers:
support:
contradicting_evidence:
validity_domain:
freshness / expiry:
verifier / producer:
```

Do not treat the schema as sacred. Preserve the semantics.

## 4. Evaluate Evidence By Semantic Reach

Every evidence item must answer:

### Admissibility

- Was it actually produced?
- Is it source/artifact/environment bound where necessary?
- Is it fresh enough for the claim?
- Is its producer/verifier within the stated trust boundary?

### Discrimination

- What invalid alternative would make the check fail?
- Has a known-bad or mutation/negative case been tested when feasible?
- Could the evidence pass even if the target failure still existed?

### Semantic reach

Examples:

```text
compile                 -> structural/type validity only
test                     -> covered behavior only
property/fuzz/mutation   -> broader behavioral evidence in explored domain
model checker            -> formal property in the supplied model
kernel-checked proof     -> proposition under explicit axioms/assumptions
SLSA/in-toto provenance  -> how an artifact was produced, not behavioral safety
runtime telemetry        -> observed field behavior, not universal proof
human approval           -> authority/acceptance, not empirical truth
```

Never upgrade evidence beyond its reach.

## 5. Compute Applicability After Change

For each critical claim, return one status:

- `PRESERVED` — existing support remains semantically applicable.
- `STALE` — support may once have justified the claim but a changed dependency, expiry, or validity-domain exit means it no longer authorizes action.
- `INVALID` — explicit counterevidence contradicts the claim in the relevant scope.
- `TRANSPORTED` — an explicit transition witness justifies carrying the claim across changed semantics.
- `REPLACED` — the old claim is retired and a new semantic identity is introduced with explicit replacement justification.
- `UNKNOWN` — available evidence cannot determine applicability; do not silently choose `PRESERVED`.

### Invalidation rule

If an assumption or meaning-bearing dependency changes, dependent assurance is stale until restored:

```text
changed assumption/model/spec/verifier/governance
  -> affected claim support becomes stale
  -> dependent approvals/authority become stale
  -> restore only with independent applicable support, revalidation, or explicit transition witness
```

### No silent resurrection

If a predecessor recorded a critical claim as `INVALID` or `STALE`, a successor may not simply present the same semantic claim as `PRESERVED` because history was compacted, a branch was merged, or context was replaced.

Require one of:

- new discriminating evidence;
- explicit correction of the prior counterevidence;
- a valid scope distinction;
- a replacement/transport witness.

Preserve contradictions as data. Consensus is not a substitute for resolving an explicit counterexample.

## 6. Detect Semantic Identity Drift

Stable IDs help only if stable IDs retain stable meaning.

Ask:

```text
same identifier?
same proposition?
same scope?
same assumptions?
same verifier semantics?
same authority semantics?
```

If the ID is unchanged but the meaning changed, treat it as semantic drift. Do not infer continuity.

Preferred operations:

```text
preserve   -> same claim semantics, applicable support survives
transport  -> semantics changed but explicit witness proves relevant continuity
replace    -> old identity retired; new identity introduced with explicit relation
merge      -> divergent parent meanings reconciled with explicit resolution
```

## 7. Separate The Five Action Questions

For consequential action `a`, evaluate independently:

```text
CAN(a)          Is it technically/physically feasible under the current model?
KNOW(a)         Are the relevant factual/behavioral claims sufficiently supported now?
MAY(a)          Does this actor have authority for this action and scope?
ADMISSIBLE(a)   Does the action satisfy governing safety/normative/policy constraints?
RECOVER(a)      If wrong, does a credible timely corrective path remain?
```

Do not collapse these into a single `safe=true` field.

Examples:

- `CAN=true`, `MAY=false`: technically possible, unauthorized.
- `MAY=true`, `KNOW=false`: authorized actor, insufficient evidence.
- first four true, `RECOVER=false`: justified belief but unacceptable irreversible exposure.

## 8. Check Corrective Capacity For Consequential Effects

For ordinary reversible work, a normal rollback/test plan may suffice.

For high-impact work, trace a corrective path:

```text
observe
-> diagnose
-> construct repair / safe alternative
-> verify
-> authorize
-> execute
-> validate
```

Then ask:

- Can each step actually run after the proposed change?
- Is the path fast enough before irreversibility?
- Do apparently redundant paths share the same service, verifier, credential, operator, data source, or failure domain?
- Does the action remove the last independent path for detecting or repairing its own failure?
- Can critical corrective capability be reconstructed if the primary mechanism fails?

Read `references/corrective-closure.md` when these questions matter.

## 9. Produce An Authority Envelope, Not Just Yes/No

Prefer the smallest justified scope.

Verdicts:

```text
ADMIT              full proposed scope justified
CONSTRAIN          smaller/reversible scope justified
REQUIRE_EVIDENCE   named uncertainty or stale claim blocks full action
REQUIRE_AUTHORITY  evidence may suffice; authority does not
SHADOW             observe/simulate without consequential side effect
BLOCK              known contradiction, unacceptable irreversibility, or lost correction path
```

Useful constraints include:

- canary percentage;
- one workspace/tenant;
- read-only mode;
- simulation/shadow mode;
- short TTL;
- rate or budget cap;
- mandatory telemetry;
- automatic rollback condition;
- human approval before expansion.

Authority should normally decrease when evidence becomes stale, the environment becomes anomalous, action depth increases, reversibility falls, or corrective capacity degrades.

## 10. Find The Minimum Evidence Plan

A `REQUIRE_EVIDENCE` result should identify what to do next.

For every blocking claim, enumerate credible evidence-producing actions:

```text
run targeted regression
construct known-bad mutation
run model checker
collect runtime observation
perform canary
inspect provenance
ask domain owner
reproduce counterexample
build transition witness
split claim scope
```

Prefer the least-cost path that actually discriminates the uncertainty.

Do not recommend evidence that is merely easy to collect if it cannot change the decision.

Read `references/evidence-planning.md` for the full method.

## 11. Handle Branches And Merges

For two parents `A` and `B`, do not merge assurance by ID alone.

Check:

```text
claim exists in both?
semantic fingerprint equivalent?
support sets compatible?
counterevidence retained from both?
validity domains compatible?
authority scopes compatible?
```

If parents disagree, require explicit resolution. A code merge that compiles and passes tests does not automatically merge the reasons the two branches were trusted.

## 12. Handle Self-Modification Carefully

If the candidate changes:

```text
memory
skill/tool
workflow/scaffold
world model
specification
verifier
authority policy
governance-change process
```

increase scrutiny with depth.

Rules:

- preserve the incumbent until candidate admission succeeds;
- a candidate may propose changes to its evaluator, but must not be the sole authority approving those changes;
- preserve evidence and counterevidence across the mutation;
- require held-out or independent evaluation where feasible;
- use a canary or constrained authority before broad promotion;
- treat verifier or governance mutation as a different class from ordinary code mutation.

## 13. Distinguish Repository Truth From World Truth

Repository evidence can establish things like:

- source/build integrity;
- implementation behavior under tests;
- proof validity under its assumptions;
- package consistency.

It does not by itself establish:

- customer value;
- scientific truth;
- business legitimacy;
- external policy legitimacy;
- absence of real-world harm outside modeled scope.

When a claim is world-facing, attach field evidence or an explicit falsifiable assumption.

## 14. Output A Justified Change Packet

Return the smallest useful packet. For robust/deep work use:

```text
# Justified Change Packet

Mode: fast / robust / deep

## Intent
Predecessor:
Successor / action:
Expected benefit:
Consequence / reversibility:

## Change Surface
Changed layers:
Meaning-bearing changes:
Unchanged boundaries relied upon:

## Critical Claims
- CLAIM-* statement, scope, assumptions, sensitivity

## Evidence Applicability
- evidence -> claim -> PRESERVED / STALE / INVALID / TRANSPORTED / REPLACED / UNKNOWN

## Counterevidence And History
Prior invalidations/disagreements that must survive:

## Action Judgment
CAN:
KNOW:
MAY:
ADMISSIBLE:
RECOVER:

## Corrective Capacity
Primary correction path:
Shared failure domains:
Irreversibility / deadline:
Remaining unknowns:

## Verdict
ADMIT / CONSTRAIN / REQUIRE_EVIDENCE / REQUIRE_AUTHORITY / SHADOW / BLOCK
Permitted scope:
Expiry / re-check trigger:

## Minimum Evidence Plan
1.
2.
3.

## Transition Semantics
Preserved claims:
Transport witnesses:
Replacements / retirements:
Unresolved semantic drift:

## Residual Uncertainty
Explicit unknowns and assumptions:
```

Do not fill sections with ceremony. Omit irrelevant fields in fast mode.

## 15. Stop Conditions

Stop and escalate instead of looping when:

- no available evidence can discriminate the blocking uncertainty;
- the only proposed verifier is controlled by the candidate it judges;
- necessary authority cannot be obtained;
- all corrective paths are unavailable or slower than irreversibility;
- the system cannot reconstruct the predecessor/claim semantics well enough to justify transport;
- repeated attempts reproduce the same state without new evidence.

A precise blocker with options is a successful outcome.

## 16. Quality Check

Before finishing, ask:

- Did I distinguish “new thing works” from “old justification still applies”?
- Did I preserve counterevidence?
- Did I state what each evidence item actually proves?
- Did I separate knowledge, authority, admissibility, and recovery?
- Did I avoid fake precision or an unsupported aggregate score?
- If I blocked the action, did I identify the cheapest credible path forward?
- Did I keep the framework smaller than the problem warrants?
