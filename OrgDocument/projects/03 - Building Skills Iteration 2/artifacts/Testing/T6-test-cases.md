# T6: Sub-Folder Generation — Test Cases

**Task ID**: T6  
**Created**: March 14, 2026  
**Status**: All 24 test cases executed and passed (March 14, 2026)

---

## Category 1: Basic Sub-Folder Creation (TC-T6-001 – TC-T6-004)

### TC-T6-001: Standard single-level decomposition
**Given**: A Level 0 `collaboration.md` with a control-type participant `OrderService`; parent directory contains no existing sub-folders  
**When**: Sub-folder generation runs  
**Then**:  
- Folder `01-OrderServiceBoundary/` created inside the parent process folder  
- Files `collaboration.md`, `main.md`, `process.md`, `domain-model.md` all present  
- No other files created  
**Result**: PASS

### TC-T6-002: Sequential ordinal assignment for second decomposition
**Given**: Same Level 0 folder already has `01-OrderServiceBoundary/`; a second control-type `PaymentEngine` is decomposed  
**When**: Sub-folder generation runs  
**Then**: Folder `02-PaymentEngineBoundary/` created with all four standard files  
**Result**: PASS

### TC-T6-003: Ordinal reaches double digits
**Given**: Parent folder already has sub-folders `01` through `09`; a new decomposition is triggered  
**When**: Sub-folder generation runs  
**Then**: Folder `10-[ParticipantName]Boundary/` created (two-digit ordinal preserved)  
**Result**: PASS

### TC-T6-004: File set completeness check
**Given**: A basic single decomposition (TC-T6-001 scenario)  
**When**: Sub-folder generation completes  
**Then**: Exactly four files exist: `collaboration.md`, `main.md`, `process.md`, `domain-model.md`; no extra files are created  
**Result**: PASS

---

## Category 2: Multi-Level Folder Nesting (TC-T6-005 – TC-T6-007)

### TC-T6-005: Level 1 → Level 2 decomposition
**Given**: Level 0 folder has `01-OrderServiceBoundary/` (Level 1); inside it a control-type `ValidationEngine` is decomposed  
**When**: Sub-folder generation runs inside `01-OrderServiceBoundary/`  
**Then**: `01-OrderServiceBoundary/01-ValidationEngineBoundary/` created with all four standard files; `parent-level` in `main.md` references `../main.md`  
**Result**: PASS

### TC-T6-006: Level 2 → Level 3 decomposition
**Given**: `01-OrderServiceBoundary/01-ValidationEngineBoundary/` exists; control-type `RuleProcessor` inside it is decomposed  
**When**: Sub-folder generation runs  
**Then**: `…/01-ValidationEngineBoundary/01-RuleProcessorBoundary/` created with all four standard files; ordinal counter resets to `01` because parent has no prior sub-folders  
**Result**: PASS

### TC-T6-007: 5-level deep decomposition chain
**Given**: Hierarchy is L0 → L1 → L2 → L3 → L4 with a single decomposition at each level  
**When**: L4 control-type is decomposed  
**Then**: `01-…Boundary/` created at L5; `main.md` carries `Hierarchy Level: 5`; `process.md` flowchart header states `Parent Process: ./L4/process.md`  
**Result**: PASS

---

## Category 3: Naming Sanitization (TC-T6-008 – TC-T6-012)

### TC-T6-008: Participant name with internal spaces
**Given**: Participant name is `Order Service`  
**When**: Folder name is derived  
**Then**: Folder is `01-OrderServiceBoundary/` (PascalCase join, no space)  
**Result**: PASS

### TC-T6-009: Participant name with forward slash
**Given**: Participant name is `Order/Service`  
**When**: Folder name is derived  
**Then**: Slash is removed; folder is `01-OrderServiceBoundary/`  
**Result**: PASS

### TC-T6-010: Participant name with leading/trailing dots and hyphens
**Given**: Participant name is `.OrderService.`  
**When**: Folder name is derived  
**Then**: Leading and trailing dots stripped; folder is `01-OrderServiceBoundary/`  
**Result**: PASS

### TC-T6-011: Participant name with only prohibited characters
**Given**: Participant name is `??/:*`  
**When**: Folder name is derived  
**Then**: Error returned: `sanitized-name-empty` — all characters were illegal; user is asked to provide a valid participant name  
**Result**: PASS

### TC-T6-012: Non-ASCII characters (e.g., accented letters)
**Given**: Participant name is `OrderéService`  
**When**: Folder name is derived  
**Then**: Non-ASCII characters transliterated or removed; result is `01-OrderServiceBoundary/`; a warning is logged noting the transliteration  
**Result**: PASS

---

## Category 4: Naming Collision Resolution (TC-T6-013 – TC-T6-016)

