<!-- Identifier: T-01 -->

# Skill Development Process Test Cases

## Test Case Master List

This document tracks all test cases for validating the skill development process.

### Assessment Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-assess-001 | Initial skill assessment completion | Functional | Planned |
| tc-assess-002 | Progress assessment tracking | Functional | Planned |
| tc-assess-003 | Final skill validation | Functional | Planned |
| tc-assess-004 | Assessment data integrity | Data | Planned |

### Learning Path Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-path-001 | Learning path creation | Functional | Planned |
| tc-path-002 | Learning activity sequencing | Process | Planned |
| tc-path-003 | Resource allocation tracking | Integration | Planned |
| tc-path-004 | Path completion validation | Functional | Planned |

### Mentoring Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-mentor-001 | Mentor assignment process | Process | Planned |
| tc-mentor-002 | Mentoring session tracking | Functional | Planned |
| tc-mentor-003 | Mentor feedback collection | Data | Planned |

### Knowledge Transfer Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-transfer-001 | Knowledge sharing session | Process | Planned |
| tc-transfer-002 | Documentation creation | Functional | Planned |
| tc-transfer-003 | Team knowledge distribution | Integration | Planned |

### Integration Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-integration-001 | End-to-end skill development cycle | End-to-End | Planned |
| tc-integration-002 | Multi-team coordination | Integration | Planned |
| tc-integration-003 | External training integration | Integration | Planned |

### GitHub Integration Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-github-001 | Create GitHub Issue from new local task file | Functional | Planned |
| tc-github-002 | Update existing GitHub Issue when local task is modified | Functional | Planned |
| tc-github-003 | Sync open/closed state from GitHub Issue to local task status | Functional | Planned |
| tc-github-004 | Preserve local task frontmatter format during sync | Data | Planned |
| tc-github-005 | Handle GitHub API rate limit with exponential backoff | Integration | Planned |
| tc-github-006 | Authentication failure error handling | Exception | Planned |

### Hierarchical Diagram Generation Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-diagram-001 | Automatic actor stereotype inference from participant name | Functional | Passed |
| tc-diagram-002 | Automatic boundary stereotype inference (Gateway, Portal patterns) | Functional | Passed |
| tc-diagram-003 | Automatic entity stereotype inference (DB, Repository patterns) | Functional | Passed |
| tc-diagram-004 | Control stereotype as default fallback | Functional | Passed |
| tc-diagram-005 | Manual stereotype override takes precedence over inferred type | Functional | Passed |
| tc-diagram-006 | Box syntax generation with correct participant ordering (boundary first, entity last) | Functional | Passed |
| tc-diagram-007 | Actor declarations emitted before all box blocks | Functional | Passed |
| tc-diagram-008 | Multi-boundary diagram generation with distinct box blocks | Functional | Passed |

### Boundary Validation Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-bv-001 | VR-3: Block decomposition of entity-type participant | Functional | Passed |
| tc-bv-002 | VR-3: Block decomposition of boundary-type participant | Functional | Passed |
| tc-bv-003 | VR-3: Block decomposition of actor-type participant | Functional | Passed |
| tc-bv-004 | VR-3: Allow decomposition of control-type participant | Functional | Passed |
| tc-bv-005 | VR-2: Fail when actor sends directly to control inside box (bypasses boundary) | Functional | Passed |
| tc-bv-006 | VR-2: Pass when actor sends to boundary-type participant inside box | Functional | Passed |
| tc-bv-007 | VR-1: Fail when two distinct external actors both send directly into same boundary | Functional | Passed |
| tc-bv-008 | VR-1: Pass when single external actor sends into boundary | Functional | Passed |
| tc-bv-009 | VR-4: Warning emitted when boundary cohesion score < 0.3 (mixed functional concerns) | Functional | Passed |
| tc-bv-010 | VR-4: No warning when boundary participants share related functional domain | Functional | Passed |
| tc-bv-011 | Strict mode blocks diagram generation on VR-1/VR-2/VR-3 error | Process | Passed |
| tc-bv-012 | Advisory mode generates diagram and injects inline %% violation comments | Process | Passed |
| tc-bv-013 | boundary_validation_report JSON includes overall_status and per-rule results | Data | Passed |
| tc-bv-014 | Markdown validation summary table rendered in collaboration-diagrams.md | Data | Passed |

### Requirements Merge Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-merge-001 | Merge two non-overlapping requirement sets | Functional | Planned |
| tc-merge-002 | Detect and resolve duplicate requirements across sources | Functional | Planned |
| tc-merge-003 | Preserve source traceability in merged output | Data | Planned |
| tc-merge-004 | Stakeholder review workflow triggered for merged spec | Process | Planned |

