---
name: edps-enhanced-nlp
description: Enhanced natural language processing capabilities for the EDPS skill system providing advanced user intent recognition, contextual understanding, and intelligent skill recommendation. Implements multi-modal pattern recognition, entity extraction, context-aware recommendations, and natural language workflow specification. Builds upon the edps-skill-navigator foundation to create sophisticated pattern recognition that understands complex user requests and business contexts.
license: MIT
---

# EDPS Enhanced NLP - Advanced User Prompt Pattern Recognition

An intelligent natural language processing system that understands complex user requests in the context of EDPS methodology, providing accurate intent classification, entity extraction, context-aware skill recommendations, and natural language workflow specification with continuous learning capabilities.

## Intent

Transform how users interact with the EDPS skill ecosystem by providing a natural language interface that accurately interprets user goals, extracts relevant context and entities, recommends appropriate skills and workflows, and learns from interaction patterns to continuously improve recommendation quality.

## Inputs

- **User prompts**: Natural language requests describing desired EDPS tasks and outcomes
- **Project context**: Current project state, completed artifacts, ongoing workflows, and history
- **Organizational context**: EDPS methodology requirements, compliance standards, quality gates
- **Skill ecosystem context**: Available skills, workflow patterns, resource availability

## Outputs

- **Intent classification**: Categorized user intent with confidence scores (>90% accuracy target)
- **Extracted entities**: Domain entities, constraints, quality requirements, context indicators
- **Skill recommendations**: Ranked list of relevant skills with confidence and rationale
- **Workflow suggestions**: Recommended workflow patterns with natural language explanations
- **Clarification questions**: Targeted questions for ambiguous or underspecified requests
- **Execution ready workflows**: Complete workflow configurations from natural language descriptions

## Core Capabilities

### 1. Multi-Modal Intent Analysis Engine

