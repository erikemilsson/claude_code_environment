# Scenario 01: Decision Discovery During `/iterate`

Verify that `/iterate` identifies spec sections with vague language implying unresolved choices and suggests creating decision records.

## State

- Spec exists with content (not empty/placeholder)
- Phase 2 says "Apply appropriate statistical methods" (vague method)
- Phase 3 says "Use a charting library suitable for academic publications" (unnamed choice)
- No decision records exist
- No tasks exist

## Trace: `/iterate` Step 2 — Readiness Assessment

- **Path:** iterate.md → "If spec has content" → readiness checklist
- Checklist item `Key decisions documented: ✗` triggers (0 decision records)
- **Implicit decision detection** (iterate.md, after checklist): scan spec for vague language
  - "appropriate statistical methods" → matches "vague method references" pattern
  - "a charting library" → matches "unnamed technology choices" pattern
- Both flagged as implicit decisions contributing to `✗`

### Expected

```
Key decisions documented: ✗
  - Resolved decisions: 0
  - (2 implicit decisions detected in spec text)
```

## Trace: `/iterate` Steps 3-4 — Questions and Suggestions

- Step 3: Questions surface whether each is inflection point or pick-and-go
- User confirms: statistical method is critical (affects data prep + reporting), charting library matters less
- Step 4: **Must suggest decision records** (iterate.md: "suggest creating a decision record rather than filling in the choice inline")

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
