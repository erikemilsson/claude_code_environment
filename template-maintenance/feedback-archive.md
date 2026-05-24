# Archived Feedback

All resolved feedback items. Each entry preserves its final status and reason.

- **promoted** — Incorporated into the spec via `/iterate`
- **absorbed** — Combined into another item (has `absorbed_into` pointer)
- **closed** — Investigated but decided against
- **archived** — Not relevant (quick triage)

---

## FB-001: /work must check memory for known dangerous operations before executing

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Combined into FB-008
**Absorbed Into:** FB-008

When `/work` routes to actions that involve running processes, it proceeds without checking whether previous sessions flagged those operations as dangerous.

## FB-002: /work session continuity fails across conversation boundaries

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Combined into FB-008
**Absorbed Into:** FB-008

`/work` re-derives project state from task files alone in new sessions, missing blocked tasks and promises from previous sessions.

## FB-004: Plan mode workflow changed — template should guide the new "plan to file" pattern

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Combined into FB-009
**Absorbed Into:** FB-009

The old "compact with plan" feature no longer exists. The template should guide users toward the write-to-file replacement workflow.

## FB-006: Exiting plan mode should prompt to persist the plan to a file

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Combined into FB-009, then FB-009 absorbed into FB-007
**Absorbed Into:** FB-007

When the user exits plan mode, there's no prompt to save the plan to a durable file. The exit moment is the natural trigger point for persistence.

## FB-009: Plan persistence workflow — guide users and prompt at exit

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Collapses into FB-007 once persistence guidance is clear enough
**Absorbed Into:** FB-007

The old "compact with plan" is gone. The replacement (write plan to workspace, clear, read and execute) works but is non-obvious. Users need guidance at the right moment. Collapsed into FB-007 because clear persistence guidance resolves both items.

## FB-010: Subagents spawned by /work cannot write `.claude/tasks/` or spawn nested Task tools

**Status:** absorbed
**Captured:** 2026-04-07
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-004
**Reason:** DEC-004 (subagent capability contract, approved 2026-04-14, implemented 2026-04-17) adopted Option B — orchestrator owns all `.claude/` state transitions; subagents return structured reports. This resolves the documented workflow-violation by making the report-returning pattern the contract rather than a workaround.

**Refined:** 2026-04-14 — Reconcile the subagent-capability contract. First investigate what subagents are actually allowed to do in the current harness (writes to `.claude/tasks/`, nested `Task` tool). Then align either the permissions/sandbox or the agent-definition docs so the documented workflow matches execution reality. Preference: if subagents can be given the capability, let them own Steps 6a/6b as documented — orchestrator fallback only if the harness genuinely can't allow it. Primary concern is the workflow-contract violation.
**Assessed:** 2026-04-14 — Affects `.claude/agents/implement-agent.md` (Steps 3, 6a, 6b, 6c), `.claude/agents/verify-agent.md` (T6, T7), `.claude/commands/work.md` (Step 4 dispatch), `.claude/rules/agents.md` (Context Separation), `system-overview.md` (atomic implement→verify contract). Scope: corrective. Conflict: current docs assert atomic agent-owned contract; if harness can't be fixed, orchestrator becomes co-owner — a non-trivial architectural shift. Best routed to a decision record (store at root `decisions/`, ephemeral) rather than a direct template edit, since "fix sandbox" vs "formalize orchestrator ownership" lead to different architectures.

When `/work` dispatches implement-agents and verify-agents via the `Task` tool (both in parallel batches and sequentially), the spawned subagents run in a sandbox that:

1. **Denies write access to `.claude/tasks/`** — Edit, Write, and even `Bash` (with `dangerouslyDisableSandbox: true`) all return permission-denied for any path under `.claude/tasks/`, despite the additional working directories listed in the agent env. Reads work; only writes are blocked. The implementation file edits inside `app/` succeed — only writes outside `app/` (the project's primary cwd) are blocked.

2. **Does not expose the `Task` tool** — implement-agents cannot spawn the verify-agent subagent that Step 6b of `implement-agent.md` mandates. `Task` is not in the agent's tool list and `ToolSearch` cannot find it.

The implement-agent and verify-agent workflows in `.claude/agents/*.md` both assume the agent can:
- Step 6a: write `task.status = "Awaiting Verification"` and notes back to `task-{id}.json`
- Step 6b: spawn verify-agent as a separate subagent
- Verify-agent T-steps: write `task_verification` block back to the task JSON

None of these are possible from within a spawned subagent in the current harness. Every parallel implement-agent returns a structured "I'm done, here's what I did, the coordinator needs to handle 6a/6b" report, and the orchestrator (parent `/work` agent) has to manually:
1. Read the modified task file
2. Edit status `In Progress → Awaiting Verification` + write notes
3. Spawn verify-agent itself
4. Read the verify-agent's structured report
5. Manually persist the `task_verification` block + status `Awaiting Verification → Finished`

This worked but added significant orchestrator overhead per task. In a recent Phase 10 session (7 tasks across 3 dispatch rounds), the coordinator handled 14 manual JSON edits + 7 verify-agent dispatches + 7 manual verification persistences. The cost is real: extra context window pressure on the coordinator, slower parallel batches (because re-serialization at the orchestrator), and a workflow contract violation (Steps 6a/6b are nominally the implement-agent's responsibility, not the coordinator's).

## FB-012: Standardized base allowedTools set in template with merge-aware health-check

**Status:** absorbed
**Captured:** 2026-04-08
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-005
**Reason:** DEC-005 (base allowedTools shipping policy, approved 2026-04-14, implemented 2026-04-17) adopted Option E — template ships `.claude/settings.json` with 15-entry base `permissions.allow`; additions layer via `settings.local.json`; health-check enforces the boundary. All four concerns from this item (base set shape, merge strategy, file ownership, health-check behavior) are resolved by the decision record and its implementation. FB-026 (auto-mode reevaluation) may revisit the permissions model, but that is a new decision, not a reopening of this item.

**Refined:** 2026-04-14 — Promoted without Q&A; capture text is the refined insight. Add a conservative template-owned "base" `allowedTools` set (safe for any project) to reduce permission prompts in `acceptEdits` mode. Projects extend via their own `.claude/settings.json` / `.claude/settings.local.json`. Health-check must merge the base set into existing projects without clobbering project-specific additions.
**Assessed:** 2026-04-14 — Requires a new shipped `.claude/settings.json` (doesn't exist today — template policy is currently "doesn't ship settings"), reclassifying it in `.claude/sync-manifest.json` (probably to a new `merge` category), flipping `health-check.md` Part 5c (which currently asserts the opposite), adding key-granular merge logic to Part 5 Template Sync, and updating `system-overview.md` and root `CLAUDE.md` file-boundary table. Scope: additive + corrective. Open policy questions (merge strategy add-only vs remove-on-update, which Bash commands belong in base set, whole-file vs key-granular merge) warrant a decision record at root `decisions/` before implementation. Note: the reversal should be scoped to `allowedTools` only — hooks/env/theme stay user-owned, which forces key-granular merge logic.

Add a standardized set of accepted permissions (`allowedTools`) to the Claude Code environment template. Goal: reduce permission prompts (especially in `acceptEdits` mode, since Max plan can't use auto mode) while keeping things safe and maintainable.

## FB-013: Revisit hard phase transition dependencies for cross-phase parallel tasks

**Status:** absorbed
**Captured:** 2026-04-10
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-006
**Reason:** DEC-006 (phase gate flexibility, approved 2026-04-14, implemented 2026-04-17) adopted Option A — optional `cross_phase: true` boolean on individual tasks exempts them from the phase gate on eligibility while preserving phase membership for verification. Directly resolves the SIREN recruitment case that surfaced this item; schema, eligibility, dashboard annotation, breakdown inheritance, and health-check boolean validation all landed in the same pass.

**Refined:** 2026-04-14 — The hard phase gate is a software-centric assumption that breaks for research/procurement/stakeholder-engagement domains where long-running activities (often `owner: human`) must start before prior phases close. SIREN is representative, not a one-off, so a schema change is justified. Two viable mechanisms remain open and should go to a decision record: (a) add optional `cross_phase: true` on individual tasks, or (b) weaken the phase gate to only block on `owner: claude` / `owner: both`, letting `owner: human` tasks float. Other directions (spec-level phase-overlap declarations, document-the-workaround) are disfavored.
**Assessed:** 2026-04-14 — Affects `task-schema.md` (`phase` field definition line 122), `phase-decision-gates.md` (enforcement procedure), `commands/work.md` Step 4, `rules/task-management.md` + `rules/spec-workflow.md`, `commands/health-check.md` Part 1, `commands/breakdown.md` (subtask inheritance under option a), `dashboard-regeneration.md` (cross-phase rendering), `system-overview.md` (invariant description). Scope: additive (option a) or corrective (option b reverses a documented invariant). Note: parallel-execution rules in `task-management.md` already use dependency+file-conflict eligibility without referencing phase — FB-013 is consistent with that model. Decision record at root `decisions/` (ephemeral) should resolve (a) vs (b); once decided, implementation is bounded.

Original capture: phase gate blocks Phase N+1 tasks until all Phase N complete — breaks for research/procurement/stakeholder work with long-running activities that naturally span phases. SIREN workshop recruitment was the surfacing case.

## FB-020: Research Skills architectural limitations before template adoption

**Status:** absorbed
**Captured:** 2026-04-17
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-007
**Reason:** DEC-007 (Skills adoption scope, approved 2026-04-17 Option B — reference-only adoption) resolved the user's blocking concern. Research finding: Skills inject into the caller's message stream (shared context), so orchestration/verify flows cannot live in Skills, but subagents spawned from within a Skill still get fresh context. DEC-004 isolation is preserved. Template will adopt Skills only for on-demand reference content; orchestration and verify flows stay in commands and subagents. Also resolves FB-033's Skill-vs-subagent sub-question: spec-auditor must be a subagent.

**Assessed:** 2026-04-17 — Affects potentially new `.claude/skills/` dir, `.claude/CLAUDE.md`, `.claude/rules/agents.md`, commands, and subagent/skill context-window architecture. Scope: exploratory. Research-first: must resolve subagent-vs-skill context-window semantics (user's primary concern — would affect DEC-004 guarantees) plus distribution/override semantics and permissions inheritance before any migration. FB-033 depends on this outcome (subagent vs skill for spec-auditor). Route: Phase 3 research (candidate DEC-007). Do not begin any implementation.

Source: Claude Code best-practices doc (fetched 2026-04-17) — presents Skills as the on-demand alternative to CLAUDE.md for "domain knowledge or workflows that are only relevant sometimes." User flagged adoption as research-first, not implementation. Primary concern: subagent context-window behavior when spawned from a Skill.

## FB-026: Reevaluate permissions story given auto-mode maturity

**Status:** absorbed
**Captured:** 2026-04-17
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-008
**Reason:** DEC-008 (auto-mode reevaluation, approved 2026-04-17 Option D — narrow to 8 entries + document auto mode) resolved the inflection question. Research finding: `permissions.allow` rules short-circuit the auto-mode classifier — the shipped allowlist is not dead code (saves latency, covers dontAsk/CI, supports hooks). Full reversal would break hooks and non-Opus-4.7 users. Option D narrows the shipped list from 15 to 8 essential entries and adds auto-mode documentation. The layered two-file model from DEC-005 stays intact. Unblocks FB-037.

**Assessed:** 2026-04-17 — Affects `.claude/settings.json`, `.claude/sync-manifest.json`, `.claude/commands/health-check.md` Part 5c, `.claude/CLAUDE.md` Critical Invariants, `system-overview.md`, `.claude/README.md` Settings section. Scope: corrective — may reverse portions of DEC-005. Inflection-point candidate DEC-008. Blocks FB-037 (hook recipe shape depends on outcome). Research can start immediately — no upstream dependencies. Route: Phase 3 research (candidate DEC-008).

Source: Claude Code best-practices doc (fetched 2026-04-17) mentioned auto mode (`--permission-mode auto`) as alternative to explicit allowlists. Auto mode became available on Max plan ~2026-04-13, post-dating DEC-005's assumptions. User flagged the potential inflection: if auto mode covers most of the base allowlist at runtime, the shipped file may be unnecessary complexity.

## FB-003: Template's subdirectory layout causes Turbopack CSS resolution failure in Next.js 16

**Status:** promoted
**Captured:** 2026-04-02
**Promoted:** 2026-04-02 — Incorporated into template: `.claude/support/reference/known-issues.md` (KI-001), `commands/work.md` § Step 0 Preamble + Step 4 Safety Gate

Template ships contextual advisory about Turbopack/subdirectory bug, surfaced via `/work` hazard check when dev servers are relevant. Subdirectory vs. flat layout research deferred to a separate decision record.

## FB-005: Template files changed — system-overview.md needs updating

**Status:** promoted
**Captured:** 2026-04-02
**Promoted:** 2026-04-02 — Incorporated into `system-overview.md` § Instruction Architecture (rules inventory) and § Proactive Context Transitions (authoritative files)

Updated system-overview.md to reflect session-management.md and Session Management section in CLAUDE.md.

## FB-007: Handoff, plan, and memory overlap — streamline into a coherent workflow

**Status:** promoted
**Captured:** 2026-04-02
**Promoted:** 2026-04-02 — Incorporated into `system-overview.md` § Three Persistence Mechanisms, `commands/work.md` § Step 0a2, `rules/session-management.md` § Which Persistence Mechanism When

Three-lane model (handoff/plan/memory) with clear decision table, explore→plan→execute named workflow, and `/work` Step 0 plan file auto-discovery.

## FB-008: /work fails to restore context at session boundaries

**Status:** promoted
**Captured:** 2026-04-02
**Promoted:** 2026-04-02 — Incorporated into `system-overview.md` § Dangerous Operations Require Safety Checks, `commands/work.md` § Step 0 Preamble + Step 4 Safety Gate

New design principle: never auto-execute flagged-dangerous operations. `/work` Step 0 consults auto-memory and known-issues before execution, Step 4 gates dangerous processes behind user confirmation.

## FB-014: Dashboard Mermaid diagrams are unreadable at scale — need diagram rules overhaul

**Status:** promoted
**Captured:** 2026-04-10
**Refined:** 2026-04-14 — Reframe the dashboard diagram's purpose from "project overview" to "orientation snapshot": show where the user is now and what's next in line, with dependency detail on upcoming tasks. It does not need uniformly-sized boxes for every task or phase. The current approach works up to ~10 tasks and breaks beyond that. Mermaid is preferred but not mandatory. Scope: diagram-generation rules in `dashboard-regeneration.md` and `rules/dashboard.md`. Large-project rendering should zoom in on the active frontier rather than fitting the whole project on one canvas.
**Assessed:** 2026-04-14 — Primary rewrite target: `dashboard-regeneration.md` § "Project Overview Diagram" — remove `graph LR` as hard rule, drop the ">15 nodes" critical-path-only threshold, revisit the 4-task render threshold, switch labeling model to frontier-vs-context, and shift scaling from "fit everything" to "show the frontier". Direct template edit — no decision record needed.
**Promoted:** 2026-04-14 — Incorporated into `system-overview.md` § Communication: Dashboard and CLI-Direct → "Dashboard visualization features" (Orientation diagram bullet). Follow-up work targets `dashboard-regeneration.md` § "Project Overview Diagram" and `rules/dashboard.md` § Scaling.

## FB-016: Feedback review should persist review notes for /iterate handoff

**Status:** promoted
**Captured:** 2026-04-13
**Refined:** 2026-04-14 — Phase 2 refinement Q&A and Phase 3 impact assessment Q&A both generate context (scoping decisions, motivation, priority signals, "explicitly not X" boundaries) that is lost after the one-line `**Refined:**` / `**Assessed:**` summaries. Add a `**Review notes:**` section captured at both trigger points (end of Phase 2 refinement, and on `[Y] Approve` in Phase 3). The command must explicitly prompt the user for review notes — do not auto-generate from the conversation (fabrication risk). Prefer noisier UX over silent drift. Scope: `commands/feedback.md` Phase 2 and Phase 3 flow.
**Assessed:** 2026-04-14 — Isolated to `commands/feedback.md`. `commands/iterate.md` already reads ready items — no logic change, just benefits from richer source. Dependency: FB-018 also edits Phase 2 flow — bundle implementation. Review notes apply after `[R] Refine` Q&A only, not after `[P] Promote`.
**Promoted:** 2026-04-14 — Incorporated into `system-overview.md` § Feature Catalog → Feedback System (Review notes persistence). Follow-up work targets `commands/feedback.md` Phase 2 Refine flow and Phase 3 Approve flow.

## FB-018: /feedback review Phase 2 options need clarification and a "proceed without refining" path

**Status:** promoted
**Captured:** 2026-04-14
**Refined:** 2026-04-14 — Two UX gaps: (1) inline option prompts like `[R] / [C] / [N] / [S]` need a short one-line gloss on every letter; a single legend printed once is not enough — the gloss must ride with every prompt. (2) Add `[P] Promote — mark refined using current text` in Phase 2 that skips Q&A refinement and sets status to `refined` using the capture text. Phase 2 only — Phase 3 keeps its `[Y] Approve` gate. Scope: `commands/feedback.md` Phase 2 prompts and option handling.
**Assessed:** 2026-04-14 — Isolated to `commands/feedback.md`: add glosses everywhere option menus appear and add a `[P] Promote` action handler. Dependency: FB-016 (Review notes) — bundle implementation since both edit Phase 2; Review notes apply after `[R] Refine` Q&A only, not after `[P] Promote`.
**Promoted:** 2026-04-14 — Incorporated into `system-overview.md` § Feature Catalog → Feedback System (Promote path). Follow-up work targets `commands/feedback.md` Phase 2 prompts (glosses on every option menu) and the new `[P] Promote` action handler.

## FB-040: Build cross-project feedback pipeline — DEC-001 Option D bridge

**Status:** promoted
**Captured:** 2026-05-12
**Refined:** 2026-05-12 — Initial framing claimed DEC-001 (Option C: Hybrid Pipeline) was approved-but-never-implemented. Closer reading on 2026-05-13 corrected the picture: Option C is in fact fully documented end-to-end across `implement-agent.md`, `verify-agent.md`, `work.md`, `pre-compact-handoff.sh`, and `health-check.md` Part 7. The friction the user actually described — running `/feedback` in a downstream project, the FB entry landing locally, and manually carrying it back to `template-maintenance/feedback.md` — is **Option D from DEC-001 research** ("Lightweight Feedback Bridge"), which was discussed but not selected at the time. This entry was rescoped to ship Option D as a complement to Option C (not a replacement). Option C's end-to-end execution remains untested separately — see FB-041.
**Assessed:** 2026-05-12 — Scope: additive. Affected files: `.claude/commands/feedback.md` (new `template:` prefix in Mode 1 + Template Bridge Export section), `.claude/commands/health-check.md` Part 7 (dispatch by `kind` field + path fix from `.claude/support/feedback/feedback.md` to `template-maintenance/feedback.md`), `.claude/version.json` (version bump 3.0.0 → 3.1.0; notes string updated), `interaction-logs/README.md` (documents the two export shapes). No agent changes, no hook changes — bridge runs entirely in orchestrator context on the downstream side and `/health-check` on the template side.
**Promoted:** 2026-05-13 — Incorporated into `.claude/commands/feedback.md` (Mode 1 `template:` prefix + new Template Bridge Export section), `.claude/commands/health-check.md` Part 7 (dispatch by `kind` field, user-feedback routing path 3c, path fix to `template-maintenance/feedback.md` in step 6), `.claude/commands/health-check.md` Part 5d (NEW — cross-project bridge configuration check for downstream projects, surfaces unset/broken `template_inbox_path`), `.claude/commands/work.md` `/work complete` Step 3c (REWRITTEN — dual-prompt with plain-English labels: "Project notes" always + "Template notes" when bridge configured), `interaction-logs/README.md` (two-shape documentation), `.claude/version.json` (3.1.0).

Bridge contract: `/feedback template: [text]` writes the FB-NNN locally as today AND writes a `{"kind": "user_feedback", ...}` export to the template repo's `interaction-logs/inbox/` (via `template_inbox_path`). `/health-check` Part 7 in the template repo dispatches by `kind`: user-feedback exports route into `template-maintenance/feedback.md` with user confirmation; session exports continue through the existing aggregation logic. Bridge silently no-ops when `template_inbox_path` is unset — capture remains local-only.

Two follow-on additions surfaced during the same session and shipped together:
- **`/health-check` Part 5d** closes the discoverability gap for `template_inbox_path` — the slot ships empty, and previously no command prompted the user to set it. Part 5d runs in downstream projects only, prompts on unset, validates set paths, and offers `[F] Fix | [C] Clear | [S] Skip` when the configured path is invalid.
- **`/work complete` Step 3c rewrite** addresses a UX friction the user described: when Claude asked "any notes on how this went?" after a task, it was unclear whether to type project-relevant or template-relevant feedback, and template-relevant input got buried in `task.user_feedback` requiring manual carry-back. The rewrite splits the single ambiguous prompt into two clearly-labeled prompts — "Project notes" (always shown, stores in `task.user_feedback`) and "Template notes" (only shown when `template_inbox_path` is configured, invokes `/feedback template:` Mode 1 with the source task context prepended to the body). Plain English in both prompts — no template-internal jargon (`spec drift`, `friction signal`, `scope creep`) in user-facing text. The template prompt is conditional specifically to avoid creating local-only FB entries that would re-create the same manual-carry-back friction the bridge was built to eliminate.

Option C (implicit-signal pipeline) is unaffected and remains a separate question tracked in FB-041.

## FB-017: /work Step 2b doesn't detect checked decision checkboxes or finalize decisions

**Status:** promoted
**Captured:** 2026-04-13
**Refined:** 2026-04-14 — Decision auto-finalization (checkbox → `status: approved` + frontmatter + Decision/Rationale + unblock dependents) is documented in three places but the caller (`/work` Step 2b) doesn't reliably execute it. Confirmed in styler (2026-04-13): DEC-039, DEC-040, DEC-026-revision all stayed `proposed` after boxes were checked. Root cause is likely *both* a documentation problem (Step 2b underspecifies and points to a referenced procedure rather than inlining it) and an LLM reliability problem (procedure skipped under load). Fix should address both: tighten/inline the Step 2b procedure, and consider extracting detection into a deterministic script (connects to FB-011). `/iterate` should also run the same detection so the finalization path is tolerant at both entry points. Scope: `commands/work.md` Step 2b, `commands/iterate.md`, `phase-decision-gates.md`.
**Assessed:** 2026-04-14 — Primary rewrite: `commands/work.md` Step 2b (line 330) — inline the core checkbox-detection steps so the caller is unambiguously responsible; keep `phase-decision-gates.md` (lines 62-96) as edge-case reference, possibly restructured into "caller checklist" vs "full procedure". Add detection entry step to `commands/iterate.md`. Audit `decisions.md` line 151 and `workflow.md` lines 195-201 (the docs promising auto-finalization). Scope: corrective. Dependencies: FB-011 (script extraction is a strong candidate for the reliability leg of the root cause) and FB-010 (if Step 2b ran in a subagent, script invocation could hit sandbox issues — argues for keeping it in the orchestrator). Direct template edit for the doc/inline fix; script extraction follows under FB-011.
**Promoted:** 2026-04-17 — Inlined checkbox-detection trigger in `.claude/commands/work.md` Step 2b (lines 345-359); mirrored in `.claude/commands/iterate.md`. Commits `3549f59` + `1508579`.

Decision documents have a "## Select an Option" section with checkboxes (`- [ ] Option A`, `- [x] Option B`). The user selects an option by checking a box. The documentation explicitly promises auto-finalization:

- `decisions.md` line 151: "Check your selection — `/work` auto-updates status to `approved` and sets the `decided` date"
- `workflow.md` lines 195-201: "User selects option via checkbox → `/work` auto-updates status to `approved` → dependent tasks unblock"
- `phase-decision-gates.md` lines 62-96: Full algorithm specified — checkbox normalization (`[x]`, `[X]`, `[✓]`, `[✔]`), frontmatter update procedure, option name extraction

But when `/work` actually runs, Step 2b doesn't execute this detection. The frontmatter stays at `status: proposed`, `decided` date stays empty, and the Decision/Trade-offs/Impact sections remain blank. Dependent tasks stay blocked.

**Observed in styler project (2026-04-13):** User checked boxes in DEC-039, DEC-040, and DEC-026-revision. All three remained `status: proposed` with empty Decision sections. The user only discovered this when running `/iterate` and asking why the decisions hadn't been picked up.

**Root cause:** `/work` Step 2b references `phase-decision-gates.md` but doesn't reliably execute the checkbox detection and frontmatter update algorithm it specifies. The procedure document is complete and correct — the caller doesn't follow through.

**What needs fixing:**
1. `/work` Step 2b must actually scan each `proposed` decision file's markdown content for checked boxes in the "## Select an Option" section
2. When a checked box is found: update frontmatter (`status: approved`, `decided: YYYY-MM-DD`), extract the selected option name, and populate the Decision section (Selected + Rationale from the research)
3. After updating, check if the decision is an inflection point — if so, flag for `/iterate`
4. Consider whether `/iterate` should also run this detection (it already checks for unresolved inflection points but not for unchecked→checked transitions)

---

## FB-015: Action Required section cluttered by work summaries — separate actionable from informational

**Status:** promoted
**Captured:** 2026-04-12
**Refined:** 2026-04-14 — Keep Action Required strictly actionable — only items needing user input, with just enough context to act. Do not create a Recent Activity section: work summaries should be removed from the dashboard entirely, since git log and task JSON already preserve history. If any summary content remains anywhere, prune by age (drop anything older than the last session). Scope: `rules/dashboard.md` and `dashboard-regeneration.md` — tighten the definition of what belongs in Action Required and remove guidance that lets summaries accumulate there.
**Assessed:** 2026-04-14 — Primary edit: `dashboard-regeneration.md` § "Action Item Contract" (lines 322-329) needs a negative rule ("must NOT include work summaries, completion reports, or recent-activity recaps"). Secondary: `rules/dashboard.md` § Sections (confirm no Recent Activity section), `commands/work.md` (any post-completion dashboard emission paths), `commands/health-check.md` Part 6 check #4 (extend to detect summary-shaped content if feasible). Existing Action Item Contract is ~80% aligned already — this formalizes the "what NOT to include" side. Dependencies: FB-014 (frontier philosophy), FB-011 (deterministic generator would make this enforceable by construction). Scope: corrective. Direct template edit — no decision record needed.
**Promoted:** 2026-04-17 — Incorporated into `.claude/support/reference/dashboard-regeneration.md` § Action Item Contract (line 333) — negative rule "must NOT include work summaries, completion reports, or recent-activity recaps" landed. Commits `5e570aa` (primary rule) + `3549f59` (work.md audit).

The dashboard's "Action Required" section sometimes includes summaries of recently completed work alongside the actual items needing user input. This clutters the section and slows down the user's ability to identify what they need to do and give feedback.

Proposed changes:
1. Keep "Action Required" tight — only items that require user action, with just enough context to understand what's needed.
2. Move work summaries and completion reports to a separate section further down the dashboard (e.g., "Recent Activity" or "Work Summary").
3. Establish clear rules for how Claude writes these summaries so they stay useful without becoming an ever-growing pile of information as phases and tasks get finished. Need rules for what gets included, how much detail, and when old summaries get pruned or collapsed.

## FB-019: Adopt `@path` imports in `.claude/CLAUDE.md` for rules files

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/CLAUDE.md` (Workflow Rules section). Scope: corrective. Makes existing rules-file loading declarative via `@path` imports instead of prose references. No cross-item overlap. Route: Phase 4 direct.
**Promoted:** 2026-04-17 — `@path` imports for all rules files landed in `.claude/CLAUDE.md` Workflow Rules section. Commit `dc108d4`.

Source: Claude Code best-practices doc (fetched 2026-04-17) — CLAUDE.md supports `@path/to/import` syntax; imports are auto-loaded by the harness.

The template's `.claude/CLAUDE.md` currently lists rules files in a "Workflow Rules" prose section but does not import them explicitly — they happen to be loaded by other mechanisms. Switch to explicit `@.claude/rules/task-management.md`, `@.claude/rules/spec-workflow.md`, etc., making the dependency declarative.

**Impact scope:** `.claude/CLAUDE.md` (one section). Possibly `.claude/rules/*.md` if reorganized.

**Why:** Makes context loading explicit and predictable; aligns the template with the documented harness feature; surfaces accidental-load behavior. Low risk if rules are already short.

## FB-021: Use AskUserQuestion-driven interview in `/iterate distill`

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/commands/iterate.md` (distill subcommand). Scope: additive. Complements FB-032 (decisions surfacing in `/iterate` propose): FB-021 surfaces decisions *before* writing, FB-032 forces them to surface *in* the proposal — the two together cover both directions of the silent-decisions failure mode. Route: Phase 4 direct.
**Promoted:** 2026-04-17 — `AskUserQuestion`-driven structured-distillation interview added to `.claude/commands/iterate.md` distill (lines 89-91). Commit `1508579`.

Source: Claude Code best-practices doc (fetched 2026-04-17) — recommends interviewing the user via the `AskUserQuestion` tool before writing a spec, to surface implementation, UX, edge-case, and tradeoff questions they haven't considered.

The template's `/iterate distill` already extracts a spec from a vision doc but doesn't explicitly use `AskUserQuestion`. Adopt the structured-question pattern so distillation surfaces hard-to-see decisions rather than silently assuming.

**Impact scope:** `.claude/commands/iterate.md` (distill subcommand section).

**Why:** Direct mapping; vision-doc-to-spec is exactly the use case the doc describes. Improves spec quality at the most important leverage point in the whole workflow.

## FB-022: Add "address root causes, not symptoms" rule to implement-agent

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/rules/agents.md` and/or `.claude/agents/implement-agent.md`; optionally a matching check in `.claude/agents/verify-agent.md` per-task return schema so verify-agent has unambiguous grounds to reject symptom-only fixes. Scope: additive. Aligns with the template's verification-first design. Route: Phase 4 direct.
**Promoted:** 2026-04-17 — "Root Cause Over Symptom" rule added to `.claude/rules/agents.md` with explicit verify-agent rejection criteria. Commit `1f825ab`.

Source: Claude Code best-practices doc (fetched 2026-04-17) — verification table entry: *"the build fails with this error: [paste]. fix it and verify the build succeeds. address the root cause, don't suppress the error."*

implement-agent does not currently codify this principle. Add a short explicit rule (in agent prompt or `.claude/rules/agents.md`) so verify-agent has unambiguous grounds to reject symptom-only fixes: try/except swallows, suppressed warnings, magic-number overrides, silenced failing tests, skipped assertions.

**Impact scope:** `.claude/agents/implement-agent.md` and/or `.claude/rules/agents.md`. Possibly a matching check in verify-agent's per-task return schema.

**Why:** Aligns with the template's verification-first design. Currently implicit; making it explicit gives verify-agent a clear, citable check.

## FB-023: Document `/btw` for side questions in session-management

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/rules/session-management.md` (Managing Context Pressure bullet). Scope: additive. Bundle with FB-024 and FB-025 (same file, three session-management tool additions). Route: Phase 4 direct.
**Promoted:** 2026-04-17 — `/btw {question}` documented in `.claude/rules/session-management.md` Managing Context Pressure section (line 49). Commit `212056d`.

Source: Claude Code best-practices doc (fetched 2026-04-17) — `/btw` answers appear in a dismissible overlay and never enter conversation history.

Template's `.claude/rules/session-management.md` already documents `/clear` and `/compact` for managing context pressure. Add `/btw` as a third tool for "quick question that shouldn't bloat context."

**Impact scope:** `.claude/rules/session-management.md` (one bullet in Managing Context Pressure section).

**Why:** Direct context-discipline tool that complements existing guidance. Minimal addition, real leverage for long sessions.

## FB-024: Document `/rewind` and Esc+Esc checkpoint flow in session-management

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/rules/session-management.md` (new short section, likely after "What Survives What" table). Scope: additive. Bundle with FB-023 and FB-025 (same file). Route: Phase 4 direct.
**Promoted:** 2026-04-17 — `/rewind` + `Esc+Esc` documented in `.claude/rules/session-management.md` § Checkpointing and Rewind (lines 93-98). Commit `212056d`.

Source: Claude Code best-practices doc (fetched 2026-04-17) — every Claude action creates a checkpoint; `Esc+Esc` or `/rewind` opens the menu; can restore conversation only, code only, or both; persists across sessions.

Template's `session-management.md` doesn't mention checkpointing at all — it focuses on `/work pause` and handoff files. Add a short section noting checkpointing as a complementary recovery mechanism (for recovering from agent missteps without needing `/work pause` or a fresh session).

**Impact scope:** `.claude/rules/session-management.md` (new short section, likely after "What Survives What" table).

**Why:** Important user-facing feature currently undocumented in the template's session guidance.

## FB-025: Document `/rename` for naming sessions

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/rules/session-management.md` (resume-methods section, one-liner). Scope: additive. Bundle with FB-023 and FB-024 (same file). Route: Phase 4 direct.
**Promoted:** 2026-04-17 — `/rename` documented in `.claude/rules/session-management.md` resume-methods note (line 27). Commit `212056d`.

Source: Claude Code best-practices doc (fetched 2026-04-17) — `/rename` gives sessions descriptive names (e.g., `oauth-migration`, `debugging-memory-leak`) so they're findable via `claude --resume`.

Template's resume-methods table in `session-management.md` doesn't mention this. Add a one-liner.

**Impact scope:** `.claude/rules/session-management.md` (one row in resume-methods table or a one-liner under "Resuming Sessions").

**Why:** Useful when running this template across multiple long-running projects. Pure documentation, no behavior change.


## FB-027: Skip-planning guidance for trivial tasks

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/commands/research.md` or `.claude/rules/decisions.md` (callout), possibly `.claude/commands/work.md` Step 3 routing. Scope: additive. Single-callout fix; aligns with existing "no premature abstraction" ethos. Route: Phase 4 direct.
**Promoted:** 2026-04-17 — Skip-planning guidance for trivial tasks added in `.claude/commands/work.md` (hot-file batch). Commit `3549f59`.

Source: Claude Code best-practices doc (fetched 2026-04-17): *"For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly... If you could describe the diff in one sentence, skip the plan."*

Template's `/research` and decomposition flow don't currently distinguish trivial from non-trivial tasks. Add an explicit callout: skip formal planning when the diff can be described in one sentence. Prevents overhead for small fixes and aligns with the "no premature abstraction" ethos already in CLAUDE.md.

**Impact scope:** `.claude/commands/research.md` (callout) or `.claude/rules/decisions.md`; possibly `.claude/commands/work.md` Step 3 routing.

## FB-028: Add CLI-tool installation hints to setup-checklist

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/support/reference/setup-checklist.md` (CLI installs subsection). Scope: additive. Shares file with FB-037 (different subsection: FB-028 = CLI installs, FB-037 = Optional Hooks appendix) — not a conflict; file gains two independent additions. Route: Phase 4 direct.
**Promoted:** 2026-04-17 — CLI-tool installation hints added to `.claude/support/reference/setup-checklist.md` (gh / aws / gcloud / etc.). Commit `818db30`.

Source: Claude Code best-practices doc (fetched 2026-04-17) — recommends installing `gh`, `aws`, `gcloud`, `sentry-cli` etc. for context-efficient external interactions, noting unauthenticated API calls often hit rate limits.

Template's `.claude/support/reference/setup-checklist.md` could detect which CLIs are present and suggest installs based on spec content (e.g., spec mentions GitHub PRs → suggest `gh`).

**Impact scope:** `.claude/support/reference/setup-checklist.md`.

**Why:** Aligns with the template's setup-time validation pattern. Low-cost addition.

## FB-029: Document non-interactive mode (`claude -p`) as automation primitive

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects new `.claude/support/reference/automation.md` or section in `.claude/README.md`. Scope: additive. Bundle with FB-030 (same target file; FB-030 uses `claude -p` as its primitive and belongs as a pattern section in the same doc). Connects to FB-011 — some FB-011 script candidates may be better expressed as `claude -p` one-liners than bash scripts, so sequence FB-029/030 before FB-011 implementation. Route: Phase 4 direct.
**Promoted:** 2026-04-17 — `claude -p` non-interactive mode documented in new `.claude/support/reference/automation.md`. Commit `75daf81` (bundled with FB-030).

Source: Claude Code best-practices doc (fetched 2026-04-17) — `claude -p "prompt"` runs without a session; with `--output-format json`/`stream-json` and `--allowedTools`, it's the building block for CI, pre-commit hooks, scripts, and fan-out patterns.

Worth a short reference for users automating template workflows (e.g., nightly `/health-check`, batch report generation, scheduled dashboard refresh).

**Impact scope:** New `.claude/support/reference/automation.md` or section in `.claude/README.md`.

**Why:** Connects directly to FB-011 (scripts as alternative) and may influence FB-011's scope — some "scripts" candidates might be better expressed as `claude -p` one-liners than as bash scripts.

## FB-030: Document fan-out pattern for batch task execution

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/support/reference/automation.md` (shared with FB-029; new file) and/or addendum to `.claude/support/reference/parallel-execution.md`. Scope: additive. Bundle with FB-029 (depends on `claude -p` primitive). Route: Phase 4 direct.
**Promoted:** 2026-04-17 — Fan-out pattern documented in `.claude/support/reference/automation.md`. Commit `75daf81` (bundled with FB-029).

Source: Claude Code best-practices doc (fetched 2026-04-17) — `for file in $(...); do claude -p "Migrate $file..." --allowedTools "Edit,Bash(git commit *)"; done` pattern for large migrations.

Template's parallel execution is intra-session (multiple `Task` agents coordinated by one `/work` orchestrator); fan-out is inter-session (many independent `claude` processes). The two scaling axes are complementary. Document the fan-out pattern so users know it exists for very large workloads (e.g., migrating hundreds of files).

**Impact scope:** New section in an automation doc (depends on FB-029) or addendum to `parallel-execution.md`.

**Why:** Different scaling axis from current parallel model. Worth flagging even if template does not itself implement fan-out — users may discover and adopt it themselves.

## FB-031: Document Writer/Reviewer parallel-session pattern

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/README.md` or `.claude/rules/agents.md` (short mention). Scope: additive. Reinforces existing implement-agent/verify-agent separation-of-concerns design — no behavioral change, just making an external scaling axis visible. Route: Phase 4 direct.
**Promoted:** 2026-04-17 — Writer/Reviewer parallel-session pattern added to `.claude/rules/agents.md` (line 10). Commit `1f825ab`.

Source: Claude Code best-practices doc (fetched 2026-04-17) — running parallel Claude sessions for quality: Session A writes, Session B reviews with fresh context, avoiding bias toward code it just wrote.

Template already enforces this via the implement-agent / verify-agent split within one session, but users can go further by running two separate `claude` instances (e.g., one implementing a feature, another doing a deeper security or architectural review of the finished code).

**Impact scope:** `.claude/README.md` or `.claude/rules/agents.md`.

**Why:** Reinforces the template's existing separation-of-concerns design. Small mention, no behavioral change.

## FB-032: Require explicit "Decisions in This Proposal" section in `/iterate` output

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/commands/iterate.md` (propose subcommand output contract), `.claude/rules/spec-workflow.md` (propose-approve-apply), possibly `.claude/agents/verify-agent.md` matching check for spec-change tasks. Scope: additive. Complements FB-021 (before-proposal interview surfaces decisions; FB-032 forces them into the proposal itself). Under Opus 4.7 instruction-following, the structural contract should land more reliably than the report's Opus 4.6 window. Trial of this contract gates FB-033 (spec-auditor research). Route: Phase 4 direct — implement early to generate the trial data FB-033 needs.
**Promoted:** 2026-04-17 — "## Decisions in This Proposal" output contract added to `.claude/commands/iterate.md` (lines 260-273) and `.claude/rules/spec-workflow.md` (line 13). Commit `1508579`.

Source: Claude Code usage insights report (fetched 2026-04-17) — the report's #1 friction, with a concrete data point: *"You had to ask 'did you make any silent decisions' twice in one session to surface unapproved design choices in a spec proposal."* The report's fun-ending calls this out across 5+ sessions.

Convert reactive vigilance into a structural output contract. Every `/iterate` spec-change proposal must end with a `## Decisions in This Proposal` section listing each non-trivial choice tagged `[NEEDS APPROVAL]`, `[FROM EXISTING SPEC]`, or `[USER REQUESTED]`. `/iterate` does not proceed to apply until each `[NEEDS APPROVAL]` item is resolved.

Complements FB-021 (AskUserQuestion-driven interview in `/iterate distill`) — FB-021 surfaces decisions *before* proposing; FB-032 forces them to surface *in* the proposal. Under Opus 4.7's stronger instruction-following, the structural contract should land more reliably than during the report's Opus 4.6 window.

**Impact scope:** `.claude/commands/iterate.md` (propose subcommand output contract), `.claude/rules/spec-workflow.md` (propose-approve-apply section), possibly a matching check in `.claude/agents/verify-agent.md` for spec-change tasks.

**Why:** Converts recurring reactive friction into a structural guarantee. Small contract change with high leverage on the report's #1 pattern.

## FB-034: "Respect user kills" — don't restart long-running processes without renewed approval

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/CLAUDE.md` (Critical Invariants — template-owned, ships to projects), `.claude/rules/agents.md`, and/or `.claude/agents/implement-agent.md`. NOT root `./CLAUDE.md` (template-maintenance only). Scope: additive. Capture-time conflict (earlier broader framing vs root `CLAUDE.md`'s UI-testing guidance) already resolved via narrow restart-after-kill scope — no conflict remains. Related to FB-036 (both address over-eager execution, different trigger points). Auto mode does not absorb this (behavioral rule, not permission). Route: Phase 4 direct.
**Promoted:** 2026-04-17 — "Respect prior kills" rule added to `.claude/CLAUDE.md` Critical Invariants and `.claude/rules/agents.md` § Behavioral Rules. Commit `1f825ab`.

Source: Claude Code usage insights report (fetched 2026-04-17) — documented a 140GB-RAM Ghostty/Turbopack crash traced to Claude restarting dev servers after being told to kill them: *"Claude started dev servers despite explicit memory warnings and restarted them after you said to kill them, contributing to a 140GB RAM Ghostty crash."*

When the user kills a long-running process (dev server, watcher, batch loop, mass file processing, external-API scan), do not restart it in the same session without renewed approval. Confirm before re-initiating any process the user just halted.

Note: an earlier framing ("don't autonomously start long-running processes") was rejected during review because it conflicts with root `CLAUDE.md`'s own UI-testing guidance: *"For UI or frontend changes, start the dev server and use the feature in a browser before reporting the task as complete."* Starting dev servers for verification is a **feature**, not a bug. The narrower restart-after-kill rule avoids that conflict.

Auto mode does **not** absorb this — the classifier approves or denies individual tool calls but does not enforce "respect prior kills." Behavioral rule, not a permission.

**Impact scope:** `.claude/CLAUDE.md` (Critical Invariants — template-owned and ships to projects), `.claude/rules/agents.md`, and/or `.claude/agents/implement-agent.md`. Not root `./CLAUDE.md` (that file is template-maintenance-only and gets replaced on project setup).

**Why:** Domain-agnostic version of a concrete failure case (140GB crash). Complements DEC-005 (which stops unauthorized tool calls) by addressing authorized-but-destructive sequences. Small doc addition, zero implementation risk.

## FB-035: Implement-agent file-reading guidance for large files (prefer Grep/Glob; use Read `offset`/`limit`)

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/agents/implement-agent.md` (Tool Preferences section) or `.claude/rules/agents.md` § Tool Preferences. Scope: additive. Real quantified friction (61 file-too-large events, largest single tool-error category in the usage report). Single-paragraph fix, zero behavioral risk. Route: Phase 4 direct.
**Promoted:** 2026-04-17 — Large-file reading guidance (Grep/Glob preference + Read offset/limit + file-too-large recovery) added to `.claude/agents/implement-agent.md` Tool Preferences. Commit `1f825ab`.

Source: Claude Code usage insights report (fetched 2026-04-17) — "Tool Errors Encountered" chart flags **File Too Large (61 events)** as the single largest error category, larger than "Command Failed" (56) or "File Not Found" (19).

Current implement-agent Tool Preferences guidance says "use dedicated tools" but doesn't advise on large-file strategy. Add a short rule: prefer Grep/Glob for content lookup over reading whole files; when a file is known or suspected large, use Read with `offset`/`limit` rather than a full read.

**Impact scope:** `.claude/agents/implement-agent.md` (Tool Preferences section) or `.claude/rules/agents.md` § Tool Preferences.

**Why:** Real quantified friction (61 of the top tool errors — the largest single category). Single-paragraph fix, no behavioral risk.

## FB-036: "Confirm before dispatching parallel work" rule in implement-agent / `/work`

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/commands/work.md` Step 4 (parallel dispatch path) and `.claude/support/reference/parallel-execution.md`. Scope: additive. Related to FB-034 (shared over-eager-execution theme; proactive vs reactive). Independent of FB-026 outcome — if auto mode removes permission-prompt checkpoints, pre-dispatch summary becomes *more* valuable, not less. Route: Phase 4 direct.
**Promoted:** 2026-04-17 — Pre-dispatch confirmation rule for batches ≥ 3 added to `.claude/commands/work.md` Step 4 (line 590) and `.claude/support/reference/parallel-execution.md`. Commit `3549f59`.

Source: Claude Code usage insights report (fetched 2026-04-17) — *"You interrupted background bash and parallel agent dispatches multiple times across /onboard and /work sessions because Claude moved faster than your validation step."*

Current `/work` decomposition can dispatch multiple parallel implement-agents without an explicit pre-dispatch confirmation step. Add: when a batch spawns more than N parallel agents (N configurable; default 3), summarize the dispatch plan (which tasks, which files affected, verify strategy) and await user confirmation before spawning.

Related to FB-034 (respect user kills): both address over-eager execution. FB-034 is reactive (after a kill); FB-036 is proactive (before a dispatch).

Note on auto mode: auto mode may actually *worsen* this friction by removing the natural permission-prompt pause points that currently force a checkpoint. A pre-dispatch summary restores a cheap human checkpoint independent of the permissions layer.

**Impact scope:** `.claude/commands/work.md` Step 4 (parallel dispatch path), `.claude/support/reference/parallel-execution.md`.

**Why:** Preserves the productivity of parallel dispatch while adding a cheap human checkpoint. Small behavioral change at one site.

## FB-037: Optional PreToolUse hook example for dev-server guarding in `setup-checklist.md` (defer until FB-026 resolves)

**Status:** promoted
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/support/reference/setup-checklist.md` (new "Optional Hooks" subsection/appendix). Scope: additive. **Unblocked 2026-04-17 by DEC-008 (Option D approved)** — layered two-file model from DEC-005 stays intact; hook recipe references `.claude/settings.local.json` under the `hooks` key. Shares file with FB-028 (different subsection). Route: Phase 4 direct — ready now.
**Promoted:** 2026-04-17 — Optional Hooks recipe (PreToolUse dev-server guard) added to `.claude/support/reference/setup-checklist.md` § Optional Hooks (line 79). Commit `96bf1d2`.

Source: Claude Code usage insights report (fetched 2026-04-17) — report recommends a PreToolUse hook blocking `next dev` / `npm run dev` / `pnpm dev` unless explicitly approved. Complements FB-034 (universal behavioral rule) by providing a structural hook recipe for users who want hard blocks.

Per DEC-005, hooks belong in `settings.local.json` (user-owned) and the template does not ship hooks. But `.claude/support/reference/setup-checklist.md` can document an opt-in hook example for users running frontend projects.

**Dependency on FB-026 (candidate DEC-008 — auto-mode reevaluation):** The hook recipe's shape depends on whether DEC-008 keeps, simplifies, or retires the DEC-005 layered-settings model. If DEC-008 moves primary enforcement to auto mode's classifier, the hook recipe becomes a narrower "belt-and-braces" add-on for users who want hard blocks in addition to classifier approvals. **Defer full drafting until FB-026 resolves** — the recipe could be wasted work if the permissions story changes shape.

**Impact scope:** `.claude/support/reference/setup-checklist.md` (new "Optional Hooks" subsection or appendix).

**Why:** Opt-in advice for users who want structural dev-server protection. Keeps the domain-agnostic template clean while giving frontend users a working example to copy into their own `settings.local.json`.

## FB-041: Verify DEC-001 Option C executes end-to-end in real downstream sessions

**Status:** absorbed
**Captured:** 2026-05-13
**Absorbed:** 2026-05-13 — Combined into FB-057
**Absorbed Into:** FB-057
**Update 2026-05-13:** Cause 1 (unset `template_inbox_path`) is now surfaced by `/health-check` Part 5d in downstream projects — discoverability gap closed; the bridge is now opt-in via an explicit prompt rather than an empty slot. Investigation remains for cause 2 (orchestrator-side marker append in `work.md:543,559`) and cause 3 (`/work pause` Session Export step), both of which require empirical observation from real downstream sessions to diagnose.

DEC-001 Option C (Track 1 friction markers + Track 2 Claude retrospective + Phase 3 ingest pipeline) is documented end-to-end across:

- `.claude/agents/implement-agent.md:142-149,235-260` — `friction_markers[]` in return schema + taxonomy + emission guidance
- `.claude/agents/verify-agent.md:335,679-694` — same for verify-agent return schemas (per-task + phase-level)
- `.claude/commands/work.md:543,559` — orchestrator appends markers to `.claude/support/workspace/.session-log.jsonl`
- `.claude/commands/work.md:913-970` — `/work pause` Track 2 assessment + Session Export step
- `.claude/hooks/pre-compact-handoff.sh:138-208` — PreCompact bundles markers, copies to `template_inbox_path`
- `.claude/commands/health-check.md:695-735` — Part 7 ingest (now `kind`-dispatched per FB-040)

But `interaction-logs/inbox/` is empty as of 2026-05-13. Three possible causes (or a mix):

1. **No downstream project has set `template_inbox_path`** in its `.claude/version.json`. The slot ships empty by default, and no `/health-check` substep prompts the user to set it.
2. **The orchestrator-side "append marker to `.session-log.jsonl`" step (`work.md:543,559`) is documented but not reliably executed** by Claude during `/work` runs. FB-017-class doc-vs-execution gap.
3. **`/work pause` Track 2 + Session Export step is not reliably run.** Users may close sessions without running `/work pause`, or Claude may skip the export step under context pressure.

Investigation steps:

- Check if any downstream project has `template_inbox_path` set
- Run a `/work` session in a downstream project with markers expected to fire (e.g., a verification failure on first attempt) — inspect `.session-log.jsonl` afterwards to confirm the orchestrator appended
- Run `/work pause` in a downstream project, confirm `.session-export-YYYY-MM-DD.json` appears in workspace and is copied to the configured inbox

Outcomes:

- If cause 1: add a `/health-check` substep that surfaces unset `template_inbox_path` as a configuration gap (low effort, high value)
- If cause 2 or 3: extract the marker-append + export steps into a deterministic script (FB-011 Family D/E candidate) to remove the LLM reliability layer
- If all three contribute: combine fixes

Discovered while implementing FB-040 (Option D bridge). FB-040 shipped in `template_version 3.1.0`; this entry tracks the separate Option C execution question and does not block any current work.

## FB-045: Orchestrator should append friction markers eagerly, not at /work pause

**Status:** absorbed
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-005 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Absorbed:** 2026-05-13 — Combined into FB-057
**Absorbed Into:** FB-057

The "After implement-agent returns" protocol in /work command (Step 2) says: "Append friction markers: for each marker in report.friction_markers, add task_id and append as a JSON line to .claude/support/workspace/.session-log.jsonl".

Observation from a downstream styler project's Phase 20 work session: the orchestrator (Claude Code, executing /work in auto mode) skipped this step throughout the session — friction markers from agent reports were captured in task notes (task-XXX.json) but NOT appended to .session-log.jsonl in real-time. At /work pause time, the orchestrator caught up and batch-appended 8 markers from the session.

The risk: if the session terminates abruptly (compaction, crash, usage limit before pause is invoked), friction markers from that session are lost — only the task notes survive, and task notes aren't structured for cross-project Track 1 telemetry consumption.

Suggested template improvements (any of):

- **Document a clearer protocol** in /work or implement-agent.md — "Append marker via single bash call (`cat >> file <<JSON`) immediately after agent return; do not batch."
- **Make catchup idempotent** — if the orchestrator (or PreCompact hook) sees task notes with friction markers but no corresponding .session-log entry, append the missing markers automatically.
- **Move append responsibility into a hook** (PostAgentReturn or PostToolUse hook gated on Task subagent) so it can't be skipped by the orchestrator.

This is partly a behavioral nudge for the orchestrator — the "skip" was a judgment call to focus on user-facing communication, with the cost being post-hoc reconstruction at pause time. But making it harder to skip (Option 3, hooks) closes the gap structurally rather than relying on prompt discipline.

**Related:** FB-041 cause #2 (orchestrator-side marker append is documented but not reliably executed) — this is the same observation. FB-045's evidence informs FB-041's investigation.

## FB-047: Files_affected drift — decomposition should auto-enumerate ripple-affected fixture files

**Status:** absorbed
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-007 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler
**Absorbed:** 2026-05-13 — Combined into FB-058
**Absorbed Into:** FB-058

Across 12+ tasks in styler's Phase 20 alone, ~40% of friction markers cite some form of "files_affected was under-counted because the change rippled into a fixture / downstream caller / npm-test-chain entry that the task's declared scope didn't include." Implementations were correct in every case; the friction was purely scope-bookkeeping.

This is broader than FB-051 (path drift): FB-051 catches "task referenced a wrong path"; FB-047 catches "task referenced the right path, but missing collateral files."

**Concrete examples from one styler session (2026-04-27):**

- **T428** (retire `life_stage` registry field): files_affected = `[field-definitions.json]`. Reality: 2 test files hard-coded `life_stage` in fixtures — both had to be updated.
- **T435** (DEC-048 cap relax `.max(4)` → `.max(6)`): files_affected = 6 files. Reality: `loader.test.ts` had 2 fixtures (test 5 + test 10) hard-coded to a 5-bucket trip threshold — the cap change broke them and they had to be updated to 7-bucket fixtures. Friction marker logged.
- **T439** (derivation pipeline writeback): files_affected = `[derivation.ts, derivation.test.ts, onboard.md]`. Reality: also added `derivation-pipeline.ts` + `derivation-pipeline.test.ts` (new files) and edited `package.json` to chain the new test. 3 friction markers logged.
- **T460** (extend validator to list_builder item_fields): files_affected = `[schema-zod.ts, registry-consistency.test.ts]`. Reality: every downstream caller of `RegistrySchemaZ.parse()` broke — extended to 4 files. Mitigation was a centralized allowlist helper, but the file list was still under-counted.

**Proposed fix:** During `decomposition.md` (or its sub-procedure for setting `files_affected`), run a static-analysis pre-pass:

1. **For field/type retirements** ("remove `X`", "retire `X`"): `grep -r "X"` across `**/__tests__/**`, `**/*.test.{ts,py,js}`, fixture directories, and any path matching `*fixture*`/`*mock*`. Add matches to files_affected.
2. **For schema-cap or threshold changes** (e.g., `.max(N)` → `.max(M)`): `grep -r "{old_threshold_value}"` in fixture files; flag any matches that share the schema constant's name as candidates for files_affected.
3. **For new test files added under a `__tests__` or sibling-test convention:** check `package.json` `scripts.test` for chain-style invocation (`tsx ... && tsx ...`); if the chain is explicit-path-listing (vs glob-based), add `package.json` to files_affected automatically.
4. **For validator-walk extensions** (changes to a Zod / Pydantic / similar schema's superRefine or strict-parse logic): `grep -r "{ParserSchemaName}\.parse\\|\.{ParserSchemaName}\.safeParse"` to find downstream callers; add their files.

Implementation note: this is the same kind of pre-pass FB-051 proposes for path validation, just generalized to ripple-affected files. Could ship as a single decomposition-validation enhancement covering both.

## FB-051: Validate file paths during /work decomposition (originally styler FB-053)

**Status:** absorbed
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-011 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — originally captured locally as FB-053, lifted here because it's template-improvement (per styler's own dashboard note: "FB-053 is template-improvement, not Phase 20 scope").
**Absorbed:** 2026-05-13 — Combined into FB-058
**Absorbed Into:** FB-058

Decomposition step in `/work` should validate that file paths referenced in task descriptions and `files_affected` actually exist before the task is created.

**Concrete repro (styler T453 implementation, 2026-04-27):**

- `files_affected` listed `src/components/grooming/GroomingSection.tsx`
- Actual file lives at `src/components/style/GroomingSection.tsx`
- Implementer correctly grep'd and found the actual file; orchestrator updated metadata post-hoc (and the implementer wasted ~3 tool uses searching the wrong directory first)

**Proposed fix:** When decomposition references a path that doesn't resolve, flag it inline so the human reviewing decomposition output can correct it before tasks ship. Low-cost addition to the decomposition checklist (or `/health-check`); high-value preventing wasted implementer cycles searching wrong directories.

Could also catch related drift — task body mentioning a function name that no longer exists, etc. — but path validation alone covers the most common case.

**Relationship to FB-047:** FB-047 is broader ("ripple-affected fixture files missing from `files_affected`"); FB-051 is the narrower path-correctness check. They could ship as one decomposition-validation pre-pass enhancement covering both: (1) declared paths must resolve; (2) implied collateral paths (fixtures matching grep patterns) should be auto-suggested for inclusion.

## FB-039: validate-tasks.py and fingerprint.py read `data['task_id']` but schema field is `id`

**Status:** promoted
**Captured:** 2026-04-29
**Assessed:** 2026-05-13 — Affects `.claude/scripts/validate-tasks.py` (lines 14, 104, 127) and `.claude/scripts/fingerprint.py` (lines 49, 55, 73). Scope: corrective. Replace `task_id` with `id` to match `task-schema.md` and the existing task corpus; audit `tests/` fixtures for any that mask the bug before shipping. Secondary: decide whether `fingerprint.py`'s 2-field rollup should match `dashboard-regeneration.md:253`'s 4-field `task_hash`, or document the divergence. Bug introduced in `d0c15e4`; failure mode is silent (false-positive schema errors + constant hash). Route: Phase 4 direct.
**Promoted:** 2026-05-13 — Fixed `task_id` → `id` field-read in `.claude/scripts/validate-tasks.py` (REQUIRED_FIELDS line 14; data.get call line 104) and `.claude/scripts/fingerprint.py` (line 55). Schema label key in debt output kept as `task_id` (label, not JSON-field). Smoke-tested via `validate-tasks.py` against the (empty) template repo `.claude/tasks/` — exits clean. Shipped in template_version 3.1.1.

The two FB-011 scripts shipped in v3.0.0 use the wrong key when reading task JSONs. They reference `task_id`, but the canonical schema and every existing task file use `id`. Surfaced by `/health-check` in the nordgrid-data-engineering project (27 tasks, all valid; both scripts mis-flagged or skipped them all).

**The mismatch:**

- `.claude/support/reference/task-schema.md:89` — required field is `id`: `| id | String | Number for top-level ("1"), underscore for subtasks ("1_1") |`. Examples on lines 6, 18 also use `"id": "1"`.
- All task JSONs in real projects use `id` (verified across nordgrid-data-engineering, and likely styler, siren, etc. — anything decomposed against the documented schema).
- `.claude/scripts/validate-tasks.py` lines 14, 104, 127 — references `task_id`. `REQUIRED_FIELDS` includes `"task_id"`, so the validator emits `missing required field: task_id` for every conformant task.
- `.claude/scripts/fingerprint.py` lines 49, 55, 73 — `hash_dashboard_rollup` does `entries.append(f"{data['task_id']}:{data['status']}")`. Hits a `KeyError`, prints a warning, skips the task — output is the SHA-256 of an empty string for any project using the documented schema.

**Effect:**

- `/health-check` Part 1 Check 1 (when delegated to the script) reports false-positive "missing required field" for every task. Manual verification has to step in to confirm the schema is actually fine.
- `/work` Step 1a / `/status` dashboard-freshness check: if it ever calls `fingerprint.py --dashboard-rollup`, it gets a constant hash regardless of task state — meaning content-staleness detection silently always-or-never fires.
- The bug is invisible in the template's own test suite if the suite uses fixtures with `task_id` (worth checking).

**Fix:** in both scripts, replace `task_id` with `id` to match the schema doc and existing task corpus.

- `validate-tasks.py:14` — `REQUIRED_FIELDS = {"id", "title", "description", "status", "difficulty", "owner", "dependencies", "files_affected"}`
- `validate-tasks.py:104, 127` — read `data["id"]` (and rename the dict key in the summary if you want, but the schema is the authority)
- `fingerprint.py:49, 55, 73` — same; update the docstring and `--help` text

Also worth a quick audit of any test fixtures in `tests/` that may have been written using `task_id` and would mask the bug.

**Secondary observation (not strictly part of this fix):** `fingerprint.py`'s `hash_dashboard_rollup` formula is `task_id:status` (2 fields), but `dashboard-regeneration.md:253` specifies the dashboard `task_hash` as `task_id:status:difficulty:owner` (4 fields). The script and the regen rule compute different hashes — reasonable if the script is intended for a separate purpose (per its docstring it mirrors `commands/status.md:36`), but worth confirming the two formulas aren't supposed to converge.

**Why it slipped through:** introduced in `d0c15e4` ("Phase 4: FB-011 Families A + B"). The failure mode is silent — `validate-tasks.py` exits 1 with structured errors that look like real schema violations, and `fingerprint.py` returns a real-looking hash (just always the same one). Neither crashes loudly enough to be obvious without comparing against actual task data.

Source: `/health-check` run in nordgrid-data-engineering, 2026-04-29.

## FB-052: implement-agent.md:223 grants subagent decision-record write that agents.md § State Ownership forbids

**Status:** promoted
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-012 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — multi-agent template audit, 2026-04-28. `agents/` files are byte-identical to template.
**Assessed:** 2026-05-13 — Affects `.claude/agents/implement-agent.md` (line 223 carve-out) and `.claude/rules/agents.md` § State Ownership (forbids subagent `.claude/` writes per harness sandbox + Anthropic issue #38806). Scope: corrective. Preferred fix (option a): rewrite implement-agent's decision-creation step to mirror `research-agent.md:181` — agent generates decision content, includes it in return report under a new field (e.g., `decisions_to_record`), orchestrator writes the file. Aligns all three agents and respects the documented sandbox. Route: Phase 4 direct.
**Promoted:** 2026-05-13 — Rewrote `.claude/agents/implement-agent.md` § 'Decisions Made During Implementation' to match research-agent's report-pattern: agent generates decision content in new `decisions_to_record` return-schema field, orchestrator writes the file. Added matching handler step (new step 3) in `.claude/commands/work.md` § 'After implement-agent returns'. Shipped in template_version 3.1.1.

`implement-agent.md:223` instructs the subagent to: *"Create a `decision-*.md` file in `.claude/support/decisions/` using that template (decision records live outside `.claude/tasks/`, so subagent writes there are permitted)."*

This contradicts `rules/agents.md § State Ownership`, which states subagents *"do not write to `.claude/` paths"* and cites this as *"a hard constraint of the Claude Code harness (subagents are sandboxed from `.claude/` writes per Anthropic issue #38806) and is not expected to change."* The path `.claude/support/decisions/` is under `.claude/`, so the carve-out in implement-agent.md describes a write the harness may not actually permit at runtime.

`agents.md § Tool Preferences` already states the canonical pattern: *"When an agent's documented workflow describes a state transition, it means 'include in return report'; the orchestrator performs the actual write."* And `research-agent.md:181` follows this correctly — it generates decision content, reports it, and lets the caller (`/research` or `/work`/`/iterate`) write the file.

Only `implement-agent.md` violates the pattern.

**Suggested fix (option a, preferred):** rewrite `implement-agent.md:219-225` to match research-agent's pattern — agent generates the decision content, includes it in the return report under a new field (e.g., `decisions_to_record`), orchestrator writes the file. Consistent with the rest of the template and respects the harness sandbox.

**Suggested fix (option b):** verify whether Anthropic issue #38806 still applies; if subagents now CAN write under `.claude/support/decisions/`, update `agents.md § State Ownership` to carve out the exception explicitly rather than burying it in implement-agent.md. Requires evidence that the harness actually permits the write — current docs say it doesn't.

Either way, the two files should agree.

## FB-053: Tool Preferences block duplicated verbatim across 3 agent files

**Status:** promoted
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-013 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — multi-agent template audit, 2026-04-28. `agents/` files are byte-identical to template.
**Assessed:** 2026-05-13 — Affects `.claude/agents/implement-agent.md` (lines 24-32), `.claude/agents/verify-agent.md` (lines 34-42), `.claude/agents/research-agent.md` (lines 23-31); canonical home `.claude/rules/agents.md` § Tool Preferences (lines 51-60). Scope: corrective. Replace per-agent blocks with one-line pointer ("Tool preferences: see `rules/agents.md § Tool Preferences`"). Removes drift risk; saves ~30 lines per multi-agent flow. Bundle with FB-052 — both touch the same three agent files. Route: Phase 4 direct.
**Promoted:** 2026-05-13 — Extracted canonical Tool Preferences table to `.claude/rules/agents.md` § Tool Preferences; replaced duplicated table in `.claude/agents/{implement,verify,research}-agent.md` with pointers + agent-specific bash-usage notes. Preserved agent-specific guidance (implement-agent's editing strategy + large-file strategy). Shipped in template_version 3.1.1.

`implement-agent.md:24-32`, `verify-agent.md:34-42`, and `research-agent.md:23-31` each contain a near-identical Tool Preferences block (~9 lines × 3). The same content already exists canonically in `rules/agents.md § Tool Preferences` (lines 51-60). Four sources of truth for the same rule.

Drift hazard: a future edit will likely land in `rules/agents.md` (the canonical home) and skip the three agent files, leaving the per-agent restatements stale. Or vice versa.

**Suggested fix:** delete the per-agent restatements; replace each with a one-line pointer like *"Tool preferences: see `rules/agents.md § Tool Preferences`."* Saves ~30 lines of duplicated context per multi-agent flow and removes the drift risk.

Lighter alternative: keep the per-agent pointers but add a comment in `rules/agents.md` reminding maintainers to ripple any change to the three agent files. Less robust but lower-disruption.

Same pattern likely exists in downstream forks for product-specific commands (e.g., styler's six product commands all duplicate an "Output Formatting" block) — that's a fork-side issue, but the agent-side fix here would model the right pattern.

## FB-054: breakdown.md:17-18 numbered list skips step 2

**Status:** promoted
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-014 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — multi-agent template audit, 2026-04-28. `commands/breakdown.md` byte-identical to template.
**Assessed:** 2026-05-13 — Affects `.claude/commands/breakdown.md` Process section (lines 17-18). Scope: corrective. Renumber surviving steps 3 → 2, 4 → 3, 5 → 4; OR restore the deleted step 2 if its removal was unintentional. Cosmetic but reads as broken in markdown viewers that don't auto-renumber. Route: Phase 4 direct.
**Promoted:** 2026-05-13 — Renumbered `.claude/commands/breakdown.md` Process section from 1, 3, 4, 5 → 1, 2, 3, 4. Shipped in template_version 3.1.1.

`commands/breakdown.md` Process section is numbered 1, 3, 4, 5 — there is no step 2:

```markdown
## Process

1. Identify logical components (aim for 3-6 subtasks)
3. Create subtask files (inheriting spec provenance from parent):
   ...
4. Update parent task:
   ...
```

Likely a step that got deleted without renumbering the survivors. Cosmetic but reads as broken in markdown viewers that auto-renumber lists.

**Suggested fix:** renumber 3 → 2, 4 → 3, 5 → 4 throughout the section. Or, if a step is missing, restore it.

## FB-043: implement-agent prompt should emphasize "extend ALL enum/union locations"

**Status:** promoted
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-003 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Refined:** 2026-05-13 — Add a Step 2.5 to implement-agent: when adding a new enum value or string-literal union member, grep for ALL synchronized extension points (TS union, Zod enum, dispatcher cases, validator switch arms) BEFORE editing. Don't trust `files_affected` for enum-related work. A one-line 'Common pitfalls' note suffices. Scope: `implement-agent.md`.
**Assessed:** 2026-05-13 — Affects `.claude/agents/implement-agent.md` (new 'Common Pitfalls' subsection, or extension of existing). Scope: additive. Complements FB-058 ripple-inference leg (FB-058 catches the ripple at decomposition time; FB-043 catches it at implementation time — belt-and-braces, no conflict). Route: Phase 4 direct.
**Promoted:** 2026-05-13 — Added new '### Synchronized Locations: Enums, Unions, Dispatchers' subsection to `.claude/agents/implement-agent.md` § Implementation Guidelines. Instructs the agent to grep for ALL synchronized extension points (TS unions, Zod/Pydantic enum schemas, dispatcher cases, validator switch arms, configuration whitelists) BEFORE editing — and to add a friction marker (type: `template_gap`) when `files_affected` under-counts the actual extension set. Shipped in template_version 3.2.0.

When an implement-agent task adds a new enum value (e.g., a new capture method, status, or any string-literal union member), the implementation typically needs to extend multiple synchronized locations:

- TypeScript union type (e.g., `CaptureMethod` in types.ts)
- Zod enum schema (e.g., `CaptureMethodSchema` in schema-zod.ts)
- Dispatcher case handlers (e.g., onboard.md case statements)
- Validator handlers (loader.ts switch arms, if any)

Concrete example from a downstream styler project's T424 (add Zod + TS types for `split_strategy` per DEC-047): agent added `SplitBucketSchema` + `SplitStrategySchema` + extended `FieldCaptureSchema` with new optional fields, but **missed adding `'ask_user_question_split'` to `CaptureMethodSchema` enum AND `CaptureMethod` TS union**. T425 (the next task) absorbed the fix (5-line addition across two files), no harm done — but the gap delayed T425's start by ~5 minutes of root-cause investigation, and surfaced as a friction marker at session pause.

Suggested template improvement: add a Step 2.5 (after planning, before editing) to implement-agent.md — "When adding a new enum value or string-literal union member, list ALL locations that enumerate this value across the codebase (TS union, Zod enum, dispatcher cases, validator switch arms) and extend each one. Don't trust the task description's `files_affected` list to be exhaustive for enum-related work — search for the existing enum's name with grep first to find all extension points."

Even a one-line note in implement-agent.md's "Common pitfalls" section would catch this.

## FB-046: Parallel-batch cross-task scaffolding contracts need single composed brief

**Status:** promoted
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-006 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler (Personal Style Intelligence System)
**Refined:** 2026-05-13 — When `/work` Step 2c builds a parallel batch with shared test scaffolding (allowlists, fixtures), compose a single shared briefing block both implement-agents receive verbatim — names who-owns-what, who-drains-what, and the mediating test signal. Detection heuristic: overlapping `files_affected` where one task description mentions `expected`/`allowlist`/`fixture` and another mentions `drain`/`drop`/`close`. Add `shared_contract` field to dispatch payload. Scope: `commands/work.md` Step 2c, `parallel-execution.md`.
**Assessed:** 2026-05-13 — Affects `.claude/commands/work.md` Step 2c (parallel-batch dispatch), `.claude/support/reference/parallel-execution.md`. Scope: additive. Complementary to FB-058 (different concerns: FB-058 enumerates files at decomposition; FB-046 mediates contracts between parallel tasks at dispatch). Route: Phase 4 direct. The detection heuristic ('expected/allowlist/fixture' vs 'drain/drop/close') may need refinement after trial — not blocking initial implementation.
**Promoted:** 2026-05-13 — Added new '## Shared Scaffolding Contracts' section to `.claude/support/reference/parallel-execution.md` with detection heuristic, contract schema, briefing behavior, and Pre-Dispatch Confirmation integration. Added a Step 5 callout in Eligibility Assessment and a reference in `.claude/commands/work.md` Step 2c summary. Heuristic fires when overlapping `files_affected` exists AND one task description mentions `expected`/`allowlist`/`fixture`/`scaffolding` AND the other mentions `drain`/`drop`/`close`/`resolve`/`remove`. The `agreement` field overrides contradictory per-agent briefs. Shipped in template_version 3.2.0.

When `/work` Step 2c builds a parallel batch of tasks that share cross-task synchronization contracts (test allowlists, fixture scaffolding, expected-violation lists), the orchestrator currently writes independent briefs that can contradict each other on file boundaries.

**Concrete repro (styler Phase 20 batch 13, 2026-04-27):**

The orchestrator dispatched **T462** (close § 20.4 split-strategy debt) + **T463** (broaden T460 validator) in parallel. Both modify allowlist scaffolding spread across `schema-zod.ts` and `registry-consistency.test.ts`.

- T462's brief said: "do NOT touch `registry-consistency.test.ts` (T463's territory; T463 may modify fixtures)".
- T463's actual implementation wrote scaffolding into `registry-consistency.test.ts` containing a self-documenting `EXPECTED_T463_VIOLATIONS` array AND a failing-test message reading `"drop them now"` whenever the array still listed entries that T462 had supposedly drained.
- Result: T462 was **forced** to drain `EXPECTED_T463_VIOLATIONS` to keep `npm test` green, violating its own brief. The friction marker (`type: template_gap`) was logged.

Final state was correct (both edits cleanly merged on disk and tests passed), but the brief contradicted the runtime contract.

**Proposed fix:** When `/work` Step 2c builds a parallel batch and detects a shared scaffolding contract (e.g., both tasks touch the same allowlist file, or one task writes test scaffolding that another task is responsible for draining), compose a **single shared briefing block** that both implement-agents receive verbatim, naming who-drains-what and why.

Schema sketch for an additional `shared_contract` field in the parallel-batch dispatch payload:

```json
{
  "shared_contract": {
    "type": "allowlist_drain",
    "file": "registry-consistency.test.ts",
    "constants": ["EXPECTED_T463_VIOLATIONS"],
    "owner": "T463 (writes scaffolding)",
    "drainer": "T462 (drops entries when violations resolve)",
    "test_signal": "failing-test message 'drop them now'"
  }
}
```

Each agent's brief inherits the shared block; neither agent gets a contradicting "do not touch" instruction. Detection heuristic: if two parallel tasks have overlapping `files_affected` AND one task's description mentions `expected`/`allowlist`/`fixture` while the other's mentions `drain`/`drop`/`close`, surface the contract for the orchestrator to compose.

## FB-058: Decomposition pre-pass — validate paths + auto-enumerate ripple-affected files

**Status:** promoted
**Captured:** 2026-05-13
**Combined from:** FB-047 + FB-051
**Refined:** 2026-05-13 — Unified decomposition pre-pass covering two failure modes: (1) path resolution (FB-051 leg) — verify every declared path exists, surface non-resolvers inline before decomposition completes; (2) ripple inference (FB-047 leg, ~40% of styler Phase 20 friction) — auto-enumerate collateral fixtures/callers via 4 heuristics: field/type retirement grep, schema-cap value grep, `package.json` test-chain detection, validator-walk caller grep. Scope: `decomposition.md` or sub-procedure.
**Assessed:** 2026-05-13 — Affects `.claude/support/reference/decomposition.md` (or its sub-procedure), possibly `.claude/skills/decomposition-heuristics/` (the skill that owns the decomposition logic), possibly `.claude/commands/work.md` Step 1c (decomposition step), possibly `.claude/commands/health-check.md` (if integrated as a health-check). Scope: additive. Coheres with FB-043 (implementation-time enum ripple) and FB-046 (cross-task allowlist contracts) — together form a 'files_affected correctness suite.' Route: Phase 4 direct. The 4 ripple-inference heuristics are concrete enough to ship in one pass.
**Promoted:** 2026-05-13 — Added new '## Decomposition Pre-Pass Validation' section to `.claude/support/reference/decomposition.md` AND mirrored to `.claude/skills/decomposition-heuristics/SKILL.md` (both stay in sync per DEC-007 Option B trial). Two-leg pre-pass: Leg 1 (path resolution) verifies declared `files_affected` paths exist + fuzzy-matches the closest alternative; Leg 2 (ripple inference) runs four targeted-grep heuristics for field/type retirements, schema-cap changes, new test files under `__tests__`, and validator-walk extensions. Both legs are advisory (present-and-ask), not auto-rewriting. Step 8 of the procedure now references the pre-pass; SKILL.md metadata description updated to include it. Shipped in template_version 3.2.0.

`/work` decomposition currently produces `files_affected` lists that either reference paths that don't resolve OR miss ripple-affected files (fixtures, downstream callers, test-chain entries). Both modes cause implementer friction — ~3 wasted tool uses per path-correction case; friction markers across ~40% of styler Phase 20 tasks for under-counted scopes. FB-047 and FB-051 propose a unified pre-pass.

**Failure mode 1 — declared path doesn't resolve (FB-051):** Task references a path that doesn't exist. Example styler T453: declared `src/components/grooming/GroomingSection.tsx`; actual at `src/components/style/GroomingSection.tsx`.

**Failure mode 2 — declared paths correct but missing ripples (FB-047):** ~40% of styler Phase 20 friction markers cite under-counted `files_affected`. Examples:

- T428 (retire `life_stage`): declared `[field-definitions.json]`; missed 2 test files hard-coding the value.
- T435 (`.max(4)` → `.max(6)`): declared 6 files; missed `loader.test.ts` with hard-coded threshold fixtures.
- T439: declared 3 files; missed 2 new files + `package.json` chain edit.
- T460: declared 2 files; missed 4 downstream `RegistrySchemaZ.parse()` callers.

**Proposed unified pre-pass (decomposition.md or sub-procedure):**

1. **Path resolution check (FB-051 leg):** verify every path in `files_affected` and any path-shaped reference in task body exists. Surface non-resolving paths inline for human correction before decomposition completes.
2. **Ripple inference (FB-047 leg):**
   - Field/type retirement ("remove X" / "retire X") → `grep -r "X"` across `**/__tests__/**`, fixtures, mocks → add matches.
   - Schema-cap / threshold change (`.max(N)` → `.max(M)`) → `grep -r "{old_value}"` in fixtures → flag schema-constant-name matches.
   - New test files under sibling/`__tests__` conventions → if `package.json` `scripts.test` chains explicit paths → add `package.json`.
   - Validator-walk extension (Zod/Pydantic schema change) → `grep -r "{SchemaName}\.parse\|\.{SchemaName}\.safeParse"` → add downstream caller files.

Could extend later to function-name drift detection; path + ripple covers the dominant friction.

Sources: FB-051 (originally styler FB-053) + FB-047 (styler Phase 20 friction-marker analysis, 2026-04-27).

## FB-042: Phase-restoration audit task descriptions need literal-ID cross-check

**Status:** promoted
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-002 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Refined:** 2026-05-13 — Audit-task descriptions of the form 'verify whether downstream task X is needed' must compare target IDs literally, not by count or semantic name match. Required behavior: (1) read X's task body for literal target IDs, (2) compare against current state by ID, (3) only report 'stale/no-op' on literal match, (4) report 'scope_clarification_needed' on semantic-without-ID match. Scope: `implement-agent.md` audit-task pattern OR `rules/task-management.md`.
**Assessed:** 2026-05-13 — Affects `.claude/rules/task-management.md` (new audit-task guidance subsection — implement-agent.md has no dedicated audit-task section, so the rule belongs here). Scope: additive. No cross-conflicts with active items; only loosely related to FB-058 (different lifecycle phase: audit vs decomposition). Route: Phase 4 direct.
**Promoted:** 2026-05-13 — Added '## Audit Tasks' section to `.claude/rules/task-management.md` (after Parallel Execution, before References) requiring literal-ID comparison in audit tasks of the form 'verify whether downstream task X is needed'. Specifies 4-step required behavior and the `scope_clarification_needed` reporting path for semantic-without-literal-ID matches. Calibrated against the styler Phase 20 T429 false-positive 'no-op' finding. Shipped in template_version 3.2.1.

Phase-restoration / pre-flight audit task descriptions (e.g., a "Phase N prereq audit" task that checks whether downstream registry edits are needed) tend to produce false-positive "stale" or "no-op" findings when they compare against task target sets via name-matching or count-matching rather than literal-ID matching.

Concrete example from a downstream styler project's Phase 20 prereq audit:

- Audit reported "measurements_core ALREADY=10 sub_fields, all 7 spec-named present" → orchestrator broadcast "T429 will be a verify-only no-op" to the user. Reality: T429's 7 measurements (across_back, bicep, wrist, torso_length, outseam, calf, head_circumference) are entirely different IDs from the 10 already present (height, weight, chest, waist, hips, shoulder_width, arm_length, inseam, neck, thigh). T429 was real work.
- Same audit reported "winter_months — likely single_enum, should become multi_enum" → reality: already multi_enum, but spec body actually said "render-as-enum" (UI bug), not "type-as-enum" (schema bug). The audit's hypothesis didn't match the spec's actual claim.

Both findings caused downstream confusion: the orchestrator told the user "T429 is a no-op" then T429 turned out to be real work; same pattern with T431.

Suggested template improvement: when a phase-restoration / pre-flight audit task description includes "verify whether downstream task X is needed", require it to:

1. Read X's task description (the actual target IDs / values / shapes).
2. Compare literally against current state (by ID, not by count or semantic name match).
3. Only report "stale/no-op" if the literal IDs match exactly.
4. If similar-but-different (semantic match without ID match), report as "scope_clarification_needed" rather than "stale".

This could live as a guideline in implement-agent.md's audit-task pattern, or as a sentence in the task-management.md rules around audit tasks.

## FB-044: Heavy editorial verify-agent prompts may benefit from structural+content split

**Status:** promoted
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-004 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Refined:** 2026-05-13 — Add a budget guideline to verify-agent.md for heavy editorial tasks: 'if verification target includes ≥3 substantial markdown files, plan ≤25 tool calls; consider splitting or invoking a content-only sub-agent.' Lightest-touch of 3 body options (option 2); defer structural splits (separate structural+content passes; task-JSON `verify_strategy` field) until guideline proves insufficient. Scope: `verify-agent.md`.
**Assessed:** 2026-05-13 — Affects `.claude/agents/verify-agent.md` (new budget guideline subsection). Scope: additive. Complements FB-049 (proactive budget prevention vs reactive graceful resume). Route: Phase 4 direct. The '≤25 tool calls for ≥3 prose files' heuristic is calibratable post-trial — start with the guideline, tighten later if budget overruns continue.
**Promoted:** 2026-05-13 — Added '## Editorial-Content Budget Guideline' section to `.claude/agents/verify-agent.md` (between Turn Budget Protocol and Wind-Down Protocol). Heuristic: ≥3 substantial markdown files (or single file >500 lines prose) → plan ≤25 tool calls; three options (split structural+content / reduce scope / tighten reads). Calibrated against styler T447's 32-call quota exhaustion 2026-04-27. Shipped in template_version 3.2.1.

Verify-agents on heavy editorial content tasks (rewriting style principles, restructuring documentation, multi-file prose changes) approach the per-agent budget ceiling.

Concrete example from a downstream styler project's T447 verify-agent (rewrite 3 universal style principles + add 3 feminine-gated rules + delete archetype framework section, 6 files modified):

- 32 tool calls; ran out of Anthropic usage quota mid-verification.
- Verification target included: read 6 modified markdown files end-to-end; run 4 test suites (registry-consistency 62/62, completeness 41/41, prompt-render 23/23, suggestions-context 10/10); run tsc --noEmit; multiple greps to verify cross-refs + archetype residue; judge editorial content quality (axis vocabulary, voice consistency, ID cross-ref integrity, scope expansion sensibility).
- Verify-agent was actively working when quota exhausted — not stuck — but ran past quota.

Suggested template improvement: for editorial-content tasks (heuristic: difficulty ≥ 5 AND files_affected includes prose/markdown), consider one of:

1. **Split verify-agent into two passes** — structural (files exist, scope clean, cross-refs resolve, tests pass, no out-of-scope edits) + content (read prose, judge tone/voice, semantic correctness). Sub-verifications can run in parallel.
2. **Document a budget guideline in verify-agent.md** — "If verification target includes ≥3 substantial markdown files, plan ≤25 tool calls — heavy editorial review may need to be split or invoke a separate content-only sub-agent."
3. **Add a `verify_strategy: structural+content` field** to task JSON — the orchestrator reads this at dispatch and routes to a different agent template when set.

Option 2 is the lightest-touch — a sentence in verify-agent.md prompts the agent to budget-aware itself.

## FB-056: Playwright MCP UI inspection doesn't parallelize across subagents — document the limit and the sequential pattern

**Status:** promoted
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-016 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler
**Refined:** 2026-05-13 — Add a 'MCP and Parallel Execution' subsection to `rules/agents.md` documenting that single-session MCP servers (Playwright, browser automation, any stateful single-instance resource) cannot be safely fanned out across parallel subagents — concurrent calls share underlying state and interleave silently. Orchestrator pattern: route MCP-driving work through one agent, parallelize the rest; for multi-route UI inspection, dispatch sequential agents with focused scopes. Adjacent (lower priority): `/work` Step 2c parallel-batch heuristic could extend to `mcp_resource_overlap` detection. Scope: `rules/agents.md`.
**Assessed:** 2026-05-13 — Affects `.claude/rules/agents.md` (new 'MCP and Parallel Execution' subsection). Scope: additive. Adjacent connection to FB-046: FB-056's lower-priority `mcp_resource_overlap` heuristic could land at the same call site as FB-046's `shared_contract` work — worth bundling implementation if both go in the same pass. Route: Phase 4 direct.
**Promoted:** 2026-05-13 — Added '## MCP and Parallel Execution' section to `.claude/rules/agents.md` (between Behavioral Rules and Tool Preferences). Documents single-session MCP server constraint (Playwright, browser automation, auth-session MCPs) — concurrent calls share state and interleave silently. Three-pattern orchestrator response: route MCP-driving work through one agent / parallelize the rest / dispatch sequential agents for multi-route inspection. Notes lower-priority `mcp_resource_overlap` heuristic for future /work Step 2c extension. Shipped in template_version 3.2.1.

User asked whether multiple subagents could simultaneously drive Playwright MCP to inspect the running app. The honest answer is no: the Playwright MCP server holds a single browser session, so subagents that all call `mcp__playwright__browser_*` would be driving the *same* tab — navigations, clicks, snapshots, and console reads interleave instead of running in parallel. That's contention, not parallelism, and the failure mode is silent (snapshots that look fine but reflect another agent's mid-action state).

This question will recur in any project that uses Playwright MCP for UI verification (the styler template explicitly pre-authorizes Playwright MCP for implement/verify agents, per `feedback_playwright_mcp_preauthorized` in user memory). It's worth a one-paragraph callout in the template so future orchestrators don't fan out Playwright work into a parallel batch and assume it'll behave like file-edit parallelism.

**Concrete usage patterns that *do* work** — worth naming so the orchestrator has a default:

1. **Sequential Playwright agents, shared browser** — dispatch one Playwright-driving agent per route/flow, in series. Each gets a tight scope ("audit /coloring", "audit /wardrobe"). One browser session, no contention.
2. **Parallel agents, only one drives Playwright** — the second agent does code reads / greps / test runs while the first agent drives the browser. Parallelism without collision.
3. **True parallel browser inspection** — would need multiple Playwright MCP server instances on different ports (or separate user-data dirs); not how the template ships and not trivial to set up. Out of scope for most projects.

**Suggested template improvement:** add a short subsection to `rules/agents.md` (probably under a new "MCP and Parallel Execution" heading, or appended to "Tool Preferences") that says:

> **Single-session MCP servers don't parallelize.** Playwright MCP, browser automation MCPs, and any MCP that exposes a stateful single-instance resource (one browser, one auth session, one connection) cannot be safely fanned out across parallel subagents — concurrent calls share the underlying state and interleave silently. When `/work` builds a parallel batch involving such tools, route the MCP-driving work through one agent and parallelize the rest. For multi-route UI inspection, dispatch sequential agents with focused scopes rather than a parallel batch.

Could also be worth a one-line caveat in `agents/implement-agent.md` and `agents/verify-agent.md` near where Playwright MCP is mentioned, but the rule belongs in `rules/agents.md` so it's discoverable from the rules-index.

**Adjacent observation:** auto mode's parallel-batch heuristic (Step 2c in `commands/work.md`) currently keys on `files_affected` overlap. For MCP-shared-state contention, that signal won't fire — two tasks with disjoint `files_affected` can still both want the browser. If the template ever wants to be precise here, the parallel-batch builder could also check for `mcp_resource_overlap` (any pair of tasks both expected to use the same single-instance MCP server). Lower priority than the documentation fix above.

## FB-048: Inline-command pattern — extract a shared template reference doc

**Status:** promoted
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-008 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler
**Refined:** 2026-05-13 — Extract a canonical inline-command pattern doc at `.claude/support/reference/inline-command-pattern.md`: named-subroutine contract table, idempotency contract with dedup-tuple guidance, standalone-only step flag, retirement callout format, vestigial-key handling. Individual command markdowns reference it instead of re-deriving from a peer (styler observed 3 inline commands with already-drifting dedup tuples). Scope: new reference doc + light edits to inline-capable command markdowns.
**Assessed:** 2026-05-13 — Affects new `.claude/support/reference/inline-command-pattern.md` (file doesn't yet exist; verified). Scope: additive. The template itself doesn't ship inline-capable commands — this is a pattern reference for downstream projects (like styler) that compose slash commands. No conflict with template-side changes. Route: Phase 4 direct. Worth marking the doc as 'pattern reference, not enforced behavior' so users know it's optional guidance.
**Promoted:** 2026-05-13 — Created new `.claude/support/reference/inline-command-pattern.md` documenting the canonical pattern for composable slash commands (child runs both standalone and inline from a parent). Covers: '## Inline Invocation from /{parent}' section header convention, four-column named-subroutine contract table (Inputs / Outputs / Standalone wrapper / Inline call site), idempotency contract with dedup-tuple guidance, Standalone-only step flag convention, retirement callout format for legacy delegate-and-stop framing, and progress-state vestigial-key handling for backward compat. Marked as 'pattern reference, not enforced behavior' — template does not ship inline-capable commands. Added to `.claude/sync-manifest.json` sync list and `.claude/support/reference/README.md` guides table. Shipped in template_version 3.2.2.

When a project has multiple slash commands that can be invoked **inline within a parent command** (e.g., `/coloring` invoked from inside `/onboard`, `/grooming` from inside `/onboard`, `/wardrobe` from inside `/onboard`), the integration pattern is non-trivial: named subroutines, idempotency contracts, standalone-only step flagging, retired-delegate-framing callouts, vestigial-key handling for backward compat, etc.

**Observation from styler (2026-04-27):**

Three tasks landed the same pattern in close succession — T449 (`/coloring` inline), T450 (`/grooming` inline), T454 (`/wardrobe` inline). Each implement-agent re-derived the pattern from the prior task as a precedent. The result is **near-duplicated** structure across the three command markdown files (`coloring.md`, `grooming.md`, `wardrobe.md`):

- Same "Inline Invocation from /onboard" section header
- Same contract-table column shape (Inputs / Outputs / Standalone wrapper / Inline call site)
- Same Idempotency Contract clause **with slightly different dedup tuples** — selfie+date for coloring/grooming, item-file-path for wardrobe
- Same Standalone-only flag convention on standalone-analysis steps
- Same retirement-callout format for the now-retired delegate framing

This is correctness-by-precedent, but each future inline command will pay the same duplication cost, and the dedup-tuple drift (across already three commands) is a foot-gun.

**Proposed fix:** Add a template reference doc, e.g., `.claude/support/reference/inline-command-pattern.md`, that describes the canonical pattern:

1. The named-subroutine contract table format (Inputs / Outputs / Standalone wrapper / Inline call site columns)
2. The Idempotency Contract structure with explicit guidance on choosing the dedup tuple ("a stable identity that re-running with the same inputs and same wall-clock day should not regenerate" — selfie path, item file path, etc.)
3. The Standalone-only flag convention for steps that don't run inline
4. The retirement callout format for legacy delegate-and-stop framing
5. The progress-state vestigial-key handling for backward compat with existing on-disk progress JSON

Then individual command markdowns can `@reference` the template doc instead of re-deriving it from a peer. Future inline commands inherit the pattern by reference, not by copy.

This is template-side because the **pattern itself** is generic — any project with composable slash commands will hit the same shape.

## FB-055: subagent_type "general-purpose" used to dispatch specialist agents in work.md / research.md

**Status:** promoted
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-015 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — multi-agent template audit, 2026-04-28. `commands/work.md` and `commands/research.md` byte-identical to template.
**Refined:** 2026-05-13 — Three call sites (`work.md:603,686`; `research.md:74`) dispatch named specialist agents with `subagent_type: 'general-purpose'`. Switch to named subagent_types (`implement-agent`, `verify-agent`, `research-agent`) — aligns dispatch with definition, leverages `.claude/agents/` auto-discovery the template implicitly assumes by shipping definition files. Alternative (b) — document 'general-purpose' as intentional in `rules/agents.md` for portability — is the fallback if auto-discovery proves harness-version-fragile. Scope: `commands/work.md`, `commands/research.md`.
**Assessed:** 2026-05-13 — Affects `.claude/commands/work.md` (lines 603, 686 — implement-agent + verify-agent dispatch), `.claude/commands/research.md` (line 74 — research-agent dispatch). Scope: corrective. Dependency on DEC-004 (subagent capability contract — must verify named subagent_type doesn't change sandbox behavior relative to general-purpose; low risk but check first with a smoke test). Route: Phase 4 direct. Small change (3 sites + smoke test).
**Promoted:** 2026-05-13 — Added '## Dispatch Convention' section to `.claude/rules/agents.md` (between Behavioral Rules/Tool Preferences area and Model Requirement). Documents the intentional `subagent_type: "general-purpose"` + persona-via-prompt-content pattern at the three call sites (work.md:605 per-task verify, work.md:688 phase-level verify, research.md:74 research-agent). Rationale: Claude Code's `.claude/agents/*.md` auto-discovery is not uniform across harness versions; named subagent_types would risk dispatch failures. Future migration gate documented — switch only after smoke-test validates named-from-disk auto-discovery is stable. Chose body Option (b) over Option (a) because the AVAILABLE AGENT TYPES list in the current harness (Opus 4.7) does NOT auto-include `.claude/agents/*.md` definitions; a flipped dispatch shape would currently regress. Shipped in template_version 3.2.3.

Three call sites dispatch named specialist agents (implement-agent, verify-agent, research-agent) but with `subagent_type: "general-purpose"`:

- `work.md:603` (implement-agent dispatch)
- `work.md:686` (verify-agent dispatch)
- `research.md:74` (research-agent dispatch)

The agent definitions live at `.claude/agents/{implement,verify,research}-agent.md` but the dispatch shape doesn't reference them as named subagent types. This works because the dispatched agent's prompt directs it to read its own definition file — but it bypasses any per-agent configuration that Claude Code's `.claude/agents/` discovery would otherwise apply (e.g., per-agent model default, per-agent tool allowlist if/when the harness supports them via frontmatter).

Two paths:

- **(a) Switch to named subagent_types** — `subagent_type: "implement-agent"`, `"verify-agent"`, `"research-agent"`. Relies on Claude Code's auto-discovery of `.claude/agents/*.md`. Aligns dispatch with definition.
- **(b) Document that "general-purpose" is intentional** — perhaps for portability across harness versions where named subagents might not auto-discover, or to keep the persona-via-prompt-content pattern. Add a one-line note in `rules/agents.md` explaining the choice.

Either is defensible; the current state is "neither documented nor uniformly applied." Worth picking one and being explicit. (a) seems cleaner if Claude Code's `.claude/agents/` discovery is stable, which the template implicitly assumes by shipping definition files there.

## FB-038: Action Required regression — completion summaries still clutter section despite FB-015 fix

**Status:** promoted
**Captured:** 2026-04-22
**Refined:** 2026-05-13 — Audit whether FB-015's Action Item Contract negative rule (now at `dashboard-regeneration.md:333`) actually fires during regeneration. Styler 2026-04-22 evidence shows completion summaries still clutter Action Required despite FB-015 promoted 2026-04-17. Two follow-ups: (a) audit dashboard-emission call sites for compliance; (b) if violations persist, escalate to FB-011 Family C (extract regen into a script — enforced by construction). Scope: `dashboard-regeneration.md`, `commands/work.md` post-completion emission paths, `health-check.md` Part 6 check #4.
**Assessed:** 2026-05-13 — Affects `.claude/support/reference/dashboard-regeneration.md` (verify rule landed and is well-formed; already at line 333), `.claude/commands/work.md` post-completion emission paths, `.claude/commands/health-check.md` Part 6 check #4 (extend to detect summary-shaped content if feasible). Scope: corrective. Two-step: (a) audit downstream emitters for compliance with FB-015's negative rule; (b) if LLM compliance keeps failing, escalate to FB-011 Family C (extract dashboard regen to a script — tracked in `template-maintenance/scripts-candidates.md`). Direct dependency on FB-015 (just promoted; freshness risk that the rule was added but emitters bypass it). Route: Phase 4 direct for the audit; FB-011 Family C escalation is a separate gate.
**Promoted:** 2026-05-13 — Audit findings: FB-015's negative rule is in place at `.claude/support/reference/dashboard-regeneration.md:333`; `commands/work.md:724` reflects it (Action Required clears post-completion); the canonical Action Required sub-section order (line 372) intentionally omits 'Recent Activity'/'Work Summary'. **The gap:** `commands/health-check.md` Part 6 check #4 only validated actionability — did not detect summary-shape violations. **Fix:** split check #4 into 4a (existing actionability check) + 4b (new summary-shape detection) with four heuristics: past-tense completion verbs, forbidden sub-section headings, long-prose items, bulleted lists of finished work. Each match emits a severity-3 error per occurrence. **Escalation note in the check:** if 4b fires repeatedly across runs on the same project, root cause is likely LLM emitter compliance — escalate to FB-011 Family C (script extraction, tracked in scripts-candidates.md). Shipped in template_version 3.2.4.

The dashboard's Action Required section is again dominated by non-actionable content even after FB-015 (currently `ready`) was supposed to address exactly this. Observed in the styler project dashboard export (`dashboard_export_styler.pdf`, 2026-04-22).

**What the section contains (none of which is user-action):**
- Paragraph-long closure summary for § 17.15 Phone Layout Remediation ("2 BLOCKERs + 12 HIGHs → [OK]")
- Bulleted shipped-tasks list (321–330) with one-line descriptions
- Multi-paragraph Task 331 completion report (fix details, verification method, "suggest bundling into a commit")
- Repo state narrative (committed vs uncommitted, untracked PNGs to discard)
- "Phase 5 still On Hold" reminder and "Residual follow-ups from earlier phases" with accepted spec drift

The only arguably-actionable fragment — "Change is uncommitted" — is buried inside a paragraph, not surfaced as an action item.

**User-reported phrasing:** *"even more cluttered with stuff that isn't actionable now after we implemented a fix. Something is going on"* — pattern appears to be regressing, not just failing to improve.

**Possible root causes** (to refine):
1. FB-015 is `ready` but not yet promoted via `/iterate` — the rule edit may never have landed in `dashboard-regeneration.md` § Action Item Contract. Verify before anything else.
2. Rule landed but generators (`/work complete`, phase-closure regen, implement-agent post-completion emission) bypass the Action Item Contract in practice.
3. LLM interprets completion summaries as "actionable" because they imply follow-ups (commit change, discard PNGs, resume On Hold phase).
4. Action Required is being used as a catch-all narrative slot because the dashboard has no dedicated "recent activity" or "session recap" section — matter removed from Action Required has nowhere else to go.

**Possible direction:** reopen/extend FB-015 rather than treat this as a new independent item. Also consider whether FB-011's deterministic generator is the only reliable backstop for a contract the LLM persistently violates.

Source: `dashboard_export_styler.pdf` (styler project, 2026-04-22).

## FB-050: /iterate spec-vs-registry hygiene pass — grep-validate spec claims

**Status:** promoted
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-010 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler
**Refined:** 2026-05-13 — Add an `/iterate hygiene` pass that grep-validates spec noun-phrase claims about registry/schema state. Patterns: 'previously-empty X', 'field Y under section Z', 'update the X description'. Cross-reference against project's structured artifact (path configurable in `.claude/version.json`). Flag drift as `[NEEDS APPROVAL]` in the 'Decisions in This Proposal' section. Lighter alternative: fold into `/health-check` as per-spec consistency audit. Scope: `commands/iterate.md` OR `commands/health-check.md`.
**Assessed:** 2026-05-13 — Affects `.claude/commands/iterate.md` (new hygiene sub-command). Scope: additive. Complements FB-032 (Decisions in This Proposal — drift findings surface there). New config field needed: `structured_artifact_path` in `.claude/version.json` (project-configurable). Route: Phase 4 direct. The 'lighter alternative' (fold into `/health-check`) is a sub-decision worth flagging at implementation time — pick one before writing.
**Promoted:** 2026-05-13 — Added new `/iterate hygiene` sub-command to `.claude/commands/iterate.md`. Cross-checks spec noun-phrase claims (subsection state, structural location, modification targets) against the project's structured artifact (path configurable via new `structured_artifact_path` field in `.claude/version.json`). Best-effort parse for .json/.ts/.js/.yaml/.md; 4 cross-reference categories (state / structural / modification / missing-attribute); findings reported as `[NEEDS APPROVAL]` candidates surfaced into the next `/iterate` propose cycle. Follow-up options: [P]ropose / [E]xport to workspace / [S]kip. Hygiene mode never silently rewrites — surfaces findings, routes fixes through propose-approve-apply (Step 4). Picked /iterate sub-command over /health-check fold-in per the body's preferred option. Shipped in template_version 3.3.0.

Spec text drifts from registry/schema state over time. Each drift triggers a `spec_drift` friction marker but is otherwise resolvable inline by the implement-agent — meaning the drift accumulates silently until a future spec edit is needed.

**Two concrete examples from one session:**

1. **Spec § 20.2** said the `extremities` subsection was "previously-empty" — registry actually had `feet` / `hands` / `head` / `glasses_sunglasses` / `everyday_jewelry` already populated. Implementer (T430) had to interpret intent and add new fields under the existing `head` composite rather than treating the subsection as truly empty. Friction marker logged.

2. **Spec § 20.2** instruction "update the extremities subsection description" — `SubsectionDefSchema` has only `id` / `label` / `order` / `storage_file` (no `description` field). Instruction was unimplementable as written; implementer worked around by updating `head.description` (the composite field's description) instead. Friction marker logged.

Each case caused avoidable confusion and post-hoc workaround. Both would have been caught at spec-revision time by a static cross-check.

**Proposed fix:** Add a `/iterate hygiene` sub-command (or fold into existing `/iterate`) that runs at spec-revision time:

1. **Parse the spec** for noun-phrase claims about registry/schema state — patterns like:
   - "the X subsection / field / type"
   - "previously-empty / previously-X / now-X"
   - "field Y under section Z"
2. **Cross-reference against the actual structured artifact** (project-specific: `field-definitions.json`, `schema.ts`, etc. — could be parameterized via a config field in `.claude/version.json`).
3. **Flag drift:** "Spec § 20.2 says 'previously-empty extremities' but registry has 5 top-level fields under `extremities`." Surface as a `[NEEDS APPROVAL]` item in `/iterate`'s "Decisions in This Proposal" section.
4. **Cross-reference spec instructions** like "update the X description" against the schema (`SubsectionDefSchema`, `FieldDefSchema`) to verify the target attribute exists. Flag unimplementable instructions before they reach decomposition.

This is generally useful even outside styler: any spec-driven project with a structured artifact (registry, schema, config) accumulates this drift over many revisions.

Alternative (lighter): add this to `/health-check` as a per-spec consistency audit, run on demand rather than as a separate `/iterate` mode.

## FB-049: Anthropic usage-limit partial-completion structured resume contract

**Status:** promoted
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-009 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler
**Refined:** 2026-05-13 — Extend implement-agent return schema with a `partial_completion` envelope the agent fills when sensing usage-limit approach with unfinished sub-targets: `implementation_status: partial_resume_pending`, `completed_subtargets[]`, `remaining_subtargets[]`, `partial_state_notes`, `resume_instructions`. Orchestrator persists to task JSON; next dispatch brokers a 'resume from where you stopped' prompt instead of re-deriving from git diff. Detection heuristic: tool_uses > 75% of budget AND remaining sub-targets > 0. Extend `.handoff.json` schema for task-level partial state. Scope: `implement-agent.md` schema + `work.md` dispatch.
**Assessed:** 2026-05-13 — Affects `.claude/agents/implement-agent.md` (return schema fields), `.claude/commands/work.md` (dispatch + persistence), `.claude/tasks/.handoff.json` schema. Possibly `.claude/agents/verify-agent.md` (matching envelope?). Scope: additive. No conflict with DEC-004 state ownership (orchestrator persists; agent reports). Multiple non-trivial design choices remain: minimal envelope vs full, detection threshold (75% of budget — arbitrary), whether verify-agent gets a matching envelope, `.handoff.json` schema impact. **Route: Phase 3 research → candidate DEC-010.** Trial-gated on real usage-limit incidents (already observed twice in styler session per body — sufficient empirical basis to research now).
**Promoted:** 2026-05-13 — Implemented DEC-010 Option C (middle path): added `partial_completion` envelope to `.claude/agents/implement-agent.md` return schema (4 fields + `confidence` discriminator). Added `partial_resume_pending` to `implementation_status` enum with detection guidance (75% heuristic OR SDK wrap-up signal). Added new '### Approaching Usage Limits' section under Handling Issues. Orchestrator-side handler added to `.claude/commands/work.md` § 'After implement-agent returns' protocol (Status transition step) and a resume-pending check at the start of 'If Executing' (git-diff audit + envelope-injected dispatch prompt). `.claude/support/reference/context-transitions.md` handoff schema updated to document the string-or-object union for `active_work[].partial_notes` (backward-compatible). Decision record: `decisions/decision-010-partial-completion-envelope.md`. Shipped in template_version 3.4.0.

Anthropic usage-limit cuts mid-implement-agent or mid-verify-agent are recurring (twice in one styler session: T433's first dispatch was cut at 41 tool uses with no structured report; T454's verify-agent dispatch in the same session never started before the limit hit). Current handoff is via free-form task notes + dashboard prose + `.last-clean-exit.json` — entirely manual. Subsequent invocations have to audit partial work and reason about resumption.

**Concrete repro (styler T433, 2026-04-27 13:25 UTC):**

First implement-agent dispatch hit usage limit at 41 tool uses / 297s, returned no structured report. Working tree had partial edits across 3 of the task's ~18 declared sub-targets. Second invocation had to:

1. Read git diff to infer what landed
2. Read task notes for partial-progress hints (none present — orchestrator had only logged "dispatch cut by limit")
3. Audit which sub-targets within the cluster sweep were already done vs remaining
4. Compose a unified report covering both invocations once it finished the rest

Workflow handled it gracefully but the cross-invocation reasoning is fragile and adds ~10–15 minutes of audit overhead.

**Proposed fix:** Extend the implement-agent return schema with a `partial_completion` envelope that the agent can fill if it senses approaching limit AND has not finished:

```json
{
  "implementation_status": "partial_resume_pending",
  "completed_subtargets": ["field_X (4 buckets)", "field_Y (3 buckets)"],
  "remaining_subtargets": ["field_Z", "field_W", "field_V"],
  "partial_state_notes": "Stopped mid-sweep at field_Z; no edits to field_Z yet. Bucket taxonomy precedent: field_X = activity-family (indoor/outdoor/...).",
  "resume_instructions": "Resume from field_Z. Follow same bucket-taxonomy precedent as field_X. After all remaining, sweep audit to confirm 0 violations."
}
```

The orchestrator persists this to task JSON. Next dispatch reads it and brokers a "resume from where you stopped" prompt — the agent doesn't have to re-derive context from git diff + task notes.

`/work pause` already has graceful wind-down for user-initiated halts; this would mirror the pattern for the rate-limit case (which the agent itself can detect by approaching `max_turns` or by Anthropic's rate-limit response surface). The `.handoff.json` schema could be extended to include task-level partial state alongside session-level state.

Detection heuristic for the agent: if `tool_uses` count exceeds 75% of typical session budget AND remaining subtargets > 0, return `partial_resume_pending` instead of pushing through.

## FB-057: DEC-001 Option C execution gaps — friction-marker append + end-to-end pipeline

**Status:** promoted
**Captured:** 2026-05-13
**Combined from:** FB-041 + FB-045
**Refined:** 2026-05-13 — Audit DEC-001 Option C pipeline execution. Cause 1 (template_inbox_path discoverability) resolved by FB-040 Part 5d. Causes 2 (orchestrator marker-append skipped under load — styler Phase 20 batch-appended at pause; abrupt termination would have lost all markers) and 3 (`/work pause` Track 2 + Session Export not reliably run) remain. Tiered fix: behavioral nudge → idempotent catchup → structural PostAgentReturn hook → deterministic script (FB-011 Family D/E candidate). Investigation steps documented (real downstream session probes). Scope: `commands/work.md`, `pre-compact-handoff.sh`, possibly new scripts.
**Assessed:** 2026-05-13 — Affects (investigation phase first): `.claude/commands/work.md` (marker-append protocol or hook), `.claude/hooks/pre-compact-handoff.sh` (idempotent catchup), possibly new `.claude/scripts/` script (FB-011 Family D/E). Scope: corrective. Gates on (a) empirical data from real downstream sessions — currently blocked because no downstream project has `template_inbox_path` set (next downstream `/health-check` will surface this via FB-040 Part 5d), and (b) FB-011 Family D/E decision per `scripts-candidates.md`. **Route: Phase 3 research → candidate DEC-011** for fix-tier selection after investigation. Cannot proceed to Phase 4 direct without telemetry.
**Promoted:** 2026-05-13 — Implemented DEC-011 Option ABp (Hybrid A+B + .pending-markers.jsonl). **Tier A (behavioral nudge):** tightened `.claude/commands/work.md` § 'After implement-agent returns' step 2 — explicit 'do not defer; append immediately within the same step' wording; mirrored in `.claude/support/reference/parallel-execution.md` collection loops. **Tier p (transient buffer):** marker-append step now dual-writes to `.claude/support/workspace/.pending-markers.jsonl` AND `.session-log.jsonl` — narrows abrupt-kill loss window to sub-second. **Tier B (idempotent catchup):** new '### Step 0d: Friction-Marker Catchup' in `commands/work.md` runs at /work startup, dedup-merges pending entries into the canonical log, truncates pending. PreCompact hook (`.claude/hooks/pre-compact-handoff.sh`) extended with the same catchup logic before reading the session log — covers both /work-resume and compaction-triggered wind-down paths. Composite dedup key: `(task_id, timestamp, type, sha256(details))` with full-line hash fallback. The catchup count surfaced inline is itself the diagnostic signal for whether Tier A's tighter prose was sufficient (count = 0 means A alone is working; non-zero indicates the catchup is doing real work). Shipped in template_version 3.5.0.

DEC-001 Option C (Track 1 friction markers + Track 2 retrospective + Phase 3 ingest) is documented end-to-end across `implement-agent.md`, `verify-agent.md`, `work.md`, `pre-compact-handoff.sh`, and `health-check.md`, but empirical evidence suggests the pipeline isn't reliably executed.

**Observed gaps:**

1. **(from FB-041)** `interaction-logs/inbox/` empty as of 2026-05-13. Three causes:
   - Cause 1 (**resolved 2026-05-13**): no downstream project had `template_inbox_path` set — discoverability gap closed by `/health-check` Part 5d (FB-040 ship).
   - Cause 2: orchestrator-side marker append (`work.md:543,559`) documented but not reliably executed during `/work` runs.
   - Cause 3: `/work pause` Track 2 + Session Export step not reliably run (users close without pause; Claude may skip under context pressure).

2. **(from FB-045 — concrete repro for cause 2)** Styler Phase 20: orchestrator skipped the marker-append step throughout the session — markers from agent reports landed in task notes but NOT in `.session-log.jsonl` in real-time. At `/work pause` the orchestrator batch-appended 8 markers. Abrupt termination (compaction, crash, usage limit) would have silently lost those markers from Track 1 telemetry — task notes aren't structured for cross-project consumption.

**Investigation steps:**

- Run `/work` in a downstream project with markers expected to fire; inspect `.session-log.jsonl`.
- Run `/work pause`; confirm `.session-export-YYYY-MM-DD.json` appears in workspace and reaches `template_inbox_path`.
- Audit whether marker-append happens real-time vs catchup at pause.

**Proposed fixes (tiered):**

- Behavioral nudge: tighter protocol — append via single bash call immediately after agent return; do not batch.
- Idempotent catchup: if task notes contain markers without corresponding `.session-log` entries, orchestrator (or PreCompact hook) auto-appends.
- Structural: move append into a PostAgentReturn / PostToolUse hook gated on Task subagent — un-skippable.
- Or extract into a deterministic script (FB-011 Family D/E candidate) — removes the LLM reliability layer entirely.

Sources: FB-041 (2026-05-13, Option C audit) + FB-045 (2026-04-27, styler Phase 20).

## FB-059: `/health-check` Part 5 selective sync conflates unsynced template content with genuine local additions (false-positive SKIP)

**Status:** promoted
**Captured:** 2026-05-15
**Promoted:** 2026-05-16 — Implemented DEC-014 Option F (sidecar + algorithm, no category change) in template_version 3.15.0. New `.claude/.sync-state.json` sidecar (gitignored, schema-versioned, full SHA-256 with `sha256:` prefix) records per-file last-synced hash on every successful sync. `/health-check` Part 5 now classifies each diff via 2-condition algorithm: `local_hash == sidecar.synced_hash` → "Template content not yet applied" (default APPLY); mismatch or missing entry → "Modified upstream" (current behavior + "Show me the diff" sub-action). The Styler false-positive case (SKILL.md with pure template movement) now classifies correctly without confusing the user. Phase 2 (sync_strict category schema) deferred per DEC-014 — every current `sync` member is uniformly template-owned, so the sidecar's hash check is category-agnostic and sufficient. Decision record: `decisions/decision-014-sync-state-and-file-ownership-categories.md`. Affected files: `.claude/commands/health-check.md` Part 5 (Sync State Sidecar sub-section + Steps 2/3/4), `.claude/sync-manifest.json` (added `.claude/.sync-state.json` to `ignore`), `.claude/version.json` (bump 3.14.2 → 3.15.0).
**Source:** observed during downstream Styler `/health-check` after audit family v3.12.0 ship.

**Observation:** Part 5 (Template Sync Check) flagged two files as having "local additions" and offered selective sync that would SKIP both. Inspection showed the flag was correct for one file and a false-positive for the other:

- **`.claude/skills/dashboard-style/SKILL.md`** — 100% false positive. The diff was purely Stage 6 Option C content (kind-conditional `[Fix it]` action labels for the audit findings sub-section) that template shipped in v3.12.0 but Styler's local copy never received. Styler's `version.json` correctly read `template_version: 3.12.0` (the version field synced) but the file content stayed at Stage 6a state. Skipping the SKILL.md sync per the menu offer would have permanently prevented Styler from rendering `[Fix it]` labels until manual reconciliation.
- **`.claude/CLAUDE.md`** — correct flag. Styler genuinely added 2 project-specific rule imports (`brand-mention-provenance.md` per DEC-060, `feature-retirement.md` per FB-070 / § 27.1) plus their summary-table rows.

**Root cause hypothesis:** Part 5's detection compares downstream's *current* file content to template's *new* file content; any line-level diff is treated as a "local addition" warranting skip. This conflates two distinct conditions:
- (a) Downstream has unsynced template content (was at template_version N, template is at N+1, file content didn't sync along with the version field) → should sync
- (b) Downstream has genuinely user-added local content (file was customized after the last sync) → should preserve

The current algorithm can't distinguish these without per-file last-synced state.

**Proposed detection refinement:** Part 5 should compare downstream's file content to *the template version it last synced from*, not the *current template version*. The diff vs last-synced-version reveals genuine local additions. The diff vs current-template reveals all changes (sync delta + local additions). The intersection is what to sync without conflict; the symmetric difference is what to preserve as local. Requires the sync to record per-file last-synced template_version (or content hash). Could live in `dashboard-state.json` or a new `.claude/.sync-state.json` sidecar.

**Practical impact during this observation:** zero immediate harm because the `/audit-coherence` run that triggered the discovery had 0 bundle-eligible findings (so the missing `[Fix it]` labels weren't rendering anywhere). But future audits in Styler with bundle-eligible findings would have rendered with stale Stage 6a labels until manually reconciled.

**Workaround for affected projects (until Part 5 is refined):** when Part 5 offers selective sync, manually review the diff for each "skip" candidate via `diff <template-path> <project-path>`. If the diff is purely template content (lines present in template but not project), override the skip or manually copy the new template content into the project's file.

**Likely route:** scope-add to a new `/health-check` Part 5 refinement (not FB-058 — that's about `/work` decomposition path validation). Worth a research-light to confirm the proposed sidecar-based detection is feasible without restructuring the sync engine. Could also incorporate a "show me the diff" sub-action in the Part 5 menu so users can manually adjudicate per file.

## FB-065: Decomposition systematically under-counts synchronized-enum-locations in files_affected

**Status:** promoted
**Captured:** 2026-05-16
**Promoted:** 2026-05-16 — Added 5th heuristic row to FB-058's Decomposition Pre-Pass Leg 2 (Ripple Inference) in both `.claude/support/reference/decomposition.md` AND `.claude/skills/decomposition-heuristics/SKILL.md` (mirror per DEC-007 Option B). New heuristic fires on "new enum / literal-union / `as const` member" patterns (e.g., `add 'foo' to CriterionId`); grep finds importers and the procedure inspects them for `switch(...)` over the enum or `Record<EnumName, ...>` maps; surfaces parsers, formatters, header maps, barrel re-exports, and per-case test factories as ripple candidates. Advisory (present-and-ask), consistent with the other four legs. Shipped in template_version 3.16.0.
**Source:** 5+ occurrences across echothread sessions 2026-05-13/14/15 (T67, T80, T81, T82, T83 — see `interaction-logs/processed/echothread-session-2026-05-14.json` + `echothread-session-2026-05-15.json`). Cross-session friction-marker pattern.

**Observation:** When a task extends an enum (e.g., adds a new `CriterionId` member), the task's declared `files_affected` systematically under-counts the actual edit surface by 5-10 files. Concrete examples:
- T80: declared 4 files, edited 10 (synchronized locations under `CriterionId` / `CRITERION_ORDER` / `CRITERION_HEADERS` / `EvaluationInputs` / barrel / category-rename / inline polish / test-factory).
- T81: declared 4 files, edited 11 (under-counted by 7).
- T82: declared 4 files, edited 13.
- T83: declared 4 files, edited 14.

The synchronized-enum-locations rule (template's `.claude/rules/agents.md § Synchronized Locations` — implicit via `## Root Cause Over Symptom` semantics; implement-agent currently catches this at grep time, not at decomposition time) means the gap is recovered downstream but at the cost of (a) implement-agent doing extra synchronization work outside declared scope (every occurrence registered a `template_gap` or `scope_creep` marker), and (b) verify-agent's `scope_validation` check having to gracefully accept "actually edited 13 files, declared 4."

**Cross-reference:** FB-058, FB-047, echothread sessions 2026-05-13/14/15.

## FB-066: verify-agent missing default "production-consumption" check for class-export tasks

**Status:** promoted
**Captured:** 2026-05-16
**Promoted:** 2026-05-16 — Added production-consumption sub-bullet to `.claude/agents/verify-agent.md` Step T5 (Verify Integration Boundaries). Check fires when any file in `files_affected` declares a top-level class export (regex: `^export (default )?class \w+`); greps `new {ClassName}\(` across `src/` excluding `__tests__` and `*.test.*`; requires ≥1 hit OR explicit "consumer task deferred" note. Failure feeds the existing `integration_ready` key (no new schema field needed) and emits a `major` issue. Skips cleanly for tasks without class-exporting files. Catches the structural-vs-runtime verification gap that echothread Phase 4 surfaced only via interactive Playwright run on T71. Shipped in template_version 3.16.0.
**Source:** 3+ occurrences across echothread sessions 2026-05-14/15. Pattern: T71→T85 integration-gap discovery + T85_1/T85_2/T85_3 verifications adding ad-hoc grep checks.

**Observation:** Structural verification (files exist, types correct, tests pass) is necessary but not sufficient for tasks that ship a new top-level class export. Echothread's Phase 4 introduced 6 new module classes (`BeatEmitter`, `BeatResponse`, `ResonanceTracker`, `CriticalEvaluator`, `BeatEffects`, `NodeTrace`); structural verification passed for all 14 individual implementation tasks; the **integration gap** — modules exported but never `new`'d in `src/` — was discovered only via interactive Playwright-driven runtime test on T71. T85 was decomposed retroactively into 3 subtasks to close the gap. Subsequent T85_1/T85_2/T85_3 verifications each independently ran a `grep -rn 'new {ClassName}(' src/ | grep -v __tests__` check as a one-off addition to per-task verification — re-inventing the same pattern.

**Boundary with FB-064:** FB-064 proposes a *decomposition-time* heuristic that authors scenario tests for runtime/UI tasks. FB-066 proposes a *verification-time* check that catches "structural code shipped, no consumer" cases. They complement each other: FB-064 grows the test suite; FB-066 catches gaps even when scenario tests don't exist yet.

**Cross-reference:** FB-064, echothread sessions 2026-05-14/15 (markers from T71, T85_1, T85_2, T85_3).

## FB-064: Decomposition heuristic for project-local test-harness awareness

**Status:** promoted
**Captured:** 2026-05-16
**Promoted:** 2026-05-16 — Added new "Test-Harness Awareness" section to `.claude/support/reference/decomposition.md` AND `.claude/skills/decomposition-heuristics/SKILL.md` (mirror per DEC-007 Option B). Heuristic detects harness-eligible tasks via three OR conditions (`interaction_hint: cli_direct`, runtime-surface `files_affected` glob, runtime/UI `test_protocol`); scans for project-conventional harness directories (`tooling/test-scenarios/`, `tooling/scenarios/`, `tests/scenarios/`, `e2e/scenarios/`) with root `./CLAUDE.md` opt-in for custom paths/globs; proposes a scenario-authoring `_h` subtask when a harness exists but no scenario covers the task; surfaces a soft suggestion when no harness exists (does not force convention). Step 8 of standard decomposition procedure now references the check alongside the Pre-Pass Validation. SKILL.md frontmatter description extended to mention test-harness awareness. Shipped in template_version 3.17.0.
**Source:** Bridged from echothread `echothread-FB-009` (`echothread-feedback-2026-05-15-test-harness-pattern.json`, template_version 3.5.1) via interaction-logs inbox processing.

**Observation:** Claude only reaches for project-local programmatic test harnesses (e.g., Playwright-driven scenarios using `window.__app.engine.processKeystroke()`-style entry points) when prompted. The pattern gets re-discovered or re-justified each decomposition cycle. Echothread's 2026-05-15 T71 listening test (drove the game through a 1994-char passage via Playwright MCP + `engine.processKeystroke` rather than asking the user to type manually) was authored ad-hoc; the user (correctly) observed that the harness pattern is reusable and asked: how do we make Claude reach for this automatically during decomposition?

**Why template-side, not just project-side:** echothread is solving its immediate need via project-specific T86 (root `CLAUDE.md` addition). But every downstream project that adopts a programmatic-scenario harness convention will face the same "Claude only reaches for the harness when prompted" problem. Template-side heuristic makes harness-aware decomposition the default for any project that opts in.

**Cross-reference:** FB-058 (decomposition pre-pass — sibling), FB-066 (verify-time complement — catches "no consumer" gaps when scenarios don't exist yet).

## FB-071: `disable-model-invocation: true` frontmatter audit pass

**Status:** promoted
**Captured:** 2026-05-19
**Verified:** 2026-05-19 — claude-code-guide agent docs lookup confirmed `disable-model-invocation: true` is fully supported on `.claude/commands/*.md` with identical semantics to `.claude/skills/<name>/SKILL.md`. Sources: [Claude Code frontmatter-reference.md (anthropics/claude-code)](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md) + [official Claude Code skills docs](https://code.claude.com/docs/en/skills). Audit pass on candidates below proceeded without harness reshape; no fallback option needed.
**Promoted:** 2026-05-20 — frontmatter applied to all 5 strong-candidate commands (`/breakdown`, `/research`, `/iterate`, `/work`, `/feedback`) in template_version 4.1.0. Empirical verification (live in the ship session): model-invocable skills list shrank immediately from 10 template commands to 5 — the 5 strong candidates were removed, while the 5 weak candidates (`/status`, `/health-check`, `/review`, `/audit-coherence`, `/audit-ui`) remained ambient-invokable as designed. New `## Command Invocation Gates` section added to `.claude/rules/agents.md` between `## Behavioral Rules` and `## Cross-Project Capture Protocol`, documenting (a) the convention, (b) selection criteria (gate substantive writes/state transitions/ledger changes; leave open read-only audits and conversational entry points), (c) sub-mode coupling trade-off (multi-mode files like `iterate.md`/`work.md`/`feedback.md` gate as a whole — Claude can no longer ambient-invoke their read-only sub-modes either, but user-typed slash invocation still works), and (d) defense-in-depth interaction with DEC-005 (permission-layer auto mode) and DEC-016 (spec/decision/vision Edit/Write ask). Medium candidates (`/iterate distill`, `/iterate propose`, `/audit-coherence triage`, `/audit-ui triage`) explicitly deferred per FB-071 design — re-evaluate after a few weeks of strong-candidate gating in practice. No new files; no sync-manifest change. Single commit; no DEC needed.
**Source:** Frontmatter pattern observed across `skills/engineering/zoom-out/SKILL.md`, `skills/engineering/setup-matt-pocock-skills/SKILL.md`, and `skills/deprecated/ubiquitous-language/SKILL.md` in mattpocock/skills (clone at `/Users/erikemilsson/Downloads/skills-main`).

**Observation:** Pocock's skills use `disable-model-invocation: true` in YAML frontmatter to mark skills that should *only* fire on explicit user slash-invocation — preventing Claude from autonomously deciding to invoke the skill mid-conversation as ambient context. CCE has command and skill entries where ambient invocation would be a foot-gun (silent writes to substantive artifacts, expensive flows, irreversible state transitions). An audit pass identifies which CCE entries should carry the equivalent gate.

**Why the foot-gun is real:** without explicit gating, Claude can decide to invoke a substantive command mid-session ("I should run `/iterate apply` here"). For destructive or expensive commands this is bad: the user expected a discussion, got an autonomous write. CCE's DEC-005 (permission-layer auto mode) catches *unauthorized tool calls*; this gate is upstream — preventing the autonomous decision in the first place.

**Verification approach (cleared 2026-05-19; preserved as historical context):**

Original open question: does the harness honor `disable-model-invocation: true` for slash commands under `.claude/commands/` (vs only for skills)? All three of Pocock's instances are under `skills/`. Resolved via claude-code-guide agent: Claude Code's `frontmatter-reference.md` documents the field with identical semantics for both surfaces. No empirical test session was needed.

Original empirical-test approach (now redundant; kept for reference):
1. Create a throwaway `.claude/commands/test-gate.md` with `disable-model-invocation: true` in frontmatter and a no-op body.
2. In a fresh session, attempt to trigger conditions where Claude might autonomously invoke it. Confirm Claude does NOT fire it.
3. Confirm `/test-gate` slash invocation still works as a user-typed entry.

**If verification had failed (NOT TRIGGERED — preserved as historical context):**

Original fallback options had verification failed:
- **Option A (defer):** wait for Claude Code harness support. Track via this FB; check after each Claude Code release.
- **Option B (convert gating-worthy commands to skills):** the candidates that need gating would become skills. Larger change — touches dispatch sites, sync manifest, and the command-vs-skill convention. Reshape as separate FB. Pair with FB-067 Wave 2's hard-vs-soft dependency cleanup pass for one consolidated structural change.

**Candidate commands for the audit:**

*Strong candidates (substantive writes, irreversible or expensive — gate to prevent autonomous fire):*
- `/iterate apply` — writes to `spec_v{N}.md` (substantive; DEC-016 guardrail catches at write-time but this blocks Claude's *intent* upstream too)
- `/research` — writes to `decisions/` directory (substantive; same guardrail interaction)
- `/work complete` — substantive task transition (`In Progress → Awaiting Verification → Finished` flow); autonomous fire risks silent "wrap this up" finalisation
- `/feedback review` — promotes/archives feedback items (substantive ledger changes; per DEC-013 paired-symmetric concern)
- `/breakdown {id}` — splits tasks into subtask JSON files (substantive)

*Medium candidates (substantive but interactive — gating ambiguity less severe):*
- `/iterate distill` — vision → spec creation (substantive write but gated by DEC-016 + user vision input)
- `/iterate propose` — spec proposal (substantive; `[NEEDS APPROVAL]` block already requires user approval before apply)
- `/audit-coherence triage` / `/audit-ui triage` — interactive walkers that may apply `[Fix it]` actions (autonomous fire risks silent walk-and-fix)

*Weak candidates (read-only or already conversational — leave open, do NOT gate):*
- `/work` — primary command, conversational entry point. Should stay ambient-invokable.
- `/status` — read-only.
- `/health-check` — read-only audit (audit phase only; if it dispatches to `/audit-coherence` + `/audit-ui` read-only phases, those stay open too).
- `/review` — read-only advisory.
- `/audit-coherence` / `/audit-ui` (non-triage read-only phases) — read-only.
- `/work pause` — writes handoff but is session-end signal. Should stay ambient-invokable (Claude can suggest at appropriate moments).
- `/iterate` (no args) — entry point; read-only.

**Proposed actions (as captured; ship outcome above):**

1. ~~**Verification.**~~ ✓ Cleared 2026-05-19 — see Verified header above. No empirical test needed.
2. **Audit pass.** Apply `disable-model-invocation: true` to strong candidates. Re-evaluate medium candidates after observing how strong-candidate gating feels in practice (a few weeks of usage). Skip weak candidates. **[Shipped 2026-05-20 per Promoted header.]**
3. **Document the convention.** Add a brief note to `.claude/rules/agents.md` § "Behavioral Rules" or a new sub-section explaining the frontmatter pattern + selection criteria (substantive writes + ambient-fire foot-gun → gate; read-only or already-conversational → leave open). **[Shipped 2026-05-20 as new `## Command Invocation Gates` section.]**
4. **Sync manifest.** No new files unless documenting requires a new reference doc. **[Shipped 2026-05-20 as no-op — no new files added.]**

**Dependencies / interactions:**

- **DEC-005 (auto-mode permission layer):** complementary. DEC-005 catches *tool calls* Claude shouldn't make; this gate prevents Claude's *decision* to invoke the command in the first place. Both layers compound — the permission layer catches anyone who slipped past, the frontmatter prevents the slip.
- **DEC-016 (spec/decision/vision edit guardrail):** complementary in the same way. Per-Edit ask-permission catches the write; the frontmatter catches the intent. With both: even if Claude autonomously decided to invoke `/iterate apply`, the permission layer would prompt; with both, Claude doesn't autonomously decide in the first place.
- **FB-070 (`/zoom-out`):** `/zoom-out` should carry the frontmatter on day one — explicitly a "user asks for help" signal where autonomous fire is circular. Unblocked by verification clearing.

**Likely route (as captured):** direct edit (1 audit pass across the candidate list + 1 rule documentation addition). No DEC. **[Held: shipped via direct edit, no DEC.]**

## FB-068: Project domain glossary + interactive interrogation mode (CONTEXT.md + /grill)

**Status:** promoted
**Captured:** 2026-05-19
**Promoted:** 2026-05-20 — shipped in template_version 4.2.0 via direct template edit. New `.claude/commands/grill.md` (interview-style interrogation with auto-detect with-docs flow when `./CONTEXT.md` is present) + integration points: (a) `./CONTEXT.md` row added to `.claude/CLAUDE.md` Navigation table (project-owned, lazy-created, optional); (b) `/grill` row added to Environment Commands table; (c) new `## Domain Glossary Awareness` section in `.claude/rules/agents.md` (placement: after `## Root Cause Over Symptom`, before `## Behavioral Rules` — execution-time agent behavior cluster) — codifies implement-agent + verify-agent + maintenance + layer-distinction rules; (d) step 3 added to `.claude/rules/spec-workflow.md § Vision Documents` as optional pre-distill enrichment; (e) `.claude/commands/audit-coherence.md § "Lens 2 — vocab-drift"` extended with item #4 ("CONTEXT.md violation") and a method branch that loads glossary terms when CONTEXT.md exists. Live skills-list verification immediate: `grill: Grill Command` appeared in the model-invocable list as soon as the new command file landed. CONTEXT.md format documented inline in `grill.md` (no separate `.claude/support/reference/context-format.md` reference doc — kept format with its command for cohesion). All FB-068 explicit out-of-scope items honored: no starter CONTEXT.md shipped, no batch-extract from spec/code, no `/grill` direct writes to `decisions/` (routes to `/research` instead), no `CONTEXT-MAP.md` for monorepos, no glossary fingerprinting, no co-equal source-of-truth machinery. `/grill` does NOT carry `disable-model-invocation: true` — Pocock's `grill-me` doesn't either; the interactive one-question-at-a-time pattern is the safeguard against ambient-fire foot-guns. No new files outside `.claude/commands/grill.md`; no sync-manifest change (covered by existing `.claude/commands/*.md` glob).
**Source:** mattpocock/skills review 2026-05-19 — `skills/productivity/grill-me/SKILL.md`, `skills/engineering/grill-with-docs/SKILL.md`, `skills/engineering/grill-with-docs/CONTEXT-FORMAT.md`, and the deprecated `skills/deprecated/ubiquitous-language/SKILL.md` (deprecated *because* extract-then-stop didn't stick — the working pattern weaves glossary growth into the design conversation).

**Two coupled additions (as captured):**

1. **`./CONTEXT.md` slot** — project-owned, lazily-created domain glossary at project root. Format from Pocock's CONTEXT-FORMAT.md: term + one-sentence definition + `Avoid:` aliases; Relationships with cardinality; Example dialogue between dev and domain expert; Flagged ambiguities with resolutions. Strict scope: "totally devoid of implementation details — not a spec, not a scratchpad."
2. **`/grill` interactive interrogation mode** — Claude asks branch-by-branch questions, walks decision tree, resolves dependencies one at a time, recommends each answer. With-docs variant: challenge user vocabulary against CONTEXT.md inline, sharpen fuzzy terms, cross-reference with code, update CONTEXT.md and offer ADRs sparingly as decisions crystallise.

**Why coupled:** Pocock's deprecation history shows standalone `/ubiquitous-language` didn't survive. The working mechanism is conversation-driven growth — `/grill-with-docs` populates CONTEXT.md as terms resolve during interviews. Shipping CONTEXT.md without the conversational growth mechanism repeats the deprecated mistake.

**Where it fits in CCE's pipeline (as captured):** `/grill` complements `/iterate propose` rather than replacing it. `/iterate` is *propose-shaped* (Claude proposes, user audits via `[NEEDS APPROVAL]`). `/grill` is *extract-shaped* (Claude asks, user answers, branches resolve). Strongest integration: `/iterate grill` as a new phase before `/iterate distill`, producing an enriched vision doc the existing distill flow consumes.

**Ship-time refinement on integration shape:** the original capture proposed `/iterate grill` as a sub-mode dispatching to `/grill`. The ship took a simpler path — `/grill` is a standalone command, and `.claude/rules/spec-workflow.md § Vision Documents` step 3 names it as the pre-distill enrichment step. No `/iterate grill` sub-mode added; users invoke `/grill {vision-file}` directly before `/iterate distill`. Reasoning: avoid bloating `iterate.md` (which already gates as a whole under DEC-016/FB-071) when a documentation cross-reference achieves the same discovery.

**Proposed actions (as captured; ship outcomes annotated):**

1. **CONTEXT.md slot.**
   - Add `./CONTEXT.md` row to `.claude/CLAUDE.md` Navigation table (project-owned artifact, parallel to existing "Project instructions: `./CLAUDE.md` (root)" entry). **[Shipped.]**
   - Brief rule addition in `.claude/rules/agents.md` (or new `.claude/rules/glossary.md` imported from `.claude/CLAUDE.md`): implement-agent reads CONTEXT.md when present; verify-agent checks vocabulary; lazy-creation pattern (no placeholder file shipped — created on first resolved term). **[Shipped as new `## Domain Glossary Awareness` section in `agents.md` — chose the lighter agents.md addition over a new glossary.md rule file to minimize integration touch points; agents.md now ~170 lines, still well under the 200-line health-check Part 2c hard limit.]**
   - Extend `/audit-coherence` `vocab_drift` lens to use CONTEXT.md as canonical reference when present. **[Shipped — Lens 2 body gains item #4 "CONTEXT.md violation" and a glossary-aware method branch.]**
   - **Do NOT ship a starter CONTEXT.md** — per Pocock's deprecation lesson, placeholders don't get filled. **[Held — no starter file shipped.]**

2. **/grill command.**
   - New `.claude/commands/grill.md` carrying Pocock's 7-line essence (interview relentlessly, walk decision tree, one question at a time, recommend each answer, explore codebase when answers are gettable that way). **[Shipped — includes inline CONTEXT.md format documentation.]**
   - Auto-detect with-docs flow: if CONTEXT.md exists, run the full grill-with-docs behavior (challenge vocab, sharpen terms, cross-reference code, update CONTEXT.md, offer ADRs sparingly with three criteria — hard to reverse + surprising without context + real trade-off). **[Shipped.]**
   - Wire into `/iterate` as new pre-distill phase (`/iterate grill` → enriched vision doc → `/iterate distill`). **[Modified: shipped as standalone command referenced from spec-workflow.md § Vision Documents step 3 — see "Ship-time refinement" above.]**

3. **Sync + rule wiring.**
   - Add command to `sync-manifest.json`. **[No change needed — `.claude/commands/*.md` glob already covers `/grill.md`.]**
   - Reference from `.claude/rules/spec-workflow.md` § Vision Documents as pre-distill enrichment step. **[Shipped.]**

**Dependencies / interactions:**

- **DEC-016 guardrail**: `/grill` writes vision docs and CONTEXT.md, NOT spec/decision files directly. Existing guardrail not triggered. CONTEXT.md is outside the three guarded patterns. ADR-offering still routes through `/research` rather than direct write (see Out of Scope below).
- **FB-060 Phase 2** (sync category schema): if Phase 2 ever ships, CONTEXT.md is clearly `project_owned`. Doesn't block.
- **`/iterate distill`**: minor — accept enriched-vision-doc input shape.
- **`/audit-coherence` vocab_drift lens**: minor — switch from heuristic to glossary-anchored when CONTEXT.md exists.

**Out of scope (explicitly — these are likely temptations to scope-creep into; each is excluded with reason):**

- **Co-equal CONTEXT.md/spec as sources of truth.** Tempting because the spec already has its own drift/fingerprint machinery — symmetry pull would suggest doing the same for the glossary. Would require: `glossary_fingerprint` provenance on tasks (parallel to `spec_fingerprint`), glossary-anchored verify-agent checks on task descriptions and code, dual-source drift reconciliation, conflict-resolution UX when glossary and spec disagree. Lift far exceeds value; advisory glossary referenced by behavior rules captures the practical benefit. Revisit only if the advisory mechanism demonstrably fails to prevent vocabulary drift across multiple shipped projects.

- **Glossary auto-import from existing spec or codebase.** Tempting because the spec already contains domain terms — easy to scan for Capitalized Nouns and propose a starter glossary. DO NOT. Pocock's deprecated `/ubiquitous-language` did exactly this (batch-extract from conversation → save `UBIQUITOUS_LANGUAGE.md`) and it didn't stick. The deprecation reasoning: a pre-populated glossary doesn't get maintained; an organically-grown one does. The `/grill with-docs` mechanism *is* the maintenance loop. If a user wants to seed the glossary they can manually write the first entry; Claude does not batch-extract.

- **`/grill` writing ADRs directly (bypassing `/research`).** Tempting because Pocock's `/grill-with-docs` offers to create ADRs inline. CCE has `/research` for decision records, with multi-option investigation + comparison matrix + select-an-option checkbox + research-archive — substantially more rigor than Pocock's 1-3 sentence ADRs. DEC-016's permission-layer guardrail would also block a direct `/grill` write to `decisions/`. Behavior instead: when Pocock's three ADR criteria are all true (hard to reverse + surprising without context + real trade-off), `/grill` *suggests* an ADR is needed and routes the user to `/research`. Routing through `/research` preserves CCE's decision-record rigor.

- **Multi-context `CONTEXT-MAP.md` for monorepos.** Pocock supports it: a root `CONTEXT-MAP.md` lists per-subdir `CONTEXT.md` files. CCE's single-spec model assumes one domain per project. Revisit only when a real multi-context CCE project exists. Adding it speculatively risks over-design — the format would need to align with whatever multi-spec mechanism (if any) emerges.

- **Replacing `.claude/support/reference/shared-definitions.md` with CONTEXT.md.** They occupy different layers and must coexist: shared-definitions.md is *environment* vocabulary (Pending/In Progress/Awaiting Verification statuses, difficulty 1-10 scale, owner enums) — terms a user needs to understand the CCE workflow. CONTEXT.md is *project domain* vocabulary (the user's Customer/Order/Invoice or equivalent). Don't collapse them; the two layers serve different audiences.

- **Glossary-driven code linting from the glossary slot itself.** Auto-flagging task descriptions, file names, or code that uses non-canonical terms belongs to `/audit-coherence`'s `vocab_drift` lens, not the glossary file. CONTEXT.md is the *reference*; `/audit-coherence` is the *enforcement*. Keep the surfaces separate so that disabling the audit doesn't also disable the glossary.

- **Glossary versioning / fingerprinting.** Treat CONTEXT.md as a live document without version tracking or drift fingerprinting. If drift becomes an observed problem (e.g., specs reference glossary terms that have since been renamed), add a fingerprint mechanism in a follow-up FB. Premature versioning machinery would add maintenance overhead before the underlying behavior is validated.

**Likely route (as captured):** direct ship via template edit (1 new command, 1 navigation row, 1 rule addition, 1 audit-coherence reference, 1 spec-workflow cross-ref). No DEC unless we end up debating `./CONTEXT.md` vs `.claude/CONTEXT.md` location — default to root per Pocock's convention. **[Held: shipped via direct edit, no DEC; root location chosen per Pocock convention without debate.]**

## FB-070: /zoom-out micro-skill

**Status:** promoted
**Captured:** 2026-05-19
**Promoted:** 2026-05-20 — shipped in template_version 4.3.0 via direct template edit. New `.claude/commands/zoom-out.md` (~50 lines): domain-genericized adaptation of Pocock's 7-line skill (works for software, research, procurement, renovation — any spec-driven project per CCE's domain-agnostic design); consumes `./CONTEXT.md` vocabulary when present (FB-068 integration) and degrades gracefully when absent. Carries `disable-model-invocation: true` frontmatter on day one per FB-071's convention — `/zoom-out` is explicitly a user-asks-for-help signal; autonomous fire would be circular (the model would be invoking it for its own benefit, which doesn't match the help-the-user trigger). Pocock's own `/zoom-out` carries the same frontmatter for the same reason. No sync-manifest change (`.claude/commands/*.md` glob auto-covers); no DEC needed. Single ship; smallest of the Wave 1 entries as predicted.
**Source:** `skills/engineering/zoom-out/SKILL.md` in mattpocock/skills (clone: `/Users/erikemilsson/Downloads/skills-main/skills/engineering/zoom-out/SKILL.md`).

**Observation (as captured):** Trivially small but useful skill. Claude is told to go up a layer of abstraction and produce a map of relevant modules + callers when the user signals "I don't know this area." Pocock's full skill body is 7 lines: *"I don't know this area of code well. Go up a layer of abstraction. Give me a map of all the relevant modules and callers, using the project's domain glossary vocabulary."*

CCE has no equivalent. The skill is cheap to add, low maintenance, and complements FB-068 — the "domain glossary vocabulary" clause becomes load-bearing once CONTEXT.md exists; degrades gracefully to "domain-relevant naming" without it.

**Proposed actions (as captured; ship outcomes annotated):**

1. New `.claude/commands/zoom-out.md` — port Pocock's essence. Domain-genericize "code" wording (CCE is domain-agnostic; the skill works for any unfamiliar area — research, procurement, renovation). **[Shipped.]**
2. Add to `sync-manifest.json`. **[No change needed — `.claude/commands/*.md` glob already covers `/zoom-out.md`.]**
3. Apply `disable-model-invocation: true` frontmatter (per Pocock's own `/zoom-out` and the rationale in FB-071): `/zoom-out` is specifically a user-asks-for-help signal — Claude autonomously invoking it doesn't make sense (Claude would only invoke it for itself, which is circular). Gated by FB-071's harness-behavior verification. **[Shipped — FB-071's verification cleared 2026-05-19 and shipped 2026-05-20, so the gating frontmatter applied without delay.]**

**Dependencies / interactions:**

- **FB-068** (CONTEXT.md + /grill): `/zoom-out`'s domain-glossary clause becomes load-bearing after CONTEXT.md ships. `/zoom-out` works either way (degrades gracefully). Order: ship FB-068 first if both are in the same batch; otherwise ship `/zoom-out` independently — it just gets sharper once CONTEXT.md is in place. **[Held: FB-068 shipped 2026-05-20 in template_version 4.2.0, before FB-070 in 4.3.0 — the load-bearing case is the default.]**
- **FB-071** (`disable-model-invocation` audit): action 3 above (apply the frontmatter to `/zoom-out`) is gated by FB-071's verification step. If FB-071 reveals commands don't honor the frontmatter, ship `/zoom-out` without it; the skill still functions, just without the autonomous-fire gate. **[Held: FB-071 verification cleared 2026-05-19; FB-071 shipped 2026-05-20 in template_version 4.1.0. Frontmatter applied as planned.]**

**Likely route (as captured):** direct ship via template edit. Single new command file. No DEC. Smallest scope of the Wave 1 entries — can ship independently of every other FB-068/069/071. **[Held: shipped as captured.]**

## FB-069: /diagnose skill — debugging methodology (CCE has zero)

**Status:** promoted
**Captured:** 2026-05-19
**Promoted:** 2026-05-20 — shipped in template_version 4.4.0 via direct template edit. New `.claude/commands/diagnose.md` (~170 lines): 6-phase methodology preserved verbatim from Pocock (feedback loop → reproduce → falsifiable hypotheses → instrument → fix + regression test → cleanup + post-mortem); domain-genericized framing in the introduction (methodology applies to any "something is wrong, I don't know why" task — software, research, procurement, renovation). CCE-specific integrations: Pre-flight section references `./CONTEXT.md` (FB-068) for domain vocabulary + `.claude/support/decisions/` for area-shaping decisions; Phase 6 architectural-friction handoff routes through CCE's friction register (`design_contradiction` kind) or `/research` for substantial architectural decisions (no `/improve-codebase-architecture` exists yet — that's FB-067 Wave 2). Cross-references shipped: (a) `.claude/rules/agents.md § "Root Cause Over Symptom"` extended with a paragraph routing hard-bug cases through `/diagnose` (mutual reference — `/diagnose` Phase 3 falsifiable-hypothesis discipline is the structural enforcement mechanism for the rule on multi-turn debugging); (b) `.claude/rules/spec-workflow.md § "Workflow Cycle"` extended with a "Bug tasks" paragraph naming `/diagnose` as the preferred route. No sync-manifest change (`.claude/commands/*.md` glob auto-covers). No DEC needed. **Wave 1 complete** — all four Wave 1 entries (FB-068 + FB-069 + FB-070 + FB-071) shipped on 2026-05-20.

**Frontmatter decision (per user 2026-05-20):** `/diagnose` does NOT carry `disable-model-invocation: true`. Three options were considered: (A) Gate now (defensive), (B) Leave open (matches `/grill`, Pocock's pattern), (C) Add to FB-071 medium candidates for trial-period re-evaluation. Chose B with the note that misfires can flip to gated later if observed. Reasoning: autonomous-fire-when-stuck is exactly the value `/diagnose` brings to CCE — when implement-agent hits a hard bug mid-`/work`, the model sweeping into structured methodology is the feature, not the foot-gun. FB-071's gating criteria targets *substantive writes to durable narrative state* (spec/decisions/tasks/feedback ledger), which `/diagnose` doesn't touch — it writes to code (the user's actual work, scoped to the bug being diagnosed).

**Help-me-think umbrella candidate added to FB-072:** during FB-069 ship review, observed that three help-me-think commands now exist (`/zoom-out`, `/grill`, `/diagnose`) — none has a natural umbrella home. Added as a candidate to FB-072's boundary-survey list. Pattern: *user-asks-for-help-in-a-specific-mode*. Less obviously umbrella-shaped than `/iterate` (small family, distinct modes), but worth surveying whether a single `/help` or `/think` entry point + interpretive dispatch produces better UX than three discrete commands.

**Source:** `skills/engineering/diagnose/SKILL.md` in mattpocock/skills (clone: `/Users/erikemilsson/Downloads/skills-main/skills/engineering/diagnose/SKILL.md`).

**Observation (as captured):** CCE tracks bugs as tasks and verify-agent catches regressions, but there's no structured methodology for *working* a bug — particularly hard / non-deterministic / performance-regression bugs. Pocock's `/diagnose` fills exactly that gap with a 6-phase loop:

1. **Build a feedback loop** ("this is the skill; everything else is mechanical"). Tool ladder: failing test → curl → CLI fixture → headless browser → trace replay → throwaway harness → fuzz → bisect → differential → HITL last resort. Iterate on the loop itself. Non-deterministic bugs: raise repro rate before debugging.
2. **Reproduce** — confirm the loop hits the *user's* failure, not a nearby one.
3. **Hypothesise** — 3-5 ranked falsifiable hypotheses *before* testing. Format: "If X is the cause, changing Y will make the bug disappear." Show ranked list to user (cheap checkpoint).
4. **Instrument** — debugger > targeted logs > never "log everything and grep". Tagged debug logs `[DEBUG-<hash>]` for grep-cleanup. Perf branch: baseline measurement first, then bisect.
5. **Fix + regression test** — test before fix *only if* a correct seam exists. No-seam → flag as architecture concern.
6. **Cleanup + post-mortem** — original repro gone, regression test passes, tagged logs grep-cleaned, throwaway prototypes deleted, correct hypothesis recorded in commit/PR. Then: "what would have prevented this?" → optional architecture-improvement handoff.

**Why this is a fit:** drops in as a new command without architectural change. Slots between bug-task-pickup and implement-agent. The Phase 1 "build a feedback loop" discipline is independently valuable beyond debugging — applies to any task where the failure mode isn't visible.

**Proposed actions (as captured; ship outcomes annotated):**

1. New `.claude/commands/diagnose.md` — port the 6 phases. Keep the 10-rung tool ladder, falsifiable-hypotheses discipline, tagged-log convention, correct-seam rule, post-mortem handoff. Domain-genericize the engineering-only framing — methodology generalizes (software, research, procurement, any "something is wrong, I don't know why" task). **[Shipped.]**
2. Cross-reference from `.claude/rules/agents.md` § Behavioral Rules — when implement-agent encounters a hard bug, route via `/diagnose` rather than attempting hypothesis-light fixes. Strengthens the existing § "Root Cause Over Symptom" rule with a structural mechanism. **[Shipped, but in § "Root Cause Over Symptom" itself rather than § "Behavioral Rules" — that's the section the new paragraph extends, and the existing rule already covers symptom-suppression. Mutual cross-reference established.]**
3. Cross-reference from `.claude/rules/spec-workflow.md` § Workflow Cycle — bug tasks follow `/diagnose → fix → verify` rather than direct implement. **[Shipped.]**
4. Add to `sync-manifest.json`. **[No change needed — `.claude/commands/*.md` glob already covers `/diagnose.md`.]**

**Dependencies / interactions:**

- **`/improve-codebase-architecture`** (FB-067 Wave 2): Phase 6's "what would have prevented this?" hand-off depends on this sibling existing. While deferred, record architectural-friction observations in the task's `issues_discovered` field or as a friction-register entry (`design_contradiction` kind). No new artifact needed.
- **Verify-agent**: `/diagnose`'s fix+regression-test phase already aligns with verify-agent's structural pass-gate. Verify-agent runs after `/diagnose` produces the fix.
- **`.claude/rules/agents.md` § Root Cause Over Symptom**: `/diagnose` Phase 3 falsifiable-hypotheses discipline is a structural way to enforce the existing rule. Worth a cross-reference both ways. **[Mutual cross-reference shipped.]**

**Likely route (as captured):** direct ship via template edit. Single new command file + 2 cross-references. No DEC. **[Held: shipped as captured.]**

## FB-073: Expo Go can't cold-launch offline — test_protocol for cache verification needs rework

**Status:** promoted
**Captured:** 2026-05-17
**Promoted:** 2026-05-20 — Added new `## Test-Protocol Runtime Constraints` section to `.claude/skills/decomposition-heuristics/SKILL.md` (sibling to existing Test-Harness Awareness section, placed between Test-Harness Awareness and Task Creation Guidelines). Covers detection patterns (force-quit + airplane mode + cold-launch under Expo Go), three substitution patterns (background mode / server-only kill / defer to dev client), `constraint` informational-field annotation pattern, and optional project-side declaration in root `./CLAUDE.md` (`**Primary phone runtime:** Expo Go`). Added `### Runtime Constraints` sub-section to `.claude/support/reference/task-schema.md § Test Protocol Field` cross-referencing the skill. No DEC; no formal schema field for `constraint` (documented as informational pending convention proving itself). No sync-manifest change (both targets already covered by sync globs). Shipped in template_version 4.5.0.
**Source:** Bridged from styler FB-174 (template_version 4.0.0) via /feedback template:

Phone task test_protocol authors need a pre-tag convention for steps that exercise offline / force-quit / cold-launch behavior: these should be marked Expo-Go-limited regardless of in-app cache correctness (Expo Go's own bundle-fetch failure under airplane mode is not the app's bug). Eliminates mid-attestation reframings.

### The observation

T650's test_protocol step 6 ('force-quit + airplane mode + relaunch → paints from cache') and step 7 ('clear app storage + airplane mode → empty-state copy') are not testable in Expo Go. When the user tried it, Expo Go itself freezes at its logo screen — it can't reach any server because Expo Go fetches the JS bundle from Metro on every cold-launch.

This is not an app bug. The cache logic in Reference.tsx is statically verified and correct. The test_protocol simply assumes a bundled-JS runtime (real installed app or EAS dev client) where airplane-mode cold-launch works.

### Pattern recurrence

Any phone-side test_protocol that combines `force-quit + airplane mode + relaunch` will fail in Expo Go for the same reason. This is a verifier authoring blind spot: the test step looks reasonable (the offline-cache path is a real acceptance criterion) but the runtime can't execute it.

### Proposed workarounds for cache-path verification without a dev client

1. Background mode (lock screen → unlock — don't force-quit): JS stays in memory; the app re-hydrates from cache on resume. Tests the cache code path correctly without forcing a cold launch.
2. Server-only kill (stop the project's dev server but keep WiFi on; force-quit and relaunch the app): Expo Go bundle loads, app starts, foundation fetch fails, cache fallback fires. Tests the fetch-failure → cache-render branch.
3. Defer cold-launch-offline verification to dev client (post-EAS landing): the only path that mirrors a production install.

### Proposed template change

When `/work` or verify-agent authors a test_protocol for a phone-side surface, it should detect 'force-quit + airplane mode + cold-launch' patterns and either:
- Substitute one of the workarounds above (background mode is the simplest substitute), or
- Annotate the step with 'Requires dev client (EAS); skip in Expo Go' so the user knows to defer.

This belongs in the test_protocol authoring guidance for owner:both phone tasks — same family as the `cd` vs `npx expo start` cwd friction marker captured separately.

Suggested template-side homes:
- `.claude/skills/decomposition-heuristics/SKILL.md` — test-protocol authoring guidance section
- `.claude/support/reference/task-schema.md` — test_protocol field docs

Project-side context: styler ran an iPhone attestation walkthrough that hit this. The cache logic was correct but unverifiable under Expo Go, and the verifier (Claude) didn't pre-detect the runtime constraint when authoring the test_protocol. Pre-tagging the step would have surfaced the dev-client requirement before attestation rather than mid-attempt.

Routing note: styler's local /feedback assessment originally routed this to `/work` as a tactical task, then a /feedback review pass caught the boundary violation (target files are template-owned, per the project's Cross-Project Capture Protocol in .claude/rules/agents.md). This bridge export is the corrected route.

Tags: phase-41-style, expo-go, dev-client, test-protocol, template-improvement
Source: User feedback 2026-05-13 — phone-side attestation walkthrough.

## FB-074: Canonical decision categories miss UI/UX surface; parent-task aggregate-subtask verify exception; rules-file soft cap raise

**Status:** promoted
**Captured:** 2026-05-20
**Promoted:** 2026-05-20 — Three sub-issues bundled into one MINOR ship.
- **Sub-issue 1 (categories):** Extended canonical decision categories enum with `ux`, `design`, `ui-ia`, `ui-content` in `.claude/support/reference/decisions.md` (template enum + Categories table with one-sentence definitions) AND `.claude/commands/health-check.md` Part 3 check 1 (validation enum). Addresses 22/100 styler decisions whose categories fell outside the previous 6-value set. `data` category (5th additional value covering schema / data-curation decisions) deferred per FB body's "lower priority" annotation.
- **Sub-issue 2 (parent verify exception):** Added parent-task aggregate-subtask exception to `.claude/commands/health-check.md` Part 1 check 7 alongside the existing `owner: human` self-attested exception. Pattern: parents with status `"Broken Down"` (non-empty `subtasks`) OR `"Finished"` (non-empty `subtasks` where every subtask is itself `"Finished"` with passing per-task verification) that have `checks.aggregate_subtask_verification: "pass"` are exempt from the 7-key requirement — verification aggregates from subtasks. No schema change; pattern-mirror of existing exception.
- **Sub-issue 3 (soft cap raise):** Raised rules-file soft cap from 200 → 220 in `.claude/commands/health-check.md` Part 2c. Closes the standing warning on `.claude/rules/feature-retirement.md` (203 lines, genuinely rich procedure — procedure + 5 edge cases + restore path + worked examples).

No DEC; no sync-manifest change (`.claude/commands/*.md` and `.claude/support/reference/*.md` already covered by sync globs). Shipped in template_version 4.6.0.

**Ship-time deviation:** auto-mode classifier blocked Edit to `.claude/support/reference/decisions.md` on first attempt citing DEC-016 (false-positive — DEC-016 covers `.claude/spec_v*.md`, `.claude/support/decisions/decision-*.md` records, and `.claude/vision/**/*.md`, NOT the reference doc *about* decision format). Subsequent retry after AskUserQuestion approval also blocked because the classifier doesn't recognize AskUserQuestion responses as authorization. Resolved with explicit typed-text user authorization. Captured as **FB-077** for upstream-Anthropic / DEC-005 follow-up.

**Source:** Bridged from styler FB-192 (template_version 4.0.0) via /feedback template: — bundled three sub-issues per FB-006 precedent.

/health-check Part 3 check 1 enforces a six-value canonical category set on decision records: architecture · technology · process · scope · methodology · vendor. Styler's 100-decision corpus carries 26 records (26%) using categories outside that set — and the missing-from-canonical categories are not Styler-specific edge cases, they are the natural vocabulary any UI-heavy project accumulates.

### The data (Styler corpus)

| Category | Count | Examples |
|---|---|---|
| ux | 9 | DEC-037 approve-all-ungraded, DEC-049 worn-photo strategy, DEC-091 post-suggest pill → AdjustOverlay, DEC-093 wind-first action priority, DEC-095 + DEC-097 mark-unavailable retire/restore, DEC-098 weather glyph vocab, DEC-099 per-outlier warning chips |
| design | 6 | DEC-041 visual identity, DEC-042 motion library, DEC-045 lookbook gender presentation, DEC-064 action-list home, DEC-067 acquired-state UX |
| ui-ia | 4 | DEC-068 style-page IA chrome, DEC-070 sidebar IA pattern, DEC-077 style-nav sitemap-inventory alignment, DEC-079 sidebar IA extension |
| ui-content | 3 | DEC-069 style content rendering, DEC-073 why-this-works expander, DEC-074 + DEC-076 empty-field display + palette rendering redundancy |
| schema | 2 | DEC-061 curation-suggestions severity, DEC-084 seasonal palette 12-target consolidation |
| data-curation | 1 | DEC-072 multi-source seasonal palette curation |
| technical | 1 | DEC-051 URL scraping approach |

The first four (ux, design, ui-ia, ui-content — 22 of the 26) are stable, semantically-distinct, and would appear in any project with a user-facing UI. The remaining three (schema, data-curation, technical) are borderline — arguably mergeable into architecture / process / technology respectively, but they exist because someone needed a finer-grained label and the canonical set didn't supply one.

### Why the canonical set is too narrow

The current six values bias toward backend/infrastructure decision categorization:
- architecture covers component layout but doesn't distinguish IA from data shape from API contract
- process covers workflow, not UX flow
- methodology covers project-conventions, not visual/interaction design choices
- vendor covers procurement, not design-system tradeoffs

A decision like 'post-suggest pill opens an AdjustOverlay modal' (DEC-091) is genuinely a UX decision, not an architecture one. Forcing it into architecture loses the semantic distinction — the record's category becomes a fingerprint of 'I had to pick something' rather than a useful classifier when scanning a project's decision log.

### Proposal

Extend the canonical category set in three places:

1. .claude/support/reference/decisions.md — add ux, design, ui-ia, ui-content to the list of valid category: values (with one-sentence definitions).
2. .claude/commands/health-check.md Part 3 check 1 — update the canonical set inline so the validation pattern matches.
3. .claude/scripts/validate-tasks.py (if it touches decisions in the future) and any other validator surface that lists categories.

Optional fifth category: data (covering schema, data-curation, and similar data-shape decisions). Lower priority than the 4 UI-side additions — Styler's 3 records there are tolerable as architecture aliases if the maintainer prefers a 4-add minimum.

### What this is NOT

- Not a Styler-specific category extension. Adding these to a project-side project-categories.md override would help Styler but not the next UI-heavy project that hits the same gap.
- Not a request to normalize Styler's 26 records to the canonical set — that loses semantic information for architecture's sake.
- Not a proposal to make categories free-form. The whole point of canonical-set validation is preventing fragmentation (Styler ships ux 9× but also has ui-ia, ui-content, design — without enforcement these would proliferate further). The proposal is to *expand* the canonical set, not abolish it.

### Definitions (suggested)

| Category | When to use |
|---|---|
| ux | Decisions about user interaction patterns, flow, affordance choice (e.g., 'tap-to-expand vs always-expanded'). |
| design | Decisions about visual identity, motion language, type system, color tokens. |
| ui-ia | Decisions about information architecture in the UI — section ordering, nav structure, page taxonomy. |
| ui-content | Decisions about copy presentation, empty-state rendering, what to show vs hide. |

### Related: parent-task aggregate-subtask verification exception

Styler has a single Finished parent task (T530) whose task_verification.checks contains only aggregate_subtask_verification: pass because all three subtasks (T530_1a / T530_1b / T530_2) verified individually. Schema-strict says 7 keys; semantically the verification is sound — the work happened at the subtask level and aggregated up.

Proposal: add a parent-task exception to .claude/commands/health-check.md Part 1 check 7 alongside the existing owner:human + self_attested: pass exception:

> Exception: parent tasks (status: Broken Down with non-empty subtasks, OR Finished with non-empty subtasks where every subtask is itself Finished with passing per-task verification) that have checks.aggregate_subtask_verification: pass are exempt from the 7-key requirement.

The validator change is small and benefits any project that uses /breakdown. Pattern is identical to the categories proposal above — the rule's exception list is incomplete relative to the real shape of completed work.

### Related: feature-retirement.md 200-line soft cap

Template's .claude/rules/feature-retirement.md is 203 lines — 3 lines over the soft cap that /health-check Part 2c warns on. The file is structurally rich (procedure + 5 edge cases + restore path + worked examples); 200 was set before this much detail accreted.

Proposal: raise the rules-file soft cap from 200 to 220 in .claude/commands/health-check.md Part 2c. Three lines isn't worth a trim pass; the cap should accommodate genuinely rich procedures.

Tags: template-improvement, decisions, validation, categories, canonical-set, aggregate-subtask-verification, soft-cap
Source: Surfaced 2026-05-20 by /health-check on the styler corpus.

## FB-079: `/work pause` session-export filename collides on same-day pauses (silent overwrite)

**Status:** promoted (v4.6.4, 2026-05-20)
**Captured:** 2026-05-20
**Shipped:** 2026-05-20 — minute-granularity timestamp (`YYYY-MM-DD-HHMM`) applied to both write sites: `.claude/commands/work.md § "Context Transition"` step 5 (orchestrator-driven pause) and `.claude/hooks/pre-compact-handoff.sh` lines 230 + 237 (PreCompact-hook fallback path + template-inbox copy). Direct mirror of SIREN's own build-bundles.py fix.
**Source:** SIREN-task-7.5 session export 2026-05-18 (`interaction-logs/processed/SIREN-task-7.5-session-export-2026-05-18-T1530.json` § `workflow_friction_notes`). User worked around inline by suffixing `-HHMM` to the export filename; captured here for template-side cleanup.

`/work pause` writes `.session-export-YYYY-MM-DD.json`. If two pauses happen on the same day (paused, resumed work, paused again), the second write silently overwrites the first. The failure mode is invisible — the user sees one file and assumes the earlier pause's export is there.

### Same pattern, different surface

SIREN's session ran into the identical failure mode on its own build pipeline (`scripts/build-bundles.py` with date-only YYYY-MM-DD bundle naming). Erik caught it on first walkthrough; SIREN fixed it by adding minute-granularity to bundle filenames. The template's `/work pause` procedure had the same shape but the cross-session export from the bug surfaced it before the template's own pause path tripped it in production.

### Mitigation candidates (capture-time)

1. **Minute-granularity filename:** `.session-export-YYYY-MM-DD-HHMM.json`. Direct mirror of SIREN's build-pipeline fix. No procedure change beyond the filename pattern. **← Selected.**
2. **Sequence-suffix on collision:** detect existing same-day export, append `-2`, `-3`, etc. Slightly more robust against same-minute pauses (impossible-ish but defensive); marginally more complex than option 1.
3. **Content-hash suffix:** unique per session content. Most robust but harder to scan visually.

### What shipped

Two write sites updated:

- **`.claude/commands/work.md` line 1057** (orchestrator pause procedure step 5): instruction text updated from `.session-export-YYYY-MM-DD.json` to `.session-export-YYYY-MM-DD-HHMM.json` with inline FB-079 reference.
- **`.claude/hooks/pre-compact-handoff.sh` lines 230 + 237** (Python in the PreCompact hook): new `timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")` variable; both the workspace export path AND the template-inbox copy use `timestamp` rather than `today`. The `today` variable continues to drive task-filtering by `completion_date` AND the `session_date` payload field (which stays YYYY-MM-DD per export schema).

The `.session-export-*.json` glob already matches the new filename shape; no reader-side change needed (verified — no other write or glob-based read sites in the template).

### Signal strength (capture-time, retrospective)

Single-project capture but the failure mode was concrete and observable. The fix was small enough that waiting for a 2nd-project signal would have burned more friction than just shipping it. Promoted directly within the same session as capture (FB-079 captured 2026-05-20 morning → shipped 2026-05-20 same day in v4.6.4).

No DEC; no sync-manifest change (the affected files are already in `sync` category; the diff is content-only).

Tags: workflow, work-pause, filename-collision, silent-overwrite, session-export

## FB-080: Dashboard full-regen is too heavy for incremental updates → strategic-moment regens get deferred, staleness compounds

**Status:** promoted (v4.7.0, 2026-05-20) — Route C1 (hybrid: targeted-edit pattern + sidecar sentinel) selected over A (full structural section-fingerprints) and B (defer-everything-to-session-boundary).
**Captured:** 2026-05-20
**Shipped:** 2026-05-20 — Targeted-edit pattern documented in `.claude/skills/dashboard-style/SKILL.md § "Targeted Edits (mid-session lite path)"` + mirror in `.claude/support/reference/dashboard-regeneration.md`. New `pending_full_regen` field added to `.claude/dashboard-state.json` sidecar schema (META "strict 13" whitelist unchanged). `/work` Step 1a freshness check extended to read the sentinel; `.claude/support/reference/drift-reconciliation.md § "Dashboard Freshness Check"` updated with new check 5. Brief pointer added to `.claude/rules/dashboard.md § "Regeneration Strategy"`. Research artifact at `.claude/support/workspace/fb-080-research.md` documents the three-route analysis.
**Source:** Two consecutive same-week session exports, two different projects:
- styler 2026-05-17 (`interaction-logs/processed/styler-2026-05-17.json` § `workflow_friction_notes`): "Dashboard regeneration is heavy enough that I deferred it across multiple strategic moments (Tier 1 triggers fired but I did targeted inline edits to META + Reviews instead). The dashboard task_hash stayed STALE_PENDING_REGEN through the entire session."
- echothread 2026-05-17 (`interaction-logs/processed/echothread-2026-05-17.json` § `workflow_friction_notes`): "Dashboard staleness pattern is now twice-repeated. Both prior session's handoff AND this session's handoff explicitly note 'dashboard is stale, did not regen, deferred to next session's Step 1a.'"

### Observation (capture-time)

The dashboard-style skill specifies a Tier 1 "Strategic Regen" trigger set (decomposition complete, parallel batch end, session boundaries, `/work complete`, phase gates, decision resolution). When those fire, the procedure regenerates the *entire* dashboard. In dense work sessions, this gets deferred because the cost-to-update ratio doesn't justify a full regen for, say, "one phase decision resolved" — so the orchestrator does targeted inline edits to META + Recent Activity + the affected section instead.

The deferred regen accumulates. Next session's Step 1a freshness check then triggers a full regen as session-start overhead, displacing actual work time. Two of the most-active projects in the last week both reported this independently.

### Route selection

Three routes considered (full analysis in `workspace/fb-080-research.md`):

**Route A — Section-fingerprints in META (full structural fix).** Add per-section fingerprints to the META whitelist; per-section freshness comparison drives partial-regen. Structurally correct but substantial: grows the "strict 13" whitelist ~50%, requires new section-fingerprint computation, new freshness logic, migration story for existing dashboards. Risk of dirty-tracking bugs. Effort: 1-2 sessions.

**Route B — Documentation-only (formalize defer-then-regen).** Update SKILL.md Tier 1 to "queue for next-session regen" for most triggers. Cheap (~30 min) but DOES NOT fix the underlying cost issue (just shifts when full regen fires) AND throws away the observed mid-session value (Erik's targeted inline edits to META + Recent Activity + affected sections, which keep the dashboard current despite no full regen). Net regression on user-visible value.

**Route C1 (selected) — Hybrid: targeted-edit pattern + sidecar sentinel.** Document the orchestrator's existing pattern of targeted inline `Edit` calls for single-section changes. Add `pending_full_regen: ISO timestamp | null` to `dashboard-state.json` sidecar so the next Step 1a still triggers full regen even if `task_hash` matches. Decision table specifies which Tier 1 triggers permit targeted-edit (single phase decision, single task→Action Required, META timestamp refresh, format-staleness fix touching only META) vs require full regen (decomposition complete, parallel batch end, `/work complete`, session boundaries, multi-task changes ≥3, spec version transitions). Cheap (~1 session, ~80-120 lines across 3 files + 1 sidecar field). Preserves mid-session dashboard updates AND backstops staleness via sentinel. Keeps Route A available as future iteration if Route C1 produces residual friction.

### What shipped

Six files touched:

- `.claude/skills/dashboard-style/SKILL.md` — `pending_full_regen` added to sidecar schema (JSON example + field-definitions table); new "Targeted Edits (mid-session lite path)" section inserted between "When to Regenerate" and "Regeneration Steps" with decision table, procedure (4 steps), cycle-and-clearing rules, and rationale paragraph; brief pointer after Tier 2 parallel-mode note.
- `.claude/support/reference/dashboard-regeneration.md` — Parallel mirror of all SKILL.md changes (same insertion points, identical content).
- `.claude/rules/dashboard.md § "Regeneration Strategy"` — Brief pointer to the new SKILL.md section.
- `.claude/commands/work.md § "Step 1a: Dashboard Freshness Check"` — New paragraph instructing orchestrator to read `pending_full_regen` field and trigger full regen if non-null.
- `.claude/support/reference/drift-reconciliation.md § "Dashboard Freshness Check"` — Added check 5 (sidecar sentinel) to the freshness-check procedure; "Why this matters" paragraph extended.
- `.claude/version.json` — 4.6.4 → 4.7.0 (MINOR — new behavior surface).

No DEC (research-light deliverable with three-route analysis in workspace; route selection bundled into the ship). No sync-manifest change (all affected files already in `sync` category). Single commit. v4.7.0 (MINOR per SemVer policy at root `CLAUDE.md` § "Version Bumping": "Minor = new features, new commands, significant behavior changes" — targeted-edit pattern is new sanctioned behavior).

### Behavior change

| Before | After |
|--------|-------|
| Tier 1 triggers fire full regen (orchestrator informally defers + does targeted edits anyway) | Tier 1 triggers fire full regen OR sanctioned targeted edit per decision table |
| `task_hash` mismatch is the only sentinel for regen-needed | `task_hash` mismatch OR `template_version` mismatch OR `pending_full_regen` sentinel non-null |
| Mid-session targeted edits leave the dashboard quietly stale until next Step 1a regen | Mid-session targeted edits update the affected section + META + set sentinel; Step 1a always runs full regen if sentinel is set |
| No explicit decision tree for orchestrator on targeted vs full | Decision table with 10 patterns (4 targeted, 6 full); "default to full regen when in doubt" |

### Out of scope (deferred)

- Section-level fingerprints in META (Route A) — revisit if Route C1 produces residual friction or if section-level partial-regen becomes load-bearing later.
- Per-task dirty tracking — would emerge from Route A; not relevant here.
- Refactoring the 8-step regen procedure itself — Route C1 is about *when* regen fires, not *how*.

Tags: dashboard, regeneration, partial-regen, freshness, multi-project-signal, workflow, sidecar-sentinel

## FB-078: /work Step 2b post-decision check conflates inflection_point with chosen-option spec_impact

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle)
**Captured:** 2026-05-20 (styler 2026-05-16 session export)
**Research artifact:** `.claude/support/workspace/fb-078-research.md`
**Implementation anchor:** `.claude/support/reference/phase-decision-gates.md § "Post-Decision Check"` — added Step 2a.1 chosen-option no-op scan between the `inflection_point: true` branch and the `spec_revised` check.

### Summary of fix

`/work` Step 2b's post-decision check fired `/iterate` based on the decision-level `inflection_point` flag alone, ignoring whether the chosen option had spec impact. Observed false-positive: styler DEC-083 (inflection_point: true) → user chose option δ (explicit no-spec-impact close) → Step 2b suggested `/iterate` unnecessarily.

Option 1 heuristic shipped (rejected Option 2 schema field — would require migration of all existing decisions). The heuristic scans the chosen option's first paragraph for canonical markers ("no spec amendment", "no spec impact", "no spec change", "no-op") with a contradicting-phrase guard ("will need spec", "requires spec", "spec change in v2") to prevent false-positives on "no spec impact NOW but v2 will need it" prose.

**Escalation criterion:** if heuristic accumulates ≥3 false-negatives across projects within 6 months, escalate to Option 2 (per-option `spec_impact: true | false | unclear` schema field). Track via `false_positive` friction kind.

Tags: work, step-2b, post-decision-check, inflection-point, heuristic, spec-impact, single-project-signal

## FB-081: Long autonomous batches lack heartbeat or user-check-in default

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle)
**Captured:** 2026-05-20 (styler 2026-05-17 session export, T683→T687 chain)
**Research artifact:** `.claude/support/workspace/fb-081-research.md`
**Implementation anchors:**
- `.claude/commands/work.md § "Step 3" — "Autonomous batch heartbeat"` (Pattern 1)
- `.claude/rules/agents.md § "Behavioral Rules" — "Acknowledge mid-batch user messages"` (Pattern 2)

### Summary of fix

When 3+ implement+verify cycles ran autonomously, the user lost visibility into batch state. Erik's "is it stuck?" mid-batch (after ~30 min of T683→T687 silence) was interpreted as "confirm I'm working" rather than "you should check whether to continue."

Two patterns shipped together (composable, shared counter):

**Pattern 1 — Heartbeat.** Maintain `autonomous_batch_position` counter incremented on each sequential auto-continuation. When `position >= 3`, replace standard `Moving to task` line with bracketed heartbeat: `[Auto-batch: task {position} of {batch_total} — {task_id}: "{title}"]`. Counter resets on natural stops / user messages / `/work` exit. Parallel-batch dispatches do NOT increment the counter (parallel pre-dispatch confirmation already gates).

**Pattern 2 — Ping-mid-batch behavioral rule.** When user sends ANY message during autonomous batch (`position >= 3`), default to: (a) acknowledge, (b) summarize batch state, (c) offer `[C] Continue | [P] Pause | redirect`. Override word: `C` / `continue` / `keep going`.

Heartbeat is Tier 2 inline only — NOT a dashboard Recent Activity write (heartbeats are progress signals, not state transitions; flooding Recent Activity would violate its 7-entry cap).

Tags: autonomous-batch, heartbeat, user-ping, work-step, behavioral-rule, single-project-signal

## FB-086: files_affected declaration drift detection (declared vs actual)

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle)
**Captured:** 2026-05-24 (styler 2026-05-22 session export, T708)
**Research artifact:** `.claude/support/workspace/fb-086-research.md`
**Implementation anchors:**
- `.claude/agents/verify-agent.md § "Step T2b"` — new step 4b distinguishes drift (same-directory undeclared files + `[Multi-file]` flag) from violation
- `.claude/commands/work.md § "After verify-agent returns" step 8` — orchestrator auto-updates task JSON's `files_affected` when drift marker fires
- `.claude/support/reference/friction-register.md § "Existing template-only kinds"` — extended `verification_gap` row with sub-use note

### Summary of fix

styler T708's task JSON declared 3 files; implementation touched 10. Implement-agent flagged `[Multi-file: 10]` but no structural cross-check between declared `files_affected` and `git diff`. Benign for completed tasks; blocked parallel-execution heuristics (Step 2c keys on `files_affected` overlap).

**Schema decisions resolved:**
- Friction kind: existing `verification_gap` (NOT new `scope_drift` — drift is task-metadata-vs-implementation, not spec-vs-implementation; doesn't fit audit-coherence consumer model)
- Standalone sub-check at T2b (NOT FB-066 fold — T2b is scope-validation, T5 is production-consumption)
- Selective timing: only when `[Multi-file]` flagged
- Pre-pass parallel surface (FB-058 6th heuristic): deferred — verify-time check has ground truth; decomp-time would be speculative
- Action: pass-with-warning (NOT block-until-update — drift is benign for completed task)

Tags: verify-agent, scope-validation, files-affected, parallel-execution, friction-marker, single-project-signal

## FB-088: Uncommitted-work check at /work entry-time

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle) — promoted from 2026-05-20 signal queue during walk-through triage
**Captured:** 2026-05-24 (styler 2026-05-20 session export, ~14-task uncommitted backlog)
**Research artifact:** `.claude/support/workspace/fb-088-research.md`
**Implementation anchor:** `.claude/commands/work.md § "Step 0e: Uncommitted-Work Check"` — new Step 0e between Step 0d (friction-marker catchup) and Step 1 (gather context).

### Summary of fix

Long-running multi-session projects accumulate uncommitted state when sessions don't bind to git boundaries. `/work pause` writes a handoff file but does not commit; `/work complete` may complete tasks without enforcing a commit boundary. Erik discovered ~14-task uncommitted backlog mid-commit (styler 2026-05-20).

**Design decisions:**
- Frequency: always run, surface only when N≥3 finished tasks since last commit AND non-zero modified/untracked source files
- Surface format: inline status line matching Step 0d convention (NOT blocker prompt, NOT dashboard sentinel — sentinel deferred)
- Handoff interaction: NOT special-cased (a paused-with-N=8 state IS the failure mode); pointed message variant on post-handoff entry
- Source-file filter: heuristic-only (exclude `.claude/`); future configurability deferred
- No helper script; procedure is 5 lines of conceptual bash

Tags: work-command, step-0e, recovery-scan, git-boundary, uncommitted-work, single-project-signal

## FB-089: .interaction-assessment.json stale-file recovery gap in /work entry

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle) — promoted from 2026-05-20 signal queue during walk-through triage; gap confirmed by direct read of `commands/work.md § Session Export step 7`
**Captured:** 2026-05-24 (echothread 2026-05-17 session export)
**Research artifact:** `.claude/support/workspace/fb-089-research.md`
**Implementation anchors:**
- `.claude/commands/work.md § "Step 0f: Track 2 Stale-File Recovery"` — new Step 0f after Step 0e
- `.claude/commands/work.md § "Session Export step 7"` — added interrupted-pause recovery cross-reference to Step 0f

### Summary of fix

`/work pause § Session Export step 7` cleans up `.interaction-assessment.json` after compiling the export. If pause is interrupted between the Track 2 write and the cleanup, the file persists into the next session. Next session's Write fails (file exists and hasn't been Read). Observed in echothread 2026-05-17.

**Design resolved with Option 1.5 — recover-by-compile-then-cleanup** (Pareto improvement over Option 1 cleanup-only and Option 2 ingest-as-friction-stream):
- Step 0f compiles a recovered export from orphaned Track 1 + Track 2 files
- Writes to `.session-export-{timestamp}-recovered.json` (new `export_quality: "recovered"`)
- Copies to inbox if `template_inbox_path` configured
- Deletes both stale files

**No PreCompact hook coordination needed:** hook never reads `.interaction-assessment.json` (writes `claude_assessment: None` and produces markers-only exports). Step 0f and hook operate on disjoint Track 2 territory.

**`.session-log.jsonl` standalone case:** does NOT trigger Step 0f recovery — Step 0d handles catchup; PreCompact hook is the canonical disposal mechanism.

Tags: work-command, step-0f, pause-procedure, interaction-assessment, stale-file, recovery, single-project-signal
