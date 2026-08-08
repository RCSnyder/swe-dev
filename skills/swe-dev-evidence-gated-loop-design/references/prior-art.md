# Prior Art And Research Spine

Use this reference when explaining **why** the loop-design rules exist, comparing an architecture to prior work, or making novelty/research claims.

Do not cite this file as proof that an implementation is patentable or legally novel. Patent analysis depends on exact claims, dates, jurisdictions, and disclosures.

## Prior-Art Boundary: Do Not Claim These Primitives As New

| Primitive | Representative prior art | Implication |
|---|---|---|
| reason/act/observe loop | ReAct (2022), arXiv:2210.03629 | Iterative tool-using agent loops are foundational |
| self-critique / refinement | Reflexion (2023), Self-Refine (2023) | Retry + reflection is not novelty |
| role-specialized agentic SDLC | ChatDev, MetaGPT; US20250165890A1 claims Nov. 22, 2023 provisional priority | planner/coder/tester/reviewer pipelines are crowded prior art |
| requirements ↔ code/test traceability | US20130086556A1 / US8799869B2; US20150095890A1 | trace links and test coverage management predate LLM agents |
| coding-agent harness | SWE-agent, OpenHands | tool/shell/repository harnessing is established |
| formal verification | decades of theorem proving, model checking, Hoare/refinement/separation logic | proof checking itself is not an agent innovation |
| self-modifying agent scaffold | ADAS, SICA, Darwin Gödel Machine | agent architecture search and self-modification are established |
| closed-loop science | Robot Scientist lineage, self-driving laboratories | hypothesis → experiment → evidence → update is established |

The interesting engineering frontier is **how these primitives are composed and controlled**, not the existence of the primitives.

## Highest-Value Current Signals

### 1. Loop Specification As A First-Class Artifact

**Sandeco Macedo — Stop Hand-Holding Your Coding Agent: Engineering the Loops that Replace Step-by-Step Prompting**
arXiv:2607.00038 — 2026 preprint
https://arxiv.org/abs/2607.00038

High-value signal:

```text
loop = trigger + goal + verification + stopping + memory
```

It distinguishes the external recurring loop from both ordinary programming loops and the harness's internal act/observe plumbing.

Design consequence:

- define the loop before optimizing prompts;
- name terminal states;
- treat durable memory and automated triggering as explicit engineering surfaces.

### 2. Lifecycle State Must Be Evidence-Gated

**Huang et al. — Proof-or-Stop: Don't Trust the Agent, Trust the Evidence**
arXiv:2607.14890 — 2026 preprint
https://arxiv.org/abs/2607.14890

High-value signal:

```text
agent statement = claim
lifecycle transition = predicate over fresh source-bound evidence
```

The paper explicitly binds evidence to tracked source state and mechanically checks lifecycle gates.

Design consequence:

- `DONE` cannot be agent-authored truth;
- stale receipts cannot authorize a new revision;
- review should be enforced as a gate when required, not merely suggested by another agent.

### 3. Long-Horizon Loops Need Persistent Regression Obligations

**Li et al. — LoopsBench: From Harness Engineering to Loop Engineering in Benchmarking Coding Agent**
arXiv:2608.00267 — 2026 preprint
https://arxiv.org/abs/2608.00267

High-value signal:

Long-horizon work is not "one big SWE-bench task." It has prerequisite structure and already-completed obligations that must remain valid as later work changes the repository.

Design consequence:

- represent dependency structure;
- retain completed work as regression obligations;
- evaluate sustained evolution, not only final snapshot success.

### 4. Verification Is A Moving Proxy For Intent

**Wang et al. — The Verification Horizon: No Silver Bullet for Coding Agent Rewards**
arXiv:2606.26300 — 2026 preprint
https://arxiv.org/abs/2606.26300

High-value signal:

Verifier quality has at least three dimensions:

- scalability;
- faithfulness;
- robustness.

No fixed reward/verifier remains adequate indefinitely as generators improve.

Design consequence:

- never equate the current checker with human intent;
- use verifier portfolios;
- evolve verification only through an independent process.

### 5. A Green Test May Not Test The Bug

**Xu & Wu — Validation Evidence in LLM Repair Agents: How Much of What Passes Actually Tests the Bug?**
arXiv:2607.28871 — 2026 preprint
https://arxiv.org/abs/2607.28871

High-value signal:

A large fraction of positive validation events in the study carried no bug-discriminating information.

The useful abstraction is **contrastive evidence**:

```text
buggy state   → fail
candidate     → pass
known-good    → pass, when available
```

