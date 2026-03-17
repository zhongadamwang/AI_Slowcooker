/**
 * EDPS Workflow Orchestrator - Execution Engine Implementation
 * 
 * This module implements the core execution engine that coordinates
 * skill invocations, manages workflow state, and handles monitoring
 * and error recovery according to T07 specifications.
 */

import { EventEmitter } from 'events';
import { WorkflowPatterns } from './workflow-patterns.json';
import { SkillRegistry } from '../edps-skill-navigator/skill-registry';
import { QualityGateSystem } from '../quality-gates/gate-system'; // T08 integration
import { EnhancedNLPEngine } from '../enhanced-nlp/nlp-engine'; // T09 integration

/**
 * Main Workflow Execution Engine
 * Manages the complete lifecycle of workflow execution from selection to completion
 */
export class WorkflowExecutionEngine extends EventEmitter {
    constructor(config = {}) {
        super();
        
        this.config = {
            maxConcurrentWorkflows: config.maxConcurrentWorkflows || 20,
            defaultTimeout: config.defaultTimeout || 300000, // 5 minutes
            retryAttempts: config.retryAttempts || 3,
            performanceThresholds: config.performanceThresholds || {},
            ...config
        };

        // Core components
        this.activeWorkflows = new Map();
        this.workflowQueue = [];
        this.skillRegistry = new SkillRegistry();
        this.qualityGateSystem = new QualityGateSystem(); // T08 integration
        this.nlpEngine = new EnhancedNLPEngine(); // T09 integration
        
        // Monitoring and analytics
        this.monitoringSystem = new WorkflowMonitoringSystem();
        this.analyticsCollector = new AnalyticsCollector();
        this.performanceTracker = new PerformanceTracker();
        
        // Error handling and recovery
        this.errorRecoveryManager = new ErrorRecoveryManager();
        this.adaptationEngine = new AdaptiveWorkflowEngine();
        
        // Resource management
        this.resourceManager = new ResourceManager(this.config);
        
        this.initializeEngine();
    }

    async initializeEngine() {
        await this.skillRegistry.initialize();
        await this.monitoringSystem.initialize();
        await this.qualityGateSystem.initialize();
        await this.nlpEngine.initialize();
        
        this.emit('engine_initialized');
    }

    /**
     * Main entry point for workflow execution
     * Analyzes user intent, selects optimal workflow, and executes it
     */
    async orchestrateWorkflow(userInput, projectContext = {}, executionOptions = {}) {
        const executionId = this.generateExecutionId();
        
        try {
            // Phase 1: Intent Analysis and Workflow Selection (< 2 seconds target)
            const selectionStart = Date.now();
            
            const intentAnalysis = await this.nlpEngine.analyzeUserIntent(
                userInput, 
                projectContext,
                { includeWorkflowRecommendations: true }
            );
            
            const workflowSelection = await this.selectOptimalWorkflow(
                intentAnalysis,
                projectContext, 
                executionOptions
            );

            const selectionDuration = Date.now() - selectionStart;
            this.performanceTracker.recordSelectionTime(executionId, selectionDuration);
            
            if (selectionDuration > this.config.performanceThresholds.selectionTime || 2000) {
                this.emit('performance_warning', {
                    type: 'selection_time_exceeded',
                    executionId,
                    actual: selectionDuration,
                    threshold: 2000
                });
            }

            // Phase 2: Execution Planning and Resource Allocation
            const executionPlan = await this.createExecutionPlan(
                workflowSelection.selectedWorkflow,
                projectContext,
                executionOptions
            );

            await this.resourceManager.allocateResources(executionId, executionPlan);

            // Phase 3: Workflow Execution with Monitoring
            const execution = new WorkflowExecution(
                executionId,
                executionPlan,
                this.createExecutionContext(intentAnalysis, projectContext, executionOptions)
            );

            this.activeWorkflows.set(executionId, execution);
            await this.monitoringSystem.startMonitoring(executionId);

            const result = await this.executeWorkflowPlan(execution);

            // Phase 4: Completion and Analytics
            await this.finalizeExecution(executionId, result);
            
            return {
                executionId,
                status: 'completed',
                result,
                workflowSelection,
                metrics: await this.collectExecutionMetrics(executionId),
                analytics: await this.generateExecutionAnalytics(executionId)
            };

        } catch (error) {
            return await this.handleExecutionError(executionId, error, userInput, projectContext);
        }
    }

