# Scenario 01: Decision Discovery During `/iterate`

Verify that `/iterate` identifies spec sections with vague language implying unresolved choices and suggests creating decision records.

## State

- Spec exists with content (not empty/placeholder)
- Phase 2 says "Apply appropriate statistical methods" (vague method)
- Phase 3 says "Use a charting library suitable for academic publications" (unnamed choice)
- No decision records exist
- No tasks exist

## Trace

`/iterate` readiness check flags implicit decisions in vague spec text: "appropriate statistical methods" and "a charting library". User confirms statistical method is inflection point, charting library is pick-and-go.

### Expected suggestions

- `decision-001-analysis-method.md` with `inflection_point: true`
- `decision-002-charting-library.md` with `inflection_point: false`
- Spec updates referencing decisions by ID

## Pass criteria

- [ ] Readiness check flags `Key decisions documented: ✗`
- [ ] "appropriate statistical methods" identified as implicit decision
- [ ] "a charting library" identified as implicit decision
- [ ] Suggests creating decision records, not filling in choices inline
- [ ] Distinguishes inflection point vs pick-and-go based on user input
- [ ] Suggested spec updates reference decision IDs

## Fail indicators

- Spec declared "ready for /work" without flagging open choices
- Claude picks a method/library itself instead of creating a decision record
- Both decisions treated identically (no inflection vs pick-and-go distinction)
