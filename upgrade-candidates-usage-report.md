# Upgrade Candidates — Claude Code Usage Insights Report

**Source:** `file:///Users/erikemilsson/.claude/usage-data/report.html` (fetched 2026-04-17)
**Tag:** DELETE-AFTER (cleanup in Phase 5)
**Status:** Awaiting per-item user review

---

## How to use this file

For each candidate below, mark one of:
- `[approve]` — capture via `/feedback` as-is
- `[edit] {what to change}` — capture with the noted edit
- `[reject] {1-line reason}` — drop; reason prevents resurfacing

After review, I capture the approved set into the `/feedback` pipeline (one item per candidate). No `/feedback` invocations happen until you've marked the list. Items flagged "overlaps with FB-NNN" are **not** captured as new — they become routing notes for the next `/feedback review` triage (Phase 2 hand-off).

Candidates are grouped: **A = template/architecture changes**, **B = doc and rules tweaks**, **C = user-facing tips/setup**, **D = preemptively rejected** (called out so you can override).

> **Note (timing disclosure):** The source report covers **2026-03-15 to 2026-04-14**, which predates (a) **Opus 4.7** (the report reflects Opus 4.6 behavior — instruction-following is meaningfully better on 4.7), (b) **auto mode on the Max plan** (released just a few days before 2026-04-17; permissions landscape is shifting via FB-026 / candidate DEC-008), and (c) the **best-practices intake** (FB-019–FB-031 captured 2026-04-17). Candidates below have been scanned against all three filters — items already absorbed by those changes are routed to "Already covered" rather than created as new. The preemptive-drop summary below is the original filter-1 pass (see upgrade-tracker memory: "Opus 4.7 + 1M + Max auto filtering").

> **Note:** Four insights were preemptively dropped in addition to the D list below, for reasons that mirror the best-practices intake's top note: report's CLAUDE.md-suggestion items CM2/CM3 mixed domain-agnostic principles with software-specific examples (touch targets, EXIF, hydration, dev servers) — the principles are covered elsewhere or generalized into B1/B2; the specific examples are dropped as not-domain-agnostic. CM4 (advice-before-implementation) is already stated verbatim in root `CLAUDE.md`'s "Doing tasks" section and follows more reliably under Opus 4.7. CM1 (surface silent decisions) is reflected in A1 below in a more structural shape than a CLAUDE.md one-liner.

---

## A. Template / architecture changes

### A1: Require explicit "Decisions in This Proposal" section in `/iterate` output

**Description:** The report's #1 friction — with a data point — is silent design decisions in spec proposals: *"You had to ask 'did you make any silent decisions' twice in one session to surface unapproved design choices in a spec proposal"* and the report's "fun ending" calls this out across 5+ sessions. Convert reactive vigilance into a structural output contract: every `/iterate` spec-change proposal must end with a `## Decisions in This Proposal` section listing each non-trivial choice tagged `[NEEDS APPROVAL]`, `[FROM EXISTING SPEC]`, or `[USER REQUESTED]`. `/iterate` does not proceed to apply until each `[NEEDS APPROVAL]` item is resolved.
**Impact scope:** `.claude/commands/iterate.md` (propose subcommand output contract), `.claude/rules/spec-workflow.md` (propose-approve-apply section), possibly a matching check in verify-agent.
**Relevance rationale:** Complements FB-021 (AskUserQuestion-driven interview in distill) — FB-021 surfaces decisions before proposing; A1 forces them to surface *in* the proposal. Small contract change with high leverage on recurring friction. Low implementation risk.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject ___

### A2: Spec-auditor subagent + PreToolUse gate on spec/decision writes (research-first — candidate DEC-009)

**Description:** The report's "On the Horizon" proposes an adversarial-reviewer subagent that intercepts every `Write`/`Edit` to `spec*.md` or `decisions/*.md`, diffs the change, extracts new assertions/decisions, cross-references the current session's explicit instructions, emits a "user-requested vs agent-inferred" table, and blocks the write until agent-inferred items are approved. Bigger-hammer version of A1. Flag as **research-first** — the shape depends on open questions and should not be built speculatively.
**Impact scope:** Potentially large — new `.claude/agents/spec-auditor.md` (or as a Skill, depending on FB-020 outcome), PreToolUse hook wiring, integration with research-agent/verify-agent contract. Overlaps with FB-020 (Skills research — subagent-context-window question from FB-020 is load-bearing for this). Hook placement interacts with DEC-005 (template-owned vs user-owned settings split).
**Relevance rationale:** A structural guardrail rather than an output convention. **Increasingly contingent under Opus 4.7:** A1's structural output contract should land more reliably under 4.7's better instruction-following than it would have under the report's 4.6-era data. Worth doing **only if** A1 is trialed and proves insufficient, and only after FB-020's Skills research and FB-026's auto-mode reevaluation close (the latter affects where PreToolUse hooks can live). Likely candidate decision record (DEC-009) if the gate is still needed after those upstreams resolve.
**Decision:** [ ] approve  [x ] edit __wait until A1 is trialed properly before deciding_  [ ] reject ___

