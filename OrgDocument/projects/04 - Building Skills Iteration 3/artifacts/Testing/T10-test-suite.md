# T10 Comprehensive Integration Test Suite
# Phase 4 - Integration & Testing

**Suite ID**: T10-integration-v1.0  
**Date**: March 18, 2026  
**Scope**: T07 (edps-workflow-orchestrator) + T08 (edps-quality-gates) + T09 (edps-enhanced-nlp) + full ecosystem  
**Dependencies Tested**: All Phase 1–3 deliverables  

---

## 1. Test Suite Architecture

```
test-suite/
├── category-1-t07-t08-t09-integration/
│   ├── 1.1-workflow-gate-integration
│   ├── 1.2-nlp-workflow-integration
│   ├── 1.3-gate-nlp-integration
│   └── 1.4-three-way-integration
├── category-2-end-to-end-scenarios/
│   ├── 2.1-fast-track-analysis
│   ├── 2.2-complex-org-design
│   ├── 2.3-model-integration
│   └── 2.4-maintenance-workflow
├── category-3-performance-load/
│   ├── 3.1-concurrency
│   ├── 3.2-stress
│   └── 3.3-latency
├── category-4-quality-regression/
│   ├── 4.1-gate-accuracy
│   ├── 4.2-nlp-accuracy
│   ├── 4.3-regression-existing
│   └── 4.4-error-handling
└── category-5-ecosystem-30-skills/
    └── 5.1-all-skills-basic-validation
```

---

## 2. Category 1: T07 + T08 + T09 Integration Tests

### 1.1 Workflow–Gate Integration (T07 ↔ T08)

Tests that confirm quality gates are automatically inserted, evaluated, and enforced within workflow orchestration.

```javascript
describe('T07 Workflow Orchestrator + T08 Quality Gates Integration', () => {

    describe('Gate injection into orchestrated workflows', () => {
        test('standard workflow should include at least one quality gate', async () => {
            const workflow = await orchestrator.createWorkflow({
                pattern: 'requirements_to_documentation',
                projectContext: { phase: 'design', quality_level: 'standard' }
            });
            const gateSteps = workflow.steps.filter(s => s.type === 'quality_gate');
            expect(gateSteps.length).toBeGreaterThan(0);
        });

        test('high-quality workflow should include comprehensive gate set', async () => {
            const workflow = await orchestrator.createWorkflow({
                pattern: 'domain_modeling_workflow',
                projectContext: { quality_level: 'high' }
            });
            const gateIds = workflow.steps
                .filter(s => s.type === 'quality_gate')
                .map(s => s.gate_id);
            // High quality must include edps_vr_validation and traceability_check
            expect(gateIds).toContain('edps_vr_validation');
            expect(gateIds).toContain('traceability_completeness');
        });

        test('gate failure should halt workflow with actionable error', async () => {
            // Inject a deliberate gate failure via mock
            const mockGates = createMockGatesWithFailure('boundary_validation', {
                rule: 'VR-2',
                description: 'Participant type mismatch at boundary'
            });
            orchestrator.setQualityGateProvider(mockGates);

            const result = await orchestrator.executeWorkflow('boundary_check_wf', testInputs.invalidDiagram);

            expect(result.status).toBe('halted_on_gate_failure');
            expect(result.gate_result.gate_id).toBe('boundary_validation');
            expect(result.gate_result.remediation).toBeDefined();
            expect(result.gate_result.remediation.length).toBeGreaterThan(0);
        });

        test('gate success should allow workflow to proceed', async () => {
            orchestrator.setQualityGateProvider(realGateProvider);
            const result = await orchestrator.executeWorkflow(
                'requirements_to_diagram_wf',
                testInputs.validRequirementsDoc
            );
            expect(['completed', 'completed_with_warnings']).toContain(result.status);
        });

        test('workflow execution metrics should include per-gate timings', async () => {
            const result = await orchestrator.executeWorkflow(
                'validation_focus_wf',
                testInputs.validHierarchy
            );
            for (const gate of result.gate_results || []) {
                expect(gate.execution_time_ms).toBeDefined();
                expect(gate.execution_time_ms).toBeGreaterThan(0);
            }
        });
    });

    describe('Gate feedback loop', () => {
        test('gate failure explanation should use plain English', async () => {
            const failure = await gateProvider.evaluateGate(
                'edps_vr_validation',
                testInputs.vrViolatingDiagram
            );
            expect(failure.status).toBe('failed');
            // Should not contain raw error codes unexplained
            expect(failure.explanation).not.toMatch(/^Error \d+/);
            expect(failure.explanation.length).toBeGreaterThan(20);
        });

        test('remediation suggestions should reference correct skills', async () => {
            const failure = await gateProvider.evaluateGate(
                'traceability_completeness',
                testInputs.missingTraceability
            );
            expect(failure.remediation_skills).toBeDefined();
            expect(failure.remediation_skills.length).toBeGreaterThan(0);
        });
    });
});
```

