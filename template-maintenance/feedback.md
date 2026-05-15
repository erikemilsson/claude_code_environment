# Feedback Log

Items are captured via `/feedback` and triaged via `/feedback review`.

---

## FB-011: Explore scripts as alternative to commands or within skills folders

**Status:** ready
**Captured:** 2026-04-08
**Refined:** 2026-04-14 — Identify command procedures where a deterministic script would outperform LLM-executed natural-language instructions — starting with the dashboard, where output variation across regenerations makes the artifact harder to comprehend. Scripts could live alongside commands or inside skills folders if that's a valid pattern. Gains: (1) consistency of standardized artifacts, (2) reduced error rate from procedure drift, (3) lower token cost. Scope is exploratory — inventory candidates and propose which procedures to extract before committing.
**Assessed:** 2026-04-14 — Primary target is dashboard regeneration (touching `.claude/support/reference/dashboard-regeneration.md`, `.claude/rules/dashboard.md`, and call sites in implement-agent Steps 3, 6a, 6c). Shipping scripts needs a new home (likely `.claude/scripts/` — root `scripts/` is template-maintenance and does not ship). Conflict: `rules/agents.md` restricts Bash, and scripts depend on it — connects to FB-010 (subagent Bash sandbox limits). Dependencies: FB-017 (checkbox detection is a concrete second candidate). Scope: start with a workspace inventory doc (`.claude/support/workspace/scripts-candidates.md`) listing candidates with tradeoffs; first extraction targets dashboard regen.

Look into where scripts could be used instead of commands, or even perhaps as part of skills folders if that is a valid use-case. Needs to be more robust or save tokens or minimize errors, improve quality etc.

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

## FB-059: `/health-check` Part 5 selective sync conflates unsynced template content with genuine local additions (false-positive SKIP)

**Status:** new
**Captured:** 2026-05-15
**Source:** observed during downstream Styler `/health-check` after audit family v3.12.0 ship.

**Observation:** Part 5 (Template Sync Check) flagged two files as having "local additions" and offered selective sync that would SKIP both. Inspection showed the flag was correct for one file and a false-positive for the other:

- **`.claude/skills/dashboard-style/SKILL.md`** — 100% false positive. The diff was purely Stage 6 Option C content (kind-conditional `[Fix it]` action labels for the audit findings sub-section) that template shipped in v3.12.0 but Styler's local copy never received. Styler's `version.json` correctly read `template_version: 3.12.0` (the version field synced) but the file content stayed at Stage 6a state. Skipping the SKILL.md sync per the menu offer would have permanently prevented Styler from rendering `[Fix it]` labels until manual reconciliation.
- **`.claude/CLAUDE.md`** — correct flag. Styler genuinely added 2 project-specific rule imports (`brand-mention-provenance.md` per DEC-060, `feature-retirement.md` per FB-070 / § 27.1) plus their summary-table rows.

