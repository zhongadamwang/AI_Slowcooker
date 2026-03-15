<!-- Identifier: C-02 -->

# 02 - Analysis Process — Collaboration

## Entity Interactions

```mermaid
sequenceDiagram
    participant P as PractitionerActor
    participant AP as AnalysisPipelineBoundary
    participant OC as OrchestrationControl
    participant RC as RequirementChunkEntity
    participant AD as AlignmentDecisionEntity

    P->>AP: submitRequirements(input_file)
    AP->>OC: initiateIngestion(input_file)
    OC->>RC: createChunks(input_file)
    RC-->>OC: chunks[]
    OC->>OC: extractConcepts(chunks[])
    OC->>AD: recordAlignmentDecisions(concepts[])
    AD-->>OC: decisions[]
    OC-->>AP: pipelineComplete(decisions[])
    AP-->>P: analysisResult(decisions[])
```

## Interaction Patterns

- All external requests enter through `AnalysisPipelineBoundary`.
- `OrchestrationControl` drives the ingestion → extraction → alignment sequence.
- `RequirementChunkEntity` and `AlignmentDecisionEntity` are passive stores updated by the control.

## Communication Channels

- Synchronous request-response between practitioner and boundary.
- Internal control-to-entity calls are synchronous.

## Data Flow

- `input_file` → `RequirementChunk[]` → extracted concepts → `AlignmentDecision[]` → `analysisResult`
