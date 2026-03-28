# Enhanced Skill Integration and Performance Optimizations

## Integration with Hierarchy-Management Skill

### Bidirectional Communication Protocol

```javascript
/**
 * Enhanced integration interface between diagram-generatecollaboration 
 * and hierarchy-management skills
 */
class HierarchyIntegrationProtocol {
    constructor(hierarchyManagementSkill, hierarchyValidationSkill) {
        this.hierarchyManager = hierarchyManagementSkill;
        this.hierarchyValidator = hierarchyValidationSkill;
        this.integrationCache = new Map();
    }

    async coordinateDecomposition(participant, parentDiagram, decompositionRequest) {
        // Step 1: Validate decomposition eligibility using our enhanced VR-3
        const eligibilityCheck = await this.validateDecompositionEligibility(
            participant, 
            parentDiagram,
            decompositionRequest
        );
        
        if (!eligibilityCheck.eligible) {
            return {
                success: false,
                reason: "decomposition_not_eligible", 
                details: eligibilityCheck
            };
        }
        
        // Step 2: Generate child diagram structure
        const childDiagram = await this.generateChildDiagram(
            participant,
            parentDiagram,
            decompositionRequest
        );
        
        // Step 3: Coordinate with hierarchy-management for folder structure
        const hierarchyUpdate = await this.hierarchyManager.createSubProcess({
            parentPath: parentDiagram.path,
            participantName: participant.name,
            childDiagramSpec: childDiagram,
            decompositionMetadata: {
                parentLevel: parentDiagram.level,
                decompositionReason: decompositionRequest.reason,
                expectedComplexity: childDiagram.estimatedComplexity
            }
        });
        
        // Step 4: Coordinate with hierarchy-validation for structural integrity
        const validationResults = await this.hierarchyValidator.validateCrossLevel({
            parentDiagram: parentDiagram,
            childDiagram: childDiagram,
            decompositionParticipant: participant,
            hierarchyContext: hierarchyUpdate.context
        });
        
        // Step 5: Generate final coordinated result
        return {
            success: true,
            parentDiagramUpdated: await this.updateParentDiagramForDecomposition(parentDiagram, participant, hierarchyUpdate),
            childDiagramGenerated: childDiagram,
            hierarchyStructure: hierarchyUpdate,
            validationResults: validationResults,
            integrationMetadata: {
                coordinatedAt: new Date().toISOString(),
                participantDecomposed: participant.name,
                newHierarchyLevel: hierarchyUpdate.level,
                crossLevelConsistency: validationResults.crossLevelConsistency
            }
        };
    }

    async validateDecompositionEligibility(participant, parentDiagram, decompositionRequest) {
        // Enhanced VR-3 validation with quality assessment
        const qualityAssessment = await assessDecompositionQuality(
            participant, 
            parentDiagram.complexityMetrics,
            decompositionRequest
        );
        
        const eligibilityChecks = {
            isControlType: participant.stereotype === "control",
            hasAdequateComplexity: qualityAssessment.readinessScore >= 6,
            notAlreadyDecomposed: !this.isParticipantDecomposed(participant, parentDiagram),
            hierarchyDepthOk: parentDiagram.level < this.getMaxHierarchyDepth()
        };
        
        const eligible = Object.values(eligibilityChecks).every(check => check === true);
        
        return {
            eligible: eligible,
            checks: eligibilityChecks,
            qualityAssessment: qualityAssessment,
            recommendations: eligible ? 
                qualityAssessment.decompositionStrategy :
                this.generateEligibilityRecommendations(eligibilityChecks, qualityAssessment)
        };
    }

    async generateChildDiagram(participant, parentDiagram, decompositionRequest) {
        // Analyze participant's internal structure from parent diagram context
        const participantContext = this.extractParticipantContext(participant, parentDiagram);
        
        // Generate child participants based on decomposition strategy
        const decompositionStrategy = this.determineDecompositionStrategy(
            participant, 
            participantContext, 
            decompositionRequest
        );
        
        const childParticipants = await this.generateChildParticipants(
            participant,
            participantContext,
            decompositionStrategy  
        );
        
        // Generate child interactions based on parent context
        const childInteractions = await this.generateChildInteractions(
            participant,
            participantContext,
            childParticipants,
            decompositionStrategy
        );
        
        return {
            level: parentDiagram.level + 1,
            parentParticipant: participant.name,
            participants: childParticipants,
            interactions: childInteractions,
            boundaries: this.detectChildBoundaries(childParticipants, childInteractions),
            estimatedComplexity: this.calculateChildComplexity(childParticipants, childInteractions),
            traceabilityLinks: this.generateChildTraceability(participant, parentDiagram),
            decompositionMetadata: {
                strategy: decompositionStrategy.name,
                rationale: decompositionStrategy.rationale,
                parentContext: participantContext
            }
        };
    }

    determineDecompositionStrategy(participant, context, request) {
        const availableStrategies = {
            functional_decomposition: {
                name: "functional_decomposition",
                applicable: context.functionalBreadth > 0.6,
                rationale: "Participant has multiple distinct functional responsibilities",
                childPatternTemplate: "functional_services"
            },
            layer_decomposition: {
                name: "layer_decomposition", 
                applicable: context.layeredInteractions > 5,
                rationale: "Participant shows clear layered interaction patterns",
                childPatternTemplate: "layered_architecture"
            },
            workflow_decomposition: {
                name: "workflow_decomposition",
                applicable: context.workflowSteps > 4,
                rationale: "Participant orchestrates complex workflow steps",
                childPatternTemplate: "workflow_steps"
            },
            integration_decomposition: {
                name: "integration_decomposition",
                applicable: context.externalIntegrations > 3,
                rationale: "Participant manages multiple external integrations",
                childPatternTemplate: "integration_adapters"
            }
        };
        
        // Select best strategy based on context analysis
        const applicableStrategies = Object.values(availableStrategies)
            .filter(strategy => strategy.applicable);
            
        if (applicableStrategies.length === 0) {
            return {
                name: "generic_decomposition",
                rationale: "Generic decomposition based on interaction patterns",
                childPatternTemplate: "generic_services"
            };
        }
        
        // Use explicitly requested strategy if applicable
        if (request.preferredStrategy && 
            availableStrategies[request.preferredStrategy]?.applicable) {
            return availableStrategies[request.preferredStrategy];
        }
        
        // Otherwise select strategy with highest applicability score
        return applicableStrategies.reduce((best, current) => 
            current.applicabilityScore > best.applicabilityScore ? current : best
        );
    }
}
```

