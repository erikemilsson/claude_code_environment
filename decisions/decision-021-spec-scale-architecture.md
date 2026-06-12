---
id: DEC-021
title: Spec-scale architecture — the single-file ceiling at large-project scale
status: implemented
category: architecture
created: 2026-06-12
decided: 2026-06-12
related:
  tasks: []
  decisions: [DEC-016, DEC-018, DEC-019]
implementation_anchors:
  - file: ".claude/scripts/fingerprint.py"
    description: "--index (spec section index) + --sections --depth 3 (additive ### hashes, companion a)"
  - file: ".claude/scripts/tests/test_fingerprint.py"
    description: "5 new tests for --index + --depth (suite 70/70 green)"
  - file: ".claude/rules/spec-workflow.md"
    description: "§ Section-scoped spec reading — canonical discipline (auto-loaded)"
  - file: ".claude/support/reference/drift-reconciliation.md"
    description: "§ Spec Index Freshness — regenerate-on-fingerprint-change rule"
  - file: ".claude/commands/work.md"
    description: "Step 1b index-refresh + If Decomposing index generation"
  - file: ".claude/agents/implement-agent.md"
    description: "section-scoped spec-read pointer (subagent context)"
  - file: ".claude/agents/verify-agent.md"
    description: "section-scoped spec-read pointer (subagent context)"
inflection_point: true
spec_revised:
spec_revised_date:
blocks: []
---

# Spec-scale architecture — the single-file ceiling at large-project scale

> **Template-maintenance decision** (root `decisions/`, not `.claude/support/decisions/`). Source: **FB-095** (`template-maintenance/feedback.md`). Research archive: `decisions/.archive/decision-021-research-2026-06-12.md`. Produced via `/research` (research-agent investigation, Opus tier, 2026-06-12).

## Select an Option

Mark your selection by checking one box:

- [ ] **Option 1:** Sharded spec — `.claude/spec/` directory of per-domain files + a generated manifest (invariant → "exactly one manifest")
- [x] **Option 2:** Single file + mandatory generated index + section-scoped read discipline — *(recommended)* — **SELECTED 2026-06-12**
- [ ] **Option 3:** Tiered spec — stable-core + active-surface files, periodic merge
- [ ] **Option 4:** Status quo + spec-diet discipline (`/iterate hygiene` move-to-archive pass)

*Check one box above, then fill in the Decision section below. The two **companion actions** (see Recommendation) are orthogonal to this choice and can ship under any option — note in the Decision section whether you want them.*

## Background

The template's spec workflow assumes a **single monolithic `spec_v{N}.md` readable in one pass**. The most active downstream project (styler) has outgrown that assumption, and the assumption is encoded in a **Critical Invariant** (`.claude/CLAUDE.md`: *"Exactly one `spec_v{N}.md` exists in `.claude/` at any time"*), so this is a template-level architecture question, not a styler-local one.

**Evidence (styler, confirmed empirically during research):**
- `spec_v15.md` = **846,107 chars (~200K+ tokens)** — larger than a 200K context window outright; dominates any working set when combined with code. (FB-095 captured 837K on 2026-06-10; grown ~9K since — it grows monotonically by design.)
- Structure: **57 top-level `## ` sections** (~50 are `## Phase N`, appended Phase 1 → 48+), **406 `### ` subsections**. **12 sections exceed 20K chars; the largest, `## Phase 40`, is 58,031 chars.**
- 15 prior spec versions archived (56 files); 132 decision records.
- Friction register: **22 of 39 markers are `spec_implementation_gap`**; 8 of 10 open markers are spec-vs-code gaps.
- `/iterate` is the #2 command by usage (59 vs `/work`'s 87 across a 47-export corpus); **38% of sessions are zero-task meta-sessions** (spec upkeep on a file no agent can hold whole).
- Specs only grow: feature retirement **annotates rather than excises** (`rules/feature-retirement.md`) — correct for drift detection, but monotonic by construction.

**The operative pain is consumption, not storage** — the spec is too big to hold whole, locate within, and reason against, which is what inflates `/iterate` cost and meta-session share. That framing is what separates the options below.

## Options Comparison

