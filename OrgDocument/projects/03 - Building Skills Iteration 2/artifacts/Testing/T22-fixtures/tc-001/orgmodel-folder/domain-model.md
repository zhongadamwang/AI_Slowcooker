<!-- Identifier: DM-01-01 -->

# Skill Pipeline Execution — Domain Model

**Parent Process**: [01 - Skill Development Process Domain Model](../domain-model.md)
**Hierarchy Level**: 1

## Domain Class Diagram

```mermaid
classDiagram
    class PractitionerActor:::actor {
        +user_id: String
        +invoke()
    }
    class SkillPipelineBoundary:::boundary {
        +skill_name: String
        +receive()
    }
    class PipelineOrchestrationControl:::control {
        +stage: String
        +orchestrate()
    }
    class SkillOutputEntity:::entity {
        +artifact_path: String
        +store()
    }

    PractitionerActor --> SkillPipelineBoundary
    SkillPipelineBoundary --> PipelineOrchestrationControl
    PipelineOrchestrationControl --> SkillOutputEntity

    classDef actor fill:#e1f5fe
    classDef boundary fill:#f3e5f5
    classDef control fill:#e8f5e8
    classDef entity fill:#fff3e0
```
