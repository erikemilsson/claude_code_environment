# Scenario 25: Research Agent Triggered from /iterate Implicit Decision Detection

Verify that `/iterate` correctly detects implicit decisions in spec text, offers the research option, and delegates to the research workflow when selected.

## State

- Spec v1: status `draft`, has content with several sections
- Spec text includes: "The system will use a suitable charting library to render dashboards"
- Spec text includes: "Data will be stored in a database"
- No decision records exist yet
- No tasks exist yet (pre-decomposition)

## Trace: `/iterate` implicit decision detection

- iterate.md Step 2: spec has content → readiness check
- Scans for vague language:
  - "a suitable charting library" → implicit technology decision
  - "a database" → implicit technology decision
- Reports in readiness check: `Key decisions documented: ✗`

### Expected

For each implicit decision, presents options:
```
Implicit decision detected: Charting library selection ("a suitable charting library")
  [C] Create decision record and research options (spawns research-agent)
  [R] Create decision record only (you'll research later)
  [S] Skip (not a real decision)
```

## Trace: User selects [C] for charting library

1. `/iterate` creates decision record:
   - `decision-001-charting-library.md`
   - Frontmatter: id `DEC-001`, status `draft`, category `technology`
   - Background pre-filled from spec context
2. Delegates to research workflow (research.md Steps 2-4):
   - Gathers context from spec and new decision record
   - Spawns research-agent

### Expected

- Decision record created before research-agent spawned
- Research-agent receives the decision record path
- After research completes, decision has populated options and status `proposed`

## Trace: User selects [R] for database

1. `/iterate` creates decision record:
   - `decision-002-database-choice.md`
   - Frontmatter: id `DEC-002`, status `draft`, category `technology`
   - Background pre-filled from spec context
2. No research-agent spawned

### Expected

- Decision record created with empty comparison matrix
- Status remains `draft`
- User can later run `/research DEC-002` to populate it

## Trace: User selects [S] for a false positive

- If spec says "we will use React" — that's a stated choice, not an implicit decision
- User selects [S]

### Expected

- No decision record created
- No research-agent spawned
- `/iterate` continues to next implicit decision or Step 3

## Pass criteria

- [ ] Implicit decisions detected from vague spec language
- [ ] Three options presented per implicit decision: [C], [R], [S]
- [ ] [C] creates decision record THEN spawns research-agent
- [ ] [R] creates decision record without research
- [ ] [S] skips without creating anything
- [ ] Decision IDs assigned sequentially (DEC-001, DEC-002)
- [ ] Category correctly inferred (technology for libraries/databases)
- [ ] Background section pre-filled from spec context
- [ ] Multiple implicit decisions handled independently (each gets its own choice)
- [ ] `/iterate` continues to Step 3 (questions) after handling all implicit decisions

## Fail indicators

- Research-agent spawned without first creating a decision record
- All implicit decisions bundled into one prompt (should be individual)
- Decision record created in wrong directory
- Stated choices (not vague) flagged as implicit decisions
- `/iterate` skips Step 3 questions after handling decisions
