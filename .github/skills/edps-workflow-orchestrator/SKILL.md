---
name: edps-workflow-orchestrator
description: Intelligent workflow orchestration system that dynamically generates, selects, and executes optimal skill combinations based on user intent and project context. Builds advanced automation capabilities on top of the edps-skill-navigator foundation.
license: MIT
---

# EDPS Workflow Orchestrator

An advanced workflow coordination system that provides intelligent, context-aware orchestration of EDPS skill sequences. This skill builds upon the edps-skill-navigator foundation to deliver dynamic workflow generation, adaptive execution, and comprehensive monitoring of multi-skill processes.

## Intent

Transform user requirements into optimally sequenced, automatically executed workflow processes. Provide sophisticated orchestration that adapts to project context, user urgency, quality requirements, and resource constraints while maintaining comprehensive monitoring and error recovery capabilities.

## Inputs

- **User intent**: Natural language workflow requests (e.g., "analyze requirements comprehensively", "design organizational model", "integrate new process")
- **Project context**: Current project state, available artifacts, team size, timeline constraints
- **Quality requirements**: Performance expectations, compliance standards, documentation depth
- **Resource constraints**: Time limitations, concurrent capacity, priority levels

## Outputs

- **Dynamic workflow plans**: Context-optimized execution sequences with multiple alternatives
- **Automated execution**: Coordinated skill invocation with real-time monitoring
- **Progress analytics**: Comprehensive tracking, performance metrics, and completion forecasting
- **Recovery mechanisms**: Intelligent error handling and alternative execution paths

## Core Function

**Purpose**: Provide intelligent, adaptive workflow orchestration with dynamic optimization and comprehensive monitoring
**Input**: User intent, project context, and execution requirements
**Output**: Executed workflows with analytics, monitoring, and adaptive optimization
**Integration**: Advanced orchestration layer built on edps-skill-navigator foundation

## Core Capabilities

### 1. Dynamic Workflow Generation