---

## B. Doc and rules tweaks

### B1: "Respect user kills — don't restart long-running processes without renewed approval" rule

**Description:** The report documents a 140GB-RAM Ghostty/Turbopack crash traced to Claude **restarting** dev servers after being told to kill them. Originally framed more broadly as "don't autonomously start long-running processes," but that framing conflicts with root `CLAUDE.md`'s own UI-testing guidance (*"For UI or frontend changes, start the dev server and use the feature in a browser before reporting the task as complete"*) — starting dev servers for verification is a **feature**, not a bug. The actual failure mode is narrower: ignoring a user's explicit kill. Revised rule: when the user kills a long-running process (dev server, watcher, batch loop, external-API scan), do not restart it in the same session without renewed approval; confirm before re-initiating any process the user just halted.
**Impact scope:** `./CLAUDE.md` (template-replaced root file — "Executing actions with care" section is the natural home) or `.claude/rules/agents.md`. Also worth adding to `.claude/agents/implement-agent.md`.
**Relevance rationale:** Domain-agnostic version of a concrete failure case (140GB crash). Behavioral rule — **auto mode does not absorb this**: the classifier approves or denies individual tool calls but does not enforce "respect prior kills." Narrower than originally drafted so it doesn't conflict with existing UI-testing guidance. Small doc addition, zero implementation risk.
**Decision:** [x ] approve  [ ] edit ___  [ ] reject ___

### B2: Implement-agent file-reading guidance (prefer Grep/Glob; use Read `offset`/`limit` for large files)

**Description:** Report's "Tool Errors Encountered" chart flags **File Too Large (61 events)** as the single largest error category — larger than "Command Failed" (56) or "File Not Found" (19). Current implement-agent tool-preferences guidance says "use dedicated tools" but doesn't advise on large-file strategy. Add a short rule: prefer Grep/Glob for content lookup over reading whole files; when a file is known or suspected large, use Read with `offset`/`limit` rather than a full read.
**Impact scope:** `.claude/agents/implement-agent.md` (Tool Preferences section) or `.claude/rules/agents.md` § Tool Preferences.
**Relevance rationale:** Real quantified friction with a single-paragraph fix. No behavioral risk.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject ___

### B3: "Confirm before dispatching parallel work" rule in implement-agent / `/work`

**Description:** Report: *"You interrupted background bash and parallel agent dispatches multiple times across /onboard and /work sessions because Claude moved faster than your validation step."* Current `/work` decomposition can dispatch multiple parallel implement-agents without an explicit pre-dispatch confirm step. Add: when a batch spawns more than N parallel agents (N configurable; default 3), summarize the dispatch plan (which tasks, which files affected, verify strategy) and await confirmation before spawning.
**Impact scope:** `.claude/commands/work.md` Step 4 (parallel dispatch path), `.claude/support/reference/parallel-execution.md`.
**Relevance rationale:** Friction pattern consistent with B1 (over-eager execution). Preserves the productivity of parallel dispatch while adding a cheap human checkpoint. Small behavioral change at one site.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject __ 

---

## C. User-facing tips and setup

### C1: Optional PreToolUse hook example for dev-server guarding in `setup-checklist.md`

**Description:** Report recommends a PreToolUse hook blocking `next dev` / `npm run dev` / `pnpm dev` unless explicitly approved. Per DEC-005, hooks belong in `settings.local.json` (user-owned) and the template should not ship hooks — but `setup-checklist.md` can document an optional hook example for users running frontend projects. Connects to B1 above (B1 is the universal behavioral rule; C1 is the concrete hook recipe for users who want structural enforcement).
**Impact scope:** `.claude/support/reference/setup-checklist.md` (new "Optional Hooks" subsection or appendix).
**Relevance rationale:** Opt-in advice. Keeps the domain-agnostic template clean while giving users who need it a working example to copy into their own `settings.local.json`.
**Dependency on FB-026 (auto-mode reevaluation):** The hook recipe's shape depends on whether DEC-008 keeps, simplifies, or retires the DEC-005 layered-settings model. If DEC-008 moves primary enforcement to auto mode's classifier, the hook recipe becomes a narrower "belt-and-braces" add-on for users who want hard blocks in addition to classifier approvals. Defer full drafting until FB-026 resolves.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject ___

### C2: Sandbox Permission Blocks (7 events) — directly informs DEC-008 scope via FB-026

