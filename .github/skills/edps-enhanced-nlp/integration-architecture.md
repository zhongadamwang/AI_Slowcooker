# EDPS Enhanced NLP - Integration Architecture

## Overview

This document describes how T09 Enhanced NLP integrates with the existing EDPS ecosystem — specifically the T06 skill navigator, T07 workflow orchestrator, and T08 quality gates — to provide a seamless natural language experience across all EDPS skill interactions.

## Integration Map

```
┌─────────────────────────────────────────────────────────┐
│                    User Prompt Input                    │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              T09 EDPS Enhanced NLP Engine               │
│                                                         │
│  ┌──────────────┐  ┌─────────────────┐  ┌───────────┐  │
│  │ Intent       │  │ Entity          │  │ Context   │  │
│  │ Analyzer     │  │ Extractor       │  │ Builder   │  │
│  └──────┬───────┘  └────────┬────────┘  └─────┬─────┘  │
│         │                  │                  │         │
│         └──────────────────┴──────────────────┘         │
│                            │                            │
│                  ┌─────────▼──────────┐                 │
│                  │  Recommendation    │                 │
│                  │  Engine            │                 │
│                  └─────────┬──────────┘                 │
│                            │                            │
│         ┌──────────────────┼──────────────────┐         │
│         ▼                  ▼                  ▼         │
│  ┌──────────────┐  ┌─────────────────┐  ┌───────────┐  │
│  │ T06          │  │ T07             │  │ T08       │  │
│  │ Navigator    │  │ Orchestrator    │  │ Quality   │  │
│  │ Integration  │  │ Integration     │  │ Gates     │  │
│  └──────────────┘  └─────────────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 1. T06 Skill Navigator Integration

T09 builds directly upon the T06 enhanced navigation framework, extending its foundational NLP capabilities with advanced multi-modal intent analysis and entity extraction.

### Integration Interface

```javascript
/**
 * T09 ↔ T06 Navigation Bridge
 * Extends T06's skill discovery with intent-driven filtering and ranking
 */
export class T06NavigatorBridge {
    constructor(navigator, nlpEngine) {
        this.navigator = navigator;
        this.nlpEngine = nlpEngine;
        this.setupSkillDiscoveryHooks();
    }

    setupSkillDiscoveryHooks() {
        // Hook into T06's skill discovery pipeline
        this.navigator.on('skill_query', async (query) => {
            // Enhance query with NLP intent analysis
            const intentContext = await this.nlpEngine.analyzePrompt(query.user_input);
            
            return {
                ...query,
                intent_context: intentContext,
                ranked_skills: await this.rankSkillsByIntent(
                    query.candidate_skills,
                    intentContext
                )
            };
        });

        // Hook into T06's skill recommendation output
        this.navigator.on('recommendations_ready', async (recommendations) => {
            // Enrich recommendations with NLP explanations
            return {
                ...recommendations,
                nlp_explanations: await this.generateRecommendationExplanations(recommendations)
            };
        });
    }

    async rankSkillsByIntent(candidateSkills, intentContext) {
        const rankedSkills = [];

        for (const skill of candidateSkills) {
            const intentAlignment = this.calculateIntentAlignment(skill, intentContext);
            const entityRelevance = this.calculateEntityRelevance(skill, intentContext.entities);
            const contextFit = this.calculateContextFit(skill, intentContext.context_applied);

            rankedSkills.push({
                ...skill,
                nlp_scores: {
                    intent_alignment: intentAlignment,
                    entity_relevance: entityRelevance,
                    context_fit: contextFit,
                    overall: (intentAlignment * 0.5) + (entityRelevance * 0.3) + (contextFit * 0.2)
                }
            });
        }

        return rankedSkills.sort((a, b) => b.nlp_scores.overall - a.nlp_scores.overall);
    }

    calculateIntentAlignment(skill, intentContext) {
        // Check if skill appears in matched sub-category recommendations
        for (const sub of intentContext.intent.matched_subcategories) {
            if (sub.recommended_skills?.includes(skill.id)) {
                return sub.score;
            }
        }
        return 0.3; // Base score for non-matched skills
    }

