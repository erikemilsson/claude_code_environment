# Dashboard Regeneration Procedure

Every dashboard regeneration MUST follow this procedure. All commands and agents reference this file for consistency.

---

## Section Toggle Configuration

The primary source for section toggles is the **dashboard.md section toggle checklist** — a visible, editable checklist near the top of the dashboard between `<!-- SECTION TOGGLES -->` and `<!-- END SECTION TOGGLES -->` markers.

**Reading logic:**
1. Parse the checklist between the markers
2. `- [x] Section Name` → `build` mode (actively generate)
3. `- [ ] Section Name` → `exclude` mode (skip during regeneration)
4. Notes section: always `preserve` regardless of checkbox state (enforced)
5. Fallback: if no checklist exists, check spec frontmatter `dashboard_sections` or `.claude/CLAUDE.md`

### First Regeneration (Replacing Template Example)

Detection: the dashboard is still the template example if it contains the line `> **This is a format example**`. On first regeneration, compute toggle defaults from project state instead of using static defaults:

```
Action Required  → [x] always (core section)
Progress         → [x] always (core section)
Tasks            → [x] always (core section)
Decisions        → [x] if any decision-*.md files exist, [ ] otherwise
Notes            → [x] always (preserve mode)
Timeline         → [x] if any task has due_date or external_dependency.expected_date, [ ] otherwise
Custom Views     → [ ] always (user opts in when they want custom views)
```

### On Phase Transitions

When `/work` detects a phase transition (all Phase N tasks "Finished", Phase N+1 becoming active), check whether toggle suggestions are warranted:
- If Phase N+1 introduces decision dependencies and Decisions is unchecked → suggest: "Phase {N+1} has pending decisions. Consider enabling the Decisions section in the dashboard."
- If Phase N+1 tasks have due dates and Timeline is unchecked → suggest: "Phase {N+1} has deadlines. Consider enabling the Timeline section."
- Suggestions are logged, never auto-toggled. The user's checkbox state is always authoritative.

### During Regeneration (All Subsequent)

