# Plan: FB-059 + FB-060 — file-ownership categories + per-file sync state

**Status:** partially implemented — Phases 1, 3, 4, 5 shipped; Phase 2 (`sync_strict` category schema) deferred per DEC-014
**Date:** 2026-05-16
**Covers:** FB-059 (`/health-check` Part 5 false-positive SKIP) + FB-060 (template/project file-ownership boundary). Items are tightly coupled per FB-060 "Likely route: one DEC covering both."
**Outcome:** Phase 1 (behavioral complement in `.claude/rules/agents.md`) + Phase 5 (`extension-hooks.md` doc) shipped in v3.14.2 (2026-05-16). Phase 3 (`.claude/.sync-state.json` sidecar) + Phase 4 (Part 5 2-condition algorithm refinement) shipped in v3.15.0 (2026-05-16) via DEC-014 **Option F** (sidecar + algorithm, no category change). Phase 2 (`sync_strict` category schema) was **not implemented** — DEC-014 § Decision selected Option F because the sidecar's `local_hash == synced_hash` check is category-agnostic; adding `sync_strict` alongside would ship a label without a function (every current `sync` member is uniformly template-owned, so the category wouldn't gate anything beyond what the hash check already gates). Phase 2 is forward-compatible if a real `project_extensible` member ever emerges — adding the category then is purely additive.
**Decision record:** `decisions/decision-014-sync-state-and-file-ownership-categories.md` (status: implemented after v3.15.0 ship).

## 1. The concrete bug (recap)

Styler 2026-05-15 `/health-check` Part 5 flagged two files as having "local additions" and offered selective sync that would SKIP both:

- **`.claude/skills/dashboard-style/SKILL.md`** — 100% false positive. Pure Stage 6 Option C content shipped in template v3.12.0 but never synced into Styler. Styler's `version.json` correctly read `template_version: 3.12.0` (version synced) but file content stayed at Stage 6a state. Skipping would have permanently masked the missing template content.
- **`.claude/CLAUDE.md`** — correct flag. Styler genuinely added project-specific rule imports.

Root cause: Part 5 compares `local` to `template/{branch}:path` via `git diff`. Any diff is presented uniformly. The UX gives "Apply all / Select individually / Skip" without distinguishing whether the local-vs-template difference is (a) unsynced template content the user should accept, or (b) user-authored local content the user should preserve.

## 2. Current state inventory

### sync-manifest.json (current categories)

- `sync` (flat list of ~45 files/globs) — touchable by Part 5
- `customize` (~3 files) — never touched by sync
- `ignore` (~17 globs) — project data, never touched

No category distinguishes "template_owned strict" from "template_owned but project may add content alongside."

### Part 5 algorithm

1. `git fetch template` → `git remote show template` for default branch
2. Per `sync` file: `git diff` local against `template/{branch}:path`
3. Per-file status: Up to date / Modified upstream / New in template / Local only
4. Present diffs → Apply all / Select / Skip
5. Apply via `git checkout template/{branch} -- path`
6. Update `template_version` in `version.json`
7. Post-sync dashboard re-check

No per-file last-synced state. No category-aware behavior. UX cannot distinguish drift-shape.

### Existing precedent: `.claude/CLAUDE.md` already has per-file hash tracking (Part 2a, lines 218-223)

```
1. If template remote configured: diff against template/{branch}:.claude/CLAUDE.md
2. Else: compare against `claude_md_hash` in version.json
3. If modified: Revert / Keep (records `claude_md_override: true`) / Merge
```

This is a partial precedent for the sidecar-state mechanism this plan generalizes. Currently `claude_md_hash` and `claude_md_override` fields are **not present** in the shipped `version.json`; they're documented but unused. Extending this pattern to all sync-category files is a natural generalization.

### Behavioral complement state

FB-060 § "Behavioral complement (preventive layer)" describes a pre-sync diff against last-synced template state, with routing of findings to project→template promotion (generic) OR project-owned migration (specific). Currently documented only in FB-060's text (commit `27616a9` added the section to `template-maintenance/feedback.md`). Not shipped to any template file. Downstream projects don't inherit this guidance yet.

## 3. Design choices

### Q1: Per-file sync state — hash, version, or both?

**Recommendation:** content hash (sha256, truncated to 16 chars) PER FILE. Cheap (~50 files × hash = sub-second), correct (catches any drift), human-debuggable. Skip version-string per file; the global `template_version` provides chronological reference if needed.

Alternative: hash + last-synced version per file. Adds disk size (~30%) for marginal added value. Not recommended.

### Q2: Where does sync state live?