## Integration with Hierarchy-Validation Skill

### Enhanced Cross-Level Validation

```javascript
class EnhancedHierarchyValidation {
    constructor(hierarchyValidationSkill) {
        this.hierarchyValidator = hierarchyValidationSkill;
        this.crossLevelCache = new Map();
    }

    async validateDiagramGeneration(diagrams, hierarchyContext) {
        // Delegate structural validation to hierarchy-validation skill
        const structuralValidation = await this.hierarchyValidator.validateStructuralIntegrity({
            diagrams: diagrams,
            hierarchyContext: hierarchyContext,
            validationLevel: "comprehensive"
        });
        
        // Perform our diagram-specific validations
        const diagramValidation = await this.validateDiagramSpecificRequirements(
            diagrams,
            hierarchyContext,
            structuralValidation
        );
        
        // Combine results with clear responsibility separation
        return {
            structuralIntegrity: structuralValidation,
            diagramCompliance: diagramValidation,
            combinedResults: this.combineValidationResults(structuralValidation, diagramValidation),
            validationMetadata: {
                structuralValidatorUsed: "hierarchy-validation skill",
                diagramValidatorUsed: "diagram-generatecollaboration skill", 
                validationTimestamp: new Date().toISOString()
            }
        };
    }

    async validateDiagramSpecificRequirements(diagrams, hierarchyContext, structuralBaseline) {
        const diagramValidations = await Promise.all(
            diagrams.map(diagram => this.validateSingleDiagram(diagram, hierarchyContext))
        );
        
        const crossDiagramValidations = await this.validateCrossDiagramConsistency(
            diagrams, 
            hierarchyContext
        );
        
        return {
            perDiagramResults: diagramValidations,
            crossDiagramResults: crossDiagramValidations,
            overallDiagramCompliance: this.calculateOverallDiagramCompliance(
                diagramValidations,
                crossDiagramValidations
            )
        };
    }

    async validateSingleDiagram(diagram, hierarchyContext) {
        // Run our enhanced boundary validation rules (VR-1 through VR-4)
        const boundaryValidation = await validateBoundaryRules_Enhanced(
            diagram,
            hierarchyContext
        );
        
        // Validate participant stereotype consistency
        const stereotypeValidation = await this.validateParticipantStereotypes(
            diagram,
            hierarchyContext
        );
        
        // Validate requirement traceability preservation
        const traceabilityValidation = await this.validateRequirementTraceability(
            diagram,
            hierarchyContext
        );
        
        return {
            diagramId: diagram.id,
            boundaryValidation: boundaryValidation,
            stereotypeValidation: stereotypeValidation,
            traceabilityValidation: traceabilityValidation,
            overallCompliance: this.calculateDiagramCompliance([
                boundaryValidation,
                stereotypeValidation, 
                traceabilityValidation
            ])
        };
    }

    async validateCrossDiagramConsistency(diagrams, hierarchyContext) {
        const consistencyChecks = {
            participantTypeConsistency: await this.validateParticipantTypesAcrossLevels(diagrams),
            boundaryNamingConsistency: await this.validateBoundaryNaming(diagrams),
            requirementTraceContinuity: await this.validateRequirementTraceContinuity(diagrams),
            decompositionIntegrity: await this.validateDecompositionIntegrity(diagrams, hierarchyContext)
        };
        
        return {
            checks: consistencyChecks,
            overallConsistency: this.calculateConsistencyScore(consistencyChecks),
            inconsistencies: this.extractInconsistencies(consistencyChecks),
            recommendations: this.generateConsistencyRecommendations(consistencyChecks)
        };
    }

    combineValidationResults(structural, diagram) {
        // Intelligent combination respecting each skill's authority
        const combinedResult = {
            overallStatus: this.determineOverallStatus(structural.status, diagram.overallCompliance),
            structuralScore: structural.score,
            diagramScore: diagram.overallCompliance.score,
            combinedScore: (structural.score * 0.6) + (diagram.overallCompliance.score * 0.4),
            issues: [
                ...structural.issues.map(issue => ({ ...issue, source: "structural" })),
                ...diagram.overallCompliance.issues.map(issue => ({ ...issue, source: "diagram" }))
            ],
            recommendations: this.combineRecommendations(structural.recommendations, diagram.overallCompliance.recommendations)
        };
        
        return combinedResult;
    }
}
```

