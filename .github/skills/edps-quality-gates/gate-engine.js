/**
 * EDPS Quality Gate System - Core Execution Engine
 * Comprehensive gate validation with workflow integration and intelligent recovery
 * 
 * @fileOverview Main execution engine for quality gates with T07 integration
 * @version 1.0.0
 * @requires fs-extra, lodash, chalk
 */

import fs from 'fs-extra';
import path from 'path';
import { EventEmitter } from 'events';
import _ from 'lodash';
import chalk from 'chalk';

/**
 * Core Quality Gate System with comprehensive validation and recovery capabilities
 */
export class QualityGateSystem extends EventEmitter {
    constructor(config = {}) {
        super();
        
        this.config = {
            defaultTimeout: config.defaultTimeout || 10000,
            parallelExecution: config.parallelExecution || true,
            failureEscalation: config.failureEscalation || true,
            auditLogging: config.auditLogging || true,
            maxRetrites: config.maxRetries || 3,
            performanceMonitoring: config.performanceMonitoring || true,
            ...config
        };

        // Core system components
        this.gateRegistry = new GateRegistry(this.config);
        this.validationEngine = new ValidationEngine(this.config);
        this.remediationSystem = new RemediationSystem(this.config);
        this.auditTrail = new AuditTrailManager(this.config);
        this.integrationLayer = new WorkflowIntegrationLayer(this.config);
        
        // Performance and monitoring systems
        this.performanceMonitor = new GatePerformanceMonitor(this.config);
        this.alertingSystem = new GateAlertingSystem(this.config);
        this.analyticsEngine = new GateAnalyticsEngine(this.config);
        
        // State management
        this.executionCache = new Map();
        this.gateStates = new Map();
        this.pendingExecutions = new Map();
        
        this.initializeSystem();
    }

    async initializeSystem() {
        try {
            console.log(chalk.blue('🔧 Initializing EDPS Quality Gate System...'));
            
            await this.gateRegistry.loadGateDefinitions();
            await this.validationEngine.initialize();
            await this.integrationLayer.connectToWorkflowOrchestrator();
            await this.performanceMonitor.initialize();
            
            this.emit('gate_system_initialized', {
                timestamp: new Date(),
                gates_loaded: this.gateRegistry.getGateCount(),
                validation_rules: this.validationEngine.getRuleCount()
            });
            
            console.log(chalk.green('✅ Quality Gate System initialized successfully'));
            console.log(chalk.cyan(`📊 Loaded ${this.gateRegistry.getGateCount()} gates with ${this.validationEngine.getRuleCount()} validation rules`));
            
        } catch (error) {
            console.error(chalk.red('❌ Failed to initialize Quality Gate System:', error.message));
            throw new SystemInitializationError(`Gate system initialization failed: ${error.message}`);
        }
    }

