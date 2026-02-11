# Scenario 21: Large Task History and Archival

Verify that the template remains performant and navigable when a project accumulates hundreds of completed tasks.

## Context

Long-lived projects accumulate significant task history. Real projects have reached 380+ tasks. The template must handle this scale: `/work` should focus on active tasks, the dashboard should remain useful, and archival should kick in at the documented threshold.

## State

- `.claude/tasks/` contains 380 task JSON files:
  - 350 completed
  - 20 pending (across 2 phases)
  - 10 in_progress (5 with implement-agent, 5 with verify-agent)
- `task-overview.md` is 2000+ lines
- Dashboard was last regenerated with 370 tasks (10 new since then)

## Trace 21A: /work focuses on active tasks

- **Path:** `/work` invoked with large task history
- Must identify eligible tasks among 380 total

### Expected

- `/work` efficiently finds pending/in_progress tasks without re-processing all 350 completed ones
- Task dispatch considers only active tasks for dependency checks
- Response time is not noticeably degraded by task volume

### Pass criteria

- [ ] Active task lookup does not require processing all completed tasks
- [ ] `/work` correctly identifies the 20 pending + 10 in_progress tasks
- [ ] Dependency resolution only considers relevant blocking relationships

### Fail indicators

- `/work` reads and processes all 380 task files before determining what to do
- Noticeable delay compared to a project with 10 tasks
- Completed tasks are re-evaluated for eligibility

---

## Trace 21B: Dashboard generation at scale

- **Path:** dashboard.md regeneration with 380 tasks
- Dashboard must show actionable information without becoming unwieldy

### Expected

- Dashboard shows recent completions (last N), not full history of 350
- Active tasks (in_progress, pending) are shown in detail
- Completed task count is summarized, not listed individually
- Dashboard length remains reasonable (not 2000+ lines)

### Pass criteria

- [ ] Dashboard generation doesn't degrade with task count
- [ ] Completed tasks are summarized, not individually listed
- [ ] Active tasks remain prominently displayed
- [ ] Dashboard remains under a reasonable line count

### Fail indicators

- Dashboard lists all 350 completed tasks individually
- Dashboard exceeds 200 lines due to task volume
- Active tasks are buried under completed task history
- Dashboard regeneration takes excessive time/context

---

## Trace 21C: Archival threshold triggers

- **Path:** `/work` or `/health-check` → archival check
- CLAUDE.md specifies archival threshold at 100 completed tasks
- Current count: 350 completed tasks, well above threshold

### Expected

- Archival is suggested (or triggered if automatic) when threshold is exceeded
- Completed tasks are moved to `.claude/tasks/archive/`
- Archived tasks are removed from active processing but preserved for reference
- `task-overview.md` is regenerated with only active tasks

### Pass criteria

- [ ] Archival is suggested when threshold is exceeded
- [ ] Archive location matches CLAUDE.md specification (`.claude/tasks/archive/`)
- [ ] Archived tasks are preserved, not deleted
- [ ] Active task processing improves after archival

### Fail indicators

- No archival suggestion despite 350 completed tasks (threshold is 100)
- Tasks are deleted instead of archived
- Archived tasks still processed during `/work` dispatch
- Archive goes to a non-standard location

---

## Trace 21D: /status responds quickly at scale

- **Path:** `/status` invoked with 380 tasks
- `/status` is documented as read-only and quick

### Expected

- `/status` provides a summary without processing every task file in detail
- Shows counts by status, current phase, and recent activity
- Does not regenerate the dashboard or modify any files

### Pass criteria

- [ ] `/status` responds without noticeable delay
- [ ] Summary is accurate (correct counts per status)
- [ ] No file modifications occur

### Fail indicators

- `/status` takes as long as `/work` to process
- Status output is wrong because it over-counts or under-counts
- `/status` triggers dashboard regeneration or task file updates
