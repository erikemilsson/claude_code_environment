# Plan — work.md Hot-File Batch Implementation

**Purpose:** Apply the work.md-touching slice of FB-015, FB-017, FB-027, and FB-036 in a single read-and-edit pass per the File Collision Map's hot-files rule. Out-of-file primary edits (`dashboard-regeneration.md` for FB-015, audit pass on `decisions.md`/`workflow.md` for FB-017, alt-site callouts for FB-027) are deferred to follow-on batches.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Source feedback items:** FB-015, FB-017, FB-027, FB-036 (in `.claude/support/feedback/feedback.md`)
**Related decision:** none — these are direct-implementation FB items
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in the same commit as this plan)
**Tracker status line to advance:** `Phase 4 — DEC-007 + DEC-008 + FB-037 implemented; remaining direct items next (hot-file batches)` → `Phase 4 — work.md hot-file batch implemented (FB-017 primary, FB-027 + FB-036 + parallel-execution.md, FB-015 work.md audit); remaining direct items next`

---

## Scope

### In scope (this commit)

| Item | Touch site | Edit type | Notes |
|------|-----------|-----------|-------|
| FB-017 | `work.md` Step 2b | **Primary edit** | Inline the checkbox-detection trigger so the caller is unambiguously responsible for firing the auto-finalization algorithm in `phase-decision-gates.md`. Resolves the styler-project regression (DEC-039/040/026 stayed `proposed` after boxes were checked). |
| FB-027 | `work.md` Step 2 spec check | **Work.md slice** | Extend the "Minor/trivial addition" branch with explicit "no formal planning" wording. New paragraph below the decision tree spells out: one-sentence diffs skip `/research`/decisions/decomposition, dispatch implement-agent directly. |
| FB-036 | `work.md` § "If Executing (Parallel)" + `parallel-execution.md` new § "Pre-Dispatch Confirmation" | **Primary edit (two files)** | New procedure section in parallel-execution.md (between Eligibility Assessment and Parallel Dispatch); work.md gains a new top bullet in "Key rules" referencing it. Threshold: batch ≥ 3 (matches `max_parallel_tasks` default). |
| FB-015 | `work.md` § "If Completing" | **Audit only** | Reword the "Regenerate dashboard with completion summary" bullet — the "summary" framing is the only summary-coded language in work.md's regen paths. Tiny tweak. |

### Out of scope (deferred to follow-on batches)

