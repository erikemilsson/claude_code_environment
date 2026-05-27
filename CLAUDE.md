# Template Repository Context

**You are working on the template itself, not on a project that uses the template.**

The `.claude/` directory contains the environment that ships to new projects. The root-level files (this file, `README.md`, `tests/`) are template maintenance infrastructure.

## What This Means

- **Don't fill in template placeholders** — sections like `[Brief description]` and `[Your license here]` are intentionally blank
- **Don't create project-specific content** — no real specs, tasks, or decisions
- **Don't run `/work` or `/iterate` as if building a project** — these commands are what you're maintaining, not using
- **The spec file (`.claude/spec_v1.md`) should stay as a placeholder** — it's a template for users to fill in
- **The dashboard (`.claude/dashboard.md`) is a populated format example** — unlike other template files that use `[bracketed placeholders]`, the dashboard shows a fictional renovation project mid-execution. This is intentional: it serves as a golden example for Claude to pattern-match when generating dashboards. It gets replaced on first `/work` run.

## What You Should Do

- **Edit command definitions** (`.claude/commands/*.md`) to improve workflow logic
- **Edit agent definitions** (`.claude/agents/*.md`) to improve implementation/verification
- **Edit reference docs** (`.claude/support/reference/*.md`) to improve patterns and schemas
- **Edit `.claude/CLAUDE.md`** to improve environment instructions (template-owned core)
- **Edit `.claude/rules/*.md`** to improve modular workflow rules
- **Edit `.claude/README.md`** to improve the user-facing environment guide
- **Run conceptual tests** (`tests/scenarios/`) after significant command changes
- **Use `[bracketed text]` for user-customizable placeholder sections** (exception: `dashboard.md` uses populated example data instead)

## Template Maintenance Workflow

When making changes to the template, use the `.claude/` command definitions as reference for what you're editing — but don't use the `.claude/` spec/task/dashboard/decision workflow to manage the template's own work (those are template content, not tools).

- **Source of truth:** `system-overview.md` (root) describes the template's design intent
- **Decision records:** `decisions/` (root) — for formal decisions about template changes via `/research`
- **Feedback (four files; see FB-062 for the convention):**
  - `.claude/support/feedback/feedback.md` (shipped, active) + `archive.md` (shipped, resolved) — `/feedback review` triages.
  - `template-maintenance/feedback.md` (maintenance, active) + `feedback-archive.md` (maintenance, resolved) — manual triage. Append manually; do NOT use `/feedback` here.

  **Naming-asymmetry trap:** the maintenance archive is `feedback-archive.md`, NOT `archive.md`. Dedup checks that probe `template-maintenance/archive.md` will silently report "does not exist" and miss predecessors (observed 2026-05-15: FB-004 + FB-005 captured as duplicates of already-shipped FB-042 + FB-056 because of this exact miss; see FB-062 § "Observed empirical instances").

  **Cross-project capture pattern:** downstream-project sessions write template-fix items to the **shipped** location (`.claude/support/feedback/feedback.md`) where template-side `/feedback review` picks them up. Template-side sessions append maintenance items to `template-maintenance/feedback.md`. Before assigning a new `FB-NNN`, scan **all four files by exact filename** — they share one ID namespace.
- **Staged work inventories:** `template-maintenance/` (root) — deferred extractions and multi-stage plans (e.g., `scripts-candidates.md`)

These are template-maintenance artifacts that don't ship to projects.

## Active Follow-ups

Template-maintenance work staged for later sessions. Read these first if resuming template work after a gap.

**Active feedback items** (`template-maintenance/feedback.md` — triage manually; do NOT run `/feedback review` against this path, that command targets the shipped `.claude/support/feedback/` queue):

