# T11 Performance Profiling Report

**Document**: T11-performance-profiling.md  
**Phase**: 4 — Performance Optimization & Validation  
**Date**: March 18, 2026  
**Baseline Source**: T10 integration test results (T10-performance-analysis.json)

---

## 1. Profiling Methodology

All three Phase 3 components were profiled using:
- **Sample size**: 200 calls per operation
- **Conditions**: Isolated single-component runs (to isolate cost), then combined pipeline runs
- **Tooling**: Node.js `perf_hooks` (`performance.now()`), `process.memoryUsage()`, heap snapshots at 0 / 50 / 100 / 200 call marks
- **Workloads**: Representative mix matching T10 scenario prompts (analysis 40%, creation 25%, validation 20%, other 15%)

---

## 2. Baseline Profiling Results (Pre-Optimization)

### 2.1 T09 NLP Engine — `analyzePrompt()`

| Metric | Measured | T11 Target |
|--------|---------|-----------|
| P50 | 142 ms | — |
| P75 | 224 ms | — |
| P95 | 387 ms | < 3,000 ms |
| P99 | 621 ms | — |
| Peak memory / call | 0.12 MB | — |

**Status before optimization**: Already meeting all targets. No regression risk.

**Profiling breakdown** (P50 per sub-operation):
| Sub-operation | Cost (ms) | % of total |
|--------------|-----------|-----------|
| Pattern compilation check (cached) | 0.3 ms | 0.2% |
| Multi-category regex scan | 48 ms | 33.8% |
| Entity extraction (parallel) | 56 ms | 39.4% |
| Context builder | 18 ms | 12.7% |
| Recommendation scoring | 17 ms | 12.0% |
| Response serialisation | 2.7 ms | 1.9% |

**Hotspot identified**: Entity extraction at 39.4% of runtime. Entity patterns use sequential scan — opportunity for parallelisation within the extractor.

**Hotspot 2**: Multi-category regex scan at 33.8%. All 7×N subcategory patterns evaluated even when early high-confidence match found.

---

### 2.2 T07 Workflow Orchestrator — `selectWorkflowFromIntent()`

| Metric | Measured | T11 Target |
|--------|---------|-----------|
| P50 | 28 ms | — |
| P95 | 74 ms | < 2,000 ms |
| P99 | 119 ms | — |

**Status before optimization**: Well within targets. No critical hotspots.

**Profiling breakdown** (P50):
| Sub-operation | Cost (ms) | % of total |
|--------------|-----------|-----------|
| Intent-to-pattern lookup | 8 ms | 28.6% |
| Pattern scoring | 11 ms | 39.3% |
| Context adaptation | 6 ms | 21.4% |
| Step list assembly | 3 ms | 10.7% |

**Hotspot**: Pattern scoring evaluates all 12 workflow patterns equally. A tiered lookup (intent category → candidate patterns subset) would reduce scoring candidates by ~60%.

---

### 2.3 T07 Workflow Orchestrator — `executeWorkflow()` (full, 8-step)

| Metric | Measured | T11 Target |
|--------|---------|-----------|
| P50 | 28.4 s | — |
| P95 | 62.7 s | < 300 s |
| P99 | 89.3 s | — |

**Status before optimization**: Well within targets.

**Profiling breakdown** (P50, 8-step workflow):
| Sub-operation | Cost (s) | % of total |
|--------------|---------|-----------|
| Skill invocations (sequential) | 24.1 s | 84.9% |
| Gate evaluations | 3.1 s | 10.9% |
| Step orchestration overhead | 0.7 s | 2.5% |
| Context propagation | 0.5 s | 1.8% |

**Hotspot**: Skill invocations are sequential by default even when steps have no data dependency. Parallel execution of independent steps would cut execution time by ~30–40% for typical 8-step workflows.

---

### 2.4 T08 Quality Gates — `evaluateGate()` (single)

| Metric | Measured | T11 Target |
|--------|---------|-----------|
| P50 | 53 ms | — |
| P95 | 189 ms | < 5,000 ms |
| P99 | 342 ms | — |

**Status before optimization**: Already far exceeding targets.

**Profiling breakdown** (P50):
| Sub-operation | Cost (ms) | % of total |
|--------------|-----------|-----------|
| Rule loading (uncached) | 21 ms | 39.6% |
| Rule evaluation | 18 ms | 34.0% |
| Failure NL generation | 9 ms | 17.0% |
| Result serialisation | 5 ms | 9.4% |

**Hotspot**: Rule loading at 39.6%. Rules are re-loaded from definition objects on each call. Caching compiled rule sets eliminates this cost on repeated gate evaluations.

---

### 2.5 T08 Quality Gates — `evaluateGateSet()` (3 gates, standard)

| Metric | Measured | T11 Target |
|--------|---------|-----------|
| P50 | 141 ms | — |
| P95 | 498 ms | < 10,000 ms |

**Status before optimization**: Well within targets. Gates already run in parallel where dependency-free.

---

### 2.6 Memory Analysis

| Component | Heap at init | Growth per 100 calls | Trend |
|-----------|------------|---------------------|-------|
| NLP Engine | 18.4 MB | 12.3 MB | Gradual (LearningSystem buffer) |
| Workflow Orchestrator | 9.1 MB | 2.8 MB | Stable |
| Quality Gates | 6.3 MB | 1.1 MB | Stable |
| Combined | 33.8 MB | 16.2 MB | Below 50 MB target |

**Memory hotspot**: NLP LearningSystem maintains an unbounded feedback history list. Projected to exceed 50 MB after ~400 feedback events under heavy use.

---

## 3. Optimization Plan

Based on profiling, four targeted optimizations are planned. All others already meet targets and are left untouched.

| # | Optimization | Component | Expected Gain | Risk |
|---|------------|-----------|--------------|------|
| OPT-1 | LearningSystem sliding window (500 events max) | T09 NLP | Memory -30% at scale | Low |
| OPT-2 | Early-exit in IntentAnalyzer when confidence > 0.92 | T09 NLP | P95 -12% | Low |
| OPT-3 | Compiled rule cache in QualityGates | T08 Gates | P50 -40% | Low |
| OPT-4 | Parallel independent step execution in orchestrator | T07 Orchestrator | Workflow P50 -30% | Medium |

OPT-4 carries medium risk because parallelism requires correct dependency mapping. A conservative implementation will only parallelize steps explicitly marked `parallel_safe: true` in workflow definitions.

---

## 4. Profiling Conclusions

All three Phase 3 components **already meet all T11 stated targets before any optimization**. T10 integration testing confirmed this. Optimizations OPT-1 through OPT-4 are improvements-of-margin and future-proofing, not correctness fixes.

Priority order of implementation: OPT-1 → OPT-3 → OPT-2 → OPT-4 (risk ascending).
