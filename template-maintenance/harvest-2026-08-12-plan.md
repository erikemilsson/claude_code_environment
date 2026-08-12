# Harvest plan — 2026-08-12 inbox (56 exports)

**Status:** clusters 1, 2, 5 DONE this session (2026-08-12); clusters 3 and 4+6 remain.
**Created:** 2026-08-12 (template-repo `/health-check` + 4-agent impact assessment)
**Supersedes nothing.** Sibling precedent: `harvest-2026-07-19-triage.md` (38 exports).

### Session 1 result (2026-08-12)

- **Cluster 1 → FB-113** (unqualified `ready`). Insight: `interaction-logs/insights/2026-08-12_implement-agent_files-affected-derivation.md` — extends the 2026-06-11 predecessor (trigger met). 9 incidents.
- **Cluster 2 → FB-114** (unqualified `ready`). Insight: `interaction-logs/insights/2026-08-12_agents_negative-findings-positive-control-defeated.md`. 9 core incidents (the 07-31 dotfile held two markers, so 9 not 8) + 2 same-class + 1 success. Sub-issue 2 (Grep absent from subagents) flagged upstream-gated.
- **Cluster 5 → FB-115** (ready, single-project caveat). Insight: `interaction-logs/insights/2026-08-12_verify-agent_closure-sweep-lexical-vs-structural.md`. 5 incidents; incident 5 (task-062) cross-references FB-114 Adjacent B.
- **FB-076 NOT touched** (correction belongs with cluster 3, per plan).
- **Moved to `processed/` (5 files, copy→cmp→rm verified):** 07-27-0830, 07-28-0257, 08-01-0336, 08-01-1345, 08-05-2354. Only files whose dates are fully harvested (no overlap with unfinished cluster 3/4+6 dates) were moved. Files on shared dates (07-23, 07-30, 07-31, 08-10, 08-11) remain in `inbox/` for the next session — they contain finished-cluster evidence but also sit on dates claimed by clusters 3/4+6.
- **Remaining for next session:** cluster 3 (verify-agent runtime_validation → insight doc + **sibling FB** extending FB-076, per the correction section; do NOT unlock mitigations 2/3) and cluster 4+6 merged (task/AC authoring → one insight doc + one FB with single-project caveat). Next free FB ID: **FB-116**.

This plan exists because the cluster analysis below cost a full `/health-check` run plus four
parallel assessment agents, and it lived only in a conversation. Everything needed to execute
the harvest is here — a cold session should not need to re-derive any of it.

---

## Inbox state at plan time

- **56 `.json` files** in `interaction-logs/inbox/`, **7 dot-prefixed (hidden)**.
- Enumerate with `find interaction-logs/inbox -maxdepth 1 -type f -name '*.json'` — a bare
  `*.json` glob returns only 49. (`/health-check` Part 7 step 1 was fixed for this in v5.4.3;
  the producer-side root cause is open as **FB-109**, so new dot-files will keep arriving.)
- Provenance: 52 OEMMatInsightBI, 2 styler, 1 flirty-gym, 1 tinder-streamliner-cc.
- Payload: **159 automated markers** (142 unique signatures), 80 design-pushback entries,
  140 workflow-friction notes. **79 markers carry `template_area`** = template-relevant;
  the rest are project-level drift and are not harvest material.

### Duplicate-marker methodology (do not miscount)

17 markers are byte-identical across exports. These are **not** pipeline bugs and **not**
duplicate sessions — the export pipeline re-emits *open* markers every session until the
underlying gap ships a fix. Verified: the 08-06 and 08-10 exports have different
`session_metrics` and are genuinely distinct sessions.

**Rule:** count a re-emitted marker as **one** incident. Do not treat re-emission as
corroboration, and do not treat it as noise to discard.

---

## ID allocation