    calculateEntityRelevance(skill, entities) {
        // Check if skill was explicitly mentioned in user prompt
        if (entities.skills_mentioned?.some(s =>
            s.toLowerCase().includes(skill.id.toLowerCase()))) {
            return 1.0;
        }

        // Check skill relevance to extracted domain entities
        const domainComponents = entities.edps_components ?? [];
        const relevant = domainComponents.some(entity =>
            skill.domain_keywords?.some(kw =>
                entity.value.toLowerCase().includes(kw.toLowerCase())
            )
        );
        return relevant ? 0.7 : 0.4;
    }

    calculateContextFit(skill, contextFactors) {
        // Default fit — could be enhanced with project history
        return 0.6;
    }

    async generateRecommendationExplanations(recommendations) {
        return recommendations.skills.map(rec => ({
            skill_id: rec.skill_id,
            explanation: this.buildExplanation(rec),
            confidence_rationale: this.buildConfidenceRationale(rec)
        }));
    }

    buildExplanation(recommendation) {
        const reasons = [];
        if (recommendation.explicitly_mentioned) {
            reasons.push('You specifically mentioned this skill');
        }
        if (recommendation.phase_boosted) {
            reasons.push('Highly relevant to your current project phase');
        }
        if (recommendation.historically_successful) {
            reasons.push('Delivered good results in similar past scenarios');
        }
        reasons.push(recommendation.reason || 'Matches your intent');
        return reasons.join('. ');
    }

    buildConfidenceRationale(recommendation) {
        const confidence = recommendation.confidence ?? 0;
        if (confidence > 0.85) return 'High confidence based on clear intent match';
        if (confidence > 0.70) return 'Good match with moderate confidence';
        return 'Possible match — consider reviewing alternatives';
    }
}
```

### T06 Enhancement Points
- **Natural Language Query Processing**: T09 pre-processes user queries before T06 skill discovery
- **Intent-Aware Ranking**: T06's candidate list is re-ranked using T09's intent scores
- **Recommendation Explanations**: T09 adds natural language explanations to T06's recommendations
- **Context Propagation**: T09 project context enriches T06's skill selection criteria

## 2. T07 Workflow Orchestrator Integration

T09 provides the natural language interface for T07's workflow execution, translating user descriptions into workflow configurations and providing intelligent workflow recommendations.

### Integration Interface

```javascript
/**
 * T09 ↔ T07 Workflow Integration Bridge
 * Translates natural language workflow descriptions into T07-executable configurations
 */
export class T07WorkflowBridge {
    constructor(orchestrator, nlpEngine) {
        this.orchestrator = orchestrator;
        this.nlpEngine = nlpEngine;
        this.setupWorkflowHooks();
    }

    setupWorkflowHooks() {
        // Hook into T07's workflow selection pipeline
        this.orchestrator.on('natural_language_workflow_request', async (request) => {
            const workflowSpec = await this.nlpEngine.parseWorkflowDescription(
                request.description,
                request.context
            );
            return await this.convertToOrchestratorFormat(workflowSpec);
        });

        // Hook into workflow modification requests
        this.orchestrator.on('workflow_modification_request', async (request) => {
            const modSpec = await this.nlpEngine.parseWorkflowModification(
                request.modification_text,
                request.existing_workflow,
                request.context
            );
            return await this.applyModificationToWorkflow(modSpec, request.existing_workflow);
        });

        // Provide NLP context for workflow adaptation decisions
        this.orchestrator.on('workflow_adaptation_needed', async (context) => {
            const adaptationSuggestions = await this.generateAdaptationSuggestions(context);
            return adaptationSuggestions;
        });
    }

