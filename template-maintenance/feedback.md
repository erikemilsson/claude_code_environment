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

## FB-038: Action Required regression — completion summaries still clutter section despite FB-015 fix

**Status:** new
**Captured:** 2026-04-22

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

## FB-039: validate-tasks.py and fingerprint.py read `data['task_id']` but schema field is `id`

**Status:** new
**Captured:** 2026-04-29

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

## FB-041: Verify DEC-001 Option C executes end-to-end in real downstream sessions

**Status:** new
**Captured:** 2026-05-13
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

## FB-042: Phase-restoration audit task descriptions need literal-ID cross-check

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-002 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).

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

## FB-043: implement-agent prompt should emphasize "extend ALL enum/union locations"

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-003 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).

When an implement-agent task adds a new enum value (e.g., a new capture method, status, or any string-literal union member), the implementation typically needs to extend multiple synchronized locations:

- TypeScript union type (e.g., `CaptureMethod` in types.ts)
- Zod enum schema (e.g., `CaptureMethodSchema` in schema-zod.ts)
- Dispatcher case handlers (e.g., onboard.md case statements)
- Validator handlers (loader.ts switch arms, if any)

Concrete example from a downstream styler project's T424 (add Zod + TS types for `split_strategy` per DEC-047): agent added `SplitBucketSchema` + `SplitStrategySchema` + extended `FieldCaptureSchema` with new optional fields, but **missed adding `'ask_user_question_split'` to `CaptureMethodSchema` enum AND `CaptureMethod` TS union**. T425 (the next task) absorbed the fix (5-line addition across two files), no harm done — but the gap delayed T425's start by ~5 minutes of root-cause investigation, and surfaced as a friction marker at session pause.

Suggested template improvement: add a Step 2.5 (after planning, before editing) to implement-agent.md — "When adding a new enum value or string-literal union member, list ALL locations that enumerate this value across the codebase (TS union, Zod enum, dispatcher cases, validator switch arms) and extend each one. Don't trust the task description's `files_affected` list to be exhaustive for enum-related work — search for the existing enum's name with grep first to find all extension points."

Even a one-line note in implement-agent.md's "Common pitfalls" section would catch this.

## FB-044: Heavy editorial verify-agent prompts may benefit from structural+content split

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-004 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).

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

## FB-045: Orchestrator should append friction markers eagerly, not at /work pause

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-005 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).

The "After implement-agent returns" protocol in /work command (Step 2) says: "Append friction markers: for each marker in report.friction_markers, add task_id and append as a JSON line to .claude/support/workspace/.session-log.jsonl".

Observation from a downstream styler project's Phase 20 work session: the orchestrator (Claude Code, executing /work in auto mode) skipped this step throughout the session — friction markers from agent reports were captured in task notes (task-XXX.json) but NOT appended to .session-log.jsonl in real-time. At /work pause time, the orchestrator caught up and batch-appended 8 markers from the session.

The risk: if the session terminates abruptly (compaction, crash, usage limit before pause is invoked), friction markers from that session are lost — only the task notes survive, and task notes aren't structured for cross-project Track 1 telemetry consumption.

Suggested template improvements (any of):

- **Document a clearer protocol** in /work or implement-agent.md — "Append marker via single bash call (`cat >> file <<JSON`) immediately after agent return; do not batch."
- **Make catchup idempotent** — if the orchestrator (or PreCompact hook) sees task notes with friction markers but no corresponding .session-log entry, append the missing markers automatically.
- **Move append responsibility into a hook** (PostAgentReturn or PostToolUse hook gated on Task subagent) so it can't be skipped by the orchestrator.

This is partly a behavioral nudge for the orchestrator — the "skip" was a judgment call to focus on user-facing communication, with the cost being post-hoc reconstruction at pause time. But making it harder to skip (Option 3, hooks) closes the gap structurally rather than relying on prompt discipline.

**Related:** FB-041 cause #2 (orchestrator-side marker append is documented but not reliably executed) — this is the same observation. FB-045's evidence informs FB-041's investigation.

## FB-046: Parallel-batch cross-task scaffolding contracts need single composed brief

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-006 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler (Personal Style Intelligence System)

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

## FB-047: Files_affected drift — decomposition should auto-enumerate ripple-affected fixture files

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-007 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler

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

## FB-048: Inline-command pattern — extract a shared template reference doc

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-008 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler

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

## FB-049: Anthropic usage-limit partial-completion structured resume contract

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-009 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler

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

## FB-050: /iterate spec-vs-registry hygiene pass — grep-validate spec claims

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-010 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler

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

## FB-051: Validate file paths during /work decomposition (originally styler FB-053)

**Status:** new
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-011 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — originally captured locally as FB-053, lifted here because it's template-improvement (per styler's own dashboard note: "FB-053 is template-improvement, not Phase 20 scope").

Decomposition step in `/work` should validate that file paths referenced in task descriptions and `files_affected` actually exist before the task is created.

**Concrete repro (styler T453 implementation, 2026-04-27):**

- `files_affected` listed `src/components/grooming/GroomingSection.tsx`
- Actual file lives at `src/components/style/GroomingSection.tsx`
- Implementer correctly grep'd and found the actual file; orchestrator updated metadata post-hoc (and the implementer wasted ~3 tool uses searching the wrong directory first)

**Proposed fix:** When decomposition references a path that doesn't resolve, flag it inline so the human reviewing decomposition output can correct it before tasks ship. Low-cost addition to the decomposition checklist (or `/health-check`); high-value preventing wasted implementer cycles searching wrong directories.

