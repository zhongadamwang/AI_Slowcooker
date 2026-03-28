# Migration Support: Flat-to-Hierarchical Diagram Conversion

## Overview
Non-destructive migration utility that converts existing flat collaboration diagrams to hierarchical format with boundary groupings and participant stereotypes, preserving all requirement traceability and message sequences.

## Migration Pipeline Architecture

### Phase 1: Analysis and Detection

```javascript
function analyzeFlatDiagram(collaborationDiagram) {
    const analysis = {
        currentFormat: detectDiagramFormat(collaborationDiagram),
        participants: extractParticipants(collaborationDiagram),
        interactions: extractInteractions(collaborationDiagram),
        requirements_traceability: extractRequirementLinks(collaborationDiagram),
        complexity_metrics: calculateComplexityMetrics(collaborationDiagram),
        migration_readiness: assessMigrationReadiness(collaborationDiagram)
    };
    
    return analysis;
}

function detectDiagramFormat(diagram) {
    // Detect current diagram structure and format
    const formatIndicators = {
        hasBoxSyntax: /box\s+.*?\s*\n.*?\nend/gm.test(diagram.content),
        hasStereotypes: /@\{.*?"type"\s*:\s*"(actor|boundary|control|entity)".*?\}/.test(diagram.content),
        hasParticipantAnnotations: /participant\s+\w+@\{/.test(diagram.content),
        hasBoundaryComments: /%% Boundary:/.test(diagram.content),
        isSequenceDiagram: /sequenceDiagram/.test(diagram.content),
        isClassDiagram: /classDiagram/.test(diagram.content)
    };
    
    if (formatIndicators.hasBoxSyntax && formatIndicators.hasStereotypes) {
        return {
            format: "hierarchical_project3",
            version: "3.0",
            readyForEnhancement: true,
            migrationNeeded: false
        };
    } else if (formatIndicators.isSequenceDiagram && !formatIndicators.hasBoxSyntax) {
        return {
            format: "flat_project1", 
            version: "1.0",
            readyForEnhancement: false,
            migrationNeeded: true,
            targetFormat: "hierarchical_project3"
        };
    } else {
        return {
            format: "mixed_or_partial",
            version: "unknown",
            readyForEnhancement: false,
            migrationNeeded: true,
            requiresAnalysis: true
        };
    }
}

function assessMigrationReadiness(diagram, analysis) {
    const readinessFactors = {
        participant_count: analysis.participants.length,
        interaction_complexity: analysis.interactions.length,
        requirements_links: analysis.requirements_traceability.length,
        has_clear_actors: identifyActors(analysis.participants).length > 0,
        has_system_components: identifySystemComponents(analysis.participants).length > 0,
        message_flow_clarity: assessMessageFlowClarity(analysis.interactions)
    };
    
    let readinessScore = 0;
    let blockers = [];
    let recommendations = [];
    
    // Assess each factor
    if (readinessFactors.participant_count >= 3 && readinessFactors.participant_count <= 50) {
        readinessScore += 20;
    } else if (readinessFactors.participant_count > 50) {
        blockers.push("Too many participants - consider splitting into multiple diagrams");
    } else {
        recommendations.push("Add more participants for meaningful boundary detection");
    }
    
    if (readinessFactors.has_clear_actors) {
        readinessScore += 25;
    } else {
        blockers.push("No clear actors identified - boundary detection requires external actors");
    }
    
    if (readinessFactors.has_system_components) {
        readinessScore += 25;
    } else {
        recommendations.push("Add system components for hierarchical decomposition");
    }
    
    if (readinessFactors.interaction_complexity >= 5) {
        readinessScore += 20;
    } else {
        recommendations.push("Add more interactions for meaningful boundary grouping");
    }
    
    if (readinessFactors.message_flow_clarity > 0.7) {
        readinessScore += 10;
    } else {
        recommendations.push("Clarify message flow patterns for better boundary detection");
    }
    
    return {
        readiness_score: readinessScore,
        readiness_level: readinessScore >= 80 ? "high" : readinessScore >= 60 ? "medium" : "low",
        migration_recommended: readinessScore >= 60 && blockers.length === 0,
        blockers: blockers,
        recommendations: recommendations,
        factors: readinessFactors
    };
}
```

### Phase 2: Intelligent Boundary Detection

