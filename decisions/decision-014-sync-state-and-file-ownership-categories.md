---
id: DEC-014
title: Sync-state mechanism + file-ownership category schema (FB-059 + FB-060 structural fix)
status: proposed
category: architecture
created: 2026-05-16
decided:
related:
  tasks: []
  decisions: [DEC-005, DEC-008, DEC-013]
  feedback: [FB-059, FB-060]
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Sync-state mechanism + file-ownership category schema (FB-059 + FB-060 structural fix)

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Full ship per plan — `sync_strict` category + `.claude/.sync-state.json` sidecar + Part 5 algorithm refinement, no `project_extensible` member, three phases land together as v3.15.0 / v3.16.0 / v3.17.0.
- [ ] Option B: Conservative split — ship only Phase 3 (`.sync-state.json` write-only sidecar) now, defer Phases 2 + 4 to separate decisions. Each future ship has more data to inform the design.
- [ ] Option C: Aggressive consolidation — rename `sync` → `template_owned` per FB-060's preferred terminology; add `project_extensible` and `template_shipped_then_project_owned` as empty categories with documented criteria; all other Phase 2-4 work per plan. Downstream-breaking.
- [ ] Option D: Inverted — behavioral + UX only, no schema change. Add "Show me the diff" sub-action in Part 5 menu (Phase 4c only). Solve FB-059 via better UX, not structural fix. Doesn't address FB-060's category-tagging gap.
- [ ] Option E: Defer indefinitely — document FB-059 + FB-060 structural fix as "known issue" with manual workaround. Revisit only if dedup-or-sync-miss recurs frequently across projects.
- [ ] Option F: Sidecar-first + algorithm-second, no category change — ship Phase 3 (sidecar) AND Phase 4 (algorithm refinement) in one decision but skip Phase 2 (no new `sync_strict` category). The sidecar's `local_hash == synced_hash` check classifies "pure template movement" generically without needing per-file ownership tagging. Defer the category schema until a real `project_extensible` member emerges.

*Check one box above, then fill in the Decision section below.*

---

## Background

### The trigger

Styler 2026-05-15 `/health-check` Part 5 flagged two files as "having local additions" and offered selective sync that would SKIP both:

- **`.claude/skills/dashboard-style/SKILL.md`** — 100% false positive (pure template content unsynced from v3.12.0; skipping would have permanently masked the missing template content).
- **`.claude/CLAUDE.md`** — correct flag (genuinely user-modified with project-specific rule imports).

The current Part 5 algorithm can't distinguish (a) unsynced template content from (b) genuine local additions, because there's no per-file last-synced state. It compares `local` to `template/{branch}:path` via `git diff` and presents any diff uniformly. The UX gives "Apply all / Select individually / Skip" without distinguishing drift-shape.

Captured as **FB-059** (`/health-check` Part 5 detection bug) + **FB-060** (template-owned vs project-owned file-ownership boundary not enforced or discoverable) in `template-maintenance/feedback.md`.

### What's already shipped (Phases 1 + 5)

- **Phase 1 (v3.14.2):** behavioral complement — `.claude/rules/agents.md § "Cross-Project Capture Protocol"` codifies the pre-sync boundary check. Reduces frequency of the violation.
- **Phase 5 (v3.14.2):** discoverability — `.claude/support/reference/extension-hooks.md` maps each extension need to its canonical project-owned location.

What's deferred to this decision: **Phases 2-4** — the structural fix.

### What Phases 2-4 cover

