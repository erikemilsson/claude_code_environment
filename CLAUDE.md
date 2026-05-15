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

Template-maintenance work staged for later sessions. Read these first if resuming template work after a gap:

- **FB-011 scripts extraction.** Families A + B landed in v3.0.0 (`.claude/scripts/fingerprint.py` + `validate-tasks.py`); bug-fixed in v3.1.1 (FB-039: `task_id` → `id` field). Families C/D/E remain deferred per `template-maintenance/scripts-candidates.md`:
  - **Family C (dashboard regen):** new trigger (2026-05-13) — escalate if `health-check.md` Part 6 check 4b (FB-038 ship) fires repeatedly across downstream projects.
  - **Family D (parallel-plan):** trigger on observed real conflicts the LLM misses.
  - **Family E (decision finalization):** 30-day trial window 2026-04-17 → 2026-05-17. Re-assess on or after 2026-05-17.
- **Feedback backlog.** `template-maintenance/feedback.md` currently holds 2 active items after the May 2026 Phase 4 pass + DEC-010/DEC-011 ships:
  - **FB-011** (special-case): scripts tracker — Families A+B shipped, C/D/E deferred per `template-maintenance/scripts-candidates.md`.
  - **FB-033** (special-case): spec-auditor subagent — trial-gated on FB-032 (DEC-009 if escalated).
  - **DEC-010 shipped 2026-05-13 (v3.4.0):** Option C — `partial_completion` envelope for usage-limit graceful resume. Decision record: `decisions/decision-010-partial-completion-envelope.md`. Promoted FB-049.
  - **DEC-011 shipped 2026-05-13 (v3.5.0):** Option ABp — Hybrid A+B + `.pending-markers.jsonl` transient buffer for Track 1 pipeline reliability. Decision record: `decisions/decision-011-track1-pipeline-execution.md`. Promoted FB-057.
  - Triage manually by reading the file and re-assessing; do not run `/feedback review` against it (that command targets the shipped `.claude/support/feedback/` path).
- **DEC-009 / FB-033 trial gate.** FB-032 (Decisions in This Proposal structural contract) shipped 2026-04-17 in `.claude/commands/iterate.md`. Trial accumulates as downstream projects run `/iterate propose` sessions. If silent-decisions friction persists despite FB-032, escalate to DEC-009 (spec-auditor subagent research).
- **Audit family shipped 2026-05-15 (v3.6.0 → v3.12.0, 7 commits).** 6.5 of 7 stages from `template-maintenance/audit-command-family-proposal.md`. Highlights: dashboard slim (META whitelist + Recent Activity cap); friction register at `.claude/support/friction.jsonl`; new commands `/audit-coherence` (6 lenses) + `/audit-ui` (7 lenses + mobile, migrated from Styler) dispatched by `/health-check` Part 8; persistent `🔍 Audit Findings` dashboard section with `[Promote to FB] / [Dismiss]`; `[Fix it]` inline-apply for `bundle-eligible` kind only (per DEC-013 Option C). Decision record: `decisions/decision-013-audit-fix-it-autonomy-boundary.md`. **Two open follow-ups:**
  - **Stage 7 (bundled-apply batch UX) deferred** per DEC-013 Q4 rollback analysis (all-or-nothing batch revert is materially worse than single-commit-per-finding). Reconsider after Stage 6 Option C telemetry accumulates.
  - **Fix-eligible inline-apply expansion** gated on telemetry validation: ≥5 successful `[Fix it]` invocations on bundle-eligible findings across downstream projects + manual diff inspection sample for zero silent-corruption events. If clean: open follow-up DEC for fix-eligible expansion. If not: revisit Option F (add dry-run-first). Telemetry observable via `resolved_by.kind == "fix_it"` count in `friction.jsonl` + per-audit `digest.json items[].status` counts.

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
