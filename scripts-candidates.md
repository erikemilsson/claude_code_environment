# Scripts Candidates Inventory (FB-011)

**Purpose:** Identify template procedures where a deterministic script would outperform LLM-executed natural-language instructions, propose extraction order, and surface the decisions needed before any script lands.

**Status:** Stage 1 (inventory) — awaiting user review before any Stage 2 extraction.

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

### Family A — Fingerprint / hash computation

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

### Family B — Task JSON validation & health-check checks

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

### Family E — Decision auto-finalization

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

**Recommendation:** **Defer pending trial.** Explicitly hold this one for 30–60 days of observed `/work` + `/iterate` runs. If FB-017 recurs, extract immediately; if not, leave as LLM-executed and save the maintenance burden.

---

## Recommended extraction order

**Tier 1 — extract now** (low risk, high ROI, minimal scope):
1. **Family A** — fingerprinting (A1, A2, A3 as one script)
2. **Family B** — task validation + verification debt (B1, B2 as one script; consider `task-schema.json` alongside)

**Tier 2 — extract after Tier 1 stabilizes** (medium scope or dependency on Tier 1):
3. **Family C** — dashboard regeneration, hybrid (script for structural sections, LLM for synthesis). Start with Tasks-by-phase as proof-of-concept.

**Tier 3 — extract on observed need** (low frequency or overlaps with just-landed fixes):
4. **Family D** — parallel-plan computation. Only if real conflicts surface.
5. **Family E** — decision auto-finalization. Only if FB-017 regresses.

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

Awaiting user review of:
- The candidate list (any missing? any to drop?)
- The tiered extraction order (Tier 1 now? together or separately?)
- The seven open questions above (particularly #1 scope and #6 testing story).

Once decisions are made, Stage 2 proceeds with a per-extraction plan (fresh-session executable), one commit per family.