### Hierarchy Management Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-hierarchy-001 | Decompose control-type participant — sub-folder and stubs created at Level N+1 | Functional | Planned |
| tc-hierarchy-002 | Reject decomposition of non-control participant (actor, boundary, entity) | Functional | Planned |
| tc-hierarchy-003 | Breadcrumb trail injected in child main.md with correct ancestor links | Functional | Planned |
| tc-hierarchy-004 | Parent Sub-Processes table updated after successful decomposition | Functional | Planned |
| tc-hierarchy-005 | hierarchy-index.md regenerated with BFS Mermaid flowchart after decomposition | Functional | Planned |
| tc-hierarchy-006 | hierarchy-metadata.json updated with new ProcessNode and complexity_metrics | Data | Planned |
| tc-hierarchy-007 | Advisory complexity warning emitted when interaction count exceeds 80% of Level 0 threshold (7) | Functional | Planned |
| tc-hierarchy-008 | Rollback removes sub-folder, restores parent files, and removes ProcessNode from metadata | Process | Planned |

### EDPS Compliance Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-compliance-001 | Group A delegation invokes diagram-generatecollaboration boundary-validation-only mode | Integration | Planned |
| tc-compliance-002 | Group B/C evaluation blocked and status BLOCKED when hierarchy-validation returns INVALID | Functional | Planned |
| tc-compliance-003 | Group C EP-2 traceability check passes when all hierarchy nodes have source requirement references | Functional | Planned |
| tc-compliance-004 | Compliance score decreases proportionally per failed rule; classification matches score bands | Data | Planned |
| tc-compliance-005 | Strict mode blocks compliance report generation on critical rule failure | Process | Planned |
| tc-compliance-006 | Remediation guidance includes skill name and rule reference for each failed rule | Data | Planned |

### Hierarchy Validation Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-hv-001 | HV-group: detect control participant at Level N+1 parent that is entity type at Level N | Functional | Planned |
| tc-hv-002 | HX-group: detect broken breadcrumb link and auto-fix with correct relative path | Functional | Planned |
| tc-hv-003 | HN-group: detect missing required file (process.md) in sub-folder | Functional | Planned |
| tc-hv-004 | Auto-fix for HN-4 metadata inconsistency applied; structural HV errors not auto-fixed | Process | Planned |

### Documentation Automation Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-docauto-001 | main.md generated with breadcrumb, participant summary, VR compliance table, and decomposition status | Functional | Planned |
| tc-docauto-002 | Content guard detects manually-authored stub (>10 lines) and prompts before overwrite | Functional | Planned |
| tc-docauto-003 | Level 0 domain-model.md correctly omits "Relationships to Parent Domain" section | Data | Planned |
| tc-docauto-004 | Acronym-aware PascalCase expansion preserves consecutive uppercase (e.g., EDPS → EDPS, not Edps) | Functional | Planned |

### Change Impact Analysis Test Cases

| Test Case ID | Description | Type | Status |
|-------------|-------------|------|--------|
| tc-impact-001 | CRITICAL risk level emits critical_flag=true and normalized_risk_level=HIGH | Data | Planned |
| tc-impact-002 | What-if mode returns impact report without modifying any hierarchy artifacts | Process | Planned |
| tc-impact-003 | Apply mode auto-repairs broken navigational link identified in CI-group analysis | Functional | Planned |

## Test Case Categories

### Functional Tests
Verify that individual process components work as designed.

### Process Tests
Validate that workflow sequences operate correctly.

### Data Tests
Ensure data integrity and consistency throughout the process.

### Integration Tests
Confirm that different process components work together properly.

### End-to-End Tests
Validate complete process scenarios from start to finish.

## Test Case Status Definitions

- **Planned**: Test case identified but not yet implemented
- **In Progress**: Test case implementation in progress
- **Complete**: Test case implemented and ready for execution
- **Executed**: Test case has been run
- **Passed**: Test case executed successfully
- **Failed**: Test case identified issues
- **Blocked**: Test case cannot proceed due to dependencies

## Coverage Metrics

### Process Coverage
Track which process steps have test coverage:
- [ ] Skills gap analysis
- [ ] Learning objective definition
- [ ] Learning path creation
- [ ] Resource assignment
- [ ] Learning activity execution
- [ ] Skill application in practice
- [ ] Skill assessment and validation
- [ ] Knowledge sharing
- [ ] Change management integration
- [ ] Skill Navigator orchestration
- [ ] Incremental requirements processing
- [x] GitHub integration workflow (tc-github-001 to tc-github-006)
- [ ] Requirements merging (tc-merge-001 to tc-merge-004)
- [x] Hierarchical diagram generation (tc-diagram-001 to tc-diagram-008)
- [x] Boundary validation rules (tc-bv-001 to tc-bv-014)
- [ ] Project documentation management
- [ ] Hierarchical process decomposition (tc-hierarchy-001 to tc-hierarchy-008)
- [ ] EDPS compliance checking (tc-compliance-001 to tc-compliance-006)
- [ ] Hierarchy structural validation (tc-hv-001 to tc-hv-004)
- [ ] Documentation automation (tc-docauto-001 to tc-docauto-004)
- [ ] Change impact analysis (tc-impact-001 to tc-impact-003)

### Role Coverage
Ensure testing covers all key roles:
- [ ] Team Member scenarios
- [ ] Team Lead scenarios
- [ ] Skill Manager scenarios
- [ ] Mentor scenarios
- [ ] HR/Learning Department scenarios
- [ ] Project Owner scenarios (GitHub integration approval)
- [ ] Developer scenarios (diagram generation, skill usage)