    /**
     * Main gate execution entry point with comprehensive validation and recovery
     */
    async executeGate(gateId, executionContext, options = {}) {
        const executionStart = performance.now();
        const gateExecutionId = this.generateExecutionId(gateId);
        
        console.log(chalk.blue(`🚪 Executing gate: ${gateId} (${gateExecutionId})`));

        try {
            // Initialize and enrich execution context
            const enrichedContext = await this.enrichExecutionContext(
                executionContext, 
                gateExecutionId,
                options
            );
            
            // Load and validate gate configuration
            const gateConfig = await this.gateRegistry.getGateConfiguration(gateId);
            if (!gateConfig) {
                throw new GateConfigurationError(`Gate configuration not found: ${gateId}`);
            }

            // Execute validation rules with performance monitoring
            const validationResults = await this.executeValidationRules(
                gateConfig.validation_rules,
                enrichedContext,
                gateConfig
            );

            // Aggregate results and determine overall gate outcome
            const gateResult = await this.aggregateValidationResults(
                validationResults,
                gateConfig,
                enrichedContext
            );

            // Handle gate failure with intelligent recovery
            if (!gateResult.passed) {
                gateResult.remediation = await this.remediationSystem.generateRefinementGuidance(
                    gateResult,
                    gateConfig,
                    enrichedContext
                );
                
                // Attempt recovery if configured
                if (gateConfig.failure_actions && this.config.failureEscalation) {
                    const recoveryResult = await this.handleGateFailure(
                        gateResult, 
                        gateConfig, 
                        enrichedContext
                    );
                    gateResult.recovery = recoveryResult;
                }
            }

            // Record execution metrics and audit trail
            const executionTime = performance.now() - executionStart;
            await this.recordGateExecution(gateExecutionId, gateResult, executionTime, gateConfig);
            
            // Emit completion event for monitoring
            this.emit('gate_execution_completed', {
                gate_id: gateId,
                execution_id: gateExecutionId,
                passed: gateResult.passed,
                execution_time: executionTime,
                validation_count: validationResults.length
            });

            console.log(gateResult.passed ? 
                chalk.green(`✅ Gate ${gateId} passed (${Math.round(executionTime)}ms)`) :
                chalk.red(`❌ Gate ${gateId} failed (${Math.round(executionTime)}ms)`)
            );

            return gateResult;

        } catch (error) {
            const executionTime = performance.now() - executionStart;
            await this.handleGateExecutionError(gateExecutionId, gateId, error, executionTime);
            throw error;
        }
    }

    /**
     * Execute multiple gates with parallel processing and dependency management
     */
    async executeMultipleGates(gateConfigurations, executionContext, options = {}) {
        console.log(chalk.blue(`🚪🚪 Executing ${gateConfigurations.length} gates...`));
        
        const executionStart = performance.now();
        const results = new Map();
        
        try {
            // Build dependency graph for ordered execution
            const dependencyGraph = this.buildGateDependencyGraph(gateConfigurations);
            const executionPlan = this.createExecutionPlan(dependencyGraph, options.parallelism);
            
            // Execute gates in planned sequence with parallel optimization
            for (const executionStage of executionPlan) {
                const stagePromises = executionStage.map(async (gateConfig) => {
                    const gateResult = await this.executeGate(
                        gateConfig.gate_id, 
                        executionContext,
                        { ...options, stage: executionStage }
                    );
                    results.set(gateConfig.gate_id, gateResult);
                    return gateResult;
                });
                
                // Wait for all gates in stage to complete
                await Promise.allSettled(stagePromises);
            }

            const totalTime = performance.now() - executionStart;
            const overallResult = this.aggregateMultiGateResults(results, totalTime);
            
            console.log(chalk.green(`✅ Completed ${gateConfigurations.length} gates in ${Math.round(totalTime)}ms`));
            
            return overallResult;

        } catch (error) {
            const totalTime = performance.now() - executionStart;
            console.error(chalk.red(`❌ Multi-gate execution failed after ${Math.round(totalTime)}ms:`, error.message));
            throw new MultiGateExecutionError(`Multi-gate execution failed: ${error.message}`);
        }
    }

    /**
     * Execute validation rules with delegation support and performance optimization
     */
    async executeValidationRules(validationRules, context, gateConfig) {
        const ruleExecutions = validationRules.map(rule => {
            return {
                rule,
                execute: () => this.executeValidationRule(rule, context, gateConfig)
            };
        });

        if (this.config.parallelExecution && !this.hasRuleDependencies(validationRules)) {
            // Execute rules in parallel for performance optimization
            const rulePromises = ruleExecutions.map(ruleExecution => 
                ruleExecution.execute().catch(error => ({
                    rule_id: ruleExecution.rule.rule_id,
                    status: 'error',
                    error: error.message,
                    timestamp: new Date()
                }))
            );
            
            return await Promise.allSettled(rulePromises).then(results =>
                results.map(result => result.status === 'fulfilled' ? result.value : result.reason)
            );
        } else {
            // Sequential execution for rule dependencies
            const results = [];
            for (const ruleExecution of ruleExecutions) {
                try {
                    const result = await ruleExecution.execute();
                    results.push(result);
                } catch (error) {
                    results.push({
                        rule_id: ruleExecution.rule.rule_id,
                        status: 'error',
                        error: error.message,
                        timestamp: new Date()
                    });
                }
            }
            return results;
        }
    }