#### Intent Classification System
```javascript
/**
 * EDPS Enhanced NLP - Intent Analysis Engine
 * Multi-modal classification with domain-specific pattern recognition
 */

const intentCategories = {
    analysis: {
        id: "analysis",
        name: "Analysis and Review",
        description: "User wants to analyze, review, or examine existing artifacts",
        patterns: [
            // Direct action verbs
            /\b(analyze|analyse|review|examine|assess|evaluate|inspect|check|audit)\b/i,
            // Domain-specific patterns
            /\b(what are|identify|find|discover|detect|understand)\b.*\b(domain|concept|entity|requirement|issue|gap)\b/i,
            // Compliance-oriented patterns
            /\b(comply|compliance|validate|verify|conform|adherence)\b/i,
            // Review-focused patterns
            /\b(look at|go through|scan|survey|investigate)\b/i
        ],
        subCategories: {
            requirements_analysis: {
                patterns: [/\b(requirement|specification|constraint|need|feature)\b/i],
                skills: ["requirements-ingest", "process-w5h", "goals-extract"]
            },
            domain_analysis: {
                patterns: [/\b(domain|concept|entity|terminology|vocabulary)\b/i],
                skills: ["domain-extractconcepts", "domain-alignentities"]
            },
            compliance_analysis: {
                patterns: [/\b(edps|compliance|boundary|validation|rule|vr-[1-4])\b/i],
                skills: ["edps-compliance", "hierarchy-validation", "diagram-generatecollaboration"]
            },
            quality_analysis: {
                patterns: [/\b(quality|standard|threshold|metric|score)\b/i],
                skills: ["edps-quality-gates", "edps-compliance"]
            }
        }
    },

    creation: {
        id: "creation",
        name: "Creation and Generation",
        description: "User wants to create, build, or generate new artifacts",
        patterns: [
            /\b(create|build|generate|produce|make|develop|design|construct)\b/i,
            /\b(set up|initialize|bootstrap|start|begin|initiate)\b.*\b(project|process|model|workflow)\b/i,
            /\b(new|fresh|from scratch|initial)\b.*\b(document|model|diagram|structure)\b/i,
            /\b(draft|write|author|compose)\b/i
        ],
        subCategories: {
            diagram_creation: {
                patterns: [/\b(diagram|collaboration|sequence|flow|chart)\b/i],
                skills: ["diagram-generatecollaboration"]
            },
            documentation_creation: {
                patterns: [/\b(document|documentation|readme|guide|manual)\b/i],
                skills: ["documentation-automation", "project-document-management"]
            },
            workflow_creation: {
                patterns: [/\b(workflow|process|pipeline|flow)\b/i],
                skills: ["edps-workflow-orchestrator", "plan-derivetasks"]
            },
            project_creation: {
                patterns: [/\b(project|structure|hierarchy|organization)\b/i],
                skills: ["project-document-management", "orgmodel-update"]
            }
        }
    },

    validation: {
        id: "validation",
        name: "Validation and Compliance",
        description: "User wants to validate compliance, check rules, or verify correctness",
        patterns: [
            /\b(validate|verify|check|ensure|confirm|test|assert)\b/i,
            /\b(correct|accurate|valid|complete|consistent|compliant)\b/i,
            /\b(boundary rule|vr-[1-4]|edps|methodology)\b/i,
            /\b(pass|fail|meeting|satisf)\b.*\b(requirement|criterion|standard|rule)\b/i
        ],
        subCategories: {
            edps_validation: {
                patterns: [/\b(edps|boundary|vr-[1-4]|participant|message flow|hierarchy)\b/i],
                skills: ["edps-compliance", "hierarchy-validation", "diagram-generatecollaboration"]
            },
            quality_validation: {
                patterns: [/\b(quality|completeness|accuracy|threshold)\b/i],
                skills: ["edps-quality-gates"]
            },
            traceability_validation: {
                patterns: [/\b(traceab|trace|link|reference|requirement)\b/i],
                skills: ["hierarchy-validation", "edps-compliance"]
            }
        }
    },

    integration: {
        id: "integration",
        name: "Integration and Merging",
        description: "User wants to integrate, merge, combine, or update artifacts",
        patterns: [
            /\b(integrat|merge|combine|consolidate|unify|reconcile)\b/i,
            /\b(update|modify|change|revise|refactor|restructure)\b.*\b(model|diagram|requirement|process)\b/i,
            /\b(add|include|incorporate|embed|insert)\b.*\b(to|into|within)\b/i,
            /\b(sync|synchronize|align|harmonize)\b/i
        ],
        subCategories: {
            requirement_integration: {
                patterns: [/\b(requirement|specification|source)\b/i],
                skills: ["requirements-merge", "process-merge"]
            },
            model_integration: {
                patterns: [/\b(model|orgmodel|organization|domain)\b/i],
                skills: ["model-integration", "orgmodel-update", "process-findtopandupdate"]
            },
            change_integration: {
                patterns: [/\b(change|impact|effect|consequence)\b/i],
                skills: ["change-management", "change-impact-analysis"]
            }
        }
    },

    planning: {
        id: "planning",
        name: "Planning and Scheduling",
        description: "User wants to plan, schedule, estimate, or track project work",
        patterns: [
            /\b(plan|schedule|estimate|prioritize|roadmap|timeline)\b/i,
            /\b(task|milestone|deadline|delivery|sprint|iteration)\b/i,
            /\b(effort|duration|workload|capacity|resource)\b/i,
            /\b(track|monitor|progress|status|report)\b/i
        ],
        subCategories: {
            task_planning: {
                patterns: [/\b(task|story|backlog|work item)\b/i],
                skills: ["plan-derivetasks", "project-planning-tracking"]
            },
            schedule_planning: {
                patterns: [/\b(schedule|timeline|gantt|sprint|iteration)\b/i],
                skills: ["plan-buildschedule"]
            },
            effort_planning: {
                patterns: [/\b(estimate|effort|size|complexity|points)\b/i],
                skills: ["plan-estimateeffort"]
            },
            status_reporting: {
                patterns: [/\b(status|report|dashboard|progress|metric)\b/i],
                skills: ["project-status-reporting"]
            }
        }
    },

    troubleshooting: {
        id: "troubleshooting",
        name: "Troubleshooting and Debugging",
        description: "User wants to diagnose problems, fix issues, or resolve conflicts",
        patterns: [
            /\b(fix|solve|resolve|debug|troubleshoot|diagnose)\b/i,
            /\b(issue|problem|error|conflict|inconsistency|violation)\b/i,
            /\b(why|what went wrong|not working|failing|broken)\b/i,
            /\b(investigate|root cause|finding|analysis)\b/i
        ],
        subCategories: {
            compliance_issues: {
                patterns: [/\b(edps|boundary|validation|rule|vr)\b/i],
                skills: ["edps-compliance", "hierarchy-validation"]
            },
            integration_issues: {
                patterns: [/\b(merge|conflict|inconsistency|mismatch)\b/i],
                skills: ["change-impact-analysis", "requirements-merge"]
            }
        }
    },

    documentation: {
        id: "documentation",
        name: "Documentation and Reporting",
        description: "User wants to document, describe, explain, or report on work",
        patterns: [
            /\b(document|documenting|documentation|describe|explain|report)\b/i,
            /\b(write up|summarize|overview|summary)\b/i,
            /\b(guide|manual|instruction|tutorial|how-to)\b/i,
            /\b(communicate|present|share|publish)\b/i
        ],
        subCategories: {
            process_documentation: {
                patterns: [/\b(process|workflow|procedure|step)\b/i],
                skills: ["documentation-automation"]
            },
            project_documentation: {
                patterns: [/\b(project|status|progress|deliverable)\b/i],
                skills: ["project-status-reporting", "project-document-management"]
            }
        }
    }
};
```

