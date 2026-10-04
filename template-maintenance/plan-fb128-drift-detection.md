# Plan: FB-128 — detected spec drift reaches the user

**Status:** IMPLEMENTED in v5.9.0 (2026-10-04); see ship-log. The build contract below was amended (A1–A7) and then superseded where the "Review fixes" section at the end differs. Originally APPROVED 2026-10-04: all eight design decisions as recommended (script check every `/work`, META fast path removed; `[V]` and `[K]`; no defer-all; unresolvable Finished headings counted only; live drift on dashboard, `/status` and Needs-you; v5.9.0 via three parallel agents + reviewer). Decision 6 → provenance coverage filed as **FB-135**, not built here.
**Target:** v5.9.0 (minor: new script mode, new reconciliation options, `/work` Step 1 behaviour change).
**Scope:** FB-128 (a)–(c), plus the two items the 2026-10-03 triage bundled with it: FB-115's fingerprint-blindness note and FB-117's decision-gated tasks in Step 1d.
**Line numbers** are at v5.8.0 (`eab22eb`).

## Why the sketched fixes change

FB-128's fix sketch offered two options for (a). This plan takes the first one (a task-provenance check) without a cache:

- **`/iterate`-written marker (the FB-106 pattern):** misses every spec edit made outside `/iterate`. DEC-016 gates direct edits with an ask prompt but allows them, and users also edit in an editor.
- **Task-provenance fingerprint stamped in META:** once you define it, computing that fingerprint *is* the per-task section comparison. A cached copy in META only adds a second thing that can go stale, and keeping the full-spec `spec_fingerprint` current would mean rewriting every unaffected task file after each edit (styler: 313 files).

So the check is computed fresh on every `/work` by a script. It costs milliseconds (hash ~60 sections and read ~300 task files).

## Survey: what upgrading will surface (2026-10-04, read-only)

Script: per-task `section_fingerprint` vs. the current hash of its `## ` section. Absorbed and Broken Down tasks are skipped, as are Finished tasks from an older spec version (historical by design, per Task Migration).

| Project | Drifted now (sections / tasks) | Status of drifted tasks | No section fingerprint |
|---|---|---|---|
| difficult-conversation-simplifier | 6 / 17 | 17 Finished | 0 |
| nordgrid-data-engineering | 6 / 27 | 25 Finished, 2 Pending | 0 |
| escalation_map_training | 2 / 6 | 1 Finished, 5 Pending | 0 |
| flirty-gym (spec_v4) | 1 / 6 | 6 Finished | 0 |
| tinder-streamliner-cc (spec_v8) | 1 / 4 | 3 Finished, 1 Pending | 0 |
| conversation_opener | 1 / 1 | 1 Pending | 1 |
| styler (spec_v15) | 0 / 0 of 105 checkable | (fingerprints hand-maintained) | 20 |
| LTP | 0 / 0 | — | 0 |
| PortfolioWebsite | 1 / 1 checkable | 1 Finished | **74 of 75** |
| OEMMatInsightBI | 0 checkable | — | **19 of 20** |

Consequences:
1. Fixing (a) alone would greet five projects with an Apply-only prompt that resets verified work. Two of them (6 drifted sections each) would exceed the 3-section deferral budget if the user tried to defer. So (a) ships only with (c) and a batch prompt.
2. Nine Pending tasks in five projects sit in sections that changed after the tasks were written. That is the case most worth catching, since an agent would build against a stale task description.
3. styler has 47 current-version tasks whose `spec_section` is not a current heading: 45 are Finished, most are free-form values (`§ 52.1 (…) + § 52.6 (…)`), and one heading differs only by a trailing space. Prompting on these every session would be noise.
4. PortfolioWebsite and OEMMatInsightBI barely record section provenance (tasks were created outside decomposition), so no drift check can see their edits. That is a coverage problem, separate from this item (decision 6).

## Part 1 — a deterministic drift check (fixes a)

New mode: `python3 .claude/scripts/fingerprint.py --drift .claude` → JSON on stdout. It is read-only, exits 0 on success and 2 on a usage or runtime error. A shared function `compute_drift(claude_dir) -> dict` lives in `fingerprint.py`, and the renderer reuses it.

