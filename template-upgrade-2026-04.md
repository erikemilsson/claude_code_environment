# Template Upgrade — April 2026

**Purpose:** Coordinate multi-session template improvements from three inputs (Opus 4.7 upgrade, Claude Code best-practices doc, usage insights report) alongside the existing feedback backlog and approved decisions.

**Status:** Phase 4 — DEC-007 Option B implemented (skills trial live); DEC-008 Option D and remaining direct items next
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

- **Active phase:** Phase 3 closed — both research decisions approved. Phase 4 implementation ready to begin.
- **DEC-007 outcome:** Option B approved (Adopt Skills for on-demand reference only). Subagents retain context-isolation guarantees. Implementation scope: new `.claude/skills/` dir, initial Skills for `decomposition-heuristics`, `spec-checklist`, `dashboard-style` (thin wrappers over existing reference content). FB-033's sub-question resolved: spec-auditor will be a subagent (if pursued).
- **DEC-008 outcome:** Option D approved (Narrow allowlist to 8 entries + document auto mode). DEC-005's layered two-file model stays intact. Implementation scope: narrow `.claude/settings.json` from 15 to 8 entries (drop: `branch`, `check-ignore`, `ls-tree`, `tree`, `find`, `sort`, `shasum`); add auto-mode documentation section to `.claude/README.md` (or setup-checklist.md); update `.claude/CLAUDE.md` Settings invariant to reference auto-mode layering. Unblocks FB-037.
- **Feedback state:** FB-020 and FB-026 archived as `absorbed` (→DEC-007 / →DEC-008). FB-033 assessment updated to note dependency resolutions (still deferred on FB-032 trial). FB-037 assessment updated to note unblocking.
- **Inflection note on DEC-008:** Frontmatter flag was conservative. Option D is narrowing + documentation, not reversal — layered model preserved. No `/iterate` spec revisit needed; template-maintenance implementation work captured in Phase 4.
- **DEC-007 Option B implemented 2026-04-17:** `.claude/skills/` directory created with three Skills (`decomposition-heuristics`, `spec-checklist`, `dashboard-style`) each containing full content from the companion reference doc plus auto-invocation frontmatter. Reference docs kept as fallback during trial — each file (Skill and reference) carries a dual-location comment so maintainers know to edit both until one is retired. `.claude/README.md` updated (Essential Files row, File Ownership list, new Skills subsection, Where to Find Things row). `sync-manifest.json` `sync` category adds `.claude/skills/*/SKILL.md`.
- **Next action:** Erik chooses the next Phase 4 unit. Suggested: (1) DEC-008 Option D implementation (narrow settings.json + auto-mode documentation, unblocks FB-037); (2) one of the hot-file batches for remaining direct-implementation items. Skills trial is passive — it validates itself through use during subsequent `/work` and `/iterate` runs.
- **Blocked on:** nothing. FB-033 remains deferred on FB-032 trial (Phase 4 direct item). FB-037 ready now.

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
- [x] Claude reads the report and produces `upgrade-candidates-usage-report.md` (root, `DELETE-AFTER`) in the same format
- [x] User reviews and approves/rejects
- [x] Claude captures approved items via `/feedback`

**Triage:**
- [x] `/feedback review` — triage complete (2026-04-17). 19 new items assessed. 3 carryover archived as absorbed (FB-010→DEC-004, FB-012→DEC-005, FB-013→DEC-006). File Collision Map Best-prac / Usage columns populated below. No duplicates among FB-019–FB-037; no rejects; no items held for refinement.
- [x] Phase 3 (research) vs Phase 4 (direct) classification — see sections below.

### Phase 3 — Cross-cutting research

Only for new items that emerge as cross-file or inflection-point decisions. Research runs iteratively (keep conversation context rather than fresh-session). Decision records land in root `decisions/`.

