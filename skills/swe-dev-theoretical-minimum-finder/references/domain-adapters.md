# Domain Adapters

The theoretical-minimum workflow is domain-general, but evidentiary rules are not. Use the adapter closest to the target and combine adapters for interdisciplinary work.

## Mathematics and theoretical computer science

Prefer:
- original papers for named theorems/results;
- authoritative textbooks/monographs for current standard formulations;
- formal definitions and proofs over popular explanations.

Core artifact should emphasize:
- primitive definitions;
- theorem assumptions;
- proof ideas and counterexamples;
- equivalence/non-equivalence of formulations;
- lower bounds and impossibility results;
- canonical problem classes only when source status is supported.

Hallucination risks:
- remembering theorem hypotheses incompletely;
- inventing attribution/priority;
- quoting a theorem stronger than the actual result;
- confusing folklore with published result.

Mastery tests should require derivation/proof/counterexample, not vocabulary recall.

## Software engineering, systems, and computing practice

Prefer:
- original systems/research papers;
- official specifications and maintained documentation for current behavior;
- standards bodies;
- source code/release notes when implementation behavior matters;
- authoritative textbooks for durable theory.

Separate:
- mathematical/model guarantees;
- implementation guarantees;
- operational guidance;
- vendor claims;
- field folklore.

Current versions matter. Never use an old API/standard claim as current without checking.

Strong theoretical-minimum units often organize around state, information, composition, concurrency, failure, resources, control, and evolution rather than frameworks.

## Natural and experimental sciences

Prefer:
- original peer-reviewed studies for specific experiments;
- systematic reviews/meta-analyses or authoritative reviews for synthesis;
- official datasets and instrumentation/method papers;
- major textbooks for mature theory.

Track:
- population/sample;
- experimental design;
- measurement method;
- uncertainty/error bars;
- replication status;
- causal versus correlational claims;
- model regime and boundary conditions.

Do not treat one paper as consensus. A famous result may have been revised, narrowed, or disputed.

Mastery tests should include experimental design, model discrimination, and interpretation of anomalous data.

## Medicine and health

This adapter raises the evidentiary bar.

Prefer:
- current clinical guidelines from authoritative bodies;
- systematic reviews/meta-analyses;
- major randomized trials for intervention claims;
- regulatory labels/safety notices;
- primary epidemiological datasets where relevant.

Always separate:
- mechanistic plausibility;
- surrogate endpoints;
- clinical outcomes;
- population-specific evidence;
- guideline recommendation strength.

Use current sources. Flag jurisdiction and date. Never convert a research dossier into individualized medical advice.

## Law and regulation

Pin jurisdiction and date.

Prefer:
- statutes/regulations;
- court opinions;
- official agency guidance/orders;
- legislative history where relevant;
- authoritative treatises/reviews for synthesis.

Distinguish:
- binding authority;
- persuasive authority;
- agency interpretation;
- scholarly interpretation;
- unsettled/contested doctrine.

Do not claim current law from memory. Search current official sources. Quote exact language only when inspected.

Mastery tests should include rule extraction, fact-pattern transfer, counterargument, and authority hierarchy.

## History and humanities

Prefer a mixed evidentiary stack:
- primary archival/historical sources for what actors recorded;
- scholarly monographs/articles for interpretation;
- historiographical reviews for major schools/debates.

Do not collapse interpretation into 'fact'. Distinguish:
- event/record;
- source perspective and bias;
- later scholarly interpretation;
- contested historiography.

Avoid fake balance: include disputes that actually exist in scholarship.

Mastery tests should ask the learner to interpret the same evidence under competing frameworks and identify which claims the source can and cannot support.

## Economics, markets, and business

Prefer:
- official statistics and datasets;
- filings and audited reports;
- central bank/government material;
- peer-reviewed or high-quality working papers;
- company documentation for company-specific facts;
- reputable industry research for contextual estimates, clearly labeled.

Separate:
- accounting fact;
- market observation;
- causal economic claim;
- management narrative;
- forecast;
- strategic synthesis.

Current data is time-sensitive. Record observation date. Do not present forecasts as facts.

Mastery tests should include alternative causal explanations, incentive analysis, unit economics, sensitivity, and decision under uncertainty.

## Security and safety

Prefer:
- official advisories/CVEs and vendor patches for current vulnerabilities;
- standards and threat-model references;
- peer-reviewed security/safety research;
- incident/postmortem evidence when primary and available.

Keep the artifact defensive and analytical. Focus on threat models, invariants, failure classes, mitigation principles, and verification—not operational abuse instructions.

For safety, distinguish component reliability from system-level unsafe control/interactions.

## AI and fast-moving emerging technology

Assume high temporal volatility.

Prefer:
- current papers/preprints for frontier claims;
- official model/system cards and technical reports for system-specific behavior;
- code/release notes for implementations;
- benchmarks only with their dataset/method limits visible;
- independent replications when available.

Distinguish:
- demonstrated capability;
- benchmark result;
- product claim;
- extrapolation;
- speculative mechanism;
- social/market forecast.

Do not call a frontier result established because it is popular. Record version/date precisely.

## Philosophy and conceptual domains

Prefer:
- primary texts for an author's actual argument;
- scholarly editions/commentary for historical context;
- reputable secondary literature for major interpretations.

Theoretical minimum should include competing definitions, argument structures, counterexamples, and distinctions—not force empirical-style consensus.

Mastery tests should require reconstruction and objection/reply, not just attribution.

## Interdisciplinary topics

Do not let one domain's evidence rules colonize another.

Example: an AI-in-medicine theoretical minimum may need:
- ML papers for algorithmic claims;
- clinical evidence for health outcomes;
- regulatory sources for legal status;
- human-factors/safety literature for operational risk.

Create separate claim lanes and only synthesize after each lane is grounded under its own standards.
