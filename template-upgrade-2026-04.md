# Template Upgrade — April 2026

**Purpose:** Coordinate multi-session template improvements from three inputs (Opus 4.7 upgrade, Claude Code best-practices doc, usage insights report) alongside the existing feedback backlog and approved decisions.

**Status:** Phase 2 in progress — best-practices intake complete; usage-report intake pending
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

- **Active phase:** Phase 2 — New input intake (usage-report bundle remaining)
- **Next action:** Fresh session reads `plan-usage-report-intake.md` at root and executes. Source is `file:///Users/erikemilsson/.claude/usage-data/report.html`; output is `upgrade-candidates-usage-report.md` at root (DELETE-AFTER) in the same A/B/C/D format as `upgrade-candidates-best-practices.md`. Approved captures continue the FB sequence from FB-032.
- **Blocked on:** nothing — best-practices intake bundle committed; `plan-usage-report-intake.md` and Cleanup Manifest update committed as Phase 2 prep for fresh-context handoff.

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
- [x] **DEC-006** — Phase gate flexibility → `decisions/decision-006-phase-gate-flexibility.md`. Closes FB-013. *(Option A implemented 2026-04-17 — `cross_phase: true` boolean field added; per-task opt-in exempts task from phase gate on eligibility while preserving phase membership for verification.)*

**Implementation order:** hottest file first — `commands/work.md` takes touchpoints from all three decisions + FB-017. Apply in a single editing pass to avoid re-reading.

### Phase 2 — New input intake

Intake control is explicit: Claude produces a candidate list first, user approves per-item, only approved items enter `/feedback`.