**Recommendation:** `.claude/.sync-state.json` (new dotfile, gitignored). Schema:

```json
{
  "schema_version": "1.0",
  "last_full_sync_version": "3.14.1",
  "last_full_sync_date": "2026-05-16",
  "files": {
    ".claude/CLAUDE.md": {
      "synced_hash": "a3f2c91e5d8b4762"
    },
    ".claude/rules/agents.md": {
      "synced_hash": "b7d9e842f1c63a5e"
    }
    // ... one entry per sync-category file successfully synced
  }
}
```

Alternative locations considered + rejected:
- Extend `version.json` — pollutes user-facing version semantics; the file is already in `ignore` per sync-manifest, but its primary purpose is provenance + config, not state.
- Extend `dashboard-state.json` — different concerns; co-locating risks coupling unrelated subsystems.

### Q3: Category schema in sync-manifest

**Recommendation:** keep current 3-way split (`sync`/`customize`/`ignore`); add a 4th category `sync_strict` (the formal "template-owned, no local additions tolerated" subset of `sync`). Default behavior of files in `sync` remains as today. `sync_strict` carries the warning-on-deviation behavior. Migration: most current `sync` entries move to `sync_strict`.

Why not the 5-category design from FB-060? Two reasons:
1. **`project_extensible` has no current members.** `.claude/dashboard.md` is in `ignore` (regenerated by `/work`, never synced). No other shipped file has the "template ships + project adds alongside" shape today. Shipping an empty category is premature scaffolding.
2. **`template_shipped_then_project_owned` ≈ existing `customize`.** Already covered. The name change is bikeshed; the behavior exists.

So the proposed minimum delta: split `sync` into `sync_strict` (most files — warn on local deviation) + `sync` (kept name, used for the empty-for-now "respects local additions" case if we need it later). All current sync entries migrate to `sync_strict`. Forward-compatible if `project_extensible`-shaped use cases emerge.

**Alternative:** rename `sync` → `template_owned` per FB-060's preferred terminology. Cosmetic; downstream-breaking (any project referencing the category name in their own tooling breaks). Recommend deferring rename until a more compelling case exists.

### Q4: Part 5 algorithm refinement

The fix has three independent pieces; each is shippable alone.

**(a) Write `.sync-state.json` on successful sync (forward-compatible, no behavior change yet).** Part 5's "Apply Updates" step computes the post-sync hash for each accepted file and writes the sidecar. Future runs can read it. Shipping this alone is a no-op for current users — the file accumulates state silently until step (b) lands.

**(b) Use the sidecar to refine the diff classification.** When a sync-category file shows a diff against template:
- If `local_hash == sidecar.synced_hash` → file was untouched since last sync → diff is **pure template movement** → label as "Template content not yet applied" (NOT "local additions"). Default action: APPLY.
- If `local_hash != sidecar.synced_hash` AND file is in `sync_strict` → user modified a strict-template file → label as "**Local modification of template-owned file** (recommended: revert + move additions to project-owned location)". Default action: REVERT, with explicit Keep override.
- If sidecar entry missing (first sync after this lands, OR a new sync-category file) → fall back to current behavior (treat as "Modified upstream"). Migrate gracefully.

**(c) Add "Show me the diff" sub-action in the Apply/Select menu.** Per-file diff display for the user to adjudicate when sidecar state is ambiguous (missing or pre-this-refinement). Cheap; no schema dependency.

### Q5: Where does the "Project Extension Hooks" doc live?

**Recommendation:** new `.claude/support/reference/extension-hooks.md`. One canonical map. Linked from `setup-checklist.md` and root README.

Content outline:
- Rule imports → root `./CLAUDE.md`
- Project-specific rule files → `.claude/rules/project-*.md` (gitignored per sync-manifest)
- Project-specific commands → `.claude/commands/audit-{name}.md` (per audit family Component 9 graduation pattern) or custom slash commands
- Project-specific skills → `.claude/skills/{name}/SKILL.md`
- Project-specific reference docs → `.claude/support/reference/project-*.md` (gitignored)
- Project-specific decisions → `.claude/support/decisions/decision-*.md`
- Project-specific feedback → `.claude/support/feedback/feedback.md`
- Operational documents → project root `docs/`

Alternative homes considered + rejected:
- Append to setup-checklist.md — buries the canonical map inside an onboarding checklist.
- Append to root README.md — README is user-facing project intro; extension hooks are a developer-side concern.
- `.claude/README.md` — `.claude/README.md` is in `customize` category, so it's user-editable; can't ship updates to it via sync.

### Q6: Behavioral complement — where does it ship?