**Rules** (the prose fallback in `drift-reconciliation.md` states the same rules; this is a dual location):
1. Candidates: `.claude/tasks/task-*.json` (not `archive/`). Skip `Absorbed` and `Broken Down`, because subtasks carry the provenance (`/breakdown` copies it). Unparseable files are skipped and listed in `unreadable`.
2. Current spec: the single `spec_v{N}.md`, with the highest N if there are several.
3. **Historical:** skip a Finished task whose `spec_version` is set and differs from the current stem, since Task Migration leaves its provenance unchanged by design. A non-Finished task on an older version goes in `unmigrated` (the existing version-transition path handles it). A missing `spec_version` counts as current.
4. **No provenance:** a task with no `section_fingerprint` is counted in `no_provenance` and never flagged. Today's prose says such tasks "fall back to full-spec comparison", which would flag every one of them on every edit. It only stayed quiet because the META fast path masked it. The fallback sentence goes.
5. **Heading match:** compare `spec_section.strip()` with each current `## ` heading line `.strip()`. If nothing matches, also try `"## " + spec_section.strip()`.
6. **Matched and the fingerprint differs → drifted.** Group by section. When the task carries `spec_subsection` + `subsection_fingerprint` and that `### ` hash is unchanged, mark the task `subsection_unchanged: true` (DEC-021 narrowing: shown as "likely unaffected", never dropped).
7. **Not matched:** a non-Finished task goes in `missing` (the section was renamed or deleted, and the existing `[D]`/`[O]`/`[R]` flow handles it). A Finished task only adds to the `unmatched` count, because the work shipped and the provenance is historical or free-form, so `/work` doesn't prompt about it.
8. **Deferrals:** a drifted section listed in `drift-deferrals.json` is marked `deferred: true`. If the deferral entry lists `affected_tasks`, only those tasks count as deferred.

**Output:**
```json
{
  "spec": "spec_v3",
  "spec_fingerprint": "sha256:…",
  "drifted": [
    {"section": "## Auth", "fingerprint": "sha256:…", "deferred": false,
     "tasks": [{"id": "12", "title": "…", "status": "Finished", "owner": "claude",
                "subsection_unchanged": false}]}
  ],
  "missing": [{"section": "## Old name", "tasks": [{"id": "…", "title": "…", "status": "Pending", "owner": "claude"}]}],
  "unmigrated": ["31"],
  "unmatched": 45,
  "no_provenance": 20,
  "unreadable": []
}
```
"Unreconciled drift" means any `drifted` entry with `deferred: false`, or any `missing` entry.

**`/work` Step 1 changes:**
- **Remove the META fast path** (`work.md:207`). Steps 1a and 1b each come down to one script call, so they run on every `/work`. Keep "always check `drift-deferrals.json`" (budget and expiry).
- **Step 1a freshness** adds a trigger: regenerate when META `spec_fingerprint` ≠ the current spec hash. That field now means "the spec this dashboard was rendered from" and is documented as **not** evidence that drift was checked. The FB-106 `pending_decomposition[]` check stays first: a new section has no task that could drift.
- **Step 1b** runs `--drift`. If the script can't run, the prose rules above apply, which costs a read of every task JSON. The spec-index refresh moves along with it.
- **Tier-1 regen trigger** added in `rules/dashboard.md` and `dashboard-regeneration.md`: after a drift reconciliation is applied, because `task_hash` doesn't include fingerprints.

## Part 2 — detected drift reaches the user (fixes b)

- **New order:** 1b detect → 1c summary → **Drift Reconciliation** → 1d. Step 1d gains a precondition: no unreconciled drift. Reconciliation can create actionable work (reset or re-verify), so Step 1d is evaluated after it.
- **FB-117 clause in Step 1d:** a task with any unresolved entry in `decision_dependencies` counts as non-actionable, the same as Blocked. The fast-exit output lists it under "Waiting on decisions:" with `/research {DEC-ID}`. This matches Step 2c, which already excludes such tasks from batches.
- **Renderer** (`dashboard-render.py`): reuse `compute_drift()`, loaded by path (`importlib`, sibling file). If it can't load, the footer says "drift unchecked" and nothing breaks.
  - Footer: "spec aligned" only when unreconciled drift = 0, deferrals = 0 and debt = 0. Otherwise: "⚠️ N spec sections changed since their tasks were built · M drift deferrals · K verification debt".
  - Needs-you → Spec Drift: one row per unreconciled section ("`## Auth` changed since 3 Finished, 1 Pending task(s) were built → run `/work` to reconcile"), kept beside the existing deferral row.
  - META gains `drift_sections: N`.
- **`/status`:** the "✓ Spec aligned" line (`status.md:183-187`) uses the same check instead of counting deferrals only.

