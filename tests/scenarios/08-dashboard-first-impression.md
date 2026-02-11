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
1. `# Dashboard` + metadata block + header lines (project name, stage, completion %)
2. `## 🚨 Action Required` — decisions, human tasks, reviews (only populated sub-sections shown)
3. `## 📊 Progress` — phase table, critical path one-liner, this week activity

### Expected (current spec)

- Header lines: project name, Setup stage, start date, 0% complete, task/decision counts
- Action Required:
  - Decisions: DEC-001 with link to decision doc
  - Your Tasks: Task 5 "Configure API keys" with link to `.env.example`
  - (Verification Debt, Reviews sub-sections omitted — nothing to show)

### Observation: null-state noise handled by omission

Empty sub-sections within Action Required are omitted entirely (no "✅ None" placeholders). At project start this means only Decisions and Your Tasks appear — no Verification Debt, Reviews, or Spec Drift noise.

### Pass criteria

- [ ] Action Required is visible without scrolling past boilerplate
- [ ] DEC-001 appears with a link to the decision doc file
- [ ] Human task "Configure API keys" appears with a link and action description
- [ ] Progress phase table shows all 3 phases with blocking reasons for Phase 2 and 3
- [ ] Critical path one-liner shows user actions before Claude actions

### Fail indicators

- User must scroll past empty sections to reach actionable content
- DEC-001 appears in the table but without a clickable link to the file
- "Configure API keys" appears but user doesn't know what to do or where to go
- Empty sub-sections rendered with placeholder text instead of being omitted

---

## Trace 08B: Section redundancy audit

- **Path:** work.md § Section Format Reference → section definitions

### Redundancy between sections at project start

| Information | Where it appears | Redundant? |
|-------------|------------------|------------|
| DEC-001 blocks Phase 2 | Action Required → Decisions, Tasks Phase 2 summary | 2 places (within budget) |
| Phase 2 is blocked | Progress phase table, Tasks phase summary | 2 places (within budget) |
| Human task exists | Action Required → Your Tasks, Tasks | 2 places (within budget) |
| No work started | Header (0%), Progress phase table | 2 places (within budget) |

### Expected

Each fact appears in at most 2 places (primary actionable location + reference detail). The consolidated structure eliminates the previous 4-5 place redundancy.

### Pass criteria

- [ ] A piece of blocking information appears in at most 2 sections (primary + detail)
- [ ] Sections that are empty/null at project start are either excluded or collapsed to 1 line
- [ ] The dashboard for a fresh project fits in a reasonable scroll (< 80 lines of rendered content)

### Fail indicators

- Same blocking fact repeated in 4+ sections with no additional context each time
- Empty sections take more than 1 line each
- Dashboard is 150+ lines for a project with 10 tasks and no work done

---

## Trace 08C: Information hierarchy and density

- **Path:** dashboard.md → section structure (header lines → Action Required → Progress)

### Current position

Header lines provide instant orientation (project name, stage, completion %). Action Required follows immediately with only populated sub-sections. Progress comes next.

### Observation

At project start, the user wants two things immediately:
1. **Where are we?** — overall shape of the project (phases, task counts, what's blocked)
2. **What do I need to do?** — decisions, human tasks

The header lines answer #1 (completion %, task counts). Action Required answers #2 (decisions, human tasks). Both appear in the first ~15 lines because header is compact (2 lines) and Action Required omits empty sub-sections.

### Pass criteria

- [ ] Progress data (phase breakdown) is reachable within 20 lines of the dashboard heading
- [ ] Header lines provide enough orientation that a separate "Project Context" section isn't needed
- [ ] Action Required sub-sections omit empty categories (no null-state noise)

### Fail indicators

- Action Required is 30+ lines of mostly-empty sub-sections pushing Progress out of view
- Header lines and Progress section show nearly identical information