### 2. Entity Extraction System

#### Domain Entity Recognition
```javascript
const entityExtractors = {
    /**
     * EDPS Domain Entities - Core methodology components
     */
    edps_domain: {
        boundary_types: {
            patterns: [
                /\b(boundary|boundaries|scope|context)\b/i,
                /\b(vr-1|vr1|boundary scope)\b/i,
                /\b(vr-2|vr2|participant type)\b/i,
                /\b(vr-3|vr3|message flow)\b/i,
                /\b(vr-4|vr4|hierarchy structure)\b/i
            ],
            extraction_function: "extractBoundaryEntities",
            entity_type: "edps_boundary"
        },
        hierarchy_elements: {
            patterns: [
                /\b(hierarchy|hierarchical|level [0-9]+|parent|child|decompos)\b/i,
                /\b(process|subprocess|activity|task) (level|decomposition)\b/i,
                /level\s*[0-9]+/i
            ],
            extraction_function: "extractHierarchyEntities",
            entity_type: "hierarchy_element"
        },
        participants: {
            patterns: [
                /\b(participant|actor|stakeholder|role|user|system|service)\b/i,
                /\b(control|entity|boundary|external)\b.*\b(type|stereotype|actor)\b/i
            ],
            extraction_function: "extractParticipantEntities",
            entity_type: "participant"
        },
        skills: {
            patterns: [
                /\b(skill|capability|function|feature|module)\b/i,
                // Direct skill name references
                /\b(requirements-ingest|goals-extract|process-w5h|domain-extract)\b/i,
                /\b(diagram-generate|hierarchy-manage|edps-compliance)\b/i,
                /\b(plan-derive|plan-estimate|plan-build|change-manage)\b/i
            ],
            extraction_function: "extractSkillEntities",
            entity_type: "edps_skill"
        }
    },

    /**
     * Project Context Entities - Current project state indicators
     */
    project_context: {
        project_phase: {
            patterns: [
                /\b(phase [0-9]+|iteration [0-9]+|sprint [0-9]+|milestone)\b/i,
                /\b(early|initial|mid|final|completion) phase\b/i,
                /\b(requirement|design|implementation|testing|deployment) phase\b/i
            ],
            extraction_function: "extractProjectPhase",
            entity_type: "project_phase"
        },
        artifacts: {
            patterns: [
                /\b(document|artifact|deliverable|output|result)\b/i,
                /\b(requirement[s]?|specification[s]?|diagram[s]?|model[s]?)\b/i,
                /\b(main\.md|process\.md|collaboration\.md|domain-model\.md)\b/i
            ],
            extraction_function: "extractArtifactEntities",
            entity_type: "project_artifact"
        },
        constraints: {
            patterns: [
                /\b(deadline|due date|by [a-z]+ [0-9]+|before [a-z]+)\b/i,
                /\b(budget|resource|capacity|limit|constraint|restriction)\b/i,
                /\b(must|required|mandatory|critical|blocking)\b/i
            ],
            extraction_function: "extractConstraintEntities",
            entity_type: "constraint"
        }
    },

    /**
     * Quality Entities - Quality requirements and standards
     */
    quality_context: {
        quality_level: {
            patterns: [
                /\b(high quality|comprehensive|thorough|detailed|complete)\b/i,
                /\b(standard quality|normal|typical|regular|moderate)\b/i,
                /\b(fast|quick|rapid|expedited|minimal|basic)\b/i
            ],
            extraction_function: "extractQualityLevel",
            entity_type: "quality_level",
            mapping: {
                high: ["high quality", "comprehensive", "thorough", "detailed", "complete"],
                standard: ["standard", "normal", "typical", "regular", "moderate"],
                fast: ["fast", "quick", "rapid", "expedited", "minimal", "basic"]
            }
        },
        urgency: {
            patterns: [
                /\b(urgent|immediately|asap|critical|priority [0-9])\b/i,
                /\b(soon|shortly|quickly|as soon as)\b/i,
                /\b(deadline|due|overdue|past due)\b/i,
                /\b(no rush|when possible|eventually|backlog)\b/i
            ],
            extraction_function: "extractUrgencyLevel",
            entity_type: "urgency",
            mapping: {
                high: ["urgent", "immediately", "asap", "critical", "deadline", "overdue"],
                medium: ["soon", "shortly", "quickly", "as soon as"],
                low: ["no rush", "when possible", "eventually", "backlog"]
            }
        }
    }
};
```