- [x] **FB-020** — Skills architectural research → **DEC-007 approved 2026-04-17 (Option B — reference-only adoption)**. Subagents retain context-isolation guarantees. FB-033's Skill-vs-subagent sub-question resolved: subagent. Implementation scope: new `.claude/skills/` with thin wrappers for `decomposition-heuristics`, `spec-checklist`, `dashboard-style`. FB-020 moved to archive as absorbed.
- [x] **FB-026** — Permissions story given auto-mode maturity → **DEC-008 approved 2026-04-17 (Option D — narrow to 8 entries + document auto mode, inflection-flag conservative)**. Layered two-file model preserved. Implementation scope: drop 7 entries from `.claude/settings.json` (`branch`, `check-ignore`, `ls-tree`, `tree`, `find`, `sort`, `shasum`); add auto-mode documentation to `.claude/README.md`; update `.claude/CLAUDE.md` Settings invariant wording. Unblocks FB-037. FB-026 moved to archive as absorbed.
- [ ] **FB-033** — Spec-auditor subagent + PreToolUse gate → candidate **DEC-009**. **Deferred** — gated on FB-032 trial data. Depends on FB-020 (skill-vs-subagent) and FB-026 (hook surface) outcomes. Do not start until FB-032 has been implemented (Phase 4) and trialed across several real `/iterate` sessions.

**Ordering constraints:**
- FB-020 and FB-026 can start immediately and in parallel (no shared files during research phase; decision records are isolated).
- Consider whether FB-020 and FB-026 should share a research session — both touch settings/subagent architecture, and FB-020's outcome affects where hooks could live (interacts with FB-026's DEC-005 reevaluation). Loose coupling; separate research is fine but the researcher should cross-reference.
- FB-033 research starts only after FB-032 (Phase 4) has landed + generated trial data.

### Phase 4 — Implementation of remaining items

Existing `ready` items + new items routed as direct implementation. Group by file (hot files first per implementation-grouping rule).

**Hot files** (3+ in-flight items — do these first to avoid re-reads):

- [ ] **`.claude/commands/work.md`** — FB-015 (Action Required cleanup), FB-017 (Step 2b checkbox detection), FB-027 (skip-planning callout in Step 3 routing), FB-036 (pre-dispatch confirm in Step 4).
- [ ] **`.claude/rules/session-management.md`** — FB-023 (`/btw`), FB-024 (`/rewind`/Esc+Esc), FB-025 (`/rename`). Single bundled edit.
- [ ] **`.claude/rules/agents.md`** and/or **`.claude/agents/implement-agent.md`** — FB-022 (root-cause rule), FB-034 (respect user kills), FB-035 (large-file Read guidance), FB-031 (Writer/Reviewer parallel-session mention — may alternatively go to `.claude/README.md`). Plus FB-011 call-sites if FB-011 implementation lands here.
- [ ] **`.claude/commands/iterate.md`** — FB-021 (AskUserQuestion in distill), FB-032 (Decisions-in-Proposal output contract in propose). FB-032 should land first to start generating trial data for FB-033.

**Single-item / single-file batches:**

- [ ] **FB-011** — Scripts as alternative (dashboard regen, checkbox detection); starts with a candidates inventory doc. Consider after FB-029/FB-030 (some candidates may become `claude -p` one-liners instead of bash scripts).
- [ ] **FB-019** — `@path` imports in `.claude/CLAUDE.md` (Workflow Rules section).
- [ ] **FB-028** — CLI-tool installation hints in `.claude/support/reference/setup-checklist.md`.
- [ ] **FB-029 + FB-030** — New `.claude/support/reference/automation.md`: `claude -p` primitive + fan-out pattern. Bundle (same file).

**Blocked within Phase 4:**

- [ ] **FB-037** — ~~**Blocked on FB-026 → DEC-008 closing**~~ **Unblocked 2026-04-17** by DEC-008 Option D (layered model preserved). Hook recipe now implementable: reference `.claude/settings.local.json` under `hooks` key; position in `setup-checklist.md` new "Optional Hooks" subsection.