#### Pattern Library Management
```javascript
const workflowPatterns = {
    // Fast-Track Workflows (30-45 min execution)
    requirements_quick_analysis: {
        pattern: "linear",
        skills: ["requirements-ingest", "goals-extract", "process-w5h"],
        execution_time: "30-45 minutes",
        complexity: "low",
        conditions: {
            requirements: ["simple", "well_defined"],
            urgency: ["high"],
            quality_level: ["standard"]
        },
        optimizations: {
            skip_validation: true,
            use_templates: true,
            minimal_documentation: true,
            parallel_execution: false
        }
    },

    domain_discovery_rapid: {
        pattern: "parallel_convergence", 
        skills: ["requirements-ingest", "domain-extractconcepts", "goals-extract"],
        execution_time: "45-60 minutes",
        complexity: "medium",
        conditions: {
            requirements: ["moderate", "clear_scope"],
            urgency: ["high", "medium"],
            team_size: ["multiple"],
            quality_level: ["standard", "high"]
        },
        optimizations: {
            parallel_execution: ["requirements-ingest", "goals-extract"],
            quick_convergence: "domain-extractconcepts",
            validation_gates: ["minimal"]
        }
    },

    // Standard Analysis Workflows (2-3 hours)
    complete_requirements_analysis: {
        pattern: "sequential_with_feedback",
        skills: [
            "requirements-ingest",
            "goals-extract",
            "process-w5h", 
            "domain-extractconcepts",
            "domain-alignentities",
            "requirements-merge"
        ],
        execution_time: "2-3 hours",
        complexity: "medium",
        conditions: {
            requirements: ["complex", "multiple_sources"],
            quality_level: ["high", "comprehensive"],
            documentation: ["complete"]
        },
        validation_gates: [
            { after: "requirements-ingest", check: "requirements_quality" },
            { after: "domain-alignentities", check: "domain_consistency" },
            { after: "requirements-merge", check: "completeness" }
        ],
        optimizations: {
            parallel_opportunities: ["goals-extract", "process-w5h"],
            feedback_loops: true,
            comprehensive_validation: true
        }
    },

    // End-to-End Process Design (4-6 hours)
    end_to_end_process_design: {
        pattern: "hierarchical_decomposition",
        skills: [
            "project-document-management",
            "requirements-ingest",
            "domain-extractconcepts",
            "diagram-generatecollaboration",
            "hierarchy-management", 
            "hierarchy-validation",
            "edps-compliance",
            "documentation-automation"
        ],
        execution_time: "4-6 hours",
        complexity: "high",
        conditions: {
            scope: ["large", "organizational"],
            methodology: ["edps"],
            deliverable: ["comprehensive"],
            quality_level: ["high", "enterprise"]
        },
        strategic_decision_points: [
            { after: "domain-extractconcepts", decision: "depth_vs_breadth" },
            { after: "diagram-generatecollaboration", decision: "hierarchy_depth" },
            { after: "hierarchy-management", decision: "validation_thoroughness" }
        ],
        validation_gates: [
            { after: "requirements-ingest", check: "requirements_completeness" },
            { after: "diagram-generatecollaboration", check: "boundary_validation" },
            { after: "hierarchy-validation", check: "structural_integrity" },
            { after: "edps-compliance", check: "methodology_adherence" }
        ]
    },

    // Specialized Workflows
    hierarchy_deep_dive: {
        pattern: "iterative_refinement",
        skills: [
            "diagram-generatecollaboration",
            "hierarchy-management",
            "hierarchy-validation",
            "change-impact-analysis",
            "edps-compliance",
            "documentation-automation"
        ],
        execution_time: "3-4 hours",
        complexity: "high",
        conditions: {
            focus: ["hierarchy", "structure"],
            has_collaboration_diagram: true,
            depth_requirements: ["multi_level"]
        },
        iteration_strategy: {
            max_iterations: 5,
            convergence_criteria: ["validation_score > 0.9", "no_structural_issues"],
            refinement_focus: ["boundary_optimization", "participant_classification"]
        }
    },

    integration_and_validation: {
        pattern: "validation_cascade",
        skills: [
            "hierarchy-validation",
            "edps-compliance",
            "integration-testing", 
            "change-impact-analysis"
        ],
        execution_time: "1-2 hours",
        complexity: "medium",
        conditions: {
            has_artifacts: ["hierarchy", "models"],
            phase: ["validation", "integration"],
            quality_gates: true
        },
        validation_cascade: [
            { level: "structural", skills: ["hierarchy-validation"] },
            { level: "methodology", skills: ["edps-compliance"] },
            { level: "integration", skills: ["integration-testing"] },
            { level: "impact", skills: ["change-impact-analysis"] }
        ]
    },

    // Maintenance & Evolution Workflows
    model_evolution: {
        pattern: "change_propagation",
        skills: [
            "change-impact-analysis",
            "model-integration",
            "process-merge",
            "orgmodel-update",
            "hierarchy-validation"
        ],
        execution_time: "2-4 hours",
        complexity: "high",
        conditions: {
            change_type: ["model_update", "process_modification"],
            impact_scope: ["organizational", "multi_process"],
            change_approval: true
        },
        change_management: {
            impact_assessment: true,
            rollback_plan: true,
            stakeholder_approval: true,
            gradual_rollout: true
        }
    }
};
```

#### Context-Aware Selection Algorithm
```javascript
async function selectOptimalWorkflow(userIntent, projectContext, requirements) {
    const candidateWorkflows = await generateWorkflowCandidates(userIntent);
    const scoredWorkflows = await scoreWorkflows(candidateWorkflows, projectContext, requirements);
    
    return {
        selected: scoredWorkflows[0],
        alternatives: scoredWorkflows.slice(1, 3),
        selection_rationale: generateSelectionRationale(scoredWorkflows[0], projectContext),
        confidence: calculateSelectionConfidence(scoredWorkflows),
        execution_plan: await generateExecutionPlan(scoredWorkflows[0], projectContext)
    };
}

async function scoreWorkflows(workflows, projectContext, requirements) {
    return workflows.map(workflow => ({
        ...workflow,
        score: calculateWorkflowScore(workflow, projectContext, requirements),
        fitness_factors: {
            complexity_match: assessComplexityFit(workflow.complexity, requirements.complexity),
            urgency_alignment: assessUrgencyFit(workflow.execution_time, requirements.urgency),
            quality_satisfaction: assessQualityFit(workflow.quality_gates, requirements.quality_level),
            resource_efficiency: assessResourceFit(workflow.resources, projectContext.available_resources),
            context_appropriateness: assessContextFit(workflow.conditions, projectContext)
        }
    })).sort((a, b) => b.score - a.score);
}
```

### 2. Execution Engine