**Recommendation:** new sub-section in `.claude/rules/agents.md` titled `## Cross-Project Capture Protocol`. Mirrors FB-060's behavioral-complement text. Two reasons agents.md is the right home:
1. It's the rule file that Claude reads when reasoning about template/project boundaries (already imports cleanly).
2. The complement IS agent guidance — it tells Claude what to do BEFORE recommending a sync, which is a behavioral rule.

Alternative: new `.claude/support/reference/cross-project-capture.md`. Cleaner separation but adds another file to navigate. Not recommended — agents.md keeps the guidance close to the related "Behavioral Rules" section.

## 4. Recommended implementation sequence

**Five phases. Each is independently shippable. Stop after any phase if friction reveals scope issues.**

### Phase 1 — Ship the behavioral complement (smallest, lowest risk)

- Add new `## Cross-Project Capture Protocol` section to `.claude/rules/agents.md` (between current `## Behavioral Rules` and `## MCP and Parallel Execution`).
- Content: FB-060's behavioral-complement text, lightly edited for the rule-file voice.
- Bump version.json (patch: 3.14.1 → 3.14.2).
- **Estimated effort:** 20 minutes.
- **Risk:** very low. Pure additive doc.
- **Verification:** read the new section in context; confirm it correctly describes the pre-sync diff + routing logic.

### Phase 2 — sync-manifest schema: add `sync_strict` category

- Extend sync-manifest schema to include `sync_strict` array.
- Migrate current `sync` entries to `sync_strict` (most files; verify per-file via current template-owned convention).
- Bump version.json (minor: 3.14.x → 3.15.0 — schema change in sync-manifest).
- **Estimated effort:** 1 hour (categorization + manifest edit + sync-manifest schema doc update).
- **Risk:** medium. Downstream tooling that hardcodes the category name `sync` may need updating. Mitigation: keep `sync` as a valid category (now used only for the project-extensible case that has no current members) — downstream tooling continues to work.
- **Verification:** `/health-check` Part 5 still processes all files identically (no behavior change yet); test against template-self (`/health-check` against this repo).

### Phase 3 — `.sync-state.json` sidecar mechanism (write-only)

- Part 5 computes per-file sha256 hash on every successful sync and writes `.claude/.sync-state.json`.
- Sidecar in `ignore` category (project data, never synced).
- Schema versioned (`schema_version: "1.0"`) for forward-compat.
- Bump version.json (minor: 3.15.0 → 3.16.0 — new feature).
- **Estimated effort:** 2 hours (logic + schema + migration handling for first-run case).
- **Risk:** low. Write-only; no read paths yet; degrades gracefully if absent.
- **Verification:** run `/health-check` on a project, confirm `.sync-state.json` populated with correct hashes.

### Phase 4 — Part 5 algorithm refinement (the actual fix)

- Part 5 reads `.sync-state.json` and uses it to classify diffs:
  - **Pure template movement** (local_hash == sidecar) → default APPLY
  - **Local mod of sync_strict file** → default REVERT, surface migration recommendation
  - **Sidecar missing / pre-refinement project** → fall back to current behavior
- Add "Show me the diff" sub-action to the per-file menu.
- Update report-format examples in health-check.md.
- Bump version.json (minor: 3.16.0 → 3.17.0).
- **Estimated effort:** 3-4 hours (logic + 3-condition UX + docs).
- **Risk:** medium-high. Behavior change touches a workflow downstream projects use. Mitigation: graceful fallback when sidecar missing; clear messaging in the menu.
- **Verification:** test against template-self + simulated downstream project (fixture with modified CLAUDE.md + missing sidecar).

### Phase 5 — Project Extension Hooks doc

- New `.claude/support/reference/extension-hooks.md` (per Q5 outline above).
- Link from `setup-checklist.md` and root README.
- Add to `sync-manifest.json` under `sync_strict`.
- Bump version.json (patch: 3.17.0 → 3.17.1).
- **Estimated effort:** 1 hour.
- **Risk:** very low. Pure additive doc.
- **Verification:** read the doc in context; confirm each "extension need → canonical home" mapping is correct against current template state.

### Total estimated effort: 7-9 hours across 5 commits.

## 5. Open questions for user input