## Part 3 — keep verification (fixes c)

**Per-section options** (`drift-reconciliation.md § Granular Reconciliation UI`):

| Option | Fingerprints | Finished tasks | Other tasks |
|---|---|---|---|
| `[A]` Apply | refreshed | reset to Pending; `task_verification` + `user_review_pending` cleared (unchanged behaviour) | task text updated to the new section if needed |
| `[V]` Re-verify **(new)** | refreshed | → Awaiting Verification; verify-agent checks the shipped work against the current text (pass → Finished; fail → the normal fail path). Human-owned tasks get `user_review_pending: true` instead. | as `[K]` |
| `[K]` Keep **(new)** | refreshed | status, `task_verification`, `user_review_pending` untouched | untouched |
| `[R]` Review individually | per task, with `[A]`/`[V]`/`[K]`/`[E]`/`[S]`/`[O]` | | |
| `[S]` Skip | unchanged; deferral recorded (budget applies) | | |

- `[V]` and `[K]` append a note: `[DRIFT RE-VERIFY {date}] {section} changed; re-verifying against the current text` or `[DRIFT KEPT {date}] {section} changed; user kept verification: {one-line reason}`.
- **Claude recommends one option per section** from the diff: status/annotation/typo-only → `[K]`; acceptance text changed but the shipped work may already match → `[V]`; requirements changed → `[A]`. The user always picks; nothing applies by default.
- **Batch prompt** when 2+ sections are unreconciled: list each with task counts by status, then `[E] Go through each section` | `[K] Keep all`. There is no "defer all", because two surveyed projects would exceed the deferral budget.
- **Invariant** (`drift-reconciliation.md:291`) becomes: "no Finished task carries a verification result computed against a different section text than its current fingerprints, unless the user chose `[K]`, which its notes record."
- Diffs still come from `section_snapshot_ref` (the decomposition snapshot), so after a `[K]` later diffs show changes since decomposition, not since the keep. Stated, not fixed.

## Part 4 — bundled

- **FB-115 incident 2** (`drift-reconciliation.md`, new short subsection): fingerprints detect *change*, not *wrongness*. A section can be fingerprint-current and still misdescribe shipped work if it was wrong when written (PortfolioWebsite 09-19-0210: eight days, four cleanup passes). Closure sweeps (verify-agent T2c item 4) and `/audit-coherence` are the instruments for that.
- **`/iterate`**, one line beside the FB-106 post-apply step: edits to existing sections need no marker, because `/work`'s drift check detects them.

## Files (blast radius)

| File | Change |
|---|---|
| `.claude/scripts/fingerprint.py` + `tests/test_fingerprint.py` | `--drift` mode + `compute_drift()`; tests per rule 1–8 |
| `.claude/scripts/dashboard-render.py` + `tests/test_dashboard_render*.py` | load `compute_drift()` by path; footer; Needs-you rows; META `drift_sections` |
| `.claude/scripts/README.md` | `fingerprint.py` row mentions `--drift`; the renderer → fingerprint dependency |
| `.claude/commands/work.md` | Step 1 fast path removed; 1a trigger; 1b; reconciliation moved before 1d; 1d precondition + decision clause; options list; pause note (`:683`) |
| `.claude/support/reference/drift-reconciliation.md` | detection rules (script-first); options table, batch prompt, invariant; FB-115 note; drop the full-spec fallback sentence |
| `.claude/support/reference/dashboard-regeneration.md` | META example (`:241`); Needs-you derivation; Tier-1 trigger |
| `.claude/rules/dashboard.md` | Tier-1 trigger list |
| `.claude/commands/status.md` | drift line |
| `.claude/commands/iterate.md` | one line |
| `tests/scenarios/` | update the drift scenario(s); add masked-drift-after-regen + batch keep |
| `template-maintenance/architecture-map.md` | renderer → `fingerprint.py` edge (map otherwise stays FB-112(a)) |

**Build split** (disjoint files; agents edit scratch mirrors): (1) both scripts + their tests + scripts README; (2) `work.md`, `drift-reconciliation.md`, `iterate.md`, `status.md`; (3) `dashboard-regeneration.md`, `rules/dashboard.md`, scenarios. Then the independent reviewer over `git diff`, fixes, re-verify.

## Not in this release

