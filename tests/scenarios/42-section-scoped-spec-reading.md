# Scenario 42 — Section-scoped spec reading

Conceptual trace test for the Option 2 spec-scale implementation: the generated section index, the scoped-read discipline, index freshness, and the additive `--depth 3` companion. Verifies the convention preserves the single-spec invariant and never affects drift correctness.

## Setup / State

- A project with `.claude/spec_v3.md` (~850K chars, ~50 `## Phase N` sections — styler-scale).
- Tasks decomposed against it (carrying `spec_section`, `spec_fingerprint`, `section_fingerprint`).
- `.claude/spec_v3.index.json` present or absent (both cases traced).

## Trace A — `/work` Step 1b refreshes a stale/missing index

Command path: `commands/work.md § "Step 1b: Spec Drift Detection"` → `support/reference/drift-reconciliation.md § "Spec Index Freshness"`.

1. Orchestrator has the full-spec fingerprint from Step 1b's drift check (`spec_fingerprint` in the `fingerprint.py --drift .claude` output).
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

**Expected:** the agent loads only Phase 40's ~58K-char range, not the whole 850K file. If the index is absent, it searches for the heading (the `Grep` tool, or `rg` via Bash when the harness has none, per the agent's Tool Preferences), then does a scoped `Read`. The search names `.claude/spec_v3.md` directly, so `rg` skipping the hidden `.claude/` directory doesn't apply. Whole-file reads are reserved for first decomposition / full audits ("whole when warranted").

**Pass criteria:** no full-spec `Read` for a single-section task; correct offset/limit derived from the index; graceful heading-search fallback when the index is absent, with or without a `Grep` tool.

## Trace C — companion `--depth 3` is additive (no drift churn)

Command path: `scripts/fingerprint.py` / `drift-reconciliation.md`.

1. `fingerprint.py --sections spec.md` → `## `-only map (unchanged from pre-DEC-021).
2. `fingerprint.py --sections spec.md --depth 3` → the SAME `## ` keys + values, PLUS `### ` subsection hashes.

**Expected:** existing `## ` `section_fingerprint` values are byte-identical regardless of `--depth`, so opting into finer `### ` granularity never triggers false drift on existing tasks.

**Pass criteria:** `--depth 2` output ⊆ `--depth 3` output; `## ` values identical across depths. (Mechanically covered by `test_sections_depth3_is_additive`.)

## Trace D — subsection narrowing spares unaffected tasks (DEC-021 companion, v4.25.0)

Command path: `commands/work.md § "Step 1b"` (`fingerprint.py --drift .claude`) → `drift-reconciliation.md § "Subsection-level drift narrowing"`.

State: `## Phase 40` (58K, subsections `### A`–`### H`) has 47 tasks. A one-line edit lands in `### X` only. Some tasks carry `spec_subsection` + `subsection_fingerprint` (DEC-021 optional provenance), some are legacy (none).

1. The drift check lists `## Phase 40` under `drifted` (its `## ` hash changed), with every task whose `section_fingerprint` differs.
2. Each listed task carries `subsection_unchanged`. It is `true` only when the task has a non-empty `spec_subsection` and `subsection_fingerprint`, and the current hash of that `### ` subsection, looked up under `## Phase 40` only, exists and equals `subsection_fingerprint`. The flag needs no snapshot and no section-size threshold.
3. With the snapshot present, the UI also shows the subsection breakdown (`fingerprint.py --sections --depth 3`, current vs snapshot): *"Phase 40 changed — specifically `### X` (`### A`–`### H` minus X unchanged)."*
4. Task grouping:
   - `spec_subsection == "### X"` → its stored `subsection_fingerprint` no longer matches → `subsection_unchanged: false` → flagged for reconciliation.
   - `spec_subsection` in an unchanged subsection → `subsection_unchanged: true` → "likely unaffected (subsection unchanged)" group with `[K]` Keep recommended, surfaced, not dropped.
   - No `spec_subsection` (legacy), no `subsection_fingerprint`, or a subsection heading no longer in the spec → `subsection_unchanged: false` → flagged at `## `-level exactly as today.
5. Narrowed tasks stay in the section's `drifted` list, so `## Phase 40` still counts in `unreconciled_sections` until the user reconciles it.

**Expected:** tasks whose subsection is provably unchanged are marked likely unaffected; legacy tasks behave exactly as before; nothing is silently dropped.

**Pass criteria:** narrowing marks only tasks with both provenance fields and an unchanged current `### ` hash; conservative "surface, don't drop"; the per-task flag doesn't depend on the snapshot or the section's size (the snapshot only feeds the breakdown and the diff); `## `-level fallback when the task lacks provenance or its subsection heading is gone. (Additive `### ` hashing is mechanically covered by `test_sections_depth3_is_additive`.)

## Invariant checks

- Exactly one `spec_v{N}.md` still exists — Option 2 changed no file-structure invariant (the higher-bar edit Options 1/3 would have required).
- `settings.json` DEC-016 `permissions.ask` globs unchanged (`.claude/spec_v*.md` still matches; the generated `.index.json` is not hand-edited spec text, so it needs no gate).
- The index is regenerable; deleting it degrades to whole-file reads with zero correctness impact (the reversibility that drove the Option 2 choice).