#### Workflow Coordination Framework
```javascript
class WorkflowExecutionEngine {
    constructor() {
        this.activeWorkflows = new Map();
        this.skillRegistry = new SkillRegistry();
        this.monitoringSystem = new WorkflowMonitoringSystem();
        this.recoveryManager = new ErrorRecoveryManager();
        
        this.initializeExecutionPools();
        this.initializeMonitoring();
    }

    async executeWorkflow(workflowPlan, executionContext) {
        const executionId = this.generateExecutionId();
        const execution = new WorkflowExecution(executionId, workflowPlan, executionContext);
        
        try {
            this.activeWorkflows.set(executionId, execution);
            await this.monitoringSystem.startMonitoring(executionId);
            
            const result = await this.coordinateExecution(execution);
            await this.finalizeExecution(executionId, result);
            
            return {
                execution_id: executionId,
                status: "completed",
                result: result,
                metrics: await this.collectExecutionMetrics(executionId),
                duration: execution.getTotalDuration()
            };
            
        } catch (error) {
            return await this.handleExecutionError(executionId, error);
        }
    }

    async coordinateExecution(execution) {
        const steps = execution.workflowPlan.steps;
        const results = new Map();
        
        for (const step of steps) {
            if (step.execution_pattern === "parallel") {
                const parallelResults = await this.executeParallelSteps(step.skills, execution.context);
                parallelResults.forEach((result, skillId) => results.set(skillId, result));
            } else {
                const skillResult = await this.executeSkillStep(step, execution.context, results);
                results.set(step.skill_id, skillResult);
            }
            
            // Apply quality gates if defined
            if (step.quality_gates) {
                await this.validateStepOutput(step, skillResult);
            }
            
            // Update execution context with results
            execution.context = this.updateExecutionContext(execution.context, skillResult);
            
            // Check for adaptive workflow adjustments
            const adaptations = await this.checkForWorkflowAdaptations(execution, results);
            if (adaptations.length > 0) {
                execution = await this.applyWorkflowAdaptations(execution, adaptations);
            }
        }
        
        return this.aggregateWorkflowResults(results);
    }

    async executeParallelSteps(skills, context) {
        const promises = skills.map(skill => 
            this.executeSkillStep({ skill_id: skill.id, parameters: skill.parameters }, context)
        );
        
        const results = await Promise.allSettled(promises);
        return this.processParallelResults(results, skills);
    }

    async executeSkillStep(step, context, previousResults) {
        const skill = await this.skillRegistry.getSkill(step.skill_id);
        const enrichedContext = this.enrichContextWithPreviousResults(context, previousResults);
        
        const startTime = Date.now();
        try {
            const result = await skill.execute(step.parameters, enrichedContext);
            const duration = Date.now() - startTime;
            
            await this.monitoringSystem.recordStepCompletion(step.skill_id, duration, result);
            return result;
            
        } catch (error) {
            const duration = Date.now() - startTime;
            await this.monitoringSystem.recordStepError(step.skill_id, duration, error);
            
            // Attempt recovery
            return await this.recoveryManager.handleStepError(step, error, context);
        }
    }
}
```

### 3. Monitoring & Analytics System

#### Real-Time Progress Tracking
```javascript
class WorkflowMonitoringSystem {
    constructor() {
        this.activeMonitors = new Map();
        this.metricsCollector = new MetricsCollector();
        this.alertingSystem = new AlertingSystem();
        this.analyticsEngine = new AnalyticsEngine();
    }

    async startMonitoring(executionId) {
        const monitor = new WorkflowMonitor(executionId);
        this.activeMonitors.set(executionId, monitor);
        
        await monitor.initialize({
            progress_tracking: true,
            performance_monitoring: true,
            error_detection: true,
            resource_monitoring: true
        });
        
        return monitor;
    }

    async getWorkflowProgress(executionId) {
        const monitor = this.activeMonitors.get(executionId);
        if (!monitor) return null;
        
        return {
            execution_id: executionId,
            current_step: monitor.getCurrentStep(),
            completed_steps: monitor.getCompletedSteps(),
            remaining_steps: monitor.getRemainingSteps(),
            progress_percentage: monitor.calculateProgressPercentage(),
            estimated_completion: monitor.getEstimatedCompletion(),
            performance_metrics: {
                average_step_duration: monitor.getAverageStepDuration(),
                current_performance_trend: monitor.getPerformanceTrend(),
                resource_utilization: monitor.getResourceUtilization()
            },
            current_status: monitor.getCurrentStatus()
        };
    }

    async recordStepCompletion(skillId, duration, result) {
        await this.metricsCollector.recordMetric({
            type: "step_completion",
            skill_id: skillId,
            duration: duration,
            success: true,
            result_quality: this.assessResultQuality(result),
            timestamp: new Date().toISOString()
        });
        
        // Check for performance alerts
        const performanceThreshold = this.getPerformanceThreshold(skillId);
        if (duration > performanceThreshold) {
            await this.alertingSystem.triggerAlert({
                type: "performance_degradation",
                skill_id: skillId,
                actual_duration: duration,
                expected_duration: performanceThreshold,
                severity: this.calculateAlertSeverity(duration, performanceThreshold)
            });
        }
    }

    async generateExecutionReport(executionId) {
        const monitor = this.activeMonitors.get(executionId);
        const metrics = await this.metricsCollector.getExecutionMetrics(executionId);
        
        return {
            execution_summary: {
                execution_id: executionId,
                total_duration: metrics.total_duration,
                steps_completed: metrics.completed_steps.length,
                success_rate: metrics.success_rate,
                overall_quality: metrics.overall_quality_score
            },
            performance_analysis: {
                duration_breakdown: metrics.step_durations,
                performance_vs_baseline: await this.compareToBaseline(executionId),
                bottleneck_analysis: await this.identifyBottlenecks(metrics),
                optimization_opportunities: await this.identifyOptimizations(metrics)
            },
            quality_analysis: {
                output_quality_scores: metrics.quality_scores,
                validation_gate_results: metrics.gate_results,
                error_analysis: metrics.error_summary
            },
            recommendations: await this.generateRecommendations(executionId, metrics)
        };
    }
}
```

