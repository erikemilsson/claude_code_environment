# Template Upgrade — April 2026

**Purpose:** Coordinate multi-session template improvements from three inputs (Opus 4.7 upgrade, Claude Code best-practices doc, usage insights report) alongside the existing feedback backlog and approved decisions.

**Status:** Phase 1 — Implement approved decisions
**Last updated:** 2026-04-17

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

- **Active phase:** Phase 1 — Implement approved decisions
- **Next action:** DEC-006 — Phase gate flexibility. Read `decisions/decision-006-phase-gate-flexibility.md` first to confirm selected option; plan touchpoints across `commands/work.md`, `commands/health-check.md`, `commands/breakdown.md`, `commands/iterate.md`, `rules/task-management.md`, `rules/spec-workflow.md`, `support/reference/task-schema.md`, `support/reference/phase-decision-gates.md`, `system-overview.md`.
- **Blocked on:** nothing — DEC-005 executed; DEC-004 already committed as `c5805b8`

---

## Phases

### Phase 0 — Hygiene ✓ Complete (commits `40f80a5`, `05a17f2`)

- [x] **Root file cleanup** — deleted `coworkfolderspec.md`, `insights-report.html`, `migration-guide.md`, `migration-plan-v2-flat-layout.md`, `.DS_Store`; tracked `dashboard_example_SIREN.pdf`
- [x] **`.gitignore`** — `.DS_Store` already present (lines 5-6), no edit needed
- [x] **Opus 4.7 reference sweep** — 19 occurrences updated across 12 files; pinned `claude-opus-4-7[1m]` in docs, alias `opus[1m]` in Task spawns
- [x] **Context discipline note** added to `.claude/CLAUDE.md` § Model Requirement
- [x] **Pre-commit hook** — verified functional (warned on version.json during 4.7 commit)
- [ ] **Version bump** — deferred to Phase 5 (decide scope once total changes known)

### Phase 1 — Implement approved decisions

Decisions already researched and approved (commit `55c1040`). Read each decision record first to confirm the selected option's scope matches the feedback `**Assessed:**` line (scope may have narrowed during research).

- [x] **DEC-004** — Subagent capability contract → `decisions/decision-004-subagent-capability-contract.md`. Closes FB-010. *(Option B implemented 2026-04-17 — orchestrator owns all `.claude/` state transitions.)*
- [x] **DEC-005** — Base allowedTools shipping policy → `decisions/decision-005-base-allowedtools-shipping-policy.md`. Closes FB-012. *(Option E implemented 2026-04-17 — template ships `.claude/settings.json` with 15-entry base `permissions.allow`; user additions layer in `settings.local.json`.)*
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
| `commands/work.md` | ~~Step 4~~ ✓ | | Step 4 | | • | Step 2b | | TBD | TBD |
| `system-overview.md` | ~~atomic contract~~ ✓ | ~~file boundary~~ ✓ | invariant | | | | sweep | TBD | TBD |
| `commands/health-check.md` | | ~~Part 5 merge~~ ✓ | Part 1 gate | | Part 6 | | | TBD | TBD |
| `rules/agents.md` | ~~Context Separation~~ ✓ | | | | | | model req | TBD | TBD |
| `.claude/agents/implement-agent.md` | ~~Steps 3, 6a-c~~ ✓ | | | Steps 3, 6a, 6c | | | frontmatter | TBD | TBD |
| `.claude/agents/verify-agent.md` | ~~T6, T7~~ ✓ | | | | | | frontmatter | TBD | TBD |
| `.claude/agents/research-agent.md` | | | | | | | frontmatter | TBD | TBD |
| `.claude/CLAUDE.md` | | ~~file-boundary~~ ✓ | | | | | model req | TBD | TBD |
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
| `.claude/sync-manifest.json` | | ~~new `merge` cat~~ ✓ (used existing `sync`) | | | | | | TBD | TBD |
| `.claude/settings.json` (new) | | ~~•~~ ✓ | | | | | | TBD | TBD |
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
| `plan-dec-004-implementation.md` | DELETE-AFTER | DEC-004 implementation plan for fresh-session execution |
| `plan-dec-005-implementation.md` | DELETE-AFTER | DEC-005 implementation plan for fresh-session execution |
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
- Established Control and Commits section — user approves intake and edit units; one commit per logical unit
- **Executed Phase 0** (commits `40f80a5` root cleanup, `05a17f2` Opus 4.7 sweep)
- Verified Task spawn syntax via claude-code-guide agent: `opus[1m]` alias forces 1M context; plain `opus` resolves to non-1M
- Added context-discipline note to `.claude/CLAUDE.md` — 1M is headroom, not license