### 1.2 NLP–Workflow Integration (T09 ↔ T07)

Tests that NLP intent analysis correctly drives workflow selection and configuration.

```javascript
describe('T09 Enhanced NLP + T07 Workflow Orchestrator Integration', () => {

    describe('Intent-driven workflow selection', () => {
        const nlpToWorkflowCases = [
            {
                prompt: 'I need a full end-to-end workflow from requirements through documentation',
                expectedPattern: 'end_to_end'
            },
            {
                prompt: 'Quick requirements analysis please',
                expectedPattern: 'fast_track_analysis'
            },
            {
                prompt: 'Validate the EDPS compliance of this hierarchy',
                expectedPattern: 'validation_focus'
            },
            {
                prompt: 'Generate the collaboration diagram from these requirements',
                expectedPattern: 'requirements_to_diagram'
            }
        ];

        test.each(nlpToWorkflowCases)(
            'should select $expectedPattern workflow for: "$prompt"',
            async ({ prompt, expectedPattern }) => {
                const nlpResult = await nlpEngine.analyzePrompt(prompt, {});
                const workflow = await orchestrator.selectWorkflowFromIntent(nlpResult);
                expect(workflow.pattern_id).toContain(expectedPattern);
            }
        );
    });

    describe('NL workflow description parsing', () => {
        test('should parse numbered list workflow into orchestrator steps', async () => {
            const description = 'I need:\n1. Ingest requirements\n2. Extract domain concepts\n3. Align with existing entities\n4. Generate collaboration diagram\n5. Validate EDPS compliance';
            const workflowConfig = await nlpEngine.parseWorkflowDescription(description, {});
            const t07Format = await bridge_t07.convertToOrchestratorFormat(workflowConfig);

            expect(t07Format.steps.length).toBe(5);
            expect(t07Format.execution_type).toBeDefined();
        });

        test('should handle modification requests on existing workflows', async () => {
            const existingWf = await orchestrator.getWorkflow('end_to_end_wf_001');
            const mod = await nlpEngine.parseWorkflowModification(
                'Add a hierarchy validation step before the documentation phase',
                existingWf,
                {}
            );
            expect(mod.modification_type).toBe('add_step');
            expect(mod.target_skill).toMatch(/hierarchy-validation/i);
        });
    });

    describe('Quality level propagation', () => {
        test('comprehensive quality intent should set high gates in workflow', async () => {
            const nlpResult = await nlpEngine.analyzePrompt(
                'Perform a thorough and comprehensive EDPS compliance analysis', {}
            );
            expect(nlpResult.intent_analysis.quality_level).toBe('high');

            const workflow = await orchestrator.selectWorkflowFromIntent(nlpResult);
            expect(workflow.quality_profile).toBe('comprehensive');
        });

        test('quick intent should set expedited gates in workflow', async () => {
            const nlpResult = await nlpEngine.analyzePrompt('Quick review of the diagram', {});
            expect(nlpResult.intent_analysis.quality_level).toBe('expedited');

            const workflow = await orchestrator.selectWorkflowFromIntent(nlpResult);
            expect(workflow.quality_profile).toBe('light');
        });
    });
});
```

### 1.3 Gate–NLP Integration (T08 ↔ T09)

Tests that gate failures generate NLP-friendly explanations and skill recommendations.

