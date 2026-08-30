---
name: swe-dev-performance-aware-engineering
description: Designs, implements, reviews, and optimizes software with performance awareness. Use for performance-sensitive code, latency or throughput problems, inefficient architecture, excessive CPU/memory/I/O, scaling concerns, benchmarking, profiling, or when a design should remain efficiently optimizable as it grows.
argument-hint: Describe the code, system, workload, performance problem, proposed architecture, benchmark, or optimization you want implemented or reviewed.
---

# Performance-Aware Engineering

## Purpose

Produce software that sits at the intersection of:

- correctness;
- simplicity;
- comprehensibility;
- maintainability;
- appropriate performance;
- observability;
- adaptability;
- future optimizability.

The objective is not maximum benchmark scores.

The objective is to make the machine perform the necessary work with as little unnecessary work, movement, waiting, coordination, and complexity as practical, while keeping the computation understandable enough that humans can continue to reason about it.

Performance is a design property before it becomes an optimization problem.

Optimization is a controlled transformation of a known computation, not a substitute for understanding the computation.

---

# Core Thesis

Do not begin with:

> What line should I optimize?

Begin with:

> What effect must the system produce?

Then ask:

> What computation is actually necessary to produce that effect?

Then:

> What resources should that computation plausibly require?

Then:

> What architecture preserves a direct path from the required effect to that computation?

Only after an implementation exists should you ask:

> Where does this representative workload actually spend its resources?

Finally:

> What explains the gap between required work, plausible machine capability, and observed behavior?

A profiler can attribute observed cost.

It cannot tell you whether the architecture should have required that work in the first place.

A theoretical model can expose impossible or wasteful architecture.

It cannot reliably tell you which source lines dominate a real workload.

Use both.

---

# Foundational Model

## The program is not the computation

Source code is a static description.

The actual subject is the dynamic computation it evokes:

- which operations execute;
- in what order;
- how often;
- on what data;
- with what dependencies;
- with what resource costs;
- while maintaining what truths.

Whenever you claim that code is:

- correct;
- fast;
- memory-efficient;
- scalable;
- concurrent;
- deterministic;

you are making a claim about possible executions, not merely about the appearance of the source text.

Therefore:

- review dynamic behavior, not syntax alone;
- keep control flow mappable to execution;
- keep expensive work visible;
- keep invariants explicit;
- keep state transitions understandable;
- do not confuse elegant source structure with efficient computation.

## Structure is a reasoning aid

Structure is valuable when it reduces the amount of state a human must hold in mind.

Good structure lets a maintainer reason locally about:

- what enters;
- what leaves;
- what remains invariant;
- what can happen next;
- what work is performed;
- what resources are consumed.

Abstraction is successful when it compresses reasoning without destroying information needed to make engineering decisions.

Abstraction that hides essential cost, state, failure, or ordering is not simplification. It is displaced complexity.

## Correctness should be constructed

Do not treat correctness as something added after implementation through debugging.

For non-trivial behavior:

1. state what must be true;
2. choose representations that make those truths expressible;
3. derive operations that preserve them;
4. refine one decision at a time;
5. verify each refinement.

Testing remains essential, but testing is strongest when it checks a design whose correctness conditions are already understood.

## Optimization selects among equivalent computations

A performance change should be understood as choosing another member of a family of implementations that preserve the required external effect while changing resource usage.

Typical exchanges include:

- computation for storage;
- storage for computation;
- latency for throughput;
- memory for locality;
- preprocessing for query speed;
- precision for speed, only when permitted;
- duplicated state for fewer round trips;
- batching for higher latency per item but lower total overhead;
- specialized code for lower generality.

The engineering task is not merely to make something faster.

It is to preserve the contract while deliberately changing the resource trade.

---

# Slogan Firewall

Do not use slogans as engineering arguments.

The following phrases are prompts for analysis, not conclusions:

- "premature optimization is the root of all evil";
- "goto considered harmful";
- "clean code";
- "DRY";
- "YAGNI";
- "OOP is bad";
- "abstractions are free";
- "the compiler will optimize it";
- "hardware is fast enough";
- "we can optimize it later".

When one appears, translate it into a falsifiable claim.

Instead of:

> This is premature optimization.

Ask:

- What concrete cost is being avoided?
- Is the decision architectural or a local micro-optimization?
- Will delaying it close an important optimization path?
- Is the workload known?
- Is the change reversible?
- Is there evidence this region is critical?
- What maintenance cost does the optimization introduce?

Instead of:

> This abstraction is cleaner.

Ask:

- What reasoning does it simplify?
- What design decision does it hide?
- Does it hide I/O, allocation, copying, synchronization, or remote calls?
- Can callers still predict important costs?
- Does it preserve the ability to batch, specialize, or change layout?

Never let a famous sentence terminate an investigation.

---

# Two Kinds of Performance Reasoning

## 1. Architectural cost reasoning before measurement

Before code exists, you can and should reason about things such as:

- asymptotic complexity;
- number of network round trips;
- number of database queries;
- bytes that must move;
- serialization boundaries;
- dependency depth;
- synchronization points;
- required copies;
- expected allocation volume;
- unavoidable storage access;
- maximum useful parallelism;
- expected working-set size;
- likely cache behavior at a coarse level.

This is not hotspot guessing.

It is reasoning about the shape and lower bounds of the computation.

Use it to reject architectures that are slow by construction.

## 2. Empirical attribution after implementation

Once executable code exists, do not guess which functions or lines dominate.

Measure under representative workloads.

Use:

- profiles;
- traces;
- counters;
- benchmark results;
- query plans;
- allocator statistics;
- hardware counters when appropriate.

A priori reasoning tells you what should matter.

Measurement tells you what does matter in this implementation on this workload.

When they disagree, investigate the disagreement.

That gap often contains the most useful information.

---

# Non-Negotiable Rules

## 1. Correctness bounds optimization

Preserve required:

- behavior;
- invariants;
- precision;
- ordering;
- consistency;
- security;
- compatibility;
- failure semantics;
- concurrency semantics;
- resource ownership.

A faster wrong answer is a regression.

## 2. Never make unmeasured performance claims

Separate:

- measured facts;
- calculated bounds;
- estimates;
- hypotheses;
- expectations.

If no benchmark was run, say so.

If the workload is synthetic, say so.

If the result is noisy, say so.

If the improvement is workload-specific, say so.

## 3. Optimize the computation, not the profiler screenshot

A hotspot may be:

- necessary work;
- duplicated work;
- the visible symptom of a bad API;
- the endpoint of an N+1 pattern;
- the serialization point in a dependency chain;
- the place where poor data layout finally becomes expensive;
- a library call made too often;
- a consequence of upstream allocation or copying.

Trace cost to its cause before editing the hottest line.

## 4. Preserve optimization paths

Code does not need to be maximally optimized today.

It should avoid needless commitments that make meaningful optimization tomorrow require a rewrite.

Be wary of early decisions that hard-code:

- serialized execution;
- chatty APIs;
- per-item remote calls;
- opaque ownership;
- scattered state;
- pointer-heavy layouts;
- irreversible data representations;
- hidden allocation;
- mandatory copying;
- cross-layer callbacks;
- abstraction boundaries that prevent batching.

