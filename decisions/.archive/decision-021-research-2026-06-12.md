# DEC-021 Research Archive — Spec-Scale Ceiling (FB-095)

**Date:** 2026-06-12 · **Category:** architecture · **Inflection point:** yes (touches a Critical Invariant) · **Status at research time:** draft → proposed

**Methodology:** `/research` flow — research-agent (Opus tier, general-purpose persona) dispatched by the orchestrator to investigate FB-095's four candidate directions against the template's actual spec-handling surface, then return a structured report. The orchestrator wrote this archive + `decision-021-spec-scale-architecture.md` from the report (subagents do not own root `decisions/` writes; write-ownership stays with the orchestrator). The agent did NOT select an option — evidence only.

**Files read (template repo, all under `/Users/erikemilsson/Developer/claude_code_environment/`):** `.claude/CLAUDE.md`, root `CLAUDE.md`, `template-maintenance/feedback.md` (full FB-095), `.claude/rules/spec-workflow.md`, `.claude/support/reference/drift-reconciliation.md`, `.claude/scripts/fingerprint.py` + `tests/test_fingerprint.py`, `.claude/commands/{iterate,work,audit-coherence,health-check,shakedown,grill,review,status,research}.md`, `.claude/settings.json`, `.claude/support/reference/{task-schema,decomposition,paths,workflow,decisions,extension-hooks}.md`, `.claude/agents/{research,verify,implement}-agent.md`.