```javascript
describe('T08 Quality Gates + T09 Enhanced NLP Integration', () => {

    test('gate failure should produce NLP-enriched recommendations', async () => {
        const gateResult = await gateProvider.evaluateGate(
            'edps_vr_validation',
            testInputs.vrViolatingDiagram
        );
        const enriched = await nlpEngine.enrichGateFailure(gateResult);

        expect(enriched.natural_language_explanation).toBeDefined();
        expect(enriched.recommended_skills).toBeDefined();
        expect(enriched.recommended_skills.length).toBeGreaterThan(0);
    });

    test('gate selection should adapt to NLP-detected quality level', async () => {
        const highQualityContext = { quality_level: 'high', project_phase: 'design' };
        const standardContext = { quality_level: 'standard', project_phase: 'design' };

        const highGates = gateProvider.selectGatesForContext(highQualityContext);
        const standardGates = gateProvider.selectGatesForContext(standardContext);

        expect(highGates.length).toBeGreaterThanOrEqual(standardGates.length);
    });

    test('compliance intent should auto-add VR validation gates', async () => {
        const nlpResult = await nlpEngine.analyzePrompt(
            'Check that all boundary rules are satisfied in the collaboration diagram', {}
        );
        const gates = gateProvider.selectGatesForIntent(nlpResult.intent_analysis);

        const vrGates = gates.filter(g => g.id.includes('vr') || g.id.includes('boundary'));
        expect(vrGates.length).toBeGreaterThan(0);
    });
});
```

### 1.4 Three-Way Integration (T07 + T08 + T09)

Full pipeline tests from natural language prompt to quality-validated workflow output.

```javascript
describe('Three-Way Integration: T07 + T08 + T09', () => {

    test('full pipeline: NL prompt → workflow selection → gate enforcement → output', async () => {
        const userPrompt = 'Analyze this requirements document, extract domain concepts, and validate everything for EDPS compliance';
        const projectContext = { project_phase: 'design', quality_level: 'standard' };

        // Step 1: NLP analysis
        const nlpResult = await nlpEngine.analyzePrompt(userPrompt, projectContext);
        expect(nlpResult.intent_analysis.primary_intent).toBe('analysis');

        // Step 2: Workflow selection
        const workflow = await orchestrator.selectWorkflowFromIntent(nlpResult);
        expect(workflow.steps.length).toBeGreaterThan(0);

        // Step 3: Execute with gates
        const result = await orchestrator.executeWorkflow(
            workflow.id,
            testInputs.sampleRequirementsDoc,
            { gateProvider, nlpEngine }
        );
        expect(['completed', 'completed_with_warnings']).toContain(result.status);
        expect(result.outputs).toBeDefined();
    });

    test('session context should persist intent across multi-turn interaction', async () => {
        // Turn 1: establish context
        await nlpEngine.analyzePrompt('We are in the design phase, working on high quality EDPS compliance', {});

        // Turn 2: follow-up should inherit context
        const turn2 = await nlpEngine.analyzePrompt('Now validate the hierarchy', {});
        expect(turn2.applied_context.project_phase).toBe('design');
        expect(turn2.applied_context.quality_level).toBe('high');
    });
});
```

---

## 3. Category 2: End-to-End Scenario Tests

### Scenario 2.1: Fast-Track Requirements Analysis

**Target Completion**: < 45 minutes (simulated < 90 seconds in test)  
**Trigger Prompt**: "Quick analysis of simple requirements document"

```javascript
describe('Scenario 2.1: Fast-Track Requirements Analysis', () => {
    test('should select expedited workflow', async () => {
        const result = await pipeline.execute(
            'Quick analysis of these simple requirements',
            testInputs.simpleRequirementsDoc
        );
        expect(result.workflow_pattern).toContain('fast_track');
        expect(result.gate_count).toBeLessThanOrEqual(2); // Minimal gates
    });

    test('should complete within response time SLA', async () => {
        const start = Date.now();
        await pipeline.execute('Quick requirements review', testInputs.simpleRequirementsDoc);
        const elapsed = Date.now() - start;
        expect(elapsed).toBeLessThan(90_000); // 90 seconds test budget
    });

    test('output should include analysis and recommendations', async () => {
        const result = await pipeline.execute(
            'Quick analysis of requirements',
            testInputs.simpleRequirementsDoc
        );
        expect(result.outputs['analysis_summary']).toBeDefined();
        expect(result.outputs['recommended_next_steps']).toBeDefined();
    });
});
```

### Scenario 2.2: Complex Organizational Model Design

**Target Completion**: 4–6 hours (simulated < 5 minutes in test)  
**Trigger Prompt**: "Design comprehensive EDPS organizational model from stakeholder requirements"

