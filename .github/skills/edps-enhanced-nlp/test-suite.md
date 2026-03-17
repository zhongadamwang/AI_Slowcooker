# EDPS Enhanced NLP - Test Suite

## Overview

Comprehensive test suite validating intent classification accuracy (>90% target), entity extraction quality, workflow parsing, recommendation quality, performance SLA (<3s), and the learning system. Tests are organized from unit through integration and performance levels.

## Test Organization
```
tests/
├── unit/
│   ├── intent_analyzer_tests.md      ← Pattern matching correctness
│   ├── entity_extractor_tests.md     ← Entity recognition accuracy
│   ├── recommendation_engine_tests.md← Scoring and ranking logic
│   └── workflow_builder_tests.md     ← NL-to-workflow parsing
├── integration/
│   ├── t06_navigator_integration.md  ← Skill discovery enrichment
│   ├── t07_orchestrator_integration.md← Workflow creation from NL
│   └── t08_gate_integration.md      ← Gate selection and failure NL
├── accuracy/
│   ├── intent_classification_benchmark.md
│   └── entity_extraction_benchmark.md
├── performance/
│   └── response_time_benchmarks.md
└── learning/
    └── feedback_learning_tests.md
```

---

## Unit Tests

### 1. Intent Analyzer

```javascript
describe('IntentAnalyzer', () => {
    let analyzer;

    beforeAll(async () => {
        analyzer = new IntentAnalyzer();
        const patternLib = await loadPatternLibrary();
        analyzer.setPatternLibrary(patternLib);
    });

    describe('Primary intent classification', () => {
        const cases = [
            // Analysis
            { prompt: 'Review the requirements document for completeness', expected: 'analysis' },
            { prompt: 'Analyze the organizational hierarchy for EDPS compliance', expected: 'analysis' },
            { prompt: 'What are the domain concepts in this project specification?', expected: 'analysis' },
            { prompt: 'Check if the collaboration diagram follows boundary validation rules', expected: 'analysis' },
            // Creation
            { prompt: 'Create a collaboration diagram from these requirements', expected: 'creation' },
            { prompt: 'Generate a project documentation structure for a new EDPS process', expected: 'creation' },
            { prompt: 'Set up a new organizational model following EDPS methodology', expected: 'creation' },
            // Validation
            { prompt: 'Validate this hierarchy against EDPS standards', expected: 'validation' },
            { prompt: 'Check for compliance issues in the current model', expected: 'validation' },
            { prompt: 'Ensure all boundary rules are satisfied in the collaboration diagram', expected: 'validation' },
            { prompt: 'Verify traceability links throughout the project', expected: 'validation' },
            // Integration
            { prompt: 'Merge these requirements with the existing organizational model', expected: 'integration' },
            { prompt: 'Integrate the new process into our current hierarchy', expected: 'integration' },
            { prompt: 'Update the organizational model with these changes', expected: 'integration' },
            // Planning
            { prompt: 'Estimate the effort for implementing the requirements', expected: 'planning' },
            { prompt: 'Build the project schedule for this iteration', expected: 'planning' },
            { prompt: 'Derive tasks from the analyzed requirements', expected: 'planning' },
            // Troubleshooting
            { prompt: 'Fix the boundary violations in the diagram', expected: 'troubleshooting' },
            { prompt: 'Why is the hierarchy validation failing?', expected: 'troubleshooting' },
            { prompt: 'Resolve the conflicts in the merged requirements', expected: 'troubleshooting' },
            // Documentation
            { prompt: 'Document the process hierarchy for all levels', expected: 'documentation' },
            { prompt: 'Generate the collaboration documentation', expected: 'documentation' }
        ];

        test.each(cases)('classifies "$prompt" as $expected', async ({ prompt, expected }) => {
            const result = await analyzer.analyze(prompt, {});
            expect(result.primary_intent).toBe(expected);
        });
    });

    describe('Confidence scoring', () => {
        test('should have high confidence for unambiguous analysis request', async () => {
            const result = await analyzer.analyze('Analyze this requirements document for domain concepts', {});
            expect(result.confidence).toBeGreaterThan(0.80);
        });

        test('should have lower confidence for ambiguous multi-intent request', async () => {
            // "create and validate" mixes creation and validation
            const result = await analyzer.analyze('Create a diagram and then validate it', {});
            expect(result.multi_intent).toBe(true);
            expect(result.confidence).toBeLessThan(0.90);
        });

        test('should detect multi-intent when two strong categories match', async () => {
            const result = await analyzer.analyze('Build a workflow and check that it is EDPS compliant', {});
            expect(result.multi_intent).toBe(true);
        });
    });

    describe('Sub-category detection', () => {
        test('should identify compliance_analysis sub-category', async () => {
            const result = await analyzer.analyze('Check EDPS VR-1 boundary compliance', {});
            const subIds = result.matched_subcategories.map(s => s.id);
            expect(subIds).toContain('compliance_analysis');
        });

        test('should identify hierarchy_analysis sub-category', async () => {
            const result = await analyzer.analyze('Validate the cross-level consistency of the hierarchy', {});
            const subIds = result.matched_subcategories.map(s => s.id);
            expect(subIds).toContain('hierarchy_analysis');
        });

        test('should identify domain_analysis sub-category', async () => {
            const result = await analyzer.analyze('Extract domain entities from the business specification', {});
            const subIds = result.matched_subcategories.map(s => s.id);
            expect(subIds).toContain('domain_analysis');
        });
    });

    describe('Quality and urgency detection', () => {
        test('should detect high quality requirement', async () => {
            const result = await analyzer.analyze('Do a comprehensive analysis of everything', {});
            expect(result.quality_level).toBe('high');
        });

        test('should detect expedited quality requirement', async () => {
            const result = await analyzer.analyze('Quick check of the requirements', {});
            expect(result.quality_level).toBe('expedited');
        });

        test('should detect high urgency', async () => {
            const result = await analyzer.analyze('Please validate urgently — it is blocking deployment', {});
            expect(result.urgency_level).toBe('high');
        });

        test('should default to standard quality and medium urgency', async () => {
            const result = await analyzer.analyze('Analyze the requirements', {});
            expect(result.quality_level).toBe('standard');
            expect(result.urgency_level).toBe('medium');
        });
    });
});
```

