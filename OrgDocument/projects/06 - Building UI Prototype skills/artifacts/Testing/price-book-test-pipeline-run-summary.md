# Real-World Pipeline Test — Price Book Management System

**Branch**: `test-ui-prototype-skills`
**Date**: 2026-10-27
**Purpose**: Exercise the full UI Prototyping pipeline (S33–S38) against genuine, messy, externally-supplied source material — a raw, unpunctuated dictated transcript describing a Price Book/Category/Header/Item management system — as a second, independent confirmation beyond T11's toy-order-domain fixture.

## Why This Test Matters

T11's end-to-end validation used T03's clean, already-validated toy UI Model. This test instead starts from the messiest possible real input: a single run-on dictated paragraph with speech-recognition artifacts, no punctuation, and some genuinely ambiguous phrases — closer to what a real user might actually hand the pipeline than a tidy fixture.

## Pipeline Run Summary

| Stage | Output | Result |
|---|---|---|
| Source capture | `Source Materials/price-book-test/raw-dictated-requirements.md` | Raw transcript preserved verbatim |
| `requirements-sanitize` | `Analysis/price-book-test/sanitized-requirements.md` + `sanitization-report.md` | Reorganized into clean business requirements; 2 fields flagged `[REVIEW NEEDED]` rather than guessed |
| `requirements-ingest` | `Analysis/price-book-test/requirements.md`/`.json` | 24 atomic requirements (R-701–R-724), one (R-724) carries reduced confidence (0.6) reflecting the unresolved flags |
| Domain concept extraction | `Analysis/price-book-test/domain-concepts.md` | 4 entities (PriceBook, PriceCategory, PriceHeader, PriceItem) with a shared `VersionAuditInfo` value object for the repeated audit-field pattern |
| UI Model | `orgModel/.../price-book-test/ui-model.json` | 4 UI Model entries, one per entity — no splitting/merging needed since the source described exactly one screen per entity |
| `screen-generateinventory` (S33) | `screen-inventory.md`/`.json` | 4 screens, SCR-101–SCR-104 |
| `screen-generatelayout` (S34) | 4× `layout-spec.md` | Literal HTML/CSS per screen; SCR-104 (Price Item) visibly the richest, reflecting its larger attribute set |
| `screen-generatemockup` (S35) | 4× `mockup.html` | All validated: well-formed HTML, zero external file refs, no framework leakage, real cross-screen navigation |
| `screen-generateflow` (S36) | `interaction-flows.md` | One flow (IF-101), a 4-level drill-down chain; 6 edges, all independently verified against actual mockup hrefs (count matched exactly) |
| `screen-assembledocument` (S37) | `design-document.md`/`.json` | Consolidated, references rather than duplicates source artifacts; flags the 2 unresolved fields as a Known Open Item |
| `screen-discussfeedback` (S38) | `feedback-log.md` → `Changes/2026-10-27-PROC-CHG-101-*.md` | One role-played feedback item routed with no re-transcription, into a valid `change-management`-schema change document |

## Key Finding: The Pipeline Handles Genuinely Ambiguous Source Material Correctly

The most important result of this test isn't that four screens were generated — it's that **the pipeline correctly refused to silently resolve two genuinely ambiguous requirements**, instead:
1. Flagging them explicitly at the sanitization stage (not guessing a plausible-sounding name)
2. Carrying that flag through the domain model (`FlagAttribute5`/`FlagAttribute6` placeholders, not invented names)
3. Carrying it further into the generated screen itself (`[REVIEW NEEDED]` labels, visible in the actual mockup, not hidden)
4. Surfacing it again in the consolidated design document's "Known Open Item" section
5. Finally generating a real, routable change request asking for exactly this clarification

This is the discipline pattern designed throughout T04–T09 (e.g., `screen-generateinventory`'s "flag rather than invent a destination," `screen-generatelayout`'s literalness requirement using *realistic* values rather than guesses) surviving contact with real messy input, not just performing correctly against a clean fixture.

## Confirmed Working a Second Time (Not Fixture-Specific)

- **Manual flow verification** (grep-count cross-check) scaled cleanly from 2 screens/3 edges (T11) to 4 screens/6 edges (this test) with the same technique
- **Feedback→change-management routing** worked against an independent project, confirming T09's TR-09.1 schema-compatibility finding isn't specific to the toy-order-domain's change type or structure
- **The shared list+tabbed-detail layout pattern across 4 screens** demonstrates the pipeline correctly recognizing and reusing a repeated structural pattern described once and implied for every entity, rather than treating each screen as an isolated design problem

## No Pipeline Defects Found

Every artifact generated cleanly against gate-style checks (HTML validity, zero external refs, no framework leakage, changelog presence, link resolution). No skill or convention from T01–T11 needed revision as a result of this test.
