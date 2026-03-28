# Hierarchical Process Examples

**Project**: 03-Building-Skills-Iteration-2  
**Created**: March 13, 2026  
**Purpose**: Concrete examples demonstrating hierarchical EDPS modeling with boundaries

## Example 1: User-Computer Interaction

### Level 0: External System View
**Scope**: User interaction with computer system
**Focus**: High-level operation request

```mermaid
sequenceDiagram
    participant User@{ "type" : "actor" } as External User
    participant Computer@{ "type" : "control" } as Computer System
    
    User->>Computer: Execute Program
    Computer->>User: Return Results
```

**Analysis**: Computer System is a control type, eligible for decomposition into sub-processes.

### Level 1: Computer System Boundary
**Scope**: Internal computer system components  
**Focus**: Hardware component collaboration

```mermaid
sequenceDiagram
    participant User@{ "type" : "actor" } as External User
    
    box Computer System Boundary
        participant CPU@{ "type" : "control" } as Central Processing Unit
        participant Memory@{ "type" : "entity" } as System Memory
        participant Storage@{ "type" : "entity" } as Storage Device
        participant IO@{ "type" : "boundary" } as I/O Controller
    end
    
    User->>IO: Execute Program Request
    IO->>CPU: Forward Program Request
    
    Note over CPU,IO: Internal hardware collaboration
    CPU->>Memory: Load Program Instructions
    Memory->>CPU: Return Instructions
    CPU->>Storage: Read Program Data
    Storage->>CPU: Return Data
    CPU->>IO: Output Results
    IO->>User: Display Results
```

**Boundary Rules Applied:**
- **Single external interface**: User → I/O Controller (boundary type first recipient)
- **System decomposition**: Only CPU (control type) can be further decomposed
- **Entity stability**: Memory and Storage (entity type) represent stable resources
- **UI mediation**: I/O Controller (boundary type) mediates between actor and internal systems

### Level 2: CPU Boundary (Sub-process)
**Scope**: Internal CPU operations  
**Focus**: Processing unit components

```mermaid
sequenceDiagram
    participant System@{ "type" : "control" } as Computer System
    
    box CPU Boundary
        participant Control@{ "type" : "boundary" } as Control Unit
        participant ALU@{ "type" : "control" } as Arithmetic Logic Unit  
        participant Registers@{ "type" : "entity" } as CPU Registers
        participant Cache@{ "type" : "entity" } as CPU Cache
    end
    
    System->>Control: Execute Instruction
    
    Note over Control,Cache: Internal CPU operations
    Control->>Cache: Fetch Next Instruction
    Control->>Registers: Load Operands
    Control->>ALU: Execute Operation
    ALU->>Registers: Store Result
    Registers->>Control: Operation Complete
```

**Sub-Folder Structure:**
```
01-UserComputerInteraction/
├── main.md
├── collaboration.md          # Level 0 diagram
├── process.md
└── 01-ComputerSystemBoundary/
    ├── main.md
    ├── collaboration.md      # Level 1 diagram
    ├── 01-CPUBoundary/
    │   ├── main.md
    │   └── collaboration.md  # Level 2 diagram
    ├── 02-MemoryBoundary/
    └── 03-StorageBoundary/
```

## Example 2: E-commerce Order Processing

### Level 0: Customer Journey
**Scope**: Customer interaction with e-commerce system
**Focus**: End-to-end order placement

```mermaid
sequenceDiagram
    participant Customer@{ "type" : "actor" } as Customer
    participant ECommerce@{ "type" : "control" } as E-commerce Platform
    participant Payment@{ "type" : "control" } as Payment Provider
    participant Fulfillment@{ "type" : "control" } as Fulfillment Center
    
    Customer->>ECommerce: Browse & Select Items
    Customer->>ECommerce: Place Order
    ECommerce->>Payment: Process Payment
    ECommerce->>Fulfillment: Fulfill Order
    Fulfillment->>Customer: Deliver Product
```

**Analysis**: All three systems (E-commerce Platform, Payment Provider, Fulfillment Center) are control types and can be decomposed into sub-processes.

### Level 1: E-commerce Platform Boundary
**Scope**: Internal platform services
**Focus**: Service orchestration and workflow