- **FB-015 primary edit:** negative rule in `dashboard-regeneration.md § Action Item Contract` ("must NOT include work summaries, completion reports, or recent-activity recaps"). Goes in a dashboard-regeneration.md focused commit. Listed as the natural follow-on after this batch.
- **FB-015 secondary:** `commands/health-check.md` Part 6 check #4 (extend to detect summary-shaped content if feasible). Stays in the health-check edit batch.
- **FB-017 audit:** re-verify `decisions.md` line 151 and `workflow.md` lines 195-201 still describe accurate auto-finalization promises after the work.md inlining. Expected outcome: no edit needed — the inlining makes the promises true. Spot-check post-commit.
- **FB-017 secondary (optional):** restructure `phase-decision-gates.md` into "caller checklist" vs "full procedure" sections. Defer — the work.md inlining alone is the load-bearing fix.
- **FB-027 alt-sites:** `commands/research.md` callout and `rules/decisions.md` cross-reference. The work.md edit handles the immediate user-flow case; alt-sites are reinforcement.
- **FB-027 outside-batch:** `commands/iterate.md` should also run the FB-017-style detection (per FB-017's item #4) — separate file, separate batch.
- **FB-036 related:** FB-034 ("respect user kills") shares the over-eager-execution theme but lands in `rules/agents.md` / `implement-agent.md` — different file, different batch.

---

## Context to Load Before Executing

Read in this order at session start:

1. **`.claude/commands/work.md`** — full file (~950 lines). All four edits land here. Load once and keep open.
2. **`.claude/support/feedback/feedback.md`** lines 16-50 (FB-017, FB-015), 142-152 (FB-027), 280-296 (FB-036) — confirm the Assessed lines haven't drifted since plan was written.
3. **`.claude/support/reference/phase-decision-gates.md`** — confirm § "Decision Dependency Check" (lines 68-103) still describes the auto-update logic. FB-017's inline trigger anchors to this section; if the section was renamed or moved, update the cross-reference in Step 1 below.
4. **`.claude/support/reference/parallel-execution.md`** — confirm § "Parallelism Eligibility Assessment" (lines 7-109) and § "Parallel Dispatch" (line ~113) are the right anchor points. The new "Pre-Dispatch Confirmation" section sits between them.
5. **`template-upgrade-2026-04.md`** — Current State + Phase 4 Hot-files block + File Collision Map work.md row. Confirm work.md row lists FB-015/017/027/036 (no new items added since plan was written).

Auto-memory: no specific entry is load-bearing for this plan beyond what's already in `.claude/CLAUDE.md`.

---

## Implementation Steps

### Step 1: FB-017 — Inline checkbox-detection trigger in Step 2b

Locate Step 2b in `.claude/commands/work.md` (currently lines 330-359). The opening paragraph and the "Read `.claude/support/reference/phase-decision-gates.md` and follow its procedure" block stay as-is.

**Insert this block immediately after the bulleted summary list (the bullets ending with "Early-exit conditions"), and BEFORE the existing `**When a decision blocks work**, present options including research:` line:**

```markdown
**Required inline trigger — checkbox detection on every entry:**

For every `decision-*.md` file with frontmatter `status: proposed`:

1. Read the file's `## Select an Option` section
2. Scan for checked boxes — match `[x]`, `[X]`, `[✓]`, `[✔]` (per the normalization in `phase-decision-gates.md` § "Phase Check")
3. If a checked box is found AND frontmatter `status` is still `proposed`:
   - Extract the selected option name (text after `[x] ` on the matched line)
   - Update frontmatter: `status: approved`, `decided: <today's YYYY-MM-DD>`
   - Populate the Decision section using the option name and the matching Option Details rationale
   - Run the Post-Decision Check (`phase-decision-gates.md` § "Post-Decision Check") — handles inflection-point pause if applicable
   - Log: `Decision {DEC-ID} resolved → status updated to 'approved' (selected: {option_name})`
4. If no checked boxes are found across all proposed decisions, proceed to the rest of Step 2b without changes.

This step MUST run on every Step 2b invocation. It is the caller's responsibility — `phase-decision-gates.md` defines the algorithm, but `/work` Step 2b is what fires it. Do not skip this scan even if other Step 2b checks suggest no new decisions.
```

The rest of Step 2b (the "When a decision blocks work" block, ambiguity-handling block, research dispatch, "If all checks pass → proceed to Step 2c") stays as-is.

**Why this shape:** `phase-decision-gates.md § Decision Dependency Check` already specifies the auto-update logic correctly. The failure mode is "caller forgets to fire it." Restructuring the reference doc would still leave call-site ambiguity. Inlining the trigger as an imperative caller-side checklist removes the ambiguity without duplicating the full algorithm.

---

### Step 2: FB-027 — Skip-planning callout in Step 2 spec check

Locate Step 2 (Spec Check) in `.claude/commands/work.md` (currently lines 308-328). The current decision tree:

```
Check request against spec:
├─ Clearly aligned → Proceed
├─ Minor/trivial addition → Proceed (doesn't need spec change)
└─ Significant but not in spec → Surface it:
   "This isn't covered in the spec. Options:
    1. Add to spec: [suggested addition]
    2. Proceed anyway (won't be verified against spec)
    3. Skip for now"
```

**Edit the "Minor/trivial addition" line:**
- Old: `├─ Minor/trivial addition → Proceed (doesn't need spec change)`
- New: `├─ Minor/trivial addition → Proceed (no spec change, no formal planning)`

**Insert this paragraph immediately after the decision tree code block, BEFORE the existing `**If user selects "Proceed anyway":**` block:**

```markdown
**Skip formal planning for trivial requests:** If the diff for the request fits in one sentence (typo fix, log line addition, variable rename, single import update), dispatch implement-agent directly — do not route through `/research`, decision records, or task decomposition. The "Minor/trivial addition" branch above is the entry point. The principle: planning overhead should be proportional to scope.
```

The "Scope significance:" paragraph that already exists (currently the last paragraph in Step 2) stays as-is and reinforces the new paragraph.

**Why Step 2 (not Step 3 routing as the collision map suggested):** Step 3's routing table is about phase/decision/parallel-batch state, not about request-scope-vs-planning-overhead. The natural home for a skip-planning callout is Step 2 where requests are first triaged for scope. The collision-map "Step 3 routing" label was a loose pointer; Step 2 is the actual call site.

---

### Step 3: FB-036 — Pre-dispatch confirmation in parallel batch

**Two-file edit.** The procedure detail lives in `parallel-execution.md`; `work.md` gets a thin reference in the right spot.

#### 3a. `parallel-execution.md` — new section between Eligibility Assessment and Parallel Dispatch

Locate `.claude/support/reference/parallel-execution.md`. The current structure has:
- `## Parallelism Eligibility Assessment` (lines 7-109)
- horizontal-rule `---` (line 111)
- `## Parallel Dispatch` (line 113+)

**Insert a new section between the horizontal rule and `## Parallel Dispatch`:**

```markdown
## Pre-Dispatch Confirmation

When Step 2c produces a parallel batch of **3 or more tasks**, confirm with the user before spawning. Batches of 2 skip this step — the parallel-dispatch default of 3 means a 2-batch is a partial use of the budget and the cheapest case to interrupt if wrong.

### Format

\`\`\`
Parallel dispatch ready: {N} tasks

  Task {id}: "{title}" → files: [{files_affected}]
  Task {id}: "{title}" → files: [{files_affected}]
  ...

Verify strategy: per-task verify-agent dispatched as each implement-agent completes.

{If held_back is non-empty:}
Held back (file conflicts):
  Task {id}: "{title}" — conflict with Task {conflict_with} on [{conflict_files}]

[D] Dispatch  [S] Skip — review batch first  [1] Dispatch only first task
\`\`\`

### Behavior

- `[D]` Dispatch → proceed to § "Parallel Dispatch" Step 1 (Log the Parallel Dispatch)
- `[S]` Skip → return to `/work` Step 2c. User can review tasks, adjust priorities, edit `files_affected`, then re-run `/work`.
- `[1]` Dispatch only first task → drop the batch, treat as sequential single-task dispatch on the highest-priority eligible task.

### Rationale

Parallel batches scale Claude's throughput but also remove the natural pause-points that sequential dispatch provides (per-call permission prompts, post-task user-visible state changes). A pre-dispatch confirmation restores a cheap human checkpoint without changing parallel-batch behavior.

Independent of permission settings or auto-mode classifier behavior — auto mode (which removes per-call permission prompts) actually makes this checkpoint *more* valuable, not less.

---
```

(Note: the closing `---` is a new horizontal rule between Pre-Dispatch Confirmation and Parallel Dispatch.)

#### 3b. `work.md` § "If Executing (Parallel)" — add Key Rules bullet

Locate `.claude/commands/work.md` § "If Executing (Parallel)" (currently lines 563-574). The current "Key rules:" list begins with "Orchestrator sets all batch tasks to 'In Progress'…".

**Insert this bullet at the top of the "Key rules:" list, BEFORE the existing "Orchestrator sets all batch tasks…" bullet:**

```markdown
- **Pre-dispatch confirmation (batch ≥ 3):** Before spawning, present the dispatch plan to the user — task IDs, titles, files affected, verify strategy — and await explicit confirmation. Skip for batches of 2 (low surprise; partial budget). See parallel-execution.md § "Pre-Dispatch Confirmation" for the prompt format and `[D]`/`[S]`/`[1]` behavior.
```

The rest of the Key Rules list and the "Full procedure" reference above it stay as-is.

**Threshold judgment:** Set at "≥ 3" rather than "≥ 2" so a 2-task batch (cheap, low surprise, easy to interrupt mid-run) doesn't accumulate friction. 3 matches the default `max_parallel_tasks` — confirmation triggers when the batch hits the configured maximum. FB-036's "N configurable; default 3" wording supports this; the threshold can be made configurable as a follow-up if desired.

---

### Step 4: FB-015 — Audit dashboard-regen wording in "If Completing"

Locate `.claude/commands/work.md` § "If Completing" (currently lines 689-704). Bullet 2 currently reads:

```
2. **Regenerate dashboard** with completion summary
```

**Replace with:**

```
2. **Regenerate dashboard** to reflect completion state (Action Required clears; Progress shows final phase complete; Tasks section collapses fully-finished phases)
```

Other dashboard-regen call sites in `work.md` (Step 4 § State Persistence Protocol's two regen lines, `/work complete` § step 7) currently say "Regenerate dashboard" with no "summary" framing — those need no change. Confirm by Grep `summary.*dashboard|dashboard.*summary` in `work.md` after the edit.

**Why this is audit-only:** The primary FB-015 edit (a "must NOT include work summaries" negative rule in `dashboard-regeneration.md § Action Item Contract`) lives in a different file and is deferred to its own batch per the Scope section above. The work.md slice only removes the one piece of summary-coded language in work.md's regen paths.

---

### Step 5: Tracker bookkeeping

Update `template-upgrade-2026-04.md`:

**5a. Status line** (top of file):
- Replace: `**Status:** Phase 4 — DEC-007 + DEC-008 + FB-037 implemented; remaining direct items next (hot-file batches)`
- With: `**Status:** Phase 4 — work.md hot-file batch implemented (FB-017 primary + FB-027 + FB-036 + FB-015 audit); remaining direct items next`

**5b. Current State block:** add a new bullet after the FB-037 implemented bullet:

```
- **work.md hot-file batch implemented 2026-04-17:** Step 2b inlines the checkbox-detection trigger so `/work` reliably auto-finalizes checked decisions (FB-017 primary fix; resolves styler-project regression). Step 2 spec-check tree's "Minor/trivial addition" branch now explicitly says "no spec change, no formal planning" with a new paragraph routing one-sentence diffs around `/research` (FB-027 work.md slice). New `## Pre-Dispatch Confirmation` section in `parallel-execution.md` (referenced from work.md § "If Executing (Parallel)" Key Rules) gates parallel batches ≥ 3 behind a `[D]`/`[S]`/`[1]` prompt (FB-036 primary). "If Completing" dashboard-regen bullet rephrased from "completion summary" to "completion state" (FB-015 work.md audit slice). Out-of-file primary edits remain: dashboard-regeneration.md § Action Item Contract negative rule for FB-015; phase-decision-gates.md restructure (optional) and decisions.md/workflow.md audit (likely no edit) for FB-017; alt-site callouts (research.md, rules/decisions.md) for FB-027.
```

**5c. Update the `**Next action:**` bullet** (replace the FB-037-era suggestion):

```
- **Next action:** Erik chooses the next Phase 4 unit. Suggested: (1) FB-015 primary edit in `dashboard-regeneration.md § Action Item Contract` — small, completes FB-015; (2) `rules/session-management.md` group (FB-023 + FB-024 + FB-025); (3) `rules/agents.md` / `implement-agent.md` group (FB-022 + FB-034 + FB-035 + FB-031).
```

**5d. Phase 4 Hot files block:** flip the `commands/work.md` line:

- Replace: `- [ ] **\`.claude/commands/work.md\`** — FB-015 (Action Required cleanup), FB-017 (Step 2b checkbox detection), FB-027 (skip-planning callout in Step 3 routing), FB-036 (pre-dispatch confirm in Step 4).`
- With: `- [x] **\`.claude/commands/work.md\`** — FB-015 (work.md audit only — primary edit deferred to dashboard-regeneration.md), FB-017 (Step 2b inlining — primary done), FB-027 (Step 2 spec-check skip-planning callout — work.md slice; alt-sites in research.md/decisions.md deferred), FB-036 (work.md callout + parallel-execution.md primary done). Implemented 2026-04-17.`

**5e. File Collision Map:** strikethrough the work.md and parallel-execution.md row entries. Format mirrors prior strikes (e.g., the DEC-006 strikes use `~~text~~ ✓`).

In the `commands/work.md` row:
- `FB-011 •` → leave as-is (FB-011 not in this batch)
- `FB-015 •` → `~~FB-015 audit~~ ✓`
- `FB-017 Step 2b` → `~~FB-017 Step 2b inlined~~ ✓`
- `FB-027 Step 3 routing` → `~~FB-027 Step 2 callout~~ ✓` (also note: actual home was Step 2, not Step 3 — collision map label was loose)
- `FB-036 Step 4` → `~~FB-036 Key Rules bullet~~ ✓`

In the `support/reference/parallel-execution.md` row:
- `FB-036 pre-dispatch confirm` → `~~FB-036 Pre-Dispatch Confirmation section~~ ✓` (FB-030 fan-out alt-site stays as-is — not implemented in this batch)

In the `support/reference/dashboard-regeneration.md` row:
- Add note that FB-015 primary edit remains pending in `support/reference/dashboard-regeneration.md` § Action Item Contract — should not get a strike yet.

**5f. Cleanup Manifest:** add a row for `plan-work-md-batch.md` immediately after the existing `plan-dec-008-implementation.md` row:

```
| `plan-work-md-batch.md` | DELETE-AFTER | work.md hot-file batch (FB-015/017/027/036) implementation plan for fresh-session execution |
```

**5g. Session Log:** append a new entry at the bottom (after the FB-037 entry):

```markdown
### 2026-04-17 — Phase 4: work.md hot-file batch (FB-015 audit + FB-017 + FB-027 + FB-036)

**Done:**
- **FB-017 (primary):** Inlined the checkbox-detection trigger into work.md Step 2b. Step 2b now explicitly enumerates "for every proposed decision file, scan for checked boxes, normalize, update frontmatter to approved, populate Decision section, run post-decision check." `phase-decision-gates.md` retains the algorithm; Step 2b ensures the algorithm fires on every entry. Resolves the styler-project regression (DEC-039/040/026 stayed `proposed` after boxes were checked).
- **FB-027 (work.md slice):** Step 2 spec-check tree's "Minor/trivial addition" branch reworded to "(no spec change, no formal planning)". New paragraph below the tree spells out: one-sentence diffs (typo, log line, rename, single import) skip `/research`/decisions/decomposition, dispatch implement-agent directly. Alt-site callouts in research.md / rules/decisions.md remain available as follow-up.
- **FB-036 (primary):** New `## Pre-Dispatch Confirmation` section in `parallel-execution.md` between Eligibility Assessment and Parallel Dispatch. Triggers for batches ≥ 3 (matches `max_parallel_tasks` default). Format: dispatch summary + `[D] Dispatch / [S] Skip / [1] First-only` prompt. work.md § "If Executing (Parallel)" gains a "Pre-dispatch confirmation" bullet at the top of "Key rules" referencing the new procedure.
- **FB-015 (work.md audit slice):** "If Completing" bullet 2 reworded from "Regenerate dashboard with completion summary" → "Regenerate dashboard to reflect completion state". The "summary"-coded framing was the only such language in work.md's regen paths. Other regen call sites in work.md already use neutral wording. Primary FB-015 edit (negative rule in `dashboard-regeneration.md § Action Item Contract`) remains deferred to its own batch.
- Tracker bookkeeping: status line, Current State, Phase 4 hot-files block (work.md → `[x]`), File Collision Map (work.md row + parallel-execution.md row strikes), Cleanup Manifest (plan file added), Session Log entry.
- Pre-commit hook: warns about `version.json` not being bumped (work.md and parallel-execution.md are sync-category files). Expected per existing tracker policy; commit anyway. Phase 5 cleanup handles version-bump scope.

**Judgment calls:**
- **FB-017 inline-vs-restructure:** Inlined the trigger as an imperative caller-side checklist rather than restructuring `phase-decision-gates.md` itself. Reasoning: the algorithm is correct; the failure mode is "caller forgets to fire it." Restructuring the reference would still leave call-site ambiguity. Inlining at the call-site is the more direct fix. `phase-decision-gates.md` restructure remains optional follow-up.
- **FB-027 placement:** Kept the work.md slice in Step 2 (spec check) rather than Step 3 (routing). Step 3's routing table is about phase/decision/parallel-batch state, not request-scope-vs-planning-overhead. The collision-map "Step 3 routing" label was a loose pointer. Alt-sites (research.md, rules/decisions.md) would reinforce the principle but aren't load-bearing for the user-flow fix.
- **FB-036 threshold:** Set at "≥ 3" rather than "≥ 2" so the cheap case (2-task batch, low surprise) doesn't get the friction. Matches the default `max_parallel_tasks` value (3) — confirmation triggers when the batch is at the configured maximum. FB's "N configurable; default 3" wording supports this; threshold-as-config can be a follow-up.
- **FB-015 file-grouping discipline:** Deliberately did NOT touch `dashboard-regeneration.md` in this batch even though it's the primary FB-015 location. The work.md batch principle is "edit work.md once"; cross-cutting into a different reference file would violate the file-grouping rule. The primary FB-015 edit gets its own commit.

**Next:** Erik chooses the next Phase 4 unit. Strong candidates:
1. **FB-015 primary** in `dashboard-regeneration.md § Action Item Contract` — small file, completes FB-015 work begun in this batch, neighbours the work.md audit just done.
2. **`rules/session-management.md` group** (FB-023 `/btw` + FB-024 `/rewind`/Esc+Esc + FB-025 `/rename`) — three items in one file, single bundled edit.
3. **`rules/agents.md` + `implement-agent.md` group** (FB-022 root-cause rule + FB-034 respect user kills + FB-035 large-file Read guidance + FB-031 Writer/Reviewer mention) — larger group, two related files.

**Open questions for later:**
- After this batch lands, re-verify that `decisions.md` line 151 and `workflow.md` lines 195-201 (the auto-finalization promises FB-017 was meant to honor) still read accurately. Expected: yes — the work.md inlining should make those promises true again. Edit only if wording drifted.
- FB-027 alt-sites (research.md callout, rules/decisions.md cross-reference) become available follow-on work but aren't required if work.md handles the user-flow case.
- FB-036 threshold may want to become configurable (`pre_dispatch_confirm_threshold` in spec frontmatter or a settings field) — not implemented here; assess after some real-world dispatches.
- Version bump tally for Phase 5 now includes DEC-007 + DEC-008 + FB-037 + work.md batch.
```

---

### Step 6: Commit

Single commit. Pre-commit hook will warn about `version.json` (`work.md` and `parallel-execution.md` are sync-category files); commit anyway per existing tracker policy.

Commit message (HEREDOC):

```
Phase 4: work.md hot-file batch — FB-015 audit + FB-017 + FB-027 + FB-036

Implements the work.md-touching slice of four feedback items in a single
read-and-edit pass per the File Collision Map's hot-files rule. Out-of-file
primary edits (dashboard-regeneration.md for FB-015; decisions.md/workflow.md
audit for FB-017; alt-site callouts for FB-027) deferred to follow-on batches.

FB-017 (primary): work.md Step 2b now inlines the checkbox-detection trigger
- "For every proposed decision file: scan for checked boxes (normalize
  [x]/[X]/[✓]/[✔]), update frontmatter to approved, populate Decision
  section, run post-decision check."
- phase-decision-gates.md retains the algorithm reference; Step 2b ensures
  the algorithm fires on every entry. Addresses the styler-project regression
  where checked decisions stayed `proposed` until the user noticed.

FB-027 (work.md slice): Step 2 spec-check "Minor/trivial addition" branch
extended with explicit "no formal planning" wording, plus a new paragraph
spelling out: one-sentence diffs (typo, log line, rename, single import)
skip /research and decision records — dispatch implement-agent directly.
Alt-site callouts in commands/research.md / rules/decisions.md remain
available as follow-on reinforcement.

FB-036 (primary): new "## Pre-Dispatch Confirmation" section in
parallel-execution.md between Eligibility Assessment and Parallel Dispatch.
Triggers for batches >= 3 (matches default max_parallel_tasks) with a
[D] Dispatch / [S] Skip / [1] First-only prompt. work.md § "If Executing
(Parallel)" gains a "Pre-dispatch confirmation" bullet at the top of
"Key rules" referencing the new procedure.

FB-015 (work.md audit slice): "If Completing" bullet rephrased from
"Regenerate dashboard with completion summary" to "Regenerate dashboard to
reflect completion state (Action Required clears; Progress shows final
phase complete; Tasks section collapses fully-finished phases)". Removes
the only summary-coded framing in work.md's regen paths. Primary FB-015
edit (negative rule in dashboard-regeneration.md § Action Item Contract)
remains deferred.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Verification Checklist (post-edit, pre-commit)

- [ ] `work.md` Step 2b has the new "Required inline trigger — checkbox detection on every entry" block placed AFTER the bulleted summary list and BEFORE "When a decision blocks work" paragraph
- [ ] Block enumerates: scan proposed files, normalize checkbox forms, update frontmatter (`status: approved` + `decided` date), populate Decision section, run post-decision check
- [ ] `work.md` Step 2 spec-check tree shows `Minor/trivial addition → Proceed (no spec change, no formal planning)`
- [ ] `work.md` Step 2 has the new "Skip formal planning for trivial requests:" paragraph after the decision tree code block, before "If user selects 'Proceed anyway':"
- [ ] `work.md` § "If Executing (Parallel)" Key Rules first bullet is the new "Pre-dispatch confirmation (batch ≥ 3)" entry referencing parallel-execution.md
- [ ] `work.md` § "If Completing" bullet 2 reads "Regenerate dashboard to reflect completion state (Action Required clears; Progress shows final phase complete; Tasks section collapses fully-finished phases)"
- [ ] Grep `work.md` for `completion summary` — no matches
- [ ] `parallel-execution.md` has new `## Pre-Dispatch Confirmation` section between `## Parallelism Eligibility Assessment` and `## Parallel Dispatch` with: format block (`Parallel dispatch ready: {N} tasks` + tasks list + verify strategy + held-back conditional + `[D]`/`[S]`/`[1]` prompt), Behavior subsection, Rationale subsection, trailing horizontal rule
- [ ] Tracker: status line, Current State new bullet, Next action updated, Phase 4 hot-files `[x]`, File Collision Map strikes (work.md row + parallel-execution.md row), Cleanup Manifest new row for `plan-work-md-batch.md`, Session Log entry appended
- [ ] Pre-commit hook output shows `version.json` warning (expected — not an error)
- [ ] No broken cross-references introduced: grep all `.claude/` files for any pointer to "completion summary" or other removed phrasings

---

## What NOT to Do

- **Don't** edit `dashboard-regeneration.md`, `decisions.md`, `workflow.md`, `phase-decision-gates.md`, `commands/research.md`, or `rules/decisions.md` in this batch. They're listed in Scope's "Out of scope" section.
- **Don't** restructure `phase-decision-gates.md` into "caller checklist" vs "full procedure" sections. Optional follow-up only.
- **Don't** lower the FB-036 threshold below 3. Setting it at 2 would friction every parallel run; the value is in catching the full-budget cases.
- **Don't** add the FB-036 confirmation to sequential dispatch. The FB is specifically about parallel-batch over-eagerness.
- **Don't** rewrite the existing Step 2b (phase check, ambiguity handling, research dispatch) — only add the inline-trigger block.
- **Don't** reduce or expand the FB-027 paragraph beyond a clear "one-sentence-diff = skip planning" rule. The Scope-significance paragraph that already exists provides the complementary "what counts as significant" framing.
- **Don't** touch `.claude/version.json` — Phase 5 cleanup handles version-bump scope once total change tally is known.
- **Don't** archive any FB items in `feedback.md` — same convention as the FB-037 commit (Phase 5 will define the direct-implementation archive convention).
- **Don't** edit `commands/iterate.md` to also run the FB-017 detection (FB-017's item #4 mentions this) — separate file, separate batch.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Tracker | `template-upgrade-2026-04.md` (root) |
| Source feedback items | `.claude/support/feedback/feedback.md` (FB-015 line 43, FB-017 line 16, FB-027 line 142, FB-036 line 280) |
| Primary target | `.claude/commands/work.md` (~950 lines) |
| Mirror target | `.claude/support/reference/parallel-execution.md` (FB-036 only) |
| Algorithm reference (FB-017) | `.claude/support/reference/phase-decision-gates.md` § "Decision Dependency Check" |
| Auto-finalization promises (FB-017 audit, no edit expected) | `.claude/support/reference/decisions.md` line 151, `.claude/support/reference/workflow.md` lines 195-201 |
| Deferred FB-015 primary | `.claude/support/reference/dashboard-regeneration.md` § "Action Item Contract" (lines ~322-331) |
| Deferred FB-027 alt-sites | `.claude/commands/research.md`, `.claude/rules/decisions.md` |

---

## Post-Commit: What Happens Next

After commit:
- Tracker shows `commands/work.md` row `[x]` in Phase 4 hot-files.
- File Collision Map shows all four FB items struck through in the work.md row; FB-036 also struck in the parallel-execution.md row.
- FB-015 partial: work.md audit slice done; primary in `dashboard-regeneration.md` still open. The Phase 4 next-action note suggests it as the natural follow-on.
- FB-017, FB-027, FB-036 are functionally done from a user-flow perspective even though some alt-site reinforcement edits remain available.
- Erik chooses the next batch — do not pick autonomously. Suggested order in tracker Current State.