Design consequence:

Evidence should record not just `pass`, but **what invalid alternative it rules out**.

### 6. Formal Proof Does Not Solve Intent Formalization

**Agarwal et al. — Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization**
arXiv:2605.26457 — 2026 preprint
https://arxiv.org/abs/2605.26457

High-value signal:

A proof can be valid relative to a generated formal specification while the specification itself omits or distorts intended constraints. Their executable/adversarial evaluator catches failures missed by LLM judging.

Design consequence:

Keep separate gates for:

```text
intent → specification faithfulness
specification → implementation conformance
```

Formal methods harden the second edge. They do not erase the first.

### 7. Traceability Graphs Are Already Entering Agentic SDLC Research

**Chen et al. — TraceDev: A Traceability-Driven Multi-agent Framework for Requirement-to-Code Development**
arXiv:2607.18886; ISSTA 2026 research paper
https://arxiv.org/abs/2607.18886

High-value signal:

TraceDev maintains a heterogeneous graph linking requirements, design models, and code artifacts across specialized agents.

Design consequence:

Do not position "agentic traceability graph" alone as novel.

The harder frontier is:

- source-bound evidence;
- test/proof links;
- actual-vs-declared dependency reconciliation;
- invalidation propagation;
- field evidence;
- authority provenance.

### 8. Typed Semantic Repair Beats Blind Regeneration As A Control Primitive

**Ruslan Khrulev — BlueprintRepair: Typed Local Edits for Failed Lean Proof Blueprints**
arXiv:2607.28110 — 2026 preprint
https://arxiv.org/abs/2607.28110

High-value signal:

The editable object can be a typed dependency graph, with kernel checking and explicit declared dependency constraints, rather than arbitrary source rewriting.

Design consequence:

- repair the smallest responsible semantic object;
- retain provenance;
- verify that declared graph edges reflect actual proof dependencies where feasible.

### 9. Release Validity Is Relational, Not Merely Local

**Tengjiao Liu — Beyond Object Validation: Relational Conformance in Multi-Artifact Agent Releases**
arXiv:2607.14155 — 2026 preprint
https://arxiv.org/abs/2607.14155

High-value signal:

Individually valid artifacts can contradict each other. The proposed profile treats claims, evidence, authority, lineage, and published bytes as a graph whose relationships must be consistent.

Design consequence:

The certified object for a serious release should approach:

```text
consistent(claims, evidence, authority, lineage, bytes)
```

not merely:

```text
all files individually validated
```

Caution: the paper presents a candidate profile and motivating mechanisms; comparative evidence for the full profile remains open.

### 10. Translation Edges Have Different Assurance Strength

**Christoph Kirsch — Untrusted Authors, Trusted Answers: A Calculus of Fidelity-Graded Translations**
arXiv:2607.14137 — 2026 preprint
https://arxiv.org/abs/2607.14137

High-value signal:

Semantic transformations can be modeled as a graph with different fidelity grades; independent routes can corroborate one another, and end-to-end assurance is constrained by weak transformations.

Design consequence:

A professional trace graph should not pretend these edges are equivalent:

```text
human intent → formal spec       interpretive
formal spec → code contract      translation/validation
contract → implementation        deductive, when proved
implementation → field outcome   empirical
```

This provides a useful formal lens for heterogeneous evidence chains.

### 11. Agent-Framework "Approval" Is Not Necessarily An Enforcement Boundary

**Sajjad Khan — Stop Means Stop: Measuring and Repairing the Enforcement Gap in Agent-Framework Control Primitives**
arXiv:2607.14166 — 2026 preprint
https://arxiv.org/abs/2607.14166

High-value signal:

The paper reports approval/cancellation/timeout enforcement gaps across tested agent frameworks and proposes SOUNDGATE, an environment-external effect gate with model-checked/verified properties.

Design consequence:

- do not rely on conversational or framework-local "approval required";
- mediate side effects at an external reference monitor/effect boundary;
- design replay, cancellation, and sibling concurrency semantics explicitly.

### 12. Persistent Self-Improvement Needs Admission Gates

**Jia et al. — VeriSkill: A Self-Evolution Framework for Program Verification Skills**
arXiv:2607.27733 — 2026 preprint
https://arxiv.org/abs/2607.27733

High-value signal:

Verification failures are attributed before becoming reusable skills, and candidate skill revisions are admitted only when verification improves while executable program semantics are preserved.

Design consequence:

```text
failure
≠ automatically learn a lesson
```

Use:

```text
failure attribution
→ reusable hypothesis
→ candidate skill
→ held-out/executable validation
→ admission
```