- **Phase 2: sync-manifest category extension.** Currently `sync` / `customize` / `ignore`. The proposal adds a way to distinguish "strict template-owned" (warn on local edits) from the rest. FB-060 proposed `template_owned` / `project_extensible` / `template_shipped_then_project_owned` — but `project_extensible` has no current members (`.claude/dashboard.md` is in `ignore`, not `sync`), and `template_shipped_then_project_owned` ≈ existing `customize`. The plan recommends the minimum delta: split `sync` into `sync_strict` (strict, warn-on-deviation) + `sync` (kept name, currently empty), forward-compatible.
- **Phase 3: per-file sync state.** A `.claude/.sync-state.json` sidecar (gitignored) recording per-file SHA-256 hash at last successful sync. Existing precedent: Part 2a already has `claude_md_hash` and `claude_md_override` fields documented for `.claude/CLAUDE.md` specifically (but unused in current `version.json` schema). This phase generalizes the pattern.
- **Phase 4: Part 5 algorithm refinement.** Use category + sidecar to classify diffs:
  - `local_hash == sidecar.synced_hash` → pure template movement → default APPLY.
  - `local_hash != sidecar.synced_hash` AND file in `sync_strict` → local modification of template-owned file → default REVERT with explicit Keep override; surface migration recommendation.
  - Sidecar entry missing → fall back to current behavior + populate sidecar on next sync (graceful migration).
- Plus optionally: "Show me the diff" sub-action per file in the menu (Phase 4c, separable).

### Why a decision record now (not just ship)

- **Schema change** to `sync-manifest.json` affects every downstream project on next sync.
- **Algorithm change** to Part 5 alters a workflow downstream projects use.
- **Migration story** for projects without `.sync-state.json` needs explicit design.
- **Forward-compat** for `project_extensible` shape — should we ship the category now or wait for a member?
- Per root CLAUDE.md File Boundary: "**Decision records:** `decisions/` (root) — for formal decisions about template changes via `/research`". This decision warrants the formal process.

Plan: `template-maintenance/plan-fb059-fb060.md` (canonical reference for the full design space + recommended sequence).

## Options Comparison

| Criteria (weight) | A: Full ship | B: Conservative split | C: Aggressive | D: Inverted (UX only) | E: Defer | F: Sidecar+algo, no category |
|----------|---|---|---|---|---|---|
| Closes FB-059 (sync-detection false-positive) (3) | Yes | Partially (no UX fix yet) | Yes | Yes (via better UX) | No | Yes |
| Closes FB-060 (file-ownership boundary structurally) (2) | Yes | No | Yes | No | No | No (behavioral only) |
| Downstream-breaking (3) | No (forward-compat) | No | Yes (rename) | No | No | No |
| Effort (-1, penalty) | High (7-9h) | Low (2-3h) | Higher (7-9h + migration tooling) | Very low (1-2h) | Zero | Medium (4-6h) |
| Risk to existing projects (-2, penalty) | Low (graceful migration) | Very low | Medium (rename breakage) | Very low | None | Low |
| Provides per-file state for future use (2) | Yes | Yes | Yes | No | No | Yes |
| Locks in shape that may not generalize (-1, penalty) | Some (sync_strict naming) | Less (only sidecar lands) | Most (full FB-060 schema) | None | None | Least (no category change) |
| Migration cost for downstream projects (-1, penalty) | Low (graceful fallback) | None | Higher (rename + 2 empty cats) | None | None | Low (graceful fallback) |
| User-visible friction reduction now (3) | High | Low | High | Medium | None | High |
| Overall | Single-coherent ship; bundles category schema (which has only one member today) with the actually-load-bearing sidecar+algo. Highest immediate value; lowest forward-compat lock-in than C. Best fit if user wants FB-059+FB-060 closed in one decision. | Half-measure: ships durable state but defers the user-visible fix. Buys data but adds two future decisions and leaves the original symptom unfixed. Recommended only if the algorithm design feels under-specified. | Most ambitious; cleanest end-state vocabulary; only viable if user accepts rename cost. The two empty categories (`project_extensible`, `template_shipped_then_project_owned`) are premature scaffolding with no confirmed member, so most of C's "upside" is naming aesthetics. | Cheapest, addresses only one of the two FBs and pushes interpretation cost back to the user every sync. Good as a v0 if you suspect Phases 2-4 are over-engineered. The Styler false-positive case is still confusing even with the diff visible. | Concedes the gap. Workaround documented elsewhere; user repeats the same manual diff routine each occurrence. Phases 1+5 stand isolated without the structural complement, leaving the improvement story incoherent. | **Strictly cheaper than A with ~all of A's user-visible value.** The sidecar's `local_hash == synced_hash` check classifies "pure template movement" without needing per-file ownership tags — every file in `sync` is template-owned today (FB-060 confirms this). Defers Phase 2's category schema until a real `project_extensible` member emerges. Tradeoff: loses FB-060's "warn on local mod of template-owned file" because all files are uniformly treated; the warning is replaced by a single classification ("template content not yet applied" vs "diff with both local and template changes"). |