- **FB-011** (special-case): scripts tracker — Families A+B shipped (v3.0.0/3.1.1), **Family E dropped 2026-05-20** (v4.6.2 — no FB-017 regression during trial 2026-04-17 → 2026-05-17), C/D remain deferred per `template-maintenance/scripts-candidates.md`. Escalate Family C if `/health-check` Part 6 check 4b fires repeatedly; Family D triggers on observed real LLM-missed parallel conflicts.
- **FB-033** (special-case): spec-auditor subagent — trial-gated on FB-032 (Decisions in This Proposal structural contract, shipped 2026-04-17). Escalate to DEC-009 only if silent-decisions friction persists across `/iterate propose` sessions despite FB-032.
- **FB-060** (partial): file-ownership boundary — Phases 1+3+4+5 shipped (v3.14.2 + v3.15.0); Phase 2 (`sync_strict` category schema) deferred per DEC-014 § Decision. Re-open only if a real `project_extensible` category member emerges.
- **FB-062** (cheap action shipped, v3.14.1): two FB-NNN locations convention — root `CLAUDE.md` § File Boundary documents the four-file enumeration. Medium (rename to TM-NNN) / Higher (consolidate with `track:` field) options remain if dedup misses recur.
- **FB-063** (cheap action shipped, v3.14.1): background-session auto-worktree breaks gitignored-state reads — per-command note added to `/audit-coherence` + `/audit-ui`. Medium (extend preamble carve-out) / Higher (worktree bind-mount) options remain if other commands hit the same trap.
- **FB-067** (deferred): mattpocock/skills Wave 2 candidates — re-assess on/after 2026-06-02. **Wave 1 complete** — all four entries shipped 2026-05-20: FB-071 (v4.1.0), FB-068 (v4.2.0), FB-070 (v4.3.0), FB-069 (v4.4.0). Wave 2 candidates (`/tdd`, `/prototype`, `/improve-codebase-architecture`, `/caveman`, hard-vs-soft dep cleanup, bucketed skills) signal-gated on Wave 1 outcomes. Source: video https://www.youtube.com/watch?v=6BB6exR8Zd8 + repo `mattpocock/skills`.
- **FB-072** (CLOSED — DEC-018 → Option B): command routing as a UX pattern. Resolved 2026-05-24 — declined the interpretive-router proposal in favor of status quo (explicit-arg dispatch) after a value deep-dive found near-absent recall-the-token friction in CCE's 26-session usage logs (marginal value vs. permanent cost). Decision `decisions/decision-018-command-routing-interpretive-vs-explicit.md` (`approved`); boundary survey + research archive preserved. Re-open if Wave 2 materially grows the command surface (condition in DEC-018 Impact). The `/walkthrough` / `/preflight` sibling idea is available for separate re-capture.
- **FB-075** (cheap action shipped, v4.6.1): TaskCreate / TaskUpdate harness reminder noise — `.claude/README.md § Known Constraints` documents the unavoidable harness-emitted nudge as benign in projects using `.claude/tasks/*.json`. Structural fix (per-project opt-out) requires Anthropic-side mechanism (CLAUDE.md sentinel, settings hook, or per-project flag). Re-assess when (a) upstream offers such a mechanism, OR (b) token tax scales materially (currently ~10 fires/session, modest).
- **FB-076** (deferred, research-gated): verify-agent runtime_validation gaps — bundle-boundary breaks + catalog-state-dependent precondition gaps. Extends FB-066 (production-consumption check, shipped v3.16.0). Single-project signal (styler T667). Mitigations (production-build invocation, ESLint client-import rule, live-data cross-ref) less mechanical than FB-066's regex+grep — require design work. Re-assess when (a) 2nd project signals same pattern, OR (b) FB-066 downstream telemetry surfaces broader runtime_validation hardening need. If escalated: `/research` for design.
- **FB-077** (cheap action shipped, v4.6.3): auto-mode classifier false-positives — `.claude/README.md § Known Constraints` documents both sub-issues + workarounds. (a) DEC-016 scope over-broad on `.claude/support/reference/decisions.md`; workaround: explicit context-clarifying language, or typed-text user authorization. (b) AskUserQuestion responses don't count as classifier-bypass authorization; workaround: agents prefer free-text prompts for permission flows. Structural fixes upstream-Anthropic gated. Re-assess when Anthropic offers (a) per-path DEC-016 scope declaration, (b) AskUserQuestion authorization recognition, OR (c) workaround friction recurs across N sessions despite README docs.
- **FB-084** (cheap action shipped, v4.7.3): pre-retirement engine-consumer audit — new section in `.claude/rules/feature-retirement.md` covers 4-pattern grep (snake_case + CamelCase derivatives + shortened forms + string literals). Heavier route (extend FB-066 production-consumption check to proposal stage in `/research` / `/iterate distill`) deferred — research-gated + 2nd-project-signal-gated. Re-assess if (a) 2nd project signals same naming-derivative coverage gap, OR (b) FB-066 telemetry surfaces proposal-time parallel.
- **FB-085** (deferred, signal-gated): load-bearing browser-behavior assumption verification gap on `runtime_validation: partial` + `owner: both`. Writer/reviewer shared-premise blindspot (implement-agent + verify-agent both confirmed wrong premise; caught only by orchestrator-Playwright re-test). Single-project signal (styler T697). **Resolved design (`/visual-verify` grill 2026-05-24, `template-maintenance/visual-verify-vision.md`):** fold the empirical-verification loop into `/diagnose` as a `## Visual / browser-rendering bugs` recipe running at orchestrator level — which dissolves the original "fragile enforcement scope" blocker (the verify-agent subagent Playwright-sandbox problem) by routing the browser loop through the orchestrator, exactly as this entry's prior triage anticipated. General-merit half (outcome-not-mechanism hypothesis discipline) shipped to `/diagnose` Phase 3 in **v4.10.2**; the UI-specific recipe (~20 lines: geometry/computed-style assertion vocabulary + `browser_evaluate` measurement + N=3 outcome-guided loop + conditional persistence) stays captured in `template-maintenance/feedback.md` FB-085 § "Resolved design", ready to ship on a 2nd-project signal. Re-assess on 2nd project signal of same shared-premise failure.
*(FB-082 + FB-083 promoted via DEC-017 Option B; v4.9.0 shipped 2026-05-24. Both archived in `template-maintenance/feedback-archive.md`. DEC-017 implementation_anchors enumerate the 10-file ship.)*