### 3. Context-Aware Recommendation Engine

#### Multi-Factor Recommendation System
```javascript
/**
 * Context-Aware Recommendation Engine
 * Generates ranked skill and workflow recommendations based on multi-factor analysis
 */
export class ContextAwareRecommendationEngine {
    constructor(config = {}) {
        this.config = config;
        this.intentAnalyzer = new IntentAnalyzer();
        this.entityExtractor = new EntityExtractor();
        this.contextBuilder = new ProjectContextBuilder();
        this.workflowMatcher = new WorkflowPatternMatcher();
        this.learningSystem = new RecommendationLearningSystem();
        this.rankingEngine = new RecommendationRankingEngine();
    }

    async generateRecommendations(userPrompt, executionContext = {}) {
        const analysisStart = performance.now();

        // Step 1: Multi-modal intent analysis
        const intentAnalysis = await this.intentAnalyzer.analyzeIntent(
            userPrompt,
            executionContext
        );

        // Step 2: Entity extraction with context enrichment
        const extractedEntities = await this.entityExtractor.extractEntities(
            userPrompt,
            intentAnalysis,
            executionContext
        );

        // Step 3: Build comprehensive project context
        const projectContext = await this.contextBuilder.buildContext(
            executionContext,
            extractedEntities
        );

        // Step 4: Generate candidate skill recommendations
        const candidateSkills = await this.generateSkillCandidates(
            intentAnalysis,
            extractedEntities,
            projectContext
        );

        // Step 5: Match workflow patterns
        const workflowRecommendations = await this.workflowMatcher.matchWorkflows(
            intentAnalysis,
            extractedEntities,
            projectContext
        );

        // Step 6: Rank and filter recommendations
        const rankedRecommendations = await this.rankingEngine.rankRecommendations(
            candidateSkills,
            workflowRecommendations,
            intentAnalysis,
            projectContext
        );

        // Step 7: Handle low-confidence scenarios with clarification
        const clarifications = await this.generateClarifications(
            intentAnalysis,
            rankedRecommendations,
            extractedEntities
        );

        const analysisTime = performance.now() - analysisStart;

        return {
            intent: intentAnalysis,
            entities: extractedEntities,
            recommendations: {
                skills: rankedRecommendations.skills,
                workflows: rankedRecommendations.workflows,
                primary_action: rankedRecommendations.primary_action
            },
            clarifications: clarifications,
            confidence: intentAnalysis.confidence,
            analysis_time: analysisTime,
            context_applied: projectContext.applied_context_factors
        };
    }

    async generateSkillCandidates(intentAnalysis, entities, projectContext) {
        const candidates = new Map();
        
        // Primary skills from intent categories
        for (const subCategory of intentAnalysis.matched_subcategories) {
            for (const skillId of subCategory.skills) {
                const score = this.calculateSkillScore(skillId, intentAnalysis, projectContext);
                candidates.set(skillId, {
                    skill_id: skillId,
                    score: score,
                    reason: `Matched ${intentAnalysis.primary_intent} intent in ${subCategory.id}`,
                    confidence: intentAnalysis.confidence * score
                });
            }
        }

        // Entity-based skill additions
        for (const entity of entities) {
            const entitySkills = await this.getSkillsForEntity(entity, projectContext);
            for (const { skill_id, relevance } of entitySkills) {
                if (candidates.has(skill_id)) {
                    // Boost existing candidate
                    candidates.get(skill_id).score *= (1 + relevance * 0.2);
                    candidates.get(skill_id).entity_reinforced = true;
                } else {
                    candidates.set(skill_id, {
                        skill_id,
                        score: relevance,
                        reason: `Relevant to extracted entity: ${entity.value}`,
                        confidence: relevance * 0.8
                    });
                }
            }
        }

        // Historical pattern boosting
        const historicalBoosts = await this.learningSystem.getHistoricalBoosts(
            intentAnalysis,
            projectContext
        );
        
        for (const boost of historicalBoosts) {
            if (candidates.has(boost.skill_id)) {
                candidates.get(boost.skill_id).score *= boost.multiplier;
                candidates.get(boost.skill_id).historically_successful = true;
            }
        }

        return Array.from(candidates.values()).sort((a, b) => b.score - a.score);
    }

    calculateSkillScore(skillId, intentAnalysis, projectContext) {
        let score = 0.7; // Base score for intent-matched skills

        // Adjust for project phase alignment
        const phaseAlignment = this.assessPhaseAlignment(skillId, projectContext.project_phase);
        score *= phaseAlignment;

        // Adjust for quality requirements
        const qualityAlignment = this.assessQualityAlignment(skillId, intentAnalysis.quality_level);
        score *= qualityAlignment;

        // Adjust for dependency availability
        const dependencyScore = this.assessDependencyAvailability(skillId, projectContext);
        score *= dependencyScore;

        return Math.min(1.0, score);
    }

    async generateClarifications(intentAnalysis, recommendations, entities) {
        const clarifications = [];

        // Generate clarifications for low-confidence intent
        if (intentAnalysis.confidence < 0.7) {
            clarifications.push({
                type: "intent_clarification",
                question: await this.generateIntentClarificationQuestion(
                    intentAnalysis,
                    entities
                ),
                options: intentAnalysis.top_candidates.map(c => c.category),
                priority: "high"
            });
        }

        // Check for missing critical entities
        const missingEntities = await this.identifyMissingCriticalEntities(
            intentAnalysis,
            entities
        );
        
        for (const missing of missingEntities) {
            clarifications.push({
                type: "entity_clarification",
                question: missing.clarification_question,
                context: missing.why_needed,
                priority: missing.priority
            });
        }

        // Scope clarification for complex requests
        if (recommendations.workflows.length > 1 && !entities.some(e => e.type === 'scope')) {
            clarifications.push({
                type: "scope_clarification",
                question: "What scope of work are you targeting? (quick review / comprehensive analysis / full workflow execution)",
                options: ["quick", "standard", "comprehensive"],
                priority: "medium"
            });
        }

        // Sort by priority and limit to prevent overwhelming users
        return clarifications
            .sort((a, b) => this.clarificationPriority(a) - this.clarificationPriority(b))
            .slice(0, 2); // Maximum 2 clarification questions at once
    }
}
```