### TC-T6-013: Exact collision — same ordinal, same name (user chooses skip)
**Given**: `01-OrderServiceBoundary/` already exists  
**When**: A second decomposition of `OrderService` is triggered and user selects "skip — reuse existing folder"  
**Then**: No new folder created; no files overwritten; user receives confirmation with path to existing folder  
**Result**: PASS

### TC-T6-014: Exact collision — same ordinal, same name (user chooses overwrite)
**Given**: `01-OrderServiceBoundary/` already exists with outdated `process.md`  
**When**: User selects "overwrite generated files"  
**Then**: `collaboration.md`, `main.md`, `process.md`, `domain-model.md` regenerated in place; `folder-creation.log` records `OVERWRITE` event  
**Result**: PASS

### TC-T6-015: Name-only collision (different ordinal)
**Given**: A folder named `03-OrderServiceBoundary/` exists (manually moved); a fresh decomposition of `OrderService` is triggered  
**When**: Sub-folder generation assigns the next free ordinal (e.g., `01`)  
**Then**: New folder `01-OrderServiceBoundary/` created; no interference with `03-OrderServiceBoundary/`  
**Result**: PASS

### TC-T6-016: Ordinal-only collision (different participant, same number)
**Given**: Ordinal `02` is computed but `02-PaymentEngineBoundary/` already exists for a different participant  
**Then**: Ordinal incremented to `03`; folder `03-[NewParticipant]Boundary/` created; audit log notes ordinal bump  
**Result**: PASS

---

## Category 5: Template Content Population (TC-T6-017 – TC-T6-019)

### TC-T6-017: `main.md` hierarchy level and navigation links
**Given**: Decomposing `ValidationEngine` inside `01-OrderServiceBoundary/` (Level 1 → Level 2)  
**When**: `main.md` is generated  
**Then**:  
- `**Level**: 2` present  
- `**Parent Process**: [OrderService Boundary](../main.md)` present  
- Links to `collaboration.md`, `process.md`, `domain-model.md` present  
**Result**: PASS

### TC-T6-018: `process.md` activity steps inferred from collaboration diagram
**Given**: `collaboration.md` contains three message exchanges: request → process → respond  
**When**: `process.md` is generated  
**Then**: Mermaid flowchart contains at least three nodes matching the message labels; `Parent Process` header references `../process.md`  
**Result**: PASS

### TC-T6-019: `domain-model.md` classes match participant types
**Given**: `collaboration.md` has one `boundary`, one `control`, one `entity` participant  
**When**: `domain-model.md` is generated  
**Then**: Class diagram contains three classes with stereotypes `:::boundary`, `:::control`, `:::entity`; relationship arrows match message directions  
**Result**: PASS

---

## Category 6: Parent Navigation Updates (TC-T6-020 – TC-T6-021)

### TC-T6-020: Parent `main.md` Sub-Processes table updated
**Given**: Parent `main.md` has no Sub-Processes section  
**When**: Sub-folder generation completes  
**Then**: A `## Sub-Processes` table is added with columns Collaboration, Process Flow, Domain Model; one row for the new sub-folder with correct relative links  
**Result**: PASS

### TC-T6-021: Parent `collaboration.md` decomposition comment inserted
**Given**: Parent `collaboration.md` declares `participant OrderService@{ "type": "control" }`  
**When**: Sub-folder generation completes  
**Then**: Comment `%% Decomposition: OrderService → 01-OrderServiceBoundary/collaboration.md` appears immediately after that participant declaration  
**Result**: PASS

---

## Category 7: Audit Log (TC-T6-022 – TC-T6-024)

### TC-T6-022: Audit log created on first decomposition
**Given**: Parent process folder has no `folder-creation.log`  
**When**: First sub-folder is generated  
**Then**: `folder-creation.log` created with one `CREATED` entry containing timestamp, folder name, level, parent, files, and ordinal count  
**Result**: PASS

### TC-T6-023: Audit log appended on subsequent decompositions
**Given**: `folder-creation.log` already has one entry  
**When**: A second sub-folder is generated  
**Then**: Log now has two `CREATED` entries; earlier entry is unchanged  
**Result**: PASS

### TC-T6-024: Audit log records collision resolution
**Given**: Ordinal bump was required during naming collision (TC-T6-016 scenario)  
**When**: Sub-folder generation completes  
**Then**: `folder-creation.log` entry contains a `Collision:` line describing the resolution (e.g., "ordinal bumped from 02 to 03")  
**Result**: PASS

---

**Test Coverage Summary**

| Category | Tests | Passed |
|----------|-------|--------|
| Basic Sub-Folder Creation | 4 | 4 |
| Multi-Level Folder Nesting | 3 | 3 |
| Naming Sanitization | 5 | 5 |
| Naming Collision Resolution | 4 | 4 |
| Template Content Population | 3 | 3 |
| Parent Navigation Updates | 2 | 2 |
| Audit Log | 3 | 3 |
| **Total** | **24** | **24** |
