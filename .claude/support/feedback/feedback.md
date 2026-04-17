# Feedback Log

Items are captured via `/feedback` and triaged via `/feedback review`.

---

## FB-011: Explore scripts as alternative to commands or within skills folders

**Status:** ready
**Captured:** 2026-04-08
**Refined:** 2026-04-14 — Identify command procedures where a deterministic script would outperform LLM-executed natural-language instructions — starting with the dashboard, where output variation across regenerations makes the artifact harder to comprehend. Scripts could live alongside commands or inside skills folders if that's a valid pattern. Gains: (1) consistency of standardized artifacts, (2) reduced error rate from procedure drift, (3) lower token cost. Scope is exploratory — inventory candidates and propose which procedures to extract before committing.
**Assessed:** 2026-04-14 — Primary target is dashboard regeneration (touching `.claude/support/reference/dashboard-regeneration.md`, `.claude/rules/dashboard.md`, and call sites in implement-agent Steps 3, 6a, 6c). Shipping scripts needs a new home (likely `.claude/scripts/` — root `scripts/` is template-maintenance and does not ship). Conflict: `rules/agents.md` restricts Bash, and scripts depend on it — connects to FB-010 (subagent Bash sandbox limits). Dependencies: FB-017 (checkbox detection is a concrete second candidate). Scope: start with a workspace inventory doc (`.claude/support/workspace/scripts-candidates.md`) listing candidates with tradeoffs; first extraction targets dashboard regen.