## 5. Prefer simple transformations over clever tricks

A strong optimization often removes something:

- work;
- data movement;
- allocation;
- branches;
- queries;
- round trips;
- synchronization;
- layers;
- conversions;
- repeated derivations.

Prefer deleting a cost over making the cost execute more cleverly.

## 6. Keep cost observable

Performance-sensitive systems should make important costs easy to inspect.

Where practical, preserve:

- benchmark targets;
- profiler-friendly symbols;
- metrics;
- traces;
- query counts;
- allocation counts;
- cache hit/miss information;
- request fan-out;
- queue time;
- dependency timing.

Observability is part of performance architecture.

---

# Performance Model

For significant work, build a model across the dimensions below.

## Required effect

State what the user or caller actually needs.

Separate the externally required effect from incidental implementation work.

Ask:

- What output must exist?
- What state must change?
- What guarantees must hold?
- What information is truly required to compute the result?

This helps distinguish necessary work from accidental work.

## Work

Count meaningful units:

- iterations;
- comparisons;
- hashes;
- parses;
- encodes/decodes;
- allocations;
- syscalls;
- queries;
- RPCs;
- rows scanned;
- objects visited;
- pixels processed;
- tasks scheduled;
- lock acquisitions.

Prefer counts before percentages.

"12 requests" is more actionable than "network seems slow."

## Algorithmic growth

For input size `n`, identify:

- time complexity;
- space complexity;
- expected-case behavior;
- worst realistic case;
- skew sensitivity.

Do not stop at Big-O.

Constants, memory access, vectorization, and I/O often dominate at practical sizes.

But do not micro-optimize constants while ignoring a poor growth rate.

## Data movement

Estimate:

- bytes read;
- bytes written;
- bytes copied;
- bytes serialized;
- bytes transferred over the network;
- bytes moved through caches;
- rows or pages fetched from storage.

Ask:

> Is the system doing more work, or merely moving more data than necessary?

On modern machines, moving data is frequently more expensive than arithmetic on data already present.

## Dependency depth

Represent important work as a dependency graph.

Find the longest required serial chain.

For every edge:

> Must B actually wait for A?

Look for:

- false dependencies;
- request waterfalls;
- sequential awaits;
- lock chains;
- producer/consumer stalls;
- repeated barriers.

Latency is constrained by serial dependency depth even when abundant parallel resources exist.

## Parallel fraction

When parallelizing, distinguish:

- work that can run concurrently;
- work that must remain serial;
- overhead introduced by coordination.

Use Amdahl-style reasoning:

If fraction `p` can be improved by factor `s`, ideal total speedup is bounded by:

`1 / ((1 - p) + p / s)`

Consequences:

- optimizing a tiny fraction cannot create a huge total speedup;
- infinite speedup of the parallel part still leaves the serial fraction;
- coordination overhead makes reality worse than the ideal bound.

Use the equation as a sanity check, not a prediction oracle.

## Latency versus throughput

Do not conflate them.

A change may:

- increase throughput but worsen per-request latency;
- reduce median latency while worsening tail latency;
- improve single-thread speed but reduce total system throughput;
- increase utilization while reducing headroom.

State which metric matters.

## Queueing and saturation

At high utilization, small increases in service time can produce large increases in waiting time.

Inspect:

- CPU saturation;
- connection pool saturation;
- thread pool saturation;
- disk queue depth;
- event-loop stalls;
- rate limits;
- downstream capacity.

A system can be slow because it is waiting, not because its code is computationally expensive.

## Memory

Consider:

- total footprint;
- working set;
- allocation rate;
- object lifetime;
- fragmentation;
- garbage collection;
- locality;
- indirection;
- cache lines touched;
- temporary buffers;
- duplication.

Do not treat memory use as a single scalar.

An extra 100 MB of contiguous read-mostly data and an extra 100 MB of tiny short-lived allocations can have very different effects.

## I/O

Count:

- syscalls;
- reads/writes;
- random versus sequential access;
- request sizes;
- fsyncs;
- network handshakes;
- query round trips;
- serialization boundaries.

Batching often beats local computation tuning because fixed I/O overheads are large.

---

# Correctness-by-Construction

Performance work becomes safer when the code has explicit correctness structure.

## Start from invariants

For stateful logic, write down relations that must remain true.

Examples:

- `used <= capacity`
- `cached_value == f(source_state)` when cache is valid
- every request ID is unique among in-flight operations
- queue indices preserve FIFO order
- aggregate count equals sum of member counts
- sorted region remains sorted after insertion
- reference count equals number of owning references

Then design operations around preserving these relations.

## Prefer representations that make invalid states difficult

A representation is not neutral.

It determines:

- what is cheap;
- what is expensive;
- what is easy to prove;
- what can become inconsistent.

Choose state that makes the important operations and invariants direct.

Avoid state duplicated without a maintenance rule.

When duplicating state for performance, define the synchronization invariant explicitly.

## Refine one decision at a time

For non-trivial algorithms:

1. describe the desired effect at a high level;
2. choose one unresolved operation;
3. refine only that operation;
4. state what new invariant or representation it introduces;
5. preserve all earlier contracts;
6. repeat until executable.

This prevents accidental coupling between unrelated decisions.

It also keeps alternatives open longer.

## Separate what from how at each level

At each refinement boundary, be able to say:

- what this operation guarantees;
- how the current implementation achieves it.

If the two cannot be separated, the abstraction may be poorly chosen.

This is especially important in performance-sensitive code because the "how" may later change while the "what" must remain stable.

---

# Program Families and Future Change

Do not regard the current implementation as the only possible program.

For important components, mentally maintain a family of equivalent alternatives.

Examples:

- recompute vs cache;
- array-of-structures vs structure-of-arrays;
- per-item call vs batch call;
- eager vs lazy;
- synchronous vs pipelined;
- generic vs specialized;
- interpreted vs compiled;
- normalized vs denormalized storage;
- single-pass vs multi-pass;
- local compute vs remote compute.

Ask:

- Which decisions are stable?
- Which are likely to change?
- Can the current structure accommodate another family member without replacing everything?

Good structure supports both correctness and adaptation.

## Optimization as family selection

When performance becomes inadequate:

1. identify the resource that is unsatisfactory;
2. identify equivalent program variants;
3. choose a variant that changes the relevant resource trade;
4. preserve the external contract;
5. verify equivalence;
6. measure the new resource profile.

This is more disciplined than opportunistic tweaking.

---

# Space-Time Tradeoffs

Trading storage for computation is one of the oldest and most general performance transformations.

## Cached derived state

Suppose the system repeatedly needs:

`derived = F(source)`

Two basic implementations exist.

### Recompute

Store only `source`.

Compute `F(source)` on demand.

Benefits:

- minimal duplicated state;
- simple consistency;
- lower memory use.

Costs:

- repeated computation.

### Maintain derived state

Store both `source` and `derived`.

Maintain the invariant:

`derived == F(source)`

Benefits:

- cheap reads.

Costs:

- more memory;
- more expensive writes;
- more correctness burden.

