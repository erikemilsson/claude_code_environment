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

## FB-019: Adopt `@path` imports in `.claude/CLAUDE.md` for rules files

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — CLAUDE.md supports `@path/to/import` syntax; imports are auto-loaded by the harness.

The template's `.claude/CLAUDE.md` currently lists rules files in a "Workflow Rules" prose section but does not import them explicitly — they happen to be loaded by other mechanisms. Switch to explicit `@.claude/rules/task-management.md`, `@.claude/rules/spec-workflow.md`, etc., making the dependency declarative.

**Impact scope:** `.claude/CLAUDE.md` (one section). Possibly `.claude/rules/*.md` if reorganized.

**Why:** Makes context loading explicit and predictable; aligns the template with the documented harness feature; surfaces accidental-load behavior. Low risk if rules are already short.

## FB-020: Research Skills architectural limitations before template adoption

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — presents Skills as the on-demand alternative to CLAUDE.md for "domain knowledge or workflows that are only relevant sometimes." User flagged adoption as **research-first**, not implementation.

The template currently uses commands + rules + agents for everything. Skills could, in principle, carry domain-specific guidance (software vs. research vs. procurement vs. renovation patterns) loaded only when invoked, instead of bundling it in spec-checklist or rules. But before committing to any migration from commands/rules → skills or from subagents → skill-invocation, the architectural limitations need investigation.

**Known concerns to investigate:**
- Do subagents that run *through* a skill get their own context window, or does the skill's execution share the caller's context? (User's primary concern — would invalidate the separation-of-concerns guarantees underpinning DEC-004.)
- What other constraints exist for replacing commands or rules with skills (e.g., invocation semantics, parameter passing, discoverability, scope of `disable-model-invocation`)?
- Can skills be template-owned (ship in `.claude/skills/`) the same way commands ship, or do they carry different distribution/override semantics?
- Interaction with the settings/permissions layer: do skills inherit `permissions.allow` from parent CLAUDE.md, or do they need their own?

**Scope if pursued after research:** potentially large — new `.claude/skills/` directory, redistribution of content from `support/reference/`, possible refactor of some commands. Do not begin any migration until the above questions are answered.

**Likely outcome:** this becomes a formal decision record (candidate DEC-007) once the research phase closes.

## FB-021: Use AskUserQuestion-driven interview in `/iterate distill`

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — recommends interviewing the user via the `AskUserQuestion` tool before writing a spec, to surface implementation, UX, edge-case, and tradeoff questions they haven't considered.

The template's `/iterate distill` already extracts a spec from a vision doc but doesn't explicitly use `AskUserQuestion`. Adopt the structured-question pattern so distillation surfaces hard-to-see decisions rather than silently assuming.

**Impact scope:** `.claude/commands/iterate.md` (distill subcommand section).

**Why:** Direct mapping; vision-doc-to-spec is exactly the use case the doc describes. Improves spec quality at the most important leverage point in the whole workflow.

## FB-022: Add "address root causes, not symptoms" rule to implement-agent

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — verification table entry: *"the build fails with this error: [paste]. fix it and verify the build succeeds. address the root cause, don't suppress the error."*

implement-agent does not currently codify this principle. Add a short explicit rule (in agent prompt or `.claude/rules/agents.md`) so verify-agent has unambiguous grounds to reject symptom-only fixes: try/except swallows, suppressed warnings, magic-number overrides, silenced failing tests, skipped assertions.

**Impact scope:** `.claude/agents/implement-agent.md` and/or `.claude/rules/agents.md`. Possibly a matching check in verify-agent's per-task return schema.

**Why:** Aligns with the template's verification-first design. Currently implicit; making it explicit gives verify-agent a clear, citable check.

## FB-023: Document `/btw` for side questions in session-management

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — `/btw` answers appear in a dismissible overlay and never enter conversation history.

Template's `.claude/rules/session-management.md` already documents `/clear` and `/compact` for managing context pressure. Add `/btw` as a third tool for "quick question that shouldn't bloat context."

**Impact scope:** `.claude/rules/session-management.md` (one bullet in Managing Context Pressure section).

**Why:** Direct context-discipline tool that complements existing guidance. Minimal addition, real leverage for long sessions.

## FB-024: Document `/rewind` and Esc+Esc checkpoint flow in session-management

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — every Claude action creates a checkpoint; `Esc+Esc` or `/rewind` opens the menu; can restore conversation only, code only, or both; persists across sessions.

Template's `session-management.md` doesn't mention checkpointing at all — it focuses on `/work pause` and handoff files. Add a short section noting checkpointing as a complementary recovery mechanism (for recovering from agent missteps without needing `/work pause` or a fresh session).

**Impact scope:** `.claude/rules/session-management.md` (new short section, likely after "What Survives What" table).

**Why:** Important user-facing feature currently undocumented in the template's session guidance.

## FB-025: Document `/rename` for naming sessions

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — `/rename` gives sessions descriptive names (e.g., `oauth-migration`, `debugging-memory-leak`) so they're findable via `claude --resume`.

Template's resume-methods table in `session-management.md` doesn't mention this. Add a one-liner.

**Impact scope:** `.claude/rules/session-management.md` (one row in resume-methods table or a one-liner under "Resuming Sessions").

**Why:** Useful when running this template across multiple long-running projects. Pure documentation, no behavior change.

## FB-026: Reevaluate permissions story given auto-mode maturity (potential inflection — may impact DEC-005)

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) mentions auto mode (`--permission-mode auto`) and sandboxing as alternatives to explicit allowlists. User flagged this as more than a doc tweak — it may change the foundation DEC-005 was built on.

