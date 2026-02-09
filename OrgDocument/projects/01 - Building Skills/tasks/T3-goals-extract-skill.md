# Issue: T3 - Goals.Extract Skill
**State:** completed  
**Labels:** feature, core-skill, phase1  
**Assignees:** adam.wang  
**Milestone:** Phase 1 - Foundation & Core Skills  
**Priority:** High
**Issue Number:** #T3
**Estimated Effort:** 1.1 days
**Completed Date:** 2026-02-08

## Description
Develop the Goals.Extract skill that identifies and extracts business goals, success criteria, constraints, and assumptions from processed requirements. This skill provides strategic clarity for requirement analysis.

## Acceptance Criteria
- [x] Extracts business goals and objectives from requirement text
- [x] Identifies success criteria and key performance indicators
- [x] Discovers constraints, limitations, and assumptions
- [x] Produces structured markdown output with clear categorization
- [x] Maintains traceability to source requirements
- [x] Supports both explicit and implicit goal identification

## Tasks
- [x] Design goal extraction algorithms and classification system
- [x] Implement business goal and success criteria identification logic
- [x] Create constraint and assumption detection mechanisms
- [x] Build structured markdown output formatting
- [x] Test with various requirement types and domains
- [x] Document skill capabilities and usage examples

 ## Dependencies
- T1: Skill Framework Setup
- T2: Requirements.Ingest Skill (for input format consistency)

## Comments
**Completion Summary (Feb 8, 2026)**
The goals-extract skill has been successfully implemented with the following key features:

**Core Capabilities:**
- Rule-based pattern extraction using outcome cue words (`increase|reduce|improve|decrease|optimize|ensure|enhance|streamline|grow|expand`)
- Intent signal detection ("should aim to", "objective is to", "goal is to", "we will", "by [date]")
- spaCy/Universal Dependencies for grammatical analysis and (VERB→dobj) pattern extraction 
- Negative filtering to exclude system mandates unless followed by outcome language
- RAKE/YAKE/TextRank keyphrase extraction constrained to outcome sentences
- OpenIE for (subject, relation, object) tuple extraction with outcome verbs

**Implementation Approach:**
- Two-phase algorithm: Rule-based extraction (primary) + LLM validation (secondary)
- Focuses specifically on outcome goals vs. general business requirements
- >90% precision target for pattern-based extraction

**Outputs:**
- `goals.json` - Structured data with traceability fields and extraction metadata
- `goals.md` - Human-readable documentation with source references
- Complete traceability to source requirements with confidence scoring
- Integration with Analysis folder structure for seamless workflow

**Status:** Minimum viable implementation completed, ready for integration testing with requirements-ingest skill outputs.