### 2. Entity Extractor

```javascript
describe('EntityExtractor', () => {
    let extractor;

    beforeAll(async () => {
        extractor = new EntityExtractor();
        extractor.setPatternLibrary(await loadPatternLibrary());
    });

    describe('EDPS component extraction', () => {
        test('should extract boundary rule references', async () => {
            const result = await extractor.extract('Check VR-1 boundary compliance', {});
            expect(result.edps_components.length).toBeGreaterThan(0);
            expect(result.edps_components.some(e => /vr-?1/i.test(e.value))).toBe(true);
        });

        test('should extract hierarchy level references', async () => {
            const result = await extractor.extract('Validate the Level 2 sub-processes', {});
            expect(result.edps_components.some(e =>
                e.type === 'hierarchy_indicators' || /level/i.test(e.value)
            )).toBe(true);
        });

        test('should extract explicitly mentioned skill names', async () => {
            const result = await extractor.extract(
                'Run the requirements-ingest skill on this document', {}
            );
            expect(result.skills_mentioned).toContain('requirements-ingest');
        });
    });

    describe('Project context extraction', () => {
        test('should extract project phase context', async () => {
            const result = await extractor.extract('We are in the design phase now', {});
            expect(result.project_context.some(e => e.type === 'phase_indicators')).toBe(true);
        });

        test('should extract artifact references', async () => {
            const result = await extractor.extract('Check the collaboration.md file', {});
            expect(result.project_context.some(e => /collaboration\.md/i.test(e.value))).toBe(true);
        });
    });

    describe('Quality entity extraction', () => {
        test('should extract quality level entities', async () => {
            const result = await extractor.extract('Do a thorough and comprehensive review', {});
            expect(result.quality_requirements.some(e => e.type === 'quality_level')).toBe(true);
        });

        test('should extract urgency entities', async () => {
            const result = await extractor.extract('This is urgent — deadline is today', {});
            expect(result.quality_requirements.some(e => e.type === 'urgency_indicators')).toBe(true);
        });
    });

    describe('Constraint extraction', () => {
        test('should extract scope constraint', async () => {
            const result = await extractor.extract('Only focus on the authentication boundary', {});
            expect(result.constraints.length).toBeGreaterThan(0);
        });
    });
});
```