- **Provenance coverage** (PortfolioWebsite 74/75, OEMMatInsightBI 19/20 tasks without a section fingerprint): needs a rule for every task-creation path (fix tasks, ad hoc tasks; `/breakdown` already copies) plus a one-time baseline. Filed as FB-135.
- **`/iterate` recording the disposition at apply time** (ask once when the user approves the edit, and `/work` applies it without asking again): defer until `[K]` prompts prove noisy.
- **Phase-level `verification-result.json`** is still invalidated by any full-spec change (FB-117 B3); `[K]` doesn't cover it.
- **FB-122** (`work-state.py`): this adds one deterministic check, not the routing script.

## Build contract (pinned; every agent codes and documents against this text)

**CLI and function.** `python3 .claude/scripts/fingerprint.py --drift .claude` (the argument is the `.claude` directory, like `--dashboard-rollup DIR`). Library function in `fingerprint.py`: `compute_drift(claude_dir: Path) -> dict`. Exit 0 on success (including "no spec" and "no tasks"); exit 2 when the directory doesn't exist or on a usage error.

**Output** (keys always present; lists sorted by section heading, tasks by natural id order, so output is deterministic):
```json
{
  "spec": "spec_v3",
  "spec_fingerprint": "sha256:…",
  "checked": 42,
  "drifted": [
    {"section": "## Auth", "fingerprint": "sha256:<current section hash>", "deferred": false,
     "tasks": [{"id": "12", "title": "…", "status": "Finished", "owner": "claude",
                "deferred": false, "subsection_unchanged": false}]}
  ],
  "missing": [{"section": "## Old name",
               "tasks": [{"id": "31", "title": "…", "status": "Pending", "owner": "claude"}]}],
  "unmigrated": ["7"],
  "historical": 33,
  "unmatched": 45,
  "no_provenance": 20,
  "unreadable": ["task-9.json"],
  "unreconciled_sections": 1
}
```
No spec file → `spec` and `spec_fingerprint` are `null`, every list empty, every count 0. Several spec files → use the highest N (numeric), as the renderer's `load_spec` does.

**Per-task rule order** (first match wins). Candidates are `.claude/tasks/task-*.json` (non-recursive, so `archive/` is excluded). A file that fails to parse, or whose JSON is not an object, goes in `unreadable` (file name).
1. `status` is `Absorbed` or `Broken Down` → skip; not counted anywhere.
2. `spec_version` is a non-empty string ≠ the current spec stem → `Finished`: `historical += 1`; any other status: append id to `unmigrated`.
3. `spec_section` or `section_fingerprint` is missing/empty → `no_provenance += 1`.
4. Heading match: `s = spec_section.strip()`; it matches a current `## ` heading line `h` when `h.strip() == s`, or else when `h.strip() == "## " + s`. No match → `Finished`: `unmatched += 1`; any other status: add to `missing` under section `s`.
5. Matched → `checked += 1`. Equal to the current section hash → in sync, nothing reported.
6. Different → add to `drifted` under the matched heading (`h.strip()`). `subsection_unchanged` is true only when the task has non-empty `spec_subsection` and `subsection_fingerprint`, and the current `### ` hash for `spec_subsection.strip()` exists and equals `subsection_fingerprint`.

**Deferrals.** `.claude/drift-deferrals.json` may be `{"deferrals": [...]}` or a bare list; ignore anything else and any entry that isn't an object with a string `section`. An entry matches a drifted section when `entry.section.strip()` equals the heading, or `"## " + entry.section.strip()` does. If the entry has a non-empty `affected_tasks` list, only drifted tasks whose `str(id)` is in it are `deferred: true`; otherwise every drifted task in that section is. A section's `deferred` is true when all of its drifted tasks are deferred. Missing sections are never deferred.

**`unreconciled_sections`** = drifted sections with at least one non-deferred task + missing sections. "Unreconciled drift" everywhere in the docs means this number is above 0.

**Renderer** (`dashboard-render.py`): load `compute_drift` from the sibling file by path (`importlib.util.spec_from_file_location`). If loading or the call fails, the drift state is *unchecked* and nothing else breaks.
- META: add `drift_sections: {unreconciled_sections}` right after `drift_deferrals:` (`drift_sections: unchecked` when unchecked). `spec_fingerprint` stays as is.
- Footer indicator, three cases (`d` = deferral count, `k` = verification debt, `u` = `unreconciled_sections`):
  - unchecked: `drift unchecked · {d} drift deferrals, {k} verification debt`
  - `u == 0 and d == 0 and k == 0`: `spec aligned · 0 drift deferrals, 0 verification debt` (the existing string, unchanged)
  - otherwise: `⚠️ {u} changed spec section(s), {d} drift deferrals, {k} verification debt`
