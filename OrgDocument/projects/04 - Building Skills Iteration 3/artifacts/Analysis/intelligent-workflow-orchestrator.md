# Intelligent Workflow Orchestration System

## Advanced Workflow Engine

### Dynamic Workflow Generator
```javascript
class IntelligentWorkflowOrchestrator {
    constructor() {
        this.workflowPatterns = new WorkflowPatternLibrary();
        this.executionEngine = new SkillExecutionEngine();
        this.monitoringSystem = new WorkflowMonitoringSystem();
        this.adaptationEngine = new AdaptiveWorkflowEngine();
        
        this.initializeWorkflowTemplates();
        this.initializeExecutionPatterns();
        this.initializeOptimizationRules();
    }

    async orchestrateWorkflow(skillRecommendations, intentAnalysis, projectContext) {
        // Generate workflow plans
        const workflowOptions = await this.generateWorkflowOptions(skillRecommendations, intentAnalysis, projectContext);
        
        // Select optimal workflow
        const selectedWorkflow = await this.selectOptimalWorkflow(workflowOptions, projectContext);
        
        // Create execution plan
        const executionPlan = await this.createExecutionPlan(selectedWorkflow, projectContext);
        
        // Set up monitoring
        const monitoringContext = await this.setupMonitoring(executionPlan);
        
        return {
            workflow: selectedWorkflow,
            execution_plan: executionPlan,
            monitoring: monitoringContext,
            alternatives: workflowOptions.filter(opt => opt.id !== selectedWorkflow.id),
            metadata: {
                generated_at: new Date().toISOString(),
                complexity: selectedWorkflow.complexity,
                estimated_duration: selectedWorkflow.estimated_duration,
                confidence: selectedWorkflow.confidence
            }
        };
    }

    async generateWorkflowOptions(skillRecommendations, intentAnalysis, projectContext) {
        const workflowTemplates = {
            // Fast Track Workflows
            "requirements_quick_analysis": {
                pattern: "linear",
                skills: ["requirements-ingest", "goals-extract", "process-w5h"],
                parallelizable: false,
                estimated_duration: "30-45 minutes",
                complexity: "low",
                conditions: {
                    requirements: ["simple", "well_defined"],
                    urgency: ["high"],
                    experience: ["any"]
                },
                optimization_hints: {
                    skip_validation: true,
                    use_templates: true,
                    minimal_documentation: true
                }
            },

            "domain_discovery_rapid": {
                pattern: "parallel_convergence",
                skills: ["requirements-ingest", "domain-extractconcepts", "goals-extract"],
                parallelizable: true,
                estimated_duration: "45-60 minutes", 
                complexity: "medium",
                conditions: {
                    requirements: ["moderate", "clear_scope"],
                    urgency: ["high", "medium"],
                    team_size: ["multiple"]
                },
                optimization_hints: {
                    parallel_execution: ["requirements-ingest", "goals-extract"],
                    quick_convergence: "domain-extractconcepts"
                }
            },

            // Standard Workflows
            "complete_requirements_analysis": {
                pattern: "sequential_with_feedback",
                skills: [
                    "requirements-ingest",
                    "goals-extract", 
                    "process-w5h",
                    "domain-extractconcepts",
                    "domain-alignentities",
                    "requirements-merge"
                ],
                parallelizable: "partial",
                estimated_duration: "2-3 hours",
                complexity: "medium",
                conditions: {
                    requirements: ["complex", "multiple_sources"],
                    quality: ["high"],
                    documentation: ["comprehensive"]
                },
                validation_gates: [
                    { after: "requirements-ingest", check: "requirements_quality" },
                    { after: "domain-alignentities", check: "domain_consistency" }
                ]
            },

            "end_to_end_process_design": {
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
                parallelizable: "strategic",
                estimated_duration: "4-6 hours",
                complexity: "high",
                conditions: {
                    scope: ["large", "organizational"],
                    methodology: ["edps"],
                    deliverable: ["comprehensive"]
                },
                strategic_points: [
                    { after: "domain-extractconcepts", decision: "depth_vs_breadth" },
                    { after: "diagram-generatecollaboration", decision: "hierarchy_depth" },
                    { after: "hierarchy-management", decision: "validation_thoroughness" }
                ]
            },

            // Specialized Workflows 
            "hierarchy_deep_dive": {
                pattern: "iterative_refinement",
                skills: [
                    "diagram-generatecollaboration",
                    "hierarchy-management",
                    "hierarchy-validation",
                    "change-impact-analysis",
                    "edps-compliance",
                    "documentation-automation"
                ],
                parallelizable: false,
                estimated_duration: "3-4 hours",
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

            "integration_and_validation": {
                pattern: "validation_cascade",
                skills: [
                    "hierarchy-validation",
                    "edps-compliance", 
                    "integration-testing",
                    "change-impact-analysis"
                ],
                parallelizable: true,
                estimated_duration: "1-2 hours",
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

            // Maintenance Workflows
            "model_evolution": {
                pattern: "change_propagation",
                skills: [
                    "change-impact-analysis",
                    "model-integration",
                    "process-merge",
                    "orgmodel-update",
                    "hierarchy-validation"
                ],
                parallelizable: "careful",
                estimated_duration: "2-4 hours",
                complexity: "high",
                conditions: {
                    change_type: ["model_update", "process_modification"],
                    has_existing_models: true,
                    impact_scope: ["medium", "large"]
                },
                change_strategy: {
                    impact_first: true,
                    staged_rollout: true,
                    rollback_plan: true
                }
            }
        };

        const applicableWorkflows = [];
        
        for (const [templateId, template] of Object.entries(workflowTemplates)) {
            const applicability = await this.assessWorkflowApplicability(template, skillRecommendations, intentAnalysis, projectContext);
            
            if (applicability.applicable) {
                const customizedWorkflow = await this.customizeWorkflow(template, skillRecommendations, projectContext);
                customizedWorkflow.id = templateId;
                customizedWorkflow.applicability_score = applicability.score;
                customizedWorkflow.customizations = applicability.customizations;
                
                applicableWorkflows.push(customizedWorkflow);
            }
        }

        // Generate custom workflows if no templates match well
        if (applicableWorkflows.length === 0 || Math.max(...applicableWorkflows.map(w => w.applicability_score)) < 0.6) {
            const customWorkflow = await this.generateCustomWorkflow(skillRecommendations, intentAnalysis, projectContext);
            applicableWorkflows.push(customWorkflow);
        }

        // Sort by applicability and optimization potential
        return applicableWorkflows.sort((a, b) => {
            const scoreA = a.applicability_score + (a.optimization_potential || 0) * 0.3;
            const scoreB = b.applicability_score + (b.optimization_potential || 0) * 0.3;
            return scoreB - scoreA;
        });
    }

    async assessWorkflowApplicability(template, skillRecommendations, intentAnalysis, projectContext) {
        let score = 0;
        const customizations = [];
        
        // Skill overlap assessment
        const templateSkills = new Set(template.skills);
        const recommendedSkills = new Set(skillRecommendations.map(r => r.skill));
        const intersection = new Set([...templateSkills].filter(x => recommendedSkills.has(x)));
        const skillOverlap = intersection.size / Math.max(templateSkills.size, recommendedSkills.size);
        score += skillOverlap * 0.4;
        
        // Condition matching
        const conditions = template.conditions || {};
        let conditionScore = 0;
        let conditionCount = 0;
        
        for (const [condition, expectedValues] of Object.entries(conditions)) {
            conditionCount++;
            const contextValue = this.getContextValue(condition, projectContext, intentAnalysis);
            
            if (Array.isArray(expectedValues)) {
                if (expectedValues.includes(contextValue)) {
                    conditionScore += 1;
                } else {
                    // Suggest customization
                    customizations.push({
                        type: "condition_adaptation",
                        condition: condition,
                        expected: expectedValues,
                        actual: contextValue,
                        suggestion: this.suggestConditionAdaptation(condition, expectedValues, contextValue)
                    });
                }
            } else if (expectedValues === contextValue) {
                conditionScore += 1;
            }
        }
        
        if (conditionCount > 0) {
            score += (conditionScore / conditionCount) * 0.3;
        } else {
            score += 0.3; // No conditions = always applicable
        }
        
        // Intent alignment
        const intentAlignment = this.assessIntentAlignment(template, intentAnalysis);
        score += intentAlignment * 0.3;
        
        // Resource and constraint satisfaction
        const constraintSatisfaction = this.assessConstraintSatisfaction(template, projectContext);
        score += constraintSatisfaction * 0.1; // Lighter weight for constraints
        
        return {
            applicable: score >= 0.5,
            score: score,
            customizations: customizations,
            breakdown: {
                skill_overlap: skillOverlap * 0.4,
                condition_match: conditionCount > 0 ? (conditionScore / conditionCount) * 0.3 : 0.3,
                intent_alignment: intentAlignment * 0.3,
                constraint_satisfaction: constraintSatisfaction * 0.1
            }
        };
    }

    getContextValue(condition, projectContext, intentAnalysis) {
        const contextMappings = {
            requirements: () => {
                if (!projectContext.hasRequirements) return "missing";
                if (projectContext.requirementSources > 3) return "complex";
                if (projectContext.requirementSources > 1) return "moderate";
                return "simple";
            },
            urgency: () => intentAnalysis.urgency_level,
            complexity: () => intentAnalysis.complexity_indicators,
            has_collaboration_diagram: () => Boolean(projectContext.hasCollaborationDiagram),
            has_existing_models: () => Boolean(projectContext.hasExistingModels),
            scope: () => {
                const artifactCount = Object.keys(projectContext.availableArtifacts || {}).length;
                if (artifactCount > 10) return "large";
                if (artifactCount > 3) return "medium";
                return "small";
            },
            methodology: () => projectContext.methodology || "unknown",
            team_size: () => {
                // Infer from context or default
                return projectContext.teamSize || "single";
            }
        };
        
        const mapper = contextMappings[condition];
        return mapper ? mapper() : "unknown";
    }

    async generateCustomWorkflow(skillRecommendations, intentAnalysis, projectContext) {
        // Create a custom workflow based on skill dependencies and patterns
        const skills = skillRecommendations.map(r => r.skill);
        
        // Analyze skill dependencies to determine execution order
        const executionGraph = await this.buildExecutionGraph(skills, projectContext);
        const optimizedSequence = await this.optimizeExecutionSequence(executionGraph, intentAnalysis);
        
        // Determine pattern based on dependencies and parallelization opportunities
        const pattern = this.inferWorkflowPattern(executionGraph, optimizedSequence);
        
        // Estimate duration and complexity
        const duration = this.estimateWorkflowDuration(skills, pattern);
        const complexity = this.assessWorkflowComplexity(skills, pattern, projectContext);
        
        return {
            id: "custom_workflow_" + Date.now(),
            pattern: pattern,
            skills: optimizedSequence,
            parallelizable: pattern.includes("parallel"),
            estimated_duration: duration,
            complexity: complexity,
            applicability_score: 0.8, // Custom workflows get high applicability
            customizations: [{
                type: "custom_generation",
                reason: "Generated specifically for current context and requirements"
            }],
            is_custom: true
        };
    }

    async buildExecutionGraph(skills, projectContext) {
        const dependencies = {
            "requirements-merge": ["requirements-ingest"],
            "goals-extract": ["requirements-ingest"],
            "process-w5h": ["requirements-ingest"],
            "domain-extractconcepts": ["requirements-ingest"],
            "domain-alignentities": ["domain-extractconcepts"],
            "domain-proposenewconcepts": ["domain-alignentities"],
            "diagram-generatecollaboration": ["domain-extractconcepts"],
            "hierarchy-management": ["diagram-generatecollaboration"],
            "documentation-automation": ["hierarchy-management"],
            "hierarchy-validation": ["hierarchy-management"],
            "edps-compliance": ["hierarchy-validation"],
            "plan-derivetasks": ["requirements-ingest", "goals-extract"],
            "plan-estimateeffort": ["plan-derivetasks"],
            "plan-buildschedule": ["plan-estimateeffort"]
        };
        
        const graph = {
            nodes: skills.map(skill => ({ skill, dependencies: dependencies[skill] || [] })),
            edges: []
        };
        
        // Build edges based on dependencies
        for (const node of graph.nodes) {
            for (const dep of node.dependencies) {
                if (skills.includes(dep)) {
                    graph.edges.push({ from: dep, to: node.skill, type: "dependency" });
                }
            }
        }
        
        return graph;
    }

    async optimizeExecutionSequence(executionGraph, intentAnalysis) {
        // Topological sort with optimization hints
        const inDegree = new Map();
        const adjList = new Map();
        
        // Initialize
        for (const node of executionGraph.nodes) {
            inDegree.set(node.skill, 0);
            adjList.set(node.skill, []);
        }
        
        // Build adjacency list and calculate in-degrees
        for (const edge of executionGraph.edges) {
            adjList.get(edge.from).push(edge.to);
            inDegree.set(edge.to, inDegree.get(edge.to) + 1);
        }
        
        // Topological sort with priority (considering urgency and complexity)
        const queue = [];
        const result = [];
        
        // Add nodes with no dependencies
        for (const [skill, degree] of inDegree.entries()) {
            if (degree === 0) {
                queue.push(skill);
            }
        }
        
        // Sort queue by priority
        const prioritySort = (a, b) => {
            const priorityA = this.calculateSkillPriority(a, intentAnalysis);
            const priorityB = this.calculateSkillPriority(b, intentAnalysis);
            return priorityB - priorityA;
        };
        
        while (queue.length > 0) {
            queue.sort(prioritySort);
            const current = queue.shift();
            result.push(current);
            
            // Update dependencies
            for (const neighbor of adjList.get(current)) {
                inDegree.set(neighbor, inDegree.get(neighbor) - 1);
                if (inDegree.get(neighbor) === 0) {
                    queue.push(neighbor);
                }
            }
        }
        
        return result;
    }

    calculateSkillPriority(skill, intentAnalysis) {
        // Priority factors
        let priority = 0;
        
        // Urgency impact
        const urgencyMultiplier = {
            "high": 1.5,
            "medium": 1.0,
            "low": 0.8
        };
        priority += urgencyMultiplier[intentAnalysis.urgency_level] || 1.0;
        
        // Skill type priority
        const skillTypePriority = {
            "project-document-management": 10, // Setup first
            "requirements-ingest": 9,          // Foundation
            "goals-extract": 8,                // Early analysis
            "process-w5h": 7,
            "domain-extractconcepts": 6,
            "diagram-generatecollaboration": 5,
            "hierarchy-management": 4,
            "hierarchy-validation": 3,
            "edps-compliance": 2,              // Validation later
            "integration-testing": 1           // Very last
        };
        
        priority += skillTypePriority[skill] || 5;
        
        return priority;
    }

    inferWorkflowPattern(executionGraph, optimizedSequence) {
        // Analyze the structure to determine pattern
        const hasParallelPaths = this.detectParallelPaths(executionGraph);
        const hasBranching = this.detectBranching(executionGraph);
        const isLinear = optimizedSequence.length === executionGraph.nodes.length && 
                        executionGraph.edges.length === optimizedSequence.length - 1;
        
        if (isLinear) return "linear";
        if (hasParallelPaths && hasBranching) return "parallel_convergence";
        if (hasParallelPaths) return "parallel";
        if (hasBranching) return "branching";
        return "sequential";
    }

    detectParallelPaths(graph) {
        // Simple heuristic: if multiple nodes have same dependency, they can run in parallel
        const dependencyMap = new Map();
        
        for (const edge of graph.edges) {
            if (!dependencyMap.has(edge.from)) {
                dependencyMap.set(edge.from, []);
            }
            dependencyMap.get(edge.from).push(edge.to);
        }
        
        for (const dependents of dependencyMap.values()) {
            if (dependents.length > 1) {
                return true;
            }
        }
        
        return false;
    }

    detectBranching(graph) {
        // Check if any node has multiple outgoing edges
        const outDegree = new Map();
        
        for (const node of graph.nodes) {
            outDegree.set(node.skill, 0);
        }
        
        for (const edge of graph.edges) {
            outDegree.set(edge.from, outDegree.get(edge.from) + 1);
        }
        
        for (const degree of outDegree.values()) {
            if (degree > 1) {
                return true;
            }
        }
        
        return false;
    }

    estimateWorkflowDuration(skills, pattern) {
        // Base duration estimates per skill (in minutes)
        const baseDurations = {
            "requirements-ingest": 20,
            "goals-extract": 15,
            "process-w5h": 25,
            "domain-extractconcepts": 30,
            "domain-alignentities": 25,
            "diagram-generatecollaboration": 45,
            "hierarchy-management": 60,
            "hierarchy-validation": 20,
            "edps-compliance": 15,
            "plan-derivetasks": 30,
            "integration-testing": 40
        };
        
        let totalDuration = 0;
        for (const skill of skills) {
            totalDuration += baseDurations[skill] || 20; // default 20 minutes
        }
        
        // Pattern adjustments
        const patternMultipliers = {
            "linear": 1.0,
            "parallel": 0.6,
            "parallel_convergence": 0.7,
            "sequential": 1.1,
            "branching": 1.2
        };
        
        const adjustedDuration = totalDuration * (patternMultipliers[pattern] || 1.0);
        
        // Convert to human-readable format
        if (adjustedDuration < 60) {
            return `${Math.round(adjustedDuration)} minutes`;
        } else if (adjustedDuration < 240) {
            const hours = Math.ceil(adjustedDuration / 60);
            return `${hours} hour${hours > 1 ? 's' : ''}`;
        } else {
            const hours = Math.ceil(adjustedDuration / 60);
            return `${Math.floor(hours / 24)} day${Math.floor(hours / 24) > 1 ? 's' : ''} ${hours % 24} hours`;
        }
    }

    assessWorkflowComplexity(skills, pattern, projectContext) {
        let complexityScore = 0;
        
        // Skill-based complexity
        const skillComplexity = {
            "requirements-ingest": 1,
            "goals-extract": 1,
            "process-w5h": 2,
            "domain-extractconcepts": 2,
            "domain-alignentities": 3,
            "diagram-generatecollaboration": 3,
            "hierarchy-management": 4,
            "hierarchy-validation": 3,
            "edps-compliance": 2,
            "integration-testing": 4
        };
        
        for (const skill of skills) {
            complexityScore += skillComplexity[skill] || 2;
        }
        
        // Pattern complexity
        const patternComplexity = {
            "linear": 0,
            "parallel": 1,
            "sequential": 0,
            "parallel_convergence": 2,
            "branching": 2
        };
        
        complexityScore += patternComplexity[pattern] || 1;
        
        // Context complexity
        const contextFactors = Object.keys(projectContext.availableArtifacts || {}).length;
        complexityScore += Math.floor(contextFactors / 3);
        
        // Normalize to complexity levels
        if (complexityScore <= 8) return "low";
        if (complexityScore <= 15) return "medium";
        return "high";
    }
}
```