Look into where scripts could be used instead of commands, or even perhaps as part of skills folders if that is a valid use-case. Needs to be more robust or save tokens or minimize errors, improve quality etc.

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

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/CLAUDE.md` (Workflow Rules section). Scope: corrective. Makes existing rules-file loading declarative via `@path` imports instead of prose references. No cross-item overlap. Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — CLAUDE.md supports `@path/to/import` syntax; imports are auto-loaded by the harness.

The template's `.claude/CLAUDE.md` currently lists rules files in a "Workflow Rules" prose section but does not import them explicitly — they happen to be loaded by other mechanisms. Switch to explicit `@.claude/rules/task-management.md`, `@.claude/rules/spec-workflow.md`, etc., making the dependency declarative.

**Impact scope:** `.claude/CLAUDE.md` (one section). Possibly `.claude/rules/*.md` if reorganized.

**Why:** Makes context loading explicit and predictable; aligns the template with the documented harness feature; surfaces accidental-load behavior. Low risk if rules are already short.

## FB-021: Use AskUserQuestion-driven interview in `/iterate distill`

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/commands/iterate.md` (distill subcommand). Scope: additive. Complements FB-032 (decisions surfacing in `/iterate` propose): FB-021 surfaces decisions *before* writing, FB-032 forces them to surface *in* the proposal — the two together cover both directions of the silent-decisions failure mode. Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — recommends interviewing the user via the `AskUserQuestion` tool before writing a spec, to surface implementation, UX, edge-case, and tradeoff questions they haven't considered.

The template's `/iterate distill` already extracts a spec from a vision doc but doesn't explicitly use `AskUserQuestion`. Adopt the structured-question pattern so distillation surfaces hard-to-see decisions rather than silently assuming.

**Impact scope:** `.claude/commands/iterate.md` (distill subcommand section).

**Why:** Direct mapping; vision-doc-to-spec is exactly the use case the doc describes. Improves spec quality at the most important leverage point in the whole workflow.

## FB-022: Add "address root causes, not symptoms" rule to implement-agent

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/rules/agents.md` and/or `.claude/agents/implement-agent.md`; optionally a matching check in `.claude/agents/verify-agent.md` per-task return schema so verify-agent has unambiguous grounds to reject symptom-only fixes. Scope: additive. Aligns with the template's verification-first design. Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — verification table entry: *"the build fails with this error: [paste]. fix it and verify the build succeeds. address the root cause, don't suppress the error."*

implement-agent does not currently codify this principle. Add a short explicit rule (in agent prompt or `.claude/rules/agents.md`) so verify-agent has unambiguous grounds to reject symptom-only fixes: try/except swallows, suppressed warnings, magic-number overrides, silenced failing tests, skipped assertions.

**Impact scope:** `.claude/agents/implement-agent.md` and/or `.claude/rules/agents.md`. Possibly a matching check in verify-agent's per-task return schema.

**Why:** Aligns with the template's verification-first design. Currently implicit; making it explicit gives verify-agent a clear, citable check.

## FB-023: Document `/btw` for side questions in session-management

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/rules/session-management.md` (Managing Context Pressure bullet). Scope: additive. Bundle with FB-024 and FB-025 (same file, three session-management tool additions). Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — `/btw` answers appear in a dismissible overlay and never enter conversation history.

Template's `.claude/rules/session-management.md` already documents `/clear` and `/compact` for managing context pressure. Add `/btw` as a third tool for "quick question that shouldn't bloat context."

**Impact scope:** `.claude/rules/session-management.md` (one bullet in Managing Context Pressure section).

**Why:** Direct context-discipline tool that complements existing guidance. Minimal addition, real leverage for long sessions.

## FB-024: Document `/rewind` and Esc+Esc checkpoint flow in session-management

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/rules/session-management.md` (new short section, likely after "What Survives What" table). Scope: additive. Bundle with FB-023 and FB-025 (same file). Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — every Claude action creates a checkpoint; `Esc+Esc` or `/rewind` opens the menu; can restore conversation only, code only, or both; persists across sessions.

Template's `session-management.md` doesn't mention checkpointing at all — it focuses on `/work pause` and handoff files. Add a short section noting checkpointing as a complementary recovery mechanism (for recovering from agent missteps without needing `/work pause` or a fresh session).

**Impact scope:** `.claude/rules/session-management.md` (new short section, likely after "What Survives What" table).

**Why:** Important user-facing feature currently undocumented in the template's session guidance.

## FB-025: Document `/rename` for naming sessions

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/rules/session-management.md` (resume-methods section, one-liner). Scope: additive. Bundle with FB-023 and FB-024 (same file). Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — `/rename` gives sessions descriptive names (e.g., `oauth-migration`, `debugging-memory-leak`) so they're findable via `claude --resume`.

Template's resume-methods table in `session-management.md` doesn't mention this. Add a one-liner.

**Impact scope:** `.claude/rules/session-management.md` (one row in resume-methods table or a one-liner under "Resuming Sessions").

**Why:** Useful when running this template across multiple long-running projects. Pure documentation, no behavior change.


## FB-027: Skip-planning guidance for trivial tasks

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/commands/research.md` or `.claude/rules/decisions.md` (callout), possibly `.claude/commands/work.md` Step 3 routing. Scope: additive. Single-callout fix; aligns with existing "no premature abstraction" ethos. Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17): *"For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly... If you could describe the diff in one sentence, skip the plan."*

Template's `/research` and decomposition flow don't currently distinguish trivial from non-trivial tasks. Add an explicit callout: skip formal planning when the diff can be described in one sentence. Prevents overhead for small fixes and aligns with the "no premature abstraction" ethos already in CLAUDE.md.

**Impact scope:** `.claude/commands/research.md` (callout) or `.claude/rules/decisions.md`; possibly `.claude/commands/work.md` Step 3 routing.

## FB-028: Add CLI-tool installation hints to setup-checklist

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/support/reference/setup-checklist.md` (CLI installs subsection). Scope: additive. Shares file with FB-037 (different subsection: FB-028 = CLI installs, FB-037 = Optional Hooks appendix) — not a conflict; file gains two independent additions. Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — recommends installing `gh`, `aws`, `gcloud`, `sentry-cli` etc. for context-efficient external interactions, noting unauthenticated API calls often hit rate limits.

Template's `.claude/support/reference/setup-checklist.md` could detect which CLIs are present and suggest installs based on spec content (e.g., spec mentions GitHub PRs → suggest `gh`).

**Impact scope:** `.claude/support/reference/setup-checklist.md`.

**Why:** Aligns with the template's setup-time validation pattern. Low-cost addition.

## FB-029: Document non-interactive mode (`claude -p`) as automation primitive

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects new `.claude/support/reference/automation.md` or section in `.claude/README.md`. Scope: additive. Bundle with FB-030 (same target file; FB-030 uses `claude -p` as its primitive and belongs as a pattern section in the same doc). Connects to FB-011 — some FB-011 script candidates may be better expressed as `claude -p` one-liners than bash scripts, so sequence FB-029/030 before FB-011 implementation. Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — `claude -p "prompt"` runs without a session; with `--output-format json`/`stream-json` and `--allowedTools`, it's the building block for CI, pre-commit hooks, scripts, and fan-out patterns.

Worth a short reference for users automating template workflows (e.g., nightly `/health-check`, batch report generation, scheduled dashboard refresh).

**Impact scope:** New `.claude/support/reference/automation.md` or section in `.claude/README.md`.

**Why:** Connects directly to FB-011 (scripts as alternative) and may influence FB-011's scope — some "scripts" candidates might be better expressed as `claude -p` one-liners than as bash scripts.

## FB-030: Document fan-out pattern for batch task execution

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/support/reference/automation.md` (shared with FB-029; new file) and/or addendum to `.claude/support/reference/parallel-execution.md`. Scope: additive. Bundle with FB-029 (depends on `claude -p` primitive). Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — `for file in $(...); do claude -p "Migrate $file..." --allowedTools "Edit,Bash(git commit *)"; done` pattern for large migrations.

Template's parallel execution is intra-session (multiple `Task` agents coordinated by one `/work` orchestrator); fan-out is inter-session (many independent `claude` processes). The two scaling axes are complementary. Document the fan-out pattern so users know it exists for very large workloads (e.g., migrating hundreds of files).

**Impact scope:** New section in an automation doc (depends on FB-029) or addendum to `parallel-execution.md`.

**Why:** Different scaling axis from current parallel model. Worth flagging even if template does not itself implement fan-out — users may discover and adopt it themselves.

## FB-031: Document Writer/Reviewer parallel-session pattern

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/README.md` or `.claude/rules/agents.md` (short mention). Scope: additive. Reinforces existing implement-agent/verify-agent separation-of-concerns design — no behavioral change, just making an external scaling axis visible. Route: Phase 4 direct.

Source: Claude Code best-practices doc (fetched 2026-04-17) — running parallel Claude sessions for quality: Session A writes, Session B reviews with fresh context, avoiding bias toward code it just wrote.

Template already enforces this via the implement-agent / verify-agent split within one session, but users can go further by running two separate `claude` instances (e.g., one implementing a feature, another doing a deeper security or architectural review of the finished code).

**Impact scope:** `.claude/README.md` or `.claude/rules/agents.md`.

**Why:** Reinforces the template's existing separation-of-concerns design. Small mention, no behavioral change.

## FB-032: Require explicit "Decisions in This Proposal" section in `/iterate` output

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/commands/iterate.md` (propose subcommand output contract), `.claude/rules/spec-workflow.md` (propose-approve-apply), possibly `.claude/agents/verify-agent.md` matching check for spec-change tasks. Scope: additive. Complements FB-021 (before-proposal interview surfaces decisions; FB-032 forces them into the proposal itself). Under Opus 4.7 instruction-following, the structural contract should land more reliably than the report's Opus 4.6 window. Trial of this contract gates FB-033 (spec-auditor research). Route: Phase 4 direct — implement early to generate the trial data FB-033 needs.

Source: Claude Code usage insights report (fetched 2026-04-17) — the report's #1 friction, with a concrete data point: *"You had to ask 'did you make any silent decisions' twice in one session to surface unapproved design choices in a spec proposal."* The report's fun-ending calls this out across 5+ sessions.

Convert reactive vigilance into a structural output contract. Every `/iterate` spec-change proposal must end with a `## Decisions in This Proposal` section listing each non-trivial choice tagged `[NEEDS APPROVAL]`, `[FROM EXISTING SPEC]`, or `[USER REQUESTED]`. `/iterate` does not proceed to apply until each `[NEEDS APPROVAL]` item is resolved.

Complements FB-021 (AskUserQuestion-driven interview in `/iterate distill`) — FB-021 surfaces decisions *before* proposing; FB-032 forces them to surface *in* the proposal. Under Opus 4.7's stronger instruction-following, the structural contract should land more reliably than during the report's Opus 4.6 window.

**Impact scope:** `.claude/commands/iterate.md` (propose subcommand output contract), `.claude/rules/spec-workflow.md` (propose-approve-apply section), possibly a matching check in `.claude/agents/verify-agent.md` for spec-change tasks.

**Why:** Converts recurring reactive friction into a structural guarantee. Small contract change with high leverage on the report's #1 pattern.

## FB-033: Spec-auditor subagent + PreToolUse gate (research-first; trial FB-032 first; candidate DEC-009)

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects new `.claude/agents/spec-auditor.md` (subagent, not Skill — resolved by DEC-007), hook wiring, verify-agent integration. Scope: exploratory. Research-first AND trial-gated on FB-032 (only pursue if the structural output contract proves insufficient after real `/iterate` sessions under Opus 4.7). FB-020 dependency resolved by DEC-007 (subagent is the correct home). FB-026 dependency resolved by DEC-008 (layered settings stay; hook wiring goes in `settings.local.json` if pursued). Route: Phase 3 research — **deferred** until FB-032 trial data exists (candidate DEC-009).

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

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/CLAUDE.md` (Critical Invariants — template-owned, ships to projects), `.claude/rules/agents.md`, and/or `.claude/agents/implement-agent.md`. NOT root `./CLAUDE.md` (template-maintenance only). Scope: additive. Capture-time conflict (earlier broader framing vs root `CLAUDE.md`'s UI-testing guidance) already resolved via narrow restart-after-kill scope — no conflict remains. Related to FB-036 (both address over-eager execution, different trigger points). Auto mode does not absorb this (behavioral rule, not permission). Route: Phase 4 direct.

Source: Claude Code usage insights report (fetched 2026-04-17) — documented a 140GB-RAM Ghostty/Turbopack crash traced to Claude restarting dev servers after being told to kill them: *"Claude started dev servers despite explicit memory warnings and restarted them after you said to kill them, contributing to a 140GB RAM Ghostty crash."*

When the user kills a long-running process (dev server, watcher, batch loop, mass file processing, external-API scan), do not restart it in the same session without renewed approval. Confirm before re-initiating any process the user just halted.

Note: an earlier framing ("don't autonomously start long-running processes") was rejected during review because it conflicts with root `CLAUDE.md`'s own UI-testing guidance: *"For UI or frontend changes, start the dev server and use the feature in a browser before reporting the task as complete."* Starting dev servers for verification is a **feature**, not a bug. The narrower restart-after-kill rule avoids that conflict.

Auto mode does **not** absorb this — the classifier approves or denies individual tool calls but does not enforce "respect prior kills." Behavioral rule, not a permission.

**Impact scope:** `.claude/CLAUDE.md` (Critical Invariants — template-owned and ships to projects), `.claude/rules/agents.md`, and/or `.claude/agents/implement-agent.md`. Not root `./CLAUDE.md` (that file is template-maintenance-only and gets replaced on project setup).

**Why:** Domain-agnostic version of a concrete failure case (140GB crash). Complements DEC-005 (which stops unauthorized tool calls) by addressing authorized-but-destructive sequences. Small doc addition, zero implementation risk.

## FB-035: Implement-agent file-reading guidance for large files (prefer Grep/Glob; use Read `offset`/`limit`)

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/agents/implement-agent.md` (Tool Preferences section) or `.claude/rules/agents.md` § Tool Preferences. Scope: additive. Real quantified friction (61 file-too-large events, largest single tool-error category in the usage report). Single-paragraph fix, zero behavioral risk. Route: Phase 4 direct.

Source: Claude Code usage insights report (fetched 2026-04-17) — "Tool Errors Encountered" chart flags **File Too Large (61 events)** as the single largest error category, larger than "Command Failed" (56) or "File Not Found" (19).

Current implement-agent Tool Preferences guidance says "use dedicated tools" but doesn't advise on large-file strategy. Add a short rule: prefer Grep/Glob for content lookup over reading whole files; when a file is known or suspected large, use Read with `offset`/`limit` rather than a full read.

**Impact scope:** `.claude/agents/implement-agent.md` (Tool Preferences section) or `.claude/rules/agents.md` § Tool Preferences.

**Why:** Real quantified friction (61 of the top tool errors — the largest single category). Single-paragraph fix, no behavioral risk.

## FB-036: "Confirm before dispatching parallel work" rule in implement-agent / `/work`

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/commands/work.md` Step 4 (parallel dispatch path) and `.claude/support/reference/parallel-execution.md`. Scope: additive. Related to FB-034 (shared over-eager-execution theme; proactive vs reactive). Independent of FB-026 outcome — if auto mode removes permission-prompt checkpoints, pre-dispatch summary becomes *more* valuable, not less. Route: Phase 4 direct.

Source: Claude Code usage insights report (fetched 2026-04-17) — *"You interrupted background bash and parallel agent dispatches multiple times across /onboard and /work sessions because Claude moved faster than your validation step."*

Current `/work` decomposition can dispatch multiple parallel implement-agents without an explicit pre-dispatch confirmation step. Add: when a batch spawns more than N parallel agents (N configurable; default 3), summarize the dispatch plan (which tasks, which files affected, verify strategy) and await user confirmation before spawning.

Related to FB-034 (respect user kills): both address over-eager execution. FB-034 is reactive (after a kill); FB-036 is proactive (before a dispatch).

Note on auto mode: auto mode may actually *worsen* this friction by removing the natural permission-prompt pause points that currently force a checkpoint. A pre-dispatch summary restores a cheap human checkpoint independent of the permissions layer.

**Impact scope:** `.claude/commands/work.md` Step 4 (parallel dispatch path), `.claude/support/reference/parallel-execution.md`.

**Why:** Preserves the productivity of parallel dispatch while adding a cheap human checkpoint. Small behavioral change at one site.

## FB-037: Optional PreToolUse hook example for dev-server guarding in `setup-checklist.md` (defer until FB-026 resolves)

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects `.claude/support/reference/setup-checklist.md` (new "Optional Hooks" subsection/appendix). Scope: additive. **Unblocked 2026-04-17 by DEC-008 (Option D approved)** — layered two-file model from DEC-005 stays intact; hook recipe references `.claude/settings.local.json` under the `hooks` key. Shares file with FB-028 (different subsection). Route: Phase 4 direct — ready now.

Source: Claude Code usage insights report (fetched 2026-04-17) — report recommends a PreToolUse hook blocking `next dev` / `npm run dev` / `pnpm dev` unless explicitly approved. Complements FB-034 (universal behavioral rule) by providing a structural hook recipe for users who want hard blocks.

Per DEC-005, hooks belong in `settings.local.json` (user-owned) and the template does not ship hooks. But `.claude/support/reference/setup-checklist.md` can document an opt-in hook example for users running frontend projects.

**Dependency on FB-026 (candidate DEC-008 — auto-mode reevaluation):** The hook recipe's shape depends on whether DEC-008 keeps, simplifies, or retires the DEC-005 layered-settings model. If DEC-008 moves primary enforcement to auto mode's classifier, the hook recipe becomes a narrower "belt-and-braces" add-on for users who want hard blocks in addition to classifier approvals. **Defer full drafting until FB-026 resolves** — the recipe could be wasted work if the permissions story changes shape.

**Impact scope:** `.claude/support/reference/setup-checklist.md` (new "Optional Hooks" subsection or appendix).

**Why:** Opt-in advice for users who want structural dev-server protection. Keeps the domain-agnostic template clean while giving frontend users a working example to copy into their own `settings.local.json`.