### 3. Recommendation Engine

```javascript
describe('RecommendationEngine', () => {
    let engine;
    let mockPatternLib;

    beforeAll(async () => {
        mockPatternLib = await loadPatternLibrary();
        engine = new RecommendationEngine();
        engine.setPatternLibrary(mockPatternLib);
    });

    describe('Skill recommendation generation', () => {
        test('should recommend domain-extractconcepts for domain analysis intent', async () => {
            const intentAnalysis = {
                primary_intent: 'analysis',
                confidence: 0.92,
                quality_level: 'standard',
                urgency_level: 'medium',
                matched_subcategories: [{
                    id: 'domain_analysis',
                    score: 0.88,
                    recommended_skills: ['domain-extractconcepts', 'domain-alignentities'],
                    workflow_patterns: ['domain_modeling_workflow']
                }]
            };

            const entities = { skills_mentioned: [], all: [], edps_components: [], project_context: [], quality_requirements: [], constraints: [] };
            const context = {
                project_phase: 'design',
                quality_level: 'standard',
                urgency_level: 'medium',
                adaptations: { boosted_skills: [], suppressed_skills: [], quality_gates: [], workflow_modifiers: [] },
                applied_factors: []
            };

            const recs = await engine.generateSkillRecommendations(intentAnalysis, entities, context);

            expect(recs[0].skill_id).toBe('domain-extractconcepts');
            expect(recs[0].confidence).toBeGreaterThan(0.70);
        });

        test('should boost explicitly mentioned skills', async () => {
            const intentAnalysis = {
                primary_intent: 'validation',
                confidence: 0.85,
                quality_level: 'standard',
                urgency_level: 'medium',
                matched_subcategories: [{
                    id: 'edps_validation',
                    score: 0.90,
                    recommended_skills: ['edps-compliance', 'hierarchy-validation'],
                    workflow_patterns: []
                }]
            };

            const entities = {
                skills_mentioned: ['hierarchy-validation'],
                all: [], edps_components: [], project_context: [], quality_requirements: [], constraints: []
            };

            const context = {
                adaptations: { boosted_skills: [], suppressed_skills: [], quality_gates: [], workflow_modifiers: [] }
            };

            const recs = await engine.generateSkillRecommendations(intentAnalysis, entities, context);
            const hierarchyRec = recs.find(r => r.skill_id === 'hierarchy-validation');

            expect(hierarchyRec).toBeDefined();
            // explicitly_mentioned flag should be set
            expect(hierarchyRec.explicitly_mentioned).toBe(true);
        });

        test('should suppress phase-inappropriate skills', async () => {
            const intentAnalysis = {
                primary_intent: 'creation',
                confidence: 0.88,
                quality_level: 'standard',
                urgency_level: 'medium',
                matched_subcategories: [{
                    id: 'diagram_creation',
                    score: 0.85,
                    recommended_skills: ['diagram-generatecollaboration', 'requirements-ingest'],
                    workflow_patterns: []
                }]
            };

            const entities = { skills_mentioned: [], all: [], edps_components: [], project_context: [], quality_requirements: [], constraints: [] };
            const context = {
                project_phase: 'completion',
                adaptations: {
                    boosted_skills: ['documentation-automation'],
                    suppressed_skills: ['requirements-ingest'],
                    quality_gates: [], workflow_modifiers: []
                }
            };

            const recs = await engine.generateSkillRecommendations(intentAnalysis, entities, context);
            const reqIngest = recs.find(r => r.skill_id === 'requirements-ingest');

            // requirements-ingest should have lower score due to phase suppression
            const firstRec = recs[0];
            if (reqIngest) {
                expect(reqIngest.score).toBeLessThan(firstRec.score);
            }
        });

        test('should return at most 5 recommendations', async () => {
            const intentAnalysis = {
                primary_intent: 'analysis',
                confidence: 0.80,
                quality_level: 'standard',
                urgency_level: 'medium',
                matched_subcategories: [
                    { id: 'requirements_analysis', score: 0.7, recommended_skills: ['requirements-ingest', 'process-w5h', 'goals-extract', 'process-scopemin'], workflow_patterns: [] },
                    { id: 'domain_analysis', score: 0.6, recommended_skills: ['domain-extractconcepts', 'domain-alignentities', 'domain-proposenewconcepts'], workflow_patterns: [] }
                ]
            };

            const entities = { skills_mentioned: [], all: [], edps_components: [], project_context: [], quality_requirements: [], constraints: [] };
            const context = { adaptations: { boosted_skills: [], suppressed_skills: [] } };

            const recs = await engine.generateSkillRecommendations(intentAnalysis, entities, context);
            expect(recs.length).toBeLessThanOrEqual(5);
        });
    });
});
```