## Performance Optimizations for Large Processes

### Scalable Architecture for 50+ Participants

```javascript
class PerformanceOptimizedDiagramGeneration {
    constructor(options = {}) {
        this.maxParticipants = options.maxParticipants || 100;
        this.batchSize = options.batchSize || 25;
        this.enableCaching = options.enableCaching !== false;
        this.parallelProcessing = options.parallelProcessing !== false;
        this.memoryThreshold = options.memoryThreshold || 0.8; // 80% memory usage threshold
        
        if (this.enableCaching) {
            this.cache = new PerformanceCache();
        }
        
        this.performanceMetrics = new PerformanceMonitor();
    }

    async generateDiagramOptimized(largeProcessData, options = {}) {
        // Pre-flight performance check
        const performanceAssessment = await this.assessPerformanceRequirements(largeProcessData);
        
        if (!performanceAssessment.canProcess) {
            return {
                success: false,
                reason: "performance_constraints_exceeded",
                assessment: performanceAssessment,
                recommendations: performanceAssessment.recommendations
            };
        }
        
        // Select optimal processing strategy based on size
        const processingStrategy = this.selectProcessingStrategy(largeProcessData, performanceAssessment);
        
        let result;
        switch (processingStrategy.name) {
            case "standard_processing":
                result = await this.processStandard(largeProcessData, options);
                break;
            case "batch_processing": 
                result = await this.processBatched(largeProcessData, options);
                break;
            case "streaming_processing":
                result = await this.processStreaming(largeProcessData, options);
                break;
            case "hierarchical_partitioning":
                result = await this.processHierarchicalPartitions(largeProcessData, options);
                break;
            default:
                throw new Error(`Unknown processing strategy: ${processingStrategy.name}`);
        }
        
        // Add performance metrics to result
        result.performanceMetrics = this.performanceMetrics.getReport();
        
        return result;
    }

    async processBatched(largeProcessData, options) {
        const { participants, interactions } = largeProcessData;
        this.performanceMetrics.start("batch_processing");
        
        // Partition participants into manageable batches
        const participantBatches = this.partitionParticipants(participants, this.batchSize);
        const batchResults = [];
        
        for (let i = 0; i < participantBatches.length; i++) {
            const batch = participantBatches[i];
            
            // Memory management check
            if (await this.shouldPauseForMemory()) {
                await this.performMemoryCleanup();
            }
            
            const batchContext = this.createBatchContext(batch, interactions, i);
            const batchResult = await this.processBatchWithRetry(batchContext, options);
            
            batchResults.push(batchResult);
            
            // Update progress if callback provided 
            if (options.progressCallback) {
                options.progressCallback({
                    completed: i + 1,
                    total: participantBatches.length,
                    percentage: Math.round(((i + 1) / participantBatches.length) * 100)
                });
            }
        }
        
        // Merge batch results efficiently
        const mergedResult = await this.mergeBatchResults(batchResults, largeProcessData);
        
        this.performanceMetrics.end("batch_processing");
        return mergedResult;
    }

    async processStreaming(largeProcessData, options) {
        const { participants, interactions } = largeProcessData;
        this.performanceMetrics.start("streaming_processing");
        
        // Set up streaming pipeline
        const streamProcessor = new StreamingDiagramProcessor({
            inputData: largeProcessData,
            batchSize: this.batchSize,
            enableCache: this.enableCaching,
            memoryThreshold: this.memoryThreshold
        });
        
        const streamResult = {
            diagrams: [],
            metadata: { processingMethod: "streaming" },
            errors: []
        };
        
        // Process data stream with backpressure handling
        await streamProcessor.process({
            onDiagramGenerated: (diagram) => {
                streamResult.diagrams.push(diagram);
            },
            onError: (error) => {
                streamResult.errors.push(error);
            },
            onProgress: options.progressCallback,
            onMemoryPressure: async () => {
                await this.performMemoryCleanup();
            }
        });
        
        this.performanceMetrics.end("streaming_processing");
        return streamResult;
    }

    async processHierarchicalPartitions(largeProcessData, options) {
        // Strategy for extremely large processes: automatic hierarchical decomposition
        this.performanceMetrics.start("hierarchical_partitioning");
        
        const partitions = await this.createHierarchicalPartitions(largeProcessData);
        const partitionResults = await Promise.all(
            partitions.map((partition, index) => 
                this.processPartition(partition, index, options)
            )
        );
        
        // Generate top-level diagram connecting partitions
        const topLevelDiagram = await this.generateTopLevelConnectingDiagram(
            partitionResults, 
            largeProcessData
        );
        
        const hierarchicalResult = {
            topLevelDiagram: topLevelDiagram,
            partitions: partitionResults,
            partitionStrategy: partitions.strategy,
            metadata: {
                processingMethod: "hierarchical_partitioning",
                totalPartitions: partitions.length,
                partitioningRationale: partitions.rationale
            }
        };
        
        this.performanceMetrics.end("hierarchical_partitioning");
        return hierarchicalResult;
    }

    async createHierarchicalPartitions(largeProcessData) {
        // Intelligent partitioning based on participant clustering
        const clusteringResult = await this.performParticipantClustering(
            largeProcessData.participants,
            largeProcessData.interactions
        );
        
        const partitions = clusteringResult.clusters.map((cluster, index) => ({
            id: `partition_${index}`,
            name: cluster.name || `Partition ${index + 1}`,
            participants: cluster.participants,
            interactions: this.filterInteractionsForCluster(cluster, largeProcessData.interactions),
            boundaryHints: cluster.suggestedBoundaries,
            estimatedComplexity: cluster.complexityScore
        }));
        
        return {
            partitions: partitions,
            strategy: clusteringResult.strategy,
            rationale: `Large process (${largeProcessData.participants.length} participants) partitioned into ${partitions.length} manageable segments`
        };
    }

    async shouldPauseForMemory() {
        const memoryUsage = process.memoryUsage();
        const memoryUsageRatio = memoryUsage.heapUsed / memoryUsage.heapTotal;
        
        return memoryUsageRatio > this.memoryThreshold;
    }

    async performMemoryCleanup() {
        // Clear caches if enabled
        if (this.enableCaching && this.cache) {
            await this.cache.clearOldEntries();
        }
        
        // Trigger garbage collection if available
        if (global.gc) {
            global.gc();
        }
        
        // Wait briefly to allow cleanup to complete
        await new Promise(resolve => setTimeout(resolve, 100));
    }
}

class PerformanceCache {
    constructor(maxSize = 1000, ttlMs = 300000) { // 5 minute TTL
        this.cache = new Map();
        this.maxSize = maxSize;
        this.ttlMs = ttlMs;
        this.accessTimes = new Map();
    }

    async get(key) {
        if (this.cache.has(key)) {
            this.accessTimes.set(key, Date.now());
            return this.cache.get(key);
        }
        return null;
    }

    async set(key, value) {
        // Implement LRU eviction if cache is full
        if (this.cache.size >= this.maxSize) {
            await this.evictLRU();
        }
        
        this.cache.set(key, value);
        this.accessTimes.set(key, Date.now());
    }

    async clearOldEntries() {
        const now = Date.now();
        const keysToDelete = [];
        
        for (const [key, accessTime] of this.accessTimes.entries()) {
            if (now - accessTime > this.ttlMs) {
                keysToDelete.push(key);
            }
        }
        
        keysToDelete.forEach(key => {
            this.cache.delete(key);
            this.accessTimes.delete(key);
        });
        
        return keysToDelete.length;
    }

    async evictLRU() {
        // Find least recently used entry
        let oldestKey = null;
        let oldestTime = Infinity;
        
        for (const [key, time] of this.accessTimes.entries()) {
            if (time < oldestTime) {
                oldestTime = time;
                oldestKey = key;
            }
        }
        
        if (oldestKey) {
            this.cache.delete(oldestKey);
            this.accessTimes.delete(oldestKey);
        }
    }
}

class PerformanceMonitor {
    constructor() {
        this.metrics = new Map();
        this.startTimes = new Map();
    }

    start(operation) {
        this.startTimes.set(operation, process.hrtime.bigint());
    }

    end(operation) {
        if (this.startTimes.has(operation)) {
            const startTime = this.startTimes.get(operation);
            const endTime = process.hrtime.bigint();
            const duration = Number(endTime - startTime) / 1000000; // Convert to milliseconds
            
            if (!this.metrics.has(operation)) {
                this.metrics.set(operation, []);
            }
            
            this.metrics.get(operation).push({
                duration: duration,
                timestamp: new Date().toISOString(),
                memoryUsage: process.memoryUsage()
            });
            
            this.startTimes.delete(operation);
        }
    }

    getReport() {
        const report = {};
        
        for (const [operation, measurements] of this.metrics.entries()) {
            const durations = measurements.map(m => m.duration);
            report[operation] = {
                totalExecutions: measurements.length,
                averageDuration: durations.reduce((a, b) => a + b, 0) / durations.length,
                minDuration: Math.min(...durations),
                maxDuration: Math.max(...durations),
                totalDuration: durations.reduce((a, b) => a + b, 0),
                measurements: measurements
            };
        }
        
        return report;
    }
}
```