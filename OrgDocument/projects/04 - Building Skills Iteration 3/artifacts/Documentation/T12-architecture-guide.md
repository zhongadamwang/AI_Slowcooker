# EDPS Iteration 3 — Architecture & Technical Guide

**Document**: T12-architecture-guide.md  
**Version**: 3.0.0  
**Date**: March 18, 2026  
**Audience**: Developers, system integrators, skill authors  

---

## 1. System Overview

Building Skills Iteration 3 adds an intelligent orchestration layer on top of the 30-skill EDPS ecosystem established in Iterations 1 and 2. The three new components form a loosely coupled triad:

```
User natural-language prompt
        │
        ▼
┌───────────────────────────────┐
│   edps-enhanced-nlp  (T09)    │  Intent classification, entity extraction,
│   EDPSNLPEngine               │  recommendation engine, context tracking
└───────────────┬───────────────┘
                │  IntentAnalysisResult
     ┌──────────┴──────────┐
     ▼                     ▼
┌─────────────┐    ┌──────────────────────────────┐
│ edps-quality│    │  edps-workflow-orchestrator   │
│ -gates (T08)│    │  (T07)  WorkflowOrchestrator  │
│ QualityGate │◄───│  selectWorkflowFromIntent()   │
│ Provider    │    │  executeWorkflow()             │
└──────┬──────┘    └──────────────┬───────────────┘
       │                          │
       │      Gate results        │  Skill invocations
       └──────────────────────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │  30-skill ecosystem │
              │  requirements-ingest│
              │  domain-extract...  │
              │  edps-compliance    │
              │  hierarchy-valid.   │
              │  ... (27 more)      │
              └─────────────────────┘
```

---

## 2. Component Architecture

### 2.1 edps-enhanced-nlp (T09)

**Location**: `.github/skills/edps-enhanced-nlp/`

```
edps-enhanced-nlp/
├── SKILL.md                  ← Copilot-facing skill definition
├── intent-patterns.json      ← Pattern library (7 categories × N subcategories)
├── nlp-engine.js             ← Core implementation
├── integration-architecture.md
└── test-suite.md
```

**Class hierarchy** (`nlp-engine.js`):
```
EDPSNLPEngine                    ← Main entry point
  ├── IntentAnalyzer             ← Regex pattern matching, confidence scoring
  ├── EntityExtractor            ← EDPS component / project context extraction
  ├── ProjectContextBuilder      ← Phase / quality / urgency context adaptation
  ├── RecommendationEngine       ← Skill and workflow ranking
  ├── NLWorkflowBuilder          ← NL description → structured workflow config
  ├── ClarificationGenerator     ← Threshold-based follow-up question generation
  └── LearningSystem             ← Sliding-window feedback history, pattern boosts
```

**Key interfaces**:
```typescript
// Primary call — returns full analysis result
analyzePrompt(prompt: string, context: ProjectContext): Promise<NLPAnalysisResult>

// Parse a natural language workflow description into a structured config
parseWorkflowDescription(description: string, context: ProjectContext): Promise<WorkflowConfig>

// Parse a modification request against an existing workflow
parseWorkflowModification(description: string, workflow: WorkflowConfig, context: ProjectContext): Promise<ModificationResult>

// Feed acceptance/rejection signal back to learning system
recordFeedback(feedback: FeedbackEvent): Promise<void>
```

**Intent categories** (7):
`analysis` | `creation` | `validation` | `integration` | `planning` | `troubleshooting` | `documentation`

**Performance** (post-OPT-2):  
P50: 132 ms · P95: 341 ms · P99: 598 ms · Memory growth: 4.1 MB / 100 calls

**Configuration** (constructor options):
```javascript
new EDPSNLPEngine({
    learningEnabled: true,          // default: true
    sessionTimeoutMs: 1_800_000,    // 30 minutes
    earlyExitConfidence: 0.92,      // OPT-2 threshold
    earlyExitMargin: 0.15,          // OPT-2 margin
    learningHistoryMax: 500         // OPT-1 sliding window
})
```

---

### 2.2 edps-workflow-orchestrator (T07)

**Location**: `.github/skills/edps-workflow-orchestrator/`

**Responsibilities**:
- Maintain a library of workflow patterns (end-to-end, fast-track, validation-focus, etc.)
- Accept `IntentAnalysisResult` and map to best-fit workflow pattern
- Execute selected workflow, invoking skills in dependency order
- Insert and evaluate quality gates at configured checkpoints
- Support parallel step groups (`parallel_group` field on step definitions)
- Adapt workflow quality profile based on NLP-detected quality/urgency level

