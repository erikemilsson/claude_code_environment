# Feedback Log

Items are captured via `/feedback` and triaged via `/feedback review`.

---

## FB-010: Subagents spawned by /work cannot write `.claude/tasks/` or spawn nested Task tools

**Status:** ready
**Captured:** 2026-04-07
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

**Possible directions to investigate (not decided — for triage):**
- Document the limitation in `implement-agent.md` and `verify-agent.md` so the agents know to return structured reports rather than retrying writes
- Update `/work` Step 4 "If Executing (Parallel)" to explicitly say "the coordinator handles 6a/6b for parallel agents in environments where subagents lack write access to `.claude/`"
- Investigate whether the harness sandbox can be relaxed for subagents (additional working directories should propagate from parent to spawned Task agents — currently they don't seem to)
- Add a coordinator helper procedure for "persist verify-agent structured report → task JSON" since the same edit shape is repeated for every task
- Reconsider whether implement-agent should write task JSON at all — maybe the orchestrator should always own task state transitions, leaving agents to focus purely on code work

Worth flagging: this issue is not visible from a single sequential dispatch (the user sees "task verified, marked Finished" without the orchestrator's manual work being obvious). It only becomes painful at parallel-batch scale, which is the workflow `/work` already optimizes for.

## FB-011: Explore scripts as alternative to commands or within skills folders

**Status:** ready
**Captured:** 2026-04-08
**Refined:** 2026-04-14 — Identify command procedures where a deterministic script would outperform LLM-executed natural-language instructions — starting with the dashboard, where output variation across regenerations makes the artifact harder to comprehend. Scripts could live alongside commands or inside skills folders if that's a valid pattern. Gains: (1) consistency of standardized artifacts, (2) reduced error rate from procedure drift, (3) lower token cost. Scope is exploratory — inventory candidates and propose which procedures to extract before committing.
**Assessed:** 2026-04-14 — Primary target is dashboard regeneration (touching `.claude/support/reference/dashboard-regeneration.md`, `.claude/rules/dashboard.md`, and call sites in implement-agent Steps 3, 6a, 6c). Shipping scripts needs a new home (likely `.claude/scripts/` — root `scripts/` is template-maintenance and does not ship). Conflict: `rules/agents.md` restricts Bash, and scripts depend on it — connects to FB-010 (subagent Bash sandbox limits). Dependencies: FB-017 (checkbox detection is a concrete second candidate). Scope: start with a workspace inventory doc (`.claude/support/workspace/scripts-candidates.md`) listing candidates with tradeoffs; first extraction targets dashboard regen.

Look into where scripts could be used instead of commands, or even perhaps as part of skills folders if that is a valid use-case. Needs to be more robust or save tokens or minimize errors, improve quality etc.

## FB-012: Standardized base allowedTools set in template with merge-aware health-check

**Status:** ready
**Captured:** 2026-04-08
**Refined:** 2026-04-14 — Promoted without Q&A; capture text is the refined insight. Add a conservative template-owned "base" `allowedTools` set (safe for any project) to reduce permission prompts in `acceptEdits` mode. Projects extend via their own `.claude/settings.json` / `.claude/settings.local.json`. Health-check must merge the base set into existing projects without clobbering project-specific additions.
**Assessed:** 2026-04-14 — Requires a new shipped `.claude/settings.json` (doesn't exist today — template policy is currently "doesn't ship settings"), reclassifying it in `.claude/sync-manifest.json` (probably to a new `merge` category), flipping `health-check.md` Part 5c (which currently asserts the opposite), adding key-granular merge logic to Part 5 Template Sync, and updating `system-overview.md` and root `CLAUDE.md` file-boundary table. Scope: additive + corrective. Open policy questions (merge strategy add-only vs remove-on-update, which Bash commands belong in base set, whole-file vs key-granular merge) warrant a decision record at root `decisions/` before implementation. Note: the reversal should be scoped to `allowedTools` only — hooks/env/theme stay user-owned, which forces key-granular merge logic.

Add a standardized set of accepted permissions (`allowedTools`) to the Claude Code environment template. Goal: reduce permission prompts (especially in `acceptEdits` mode, since Max plan can't use auto mode) while keeping things safe and maintainable.

**Context from a planning conversation:**

- Claude Code settings layer additively: user-level (`~/.claude/settings.json`) → project-level (`.claude/settings.json`) → project-local (`.claude/settings.local.json`). `allowedTools` lists merge across levels.
- The template should own a conservative "base" set of allowed tools that's safe for any project (e.g., safe git read commands, linting, formatting, the health-check command itself).
- Individual projects can then extend permissions in their own `.claude/settings.json` or `.claude/settings.local.json` for project-specific tools.
- The health-check/update command needs to handle this carefully — it should merge the base allowed tools into a project without clobbering any project-specific additions.

**What needs to happen:**

1. Look at the current template repo structure, especially anything related to permissions, `allowedTools`, settings files, and the health-check command.
2. Assess: what permissions exist today? What does the health-check currently do when it updates a project?
3. Propose how to implement a base `allowedTools` set in the template, including how the health-check would merge it into projects that may have added their own project-specific permissions.
4. Do an impact assessment: what would change in the template, and what would change in existing projects that already use it?

**Important:** Don't make implementation decisions silently. Present options with tradeoffs where choices exist, especially around which tools belong in the base set and how the merge strategy should work.

## FB-013: Revisit hard phase transition dependencies for cross-phase parallel tasks

**Status:** ready
**Captured:** 2026-04-10
**Refined:** 2026-04-14 — The hard phase gate is a software-centric assumption that breaks for research/procurement/stakeholder-engagement domains where long-running activities (often `owner: human`) must start before prior phases close. SIREN is representative, not a one-off, so a schema change is justified. Two viable mechanisms remain open and should go to a decision record: (a) add optional `cross_phase: true` on individual tasks, or (b) weaken the phase gate to only block on `owner: claude` / `owner: both`, letting `owner: human` tasks float. Other directions (spec-level phase-overlap declarations, document-the-workaround) are disfavored.
**Assessed:** 2026-04-14 — Affects `task-schema.md` (`phase` field definition line 122), `phase-decision-gates.md` (enforcement procedure), `commands/work.md` Step 4, `rules/task-management.md` + `rules/spec-workflow.md`, `commands/health-check.md` Part 1, `commands/breakdown.md` (subtask inheritance under option a), `dashboard-regeneration.md` (cross-phase rendering), `system-overview.md` (invariant description). Scope: additive (option a) or corrective (option b reverses a documented invariant). Note: parallel-execution rules in `task-management.md` already use dependency+file-conflict eligibility without referencing phase — FB-013 is consistent with that model. Decision record at root `decisions/` (ephemeral) should resolve (a) vs (b); once decided, implementation is bounded.

The current task schema enforces a hard phase gate: "Tasks in Phase N+1 are blocked until all Phase N tasks complete." This works for software projects where phases represent strict dependency boundaries (can't test until built), but breaks down for research, procurement, and other non-software projects where some activities naturally span phase boundaries.

**Case that surfaced this:** In a research project (SIREN), workshop participant recruitment (Phase 2) needed to start weeks before all Phase 1 preparation tasks were done. Two remaining Phase 1 tasks (internal trial run, Teams Whiteboard test) were pre-session activities with no logical connection to recruitment, but the phase gate blocked all of Phase 2 until they were Finished. The workaround was to move those tasks to Phase 2, which solved the immediate problem but required reshuffling tasks to fit the environment's constraints rather than the project's natural structure.

**What should be considered:**

- Some tasks are inherently long-running and should start early regardless of phase (recruitment, procurement, approvals, stakeholder engagement). These are often `owner: "human"` tasks.
- The current model forces a choice: either (a) put everything in one phase (losing the organizational benefit of phases) or (b) accept that some tasks will be artificially blocked.
- A softer model might allow specific tasks to be tagged as "cross-phase eligible" or "early-start," meaning they can begin when their task-level dependencies are met, regardless of phase gate status.
- Alternatively, the phase gate could be weakened to "all Phase N tasks with `owner: claude` must complete" while `owner: human` tasks are allowed to carry over, since human tasks often have external timelines that don't align with phase boundaries.

**Possible directions (not decided):**
- Add an optional `cross_phase: true` field to the task schema that exempts a task from the phase gate
- Weaken the phase gate to only block on `owner: claude` and `owner: both` tasks, letting `owner: human` tasks float
- Allow explicit "phase overlap" declarations in the spec (e.g., "Phase 2 recruitment may begin during Phase 1")
- Keep the hard gate but document the "move tasks to unblock" pattern as a standard workaround
- Some combination of the above

## FB-017: /work Step 2b doesn't detect checked decision checkboxes or finalize decisions

**Status:** ready
**Captured:** 2026-04-13
**Refined:** 2026-04-14 — Decision auto-finalization (checkbox → `status: approved` + frontmatter + Decision/Rationale + unblock dependents) is documented in three places but the caller (`/work` Step 2b) doesn't reliably execute it. Confirmed in styler (2026-04-13): DEC-039, DEC-040, DEC-026-revision all stayed `proposed` after boxes were checked. Root cause is likely *both* a documentation problem (Step 2b underspecifies and points to a referenced procedure rather than inlining it) and an LLM reliability problem (procedure skipped under load). Fix should address both: tighten/inline the Step 2b procedure, and consider extracting detection into a deterministic script (connects to FB-011). `/iterate` should also run the same detection so the finalization path is tolerant at both entry points. Scope: `commands/work.md` Step 2b, `commands/iterate.md`, `phase-decision-gates.md`.
**Assessed:** 2026-04-14 — Primary rewrite: `commands/work.md` Step 2b (line 330) — inline the core checkbox-detection steps so the caller is unambiguously responsible; keep `phase-decision-gates.md` (lines 62-96) as edge-case reference, possibly restructured into "caller checklist" vs "full procedure". Add detection entry step to `commands/iterate.md`. Audit `decisions.md` line 151 and `workflow.md` lines 195-201 (the docs promising auto-finalization). Scope: corrective. Dependencies: FB-011 (script extraction is a strong candidate for the reliability leg of the root cause) and FB-010 (if Step 2b ran in a subagent, script invocation could hit sandbox issues — argues for keeping it in the orchestrator). Direct template edit for the doc/inline fix; script extraction follows under FB-011.

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

**Status:** ready
**Captured:** 2026-04-12
**Refined:** 2026-04-14 — Keep Action Required strictly actionable — only items needing user input, with just enough context to act. Do not create a Recent Activity section: work summaries should be removed from the dashboard entirely, since git log and task JSON already preserve history. If any summary content remains anywhere, prune by age (drop anything older than the last session). Scope: `rules/dashboard.md` and `dashboard-regeneration.md` — tighten the definition of what belongs in Action Required and remove guidance that lets summaries accumulate there.
**Assessed:** 2026-04-14 — Primary edit: `dashboard-regeneration.md` § "Action Item Contract" (lines 322-329) needs a negative rule ("must NOT include work summaries, completion reports, or recent-activity recaps"). Secondary: `rules/dashboard.md` § Sections (confirm no Recent Activity section), `commands/work.md` (any post-completion dashboard emission paths), `commands/health-check.md` Part 6 check #4 (extend to detect summary-shaped content if feasible). Existing Action Item Contract is ~80% aligned already — this formalizes the "what NOT to include" side. Dependencies: FB-014 (frontier philosophy), FB-011 (deterministic generator would make this enforceable by construction). Scope: corrective. Direct template edit — no decision record needed.

The dashboard's "Action Required" section sometimes includes summaries of recently completed work alongside the actual items needing user input. This clutters the section and slows down the user's ability to identify what they need to do and give feedback.

Proposed changes:
1. Keep "Action Required" tight — only items that require user action, with just enough context to understand what's needed.
2. Move work summaries and completion reports to a separate section further down the dashboard (e.g., "Recent Activity" or "Work Summary").
3. Establish clear rules for how Claude writes these summaries so they stay useful without becoming an ever-growing pile of information as phases and tasks get finished. Need rules for what gets included, how much detail, and when old summaries get pruned or collapsed.
