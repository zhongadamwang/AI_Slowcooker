# Collaboration Diagrams

**Project**: simple-todo-app  
**Generated**: 2026-02-20T18:45:20Z  
**Source**: domain-concepts.json, requirements.json

## Domain Class Model

### Entity Relationship Overview *(Diagram D-001)*
**Source Requirements**: [R-001], [R-002], [R-003], [R-004], [R-005], [R-006]  
**Domain Entities**: User, Task, TodoList

```mermaid
classDiagram
    class User:::actor {
        -session_id: String
        -preferences: Object
        +createTask(description): Task
        +editTask(id, description): void
        +markComplete(id): void
        +viewTasks(): Task[]
    }
    
    class Task:::entity {
        +task_id: String
        +description: String
        +is_completed: Boolean
        +created_at: DateTime
        +completed_at: DateTime
        +updateDescription(text): void
        +toggleComplete(): void
    }
    
    class TodoList:::entity {
        -tasks: Array~Task~
        +total_count: Number
        +completed_count: Number  
        +remaining_count: Number
        +addTask(task): void
        +removeTask(id): Boolean
        +sortByNewest(): void
        -persistToStorage(): Boolean
        -loadFromStorage(): Boolean
        +getProgressSummary(): Object
    }
    
    User -->|interacts with| TodoList : manages
    TodoList *-->|contains| Task : composition
    User -->|operates on| Task : direct manipulation
```

## User-System Interactions

### Task Creation Flow *(Diagram D-002)*
**Source Requirements**: [R-001], [R-008]  
**Entities Involved**: User, TodoList, Task

```mermaid
sequenceDiagram
    participant U as User
    participant TL as TodoList
    participant T as Task
    participant LS as LocalStorage
    
    U->>+TL: createTask("Buy groceries")
    TL->>+T: new Task()
    T-->>-TL: task object created
    TL->>TL: addTask()
    TL->>TL: sortByNewest()
    TL->>+LS: persistToStorage()
    LS-->>-TL: save successful
    TL-->>-U: task added to list
    
    Note over U,LS: Simple text entry + Enter key
    Note over TL: Newest tasks appear at top
```

### Task Completion Flow *(Diagram D-003)*
**Source Requirements**: [R-003], [R-005], [R-009]  
**Entities Involved**: User, TodoList, Task

```mermaid
sequenceDiagram
    participant U as User
    participant TL as TodoList
    participant T as Task
    participant LS as LocalStorage
    
    U->>+TL: markComplete(task_id)
    TL->>+T: toggleComplete()
    T->>T: set is_completed = true
    T->>T: set completed_at = now()
    T-->>-TL: task updated
    TL->>TL: updateProgressCounts()
    TL->>+LS: persistToStorage()
    LS-->>-TL: save successful
    TL-->>-U: progress updated
    
    Note over U: Single click/tap operation
    Note over T: Task remains visible
    Note over TL: Counters updated for progress display
```

### Session Persistence Flow *(Diagram D-004)*
**Source Requirements**: [R-006], [R-012]  
**Entities Involved**: TodoList, LocalStorage

```mermaid
sequenceDiagram
    participant UA as User (App Start)
    participant TL as TodoList
    participant LS as LocalStorage
    participant UC as User (App Close)
    
    UA->>+TL: initialize()
    TL->>+LS: loadFromStorage()
    alt Data exists
        LS-->>TL: return saved tasks
        TL->>TL: restore task list
    else No data
        LS-->>TL: return empty
        TL->>TL: initialize empty list
    end
    TL-->>-UA: app ready with tasks
    
    Note over UA,UC: Session boundary
    
    UC->>+TL: application closing
    TL->>+LS: persistToStorage() 
    LS-->>-TL: data saved
    TL-->>-UC: session ended
    
    Note over LS: No internet connectivity required
    Note over TL: Data persists across browser sessions
```

## System Workflows

### Task Management Process *(Diagram D-005)*
**Source Requirements**: [R-001], [R-002], [R-003], [R-004], [R-005]  
**Business Process**: Complete task lifecycle

```mermaid
flowchart TD
    A[User opens app] --> B[Load existing tasks]
    B --> C{Any existing tasks?}
    C -->|Yes| D[Display sorted list]
    C -->|No| E[Show empty state]
    
    D --> F[User adds new task]
    E --> F
    F --> G[Enter task description]
    G --> H[Press Enter]
    H --> I[Task added to top of list]
    I --> J[Auto-save to local storage]
    
    J --> K{User wants to edit?}
    K -->|Yes| L[Click task description]
    K -->|No| M{Task completed?}
    
    L --> N[Modify text]
    N --> O[Save changes]
    O --> P[Auto-save to storage]
    P --> M
    
    M -->|Yes| Q[Single click/tap to complete]
    M -->|No| R[Continue using app]
    
    Q --> S[Mark as completed]
    S --> T[Update progress counters]
    T --> U[Auto-save to storage]
    U --> R
    
    R --> V{Add more tasks?}
    V -->|Yes| F
    V -->|No| W[View progress summary]
    W --> X[App session continues]
    
    style A fill:#e1f5fe
    style X fill:#e8f5e8
    style J fill:#fff3e0
    style P fill:#fff3e0
    style U fill:#fff3e0
```

### Responsive Interface Adaptation *(Diagram D-006)*
**Source Requirements**: [R-010], [R-007]  
**Cross-Platform Behavior**: Desktop/Mobile adaptation

```mermaid
flowchart LR
    A[User accesses app] --> B{Device type detection}
    
    B -->|Desktop| C[Wide screen layout]
    B -->|Mobile| D[Touch-optimized layout]
    
    C --> E[Keyboard-friendly input]
    C --> F[Mouse click interactions]
    C --> G[Full feature set display]
    
    D --> H[Touch keyboard input]
    D --> I[Touch tap interactions]
    D --> J[Simplified UI elements]
    
    E --> K[Enter key submission]
    F --> L[Precise cursor targeting]
    
    H --> M[Touch-friendly submission]
    I --> N[Large touch targets]
    
    G --> O[Detailed progress display]
    J --> P[Essential info only]
    
    K --> Q[Consistent app behavior]
    L --> Q
    M --> Q  
    N --> Q
    O --> Q
    P --> Q
    
    style B fill:#e1f5fe
    style Q fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fff3e0
```

---

**Diagram Summary**:
- **D-001**: Domain model showing core entities and relationships
- **D-002**: Task creation user workflow with persistence
- **D-003**: Task completion workflow with progress tracking  
- **D-004**: Session management and browser storage integration
- **D-005**: Complete business process flow for task lifecycle
- **D-006**: Responsive design adaptation for cross-platform usage

**Traceability**: Generated from domain entities [ENT-001, ENT-002, ENT-003] and requirements [R-001 through R-012]  
**Maintenance Priority**: All workflows are high priority for this core functionality  
**Generated**: 2026-02-20T18:45:20Z