**DEC-007 implementation (Option B — skills trial):**
- [x] **Create `.claude/skills/` directory** — done 2026-04-17
- [x] **`decomposition-heuristics/SKILL.md`** — 95 lines, mirrors `support/reference/decomposition.md`; auto-invoke description covers decomposition procedure, provenance fields, stages, cross_phase heuristic
- [x] **`spec-checklist/SKILL.md`** — 65 lines, mirrors `support/reference/spec-checklist.md`; auto-invoke description covers readiness levels, core questions, red flags, calibration
- [x] **`dashboard-style/SKILL.md`** — 489 lines, mirrors `support/reference/dashboard-regeneration.md`; auto-invoke description covers regeneration triggers, steps, section format, critical path, Project Overview diagram
- [x] **Dual-location HTML comments** added to both the Skill file and the companion reference doc so maintainers know to update both until one is retired
- [x] **`.claude/README.md`** updated — Essential Files row, File Ownership list (Template-owned), new Skills subsection, Where to Find Things row
- [x] **`.claude/sync-manifest.json`** — added `.claude/skills/*/SKILL.md` to `sync` category
- [ ] **Trial validation (passive, no action required):** subsequent `/work` decompositions and dashboard regens should auto-invoke the Skills by description match. If auto-invocation works reliably, follow-up work retires the companion reference docs and updates citation sites in commands/rules. If not, revert the Skill dir (companion docs already preserved).

**DEC-008 implementation (Option D — narrow allowlist + document auto mode):**
- [ ] **`.claude/settings.json`** — narrow `permissions.allow` from 15 entries to 8 (drop: `branch`, `check-ignore`, `ls-tree`, `tree`, `find`, `sort`, `shasum`; keep: `git status`, `git log`, `git diff`, `ls`, `grep`, `test`, `head`, `wc`)
- [ ] **`.claude/README.md`** — add auto-mode subsection next to the existing Settings subsection; explain plan/model requirements, composition with `permissions.allow`, when to enable
- [ ] **`.claude/CLAUDE.md`** — update Settings invariant wording (bullet 8) to mention auto-mode layering
- [ ] **`.claude/commands/health-check.md` Part 5c** — verify wording still accurate after allowlist narrowing (no boundary-validation change expected; just word check)
- [ ] **Unblocks FB-037** — once DEC-008 implementation commits, FB-037 hook recipe can land in `support/reference/setup-checklist.md`

**Notes:**
- FB-034 + FB-036 share an "over-eager execution" theme but land in different files (`rules/agents.md` / `implement-agent.md` vs `commands/work.md` / `parallel-execution.md`). Implementer may choose to phrase them consistently, but they are not a single edit.
- FB-032 implementation should precede FB-033 research dispatch (FB-033 is gated on FB-032 trial data).
- FB-029/FB-030 should precede FB-011 implementation if pursued as bash scripts (some candidates may collapse to `claude -p` one-liners).

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
| `commands/work.md` | ~~Step 4~~ ✓ | | ~~Step 2c summary~~ ✓ | | • | Step 2b | | FB-027 Step 3 routing | FB-036 Step 4 |
| `system-overview.md` | ~~atomic contract~~ ✓ | ~~file boundary~~ ✓ | ~~Pending Decisions~~ ✓ | | | | sweep | — | — |
| `commands/health-check.md` | | ~~Part 5 merge~~ ✓ | ~~Part 1 boolean check~~ ✓ | | Part 6 | | | — | — |
| `rules/agents.md` | ~~Context Separation~~ ✓ | | | | | | model req | FB-022 root-cause; FB-031 Writer/Reviewer | FB-034 behavior; FB-035 Tool Prefs |
| `.claude/agents/implement-agent.md` | ~~Steps 3, 6a-c~~ ✓ | | | Steps 3, 6a, 6c | | | frontmatter | FB-022 root-cause | FB-034 behavior; FB-035 Tool Prefs |
| `.claude/agents/verify-agent.md` | ~~T6, T7~~ ✓ | | | | | | frontmatter | FB-022 symptom-fix check | FB-032 decisions check |
| `.claude/agents/research-agent.md` | | | | | | | frontmatter | — | — |
| `.claude/CLAUDE.md` | | ~~file-boundary~~ ✓ | | | | | model req | FB-019 `@path` imports | FB-034 Critical Invariants |
| `rules/task-management.md` | | | ~~• (stale — no edit needed)~~ | | | | | — | — |
| `rules/spec-workflow.md` | | | ~~• (stale — no edit needed)~~ | | | | | — | FB-032 propose-approve-apply |
| `rules/dashboard.md` | | | | • | Sections | | | — | — |
| `rules/session-management.md` (new row) | | | | | | | | FB-023 `/btw`; FB-024 `/rewind`; FB-025 `/rename` | — |
| `rules/decisions.md` (new row) | | | | | | | | FB-027 skip-planning (alt site) | — |
| `commands/breakdown.md` | | | ~~subtask inherit~~ ✓ | | | | | — | — |
| `commands/iterate.md` | | | ~~(stale — no edit needed)~~ | | | detection | | FB-021 distill interview | FB-032 propose output contract |
| `commands/research.md` (new row) | | | | | | | | FB-027 trivial-skip callout | — |
| `support/reference/task-schema.md` | | | ~~`phase` row + new `cross_phase` row~~ ✓ | | | | | — | — |
| `support/reference/phase-decision-gates.md` | | | ~~skip rule + Cross-Phase section~~ ✓ | | | • | | — | — |
| `support/reference/dashboard-regeneration.md` | | | ~~`(cross-phase)` suffix~~ ✓ | • | Action Item Contract | | | — | — |
| `support/reference/parallel-execution.md` | | | ~~OR clause in eligibility~~ ✓ | | | | | — | FB-036 pre-dispatch confirm; FB-030 fan-out (alt site) |
| `support/reference/decomposition.md` | | | ~~heuristic bullet~~ ✓ | | | | | — | — |
| `support/reference/decisions.md` | | | | | | line 151 | | — | — |
| `support/reference/workflow.md` | | | | | | lines 195-201 | | — | — |
| `support/reference/setup-checklist.md` (new row) | | | | | | | | FB-028 CLI installs | FB-037 Optional Hooks appendix |
| `support/reference/automation.md` (new file) | | | | | | | | FB-029 `claude -p`; FB-030 fan-out | — |
| `.claude/README.md` (new row) | | ~~File Ownership + Settings~~ ✓ | | | | | | FB-031 Writer/Reviewer (alt site); FB-029 mention (alt site) | — |
| `.claude/sync-manifest.json` | | ~~new `merge` cat~~ ✓ (used existing `sync`) | | | | | | — | — |
| `.claude/settings.json` (new) | | ~~•~~ ✓ | | | | | | — | DEC-008 may reshape (FB-026) |
| `.claude/version.json` | | | | | | | bump | — | — |
| `.claude/agents/spec-auditor.md` (if created) | | | | | | | | — | FB-033 research-first — defer |
| `.claude/skills/spec-auditor/` (if chosen over subagent) | | | | | | | | FB-020 outcome | FB-033 alternative home |

