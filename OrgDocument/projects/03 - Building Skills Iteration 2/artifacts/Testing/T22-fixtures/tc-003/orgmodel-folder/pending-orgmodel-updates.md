# Pending OrgModel Updates

**Folder**: `T22-fixtures/tc-003/orgmodel-folder/`
**Generated**: 2026-03-15T09:30:00Z
**Source Analysis**: `T22-fixtures/tc-003/input/domain-concepts.json`
**Guard Triggered By**: `hierarchy-metadata.json` found at `T22-fixtures/tc-003/orgmodel-folder/hierarchy-metadata.json`

> ⚠ This folder is managed by an EDPS hierarchy. The four shared files (`main.md`, `process.md`,
> `collaboration.md`, `domain-model.md`) were NOT overwritten. Apply the additions below manually,
> or re-run `documentation-automation --force` with the domain-concepts.json listed above as context.

> 💡 Recommendation: Re-run `documentation-automation` with `domain-concepts.json` at
> `T22-fixtures/tc-003/input/domain-concepts.json` as context to incorporate structural changes
> into the hierarchy-managed files.

> ✅ Guard-exempt files updated directly: `vocabulary.md` (5 → 7 terms), `test-case-list.md` (4 → 7 test cases).

## Proposed Additions

### New Domain Entities

| Entity | Definition | Domain Area | Source |
|--------|------------|-------------|--------|
| SkillInvocationLog | Audit record capturing who invoked a skill, when, with what inputs, and what outputs were produced. | Audit and Traceability | T22-fixtures/tc-003/input/domain-concepts.json (R-44) |

### New Vocabulary Terms

_Already merged into `vocabulary.md` (guard-exempt). No action needed here._

| Term | Action |
|------|--------|
| Skill Invocation Log | ✅ Added to vocabulary.md |
| Outcome Status | ✅ Added to vocabulary.md |

### Process Notes

- `SkillInvocationLog` references `SkillOutputEntity` and is linked to `PractitionerActor` — consider adding to the class diagram in `domain-model.md` and updating the participant summary in `main.md`.
- Consider adding a `log()` activity step to `process.md` at the pipeline completion stage.

## Human Action Required

- [ ] Review `SkillInvocationLog` entity above
- [ ] Merge entity into `domain-model.md` class diagram
- [ ] Add `SkillInvocationLog` to participant summary in `main.md` if relevant
- [ ] Vocabulary terms already merged — verify for accuracy in `vocabulary.md`
- [ ] Test cases already added (rows 5–7 in `test-case-list.md`) — no action needed
- [ ] Re-run `documentation-automation` if `process.md` needs a log() step added
- [ ] Delete this file once all items are resolved