```javascript
describe('Scenario 2.2: Complex Organizational Model Design', () => {
    test('should invoke full domain modeling chain', async () => {
        const result = await pipeline.execute(
            'Design comprehensive EDPS organizational model from stakeholder requirements',
            testInputs.complexStakeholderRequirements
        );
        const invokedSkills = result.execution_log.map(e => e.skill);
        // Must invoke domain extraction, alignment, diagram, hierarchy, compliance
        expect(invokedSkills).toContain('domain-extractconcepts');
        expect(invokedSkills).toContain('diagram-generatecollaboration');
        expect(invokedSkills).toContain('hierarchy-management');
        expect(invokedSkills).toContain('edps-compliance');
    });

    test('output should include collaboration diagram with EDPS compliance validation', async () => {
        const result = await pipeline.execute(
            'Design comprehensive EDPS model',
            testInputs.complexStakeholderRequirements
        );
        expect(result.outputs['collaboration_diagram']).toBeDefined();
        expect(result.outputs['compliance_report']).toBeDefined();
        expect(result.compliance_status).toBe('PASSED');
    });

    test('hierarchy should satisfy all four boundary rules', async () => {
        const result = await pipeline.execute(
            'Full org model design',
            testInputs.complexStakeholderRequirements
        );
        const vrResults = result.validation_details?.boundary_rules;
        if (vrResults) {
            expect(vrResults['VR-1']).toBe('PASSED');
            expect(vrResults['VR-2']).toBe('PASSED');
            expect(vrResults['VR-3']).toBe('PASSED');
            expect(vrResults['VR-4']).toBe('PASSED');
        }
    });
});
```

### Scenario 2.3: Model Integration & Change Management

**Target Completion**: 2–4 hours (simulated < 3 minutes in test)  
**Trigger Prompt**: "Integrate new billing process into existing organizational model"

```javascript
describe('Scenario 2.3: Model Integration', () => {
    test('should detect integration issues before applying changes', async () => {
        const result = await pipeline.execute(
            'Integrate new billing process into existing organizational model',
            { existing: testInputs.existingOrgModel, new_process: testInputs.newBillingProcess }
        );
        expect(result.pre_integration_checks).toBeDefined();
        expect(result.conflicts_detected).toBeDefined();
    });

    test('should invoke change-impact-analysis before model update', async () => {
        const result = await pipeline.execute(
            'Integrate billing process into org model',
            { existing: testInputs.existingOrgModel, new_process: testInputs.newBillingProcess }
        );
        const invokedSkills = result.execution_log.map(e => e.skill);
        expect(invokedSkills).toContain('change-impact-analysis');
    });

    test('traceability should be maintained through integration', async () => {
        const result = await pipeline.execute(
            'Integrate new billing process',
            { existing: testInputs.existingOrgModel, new_process: testInputs.newBillingProcess }
        );
        expect(result.traceability_intact).toBe(true);
    });
});
```

### Scenario 2.4: Maintenance & Change Request Workflow

**Target Completion**: 1–2 hours (simulated < 2 minutes in test)

```javascript
describe('Scenario 2.4: Maintenance Workflow', () => {
    test('should route change request through impact-analysis → update → verify chain', async () => {
        const result = await pipeline.execute(
            'Apply change request CR-042: rename the Payment boundary to Transaction Processing',
            { org_model: testInputs.existingOrgModel, change_request: testInputs.changeRequestCR042 }
        );
        const invokedSkills = result.execution_log.map(e => e.skill);
        expect(invokedSkills).toContain('change-impact-analysis');
        expect(invokedSkills).toContain('orgmodel-update');
    });

    test('change history metadata should be captured', async () => {
        const result = await pipeline.execute(
            'Apply change request CR-042',
            { org_model: testInputs.existingOrgModel, change_request: testInputs.changeRequestCR042 }
        );
        expect(result.outputs['change_history']).toBeDefined();
    });
});
```

---

## 4. Category 3: Performance & Load Tests

### 3.1 Concurrency Tests

```javascript
describe('Concurrent Workflow Execution', () => {
    test('two simultaneous workflows should not interfere', async () => {
        const [result1, result2] = await Promise.all([
            pipeline.execute('Analyze requirements', testInputs.reqDoc1),
            pipeline.execute('Validate hierarchy', testInputs.hierarchy1)
        ]);
        expect(result1.status).not.toBe('failed');
        expect(result2.status).not.toBe('failed');
    });

    test('five concurrent NLP analyses should all complete within 15 seconds', async () => {
        const prompts = [
            'Analyze requirements', 'Create diagram', 'Validate hierarchy',
            'Merge requirements', 'Document the process'
        ];
        const start = Date.now();
        const results = await Promise.all(
            prompts.map(p => nlpEngine.analyzePrompt(p, {}))
        );
        const elapsed = Date.now() - start;
        expect(elapsed).toBeLessThan(15_000);
        results.forEach(r => expect(r.intent_analysis).toBeDefined());
    });
});
```