    async convertToOrchestratorFormat(workflowSpec) {
        if (workflowSpec.type === 'pattern_match') {
            // Use matched pattern IDs directly from T07's pattern library
            const patterns = await this.orchestrator.getWorkflowPatterns(workflowSpec.workflow_ids);
            return {
                execution_type: 'pattern_based',
                workflow_patterns: patterns,
                customizations: workflowSpec.components,
                confidence: workflowSpec.confidence,
                ready_for_execution: true,
                nlp_metadata: {
                    pattern_matched: workflowSpec.pattern_id,
                    match_confidence: workflowSpec.confidence
                }
            };
        } else {
            // Custom workflow built from skill sequence
            return {
                execution_type: 'custom',
                skill_sequence: workflowSpec.skill_sequence,
                components: workflowSpec.components,
                confidence: workflowSpec.confidence,
                ready_for_execution: !workflowSpec.needs_review,
                needs_review: workflowSpec.needs_review,
                nlp_metadata: {
                    built_from_description: true,
                    assembly_confidence: workflowSpec.confidence
                }
            };
        }
    }

    async applyModificationToWorkflow(modSpec, existingWorkflow) {
        const modification = {
            type: modSpec.modification_type,
            target_workflow: existingWorkflow,
            change_details: modSpec.change_details,
            confidence: modSpec.confidence
        };

        if (modSpec.confidence > 0.8 && !modSpec.needs_validation) {
            // High confidence: apply directly
            return await this.orchestrator.applyWorkflowModification(modification);
        } else {
            // Lower confidence: return proposed change for confirmation
            return {
                proposed_modification: modification,
                requires_confirmation: true,
                confidence: modSpec.confidence,
                suggested_confirmation_question: this.buildConfirmationQuestion(modSpec)
            };
        }
    }

    async generateAdaptationSuggestions(context) {
        const { failure_reason, current_step, workflow_context } = context;

        // Use NLP to interpret the failure and suggest natural language alternatives
        const failureAnalysis = await this.nlpEngine.analyzePrompt(
            `Fix or adapt: ${failure_reason}`,
            workflow_context
        );

        return {
            nlp_interpretation: failureAnalysis,
            suggested_alternatives: failureAnalysis.recommendations.skills.slice(0, 3).map(s => ({
                skill_id: s.skill_id,
                adaptation_description: `Use ${s.skill_id} as alternative`,
                confidence: s.confidence
            }))
        };
    }

    buildConfirmationQuestion(modSpec) {
        const type = modSpec.modification_type;
        const templates = {
            add_step: `Add a new step to the workflow based on: "${modSpec.change_description}"?`,
            remove_step: `Remove the identified step as requested?`,
            change_quality: `Adjust the quality level as specified?`,
            add_constraint: `Add the described constraint to the workflow?`,
            change_sequence: `Reorder the workflow steps as requested?`,
            general_change: `Apply the described workflow modification?`
        };
        return templates[type] ?? `Apply workflow change: "${modSpec.change_description}"?`;
    }
}
```

### T07 Enhancement Points
- **Natural Language Workflow Specification**: Users describe workflows in natural language; T09 converts to T07 configurations
- **Intent-Driven Pattern Selection**: T09 intent scores guide T07's workflow pattern selection
- **Adaptation Language Generation**: T09 generates natural language explanations for T07 workflow adaptations
- **Modification Parsing**: T09 parses modification requests and converts to T07 modification operations

## 3. T08 Quality Gates Integration

T09 works with T08 to recommend appropriate quality gates based on inferred quality requirements and to surface gate failures in natural language explanations.

### Integration Interface

```javascript
/**
 * T09 ↔ T08 Quality Gates Integration Bridge
 * Provides NLP-driven gate selection and natural language failure explanations
 */
export class T08QualityGatesBridge {
    constructor(gateSystem, nlpEngine) {
        this.gateSystem = gateSystem;
        this.nlpEngine = nlpEngine;
        this.setupGateHooks();
    }