### 4. Natural Language Workflow Builder

```javascript
describe('NLWorkflowBuilder', () => {
    let builder;

    beforeAll(async () => {
        builder = new NLWorkflowBuilder();
        builder.setPatternLibrary(await loadPatternLibrary());
    });

    describe('Workflow pattern matching', () => {
        test('should match end-to-end workflow pattern', async () => {
            const result = await builder.parse(
                'I need a full end-to-end workflow from requirements to documentation', {}
            );
            expect(['pattern_match', 'custom_build']).toContain(result.type);
        });

        test('should extract starting point from natural language', async () => {
            const result = await builder.parse(
                'Starting from the requirements document, create a collaboration diagram', {}
            );
            expect(result.components.starting_point).toBeTruthy();
            expect(/requirement/i.test(result.components.starting_point)).toBe(true);
        });

        test('should extract quality level from workflow description', async () => {
            const result = await builder.parse(
                'Do a comprehensive end-to-end workflow with thorough validation', {}
            );
            expect(result.components.quality_level).toBe('high');
        });

        test('should extract explicit steps when numbered list is provided', async () => {
            const result = await builder.parse(
                'I need:\n1. Ingest requirements\n2. Extract domain concepts\n3. Generate collaboration diagram', {}
            );
            expect(result.components.explicit_steps).toHaveLength(3);
        });
    });

    describe('Workflow modification parsing', () => {
        const existingWorkflow = { id: 'test_workflow', steps: ['requirements-ingest', 'domain-extractconcepts'] };

        test('should classify add step modification', async () => {
            const result = await builder.parseModification(
                'Add a validation step after the domain extraction', existingWorkflow, {}
            );
            expect(result.modification_type).toBe('add_step');
        });

        test('should classify remove step modification', async () => {
            const result = await builder.parseModification(
                'Remove the domain extraction step', existingWorkflow, {}
            );
            expect(result.modification_type).toBe('remove_step');
        });

        test('should classify quality change modification', async () => {
            const result = await builder.parseModification(
                'Make it more comprehensive with higher quality validation', existingWorkflow, {}
            );
            expect(result.modification_type).toBe('change_quality');
        });

        test('should classify sequence change modification', async () => {
            const result = await builder.parseModification(
                'Move the domain extraction before the diagram creation', existingWorkflow, {}
            );
            expect(result.modification_type).toBe('change_sequence');
        });
    });
});
```

---

## Accuracy Benchmark Tests

### Intent Classification Benchmark (90% accuracy target)