Next free feedback ID is **FB-113**. (FB-109/110/111 shipped or captured 2026-08-12;
FB-112 is the doc-hygiene trio captured the same day.) Before assigning, re-scan all four
files by exact filename — `template-maintenance/feedback.md`,
`template-maintenance/feedback-archive.md`, `.claude/support/feedback/feedback.md`,
`.claude/support/feedback/archive.md`. The maintenance archive is `feedback-archive.md`,
**not** `archive.md`; probing the wrong name silently reports "does not exist" and has
caused real duplicate captures (FB-062).

`FB-162` / `FB-174` / `FB-192` appearing in those files are **downstream-project** IDs
quoted in `Source:` lines. They do not belong to this namespace.

---

## Deliverables

**5 insight docs** (not 6 — clusters 4 and 6 merge) in `interaction-logs/insights/`,
named `YYYY-MM-DD_{template-area}_{slug}.md`.

**4 new FB items** in `template-maintenance/feedback.md`, starting FB-113.

**1 FB-076 amendment** — see the correction section; this one is easy to get wrong.

**File move** to `interaction-logs/processed/` — last, and conditional. See sequencing.

---

## Cluster 1 — `files_affected` derivation → insight doc + FB

**Evidence:** 10 raw / **9 unique**. Dates 07-23, 07-27 ×2, 07-28, 07-30, 07-31, 08-01 ×2, 08-11.
All OEMMatInsightBI.

**Shape.** `files_affected` under-counts the real change surface, in a *new* domain:
- An AC asks for a data-quality check but lists only the gold notebook, while every check
  lives in `data_quality_checks.Notebook`.
- task-033's own newer scope note names `data_sources.md` and `fabric_workspace.md` as
  remaining scope, but `files_affected` omitted both **and listed wrong paths for them** —
  first dispatch shipped 7 of 9 files and needed a mid-task amendment. The `/work` dispatch
  brief fences writes to `files_affected`, so the two instructions actively conflict.
- Schema-changing tasks under-count the state-asserting schema doc that a column change
  necessarily falsifies — under-counted on two consecutive subtasks.
- Semantic-model changes under-count `docs/architecture/semantic_model.md`.
- Repeated declared-vs-actual drift, once 10 declared / 14 modified.

**Dedup verdict: not a duplicate.** FB-058 (shipped), FB-086 (shipped v4.8.0, drift
auto-union), and v5.2.0's two ripple heuristics cover CSS / test-factory / enum-extension
ripples. This is a different ripple domain: cross-artifact docs↔notebook parity, and
dispatch-brief re-sync when a scope note post-dates `files_affected`.

**Predecessor — extend, don't restate.** `interaction-logs/insights/2026-06-11_implement-agent_files-affected-ripple.md`
deferred a new FB until *"post-v4.8.0 exports still show high reconciliation noise."*
That trigger is now met. The new doc must say so explicitly and link back.

**Likely eventual blast radius:** `support/reference/decomposition.md` (Ripple Inference /
Pre-Pass Leg 2), `commands/work.md` dispatch-brief construction.

**Capture as:** unqualified `ready`. 9 distinct incidents is comfortably above the bar.

---

## Cluster 2 — negative-findings positive control → insight doc + FB

**Evidence:** 8 raw / **8 unique** (no dupes). Dates 07-23, 07-26/27, 07-31 ×2, 08-10 ×2, 08-11.

**Shape.** `.claude/rules/agents.md:125` § "Negative Findings Require a Positive Control"
requires a probe be shown to *work* — but nothing governs whether the control interrogates
the **same universe** as the claim, nor the **result set**. Three genuinely distinct
mechanisms, each with a real repro:

1. **The control itself can be invalid.** `rg --files -g '*.CopyJob*'` returned empty for
   *both* the absent target and the known-present control, because Fabric artifacts are
   directories. The control silently proved nothing. (task-033, 07-26)