**Next:** Phase 1 — implement DEC-004 (subagent capability contract). Read decision record first to confirm selected option, then plan touchpoints across `commands/work.md`, `agents/implement-agent.md`, `agents/verify-agent.md`, `rules/agents.md`, `system-overview.md`.

### 2026-04-17 — DEC-004 scoping + plan

**Done:**
- Verified current-day status of the three subagent sandbox restrictions (issues #38806, #4182, #18950/22665/37730) via claude-code-guide agent — all three still in place. Option B assumptions hold.
- Resolved three open questions from DEC-004: Q1 write scope = confirm (all writes move to orchestrator), Q2 friction-marker persistence = (a) orchestrator appends to log, Q3 = verified online first.
- Approved two structured-report schemas (implement-agent, verify-agent per-task + phase-level) as the agent↔orchestrator contract
- Approved three judgment calls: individual per-task verify-agent dispatch in parallel mode; State Persistence Protocol inlined in `work.md`; timeout logic moves to orchestrator unchanged
- Wrote full implementation plan to `plan-dec-004-implementation.md` for fresh-session execution (keeps rewrite context clean)

**Next:** Fresh session (new conversation or `/clear` then resume) reads `plan-dec-004-implementation.md` and executes the 6-file rewrite. Commit message already drafted in the plan.

**Open questions for later:** None for DEC-004. DEC-005 and DEC-006 still pending after.

### 2026-04-17 — DEC-004 execution

**Done:**
- Executed `plan-dec-004-implementation.md` across all 6 target files:
  - `.claude/agents/implement-agent.md` — full rewrite; Steps 3/6a/6b/6c collapsed into Step 6 "Return Structured Report" with JSON contract; friction-marker and handoff guidance rewritten to match report-returning model
  - `.claude/agents/verify-agent.md` — full rewrite; T6/T7 + phase Steps 6/7 restructured as return schemas (per-task + phase-level); `task_verification` persistence, `verification-result.json` writes, and fix-task creation all moved to orchestrator contract; turn-budget and wind-down protocols rewritten
  - `.claude/commands/work.md` — Step 4 gains "State Persistence Protocol" sub-section with full after-implement-agent / after-verify-agent (per-task + phase-level) procedures; the 4 existing execution sub-sections reference it
  - `.claude/support/reference/parallel-execution.md` — Write Ownership Rules table reversed (orchestrator is sole writer); Section 3 spawn prompt requires structured reports; Section 4 collect loop processes implement-agent reports and dispatches per-task verify-agents individually
  - `system-overview.md` — atomic contract reframed (implement→verify invariant preserved, writer moved to orchestrator); fresh-eyes framing clarified in "Context Separation" and "Two-Agent Verification" sections; DEC-004 references added
  - `.claude/rules/agents.md` — Context Separation updated; new "State Ownership" section; Tool Preferences note added re: subagent harness constraints
- Cleared stale references in 3 further docs (outside the 6 but surfaced by grep): `workflow.md` (build-workflow step list, guided-testing flow), `task-schema.md` ("Awaiting Verification" attribution), `shared-definitions.md` (agent glossary entries), `context-transitions.md` (wind-down step mapping)
- Grep verification: remaining `Step 6[abc]` / "verify-agent writes" references are confined to `plan-dec-004-implementation.md`, `decisions/decision-004-*.md`, `decisions/.archive/`, `.claude/support/feedback/feedback.md` (FB-010 historical context), and `tests/scenarios/` (not in this commit's scope)

**Next:** Commit the DEC-004 changes, then proceed to DEC-005 (base `allowedTools` shipping policy).

**Open questions for later:** Tests in `tests/scenarios/08-verification-gate-integrity.md` and `tests/scenarios/11-non-software-project.md` still describe the old "implement-agent writes task_verification" state — update in a follow-up commit or during Phase 5 cleanup.

### 2026-04-17 — DEC-005 plan

**Done:**
- Reviewed DEC-005 decision record (Option E approved: layered two-file settings model)
- Verified current state: template has no `.claude/settings.json`; `.claude/settings.local.json` exists (gitignored); `sync-manifest.json` has no settings entry; `health-check.md` Part 5c is a 3-line presence check
- Cross-checked the collision map against the approved option — the "new `merge` cat" column entry is stale for DEC-005 (Option E needs no new category; it uses existing `sync`). Plan reflects Option E's actual footprint.
- Wrote `plan-dec-005-implementation.md` for fresh-session execution. 6 files: new `.claude/settings.json`, sync-manifest update, health-check Part 5c rewrite, `.claude/CLAUDE.md` Critical Invariants bullet, `system-overview.md` File Map + Pending Decisions, `.claude/README.md` File Ownership + Settings subsection. Commit message drafted.

**Next:** Fresh session (new conversation or `/clear` then resume) reads `plan-dec-005-implementation.md` and executes. Commit message already drafted in the plan.

**Open questions for later:** None for DEC-005. DEC-006 remains pending.

**Open questions for later:**
- Version bump scope (major/minor/patch) — decide at Phase 5 based on landed changes; DEC-004 may change agent contract meaningfully (potential major)
- Whether to bundle Phase 1 implementation into one session or split by decision — depends on editing load per file

### 2026-04-17 — DEC-005 execution

**Done:**
- Executed `plan-dec-005-implementation.md` across all 6 target files:
  - `.claude/settings.json` (new): shipped 15-entry base `permissions.allow` set (read-only git/ls/grep/find/test/sort/shasum/head/wc/tree family); JSON structure verified (exactly `permissions.allow`, nothing else)
  - `.claude/sync-manifest.json`: added `.claude/settings.json` to `sync` (immediately after `.claude/CLAUDE.md`); `settings.local.json` confirmed still in `ignore`; `notes` field expanded to document the layered two-file pattern
  - `.claude/commands/health-check.md`: Part 5c rewritten from 3-line "Settings Conflict Detection" to full "Settings Boundary Validation" with JSON parse, scope check (only `permissions.allow` allowed), `[M]`/`[S]` prompt to move stray entries, and drift-reassurance note. Part 5/5c name references elsewhere in the file (Steps 2/3 summaries line 762, 780) already used generic wording ("settings checks") — no rename needed.
  - `.claude/CLAUDE.md`: added 8th Critical Invariants bullet about settings layering (placed after the workspace invariant)
  - `system-overview.md`: removed DEC-005 row from Pending Template Decisions (line 24); File Map table now has two rows for settings (template-owned + user-owned)
  - `.claude/README.md`: File Ownership lists updated (added `settings.json` to Template-owned, `settings.local.json` to Project-owned); new `### Settings` subsection added after File Ownership explaining the runtime merge
- Verification: both JSON files parse; settings.json has exactly `permissions.allow` with 15 entries; no lingering "Settings Conflict Detection" or "template doesn't ship settings" references in active docs (only in decision record + archive, which is correct — those are frozen research artifacts)

**Next:** Commit the DEC-005 changes, then proceed to DEC-006 (phase gate flexibility). Commit message drafted in plan file.

**Open questions for later:** None for DEC-005. DEC-006 remains pending.