    /**
     * Execute individual validation rule with delegation and built-in validation logic
     */
    async executeValidationRule(rule, context, gateConfig) {
        const ruleStart = performance.now();
        
        console.log(chalk.cyan(`  🔍 Validating rule: ${rule.rule_id}`));

        try {
            let ruleResult;

            // Determine validation strategy based on rule configuration
            if (rule.parameters?.delegation_partner) {
                console.log(chalk.yellow(`    ↗️ Delegating to ${rule.parameters.delegation_partner}`));
                ruleResult = await this.delegateValidation(rule, context, gateConfig);
            } else {
                // Execute built-in validation logic
                ruleResult = await this.validationEngine.executeRule(rule, context, gateConfig);
            }

            const executionTime = performance.now() - ruleStart;
            
            // Enhance result with execution metadata
            const enhancedResult = {
                ...ruleResult,
                rule_id: rule.rule_id,
                execution_time: executionTime,
                timestamp: new Date(),
                validation_method: rule.parameters?.delegation_partner || 'built_in'
            };

            console.log(enhancedResult.passed ? 
                chalk.green(`    ✅ Rule ${rule.rule_id} passed (${Math.round(executionTime)}ms)`) :
                chalk.red(`    ❌ Rule ${rule.rule_id} failed (${Math.round(executionTime)}ms)`)
            );

            return enhancedResult;

        } catch (error) {
            const executionTime = performance.now() - ruleStart;
            console.error(chalk.red(`    💥 Rule ${rule.rule_id} error (${Math.round(executionTime)}ms):`, error.message));
            
            return {
                rule_id: rule.rule_id,
                status: 'error',
                passed: false,
                error: error.message,
                execution_time: executionTime,
                timestamp: new Date()
            };
        }
    }

    /**
     * Delegate validation to specialized skills (T04, hierarchy-validation, etc.)
     */
    async delegateValidation(rule, context, gateConfig) {
        const delegationPartner = rule.parameters.delegation_partner;

        switch (delegationPartner) {
            case 'diagram-generatecollaboration':
                return await this.delegateToT04Validation(rule, context, gateConfig);
                
            case 'hierarchy-validation':
                return await this.delegateToHierarchyValidation(rule, context, gateConfig);
                
            default:
                return await this.delegateToGenericSkill(delegationPartner, rule, context, gateConfig);
        }
    }

    /**
     * Delegate to T04 diagram-generatecollaboration for boundary validation (97% accuracy)
     */
    async delegateToT04Validation(rule, context, gateConfig) {
        try {
            const t04ValidationService = await this.integrationLayer.getT04ValidationService();
            
            const validationRequest = {
                validation_type: rule.rule_id,
                input_data: context.stepResult || context.input_data,
                vr_rules: {
                    vr1_enabled: rule.rule_id.includes('vr1') || rule.rule_id.includes('boundary'),
                    vr2_enabled: rule.rule_id.includes('vr2') || rule.rule_id.includes('participant'),
                    vr3_enabled: rule.rule_id.includes('vr3') || rule.rule_id.includes('message'),
                    vr4_enabled: rule.rule_id.includes('vr4') || rule.rule_id.includes('hierarchy')
                },
                parameters: rule.parameters,
                context: context,
                gate_config: gateConfig
            };

            const delegationResult = await t04ValidationService.validateBoundaryCompliance(validationRequest);
            
            return {
                rule_id: rule.rule_id,
                status: delegationResult.status,
                passed: delegationResult.validation_passed,
                confidence: delegationResult.confidence || 0.97, // T04's documented accuracy
                validation_details: delegationResult.details,
                delegation_partner: 'diagram-generatecollaboration',
                t04_specific_results: delegationResult
            };

        } catch (error) {
            console.error(chalk.red(`Failed to delegate to T04 for rule ${rule.rule_id}:`, error.message));
            return {
                rule_id: rule.rule_id,
                status: 'delegation_error',
                passed: false,
                error: `T04 delegation failed: ${error.message}`,
                delegation_partner: 'diagram-generatecollaboration'
            };
        }
    }

