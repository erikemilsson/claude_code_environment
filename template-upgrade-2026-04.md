# Template Upgrade — April 2026

**Purpose:** Coordinate multi-session template improvements from three inputs (Opus 4.7 upgrade, Claude Code best-practices doc, usage insights report) alongside the existing feedback backlog and approved decisions.

**Status:** Phase 0 — Hygiene
**Last updated:** 2026-04-16

---

## How to use this file

- **At session start:** read the **Session Log** (bottom) for last-session context, then **Current State** for where to resume.
- **At session end:** append a Session Log entry with what was done + what's next, and update **Current State**.
- **This file is `DELETE-AFTER`** — listed in the Cleanup Manifest; removed in Phase 5.
- **Implementation grouping rule:** when editing within a phase, group by file (see **File Collision Map**) to avoid re-reading. Commits still follow the per-decision unit — see Control and Commits below.

## Control and Commits

User retains approval authority at every intake and edit point. Claude does not unilaterally add items or batch changes.

**Intake control (Phase 2):**
- External sources (best-practices doc, usage report) are read by Claude into a **candidate list** at root (tagged `DELETE-AFTER`).
- User reviews each candidate and marks `[approve]` / `[edit]` / `[reject]`. Rejected items get a 1-line reason so they don't resurface.
- Only approved (and possibly edited) candidates enter the `/feedback` pipeline. No silent captures.

**Edit control (Phases 0, 1, 4):**
- Before each editing unit, Claude summarizes: files about to change + scope + expected diff shape. User confirms before edits begin.
- After edits, Claude presents the diff summary and awaits confirmation before moving to the next unit.

**Commit cadence:**
- One commit per logical unit. Never batch unrelated changes.
- Logical units: root cleanup, Opus 4.7 sweep, each decision (DEC-004, DEC-005, DEC-006), each feedback implementation (FB-011, FB-015, FB-017), each new-input bundle, final cleanup.
- Commit messages follow existing style (see `git log`). User approves commit messages.
- Suggested checkpoint: commit at end of each phase at minimum; more frequently within phases where scope is large.

---

## Current State

- **Active phase:** Phase 0 — Hygiene
- **Next action:** Root file cleanup + Opus 4.7 reference sweep
- **Blocked on:** nothing

---

## Phases

### Phase 0 — Hygiene

- [ ] **Root file cleanup** — delete: `coworkfolderspec.md`, `insights-report.html`, `migration-guide.md`, `migration-plan-v2-flat-layout.md`, `.DS_Store`
- [ ] **Add `.DS_Store` to `.gitignore`** (verify not already present)
- [ ] **Keep at root:** `dashboard_example_SIREN.pdf`, `dashboard_export_SIREN_new.pdf` (references for FB-014/FB-015)
- [ ] **Opus 4.7 reference sweep** — grep for `claude-opus-4-6` and `Opus 4.6`; update in:
  - `.claude/CLAUDE.md` § Model Requirement
  - `.claude/rules/agents.md` § Model Requirement
  - `.claude/agents/implement-agent.md` frontmatter
  - `.claude/agents/verify-agent.md` frontmatter
  - `.claude/agents/research-agent.md` frontmatter
  - Any other occurrences
- [ ] **Version bump** — `.claude/version.json` (decide scope at Phase 5 based on what landed)
- [ ] **Verify pre-commit hook installed** per root `CLAUDE.md`

### Phase 1 — Implement approved decisions

Decisions already researched and approved (commit `55c1040`). Read each decision record first to confirm the selected option's scope matches the feedback `**Assessed:**` line (scope may have narrowed during research).

- [ ] **DEC-004** — Subagent capability contract → `decisions/decision-004-subagent-capability-contract.md`. Closes FB-010.
- [ ] **DEC-005** — Base allowedTools shipping policy → `decisions/decision-005-base-allowedtools-shipping-policy.md`. Closes FB-012.
- [ ] **DEC-006** — Phase gate flexibility → `decisions/decision-006-phase-gate-flexibility.md`. Closes FB-013.

