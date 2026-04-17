# Plan — commands/iterate.md Batch (FB-021 + FB-032 + FB-017 detection)

**Purpose:** Upgrade `/iterate` on three fronts: (1) AskUserQuestion-driven interview in `distill` (FB-021); (2) mandatory "Decisions in This Proposal" output contract in `propose` (FB-032); (3) mirror the checkbox-detection trigger so `/iterate` also auto-finalizes checked decisions (FB-017 item #4, mentioned in the Assessed line as "`/iterate` should also run this detection").

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Source feedback items:** FB-021 (line 71), FB-032 (line 210), FB-017 (line 16) in `.claude/support/feedback/feedback.md`
**Related decisions:** none directly; FB-032 is the gate-lifting work for FB-033's future trial.
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in same commit as this plan)
**Tracker status line to advance:** `Phase 4 — iterate.md group implemented (FB-021 + FB-032 + FB-017 detection mirror); FB-033 trial-gate unblocked`

---

## Scope

| Item | Touch site | Edit type |
|------|-----------|-----------|
| FB-017 (secondary) | `iterate.md § "Step 1"` or new § "Step 1a" | New procedure block mirroring work.md Step 2b checkbox detection |
| FB-021 | `iterate.md § "Step 2 distill"` Step 3 (Ask distillation questions) | Restructure to use `AskUserQuestion` tool |
| FB-032 | `iterate.md § "Step 4: Propose Changes"` + Step 5 gating | New mandatory `## Decisions in This Proposal` section at end of declaration + Step 5 gate |

Secondary touches:
- `rules/spec-workflow.md § "Propose-Approve-Apply"` — add one sentence making the FB-032 contract visible at the rules layer
- OPTIONAL: `agents/verify-agent.md` Per-Task Workflow — add a matching check for spec-change tasks that verifies the Decisions section was present. DEFER this to the agents batch (verify-agent is hot there too) — leave a note in the tracker.

### Out of scope

- Touch of `phase-decision-gates.md` (the FB-017 algorithm reference stays as-is; `/iterate` inlines the same imperative trigger that work.md Step 2b got)
- Verify-agent matching check for FB-032 — defer to agents batch
- `decisions.md` / `workflow.md` audit (FB-017 Assessed line mentions these; expected no edit needed post work.md inlining; re-verify at end of this batch)

---

## Context to Load Before Executing

1. **`.claude/commands/iterate.md`** — full file (~470 lines). All three primary edits land here. Load once.
2. **`.claude/commands/work.md` lines 340–361** — the inlined checkbox-detection block from the recent work.md hot-file batch. Mirror its structure verbatim in `/iterate` so the two entry points behave identically.
3. **`.claude/support/reference/phase-decision-gates.md § "Decision Dependency Check"`** — confirm anchors.
4. **`.claude/support/feedback/feedback.md`** lines 16–50 (FB-017), 71–83 (FB-021), 210–224 (FB-032) — confirm Assessed lines haven't drifted.
5. **`.claude/rules/spec-workflow.md`** — locate the Propose-Approve-Apply section for the FB-032 rules-layer addition.
6. **`template-upgrade-2026-04.md`** — Current State, File Collision Map `commands/iterate.md` + `rules/spec-workflow.md` rows.

Auto-memory: no specific entry is load-bearing.

---

## Implementation Steps

### Step 1: FB-017 — Mirror the checkbox-detection trigger in /iterate

Locate `## Process → Step 1: Load Context` in `commands/iterate.md` (lines 27–30). Step 1 currently reads the spec and assesses its state.

**Insert a new sub-section immediately after Step 1 and before Step 1b:**

```markdown
### Step 1a: Auto-Finalize Checked Decisions

Before assessing spec state, scan for unresolved-but-checked decisions. This mirrors `/work` Step 2b's inline trigger — both entry points to spec-adjacent work must fire the auto-finalization algorithm.

For every `decision-*.md` file with frontmatter `status: proposed`:

1. Read the file's `## Select an Option` section
2. Scan for checked boxes — match `[x]`, `[X]`, `[✓]`, `[✔]` (per the normalization in `phase-decision-gates.md § "Phase Check"`)
3. If a checked box is found AND frontmatter `status` is still `proposed`:
   - Extract the selected option name (text after `[x] ` on the matched line)
   - Update frontmatter: `status: approved`, `decided: <today's YYYY-MM-DD>`
   - Populate the Decision section using the option name and matching Option Details rationale
   - Run the Post-Decision Check (`phase-decision-gates.md § "Post-Decision Check"`) — handles inflection-point pause
   - Log: `Decision {DEC-ID} resolved → status updated to 'approved' (selected: {option_name})`
