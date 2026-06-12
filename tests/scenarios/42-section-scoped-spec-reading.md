# Scenario 42 — Section-scoped spec reading (DEC-021)

Conceptual trace test for the Option 2 spec-scale implementation: the generated section index, the scoped-read discipline, index freshness, and the additive `--depth 3` companion. Verifies the convention preserves the single-spec invariant and never affects drift correctness.

## Setup / State

- A project with `.claude/spec_v3.md` (~850K chars, ~50 `## Phase N` sections — styler-scale).
- Tasks decomposed against it (carrying `spec_section`, `spec_fingerprint`, `section_fingerprint`).
- `.claude/spec_v3.index.json` present or absent (both cases traced).

## Trace A — `/work` Step 1b refreshes a stale/missing index

Command path: `commands/work.md § "Step 1b: Spec Drift Detection"` → `support/reference/drift-reconciliation.md § "Spec Index Freshness"`.

1. Orchestrator computes the full-spec fingerprint (already required for drift detection).
2. It checks `.claude/spec_v3.index.json`:
   - **Missing** → regenerate: `python3 .claude/scripts/fingerprint.py --index .claude/spec_v3.md > .claude/spec_v3.index.json`.
   - **Present, `spec_fingerprint` == current** → leave as-is.
   - **Present, `spec_fingerprint` != current** → regenerate.

**Expected:** after Step 1b the index exists and its top-level `spec_fingerprint` equals the current full-spec hash. The index is NOT fingerprinted into any task and does NOT appear in drift reconciliation — a stale index never resets a Finished task.

**Pass criteria:** orchestrator regenerates only on missing/mismatch; never writes the index from a subagent; drift-reconciliation behavior is identical to pre-DEC-021.

## Trace B — implement-agent reads one section, not the monolith

Command path: `agents/implement-agent.md § "Before starting"` → `rules/spec-workflow.md § "Section-scoped spec reading"`.

State: task `spec_section: "## Phase 40 — /outfits streamline"`; index present.

1. Agent reads `.claude/spec_v3.index.json`, finds the entry whose `heading` == the task's `spec_section`.
2. Agent `Read`s `.claude/spec_v3.md` with `offset = line_start`, `limit = line_end − line_start + 1`.

**Expected:** the agent loads only Phase 40's ~58K-char range, not the whole 850K file. If the index is absent, it falls back to `Grep` for the heading then a scoped `Read`. Whole-file reads are reserved for first decomposition / full audits ("whole when warranted").

**Pass criteria:** no full-spec `Read` for a single-section task; correct offset/limit derived from the index; graceful `Grep` fallback when the index is absent.

## Trace C — companion `--depth 3` is additive (no drift churn)

Command path: `scripts/fingerprint.py` / `drift-reconciliation.md`.

1. `fingerprint.py --sections spec.md` → `## `-only map (unchanged from pre-DEC-021).
2. `fingerprint.py --sections spec.md --depth 3` → the SAME `## ` keys + values, PLUS `### ` subsection hashes.

**Expected:** existing `## ` `section_fingerprint` values are byte-identical regardless of `--depth`, so opting into finer `### ` granularity never triggers false drift on existing tasks.

**Pass criteria:** `--depth 2` output ⊆ `--depth 3` output; `## ` values identical across depths. (Mechanically covered by `test_sections_depth3_is_additive`.)

## Trace D — subsection narrowing spares unaffected tasks (DEC-021 companion, v4.25.0)

Command path: `drift-reconciliation.md § "Subsection-level drift narrowing"` → `commands/work.md § "Step 1b"`.

State: `## Phase 40` (58K, subsections `### A`–`### H`) has 47 tasks. A one-line edit lands in `### X` only. Some tasks carry `spec_subsection` (DEC-021 optional provenance), some are legacy (none).

1. Granular analysis flags `## Phase 40` (its `## ` hash changed).
2. Because the section is large, drift computes the `### ` diff (`fingerprint.py --sections --depth 3`, current vs snapshot) → only `### X` changed.
3. UI surfaces: *"Phase 40 changed — specifically `### X` (`### A`–`### H` minus X unchanged)."*
4. Task grouping:
   - Tasks with `spec_subsection == "### X"` (or a differing `subsection_fingerprint`) → flagged for reconciliation.
   - Tasks with `spec_subsection` in an unchanged subsection → "likely unaffected (subsection unchanged)" group, `[S] Skip` recommended (surfaced, not dropped).
   - Tasks with no `spec_subsection` (legacy) → flagged at `## `-level exactly as today.

**Expected:** tasks whose subsection is provably unchanged are spared mandatory reconciliation; legacy tasks behave exactly as before; nothing is silently dropped.

**Pass criteria:** narrowing only spares tasks with provenance + unchanged subsection; conservative "surface, don't drop"; full fallback to `## `-level when there's no provenance / no snapshot / `--depth 3` unavailable / the section is small. (Additive `### ` hashing is mechanically covered by `test_sections_depth3_is_additive`.)

## Invariant checks

- Exactly one `spec_v{N}.md` still exists — Option 2 changed no file-structure invariant (the higher-bar edit Options 1/3 would have required).
- `settings.json` DEC-016 `permissions.ask` globs unchanged (`.claude/spec_v*.md` still matches; the generated `.index.json` is not hand-edited spec text, so it needs no gate).
- The index is regenerable; deleting it degrades to whole-file reads with zero correctness impact (the reversibility that drove the Option 2 choice).
