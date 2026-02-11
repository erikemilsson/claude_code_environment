# Scenario 02: Decision Blocking Prevents Premature Execution

Verify that `/work` blocks tasks whose `decision_dependencies` reference unresolved decisions and only dispatches unblocked work.

## State

- Phase 1: 3 tasks (Pending, no decision deps)
- Phase 2: 3 tasks (Pending, `decision_dependencies: ["DEC-001"]`)
- Phase 3: 2 tasks (Pending, `decision_dependencies: ["DEC-002"]`, plus phase dependency)
- DEC-001: status `draft`, `inflection_point: true`
- DEC-002: status `draft`, `inflection_point: false`

## Trace: `/work` Step 2b item 4 — Decision Check

- **Path:** work.md → Step 2b → item 4 (DECISION CHECK)
- For each task, read `decision_dependencies` → read decision record → check checkbox state
- Phase 2 tasks: DEC-001 unresolved → blocked
- Phase 3 tasks: DEC-002 unresolved → blocked (also phase-blocked)
- Phase 1 tasks: no decision deps → eligible

### Expected

- Both decisions surfaced with task counts
- Phase 1 tasks dispatched when user skips decision scoring

## Trace: `/work` after Phase 1 completes

- Phase 2 still blocked by DEC-001 despite Phase 1 being done
- Phase completion does NOT override decision blocking

### Expected

```
Phase 1 complete. Phase 2 is blocked by DEC-001 (Analysis Method).
Open the decision doc to make your selection, then run /work again.
```

## Trace: Dashboard regeneration

- **Path:** dashboard.md → Claude Blocked line, Action Required → Decisions, Tasks grouped by phase
- All phases visible, blocked tasks show decision dependency in "Blocked By" column
- Phase summary lines explain blocking reason

## Pass criteria

- [ ] Phase 2/3 tasks NOT dispatched
- [ ] Both blocked decisions surfaced with task counts
- [ ] Phase 1 tasks dispatched normally
- [ ] Dashboard shows Phase 2/3 as blocked with decision IDs
- [ ] After Phase 1 completes, DEC-001 re-surfaced (not skipped)
- [ ] Phase completion doesn't override decision blocking

## Fail indicators

- Phase 2 tasks dispatched without resolving DEC-001
- Only one of two blocking decisions mentioned
- Phase and decision dependencies treated as the same thing
