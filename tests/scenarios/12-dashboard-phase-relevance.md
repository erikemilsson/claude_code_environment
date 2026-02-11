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

The consolidated structure handles null-state naturally: Action Required omits empty sub-sections, and the header provides orientation without a separate "Project Context" section. Remaining sections can be configured via `dashboard_sections` toggle.

### Pass criteria

- [ ] `dashboard_sections` config exists in spec frontmatter or CLAUDE.md
- [ ] Sections can be set to `exclude` to remove them entirely
- [ ] At project start, Action Required sub-sections are omitted when empty (no "✅ None" placeholders)
- [ ] Excluded sections leave no trace (not even a heading)

### Fail indicators

- No way to exclude sections
- Excluding a section requires editing a reference file (should be config)
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

- **Path:** work.md § Dashboard Regeneration Procedure → Section Toggle Configuration

### Current toggle system

Users configure in spec frontmatter or CLAUDE.md:
```yaml
dashboard_sections:
  action_required: build
  progress: exclude          # User doesn't care about phase table
  tasks: build
  decisions: exclude         # Small project, few decisions
  notes: preserve
```

### What's handled vs what's missing

The consolidated structure already handles the primary null-state problem: Action Required omits empty sub-sections (Verification Debt, Decisions, Your Tasks, Reviews, Spec Drift only appear when populated). This eliminates the noise that previously required toggles.

The remaining toggle use case is for **entire sections** that a project doesn't need (e.g., Decisions for a project with no decision records, Progress for a simple project).

### Pass criteria

- [ ] Current toggle system works as documented (build/maintain/exclude/preserve)
- [ ] Toggling a section to `exclude` removes it entirely from rendered dashboard
- [ ] User can configure toggles in spec frontmatter or CLAUDE.md (not reference files)
- [ ] Toggle is per-project (in spec frontmatter or CLAUDE.md)

### Fail indicators

- Toggle config is ignored during regeneration
- `exclude` still renders the section heading with "(excluded)" note
- Toggle requires editing a reference file instead of project config
