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

- **FB-011** (special-case): scripts tracker — Families A+B shipped (v3.0.0/3.1.1), **Family E dropped 2026-05-20** (v4.6.2), **Family C CLOSED — full port shipped v4.22.0** (2026-06-11; PoC v4.19.0 → evidence run against styler's 218+620-task corpus → user "go"; `dashboard-render.py --render` owns all structural sections, LLM fills Action Required + Custom Views placeholders, `--task-hash` is the single hash authority; 54 tests; record in `template-maintenance/scripts-candidates.md § Family C` + ship-log v4.22.0). Family D remains deferred (triggers on observed real LLM-missed parallel conflicts; note 2026-06-11: the styler T729/T731 package.json collision was an *input-data* miss — under-declared files_affected — not a check-logic miss, so the trigger stands unmet).
- **FB-033** (special-case): spec-auditor subagent — trial-gated on FB-032 (Decisions in This Proposal structural contract, shipped 2026-04-17). Escalate to DEC-009 only if silent-decisions friction persists across `/iterate propose` sessions despite FB-032.
- **FB-060** (partial): file-ownership boundary — Phases 1+3+4+5 shipped (v3.14.2 + v3.15.0); Phase 2 (`sync_strict` category schema) deferred per DEC-014 § Decision. Re-open only if a real `project_extensible` category member emerges.
- **FB-062** (cheap action shipped, v3.14.1): two FB-NNN locations convention — root `CLAUDE.md` § File Boundary documents the four-file enumeration. Medium (rename to TM-NNN) / Higher (consolidate with `track:` field) options remain if dedup misses recur.
- **FB-063** (cheap action shipped, v3.14.1): background-session auto-worktree breaks gitignored-state reads — per-command note added to `/audit-coherence` + `/audit-ui`. Medium (extend preamble carve-out) / Higher (worktree bind-mount) options remain if other commands hit the same trap.
- **FB-067** (deferred — signal-gated; pruned 2026-06-12): mattpocock/skills Wave 2 candidates. **Wave 1 complete** — all four shipped 2026-05-20: FB-071 (v4.1.0), FB-068 (v4.2.0), FB-070 (v4.3.0), FB-069 (v4.4.0). **Re-assessed 2026-06-12** (manual maintenance review): the 2026-06-02 recheck fired empty (ripgrep + positive control → zero downstream signal for any candidate). **Closed** `/caveman` (token-compression absorbed by the 1M context window) + hard-vs-soft dep cleanup (cosmetic); **kept signal-gated** `/tdd`, `/prototype`, `/improve-codebase-architecture`, bucketed skills; **dropped the fixed recheck date** for pure signal-gating + a 2026-12-12 backstop. Source: video https://www.youtube.com/watch?v=6BB6exR8Zd8 + repo `mattpocock/skills`.
- **FB-072** (CLOSED — DEC-018 → Option B): command routing as a UX pattern. Resolved 2026-05-24 — declined the interpretive-router proposal in favor of status quo (explicit-arg dispatch) after a value deep-dive found near-absent recall-the-token friction in CCE's 26-session usage logs (marginal value vs. permanent cost). Decision `decisions/decision-018-command-routing-interpretive-vs-explicit.md` (`approved`); boundary survey + research archive preserved. Re-open if Wave 2 materially grows the command surface (condition in DEC-018 Impact). The `/walkthrough` / `/preflight` sibling idea is available for separate re-capture.
- **FB-075** (cheap action shipped, v4.6.1): TaskCreate / TaskUpdate harness reminder noise — `.claude/README.md § Known Constraints` documents the unavoidable harness-emitted nudge as benign in projects using `.claude/tasks/*.json`. Structural fix (per-project opt-out) requires Anthropic-side mechanism (CLAUDE.md sentinel, settings hook, or per-project flag). Re-assess when (a) upstream offers such a mechanism, OR (b) token tax scales materially (currently ~10 fires/session, modest).
- **FB-076** (mitigation 1 shipped v4.15.0; rest deferred, research-gated): verify-agent runtime_validation gaps — bundle-boundary breaks now caught by `/work`'s Empirical Evidence Gate production-build check (client-marked files + root `./CLAUDE.md § Verification Hooks` build command); catalog-state-dependent precondition gaps (mitigation 3: live-data cross-ref) + ESLint client-import rule (mitigation 2) remain deferred. Extends FB-066. Single-project signal (styler T667). Re-assess remaining when (a) 2nd project signals same pattern, OR (b) FB-066 telemetry surfaces broader runtime_validation hardening need. If escalated: `/research` for design.
- **FB-077** (cheap action shipped, v4.6.3): auto-mode classifier false-positives — `.claude/README.md § Known Constraints` documents both sub-issues + workarounds. (a) DEC-016 scope over-broad on `.claude/support/reference/decisions.md`; workaround: explicit context-clarifying language, or typed-text user authorization. (b) AskUserQuestion responses don't count as classifier-bypass authorization; workaround: agents prefer free-text prompts for permission flows. Structural fixes upstream-Anthropic gated. Re-assess when Anthropic offers (a) per-path DEC-016 scope declaration, (b) AskUserQuestion authorization recognition, OR (c) workaround friction recurs across N sessions despite README docs.
- **FB-084** (cheap action shipped, v4.7.3): pre-retirement engine-consumer audit — new section in `.claude/rules/feature-retirement.md` covers 4-pattern grep (snake_case + CamelCase derivatives + shortened forms + string literals). Heavier route (extend FB-066 production-consumption check to proposal stage in `/research` / `/iterate distill`) deferred — research-gated + 2nd-project-signal-gated. Re-assess if (a) 2nd project signals same naming-derivative coverage gap, OR (b) FB-066 telemetry surfaces proposal-time parallel.
*(FB-095 resolved 2026-06-12 — `/research` → **DEC-021 Option 2** shipped in **v4.24.0**: single file + generated spec section index + section-scoped read discipline. `fingerprint.py --index` + `--sections --depth 3` (additive `### ` hashes); canonical `rules/spec-workflow.md § "Section-scoped spec reading"`; `work.md` Step 1b index-freshness regen; subagent scoped-read pointers. **Preserves the "exactly one `spec_v{N}.md`" Critical Invariant** (sharding/tiering declined on the blast-radius asymmetry). DEC-021 `implemented` (7 anchors); full FB entry archived; research archive `.archive/decision-021-research-2026-06-12.md`. **Companion follow-up available:** wire `drift-reconciliation` to *consume* the `### ` granularity the script now emits — optional, separate from this ship. **Option 1 (shard)** remains the documented escalation if edit-ergonomics/git-diff-noise later dominates over read-working-set.)*
*(FB-096 resolved 2026-06-11 — sub-issue A docs-verified + capability-doc section rewritten in **v4.21.3** (drift was broader than the `fable`-only capture: full model IDs, `inherit`, resolution order, per-agent `effort:` all added); sub-issue B decided → **option (a) ratify the float**, shipped **v4.21.4** (`.claude/CLAUDE.md § Model Requirement` targets the current Opus tier via `opus[1m]`; explicit-pin regression escape hatch documented). Full entry + both resolution notes in `template-maintenance/feedback-archive.md`.)*
*(FB-097 resolved 2026-06-12 — `/research` → **DEC-022 Option D (A + C)** shipped in **v4.26.0**. Declares `.claude/verification-result.json` `criteria[]` (dashboard `### Acceptance Criteria`) the authoritative phase acceptance-*status* surface; inline spec `- [ ]` boxes are authored input, not live status (an optional convention the template never mandated); new advisory `/audit-coherence` `acceptance-reconciliation` lens flags box-vs-`criteria[]` divergence (`kind: decision` → `/iterate`). Research **declined the FB-097-leaned Option B** (auto-tick spec boxes): unsafe `criteria[]`→box mapping (free-text, no ID link — DEC-022 Q2), drift-fingerprint cost (Finished→Pending reset risk — Q5), and the RTM/BDD/DOORS "don't write status into the authored doc" anti-pattern (Q4). DEC-022 `implemented` (6 anchors); full FB entry archived; research archive `.archive/decision-022-research-2026-06-12.md`. Net: zero edits to verify-agent / work completion flow / settings.json / drift-reconciliation — the economy of A+C over B.)*
*(FB-098 + FB-099 + FB-100 promoted 2026-06-12 — shipped together in **v4.23.0** (3-FB `/work`-family bundle from a `/feedback review` of the maintenance queue). FB-098 = new `.claude/scripts/persist-friction.py` (+11 tests, suite 65/65) mechanizing the friction dual-write + collision-safe `FR-NNN` (read-only; orchestrator appends); FB-099 = `/work` Step 0e gitignore-scoping + `/health-check` Part 4.5 untracked-source-of-truth check; FB-100 = Step 1d `owner:both` predicate + the both-owned completion shape in `work-procedures.md`. Full entries in `template-maintenance/feedback-archive.md`; durable record in ship-log v4.23.0. **FB-097** — promoted 2026-06-12 via DEC-022 (Option D), shipped v4.26.0 (see resolved note above).)*
*(FB-082 + FB-083 promoted via DEC-017 Option B; v4.9.0 shipped 2026-05-24. Both archived in `template-maintenance/feedback-archive.md`. DEC-017 implementation_anchors enumerate the 10-file ship.)*
*(FB-085 promoted 2026-06-10 — `/diagnose` `## Visual / browser-rendering bugs` recipe shipped in **v4.13.0** after user gate-override; full entry archived in `template-maintenance/feedback-archive.md`. General-merit half had shipped v4.10.2. Absorbs the signal-queue "math-check before commit-to-pixels" item. Trace test: `tests/scenarios/32-diagnose-visual-recipe.md`.)*

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