- The pulse "drift" big number = `u + d` (just `d` when unchecked); bad colour when > 0.
- Needs-you → "Spec Drift" subsection, shown when `u > 0` or `d > 0`. One row per unreconciled section, drifted first then missing, before the existing deferral row (which is unchanged):
  - drifted: `<code>{section}</code> changed since its tasks were built ({counts}) → run <code>/work</code> to reconcile`, where `{counts}` lists the non-deferred tasks by status in the order Finished, In Progress, Awaiting Verification, Pending, Blocked, On Hold, e.g. `3 Finished, 1 Pending`
  - missing: `<code>{section}</code> is no longer in the spec ({n} open task(s) reference it) → run <code>/work</code> to reconcile`

**Reconciliation options** (`drift-reconciliation.md` holds the full text; `work.md` summarises):
```
Section "## Auth" changed — 3 Finished, 1 Pending task(s).
  {diff, or the current section text when no snapshot exists}
  Recommended: [K] — {one-line reason from the diff}
  [A] Apply — reset Finished tasks to Pending (rebuild + re-verify)
  [V] Re-verify — check the shipped work against the new text, no rebuild
  [K] Keep — the edit doesn't change what was built; keep verification
  [R] Review individually | [S] Skip (defer)
```
- Every choice except `[S]` refreshes `spec_fingerprint`, `section_fingerprint` and, when present, `subsection_fingerprint` to current values.
- `[A]`: unchanged behaviour (Finished → Pending; clear `task_verification` + `user_review_pending`; existing note).
- `[V]`: Finished tasks not owned by `human` → `Awaiting Verification`, clear `task_verification` (`verification_history` stays), dispatch verify-agent with "re-verification after a spec edit; the implementation is unchanged; check it against the current section text". Finished `owner: human` tasks stay Finished with `user_review_pending: true`. Non-Finished tasks: same as `[K]`. Note: `[DRIFT RE-VERIFY {YYYY-MM-DD}] {section} changed; re-verifying against the current text`.
- `[K]`: no status or verification change. Note on every task in the section: `[DRIFT KEPT {YYYY-MM-DD}] {section} changed; user kept verification: {one-line reason}`.
- Per-task review (`[R]`): `[A]` Apply, `[V]` Re-verify, `[K]` Keep, `[E]` Edit, `[S]` Skip, `[O]` Mark out-of-spec.
- Claude recommends one option per section (status/annotation/typo-only → `[K]`; acceptance text changed but the shipped work may already match → `[V]`; requirements changed → `[A]`) and never applies one without the user's pick.
- **Batch prompt** when 2+ drifted sections are unreconciled (missing sections are never in the batch; they always go through `[D]`/`[O]`/`[R]` per task):
```
{N} spec sections changed since their tasks were built:
  ## Auth — 3 Finished, 1 Pending
  ## Billing — 2 Finished
[E] Go through each section | [K] Keep all (the edits don't change what was built)
```
- After any reconciliation that changed a task file: regenerate the dashboard (Tier-1 trigger name: **drift reconciliation applied**), since `task_hash` doesn't include fingerprints.

**Step 1d.** New precondition: `- No unreconciled spec drift (Drift Reconciliation, which now runs before Step 1d, leaves unreconciled_sections at 0)`. New non-actionable clause: a task with an unresolved decision dependency (a `decision_dependencies` entry whose record is missing or has status `draft`/`proposed`). Fast-exit output heading for these: `Waiting on decisions:` with one line per task, `- Task {id}: "{title}" — waiting on {DEC-ID} → /research {DEC-ID}`.

**`/status`.** "✓ Spec aligned" only when `unreconciled_sections == 0` and there are no deferrals; otherwise `⚠️ {u} changed spec section(s)` and/or `⚠️ {d} drift deferral(s)`. Source: `fingerprint.py --drift .claude` plus `drift-deferrals.json`.

**Pinned one-liners.**
- `/iterate`, beside the FB-106 post-apply marker: `**Edited existing sections need no marker (FB-128):** /work's drift check (fingerprint.py --drift) compares every task's section fingerprint with the current spec on each run, so an edit to a section that already has tasks surfaces at the next /work whatever dashboard regens happen in between.`
- `drift-reconciliation.md` FB-115 subsection heading: `### What fingerprints can't see (FB-115)`.