2. **The mandated tool is not always available.** `Grep` was absent from the research-agent
   session (07-23) and the verify-agent session (07-31) while the rule names it as route (a).
   On 07-31 the predicted failure then occurred verbatim — a bash-grep consumer sweep
   returned a false absence.
3. **A third silent-empty mechanism.** In this harness `grep` is a shell *function* sourced
   from `~/.claude/shell-snapshots/snapshot-zsh-*.sh` and **it skips gitignored files**.
   Repro: `grep -c` on the direct path returns 2; recursive `grep -rln` from repo root
   returns empty on the same file. (task-064, 08-11)

Adjacent, same cluster: the rule governs whether a probe works but not its *result set* —
across task-048's four rounds the same finding recurred as the failure migrated one axis per
round (output truncated by `| head -40`, then remediation scope, …). Also a mutation-testing
gap in `verify-agent.md`: `git checkout -- <file>` restores from the **index**, not HEAD.

**Dedup verdict: not a duplicate.** The 2026-07-19 harvest Tier 3 closed a *different*
BSD-grep signal as "rule fired correctly." This is three new ways the rule's own mechanism
can be defeated.

**Likely eventual blast radius:** `rules/agents.md` — **one of the 7 auto-loaded rules**, so
any edit carries a session-wide context cost every session. Sub-issue 2 (tool provisioning to
subagents) may be harness-side and outside template control — shape it like FB-075/FB-077's
upstream-gated items if so.

**Capture as:** unqualified `ready`. Strongest cluster in the set.

---

## Cluster 3 — verify-agent `runtime_validation` → insight doc + **sibling FB** (see correction)

**Evidence:** 7 raw / **6 unique**. Dates 07-23 ×2, 07-30, 07-31, 08-10, 08-11.

**Shape.** Artifact classes with **no local execution environment at all** pass structurally
and break at runtime:
- Fabric PySpark notebooks — no Spark session, no lakehouse; every notebook-touching task
  lands `runtime_validation: "not_applicable"`.
- TMDL semantic models — no parser installed; `fabric-cicd` validates only at publish, and a
  push to main fires a real publish, so there is no safe dry-run. Verification fell back to
  byte-level comparison.
- GitHub Actions workflows — task-045's `deploy-fabric.yml` passed local YAML parse plus
  `fabric-cicd` API inspection, then failed *every* real Actions run at `setup-python`
  (`cache: pip` requires a `requirements.txt`/`pyproject.toml` the repo lacks).
- Live Delta row counts — spec assertions quoting 903 / 2,560 / 3,463 rows cannot be
  re-derived; no local lakehouse read path exists.
- `delta-spark` absent made a missing `overwriteSchema` on a schema-widening Delta overwrite
  structurally invisible; it recurred in a file that already carried the guard twice.

**Important nuance — do not write the doc as "these are unverifiable."** One 07-23 marker
records the opposite failure: the task notes *and* the dispatch brief both assumed
source-reading was the ceiling, and that was **false** for the pure functions involved. The
lesson cuts both ways — the gap is that nothing forces an honest determination of what the
local ceiling actually is, so agents both over-claim and under-claim it.

**Predecessor — extend, don't restate.**
`interaction-logs/insights/2026-06-11_verify-agent_structural-green-runtime-broken.md`
flagged "FB-076 condition (a) signal present" as a watch item.

**Capture as:** caveat not required on evidence volume (6 incidents, 4 artifact classes), but
see the correction below for **where** it gets captured.

---

## ⚠ FB-076 correction — the easiest thing here to get wrong

The original queue item said: *"FB-076's re-open gate is met (2nd project signal) — mitigations
2 and 3 are no longer signal-gated."* **That is wrong. Do not do it.**

FB-076 (`template-maintenance/feedback.md`, § FB-076) documents exactly two failure modes:
1. **Client/server bundle boundary** — a Node-only transitive dep pulled into a client bundle.
2. **Catalog-state-dependent preconditions** — a branch logically unreachable because no row
   in the live catalog satisfies it (this is what mitigation 3, "live-data cross-reference",
   addresses).