```javascript
function detectBoundariesFromFlatDiagram(analysis, domainKnowledge) {
    const boundaryDetectionStrategies = [
        detectBoundariesByActorInteraction,
        detectBoundariesByFunctionalClustering,
        detectBoundariesByLayerAnalysis,
        detectBoundariesByDomainKnowledge
    ];
    
    const boundaryProposals = [];
    
    boundaryDetectionStrategies.forEach(strategy => {
        const proposals = strategy(analysis, domainKnowledge);
        boundaryProposals.push(...proposals);
    });
    
    // Consolidate and optimize boundary proposals
    const optimizedBoundaries = optimizeBoundaryProposals(boundaryProposals, analysis);
    
    return optimizedBoundaries;
}

function detectBoundariesByActorInteraction(analysis) {
    // Strategy 1: Group participants by which actors they interact with
    const actors = identifyActors(analysis.participants);
    const boundaries = [];
    
    actors.forEach(actor => {
        const interactedParticipants = findParticipantsInteractingWithActor(actor, analysis.interactions);
        
        if (interactedParticipants.length >= 2) {
            boundaries.push({
                name: generateBoundaryNameFromActor(actor),
                participants: interactedParticipants,
                strategy: "actor_interaction",
                confidence: 0.8,
                rationale: `Participants that interact with actor '${actor.name}'`
            });
        }
    });
    
    return boundaries;
}

function detectBoundariesByFunctionalClustering(analysis) {
    // Strategy 2: Group participants by functional similarity
    const functionalClusters = clusterParticipantsByFunction(analysis.participants, analysis.interactions);
    
    return functionalClusters
        .filter(cluster => cluster.participants.length >= 2)
        .map(cluster => ({
            name: cluster.functionalArea + " Boundary",
            participants: cluster.participants,
            strategy: "functional_clustering",
            confidence: cluster.cohesionScore,
            rationale: `Participants with related ${cluster.functionalArea} functionality`
        }));
}

function detectBoundariesByLayerAnalysis(analysis) {
    // Strategy 3: Group participants by architectural layer
    const layerClassification = classifyParticipantsByLayer(analysis.participants);
    const boundaries = [];
    
    Object.entries(layerClassification).forEach(([layer, participants]) => {
        if (participants.length >= 2 && layer !== "unknown") {
            boundaries.push({
                name: `${layer.charAt(0).toUpperCase() + layer.slice(1)} Layer`,
                participants: participants,
                strategy: "layer_analysis", 
                confidence: 0.7,
                rationale: `Participants in the ${layer} architectural layer`
            });
        }
    });
    
    return boundaries;
}

function optimizeBoundaryProposals(proposals, analysis) {
    // Remove duplicate and overlapping boundaries
    const optimizedProposals = removeDuplicateBoundaries(proposals);
    
    // Score each boundary proposal
    const scoredBoundaries = optimizedProposals.map(boundary => ({
        ...boundary,
        optimizationScore: calculateBoundaryOptimizationScore(boundary, analysis)
    }));
    
    // Select best non-overlapping boundaries
    const selectedBoundaries = selectOptimalBoundaries(scoredBoundaries, analysis);
    
    // Assign participants not assigned to any boundary
    const unassignedParticipants = findUnassignedParticipants(selectedBoundaries, analysis.participants);
    const finalBoundaries = assignUnassignedParticipants(selectedBoundaries, unassignedParticipants, analysis);
    
    return finalBoundaries;
}

function calculateBoundaryOptimizationScore(boundary, analysis) {
    let score = boundary.confidence * 0.4; // Base confidence
    
    // Favor boundaries with good participant count
    const participantCount = boundary.participants.length;
    if (participantCount >= 3 && participantCount <= 7) {
        score += 0.3;
    } else if (participantCount >= 2 && participantCount <= 10) {
        score += 0.2;
    }
    
    // Favor boundaries with high internal cohesion
    const cohesion = calculateBoundaryCohesion(boundary, analysis);
    score += cohesion * 0.2;
    
    // Favor boundaries with clear external interface
    const hasExternalInterface = hasExternalActorInterface(boundary, analysis);
    if (hasExternalInterface) {
        score += 0.1;
    }
    
    return Math.min(score, 1.0);
}
```

### Phase 3: Participant Stereotype Assignment