4. If no checked boxes are found across all proposed decisions, proceed to Step 1b without changes.

This step MUST run on every `/iterate` invocation. It is the caller's responsibility — `phase-decision-gates.md` defines the algorithm; `/iterate` Step 1a is what fires it. This prevents the case where the user checks a decision and runs `/iterate` (not `/work`) and the decision stays `proposed`.
```

---

### Step 2: FB-021 — AskUserQuestion-driven interview in distill

Locate `## Step 2: Determine Mode → If user specified /iterate distill:` (lines 50–134). Sub-step 3 "Ask distillation questions" currently presents a flat 4-question block.

**Restructure sub-step 3 to use `AskUserQuestion`:**

Replace the current sub-step 3 (the `Let's extract a buildable Phase 1 spec.` block with its flat numbered list) with:

```markdown
3. **Structured distillation interview (`AskUserQuestion`):**

   Use the `AskUserQuestion` tool to surface decisions rather than passively extracting them from the vision doc. Submit at most 4 questions per call, up to two calls total (8 questions max). For each question, provide 2–4 suggested answers derived from the vision doc plus an "Other" escape option.

   Question types to cover (pick 4 per call based on which surface the biggest gaps):

   - **Core value proposition:** "What's the single most important outcome for a user in Phase 1?" with suggested answers extracted from vision themes.
   - **Scope boundary:** "Which of these vision items are in Phase 1?" with options: all / MVP subset / deferred to future phases.
   - **User and critical path:** "Who's the first user and what's their happy path?" with persona options.
   - **Implementation-or-UX tradeoffs:** surface tradeoffs Claude noticed but the vision didn't resolve.
   - **Edge cases the vision didn't cover:** flag specific gaps (e.g., "Vision mentions data ingestion but not what happens on malformed input — which of these matches your intent?").
   - **Explicit non-goals:** "What's explicitly NOT in Phase 1?" with suggested exclusions.

   The structured format forces Claude to surface decisions — a flat text question lets Claude accept any answer and silently interpret it; a structured question with explicit options forces each decision to become visible.

   After the user answers, proceed to sub-step 4 (Carry structure through from vision doc).
```

---

### Step 3: FB-032 — Decisions in This Proposal contract in Step 4

Locate `### Step 4: Propose Changes (Change Declaration)` (lines 214–255). The current template ends with `Approve these changes? [Y] Apply all | ...`.

**Extend the declaration template (at the end, after the `---` and before the Approve line) with a mandatory new section:**

Replace the code block from `## Proposed Spec Changes` through `Approve these changes? ...` with:

```markdown
## Proposed Spec Changes

Based on your answers, here's what I'd change:

### Change 1: [Section name] — [add | modify | remove]

**Location:** spec_v{N}.md § [section path]
**What changes:** [Brief description of the change and why]
**Proposed text:**

> [The proposed new/modified section content]

### Change 2: [Section name] — [add | modify | remove]

**Location:** spec_v{N}.md § [section path]
**What changes:** [Brief description]
**Proposed text:**

> [The proposed content]

---

## Decisions in This Proposal

MANDATORY section — every spec-change proposal must end with this list. Enumerate every non-trivial choice embedded in the proposal and tag each:

- `[NEEDS APPROVAL]` — a design choice Claude made that the user has not explicitly approved (e.g., chose library X over Y, structured section Z as a table)
- `[FROM EXISTING SPEC]` — a decision already present in the current spec that the proposal inherits
- `[USER REQUESTED]` — a decision the user explicitly asked for in this conversation or a prior one

**Format:**
- [ ] `[NEEDS APPROVAL]` Chose table layout for acceptance criteria section — rationale: easier to scan than prose list
- [x] `[USER REQUESTED]` Added "Deferred to Future Phases" section per user ask
- [x] `[FROM EXISTING SPEC]` Retained phased structure from spec_v{N-1}

Rule: every `[NEEDS APPROVAL]` item MUST be resolved before Step 5 applies changes. If no decisions were made (rare — only for trivial wording changes), write `No non-trivial decisions — all changes are mechanical`.

---

Approve these changes? [Y] Apply all | [M] Modify (tell me what to adjust) | [P] Partial (pick which changes) | [N] Skip
```

### Step 3b: FB-032 gate in Step 5

Locate `### Step 5: Apply or Continue` (line 257). Add a new gate at the top of Step 5.