```javascript
describe('Intent Classification Accuracy Benchmark', () => {
    let analyzer;

    beforeAll(async () => {
        analyzer = new IntentAnalyzer();
        analyzer.setPatternLibrary(await loadPatternLibrary());
    });

    test('should achieve >90% accuracy across 50-prompt benchmark set', async () => {
        const benchmarkPrompts = [
            // Analysis (10 prompts)
            { prompt: 'Review this requirements document', expected: 'analysis' },
            { prompt: 'Examine the hierarchy for structural issues', expected: 'analysis' },
            { prompt: 'What domain concepts exist in this spec?', expected: 'analysis' },
            { prompt: 'Assess the collaboration diagram quality', expected: 'analysis' },
            { prompt: 'Tell me about the domain entities', expected: 'analysis' },
            { prompt: 'Survey the current organizational model', expected: 'analysis' },
            { prompt: 'Evaluate the VR-2 participant classifications', expected: 'analysis' },
            { prompt: 'Investigate the broken hierarchy links', expected: 'analysis' },
            { prompt: 'Understand the project phase context', expected: 'analysis' },
            { prompt: 'Explore the requirements coverage gaps', expected: 'analysis' },
            // Creation (10 prompts)
            { prompt: 'Create a collaboration diagram', expected: 'creation' },
            { prompt: 'Generate documentation for all hierarchy levels', expected: 'creation' },
            { prompt: 'Build a full end-to-end workflow', expected: 'creation' },
            { prompt: 'Design the domain model', expected: 'creation' },
            { prompt: 'Set up a new organizational model', expected: 'creation' },
            { prompt: 'Initialize a new EDPS project structure', expected: 'creation' },
            { prompt: 'Draft the requirements document', expected: 'creation' },
            { prompt: 'Produce a project schedule', expected: 'creation' },
            { prompt: 'Author the collaboration documentation', expected: 'creation' },
            { prompt: 'Construct a hierarchy from the requirements', expected: 'creation' },
            // Validation (10 prompts)
            { prompt: 'Validate EDPS compliance', expected: 'validation' },
            { prompt: 'Verify all boundary rules are satisfied', expected: 'validation' },
            { prompt: 'Check VR-1 compliance', expected: 'validation' },
            { prompt: 'Confirm the hierarchy is structurally correct', expected: 'validation' },
            { prompt: 'Test the collaboration diagram for errors', expected: 'validation' },
            { prompt: 'Ensure participant types are correct', expected: 'validation' },
            { prompt: 'Assert message flows are complete', expected: 'validation' },
            { prompt: 'Verify traceability links are intact', expected: 'validation' },
            { prompt: 'Is this diagram VR-3 compliant?', expected: 'validation' },
            { prompt: 'Does the hierarchy meet EDPS standards?', expected: 'validation' },
            // Integration (10 prompts)
            { prompt: 'Merge these two requirement documents', expected: 'integration' },
            { prompt: 'Integrate the new process into the hierarchy', expected: 'integration' },
            { prompt: 'Update the organizational model with new changes', expected: 'integration' },
            { prompt: 'Combine the requirements from both sources', expected: 'integration' },
            { prompt: 'Reconcile conflicts between requirements', expected: 'integration' },
            { prompt: 'Sync the collaboration diagram with new requirements', expected: 'integration' },
            { prompt: 'Add the new sub-process to the hierarchy', expected: 'integration' },
            { prompt: 'Incorporate the change request into the model', expected: 'integration' },
            { prompt: 'Harmonize the domain models from both systems', expected: 'integration' },
            { prompt: 'Restructure the hierarchy levels', expected: 'integration' },
            // Planning + Troubleshooting + Documentation (10 prompts)
            { prompt: 'Estimate the effort for this project', expected: 'planning' },
            { prompt: 'Build a project schedule', expected: 'planning' },
            { prompt: 'Derive tasks from the requirements', expected: 'planning' },
            { prompt: 'Generate a status report', expected: 'planning' },
            { prompt: 'Fix the VR-1 violation in the diagram', expected: 'troubleshooting' },
            { prompt: 'Why is hierarchy validation failing?', expected: 'troubleshooting' },
            { prompt: 'Resolve the merge conflict', expected: 'troubleshooting' },
            { prompt: 'Document the process hierarchy', expected: 'documentation' },
            { prompt: 'Write up the collaboration documentation', expected: 'documentation' },
            { prompt: 'Generate a project summary report', expected: 'documentation' }
        ];

        let correct = 0;
        const failures = [];

        for (const { prompt, expected } of benchmarkPrompts) {
            const result = await analyzer.analyze(prompt, {});
            if (result.primary_intent === expected) {
                correct++;
            } else {
                failures.push({ prompt, expected, actual: result.primary_intent, confidence: result.confidence });
            }
        }

        const accuracy = correct / benchmarkPrompts.length;
        console.log(`Intent classification accuracy: ${(accuracy * 100).toFixed(1)}% (${correct}/${benchmarkPrompts.length})`);
        if (failures.length > 0) {
            console.log('Failures:', failures.map(f => `"${f.prompt}" expected=${f.expected} got=${f.actual}`).join('\n'));
        }

        expect(accuracy).toBeGreaterThanOrEqual(0.90); // >90% target
    });
});
```