**Hot files** (3+ in-flight items):
- `commands/work.md` — `FB-015` (•) + `FB-017` (Step 2b) + `FB-027` (Step 3 routing) + `FB-036` (Step 4). 4 items.
- `rules/agents.md` — model req + FB-022 + FB-031 + FB-034 + FB-035. 5 items.
- `.claude/agents/implement-agent.md` — frontmatter + FB-011 + FB-022 + FB-034 + FB-035. 5 items.
- `rules/session-management.md` — FB-023 + FB-024 + FB-025. 3 items; bundleable as one edit.
- `commands/iterate.md` — Step 2b detection (FB-017) + FB-021 (distill) + FB-032 (propose). 3 items across two subcommands.

**Notes on "alt site" markers:** FB-031 could land in `rules/agents.md` or `.claude/README.md`; FB-030 in `support/reference/automation.md` (primary) or as addendum to `support/reference/parallel-execution.md`; FB-027 in `commands/research.md` (callout) or `rules/decisions.md` (cross-reference). These are listed on multiple rows so a future editor sees the options; the implementer picks one during the Phase 4 edit.

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
| `plan-feedback-review-triage.md` | DELETE-AFTER | Phase 2 triage plan for fresh-session execution |
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

### 2026-04-17 — Phase 2 usage-report intake

