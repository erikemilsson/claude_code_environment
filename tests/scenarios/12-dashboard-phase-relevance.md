# Scenario 12: Dashboard Section Relevance by Phase

Verify that dashboard sections provide value appropriate to the project's current phase. Sections that are noise in one phase may be critical in another. Tests the section toggle system and whether it should have smarter defaults.

## Context

The same dashboard sections are generated at every phase. Some sub-sections are empty early, some are noise late. The user wants a dashboard that adapts — or at minimum, doesn't waste screen space on null-state content.

---

## Trace 12A: Fresh project (post-decomposition)

- **State:** Just ran `/work` to decompose. All tasks Pending. No decisions yet. No drift. No verification.

### Section-by-section relevance

| Section | Content at this phase | Value |
|---------|----------------------|-------|
| Header lines | Name, Setup stage, 0% complete | **High** — orients the user |
| Action Required | Decisions pending (if any), human tasks (empty subs omitted) | **High** — tells user what to do |
| Progress | Phase table, critical path one-liner | **Medium** — provides structure overview |
| Tasks | Full task list by phase | **High** — the complete work breakdown |
| Decisions | Empty or initial decisions | **Low** — only if decisions exist |
| Notes | Empty (user hasn't written yet) | **Low** — placeholder |

### Expected behavior

The consolidated structure handles null-state naturally: Action Required omits empty sub-sections, and the header provides orientation without a separate "Project Context" section. Remaining sections can be configured via the **Sections** checklist at the top of dashboard.md (or `dashboard_sections` in spec frontmatter as fallback).

### Pass criteria

- [ ] Sections checklist exists at the top of dashboard.md (between `<!-- SECTION TOGGLES -->` markers)
- [ ] Unchecking a section (`[ ]`) excludes it from regeneration
- [ ] At project start, Action Required sub-sections are omitted when empty (no "✅ None" placeholders)
- [ ] Excluded sections leave no trace (not even a heading)

### Fail indicators

- No way to exclude sections
- Excluding a section requires editing spec frontmatter or reference files (should be a checkbox in dashboard.md)
- Empty Action Required sub-sections rendered with placeholder text

---

## Trace 12B: Active execution (mid-Phase 1)

- **State:** 3 of 8 tasks Finished, 1 In Progress, 4 Pending. 1 decision resolved. No drift.

### Section-by-section relevance

| Section | Content at this phase | Value |
|---------|----------------------|-------|
| Header lines | Phase 1, 37% complete | **High** — instant orientation |
| Action Required | Any human tasks, verification debt (Spec Drift omitted if no drift) | **High** |
| Progress | Phase table, critical path one-liner, this week completions | **High** — shows momentum |
| Tasks | Full list with statuses | **High** — detailed reference |
| Decisions | 1 resolved, 0 pending | **Low** — nothing actionable |
| Notes | User notes | **Depends** on user |

### Expected behavior

Most sections are useful during active execution. Action Required omits Spec Drift sub-section when there's no drift. Decisions is informational but not actionable.

### Pass criteria

- [ ] Active execution phase has the highest information density
- [ ] Critical path one-liner updates to show remaining work
- [ ] Tasks section clearly shows task statuses including what's In Progress

### Fail indicators

- Spec Drift sub-section takes up screen space to report no issues (should be omitted)
- Decisions section is large but contains only resolved items with no pending actions

---

## Trace 12C: Pre-verification (all tasks done)

- **State:** All 8 tasks Finished. Verification not yet run. Potential drift exists.

### Section-by-section relevance

| Section | Content at this phase | Value |
|---------|----------------------|-------|
| Header lines | Phase 1, 100% tasks done | **High** |
| Action Required | Phase transition approval, verification debt, Spec Drift (if any) | **Critical** — user decides what happens next |
| Progress | 100%, critical path one-liner, completions | **Medium** — confirms all done |
| Tasks | All Finished | **Medium** — reference for verification |
| Decisions | All resolved | **Low** — historical record |
| Notes | User notes | **Depends** |

### Key observation

Spec Drift sub-section within Action Required becomes **critical** at this phase — it was omitted (no drift) before. This is the opposite pattern from project start: previously omitted because irrelevant, now populated because essential.

### Pass criteria

- [ ] Spec Drift sub-section appears within Action Required when drift exists at verification time
- [ ] Action Required clearly shows the phase transition checkpoint
- [ ] Dashboard communicates "tasks done, verification needed" as the primary message
- [ ] Critical path one-liner simplifies to show verification as the main remaining step

### Fail indicators

- Spec Drift sub-section doesn't appear even though spec was edited (drift detection failure)
- Phase transition approval is buried below less important sections
- Dashboard looks the same as mid-execution despite being a fundamentally different moment

---

## Trace 12D: Section toggle awareness

- **Path:** dashboard.md → Sections checklist; work.md § Dashboard Regeneration Procedure → Section Toggle Configuration

### Current toggle system

Users check/uncheck items in the **Sections** checklist at the top of dashboard.md:
```markdown
<!-- SECTION TOGGLES -->
**Sections:**
- [x] Action Required
- [x] Progress
- [x] Tasks
- [ ] Decisions          # Small project, few decisions
- [x] Notes
- [x] Timeline
- [ ] Sub-Dashboards
<!-- END SECTION TOGGLES -->
```

Checked (`[x]`) → `build` mode. Unchecked (`[ ]`) → `exclude` mode. Notes always `preserve` regardless. Spec frontmatter `dashboard_sections` can override with `maintain` mode if needed.

### What's handled

The consolidated structure handles the primary null-state problem: Action Required omits empty sub-sections. Toggles control entire sections.

**Phase-aware initialization:** On first dashboard generation (replacing the template example), toggle defaults are computed from project state — Decisions is checked only if decision records exist, Timeline only if tasks have dates, Sub-Dashboards only if sub-dashboard files are referenced in spec.

**Phase transition suggestions:** When a phase transition occurs, `/work` checks whether newly relevant sections are unchecked and logs suggestions (e.g., "Phase 2 has pending decisions. Consider enabling the Decisions section."). Suggestions are never auto-applied — the user's checkbox state is authoritative.

### Pass criteria

- [ ] Sections checklist exists at the top of dashboard.md between `<!-- SECTION TOGGLES -->` markers
- [ ] Unchecking a section removes it entirely from regenerated dashboard
- [ ] Checking a section causes it to be generated from source data
- [ ] Toggle is directly in dashboard.md (user doesn't need to find a config file)
- [ ] Regeneration preserves the checklist between its markers (never overwrites user's checkbox state)
- [ ] First regeneration computes defaults from project state (not static)
- [ ] Phase transitions suggest toggle adjustments when new sections become relevant
- [ ] Suggestions are logged, never auto-applied

### Fail indicators

- Toggle config is ignored during regeneration
- `exclude` still renders the section heading with "(excluded)" note
- Regeneration overwrites the user's checklist state
- Toggle requires editing spec frontmatter or CLAUDE.md instead of the dashboard itself
- First regeneration uses static defaults regardless of project content
- Phase transition silently enables/disables sections without user consent
