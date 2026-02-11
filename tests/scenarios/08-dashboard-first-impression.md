# Scenario 08: Dashboard First Impression (Post-Iterate)

Verify that the dashboard provides useful, non-redundant information immediately after spec decomposition — the first time the user opens it side-by-side with Claude Code CLI.

## Context

This is the user's first real look at the dashboard. They've just run `/iterate`, gotten spec v1, and run `/work` which decomposed the spec into tasks. They open `dashboard.md` in a split pane. Their questions: What's the state of the project? What do I need to do? What's Claude doing?

## State

- Spec v1: active, 3 phases
- Phase 1: 4 tasks (Pending, owner: claude), 1 task (Pending, owner: human — "Configure API keys")
- Phase 2: 3 tasks (Pending, blocked by DEC-001), 1 task (Pending, owner: human)
- Phase 3: 2 tasks (Pending, blocked by Phase 2)
- DEC-001: draft, inflection_point: true, blocks Phase 2
- No work started yet
- No drift (just decomposed)
- No verification debt (nothing finished yet)

## Trace 08A: Information hierarchy — what the user sees first

- **Path:** dashboard.md → section structure (ordering)

### What appears above the fold (first ~30 lines)

The user sees `dashboard.md` in their editor. The first screenful determines whether the dashboard feels useful or overwhelming.

**Current section order (from dashboard.md):**
1. `# Dashboard` + metadata block + header line
2. `## Project Context` — name, phase, start date
3. `## 🚨 Needs Your Attention` — decisions, human tasks, reviews
4. `## Quick Status` — completion %, owner counts

### Expected (current spec)

- Project Context table: 3 rows (name, phase, date) — compact
- Needs Your Attention:
  - Verification Debt: `✅ No verification debt` (nothing to verify yet)
  - Decisions Pending: DEC-001 with link to decision doc
  - Tasks Ready for You: Task 5 "Configure API keys" with link to `.env.example`
  - Reviews & Approvals: empty (`*Nothing to review*`)
- Quick Status appears AFTER Needs Your Attention

### Observation: noise in early state

Several sub-sections are empty or uninformative at this stage:
- **Verification Debt** shows `✅ No verification debt` — accurate but takes space for a null result
- **Reviews & Approvals** shows `*Nothing to review*` — same issue
- **Spec Alignment** (section 5) shows `✅ All sections aligned` — of course it does, we just decomposed
- **Progress This Week** (section 8) shows `*No recent completions*` — nothing happened yet

### Pass criteria

- [ ] Needs Your Attention is visible without scrolling past boilerplate
- [ ] DEC-001 appears with a link to the decision doc file
- [ ] Human task "Configure API keys" appears with a link and action description
- [ ] Quick Status shows all 3 phases with blocking reasons for Phase 2 and 3
- [ ] Critical Path shows user actions (DEC-001 resolution) before Claude actions

### Fail indicators

- User must scroll past 3+ empty/null sections to reach actionable content
- DEC-001 appears in the table but without a clickable link to the file
- "Configure API keys" appears but user doesn't know what to do or where to go
- Spec Alignment section takes multiple lines to say "everything is fine"
- Progress This Week section takes multiple lines to say "nothing happened"

---

## Trace 08B: Section redundancy audit

- **Path:** dashboard.md → all section definitions

### Redundancy between sections at project start

| Information | Where it appears | Redundant? |
|-------------|------------------|------------|
| DEC-001 blocks Phase 2 | Needs Your Attention, Quick Status Phase table, Critical Path, Claude Status → Blocked, All Tasks Phase 2 summary | 5 places |
| Phase 2 is blocked | Quick Status, Critical Path, Claude Status, All Tasks | 4 places |
| Human task exists | Needs Your Attention, Quick Status owner counts, All Tasks | 3 places |
| No work started | Quick Status (0%), Claude Status, Progress This Week | 3 places |

### Expected

The dashboard should communicate each fact once in the right place, with cross-references only where they add context (e.g., "Blocked by DEC-001" in the task table is useful because it's next to the task).

### Pass criteria

- [ ] A piece of blocking information appears in at most 2 sections (primary + detail)
- [ ] Sections that are empty/null at project start are either excluded or collapsed to 1 line
- [ ] The dashboard for a fresh project fits in a reasonable scroll (< 80 lines of rendered content)

### Fail indicators

- Same blocking fact repeated in 4+ sections with no additional context each time
- Empty sections take more than 1 line each
- Dashboard is 150+ lines for a project with 10 tasks and no work done

---

## Trace 08C: Quick Status position and usefulness

- **Path:** dashboard.md → section structure (section 4: Quick Status)

### Current position

Quick Status is section 4 — after Project Context and Needs Your Attention.

### Observation

At project start, the user wants two things immediately:
1. **Where are we?** — overall shape of the project (phases, task counts, what's blocked)
2. **What do I need to do?** — decisions, human tasks

Quick Status answers #1. Needs Your Attention answers #2. Both are high-priority.

The current order (Needs Your Attention before Quick Status) prioritizes #2 over #1. This may work during active execution but at project start, the user may want the overview first.

### Pass criteria

- [ ] Quick Status data (phase breakdown, overall progress) is reachable within 15 lines of the first content section
- [ ] The phase table in Quick Status adds value beyond what's in Project Context (which already shows current phase)

### Fail indicators

- Quick Status is buried after 30+ lines of Needs Your Attention content
- Project Context and Quick Status show nearly identical information
