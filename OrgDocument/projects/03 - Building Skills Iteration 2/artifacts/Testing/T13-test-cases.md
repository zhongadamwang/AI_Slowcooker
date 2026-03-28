# T13 Migration Tools — Test Cases

**Skill Under Test**: `migration-tools`  
**Created**: March 15, 2026  
**Total Test Cases**: 22  
**Categories**: Backward Compatibility, Participant Inference, Boundary Detection, Requirement Traceability, Preview vs Apply Mode, Batch vs Individual Scope, Error Handling, Non-Destructive Guarantee

---

## Category 1: Backward Compatibility (FR-T13.1)

### TC-T13-001 — Import Project 1 MD Without Modification
**Given**: `collaboration-diagrams.md` from Project 1 (flat sequenceDiagram, no boundaries)  
**When**: `migration-tools --mode preview` runs  
**Then**:
- Original `collaboration-diagrams.md` is not modified (hash unchanged)
- Preview output is shown in chat; no files written to disk
- **Expected result**: PASS

### TC-T13-002 — Import Project 1 JSON Without Modification
**Given**: `collaboration-diagrams.json` from Project 1  
**When**: `migration-tools --mode apply` runs  
**Then**:
- Original `collaboration-diagrams.json` is not modified (hash unchanged)
- `collaboration-diagrams-enhanced.json` is a new separate file
- **Expected result**: PASS

### TC-T13-003 — Both Source Files Present
**Given**: Both `collaboration-diagrams.md` and `collaboration-diagrams.json` are present  
**When**: Migration runs  
**Then**:
- JSON is used as primary source (authoritative participant list)
- MD is parsed as secondary (message order cross-reference)
- Both originals remain unmodified
- **Expected result**: PASS

### TC-T13-004 — MD-Only Source (No JSON)
**Given**: Only `collaboration-diagrams.md` present; no JSON file  
**When**: `migration-tools --mode apply` runs  
**Then**:
- Skill parses participant declarations and message lines from MD
- Enhanced files generated from MD-only parse
- Migration log notes MD-only mode
- **Expected result**: PASS

---

## Category 2: Participant Stereotype Inference (FR-T13.3)

### TC-T13-005 — Actor Inference (Rule 1)
**Given**: Participant `Dev as DeveloperTeamMember`  
**When**: Stereotype inference runs  
**Then**:
- Inferred type: `actor`
- Confidence: `HIGH`
- Inference rule: `1`
- **Expected result**: PASS

### TC-T13-006 — Entity Inference (Rule 3)
**Given**: Participants: `Output as ProjectArtifacts`, `Report as AssessmentReport`  
**When**: Stereotype inference runs  
**Then**:
- `Output` → `entity` (HIGH, rule 3 — contains "Artifacts")
- `Report` → `entity` (HIGH, rule 3 — contains "Report")
- **Expected result**: PASS

### TC-T13-007 — Control Inference (Rule 5, Workspace)
**Given**: Participant `VSC as VSCodeWorkspace`  
**When**: Stereotype inference runs  
**Then**:
- Inferred type: `control`
- Confidence: `MEDIUM`
- Inference rule: `5`
- **Expected result**: PASS

### TC-T13-008 — Control Inference (Rule 4, Framework)
**Given**: Participant `SF as SkillFramework`  
**When**: Stereotype inference runs  
**Then**:
- Inferred type: `control`
- Confidence: `MEDIUM`
- Inference rule: `4` (contains "Framework")
- **Expected result**: PASS

### TC-T13-009 — Fallback Inference (Rule 6)
**Given**: Participant `X as CustomThing` (no matching keywords)  
**When**: Stereotype inference runs  
**Then**:
- Inferred type: `control`
- Confidence: `LOW`
- Flagged as `INFERRED_FALLBACK` in migration log
- Listed in `## Human Review Required` section
- **Expected result**: PASS

### TC-T13-010 — All Project 1 D-001 Participants Classified
**Given**: Diagram D-001 participants: Dev, VSC, Skill (AIAgentSkill), Output (ProjectArtifacts)  
**When**: Inference runs  
**Then**:
- Dev → actor (HIGH)
- VSC → control (MEDIUM)
- Skill → control (MEDIUM, rule 4 — "Skill" not a match → fallback rule 5 or 6)
- Output → entity (HIGH, "Artifacts")
- **Expected result**: PASS (acceptable if Skill falls to MEDIUM/LOW with fallback)

---

## Category 3: Boundary Grouping Detection (FR-T13.2)