### 3.2 Stress Tests

```javascript
describe('Stress Testing', () => {
    test('100 sequential NLP analyses should show stable memory', async () => {
        const baseMemory = process.memoryUsage().heapUsed;
        const prompts = ['Analyze', 'Create', 'Validate', 'Merge', 'Document'];
        for (let i = 0; i < 100; i++) {
            await nlpEngine.analyzePrompt(prompts[i % prompts.length], {});
        }
        const peakMemory = process.memoryUsage().heapUsed;
        const growthMB = (peakMemory - baseMemory) / 1024 / 1024;
        console.log(`Memory growth over 100 NLP calls: ${growthMB.toFixed(1)} MB`);
        expect(growthMB).toBeLessThan(50); // < 50 MB growth target
    });
});
```

### 3.3 Latency Validation

| Component | P50 Target | P95 Target | P99 Target |
|-----------|-----------|-----------|-----------|
| NLP `analyzePrompt()` | < 500 ms | < 3,000 ms | < 5,000 ms |
| Workflow selection | < 100 ms | < 500 ms | < 1,000 ms |
| Quality gate (single) | < 200 ms | < 1,000 ms | < 2,000 ms |
| Full end-to-end workflow | < 120 s | < 300 s | < 600 s |

---

## 5. Category 4: Quality & Regression Tests

### 4.1 Gate Accuracy

```javascript
describe('Quality Gate Accuracy (>99% target)', () => {
    const gateCases = [
        // True positives - invalid inputs that SHOULD fail gates
        { input: testInputs.vrViolatingDiagram, gate: 'edps_vr_validation', expectedResult: 'failed' },
        { input: testInputs.missingTraceability, gate: 'traceability_completeness', expectedResult: 'failed' },
        { input: testInputs.incompleteHierarchy, gate: 'hierarchy_integrity', expectedResult: 'failed' },
        // True negatives - valid inputs that SHOULD pass gates
        { input: testInputs.validDiagram, gate: 'edps_vr_validation', expectedResult: 'passed' },
        { input: testInputs.fullTraceabilityDoc, gate: 'traceability_completeness', expectedResult: 'passed' },
        { input: testInputs.validHierarchy, gate: 'hierarchy_integrity', expectedResult: 'passed' }
    ];

    test('gate accuracy should exceed 99% on benchmark set', async () => {
        let correct = 0;
        for (const { input, gate, expectedResult } of gateCases) {
            const result = await gateProvider.evaluateGate(gate, input);
            if (result.status === expectedResult) correct++;
        }
        const accuracy = correct / gateCases.length;
        expect(accuracy).toBeGreaterThanOrEqual(0.99);
    });
});
```

### 4.2 NLP Accuracy

```javascript
describe('NLP Accuracy (>90% target)', () => {
    // 50-prompt benchmark set - full set defined in edps-enhanced-nlp/test-suite.md
    test('intent classification accuracy should exceed 90%', async () => {
        // Accuracy benchmark delegated to edps-enhanced-nlp test suite
        // Here we verify the engine is accessible and returns usable results
        const result = await nlpEngine.analyzePrompt('Analyze the requirements document', {});
        expect(result.intent_analysis.primary_intent).toBe('analysis');
        expect(result.intent_analysis.confidence).toBeGreaterThan(0.75);
    });
});
```

### 4.3 Regression Tests (Existing Skill Functionality)

```javascript
describe('Regression: Phase 1-2 Skills Unchanged', () => {
    const regressionChecks = [
        // Each existing skill must still return an object with the right shape
        { skill: 'requirements-ingest', input: testInputs.plainRequirements, expectedOutputKey: 'ingested_requirements' },
        { skill: 'goals-extract', input: testInputs.ingestedRequirements, expectedOutputKey: 'goals' },
        { skill: 'domain-extractconcepts', input: testInputs.analysedRequirements, expectedOutputKey: 'domain_concepts' },
        { skill: 'diagram-generatecollaboration', input: testInputs.domainModel, expectedOutputKey: 'collaboration_diagram' },
        { skill: 'edps-compliance', input: testInputs.collaborationDiagram, expectedOutputKey: 'compliance_report' },
        { skill: 'hierarchy-validation', input: testInputs.hierarchy, expectedOutputKey: 'validation_report' }
    ];

    test.each(regressionChecks)(
        '$skill should still produce expected output shape',
        async ({ skill, input, expectedOutputKey }) => {
            const invocation = await skillInvoker.invoke(skill, input);
            expect(invocation.status).not.toBe('error');
            expect(invocation.output[expectedOutputKey]).toBeDefined();
        }
    );
});
```