    /**
     * Workflow Selection Algorithm
     * Implements multi-criteria decision making for optimal workflow selection
     */
    async selectOptimalWorkflow(intentAnalysis, projectContext, executionOptions) {
        const candidateWorkflows = await this.generateWorkflowCandidates(
            intentAnalysis,
            projectContext
        );

        const scoredWorkflows = await this.scoreWorkflows(
            candidateWorkflows,
            intentAnalysis,
            projectContext,
            executionOptions
        );

        const selectedWorkflow = scoredWorkflows[0];
        const alternatives = scoredWorkflows.slice(1, 3);

        return {
            selectedWorkflow,
            alternatives,
            selectionCriteria: this.generateSelectionCriteria(intentAnalysis, projectContext),
            selectionRationale: this.generateSelectionRationale(selectedWorkflow, scoredWorkflows),
            confidence: this.calculateSelectionConfidence(scoredWorkflows)
        };
    }

    async generateWorkflowCandidates(intentAnalysis, projectContext) {
        const candidates = [];

        // Match intent to workflow patterns
        for (const [category, patterns] of Object.entries(WorkflowPatterns.workflow_patterns)) {
            for (const [patternId, pattern] of Object.entries(patterns)) {
                const compatibility = await this.assessWorkflowCompatibility(
                    pattern,
                    intentAnalysis,
                    projectContext
                );

                if (compatibility.score > 0.3) {  // Minimum threshold
                    candidates.push({
                        ...pattern,
                        category,
                        patternId,
                        compatibility
                    });
                }
            }
        }

        return candidates;
    }

    async scoreWorkflows(workflows, intentAnalysis, projectContext, executionOptions) {
        const scoredWorkflows = [];

        for (const workflow of workflows) {
            const score = await this.calculateWorkflowScore(
                workflow,
                intentAnalysis,
                projectContext,
                executionOptions
            );

            scoredWorkflows.push({
                ...workflow,
                totalScore: score.totalScore,
                scoringBreakdown: score.breakdown,
                fitnessFacotrs: score.fitnessFactors
            });
        }

        return scoredWorkflows.sort((a, b) => b.totalScore - a.totalScore);
    }

    async calculateWorkflowScore(workflow, intentAnalysis, projectContext, executionOptions) {
        const weights = {
            complexityMatch: 0.25,
            urgencyAlignment: 0.20,
            qualitySatisfaction: 0.20, 
            resourceEfficiency: 0.15,
            contextAppropriateness: 0.20
        };

        const scores = {
            complexityMatch: await this.assessComplexityMatch(
                workflow.complexity, 
                intentAnalysis.complexityIndicators,
                projectContext
            ),
            urgencyAlignment: await this.assessUrgencyAlignment(
                workflow.execution_time,
                intentAnalysis.urgencyLevel,
                executionOptions.timeConstraints
            ),
            qualitySatisfaction: await this.assessQualityFit(
                workflow.quality_gates || [],
                executionOptions.qualityRequirements || 'standard',
                projectContext.qualityStandards
            ),
            resourceEfficiency: await this.assessResourceEfficiency(
                workflow.steps,
                projectContext.availableResources,
                this.resourceManager.getCurrentUtilization()
            ),
            contextAppropriateness: await this.assessContextFit(
                workflow.conditions,
                projectContext,
                intentAnalysis.entities
            )
        };

        const totalScore = Object.entries(weights).reduce((total, [factor, weight]) => {
            return total + (scores[factor] * weight);
        }, 0);

        return {
            totalScore,
            breakdown: scores,
            fitnessFactors: this.generateFitnessAnalysis(scores, weights, workflow)
        };
    }

