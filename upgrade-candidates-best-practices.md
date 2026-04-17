# Upgrade Candidates — Claude Code Best Practices Doc

**Source:** https://code.claude.com/docs/en/best-practices (fetched 2026-04-17)
**Tag:** DELETE-AFTER (cleanup in Phase 5)
**Status:** Awaiting per-item user review

---

## How to use this file

For each candidate below, mark one of:
- `[approve]` — capture via `/feedback` as-is
- `[edit] {what to change}` — capture with the noted edit
- `[reject] {1-line reason}` — drop; reason prevents resurfacing

After review, I capture the approved set into the `/feedback` pipeline (one item per candidate). No `/feedback` invocations happen until you've marked the list.

Candidates are grouped: **A = template/architecture changes**, **B = doc and rules tweaks**, **C = user-facing tips/setup**, **D = preemptively rejected** (called out so you can override).

> **Note:** Four candidates that were preemptively dropped due to Opus 4.7 + 1M context absorbing the failure mode they targeted: CLAUDE.md/rules bloat audit, custom compaction instructions, IMPORTANT/YOU MUST emphasis tuning, and a separate prompting-tips reference doc.

---

## A. Template / architecture changes

### A1: Adopt `@path` imports in `.claude/CLAUDE.md` for rules files

**Description:** The doc shows CLAUDE.md can import other markdown files via `@path/to/import` syntax (auto-loaded by Claude Code). Currently `.claude/CLAUDE.md` lists rules files in a "Workflow Rules" prose section but does not import them — they happen to be loaded by other mechanisms. Switch to explicit `@.claude/rules/task-management.md` etc., making the dependency declarative.
**Impact scope:** `.claude/CLAUDE.md` (one section). Possibly `.claude/rules/*.md` if reorganized.
**Relevance rationale:** Makes context loading explicit and predictable; aligns the template with the documented harness feature; surfaces accidental-load behavior. Low risk if rules are already short.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject ___

### A2: Evaluate `.claude/skills/` adoption for domain-specific knowledge

**Description:** The doc presents Skills as the on-demand alternative to CLAUDE.md for "domain knowledge or workflows that are only relevant sometimes." Template currently uses commands + rules + agents for everything. Skills could carry domain-specific guidance (software vs. research vs. procurement vs. renovation patterns) loaded only when invoked, instead of bundling it in spec-checklist or rules.
**Impact scope:** Potentially large — new `.claude/skills/` directory, redistribution of content from `support/reference/`, possible refactor of `commands/` (some commands are skill-shaped).
**Relevance rationale:** Architectural question. Skills postdate this template's design. Worth assessing whether to adopt incrementally (e.g., one domain pack first) or stay with current model.
**Decision:** [ ] approve  [ x] edit _skills have limitations that we should be aware of before making any big changes, for instance if we try to make a sub-agent run through a skill I think it won't have its own context window. There might be similar limitations for switchin to skills fro commands and rules that we need to explore and evaluate first before making changes._  [ ] reject ___

### A3: Use AskUserQuestion-driven interview in `/iterate distill`

**Description:** The doc recommends having Claude interview the user using the `AskUserQuestion` tool before writing a spec. Template's `/iterate distill` already extracts a spec from a vision doc but doesn't explicitly use `AskUserQuestion`. Adopt the structured-question pattern to surface implementation, UX, edge-case, and tradeoff questions the user hasn't considered.
**Impact scope:** `.claude/commands/iterate.md` (distill subcommand section).
**Relevance rationale:** Direct mapping; vision-doc-to-spec is exactly the use case the doc describes. Improves spec quality at the most important leverage point.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject ___

### A4: Add "address root causes, not symptoms" rule to implement-agent

**Description:** The doc highlights this in its verification table — *"address the root cause, don't suppress the error"*. Implement-agent doesn't currently codify this. Add it as a short rule (e.g., in agent prompt or `rules/agents.md`) so verify-agent has explicit grounds to reject symptom-only fixes (e.g., try/except swallow, suppressed warning, magic-number override).
**Impact scope:** `.claude/agents/implement-agent.md` and/or `.claude/rules/agents.md`.
**Relevance rationale:** Aligns with template's verification-first design. Currently implicit; making it explicit gives verify-agent a clear check.
**Decision:** [x ] approve  [ ] edit ___  [ ] reject ___

---

## B. Doc and rules tweaks

### B1: Document `/btw` for side questions in session-management

