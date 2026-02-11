# Scenario 12: Dashboard Section Relevance by Phase

Verify that dashboard sections provide value appropriate to the project's current phase. Sections that are noise in one phase may be critical in another. Tests the section toggle system and whether it should have smarter defaults.

## Context

The same 11 dashboard sections are generated at every phase. Some are empty early, some are noise late. The user wants a dashboard that adapts — or at minimum, doesn't waste screen space on null-state sections.

---

## Trace 12A: Fresh project (post-decomposition)

- **State:** Just ran `/work` to decompose. All tasks Pending. No decisions yet. No drift. No verification.

### Section-by-section relevance

| Section | Content at this phase | Value |
|---------|----------------------|-------|
| Project Context | Name, Phase 1, start date | **High** — orients the user |
| Needs Your Attention | Decisions pending (if any), human tasks | **High** — tells user what to do |
| Quick Status | 0% complete, phase table | **Medium** — provides structure overview |
| Spec Alignment | "✅ All sections aligned" | **None** — always true after decomposition |
| Critical Path | Full path from start to finish | **High** — shows the journey ahead |
| Claude Status | All tasks "Ready to Start" | **Medium** — confirms Claude knows what to do |
| Progress This Week | "No recent completions" | **None** — nothing happened yet |
| All Decisions | Empty or initial decisions | **Low** — only if decisions exist |
| All Tasks | Full task list by phase | **High** — the complete work breakdown |
| Notes & Ideas | Empty (user hasn't written yet) | **Low** — placeholder |

### Expected behavior

Sections with **None** value should either:
- Be excluded automatically (smart default), or
- Collapse to a single-line summary, or
- Be configurable via `dashboard_sections` toggle

### Pass criteria

- [ ] `dashboard_sections` config exists in spec frontmatter or CLAUDE.md
- [ ] Sections can be set to `exclude` to remove them entirely
- [ ] At project start, a reasonable default config would exclude Spec Alignment and Progress This Week
- [ ] Excluded sections leave no trace (not even a heading)

### Fail indicators

- No way to exclude sections (all 11 always rendered)
- Excluding a section requires editing a reference file (should be config)
- Empty sections take 3+ lines each (heading, empty content, separator)

---

## Trace 12B: Active execution (mid-Phase 1)

- **State:** 3 of 8 tasks Finished, 1 In Progress, 4 Pending. 1 decision resolved. No drift.

### Section-by-section relevance

| Section | Content at this phase | Value |
|---------|----------------------|-------|
| Project Context | Phase 1, 37% complete | **High** |
| Needs Your Attention | Any human tasks, verification debt | **High** |
| Quick Status | 37% overall, phase breakdown | **High** — shows momentum |
| Spec Alignment | "✅ All sections aligned" (unless spec edited) | **Low** — unless there's drift |
| Critical Path | Remaining steps with owners | **High** — shows what's blocking completion |
| Claude Status | Current task, next up, blocked | **High** — user knows what Claude is doing |
| Progress This Week | 3 completed this week | **Medium** — provides sense of progress |
| All Decisions | 1 resolved, 0 pending | **Low** — nothing actionable |
| All Tasks | Full list with statuses | **High** — detailed reference |
| Notes & Ideas | User notes | **Depends** on user |

### Expected behavior

Most sections are useful during active execution. Spec Alignment is still noise unless the user edited the spec. All Decisions is informational but not actionable.

### Pass criteria

- [ ] Active execution phase has the highest information density
- [ ] Critical Path updates to show remaining work (not the full original path)
- [ ] Claude Status clearly shows what Claude is currently doing

### Fail indicators

- Spec Alignment takes up screen space to report no issues
- All Decisions section is large but contains only resolved items with no pending actions

---

## Trace 12C: Pre-verification (all tasks done)

- **State:** All 8 tasks Finished. Verification not yet run. Potential drift exists.

### Section-by-section relevance

| Section | Content at this phase | Value |
|---------|----------------------|-------|
| Project Context | Phase 1, 100% tasks done | **High** |
| Needs Your Attention | Phase transition approval, any verification debt | **Critical** — user decides what happens next |
| Quick Status | 100% tasks, pending verification | **Medium** — confirms all done |
| Spec Alignment | Critical if spec was edited during implementation | **High** — drift must be resolved before verification |
| Critical Path | "Run verification" | **Low** — simple next step |
| Claude Status | "Ready: Phase-level verification" | **Medium** |
| Progress This Week | All completions | **Low** — looking backward at this point |
| All Decisions | All resolved | **Low** — historical record |
| All Tasks | All Finished | **Medium** — reference for verification |
| Notes & Ideas | User notes | **Depends** |

### Key observation

Spec Alignment becomes **critical** at this phase — it was noise before. This is the opposite pattern from project start.

### Pass criteria

- [ ] Spec Alignment section becomes prominent when drift exists at verification time
- [ ] Needs Your Attention clearly shows the phase transition checkpoint
- [ ] Dashboard communicates "tasks done, verification needed" as the primary message
- [ ] Critical Path simplifies to show verification as the main remaining step

### Fail indicators

- Spec Alignment still shows "all aligned" even though spec was edited (drift detection failure)
- Phase transition approval is buried below less important sections
- Dashboard looks the same as mid-execution despite being a fundamentally different moment

---

## Trace 12D: Section toggle awareness

- **Path:** work.md § Dashboard Regeneration Procedure → Section Toggle Configuration

### Current toggle system

Users configure in spec frontmatter or CLAUDE.md:
```yaml
dashboard_sections:
  spec_alignment: exclude    # Not useful for small projects
  progress: exclude          # User doesn't care about weekly stats
```

### What's missing

There's no concept of **phase-aware defaults**. The toggle is static — set once, applies always.

A more adaptive approach might be:
```yaml
dashboard_sections:
  spec_alignment:
    default: exclude
    on_drift: build          # Activate when drift detected
  progress:
    default: exclude
    on_phase_complete: build # Activate at phase boundaries
```

### Pass criteria

- [ ] Current toggle system works as documented (build/maintain/exclude/preserve)
- [ ] Toggling a section to `exclude` removes it entirely from rendered dashboard
- [ ] User can configure toggles in spec frontmatter or CLAUDE.md (not reference files)
- [ ] Toggle is per-project (in spec frontmatter or CLAUDE.md)

### Fail indicators

- Toggle config is ignored during regeneration
- `exclude` still renders the section heading with "(excluded)" note
- Toggle requires editing a reference file instead of project config