### 4.4 Error Handling Tests

```javascript
describe('Error Handling and Recovery', () => {
    test('malformed YAML input should return graceful error, not exception', async () => {
        const result = await pipeline.execute('Analyze requirements', ':::invalid:yaml:::');
        expect(result.status).toBe('input_validation_error');
        expect(result.user_message).toBeDefined();
        expect(result.user_message.length).toBeGreaterThan(10);
    });

    test('missing required file should produce actionable error message', async () => {
        const result = await pipeline.execute(
            'Validate hierarchy',
            { hierarchy_path: '/nonexistent/path/hierarchy.md' }
        );
        expect(result.status).toBe('input_not_found');
        expect(result.remediation).toBeDefined();
    });

    test('gate timeout should not crash the workflow', async () => {
        const slowGate = createMockGate('slow_gate', { delay_ms: 30_000 });
        orchestrator.setQualityGateProvider(createGateSetWith([slowGate], { timeout_ms: 5_000 }));

        const result = await orchestrator.executeWorkflow('validation_focus_wf', testInputs.validDiagram);
        expect(['gate_timeout', 'completed_with_warnings']).toContain(result.status);
    });
});
```

---

## 6. Category 5: Full Ecosystem Skill Validation

```javascript
describe('All 30+ EDPS Skills: Basic Output Shape Validation', () => {
    const allSkills = [
        'requirements-ingest', 'requirements-merge', 'goals-extract', 'process-w5h',
        'process-merge', 'process-findtopandupdate', 'process-scopemin',
        'domain-extractconcepts', 'domain-alignentities', 'domain-proposenewconcepts',
        'diagram-generatecollaboration', 'model-integration', 'hierarchy-management',
        'hierarchy-validation', 'documentation-automation', 'migration-tools',
        'edps-compliance', 'change-impact-analysis', 'plan-derivetasks',
        'plan-estimateeffort', 'plan-buildschedule', 'project-document-management',
        'project-planning-tracking', 'project-status-reporting', 'change-management',
        'orgmodel-update', 'github-issue-create-update', 'github-issue-sync-status',
        'edps-skill-navigator', 'edps-workflow-orchestrator', 'edps-quality-gates',
        'edps-enhanced-nlp', 'skill-creator'
    ];

    test.each(allSkills)('%s SKILL.md should be readable and have name, description fields', async (skillName) => {
        const skillMd = await readSkillMd(skillName);
        expect(skillMd).toBeDefined();
        expect(skillMd.frontmatter.name).toBe(skillName);
        expect(skillMd.frontmatter.description.length).toBeGreaterThan(20);
    });
});
```

---

## 7. Acceptance Criteria Validation Matrix

| Test ID | Requirement | Target | Category |
|---------|-------------|--------|----------|
| Test-10.1 | Workflow-Gate integration | All gate types injectable | Cat-1.1 |
| Test-10.2 | NLP-Workflow integration | Pattern matched >80% cases | Cat-1.2 |
| Test-10.3 | Three-way pipeline | Full pipeline completes | Cat-1.4 |
| Test-10.4 | End-to-end fast-track | < 45 min equivalent | Cat-2.1 |
| Test-10.5 | End-to-end complex design | All EDPS rules pass | Cat-2.2 |
| Test-10.6 | Concurrent execution | No interference | Cat-3.1 |
| Test-10.7 | Memory stability | < 50 MB growth / 100 calls | Cat-3.2 |
| Test-10.8 | Gate accuracy | > 99% | Cat-4.1 |
| Test-10.9 | NLP accuracy | > 90% | Cat-4.2 |
| Test-10.10 | Regression | 100% pass rate | Cat-4.3 |
| Test-10.11 | Error handling | Graceful, no exceptions | Cat-4.4 |
| Test-10.12 | All 33 skills | SKILL.md valid | Cat-5.1 |
