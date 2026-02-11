# Scenario 04: Dashboard Shows Full Project Skeleton

Verify that the dashboard shows the complete project structure — all phases, all tasks, all decisions — even when most work is blocked.

## State

Same as Scenario 02:
- Phase 1: 3 tasks (Pending, ready)
- Phase 2: 3 tasks (Pending, blocked by DEC-001)
- Phase 3: 2 tasks (Pending, blocked by DEC-002 + Phase 2)
- DEC-001: draft, inflection_point: true
- DEC-002: draft, inflection_point: false

## Trace: Dashboard regeneration

- **Path:** dashboard.md → section structure and format hints; work.md § Dashboard Regeneration Procedure
- Source: all task-*.json files + all decision-*.md files

### Expected sections (exact headings from dashboard.md)

1. **Project Context** — name, phase, start date
2. **Needs Your Attention** — both decisions in Decisions Pending table with links
3. **Quick Status** — all 3 phases in table, blocked phases show reason
4. **Spec Alignment** — drift status
5. **Critical Path** — includes decision resolution as steps (with owner indicators)
6. **Claude Status** — Ready (Phase 1 tasks) + Blocked (Phase 2/3 tasks with reasons)
7. **All Decisions** — DEC-001 and DEC-002 with status
8. **All Tasks** — grouped by phase, per-phase summary lines with blocking reasons

### Key details

- Quick Status table: `Phase 2 | 0 | 3 | Blocked (DEC-001)`
- Blocked sub-section: `Task 4 | Run analysis | DEC-001 (Analysis Method)`
- Phase summary: `*Phase 2: 0/3 complete — waiting on DEC-001*`
- Critical Path includes: `You: Resolve DEC-001 — inflection point, triggers spec revision`

## Pass criteria

- [ ] ALL phases visible (not just Phase 1)
- [ ] ALL tasks across ALL phases visible
- [ ] Decision deps shown in task Deps column
- [ ] Phase summary lines explain what's blocking
- [ ] Quick Status shows all phases with blocking reasons
- [ ] Critical Path includes decision resolution steps with owner indicators
- [ ] Decisions Pending section links to decision docs
- [ ] Blocked section lists all blocked tasks with specific reasons
- [ ] Full project journey visible from dashboard alone

## Fail indicators

- Only Phase 1 tasks shown (blocked phases hidden)
- Tasks show as "Pending" without decision dependency info
- Phase summary says "0/3 complete" without explaining the block
- Critical path doesn't include decisions
- Dashboard requires reading task JSON to understand blocking
