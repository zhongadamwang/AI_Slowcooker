# Domain Concepts Analysis

**Project**: simple-todo-app  
**Generated**: 2026-02-20T18:45:19Z  
**Source**: requirements.json, goals.json  
**Total Entities**: 3 | **Total Concepts**: 4

## Domain Areas

### Task Management
**Key Entities**: User, Task, TodoList  
**Core Concepts**: Task Management, Progressive Completion  
**Primary Processes**: Create Task, Edit Task, Mark Complete, View Progress

### Data Management  
**Key Entities**: TodoList  
**Core Concepts**: Persistence  
**Primary Processes**: Save Data, Load Data, Session Management

### User Interface
**Key Entities**: User  
**Core Concepts**: Responsive Design  
**Primary Processes**: Display Tasks, Handle Input, Provide Feedback

## Entities

### User *(ENT-001)*
**Domain Area**: Task Management  
**Description**: Individual person using the todo application for personal task management

**Attributes**:
- `session_id` (identifier): Browser session identifier for local storage access [private]
- `preferences` (object): User interface and display preferences [private]

**Operations**:
- `createTask(task_description)` → Task: Create a new task with text description [public]
- `editTask(task_id, new_description)` → void: Modify existing task description [public]
- `markComplete(task_id)` → void: Mark task as completed [public]
- `viewTasks()` → Task[]: Display current task list with completion status [public]

**Source References**: [R-001:Core Functionality], [R-002:Core Functionality], [R-008:User Interface Requirements], [R-009:User Interface Requirements]

### Task *(ENT-002)*
**Domain Area**: Task Management  
**Description**: Individual todo item with description and completion status

**Attributes**:
- `task_id` (identifier): Unique identifier for the task [public]
- `description` (string): Text description of the task to be completed [public]
- `is_completed` (boolean): Completion status of the task [public] 
- `created_at` (datetime): Timestamp when task was created [public]
- `completed_at` (datetime): Timestamp when task was marked complete [public]

**Operations**:
- `updateDescription(new_description)` → void: Change task description text [public]
- `toggleComplete()` → void: Switch completion status [public]

**Source References**: [R-001:Core Functionality], [R-002:Core Functionality], [R-003:Core Functionality], [R-004:Core Functionality]

### TodoList *(ENT-003)*
**Domain Area**: Task Management  
**Description**: Collection of tasks with persistence and display management

**Attributes**:
- `tasks` (array): Collection of Task objects [private]
- `total_count` (number): Total number of tasks in list [public]
- `completed_count` (number): Number of completed tasks [public]
- `remaining_count` (number): Number of incomplete tasks [public]

**Operations**:
- `addTask(task)` → void: Add new task to the list [public]
- `removeTask(task_id)` → boolean: Remove task from the list [public]
- `sortByNewest()` → void: Order tasks with newest at top [public]
- `persistToStorage()` → boolean: Save current list to browser local storage [private]
- `loadFromStorage()` → boolean: Restore list from browser local storage [private]
- `getProgressSummary()` → object: Return completion statistics [public]

**Source References**: [R-004:Core Functionality], [R-005:Core Functionality], [R-006:Core Functionality]

## Business Concepts

### Task Management *(CON-001)*
**Domain Area**: Personal Productivity  
**Definition**: Process of organizing, tracking, and completing individual work items or activities  
**Synonyms**: todo management, task tracking, activity organization  
**Source References**: [simple-todo-app.md:Project Overview]

### Persistence *(CON-002)*  
**Domain Area**: Data Management  
**Definition**: Data storage capability that maintains information across application sessions  
**Synonyms**: data storage, session memory, local storage  
**Source References**: [R-006:Core Functionality], [R-012:Technical Considerations]

### Progressive Completion *(CON-003)*
**Domain Area**: User Experience  
**Definition**: Workflow where users mark items as done while maintaining visibility for reference  
**Synonyms**: task completion, progress tracking, completion workflow  
**Source References**: [R-003:Core Functionality], [R-005:Core Functionality]

### Responsive Design *(CON-004)*
**Domain Area**: User Interface  
**Definition**: Interface adaptability to work effectively on both desktop and mobile devices  
**Synonyms**: mobile-friendly, cross-platform interface, adaptive layout  
**Source References**: [R-010:User Interface Requirements]

## Terminology Glossary

| Term | Definition | Domain Area | Context |
|------|------------|-------------|---------|
| Todo List | Collection of tasks or activities to be completed | Task Management | Primary application data structure |
| Local Storage | Browser-based data storage that persists without server connectivity | Technical Infrastructure | Data persistence mechanism |
| Responsive | Interface design that adapts to different screen sizes | User Interface | Cross-device compatibility requirement |
| Session | Period of continuous application use within browser context | Data Management | Data persistence scope |

## Entity Relationships

### TodoList ↔ Task *(REL-001)*
**Type**: Composition (one-to-many)  
**Description**: TodoList contains and manages multiple Task objects  
**Source**: [R-004:Core Functionality], [R-005:Core Functionality]

### User ↔ TodoList *(REL-002)*
**Type**: Interaction (one-to-one)  
**Description**: User interacts with TodoList through create, edit, and view operations  
**Source**: [R-001:Core Functionality], [R-008:User Interface Requirements]

### User ↔ Task *(REL-003)*
**Type**: Operation (one-to-many)  
**Description**: User directly manipulates Task objects through edit and completion actions  
**Source**: [R-002:Core Functionality], [R-003:Core Functionality], [R-009:User Interface Requirements]

---
**Traceability**: Extracted from requirements [R-001, R-002, R-003, R-004, R-005, R-006, R-007, R-008, R-009, R-010, R-011, R-012]  
**Confidence Score**: 0.92/1.0  
**Generated**: 2026-02-20T18:45:19Z