**Context:** Auto mode is now available on the Max plan (user's plan) as of just a few days before 2026-04-17. Previously the template was designed on the assumption that auto mode was not available to the user, which led DEC-005 to ship a two-layer allowlist model (template-owned `settings.json` with base `permissions.allow` + user-owned `settings.local.json`). Under auto mode, a classifier model approves routine actions at runtime, which may make much of that allowlist machinery unnecessary.

**Questions to resolve (likely via a decision record):**
- Does auto mode reliably cover the set that DEC-005's base allowlist was protecting? Where does it fall back to prompting the user?
- If the base allowlist becomes largely redundant under auto mode, should the template simplify or remove `settings.json`? What becomes the supported permissions model?
- Do sandboxing (`/sandbox`, OS-level isolation) and auto mode compose cleanly, or is this an either/or choice?
- How much of `commands/health-check.md` Part 5c (Settings Boundary Validation) is still useful if the allowlist simplifies?
- What would downstream projects migrating from the current DEC-005 template structure experience?

**Scope if acted upon:** potentially reverses portions of DEC-005. Likely an inflection-point decision record (candidate DEC-008). Affects `.claude/settings.json`, `sync-manifest.json`, `commands/health-check.md`, `.claude/CLAUDE.md` Critical Invariants, `system-overview.md`, `.claude/README.md` Settings section.

**User's framing:** *"Auto mode actually runs quite smoothly and it might not be so necessary to bloat the documentation and rules with specifics about ways to handle permissions. We should explore the impact of both auto mode and what simplifying the docs might mean for how well the template runs."*

## FB-027: Skip-planning guidance for trivial tasks

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17): *"For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly... If you could describe the diff in one sentence, skip the plan."*

Template's `/research` and decomposition flow don't currently distinguish trivial from non-trivial tasks. Add an explicit callout: skip formal planning when the diff can be described in one sentence. Prevents overhead for small fixes and aligns with the "no premature abstraction" ethos already in CLAUDE.md.

**Impact scope:** `.claude/commands/research.md` (callout) or `.claude/rules/decisions.md`; possibly `.claude/commands/work.md` Step 3 routing.

## FB-028: Add CLI-tool installation hints to setup-checklist

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — recommends installing `gh`, `aws`, `gcloud`, `sentry-cli` etc. for context-efficient external interactions, noting unauthenticated API calls often hit rate limits.

Template's `.claude/support/reference/setup-checklist.md` could detect which CLIs are present and suggest installs based on spec content (e.g., spec mentions GitHub PRs → suggest `gh`).

**Impact scope:** `.claude/support/reference/setup-checklist.md`.

**Why:** Aligns with the template's setup-time validation pattern. Low-cost addition.

## FB-029: Document non-interactive mode (`claude -p`) as automation primitive

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — `claude -p "prompt"` runs without a session; with `--output-format json`/`stream-json` and `--allowedTools`, it's the building block for CI, pre-commit hooks, scripts, and fan-out patterns.

Worth a short reference for users automating template workflows (e.g., nightly `/health-check`, batch report generation, scheduled dashboard refresh).

**Impact scope:** New `.claude/support/reference/automation.md` or section in `.claude/README.md`.

**Why:** Connects directly to FB-011 (scripts as alternative) and may influence FB-011's scope — some "scripts" candidates might be better expressed as `claude -p` one-liners than as bash scripts.

## FB-030: Document fan-out pattern for batch task execution

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — `for file in $(...); do claude -p "Migrate $file..." --allowedTools "Edit,Bash(git commit *)"; done` pattern for large migrations.

Template's parallel execution is intra-session (multiple `Task` agents coordinated by one `/work` orchestrator); fan-out is inter-session (many independent `claude` processes). The two scaling axes are complementary. Document the fan-out pattern so users know it exists for very large workloads (e.g., migrating hundreds of files).