### TC-T13-011 — Actor Excluded from Boundaries
**Given**: Diagram with actor participant `Dev as DeveloperTeamMember`  
**When**: Boundary grouping runs  
**Then**:
- `Dev` is NOT enclosed in any `box` block
- `Dev` appears as a standalone `participant` line after all `box...end` blocks
- **Expected result**: PASS

### TC-T13-012 — Service Boundary Rule (Shared Prefix)
**Given**: Participants `AuthService`, `AuthDB`, `AuthValidator`  
**When**: Boundary detection runs  
**Then**:
- All three grouped into `Auth Boundary`
- Box color: `rgb(230,240,255)` (first boundary)
- **Expected result**: PASS

### TC-T13-013 — Closed Subgraph Heuristic
**Given**: `ProcessorA` and `StoreB` exchange messages only with each other (no messages to/from other participants)  
**When**: Boundary detection runs  
**Then**:
- `ProcessorA` and `StoreB` are grouped into the same boundary (colocation heuristic, rule 2)
- **Expected result**: PASS

### TC-T13-014 — Singleton Boundary Fallback
**Given**: A `control` participant `ReportGenerator` that shares no prefix keyword with any other participant  
**When**: Boundary detection runs  
**Then**:
- `ReportGenerator` is placed in a singleton boundary named `"ReportGenerator System"`
- **Expected result**: PASS

---

## Category 4: Requirement Traceability Preservation (FR-T13.5)

### TC-T13-015 — Source Requirements Preserved in Enhanced MD
**Given**: D-001 header: `**Source Requirements**: [R-019], [R-021], [R-023]`  
**When**: Enhanced MD is generated  
**Then**:
- Enhanced block header contains exactly `**Source Requirements**: [R-019], [R-021], [R-023]`
- No requirement reference is missing, reformatted, or renamed
- **Expected result**: PASS

### TC-T13-016 — Source Requirements Preserved in Enhanced JSON
**Given**: D-001 original JSON `"source_requirements": ["R-019", "R-021", "R-023"]`  
**When**: Enhanced JSON is generated  
**Then**:
- `enhanced.source_requirements` = `["R-019", "R-021", "R-023"]`
- **Expected result**: PASS

### TC-T13-017 — Message Lines Preserved Verbatim
**Given**: D-001 contains `Dev->>VSC: Open project workspace` and alt/loop blocks  
**When**: Enhanced diagram is generated  
**Then**:
- Every message line from original appears unchanged in enhanced block
- `alt/else/end` and `Note over` blocks preserved verbatim
- **Expected result**: PASS

---

## Category 5: Preview vs Apply Mode (TR-T13.1)

### TC-T13-018 — Preview Mode: No Files Written
**Given**: `--mode preview`  
**When**: Migration runs  
**Then**:
- `collaboration-diagrams-enhanced.md` does NOT exist (or is unchanged if pre-existing)
- `migration-log.md` does NOT exist on disk
- Preview summary shown in chat window
- **Expected result**: PASS

### TC-T13-019 — Apply Mode: All Three Files Written
**Given**: `--mode apply`  
**When**: Migration runs  
**Then**:
- `collaboration-diagrams-enhanced.md` created/updated
- `collaboration-diagrams-enhanced.json` created/updated
- `migration-log.md` created/updated
- **Expected result**: PASS

---

## Category 6: Batch vs Individual Scope (TR-T13.1)

### TC-T13-020 — Individual Scope: Only Target Diagram Updated
**Given**: `--mode apply --scope diagram=D-002` with pre-existing enhanced file containing D-001-E  
**When**: Migration runs  
**Then**:
- D-002-E is added/updated in enhanced files
- D-001-E content in enhanced files is preserved verbatim (not overwritten)
- **Expected result**: PASS

---

## Category 7: Migration Log (TR-T13.2)

### TC-T13-021 — Migration Log Structure
**Given**: Batch apply of a 5-diagram source file  
**When**: `migration-log.md` is generated  
**Then**:
- Summary table shows: Diagrams processed=5, Participants annotated=N, Boundaries added=N
- Per-diagram section exists for each of the 5 diagrams
- Any LOW-confidence participants listed in `## Human Review Required`
- **Expected result**: PASS

---

## Category 8: Error Handling

### TC-T13-022 — Source File Not Found
**Given**: No `collaboration-diagrams.md` or `.json` in the specified path  
**When**: Migration runs  
**Then**:
- Error code `ERR_NO_SOURCE` emitted
- Descriptive message: "Provide path to collaboration-diagrams.md or collaboration-diagrams.json"
- No files written
- **Expected result**: PASS