**Description:** The doc introduces `/btw` — answers appear in a dismissible overlay and never enter conversation history. Useful when the user has a quick question mid-session that shouldn't bloat context.
**Impact scope:** `.claude/rules/session-management.md` (one bullet in Managing Context Pressure section).
**Relevance rationale:** Direct context-discipline tool that complements `/clear` and `/compact`. Template already documents the others.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject ___

### B2: Document `/rewind` and Esc+Esc checkpoint flow

**Description:** The doc describes checkpointing (every Claude action creates one; `Esc+Esc` or `/rewind` opens the menu; can restore conversation only, code only, or both; persists across sessions). Template's `session-management.md` doesn't mention checkpointing at all — it focuses on `/work pause` and handoff files. Add a short section noting checkpointing as a complementary recovery mechanism.
**Impact scope:** `.claude/rules/session-management.md` (new short section after "What Survives What" table).
**Relevance rationale:** Important user-facing feature for recovering from agent missteps without re-running `/work pause`. Currently undocumented.
**Decision:** [x ] approve  [ ] edit ___  [ ] reject ___

### B3: Document `/rename` for naming sessions

**Description:** The doc suggests `/rename` to give sessions descriptive names (e.g., `oauth-migration`, `debugging-memory-leak`) so they're findable via `claude --resume`. Template's resume table doesn't mention this.
**Impact scope:** `.claude/rules/session-management.md` (one row in the resume-methods table or a one-liner under "Resuming Sessions").
**Relevance rationale:** Useful when running this template across multiple long-running projects. Pure documentation, no behavior change.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject ___

### B4: Document auto mode and sandboxing as permission alternatives

**Description:** DEC-005 codifies the layered allowlist model. The doc notes two more options: auto mode (`--permission-mode auto`, classifier-based approvals) and sandboxing (OS-level isolation). Worth adding a short section to README or settings docs explaining when each fits — auto mode for "trust the direction, don't click every step", sandboxing for "let Claude work freely within boundaries".
**Impact scope:** `.claude/README.md` (Settings section) or new `.claude/support/reference/permissions.md`.
**Relevance rationale:** Completes the permissions story. DEC-005 only covers allowlist; users running unattended (cron, fan-out) want auto mode.
**Decision:** [ ] approve  [x ] edit __automode is now available on the Max plan, which I use. It is a recent development, just a few days old. Previously we ran on the assumption that it didn't work and the permissions were based on that. It appears that auto mode actually runs quite smoothly and it might not be so necessary to bloat the documentation and rules with specifics about ways to handle permissions. We should explore the impact of both auto mode and what simplifying the docs might mean for how well the remplate runs_  [ ] reject ___

### B5: Skip-planning guidance for trivial tasks

**Description:** The doc explicitly says skip Plan Mode for trivial tasks (typo, log line, rename) — *"If you could describe the diff in one sentence, skip the plan."* Template's `/research` and decomposition flow could note this so users don't over-formalize small fixes.
**Impact scope:** `.claude/commands/research.md` (callout) or `.claude/rules/decisions.md`.
**Relevance rationale:** Prevents the template from imposing overhead on small changes. Aligns with the "no premature abstraction" ethos already in CLAUDE.md.
**Decision:** [x ] approve  [ ] edit ___  [ ] reject ___

---

## C. User-facing tips and setup

### C1: Add CLI-tool installation hints to setup-checklist

**Description:** The doc recommends installing `gh`, `aws`, `gcloud`, `sentry-cli` etc. for context-efficient external interactions. Template's `setup-checklist.md` could note: detect which CLIs are present, and suggest installs based on spec content (e.g., spec mentions GitHub PRs → suggest `gh`).
**Impact scope:** `.claude/support/reference/setup-checklist.md`.
**Relevance rationale:** Aligns with template's setup-time validation pattern. Low-cost addition.
**Decision:** [x ] approve  [ ] edit ___  [ ] reject ___

### C2: Document `CLAUDE.local.md` as project-personal notes option

**Description:** The doc lists `./CLAUDE.local.md` (gitignored) as a fourth CLAUDE.md location for personal project-specific notes. Template's `archiving.md` and `CLAUDE.md` discuss `./CLAUDE.md` (project) and `~/.claude/CLAUDE.md` (user) but not the local variant.
**Impact scope:** `.claude/README.md` File Ownership table or `.claude/rules/archiving.md`.
**Relevance rationale:** Small documentation gap. Useful for users who want personal scratch notes alongside team-shared project context.
**Decision:** [ ] approve  [ ] edit ___  [x ] reject _the template is designed for only personal use at this point__

