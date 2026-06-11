# Scripts Candidates Inventory (FB-011)

**Purpose:** Identify template procedures where a deterministic script would outperform LLM-executed natural-language instructions, propose extraction order, and surface the decisions needed before any script lands.

**Status:** Stage 2 partial — Tier 1 (Families A + B) shipped in `template_version 3.0.0` and bug-fixed in `3.1.1` (FB-039). **Family C trigger declared MET 2026-06-10** (user decision on substituted evidence — see Trigger amendment in the Family C section); PoC authorized. Family D remains deferred per its trigger; Family E dropped 2026-05-20. Last updated: 2026-06-10.

**Scope:** Audit-only. No code written. No files outside this inventory touched.

---

## Criteria for a good candidate

A procedure is a strong script candidate when:

1. **Deterministic mapping.** Same input → same output. No judgment, synthesis, or wording choices.
2. **Failure mode is drift / skipping / error, not poor style.** Script fixes what LLM gets wrong under load; LLM wins on phrasing.
3. **Invoked frequently enough to pay back the maintenance cost.** Per-session or per-command beats once-per-project.
4. **Tokens saved > tokens spent explaining it exists.** Net win matters, not gross win.
5. **No user intent interpretation.** Checkbox detection is fine; "is this decision ready to finalize?" is not.

Procedures that fail these tests (writing action items, summarizing activity, drafting decision rationale, deciding when to break a task down) stay with the LLM.

---

## Constraints that shape extraction

- **Subagents cannot write to `.claude/`** (harness sandbox, DEC-004). Any script that mutates dashboard / task JSON / decision frontmatter / verification-result.json must be invoked by the orchestrator or by the user directly — never from a Task subagent.
- **Subagents do not inherit parent `permissions.allow`.** A subagent invoking a script at `.claude/scripts/foo.sh` will prompt unless the Task spawn passes `--allowedTools "Bash(.claude/scripts/foo.sh *)"`. Orchestrator invocation is cheaper.
- **Bash is allowed but restricted by convention.** `rules/agents.md § "Tool Preferences"` reserves Bash for shell operations; scripts are a legitimate shell operation, but cluttering agent workflows with mandatory Bash steps increases permission prompts. Extraction should reduce prompts, not add them.
- **Scripts must ship with the template.** Home: `.claude/scripts/` (root `scripts/` is template-maintenance-only). `sync-manifest.json § sync` must include `.claude/scripts/*`.
- **Dual-location risk:** every behavior that becomes a script also exists as prose in reference docs (and possibly in a Skill). Maintaining three copies is costly; extraction should decide whether the prose retires or stays as spec-of-record.

---

## Candidate inventory

Nine candidates grouped into five families. Each row: current home, current shape, failure mode, script shape, `.claude/` write (Y/N), tradeoff summary.

### Family A — Fingerprint / hash computation ✅ SHIPPED

**Shipped in `template_version 3.0.0`** (`.claude/scripts/fingerprint.py`). Bug-fixed in `3.1.1` (FB-039: field-name `task_id` → `id`).


| # | What | Current home | Writes `.claude/`? |
|---|------|--------------|--------------------|
| A1 | Spec file fingerprint (SHA-256 of full spec) | `support/reference/drift-reconciliation.md` + provenance fields in task JSON | Indirect (orchestrator writes the hash to task JSON) |
| A2 | Section fingerprint (SHA-256 per `## heading`) | Same | Indirect |
| A3 | Dashboard freshness hash (canonical task-JSON rollup) | `commands/status.md`, `commands/work.md` freshness check, sidecar `dashboard-state.json` | Indirect (freshness hash lives in sidecar) |

**Current shape:** LLM reads the file, normalizes headings / sort order, computes SHA-256 mentally or via ad-hoc Bash. Provenance-field population in task JSON is described as "compute hash; write it" — the compute step is currently Claude's.

**Failure mode:** LLMs are unreliable at cryptographic hashing. Any provenance mismatch caused by wrong normalization defeats drift detection — which is the one feature the hash exists to enable.