    /**
     * Workflow Execution Coordinator
     * Manages the actual execution of workflow steps with monitoring and adaptation
     */
    async executeWorkflowPlan(execution) {
        const { executionPlan, context } = execution;
        const results = new Map();
        const stepTrace = [];

        try {
            for (const step of executionPlan.steps) {
                const stepStart = Date.now();
                
                let stepResult;
                
                // Execute step based on execution pattern
                switch (step.execution_pattern) {
                    case 'sequential':
                        stepResult = await this.executeSequentialStep(step, context, results);
                        break;
                        
                    case 'parallel_group_a':
                    case 'parallel_group_b':
                        stepResult = await this.executeParallelStep(step, context, results);
                        break;
                        
                    case 'iterative':
                        stepResult = await this.executeIterativeStep(step, context, results);
                        break;
                        
                    case 'conditional':
                        stepResult = await this.executeConditionalStep(step, context, results);
                        break;
                        
                    default:
                        stepResult = await this.executeStandardStep(step, context, results);
                }

                const stepDuration = Date.now() - stepStart;
                
                // Record step completion
                results.set(step.skill_id, stepResult);
                stepTrace.push({
                    step,
                    result: stepResult,
                    duration: stepDuration,
                    timestamp: new Date().toISOString()
                });

                // Apply quality gates if defined
                if (step.quality_gates) {
                    await this.applyQualityGates(step, stepResult, execution);
                }

                // Update monitoring
                await this.monitoringSystem.recordStepCompletion(
                    execution.id,
                    step.skill_id,
                    stepDuration,
                    stepResult
                );

                // Check for adaptive workflow adjustments
                const adaptations = await this.adaptationEngine.analyzeAdaptationOpportunities(
                    execution,
                    results
                );

                if (adaptations.length > 0) {
                    execution = await this.applyWorkflowAdaptations(execution, adaptations);
                }

                // Update execution context with new results
                context.previousResults = results;
                context.stepTrace = stepTrace;
            }

            // Handle parallel execution groups
            await this.executeParallelGroups(executionPlan.parallel_execution_groups, context);

            return this.aggregateWorkflowResults(results, stepTrace);

        } catch (error) {
            return await this.handleStepError(execution, error, results, stepTrace);
        }
    }

    async executeSequentialStep(step, context, previousResults) {
        const skill = await this.skillRegistry.getSkill(step.skill_id);
        const enrichedContext = this.enrichContextWithPreviousResults(context, previousResults);
        
        const skillInput = this.prepareSkillInput(step.parameters, enrichedContext);
        
        return await this.executeSkillWithTimeout(
            skill,
            skillInput,
            step.timeout,
            step.success_criteria
        );
    }

    async executeParallelStep(step, context, previousResults) {
        // Find other steps in the same parallel group
        const groupSteps = execution.executionPlan.steps.filter(s => 
            s.execution_pattern === step.execution_pattern && s.order === step.order
        );

        const parallelPromises = groupSteps.map(groupStep => 
            this.executeSequentialStep(groupStep, context, previousResults)
        );

        const results = await Promise.allSettled(parallelPromises);
        return this.processParallelResults(results, groupSteps);
    }

    async executeIterativeStep(step, context, previousResults) {
        const maxIterations = context.iterationStrategy?.max_iterations || 3;
        const convergenceCriteria = context.iterationStrategy?.convergence_criteria || [];
        
        let iteration = 0;
        let result;
        let converged = false;

        while (iteration < maxIterations && !converged) {
            iteration++;
            
            const iterationContext = {
                ...context,
                iteration,
                previousIterations: result ? [result] : []
            };

            result = await this.executeSequentialStep(step, iterationContext, previousResults);
            
            // Check convergence criteria
            converged = await this.checkConvergenceCriteria(
                convergenceCriteria,
                result,
                iteration,
                context
            );

            if (!converged && iteration < maxIterations) {
                // Apply refinement based on results
                step.parameters = await this.refineParameters(
                    step.parameters,
                    result,
                    context.iterationStrategy?.refinement_focus
                );
            }
        }

        return {
            ...result,
            iterationData: {
                iterations: iteration,
                converged,
                convergence_criteria: convergenceCriteria
            }
        };
    }

