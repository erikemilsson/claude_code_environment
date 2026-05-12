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