**Script shape:** `.claude/scripts/fingerprint.py` (or `.sh` with `shasum`). Flags: `--spec {path}` → one hash; `--sections {path}` → map of heading → hash; `--dashboard-rollup` → canonical task-JSON hash. Read-only; prints to stdout. Orchestrator captures output and writes to task JSON / sidecar.

**Tradeoffs:**
- ✓ Trivial scope (~30 lines). Zero risk. Unlocks reliable drift detection.
- ✓ Reusable from pre-commit hooks, health-check, `/work` drift step.
- ✗ Normalization rules (heading case, whitespace, trailing punctuation) must be frozen in the script AND documented in the reference doc — if they drift apart, old fingerprints become invalid.
- ✗ Migration cost: existing task JSON files may have been populated with LLM-computed hashes that don't match the script's output. One-shot reconciliation needed (re-fingerprint all live tasks on first run).

**Recommendation:** Strong. Do A1+A2+A3 as one script; they share normalization logic.

---

### Family B — Task JSON validation & health-check checks ✅ SHIPPED

**Shipped in `template_version 3.0.0`** (`.claude/scripts/validate-tasks.py`). Bug-fixed in `3.1.1` (FB-039: field-name `task_id` → `id`).


| # | What | Current home | Writes `.claude/`? |
|---|------|--------------|--------------------|
| B1 | Task JSON schema validation (required fields, types, enum values) | `commands/health-check.md` Part 1, `support/reference/task-schema.md` | N (read-only report) |
| B2 | Verification debt count (Finished tasks without `task_verification.result == "pass"`) | `commands/health-check.md` Part 1 § "Verification Debt" | N |

**Current shape:** LLM opens each task JSON, checks required fields, validates boolean types for `cross_phase` / `parallel_safe` / `out_of_spec` etc., reports drift. Scales poorly as task count grows.

**Failure mode:** LLM skips edge cases under load — typical miss is a boolean stored as string (`"true"` vs `true`) or a missing `cross_phase` field after the DEC-006 schema update. One Finished task with broken `task_verification` defeats the structural enforcement invariant.

**Script shape:** `.claude/scripts/validate-tasks.py`. Iterates `.claude/tasks/task-*.json`, uses jsonschema (or minimal type-check without a dep), prints a machine-readable summary + human-readable report. Exit code 0 on clean, 1 on violations. Can run in pre-commit, health-check, or standalone.

**Tradeoffs:**
- ✓ Deterministic; cheap (O(N) with small N).
- ✓ Dual use: pre-commit hook + `/health-check` Part 1.
- ✓ Frees ~200 tokens per `/health-check` run (skip the per-task narration).
- ✗ `task-schema.md` is the source of truth; the script must mirror it. Dual-edit discipline needed.
- ✗ JSON Schema spec would be ideal (a `task-schema.json` file machine-readable from both the script AND the docs), but that's a bigger scope change — move to Stage 3 if pursued.

**Recommendation:** Strong. Do B1+B2 as one script. Consider writing a `task-schema.json` alongside to eliminate the dual-edit risk — but flag as a separate decision (next step).

---

### Family C — Dashboard regeneration

| # | What | Current home | Writes `.claude/`? |
|---|------|--------------|--------------------|
| C1 | Structural sections — Progress (phase breakdown, status summary, timeline), Tasks (by phase), Decisions (log with status) | `support/reference/dashboard-regeneration.md`, `.claude/skills/dashboard-style/SKILL.md`, `rules/dashboard.md` | Y (writes `.claude/dashboard.md`) |
| C2 | Synthesis sections — Action Required, Notes | Same | Y |

**Current shape:** LLM reads the regeneration reference + task JSON + sidecar state, renders ~200–500 lines of markdown with marker pairs, applies Section Display Rules (collapse completed phases, switch to critical-path-only when >15 active nodes, add `(cross-phase)` suffix, etc.). The full procedure is 489 lines of prose in the reference doc.

**Failure mode:** Output variation between regenerations (FB-015 and others). Drift from Section Display Rules. Phantom sub-sections appearing ("Recent Activity", "Work Summary" — the exact shape FB-015 banned). High token cost.