**Implementation order:** hottest file first — `commands/work.md` takes touchpoints from all three decisions + FB-017. Apply in a single editing pass to avoid re-reading.

### Phase 2 — New input intake

Intake control is explicit: Claude produces a candidate list first, user approves per-item, only approved items enter `/feedback`.

**Best-practices doc (https://code.claude.com/docs/en/best-practices):**
- [ ] Claude reads the doc and produces `upgrade-candidates-best-practices.md` (root, `DELETE-AFTER`). Each candidate: title, 1-line description, tentative impact scope, relevance rationale. No `/feedback` invocations yet.
- [ ] User reviews candidate list and marks each `[approve]` / `[edit]` / `[reject]` with 1-line reason on rejects
- [ ] Claude captures approved items via `/feedback` (one per candidate), using any user edits

**Usage insights report (`file:///Users/erikemilsson/.claude/usage-data/report.html`):**
- [ ] Claude reads the report and produces `upgrade-candidates-usage-report.md` (root, `DELETE-AFTER`) in the same format
- [ ] User reviews and approves/rejects
- [ ] Claude captures approved items via `/feedback`

**Triage:**
- [ ] `/feedback review` — triage captured items
  - Check overlap with existing ready items (FB-011 scripts, FB-015 action-required, FB-017 checkboxes especially) — absorb duplicates
  - Update **File Collision Map** with new `**Assessed:**` entries
- [ ] Decide which new items need `/research` (Phase 3) vs direct implementation (Phase 4)

### Phase 3 — Cross-cutting research

Only for new items that emerge as cross-file or inflection-point decisions.

- [ ] (TBD — populate after Phase 2 triage)

### Phase 4 — Implementation of remaining items

Existing ready items + new items from Phases 2–3.

- [ ] **FB-011** — Scripts as alternative (dashboard regen, checkbox detection). Depends on DEC-004 (subagent Bash sandbox).
- [ ] **FB-015** — Action Required dashboard cleanup (direct template edit).
- [ ] **FB-017** — Checkbox detection + finalization in `/work` Step 2b. May be partially resolved by FB-011 script extraction.
- [ ] (Plus new items from Phase 2)

### Phase 5 — Cleanup

- [ ] Delete all files/folders with `DELETE-AFTER` in Cleanup Manifest
- [ ] Revert the "Active multi-session work" notice at the top of root `CLAUDE.md`
- [ ] Run `/health-check` to verify `.claude/` integrity + no stray files
- [ ] Confirm `.claude/version.json` bump matches final scope (major/minor/patch per policy in root `CLAUDE.md`)
- [ ] Commit final state

---

## File Collision Map

Rows = files. Columns = in-flight items. Cells = section/step affected (or `•` for whole-file). Columns for Best-prac and Usage are populated during Phase 2 triage.

| File | DEC-004 | DEC-005 | DEC-006 | FB-011 | FB-015 | FB-017 | Opus 4.7 | Best-prac | Usage |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `commands/work.md` | Step 4 | | Step 4 | | • | Step 2b | | TBD | TBD |
| `system-overview.md` | atomic contract | file boundary | invariant | | | | sweep | TBD | TBD |
| `commands/health-check.md` | | Part 5 merge | Part 1 gate | | Part 6 | | | TBD | TBD |
| `rules/agents.md` | Context Separation | | | | | | model req | TBD | TBD |
| `.claude/agents/implement-agent.md` | Steps 3, 6a-c | | | Steps 3, 6a, 6c | | | frontmatter | TBD | TBD |
| `.claude/agents/verify-agent.md` | T6, T7 | | | | | | frontmatter | TBD | TBD |
| `.claude/agents/research-agent.md` | | | | | | | frontmatter | TBD | TBD |
| `.claude/CLAUDE.md` | | file-boundary | | | | | model req | TBD | TBD |
| `rules/task-management.md` | | | • | | | | | TBD | TBD |
| `rules/spec-workflow.md` | | | • | | | | | TBD | TBD |
| `rules/dashboard.md` | | | | • | Sections | | | TBD | TBD |
| `commands/breakdown.md` | | | subtask inherit | | | | | TBD | TBD |
| `commands/iterate.md` | | | | | | detection | | TBD | TBD |
| `support/reference/task-schema.md` | | | `phase` field | | | | | TBD | TBD |
| `support/reference/phase-decision-gates.md` | | | enforcement | | | • | | TBD | TBD |
| `support/reference/dashboard-regeneration.md` | | | render | • | Action Item Contract | | | TBD | TBD |
| `support/reference/decisions.md` | | | | | | line 151 | | TBD | TBD |
| `support/reference/workflow.md` | | | | | | lines 195-201 | | TBD | TBD |
| `.claude/sync-manifest.json` | | new `merge` cat | | | | | | TBD | TBD |
| `.claude/settings.json` (new) | | • | | | | | | TBD | TBD |
| `.claude/version.json` | | | | | | | bump | TBD | TBD |

**Hot files** (3+ in-flight items): `commands/work.md`, `system-overview.md`, `commands/health-check.md`, `.claude/agents/implement-agent.md`.

---

## Cleanup Manifest

Every working file for this upgrade is tagged. `DELETE-AFTER` items removed in Phase 5. Append new entries as working files are created.

| File | Tag | Note |
|------|-----|------|
| `template-upgrade-2026-04.md` (this file) | DELETE-AFTER | Tracker; purpose ends with upgrade |
| `CLAUDE.md` (root) — tracker pointer notice | REVERT (Phase 5) | Block under "You are working on the template itself..." — remove at cleanup |
| `upgrade-candidates-best-practices.md` (created in Phase 2) | DELETE-AFTER | Candidate list for user review; ephemeral intake doc |
| `upgrade-candidates-usage-report.md` (created in Phase 2) | DELETE-AFTER | Candidate list for user review; ephemeral intake doc |
| `coworkfolderspec.md` | DELETE (Phase 0) | No longer moving forward |
| `insights-report.html` | DELETE (Phase 0) | Stale; live at `~/.claude/usage-data/report.html` |
| `migration-guide.md` | DELETE (Phase 0) | Already applied to downstream projects |
| `migration-plan-v2-flat-layout.md` | DELETE (Phase 0) | Already applied; DEC-003 complete |
| `.DS_Store` | DELETE (Phase 0) | Junk + `.gitignore` addition |
| `dashboard_example_SIREN.pdf` | KEEP-ROOT | Reference for FB-014/FB-015 |
| `dashboard_export_SIREN_new.pdf` | KEEP-ROOT | Reference for FB-014/FB-015 |

---

## Session Log

### 2026-04-16 — Planning session

**Context:** User raised three incoming inputs (Opus 4.7 release, Claude Code best-practices doc, usage insights report) requiring multi-session coordination. Existing feedback backlog had not been factored in.

**Done:**
- Swept existing feedback: 5 ready items (FB-010 absorbed into DEC-004, FB-011, FB-012 absorbed into DEC-005, FB-013 absorbed into DEC-006, FB-015, FB-017) + 3 approved decisions (DEC-004/005/006 from commit `55c1040`)
- Audited root for stale artifacts: 5 files flagged for deletion, 2 SIREN PDFs to keep as references
- Built collision map from existing `**Assessed:**` lines + Opus 4.7 touchpoints — 4 hot files identified
- Agreed on 6-phase structure with file-level grouping for implementation

**Next:** Execute Phase 0 — root file cleanup, `.gitignore` update, Opus 4.7 sweep.

**Open questions for later:**
- Version bump scope (major/minor/patch) — decide at Phase 5 based on landed changes; DEC-004 may change agent contract meaningfully (potential major)
- Whether to bundle Phase 1 implementation into one session or split by decision — depends on editing load per file