    setupGateHooks() {
        // Map quality level from NLP analysis to gate configuration
        this.nlpEngine.on('prompt_analyzed', async (result) => {
            const gateConfig = await this.selectGatesForIntent(result);
            result.recommended_gates = gateConfig;
        });

        // Translate gate failures to natural language guidance
        this.gateSystem.on('gate_failure', async (gateFailure) => {
            const naturalLanguageExplanation = await this.explainGateFailure(gateFailure);
            gateFailure.natural_language_explanation = naturalLanguageExplanation;
        });
    }

    async selectGatesForIntent(intentAnalysis) {
        const lib = this.nlpEngine._patternLibrary?.contextual_adaptors?.quality_level_adaptations;
        const qualityLevel = intentAnalysis.intent?.quality_level ?? 'standard';
        
        const gateConfig = lib?.[qualityLevel] ?? {
            recommended_gates: ['content_completeness_gate', 'format_validation_gate'],
            workflow_modifiers: []
        };

        // Override for compliance-focused intents
        if (intentAnalysis.intent?.primary_intent === 'validation') {
            gateConfig.recommended_gates = [
                ...new Set([
                    ...gateConfig.recommended_gates,
                    'vr1_boundary_compliance_gate',
                    'vr2_participant_classification_gate'
                ])
            ];
        }

        return {
            gates: gateConfig.recommended_gates,
            reason: `Quality level "${qualityLevel}" with intent "${intentAnalysis.intent?.primary_intent}"`,
            workflow_modifiers: gateConfig.workflow_modifiers
        };
    }

    async explainGateFailure(gateFailure) {
        const { gate_id, validation_results, remediation } = gateFailure;

        const gateName = gate_id.replace(/_gate$/, '').replace(/_/g, ' ');
        const failures = validation_results?.filter(r => !r.passed) ?? [];

        const explanationParts = [
            `The ${gateName} validation did not pass.`
        ];

        for (const failure of failures.slice(0, 3)) {
            explanationParts.push(`— ${failure.rule_id?.replace(/_/g, ' ')}: ${failure.details?.message ?? 'Rule not satisfied'}`);
        }

        if (remediation?.recommendations?.length > 0) {
            explanationParts.push('\nSuggested fixes:');
            for (const rec of remediation.recommendations.slice(0, 2)) {
                explanationParts.push(`• ${rec.description ?? rec.type}`);
            }
        }

        return explanationParts.join('\n');
    }
}
```

### T08 Enhancement Points
- **Quality-Level Gate Selection**: T09's quality level inference drives T08 gate selection
- **Intent-Based Gate Tailoring**: Compliance intents trigger mandatory EDPS validation gates
- **Natural Language Failure Explanations**: T09 converts T08 technical failures to plain English guidance
- **Clarification on Gate Failure**: T09 generates targeted questions when gate failure indicates unclear scope

## 4. Copilot Chat Integration

T09 exposes itself as a skill that Copilot invokes naturally when processing user prompts in VS Code.

### Invocation Pattern

```markdown
## When T09 is invoked

T09 activates whenever a user prompt is sent in the Copilot chat with @workspace and the 
request semantically relates to EDPS tasks. It runs transparently before skill selection 
to enrich the context passed to T06/T07/T08.

### Transparent Enhancement Mode
Most users never directly address T09. Instead, T09 operates transparently:

1. User types: "@workspace analyze my requirements document for domain concepts"
2. T09 intercepts and classifies: intent=analysis, sub=domain_analysis, quality=standard
3. T09 recommends: domain-extractconcepts (0.95), domain-alignentities (0.80)
4. T06 receives intent-enriched query and presents ranked recommendations
5. User selects and workflow proceeds with T07/T08 integration

### Explicit NLP Mode
Users can also directly request NLP assistance:

"@workspace What skills should I use for [task]?"
"@workspace Build me a workflow that [description]"
"@workspace I need to [natural language goal]"
```

### Response Format

```javascript
// T09 enriches every skill execution context with NLP metadata
const enrichedContext = {
    original_prompt: userPrompt,
    nlp_analysis: {
        intent: {
            primary: 'analysis',
            confidence: 0.92,
            quality_level: 'standard',
            urgency: 'medium'
        },
        entities: {
            domain: ['requirements document', 'domain concepts'],
            skills_mentioned: [],
            constraints: []
        },
        recommendations: {
            skills: [
                { skill_id: 'domain-extractconcepts', confidence: 0.95 },
                { skill_id: 'domain-alignentities', confidence: 0.80 }
            ],
            workflows: ['domain_modeling_workflow']
        },
        clarifications: [], // Empty = intent was clear
        analysis_time_ms: 245
    }
};
```

## 5. Context Persistence and Session Continuity

T09 maintains conversation context across multi-turn interactions within a session.

### Session Context Manager

```javascript
export class SessionContextManager {
    constructor() {
        this.sessions = new Map();
        this.sessionTimeout = 30 * 60 * 1000; // 30 minutes
    }

    getOrCreateSession(sessionId) {
        if (!this.sessions.has(sessionId)) {
            this.sessions.set(sessionId, {
                id: sessionId,
                created: Date.now(),
                last_activity: Date.now(),
                interaction_history: [],
                accumulated_context: {
                    project_phase: null,
                    quality_level: 'standard',
                    established_entities: [],
                    used_skills: [],
                    workflow_in_progress: null
                }
            });
        }
        return this.sessions.get(sessionId);
    }

    updateSession(sessionId, analysisResult) {
        const session = this.getOrCreateSession(sessionId);
        session.last_activity = Date.now();
        session.interaction_history.push({
            timestamp: Date.now(),
            intent: analysisResult.intent.primary_intent,
            skills_used: analysisResult.recommendations.skills.map(s => s.skill_id)
        });

        // Accumulate context across turns
        const acc = session.accumulated_context;

        // Lock in project phase once identified
        if (!acc.project_phase && analysisResult.intent.project_phase) {
            acc.project_phase = analysisResult.intent.project_phase;
        }

        // Track quality level changes
        if (analysisResult.intent.quality_level !== 'standard') {
            acc.quality_level = analysisResult.intent.quality_level;
        }

        // Accumulate referenced entities
        for (const entity of analysisResult.entities.all ?? []) {
            if (!acc.established_entities.some(e => e.value === entity.value)) {
                acc.established_entities.push(entity);
            }
        }

        // Track skill usage
        for (const skill of analysisResult.recommendations.skills) {
            if (!acc.used_skills.includes(skill.skill_id)) {
                acc.used_skills.push(skill.skill_id);
            }
        }
    }

    getAccumulatedContext(sessionId) {
        const session = this.sessions.get(sessionId);
        if (!session) return {};

        // Expire old sessions
        if (Date.now() - session.last_activity > this.sessionTimeout) {
            this.sessions.delete(sessionId);
            return {};
        }

        return session.accumulated_context;
    }
}
```

## Performance Characteristics

| Metric | Target | Implementation Strategy |
|--------|--------|------------------------|
| Response Time (P95) | < 3 seconds | Parallel intent+entity analysis; pre-compiled regex patterns |
| Intent Accuracy | > 90% | Comprehensive pattern library; contextual adaptations; learning system |
| Entity Precision | > 85% | Domain-specific patterns; deduplication; confidence thresholds |
| Recommendation Acceptance | > 85% | Multi-factor scoring; historical learning; context adaptation |
| Memory Footprint | < 50 MB | Pre-compiled patterns; bounded history; session expiry |
| Clarification Rate | < 20% of prompts | High-coverage patterns; strong defaults; context accumulation |

## Deployment Requirements

- **Node.js**: 18+ (ES Modules support required)
- **Dependencies**: `fs-extra` for pattern library loading; no heavy NLP framework needed (pure regex + heuristics)
- **Integration**: Must be initialized before T06/T07/T08 skill invocations in the Copilot extension host
- **Configuration**: Pattern library path, confidence thresholds, and T06/T07/T08 integration references configurable via `EDPSNLPEngine` constructor options