**Description:** Report's "Primary Friction Types" chart shows 7 sandbox-permission-block events in 29 days (pre-auto-mode). Feeds directly into FB-026 (permissions/auto-mode reevaluation; candidate DEC-008) as quantitative baseline. **Not a new FB** — the data is load-bearing for the research itself: if auto mode has already absorbed most of these 7 events in the days since, that's exactly the measurement DEC-008 needs.
**Impact scope:** Route to FB-026 triage; no new FB-NNN created.
**Relevance rationale:** Pre-auto-mode baseline for a research item whose whole point is measuring auto mode's absorption of permission friction. Now more load-bearing than when the report was written — this is the "before" half of the before/after DEC-008 will weigh.
**Decision:** [x ] approve (route as absorb into FB-026)  [ ] edit ___  [ ] reject ___

### C3: Custom Skills (/verify, /spec-propose suggestions) — data point for FB-020 research

**Description:** Report's "Features to Try" explicitly recommends formalizing `/work`, `/iterate`, `/feedback` as Skills and adding `/verify` and `/spec-propose` skills. Same Skills question FB-020 is investigating. **Not a new FB** — confirms the research framing and adds specific skill candidates to consider if FB-020's architectural-limitation research resolves favorably.
**Impact scope:** Route to FB-020 triage; no new FB-NNN created.
**Relevance rationale:** External confirmation of the direction FB-020 is already taking. Adds concrete skill-shape examples for the research phase.
**Decision:** [ x] approve (route as absorb into FB-020)  [ ] edit ___  [ ] reject ___

---

## D. Preemptively rejected (override if you disagree)

### D1: `PLAN:` / `DO:` prefix mode convention (from report's "New Usage Patterns")

**Reason for preemptive reject:** User-behavior prompt convention, not template content. Belongs in upstream Claude Code docs or a user-level `~/.claude/CLAUDE.md` rather than the project template. Root `CLAUDE.md`'s existing advice-before-implementation rule already covers the underlying need at the template level.

### D2: `/autophase` overnight meta-orchestrator (from "On the Horizon")

**Reason for preemptive reject:** Too aggressive for a domain-agnostic template. `/work` already orchestrates parallel implement+verify agents within a session; cross-phase meta-orchestration with git worktrees, automatic rollback, and consolidated PR production is a project-level workflow choice, not template infrastructure. Revisit if/when the template gains explicit autonomy tiers.

### D3: Test-First Iteration with Visual+Functional Oracles (`/tdd-phase`)

**Reason for preemptive reject:** Software-specific. Template must work for research, procurement, and renovation projects where "red-green-refactor" doesn't map. A software-project plugin could carry this, but not the core template.

### D4: Playwright MCP / visual regression tooling

**Reason for preemptive reject:** Software/frontend-specific; MCP server choices are user-project-level per D3 of the best-practices intake. Report praises Erik's existing Playwright usage — that's a user-project asset, not something the template should codify.

### D5: Specific frontend bug patterns (touch targets, EXIF orientation, hydration, Next.js route coverage)

**Reason for preemptive reject:** Software/frontend-specific examples from CM3. The generalized principle (run a verify-pass after multi-file changes, check all promised items shipped) is already covered by the verify-agent architecture (DEC-004). Specific checks belong in project-level verification rubrics, not the domain-agnostic template.

---

## Already covered in template (no action needed)

For transparency, report recommendations confirmed already addressed:

- **Verify pass as required, not optional, step in `/work`** → core template design; DEC-004 and `.claude/agents/verify-agent.md` enforce this structurally. Report's own praise (verify-agents catching 44px→28px regressions, 5-of-10 API routes, hydration mismatches) validates the contract is working.
- **Advice-before-implementation** (report's CM4 / P2) → root `CLAUDE.md` § "Doing tasks" already states: *"For exploratory questions ('what could we do about X?', 'how should we approach this?', 'what do you think?'), respond in 2-3 sentences with a recommendation and the main tradeoff. ... Don't implement until the user agrees."*
- **Address root causes, not symptoms** → captured as FB-022 in the best-practices intake.
- **Writer/Reviewer parallel-session pattern** → captured as FB-031 in the best-practices intake. Report's "Multi-Clauding 11% of messages / 39 overlap events" data point confirms you already run this pattern — the template just documents it.
- **Codify repeated workflows as commands/skills** (report's "Custom Skills" feature card) → covered by FB-020 (Skills architectural research; candidate DEC-007). C3 above routes the report's specific skill suggestions into FB-020's scope.
- **Anti-scope-creep** (11 Excessive-Changes events + 9 User-Rejected-Action events) → root `CLAUDE.md` § "Doing tasks" already states: *"Don't add features, refactor, or introduce abstractions beyond what the task requires. ... Three similar lines is better than a premature abstraction."* Under Opus 4.7's stronger instruction-following, this rule is expected to land more reliably than during the report's Opus 4.6 window — so the 20 combined events are a pre-4.7 baseline, not evidence that the existing rule needs strengthening. (Was candidate C4 before the Opus-4.7 scan demoted it here.)
- **Spec-driven pipeline with decision records, parallel agents, verification** → the report characterizes this as the user's current practice ("genuinely disciplined spec-driven pipeline"), not a recommendation to adopt. The template infrastructure is already in place.