### 4. Adaptive Workflow Engine

#### Dynamic Workflow Adaptation
```javascript
class AdaptiveWorkflowEngine {
    constructor() {
        this.adaptationRules = new AdaptationRuleEngine();
        this.learningSystem = new WorkflowLearningSystem();
        this.contextAnalyzer = new ContextAnalyzer();
    }

    async analyzeAdaptationOpportunities(execution, currentResults) {
        const adaptations = [];
        
        // Performance-based adaptations
        const performanceAdaptations = await this.analyzePerformanceAdaptations(execution);
        adaptations.push(...performanceAdaptations);
        
        // Quality-based adaptations
        const qualityAdaptations = await this.analyzeQualityAdaptations(currentResults);
        adaptations.push(...qualityAdaptations);
        
        // Context-based adaptations
        const contextAdaptations = await this.analyzeContextChanges(execution.context);
        adaptations.push(...contextAdaptations);
        
        // Resource-based adaptations
        const resourceAdaptations = await this.analyzeResourceConstraints(execution);
        adaptations.push(...resourceAdaptations);
        
        return this.prioritizeAdaptations(adaptations);
    }

    async applyWorkflowAdaptation(execution, adaptation) {
        switch (adaptation.type) {
            case "parallel_optimization":
                return await this.optimizeParallelExecution(execution, adaptation);
            
            case "quality_gate_adjustment":
                return await this.adjustQualityGates(execution, adaptation);
            
            case "resource_reallocation":
                return await this.reallocateResources(execution, adaptation);
            
            case "alternative_skill_substitution":
                return await this.substituteSkills(execution, adaptation);
            
            case "workflow_pattern_switch":
                return await this.switchWorkflowPattern(execution, adaptation);
            
            default:
                throw new Error(`Unknown adaptation type: ${adaptation.type}`);
        }
    }

    async optimizeParallelExecution(execution, adaptation) {
        const parallelGroups = adaptation.parallel_groups;
        const updatedSteps = [];
        
        for (const group of parallelGroups) {
            const parallelStep = {
                execution_pattern: "parallel",
                skills: group.skills,
                coordination_strategy: group.strategy,
                timeout: group.timeout,
                failure_policy: group.failure_policy
            };
            updatedSteps.push(parallelStep);
        }
        
        execution.workflowPlan.steps = this.mergeSteps(execution.workflowPlan.steps, updatedSteps);
        return execution;
    }
}
```

### 5. Error Recovery & Resilience