    /**
     * Quality Gate Integration
     * Seamless integration with T08 quality gate system
     */
    async applyQualityGates(step, stepResult, execution) {
        if (!step.quality_gates) return;

        for (const gateConfig of step.quality_gates) {
            const gateResult = await this.qualityGateSystem.executeGate(
                gateConfig.gate_id,
                {
                    stepResult,
                    step,
                    execution_context: execution.context,
                    validation_rules: gateConfig.validation_rules
                }
            );

            if (!gateResult.passed) {
                await this.handleQualityGateFailure(
                    execution,
                    step,
                    stepResult,
                    gateResult,
                    gateConfig.failure_action
                );
            }

            // Record gate execution for analytics
            await this.analyticsCollector.recordQualityGateExecution(
                execution.id,
                step.skill_id,
                gateConfig.gate_id,
                gateResult
            );
        }
    }

    async handleQualityGateFailure(execution, step, stepResult, gateResult, failureAction) {
        switch (failureAction) {
            case 'retry_with_guidance':
                return await this.retryStepWithGuidance(step, stepResult, gateResult);
                
            case 'refine_and_retry':
                return await this.refineAndRetryStep(step, stepResult, gateResult);
                
            case 'skip_with_warning':
                return await this.skipStepWithWarning(step, gateResult);
                
            case 'manual_intervention':
                return await this.requestManualIntervention(execution, step, gateResult);
                
            default:
                throw new QualityGateFailureError(
                    `Quality gate ${gateResult.gate_id} failed for step ${step.skill_id}`,
                    { step, gateResult, failureAction }
                );
        }
    }

    /**
     * Error Recovery and Resilience
     * Comprehensive error handling with multiple recovery strategies
     */
    async handleStepError(execution, error, results, stepTrace) {
        const errorClassification = await this.errorRecoveryManager.classifyError(error);
        const recoveryStrategy = await this.errorRecoveryManager.selectRecoveryStrategy(
            errorClassification,
            execution.context,
            results
        );

        const recoveryResult = await this.errorRecoveryManager.executeRecoveryStrategy(
            recoveryStrategy,
            execution,
            error,
            results
        );

        if (recoveryResult.success) {
            // Continue execution with recovered state
            execution.context.recoveryHistory = execution.context.recoveryHistory || [];
            execution.context.recoveryHistory.push({
                error: errorClassification,
                strategy: recoveryStrategy,
                result: recoveryResult,
                timestamp: new Date().toISOString()
            });

            return await this.executeWorkflowPlan(execution);
        } else {
            // Recovery failed, escalate
            throw new WorkflowExecutionError(
                `Workflow execution failed with unrecoverable error`,
                {
                    originalError: error,
                    executionId: execution.id,
                    recoveryAttempt: recoveryResult,
                    stepTrace
                }
            );
        }
    }

    /**
     * Performance Monitoring and Analytics
     * Real-time tracking and comprehensive analytics collection
     */
    async collectExecutionMetrics(executionId) {
        const execution = this.activeWorkflows.get(executionId);
        if (!execution) return null;

        const metrics = await this.monitoringSystem.getExecutionMetrics(executionId);
        const performanceData = await this.performanceTracker.getPerformanceData(executionId);

        return {
            executionId,
            duration: metrics.totalDuration,
            stepMetrics: metrics.stepMetrics,
            performanceMetrics: performanceData,
            qualityMetrics: metrics.qualityMetrics,
            resourceUtilization: metrics.resourceUtilization,
            successRate: metrics.successRate,
            errorSummary: metrics.errorSummary
        };
    }