**Empirical grounding:** `/Users/erikemilsson/Developer/styler/.claude/spec_v15.md` — **846,107 chars** (confirms + slightly exceeds FB-095's 837,049 figure; grown ~9K since 2026-06-10). Structure: **57 top-level `## ` sections** (~50 are `## Phase N — …`, monotonically appended Phase 1 → Phase 48+), **406 `### ` subsections**, 1 H1. **12 sections exceed 20K chars; the largest, `## Phase 40`, is 58,031 chars** — larger than many entire specs. The natural shard boundary is the phase.

---

## A. Options Comparison Matrix

| Criterion | Opt 1: Sharded spec (`spec/` dir + manifest) | Opt 2: Single file + generated index | Opt 3: Tiered (stable-core + active-surface) | Opt 4: Status quo + spec-diet discipline |
|---|---|---|---|---|
| **Scaling headroom** | **Strong** — per-domain files stay individually readable; no single-file ceiling | **Weak/Moderate** — file still grows unbounded; index aids navigation, not working-set size | **Moderate** — caps *active-surface* size; stable-core still grows, merges re-inflate | **Weak** — delays ceiling; diet fights monotonic-growth-by-design |
| **Drift-detection integrity** | **Moderate** — needs `fingerprint.py` manifest mode; per-shard `## ` hashing works & gets finer | **Strong** — `fingerprint.py` untouched; index is derived, not fingerprinted | **Moderate** — two files; cross-file section moves on merge look like delete+add (false drift) | **Strong** — zero fingerprint change; diet edits ARE drift events |
| **Migration cost** (846KB) | **High** — split 57 sections, rewrite every task's provenance, build manifest, change settings globs | **Low/Med** — generate index artifact; no spec restructure; no task-JSON churn | **High** — partition 57 phases by judgment, merge ritual, dual snapshots | **Low** — one hygiene pass; no structural change |
| **Blast radius** | **Large** — ~14+ touchpoints + invariant changes | **Small** — invariant preserved; ~11 touchpoints gain an index read | **Medium** — invariant → two-file; discovery + drift + decomposition adapt | **Minimal** — one new hygiene sub-mode |
| **Tooling-change scope** | **Large** | **Medium** | **Large** | **Small** |
| **Reversibility** | **Weak** — re-concatenating + reverting provenance is a 2nd migration | **Strong** — delete the index; spec untouched | **Weak** — merge back, revert dual-snapshots | **Strong** — a discipline, not a structure |
| **Invariant impact** | **Breaks** "exactly one `spec_v{N}.md`" → "one manifest" | **None** — preserved | **Breaks** → "one core + one active" | **None** |
| **Overall** | Highest headroom, highest cost & risk; only true structural fix | **Best cost/benefit**; preserves everything, modest headroom | Headroom without solving monotonic growth; high cost; merge-drift hazard | Cheapest; explicitly a delay, not a fix |

---

## B. Option Details

### Option 1 — Sharded spec (`spec/` directory + generated manifest)
A `.claude/spec/` directory with per-phase files plus a generated `manifest.json`/index. The Critical Invariant "exactly one `spec_v{N}.md`" becomes "exactly one spec manifest."

**Strengths**
- Only option that actually solves the 846KB→growing problem: each shard stays independently readable; agents read the 1–2 shards relevant to a task.
- styler's structure makes this natural: 57 `## Phase` sections map ~1:1 to shard files with near-zero re-partitioning.
- Drift detection gets *finer*: sharding on the phase boundary turns the 58K-char Phase 40 hash into one shard's internal `## `/`### ` map.

**Weaknesses**
- Largest blast radius: ~14+ touchpoints assume a single `spec_v*.md` path/glob (§ C); the invariant change is the highest-bar edit in the template.
- Migration High: every task's `spec_version` + `section_snapshot_ref` must be rewritten; `settings.json` DEC-016 globs change; single-spec health-check inverts.
- Weak reversibility (backing out = a second migration).
- New failure mode: a section moved between shards reads as delete+add unless the manifest tracks section→shard mapping.

**Research notes**
- `fingerprint.py` `hash_sections` (L23–45) splits on `^## (?!#)` per file — works per-shard, but there is **no multi-file/manifest mode**; one must be built (`--manifest PATH`).
- `settings.json` `permissions.ask` globs are exactly `Edit/Write(.claude/spec_v*.md)` — a `spec/` dir needs `.claude/spec/**/*.md` added or DEC-016 silently un-enforces (cf. FB-077 sub-issue A, where a path-scope mismatch already caused false classifier behavior).
- `health-check.md § "1. Single-Spec Invariant"` (L448–457) hard-codes `count > 1 → ERROR` + auto-archive — actively fights a sharded layout; must be rewritten.
- `audit-coherence.md` Phase 1 step 4 builds one section map from "exactly one" spec — needs to iterate shards.

### Option 2 — Single file + mandatory generated index ⭐ (recommended)
Keep the single-file invariant. Add a compiled index artifact (`.claude/spec_v{N}.index.json` — heading → line range → section fingerprint → 1-line synopsis) + a **section-scoped read discipline**: commands/agents read the index first, then `Read` with `offset`/`limit` to pull only the relevant `## ` section(s).

**Strengths**
- Preserves everything: the Critical Invariant, `fingerprint.py`, task provenance, decision cross-refs, retirement markers, DEC-016 globs — all untouched.
- Strong reversibility: the index is derived; delete it → status quo, zero state migration.
- Smallest blast radius + migration cost: generate the index once; teach the spec-reading sites to consult it.
- Directly attacks the operative pain — *"a file no agent can hold whole"* — by making targeted reads the default. The template already uses `Read offset/limit` everywhere; `fingerprint.py --sections` already emits the heading→hash map the index needs.

**Weaknesses**
- Does **not** cap file growth — manages *consumption*, not *size*. Under-delivers if the real bottleneck is git-diff noise or single-file edit ergonomics.
- Index can go stale vs. the body (needs a freshness check — cheap, reuses the `fingerprint.py` full-spec hash).
- `/iterate propose` still reasons against the whole spec conceptually; the index helps it *locate*, not shrink the proposal surface.

**Research notes**
- The index is a near-free derivative of `fingerprint.py --sections` (L82–86) + line-ranges + synopsis (small `--index` mode / sibling script).
- `work.md § "Version discovery"` (L272–279) + `iterate.md` Step 1 + `review.md` L26 + `research.md` L68 + `status.md` L30 all glob `spec_v*.md` and `Read` it — exactly the sites that consult the index then scoped-read. No path/invariant change.
- Operationalizes the template's own **Context budget** posture (`.claude/CLAUDE.md`: *"1M is headroom, not license… prefer targeted reads"*).

### Option 3 — Tiered spec (stable-core + active-surface, periodic merge)
`spec_v{N}_core.md` (frozen completed phases) + `spec_v{N}_active.md` (current surface), periodic merge active→core. Mirrors task-archive tiering.

**Strengths**
- Caps the active-surface working set; has a template precedent (task archiving at >100 tasks).

**Weaknesses**
- Doesn't solve monotonic growth: core grows forever; each merge re-inflates. Half-measure with most of sharding's costs.
- **Merge-drift hazard:** moving a section active→core changes neither content nor fingerprint, but the *file* changes — `section_snapshot_ref` (task-schema L117) points at the wrong tier; every merge is a provenance migration that risks resetting Finished tasks to re-verify.
- Breaks the single-spec invariant (→ two-file) for less headroom than Option 1.
- Weak reversibility.

**Research notes**
- styler has no natural "stable vs active" cleave — 57 phases with cross-phase references; partitioning is judgment per phase, unlike Option 1's mechanical split.
- Phase-level verification (verify-agent reading "Specification acceptance criteria") assumes one spec holds all criteria; a split forces reading both files — re-merging the working set it meant to split.

### Option 4 — Status quo + spec-diet discipline
`/iterate hygiene` gains a "move historical/retired detail to an archive" pass.

**Strengths**
- Cheapest; minimal blast radius; strong reversibility; no invariant/fingerprint change. FB-095's own triage: direction 4 → likely no DEC.

**Weaknesses**
- **Fights the template's own design:** feature retirement **annotates, never excises** (`rules/feature-retirement.md § "Spec Annotation (do NOT excise)"`), *because* excision breaks section fingerprints (`drift-reconciliation.md`). A diet pass that moves content out **is** that excision — it would trigger version-bump/reconciliation noise on adjacent sections. **Direct internal contradiction; must be resolved before Option 4 ships safely.**
- Delays, doesn't solve. styler at 846K is past where trimming retired detail buys headroom — the bulk is *active* phases (Phase 40 = 58K, Phase 41 = 55K), not retired cruft.

**Research notes**
- `iterate.md § "hygiene mode"` (L161–224) cross-checks spec claims vs. a structured artifact; it does NOT move content. Adding a diet pass collides with the retirement-annotation invariant.

**No option discarded.** Options 2 and 4 could combine (index for read-discipline + diet for genuinely-dead detail) *if* the retirement-excision contradiction is resolved.

---

## C. Blast-Radius Enumeration (full)

Every template touchpoint assuming a single spec path/glob. "**Inv**" = depends on the single-spec invariant specifically.

| # | Touchpoint (`file § anchor`) | Assumption | Opt 1 (shard) | Opt 2 (index) | Opt 3 (tier) |
|---|---|---|---|---|---|
| 1 | `.claude/CLAUDE.md § "Critical Invariants"` — *"Exactly one `spec_v{N}.md`"* | **Inv** | **Rewrite** → "one manifest" | none | **Rewrite** → "one core + one active" |
| 2 | `.claude/CLAUDE.md § Navigation` — spec row | single path | update to dir/manifest | add index row | update to two files |
| 3 | `commands/work.md § "Version discovery"` (L272–279) — glob `spec_v*.md`, highest N | single file | glob shards + read manifest | + read index, scoped reads | glob both tiers |
| 4 | `commands/work.md § "If Decomposing"` → `decomposition.md` steps 4–6, 8 (snapshot, section parse, provenance) | one spec, one snapshot | per-shard snapshots; provenance gains shard id | unchanged (index derived) | dual-tier snapshots |
| 5 | `commands/iterate.md` Step 1 + § "Spec Versioning" (L446) + Version Transition (L481–504) | **Inv** | rewrite transition for N shards + manifest | none | rewrite for two tiers |
| 6 | `commands/iterate.md § "hygiene mode"` — reads one spec | single file | iterate shards | scoped reads via index | read active tier |
| 7 | `commands/audit-coherence.md` Phase 1 step 4 — "exactly one", one section map | **Inv** | iterate shards into combined map | unchanged (or use index) | merge two tiers |
| 8 | `commands/review.md` L26, L31 — glob + read for intent | single file | glob shards | scoped read | glob both |
| 9 | `commands/status.md` L30 — version + fingerprint | single file | manifest fingerprint | unchanged | both-tier fingerprint |
| 10 | `commands/research.md` L68, L88 — version discovery, `Spec file:` dispatch | single path | shard/manifest path | scoped path | which-tier path |
| 11 | `commands/grill.md` L33, L130 — reads/guards spec | path glob | shard glob | unchanged | both tiers |
| 12 | `commands/shakedown.md` Phase 0 step 2 — "read the spec + relevant code" | one spec | read relevant shard(s) | scoped read via index | read relevant tier |
| 13 | `commands/health-check.md § "1. Single-Spec Invariant"` (L448–457) — `count>1 → ERROR` + auto-archive | **Inv** | **invert** (shards expected; validate manifest) | none | **rewrite** (two expected) |
| 14 | `commands/health-check.md` checks 2–4 (L459–471) — version continuity, misplaced-spec scan, decomposed-spec | single-file archive model | adapt to shard archives | unchanged | adapt to tier archives |
| 15 | `commands/health-check.md` check 5 + L1028 (`READ spec_v{N}.md` completion gate) | single path | shard/manifest | scoped read | both tiers |
| 16 | `.claude/settings.json` `permissions.ask` — `Edit/Write(.claude/spec_v*.md)` (DEC-016) | path glob | **add** `.claude/spec/**/*.md` or DEC-016 silently un-enforces | none (glob still matches) | add active/core globs |
| 17 | `support/reference/paths.md` L9, L35–36 — canonical "Current spec" + single-spec + glob notes | single path/Inv | update all three | add index row | update for tiers |
| 18 | `support/reference/drift-reconciliation.md` (whole) — full-spec + `## `-section fingerprint over one path; `section_snapshot_ref` | one spec, one snapshot | manifest mode + per-shard snapshot refs | **unchanged** | per-tier refs; merge = false delete+add |
| 19 | `scripts/fingerprint.py` `--spec`/`--sections` (single `Path`) + tests | one file arg | add `--manifest` multi-file mode + tests | **unchanged** (index is a sibling derive) | callers pass two paths |
| 20 | `support/reference/task-schema.md` — `spec_version`, `spec_section`, `section_fingerprint`, `section_snapshot_ref` (L113–117) | section in one spec/snapshot | add shard provenance; rewrite refs on migrate | unchanged | rewrite refs on tier-move |
| 21 | `support/reference/workflow.md` L265, L329, L502, L589 — spec path, frontmatter status, single-spec, layout diagram | single path/Inv | update all | add index note | update for tiers |
| 22 | `support/reference/decisions.md` frontmatter `spec_revised` + `iterate.md § Post-Inflection` reads all decisions to find affected spec sections | sections in one file | section→shard resolution | unchanged | section→tier resolution |
| 23 | `agents/verify-agent.md` L52/L58/L556 (phase-level reads acceptance criteria whole) + L330 (`spec_v*.md` in `files_affected`) | one spec holds all criteria | read shards / all for phase-level | scoped reads via index | read both tiers |
| 24 | `agents/implement-agent.md` L52/L93 — read spec, find section via `spec_section` | one spec | shard-aware lookup | scoped read | tier-aware lookup |
| 25 | `support/reference/extension-hooks.md` L23 — spec *"singular per project, version-bumped"*, in sync-manifest `ignore` | single file | update description | none | update description |

**Central quantitative finding:** Option 2 touches rows 2, 3, 6, 8, 10, 11, 12, 15, 17, 23, 24 **lightly** (add an index-consult step), and rows 18/19 **not at all** — and changes **zero invariant rows (1, 5, 13, 16)**. Options 1 and 3 touch all four invariant rows plus the full set.

---

## D. Drift-Detection Deep-Dive

**Mechanism today:** `fingerprint.py hash_sections` (L23–45) reads the whole file (no size guard — slurps 846KB fine) and splits on `^## (?!#)`. Each task carries `spec_fingerprint` (full hash) + `section_fingerprint` (its `## ` section) + `section_snapshot_ref` (decomposed snapshot). `/work` Step 1b compares; changed sections trigger Granular Reconciliation.

- **Option 2:** `## `-section hashing survives **completely unchanged** — the index is *derived*, not a fingerprint input. No manifest mode. Provenance + decision cross-refs untouched. **Decisive advantage.** Only new obligation: index freshness (regenerate when full-spec fingerprint changes — cheap).
- **Option 1:** `## `-hashing works per shard and gets *finer*. But: (a) a `--manifest` multi-file mode must be **built**; (b) **task provenance breaks** — `section_snapshot_ref` needs per-shard snapshots + a migration rewriting every task; (c) a section moved between shards reads as delete+add unless the manifest tracks section→shard.
- **Option 3:** survives, but **every active→core merge is a provenance-migration event** — identical content/hash, changed ref file → drift must special-case "tier move ≠ content change" or it resets Finished tasks (`drift-reconciliation.md § "On apply"` clears `task_verification` on a changed section ref). High false-positive cascade risk.
- **Option 4:** no mechanism change, but the diet edits collide with the retirement-annotation invariant that exists *specifically to protect section fingerprints*.

**Key scale finding (orthogonal to the architecture choice):** section fingerprinting is **already coarse** at 846KB — 12 sections >20K chars, largest 58K, 406 `### ` folded into parents. A separate cheap win regardless of option: extend `fingerprint.py --sections` to optionally split on `### ` so a one-line edit in Phase 40 doesn't rehash 58K chars.

---

## E. Migration Analysis (existing 846KB `spec_v15.md`)

| Option | Procedure | Cost |
|---|---|---|
| **1 — Shard** | Split 57 `## ` sections into `.claude/spec/{phase-NN-slug}.md` (mechanical); generate `manifest.json`; **rewrite every active task's** `spec_version` + `section_snapshot_ref` (→ per-shard) + shard id; build per-shard decomposed snapshots; update settings DEC-016 globs; invert health-check single-spec validation; re-point 132 decision records' implicit spec-section refs. | **High** |
| **2 — Index** | Run `fingerprint.py --sections` (already works) → seed index; add line-ranges + 1-line synopses (one pass, agent-generated + user-reviewed); write `.claude/spec_v15.index.json`; add index-consult step to ~11 spec-reading sites. **No spec restructure, no task-JSON churn, no decision-ref rewrite, no settings change.** | **Low–Med** |
| **3 — Tier** | Judgment-partition 57 phases into core/active (cross-phase refs span the cut); create both files; rewrite task refs per tier; merge ritual + dual snapshots; update invariant + health-check; special-case drift to suppress tier-move false positives. | **High** |
| **4 — Diet** | One hygiene-style pass identifying genuinely-dead detail; move to archive doc. **Blocked on** resolving the retirement-no-excise contradiction first. | **Low** (low headroom) |

---

## F. Recommendation + Confidence

**Recommended: Option 2** (single file + mandatory generated index + section-scoped read discipline), with two orthogonal companion actions. **Confidence: Moderate** (high on the cost/risk asymmetry; moderate on whether it delivers *enough* headroom for styler's trajectory).

**Why (by criterion):** Reversibility + Invariant impact + Blast radius decisively favor Option 2 — preserves the Critical Invariant, leaves `fingerprint.py` and all task/decision provenance untouched (§ D), touches ~11 sites lightly vs. ~14-plus-invariant for Options 1/3, and is a derived artifact you can delete to revert. This matches the template's **evidence-first, reversible-default posture** (DEC-018 declined a permanent-cost router after a value deep-dive; FB-085 shipped only once cost was bounded + reversible). A migration that breaks the single-spec invariant + rewrites all task provenance is the opposite of that posture and should require much stronger evidence than "the file is big." The operative pain in FB-095 is **consumption, not storage** (*"a file no agent can hold whole,"* `/iterate` #2 command, 38% zero-task meta-sessions) — Option 2 attacks exactly that with machinery the template already has. Option 2's one weakness (manages working-set, not file size) is why confidence is Moderate.

**Conditional caveats:**
- **Option 2 if** the bottleneck is read-working-set / proposal-location / agent context (evidence points here). **Escalate to Option 1 if** the real pain is single-file edit ergonomics, git-diff noise, or spec merge conflicts — an index doesn't help those, and styler's clean phase=shard structure makes Option 1 unusually low-friction *if* its invariant + migration cost is accepted. Option 1 is the only true structural fix; styler is the best-case input for it.
- **Reject Option 3** unless a future project has a genuine stable-core/active cleave — styler doesn't, and the merge-drift provenance hazard is a real recurring false-positive generator.
- **Option 4 not standalone-viable** until the retirement-no-excise contradiction is resolved; it can ride alongside Option 2 for genuinely-dead detail only.

**Two orthogonal companion actions (capture regardless of which architecture wins):**
1. **Finer section fingerprinting** — extend `fingerprint.py --sections` to optionally split on `### `; at 846KB the `## `-only split rehashes 58K-char sections on one-line edits. Cheap, independent, improves drift precision under every option.
2. **Index-as-derivative even under status quo** — the section index is independently useful for scoped reads even with no architecture change; lowest-regret first step.

**Clears the bar for a formal DEC:** **Yes.** Even Option 2 adds a *mandatory* generated artifact + a read-discipline contract across ~11 files, and the live choice between "preserve the invariant" (Opt 2/4) and "break it for real headroom" (Opt 1/3) is the inflection-point shape FB-095 anticipated. Per FB-095's triage, directions 1–3 warrant the full record; this research recommends direction 2, which still ships tooling + a contract. (Only a *pure* Option 4 outcome would have skipped the DEC — and Option 4 is not recommended standalone.)

---

## G. Open Questions for the User

1. **What is the actual felt bottleneck?** Agent context / read-working-set (→ Option 2) *or* single-file edit ergonomics + git-diff noise + spec merge conflicts (→ Option 1)? The single question that flips the recommendation.
2. **Growth-rate tolerance:** styler is at 846KB / ~50 phases, ~1 phase/cycle. Is "manage consumption, defer the size ceiling" (Option 2) acceptable, or solve the size problem *structurally now* (Option 1) while styler's clean phase=shard structure makes migration the cheapest it will ever be?
3. **Willingness to touch the "exactly one `spec_v{N}.md`" Critical Invariant?** Higher bar than normal (FB-077 showed path-scope mismatches cause real DEC-016/classifier misfires). Options 1 & 3 require it; 2 & 4 preserve it.
4. **Appetite for the one-time migration of styler's live `spec_v15.md` now vs. later?** Opt 1/3 rewrite all active-task provenance + decision cross-refs; Opt 2 is a low-cost derive.
5. **Should the finer-fingerprinting companion (split on `### `) ship independently** of the architecture decision? Cheap + orthogonal, but adds one-time churn to existing `section_fingerprint` values.
6. **Does `/shakedown`'s capability-boundary corpus relieve spec-growth pressure** (FB-095's open question re FB-093)? If the dated shakedown corpus increasingly carries the "where the system is" duty, some spec sections may not need to grow — favoring the lighter Option 2/4.