```javascript
function assignParticipantStereotypes(participants, boundaryContext, analysis) {
    const stereotypedParticipants = participants.map(participant => {
        const context = {
            boundary: boundaryContext,
            interactions: analysis.interactions,
            domainKnowledge: analysis.domainKnowledge
        };
        
        const classification = classifyParticipant_Enhanced(participant, context);
        
        return {
            ...participant,
            originalType: participant.type || null,
            stereotype: classification.type,
            stereotypeConfidence: classification.confidence,
            stereotypeReasoning: classification.reasoning,
            migrationMetadata: {
                originalClassification: participant.type,
                migrationMethod: "enhanced_classification",
                confidenceScore: classification.confidence
            }
        };
    });
    
    // Validate stereotype assignments for boundary consistency
    const validationResults = validateStereotypeAssignments(stereotypedParticipants, boundaryContext);
    
    // Apply corrections based on validation
    const correctedParticipants = applyStereotypeCorrections(stereotypedParticipants, validationResults);
    
    return correctedParticipants;
}

function validateStereotypeAssignments(participants, boundaryContext) {
    const results = {
        violations: [],
        corrections: [],
        warnings: []
    };
    
    // Check for required boundary participant in each boundary
    boundaryContext.forEach(boundary => {
        const boundaryParticipants = participants.filter(p => 
            boundary.participants.includes(p.name)
        );
        
        const boundaryTypeParticipants = boundaryParticipants.filter(p => 
            p.stereotype === "boundary"
        );
        
        if (boundaryTypeParticipants.length === 0) {
            // Missing boundary participant - suggest conversion
            const entryPointCandidate = findBestEntryPointCandidate(boundaryParticipants);
            
            if (entryPointCandidate) {
                results.corrections.push({
                    type: "missing_boundary_participant",
                    boundary: boundary.name,
                    action: "convert_to_boundary",
                    participant: entryPointCandidate.name,
                    originalStereotype: entryPointCandidate.stereotype,
                    newStereotype: "boundary",
                    rationale: "Converted to provide boundary entry point"
                });
            }
        }
        
        // Check for actors inside boundaries
        const misplacedActors = boundaryParticipants.filter(p => p.stereotype === "actor");
        if (misplacedActors.length > 0) {
            misplacedActors.forEach(actor => {
                results.violations.push({
                    type: "actor_inside_boundary",
                    participant: actor.name,
                    boundary: boundary.name,
                    action: "move_outside_boundary",
                    rationale: "Actors must be external to all boundaries"
                });
            });
        }
    });
    
    return results;
}

function applyStereotypeCorrections(participants, validationResults) {
    const correctedParticipants = [...participants];
    
    validationResults.corrections.forEach(correction => {
        const participantIndex = correctedParticipants.findIndex(p => 
            p.name === correction.participant
        );
        
        if (participantIndex !== -1) {
            correctedParticipants[participantIndex] = {
                ...correctedParticipants[participantIndex],
                stereotype: correction.newStereotype,
                migrationMetadata: {
                    ...correctedParticipants[participantIndex].migrationMetadata,
                    correctionApplied: true,
                    correctionType: correction.type,
                    correctionRationale: correction.rationale
                }
            };
        }
    });
    
    return correctedParticipants;
}
```

### Phase 4: Hierarchical Diagram Generation

```javascript
function generateHierarchicalDiagram(flatDiagram, boundaries, stereotypedParticipants) {
    // Separate actors (external) from internal participants
    const actors = stereotypedParticipants.filter(p => p.stereotype === "actor");
    const internalParticipants = stereotypedParticipants.filter(p => p.stereotype !== "actor");
    
    // Generate main hierarchical sequence diagram
    const hierarchicalDiagram = {
        header: generateDiagramHeader(flatDiagram),
        actors: generateActorDeclarations(actors),
        boundaries: generateBoundaryBlocks(boundaries, internalParticipants),
        interactions: generateHierarchicalInteractions(flatDiagram.interactions, stereotypedParticipants),
        footer: generateDiagramFooter(flatDiagram),
        metadata: generateMigrationMetadata(flatDiagram, boundaries, stereotypedParticipants)
    };
    
    const mermaidOutput = assembleMermaidDiagram(hierarchicalDiagram);
    
    return {
        originalDiagram: flatDiagram,
        enhancedDiagram: mermaidOutput,
        migrationReport: generateMigrationReport(flatDiagram, hierarchicalDiagram),
        validationResults: validateMigratedDiagram(mermaidOutput)
    };
}

function generateBoundaryBlocks(boundaries, participants) {
    return boundaries.map(boundary => {
        const boundaryParticipants = participants.filter(p => 
            boundary.participants.includes(p.name)
        );
        
        // Order participants within boundary: boundary -> control -> entity
        const orderedParticipants = orderParticipantsForBoundary(boundaryParticipants);
        
        return {
            name: boundary.name,
            participants: orderedParticipants.map(p => ({
                name: p.name,
                stereotype: p.stereotype,
                label: p.label || p.name,
                annotation: generateParticipantAnnotation(p)
            })),
            boundaryMetadata: {
                strategy: boundary.strategy,
                confidence: boundary.optimizationScore,
                migrationSource: boundary.rationale
            }
        };
    });
}

function assembleMermaidDiagram(hierarchicalDiagram) {
    let mermaid = "sequenceDiagram\n\n";
    
    // Add migration comment
    mermaid += "    %% ═══════════════════════════════════════════════════════════\n";
    mermaid += "    %% MIGRATED FROM FLAT DIAGRAM (diagram-generatecollaboration)\n";
    mermaid += `    %% Migration Date: ${new Date().toISOString()}\n`;
    mermaid += `    %% Original Participants: ${hierarchicalDiagram.metadata.originalParticipantCount}\n`;
    mermaid += `    %% Boundaries Detected: ${hierarchicalDiagram.boundaries.length}\n`;
    mermaid += "    %% ═══════════════════════════════════════════════════════════\n\n";
    
    // Add actors (external participants)
    if (hierarchicalDiagram.actors.length > 0) {
        mermaid += "    %% External Actors\n";
        hierarchicalDiagram.actors.forEach(actor => {
            mermaid += `    participant ${actor.name}@{ "type": "actor", "label": "${actor.label}" }\n`;
        });
        mermaid += "\n";
    }
    
    // Add boundary blocks
    hierarchicalDiagram.boundaries.forEach((boundary, index) => {
        mermaid += `    %% Boundary ${index + 1}: ${boundary.name}\n`;
        mermaid += `    box ${boundary.name}\n`;
        
        boundary.participants.forEach(participant => {
            mermaid += `        participant ${participant.name}@{ "type": "${participant.stereotype}", "label": "${participant.label}" }\n`;
        });
        
        mermaid += "    end\n\n";
    });
    
    // Add interactions
    mermaid += "    %% Interactions\n";
    hierarchicalDiagram.interactions.forEach(interaction => {
        mermaid += `    ${interaction.sender}->>+${interaction.receiver}: ${interaction.message}\n`;
    });
    
    return mermaid;
}
```