### Lazy cache

Store:

- `source`;
- `derived`;
- validity/version metadata.

Invalidate on source mutation and recompute on demand.

This is a refinement of the same invariant.

The principle appears everywhere:

- memoization;
- materialized views;
- database indexes;
- denormalized fields;
- precomputed lookup tables;
- cached serialization;
- incremental builds;
- dependency graphs.

Do not say "add a cache" without stating:

- the maintained invariant;
- invalidation rule;
- ownership;
- memory bound;
- concurrency behavior;
- expected read/write ratio.

---

# Critical Regions Without Mythology

Do not assume a universal "80/20", "90/10", or "3%/97%" distribution.

Runtime concentration is empirical and workload-dependent.

A program may have:

- one dominant inner loop;
- many medium-cost regions;
- distributed I/O waits;
- a critical serial chain;
- load-dependent bottlenecks;
- hot paths that differ by user or input.

Therefore:

- measure the actual distribution;
- rank cost by contribution;
- report cumulative cost;
- verify across representative scenarios.

The number "3%" is not a law of nature.

The deeper principle is:

> Spend optimization complexity where it buys meaningful system-level improvement.

## Use Amdahl's law before local tuning

If a region consumes fraction `p` of total time and you make it `s` times faster, the maximum overall speedup is:

`1 / ((1 - p) + p / s)`

Example:

If a region is 10% of runtime and you make it infinitely fast, the whole program can improve by at most about 11%.

This prevents impressive local benchmark results from being mistaken for meaningful end-to-end improvement.

## Hotness is workload-relative

Always ask:

> Hot for which workload?

Use:

- production-like input sizes;
- realistic distributions;
- realistic concurrency;
- realistic cache state;
- realistic dependency latency.

A microbenchmark proves a local mechanism.

It does not automatically prove end-to-end importance.

---


# Napkin Math and First-Principles Capacity Estimation

Use napkin math before expensive implementation work and before interpreting benchmark results.

The goal is not precision.

The goal is to answer questions such as:

- Is this design physically plausible?
- Which resource should dominate?
- Which term is too large to ignore?
- Are two designs in the same performance class or separated by an order of magnitude?
- How much concurrency is required?
- How much memory, storage, bandwidth, or CPU should this workload consume?
- Is the measured result close to a plausible machine bound or surprisingly far away?

A useful estimate often needs only the correct exponent.

If the design target is 10 ms and the first-principles estimate is 10 seconds, do not spend a week refining the benchmark.

If two candidates estimate to 8 ms and 11 ms, the estimate is not decisive. Measure.

---

## The Estimation Standard

For important performance decisions, create a small model with:

Required effect:
Workload:
Input size:
Request/event rate:
Fixed latency terms:
Per-byte/per-item work:
Data movement:
Concurrency:
Resource ceilings:
Low estimate:
Expected estimate:
High estimate:
Target:
Dominant term:
Largest uncertainty:
Decision:

Prefer a useful rough calculation now over a precise calculation after the architecture is locked in.

---

## Order-of-Magnitude First

Start with powers of ten and one significant digit.

Examples:

- 87,000 requests/s -> `~1e5 requests/s`
- 1.7 KiB/event -> `~2 KiB/event`
- 43 ms -> `~4e-2 s`
- 850 MiB/s -> `~1 GiB/s`

Do not preserve fake precision in uncertain inputs.

The purpose of rounding is to make mental composition easy.

Refine only when the decision depends on the refinement.

### Precision ladder

Use this sequence:

1. exponent;
2. one significant digit;
3. conservative range;
4. measured calibration;
5. high-precision benchmark only when necessary.

If the decision is unchanged at step 2, stop.

---

## Fermi Decomposition

When a quantity is unknown, decompose it into quantities that are easier to estimate.

Example:

`daily_log_bytes`

can become:

`requests/day × log_events/request × bytes/log_event`

and:

`requests/day = requests/second × seconds/day`

Therefore:

`daily_log_bytes = RPS × 86,400 s/day × events/request × bytes/event`

A difficult question becomes multiplication of understandable terms.

### Decomposition rules

Prefer factors that are:

- measurable independently;
- familiar;
- stable enough to estimate;
- attached to explicit units.

If one factor is uncertain, bound it.

For example:

`payload = 1–4 KiB`

Do not hide uncertainty by choosing an unjustified exact number.

---

## Dimensional Analysis

Carry units through calculations.

Units are a lightweight type system for estimates.

Example:

`100,000 requests/s × 2 KiB/request`

gives:

`200,000 KiB/s`

which is approximately:

`200 MiB/s`

If the units do not cancel to the quantity you are trying to estimate, the equation is wrong.

### Required discipline

Write:

`RPS × bytes/request = bytes/s`

not:

`100000 × 2048 = 204800000`

The first form exposes the model.

The second exposes only arithmetic.

### Common unit errors

Watch for:

- bits vs bytes;
- MB vs MiB;
- seconds vs milliseconds;
- requests vs operations;
- logical bytes vs replicated physical bytes;
- compressed vs uncompressed bytes;
- payload bytes vs protocol bytes;
- CPU time vs wall time;
- per-core vs whole-machine throughput.

---

## Base Rates

Build intuition around a small set of memorable rates.

Base rates should be:

- rounded;
- easy to compose mentally;
- periodically revalidated;
- treated as scale references, not immutable constants.

A project with meaningful performance requirements should maintain environment-specific rates for:

- sequential memory bandwidth;
- random memory latency;
- hashing;
- serialization/deserialization;
- compression/decompression;
- syscall cost;
- sequential storage throughput;
- random storage latency;
- local network RTT/throughput;
- same-zone and same-region network RTT/throughput;
- cross-region RTT/throughput;
- database/cache round trips;
- blob/object storage latency and throughput;
- application-specific RPCs and queries.

### Contemporary scale reference

As of the 2026 measurements in `sirupsen/napkin-math`, useful rounded scales include approximately:

- sequential memory, single thread: `~20 GiB/s`;
- sequential memory, threaded: `~200 GiB/s`;
- random 64-byte memory access: `~20 ns`;
- non-cryptographic hashing: `~5 GiB/s`;
- fast serialization: `~1 GiB/s`;
- ordinary serialization: `~100 MiB/s`;
- syscall: `~300 ns`;
- sequential SSD read: `~8 GiB/s`;
- random 8 KiB SSD read: `~100 us`;
- compression: `~500 MiB/s`;
- decompression: `~1 GiB/s`;
- same-region network: order `~250 us` RTT and `~2 GiB/s`;
- simple database/cache query: order `~500 us`;
- single-stream blob GET: order `~80 ms` setup/latency and `~100 MiB/s`;
- inter-region network: tens to hundreds of milliseconds of RTT.

These are memorization-scale estimates.

They vary by:

- hardware;
- provider;
- topology;
- runtime;
- kernel;
- protocol;
- payload;
- concurrency;
- implementation.

When a decision is close, benchmark the actual environment.

When a decision differs by 10–100x, the approximate scale is often enough to eliminate a design.

---

## Maintain a Project Base-Rate Sheet

For performance-sensitive repositories, consider maintaining a small file such as:

`docs/performance/base-rates.md`

Record:

Operation:
Measured latency:
Measured throughput:
Machine/environment:
Date:
Benchmark command:
Representative payload:
Notes:

Include application-specific facts such as:

- normal RPS;
- peak RPS;
- typical request size;
- p50/p95 object size;
- average queries/request;
- average RPCs/request;
- average rows scanned;
- cache hit rate;
- log bytes/request;
- working-set size.

The most useful senior-engineer intuition is often a compact internal model of the application's base rates.

Make that model explicit and reproducible.

---

# Core Capacity Equations

Memorize the forms below.

Do not memorize answers.

## Data rate

`bandwidth = event_rate × bytes/event`

Examples:

`requests/s × bytes/request = bytes/s`

`messages/s × bytes/message = bytes/s`

If an operation causes amplification:

`physical_bandwidth = logical_bandwidth × amplification_factor`

Amplification may come from:

- replication;
- indexes;
- protocol overhead;
- retries;
- fan-out;
- multiple copies;
- read-modify-write behavior.

---

## Storage accumulation

`storage = event_rate × bytes/event × duration`

For daily accumulation:

`bytes/day = events/s × bytes/event × 86,400`

For retention:

`retained_bytes = bytes/day × retention_days`

For replicated storage:

`physical_bytes = retained_bytes × replication_factor`

Add index or metadata amplification separately.

---

## CPU capacity

If average CPU time per request is known:

`cores_at_100_percent = requests/s × CPU_seconds/request`

Provisioned cores should include headroom:

`cores_required = cores_at_100_percent / target_utilization`

Example:

`20,000 requests/s × 200 us CPU/request`

`= 4 CPU-seconds/second`

`= ~4 fully utilized cores`

At a 60% target utilization:

`4 / 0.6 ~= 7 cores`

This is a capacity estimate, not a latency prediction.

---

## Memory capacity

For resident per-item state:

`memory = item_count × bytes/item`

Include:

- allocator overhead;
- object headers;
- indexes;
- pointers;
- fragmentation;
- duplicate representations;
- caches;
- replication.

If the estimate is sensitive to overhead, measure actual resident size.

---

## Fan-out

If every incoming request causes `f` downstream operations:

`downstream_ops/s = incoming_RPS × f`

If downstream payload is `b` bytes/op:

`downstream_bandwidth = incoming_RPS × f × b`

Retries multiply this further.

A local-looking code change can create system-wide load amplification.

---

## Little's Law

For a stable system:

`in_flight = throughput × latency`

Conventionally:

`L = λW`

where:

- `L` is average items in the system;
- `λ` is average arrival/throughput rate;
- `W` is average time in the system.

Software interpretation:

`concurrency ~= requests/s × seconds/request`

Example:

`10,000 requests/s × 100 ms`

`= 10,000 × 0.1`

`= ~1,000 requests in flight`

This gives immediate estimates for:

- connection requirements;
- task counts;
- queue occupancy;
- buffer requirements;
- concurrent RPCs.

### Inverse forms

`throughput ~= concurrency / latency`

`latency ~= in_flight / throughput`

These forms are extremely useful for sanity checks.

If one connection performs a request every 100 ms, one connection can complete only about 10 requests/s without pipelining.

To sustain 10,000 requests/s at that latency requires about 1,000 operations in flight somewhere.

---

## Fixed latency plus bandwidth

A useful transfer model is:

`time ~= fixed_latency + bytes / throughput`

For a request requiring `r` serialized round trips:

`time ~= r × RTT + bytes / bandwidth + compute`

This separates:

- startup/coordination cost;
- bulk transfer cost;
- local computation.

### Crossover size

The size where latency and transfer time are equal is:

`crossover_bytes = latency × bandwidth`

This is the same dimensional idea as a bandwidth-delay product.

Below the crossover size, fixed latency tends to dominate.

Above it, throughput tends to dominate.

---

## Bandwidth-delay product

For a path:

`BDP = bandwidth × RTT`

This is approximately the amount of data that must be in flight to fill the path.

If:

`bandwidth = 1 GiB/s`

and:

`RTT = 100 ms = 0.1 s`

then:

`BDP ~= 100 MiB`

A single serialized small request cannot saturate that path.

High-throughput transfers may require:

- large windows;
- pipelining;
- concurrent ranges;
- multiple requests;
- batching.

This explains why high bandwidth does not imply low latency and why concurrency can unlock throughput.

---

## Serial stages

For strictly serial stages:

`latency_total = latency_1 + latency_2 + ... + latency_n`

The critical path is additive.

Removing a stage can be more valuable than making every stage slightly faster.

---

## Parallel stages

For independent work launched together:

`latency_parallel ~= max(stage_latencies) + coordination_overhead`

not:

`sum(stage_latencies)`

Use this only when work is truly independent.

Parallel syntax does not remove real dependencies.

---

## Pipeline throughput

For an ideal steady-state pipeline:

`throughput <= min(stage_throughputs)`

The slowest stage limits steady-state flow.

Pipeline latency may still be approximately the sum of stage latencies.

Do not confuse high pipeline throughput with low per-item latency.

---

## Batching

Suppose `n` operations each pay fixed latency `L` and transfer time `S/B`.

Individually:

`T_individual ~= n × L + n × S/B`

As one batch:

`T_batch ~= L + n × S/B`

Potential fixed-cost saving:

`~(n - 1) × L`

Batching is powerful when fixed overhead dominates.

But batching can increase:

- queueing delay;
- memory use;
- tail latency;
- failure blast radius.

Model both sides.

---

## Compression break-even

For uncompressed size `S`, I/O bandwidth `B`, compression throughput `C_comp`, decompression throughput `C_decomp`, and compression ratio `r` where `r > 1`:

Without compression:

`T_plain ~= S / B`

With compression:

`T_compressed ~= S / C_comp + (S / r) / B + S / C_decomp`

Compression helps latency/throughput only when the reduced I/O cost exceeds compression/decompression cost.

On a slow network, compression may be an obvious win.

On very fast memory or local storage, compression may lose unless it also improves cache or working-set behavior.

Measure representative data because compression ratio is workload-dependent.

---

## Cache break-even

A cache is useful when expected saved work exceeds lookup, fill, invalidation, memory, and consistency cost.

A rough expected-time model:

`T_cached ~= hit_rate × T_hit + miss_rate × T_miss`

where:

`T_miss` includes cache lookup plus underlying work and fill.

Compare against:

`T_uncached`

Also model:

- memory footprint;
- invalidation;
- write amplification;
- stampedes;
- cold-start behavior.

Never evaluate a cache by hit rate alone.

---

## Index break-even

An index trades:

- storage;
- write cost;
- maintenance complexity;

for:

- lower read work;
- fewer bytes scanned;
- better lookup latency.

Approximate:

`read_savings_per_second = reads/s × work_saved/read`

`write_cost_per_second = writes/s × extra_work/write`

The index is operationally compelling when read savings dominate relevant costs and the memory/storage footprint is acceptable.

Still inspect actual query plans.

---

## Cost estimation

Translate resource rates into money only after translating the workload into resources.

Examples:

`storage_cost = physical_GB_month × price/GB_month`

`egress_cost = GB_egress × price/GB`

`compute_cost ~= instance_hours × price/hour`

For rough comparisons, the relative resource model is often more stable than provider pricing.

Pricing changes.

Bytes, CPU-seconds, and request counts are the deeper quantities.

---

# Bound the Estimate

Never rely on one fragile point estimate for important design decisions.

Use:

Low:
Expected:
High:

or:

Optimistic:
Nominal:
Conservative:

Choose ranges for uncertain factors.

Example:

Payload:
`1–4 KiB`

Peak RPS:
`50k–100k`

Compression:
`2–4x`

Then calculate plausible extremes.

## Do not stack optimism

A design that works only if:

- traffic is low;
- payload is small;
- compression is excellent;
- cache hit rate is high;
- network is unusually fast;

is not robust.

Evaluate at least one conservative combination.

---

# Dominant-Term Reasoning

After composing an estimate, compare the terms.

If one term is 10x larger than all others, it usually deserves attention first.

Example:

Memory copy:
`5 ms`

SSD write:
`20 ms`

Cross-region network:
`600 s`

The memory-copy estimate does not need refinement.

The network term decides feasibility.

This is one of the main powers of napkin math:

It tells you what not to spend time measuring yet.

---

# Sensitivity Analysis

Ask which assumptions can change the decision.

For each uncertain parameter:

- vary it by 2x;
- vary it by 10x when plausible;
- recompute.

If changing a parameter barely changes the answer, stop debating it.

If changing one assumption flips the decision, measure that assumption first.

### Sensitivity heuristic

Prioritize uncertainty that is both:

- large;
- decision-sensitive.

Ignore uncertainty that cannot alter the conclusion.

---

# Feasibility Bands

Use rough bands to choose the next action.

## More than 10x inside target

Example:

Target:
`1 s`

Estimate:
`50 ms`

Action:

- architecture is plausibly safe;
- retain headroom;
- benchmark representative implementation later.

## Within roughly 2–5x

Example:

Target:
`100 ms`

Estimate:
`60 ms`

Action:

- estimate is not decisive;
- prototype or benchmark early;
- inspect variance and tail behavior.

## More than 10x outside target

Example:

Target:
`100 ms`

Estimate:
`5 s`

Action:

- reject or redesign;
- do not rely on micro-optimization;
- identify which term must structurally change.

These are heuristics, not mathematical laws.

---

# Go Wide Before Going Deep

When several architectures are plausible:

1. sketch each candidate;
2. estimate major resource terms;
3. calculate order-of-magnitude latency/capacity/cost;
4. eliminate clearly dominated designs;
5. prototype the survivors;
6. benchmark only where the decision remains uncertain.

This reduces attachment to the first implementation.

It also helps reveal designs outside the current abstraction layer.

Order-of-magnitude improvements often require changing:

- data representation;
- service boundary;
- storage model;
- batching strategy;
- ownership;
- precomputation;
- replication;
- protocol;
- layer of computation.

Do not assume the best solution lives inside the current abstraction.

---

# Napkin Math as an Architectural Test

Before accepting a design, answer:

## CPU

- CPU-seconds/request?
- Expected RPS?
- Cores at 100%?
- Cores at target utilization?
- Is the work parallelizable?
- Is compute actually likely to dominate?

## Memory

- Items?
- Bytes/item?
- Working set?
- Replication?
- Temporary buffers?
- Allocation rate?
- Is the design bandwidth-bound or capacity-bound?

## Storage

- Bytes written/s?
- Bytes read/s?
- Random or sequential?
- fsync required?
- Write amplification?
- Retention?
- Replication?

## Network

- Calls/request?
- RTT per dependency?
- Serialized round trips?
- Bytes transferred?
- Same host/zone/region/continent?
- BDP?
- Required in-flight operations?

## Database

- Queries/request?
- Rows scanned/query?
- Index behavior?
- Result bytes?
- Connection concurrency?
- Lock/contention risk?

## Object storage

- Request count?
- First-byte latency?
- Object size?
- Single-stream throughput?
- Can ranges/multipart/concurrency be used?

## Cost

- CPU-hours?
- Stored bytes?
- Bytes transferred?
- Requests?
- Replication?
- Headroom?

If these cannot be estimated even roughly, the design is not yet understood well enough to make strong performance claims.

---

# Mechanical Sympathy Beyond Big-O

Big-O describes growth.

It does not tell you the time scale of an operation.

Two `O(n)` implementations can differ enormously when one performs:

- contiguous memory reads;

and the other performs:

- random SSD reads;
- remote RPCs;
- pointer chasing;
- synchronization.

Therefore analyze both:

`algorithmic_count × cost_per_operation`

For an operation family:

`total_cost ~= operation_count × base_rate`

Examples:

`random_reads × latency/read`

`bytes_scanned / sequential_bandwidth`

`RPC_count × RTT`

`objects × allocation_cost`

This connects algorithmic reasoning to actual hardware.

---

# Arithmetic Intensity and the Roofline Intuition

For compute-heavy kernels, distinguish compute-bound from bandwidth-bound behavior.

Define arithmetic intensity approximately as:

`useful_operations / bytes_moved`

A simplified machine bound is:

`attainable_compute_rate <= min(peak_compute_rate, memory_bandwidth × arithmetic_intensity)`

If arithmetic intensity is low, the kernel is likely constrained by data movement.

If arithmetic intensity is high, compute throughput may dominate.

Operational implications:

When bandwidth-bound, investigate:

- locality;
- reuse;
- layout;
- unnecessary loads/stores;
- copies;
- compression;
- fusion.

When compute-bound, investigate:

- vectorization;
- instruction efficiency;
- parallelism;
- algorithmic operation count.

Do not optimize arithmetic while waiting on memory.

Do not rearrange memory while execution units are the actual bound.

Use measurement to validate the classification.

---

# Concurrency Is a Resource Conversion

Concurrency converts waiting time into required in-flight state.

From Little's Law:

`concurrency ~= throughput × latency`

This means reducing latency can reduce required:

- connections;
- threads/tasks;
- buffers;
- queued work;
- memory.

Likewise, increasing throughput at fixed latency requires more concurrency.

Concurrency is not free.

It consumes:

- memory;
- sockets;
- descriptors;
- scheduler capacity;
- queue slots;
- downstream concurrency;
- database connections.

Model those costs before solving latency with more parallelism.

---

# Headroom and Saturation

Do not design nominal capacity at 100% sustained utilization.

Near saturation:

- queues grow;
- tail latency rises;
- retries amplify load;
- small disturbances become incidents.

Napkin models should therefore distinguish:

Theoretical maximum:
Expected sustained load:
Peak load:
Target operating utilization:

A machine that can theoretically perform 100k requests/s is not necessarily a healthy 100k requests/s production machine.

Provision headroom according to:

- burstiness;
- autoscaling delay;
- failure tolerance;
- latency SLO;
- workload variance;
- dependency variance.

---

# Estimate, Then Calibrate

Napkin math is strongest as a feedback loop.