**Shipped-queue items ready for action** (`.claude/support/feedback/feedback.md` — promoted via direct template edit OR `/research`, per per-item disposition):

*(All shipped-queue items are now archived. New `ready` items from `/feedback review` land here.)*

*(FB-006 archived 2026-05-16 — all four sub-issues closed via v3.17.1 + v3.18.0 + v3.19.0; entry now in `.claude/support/feedback/archive.md` with `**Status:** promoted`.)*
*(FB-007 archived 2026-05-16 — DEC-016 Option D shipped in v4.0.0; entry now in `.claude/support/feedback/archive.md` with `**Status:** promoted`.)*

**Recent ships:** the full version-by-version changelog moved to `template-maintenance/ship-log.md` on 2026-05-27 (it was 46k of this file's 60k chars — backward-looking history that doesn't need to load into context every session). Consult it for the rationale, FB/DEC linkage, and file-list of any past ship; append new ship entries there, not here.

**Audit family open follow-ups:**

- **Stage 7 (bundled-apply batch UX) deferred** per DEC-013 Q4 rollback analysis (all-or-nothing batch revert is materially worse than single-commit-per-finding). Reconsider after Stage 6 Option C telemetry accumulates.
- **Fix-eligible inline-apply expansion** gated on telemetry: ≥5 successful `[Fix it]` invocations on bundle-eligible findings across downstream projects + manual diff inspection sample for zero silent-corruption events. If clean: open follow-up DEC for fix-eligible expansion. If not: revisit Option F (add dry-run-first). Telemetry observable via `resolved_by.kind == "fix_it"` count in `friction.jsonl` + per-audit `digest.json items[].status` counts.

**Decision record status (as of 2026-05-16):** 11 of 12 records `implemented` with populated `implementation_anchors`. DEC-003 (subdirectory vs flat layout) stays `approved` — research conclusion with no implementation commit (template was already in flat layout).

## Version Bumping

A git pre-commit hook (`.git/hooks/pre-commit`) warns when sync-category files are committed without bumping `template_version` in `.claude/version.json`. The hook warns but does not block — commit proceeds with a reminder.

**SemVer policy (to be formalized):** Major = breaking changes to command interfaces or task schema. Minor = new features, new commands, significant behavior changes. Patch = bug fixes, wording improvements, threshold adjustments.

Since `.git/hooks/` isn't tracked by git, the hook must be installed manually in each clone. To install:
```bash
cp scripts/pre-commit-hook.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

## Testing

The `tests/` directory contains conceptual trace tests for the command definitions. These are not automated — they define a state, reference a command path, and specify expected behavior. Run them by tracing through the command logic to verify correctness. See `tests/README.md`.

## File Boundary

| Location | Purpose | Ships to projects? |
|----------|---------|:--:|
| `.claude/` | Environment that users get | Yes |
| `README.md` | Template documentation | No (users delete) |
| `CLAUDE.md` | This file — template context (replaced with project-specific `./CLAUDE.md` on setup) | Replaced |
| `system-overview.md` | Environment design reference — lifecycle, features, design intent | No (users delete) |
| `tests/` | Command verification scenarios | No (users delete) |
| `decisions/` | Template-level decision records (via `/research`) | No (users delete) |
| `scripts/` | Template maintenance scripts (pre-commit hook) | No (users delete) |
| `template-maintenance/` | Template-maintenance working docs: feedback log, ship log (`ship-log.md` — version changelog), staged work inventories (see Active Follow-ups) | No (users delete) |
| `interaction-logs/` | Cross-project session exports and derived insights | No (template repo only) |
| `.gitignore` | Repo config | Partially (users may keep) |