    /**
     * Delegate to hierarchy-validation for structural integrity checking
     */
    async delegateToHierarchyValidation(rule, context, gateConfig) {
        try {
            const hierarchyValidationService = await this.integrationLayer.getHierarchyValidationService();
            
            const validationRequest = {
                target_hierarchy: context.stepResult || context.hierarchy_data,
                validation_scope: rule.parameters,
                structural_checks: {
                    cross_level_consistency: rule.parameters.cross_level_consistency || true,
                    decomposition_completeness: rule.parameters.decomposition_completeness || true,
                    parent_child_relationships: rule.parameters.parent_child_relationships || true,
                    boundary_inheritance: rule.parameters.boundary_inheritance || true
                },
                context: context,
                gate_config: gateConfig
            };

            const delegationResult = await hierarchyValidationService.validateStructuralIntegrity(validationRequest);
            
            return {
                rule_id: rule.rule_id,
                status: delegationResult.status,
                passed: delegationResult.structural_integrity_passed,
                confidence: delegationResult.confidence || 0.95,
                validation_details: delegationResult.details || delegationResult.structural_analysis,
                delegation_partner: 'hierarchy-validation',
                hierarchy_specific_results: delegationResult
            };

        } catch (error) {
            console.error(chalk.red(`Failed to delegate to hierarchy-validation for rule ${rule.rule_id}:`, error.message));
            return {
                rule_id: rule.rule_id,
                status: 'delegation_error',
                passed: false,
                error: `Hierarchy validation delegation failed: ${error.message}`,
                delegation_partner: 'hierarchy-validation'
            };
        }
    }

    /**
     * Handle gate failure with intelligent recovery strategies
     */
    async handleGateFailure(gateResult, gateConfig, context) {
        const failureAction = this.determineFailureAction(gateResult, gateConfig, context);

        console.log(chalk.yellow(`🔄 Handling gate failure with action: ${failureAction}`));

        switch (failureAction) {
            case 'retry_with_guidance':
                return await this.retryWithGuidance(gateResult, gateConfig, context);
                
            case 'refine_and_retry':
                return await this.refineAndRetry(gateResult, gateConfig, context);
                
            case 'adaptive_workflow':
                return await this.triggerWorkflowAdaptation(gateResult, gateConfig, context);
                
            case 'skip_with_warning':
                return await this.skipWithWarning(gateResult, gateConfig, context);
                
            case 'escalate_to_manual':
                return await this.escalateToManualReview(gateResult, gateConfig, context);
                
            case 'abort_workflow':
                return await this.abortWorkflow(gateResult, gateConfig, context);
                
            default:
                throw new GateFailureError(`Unknown failure action: ${failureAction}`);
        }
    }

    determineFailureAction(gateResult, gateConfig, context) {
        // Determine failure action based on severity, retry count, and configuration
        const severity = gateConfig.severity || 'moderate';
        const retryCount = context.retry_count || 0;
        const maxRetries = gateConfig.retry_count || this.config.maxRetries;

        const failureActions = gateConfig.failure_actions || {
            critical: 'retry_with_guidance',
            high: 'refine_and_retry',
            moderate: 'adaptive_workflow',
            warning: 'skip_with_warning'
        };

        // Check retry exhaustion
        if (retryCount >= maxRetries) {
            return severity === 'critical' ? 'escalate_to_manual' : 'adaptive_workflow';
        }

        return failureActions[severity] || 'retry_with_guidance';
    }