```mermaid
sequenceDiagram
    participant Customer@{ "type" : "actor" } as Customer
    
    box E-commerce Platform Boundary
        participant Web@{ "type" : "boundary" } as Web Frontend
        participant Cart@{ "type" : "control" } as Shopping Cart Service
        participant Order@{ "type" : "control" } as Order Management Service
        participant Inventory@{ "type" : "control" } as Inventory Service
        participant Customer_Service@{ "type" : "entity" } as Customer Service
    end
    
    participant Payment@{ "type" : "control" } as External Payment Provider
    
    Customer->>Web: Browse Products
    Web->>Inventory: Check Product Availability
    Customer->>Web: Add Items to Cart
    Web->>Cart: Update Shopping Cart
    Customer->>Web: Proceed to Checkout
    Web->>Order: Create Order
    Order->>Customer_Service: Validate Customer
    Order->>Inventory: Reserve Items
    Order->>Payment: Process Payment Request
```

**Participant Type Analysis:**
- **Web Frontend (boundary)**: First recipient of customer interactions, mediates all customer-system communication
- **Services (control) - Cart, Order, Inventory**: Can be decomposed into detailed sub-processes
- **Customer Service (entity)**: Data/resource component, typically stable
- **Decomposition Candidates**: Cart Service, Order Management Service, Inventory Service

### Level 2: Order Management Service Boundary
**Scope**: Internal order processing logic
**Focus**: Order lifecycle management

```mermaid
sequenceDiagram
    participant Platform@{ "type" : "control" } as E-commerce Platform
    
    box Order Management Service Boundary
        participant API@{ "type" : "boundary" } as Order API
        participant Validator@{ "type" : "control" } as Order Validator
        participant Engine@{ "type" : "control" } as Order Processing Engine
        participant Repository@{ "type" : "entity" } as Order Repository
        participant Events@{ "type" : "control" } as Event Publisher
    end
    
    Platform->>API: Create New Order
    
    Note over API,Events: Internal order processing
    API->>Validator: Validate Order Data
    Validator->>Engine: Process Valid Order
    Engine->>Repository: Store Order Record
    Repository->>Events: Trigger Order Events
    Events->>Engine: Confirm Event Published
    Engine->>API: Order Processing Complete
```

### Level 3: Order Processing Engine Boundary
**Scope**: Core business logic implementation
**Focus**: Decision making and state management

```mermaid
sequenceDiagram
    participant OrderService@{ "type" : "control" } as Order Management Service
    
    box Order Processing Engine Boundary
        participant Workflow@{ "type" : "boundary" } as Workflow Orchestrator
        participant Rules@{ "type" : "control" } as Business Rules Engine
        participant State@{ "type" : "entity" } as Order State Manager
        participant Calculator@{ "type" : "control" } as Price Calculator
    end
    
    OrderService->>Workflow: Process Order Request
    
    Note over Workflow,Calculator: Business logic execution
    Workflow->>Rules: Validate Business Rules
    Rules->>Calculator: Calculate Order Total
    Calculator->>State: Update Order State
    State->>Workflow: State Updated
    Workflow->>Rules: Apply Approval Logic
```

**Stereotype Analysis:**
- **<<UI>> Workflow Orchestrator**: Entry point for order processing requests
- **<<System>> Components (Rules Engine, Calculator)**: Can be further decomposed if needed
- **<<Entity>> Order State Manager**: Persistent state storage, typically stable
- **Deep Decomposition**: Demonstrates 3-level hierarchy with consistent stereotype application

### Level 0: Development Team Process
**Scope**: Team interaction with development tools
**Focus**: Software delivery pipeline

```mermaid
sequenceDiagram
    participant Developer as Developer
    participant DevPlatform as Development Platform
    participant QA as QA Environment
    participant Production as Production Environment
    
    Developer->>DevPlatform: Commit Code Changes
    DevPlatform->>QA: Deploy to Testing
    QA->>DevPlatform: Run Test Suite
    DevPlatform->>Production: Deploy to Production
```

### Level 1: Development Platform Boundary
**Scope**: CI/CD platform components
**Focus**: Automated build and deployment pipeline

```mermaid
sequenceDiagram
    participant Developer as Developer
    
    box Development Platform Boundary
        participant Git as Git Repository
        participant CI as CI Server
        participant Registry as Artifact Registry
        participant CD as CD Pipeline
        participant Monitor as Monitoring System
    end
    
    Developer->>Git: Push Code Changes
    
    Note over Git,Monitor: Automated pipeline execution
    Git->>CI: Trigger Build
    CI->>Registry: Store Build Artifacts
    Registry->>CD: Deploy Artifacts
    CD->>Monitor: Update Deployment Status
    Monitor->>CI: Report Metrics
```

### Level 2: CI Server Boundary
**Scope**: Continuous integration process
**Focus**: Build, test, and validation steps