### C3: Document non-interactive mode (`claude -p`) as automation primitive

**Description:** `claude -p "prompt"` runs without a session — useful for CI, pre-commit hooks, scripts. With `--output-format json`/`stream-json` and `--allowedTools`, it's the building block for fan-out patterns. Worth a short reference for users automating template workflows (e.g., "run `/health-check` nightly").
**Impact scope:** New `.claude/support/reference/automation.md` or section in README.
**Relevance rationale:** Connects to FB-011 (scripts as alternative). May influence FB-011's scope.
**Decision:** [x ] approve  [ ] edit ___  [ ] reject ___

### C4: Document fan-out pattern for batch task execution

**Description:** The doc shows a `for file in $(...); do claude -p "Migrate $file..." --allowedTools "Edit,Bash(git commit *)"; done` pattern for large migrations. Template's parallel execution is intra-session (multiple `Task` agents); fan-out is inter-session (multiple `claude` processes). Could complement parallel execution for very large workloads.
**Impact scope:** New section in automation doc (depends on C3) or addendum to `parallel-execution.md`.
**Relevance rationale:** Different scaling axis from current parallel model. Worth flagging even if not implemented — users may discover and use it themselves.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject ___

### C5: Document Writer/Reviewer parallel-session pattern

**Description:** The doc describes running parallel Claude sessions for quality (Session A writes, Session B reviews with fresh context — no bias toward code it just wrote). Template already enforces this via the implement-agent / verify-agent split, but could note that users can also run two `claude` instances for higher-stakes review (e.g., security review of a finished feature).
**Impact scope:** README or `rules/agents.md`.
**Relevance rationale:** Reinforces the template's separation-of-concerns design. Small mention.
**Decision:** [ x] approve  [ ] edit ___  [ ] reject ___

---

## D. Preemptively rejected (override if you disagree)

### D1: Verify UI changes via Claude in Chrome extension

**Reason for preemptive reject:** Domain-agnostic template; UI verification belongs in user-project-specific guidance, not the environment.

### D2: `/init` command as starter for CLAUDE.md

**Reason for preemptive reject:** Template ships with pre-written `.claude/CLAUDE.md`. The `./CLAUDE.md` placeholder at project root could mention `/init` as one option, but this is a minor README addition (could be folded into C2 if wanted).

### D3: MCP server setup (Notion, Figma, databases)

**Reason for preemptive reject:** User-domain decision, varies per project. Not template's place to recommend specific MCP servers.

### D4: Plugins (`/plugin`)

**Reason for preemptive reject:** Should this template *be* a plugin? Possibly worth its own discussion (potential decision record), but as a doc-tweak candidate it's out of scope. Flag separately if interested.

### D5: Hooks examples (eslint after every file edit, block writes to migrations folder)

**Reason for preemptive reject:** Per DEC-005, hooks belong in `settings.local.json` (user-owned). Template shouldn't ship example hooks because they bind to specific project tooling. Documentation pointer to `/hooks` already exists.

### D6: Course-correct keys (Esc, "Undo that")

**Reason for preemptive reject:** Pure user behavior, not template content. Belongs in upstream Claude Code docs.

### D7: "Develop your intuition" / "Avoid common failure patterns"

**Reason for preemptive reject:** Meta-advice for end users. Not template content.

### D8: Use `@` to reference files in prompts

**Reason for preemptive reject:** General Claude Code behavior, not template-specific. Already documented upstream.

---

## Already covered in template (no action needed)

For transparency, doc recommendations confirmed already addressed:
- **Verification criteria / Claude verifies its own work** → entire verify-agent + verification gate architecture
- **Subagents** → `.claude/agents/implement-agent.md`, `verify-agent.md`, `research-agent.md` (also see DEC-004)
- **Permission allowlists** → DEC-005 (`.claude/settings.json` ships with base allowlist)
- **Resume conversations (`--continue`, `--resume`)** → `.claude/rules/session-management.md`
- **Use subagents for investigation** → research-agent + DEC-004 framing
- **`/clear` between unrelated tasks** → `.claude/rules/session-management.md`
- **`/compact <instructions>`** → `.claude/rules/session-management.md`
- **CLAUDE.md as persistent context** → `.claude/CLAUDE.md` + `./CLAUDE.md` split
- **Reference existing patterns / point to sources** → already implicit in implement-agent's read-existing-code workflow
