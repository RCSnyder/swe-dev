# Loop Design Template

Use this template for a durable, consequential, scientific, or self-improving
loop. Omit sections that do not apply; do not fill them with generic prose.

```markdown
# Loop Design

## Classification
class / autonomy horizon / side-effect level

## Invariants
MUST NEVER:
MUST EVENTUALLY:

## Loop Contract
trigger / goal / state / capabilities / budget / terminal states

## State Machine
...

## Evidence Gates
| Claim | Evidence | Discriminates | Freshness | Trust |
|---|---|---|---|---|

## Traceability
IDs, typed edges, invalidation rules

## Failure Routing
| Failure | Route |
|---|---|

## Authority
effect boundary and delegated capabilities

## Self-Improvement
only if applicable

## Residual Risk
what the evidence still does not establish

## Minimal Implementation
smallest code/data structures needed
```

## Definition Of Done

Before returning, answer:

1. What is the authoritative state?
2. What exact evidence promotes each consequential state?
3. What source/configuration state does that evidence cover?
4. What makes it stale?
5. Which failure routes to which upstream artifact?
6. How does the system resume after interruption?
7. What are its hard budgets and terminal states?
8. Which external effects require stronger authority?
9. If it self-improves, what remains outside the candidate's control?
10. What important claim is still only a proxy for real-world intent?

Put unanswered questions under `Residual Risk` rather than silently assuming
them away.
