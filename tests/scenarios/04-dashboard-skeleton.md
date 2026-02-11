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

1. **Header lines** — project name, stage, start date, completion %, task/decision counts
2. **Action Required** — both decisions in Decisions sub-section with links
3. **Progress** — phase table, critical path one-liner, all 3 phases with blocked reasons
4. **Tasks** — grouped by phase, per-phase summary lines with blocking reasons
5. **Decisions** — DEC-001 and DEC-002 with status

### Key details

- Progress phase table: `Phase 2 | 0 | 3 | Blocked (DEC-001)`
- Phase summary in Tasks: `*Phase 2: 0/3 complete — waiting on DEC-001*`
- Critical path one-liner includes: `❗ Resolve DEC-001 → 🤖 Phase 2 tasks → Done`

## Pass criteria

- [ ] ALL phases visible (not just Phase 1)
- [ ] ALL tasks across ALL phases visible
- [ ] Decision deps shown in task Deps column
- [ ] Phase summary lines explain what's blocking
- [ ] Progress phase table shows all phases with blocking reasons
- [ ] Critical path one-liner includes decision resolution steps
- [ ] Action Required → Decisions sub-section links to decision docs
- [ ] Tasks section shows blocked tasks with decision deps in Deps column
- [ ] Full project journey visible from dashboard alone

## Fail indicators

- Only Phase 1 tasks shown (blocked phases hidden)
- Tasks show as "Pending" without decision dependency info
- Phase summary says "0/3 complete" without explaining the block
- Critical path one-liner doesn't include decisions
- Dashboard requires reading task JSON to understand blocking