## Context-Aware Skill Recommendations

### Advanced Context Analysis
```javascript
class ContextAwareRecommendationEngine {
    constructor() {
        this.contextAnalyzer = new ProjectContextAnalyzer();
        this.recommendationOptimizer = new RecommendationOptimizer();
        this.learningSystem = new AdaptiveLearningSystem();
    }

    async generateContextualRecommendations(intentAnalysis, projectContext, userPreferences = {}) {
        // Deep context analysis
        const enrichedContext = await this.enrichProjectContext(projectContext);
        
        // Generate base recommendations
        const baseRecommendations = await this.generateBaseRecommendations(intentAnalysis, enrichedContext);
        
        // Apply contextual optimization
        const optimizedRecommendations = await this.optimizeWithContext(baseRecommendations, enrichedContext, userPreferences);
        
        // Add learning insights
        const learningEnhanced = await this.enhanceWithLearning(optimizedRecommendations, enrichedContext);
        
        return {
            recommendations: learningEnhanced,
            context_analysis: enrichedContext,
            optimization_rationale: this.generateOptimizationRationale(baseRecommendations, optimizedRecommendations),
            confidence_metrics: this.calculateConfidenceMetrics(learningEnhanced, enrichedContext),
            alternative_paths: await this.generateAlternativePaths(learningEnhanced, enrichedContext)
        };
    }

    async enrichProjectContext(projectContext) {
        const enriched = { ...projectContext };
        
        // Analyze project phase and maturity
        enriched.project_maturity = await this.assessProjectMaturity(projectContext);
        enriched.artifact_quality = await this.assessArtifactQuality(projectContext);
        enriched.methodology_adherence = await this.assessMethodologyAdherence(projectContext);
        enriched.team_readiness = await this.assessTeamReadiness(projectContext);
        enriched.risk_factors = await this.identifyRiskFactors(projectContext);
        enriched.optimization_opportunities = await this.identifyOptimizationOpportunities(projectContext);
        
        // Infer missing context
        enriched.inferred_goals = await this.inferProjectGoals(projectContext);
        enriched.likely_constraints = await this.inferConstraints(projectContext);
        enriched.recommended_timeline = await this.inferTimeline(projectContext);
        
        return enriched;
    }

    async assessProjectMaturity(projectContext) {
        const maturityIndicators = {
            initialization: {
                score: 0,
                indicators: [
                    { check: () => Boolean(projectContext.projectStructure), weight: 20 },
                    { check: () => Boolean(projectContext.hasRequirements), weight: 15 },
                    { check: () => Boolean(projectContext.hasBasicDocumentation), weight: 10 }
                ]
            },
            analysis: {
                score: 0,
                indicators: [
                    { check: () => Boolean(projectContext.hasDomainConcepts), weight: 15 },
                    { check: () => Boolean(projectContext.hasGoalsExtracted), weight: 10 },
                    { check: () => Boolean(projectContext.hasProcessAnalysis), weight: 15 }
                ]
            },
            design: {
                score: 0,
                indicators: [
                    { check: () => Boolean(projectContext.hasCollaborationDiagram), weight: 20 },
                    { check: () => Boolean(projectContext.hasHierarchy), weight: 15 },
                    { check: () => Boolean(projectContext.hasArchitecture), weight: 10 }
                ]
            },
            validation: {
                score: 0,
                indicators: [
                    { check: () => Boolean(projectContext.hasValidation), weight: 15 },
                    { check: () => Boolean(projectContext.hasCompliance), weight: 10 },
                    { check: () => Boolean(projectContext.hasIntegrationTesting), weight: 15 }
                ]
            }
        };

        for (const [phase, config] of Object.entries(maturityIndicators)) {
            let phaseScore = 0;
            for (const indicator of config.indicators) {
                if (indicator.check()) {
                    phaseScore += indicator.weight;
                }
            }
            config.score = phaseScore;
        }

        // Determine current phase and overall maturity
        const scores = Object.entries(maturityIndicators).map(([phase, config]) => ({
            phase,
            score: config.score
        }));

        const maxScore = Math.max(...scores.map(s => s.score));
        const currentPhase = scores.find(s => s.score === maxScore)?.phase || "initialization";
        
        const overallMaturity = Object.values(maturityIndicators).reduce((sum, config) => sum + config.score, 0) / 100;

        return {
            current_phase: currentPhase,
            overall_score: Math.min(overallMaturity, 1.0),
            phase_scores: maturityIndicators,
            next_phase: this.determineNextPhase(currentPhase, maturityIndicators),
            readiness_assessment: this.assessPhaseReadiness(currentPhase, maturityIndicators)
        };
    }

    async generateOptimizationOpportunities(projectContext) {
        const opportunities = [];
        
        // Parallel execution opportunities
        if (projectContext.hasRequirements && !projectContext.hasDomainConcepts) {
            opportunities.push({
                type: "parallel_execution",
                opportunity: "Run goals-extract and domain-extractconcepts in parallel after requirements-ingest",
                impact: "Save 15-20 minutes",
                confidence: 0.8
            });
        }
        
        // Skip redundant validations
        if (projectContext.hasRecent && projectContext.hasRecentValidation) {
            opportunities.push({
                type: "validation_optimization",
                opportunity: "Skip intermediate validations, run comprehensive validation at end",
                impact: "Save 10-15 minutes",
                confidence: 0.7
            });
        }
        
        // Template utilization
        if (projectContext.projectType === "standard" && projectContext.hasTemplates) {
            opportunities.push({
                type: "template_acceleration",
                opportunity: "Use project templates to accelerate documentation generation",
                impact: "Save 30-45 minutes",
                confidence: 0.9
            });
        }
        
        return opportunities;
    }

    async optimizeWithContext(baseRecommendations, enrichedContext, userPreferences) {
        const optimized = [...baseRecommendations];
        
        // Apply project maturity optimizations
        const maturity = enrichedContext.project_maturity;
        if (maturity.current_phase === "initialization" && maturity.overall_score < 0.3) {
            // Add project setup skills at the beginning
            if (!optimized.some(r => r.skill === "project-document-management")) {
                optimized.unshift({
                    skill: "project-document-management",
                    confidence: 0.95,
                    category: "setup_optimization",
                    reasoning: "Project structure needed before other activities"
                });
            }
        }
        
        // Apply urgency optimizations
        if (userPreferences.urgency === "high") {
            // Filter to essential skills only
            const essential = optimized.filter(r => 
                this.isEssentialSkill(r.skill, enrichedContext.inferred_goals)
            );
            optimized.splice(0, optimized.length, ...essential);
            
            // Add fast-track annotations
            for (const rec of optimized) {
                rec.fast_track = true;
                rec.reasoning += " [Fast-track mode]";
            }
        }
        
        // Apply quality preferences
        if (userPreferences.quality_focus === "high") {
            // Add comprehensive validation
            const validationSkills = ["hierarchy-validation", "edps-compliance", "integration-testing"];
            for (const skill of validationSkills) {
                if (!optimized.some(r => r.skill === skill)) {
                    optimized.push({
                        skill: skill,
                        confidence: 0.8,
                        category: "quality_optimization",
                        reasoning: "Added for high-quality deliverables"
                    });
                }
            }
        }
        
        // Apply team size optimizations
        if (enrichedContext.team_readiness?.team_size === "multiple") {
            // Optimize for parallel execution
            const parallelizable = this.identifyParallelizableSkills(optimized);
            for (const group of parallelizable) {
                for (const rec of group) {
                    rec.parallel_group = group.map(r => r.skill).join(",");
                    rec.reasoning += " [Parallelizable with team]";
                }
            }
        }
        
        return optimized;
    }

    isEssentialSkill(skill, inferredGoals) {
        const essentialSkills = {
            "quick_analysis": ["requirements-ingest", "goals-extract"],
            "basic_modeling": ["requirements-ingest", "domain-extractconcepts", "diagram-generatecollaboration"],
            "validation_focused": ["hierarchy-validation", "edps-compliance"],
            "planning_focused": ["requirements-ingest", "goals-extract", "plan-derivetasks"]
        };
        
        const primaryGoal = inferredGoals.primary;
        const essentialForGoal = essentialSkills[primaryGoal] || [];
        
        return essentialForGoal.includes(skill);
    }

    identifyParallelizableSkills(recommendations) {
        // Group skills that can run in parallel
        const parallelGroups = [];
        const dependencies = this.getSkillDependencies();
        
        // Find skills with same dependencies (can run in parallel)
        const dependencyGroups = new Map();
        
        for (const rec of recommendations) {
            const deps = dependencies[rec.skill] || [];
            const depsKey = deps.sort().join(",");
            
            if (!dependencyGroups.has(depsKey)) {
                dependencyGroups.set(depsKey, []);
            }
            dependencyGroups.get(depsKey).push(rec);
        }
        
        // Filter groups with multiple skills
        for (const group of dependencyGroups.values()) {
            if (group.length > 1) {
                parallelGroups.push(group);
            }
        }
        
        return parallelGroups;
    }

    getSkillDependencies() {
        return {
            "requirements-merge": ["requirements-ingest"],
            "goals-extract": ["requirements-ingest"],
            "process-w5h": ["requirements-ingest"],
            "domain-extractconcepts": ["requirements-ingest"],
            "domain-alignentities": ["domain-extractconcepts"],
            "diagram-generatecollaboration": ["domain-extractconcepts"],
            "hierarchy-management": ["diagram-generatecollaboration"],
            "hierarchy-validation": ["hierarchy-management"],
            "edps-compliance": ["hierarchy-validation"]
        };
    }
}
```