**Best-practices doc (https://code.claude.com/docs/en/best-practices):**
- [x] Claude reads the doc and produces `upgrade-candidates-best-practices.md` (root, `DELETE-AFTER`). Each candidate: title, 1-line description, tentative impact scope, relevance rationale. No `/feedback` invocations yet.
- [x] User reviews candidate list and marks each `[approve]` / `[edit]` / `[reject]` with 1-line reason on rejects
- [x] Claude captures approved items via `/feedback` (one per candidate), using any user edits

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
| `commands/work.md` | ~~Step 4~~ ✓ | | ~~Step 2c summary~~ ✓ | | • | Step 2b | | TBD | TBD |
| `system-overview.md` | ~~atomic contract~~ ✓ | ~~file boundary~~ ✓ | ~~Pending Decisions~~ ✓ | | | | sweep | TBD | TBD |
| `commands/health-check.md` | | ~~Part 5 merge~~ ✓ | ~~Part 1 boolean check~~ ✓ | | Part 6 | | | TBD | TBD |
| `rules/agents.md` | ~~Context Separation~~ ✓ | | | | | | model req | TBD | TBD |
| `.claude/agents/implement-agent.md` | ~~Steps 3, 6a-c~~ ✓ | | | Steps 3, 6a, 6c | | | frontmatter | TBD | TBD |
| `.claude/agents/verify-agent.md` | ~~T6, T7~~ ✓ | | | | | | frontmatter | TBD | TBD |
| `.claude/agents/research-agent.md` | | | | | | | frontmatter | TBD | TBD |
| `.claude/CLAUDE.md` | | ~~file-boundary~~ ✓ | | | | | model req | TBD | TBD |
| `rules/task-management.md` | | | ~~• (stale — no edit needed)~~ | | | | | TBD | TBD |
| `rules/spec-workflow.md` | | | ~~• (stale — no edit needed)~~ | | | | | TBD | TBD |
| `rules/dashboard.md` | | | | • | Sections | | | TBD | TBD |
| `commands/breakdown.md` | | | ~~subtask inherit~~ ✓ | | | | | TBD | TBD |
| `commands/iterate.md` | | | ~~(stale — no edit needed)~~ | | | detection | | TBD | TBD |
| `support/reference/task-schema.md` | | | ~~`phase` row + new `cross_phase` row~~ ✓ | | | | | TBD | TBD |
| `support/reference/phase-decision-gates.md` | | | ~~skip rule + Cross-Phase section~~ ✓ | | | • | | TBD | TBD |
| `support/reference/dashboard-regeneration.md` | | | ~~`(cross-phase)` suffix~~ ✓ | • | Action Item Contract | | | TBD | TBD |
| `support/reference/parallel-execution.md` | | | ~~OR clause in eligibility~~ ✓ | | | | | TBD | TBD |
| `support/reference/decomposition.md` | | | ~~heuristic bullet~~ ✓ | | | | | TBD | TBD |
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
| `plan-dec-006-implementation.md` | DELETE-AFTER | DEC-006 implementation plan for fresh-session execution |
| `plan-usage-report-intake.md` | DELETE-AFTER | Phase 2 usage-report intake plan for fresh-session execution |
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

### 2026-04-17 — DEC-006 plan

**Done:**
- Reviewed DEC-006 decision record (Option A approved: add optional `cross_phase: true` boolean field, per-task opt-in, exempt from phase gate on eligibility only)
- DEC-005 committed as `3cb10d8` — settings layering confirmed in-place
- Verified current state of 9 target files. Key line anchors captured: `task-schema.md:122` (phase row), `phase-decision-gates.md:51-55` (skip rule), `parallel-execution.md:29` (eligibility), `work.md:367` (Step 2c summary), `breakdown.md:18-34` (subtask JSON), `decomposition.md:37-45` (Task Creation Guidelines), `dashboard-regeneration.md:~389` (Section Display Rules), `system-overview.md:23-24` (Pending Decisions), `health-check.md:25` (Check 1).
- Confirmed judgment calls with user: dashboard annotation = text `(cross-phase)` suffix (no emoji); health-check Part 1 boolean validation added as 9th touchpoint
- Noted that collision map entries for `rules/task-management.md`, `rules/spec-workflow.md`, and `commands/iterate.md` in the DEC-006 column are stale — Option A's footprint does not reach those files. To be struck through in the post-execution tracker update.
- Wrote `plan-dec-006-implementation.md` for fresh-session execution. 9 files. Commit message drafted in the plan. Inflection-point note included in commit message + post-execution tracker steps.

**Next:** Fresh session (new conversation or `/clear` then resume) reads `plan-dec-006-implementation.md` and executes. After commit, Phase 1 is complete; proceed to Phase 2 (new input intake — best-practices doc + usage insights report).

**Open questions for later:** None for DEC-006. After DEC-006 commits, Phase 1 is done.

### 2026-04-17 — DEC-006 execution

**Done:**
- Executed `plan-dec-006-implementation.md` across all 9 target files:
  - `.claude/support/reference/task-schema.md` — `phase` row now mentions the `cross_phase` escape hatch; new `cross_phase` Boolean row added immediately after `parallel_safe` with long-lead-work semantics
  - `.claude/support/reference/phase-decision-gates.md` — Phase Check procedure split into `!= true` (skip) and `== true` (bypass + log) branches; new `### Cross-Phase Tasks` sub-section explains exemption scope
  - `.claude/support/reference/parallel-execution.md` — eligibility OR clause added: `task.phase <= active_phase OR task.cross_phase == true`
  - `.claude/commands/work.md` — Step 2c summary clarifies eligibility "in active phase (or `cross_phase: true`)"
  - `.claude/commands/breakdown.md` — subtask inheritance note covering `cross_phase` (auto-inherit) and `parallel_safe` (per-subtask per side effects)
  - `.claude/support/reference/decomposition.md` — cross-phase heuristic bullet with keyword list (recruit/procure/approve/schedule/coordinate/stakeholder/vendor/contract) and 14-day `external_dependency.expected_date` threshold; always prompts before setting
  - `.claude/support/reference/dashboard-regeneration.md` — Section Display Rules has `(cross-phase)` title-suffix rule; phase table and counts remain unchanged
  - `system-overview.md` — DEC-006 bullet removed from Pending Template Decisions; DEC-004 bullet retained (per plan; tied to Phase 5 decisions-folder purge)
  - `.claude/commands/health-check.md` — Part 1 Check 1 now requires `cross_phase` (with `parallel_safe`, `out_of_spec`, `out_of_spec_rejected`, `user_review_pending`) to be Boolean when present
- Grep verification: `cross_phase` appears in all 8 expected files (all targets minus `system-overview.md`, which correctly contains no reference); `phase-decision-gates.md` has both the `!= true` skip branch (line 52) and the `== true` bypass branch (line 57) plus the new sub-section (line 64); `system-overview.md` has only the DEC-004 Pending Decisions bullet remaining
- File Collision Map updated: DEC-006 column entries struck through with done-markers; `rules/task-management.md`, `rules/spec-workflow.md`, and `commands/iterate.md` DEC-006 entries marked "stale — no edit needed" (Option A's footprint narrower than the map anticipated); two missing rows added for `support/reference/parallel-execution.md` and `support/reference/decomposition.md` (completed entries)

**Next:** Commit the DEC-006 changes. Commit message drafted in `plan-dec-006-implementation.md`. After commit, Phase 1 is complete; proceed to Phase 2 (new input intake — best-practices doc + usage insights report).

**Open questions for later:** None for DEC-006. Downstream projects running `/work` after pulling this change may encounter phase-boundary nudges toward `/iterate` — per the inflection-point note in the commit message.

### 2026-04-17 — Phase 2 best-practices intake

**Done:**
- Fetched https://code.claude.com/docs/en/best-practices via WebFetch; produced `upgrade-candidates-best-practices.md` at root (DELETE-AFTER) with 17 candidates grouped into A (template/architecture), B (doc/rules tweaks), C (user-facing tips), D (preemptively rejected with 1-line reasons) plus an "Already covered in template" transparency section
- Preemptively dropped 4 candidates after Erik flagged them as absorbed by Opus 4.7 + 1M context: CLAUDE.md/rules bloat audit, custom compaction instructions, IMPORTANT/YOU MUST emphasis tuning, separate prompting-tips reference doc. Top note in the candidate file explains what was dropped and why.
- Erik reviewed the file per-item. Tally: 11 approved, 2 edited (research/decision-flavored), 1 rejected (C2 CLAUDE.local.md — template is personal-use only)
- Captured all 13 non-rejected items into `.claude/support/feedback/feedback.md` as FB-019 through FB-031. Two edits converted candidates into bigger questions: FB-020 (Skills research-first — sub-agent context-window concern, candidate DEC-007) and FB-026 (permissions/auto-mode reevaluation — inflection-point candidate, may impact DEC-005, candidate DEC-008). Both flagged for triage route rather than direct implementation.
- Cross-reference aids for usage-report bundle: FB-011 (scripts), FB-015 (dashboard action-required), FB-017 (checkbox detection), plus new FB-020 and FB-026 are existing anchors — overlapping usage-report findings should be routed as absorbs, not duplicates

**Next:** Write the usage-report intake plan at root (`plan-usage-report-intake.md`) and commit it as Phase 2 prep. Fresh-context session then executes the plan: fetch `file:///Users/erikemilsson/.claude/usage-data/report.html`, produce `upgrade-candidates-usage-report.md`, collect Erik's decisions, capture approved items as FB-032+.

**Open questions for later:** None for the best-practices intake. Phase 2 finishes with `/feedback review` triage after the usage-report bundle lands.