**Done:**
- Read `plan-usage-report-intake.md` at root in a fresh context session and executed. WebFetch rejected the `file://` URL, so fell back to Read on `/Users/erikemilsson/.claude/usage-data/report.html` (951 lines, 64KB HTML). Extracted the full insight set from "At a Glance", "Where Things Go Wrong", "Features to Try", "New Usage Patterns", and "On the Horizon" sections.
- Produced `upgrade-candidates-usage-report.md` at root (DELETE-AFTER) with initial 9-item candidate list (A1/A2, B1/B2/B3, C1/C2/C3/C4) plus 5-item D section and a transparency "Already covered" section. Preemptive filter dropped 4 CLAUDE.md one-liner suggestions from the report (CM1 reshaped as A1; CM2/CM3 software-specific bits dropped; CM4 already in root `CLAUDE.md`).
- **Second-pass scan (Erik's request):** Re-examined all candidates through three post-report filters — Opus 4.7 (better instruction-following), auto mode on Max (post-dates report), and best-practices intake (FB-019–FB-031 already captured). Applied 6 adjustments: B1 scope narrowed (restart-after-kill only, resolving conflict with root `CLAUDE.md`'s UI-testing guidance); C4 demoted to "Already covered" (Excessive-Changes / User-Rejected-Action covered by existing anti-scope-creep rule, follows more reliably under Opus 4.7); A2 framing sharpened (explicit trial-gate on FB-032 + FB-020 + FB-026 upstreams); C1 FB-026 dependency note added; C2 reframed as DEC-008 baseline measurement; top note gained timing disclosure. No new candidates added, no rejections.
- Erik reviewed and marked decisions: 6 approved, 1 edited (A2 with "wait until A1 trialed properly" edit), 2 absorb-routes (C2→FB-026, C3→FB-020). No rejects.
- Captured 6 items as **FB-032 through FB-037**:
  - FB-032: "Decisions in This Proposal" structural output contract for `/iterate` propose
  - FB-033: spec-auditor subagent + PreToolUse gate (research-first; trial-gated on FB-032; candidate DEC-009)
  - FB-034: "Respect user kills" rule — don't restart long-running processes without renewed approval
  - FB-035: implement-agent file-reading guidance for large files (prefer Grep/Glob; Read `offset`/`limit`)
  - FB-036: confirm before dispatching parallel work in `/work`
  - FB-037: optional PreToolUse hook example in setup-checklist.md (deferred until FB-026 resolves)
- File Collision Map updated: Usage column populated for 8 files; two new rows added (`support/reference/setup-checklist.md`, `.claude/agents/spec-auditor.md` if created); `rules/agents.md` promoted to hot-files list (now 3 in-flight items).

**Next:** Commit Phase 2 usage-report intake, then begin `/feedback review` triage across FB-019–FB-037. Triage overlap checks especially relevant: FB-034/FB-036/FB-037 with FB-015 (action-required) unlikely to overlap; FB-032/FB-033 with FB-020 (Skills) and FB-021 (AskUserQuestion) — complementary, not overlap; FB-037 with FB-028 (CLI-tool hints) — same file `setup-checklist.md`, different sections, worth noting during triage. Phase 2 ends with triage complete.

**Open questions for later:** None for Phase 2 intake. Phase 3 research scope determined by triage outcomes.

### 2026-04-17 — Phase 2 triage (close)

**Done:**
- Read `plan-feedback-review-triage.md` at root in fresh-session context and executed the single-pass triage (no interactive `/feedback review` invocation, consistent with how capture was done).
- **Carryover absorbs (3 items):** Verified DEC-004/005/006 frontmatter `status: approved` + `decided: 2026-04-14`. Moved FB-010 (→DEC-004), FB-012 (→DEC-005), FB-013 (→DEC-006) from `feedback.md` to `archive.md` with `absorbed_into` pointers, absorption reasons, and preserved original body text. No ID collisions introduced.
- **New-item triage (19 items, FB-019–FB-037):** Every item set `status: ready` and gained a `**Assessed:** 2026-04-17` line following the shared format (impact scope, scope classification, overlap notes, route). Zero duplicates (no `absorbed`), zero rejects (no `closed` or `archived`), zero holds (no `refined`). Overlap decisions: FB-029/FB-030 bundled to shared file but kept as two items; FB-023/024/025 kept as three items bundled to one file; FB-034/FB-036 kept separate (different files, related theme); FB-020/FB-033 kept separate with dependency note (FB-033 gated on FB-020 outcome + FB-032 trial).
- **File Collision Map:** replaced all `TBD` placeholders with concrete item refs (e.g., `FB-027 Step 3 routing`). Added 5 new rows (`rules/session-management.md`, `rules/decisions.md`, `commands/research.md`, `support/reference/automation.md`, `.claude/skills/spec-auditor/`) for files that were not already listed. Hot-files list recomputed: `rules/agents.md` (5), `.claude/agents/implement-agent.md` (5), `commands/work.md` (4), `rules/session-management.md` (3), `commands/iterate.md` (3). Added "alt site" marker notes where an item has two plausible homes.
- **Phase 3 scope:** FB-020 (Skills / DEC-007) + FB-026 (permissions auto-mode / DEC-008 inflection) ready to start immediately. FB-033 (spec-auditor / DEC-009) deferred until FB-032 is trialed. Ordering rationale written into the Phase 3 section.
- **Phase 4 scope:** 16 items ready now; FB-037 blocked on FB-026 closure. Hot-file groupings and sequencing notes (FB-032 before FB-033 dispatch; FB-029/030 before FB-011) written into Phase 4 section.
- **Tracker bookkeeping:** Current State updated to "Phase 2 closed — Phase 3 or Phase 4 next"; Phase 2 triage checkbox `[x]`; "Decide Phase 3 vs Phase 4" checkbox `[x]`.

