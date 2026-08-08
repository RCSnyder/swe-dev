# Scientific Loop Template

Use this extension for autonomous research, experiment-as-code, laboratory, or
simulation loops. Keep ordinary engineering designs on the smaller template.

```markdown
# Scientific Loop Design

## Authorized Objective
What question is authorized, by whom, and what is explicitly out of scope?

## Safety And Resource Envelope
Materials, actions, instruments, budgets, permissions, containment, and rollback.

## Competing Hypotheses
| Hypothesis | Prediction | Falsifier | Prior uncertainty |
|---|---|---|---|

## Experiment Contract
| Field | Definition |
|---|---|
| Selection rule | Why this experiment is more informative than alternatives |
| Declarative intent | What the experiment is meant to test |
| Compilation | How intent becomes executable instrument actions |
| Measurement | What is observed and with what calibration |
| Provenance | Source, instrument, environment, parameters, and raw artifacts |
| Stop rule | When to stop, branch, replicate, or escalate |

## Epistemic Trace
hypothesis -> test -> observation -> analysis -> judgment -> belief revision

The trace is derived from immutable event, tool, instrument, and artifact records.
An agent explanation may annotate it but cannot be its sole evidence.

## Evidence Gates
Require, as applicable:

- the test discriminates at least one competing explanation;
- measurements and analysis code are linked to exact source and environment state;
- calibration, missing data, uncertainty, and negative results are recorded;
- contradictions trigger revision, a retest, a competing hypothesis, or escalation;
- independent review or replication is obtained before strong closure claims;
- the conclusion states what was not established.

## Lifecycle
INTAKE -> HYPOTHESES -> DESIGNED -> SAFETY_CHECKED -> EXECUTING -> MEASURED
-> ANALYZED -> REVISED / REPLICATED / STOPPED

## Failure Routing
| Observation | Route |
|---|---|
| unsafe or unauthorized action | safety / governance |
| invalid or uncalibrated measurement | instrument / measurement |
| analysis cannot support the claim | statistics / causal model |
| result contradicts prediction | hypothesis revision |
| repeated test is uninformative | experiment design |
| agent ignores evidence | epistemic verifier / model evaluation |
| budget or resource exhaustion | stop / escalate / re-scope |

## Residual Risk
What remains uncertain about measurement validity, causal interpretation,
replication, generalization, and real-world significance?
```

Do not promote a result to a scientific conclusion merely because the workflow
ran, the simulation completed, or one test produced a plausible answer.