**Script shape (hybrid):**
- **Script** (`.claude/scripts/dashboard-render.py`): reads task JSON + sidecar + existing dashboard (for user-preserved marker blocks). Renders **structural** sections deterministically between MARKER pairs. Emits the skeleton + structural content. Leaves Action Required and Notes as `<!-- CLAUDE: fill this -->` placeholders.
- **LLM** (`/work` orchestrator): after the script runs, fills the synthesis placeholders. Only touches what requires judgment.

**Tradeoffs:**
- ✓ Biggest single token-cost win in the template. Dashboard regen is the most frequent structural procedure.
- ✓ Eliminates FB-015 regressions structurally (phantom sections can't appear because the script doesn't emit them).
- ✗ Largest scope by far. Section Display Rules, critical-path Mermaid generation, phase collapse heuristics all need porting.
- ✗ Maintenance shift: future dashboard tweaks touch the script, not just prose. Every change requires Python edit + doc edit.
- ✗ Skills trial interaction: `skills/dashboard-style/SKILL.md` is the auto-invocation doc. If structural sections move to a script, the Skill shrinks to the synthesis+rules half. Might retire the reference doc (DEC-007 Option B retirement path).
- ✗ Hardest to test; touches the most-visible artifact. Failure is user-facing.

**Recommendation:** Medium — defer until Families A and B land and are stable. Dashboard regen benefits most but is also the highest-risk extraction. Best tackled with a small proof-of-concept on one section (e.g., Tasks-by-phase only) before the full port.

**Trigger (added 2026-05-13 via FB-038 ship):** `commands/health-check.md` Part 6 check 4b detects retrospective summary content leaking into Action Required despite the FB-015 negative rule. If 4b fires repeatedly across `/health-check` runs on the same project (≥2 different projects, OR ≥3 runs on one project), the LLM-emitter approach is structurally unreliable — escalate to Family C extraction. Track via downstream `/health-check` reports once telemetry exists.

**Trigger amendment (2026-06-10, user decision): declared MET on substituted evidence.** The 4b telemetry channel proved structurally unsampled — `/health-check` shows ~7 mentions across the 47-session `interaction-logs/` corpus and is effectively never run in the most active downstream project (styler), so the named sensor cannot fire regardless of emitter reliability. Substituted standard: *recurrent post-fix regressions in shipped dashboard behavior* — the same underlying fact 4b was designed to detect ("the LLM emitter is structurally unreliable"). Satisfied by the patch history: FB-015 → FB-038 (regression five days after the fix) → FB-080 (Tier-1 regen triggers ignored in two projects in one week) → FB-090 (discretion removed outright) + v4.7.2 example drift — five dashboard-discipline ships in ~6 weeks. **Scope authorized: the PoC only** (Tasks-by-phase section, byte-identical re-render test); the full-port decision gates on PoC results. Counterweight noted at decision time: no confirmed regression in the ~2.5 weeks since FB-090 (v4.10.1) — judged insufficient against the treadmill history plus Family C's independent token-cost value leg.

**PoC evidence run (2026-06-11, styler @ 218 active task files — the gating observation for the full-port decision):**

Script ran clean (exit 0, 176 lines, zero stderr). Comparator: styler's LLM-rendered `## 📋 Tasks` section, regenerated 2026-06-10T07:44Z at the SAME `task_count: 218` — so diffs are rendering differences, not state drift. Findings, ordered by port impact:

1. **Archive blindness is the dominant gap.** styler auto-archives Finished tasks; the active dir is only the tail. The LLM render unions active + archive-index ("Phase 1 — 38 tasks finished … Phase 18 — 69 finished", ~45 phases); the script (archive/ excluded by design) renders wrong completed-phase counts ("Phase 4 — ✅ 2 tasks finished" vs 33), omits whole phases, and emits a wrong overall footer ("193/202 complete (96%)"). **A full port requires an archive-index input** — without it the render is wrong at exactly the mature-project scale the port targets.
2. **Phase-name divergence.** The script derives names from active task files → "Phase 18 — /style Surface Polish" vs the LLM/spec's "Schema-Driven Profile IA and Capture Refactor" (Phases 4/11/12/18 all differ). Needs a canonical phase-name source (spec section titles or a registry), not active-file majority vote.
3. **Empty-phase noise.** Phases whose active files are all Absorbed render as orphan tables + "*Phase 11: 0/0 complete (0%)*"; phase-less strays render as "### Phase None". The LLM correctly collapses/omits both. Two display rules to add.
4. **The script catches real LLM rendering errors** — the deterministic-correctness argument observed live: the LLM render DROPPED decision-deps (T809 deps shown "T806, T807, T808, T813" — `DEC-072` missing; T812 "T813" — `DEC-072` missing); the script preserves both. Silent data loss in the shipped artifact, invisible without this diff.
5. **Cosmetic deltas (known PoC simplifications):** T-prefixed ids, ✅/⏳/🤖/👥 icons, judgment-flavored phase banners ("Active build closed 2026-05-28 …"). Banner prose stays LLM-owned under the hybrid split (or drops); icons/prefixes are mechanical.
6. **Adjacent, fold into the port: META `task_hash` three-way mismatch.** styler META `46ec3712…` ≠ documented-algorithm recompute (`id:status:difficulty:owner`, string-sorted) `83f495a4…` ≠ `fingerprint.py --dashboard-rollup` (`id:status`) `078fbc7e…`. Three conventions in the wild; the staleness check can't verdict reliably. The port should make the renderer the single hash authority.

**Read:** byte-determinism holds and correctness already beats the LLM where it matters (finding 4); the real port scope is *inputs* (archive index, canonical phase names) + two display rules — not rendering mechanics. Demand-side evidence: `interaction-logs/insights/2026-06-11_user-experience_dashboard-regen-cost-at-scale.md` (~18 friction notes; prescribed regens structurally bypassed at scale). Decision remains the user's.

**FULL PORT SHIPPED — v4.22.0 (2026-06-11, user decision "go" on the evidence above).** `dashboard-render.py --render` now emits every structural section (META incl. canonical `task_hash`, header lines, toggles, Progress with critical path + Mermaid, archive-aware Tasks, Decisions, Notes preservation, footer); LLM fills `<!-- CLAUDE: fill -->` placeholders for Action Required + Custom Views content. All six evidence findings addressed: (1) archive-index input (full archived task files, index fallback), (2) phase-name union vote across active+archive, (3) absorbed-only/unphased display rules, (4) deterministic deps rendering, (5) cosmetic deltas resolved to golden-example style, (6) `--task-hash` is the single hash authority. Wired via `dashboard-regeneration.md § "Script-First Rendering"`; prose remains the hand-render fallback. 54 tests. Family C CLOSED; ship-log entry v4.22.0 is the durable record.

---

### Family D — Parallel-execution orchestration

| # | What | Current home | Writes `.claude/`? |
|---|------|--------------|--------------------|
| D1 | Eligibility filter (status == Pending, owner != human, deps finished, difficulty < 7, phase <= active OR cross_phase == true) | `support/reference/parallel-execution.md` § Eligibility | N (read-only planning) |
| D2 | File-conflict detection (pairwise `files_affected` overlap via path normalization + containment) | Same, § "File Conflict Detection Algorithm" | N |

**Current shape:** LLM filters eligible tasks per-`/work`-invocation and computes pairwise conflicts among candidates for a parallel batch. Scales with active-task count × pairwise comparisons.

**Failure mode:** Path-normalization edge cases (trailing slash, symlinks, case sensitivity) occasionally produce false negatives — a subtle conflict is missed and two agents collide. Rare in practice because the orchestrator also does pre-dispatch confirmation (FB-036), but the script is cheaper insurance than a re-run.

**Script shape:** `.claude/scripts/parallel-plan.py`. Reads `.claude/tasks/*.json`, filters per eligibility rules, computes conflict matrix, outputs batch proposals as JSON (task IDs + justification). Orchestrator reads, presents to user for Pre-Dispatch Confirmation, dispatches.