    async retryWithGuidance(gateResult, gateConfig, context) {
        console.log(chalk.yellow('🔄 Applying remediation guidance for retry...'));
        
        // Generate specific remediation guidance
        const guidance = await this.remediationSystem.generateRefinementGuidance(
            gateResult,
            gateConfig,
            context
        );

        // Apply guidance to refine parameters
        const refinedParameters = await this.remediationSystem.applyRemediationGuidance(
            guidance,
            context.step?.parameters || context.parameters || {}
        );

        return {
            action: 'retry_with_guidance',
            refined_parameters: refinedParameters,
            guidance: guidance,
            retry_context: {
                ...context,
                retry_count: (context.retry_count || 0) + 1,
                previous_failure: gateResult,
                remediation_applied: guidance
            }
        };
    }

    async triggerWorkflowAdaptation(gateResult, gateConfig, context) {
        console.log(chalk.blue('🔄 Triggering workflow adaptation...'));
        
        // Integration with T07 workflow orchestrator for adaptive execution
        const workflowOrchestrator = await this.integrationLayer.getWorkflowOrchestrator();
        
        const adaptationRequest = {
            reason: 'quality_gate_failure',
            gate_result: gateResult,
            gate_config: gateConfig,
            context: context,
            suggested_adaptations: [
                'alternative_skill_substitution',
                'parallel_execution_optimization',
                'quality_criteria_adjustment',
                'workflow_path_modification'
            ]
        };

        const adaptationResult = await workflowOrchestrator.analyzeAndApplyAdaptation(adaptationRequest);
        
        return {
            action: 'adaptive_workflow',
            adaptation_result: adaptationResult,
            workflow_changes: adaptationResult.applied_changes,
            context_modifications: adaptationResult.context_updates
        };
    }

    /**
     * Generate unique execution identifier for tracking
     */
    generateExecutionId(gateId) {
        const timestamp = Date.now();
        const randomSuffix = Math.random().toString(36).substring(2, 8);
        return `${gateId}_${timestamp}_${randomSuffix}`;
    }

    /**
     * Enrich execution context with metadata and validation requirements
     */
    async enrichExecutionContext(context, executionId, options = {}) {
        return {
            ...context,
            execution_id: executionId,
            timestamp: new Date(),
            gate_system_version: '1.0.0',
            options: options,
            workflow_metadata: await this.integrationLayer.getWorkflowMetadata(context),
            validation_requirements: await this.determineValidationRequirements(context),
            performance_tracking: this.config.performanceMonitoring
        };
    }

    /**
     * Aggregate validation results into overall gate outcome
     */
    async aggregateValidationResults(validationResults, gateConfig, context) {
        const criticalFailures = validationResults.filter(r => 
            !r.passed && (r.severity === 'critical' || gateConfig.severity === 'critical')
        );
        
        const highFailures = validationResults.filter(r => 
            !r.passed && (r.severity === 'high' || r.severity === 'critical')
        );
        
        const allFailures = validationResults.filter(r => !r.passed);

        // Determine overall pass/fail based on failure severity and configuration
        const passed = criticalFailures.length === 0 && 
                      (gateConfig.severity !== 'high' || highFailures.length === 0);

        const overallResult = {
            gate_id: gateConfig.id,
            execution_id: context.execution_id,
            passed: passed,
            validation_results: validationResults,
            summary: {
                total_rules: validationResults.length,
                passed_rules: validationResults.filter(r => r.passed).length,
                failed_rules: allFailures.length,
                critical_failures: criticalFailures.length,
                high_failures: highFailures.length
            },
            confidence_score: this.calculateConfidenceScore(validationResults),
            recommendations: this.generateRecommendations(validationResults, gateConfig),
            timestamp: new Date()
        };

        return overallResult;
    }

    calculateConfidenceScore(validationResults) {
        if (validationResults.length === 0) return 0;
        
        const confidenceValues = validationResults
            .map(r => r.confidence || (r.passed ? 0.9 : 0.1))
            .filter(c => c > 0);
        
        return confidenceValues.length > 0 ? 
            confidenceValues.reduce((acc, conf) => acc + conf, 0) / confidenceValues.length : 0.5;
    }