Could also catch related drift — task body mentioning a function name that no longer exists, etc. — but path validation alone covers the most common case.

**Relationship to FB-047:** FB-047 is broader ("ripple-affected fixture files missing from `files_affected`"); FB-051 is the narrower path-correctness check. They could ship as one decomposition-validation pre-pass enhancement covering both: (1) declared paths must resolve; (2) implied collateral paths (fixtures matching grep patterns) should be auto-suggested for inclusion.

## FB-052: implement-agent.md:223 grants subagent decision-record write that agents.md § State Ownership forbids

**Status:** new
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-012 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — multi-agent template audit, 2026-04-28. `agents/` files are byte-identical to template.

`implement-agent.md:223` instructs the subagent to: *"Create a `decision-*.md` file in `.claude/support/decisions/` using that template (decision records live outside `.claude/tasks/`, so subagent writes there are permitted)."*

This contradicts `rules/agents.md § State Ownership`, which states subagents *"do not write to `.claude/` paths"* and cites this as *"a hard constraint of the Claude Code harness (subagents are sandboxed from `.claude/` writes per Anthropic issue #38806) and is not expected to change."* The path `.claude/support/decisions/` is under `.claude/`, so the carve-out in implement-agent.md describes a write the harness may not actually permit at runtime.

`agents.md § Tool Preferences` already states the canonical pattern: *"When an agent's documented workflow describes a state transition, it means 'include in return report'; the orchestrator performs the actual write."* And `research-agent.md:181` follows this correctly — it generates decision content, reports it, and lets the caller (`/research` or `/work`/`/iterate`) write the file.

Only `implement-agent.md` violates the pattern.

**Suggested fix (option a, preferred):** rewrite `implement-agent.md:219-225` to match research-agent's pattern — agent generates the decision content, includes it in the return report under a new field (e.g., `decisions_to_record`), orchestrator writes the file. Consistent with the rest of the template and respects the harness sandbox.

**Suggested fix (option b):** verify whether Anthropic issue #38806 still applies; if subagents now CAN write under `.claude/support/decisions/`, update `agents.md § State Ownership` to carve out the exception explicitly rather than burying it in implement-agent.md. Requires evidence that the harness actually permits the write — current docs say it doesn't.

Either way, the two files should agree.

## FB-053: Tool Preferences block duplicated verbatim across 3 agent files

**Status:** new
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-013 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — multi-agent template audit, 2026-04-28. `agents/` files are byte-identical to template.

`implement-agent.md:24-32`, `verify-agent.md:34-42`, and `research-agent.md:23-31` each contain a near-identical Tool Preferences block (~9 lines × 3). The same content already exists canonically in `rules/agents.md § Tool Preferences` (lines 51-60). Four sources of truth for the same rule.

Drift hazard: a future edit will likely land in `rules/agents.md` (the canonical home) and skip the three agent files, leaving the per-agent restatements stale. Or vice versa.

**Suggested fix:** delete the per-agent restatements; replace each with a one-line pointer like *"Tool preferences: see `rules/agents.md § Tool Preferences`."* Saves ~30 lines of duplicated context per multi-agent flow and removes the drift risk.

Lighter alternative: keep the per-agent pointers but add a comment in `rules/agents.md` reminding maintainers to ripple any change to the three agent files. Less robust but lower-disruption.

Same pattern likely exists in downstream forks for product-specific commands (e.g., styler's six product commands all duplicate an "Output Formatting" block) — that's a fork-side issue, but the agent-side fix here would model the right pattern.

## FB-054: breakdown.md:17-18 numbered list skips step 2

**Status:** new
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-014 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — multi-agent template audit, 2026-04-28. `commands/breakdown.md` byte-identical to template.

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

## FB-055: subagent_type "general-purpose" used to dispatch specialist agents in work.md / research.md

**Status:** new
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-015 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — multi-agent template audit, 2026-04-28. `commands/work.md` and `commands/research.md` byte-identical to template.

Three call sites dispatch named specialist agents (implement-agent, verify-agent, research-agent) but with `subagent_type: "general-purpose"`:

- `work.md:603` (implement-agent dispatch)
- `work.md:686` (verify-agent dispatch)
- `research.md:74` (research-agent dispatch)

The agent definitions live at `.claude/agents/{implement,verify,research}-agent.md` but the dispatch shape doesn't reference them as named subagent types. This works because the dispatched agent's prompt directs it to read its own definition file — but it bypasses any per-agent configuration that Claude Code's `.claude/agents/` discovery would otherwise apply (e.g., per-agent model default, per-agent tool allowlist if/when the harness supports them via frontmatter).

Two paths:

- **(a) Switch to named subagent_types** — `subagent_type: "implement-agent"`, `"verify-agent"`, `"research-agent"`. Relies on Claude Code's auto-discovery of `.claude/agents/*.md`. Aligns dispatch with definition.
- **(b) Document that "general-purpose" is intentional** — perhaps for portability across harness versions where named subagents might not auto-discover, or to keep the persona-via-prompt-content pattern. Add a one-line note in `rules/agents.md` explaining the choice.

Either is defensible; the current state is "neither documented nor uniformly applied." Worth picking one and being explicit. (a) seems cleaner if Claude Code's `.claude/agents/` discovery is stable, which the template implicitly assumes by shipping definition files there.

## FB-056: Playwright MCP UI inspection doesn't parallelize across subagents — document the limit and the sequential pattern

**Status:** new
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-016 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler

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