#### Intelligent Error Handling
```javascript
class ErrorRecoveryManager {
    constructor() {
        this.recoveryStrategies = new RecoveryStrategyLibrary();
        this.errorClassifier = new ErrorClassifier();
        this.fallbackWorkflows = new FallbackWorkflowLibrary();
    }

    async handleStepError(step, error, context) {
        const errorClassification = await this.errorClassifier.classifyError(error);
        const recoveryStrategy = await this.selectRecoveryStrategy(errorClassification, step, context);
        
        switch (recoveryStrategy.type) {
            case "retry_with_backoff":
                return await this.retryWithBackoff(step, context, recoveryStrategy.config);
            
            case "alternative_skill":
                return await this.executeAlternativeSkill(step, context, recoveryStrategy.alternative);
            
            case "skip_with_warning":
                return await this.skipStepWithWarning(step, error, recoveryStrategy.impact_assessment);
            
            case "fallback_workflow":
                return await this.executeFallbackWorkflow(step, context, recoveryStrategy.fallback);
            
            case "manual_intervention":
                return await this.requestManualIntervention(step, error, context);
            
            default:
                throw error; // Re-throw if no recovery strategy available
        }
    }

    async selectRecoveryStrategy(errorClassification, step, context) {
        const candidates = await this.recoveryStrategies.getCandidateStrategies(
            errorClassification,
            step.skill_id,
            context.criticality_level
        );
        
        return this.rankRecoveryStrategies(candidates, context)[0];
    }

    async generateRecoveryPlan(execution, errors) {
        const recoveryPlan = {
            execution_id: execution.id,
            errors: errors,
            recovery_actions: [],
            impact_assessment: {},
            rollback_plan: {}
        };
        
        for (const error of errors) {
            const strategy = await this.selectRecoveryStrategy(
                await this.errorClassifier.classifyError(error.error),
                error.step,
                execution.context
            );
            
            recoveryPlan.recovery_actions.push({
                error_id: error.id,
                strategy: strategy,
                expected_impact: strategy.expected_impact,
                confidence: strategy.confidence
            });
        }
        
        recoveryPlan.impact_assessment = await this.assessRecoveryImpact(recoveryPlan);
        recoveryPlan.rollback_plan = await this.generateRollbackPlan(execution, recoveryPlan);
        
        return recoveryPlan;
    }
}
```

## Integration Points

### Enhanced Skill Navigator Integration
- **Natural Language Processing**: Leverages T06 enhanced intent recognition
- **Skill Discovery**: Builds on T06 skill recommendation capabilities  
- **Context Management**: Extends T06 context awareness with workflow-specific insights
- **Execution Coordination**: Enhances T06 skill coordination with sophisticated orchestration

### Quality Gate Integration (T08)
- **Validation Checkpoints**: Seamless integration with quality gate validation
- **Failure Handling**: Coordinated response to gate failures with workflow adaptation
- **Quality Metrics**: Integration of gate results into workflow analytics

### Enhanced NLP Integration (T09)
- **Intent Analysis**: Workflow selection based on advanced intent recognition
- **Context Understanding**: Rich context analysis for optimal workflow adaptation
- **Natural Language Specification**: Support for natural language workflow definition

## Usage Patterns

### Simple Workflow Request
```
User: "I need to quickly analyze these requirements"
System: Analyzes intent → Selects fast-track workflow → Executes requirements_quick_analysis pattern
Result: 30-45 minute automated analysis with progress tracking
```

### Complex Organizational Design
```
User: "Design a comprehensive EDPS organizational model from stakeholder requirements"
System: Analyzes complexity → Selects end-to-end design workflow → Executes with quality gates
Result: 4-6 hour orchestrated process with validation checkpoints and documentation
```

### Adaptive Execution
```
User: "Analyze requirements but I'm in a hurry"
System: Starts standard workflow → Detects urgency → Adapts to parallel execution → Optimizes quality gates
Result: Adaptive workflow that balances speed and quality based on real-time constraints
```

## Performance Specifications

- **Workflow Selection**: < 2 seconds response time for selection decisions
- **Execution Initiation**: < 5 seconds to begin workflow execution
- **Monitoring Updates**: Real-time progress updates with < 1 second latency
- **Concurrent Workflows**: Support for 20+ simultaneous workflow executions
- **Error Recovery**: < 30 seconds for standard error recovery procedures
- **Analytics Generation**: Comprehensive reports generated within 10 seconds

## Quality Assurance

- **Validation Integration**: Seamless integration with T08 quality gate system
- **EDPS Compliance**: Built-in compliance checking with T04 boundary validation rules
- **Performance Monitoring**: Continuous performance tracking and optimization
- **Error Resilience**: Comprehensive error handling with multiple recovery strategies

## Future Extensions

- **Machine Learning Integration**: Workflow optimization based on execution history
- **Advanced Resource Management**: Dynamic resource allocation and optimization
- **Cross-Project Learning**: Learning from workflows across multiple projects
- **Enhanced Visualization**: Real-time workflow execution visualization and dashboards