    async generateExecutionAnalytics(executionId) {
        const metrics = await this.collectExecutionMetrics(executionId);
        const execution = this.activeWorkflows.get(executionId);

        return {
            performanceAnalysis: {
                vsBenchmark: await this.compareToPerformanceBenchmark(metrics),
                bottlenecks: await this.identifyPerformanceBottlenecks(metrics),
                optimizationOpportunities: await this.identifyOptimizationOpportunities(metrics)
            },
            qualityAnalysis: {
                gateEffectiveness: await this.analyzeQualityGateEffectiveness(metrics),
                outputQuality: await this.assessOutputQuality(execution),
                complianceScore: await this.calculateComplianceScore(execution)
            },
            workflowAnalysis: {
                patternEffectiveness: await this.analyzeWorkflowPatternEffectiveness(execution),
                adaptationImpact: await this.analyzeAdaptationImpact(execution),
                selectionAccuracy: await this.assessSelectionAccuracy(execution)
            },
            recommendations: await this.generateOptimizationRecommendations(execution, metrics)
        };
    }

    // Utility methods for execution coordination
    generateExecutionId() {
        return `workflow_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    createExecutionContext(intentAnalysis, projectContext, executionOptions) {
        return {
            intentAnalysis,
            projectContext,
            executionOptions,
            startTime: new Date(),
            previousResults: new Map(),
            stepTrace: [],
            adaptationHistory: [],
            recoveryHistory: []
        };
    }

    async finalizeExecution(executionId, result) {
        const execution = this.activeWorkflows.get(executionId);
        
        await this.monitoringSystem.stopMonitoring(executionId);
        await this.resourceManager.releaseResources(executionId);
        await this.analyticsCollector.finalizeCollection(executionId);
        
        execution.completedAt = new Date();
        execution.result = result;
        
        // Move to completed workflows for analytics
        this.activeWorkflows.delete(executionId);
        
        this.emit('workflow_completed', {
            executionId,
            duration: execution.completedAt - execution.context.startTime,
            success: true,
            result
        });
    }
}

/**
 * Supporting Classes
 */

class WorkflowExecution {
    constructor(id, executionPlan, context) {
        this.id = id;
        this.executionPlan = executionPlan;
        this.context = context;
        this.startedAt = new Date();
        this.status = 'running';
        this.currentStep = null;
        this.completedAt = null;
        this.result = null;
    }
}

class WorkflowMonitoringSystem {
    constructor() {
        this.monitors = new Map();
        this.metricsCollector = new MetricsCollector();
    }

    async initialize() {
        await this.metricsCollector.initialize();
    }

    async startMonitoring(executionId) {
        const monitor = new WorkflowMonitor(executionId);
        this.monitors.set(executionId, monitor);
        await monitor.start();
    }

    async stopMonitoring(executionId) {
        const monitor = this.monitors.get(executionId);
        if (monitor) {
            await monitor.stop();
            this.monitors.delete(executionId);
        }
    }

    async recordStepCompletion(executionId, skillId, duration, result) {
        await this.metricsCollector.recordStepMetric(executionId, {
            skillId,
            duration,
            success: true,
            result: result,
            timestamp: new Date().toISOString()
        });
    }

    async getExecutionMetrics(executionId) {
        return await this.metricsCollector.getMetrics(executionId);
    }
}

// Error Classes
class WorkflowExecutionError extends Error {
    constructor(message, details) {
        super(message);
        this.name = 'WorkflowExecutionError';
        this.details = details;
    }
}

class QualityGateFailureError extends Error {
    constructor(message, details) {
        super(message);
        this.name = 'QualityGateFailureError';
        this.details = details;
    }
}

export {
    WorkflowExecutionEngine,
    WorkflowExecution,
    WorkflowMonitoringSystem,
    WorkflowExecutionError,
    QualityGateFailureError
};