**Workflow execution model** (post-OPT-4):
```
executeWorkflow(workflowId, input, options)
  └── _groupStepsByOrder(steps)         ← groups steps with same order + parallel_group
      FOR each group:
        IF group.length === 1 OR no parallel_group:
          await _executeStep(step)       ← sequential (original behaviour)
          await _runGatesForStep(step)
        ELSE:
          await Promise.all(_executeStep × group)  ← parallel
          await _runGatesForParallelGroup(group)
```

**Built-in workflow patterns**:

| Pattern ID | Trigger Intent | Steps | Gates |
|-----------|---------------|-------|-------|
| `fast_track_analysis` | analysis + expedited | 3 | 1 (light) |
| `requirements_to_diagram` | creation (diagram) | 6 | 2 (standard) |
| `domain_modeling_workflow` | creation (org model) | 10 | 3 (comprehensive) |
| `validation_focus` | validation | 5 | 2 (comprehensive) |
| `process_integration_workflow` | integration | 6 | 2 (standard) |
| `change_management_workflow` | integration (change) | 4 | 1 (standard) |
| `planning_workflow` | planning | 5 | 1 (standard) |
| `end_to_end` | any + high quality | 12 | 4 (comprehensive) |

**Performance** (post-OPT-4):  
Workflow selection P95: 61 ms · Full 8-step workflow P95: 44.1 s (down from 62.7 s)  
Concurrent capacity: 28 simultaneous workflows

---

### 2.3 edps-quality-gates (T08)

**Location**: `.github/skills/edps-quality-gates/`

**Responsibilities**:
- Define a catalogue of quality gates each with typed rules
- Execute gate rules against skill outputs, return pass/fail/warning with NL explanation
- Select appropriate gate sets based on intent category and quality level
- Integrate with the orchestrator to block/allow workflow continuation on gate result
- Provide `explainGateFailure()` — translates technical failures to plain English with remediation skill references

**Gate catalogue** (representative):

| Gate ID | Checks | Typical Workflows |
|---------|--------|-------------------|
| `output_quality_check` | Completeness score ≥ threshold | All fast-track |
| `traceability_completeness` | Requirement IDs in all outputs | Standard+ |
| `edps_vr_validation` | VR-1 through VR-4 boundary rules | Comprehensive |
| `hierarchy_integrity` | Cross-level type consistency | Comprehensive |
| `conflict_check` | Pre-merge conflict detection | Integration |
| `boundary_validation` | Single external interface (VR-1) | Diagram creation |

**Gate profiles**:

| Profile | Gates | When Used |
|---------|-------|-----------|
| `light` | output_quality_check | Expedited quality intent |
| `standard` | output_quality_check + traceability_completeness | Default |
| `comprehensive` | Standard + edps_vr_validation + hierarchy_integrity | High quality intent |

**Performance** (post-OPT-3):  
Single gate P95: 139 ms · 3-gate set P95: 362 ms  
Gate accuracy: 100% on T11 benchmark

**Compiled rule cache** (OPT-3):
```javascript
this._compiledRuleCache = new Map();  // gate_id → compiled rules
// Invalidate with: gateProvider.invalidateCache('edps_vr_validation')
```

---

## 3. Integration Patterns

### 3.1 Minimum integration (NLP only)

```javascript
const { EDPSNLPEngine } = require('.github/skills/edps-enhanced-nlp/nlp-engine.js');

const engine = new EDPSNLPEngine();
await engine.initialize();

const result = await engine.analyzePrompt(userPrompt, projectContext);
// result.intent_analysis.primary_intent → 'analysis' | 'creation' | ...
// result.skill_recommendations[0].skill_id → best skill to invoke
// result.workflow_recommendations[0].pattern_id → best workflow pattern
```

### 3.2 Full triad integration

```javascript
const engine      = new EDPSNLPEngine();
const orchestrator = new WorkflowOrchestrator({ nlpEngine: engine });
const gateProvider = new QualityGateProvider(gateDefinitions);

await engine.initialize();
orchestrator.setQualityGateProvider(gateProvider);

// Single call — NLP → workflow selection → gate-enforced execution
const result = await orchestrator.executeFromPrompt(userPrompt, input, projectContext);
```

### 3.3 Session context across multi-turn interactions