## Option Details

### Option A — Full ship per plan

**Description:** Ship Phases 2-4 as designed in `template-maintenance/plan-fb059-fb060.md`. Land as three sequenced commits (3.14.2 → 3.15.0 → 3.16.0 → 3.17.0).

**What ships:**
- Phase 2: `sync_strict` category added to `sync-manifest.json`; current `sync` entries migrate to `sync_strict`; the `sync` name remains valid for future "respects local additions" use cases.
- Phase 3: `.claude/.sync-state.json` sidecar (gitignored). Part 5 computes SHA-256 (truncated to 16 chars) per file on every successful sync, writes the sidecar. Schema-versioned (`schema_version: "1.0"`).
- Phase 4: Part 5 reads sidecar + category, classifies diffs into three cases (pure template movement / local mod of strict file / fallback). Migration warning surfaces for sync_strict files with local deviations. "Show me the diff" sub-action added.

**Strengths:**
- Closes FB-059 + FB-060 in a single coherent unit.
- Forward-compatible: existing projects without sidecar fall back to current behavior gracefully; sidecar populates on first sync after this lands.
- No rename — downstream tooling that references `sync` continues to work.
- Each phase has a fallback if scope creeps mid-flight.

**Weaknesses:**
- Largest effort (7-9 hours focused work).
- Algorithm change in Phase 4 is medium-risk; touches a workflow downstream projects use.
- Bundles three semi-independent shipments; partial completion is awkward (which phases land where in commit history?).

**Research Notes:**