### 13. Outcome Success Does Not Establish Scientific Reasoning

**Ríos-García et al. - AI scientists produce results without reasoning scientifically**

arXiv:2604.18805v1 - 2026 preprint

https://arxiv.org/abs/2604.18805v1

High-value signal:

Across more than 25,000 agent runs in eight domains, the study's performance
analysis attributes 41.4% of explained variance to the base model versus 1.5%
to the agent scaffold. In the behavioral analysis of annotated traces, evidence
non-uptake occurred in 68% of traces, beliefs were never updated in 71%,
refutation-driven belief revision occurred in 26%, and convergent multi-test
evidence occurred in 7%. These are process-prevalence measures, not full-run
success rates. Agents could complete workflows without exhibiting the evidence
uptake and belief revision that make inquiry self-correcting.

Design consequence:

- do not treat successful workflow completion or final-answer accuracy as evidence that a research loop reasoned scientifically;
- record an epistemic trace linking hypothesis, test, evidence, judgment, and commitment;
- derive the trace from source-bound event and tool records; an agent explanation may annotate it but cannot be its sole evidence;
- independently validate the trace's nodes and edges against the raw records before using it as a lifecycle gate;
- gate scientific closure on evidence uptake, explicit handling of contradiction, belief revision, and convergent or otherwise discriminating tests;
- treat scaffold changes as interventions to evaluate, not guaranteed repairs.

Scope caution:

The evaluation used independent episodes, three models, two simple scaffolds,
fixed 20-40-call budgets, and no advanced orchestration, constrained decoding,
or retry-with-repair mitigation. Use it to justify process-level audits and
better evaluation, not to claim that all agent architectures fail identically.

### 14. Progressive Disclosure Is A Reliability Control

Current implementation guidance converges on a layered customization model:

- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) treats skills as task-specific, on-demand workflows with optional references and scripts.
- The [Agent Skills specification](https://agentskills.io/specification) recommends a small `SKILL.md` body, progressive disclosure, and focused reference files loaded only when needed.
- [Anthropic's context-engineering guidance](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) treats context as a finite attention budget and recommends high-signal instructions, just-in-time retrieval, structured notes, compaction, and focused subagents for long horizons.
- [Anthropic's effective-agent guidance](https://www.anthropic.com/research/building-effective-agents) recommends starting with the simplest workflow that works, adding agentic complexity only when evaluation shows it helps, and making tool interfaces explicit and testable.

Design consequence:

- keep the always-selected agent focused on routing, behavior, and output shape;
- keep the activated skill procedural and compact;
- move research registries, long templates, and source audits into references;
- make the description precise enough to discover the skill for the right task;
- evaluate real task outcomes with held-out cases instead of optimizing prose by inspection alone.

## The Professional Synthesis

The most defensible professional architecture emerging from the literature is:

```text
authorized intent
  ↓
explicit acceptance claims
  ↓
semantic/formal specifications where useful
  ↓
implementation
  ↓
portfolio of empirical + formal verification
  ↓
source-bound evidence receipts
  ↓
relational release consistency
  ↓
external authority/effect gate
  ↓
deployed behavior
  ↓
field evidence
  ↓
change-impact invalidation / repair
```

For self-improving systems, add a separate meta-loop:

```text
trajectory/failure
  ↓
responsibility attribution
  ↓
candidate skill/tool/workflow mutation
  ↓
isolated evaluation
  ↓
compare with incumbent
  ↓
promote / reject / canary / rollback
```

The candidate should not control:

- the evidence schema that judges it;
- the authority root;
- the audit root;
- or the verifier-change process used for its own admission.

## What Remains Open

No single system in this research spine demonstrates the entire chain at repository/production scale:

```text
changed human intent
→ competing semantic interpretations
→ updated formal/executable specification
→ impact analysis across architecture/code/tests/proofs
→ selective repair
→ fresh source-bound evidence
→ relationally certified release
→ authorized world effect
→ field feedback
→ validated improvement of the loop itself
```

That end-to-end problem is the interesting research target.

The strongest positioning is therefore not:

> "We invented multi-agent loop engineering."

It is:

> **We are engineering a continuously valid evidence and authority chain across an evolving autonomous software lifecycle, including governed evolution of selected parts of the loop itself.**

## Source Status

Treat the 2026 arXiv papers above as frontier research, not settled industry standards.

Use peer-reviewed papers, mechanized artifacts, source code, benchmarks, and production evidence when available.

For legal novelty or patentability, perform a separate claim-focused prior-art search.