### 4. Natural Language Workflow Builder

#### Workflow Specification from Natural Language
```javascript
/**
 * Natural Language Workflow Builder
 * Converts user natural language descriptions into executable EDPS workflows
 */
export class NaturalLanguageWorkflowBuilder {
    constructor(workflowOrchestrator, nlpEngine) {
        this.workflowOrchestrator = workflowOrchestrator;
        this.nlpEngine = nlpEngine;
        this.patternLibrary = new WorkflowPatternLibrary();
        this.constraintProcessor = new WorkflowConstraintProcessor();
        this.validationLayer = new WorkflowValidationLayer();
    }

    /**
     * Parse natural language workflow specification into executable workflow
     */
    async parseWorkflowSpecification(userDescription, context = {}) {
        // Analyze the full workflow description
        const workflowAnalysis = await this.analyzeWorkflowDescription(
            userDescription,
            context
        );

        // Match against known workflow patterns
        const patternMatches = await this.patternLibrary.matchPatterns(
            workflowAnalysis,
            context
        );

        if (patternMatches.best_match.confidence > 0.85) {
            // High-confidence pattern match: adapt existing pattern
            return await this.adaptExistingPattern(
                patternMatches.best_match,
                workflowAnalysis,
                context
            );
        } else {
            // Lower confidence: build custom workflow from components
            return await this.buildCustomWorkflow(
                workflowAnalysis,
                patternMatches.partial_matches,
                context
            );
        }
    }

    async analyzeWorkflowDescription(description, context) {
        // Extract workflow intent components
        const components = {
            starting_point: await this.identifyStartingPoint(description, context),
            end_goal: await this.identifyEndGoal(description, context),
            intermediate_steps: await this.extractIntermediateSteps(description),
            constraints: await this.extractWorkflowConstraints(description),
            quality_requirements: await this.extractQualityRequirements(description),
            parallel_indicators: await this.detectParallelismIndicators(description)
        };

        return components;
    }

    async adaptExistingPattern(patternMatch, workflowAnalysis, context) {
        const basePattern = await this.patternLibrary.loadPattern(patternMatch.pattern_id);
        
        // Apply user-specified customizations
        const customizedWorkflow = {
            ...basePattern,
            customizations: {
                quality_level: workflowAnalysis.quality_requirements,
                constraints: workflowAnalysis.constraints,
                context_adaptations: context
            }
        };

        // Validate the adapted workflow
        const validation = await this.validationLayer.validate(customizedWorkflow);
        
        return {
            workflow: customizedWorkflow,
            pattern_used: patternMatch.pattern_id,
            adaptations_applied: customizedWorkflow.customizations,
            validation_result: validation,
            confidence: patternMatch.confidence,
            ready_for_execution: validation.passed
        };
    }

    async buildCustomWorkflow(workflowAnalysis, partialMatches, context) {
        const workflowSteps = [];

        // Use starting point to determine initial skills
        const initialSkills = await this.resolveStartingPoint(
            workflowAnalysis.starting_point,
            context
        );
        workflowSteps.push(...initialSkills);

        // Add intermediate steps from description
        for (const step of workflowAnalysis.intermediate_steps) {
            const resolvedStep = await this.resolveStepToSkill(step, context);
            if (resolvedStep) {
                workflowSteps.push(resolvedStep);
            }
        }

        // Ensure end goal can be achieved
        const finalSteps = await this.resolveEndGoal(
            workflowAnalysis.end_goal,
            workflowSteps,
            context
        );
        workflowSteps.push(...finalSteps);

        // Apply constraints and quality requirements
        const constrainedWorkflow = await this.constraintProcessor.applyConstraints(
            workflowSteps,
            workflowAnalysis.constraints,
            workflowAnalysis.quality_requirements
        );

        // Optimize for parallel execution where applicable
        if (workflowAnalysis.parallel_indicators.length > 0) {
            constrainedWorkflow.execution_plan = await this.optimizeForParallelExecution(
                constrainedWorkflow,
                workflowAnalysis.parallel_indicators
            );
        }

        const validation = await this.validationLayer.validate(constrainedWorkflow);

        return {
            workflow: constrainedWorkflow,
            pattern_used: "custom_built",
            partial_patterns_applied: partialMatches.map(m => m.pattern_id),
            validation_result: validation,
            confidence: this.calculateCustomWorkflowConfidence(workflowAnalysis, validation),
            ready_for_execution: validation.passed
        };
    }

    /**
     * Allow natural language modification of existing workflows
     */
    async modifyWorkflowWithNaturalLanguage(existingWorkflow, modificationDescription, context) {
        // Parse modification intent
        const modificationAnalysis = await this.nlpEngine.analyzeModificationIntent(
            modificationDescription,
            existingWorkflow,
            context
        );

        const modifications = [];

        switch (modificationAnalysis.modification_type) {
            case 'add_step':
                modifications.push(
                    await this.addStep(existingWorkflow, modificationAnalysis)
                );
                break;

            case 'remove_step':
                modifications.push(
                    await this.removeStep(existingWorkflow, modificationAnalysis)
                );
                break;

            case 'change_quality':
                modifications.push(
                    await this.adjustQualityLevel(existingWorkflow, modificationAnalysis)
                );
                break;

            case 'add_constraint':
                modifications.push(
                    await this.addConstraint(existingWorkflow, modificationAnalysis)
                );
                break;

            case 'change_sequence':
                modifications.push(
                    await this.resequenceSteps(existingWorkflow, modificationAnalysis)
                );
                break;
        }

        // Apply and validate modifications
        const modifiedWorkflow = await this.applyModifications(existingWorkflow, modifications);
        const validation = await this.validationLayer.validate(modifiedWorkflow);

        return {
            original_workflow: existingWorkflow,
            modified_workflow: modifiedWorkflow,
            modifications_applied: modifications,
            modification_description: modificationDescription,
            validation_result: validation,
            ready_for_execution: validation.passed
        };
    }
}
```

