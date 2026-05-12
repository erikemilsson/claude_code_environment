---
name: decomposition-heuristics
description: Procedure and guidelines for decomposing a spec into granular tasks. Use when decomposing a spec (e.g., running /work decomposition step), creating task JSON files from spec sections, setting task provenance fields (spec_fingerprint, section_fingerprint, phase, cross_phase), computing spec/section hashes for drift detection, or organizing tasks into implementation stages (Foundation, Core Features, Polish, Validation). Covers all 10 decomposition steps, task creation fields, difficulty bounds, phase/cross-phase assignment heuristics, decomposition quality checks, and the post-step-8 decomposition pre-pass validation (path resolution + ripple inference heuristics).
---

<!-- During Skills trial (DEC-007 Option B, 2026-04-17): this Skill mirrors `.claude/support/reference/decomposition.md`. Update both files in sync until one is retired. -->

# Spec Decomposition

Procedure for breaking a spec into granular tasks. Run as `/work` Step 4 "If Decomposing."

---

## Procedure

1. **Run setup checklist** — Read `.claude/support/reference/setup-checklist.md` and run through its checks. Report any warnings inline. Continue regardless (advisory, not blocking).

2. **Read spec thoroughly** — Understand all requirements and acceptance criteria.

3. **Compute spec fingerprint** — SHA-256 hash of spec content (see `drift-reconciliation.md` § "Spec Drift Detection").

4. **Save spec snapshot** — Copy current spec to `.claude/support/previous_specifications/spec_v{N}_decomposed.md`.

5. **Parse spec into sections** — Extract `##` level headings and their content.

6. **Compute section fingerprints** — SHA-256 hash of each section (heading + content).

7. **Identify work items** — Each distinct piece of functionality per section.

8. **Create task files** — One JSON per task, difficulty <= 6, with full provenance:
   - `spec_fingerprint` — Hash of full spec computed in step 3
   - `spec_version` — Filename of spec (e.g., "spec_v1")
   - `spec_section` — Originating section heading (e.g., "## Authentication")
   - `section_fingerprint` — Hash of specific section computed in step 6
   - `section_snapshot_ref` — Snapshot filename (e.g., "spec_v1_decomposed.md")
   - **Important:** Create all task JSON files before regenerating the dashboard. Every task must have a `task-*.json` file — the dashboard is generated from these files, never the other way around.
   - **After creating task JSONs:** run the Decomposition Pre-Pass Validation (below) to catch declared-path drift and under-counted `files_affected` before tasks ship to `/work` Step 2c.

9. **Map dependencies** — What must complete before what.

10. **Regenerate dashboard** — Follow `.claude/support/reference/dashboard-regeneration.md` in full.

---

## Decomposition Pre-Pass Validation

Runs after step 8 (Create task files). Catches two recurring failure modes that surface as implementer-side friction (~3 wasted tool uses per path-correction; friction markers across ~40% of large-batch sessions).

### Leg 1: Path Resolution Check

For each task JSON just created, verify that every path in `files_affected` exists. Also scan the task `description` for path-shaped tokens (matches like `src/components/.../*.tsx`, `tests/.../*.test.py`) and verify those resolve too.

For any non-resolving path, surface inline:

```
Decomposition warning: Task {id} references non-existent path
  declared: src/components/grooming/GroomingSection.tsx
  closest match: src/components/style/GroomingSection.tsx
  → fix the task before continuing? [Y/N]
```

Use a fuzzy-match (e.g., `Glob` for the basename) to suggest the closest existing path. If no match, leave the warning and let the user correct. Do not auto-rewrite — the suggestion may be wrong.

### Leg 2: Ripple Inference

For each task, run targeted greps to surface ripple-affected files the declared `files_affected` may miss. Four detection heuristics:

| Pattern in task description | Grep target | Add to candidates |
|----------------------------|-------------|-------------------|
| `remove X` / `retire X` / `deprecate X` (where X is a field, type, or constant) | `grep -r "X"` across `**/__tests__/**`, `**/*.test.{ts,py,js}`, paths matching `*fixture*` / `*mock*` | Test/fixture files containing the value |
| `.max(N)` → `.max(M)` or any threshold change | `grep -r "{old_threshold}"` in fixture files | Fixtures with hard-coded values that share the schema-constant's name |
| New test files under `__tests__` / sibling-test convention | Read `package.json` `scripts.test` — if it chains explicit paths (vs glob), suggest `package.json` | `package.json` for chain-style test runners |
| Validator-walk extension (Zod/Pydantic `superRefine`, strict-parse) | `grep -r "{ParserSchemaName}\.parse\|\.{ParserSchemaName}\.safeParse"` | Downstream callers |

For each candidate, surface:

```
Decomposition note: Task {id} may be under-counting files_affected
  declared: [field-definitions.json]
  candidates from ripple grep: registry-loader.test.ts (matches "life_stage" in fixture)
  → add to files_affected? [Y/N]
```

Like Leg 1, do not auto-add — present and ask. Both legs are advisory: they reduce implementer friction without blocking decomposition if the user disagrees.

### When to Run

- Always after step 8 of the standard procedure
- Optionally as a standalone check on existing task files (via `/health-check` integration — see future scope)
- Skip for trivial decompositions (≤3 tasks, all touching disjoint single files)

### Limits

The heuristics are deliberately narrow — they catch the dominant friction patterns (verified across styler Phase 20: 12+ tasks, ~40% with files_affected under-counts) without trying to be exhaustive. Function-name drift, deep import-graph ripples, and runtime-only dependencies remain implementer-side discovery work; that's acceptable given the alternative (full static analysis at decomposition time) is much more expensive.

---

## Task Creation Guidelines

- Clear, actionable titles ("Add user validation" not "Backend stuff")
- Difficulty 1-6 (break down anything larger)
- Explicit dependencies
- Owner: claude/human/both
- Include all spec provenance fields (fingerprint, version, section, section_fingerprint, section_snapshot_ref)
- **Phase field:** Assign `phase` based on spec section structure (e.g., tasks from "## Phase 1: Data Pipeline" get `"phase": "1"`). Also set `phase_name` to the spec's descriptive name for the phase (e.g., `"phase_name": "Data Pipeline"`). Dashboard rendering uses the format "Phase {N} — {phase_name}" — generic labels like "Phase 1" alone are not acceptable.
- **Decision dependencies:** If a task depends on an unresolved decision, add the decision ID to `decision_dependencies` array. Note whether the decision is an inflection point in task notes.
- **Cross-phase flag:** Consider suggesting `cross_phase: true` for long-lead tasks that must start before prior phase completion. Heuristic: `owner: human` tasks whose title or notes contain recruit/procure/approve/schedule/coordinate/stakeholder/vendor/contract, OR any task with `external_dependency.expected_date` more than 14 days out. When the heuristic fires, ask the user: `"Task {id} looks like long-lead work. Mark as cross_phase: true? [Y/N]"`. Never set silently. See `task-schema.md` § `cross_phase` for semantics.

---

## Spec Status Transition

When decomposition begins, update the spec metadata `status` from `draft` to `active`:

```yaml
---
version: 1
status: active
---
```

This signals that the spec is being implemented. The transition to `complete` happens in the "If Completing" section of `/work`.

---

## Organizing Tasks Into Stages

When decomposing the spec, organize tasks into logical implementation stages:

| Stage | Focus | Examples |
|-------|-------|----------|
| **Foundation** | Setup, core infrastructure, initial research | Project structure, database schema, vendor research, requirements gathering |
| **Core Features** | Main functionality from spec | Primary user flows, API endpoints, procurement, key deliverables |
| **Polish** | Edge cases, error handling, refinement | Validation, error messages, budget reconciliation, final reviews |
| **Validation** | Testing, documentation, verification | Unit tests, integration tests, documentation, acceptance checks |

These are organizational stages for tasks within the Execute phase, not workflow phases.

---

## Decomposition Quality Checks

Each task must have:
- Clear "done" criteria
- Independent testability
- Explicit dependencies
- Difficulty <= 6

For the difficulty scale, see `.claude/support/reference/shared-definitions.md`.