**Tradeoffs:**
- ✓ Deterministic. Eliminates a cognitive load on `/work`.
- ✓ Composable with `claude -p` for CI-style batch planning.
- ✗ Dashboard-regen-lite: lots of rules, each touch point must port. `cross_phase` exemption, `max_parallel_tasks`, `dependencies` satisfaction checks.
- ✗ FB-036 Pre-Dispatch Confirmation just landed. The interactive confirmation step is the primary reliability mechanism; a script makes the PLAN deterministic but the DECISION still routes through the user.
- ✗ Unlike A and B, this one is only "strong" if parallel execution is used frequently. Projects running mostly sequential work get little benefit.

**Recommendation:** Medium. Defer until we see real parallel-dispatch patterns in production projects. Revisit if FB-036 confirmations repeatedly flag script-detectable conflicts that the LLM missed.

---

### Family E — Decision auto-finalization (CLOSED 2026-05-20 — dropped)

| # | What | Current home | Writes `.claude/`? |
|---|------|--------------|--------------------|
| E1 | Checkbox detection + normalization (`[x]`, `[X]`, `[✓]`, `[✔]`) across `support/decisions/decision-*.md` | `commands/work.md` Step 2b, `commands/iterate.md` Step 1a, `support/reference/phase-decision-gates.md` | Y (writes decision frontmatter + Decision section) |

**Current shape:** Just inlined into both entry points (FB-017 batch + iterate group). Scans decision files, matches checked boxes, updates frontmatter to `approved` + today's `decided` date, populates Decision section from Option Details.

**Failure mode:** Historical FB-017 bug — Step 2b underspecified the procedure; Claude skipped it under load. Now mitigated by inlining the imperative at both call sites.

**Script shape:** `.claude/scripts/finalize-decisions.sh`. Scan decision files; per checked box, edit frontmatter via `yq` or a Python script; extract option name from the heading; populate Decision section from the matching Option Details block.

**Tradeoffs:**
- ✓ Deterministic fire — can't be skipped under load.
- ✓ Reusable from pre-commit (catches checked-but-not-finalized files before they land).
- ✗ **Regression wait needed.** The inlining fix just landed. Extract only if we observe recurrence; otherwise the fix is complete and the script is redundant maintenance.
- ✗ Writing Decision sections from Option Details requires text transformation (option-name → rationale text blocks). Partially LLM-shaped work. Script can do the mechanics (frontmatter), LLM does the prose.

**Recommendation:** **CLOSED — dropped 2026-05-20 per trial outcome.** No FB-017 regression observed in this template repo or across three downstream projects (echothread, styler, SIREN) during the trial window 2026-04-17 → 2026-05-17. FB-017's inlining fix at `commands/work.md` Step 2b + `commands/iterate.md` is sufficient; script extraction is not needed. The original deferral rationale (hold 30–60 days; extract only if FB-017 recurs) held — no recurrence observed.

**Trial window:** 2026-04-17 to 2026-05-17 (30-day mark). **Outcome:** No FB-017 regression observed. Verified 2026-05-20 across feedback files, git log since 2026-04-17, and 18 cross-project session exports in `interaction-logs/processed/` (echothread / styler / SIREN). The single grep hit in `styler-session-2026-05-16.json` was a false-positive — matched "Step 2b" but referred to a different sub-feature (the inflection-flag post-decision check; captured separately as FB-078, not a FB-017 regression). Family E dropped per criterion; this section preserved for audit-trail purposes.

---

### Family F — Post-batch state-invariant checker (candidate, added 2026-06-10)

| # | What | Current home | Writes `.claude/`? |
|---|------|--------------|--------------------|
| F1 | Post-return / post-batch invariant check: friction markers actually appended when an agent report carried friction kinds (DEC-011 / FB-089 class), task-JSON status transitions legal, expected files exist at the expected moments (handoff + export at pause, `verification-result.json` at phase end), `pending_full_regen` sidecar consistency | `support/reference/work-procedures.md § "State Persistence Protocol"` (the prose the check would verify ran) | N (read-only report) |