### 5. Learning and Adaptation System

#### Continuous Improvement Engine
```javascript
/**
 * Learning and Adaptation System
 * Continuously improves intent recognition and recommendation quality from user feedback
 */
export class RecommendationLearningSystem {
    constructor(config = {}) {
        this.config = config;
        this.feedbackStore = new FeedbackDataStore();
        this.patternEvolver = new PatternEvolutionEngine();
        this.performanceTracker = new AccuracyTracker();
        this.modelRefiner = new ClassificationModelRefiner();
    }

    /**
     * Record user acceptance or rejection of recommendations
     */
    async recordFeedback(feedbackEvent) {
        const enrichedFeedback = {
            ...feedbackEvent,
            timestamp: new Date(),
            context_snapshot: await this.captureContextSnapshot(feedbackEvent),
            recommendation_metadata: feedbackEvent.recommendation_metadata,
            outcome: feedbackEvent.accepted ? 'accepted' : 'rejected'
        };

        await this.feedbackStore.store(enrichedFeedback);

        // Immediate pattern update for high-confidence feedback
        if (feedbackEvent.feedback_confidence > 0.8) {
            await this.applyImmediateLearning(enrichedFeedback);
        }

        // Batch learning updates for model refinement
        const pendingFeedback = await this.feedbackStore.getPendingForLearning();
        if (pendingFeedback.length >= this.config.batchLearningThreshold || 10) {
            await this.triggerBatchLearning(pendingFeedback);
        }

        return {
            feedback_recorded: true,
            immediate_learning_applied: feedbackEvent.feedback_confidence > 0.8,
            batch_count: pendingFeedback.length
        };
    }

    async applyImmediateLearning(feedbackEvent) {
        if (feedbackEvent.outcome === 'accepted') {
            // Boost confidence for matched patterns
            await this.patternEvolver.boostPatternConfidence(
                feedbackEvent.matched_patterns,
                feedbackEvent.context_snapshot,
                0.05 // 5% boost per positive signal
            );
        } else {
            // Reduce confidence and record negative pattern
            await this.patternEvolver.reducePatternConfidence(
                feedbackEvent.matched_patterns,
                feedbackEvent.context_snapshot,
                0.03 // 3% reduction per negative signal
            );

            // Record rejection reason if provided
            if (feedbackEvent.rejection_reason) {
                await this.patternEvolver.recordRejectionPattern(
                    feedbackEvent,
                    feedbackEvent.rejection_reason
                );
            }
        }
    }

    async triggerBatchLearning(feedbackBatch) {
        // Analyze patterns across the feedback batch
        const patternAnalysis = await this.patternEvolver.analyzeFeedbackBatch(feedbackBatch);

        // Update classification model weights
        const modelUpdates = await this.modelRefiner.refineFromFeedback(
            patternAnalysis,
            feedbackBatch
        );

        // Track accuracy improvements
        await this.performanceTracker.recordLearningCycle({
            feedback_count: feedbackBatch.length,
            model_updates: modelUpdates,
            accuracy_before: patternAnalysis.baseline_accuracy,
            accuracy_after: modelUpdates.projected_accuracy.after,
            timestamp: new Date()
        });

        // Mark feedback as processed
        await this.feedbackStore.markAsProcessed(feedbackBatch.map(f => f.id));

        return modelUpdates;
    }

    async getHistoricalBoosts(intentAnalysis, projectContext) {
        // Retrieve historically successful patterns for similar intents and contexts
        const historicalPatterns = await this.feedbackStore.querySuccessfulPatterns({
            intent_category: intentAnalysis.primary_intent,
            project_phase: projectContext.project_phase,
            quality_level: intentAnalysis.quality_level,
            min_acceptance_rate: 0.75,
            max_results: 10
        });

        return historicalPatterns.map(pattern => ({
            skill_id: pattern.recommended_skill,
            multiplier: this.calculateBoostMultiplier(pattern),
            basis: 'historical_success'
        }));
    }

    calculateBoostMultiplier(historicalPattern) {
        const acceptanceRate = historicalPattern.acceptance_count / historicalPattern.total_shown;
        const recencyWeight = this.calculateRecencyWeight(historicalPattern.last_seen);
        const contextSimilarity = historicalPattern.context_similarity_score;
        
        return 1 + (acceptanceRate * recencyWeight * contextSimilarity * 0.3);
    }

    async getPerformanceMetrics() {
        const cycles = await this.performanceTracker.getAllLearningCycles();
        const latest = await this.performanceTracker.getCurrentAccuracy();

        return {
            current_accuracy: latest.intent_classification_accuracy,
            accuracy_trend: cycles.map(c => ({
                timestamp: c.timestamp,
                accuracy: c.accuracy_after
            })),
            total_feedback_processed: await this.feedbackStore.getTotalCount(),
            recommendation_acceptance_rate: await this.calculateOverallAcceptanceRate(),
            top_improving_patterns: await this.patternEvolver.getTopImprovingPatterns(),
            areas_needing_improvement: await this.identifyImprovementAreas()
        };
    }
}
```