```javascript
// Turn 1 — establishes context
const ctx1 = await engine.analyzePrompt('Design phase, high quality model needed', {});
// Turn 2 — inherits project_phase=design, quality_level=high automatically
const ctx2 = await engine.analyzePrompt('Validate the hierarchy', {});
// ctx2.applied_context.project_phase === 'design'
// ctx2.applied_context.quality_level === 'high'
```

---

## 4. Performance Reference

| Component | Operation | P50 | P95 | P99 | Target |
|-----------|-----------|-----|-----|-----|--------|
| T09 NLP | `analyzePrompt()` | 132 ms | 341 ms | 598 ms | < 3,000 ms |
| T09 NLP | Entity extraction | — | 194 ms | — | < 1,000 ms |
| T07 Orch. | Workflow selection | 26 ms | 61 ms | 112 ms | < 2,000 ms |
| T07 Orch. | Full workflow (8-step) | 21.4 s | 44.1 s | 68.2 s | < 300 s |
| T08 Gates | Single gate | 30 ms | 139 ms | 271 ms | < 5,000 ms |
| T08 Gates | 3-gate set | — | 362 ms | — | < 10,000 ms |

**Memory**: Combined peak 84 MB · NLP growth 4.1 MB / 100 calls (bounded at 500 history entries)  
**Concurrency**: 28 simultaneous workflows tested · 0% error rate

---

## 5. Data Flow Schemas

### `IntentAnalysisResult` (output of `analyzePrompt()`)

```typescript
interface IntentAnalysisResult {
  intent_analysis: {
    primary_intent: 'analysis' | 'creation' | 'validation' | 'integration' | 'planning' | 'troubleshooting' | 'documentation';
    confidence: number;           // 0.0–1.0
    multi_intent: boolean;
    quality_level: 'expedited' | 'standard' | 'high';
    urgency_level: 'low' | 'medium' | 'high';
    matched_subcategories: SubcategoryMatch[];
  };
  entities: {
    edps_components: Entity[];
    project_context: Entity[];
    quality_requirements: Entity[];
    constraints: Entity[];
    skills_mentioned: string[];
  };
  skill_recommendations: SkillRecommendation[];    // max 5, ranked by score
  workflow_recommendations: WorkflowRecommendation[]; // max 3
  clarification_questions: string[];               // empty if confidence ≥ 0.85
  applied_context: SessionContext;                 // accumulated multi-turn state
}
```

### `GateResult` (output of `evaluateGate()`)

```typescript
interface GateResult {
  gate_id: string;
  status: 'passed' | 'failed' | 'warning';
  checks: CheckResult[];
  explanation: string;            // plain English, always set
  remediation_skills?: string[];  // set when status === 'failed'
  execution_time_ms: number;
}
```

---

## 6. Extension Points

### Adding a new workflow pattern

1. Add entry to the workflow pattern library JSON in `edps-workflow-orchestrator`
2. Set `parallel_group` on steps that are dependency-free and safe to parallelise
3. Map pattern to one or more intent subcategory IDs in the orchestrator's intent-to-pattern table
4. Add test cases to Category 2 of the T10 test suite

### Adding a new quality gate

1. Define gate in `edps-quality-gates` gate catalogue with typed rules
2. Add gate to one or more gate profiles (`light`, `standard`, `comprehensive`)
3. Implement `_compileRules()` and `_runRules()` for the new rule types
4. Call `gateProvider.invalidateCache()` after definition update
5. Add gate to `Cat-4.1` benchmark test cases

### Adding new intent subcategories (NLP)

1. Add subcategory entry to `intent-patterns.json` under the relevant category
2. Provide `primary_patterns[]`, `negative_patterns[]`, `recommended_skills[]`, `workflow_patterns[]`
3. Re-run `T11-benchmark-validation` to verify accuracy remains ≥ 90%
4. Update `T10-test-suite.md` accuracy benchmark set if new prompt types are covered

---

## 7. Dependency Matrix

| Component | Depends On | Optional Integration |
|-----------|-----------|---------------------|
| edps-enhanced-nlp | `fs-extra`, Node.js EventEmitter | T06 edps-skill-navigator (ranking), T07 (workflow bridge), T08 (gate bridge) |
| edps-workflow-orchestrator | All 30 invocable skills | T09 (NLP-driven selection), T08 (gate enforcement) |
| edps-quality-gates | None (self-contained) | T07 (gate injection), T09 (failure NL enrichment) |
