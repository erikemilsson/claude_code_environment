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

- **FB-011** (special-case): scripts tracker — Families A+B shipped (v3.0.0/3.1.1), C/D/E deferred per `template-maintenance/scripts-candidates.md`. Re-assess Family E on/after 2026-05-17 (30-day trial window 2026-04-17 → 2026-05-17 closing); escalate Family C if `/health-check` Part 6 check 4b fires repeatedly; Family D triggers on observed real LLM-missed parallel conflicts.
- **FB-033** (special-case): spec-auditor subagent — trial-gated on FB-032 (Decisions in This Proposal structural contract, shipped 2026-04-17). Escalate to DEC-009 only if silent-decisions friction persists across `/iterate propose` sessions despite FB-032.
- **FB-060** (partial): file-ownership boundary — Phases 1+3+4+5 shipped (v3.14.2 + v3.15.0); Phase 2 (`sync_strict` category schema) deferred per DEC-014 § Decision. Re-open only if a real `project_extensible` category member emerges.
- **FB-062** (cheap action shipped, v3.14.1): two FB-NNN locations convention — root `CLAUDE.md` § File Boundary documents the four-file enumeration. Medium (rename to TM-NNN) / Higher (consolidate with `track:` field) options remain if dedup misses recur.
- **FB-063** (cheap action shipped, v3.14.1): background-session auto-worktree breaks gitignored-state reads — per-command note added to `/audit-coherence` + `/audit-ui`. Medium (extend preamble carve-out) / Higher (worktree bind-mount) options remain if other commands hit the same trap.

**Shipped-queue items ready for action** (`.claude/support/feedback/feedback.md` — promoted via direct template edit OR `/research`, per per-item disposition):

- **FB-006** (partial, v3.17.1 PATCH iteration shipped): audit-findings dashboard/CLI workflow — courier pattern (dashboard tick → CLI re-specification), audit-name memory burden, dead `[Promote to FB] / [Dismiss]` inline text, opacity at decision moment (no plain-English description on dashboard). Iteration 1 (PATCH, v3.17.1) shipped: dropped per-finding `[Promote to FB] / [Dismiss]` inline text from dashboard render (closes sub-issue 3); `[Fix it]` retained for bundle-eligible (no keyword alternative); non-bundle-eligible kinds now show only the italicized kind annotation; `dashboard-regeneration.md` + `dashboard-style/SKILL.md` (mirror) + `audit-fix-workflow.md` example updated. **Deferred to future iterations:** MINOR — plain-English description per finding (closes sub-issue 4) requires `support/audits/<name>/digest.json` schema extension (`plain_english_description` field) + digest synthesizer change in `commands/audit-coherence.md` + `commands/audit-ui.md`. MINOR — `/audit-coherence triage` interactive walker (closes sub-issues 1+2, eliminates audit-name memory burden and courier pattern) — new subcommand. MINOR-or-deferred — dual-checkbox promote-vs-dismiss column; reconsider after `/audit-coherence triage` ships (single triage command may obsolete the need). Precursor to deferred Audit family Stage 7 (bundled-apply batch UX).
- **FB-007** (ready, /research routing): Claude direct-edit guardrail on `.claude/spec_v*.md` — rule tension between `spec-workflow.md` "Direct edits to the spec are always safe" and audit `iterate_routing: /iterate`. Three architectural alternatives: explicit rule override (audit-sourced edits MUST route through `/iterate`), size-based carveout (drift sweep <N lines), PreToolUse permission-layer gate (intercept Edit on spec files). Option 3 is an inflection point (structural permission-layer change). User disposition 2026-05-16: open via `/research` → DEC-NNN to evaluate the three together. DEC-013 secured the audit-system surface (HARD RULE at `audit-coherence.md:394` for `[Fix it]`); FB-007 secures Claude's general Edit-tool usage on the same files outside the audit fix-it flow. Surface: `rules/spec-workflow.md` (primary), possibly `rules/agents.md`, `.claude/settings.json` PreToolUse for Option 3.

**Recent ships:**

- **v3.4.0 (2026-05-13)** — DEC-010 Option C: `partial_completion` envelope for usage-limit graceful resume (`decisions/decision-010-partial-completion-envelope.md`). Promoted FB-049.
- **v3.5.0 (2026-05-13)** — DEC-011 Option ABp: hybrid A+B + `.pending-markers.jsonl` transient buffer for Track 1 pipeline reliability (`decisions/decision-011-track1-pipeline-execution.md`). Promoted FB-057.
- **v3.6.0 → v3.12.0 (2026-05-15, 7 commits)** — Audit family: 6.5 of 7 stages from `template-maintenance/audit-command-family-proposal.md`. Dashboard slim (META whitelist + Recent Activity cap); friction register at `.claude/support/friction.jsonl`; commands `/audit-coherence` (6 lenses) + `/audit-ui` (7 lenses + mobile) dispatched by `/health-check` Part 8; persistent `🔍 Audit Findings` dashboard section with `[Promote to FB] / [Dismiss]`; `[Fix it]` inline-apply for `bundle-eligible` kind only per DEC-013 Option C (`decisions/decision-013-audit-fix-it-autonomy-boundary.md`).
- **v3.14.0 → v3.14.2 (2026-05-16)** — FB-003 feature-retirement workflow rule promoted; FB-062 + FB-063 cheap actions shipped; FB-060 Phases 1 + 5 (Cross-Project Capture Protocol in `.claude/rules/agents.md` + new `.claude/support/reference/extension-hooks.md`).
- **v3.15.0 (2026-05-16)** — DEC-014 Option F: `.claude/.sync-state.json` sidecar + `/health-check` Part 5 2-condition algorithm refinement (`decisions/decision-014-sync-state-and-file-ownership-categories.md`). Closes FB-059; partially closes FB-060.
- **v3.16.0 (2026-05-16)** — FB-065 + FB-066 promoted: 5th heuristic on FB-058's Pre-Pass table (decomposition-time enum-extension ripple inference) + production-consumption check in verify-agent Step T5 (catches class-export integration gaps).
- **v3.17.0 (2026-05-16)** — FB-064 promoted: Test-Harness Awareness section added to decomposition.md + SKILL.md (mirror). Detects runtime-shaped tasks (`interaction_hint: cli_direct`, runtime-surface globs, runtime/UI `test_protocol`); scans for conventional harness directories with root `./CLAUDE.md` opt-in for custom paths; proposes scenario-authoring `_h` subtask when harness exists. Bridged from echothread `FB-009`.
- **v3.17.1 (2026-05-16)** — FB-006 PATCH iteration 1: dropped per-finding `[Promote to FB] / [Dismiss]` inline text from dashboard audit-findings render (closes FB-006 sub-issue 3 "dead UI"). `[Fix it]` retained for bundle-eligible (no keyword alternative); non-bundle-eligible kinds show italicized kind annotation only. `dashboard-regeneration.md` § "Audit Findings sub-section" + `dashboard-style/SKILL.md` mirror + `audit-fix-workflow.md` example updated; new "How to act on findings" sub-section documents promote (tick + bulk CLI) and dismiss (natural-language) invocation patterns. Plain-English description (sub-issue 4) + `/audit-coherence triage` (sub-issues 1+2) + dual-checkbox column deferred to future MINOR iterations.

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
| `template-maintenance/` | Template-maintenance working docs: feedback log, staged work inventories (see Active Follow-ups) | No (users delete) |
| `interaction-logs/` | Cross-project session exports and derived insights | No (template repo only) |
| `.gitignore` | Repo config | Partially (users may keep) |