### Phase 5: Migration Report Generation

```javascript
function generateMigrationReport(originalDiagram, migratedComponents) {
    const report = {
        migrationSummary: {
            migrationDate: new Date().toISOString(),
            originalFormat: "flat_project1",
            targetFormat: "hierarchical_project3",
            migrationStatus: "completed",
            preservationGuarantees: [
                "requirement_traceability_preserved",
                "message_sequences_maintained", 
                "participant_relationships_enhanced",
                "original_diagram_backup_created"
            ]
        },
        transformationDetails: {
            participantTransformations: generateParticipantTransformationSummary(migratedComponents),
            boundariesDetected: generateBoundaryDetectionSummary(migratedComponents.boundaries),
            interactionPreservation: generateInteractionPreservationSummary(originalDiagram, migratedComponents),
            enhancementsApplied: generateEnhancementsSummary(migratedComponents)
        },
        validationResults: {
            hierarchyValidation: validateHierarchicalCompliance(migratedComponents),
            boundaryValidation: validateBoundaryRules(migratedComponents),
            stereotypeValidation: validateStereotypeConsistency(migratedComponents)
        },
        rollbackInstructions: generateRollbackInstructions(originalDiagram),
        nextSteps: generateMigrationNextSteps(migratedComponents)
    };
    
    return report;
}

function generateParticipantTransformationSummary(migratedComponents) {
    const transformations = [];
    
    migratedComponents.enhancedParticipants.forEach(participant => {
        if (participant.migrationMetadata) {
            transformations.push({
                name: participant.name,
                originalType: participant.migrationMetadata.originalClassification || "untyped",
                newStereotype: participant.stereotype,
                confidence: participant.stereotypeConfidence,
                method: participant.migrationMetadata.migrationMethod,
                correctionApplied: participant.migrationMetadata.correctionApplied || false,
                reasoning: participant.stereotypeReasoning
            });
        }
    });
    
    return {
        totalParticipants: transformations.length,
        stereotypeDistribution: calculateStereotypeDistribution(transformations),
        highConfidenceClassifications: transformations.filter(t => t.confidence > 0.8).length,
        correctionsApplied: transformations.filter(t => t.correctionApplied).length,
        transformations: transformations
    };
}

function generateRollbackInstructions(originalDiagram) {
    return {
        backupLocation: generateBackupPath(originalDiagram),
        rollbackSteps: [
            "1. Locate original diagram backup file",
            "2. Replace enhanced diagram with backup",
            "3. Update collaboration-diagrams.json to remove migration metadata",
            "4. Verify requirement traceability links are intact",
            "5. Regenerate any dependent documentation"
        ],
        automatedRollback: {
            available: true,
            command: `rollback_migration --diagram="${originalDiagram.id}" --restore-backup`,
            confirmationRequired: true
        }
    };
}
```