**Impact scope:** New section in an automation doc (depends on FB-029) or addendum to `parallel-execution.md`.

**Why:** Different scaling axis from current parallel model. Worth flagging even if template does not itself implement fan-out — users may discover and adopt it themselves.

## FB-031: Document Writer/Reviewer parallel-session pattern

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code best-practices doc (fetched 2026-04-17) — running parallel Claude sessions for quality: Session A writes, Session B reviews with fresh context, avoiding bias toward code it just wrote.

Template already enforces this via the implement-agent / verify-agent split within one session, but users can go further by running two separate `claude` instances (e.g., one implementing a feature, another doing a deeper security or architectural review of the finished code).

**Impact scope:** `.claude/README.md` or `.claude/rules/agents.md`.

**Why:** Reinforces the template's existing separation-of-concerns design. Small mention, no behavioral change.

## FB-032: Require explicit "Decisions in This Proposal" section in `/iterate` output

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code usage insights report (fetched 2026-04-17) — the report's #1 friction, with a concrete data point: *"You had to ask 'did you make any silent decisions' twice in one session to surface unapproved design choices in a spec proposal."* The report's fun-ending calls this out across 5+ sessions.

Convert reactive vigilance into a structural output contract. Every `/iterate` spec-change proposal must end with a `## Decisions in This Proposal` section listing each non-trivial choice tagged `[NEEDS APPROVAL]`, `[FROM EXISTING SPEC]`, or `[USER REQUESTED]`. `/iterate` does not proceed to apply until each `[NEEDS APPROVAL]` item is resolved.

Complements FB-021 (AskUserQuestion-driven interview in `/iterate distill`) — FB-021 surfaces decisions *before* proposing; FB-032 forces them to surface *in* the proposal. Under Opus 4.7's stronger instruction-following, the structural contract should land more reliably than during the report's Opus 4.6 window.

**Impact scope:** `.claude/commands/iterate.md` (propose subcommand output contract), `.claude/rules/spec-workflow.md` (propose-approve-apply section), possibly a matching check in `.claude/agents/verify-agent.md` for spec-change tasks.

**Why:** Converts recurring reactive friction into a structural guarantee. Small contract change with high leverage on the report's #1 pattern.

## FB-033: Spec-auditor subagent + PreToolUse gate (research-first; trial FB-032 first; candidate DEC-009)

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code usage insights report (fetched 2026-04-17) — "On the Horizon" section proposes an adversarial-reviewer subagent that intercepts every `Write`/`Edit` to `spec*.md` or `decisions/*.md`. User edit on capture: *"wait until A1 is trialed properly before deciding"* — this item is explicitly gated on FB-032's trial outcome.

A bigger-hammer version of FB-032. The spec-auditor would diff each proposed change against the prior version, extract new assertions/decisions, cross-reference them against the current session's explicit user instructions, emit a "user-requested vs agent-inferred" table, and block the write until agent-inferred items are approved.

**Trial-gate:** Do not pursue until FB-032's structural output contract is trialed across several real `/iterate` sessions under Opus 4.7. If FB-032 materially reduces silent-decision friction, FB-033 is unnecessary. If FB-032 proves insufficient — silent decisions still slip through, or the output contract is bypassed — FB-033 becomes the structural backstop.

**Questions to resolve if FB-032 proves insufficient (likely via a decision record):**
- Should the spec-auditor be a subagent (`.claude/agents/`) or a Skill (`.claude/skills/`)? Depends on FB-020's findings on subagent-vs-skill context-window separation.
- Where does the PreToolUse hook live — template-owned `.claude/settings.json` (DEC-005 currently restricts that file to `permissions.allow` only), user-owned `settings.local.json`, or a documented example in `setup-checklist.md`?
- If auto mode (DEC-008 / FB-026 outcome) already covers most of the "block unapproved write" goal at the permission layer, does the hook reduce to a narrower belt-and-braces?
- Performance cost of running an adversarial diff-and-review before every spec/decision write.

**Impact scope if pursued:** potentially large — new `.claude/agents/spec-auditor.md` (or `.claude/skills/spec-auditor/`), hook wiring, integration with verify-agent contract.

**Likely outcome:** candidate DEC-009 after FB-032 trial, FB-020 research, and FB-026 resolution all close.

## FB-034: "Respect user kills" — don't restart long-running processes without renewed approval

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code usage insights report (fetched 2026-04-17) — documented a 140GB-RAM Ghostty/Turbopack crash traced to Claude restarting dev servers after being told to kill them: *"Claude started dev servers despite explicit memory warnings and restarted them after you said to kill them, contributing to a 140GB RAM Ghostty crash."*

