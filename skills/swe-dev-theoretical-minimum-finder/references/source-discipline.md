# Source Discipline for the Theoretical Minimum Finder

This reference defines what may carry a claim in a theoretical-minimum dossier.

## Source tiers

| Tier | Source | Default treatment |
|---|---|---|
| 0 | User-provided local source, artifact, dataset, or text | Ground truth for what the source contains; not automatically ground truth about the world |
| 1 | Primary source: original paper, statute, court opinion, official dataset, standard/specification, source code/release, filing, canonical archival text | Authoritative for the claim it directly makes or records |
| 2 | Authoritative synthesis: graduate textbook, scholarly monograph, peer-reviewed review, major professional handbook | Strong synthesis / field-level grounding |
| 3 | Teaching or institutional source: university notes, official tutorials, reputable course pages, maintained reference docs | Strong pedagogy/context; use carefully for broad claims |
| 4 | Secondary explainer: encyclopedia, blog, news article, video, popular book | Orientation and discovery; do not let it carry the theoretical minimum |
| 5 | Model/agent synthesis, including this skill | Hypothesis, inference, organization, or proposed connection only |

Tier is about evidentiary role, not prestige. A primary paper is authoritative for what it did and claimed, not proof that its claim remains accepted. A modern review may be stronger for current consensus than a famous original.

A user-provided transcript or design brief is Tier 0 evidence for what the user wants the workflow to embody. It is not automatically evidence that its historical, scientific, or biographical claims are true.

## Claim classes

Use these internally and expose them in the Claims and Evidence ledger:

- **grounded** — directly supported by inspected Tier 0–2 evidence appropriate to the claim.
- **cross-checked** — grounded and independently supported by another source family.
- **contested** — credible inspected sources materially disagree.
- **tentative** — some evidence exists, but reach or quality is insufficient for a strong claim.
- **inference** — reasoned conclusion from cited evidence; not directly stated in the sources.
- **synthesis** — organizational or conceptual structure created by the agent.
- **unknown** — unresolved, inaccessible, or not searched enough.

Never silently upgrade a tentative or inferred claim to grounded prose.

## Source promotion rules

A source may become load-bearing only when:

1. its existence and identity are confirmed;
2. the relevant content was actually opened/read, not merely seen in a search result;
3. the source directly bears on the claim;
4. its date/version is appropriate to the claim;
5. the claim does not exceed the source's semantic reach.

Examples of semantic reach:

- a project README supports what the project says it does, not that the method is effective;
- a benchmark supports behavior under its benchmark conditions, not universal performance;
- a proof supports a theorem under its model/assumptions, not necessarily a production system;
- a vendor doc supports current product behavior, not neutral comparative superiority;
- a single historical paper supports authorship/history and the paper's argument, not present consensus;
- a search result snippet supports almost nothing beyond discovery.

## Minimum-inclusion claims

A source that explains a concept does not, by itself, prove that the concept belongs in the minimum for the pinned target capability.

Treat these as separate claims:

1. **Content claim:** what the unit means or how it works.
2. **Dependency claim:** which target performances or later units require it.
3. **Necessity claim:** what specifically fails if it is removed.
4. **Non-redundancy claim:** why retained units cannot cheaply replace it.

Ground content claims in appropriate domain sources. Ground dependency and curriculum-status claims in inspected curricula, prerequisite statements, task analyses, expert sources, or representative problems when available. When the dependency graph or deletion judgment is agent-created, mark it `[SYNTHESIS]` or `[INFERENCE]` even if the underlying content is well sourced.

Do not upgrade "this source covers X" into "every serious practitioner needs X." The second claim is broader and target-relative.

## Link verification states

Use one of these exact values in the Source Registry:

- `content` — source opened and relevant content inspected in this run.
- `existence-only` — title/identity/reachability confirmed, but substantive content not inspected.
- `blocked` — source is known but access failed or required unavailable credentials/tooling.
- `unverified` — candidate reference not validated in this run; cannot carry a load-bearing claim.

Do not write `verified: yes`.

## Multi-source rules

One source can be enough for:

- what a specific paper proposes;
- what a statute says at a cited date;
- what an official API/version documents;
- a mathematical theorem from a reliable primary/authoritative source.

Prefer independent cross-checking for:

- field-wide consensus;
- historical priority;
- prevalence/adoption;
- causal empirical claims;
- safety/medical/legal recommendations;
- claims that a work is canonical or definitive;
- contested political/social interpretations;
- current market or industry trends.

A second page that copies the first is not independent evidence.

## Canonical-status rule

Do not call a work **canonical**, **the standard**, **the definitive text**, or equivalent merely because it is famous or familiar to the model.

A stronger status claim needs evidence such as multiple independent authoritative curricula, scholarly reviews/histories, professional guidance, or repeated field adoption visible in inspected sources.

Safer alternatives:

- foundational original
- influential early work
- authoritative reference
- widely used in the inspected curricula
- recommended spine for this theoretical minimum
- primary source for this result

## Current-information rule

Treat the following as temporally unstable unless the user pins a historical date:

- software/product behavior and APIs
- laws, regulations, standards, policies
- officeholders and company leadership
- market structure, prices, adoption, and rankings
- active research frontier claims
- medical guidance
- security vulnerabilities and mitigations

Use current primary/official sources where available and record access date.

## Contradiction handling

When reliable sources conflict:

1. verify they are answering the same question and using compatible definitions;
2. identify whether disagreement is empirical, definitional, methodological, normative, or temporal;
3. represent the strongest version of each material view;
4. do not average incompatible claims into fake consensus;
5. state which conclusion, if any, the available evidence supports and with what confidence.

## Quotes and numbers

Exact quotations, page numbers, equation labels, dates, statistics, and percentages have a higher hallucination cost than paraphrase.

Use them only when inspected directly. Otherwise paraphrase and omit the precision.

## Search stopping rule

Do not browse endlessly. Stop when additional high-quality sources mostly repeat the same dependency structure, deletion passes are stable, material disputes have representative evidence, and every retained unit has enough support for its consequence.

The goal is evidence saturation, not bibliography size.