## Usage Patterns

### Standard Intent Analysis
```markdown
@workspace [user prompt describing EDPS task]

The NLP system will:
1. Classify intent (analysis / creation / validation / integration / planning)
2. Extract entities (domain concepts, constraints, quality requirements)  
3. Apply project context (phase, history, ongoing work)
4. Recommend skills with confidence scores
5. Suggest matching workflow patterns
6. Ask targeted clarifications if intent is ambiguous
```

### Natural Language Workflow Specification
```markdown
@workspace I need a workflow that:
- Starts from raw requirements text
- Creates an EDPS collaboration diagram with boundary validation
- Validates hierarchy compliance
- Produces final documentation

The NLP system converts this description into an executable EDPS workflow with appropriate skills sequenced for the described pipeline.
```

### Feedback and Learning
```markdown
@workspace [after recommendation]
That suggestion wasn't quite right — I actually want to focus on hierarchy structure not requirements ingestion.

The NLP system records negative feedback, learns the correction, and provides updated recommendations with improved accuracy for similar future queries.
```

## Performance Specifications

- **Intent Classification Accuracy**: >90% for standard EDPS requests
- **Response Time**: <3 seconds for 95th percentile queries (standard requests)
- **Entity Extraction Precision**: >85% precision, >80% recall
- **Recommendation Acceptance**: >85% user acceptance rate target
- **Learning Rate**: Measurable accuracy improvement after 20+ feedback events
- **Clarification Efficiency**: <2 questions needed per ambiguous query

## Integration Architecture

```
User Prompt
     │
     ▼
Intent Analysis Engine (T09)
     │ ──── Pattern Matching ────▶ Intent Categories
     │ ──── Entity Extraction ───▶ Domain Entities
     │ ──── Context Building ────▶ Project Context
     │
     ▼
Recommendation Engine (T09)
     │ ──── Skill Scoring ───────▶ edps-skill-navigator (T06)
     │ ──── Workflow Matching ───▶ edps-workflow-orchestrator (T07)
     │ ──── Gate Requirements ──▶ edps-quality-gates (T08)
     │
     ▼
Output: Intent + Entities + Ranked Recommendations + Clarifications
```