- **Adjacency to existing precedent (Part 2a).** Part 2a (`health-check.md:218-223`) already implements per-file hash checking — but only for `.claude/CLAUDE.md`, and only as a fallback when the template remote isn't configured. The implementation references `claude_md_hash` and `claude_md_override` fields in `version.json`. Neither field is actually present in the current `version.json` schema (`.claude/version.json` ships with only `template_version`, `template_release_date`, `template_repo`, `project_version`, `project_initialized`, `template_inbox_path`, `structured_artifact_path`, `notes`). Option A's sidecar is the natural generalization of this dormant precedent — and it correctly moves the state out of `version.json` (which mixes provenance + config + state today; pulling state out keeps version.json focused on provenance).
- **Existing template hash convention.** `.claude/scripts/fingerprint.py` (shipped in v3.0.0, FB-039 bug-fixed in v3.1.1) uses **full SHA-256 hex** prefixed `sha256:` (e.g., `sha256:a3f8c91d2e7b4056...64-chars-total`). The plan's "truncated to 16 chars" recommendation **breaks this convention**. Switching to full SHA-256 hex aligns with `spec_fingerprint`, `section_fingerprint`, `task_hash`, dashboard META — all existing template hash sites. Storage cost: 64 hex chars × ~50 files ≈ 3.2 KB raw; with field names + JSON syntax + sidecar wrapper, total file size is ~5-7 KB. Truncation saves ~2 KB — not material. **Recommend: switch the plan from 16-char truncation to full SHA-256 hex with `sha256:` prefix** for convention consistency.
- **Schema versioning precedent.** `sync-manifest.json` already has `"manifest_version": "1.0.0"` at the top level. Option A's `schema_version: "1.0"` for the sidecar matches this pattern. No additional schema-versioning machinery needed.
- **Schema-change risk audit.** Grep across `.claude/` for the bare string `"sync"` (the category name) returns exactly one tracked reference: `sync-manifest.json` itself (the definition site). Grep for `sync-manifest` references returns 6 hits: `health-check.md` (4 — references the file by name), `workflow.md` (2 — documentation), `agents.md` (1 — Cross-Project Capture Protocol), `extension-hooks.md` (5 — references the category names `sync` / `ignore`). All references are template-internal docs; **no downstream tooling references the category name directly**. The "downstream-breaking" weakness in Option A doesn't apply because Option A keeps `sync` as a valid name; the concern is real for Option C (rename) but moot for A.
- **Three-phase commit history.** Phase 2 schema-only / Phase 3 write-only / Phase 4 algorithm — each phase ships independently with version bumps. Forward-compatibility: projects on N-1 with Phase 2 schema sync, can roll Phase 3 alone (no behavior change), then Phase 4 (active read path). The phases are reorderable but not interleavable (Phase 4 requires Phase 3's sidecar).
- **Implementation cost reality check.** The 7-9 hour estimate is dominated by Phase 4's UX (3-4h). Phase 2 is essentially a config-file edit (1h including a sync-manifest schema doc pass). Phase 3 is 2h including the schema-versioned sidecar + first-run migration. The risk-bearing change is concentrated in Phase 4 — both Phases 2 and 3 are no-ops behaviorally. Option A's actual delivery risk is Phase 4 alone.

### Option B — Conservative split

**Description:** Ship only Phase 3 (sidecar write-only) now. Defer Phase 2 (category schema) and Phase 4 (algorithm changes) to separate decisions, each informed by the data the sidecar accumulates.

**What ships:**
- `.claude/.sync-state.json` written on every successful sync (no read paths yet).
- All other behavior unchanged.

**Strengths:**
- Lowest immediate risk; no schema or algorithm change.
- The sidecar becomes a data source for future decisions (which files actually drift in practice).
- Splits commitment — Phase 2 and Phase 4 are reconsidered with fresh data.

**Weaknesses:**
- Doesn't close FB-059 (the false-positive symptom persists).
- Doesn't close FB-060 (no category-tagging).
- Three future decisions instead of one (overhead).
- Phase 4's UX improvements (the actual user-visible fix) are deferred.

**Research Notes:**

- **What "data the sidecar accumulates" actually gives us.** A write-only sidecar populated across N sync cycles records: for each file, its hash at last sync. This data alone cannot distinguish "modified by user since last sync" from "drifted by template since last sync" — both produce `local_hash != current_template_hash`. The disambiguation requires comparing `local_hash` against `sidecar.synced_hash` (which Option B ships) AND running this comparison at Part 5 time (which Option B defers). So Option B accumulates the data substrate for Phase 4 but provides no observation channel until Phase 4 lands. The "decisions informed by fresh data" framing is weak — the data Option B accumulates is useful only to validate Phase 4 once it ships, not to inform whether to ship Phase 4.
- **What does Option B actually defend against?** The case for B is procedural caution: if the user is uncertain about the sidecar schema being right (e.g., wants to see real-world projects' file enumerations before committing), shipping Phase 3 alone is a hedge. But the schema (`schema_version: "1.0"` + `files: { "path": { "synced_hash": "sha256:..." } }`) is the minimum-viable shape; adding fields later is backward-compatible. The schema risk is low. So the procedural caution doesn't have much grip.
- **FB-059's symptom persists.** A user who hits the false-positive after Option B ships still has only the manual `diff <template-path> <project-path>` workaround. The original trigger isn't closed. FB-060's behavioral piece (already shipped in v3.14.2 via Phase 1) reduces frequency but doesn't fix the symptom when it does occur.
- **Multi-decision overhead.** Three decisions (DEC-014 = Phase 3; DEC-015 = category schema; DEC-016 = algorithm) means three decision-record exercises. If we're confident the algorithm design (3-condition classification + graceful fallback) is right, splitting buys procedural caution at the cost of friction.

### Option C — Aggressive consolidation

**Description:** Adopt FB-060's full proposed terminology in one go. Rename `sync` → `template_owned`. Add `project_extensible` (empty for now) and `template_shipped_then_project_owned` (equivalent to current `customize` — keep `customize` as alias or migrate?). All other Phase 2-4 work as Option A.

**Strengths:**
- Cleanest long-term terminology — matches FB-060's preferred names.
- Forward-compatible for `project_extensible` use cases that haven't materialized yet.
- Single migration step; no future rename needed.

**Weaknesses:**
- Downstream-breaking: any tooling referencing the `sync` category name needs updating.
- Adds two categories (`project_extensible`, `template_shipped_then_project_owned`) with zero current members — premature scaffolding.
- Larger surface for migration; more places where downstream projects could hit unexpected behavior.

**Research Notes:**

- **"Downstream-breaking" assessment is qualified.** Grep across all tracked `.claude/` files reveals exactly one bare `"sync"` reference (the manifest definition). 6 references to `sync-manifest` as a file-name (docs only). The only category-name dependencies are in `extension-hooks.md` (which says e.g. "Custom names not in sync-manifest `sync` are untouched by sync") and `health-check.md` (algorithm references). Both are template-internal — they migrate alongside the rename. There is **no detected external downstream tooling** that references the category name. So "downstream-breaking" really means "every project running an outdated `.claude/sync-manifest.json` sees confusing diffs at sync time until Phase 4 sync completes." The blast radius is contained but the user impact during the transition window is real.
- **Empty-category cost.** Adding `project_extensible: []` and `template_shipped_then_project_owned: []` to the manifest is cheap in bytes but expensive in cognitive load. Future contributors reading the manifest see two categories with no examples, no documented criteria for membership beyond names. The proposal's `template_shipped_then_project_owned` is genuinely ambiguous: `.claude/spec_v1.md` (currently in `ignore`) is the closest match, but it's not synced ever, so it doesn't belong in any sync-category at all. The category-by-intent doesn't necessarily fit the algorithm-by-behavior, which is a smell.
- **`customize` overlap.** `customize` currently holds `.claude/README.md`, `README.md`, `.claude/support/documents/README.md`. These match `template_shipped_then_project_owned` semantically. If we adopt the new category name, we either rename `customize` → `template_shipped_then_project_owned` (longer name, dubious clarity gain) or keep both (two names for the same semantics, which is worse). Either way, the rename is not strictly additive.
- **Reversibility cost.** Once shipped, deprecating `project_extensible` (because no member ever materialized) becomes a second migration. Option A's "split into `sync_strict` + keep `sync` as currently-empty forward-compat" has the same forward-compat property without adding two named-but-empty categories.

### Option D — Inverted (UX-only fix)

**Description:** Skip the structural fix. Add only the "Show me the diff" sub-action in the Part 5 menu (Phase 4c, separable). Solve FB-059 by giving users the data to adjudicate, not by automating the classification.

**What ships:**
- Per-file diff display in the Apply/Select menu.
- Updated UX prompts encouraging users to inspect before skipping.

**Strengths:**
- Very low effort (1-2 hours).
- Zero schema or algorithm change.
- Lowest risk.

**Weaknesses:**
- Doesn't close FB-060 (no category-tagging, no enforcement).
- Pushes interpretation burden to the user every time.
- Doesn't accumulate state for future decisions.
- The Styler false-positive case (SKILL.md with pure template content) is still confusing even with the diff visible — distinguishing "all of template's new lines are missing from local" from "local has additions not in template" requires careful reading.

**Research Notes:**

- **Styler observation evidence.** The Styler false-positive case was already user-visible in some sense — Part 5 reported a diff. The user (Erik) caught it via manual inspection. So the UX-only fix is essentially "make the manual inspection one step shorter by inlining the diff." That's real but small.
- **Diff-display readability.** A standard git diff of a several-hundred-line SKILL.md is ~20-50 lines of context-with-changes. Pure-template-movement diffs (where the entire diff is `+` lines from template) are visually unmistakable at first glance. Pure-local-additions diffs are similarly unmistakable. The hard case is mixed (local additions in one section, template movement in another) — exactly the case Phase 4's algorithm could classify correctly but Option D leaves to the user.
- **Interaction cost over time.** Every sync cycle, the user re-pays the inspection cost. Phase 4's algorithm pays the cost once (at implementation) and amortizes across every future sync.
- **Compatibility with Option F.** Option D's "Show me the diff" sub-action is a strict subset of Option F's Phase 4 work. If Option D ships first, Option F's later ship is purely additive (no rework). This is a natural escalation path: ship D as a v0 (~1h), then F as v1 if friction recurs.

### Option E — Defer indefinitely

**Description:** Document FB-059 + FB-060 structural fix as "known issue" with the manual workaround already in FB-059's body (`diff <template-path> <project-path>` per file). Revisit only if observed friction recurs.

**Strengths:**
- Zero work.
- Avoids over-engineering a problem that's only been observed once.

**Weaknesses:**
- Doesn't close FB-059 or FB-060.
- Future cross-project capture sessions hit the same trap.
- Manual workaround is genuinely error-prone (user has to interpret diffs correctly per file).
- Phases 1 + 5 are partial; without Phases 2-4, the structural improvement story is incoherent.

**Research Notes:**

- **"Observed once" framing.** The Styler 2026-05-15 observation is one *occurrence* but the underlying *condition* (any unsynced template change + any local edit on a sync-category file) is permanent and recurs every template sync where any sync-category file has any project-side modification. The Phase 1 behavioral complement reduces frequency of the *upstream condition* (the local mods) but doesn't address what happens when those local mods exist and the user runs Part 5.
- **Coherence cost.** Shipping Phase 1 (behavioral guidance) + Phase 5 (extension-hooks doc) without Phases 2-4 leaves a doc-only story: "here are the rules; here are the places to put project content; but the sync engine still can't tell template-content drift from project additions." A future contributor reading the docs will reasonably ask "why isn't this enforced?" The current state is partial.
- **Real cost of the workaround.** The manual workaround (FB-059 body) is `diff <template-path> <project-path>` per file. For ~50 sync-category files, this is ~50 manual diff invocations + visual inspection per sync. In practice the user only does this for the flagged subset (usually 2-5 files per sync). Cost is small per sync but compounds across N sync cycles + M projects.

### Option F — Sidecar-first + algorithm-second, no category change

**Description:** Ship Phase 3 (sidecar) AND Phase 4 (algorithm refinement) together but skip Phase 2 (no `sync_strict` category). The sidecar's `local_hash == synced_hash` check classifies "pure template movement" generically without needing per-file ownership tagging. Defer the category schema until a real `project_extensible` member emerges.

**What ships:**
- `.claude/.sync-state.json` sidecar with full SHA-256 hashes (gitignored, schema-versioned).
- Part 5 algorithm refinement: classify diffs by sidecar match (3 cases — pure template movement, local mod, sidecar missing fallback).
- "Show me the diff" sub-action (Phase 4c).
- **NO** new `sync_strict` category. All files in `sync` get uniform "warn on local mod" treatment because all current `sync` members are template-owned per the FB-060 audit. If/when `project_extensible` members emerge, add the category then.

**Strengths:**
- Closes FB-059 (the actual user-visible symptom) without bundling forward-compat scaffolding.
- Closes FB-060's *behavioral* gap (Phase 1 already shipped) and *discoverability* gap (Phase 5 already shipped) — the only remaining FB-060 ask is category tagging, which the sidecar makes operationally redundant.
- No schema change to sync-manifest (zero downstream-breaking risk, no version bump for manifest itself).
- Forward-compatible: adding `sync_strict` or `project_extensible` later is purely additive.
- ~30% less effort than Option A (skip Phase 2's manifest schema work; skip the per-category branching in Phase 4 logic).

**Weaknesses:**
- Loses Phase 2's explicit warning text differentiation (Option A surfaces "Local modification of template-owned file (recommended: revert + move additions)" — Option F just surfaces "Local modification + template also changed; pick a path").
- The user has to remember which files are template-owned (the extension-hooks doc covers this, but it's a soft pointer, not enforcement).
- Less satisfying close on FB-060 — its category-schema ask remains technically open even though the operational concern is addressed.

**Research Notes:**

- **Why this works without categories.** The sidecar mechanism's load-bearing test is `local_hash == sidecar.synced_hash`. This test is category-agnostic — it tells you whether the local file has been touched since last sync, regardless of whether the file is "template-owned strict" or "project-extensible." For the pure template movement case (the Styler SKILL.md scenario), the sidecar match identifies the situation correctly without needing a category. For the local-mod-of-template-file case (the Styler CLAUDE.md scenario), the sidecar mismatch identifies the situation correctly; the recommendation ("move additions to project-owned location") can come from the extension-hooks doc lookup, not from a per-file category flag.
- **Where Option F is materially weaker than A.** If a real `project_extensible` member emerges (e.g., a future `.claude/skills/dashboard-style/SKILL.md` that ships base content from template + accepts project-side appendix sections), Option F treats it identically to other sync files — local mod triggers the same warning. Option A could mark it `project_extensible` and offer "merge" semantics. But: zero such members exist today, and the merge semantics are unspecified even in the plan. The category doesn't carry behavior; it just carries a label. Until the behavior is specified, the label is metadata-only.
- **Migration story.** Projects on older sync-manifest schemas see no schema change at all (the manifest is untouched). The sidecar is opt-in by virtue of being absent — projects without one fall back to current behavior. First sync after Option F ships populates the sidecar; subsequent syncs use the refined algorithm.
- **Future-compat for FB-060.** A future DEC-XXX can introduce `sync_strict` or `project_extensible` purely additively, with the sidecar mechanism already in place. The sidecar accumulates the operational primitive; the category schema can be added later if the value-add is demonstrated.

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision. This section is yours — Claude reads it but never overwrites it.*

**Constraints:**
- _placeholder_

**Questions:**
1. **Hash format convention:** the existing template uses **full SHA-256 hex with `sha256:` prefix** (`fingerprint.py`, `task_hash`, `spec_fingerprint`, `section_fingerprint`, dashboard META). The plan's "truncated to 16 chars" recommendation breaks this convention for a ~2KB storage saving. Adopt full-SHA-256 + `sha256:` prefix for consistency, or keep truncation for compactness?
2. **Sidecar location vs version.json:** the existing `claude_md_hash` / `claude_md_override` precedent (documented but unused) lives in `version.json`. Should the new sidecar be a separate `.claude/.sync-state.json` (cleaner — version.json stays focused on provenance), or should we generalize the existing pattern by adding a `synced_files: { ... }` object to `version.json` (less new infrastructure, but version.json becomes a mixed provenance+state file)?
3. **Migration story for projects mid-stream:** a project on template_version 3.14.x runs `/health-check` after this DEC ships. It has no sidecar. Phase 4's algorithm should fall back to current behavior + populate sidecar on first sync. Should the first-sync population happen silently (sidecar appears, no user action needed), or should it surface a one-line note ("Sync state now tracked per file — your future syncs will distinguish template drift from local additions")? The latter is more discoverable; the former is less noisy.
4. **`.claude/.sync-state.json` git visibility:** should the sidecar be gitignored? Pro-gitignore: it's project state, not template content; mirrors `version.json` being in `ignore` category. Pro-track: a tracked sidecar lets `git log` show sync history; useful for forensics when a sync goes wrong. The plan defaults to gitignored — confirm or revisit.
5. **Forward-compat for `project_extensible`:** zero current members. Is there a forward-looking concrete use case (e.g., `.claude/dashboard.md` shifting from `ignore` to `project_extensible` where template ships base + project adds notes via markers)? If yes, shipping the category empty as scaffolding has value. If no, defer (Option F).
6. **DEC granularity:** Option B argues for splitting into multiple decisions (sidecar, then category, then algorithm). Is the algorithm design (3-condition classification + graceful fallback) settled enough to bundle, or does the user want to see the sidecar accumulate real-world data first? (Option A vs B vs F is largely a function of this question.)
7. **Phase 4 UX detail — Apply default for `sync_strict` local mods:** the plan proposes "default REVERT with explicit Keep override; surface migration recommendation." This means users who legitimately need to keep their local mods (until they've migrated) face a default that loses their additions if they accept-all. Should the default be REVERT (encourages migration, risks data loss on accidental accept-all) or KEEP (preserves user data, weaker migration nudge)? This bears on Phase 4's design even within Option A.


## Decision

**Selected:** _to be filled when option selected_

**Rationale:**
_to be filled_

## Trade-offs

**Gaining:**
- _to be filled_

**Giving Up:**
- _to be filled_

## Impact

**Implementation Notes:**
_to be filled_

**Affected Areas:**
- _to be filled_

**Risks:**
- _to be filled_

---

## Recommendation

**Lean: Option F (sidecar + algorithm, no category change).** Secondary lean if the user wants to fully close FB-060's category ask: Option A.

**Why F over A:**

1. **The category schema is metadata-only today.** Phase 2's `sync_strict` category has no behavior distinct from the rest of `sync` because every current `sync` member is template-owned. The category doesn't gate anything; the sidecar's hash-comparison is what actually drives Phase 4's classification. Shipping the category alongside provides a label without a function.
2. **The `project_extensible` shape is unproven.** Zero current members. The plan's own "Why not the 5-category design" rationale (FB-060 § Q3) acknowledges this is premature scaffolding. Option F defers the decision until evidence emerges.
3. **Forward-compat is preserved.** Adding `sync_strict` later is purely additive. No migration cost. No downstream breakage. Option F sets up Option A as a clean follow-on if a member ever materializes.
4. **Closes the actual user-visible bug.** FB-059's symptom (Styler false-positive SKILL.md) is closed by the sidecar+algorithm pair alone. The category isn't load-bearing for the fix.

**Why A is the right pick if the user wants to close FB-060's category ask in this decision:**

- A signals stronger intent on the file-ownership boundary (the warning text differentiates "template-owned, recommend migration" from generic diff).
- A bundles all three phases into one decision record — single ship history rather than two (DEC-014 = F now; DEC-015 = sync_strict category later).
- A's "premature scaffolding" cost is small (one category name; no behavioral surface).

**Why not C:** the rename + two empty categories costs more than it gives. Without a real `project_extensible` member, the category is a label looking for a use case. C's "cleanest long-term terminology" argument is real but optional — the template can rename later when there's evidence the new terms carry weight.

**Why not B:** half-measure. Ships the data substrate but defers the user-visible fix. Three future decisions for the same surface. The plan's algorithm design (3-condition classification with graceful fallback) is well-specified; deferring it past a "wait and see" cycle adds friction without buying useful information.

**Why not D:** doesn't accumulate state. Each sync re-pays the user-inspection cost. Acceptable as a v0 stop-gap (~1h ship) if user wants the immediate friction down before tackling F, but as a final answer it strands the architecture in a half-built state.

**Why not E:** Phases 1+5 are already shipped without Phases 2-4; the structural story is incoherent. The condition recurs every sync where any sync-category file has local mods.

**Counter-argument worth weighing:** if the user values "single coherent decision that closes both FBs structurally," A is the right pick despite the category being metadata-only today. The cost of adding `sync_strict` as a forward-compat slot is small; the cost of opening a future DEC-015 to ship the category later is also small. The two are close. The dimension the user should focus on:

> **Is the file-ownership category schema valuable as a label even without distinct behavior?** If yes (A is right). If no, defer until behavior emerges (F is right).

A secondary dimension if user opts for staged work:

> **Ship Option D (1h UX-only) first, then Option F or A later?** D is a strict subset of F; no rework. Useful if user wants immediate friction reduction before committing to the structural design.

**Minor adjustments to apply regardless of option chosen:**
- Switch hash format from "truncated to 16 chars" to **full SHA-256 with `sha256:` prefix** to align with `fingerprint.py` / `spec_fingerprint` / `task_hash` / dashboard META precedent. Storage cost is ~2KB; convention consistency is worth more.
- Add `.claude/.sync-state.json` to `.claude/sync-manifest.json` `ignore` array (alongside `.claude/version.json`, `.claude/dashboard.md`) so the sync engine never touches it.