| Criterion | Opt 1: Shard | Opt 2: Index | Opt 3: Tier | Opt 4: Diet |
|---|---|---|---|---|
| **Scaling headroom** | Strong | Weak/Moderate | Moderate | Weak |
| **Drift-detection integrity** | Moderate (needs manifest mode) | **Strong (fingerprint.py untouched)** | Moderate (merge = false drift) | Strong |
| **Migration cost** (846KB) | High | **Low/Med** | High | Low |
| **Blast radius** | Large (~14+ incl. invariant) | **Small (~11 light, 0 invariant)** | Medium | Minimal |
| **Tooling-change scope** | Large | Medium | Large | Small |
| **Reversibility** | Weak | **Strong (delete the index)** | Weak | Strong |
| **Invariant impact** | **Breaks** | **None** | **Breaks** | None |
| **Overall** | Highest headroom, highest cost/risk; only true structural fix | **Best cost/benefit; preserves everything; modest headroom** | Headroom without solving monotonic growth; merge-drift hazard | Cheapest; explicitly a delay, not a fix |

*(Full per-criterion evidence, the complete 25-row blast-radius table, the drift-detection deep-dive, and per-option migration procedures are in the research archive.)*

## Option Details

### Option 1: Sharded spec (`spec/` dir + manifest)
**Description:** Per-domain (here: per-phase) files under `.claude/spec/`, plus a generated manifest. The Critical Invariant becomes "exactly one spec manifest."
**Strengths:** Only option that truly solves the size problem — agents read 1–2 relevant shards, never the monolith. styler's 57-phase structure maps ~1:1 to shards (mechanical split). Drift detection gets *finer* (the 58K Phase 40 hash becomes one shard's internal map).
**Weaknesses:** Largest blast radius (~14+ touchpoints, breaks the invariant — the highest-bar edit). High migration (rewrite every task's `section_snapshot_ref`, build per-shard snapshots, change DEC-016 `settings.json` globs or it silently un-enforces, invert the single-spec health-check). Weak reversibility (back-out = a 2nd migration). New failure mode: section moved between shards reads as delete+add unless the manifest tracks mapping.
**Research Notes:** `fingerprint.py` has no multi-file mode (must build `--manifest`); `settings.json` globs are exactly `Edit/Write(.claude/spec_v*.md)`; `health-check.md` § "1. Single-Spec Invariant" hard-codes `count>1 → ERROR` + auto-archive. See archive § B/C.

### Option 2: Single file + mandatory generated index *(recommended)*
**Description:** Keep the single-file invariant. Add a compiled index artifact (`.claude/spec_v{N}.index.json` — heading → line-range → section fingerprint → 1-line synopsis) + a **section-scoped read discipline**: spec-reading sites consult the index, then `Read` with `offset`/`limit` to pull only the relevant `## ` section(s).
**Strengths:** Preserves everything — invariant, `fingerprint.py`, task/decision provenance, retirement markers, DEC-016 globs. Strong reversibility (the index is derived; delete → status quo, zero state migration). Smallest blast radius + migration. Attacks the operative pain (targeted reads as default) with machinery the template already has (`Read offset/limit` everywhere; `fingerprint.py --sections` already emits heading→hash). Operationalizes the template's own *"1M is headroom, not license… prefer targeted reads"* posture.
**Weaknesses:** Does **not** cap file growth — manages consumption, not size (under-delivers if the real pain is edit ergonomics / git-diff noise / merge conflicts). Index needs a freshness check (cheap — regenerate on full-spec fingerprint change). `/iterate propose` still reasons against the whole spec conceptually.
**Research Notes:** Index is a near-free derivative of `fingerprint.py --sections` + line-ranges + synopsis. ~11 spec-reading sites (`work.md` version discovery, `iterate.md`, `review.md`, `research.md`, `status.md`, `shakedown.md`, both agents) gain an index-consult step; drift detection + `fingerprint.py` are untouched. See archive § B/C/D.

### Option 3: Tiered spec (stable-core + active-surface)
**Description:** `spec_v{N}_core.md` (frozen) + `spec_v{N}_active.md` (current), periodic merge active→core. Mirrors task-archive tiering.
**Strengths:** Caps the active-surface working set; has a template precedent (task archiving).
**Weaknesses:** Doesn't solve monotonic growth (core grows forever; merges re-inflate). **Merge-drift hazard:** moving a section active→core changes neither content nor hash but changes the *file*, so `section_snapshot_ref` points at the wrong tier — every merge is a provenance migration that risks resetting Finished tasks to re-verify. Breaks the invariant (→ two-file) for less headroom than Option 1. styler has no natural core/active cleave (cross-phase refs span the cut).
**Research Notes:** Phase-level verification assumes one spec holds all acceptance criteria — a split forces reading both, re-merging the working set it meant to split. See archive § B/D.

### Option 4: Status quo + spec-diet discipline
**Description:** `/iterate hygiene` gains a "move historical/retired detail to an archive" pass.
**Strengths:** Cheapest; minimal blast radius; strong reversibility; no invariant/fingerprint change.
**Weaknesses:** **Fights the template's own design** — feature retirement annotates, *never excises* (`rules/feature-retirement.md`), *because* excision breaks section fingerprints. A diet pass that moves content out **is** that excision → reconciliation noise on adjacent sections. **Internal contradiction that must be resolved before Option 4 ships safely.** Delays, doesn't solve — styler's bulk is *active* phases (Phase 40 = 58K, 41 = 55K), not retired cruft.
**Research Notes:** `iterate.md § "hygiene mode"` currently cross-checks, does not move content. Not standalone-viable; can ride alongside Option 2 for genuinely-dead detail only. See archive § B.

## Blast-Radius Summary

**Central quantitative finding:** Option 2 changes **zero invariant rows** and touches ~11 spec-reading sites *lightly* (add an index-consult step), leaving `drift-reconciliation.md` and `fingerprint.py` untouched. Options 1 and 3 change **all four invariant rows** — `.claude/CLAUDE.md § Critical Invariants`, `iterate.md § Spec Versioning` (version-transition procedure), `health-check.md § Single-Spec Invariant` (must invert `count>1 → ERROR`), and `settings.json` DEC-016 `permissions.ask` globs (or DEC-016 silently un-enforces — cf. FB-077 sub-issue A) — plus the full ~25-touchpoint set. The complete table is in the research archive § C.

## Recommendation

**Option 2** (single file + mandatory generated index + section-scoped read discipline). **Confidence: Moderate** — high on the cost/risk asymmetry, moderate on whether it delivers *enough* headroom for styler's specific trajectory.

The reversibility + invariant-preservation + small-blast-radius profile matches the template's **evidence-first, reversible-default posture** (DEC-018 declined a permanent-cost router after a value deep-dive; FB-085 shipped only once cost was bounded + reversible). Breaking the single-spec invariant and rewriting all task provenance is the opposite of that posture and should demand stronger evidence than "the file is big." The evidence points at **consumption** (a file no agent can hold whole; `/iterate` #2; 38% meta-sessions), which Option 2 targets directly.

**Conditional caveat:** if the user's felt bottleneck is **single-file edit ergonomics / git-diff noise / spec merge conflicts** rather than read-working-set, an index doesn't help — **escalate to Option 1**, for which styler's clean phase=shard structure is the best-case (cheapest-ever) migration input. **Reject Option 3** unless a future project has a genuine stable-core/active cleave. **Option 4** is not standalone-viable until the retirement-no-excise contradiction is resolved.

**Two companion actions (orthogonal — capture under any option):**
1. **Finer section fingerprinting** — extend `fingerprint.py --sections` to optionally split on `### `; at 846KB the `## `-only split rehashes 58K-char sections on a one-line edit. Cheap, independent, improves drift precision everywhere (one-time re-fingerprint churn on in-flight tasks).
2. **Index-as-derivative even under status quo** — the section index is independently useful for scoped reads even with no architecture change; the lowest-regret first step (and literally *is* Option 2's core artifact).

## Your Notes & Constraints

*This section is yours — Claude reads it but never overwrites it.*

**Constraints:**
-

**Questions (seeded by research — answering these narrows the choice):**
1. **What is the actual felt bottleneck?** Read-working-set / proposal-location / agent context (→ Option 2), *or* single-file edit ergonomics + git-diff noise + spec merge conflicts (→ Option 1)? *This single answer can flip the recommendation.*
2. **Growth-rate tolerance:** is "manage consumption, defer the size ceiling" (Option 2) acceptable, or do you want the size problem *structurally solved now* (Option 1) while styler's clean phase=shard structure makes migration the cheapest it will ever be?
3. **Willingness to touch the "exactly one `spec_v{N}.md`" Critical Invariant** (Options 1 & 3 require it; 2 & 4 preserve it)?
4. **Appetite for migrating styler's live `spec_v15.md` now vs. later** (Opt 1/3 = High, rewrites all task provenance + decision cross-refs; Opt 2 = Low derive)?
5. **Ship the finer-fingerprinting companion (split on `### `) independently** of this decision? (Cheap + orthogonal; one-time churn to existing `section_fingerprint` values.)
6. **Does `/shakedown`'s capability-boundary corpus relieve spec-growth pressure** (FB-095's open question re FB-093)? If the dated corpus carries more of the "where the system is" duty, some spec sections may not need to grow — favoring the lighter Option 2/4.

## Decision

**Selected:** Option 2 — Single file + mandatory generated index + section-scoped read discipline.

**Rationale:** Chosen 2026-06-12 (user) on the research recommendation. The **blast-radius asymmetry** is decisive: Option 2 preserves the "exactly one `spec_v{N}.md`" Critical Invariant, leaves `fingerprint.py` and all task/decision provenance untouched, and is a *derived (deletable) artifact* — so it carries near-zero migration cost and strong reversibility. It targets the operative pain in FB-095 — **consumption** (a file no agent can hold whole), not storage — using machinery the template already has (`Read offset/limit`; `fingerprint.py --sections`). This matches the template's evidence-first, reversible-default posture (DEC-018, FB-085): the structural options (1/3) that break the invariant and force a full styler provenance migration are not justified by current evidence, since "the file is big" is fundamentally a consumption problem the index solves more cheaply and reversibly. **Option 1 (shard) remains the documented escalation** if edit-ergonomics / git-diff-noise / spec merge-conflicts later prove the dominant bottleneck (see Risks).

## Trade-offs

**Gaining:**
- Critical Invariant preserved; zero `fingerprint.py` / task-provenance / decision-cross-ref / DEC-016-settings migration.
- Strong reversibility — the index is derived; delete it to revert.
- Scoped-read default that shrinks the spec working set for `/iterate`, decomposition, audits, `/shakedown`, and both agents — the lowest-regret first step.

**Giving Up:**
- Does **not** cap file *size* — the monolith keeps growing; this manages consumption, not storage.
- A new index-freshness obligation (cheap — fingerprint-driven regeneration).
- If edit-ergonomics / git-diff-noise become the dominant pain, the index under-delivers and Option 1 (shard) becomes the escalation.

## Impact

**Implementation Notes:** **Shipped v4.24.0 (2026-06-12)** — see ship-log + `implementation_anchors`. Scope as built:
1. A generated section-index artifact (e.g. `.claude/spec_v{N}.index.json` — heading → line-range → section fingerprint → 1-line synopsis).
2. A `fingerprint.py --index` mode (sibling to `--sections`) + tests.
3. An index-freshness check (regenerate when the full-spec fingerprint changes — reuse existing machinery: `/work` Step 1a freshness / `drift-reconciliation.md`).
4. A section-scoped read discipline added to the ~11 spec-reading sites (blast-radius rows 3, 4, 6, 8, 10, 11, 12, 15, 23, 24 + `status.md`).
5. Docs: `spec-workflow.md` + a reference note; `.claude/CLAUDE.md` Navigation row for the index.
6. **Companion actions** (orthogonal — decide at implementation): (a) finer `### ` fingerprinting in `fingerprint.py --sections`; (b) the index *is* the "index-as-derivative" companion.
Invariant, `settings.json` DEC-016 globs, `drift-reconciliation.md`, and task/decision provenance are **untouched** (rows 1, 5, 13, 16, 18, 19 in the blast-radius table stay put — `fingerprint.py` only gains an additive `--index` mode).

**Affected Areas:**
- ~11 spec-reading command/agent sites (light index-consult addition) — see Blast-Radius Summary + research archive § C.
- New: `fingerprint.py --index` mode + tests; the index artifact convention.
- Explicitly NOT modified: the single-spec invariant, drift-reconciliation core, DEC-016 settings globs.

**Risks:**
- Index staleness vs. spec body — mitigated by a fingerprint-driven freshness check.
- Scoped-read discipline is a *convention* agents follow, not structurally enforced (same status as the template's existing targeted-read guidance).
- Moderate-confidence on headroom — re-evaluate against Option 1 (shard) if the felt bottleneck proves to be edit-ergonomics rather than consumption. This is the documented escalation path, not a silent dead end.