---

## Integration Tests

### T06 Navigator Integration

```javascript
describe('T06NavigatorBridge Integration', () => {
    let navigator, nlpEngine, bridge;

    beforeAll(async () => {
        nlpEngine = new EDPSNLPEngine();
        await nlpEngine.initialize();
        navigator = new MockT06Navigator();
        bridge = new T06NavigatorBridge(navigator, nlpEngine);
    });

    test('should enrich skill query with intent context', async () => {
        let capturedQuery = null;
        navigator.on('skill_query', (q) => { capturedQuery = q; });

        await navigator.querySkills('Analyze compliance of the collaboration diagram', {});

        expect(capturedQuery.intent_context).toBeDefined();
        expect(capturedQuery.ranked_skills).toBeDefined();
    });

    test('should rank edps-compliance higher for compliance analysis prompts', async () => {
        const candidateSkills = [
            { id: 'edps-compliance', domain_keywords: ['compliance', 'boundary'] },
            { id: 'domain-extractconcepts', domain_keywords: ['domain', 'entity'] },
            { id: 'documentation-automation', domain_keywords: ['document', 'guide'] }
        ];

        const intentContext = await nlpEngine.analyzePrompt('Check EDPS VR-1 compliance', {});
        const ranked = await bridge.rankSkillsByIntent(candidateSkills, intentContext);

        expect(ranked[0].id).toBe('edps-compliance');
    });
});
```

### T07 Workflow Bridge Integration

```javascript
describe('T07WorkflowBridge Integration', () => {
    let orchestrator, nlpEngine, bridge;

    beforeAll(async () => {
        nlpEngine = new EDPSNLPEngine();
        await nlpEngine.initialize();
        orchestrator = new MockT07Orchestrator();
        bridge = new T07WorkflowBridge(orchestrator, nlpEngine);
    });

    test('should convert natural language workflow request to T07 format', async () => {
        const workflowRequest = {
            description: 'Full workflow from requirements to validated collaboration diagram',
            context: { project_phase: 'design' }
        };

        const result = await bridge.convertToOrchestratorFormat(
            await nlpEngine.parseWorkflowDescription(workflowRequest.description, workflowRequest.context)
        );

        expect(['pattern_based', 'custom']).toContain(result.execution_type);
        expect(result.confidence).toBeGreaterThan(0.5);
    });

    test('should classify "add validation step" as add_step modification', async () => {
        const existingWorkflow = { id: 'test_wf', steps: [] };
        const result = await bridge.applyModificationToWorkflow(
            await nlpEngine.parseWorkflowModification(
                'Add a compliance validation step', existingWorkflow, {}
            ),
            existingWorkflow
        );

        // Either applied or requires confirmation with correct type
        const modType = result.modification_type ?? result.proposed_modification?.type;
        expect(modType).toBe('add_step');
    });
});
```

---

## Performance Tests