    generateRecommendations(validationResults, gateConfig) {
        const recommendations = [];
        
        const failures = validationResults.filter(r => !r.passed);
        if (failures.length > 0) {
            recommendations.push({
                type: 'failure_resolution',
                priority: 'high',
                description: `Address ${failures.length} validation failures`,
                failed_rules: failures.map(f => f.rule_id)
            });
        }

        const lowConfidence = validationResults.filter(r => (r.confidence || 1) < 0.7);
        if (lowConfidence.length > 0) {
            recommendations.push({
                type: 'confidence_improvement',
                priority: 'medium',
                description: `Review validation results with low confidence`,
                affected_rules: lowConfidence.map(r => r.rule_id)
            });
        }

        return recommendations;
    }

    /**
     * Record gate execution for audit trail and analytics
     */
    async recordGateExecution(executionId, gateResult, executionTime, gateConfig) {
        const auditRecord = {
            execution_id: executionId,
            gate_id: gateResult.gate_id,
            timestamp: new Date(),
            execution_time: executionTime,
            result: gateResult,
            configuration: gateConfig,
            system_metadata: {
                version: '1.0.0',
                node_version: process.version,
                memory_usage: process.memoryUsage()
            }
        };

        await this.auditTrail.recordExecution(auditRecord);
        await this.performanceMonitor.recordMetrics(auditRecord);
        
        if (this.config.auditLogging) {
            console.log(chalk.gray(`📝 Recorded execution: ${executionId}`));
        }
    }

    /**
     * Handle gate execution errors with comprehensive logging
     */
    async handleGateExecutionError(executionId, gateId, error, executionTime) {
        const errorRecord = {
            execution_id: executionId,
            gate_id: gateId,
            error: {
                message: error.message,
                stack: error.stack,
                name: error.name
            },
            execution_time: executionTime,
            timestamp: new Date(),
            system_metadata: {
                version: '1.0.0',
                memory_usage: process.memoryUsage()
            }
        };

        await this.auditTrail.recordError(errorRecord);
        
        this.emit('gate_execution_error', errorRecord);
        
        console.error(chalk.red(`💥 Gate execution error for ${gateId} (${executionId}):`, error.message));
    }
}

/**
 * Gate Registry - Manages gate definitions and configurations
 */
export class GateRegistry {
    constructor(config = {}) {
        this.config = config;
        this.gates = new Map();
        this.gateDefinitionsPath = path.join(process.cwd(), '.github', 'skills', 'edps-quality-gates', 'gate-definitions.json');
    }

    async loadGateDefinitions() {
        try {
            console.log(chalk.blue('📖 Loading gate definitions...'));
            
            const definitionsFile = await fs.readFile(this.gateDefinitionsPath, 'utf8');
            const definitions = JSON.parse(definitionsFile);
            
            let gateCount = 0;
            
            // Load gates from all categories
            for (const [categoryName, category] of Object.entries(definitions.gate_categories)) {
                for (const [gateName, gateConfig] of Object.entries(category.gates)) {
                    this.gates.set(gateConfig.id, {
                        ...gateConfig,
                        category: categoryName
                    });
                    gateCount++;
                }
            }

            console.log(chalk.green(`✅ Loaded ${gateCount} gate definitions from ${Object.keys(definitions.gate_categories).length} categories`));
            
        } catch (error) {
            console.error(chalk.red('❌ Failed to load gate definitions:', error.message));
            throw new GateConfigurationError(`Failed to load gate definitions: ${error.message}`);
        }
    }

    async getGateConfiguration(gateId) {
        const config = this.gates.get(gateId);
        if (!config) {
            throw new GateConfigurationError(`Gate configuration not found: ${gateId}`);
        }
        return config;
    }

    getGateCount() {
        return this.gates.size;
    }

    getGatesByCategory(category) {
        return Array.from(this.gates.values()).filter(gate => gate.category === category);
    }

    async registerGateConfiguration(gateConfig) {
        this.gates.set(gateConfig.id, gateConfig);
    }
}

/**
 * Validation Engine - Executes built-in validation rules
 */