### Contract amendments (2026-10-04, after the script agent's real-data run)

**A1. Subsection-level provenance.** Some projects stamp `spec_section` with a `### ` heading and `section_fingerprint` with that subsection's hash (styler: 21 live tasks; for tasks 843 and 861 the stored fingerprint equals the current `### ` hash). Under the original rule 4 they were wrongly reported as "no longer in the spec". Rule 4 becomes:
4. Heading match, `s = spec_section.strip()`:
   (a) `s` matches a current `## ` heading line `h` when `h.strip() == s`, or else when `h.strip() == "## " + s`;
   (b) if no `## ` heading matches and `s` starts with `### `, `s` matches when **exactly one** current `### ` heading line has `.strip() == s`. Compare `section_fingerprint` with that subsection's hash, and report drift under the `### ` heading. `subsection_unchanged` stays false for these tasks;
   (c) no match, or several `### ` matches → the no-match branch (Finished: `unmatched`; any other status: `missing`).

**A2. `spec_version` normalisation.** `spec_version` names the current spec when, after `.strip()`, it equals the current stem (`spec_v3`), its bare number (`3`) or `v3`. OEMMatInsightBI writes `"1"`. Anything else goes to rule 2.

**A3. Scoped subsection lookup.** For rule 6's `subsection_unchanged`, the task's `spec_subsection` is looked up under its matched `## ` section only, so a repeated `### ` heading elsewhere in the spec doesn't count. This is how the script already behaves.

**A4. Regen after any reconciliation write.** The Tier-1 trigger "drift reconciliation applied" fires after any reconciliation choice that wrote a task file **or `drift-deferrals.json`**. An `[S]`-only pass writes just the deferral file, and the Spec Drift rows would otherwise stay stale.

**A5. Phase-level Reconciliation Gate.** Before phase-level verification, the gate (`work.md` § Reconciliation Gate) also requires `unreconciled_sections == 0`. Re-run `--drift` there, because a spec edited mid-session would otherwise slip past it.

**A6. Out-of-spec tasks are skipped.** Rule 1 becomes: `status` is `Absorbed` or `Broken Down`, **or `out_of_spec` is true** → skip; not counted anywhere. An out-of-spec task has no spec section to drift from. So `[O]` (mark out-of-spec) just sets `out_of_spec: true` and keeps the task's provenance fields; it doesn't delete fingerprints.

**A7. One spec hash.** The renderer's META `spec_fingerprint` hashes the spec file's **bytes** (as `--spec` and `compute_drift` do), not decoded text. For a CRLF spec the two differ, which would make Step 1a regenerate on every run.

### Review fixes (2026-10-04, independent review; these supersede the contract text above where they differ)

- **F1 (blocker):** Step 1d first runs Step 2b's checkbox detection, so a decision the user ticked since the last run resolves before the decision clause counts it. (Without this the fast exit skipped Step 2b and the tick was never processed.)
- **F2:** `[A]` and `[V]` set `verification_attempts` to 0 on the Finished tasks they send back; `verification_history` keeps the record. (The counter counts passes too, so a `[V]` fail at 2 would have escalated at once.)
- **F3:** `[V]` sets the optional task field `drift_reverify` (`{"section", "date"}`). Every per-task verify dispatch adds `Re-verification after a spec edit: the implementation is unchanged; check it against the current section text.` while the field is present, including session-recovery re-dispatches and timeout retries. Writing a per-task result, pass or fail, removes it. verify-agent T2b skips its diff-based scope check under that line. Spec files (`.claude/spec_v*.md`, `.index.json`, `previous_specifications/*`) join T2b's infrastructure filter.
- **F4:** under `[A]` and `[V]`, open tasks get their text updated where the new section changes it, with the note `[DRIFT UPDATED {date}] {section} changed; {what changed, or "no task change needed"}`. Batch `[K] Keep all` covers only sections whose drifted tasks are all Finished; others are listed with `(has open tasks — reviewed separately)`, and Keep-all is not offered when every section is marked. Recommendation: editorial → `[K]`; acceptance text changed → `[V]`; requirements changed → `[A]`.
- **F5:** Step 1c keys the version-transition branch on `unmigrated`. Every freshness check (Step 5 item 4, `/status`, `/health-check` check 10) also compares META `spec_fingerprint`. Substantial Change Detection's version option is now `[N] New spec version`. Task Migration re-runs `--drift`. Renderer deferral count ignores unusable entries. Map test count corrected.