**Root cause hypothesis:** Part 5's detection compares downstream's *current* file content to template's *new* file content; any line-level diff is treated as a "local addition" warranting skip. This conflates two distinct conditions:
- (a) Downstream has unsynced template content (was at template_version N, template is at N+1, file content didn't sync along with the version field) → should sync
- (b) Downstream has genuinely user-added local content (file was customized after the last sync) → should preserve

The current algorithm can't distinguish these without per-file last-synced state.

**Proposed detection refinement:** Part 5 should compare downstream's file content to *the template version it last synced from*, not the *current template version*. The diff vs last-synced-version reveals genuine local additions. The diff vs current-template reveals all changes (sync delta + local additions). The intersection is what to sync without conflict; the symmetric difference is what to preserve as local. Requires the sync to record per-file last-synced template_version (or content hash). Could live in `dashboard-state.json` or a new `.claude/.sync-state.json` sidecar.

**Practical impact during this observation:** zero immediate harm because the `/audit-coherence` run that triggered the discovery had 0 bundle-eligible findings (so the missing `[Fix it]` labels weren't rendering anywhere). But future audits in Styler with bundle-eligible findings would have rendered with stale Stage 6a labels until manually reconciled.

**Workaround for affected projects (until Part 5 is refined):** when Part 5 offers selective sync, manually review the diff for each "skip" candidate via `diff <template-path> <project-path>`. If the diff is purely template content (lines present in template but not project), override the skip or manually copy the new template content into the project's file.

**Likely route:** scope-add to a new `/health-check` Part 5 refinement (not FB-058 — that's about `/work` decomposition path validation). Worth a research-light to confirm the proposed sidecar-based detection is feasible without restructuring the sync engine. Could also incorporate a "show me the diff" sub-action in the Part 5 menu so users can manually adjudicate per file.

## FB-060: Template-owned vs project-owned file ownership boundary not enforced or discoverable

**Status:** new
**Captured:** 2026-05-15
**Source:** surfaced during FB-059 root-cause investigation. The Styler local-additions case wasn't a one-off — it exposes a structural gap: the template documents file ownership as a convention but ships no enforcement, no detection, and no documented extension pattern.

**Observation:** Template files are conceptually split into ownership categories but the template doesn't make this machine-readable or user-discoverable. Three concrete failure modes observed via Styler:

1. **`.claude/CLAUDE.md` (template-owned) was modified by Styler** to add 2 project-specific rule imports + summary rows. The file's own preamble says `"This file is template-owned — do not edit directly. Project-specific instructions belong in ./CLAUDE.md (project root)."` — but nothing prevents or warns against the violation. Convention exists; enforcement doesn't.
2. **`.claude/skills/dashboard-style/SKILL.md` (template-owned)** got the same false-positive treatment from `/health-check` Part 5 even though it had zero local additions (FB-059) — because Part 5 doesn't know which files are template-owned vs project-extensible.
3. **Discoverability gap:** nowhere in the template is the extension pattern explicitly documented. A user wanting to add project-specific rule imports has to infer that root `./CLAUDE.md` is the right home (rather than `.claude/CLAUDE.md`). The template's `setup-checklist.md`, README, and rules files don't surface this.

**Three sub-concerns to address:**

- **Detection (machine-readable ownership).** `sync-manifest.json` currently lists files in flat arrays without tagging ownership category. Proposed schema extension: each file (or file pattern) carries a `category` field — `template_owned` (sync overwrites, never preserves diffs), `project_extensible` (sync respects local additions per FB-059 refinement), or `template_shipped_then_project_owned` (template ships once at setup, then project takes ownership; sync skips entirely). Existing files like `.claude/CLAUDE.md`, `.claude/rules/*.md`, `.claude/skills/*/SKILL.md`, `.claude/commands/*.md` (template-shipped variants) become `template_owned`. Project-extensible: `.claude/dashboard.md` (mostly template-generated but has user notes section). Template-shipped-then-project-owned: `.claude/spec_v1.md` (placeholder shipped, project replaces).
- **Enforcement / warning behavior.** Part 5 uses the category to decide sync behavior:
  - `template_owned` + project-side diff detected → warn user "your local additions to {file} violate the file-ownership convention; the file is being overwritten. Recommended migration: move additions to {root CLAUDE.md / .claude/rules/ / etc.}"
  - `project_extensible` → use FB-059's per-file last-synced-version detection
  - `template_shipped_then_project_owned` → skip sync entirely
- **Discoverability of extension hooks.** Add a "Project extension hooks" section to README or `setup-checklist.md` documenting where projects should add: rule imports (root `./CLAUDE.md`), project-specific rule files (`.claude/rules/` — auto-loaded if imported), project-specific commands (`.claude/commands/audit-{name}.md` per Component 9 of audit family proposal), project-specific skills (`.claude/skills/`), etc. One canonical map. Could live alongside the file-ownership category map.

**Practical impact observed in Styler:** modified `.claude/CLAUDE.md` caused FB-059's false-positive sync friction; no warning when the violation happened; user didn't know the right alternative. Took a multi-message investigation to surface the structural concern.

**Proposed actions:**
1. Extend `sync-manifest.json` schema with `category` per file/pattern. One-time data entry pass.
2. Refine `/health-check` Part 5 to honor categories (combines with FB-059's per-file last-synced-version detection for `project_extensible` files).
3. Add "Project Extension Hooks" section to `setup-checklist.md` and/or root README. Maps each common extension need to its canonical home.
4. Add a one-line preamble check to template-owned files: if user edits detected at sync time, surface the migration recommendation prominently (not buried in the offered-fixes menu).

**Dependencies / interactions:**
- FB-059 (sync detection refinement for `project_extensible`) is a precondition for the Part 5 refinement here.
- Component 9 of audit family proposal (project-to-template graduation) overlaps — both want clear conventions for "what's project, what's template."

**Likely route:** research-light scope. Could be one DEC covering both FB-059 and FB-060 (the ownership system + sync refinement together), since they're tightly coupled. Or two ships: FB-059's per-file last-synced-version mechanism first; FB-060's category schema + Part 5 refinement second.

## FB-061: Promote `feature-retirement.md` from Styler to template (generally-useful workflow rule)

**Status:** new
**Captured:** 2026-05-15
**Source:** discovered as a Styler-local rule file during FB-059/FB-060 investigation.

**Observation:** Styler has a project-local rule file at `.claude/rules/feature-retirement.md` that codifies a generally-useful workflow: how to retire a feature in a frozen, restorable state. The workflow shape:
- Snapshot lives at the retirement commit (no orphaned state)
- Spec keeps a "Retired (YYYY-MM-DD)" marker (discoverability for future readers)
- Directory convention (`.claude/support/retired/{slug}/manifest.json`) enables mechanical restoration

This is not fashion-domain-specific. Any project doing iterative feature work that occasionally retires surfaces (renamed routes, removed components, sunset features) could benefit. The workflow integrates cleanly with the template's existing patterns (spec-as-source-of-truth, decision records, audit family's `retired-features` lens which already greps for `.claude/support/retired/*/manifest.json`).

The audit family's `audit-coherence` lens for `retired-features` already assumes this file structure exists — it scans `.claude/support/retired/*/manifest.json` and flags retired features missing spec markers. Without the workflow rule shipped in the template, downstream projects would hit the lens but have no guidance on the convention. So promoting `feature-retirement.md` makes the audit lens more legible.

**Counterpart not promoted:** Styler's `brand-mention-provenance.md` (when Claude can name brands vs substitute attributes per DEC-060) is fashion/retail-domain-specific. Stays Styler-only.

**Proposed action (small ship):**
1. Copy `styler/.claude/rules/feature-retirement.md` to `claude_code_environment/.claude/rules/feature-retirement.md`. Edit lightly to remove Styler-specific language (e.g., FB-070 references → generic "feedback item") if any.
2. Add the file to `sync-manifest.json` (rules category).
3. Add the import to template's `.claude/CLAUDE.md` (workflow rules section) + summary row.
4. Update template's `audit-coherence.md` lens-retired-features prompt to reference the workflow rule (improves the lens's "what counts as a finding" precision).
5. Bump template_version (minor — new feature: workflow rule shipped).

**Risk:** low. Pure additive — no breaking changes to existing template files. Downstream projects that don't use feature retirement see the rule but don't act on it.

**Dependencies:** none.

**Open question:** does the workflow rule depend on a specific `.claude/support/retired/` directory structure that Styler defined? Need to verify the manifest.json schema is template-shippable or whether it carries Styler-specific fields. If Styler-specific, document the abstract structure in the rule and let projects define their own manifest fields.