export class ValidationEngine {
    constructor(config = {}) {
        this.config = config;
        this.validators = new Map();
        this.ruleCount = 0;
    }

    async initialize() {
        // Register built-in validation functions
        this.registerValidator('validateRequiredFields', this.validateRequiredFields.bind(this));
        this.registerValidator('assessContentDepth', this.assessContentDepth.bind(this));
        this.registerValidator('validateSchema', this.validateSchema.bind(this));
        this.registerValidator('validateFormatting', this.validateFormatting.bind(this));
        this.registerValidator('calculateQualityScore', this.calculateQualityScore.bind(this));
        this.registerValidator('assessStakeholderValue', this.assessStakeholderValue.bind(this));
        this.registerValidator('checkPrerequisites', this.checkPrerequisites.bind(this));
        this.registerValidator('validateExecutionOrder', this.validateExecutionOrder.bind(this));
        this.registerValidator('checkResourceAvailability', this.checkResourceAvailability.bind(this));
        
        console.log(chalk.green(`✅ Initialized validation engine with ${this.validators.size} validators`));
    }

    registerValidator(name, validatorFunction) {
        this.validators.set(name, validatorFunction);
        this.ruleCount++;
    }

    async executeRule(rule, context, gateConfig) {
        const validatorFunction = this.validators.get(rule.check_function);
        if (!validatorFunction) {
            throw new ValidationError(`Validator function not found: ${rule.check_function}`);
        }

        try {
            const result = await validatorFunction(rule, context, gateConfig);
            return {
                ...result,
                rule_id: rule.rule_id,
                validation_method: 'built_in'
            };
        } catch (error) {
            throw new ValidationError(`Validation rule execution failed for ${rule.rule_id}: ${error.message}`);
        }
    }

    getRuleCount() {
        return this.ruleCount;
    }

    // Built-in validation functions
    async validateRequiredFields(rule, context, gateConfig) {
        const data = context.stepResult || context.input_data || {};
        const requiredFields = rule.parameters.required_fields || [];
        const minContentLength = rule.parameters.minimum_content_length || 0;
        
        const missingFields = [];
        const insufficientFields = [];
        
        for (const field of requiredFields) {
            const value = _.get(data, field);
            
            if (value === undefined || value === null || value === '') {
                missingFields.push(field);
            } else if (typeof value === 'string' && value.trim().length < minContentLength) {
                insufficientFields.push(field);
            }
        }
        
        const passed = missingFields.length === 0 && insufficientFields.length === 0;
        
        return {
            passed,
            confidence: passed ? 0.95 : 0.8,
            details: {
                required_fields: requiredFields,
                missing_fields: missingFields,
                insufficient_fields: insufficientFields,
                success_criteria_met: passed
            },
            validation_data: {
                total_required: requiredFields.length,
                missing_count: missingFields.length,
                insufficient_count: insufficientFields.length
            }
        };
    }

    async assessContentDepth(rule, context, gateConfig) {
        const data = context.stepResult || context.input_data || {};
        const minWordCount = rule.parameters.minimum_word_count || 50;
        const meaningfulRatio = rule.parameters.meaningful_content_ratio || 0.8;
        
        // Convert data to text for analysis
        const textContent = this.extractTextContent(data);
        const wordCount = textContent.split(/\s+/).filter(word => word.length > 0).length;
        
        // Analyze content depth
        const placeholderPatterns = ['TODO', 'TBD', 'PLACEHOLDER', '...', 'Lorem ipsum'];
        const placeholderCount = placeholderPatterns.reduce((count, pattern) => 
            count + (textContent.match(new RegExp(pattern, 'gi')) || []).length, 0
        );
        
        const meaningfulContentScore = Math.max(0, 1 - (placeholderCount / wordCount));
        const depthScore = Math.min(1, wordCount / minWordCount);
        
        const passed = wordCount >= minWordCount && meaningfulContentScore >= meaningfulRatio;
        
        return {
            passed,
            confidence: 0.85,
            details: {
                word_count: wordCount,
                minimum_required: minWordCount,
                meaningful_content_score: meaningfulContentScore,
                meaningful_ratio_required: meaningfulRatio,
                placeholder_count: placeholderCount,
                depth_score: depthScore
            }
        };
    }