**Judgment calls worth surfacing:**
- Kept FB-023/024/025 as three items rather than absorbing into one bundle — preserves per-feature citation in downstream docs even though all three land in the same file with one edit pass.
- Kept FB-029/030 as two items for the same reason (distinct concepts: primitive vs pattern), with a Phase 4 note telling the implementer to bundle them.
- FB-037 routed as Phase 4 direct rather than Phase 3 research because the *hook recipe* isn't a decision — it's a documented opt-in — but its shape depends on the DEC-008 outcome, so it's flagged "deferred until FB-026 closes". This keeps it out of the research queue.
- Marked FB-031 and FB-030 with "alt site" notes in the collision map rather than forcing a primary location — the implementer can make the call with full context during the Phase 4 edit.

**Next:** Commit Phase 2 close. Then Erik chooses between Phase 3 (research for FB-020 and/or FB-026; keep conversation rather than fresh-session; decision records land in root `decisions/`) and Phase 4 (direct implementation grouped by hot files). Do not assume — ask first.

**Open questions for later:** None blocking. Version bump scope (Phase 5) pending total-change tally.

### 2026-04-17 — Phase 3 research: DEC-007 + DEC-008 drafted

**Done:**
- Erik chose Phase 3 option C (research FB-020 and FB-026 interleaved, keeping conversation context).
- Dispatched two parallel `claude-code-guide` agents:
  - **FB-020 agent** investigated Skills context semantics, invocation, distribution, permissions inheritance, and limitations. Primary concern answered decisively: Skill content injects into the caller's message stream (shared context), but subagents spawned *inside* a Skill still receive fresh context. Implication: Skills cannot host verify-flow orchestration (DEC-004 isolation violated at the Skill layer), but remain viable for on-demand reference content.
  - **FB-026 agent** investigated auto-mode mechanics, rule-classifier interaction, latency cost, dontAsk/hook contexts, and entry-by-entry redundancy. Primary finding: `permissions.allow` rules short-circuit the classifier — DEC-005's allowlist is not dead code. Recommends narrowing to 6–8 essential entries (Option B) rather than full reversal; full reversal would break hooks, CI, and non-Opus-4.7 users.
- Drafted `decisions/decision-007-skills-adoption-scope.md` — 4 options (A no adoption / B reference-only / C broader rules+packs / D defer); research recommends B. Not inflection. Blocks FB-033.
- Drafted `decisions/decision-008-auto-mode-permissions-reevaluation.md` — 4 options (A full reversal / B narrow to 8 / C keep DEC-005 / D narrow + document); research recommends B or D. Inflection. Blocks FB-037.
- Both records follow the DEC-005 format (frontmatter + Select Option + Context + Questions + Options Comparison + Option Details + Research Findings + Notes + Recommendation).
- Tracker updated: Current State reflects drafted proposed records; Phase 3 checkboxes `[x]` for FB-020 and FB-026 research (but the records themselves still await user selection).
- FB-033 remains deferred (gated on FB-032 trial, not on DEC-007 — DEC-007 resolves the subagent-vs-skill sub-question, but the trial-gate is about whether FB-032 itself is sufficient).