1. estimate;
2. implement or benchmark;
3. compare measured vs expected;
4. explain the difference;
5. update your base rates;
6. improve future estimates.

A mismatch is valuable.

If the estimate says `100 us` and measurement says `10 ms`, ask why.

Possible explanations:

- hidden copies;
- extra round trips;
- debug build;
- allocator behavior;
- protocol overhead;
- contention;
- queueing;
- runtime/JIT;
- poor access pattern;
- environment mismatch.

Do not merely replace the estimate with the measurement.

Learn the missing mechanism.


# Operating Loop

Use this loop for performance-sensitive engineering.

## Phase 0 — Refuse slogans

Translate any broad principle into a concrete claim.

Record:

Problem:
Required effect:
Suspected cost:
Evidence:
Risk if ignored:
Risk if optimized:
Reversibility:

---

## Phase 1 — Define the contract

State:

Performance objective:
Relevant workload:
Expected scale:
Latency target:
Throughput target:
Memory/resource target:
Correctness invariants:
Compatibility constraints:
Failure semantics:
Success criterion:

Do not optimize an undefined workload.

---

## Phase 2 — Understand the desired computation

Before reading every implementation detail, describe the minimal semantic job.

Ask:

- What input information is truly required?
- What output/state change is required?
- What ordering is required?
- What work is mathematically or physically unavoidable?

Write a simple conceptual kernel.

Example:

`input -> filter -> transform -> aggregate -> output`

Then compare implementation structure to this kernel.

Large gaps indicate accidental work or unnecessary architecture.

---

## Phase 3 — Understand the current system

Inspect:

- implementation;
- call graph;
- data flow;
- control flow;
- ownership;
- service boundaries;
- storage access;
- network requests;
- synchronization;
- tests;
- existing benchmarks;
- production metrics;
- profiles/traces if available.

Do not edit before identifying where authoritative behavior lives.

---

## Phase 4 — State invariants

Write the important truths the current system must preserve.

For optimization work, include resource-related invariants when they matter.

Examples:

- no extra network requests after warmup;
- at most one allocation per batch;
- buffer never grows beyond N;
- output order remains stable;
- cache contents correspond to version V;
- no lock held across remote I/O.

These make optimizations reviewable.

---

## Phase 5 — Build a rough lower-bound model

Estimate the minimum plausible cost.

Depending on the system, consider:

- operation count;
- algorithmic lower bound;
- bytes that must move;
- memory bandwidth;
- CPU throughput;
- disk/storage latency;
- network RTT;
- database round trips;
- dependency depth;
- available parallelism.

Exact prediction is unnecessary.

Classify the current design as roughly:

- near plausible;
- moderately wasteful;
- orders of magnitude away.

If the architecture requires 100 sequential remote calls, no CPU profiler is needed to know where to start.

---

## Phase 6 — Inspect architecture before hotspots

Map the critical operation as a dependency/data-flow graph.

Identify:

- serial request chains;
- false dependencies;
- unnecessary service boundaries;
- repeated queries;
- N+1 behavior;
- repeated parsing;
- repeated serialization;
- repeated allocation;
- repeated derivation;
- global locks;
- unnecessary copies;
- hidden I/O;
- abstraction boundaries preventing batching.

Ask:

> Could a local optimization fix this, or is the system slow by construction?

Surface architectural performance debt before polishing local code.

---

## Phase 7 — Establish a baseline

Benchmark before changing behavior.

Record:

- exact workload/input;
- input size/distribution;
- environment;
- hardware;
- build mode;
- compiler/runtime version where relevant;
- benchmark command;
- warmup;
- sample count;
- median;
- tail percentiles when relevant;
- throughput;
- CPU time;
- wall time;
- memory/resource use;
- variance/noise.

Prefer realistic representative workloads.

Use microbenchmarks only to isolate a specific mechanism.

---

## Phase 8 — Attribute observed cost

Now profile.

Choose the tool that answers the current question.

### CPU

Use:

- sampling profiler;
- flame graph;
- hardware counters;
- compiler optimization report;
- generated assembly when needed.

Ask:

- where are cycles spent?
- are stalls compute, memory, branch, or synchronization related?
- is the code executed as often as expected?

### Memory

Use:

- allocation profiler;
- heap profiler;
- lifetime analysis;
- GC metrics;
- RSS/working-set metrics.

Ask:

- who allocates?
- how often?
- how large?
- how long does it live?
- what causes retention?

### Database

Use:

- query count;
- query plan;
- rows scanned;
- index usage;
- lock/wait information;
- round-trip timing.

Ask:

- is the problem query shape, query count, data volume, or contention?

### Distributed systems

Use:

- traces;
- request waterfalls;
- queue metrics;
- RPC counts;
- fan-out;
- retry counts.

Ask:

- what is on the critical path?
- what is waiting?
- what can overlap?

### Frontend/UI

Use:

- frame timing;
- layout/paint profiling;
- network waterfall;
- bundle/parse cost;
- long-task traces;
- interaction latency.

Ask:

- which work blocks the user-visible result?

Do not collect metrics without a question.

---

## Phase 9 — Reconcile model and measurement

Compare:

Expected dominant cost:
Observed dominant cost:

If they match, proceed.

If they differ, investigate:

- hidden work;
- incorrect assumptions;
- workload mismatch;
- instrumentation error;
- caching;
- JIT/runtime behavior;
- contention;
- queueing;
- branch/data skew;
- compiler transformation.

Unexpected profiles are information.

Do not immediately dismiss either the model or the measurement.

---

## Phase 10 — Choose the highest-leverage intervention

Prefer improvements in roughly this order when applicable:

1. eliminate unnecessary work;
2. eliminate unnecessary data movement;
3. improve algorithmic complexity;
4. remove false serial dependencies;
5. batch or reduce I/O;
6. move work off the critical path;
7. improve representation/data layout;
8. trade storage for repeated computation when justified;
9. eliminate allocation/copying;
10. improve locality;
11. improve concurrency/parallelism;
12. specialize a hot generic path;
13. optimize hot loops;
14. use hardware-specific techniques.

Do not start at level 14 when level 1 solves the problem.

---

## Phase 11 — Preserve a correctness bridge

For a complex optimization, maintain an obvious relationship between old and new behavior.

Useful techniques:

- keep a simple reference implementation in tests;
- differential-test optimized vs reference paths;
- assert invariants at boundaries;
- use property tests;
- compare numerical error explicitly;
- preserve old implementation behind a temporary verification flag;
- isolate the optimized kernel.

The more specialized the implementation becomes, the stronger the correctness bridge should be.

---

## Phase 12 — Implement the smallest durable change

While editing:

- preserve semantics;
- make data flow obvious;
- avoid unrelated cleanup;
- keep expensive operations visible;
- avoid speculative frameworks;
- isolate specialized paths;
- document non-obvious invariants;
- document why the chosen trade is valid;
- preserve observability.

Prefer code that communicates why it is efficient.

---

## Phase 13 — Verify correctness

Run relevant:

- unit tests;
- regression tests;
- integration tests;
- property tests;
- type/static analysis;
- numerical comparisons;
- concurrency tests;
- differential tests.

Performance changes frequently reveal hidden assumptions.

