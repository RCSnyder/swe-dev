# Performance-Aware Engineering — References and Intellectual Roots

This file contains the provenance, citations, historical context, and source material
behind `SKILL.md`.

It is intentionally separate so agents do not need to load citation material into
working context for ordinary coding tasks.

Use this file when:

- auditing why a principle exists;
- extending or revising the skill;
- checking historical context;
- validating a claim or base-rate source;
- tracing a concept back to primary or foundational material.

# Foundational Sources and Intellectual Roots
These references are not instructions to imitate historical code style.

They explain why the principles above exist.

## Edsger W. Dijkstra — A Constructive Approach to the Problem of Program Correctness (1967)

Root principle:

Do not only ask how to prove a finished program correct.

Derive the program from the required behavior and maintain correctness conditions during construction.

Operational consequence:

- write invariants early;
- choose representations that support them;
- treat implementation as refinement.

Reference:
https://www.cs.utexas.edu/~EWD/transcriptions/EWD02xx/EWD209.html

## Edsger W. Dijkstra — A Case against the GO TO Statement (1968)

Root principle:

The programmer must reason about the dynamic computation through the static program text.

Control structure is valuable when it provides a manageable coordinate system for execution.

Operational consequence:

- prefer control flow whose runtime progression is understandable from source structure;
- avoid control flow that makes state and execution history unnecessarily hard to reconstruct.

Reference:
https://www.cs.utexas.edu/~EWD/transcriptions/EWD02xx/EWD215.html

## Edsger W. Dijkstra — Stepwise Program Construction (1968)

Root principle:

Build programs through successive levels of elaboration, separating what an operation does from how it is implemented.

Operational consequence:

- refine one unresolved decision at a time;
- preserve stable contracts while changing implementation;
- keep alternative lower-level realizations possible.

Reference:
https://www.cs.utexas.edu/~EWD/transcriptions/EWD02xx/EWD227.html

## Edsger W. Dijkstra — Notes on Structured Programming (1969–1970)

Root principles:

- programs exist to evoke computations;
- structure is a mental aid;
- abstractions reduce appeals to enumeration;
- programs should be understood as families of alternatives;
- structure should anticipate modification;
- storage and computation are exchangeable resources under maintained invariants.

Operational consequence:

- reason about executions;
- preserve adaptation paths;
- model caches and derived state as explicit invariants;
- choose between equivalent implementations by resource trade.

Reference:
https://www.cs.utexas.edu/~EWD/transcriptions/EWD02xx/EWD249/EWD249.html

## Robert W. Floyd — Assigning Meanings to Programs (1967)

Root principle:

Program points can be associated with propositions that describe truths about program state, giving a rigorous basis for correctness reasoning.

Operational consequence:

- use assertions and invariants to bridge implementation steps;
- make state meaning explicit at boundaries.

## C. A. R. Hoare — An Axiomatic Basis for Computer Programming (1969)

Root principle:

Programming constructs can be reasoned about using explicit preconditions and postconditions.

Operational consequence:

- define what callers may assume;
- define what operations guarantee;
- make optimization preserve those contracts.

Reference:
https://doi.org/10.1145/363235.363259

## David Parnas — On the Criteria To Be Used in Decomposing Systems into Modules (1972)

Root principle:

Modules should be organized around design decisions that should be hidden from other modules, not merely around arbitrary processing steps.

Operational consequence:

- choose boundaries that localize likely change;
- hide implementation choices while preserving necessary cost transparency;
- do not let modularity accidentally force inefficient interaction patterns.

Reference:
https://doi.org/10.1145/361598.361623

## Donald Knuth — An Empirical Study of FORTRAN Programs (1971)

Root principle:

Execution profiles are valuable empirical evidence; programmer intuition about dynamic frequency and cost is not enough.

Operational consequence:

- make profiling normal;
- measure representative executions;
- do not guess hot regions from source appearance.

Reference:
https://doi.org/10.1002/spe.4380010203

## Donald Knuth — Structured Programming with go to Statements (1974)

Root principle:

Small efficiency improvements in non-critical code can damage clarity and maintenance, but meaningful opportunities in genuinely critical code should not be ignored.

The critical code must be identified rather than guessed.

Operational consequence:

- do not use "premature optimization" to dismiss performance work;
- distinguish architectural cost reasoning from source-level hotspot guessing;
- measure before adding local optimization complexity;
- optimize high-contribution regions deliberately.

Reference:
https://doi.org/10.1145/356635.356640

## Gene Amdahl — Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities (1967)

Root principle:

Total speedup is limited by the fraction of work that remains unimproved or serial.

Operational consequence:

- calculate contribution before tuning;
- attack large fractions and serial critical paths;
- do not confuse local speedup with system speedup.

Reference:
https://doi.org/10.1145/1465482.1465560

## Frederick P. Brooks Jr. — No Silver Bullet (1986)

Root principle:

Distinguish complexity intrinsic to the problem from complexity introduced by tools, representations, and implementation choices.

Operational consequence:

- identify necessary work;
- eliminate accidental work before optimizing its execution.

Reference:
https://www.cs.unc.edu/techreports/86-020.pdf


## Simon Eskildsen / sirupsen — Napkin Math

Root principle:

Estimate system performance from first principles using rounded, memorable base rates and Fermi-style decomposition.

The objective is often to identify the correct order of magnitude, not to manufacture false precision.

Operational consequence:

- carry units through every estimate;
- decompose unknown quantities into measurable factors;
- compare expected performance with actual performance;
- use the gap to discover inefficiency or missing understanding;
- maintain practical base rates for hardware, network, storage, and application behavior;
- go wide with approximate models before going deep on one implementation.

Reference:
https://github.com/sirupsen/napkin-math

Talk:
https://www.youtube.com/watch?v=IxkSlnrRFqc

## Enrico Fermi — Order-of-Magnitude Estimation Tradition

Root principle:

Complex questions can often be decomposed into a product of simpler estimates whose errors partly cancel or whose combined result is accurate enough to establish scale.

Operational consequence:

- seek the exponent before the decimal places;
- break unfamiliar quantities into familiar ones;
- use ranges for uncertain inputs;
- stop refining when additional precision cannot change the decision.

## John D. C. Little — A Proof for the Queuing Formula: L = lambda W (1961)

Root principle:

For a stable system, the average number of items present equals average throughput times average time in the system.

Operational consequence:

- convert latency and throughput into required concurrency;
- sanity-check connection pools, queues, and in-flight work;
- recognize that higher latency at the same throughput necessarily requires more concurrent state.

Reference:
https://doi.org/10.1287/opre.9.3.383

## Bandwidth-Delay Product — TCP Performance

Root principle:

A high-bandwidth path with non-trivial round-trip delay requires enough data in flight to fill the pipe.

Operational consequence:

- estimate `BDP = bandwidth × RTT`;
- distinguish latency from bulk throughput;
- use batching, pipelining, windows, or concurrency when fixed round trips prevent bandwidth utilization;
- do not infer low latency from high link bandwidth.

Reference:
https://www.rfc-editor.org/rfc/rfc6349

## Samuel Williams et al. — Roofline Performance Model

Root principle:

Attainable compute performance is bounded jointly by machine compute capability and data-movement bandwidth.

The deciding workload property is arithmetic intensity: useful computation performed per byte moved.

Operational consequence:

- estimate bytes moved as carefully as operation count;
- determine whether a kernel is likely bandwidth-bound or compute-bound;
- optimize locality and reuse before arithmetic when data movement is the ceiling;
- validate the bound empirically.

Reference:
https://docs.nersc.gov/tools/performance/roofline/

## Casey Muratori — The Root of the Root of All Evil (2026)

Root principle:

Famous programming slogans are lossy abstractions of historical arguments.

Their useful meaning comes from reconstructing the context, examples, goals, and evidence around them.

Operational consequence:

- reject slogan-driven review;
- recover the underlying engineering claim;
- preserve nuance between correctness, structure, measurement, and efficiency.

Reference:
https://www.computerenhance.com/p/theroot