**Judgment calls worth surfacing:**
- Kept DEC-007 and DEC-008 as two separate records despite their interaction (FB-020 research noted Skills' permission inheritance relates to where hooks can live). The interaction is loose — Skills don't change DEC-005's layering, and auto mode doesn't change Skills' context semantics. Two records are clearer for audit and each can resolve on its own timeline.
- Both records use the DEC-005 Option-Matrix + Research-Findings template. DEC-007's Q5 cross-references FB-033; DEC-008's Q5 provides per-entry analysis of DEC-005's 15-entry set to justify the narrowed 8.
- Research recommendations are explicit (`## Recommendation` section) but all four options remain available in each record — Erik picks. Research agents do not decide per `.claude/rules/agents.md`.

**Next:** Erik reviews both drafted decisions and checks one option in each. Next `/work` invocation will auto-finalize (Step 2b checkbox detection), populate Decision sections, mark as approved, and unblock FB-033 (sub-question resolved) and FB-037 (DEC-008 closed). At that point, FB-020 and FB-026 move to archive as absorbed, and the template is ready to begin Phase 4 implementation work (or Phase 1-style implementation of any chosen options).

**Open questions for later:**
- DEC-008 is flagged inflection in its frontmatter — if Erik selects Option A (full reversal) this matters a lot (spec revisit); if Option B/C/D it's a minor flag. The inflection marker is conservative.
- Whether to implement DEC-007 and DEC-008 selections in the same session they close, or treat them as Phase 1-style implementations (plan-in-fresh-session-and-execute). Suggest handling inline for DEC-007 (small: maybe one new Skill + reference pointer), and plan-and-execute for DEC-008 Option B (settings.json rewrite + health-check Part 5c check + `.claude/CLAUDE.md` Settings invariant + `.claude/README.md` Settings section — touches multiple files).

### 2026-04-17 — Phase 3 close: DEC-007 (B) + DEC-008 (D) approved

**Done:**
- Erik selected **DEC-007 Option B** (adopt Skills for on-demand reference only) and **DEC-008 Option D** (narrow allowlist to 8 entries + document auto mode).
- Auto-finalized both records inline (checkbox + frontmatter `status: approved` + `decided: 2026-04-17`) — matches DEC-004/005/006 format convention where checkbox + frontmatter are the decision; Recommendation + Option Details sections carry the rationale.
- Moved FB-020 to `archive.md` with `absorbed_into: DEC-007` and reason line referencing the primary research finding (Skills inherit caller context; subagents spawned from Skills still get fresh context).
- Moved FB-026 to `archive.md` with `absorbed_into: DEC-008` and reason line referencing the research finding (rules short-circuit the classifier; allowlist is not dead code).
- Updated FB-033 Assessed line: FB-020 dependency resolved by DEC-007 (subagent, not Skill); FB-026 dependency resolved by DEC-008 (layered settings stay, hook wiring goes in `settings.local.json`). Still deferred — gating on FB-032 trial remains.
- Updated FB-037 Assessed line: unblocked. Layered two-file model preserved per DEC-008 Option D. Hook recipe implementation ready for Phase 4.
- Tracker updated: Current State reflects Phase 3 closure; Phase 3 items fully closed `[x]` with implementation scope captured; Phase 4 is next.

**Inflection-point note (DEC-008):**
- Frontmatter `inflection_point: true` was conservative. Option D is narrowing + documentation, not reversal of DEC-005. Layered two-file model, sync-manifest categorization, and settings.local.json ownership all stay as-is.
- No `/iterate` spec-revisit needed for this template-maintenance work (there is no project spec). Template-level implementation touches: `.claude/settings.json` (entry narrowing), `.claude/README.md` (new Settings/auto-mode section), `.claude/CLAUDE.md` Critical Invariants (settings bullet wording refresh). These are captured as Phase 4 implementation scope above.

**Judgment calls:**
- Inline finalization (vs. waiting for next `/work` Step 2b auto-detection) was chosen because this is template-maintenance work within the same conversation — no reason to wait for a later session to do what's already decisive.
- Kept DEC-008's inflection flag as `true` in frontmatter despite Option D being conservative — the flag records the original question's nature, not the selected outcome's scope. Future audits benefit from seeing that the question was treated as potentially inflection.
- No updates to `system-overview.md` or `.claude/CLAUDE.md` text in this close — those live changes are Phase 4 implementation work and will be committed with the DEC-008 Option D implementation unit.

**Next:** Phase 4 implementation. Erik chooses sequencing. Suggested:
1. **DEC-008 Option D implementation** — smallest, well-scoped, unblocks FB-037. Touches `.claude/settings.json` (narrow), `.claude/README.md` (new section), `.claude/CLAUDE.md` (invariant wording). ~4 files.
2. **DEC-007 Option B implementation** — new `.claude/skills/` dir + 3 thin Skills wrapping existing reference content. Decide whether to keep duplicate reference docs or delete originals. ~4–5 new files + possible deletions.
3. **Remaining Phase 4 items** — grouped by hot file (`commands/work.md`, `rules/agents.md`, `.claude/agents/implement-agent.md`, `rules/session-management.md`, `commands/iterate.md`).

Any of these can be inline or plan-and-execute in a fresh session. DEC-008 is a good first pick — small scope, immediate FB-037 unblock, and validates the Option D narrowed set before other Phase 4 work adds entries (if any). 

**Open questions for later:** None blocking.

### 2026-04-17 — Phase 4: DEC-007 Option B implementation (skills trial)

**Done:**
- Created `.claude/skills/` directory with three Skills:
  - `decomposition-heuristics/SKILL.md` (95 lines, 5.2KB) — full content from `support/reference/decomposition.md` plus auto-invocation frontmatter
  - `spec-checklist/SKILL.md` (65 lines, 2.8KB) — full content from `support/reference/spec-checklist.md`
  - `dashboard-style/SKILL.md` (489 lines, 38.5KB) — full content from `support/reference/dashboard-regeneration.md`
- Frontmatter descriptions tuned for auto-invocation: each description explicitly lists the triggering contexts (e.g., "use when decomposing a spec", "use when regenerating .claude/dashboard.md"). This is the content Claude pattern-matches against when deciding whether to auto-load the Skill.
- Added dual-location HTML comments to all six files (3 Skills + 3 reference docs) so future template maintainers know the mirror relationship and update both until one is retired.
- Updated `.claude/README.md`: new `skills/` row in Essential Files, `SKILL.md` added to Template-owned bullet in File Ownership, new "Skills" subsection explaining the pattern + current trial set, new "On-demand reference skills" row in Where to Find Things.
- Updated `.claude/sync-manifest.json`: added `.claude/skills/*/SKILL.md` to `sync` category (after `.claude/agents/*.md`). Skills ship with the template just like commands and agents.
- Did NOT update citation sites in commands/rules. References to the three reference docs still work because those files remain in place during the trial. If trial succeeds, a follow-up pass retires the reference docs and updates ~15 citation sites.

**Judgment calls:**
- Copied full content into Skills rather than writing pointer-wrappers. A Skill that redirects to a file adds no value over a direct Read — the whole point of auto-invocation is loading content that guides behavior. Full content means each Skill is self-sufficient when invoked.
- Kept the approved name `dashboard-style` for the third Skill rather than renaming to `dashboard-regeneration` (which would be more accurate). Sticking with DEC-007's approved naming avoids drift between the decision record and implementation; renaming is a trivial follow-up.
- Trial kept reversible: reference docs preserved, no citation updates. If Skills don't auto-invoke reliably, remove `.claude/skills/` and nothing else changes.

**Next:** Erik chooses the next Phase 4 unit. Strong suggestion: DEC-008 Option D implementation (narrow `settings.json` + auto-mode documentation). Small scope (~4 files), immediate FB-037 unblock, and validates the Option D narrowed baseline before other Phase 4 work potentially re-expands it.

**Open questions for later:**
- Trial validation is passive — the next `/work` decomposition or dashboard regeneration will either auto-invoke the Skills correctly or not. If auto-invocation proves unreliable (e.g., Claude reads the companion reference doc directly instead), consider whether descriptions need tuning or whether the Skills pattern itself is a poor fit for this template's reference content.
- Follow-up if trial succeeds: retire companion reference docs (3 files), update citation sites in `commands/work.md`, `commands/iterate.md`, `commands/breakdown.md`, `rules/dashboard.md`, `rules/spec-workflow.md`, `support/reference/README.md`, `support/reference/task-schema.md`, `support/reference/phase-decision-gates.md`, `support/reference/extension-patterns.md`, `system-overview.md`.