**Rationale:** the ship history's recurring root cause is "documented but not executed" (FB-017, FB-045/DEC-011, FB-038). Families A/B validate *artifacts*; Family F validates *that the protocol ran* — converting "did I remember every State Persistence step?" from recall into a checklist diff the orchestrator runs after each batch / before pause. Same shape and invocation contract as `validate-tasks.py`.

**Trigger:** ship if post-v4.18.0 telemetry still shows skipped persistence steps — the work.md split + STOP-read gates (v4.18.0) are the first-line fix; Family F is the mechanized backstop if prose-skipping survives the split. Re-assess alongside the Family C full-port decision.

---

## Recommended extraction order

**Tier 1 — extracted ✅** (low risk, high ROI, minimal scope):
1. **Family A** — fingerprinting (A1, A2, A3 as one script) — shipped in `template_version 3.0.0` (`fingerprint.py`); bug-fixed in `3.1.1`
2. **Family B** — task validation + verification debt (B1, B2 as one script) — shipped in `template_version 3.0.0` (`validate-tasks.py`); bug-fixed in `3.1.1`. `task-schema.json` deferred as separate decision.

**Tier 2 — extract after Tier 1 stabilizes** (medium scope or dependency on Tier 1):
3. **Family C** — dashboard regeneration, hybrid (script for structural sections, LLM for synthesis). Start with Tasks-by-phase as proof-of-concept. **Trigger declared MET 2026-06-10** on substituted evidence (see Trigger amendment in the Family C section); PoC authorized, full port gates on PoC results.

**Tier 3 — extract on observed need** (low frequency or overlaps with just-landed fixes):
4. **Family D** — parallel-plan computation. Only if real conflicts surface in downstream parallel-batch sessions.
5. **Family E** — decision auto-finalization. **CLOSED 2026-05-20 — dropped** (no FB-017 regression during trial window 2026-04-17 → 2026-05-17).

---

## Home and wiring

Scripts home: `.claude/scripts/`
Recommended file layout:

```
.claude/scripts/
├── README.md              # Invocation contract, dependencies, version, output format
├── fingerprint.py         # Family A
├── validate-tasks.py      # Family B
└── (future) dashboard-render.py
```

**Sync manifest:** Add `.claude/scripts/**` to `sync-manifest.json § sync`.

**Dependencies to avoid:**
- Python stdlib only (no `pip install` required) — `hashlib`, `json`, `pathlib`, `re`, `argparse`.
- If `jsonschema` is needed for B1: ship a minimal type-check without the dep, or add an optional `requirements.txt` and document a `pip install -r .claude/scripts/requirements.txt` step in setup-checklist.
- Avoid bash-only scripts for anything over ~20 lines — Python is more maintainable and its test story is better.

**Invocation contract (for all scripts):**
- Read-only by default. Anything that writes to `.claude/` must be orchestrator-invoked, documented, and opt-in.
- Stdout: machine-parseable (JSON or newline-delimited records).
- Stderr: human-readable diagnostics.
- Exit code: 0 on success, 1 on validation failure, 2 on runtime error.
- `--help` flag shows invocation shape and sample output.

**Call-site updates** (not Stage 1 work; list for Stage 2 planning):
- Family A: `commands/work.md` Step 1b (drift detection), `commands/health-check.md` Part 2 (drift), decomposition provenance field writes in `support/reference/decomposition.md`.
- Family B: `commands/health-check.md` Part 1, `.git/hooks/pre-commit` (optional).
- Family C: `commands/work.md` regen trigger, `rules/dashboard.md § "Regeneration Strategy"`, skill file `skills/dashboard-style/SKILL.md` + reference doc (retirement or hybridization).

---

## Open questions for user review