Its defer condition reads: *"Re-assess when (a) 2nd project signals **the same verification
gap**, OR (b) FB-066 downstream telemetry suggests broader runtime_validation hardening is
needed."*

Cluster 3 is **neither documented mode**. It is a third: *no local execution environment for
the artifact class at all.* Therefore:

- **Condition (a) is NOT met** — this is not "the same verification gap."
- **Condition (b) IS met** — a third failure class under the same `runtime_validation` check.
- **Mitigation 2 (ESLint client-import rule) must stay gated.** There is no client/server
  bundle boundary in a PySpark / Fabric / Power BI stack. Unlocking it on this evidence is a
  category error that would scope real design work against inapplicable evidence.
- **Mitigation 3 is a partial match only** — closer in spirit ("can't fully trust a local
  pass") but still not its documented failure mode.

**Do this instead:** open a **new sibling FB** for the third mode, cross-referenced from
FB-076 as *extends, not duplicates* — the same framing FB-076 itself used when extending
FB-066, and FB-084 used when extending it again. Add a line to FB-076 noting the third mode
was observed in a 2nd project and satisfies condition **(b)**, without touching the status of
mitigations 2 or 3.

Candidate mitigation for the sibling item: require an explicit *declare-the-local-ceiling*
step — name the artifact class as locally unverifiable **and** emit a deferred live-validation
follow-up task — rather than silently passing `not_applicable`.

---

## Cluster 4 + 6 merged — task/AC authoring internal consistency → **one** insight doc + **one** FB

These were originally two clusters. **Merge them.** They share an anchor instance (task-063)
and are the same defect class at two different authoring sites: initial decomposition, and
phase-level fix-task creation. Writing two thin overlapping docs manufactures a false split.

**Evidence:** 3–4 unique (cluster 4) + 3 unique (cluster 6). Dates 07-22, 07-30, 08-06,
08-10 ×2, 08-11. **Single project, single six-day stretch.**

**Sub-pattern A — AC vs `owner` mismatch.**
- task-058 AC5 (*"a decision is recorded on whether to delete the four empty subdirectories"*)
  requires a **user** decision but sits on an `owner: "claude"` task. No implement-agent pass
  can satisfy it; verification can only ever mark it partial.
- `owner: "both"` tasks with majority-remote acceptance have no structural way to record
  *partial* verification — the Claude-verified half is indistinguishable in
  `task_verification` from a fully verified task.

**Sub-pattern B — phase-level fix-task authoring quality.**
- task-058's title and AC1 both say "14 references"; the description it shipped with
  enumerates 17; the actual repo count was 18 file-specific plus 3 directory refs. Wrong at
  creation.
- task-063's AC cited the DEC-002/task-032 notebook↔src parity contract for an asset with
  neither a `src/` mirror nor a function shape — unsatisfiable as written, and it cost the
  implementer a documented reinterpretation (FR-066).
- **Circular re-verification trigger:** a phase-level result is invalidated when the spec
  fingerprint changes — but the natural response to a phase-level result is to record it in
  the spec, which changes the fingerprint and invalidates the result just recorded. One full
  loop turn is confirmed in the record: `3909f351` pass → tasks 057–060 edit spec →
  `a475793a` → re-verify.

**Dedup verdict: not a duplicate.** FB-100 (shipped v4.23.0) fixed *routing* and *completion
shape* for `owner: both`, not authoring. FB-107 is about *gating*, not authoring quality.
DEC-022 is about AC *authority*, not AC authoring quality. Confirmed:
`support/reference/phase-decision-gates.md` contains zero mentions of "fingerprint",
"re-verif", or "enumerat".

**Likely eventual blast radius:** `commands/breakdown.md`, `support/reference/task-schema.md`,
`rules/task-management.md`, `support/reference/phase-decision-gates.md`, `commands/work.md`
phase-level verify dispatch prompt.

**Capture with an explicit caveat** in the `Status:` line — single-project, single-timeframe,
at the 3-occurrence floor. Frame it like FB-076 / FB-084 / FB-107 already are, not as an
unqualified `ready`.

---

## Cluster 5 — closure sweeps, lexical vs structural → insight doc + FB

**Evidence:** 5 raw / **5 unique**. Dates 08-05 ×2, 08-10 ×3.

**Shape.** task-057's implementation sweep verified that the 13 phrasings it had *changed*
returned 0 occurrences, and passed. It missed a 14th stale status assertion three lines below
an edited paragraph, because that assertion used vocabulary the sweep never searched for.
Then: **three consecutive verification attempts each found exactly one more**, and each time
the implementer's response was to widen the *sweep vocabulary* (phrasings changed → improvised
status words → …) rather than switch to a **structural task-ID cross-reference**.