Make those assumptions explicit.

---

## Phase 14 — Re-benchmark

Compare the same workload against baseline.

Report:

Baseline:
New result:
Absolute difference:
Relative difference:
Variance/noise:
CPU change:
Memory change:
I/O change:
Tail-latency change:
Tradeoffs:

Do not call a result an improvement if it is inside measurement noise.

Do not hide a regression in another resource.

---

## Phase 15 — Explain the mechanism

A strong optimization report explains why the result changed.

Examples:

- one network round trip instead of twelve;
- one scan instead of N scans;
- O(n log n) instead of O(n²);
- 400 MB less copying;
- one allocation per batch instead of per element;
- derived state maintained once instead of recomputed repeatedly;
- independent requests issued concurrently;
- contiguous traversal replacing pointer chasing;
- setup moved out of a repeated loop;
- work removed from the serial critical path.

Avoid:

> The optimized version is faster.

State the causal mechanism.

---

## Phase 16 — Review the new optimization surface

After a successful change, ask:

- What is now the bottleneck?
- Did the critical path move?
- Did memory use rise?
- Did tail latency change?
- Did concurrency expose contention?
- Did complexity increase enough to require documentation?
- Is another optimization actually necessary?

Stop when the requirement is satisfied and further complexity is not justified.

---

# Architecture Review

For proposed designs, answer these before approval.

## Computation

- What is the minimal semantic job?
- What work is unavoidable?
- What work is incidental to this design?
- Does the architecture mirror the computation or obscure it?

## Dependency structure

- What is the longest serial dependency chain?
- Which dependencies are real?
- Which are accidental?
- Which operations can overlap?
- Are remote operations unnecessarily sequential?

## Data

- What representation matches dominant operations?
- How much data moves?
- How many transformations occur?
- How many copies occur?
- Is data arranged for the way it is consumed?
- Does the abstraction hide access patterns?

## State

- What invariants connect duplicated or cached state?
- Who owns mutation?
- How is invalidation handled?
- Can inconsistent states be represented?

## Boundaries

For every:

- service;
- queue;
- database;
- RPC;
- module;
- abstraction layer;
- serialization format;

ask:

> What capability does this boundary buy, and what does it cost?

A boundary may buy:

- independent deployment;
- fault isolation;
- information hiding;
- replaceability;
- security;
- ownership clarity.

Its costs may include:

- latency;
- serialization;
- copying;
- versioning;
- retries;
- failure modes;
- loss of batching;
- loss of locality.

Do not add expensive boundaries by default.

## Modularity

A useful module hides a design decision likely to change.

Do not mechanically divide systems by chronological processing steps if that causes every likely change to touch many modules.

Good modularity reduces the blast radius of change.

Performance-sensitive design should especially hide replaceable implementation choices while exposing enough cost information for callers to make sound decisions.

## Scale

Estimate behavior at:

- current workload;
- 10x workload;
- worst realistic workload;
- peak concurrency;
- large input;
- skewed input.

Look for cliffs:

- quadratic growth;
- unbounded queues;
- lock contention;
- fan-out explosions;
- memory duplication;
- cache collapse;
- rate-limit saturation.

Do not demand infinite scalability.

Do identify where the design stops being valid.

---

# Abstraction Discipline

Abstraction is a tool for managing reasoning.

It is not automatically good or bad.

## A good abstraction

A good abstraction:

- has a clear semantic contract;
- hides a decision that may change;
- reduces the caller's reasoning burden;
- does not require callers to know irrelevant detail;
- preserves important cost visibility;
- does not prevent batching/specialization without reason;
- makes invariants easier to state.

## A dangerous abstraction

Be suspicious when an abstraction:

- makes remote calls look like local calls;
- makes allocation invisible in a hot path;
- hides repeated iteration;
- hides synchronization;
- destroys data locality;
- forces one-item-at-a-time processing;
- prevents callers from controlling lifetime;
- mixes policy with mechanism;
- adds indirection with no change-isolation benefit.

## Cost transparency

APIs need not expose implementation trivia.

They should expose enough semantic information that important costs are predictable.

Examples:

Prefer:

- `fetch_many(ids)` over forcing N calls to `fetch(id)`;
- explicit ownership/lifetime over invisible copying;
- iterators whose traversal complexity is documented;
- APIs that distinguish cached/local/remote behavior when that distinction matters.

The goal is not "zero abstraction."

The goal is abstraction that preserves engineering truth.

---

# Clean-Code Discipline

Readable code and performant code are not opposites.

Prefer:

- meaningful names;
- direct control flow;
- explicit state transitions;
- cohesive functions;
- explicit ownership;
- representations matching operations;
- comments explaining invariants and tradeoffs.

Reject "cleanliness" when it introduces:

- unnecessary polymorphism;
- needless allocation;
- hidden I/O;
- excessive indirection;
- fragmented data;
- repeated transformations;
- excessive service boundaries;
- generic machinery around one stable use case.

Do not remove useful abstractions merely because abstraction exists.

Judge whether each abstraction carries its weight.

---

# Testing and Proof Discipline

Testing and reasoning answer different questions.

## Reasoning

Use invariants, contracts, and refinement to answer:

- Why should this be correct for the whole class of allowed executions?
- Which conditions make the transformation valid?
- Which states are impossible?

## Testing

Use tests to answer:

- Did this implementation preserve behavior on exercised cases?
- Did a previously observed bug stay fixed?
- Does the optimized path agree with a reference path?
- Does integration behavior remain intact?

Tests can demonstrate failure.

Passing tests do not prove the absence of all failures.

For high-risk logic, improve both the reasoning structure and the test evidence.

## Performance tests

Benchmarks prove performance claims only for their specified workload and environment.

Treat benchmark definitions as part of the performance contract.

Keep important benchmarks reproducible.

---

# Profiling Discipline

## Profiles are conditional evidence

A profile is evidence about:

- this program version;
- this environment;
- this workload;
- this time interval.

Do not generalize beyond that without justification.

## Frequency is not cost

A frequently executed statement may be cheap.

An infrequent statement may trigger:

- I/O;
- page faults;
- allocation;
- synchronization;
- expensive library work.

Measure the resource of interest, not only execution counts.

## Inclusive versus exclusive cost

Distinguish:

- cost directly in a function;
- cost caused by callees;
- cost on the request critical path.

A wrapper with high inclusive cost may not itself need optimization.

## Sampling versus instrumentation

Prefer sampling when low overhead and broad attribution matter.

Use instrumentation/counters when exact event counts matter.

Know that measurement can perturb the system.

## Representative profiles

When workload classes differ, profile more than one.

Examples:

- small and large inputs;
- cold and warm cache;
- low and peak concurrency;
- common and pathological data distributions.

---

# Benchmark Discipline

## Benchmark the right layer

Use:

- end-to-end benchmarks for user-visible outcomes;
- subsystem benchmarks for architectural changes;
- microbenchmarks for isolated mechanisms.

A microbenchmark cannot prove an end-to-end win without a contribution model.

## Control the environment

Where relevant, control or record:

- CPU governor/frequency;
- background load;
- thermal state;
- build configuration;
- compiler flags;
- runtime/JIT warmup;
- cache state;
- network conditions;
- database state.

## Report distributions

For latency, prefer:

- median;
- p95;
- p99;
- maximum when meaningful.

Average alone can hide tail regressions.

## Avoid benchmark theater

Do not:

- cherry-pick best runs;
- change workloads between before/after;
- compare debug and release builds;
- ignore warmup;
- report only percentages;
- hide absolute values;
- omit variance;
- benchmark an unrealistic input because it flatters the change.

---

# Low-Level Inspection

Follow the problem downward only as far as needed to explain the observed behavior.

## Compiled CPU paths

Inspect generated assembly or compiler reports when:

- instruction count matters;
- vectorization is expected;
- unexpected branches appear;
- loads/stores dominate;
- compiler optimization is uncertain;
- an abstraction is suspected to generate expensive code.

Do not inspect assembly for prestige.

Inspect it to answer a concrete question.

## Managed runtimes

Inspect:

- allocation;
- GC;
- JIT compilation;
- deoptimization;
- boxing;
- runtime dispatch.

## Databases

Inspect:

- execution plans;
- indexes;
- cardinality estimates;
- rows scanned;
- sort/hash operations;
- lock waits.

## Distributed systems

Inspect:

- trace waterfalls;
- retries;
- fan-out;
- queues;
- timeout chains;
- serialized awaits.

## GPU

Inspect:

- transfer volume;
- occupancy;
- launch overhead;
- synchronization;
- memory access;
- arithmetic intensity.

The principle is always the same:

> Follow the computation until the cost has a causal explanation.

---

# Anti-Patterns

## "Optimize later" architecture

Bad when today's decision creates:

- mandatory serialization;
- chatty protocols;
- rigid data layout;
- hidden ownership;
- impossible batching;
- distributed transactions;
- irreversible coupling.

Later optimization may then mean redesign, not tuning.

## Premature-optimization dismissal

Do not confuse:

- speculative micro-tuning;
with
- preserving efficient architecture.

Reject the first when unsupported.

Practice the second continuously.

## Profile-only engineering

Profiles locate observed cost.

They do not identify:

- unnecessary requirements;
- avoidable architecture;
- a better algorithm not present in the program;
- a missing batch API;
- a bad service boundary.

## Model-only engineering

Models identify expected cost.

They do not reveal:

- compiler/runtime surprises;
- workload skew;
- hidden contention;
- cache effects;
- unexpected library behavior;
- actual production hot paths.

## Cleverness without a contribution model

Do not optimize a local operation without estimating its contribution to the whole.

Use Amdahl-style bounds.

## Cache without invariant

A cache is duplicated state.

Without an invalidation/version rule, it is a correctness bug waiting to happen.

## Parallelism without dependency analysis

Adding threads/tasks does not remove serial dependencies.

It may add:

- synchronization;
- contention;
- scheduling overhead;
- memory pressure.

Parallelize independent work, not syntax.

## Abstraction worship

Patterns and abstractions are tools, not goals.

## Hardware worship

Do not tune cache lines while a needless remote request dominates.

## Unmeasured intuition

Intuition generates hypotheses.

Measurements decide observed effects.

## Measurement worship

Measurement without a model can optimize symptoms indefinitely.

Use theory to ask better questions.

## Irreversible specialization

Do not scatter hardware-specific or workload-specific assumptions throughout the codebase.

Isolate them behind a stable semantic boundary.

---

# Decision Standard

For ordinary production code, prefer the solution that best balances:

1. correctness;
2. comprehensibility;
3. simplicity;
4. maintainability;
5. appropriate performance;
6. compatibility;
7. testability;
8. observability;
9. adaptability;
10. future optimizability.

When performance is explicitly the problem, raise performance in priority without discarding the others.

Maximum hardware utilization is not automatically the goal.

The goal is the simplest design that satisfies the actual performance requirement with acceptable resource cost and operational risk.

---

# Review Heuristics

Use these questions in code review.

## Computation

- What work does this change cause at runtime?
- Is all of that work necessary?
- How often does it happen?
- What grows with input size?

## Data

- What data moves?
- What is copied?
- What is allocated?
- What is retained?
- Does the layout match access patterns?

## Dependencies

- What must wait for what?
- Did this introduce a new serial dependency?
- Can independent work overlap?

## I/O

- Did query/RPC/syscall count change?
- Can this be batched?
- Is expensive work hidden behind an innocent-looking method?

## Correctness

- What invariant does this rely on?
- Does the optimization preserve it?
- Is duplicated state synchronized?

## Evidence

- What is measured?
- What is estimated?
- Is the benchmark representative?
- Does the claimed improvement matter end-to-end?

## Future change

- What likely adaptation became easier?
- What likely adaptation became harder?
- Did this close an optimization path?

---

# Completion Checklist

Before finishing performance-sensitive work:

- [ ] Required external effect identified
- [ ] Relevant workload defined
- [ ] Correctness invariants identified
- [ ] Minimal semantic computation described
- [ ] Existing system inspected
- [ ] Necessary vs accidental work considered
- [ ] Rough lower bound considered
- [ ] Napkin model carries explicit units
- [ ] Order-of-magnitude feasibility checked
- [ ] CPU-seconds × RPS capacity considered when relevant
- [ ] Bytes × rate bandwidth/storage considered when relevant
- [ ] Little's Law concurrency check considered when relevant
- [ ] Fixed-latency vs throughput crossover considered
- [ ] Dominant term identified before detailed tuning
- [ ] Major uncertain assumptions bounded
- [ ] Candidate designs compared cheaply before deep prototyping when relevant
- [ ] Dependency depth considered
- [ ] Data movement considered
- [ ] Space/time tradeoffs considered
- [ ] Architecture checked for optimization blockers
- [ ] Baseline measured
- [ ] Profile/trace collected when appropriate
- [ ] Model reconciled with measurement
- [ ] Root cause identified
- [ ] Contribution to end-to-end cost estimated
- [ ] Smallest high-leverage change implemented
- [ ] Correctness bridge preserved
- [ ] Correctness verified
- [ ] Benchmark repeated
- [ ] Result exceeds measurement noise
- [ ] Absolute and relative results reported
- [ ] Resource tradeoffs reported
- [ ] Mechanism of improvement understood
- [ ] New bottleneck considered
- [ ] Future optimization paths remain open
- [ ] Diff self-reviewed

---

# Final Response

For optimization work, report:

## Summary

What changed.

## Required computation

What the system fundamentally needs to do.

## Performance model

What work, data movement, dependency depth, or resource pressure should dominate.

## Evidence

Baseline, profiling/tracing evidence, and what was actually observed.

## Implementation

What was changed and why this intervention had the highest leverage.

## Correctness

Invariants and verification used to preserve behavior.

## Performance results

Baseline:
New result:
Absolute delta:
Relative delta:
Variance:
Workload/environment:

## Tradeoffs

Memory:
Complexity:
Latency/throughput:
Portability:
Compatibility:
Operational risk:

## Mechanism

Why the improvement occurred.

## Remaining opportunities

Only meaningful next optimizations supported by evidence.

---