**Prepend this paragraph to Step 5:**

```markdown
**Mandatory gate — Decisions resolved:** Before applying, verify the `## Decisions in This Proposal` section has zero unchecked `[NEEDS APPROVAL]` items. If any remain unresolved, block apply and ask the user to resolve each. This rule applies even to `[Y] Apply all` — the `[NEEDS APPROVAL]` items must be checked first.
```

---

### Step 4: FB-032 rules-layer addition

Locate `.claude/rules/spec-workflow.md § "Propose-Approve-Apply"` (sole paragraph in that section).

**Append this sentence at the end of the Propose-Approve-Apply paragraph:**

```markdown
Every spec-change proposal must end with a `## Decisions in This Proposal` section enumerating each non-trivial choice tagged `[NEEDS APPROVAL]`, `[FROM EXISTING SPEC]`, or `[USER REQUESTED]`. `/iterate` does not proceed to apply until every `[NEEDS APPROVAL]` item is resolved — this makes silent Claude-inferred decisions visible before they land in the spec.
```

---

### Step 5: Tracker bookkeeping

Update `template-upgrade-2026-04.md`:

**5a. Status line:** → `**Status:** Phase 4 — iterate.md group implemented (FB-021 + FB-032 + FB-017 detection mirror); FB-033 trial-gate unblocked; remaining direct items next`

**5b. Current State:** add new bullet:

```
- **iterate.md group implemented 2026-04-17:** `/iterate` Step 1a now inlines the same checkbox-detection trigger that work.md Step 2b got — the FB-017 fix applies at both entry points, closing the gap where running `/iterate` (not `/work`) on checked decisions left them `proposed`. Distill mode's sub-step 3 restructured to use `AskUserQuestion` for structured interview (FB-021) — explicit option lists force decisions to be visible instead of accepting flat text and silently interpreting. Step 4's change declaration now ends with a mandatory `## Decisions in This Proposal` section tagging each non-trivial choice `[NEEDS APPROVAL]` / `[FROM EXISTING SPEC]` / `[USER REQUESTED]`; Step 5 gates apply on zero-unchecked `[NEEDS APPROVAL]` (FB-032). `rules/spec-workflow.md § "Propose-Approve-Apply"` gains one sentence making the contract visible at the rules layer. Unblocks FB-033 trial-gate data generation.
```

**5c. Next action bullet:** update.

**5d. Phase 4 Hot files block:** flip the commands/iterate.md line to `[x]`.

**5e. File Collision Map:** strike-through the relevant cells in the `commands/iterate.md` and `rules/spec-workflow.md` rows:
- `commands/iterate.md`: FB-017 detection → `~~FB-017 Step 1a inlined~~ ✓`; FB-021 distill interview → `~~FB-021 AskUserQuestion restructure~~ ✓`; FB-032 propose output contract → `~~FB-032 Decisions section + Step 5 gate~~ ✓`
- `rules/spec-workflow.md`: FB-032 propose-approve-apply → `~~FB-032 rules-layer sentence~~ ✓`

**5f. Cleanup Manifest:** add row:
```
| `plan-iterate-batch.md` | DELETE-AFTER | commands/iterate.md group (FB-021 + FB-032 + FB-017 detection mirror) implementation plan for fresh-session execution |
```

**5g. Session Log entry:** append with Done / Judgment calls / Next / Open questions format, mirroring the prior entries. Judgment calls should cover: (1) why `/iterate` Step 1a mirrors work.md Step 2b verbatim rather than pointing to a shared reference (call-site explicitness is the whole point of FB-017's fix); (2) why the AskUserQuestion restructure keeps the existing question archetypes rather than replacing them wholesale (the archetypes are good; the tool choice is the change); (3) why the `## Decisions in This Proposal` section is in the declaration template rather than a separate post-declaration step (single artifact, single approval point).

---

### Step 6: Commit

Single commit. Pre-commit hook will warn about `version.json` (`commands/iterate.md` and `rules/spec-workflow.md` are sync-category).

Commit message (HEREDOC):

