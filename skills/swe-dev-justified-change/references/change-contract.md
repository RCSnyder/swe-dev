# Change Assurance Contract

Use this reference when a change needs a durable, reviewable packet rather than conversational advice.

## 1. Minimal Entities

A harness can represent these as Markdown, YAML, JSON, database rows, or ordinary prose. Preserve the semantics rather than forcing a format.

### Claim

```yaml
id: CLAIM-17
statement: Every accepted v2 record remains readable by the rollback binary.
scope: migration window
assumptions:
  - ASSUME-4
sensitive_layers:
  - implementation
  - architecture
  - specification
support:
  - EVID-22
  - EVID-23
contradicts: []
validity_domain: rollback window <= 24h
status: PRESERVED
```

### Evidence

```yaml
id: EVID-22
kind: regression-test
producer: cargo test migration_roundtrip
subject: commit-or-artifact-digest
claim_reach: covered v1/v2 round-trip cases
freshness: current candidate
known_bad_discrimination: true
```

### Assumption

```yaml
id: ASSUME-4
statement: The rollback binary is retained and executable for 24 hours.
observed_by: deployment inventory
expiry: 24h after promotion
```

### Change

```yaml
id: CHANGE-9
layers:
  - implementation
  - specification
subjects:
  - schema
  - writer
semantic_summary: Null handling changed from reject to default.
```

### Transition witness

A witness is not necessarily a formal proof. It is explicit justification connecting old and new semantics.

```yaml
id: WITNESS-3
mode: transport
from: CLAIM-17@v1
to: CLAIM-17@v2
support:
  - EVID-31
argument: The new field is ignored by the rollback reader and round-trip tests cover all serialized variants.
```

### Action

```yaml
id: ACTION-8
intent: promote migration to 100 percent
requires:
  can: [CLAIM-20]
  know: [CLAIM-17]
  may: [AUTH-2]
  admissible: [CLAIM-25]
  recover: [CLAIM-30]
```

## 2. Status Semantics

`PRESERVED`: Current support remains applicable after the change.

`STALE`: The claim may still be true, but its previous support no longer justifies action in the current state.

`INVALID`: Relevant counterevidence contradicts the claim.

`TRANSPORTED`: The claim crosses changed semantics through an explicit witness.

`REPLACED`: A new semantic identity supersedes the old one through an explicit replacement relation.

`UNKNOWN`: The available information does not support a stronger status.

Never make `UNKNOWN` silently mean `PRESERVED`.

## 3. Layer Sensitivity

Suggested order from shallow to deep:

1. `runtime`
2. `implementation`
3. `architecture`
4. `model`
5. `specification`
6. `verifier`
7. `governance`
8. `meta-governance`

This ordering is a reasoning aid, not a universal ontology. A domain may require different layers.

A claim sensitive to a changed layer is not automatically false. It is **in need of applicability analysis**.

## 4. Semantic Fingerprint Questions

When an ID survives a successor, compare at least:

- proposition text/meaning;
- scope;
- assumptions;
- validity domain;
- sensitivity/dependencies;
- verifier semantics;
- authority semantics if the entity is an approval/policy.

A stable identifier with changed meaning is semantic drift, not continuity.

## 5. Merge Contract

For each assurance identity present in multiple parents:

```text
same semantics?         yes -> union applicable independent support carefully
same status?            no  -> preserve stronger counterevidence until resolved
same assumptions?       no  -> split scope or require resolution
same verifier meaning?  no  -> require transition witness
```

Do not resolve `VALID` vs `INVALID` by majority vote.

## 6. Decision Receipt

A useful durable receipt contains:

```yaml
verdict: CONSTRAIN
permitted_scope: 5-percent canary
expires_at: 2026-08-16T03:00:00Z
blocking_claims:
  - CLAIM-17
invalidated_by:
  - CHANGE-9
required_next_evidence:
  - EVIDENCE-PLAN-4
authority_checked: AUTH-2
recovery_checked: CORRECTION-PATH-1
residual_unknowns:
  - behavior above peak historical load
```

A receipt is an explanation/provenance object. It is not cryptographic attestation unless separately signed or bound by a trusted mechanism.