```mermaid
sequenceDiagram
    participant Platform as Development Platform
    
    box CI Server Boundary
        participant Trigger as Build Trigger
        participant Builder as Code Builder
        participant Tester as Test Runner
        participant Quality as Quality Gate
        participant Publisher as Artifact Publisher
    end
    
    Platform->>Trigger: Code Change Event
    
    Note over Trigger,Publisher: CI pipeline execution
    Trigger->>Builder: Start Build Process
    Builder->>Tester: Run Unit Tests
    Tester->>Quality: Validate Quality Metrics
    Quality->>Publisher: Publish Build Artifacts
```

## Participant Type Summary

### Participant Type Usage in Hierarchical Modeling

#### **Actor Type** (`@{ "type" : "actor" }`)
- **Purpose**: External entities that initiate interactions
- **Characteristics**: Remain outside all boundaries, cannot be decomposed  
- **Examples**: Customer, User, External User, Client Application, Team Member
- **Rule**: Always external, never within boundaries

#### **Boundary Type** (`@{ "type" : "boundary" }`)
- **Purpose**: Interface components that mediate actor-system communication
- **Characteristics**: Always first recipients within boundaries, cannot be decomposed
- **Examples**: Web Frontend, API Gateway, Control Unit, Order API, I/O Controller  
- **Rule**: Must be first recipient of actor messages within any boundary

#### **Control Type** (`@{ "type" : "control" }`)
- **Purpose**: Complex components with business logic
- **Characteristics**: Only type that can be decomposed into sub-processes
- **Examples**: Order Management Service, Query Engine, CPU, E-commerce Platform
- **Rule**: Eligible for hierarchical decomposition into sub-boundaries

#### **Entity Type** (`@{ "type" : "entity" }`)
- **Purpose**: Data storage, resources, or passive components  
- **Characteristics**: Typically stable, rarely decomposed
- **Examples**: Database, Order Repository, CPU Registers, System Memory
- **Rule**: Represent stable resources without internal process decomposition

### Decomposition Decision Matrix

| From Type | To Type | Decomposition Allowed | Positioning Rule |
|-----------|---------|----------------------|------------------|
| actor | Any | ❌ No | External only |
| boundary | Any | ❌ No | First recipient in boundary |
| control | boundary, control, entity | ✅ Yes | Business logic decomposition |
| entity | Any | ⚠️ Rare | Only if complex data processing |

### Implementation Guidelines for Skills

1. **Boundary Detection**: Look for control type participants as decomposition candidates
2. **UI Positioning**: Ensure boundary type participants receive first actor messages  
3. **Validation**: Check that only control type participants are marked for decomposition
4. **Consistency**: Maintain participant type patterns across all hierarchy levels

## Boundary Detection Patterns

### Pattern 1: Interface Responsibility
**Identification**: Components that primarily handle external interactions
**Examples**: API Gateway, Web Frontend, Database Interface

**Characteristics:**
- High external interaction frequency
- Low internal processing complexity
- Clear input/output transformation

### Pattern 2: Processing Responsibility  
**Identification**: Components that handle core business logic
**Examples**: Order Processing Engine, Payment Processor, Business Rules Engine

**Characteristics:**
- Complex internal state management
- Multiple internal collaborations
- Business rule enforcement

### Pattern 3: Storage Responsibility
**Identification**: Components that manage data persistence
**Examples**: Database System, File Storage, Cache Manager

**Characteristics:**
- Data CRUD operations
- Internal query optimization
- Transaction management

### Pattern 4: Communication Responsibility
**Identification**: Components that handle inter-system communication
**Examples**: Message Queue, Event Bus, API Client

**Characteristics:**
- External system integration
- Message routing and transformation
- Protocol handling

## Hierarchy Navigation Examples

### Folder Structure for E-commerce Example
```
01-CustomerOrderJourney/
├── main.md                                 # Level 0 overview
├── collaboration.md                        # Customer → Platform → Payment
├── process.md
├── 01-EcommercePlatformBoundary/
│   ├── main.md                             # Level 1 overview  
│   ├── collaboration.md                    # Platform internal services
│   ├── 01-OrderManagementBoundary/
│   │   ├── main.md                         # Level 2 overview
│   │   ├── collaboration.md                # Order service internals
│   │   └── 01-OrderProcessingEngineBoundary/
│   │       ├── main.md                     # Level 3 overview
│   │       └── collaboration.md           # Engine internals
│   ├── 02-InventoryServiceBoundary/
│   └── 03-CustomerServiceBoundary/
├── 02-PaymentProviderBoundary/
└── 03-FulfillmentCenterBoundary/
```