- Preserve the toggle checklist between its markers (never overwrite user's checkbox state)
- Only generate sections that are checked (`[x]`)
- The Notes section is always preserved regardless of toggle state

| Mode | Behavior |
|------|----------|
| `build` | Actively generate from source data on every regeneration (default, `[x]`) |
| `maintain` | Keep existing content, only update if data changes significantly (via spec frontmatter override only) |
| `exclude` | Skip this section entirely during regeneration (`[ ]`) |
| `preserve` | Never modify (Notes always uses this) |

The checkbox UI maps to `build`/`exclude`. Users who need `maintain` mode can set it via spec frontmatter `dashboard_sections` override, which takes precedence over the checklist for that section.

---

## Regeneration Steps

### 1. Read Source Data

- All `task-*.json` files (tasks)
- All `decision-*.md` files in `.claude/support/decisions/` (decisions)
- `drift-deferrals.json` (if exists)
- `verification-result.json` (if exists)
- `.claude/support/questions/questions.md` (scan for blocking questions)

### 2. Backup User Section

- Extract content between `<!-- USER SECTION -->` and `<!-- END USER SECTION -->`
- Save to `.claude/support/workspace/dashboard-notes-backup.md`
- Rotate old backups (keep last 3)

### 2b. Backup Custom Views Instructions

- Extract content between `<!-- CUSTOM VIEWS INSTRUCTIONS -->` and `<!-- END CUSTOM VIEWS INSTRUCTIONS -->` markers
- Save to `.claude/support/workspace/dashboard-custom-views-backup.md`
- Rotate old backups (keep last 3)

### 2c. Backup Inline Feedback

- Scan dashboard for `<!-- FEEDBACK:{id} -->` / `<!-- END FEEDBACK:{id} -->` marker pairs
- For each pair, extract the content between the markers, keyed by task ID
- Store in memory alongside the user section backup (used in Step 5c)

### 2d. Backup Phase Gate Markers

- Scan dashboard for active gate pairs (`<!-- PHASE GATE:{X}→{Y} -->` / `<!-- END PHASE GATE:{X}→{Y} -->`) and approved markers (`<!-- PHASE GATE:{X}→{Y} APPROVED -->`)
- For active gates, extract the content between the markers (preserves user's checkbox state)
- For approved markers, note the transition they represent
- Store in memory alongside other backups (used in Step 5d)

### 3. Generate Dashboard

- Follow the Section Format Reference below for all formatting rules
- Use exact section headings: `# Dashboard`, `## 🚨 Action Required`, `## 📊 Progress`, `## 📋 Tasks`, `## 📋 Decisions`, `## 💡 Notes`
- Optional section heading (when enabled, placed between Decisions and Notes): `## 👁️ Custom Views`
- **Timeline sub-section** in Progress: render when any task has `due_date` or `external_dependency.expected_date`
- **Project Overview sub-section** in Progress: render inline Mermaid diagram when 4+ tasks remain (see § "Project Overview Diagram")
- Read section toggles from dashboard checklist (between `<!-- SECTION TOGGLES -->` markers) and respect modes
- Preserve the section toggle checklist between its markers during regeneration
- Enforce atomicity: only tasks with JSON files, only decisions with MD files
- On first regeneration (detected by `> **This is a format example**` line): replace the template example with actual project data and compute toggle defaults per the "First Regeneration" section above
- **Inline feedback areas:** When generating "Your Tasks", add feedback markers for each `human`/`both`-owned task:
  ```
  <!-- FEEDBACK:{id} -->
  **Task {id} — Feedback:**
  [Leave feedback here, then run /work complete {id}]
  <!-- END FEEDBACK:{id} -->
  ```
- **Phase Transitions sub-section:** When all tasks in Phase N are "Finished" AND Phase N+1 tasks exist AND no `<!-- PHASE GATE:{N}→{N+1} APPROVED -->` marker exists in the dashboard, render a phase gate with checkbox between markers:
  ```
  <!-- PHASE GATE:{N}→{N+1} -->
  - [ ] **Phase {N} complete** — Review results and approve transition to Phase {N+1}
    - {M} tasks finished, {K} tasks in Phase {N+1} ready
  <!-- END PHASE GATE:{N}→{N+1} -->
  ```
- **Verification Pending sub-section:** When all spec tasks are "Finished" with passing per-task verification AND no valid `verification-result.json` exists, render:
  ```
  All tasks complete — phase-level verification will run on next `/work`
  ```
- **Spec Drift sub-section:** When `drift-deferrals.json` exists with active deferrals, render each deferred section:
  ```
  - ⚠️ **{section}** — {N} tasks affected, deferred {M} days ago
  ```

### 4. Compute and Add Metadata Block

Add after `# Dashboard` title:
```markdown
<!-- DASHBOARD META
generated: [ISO timestamp]
task_hash: sha256:[hash of sorted task_id:status pairs]
task_count: [number]
verification_debt: [count of tasks needing verification]
drift_deferrals: [count from drift-deferrals.json]
-->
```

### 5. Restore User Section

- Insert backed-up content between markers
- If markers missing, append with warning comment

### 5b. Restore Custom Views Instructions

- Insert backed-up custom views instructions between `<!-- CUSTOM VIEWS INSTRUCTIONS -->` and `<!-- END CUSTOM VIEWS INSTRUCTIONS -->` markers
- If markers missing, skip (section may be excluded via toggle)
- Read the restored instructions and generate appropriate rendered content below `<!-- END CUSTOM VIEWS INSTRUCTIONS -->` up to the next `---` separator

### 5c. Restore Inline Feedback

- For each feedback entry backed up in Step 2c:
  - If the task still appears in "Your Tasks" (task still active with `human`/`both` owner): restore the backed-up content between its `<!-- FEEDBACK:{id} -->` markers
  - If the task is no longer in "Your Tasks" (completed or removed): write the feedback content to the task JSON `user_feedback` field (preserves feedback that would otherwise be lost)

### 5d. Restore Phase Gate Markers

- For each active gate backed up in Step 2d:
  - If the phase gate condition still applies (all Phase X tasks Finished, Phase Y tasks exist, no APPROVED marker for this transition): restore the backed-up content between its `<!-- PHASE GATE:{X}→{Y} -->` markers (preserves user's checkbox state)
  - If the phase gate no longer applies (transition was approved or phases changed): discard
- For each APPROVED marker backed up in Step 2d:
  - Always restore the `<!-- PHASE GATE:{X}→{Y} APPROVED -->` marker (permanent record of approved transitions)

### 6. Add Footer Line

At very end:
```
---
*[timestamp] · N tasks · [status indicator]*
```
- Healthy: `[Spec aligned](# "0 drift deferrals, 0 verification debt")`
- Issues: `⚠️ N drift deferrals, M verification debt`

---

## Section Format Reference

All dashboard formatting rules are documented here. This is the single authoritative source — do not add format comments to the regenerated dashboard.

### Action Item Contract

Every item in "Action Required" must be:
1. Actionable — the user can see what to do without guessing
2. Linked — if the action involves a file, include a relative path link
3. Completable — include a checkbox, command, or clear completion signal
4. Contextual — if feedback is needed, provide a feedback area or link

### Review Item Derivation

Review items are derived, not stored. During regeneration:
1. Scan for unresolved items — out_of_spec without approval, draft/proposed decisions, blocking questions from `questions.md`
2. Populate Reviews sub-section from current data
3. Never carry forward stale entries — resolved items disappear on next regeneration
4. No dangling references — every item must link to a concrete file
5. Blocking questions: scan `questions.md` for `[BLOCKING]` entries, render each as a review item linking to [questions.md](support/questions/questions.md)
6. Non-blocking unanswered questions: if count > 0, add summary line to Reviews: `- [ ] **N pending questions** → [questions.md](support/questions/questions.md)`

### Section Display Rules

- Action Required sub-sections: only render when they have content (omit empty categories entirely)
- Action Required sub-section order: Phase Transitions, Verification Pending, Verification Debt, Spec Drift, Decisions, Your Tasks, Reviews
- Phase Transitions: only render when a phase boundary has been reached (all Phase N tasks Finished, Phase N+1 exists) AND no APPROVED marker exists for that transition
- Verification Pending: only render when all spec tasks are Finished with passing per-task verification but no valid verification-result.json
- Spec Drift: only render when drift-deferrals.json has active entries
- Reviews sub-section format: `- [ ] **Item title** — what to do → [link to file](path)`
- Reviews appear for: out_of_spec tasks without approval, draft/proposed decisions, blocking questions from `questions.md` (each linked to the file)
- Timeline sub-section in Progress: only render when tasks have `due_date` or `external_dependency.expected_date`
- Timeline has its own toggle in the section checklist (independent of Progress)
- Phase table in Progress: always show ALL phases (including blocked/future)
- Critical path owners: ❗ (human), 🤖 (Claude), 👥 (both)
- Critical path parallel branches: `[step A | step B]` notation for fork/join points; max 3 branches per group
- Critical path >5 steps (after collapsing parallel branches): show first 3 + "... N more → Done"
- "This week" line: omit when all counts are zero
- Tasks grouped by phase with per-phase progress lines
- Tasks with `conflict_note`: show status as `Pending (held: conflict with Task {id})` during parallel dispatch
- Decisions: status display mapping: `approved`/`implemented` → "Decided", `draft`/`proposed` → "Pending". Decided → show selected option name; Pending → link to doc in Selected column
- Out-of-spec tasks: prefix title with ⚠️
- On Hold tasks: show status as `⏸️ On Hold` in Tasks section; exclude from Progress phase "Done" counts but include in "Total"; exclude from critical path (paused work isn't on the path)
- Absorbed tasks: show status as `Absorbed → Task {id}` in Tasks section (dimmed/collapsed style); exclude from both "Done" and "Total" in Progress phase counts; exclude from critical path
- Footer: healthy = spec aligned tooltip; issues = ⚠️ with counts
- Custom Views section: user-defined instructions (preserved between markers) followed by Claude-generated content based on those instructions (when enabled). Multiple views are rendered as `###` sub-sections, one per bold-labeled instruction.

### Per-Section Format

| Section | Columns / Format |
|---------|-----------------|
| Action Required → Phase Transitions | `- [ ] **Phase N complete** — description` with `<!-- PHASE GATE -->` markers |
| Action Required → Verification Pending | Plain text status message |
| Action Required → Verification Debt | `Task \| Title \| Issue` |
| Action Required → Spec Drift | `- ⚠️ **{section}** — {N} tasks affected, deferred {M} days ago` |
| Action Required → Decisions | `Decision \| Question \| Doc` |
| Action Required → Your Tasks | `Task \| What To Do \| Where` |
| Action Required → Reviews | `- [ ] **Item title** — what to do → [link](path)` — derived, not stored |
| Progress → Phase table | `Phase \| Done \| Total \| Status` — status: Complete, Active, Blocked (reason) |
| Progress → Timeline | `Date \| Item \| Status \| Notes` — sorted chronologically, overdue: strikethrough date + ⚠️ OVERDUE prefix, external deps with contact info, human tasks marked with ❗ |
| Tasks → Per phase | `ID \| Title \| Status \| Diff \| Owner \| Deps` — grouped by phase headers |
| Decisions | `ID \| Decision \| Status \| Selected` |
| Progress → Project Overview | Inline Mermaid `graph LR` diagram — see Project Overview Diagram rules below |
| Custom Views | Preserved instruction block between `<!-- CUSTOM VIEWS INSTRUCTIONS -->` markers + rendered `###` sub-sections generated from those instructions (one per bold-labeled view) |

### Domain Agnosticism

This format works for any project type — software, research, procurement, renovation, event planning. Use language appropriate to the project domain. No code-specific assumptions are built in.

---

## Critical Path Generation

The critical path is rendered as a single line in the **Progress** section: owner-tagged steps joined by `→`, with parallel branches shown in `[ | ]` notation.

1. **Build dependency graph** — include all incomplete tasks and their dependencies (both task deps and decision deps). Unresolved decisions appear as nodes (e.g., `❗ Resolve DEC-001`)
2. **Compute longest path** — walk the graph to find the longest chain from any current entry point to "Done". This is the critical path (determines project duration)
3. **Detect parallel branches** — find fork/join points along the critical path:
   - A **fork** is a node whose completion enables 2+ independent successors
   - A **join** is a node with 2+ predecessors that must all complete before it starts
   - Show parallel branches when they share the same fork and join nodes (the branches reconverge)
   - Branches that don't reconverge are separate sequential paths — pick the longest
4. **Format as one-liner:**
   - Sequential: `❗ Resolve DEC-001 → 🤖 Build API → Done`
   - Parallel branches: `[🤖 Rough plumbing | ❗ Resolve DEC-002] → [❗ Inspection | 🤖 Install] → 👥 Walkthrough → Done`
   - Owners: `❗` (human), `🤖` (Claude), `👥` (both)
   - **Step count** = total unique nodes in the rendered path (each branch member counts as 1): `*(N steps)*`
   - For complex paths (>5 steps after collapsing parallel branches), show first 3 + "... N more → Done"
5. **Prioritize human-owned steps** — surfaces blockers the user can act on

**Decision dependencies as path nodes:** Unresolved decisions appear on the critical path as `❗ Resolve {DEC-ID}` steps. Once resolved, they are removed and their successor tasks become direct successors of the decision's predecessors.

**Parallel branch rules:**
- Max 3 branches in a single `[ | ]` group (more than 3 → collapse to `[🤖 3 parallel tasks]`)
- Nested parallelism: don't nest `[ ]` — flatten to separate `[ | ]` groups joined by `→`
- If parallel branches have different owners, show each: `[❗ Review | 🤖 Build]`
- Branches of unequal length: show each by its first step (the branch content is what matters, not padding)

**Edge cases:** No dependencies → "All tasks can start now". No incomplete AND no valid verification-result.json → "🤖 Phase verification → Done" *(1 step)*. No incomplete AND valid passing verification-result.json → "All tasks complete! ✓". Single task → just that task → Done. No parallelism detected → pure sequential format (no brackets).

---

## Project Overview Diagram

An inline Mermaid diagram in the Progress section showing the project's dependency structure at a glance. Placed after the critical path one-liner, before the "This week" activity line, under a `### Project Overview` sub-heading.

**Generation rules:**

1. **Completed phases** → Collapse into a single node: `["✅ Phase Name (N/N)"]`
2. **Completed tasks in active phases** → Fold away. Reroute their connections: connect their predecessors directly to their incomplete successors. This keeps the diagram focused on remaining work.
3. **Active/pending tasks** → Show individually with ownership prefix: `🤖` (claude), `❗` (human), `👥` (both)
4. **Decisions** → Diamond nodes: `{"❓ Decision title"}`
5. **Dependencies** → Arrows between nodes following task dependency data
6. **Date constraints** → Annotate nodes with deadlines when present: `["🤖 Task title<br/><small>Due: 2026-02-15</small>"]`
7. **Clumping** → When >15 active nodes would result, group related tasks into subgraph clusters by phase or functional area to reduce visual noise
8. **Direction** → Always `graph LR` (left to right)
9. **Labels** → Keep short: ownership emoji + task title. No status text in labels.
10. **Gates** → Phase gates as hexagon nodes: `{{❗ Phase N Review}}` — visually distinct from tasks (rectangles) and decisions (diamonds)
11. **Styling** → Include `classDef` declarations and apply to each node. Priority: `done` first, then `human` (ownership overrides status), then `active`, then `blocked` as default for remaining nodes:
    - `classDef done fill:#c8e6c9,stroke:#2e7d32` — completed phases/tasks
    - `classDef active fill:#bbdefb,stroke:#1565c0` — in-progress tasks (claude/both-owned)
    - `classDef human fill:#fff9c4,stroke:#f57f17` — human-owned tasks and phase gates
    - `classDef blocked fill:#f5f5f5,stroke:#9e9e9e` — pending/blocked tasks (claude/both-owned)

**Edge cases:** No tasks → omit diagram. All tasks complete → omit diagram (project done). Single task → omit diagram (one-liner is sufficient). Fewer than 4 remaining tasks → omit diagram (one-liner covers it).
