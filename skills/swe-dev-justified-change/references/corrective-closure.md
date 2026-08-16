# Corrective Closure

Use this reference for changes where rollback, recovery, or future correction is material to the decision.

The purpose is not to calculate a magical resilience score. It is to expose whether a proposed action preserves a credible path for discovering and repairing error.

## 1. Trace The Correction Chain

Start with the failure or wrong-decision class that matters most.

```text
failure
-> observe
-> diagnose
-> choose / construct repair
-> verify repair
-> authorize effect
-> execute
-> validate outcome
```

For each step identify:

- concrete mechanism;
- owner/authority;
- dependency;
- latency;
- failure domain;
- whether the proposed action changes or removes it.

## 2. Common-Cause Awareness

Two paths are not independent merely because they have different names.

Examples of hidden shared failure domains:

- both verifiers run on the same control plane;
- both backups use the same corrupted credential or KMS;
- two agents use the same model/data source;
- “human fallback” and automated recovery depend on the same inaccessible dashboard;
- two suppliers depend on the same upstream service;
- rollback and forward repair both require a schema representation destroyed by the migration.

Represent common cause explicitly.

## 3. Temporal Requirement

A theoretically correct repair that completes after irreversible harm is not a viable correction path.

Estimate:

```text
t_detect
+ t_diagnose
+ t_prepare
+ t_verify
+ t_authorize
+ t_execute
+ t_validate
< t_irreversible
```

Use conservative ranges when exact timing is unknown.

If time pressure is itself uncertain, say so.

## 4. Corrective Distance

For a small system, ask qualitatively:

> What is the smallest independent set of failures that removes every credible corrective path?

If the answer is one, the system has a corrective single point of failure.

For more formal work, model capabilities and dependencies as a graph/hypergraph and use cut/path reasoning. Do not claim independence without inspecting shared failure domains.

## 5. Regeneration

Recovery mechanisms can themselves fail or decay.

Ask:

- Can the verifier be reconstructed?
- Can the build/deploy path be rebuilt?
- Can critical knowledge be regenerated from durable records?
- Can credentials/authority be restored without bypassing controls?
- Does one person/tool carry unique unreconstructible knowledge?

A running capability can be operationally healthy while becoming unreconstructible.

## 6. Action Effect On Correction

The critical question is often not:

> Does rollback exist before the action?

but:

> Does rollback/correction still exist after the action?

Examples:

- deleting telemetry can preserve functionality while destroying future diagnosis;
- consolidating independent verifiers can preserve test coverage while increasing common-mode failure;
- destructive schema migration can remove the representation needed by the rollback binary;
- changing authority policy can make emergency recovery impossible;
- agent self-modification can remove the only process capable of recognizing its own failure.

## 7. Output

```text
Failure class:
Primary correction path:
Alternative path(s):
Shared failure domains:
Irreversibility horizon:
Estimated correction latency:
Single points of corrective failure:
Capability lost after proposed action:
Regenerative dependencies:
RECOVER judgment: pass / constrained / unknown / fail
Recommended preservation or redundancy:
```
