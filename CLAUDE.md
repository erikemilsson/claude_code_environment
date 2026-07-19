# Template Repository Context

**You are working on the template itself, not on a project that uses the template.**

The `.claude/` directory contains the environment that ships to new projects. The root-level files (this file, `README.md`, `tests/`) are template maintenance infrastructure.

## What This Means

- **Don't fill in template placeholders** — sections like `[Brief description]` and `[Your license here]` are intentionally blank
- **Don't create project-specific content** — no real specs, tasks, or decisions
- **Don't run `/work` or `/iterate` as if building a project** — these commands are what you're maintaining, not using
- **The spec file (`.claude/spec_v1.md`) should stay as a placeholder** — it's a template for users to fill in
- **The dashboard is a generated, gitignored HTML artifact (`.claude/dashboard.html`, DEC-024)** — produced by `dashboard-render.py --html` from task JSON + the `dashboard-state.json` sidecar. The template ships **no** dashboard file (it's derived); a fresh project generates one on first `/work`. There is no hand-written format example to maintain — the script is the generator (its tests in `.claude/scripts/tests/` pin the format).

## What You Should Do

- **Edit command definitions** (`.claude/commands/*.md`) to improve workflow logic
- **Edit agent definitions** (`.claude/agents/*.md`) to improve implementation/verification
- **Edit reference docs** (`.claude/support/reference/*.md`) to improve patterns and schemas
- **Edit `.claude/CLAUDE.md`** to improve environment instructions (template-owned core)
- **Edit `.claude/rules/*.md`** to improve modular workflow rules
- **Edit `.claude/README.md`** to improve the user-facing environment guide
- **Run conceptual tests** (`tests/scenarios/`) after significant command changes
- **Use `[bracketed text]` for user-customizable placeholder sections** (the dashboard is no longer an exception — it's generated HTML, not a shipped file; DEC-024)

## Template Maintenance Workflow

When making changes to the template, use the `.claude/` command definitions as reference for what you're editing — but don't use the `.claude/` spec/task/dashboard/decision workflow to manage the template's own work (those are template content, not tools).

- **Topology reference:** `template-maintenance/architecture-map.md` — component wiring, state-file ownership, load order, and the blast-radius table ("change X → check Y"). Update it when topology changes (the pre-commit hook reminds on structural changes); bump its `Current as of` line when reconciled. Behavior truth lives in the shipped files themselves; change rationale in root `decisions/` + `ship-log.md`; every version is git-tagged (`v{X.Y.Z}`) for diffs and reverts.
- **`system-overview.md` was deleted 2026-07-19 (v5.1.1)** — it was the stale pre-v4 design reference and the old template-repo sentinel. The sentinel is now the **`template-maintenance/` directory** at the project root (checked by `/health-check` Parts 5/5d/7 and `scripts/pre-commit-hook.sh` — don't rename that folder). Historical content: `git show v5.1.0:system-overview.md`
- **Decision records:** `decisions/` (root) — for formal decisions about template changes via `/research`
- **Feedback (four files; see FB-062 for the convention):**
  - `.claude/support/feedback/feedback.md` (shipped, active) + `archive.md` (shipped, resolved) — `/feedback review` triages.
  - `template-maintenance/feedback.md` (maintenance, active) + `feedback-archive.md` (maintenance, resolved) — manual triage. Append manually; do NOT use `/feedback` here.

  **Naming-asymmetry trap:** the maintenance archive is `feedback-archive.md`, NOT `archive.md`. Dedup checks that probe `template-maintenance/archive.md` will silently report "does not exist" and miss predecessors (observed 2026-05-15: FB-004 + FB-005 captured as duplicates of already-shipped FB-042 + FB-056 because of this exact miss; see FB-062 § "Observed empirical instances").

  **Cross-project capture pattern:** downstream-project sessions write template-fix items to the **shipped** location (`.claude/support/feedback/feedback.md`) where template-side `/feedback review` picks them up. Template-side sessions append maintenance items to `template-maintenance/feedback.md`. Before assigning a new `FB-NNN`, scan **all four files by exact filename** — they share one ID namespace.
- **Staged work inventories:** `template-maintenance/` (root) — deferred extractions and multi-stage plans (e.g., `scripts-candidates.md`)

These are template-maintenance artifacts that don't ship to projects.

## Active Follow-ups

Template-maintenance work staged for later sessions. Read these first if resuming template work after a gap. **This section keeps only open items and their re-open gates** (trimmed 2026-07-19) — resolved-item narrative lives in `template-maintenance/ship-log.md` + `template-maintenance/feedback-archive.md`.

**DEC-023 (vision hub + spec-shaping, v4.28.0–v4.31.0) and DEC-024 (HTML dashboard, v5.0.0–v5.1.0) — COMPLETE, no open follow-ups.** Records `implemented` in `decisions/`; per-ship detail in ship-log. *Caveat on DEC-024's record + research archive:* they mislabel the broken-mermaid bug as "FB-007" — wrong (real FB-007 = spec-edit guardrail, DEC-016/v4.0.0); no FB tracked mermaid.

**Open (DEC-021 companion, optional/unscheduled):** wire `drift-reconciliation.md` to consume the `### `-level section hashes `fingerprint.py --sections` emits (DEC-021 shipped the emitter in v4.24.0; nothing consumes that granularity yet). If edit-ergonomics/git-diff-noise ever dominates read-working-set, DEC-021 Option 1 (shard) is the documented escalation.

**Active feedback items** (`template-maintenance/feedback.md` — triage manually; do NOT run `/feedback review` against this path, that command targets the shipped `.claude/support/feedback/` queue):

- **FB-011** (special-case, scripts tracker): only **Family D** (deterministic parallel-conflict check) remains open — deferred, triggers on an observed real LLM-missed parallel conflict (2026-06-11: the styler T729/T731 collision was an input-data miss — under-declared `files_affected` — not check-logic, so the trigger stands unmet). Families A+B+C shipped (v3.0.0 → v4.22.0; C superseded by DEC-024's HTML renderer in v5.0.0), Family E dropped (v4.6.2). Full history: `template-maintenance/scripts-candidates.md` + ship-log.
- **FB-033** (special-case): spec-auditor subagent — trial-gated on FB-032 (Decisions in This Proposal structural contract, shipped 2026-04-17). Escalate to DEC-009 only if silent-decisions friction persists across `/iterate propose` sessions despite FB-032.
- **FB-060** (partial): file-ownership boundary — Phases 1+3+4+5 shipped (v3.14.2 + v3.15.0); Phase 2 (`sync_strict` category schema) deferred per DEC-014 § Decision. Re-open only if a real `project_extensible` category member emerges.
- **FB-062** (cheap action shipped, v3.14.1): two FB-NNN locations convention — root `CLAUDE.md` § File Boundary documents the four-file enumeration. Medium (rename to TM-NNN) / Higher (consolidate with `track:` field) options remain if dedup misses recur.
- **FB-063** (cheap action shipped, v3.14.1): background-session auto-worktree breaks gitignored-state reads — per-command note added to `/audit-coherence` + `/audit-ui`. Medium (extend preamble carve-out) / Higher (worktree bind-mount) options remain if other commands hit the same trap.
- **FB-067** (deferred — signal-gated): mattpocock/skills Wave 2 — `/tdd`, `/prototype`, `/improve-codebase-architecture`, bucketed skills remain signal-gated (no fixed recheck date; backstop 2026-12-12). Wave 1 shipped 2026-05-20 (v4.1.0–v4.4.0); `/caveman` + dep-cleanup closed 2026-06-12 (recheck fired empty with positive control). Source: repo `mattpocock/skills` + video https://www.youtube.com/watch?v=6BB6exR8Zd8.
- **FB-072** (CLOSED — DEC-018 Option B, 2026-05-24): interpretive command routing declined for explicit-arg status quo (near-absent recall friction across 26 session logs). Re-open if Wave 2 materially grows the command surface (condition in DEC-018 Impact). `/walkthrough` / `/preflight` sibling idea available for separate re-capture.
- **FB-075** (cheap action shipped, v4.6.1): TaskCreate / TaskUpdate harness reminder noise — `.claude/README.md § Known Constraints` documents the unavoidable harness-emitted nudge as benign in projects using `.claude/tasks/*.json`. Structural fix (per-project opt-out) requires Anthropic-side mechanism (CLAUDE.md sentinel, settings hook, or per-project flag). Re-assess when (a) upstream offers such a mechanism, OR (b) token tax scales materially (currently ~10 fires/session, modest).
- **FB-076** (mitigation 1 shipped v4.15.0; rest deferred, research-gated): verify-agent runtime_validation gaps — bundle-boundary breaks now caught by `/work`'s Empirical Evidence Gate production-build check (client-marked files + root `./CLAUDE.md § Verification Hooks` build command); catalog-state-dependent precondition gaps (mitigation 3: live-data cross-ref) + ESLint client-import rule (mitigation 2) remain deferred. Extends FB-066. Single-project signal (styler T667). Re-assess remaining when (a) 2nd project signals same pattern, OR (b) FB-066 telemetry surfaces broader runtime_validation hardening need. If escalated: `/research` for design.
- **FB-077** (cheap action shipped, v4.6.3): auto-mode classifier false-positives — `.claude/README.md § Known Constraints` documents both sub-issues + workarounds. (a) DEC-016 scope over-broad on `.claude/support/reference/decisions.md`; workaround: explicit context-clarifying language, or typed-text user authorization. (b) AskUserQuestion responses don't count as classifier-bypass authorization; workaround: agents prefer free-text prompts for permission flows. Structural fixes upstream-Anthropic gated. Re-assess when Anthropic offers (a) per-path DEC-016 scope declaration, (b) AskUserQuestion authorization recognition, OR (c) workaround friction recurs across N sessions despite README docs. **Trigger-(c) candidate observed:** the styler 2026-07-06 session export reports the classifier blocking template-sanctioned `/work` Step 0f cleanup — assess at the next inbox harvest.
- **FB-084** (cheap action shipped, v4.7.3): pre-retirement engine-consumer audit — new section in `.claude/rules/feature-retirement.md` covers 4-pattern grep (snake_case + CamelCase derivatives + shortened forms + string literals). Heavier route (extend FB-066 production-consumption check to proposal stage in `/research` / `/iterate distill`) deferred — research-gated + 2nd-project-signal-gated. Re-assess if (a) 2nd project signals same naming-derivative coverage gap, OR (b) FB-066 telemetry surfaces proposal-time parallel.
**Shipped-queue** (`.claude/support/feedback/feedback.md`): empty — all items archived in `.claude/support/feedback/archive.md`; new `ready` items from `/feedback review` land here.

**Recent ships:** the full version-by-version changelog moved to `template-maintenance/ship-log.md` on 2026-05-27 (it was 46k of this file's 60k chars — backward-looking history that doesn't need to load into context every session). Consult it for the rationale, FB/DEC linkage, and file-list of any past ship; append new ship entries there, not here.

**Audit family open follow-ups:**

- **Stage 7 (bundled-apply batch UX) deferred** per DEC-013 Q4 rollback analysis (all-or-nothing batch revert is materially worse than single-commit-per-finding). Reconsider after Stage 6 Option C telemetry accumulates.
- **Fix-eligible inline-apply expansion** gated on telemetry: ≥5 successful `[Fix it]` invocations on bundle-eligible findings across downstream projects + manual diff inspection sample for zero silent-corruption events. If clean: open follow-up DEC for fix-eligible expansion. If not: revisit Option F (add dry-run-first). Telemetry observable via `resolved_by.kind == "fix_it"` count in `friction.jsonl` + per-audit `digest.json items[].status` counts.

**Decision record status (as of 2026-07-19):** 21 records; 18 `implemented` with anchors. `approved` exceptions: DEC-003 (flat layout) + DEC-018 (command routing) — research conclusions with no implementation commit, correct as-is; DEC-017 shipped in v4.9.0 but its `status:` flag was never flipped to `implemented` (flip at next housekeeping pass).

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
| `tests/` | Command verification scenarios | No (users delete) |
| `decisions/` | Template-level decision records (via `/research`) | No (users delete) |
| `scripts/` | Template maintenance scripts (pre-commit hook) | No (users delete) |
| `template-maintenance/` | Template-maintenance working docs: feedback log, ship log (`ship-log.md` — version changelog), staged work inventories (see Active Follow-ups) | No (users delete) |
| `interaction-logs/` | Cross-project session exports and derived insights | No (template repo only) |
| `.gitignore` | Repo config | Partially (users may keep) |