Two more members of the same class:
- A fifth marker, *"drift detection vs section fingerprints"* (08-05), shows the same
  lexical-vs-structural gap inside the fingerprint mechanism itself. A naive area-string grep
  misses this one — include it.
- When a task closes a criterion that other documents describe as deferred, nothing ties the
  closure to **ungated mirror surfaces**. The descope was tracked against three DEC-016-gated
  surfaces precisely because those needed approval routing; the ungated mirrors were missed.

**Dedup verdict: not a duplicate.** No existing rule or reference doc addresses it.

**Likely eventual blast radius:** `.claude/agents/verify-agent.md`, possibly
`support/reference/drift-reconciliation.md` (the DEC-021 section-fingerprint machinery is
directly adjacent).

**Capture with a single-project caveat**, same framing as the merged 4+6 item.

---

## Sequencing and safety

`interaction-logs/` is **wholly gitignored**. Git provides **zero** recovery for anything in
it. Sequence accordingly:

1. Write the insight docs.
2. Write the FB items (their bodies reference the insight docs, per Part 7 step 6).
3. Amend FB-076 + open the sibling item.
4. **Only then** move exports to `processed/` — and only the ones this pass actually
   processed. Prefer copy → verify → remove-source over a blind bulk `mv`.

**Do not move files eagerly.** Part 7's documented per-file loop moves each file as it is
read, but the 2026-07-19 harvest sequenced the batch move last, after shipping Tier 1 and
capturing Tier 2. Follow the 07-19 precedent.

---

## Resume protocol (this will take more than one session)

The harvest is **self-resuming** if the move-last rule is honored, because the filesystem
carries the progress state:

| Signal | Meaning |
|---|---|
| File still in `interaction-logs/inbox/` | Not yet harvested |
| File in `interaction-logs/processed/` | Done |
| FB item present in `feedback.md` | That cluster's conclusion has landed |
| Insight doc present in `interaction-logs/insights/` | That cluster is written up |

Clusters are independent — each is one insight doc plus one FB item. **Two or three clusters
per session is a realistic pace.** A session that runs short leaves the rest in the inbox and
its conclusions in `feedback.md`; the next session reads both and continues. No handoff file
is needed.

At the end of every session: update this plan's `Status:` line with which clusters are done.

---

## What NOT to do

- **Do not** unlock FB-076 mitigations 2 or 3. See the correction section.
- **Do not** write 6 insight docs. Clusters 4 and 6 merge.
- **Do not** capture clusters 1 or 3 as freshly discovered — both have 2026-06-11 predecessor
  docs whose dispositions predicted this exact re-assessment. Extend them.
- **Do not** move any file to `processed/` before its cluster's insight doc and FB item exist.
- **Do not** treat the 80 markers without a `template_area` as harvest material — they are
  project-level drift belonging to OEMMatInsightBI, not template feedback.
- **Do not** enumerate the inbox with a bare `*.json` glob. 7 files are dot-prefixed.