1. **Scope:** Ship all five phases, or stop after some? (Phases 1 + 5 are the cheap-and-cheerful subset that ships docs without algorithm changes; Phases 2-4 are the structural fix.)
2. **Decision record:** Skip (just ship) or write a DEC in `decisions/` first? FB-060 said "research-light scope" — a DEC may be more rigor than warranted, but it formalizes the schema decision for posterity.
3. **`sync_strict` vs `template_owned` naming:** keep current `sync` as a valid category name and add `sync_strict` (forward-compatible), OR rename `sync` → `template_owned` (cleaner but downstream-breaking)?
4. **Sidecar hash format:** sha256 truncated to 16 chars (proposed, cheap+correct) or full sha256 (more storage, no observable benefit)?
5. **Project-extensible category:** ship as empty placeholder NOW (forward-compat for future use cases) or defer until first concrete member emerges?

## 6. Out of scope

- **`/work` command refinement** to honor the new state (out of scope; sync state is Part 5's concern, not `/work`'s).
- **Retroactive sidecar population** for existing downstream projects. They hit Phase 4's "sidecar missing → fall back to current behavior" path; subsequent sync populates it. No batch migration tooling needed.
- **Multi-template support** (a project syncing from multiple templates). Currently `template_repo` is singular; extending to plural is a separate concern.
- **Sync-state validation** beyond hash check (e.g., did the user manually checkout an older commit?). The hash IS the validation; if hashes match, treat as synced.
- **The `medium` and `higher` actions from FB-062 + FB-063** (rename feedback-archive.md → archive.md; extend background-session preamble carve-out; worktree bind-mount). Separate items; let them age in the maintenance queue.
- **`audit-coherence` retired-features lens field-name alignment** (`slug` vs `feature_slug` etc.). Already deemed non-blocking — lens reads manifests generically.

## 7. Test plan per phase

Each phase verifies independently before moving to the next:

- **Phase 1:** Read agents.md; confirm new section coheres with surrounding rules; test by reading the file fresh and noting whether the protocol is parseable for a future Claude.
- **Phase 2:** Run `/health-check` Part 5 against template-self; confirm behavior unchanged. Confirm no downstream tooling references the bare `sync` category name (`grep -rn '"sync"' .claude/`).
- **Phase 3:** Touch a sync-category file, run /health-check Part 5 dry, confirm sidecar populates with correct hash. Delete sidecar, re-run, confirm regeneration.
- **Phase 4:** Three fixtures (synthesizable as workspace files):
  - **F-α**: project at template_version N-1 with sidecar; template advanced; some sync-category files diff in template only → expect "pure template movement" classification + default APPLY.
  - **F-β**: project at template_version N with sidecar; user modified one sync_strict file locally → expect "local mod of template-owned" classification + migration recommendation surfaced.
  - **F-γ**: project at template_version N WITHOUT sidecar (pre-refinement migration case) → expect fallback to current behavior + sidecar populated on first sync.
- **Phase 5:** Read the new doc; confirm each row matches a real file path; spot-check that the linked `setup-checklist.md` and root README links work both directions.

## 8. Risks and mitigations

- **Risk: Schema change breaks downstream projects mid-sync.** Mitigation: every schema-touching phase bumps version.json minor, and the sync-manifest schema doc explicitly versioned. Downstream projects on older sync-manifest schemas continue working until they sync.
- **Risk: Phase 4 produces false migration recommendations.** Mitigation: warn, never silently revert. User always sees the diff and chooses.
- **Risk: Sidecar gets out of sync with reality (e.g., user manually edits a file).** Mitigation: the hash check IS the freshness check. Next sync recomputes and updates. Sidecar is recoverable from `template_version` + git history; loss is not catastrophic.
- **Risk: Phase 4 UX is harder than estimated.** Mitigation: drop the "Show me the diff" sub-action if needed (it's Phase 4c, separable from 4a + 4b).

## 9. Recommendation summary

**Ship Phases 1 + 5 in this session as a cheap-and-cheerful batch (~1.5 hours, doc-only):**

- Phase 1: behavioral complement in `agents.md` — closes FB-060's "behavioral complement" follow-up.
- Phase 5: extension-hooks doc — closes FB-060's "discoverability gap" sub-concern.

**Queue Phases 2-4 (structural fix) for a separate session.** Reasons:
1. They warrant a DEC in `decisions/` to formalize the schema + sidecar contract.
2. The medium-risk algorithm change in Phase 4 deserves dedicated focus, not session-end fatigue.
3. Phases 2 + 3 are forward-compatible no-ops; landing them later doesn't lose any guarantee.

After Phases 1 + 5 land, FB-059 + FB-060 status becomes: "Phases 1 + 5 shipped (behavioral + discoverability); Phases 2-4 (structural) tracked separately, candidate for DEC-NNN."

Alternative: ship all five phases now in one push. Higher risk + scope-creep potential. Not recommended without a DEC step in between.