When the user kills a long-running process (dev server, watcher, batch loop, mass file processing, external-API scan), do not restart it in the same session without renewed approval. Confirm before re-initiating any process the user just halted.

Note: an earlier framing ("don't autonomously start long-running processes") was rejected during review because it conflicts with root `CLAUDE.md`'s own UI-testing guidance: *"For UI or frontend changes, start the dev server and use the feature in a browser before reporting the task as complete."* Starting dev servers for verification is a **feature**, not a bug. The narrower restart-after-kill rule avoids that conflict.

Auto mode does **not** absorb this — the classifier approves or denies individual tool calls but does not enforce "respect prior kills." Behavioral rule, not a permission.

**Impact scope:** `.claude/CLAUDE.md` (Critical Invariants — template-owned and ships to projects), `.claude/rules/agents.md`, and/or `.claude/agents/implement-agent.md`. Not root `./CLAUDE.md` (that file is template-maintenance-only and gets replaced on project setup).

**Why:** Domain-agnostic version of a concrete failure case (140GB crash). Complements DEC-005 (which stops unauthorized tool calls) by addressing authorized-but-destructive sequences. Small doc addition, zero implementation risk.

## FB-035: Implement-agent file-reading guidance for large files (prefer Grep/Glob; use Read `offset`/`limit`)

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code usage insights report (fetched 2026-04-17) — "Tool Errors Encountered" chart flags **File Too Large (61 events)** as the single largest error category, larger than "Command Failed" (56) or "File Not Found" (19).

Current implement-agent Tool Preferences guidance says "use dedicated tools" but doesn't advise on large-file strategy. Add a short rule: prefer Grep/Glob for content lookup over reading whole files; when a file is known or suspected large, use Read with `offset`/`limit` rather than a full read.

**Impact scope:** `.claude/agents/implement-agent.md` (Tool Preferences section) or `.claude/rules/agents.md` § Tool Preferences.

**Why:** Real quantified friction (61 of the top tool errors — the largest single category). Single-paragraph fix, no behavioral risk.

## FB-036: "Confirm before dispatching parallel work" rule in implement-agent / `/work`

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code usage insights report (fetched 2026-04-17) — *"You interrupted background bash and parallel agent dispatches multiple times across /onboard and /work sessions because Claude moved faster than your validation step."*

Current `/work` decomposition can dispatch multiple parallel implement-agents without an explicit pre-dispatch confirmation step. Add: when a batch spawns more than N parallel agents (N configurable; default 3), summarize the dispatch plan (which tasks, which files affected, verify strategy) and await user confirmation before spawning.

Related to FB-034 (respect user kills): both address over-eager execution. FB-034 is reactive (after a kill); FB-036 is proactive (before a dispatch).

Note on auto mode: auto mode may actually *worsen* this friction by removing the natural permission-prompt pause points that currently force a checkpoint. A pre-dispatch summary restores a cheap human checkpoint independent of the permissions layer.

**Impact scope:** `.claude/commands/work.md` Step 4 (parallel dispatch path), `.claude/support/reference/parallel-execution.md`.

**Why:** Preserves the productivity of parallel dispatch while adding a cheap human checkpoint. Small behavioral change at one site.

## FB-037: Optional PreToolUse hook example for dev-server guarding in `setup-checklist.md` (defer until FB-026 resolves)

**Status:** new
**Captured:** 2026-04-17

Source: Claude Code usage insights report (fetched 2026-04-17) — report recommends a PreToolUse hook blocking `next dev` / `npm run dev` / `pnpm dev` unless explicitly approved. Complements FB-034 (universal behavioral rule) by providing a structural hook recipe for users who want hard blocks.

Per DEC-005, hooks belong in `settings.local.json` (user-owned) and the template does not ship hooks. But `.claude/support/reference/setup-checklist.md` can document an opt-in hook example for users running frontend projects.

**Dependency on FB-026 (candidate DEC-008 — auto-mode reevaluation):** The hook recipe's shape depends on whether DEC-008 keeps, simplifies, or retires the DEC-005 layered-settings model. If DEC-008 moves primary enforcement to auto mode's classifier, the hook recipe becomes a narrower "belt-and-braces" add-on for users who want hard blocks in addition to classifier approvals. **Defer full drafting until FB-026 resolves** — the recipe could be wasted work if the permissions story changes shape.

**Impact scope:** `.claude/support/reference/setup-checklist.md` (new "Optional Hooks" subsection or appendix).

**Why:** Opt-in advice for users who want structural dev-server protection. Keeps the domain-agnostic template clean while giving frontend users a working example to copy into their own `settings.local.json`.