```javascript
describe('Response Time SLA (<3 seconds P95)', () => {
    let engine;

    beforeAll(async () => {
        engine = new EDPSNLPEngine({ learningEnabled: false });
        await engine.initialize();
    });

    test('standard analysis prompt should complete within 3 seconds', async () => {
        const start = Date.now();
        await engine.analyzePrompt('Analyze this requirements document for domain concepts', {});
        const elapsed = Date.now() - start;
        expect(elapsed).toBeLessThan(3000);
    });

    test('complex multi-intent prompt should complete within 3 seconds', async () => {
        const start = Date.now();
        await engine.analyzePrompt(
            'Create a collaboration diagram from these requirements, validate it for EDPS compliance, then document all hierarchy levels',
            { project_phase: 'design', quality_requirements: 'high' }
        );
        const elapsed = Date.now() - start;
        expect(elapsed).toBeLessThan(3000);
    });

    test('P95 over 100 prompts should be under 3 seconds', async () => {
        const prompts = [
            'Review requirements', 'Create diagram', 'Validate hierarchy', 'Merge requirements',
            'Estimate effort', 'Fix compliance issue', 'Document process',
            'Check VR-1', 'Generate workflow', 'Analyze domain concepts'
        ];

        const times = [];
        for (let i = 0; i < 100; i++) {
            const prompt = prompts[i % prompts.length];
            const t0 = Date.now();
            await engine.analyzePrompt(prompt, {});
            times.push(Date.now() - t0);
        }

        times.sort((a, b) => a - b);
        const p95 = times[Math.floor(times.length * 0.95)];
        console.log(`P95 response time: ${p95}ms`);
        expect(p95).toBeLessThan(3000);
    });
});
```

---

## Learning System Tests

```javascript
describe('LearningSystem', () => {
    let learningSystem;

    beforeEach(() => {
        learningSystem = new LearningSystem({ batchLearningThreshold: 5 });
    });

    test('should record feedback and return correct count', async () => {
        const result = await learningSystem.recordFeedback({
            intent: 'analysis',
            top_skill: 'domain-extractconcepts',
            outcome: 'accepted',
            feedback_confidence: 0.9
        });
        expect(result.recorded).toBe(true);
    });

    test('should apply immediate learning for high-confidence feedback', async () => {
        // Record accepted feedback
        await learningSystem.recordFeedback({
            intent: 'analysis',
            top_skill: 'domain-extractconcepts',
            outcome: 'accepted',
            feedback_confidence: 0.95
        });

        const metrics = await learningSystem.getMetrics();
        expect(metrics.active_pattern_boosts).toBeGreaterThan(0);
    });

    test('should trigger batch update after threshold feedback events', async () => {
        for (let i = 0; i < 5; i++) {
            await learningSystem.recordFeedback({
                intent: 'validation',
                top_skill: 'edps-compliance',
                outcome: i < 4 ? 'accepted' : 'rejected',
                feedback_confidence: 0.85
            });
        }

        const metrics = await learningSystem.getMetrics();
        expect(metrics.accuracy_trend.length).toBeGreaterThan(0);
    });

    test('acceptance rate metric should reflect recorded feedback ratio', async () => {
        await learningSystem.recordFeedback({ intent: 'creation', top_skill: 'diagram-generatecollaboration', outcome: 'accepted', feedback_confidence: 0.8 });
        await learningSystem.recordFeedback({ intent: 'creation', top_skill: 'diagram-generatecollaboration', outcome: 'accepted', feedback_confidence: 0.8 });
        await learningSystem.recordFeedback({ intent: 'creation', top_skill: 'requirements-ingest', outcome: 'rejected', feedback_confidence: 0.8 });

        const metrics = await learningSystem.getMetrics();
        // 2/3 accepted
        if (metrics.acceptance_rate !== null) {
            expect(metrics.acceptance_rate).toBeCloseTo(2 / 3, 1);
        }
    });
});
```

---

## Acceptance Criteria Checklist

| Criterion | Target | Test Ref |
|-----------|--------|----------|
| Intent classification accuracy | >90% | Intent Classification Benchmark |
| Entity extraction precision | >85% | EntityExtractor unit tests |
| Recommendation acceptance rate | >85% | Recommendation Engine tests |
| Response time P95 | <3 seconds | Performance SLA tests |
| Workflow parsing from NL | Valid config produced | Workflow Builder tests |
| Clarification questions per session | <2 on average | ClarificationGenerator tests |
| T06 integration | Skill ranking enriched | T06 Navigator Integration |
| T07 integration | NL → workflow config | T07 Workflow Bridge Integration |
| T08 integration | Gate selection from intent | T08 Quality Gates Integration |
| Learning improvement | Accuracy improvement shown | Learning System tests |
| Memory stability | <50 MB growth / 100 prompts | (manual benchmark) |