1. **Scope of Stage 2 first extraction.** Families A + B together, or one at a time? A+B bundled is a single PR with fingerprinting + validation; the file-grouping rule would argue for bundling since both touch health-check wiring.
2. **`task-schema.json` alongside B1?** Adds a canonical machine-readable schema, eliminates dual-edit drift, but doubles the initial scope. Reasonable Stage 2 decision — flag for later.
3. **Python-only vs mixed bash/Python.** Defaulting to Python for everything > 20 lines. Fingerprinting is trivially a shell one-liner (`shasum`), but keeping the same language across scripts simplifies testing. Worth a quick call.
4. **Skill-trial interaction (Family C).** If dashboard regeneration goes hybrid-with-script, does `skills/dashboard-style/SKILL.md` shrink to just the synthesis/rules layer? Does `dashboard-regeneration.md` retire? Relates to DEC-007 Option B retirement path.
5. **`rules/agents.md` Bash exception wording.** The current wording reserves Bash for "operations requiring shell execution." Explicit allow-list for `.claude/scripts/*` would make the extraction cleaner. Minor edit; flag for Stage 2.
6. **Testing story.** No test harness exists yet for scripts. Worth setting up `.claude/scripts/tests/` with a minimal runner (`python -m unittest discover`) as part of first extraction, or defer until Family C (where the test payoff is higher)?
7. **Defer E or drop it?** Decision auto-finalization is already mitigated by inlining. Trial window could be ~30 days post this inventory; if no regression, we can drop the candidate entirely rather than keeping it on the "later" list forever.

---

## What this inventory does NOT cover

- **`claude -p` one-liner candidates** — automation.md already covers the pattern; this inventory is about deterministic scripts. Ad-hoc queries ("summarize git log", "diff against upstream", "render a report from task JSON for an email") are `claude -p` territory and not re-litigated here.
- **Template maintenance scripts** (pre-commit hook, `scripts/pre-commit-hook.sh`) — those live at the root, don't ship, and already exist as scripts.
- **Test infrastructure** (tests/scenarios) — separate concern; not procedure extraction.
- **Spec-auditor subagent** (FB-033) — different shape (subagent, not script); gated on FB-032 trial data.

---

## Next action

**Tier 1 complete.** Families A + B shipped in `template_version 3.0.0`, bug-fixed in `3.1.1` (FB-039).

**Tier 2 (Family C) — PoC SHIPPED v4.19.0 (2026-06-10).** `.claude/scripts/dashboard-render.py --tasks-section` renders the Tasks-by-phase section deterministically (phase grouping/sort, completed-phase collapse, >10-finished summarization, blocked-phase collapse with deterministic blocker summary, all per-task status displays, per-phase + overall footers). 13 tests incl. the byte-identical re-render gate (`tests/test_dashboard_render.py`); 25/25 suite green. NOT yet wired into the regen flow — advisory per scripts README. **Next: the full-port decision** — script renders all structural sections between marker pairs, LLM keeps synthesis (Action Required, Notes); decide after observing PoC output against a real project's dashboard (run it in styler and diff against the LLM-rendered Tasks section). Known PoC simplification: per-phase qualifier lines are deterministic count enumerations, not the example's judgment-flavored phrasing — acceptable for structural sections, revisit at full port.

**Tier 3 (Families D + E) — observed-need gates.**
- Family D: trigger if real parallel-batch conflicts surface that the LLM missed (low frequency expected; FB-036 Pre-Dispatch Confirmation reduces this risk).
- Family E: **CLOSED 2026-05-20** — dropped per trial outcome. No FB-017 regression observed in this template repo or downstream during 2026-04-17 → 2026-05-17.

**Remaining open questions** (from "Open questions for user review" above):
- #2 `task-schema.json` alongside Family B — still open. Could land as a separate Stage 2 extension.
- #4 Skill-trial interaction (Family C) — defers with Family C trigger.
- ~~#5 `rules/agents.md` Bash exception wording — still open, low priority.~~ ✅ Closed 2026-05-13 in v3.5.1: added `Bash(python3 .claude/scripts/*.py:*)` to template-owned `settings.json` (9 entries total) + reference in `rules/agents.md` § Tool Preferences scripts paragraph.
- ~~#6 Testing story — still open; would land with Family C if extracted.~~ ✅ Closed 2026-05-13 in v3.5.1: minimal CLI-level test harness at `.claude/scripts/tests/` (12 tests, all passing). Run with `python3 -m unittest discover .claude/scripts/tests/`. Tests include explicit FB-039 regression coverage. Comprehensive coverage for Family C can be added when/if extracted.