```
Phase 4: commands/iterate.md group — FB-017 mirror + FB-021 + FB-032

FB-017 (secondary — caller mirror): new § "Step 1a: Auto-Finalize
Checked Decisions" added to commands/iterate.md, mirroring the
checkbox-detection trigger inlined into work.md Step 2b. Closes the
gap where running /iterate (not /work) on freshly-checked decisions
left them `proposed`. Both entry points now fire the algorithm.

FB-021 (AskUserQuestion in distill): distill sub-step 3 restructured
to use the AskUserQuestion tool for structured interview. Questions
carry explicit option lists (with "Other" escape); up to 8 questions
max across two tool calls. Forces decisions to be visible rather than
accepted as free-text and silently interpreted. Question archetypes
(value prop, scope boundary, users, tradeoffs, edge cases, non-goals)
retained as a guide for question selection.

FB-032 (Decisions in This Proposal): Step 4's change declaration
template extended with a mandatory final "## Decisions in This
Proposal" section tagging each non-trivial choice [NEEDS APPROVAL],
[FROM EXISTING SPEC], or [USER REQUESTED]. Step 5 gates apply on
zero-unchecked [NEEDS APPROVAL] items. `rules/spec-workflow.md §
"Propose-Approve-Apply"` gains one sentence surfacing the contract
at the rules layer. Unblocks FB-033's trial-gate data generation
(FB-033 is deferred until /iterate runs on real projects under
this contract).

Verify-agent matching check for FB-032 (verify spec-change tasks
include a Decisions section) deferred to the agents batch — fits
naturally with the other verify-agent updates.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Verification Checklist (post-edit, pre-commit)

- [ ] `iterate.md` has new `### Step 1a: Auto-Finalize Checked Decisions` between Step 1 and Step 1b
- [ ] Step 1a enumerates: scan proposed files, normalize checkbox forms, update frontmatter (`status: approved` + `decided` date), populate Decision section, run post-decision check, emit log line
- [ ] `iterate.md § "Step 2 distill"` sub-step 3 uses `AskUserQuestion` (verify by Grep `AskUserQuestion` in iterate.md — must match)
- [ ] `iterate.md § "Step 4: Propose Changes"` declaration template ends with a mandatory `## Decisions in This Proposal` section (verify by Grep `Decisions in This Proposal` — must be in iterate.md and also in spec-workflow.md)
- [ ] `iterate.md § "Step 5: Apply or Continue"` opens with the "Mandatory gate — Decisions resolved" paragraph
- [ ] `rules/spec-workflow.md § "Propose-Approve-Apply"` paragraph ends with the new sentence about the Decisions section contract
- [ ] No edits to `phase-decision-gates.md`, `decisions.md`, `workflow.md`, or any other file outside the two above + tracker
- [ ] Tracker: status line, Current State, Phase 4 Hot files `[x]`, File Collision Map strikes, Cleanup Manifest row, Session Log entry
- [ ] Pre-commit hook output shows `version.json` warning (expected)

---

## What NOT to Do

- **Don't** edit `phase-decision-gates.md` — the algorithm is already correct; the failure mode is caller-side. FB-017's fix at both callers is the right shape.
- **Don't** add the verify-agent matching check for FB-032 in this batch — defer to the agents batch so all verify-agent edits land together.
- **Don't** replace `iterate.md`'s existing question archetypes during the FB-021 restructure — the archetypes are the content; `AskUserQuestion` is the delivery mechanism.
- **Don't** expand the `## Decisions in This Proposal` format beyond 3 tag types — the simplicity is the point.
- **Don't** gate Step 5's `[N] Skip` on zero-unchecked `[NEEDS APPROVAL]` — the gate only applies to apply (Y / M / P paths). Skipping abandons the proposal entirely.
- **Don't** bump `.claude/version.json` — Phase 5 handles scope.
- **Don't** archive FB items in `feedback.md` — same convention as prior direct-implementation items.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Primary target | `.claude/commands/iterate.md` (~470 lines) |
| Rules-layer target | `.claude/rules/spec-workflow.md` |
| Algorithm reference (FB-017) | `.claude/support/reference/phase-decision-gates.md § "Decision Dependency Check"` |
| Mirror source (FB-017) | `.claude/commands/work.md` lines 340–361 (the block inlined in the recent batch) |
| Tracker | `template-upgrade-2026-04.md` (root) |
| Source feedback | `.claude/support/feedback/feedback.md` (FB-017 line 16, FB-021 line 71, FB-032 line 210) |

---

## Post-Commit: What Happens Next

- Tracker shows `commands/iterate.md` row `[x]` in Phase 4 hot-files.
- FB-032 contract is now in-force; FB-033 gains trial data as real `/iterate` sessions run under the contract.
- Verify-agent matching check for FB-032 still outstanding (tracked for agents batch).
- FB-017 fully complete (primary in work.md + secondary mirror in iterate.md).
- Erik chooses the next batch — do not pick autonomously.