    async calculateQualityScore(rule, context, gateConfig) {
        const weights = {
            clarity: rule.parameters.clarity_weight || 0.3,
            completeness: rule.parameters.completeness_weight || 0.3,
            accuracy: rule.parameters.accuracy_weight || 0.2,
            usefulness: rule.parameters.usefulness_weight || 0.2
        };
        
        const minScore = rule.parameters.minimum_score || 0.75;
        
        // Calculate individual dimension scores
        const scores = {
            clarity: await this.assessClarity(context),
            completeness: await this.assessCompleteness(context),
            accuracy: await this.assessAccuracy(context),
            usefulness: await this.assessUsefulness(context)
        };
        
        // Calculate weighted overall score
        const overallScore = Object.entries(weights).reduce((total, [dimension, weight]) => 
            total + (scores[dimension] * weight), 0
        );
        
        const passed = overallScore >= minScore;
        
        return {
            passed,
            confidence: 0.8,
            details: {
                overall_score: overallScore,
                minimum_required: minScore,
                dimension_scores: scores,
                weights_applied: weights
            }
        };
    }

    // Helper methods for quality assessment
    extractTextContent(data) {
        if (typeof data === 'string') return data;
        if (typeof data === 'object') {
            return JSON.stringify(data, null, 2);
        }
        return String(data);
    }

    async assessClarity(context) {
        // Simple clarity assessment based on sentence structure and readability
        const text = this.extractTextContent(context.stepResult || context.input_data);
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 10);
        const avgSentenceLength = sentences.reduce((acc, sent) => acc + sent.split(' ').length, 0) / sentences.length;
        
        // Score based on reasonable sentence length (10-25 words optimal)
        return Math.max(0.3, 1 - Math.abs(avgSentenceLength - 17.5) / 17.5);
    }

    async assessCompleteness(context) {
        // Assess completeness based on expected sections and content depth
        const data = context.stepResult || context.input_data || {};
        const standardSections = ['title', 'description', 'objectives', 'details'];
        
        const presentSections = standardSections.filter(section => 
            data[section] && String(data[section]).trim().length > 10
        );
        
        return presentSections.length / standardSections.length;
    }

    async assessAccuracy(context) {
        // Basic accuracy assessment - could be enhanced with domain-specific rules
        const text = this.extractTextContent(context.stepResult || context.input_data);
        
        // Check for consistency indicators
        const hasSpecificDetails = /\b\d+\b/.test(text); // Contains numbers/specifics
        const hasStructuredContent = text.includes(':') || text.includes('-') || text.includes('*');
        
        return (hasSpecificDetails ? 0.5 : 0) + (hasStructuredContent ? 0.5 : 0);
    }

    async assessUsefulness(context) {
        // Assess usefulness based on actionable content and practical value
        const text = this.extractTextContent(context.stepResult || context.input_data);
        
        const actionWords = ['implement', 'execute', 'create', 'develop', 'analyze', 'validate', 'ensure', 'provide'];
        const hasActionableContent = actionWords.some(word => 
            text.toLowerCase().includes(word.toLowerCase())
        );
        
        const hasExamples = text.includes('example') || text.includes('e.g.') || text.includes('for instance');
        
        return (hasActionableContent ? 0.7 : 0.3) + (hasExamples ? 0.3 : 0);
    }
}

// Custom error classes
export class GateConfigurationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'GateConfigurationError';
    }
}

export class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ValidationError';
    }
}

export class SystemInitializationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'SystemInitializationError';
    }
}

export class MultiGateExecutionError extends Error {
    constructor(message) {
        super(message);
        this.name = 'MultiGateExecutionError';
    }
}

export class GateFailureError extends Error {
    constructor(message) {
        super(message);
        this.name = 'GateFailureError';
    }
}