### Cross-Reference Links
Each level includes navigation links:

**Level 0 (main.md):**
```markdown
# Customer Order Journey

## Sub-Processes
- [E-commerce Platform](01-EcommercePlatformBoundary/main.md)
- [Payment Provider](02-PaymentProviderBoundary/main.md)
- [Fulfillment Center](03-FulfillmentCenterBoundary/main.md)
```

**Level 1 (E-commerce Platform main.md):**
```markdown
# E-commerce Platform Boundary

## Parent Process
- [Customer Order Journey](../main.md)

## Sub-Processes  
- [Order Management](01-OrderManagementBoundary/main.md)
- [Inventory Service](02-InventoryServiceBoundary/main.md)
- [Customer Service](03-CustomerServiceBoundary/main.md)
```

## Example 4: Organizational Skill Development Process (OrgModel Enhancement)

### Level 0: Organizational Learning Journey
**Scope**: Team member interaction with organizational skill development system
**Focus**: End-to-end skill development process

```mermaid
sequenceDiagram
    participant Member as Team Member
    participant OrgSystem as Skill Development System
    participant Manager as Learning Manager
    participant Organization as Organization
    
    Member->>OrgSystem: Request Skill Assessment
    OrgSystem->>Manager: Coordinate Learning Path
    Manager->>Organization: Report Development Progress
    Organization->>Member: Provide Resources & Recognition
```

### Level 1: Skill Development System Boundary
**Scope**: Internal organizational skill development components
**Focus**: System orchestration and capability management

```mermaid
sequenceDiagram
    participant Member as Team Member
    
    box Skill Development System Boundary
        participant Assessment as Skill Assessment Engine
        participant PathBuilder as Learning Path Builder
        participant ResourceManager as Resource Manager
        participant ProgressTracker as Progress Tracker
        participant SkillValidator as Skill Validator
    end
    
    participant Manager as Learning Manager
    
    Member->>Assessment: Complete Skill Evaluation
    Assessment->>PathBuilder: Generate Learning Recommendations
    PathBuilder->>ResourceManager: Allocate Learning Resources
    ResourceManager->>ProgressTracker: Initialize Progress Monitoring
    ProgressTracker->>SkillValidator: Schedule Validation Checkpoints
    SkillValidator->>Manager: Report Validation Results
```

### Level 2: Learning Path Builder Boundary
**Scope**: Internal learning path construction logic
**Focus**: Personalized curriculum development

```mermaid
sequenceDiagram
    participant SkillSystem as Skill Development System
    
    box Learning Path Builder Boundary
        participant Analyzer as Gap Analyzer
        participant Recommender as Learning Recommender
        participant Sequencer as Activity Sequencer
        participant Validator as Path Validator
    end
    
    SkillSystem->>Analyzer: Analyze Skill Gaps
    Analyzer->>Recommender: Identify Learning Needs
    Recommender->>Sequencer: Sequence Learning Activities
    Sequencer->>Validator: Validate Learning Path
    Validator->>SkillSystem: Deliver Personalized Path
```

**OrgModel Enhancement Benefits:**
- **Hierarchical Process Modeling**: Breaking down complex organizational processes into manageable boundaries
- **Clear Responsibility Zones**: Each boundary has well-defined responsibilities and interfaces
- **Scalable Organization**: Can decompose any organizational process to appropriate detail level
- **EDPS Alignment**: Organizational processes follow evolutionary development principles

## Benefits Demonstration

### Complexity Management
- **Level 0**: Focus on customer journey without technical details
- **Level 1**: Understand service architecture without implementation details  
- **Level 2**: Examine service internals without low-level code concerns

### Change Impact Analysis
- **Order API Change**: Affects Level 2 (Order Management) and below
- **Payment Provider Change**: Affects Level 0 and Payment Provider boundary
- **Database Schema Change**: Affects Level 3 (Repository) and related components

### Team Collaboration
- **Business Analysts**: Work with Level 0-1 diagrams
- **Solution Architects**: Focus on Level 1-2 service boundaries
- **Developers**: Implement Level 2-3 component interactions

---

**Next Steps:**
1. Use these examples to validate boundary detection algorithms
2. Test hierarchy generation with real project data
3. Implement cross-reference link automation  
4. Create migration tools for Project 1 diagrams
5. **Update OrgModel with hierarchical boundary concepts and organizational process examples**