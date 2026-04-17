# Plan — Feedback Review Triage (Phase 2 close, upgrade tracker)

**Purpose:** Triage the 19 `new`-status feedback items captured across the best-practices and usage-report intakes (FB-019 through FB-037), absorb duplicates, route items to Phase 3 (needs research) or Phase 4 (direct implementation), and update the upgrade tracker. Close Phase 2.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Upstream:** `template-upgrade-2026-04.md` — Phase 2 close
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in the same commit as this plan)

---

## Context to Load Before Executing

Read in this order at session start:

1. **`template-upgrade-2026-04.md`** — tracker. Confirm **Current State** reads *"Phase 2 intake complete — `/feedback review` triage next"*. Read the two most recent Session Log entries ("Phase 2 best-practices intake" and "Phase 2 usage-report intake") for the full item context. Note the **File Collision Map** — Best-prac and Usage columns are mostly TBD; this triage step is what populates them with `**Assessed:**`-style entries.
2. **`.claude/support/feedback/feedback.md`** — current inbox. Will contain the following `new`-status items to triage: FB-019–FB-031 (best-practices intake), FB-032–FB-037 (usage-report intake). Also contains carryover `ready` items from before the upgrade: FB-010, FB-011, FB-012, FB-013, FB-015, FB-017 — some of these may already be absorbed by DEC-004/005/006 but still sit in `feedback.md` with `ready` status.
3. **`.claude/support/feedback/archive.md`** — terminal items. Tail-read to see the archive format and ensure you don't create ID collisions if something gets archived during triage.
4. **`.claude/commands/feedback.md`** — the command definition. Reference for procedure (3-phase review: grouping → refinement → impact assessment). Do NOT invoke the command interactively; run the triage directly, consistent with how the intake captures were done (direct append, not command invocation).
5. **`decisions/` folder at root** — read `decision-004-*.md`, `decision-005-*.md`, `decision-006-*.md` briefly to confirm which existing `ready` items are already absorbed by a closed decision and should move to `archive.md` with `status: absorbed` + `absorbed_into: DEC-NNN`. Also scan for any DEC-007/008/009 stubs (unlikely yet — these are candidates, not created records).
6. **Auto-memory (already loaded via MEMORY.md)** — three relevant entries will be in context: template-decisions-at-root, candidate-list-format, Opus-4.7-+-Max-auto-filtering. If those aren't present something went wrong — pause before triaging.

Then execute this plan.

---

## Triage Goals

Each `new`-status item needs one of these outcomes:

- **`absorbed`** — duplicate of another item or covered by a closed decision. Move to `archive.md` with `absorbed_into: FB-NNN` or `absorbed_into: DEC-NNN`. Mark reason.
- **`closed`** — investigated, decided against. Move to `archive.md` with reason.
- **`archived`** — not relevant (quick triage reject). Move to `archive.md` with 1-line reason.
- **`ready`** — approved for implementation. Stays in `feedback.md` with `status: ready`. Adds a `**Assessed:**` line documenting impact scope + classification (Phase 3 research vs Phase 4 direct implementation).
- **`refined`** — needs further refinement before it's actionable. Stays in `feedback.md` with a refinement note (usually means you want to narrow scope or ask a question).

Existing `ready`-status carryover items (FB-010, FB-011, FB-012, FB-013, FB-015, FB-017) should also be re-examined: some may now be `absorbed` by a closed decision.

---

## Pre-Analysis (Use as Triage Hints, Not Prescriptions)

These overlap/routing hints were identified during capture but **not yet resolved**. Confirm each during triage — some may turn out different under closer examination.

### Existing `ready` items: likely archive candidates

- **FB-010** (subagents can't write `.claude/tasks/`) — explicitly absorbed by DEC-004 per the commit trail (`55c1040`, `cb7fbc4`). Confirm by reading DEC-004 then move to `archive.md` with `absorbed_into: DEC-004` and a brief reason.
- **FB-012** (standardized base allowedTools) — absorbed by DEC-005 (`3cb10d8`). Confirm and archive with `absorbed_into: DEC-005`.
- **FB-013** (cross-phase parallel tasks) — absorbed by DEC-006 (`6cf4ba2`). Confirm and archive with `absorbed_into: DEC-006`.
- **FB-011** (scripts as alternative) — still `ready`, not yet absorbed. Direct implementation candidate for Phase 4. Keep.
- **FB-015** (Action Required dashboard cleanup) — still `ready`. Direct implementation candidate for Phase 4. Keep.
- **FB-017** (`/work` Step 2b checkbox detection) — still `ready`. Partially depends on FB-011 (script extraction). Direct implementation for Phase 4 (possibly in the same implementation unit as FB-011).

### New items (FB-019–FB-037): overlap checks

- **FB-020 + FB-033 (spec-auditor)** — not duplicates. FB-020 is Skills architectural research (the general question). FB-033 is a specific use-case (adversarial review of spec writes) gated on FB-032's trial. Keep both; note that FB-033 depends on FB-020 closing.
- **FB-021 (AskUserQuestion in `/iterate distill`) + FB-032 (Decisions section in `/iterate propose`)** — complementary, not duplicate. Both touch `commands/iterate.md` but different subcommands. Keep both.
- **FB-026 + FB-037 (PreToolUse hook)** — complementary. FB-026 is the architectural permissions reevaluation (candidate DEC-008). FB-037 is a specific opt-in hook recipe that's deferred until FB-026 resolves. Keep both; FB-037's `**Assessed:**` should note the dependency.
- **FB-028 + FB-037 (both touch `setup-checklist.md`)** — same file, different subsections (CLI installs vs. optional hooks). Not duplicates. Note in File Collision Map that the file has two Usage-column entries.
- **FB-034 + FB-036 (over-eager execution)** — related, not duplicates. FB-034 is reactive (after a kill); FB-036 is proactive (before dispatch). Consider whether to implement as one rule set in `rules/agents.md` or separately — triage-time judgment call.
- **FB-029 + FB-030 (`claude -p` and fan-out)** — FB-030 uses `claude -p` as its primitive. Consider whether to absorb FB-030 into FB-029 as a sub-section, or keep separate. Triage judgment call — if both want the same doc file (`support/reference/automation.md`), absorbing may cleaner.
- **FB-023 + FB-024 + FB-025 (session-management doc additions: `/btw`, `/rewind`, `/rename`)** — three small doc tweaks to the same file (`rules/session-management.md`). Consider whether to leave as three items or absorb into one bundle item. Triage judgment call — keeping separate preserves individual opt-in, bundling reduces implementation friction.

### Research-flavored items (Phase 3 candidates)

- **FB-020** — Skills architectural research → candidate DEC-007
- **FB-026** — permissions/auto-mode reevaluation → candidate DEC-008 (inflection-point; may reverse parts of DEC-005)
- **FB-033** — spec-auditor (trial-gated on FB-032) → candidate DEC-009, but do NOT start research until FB-032 trial data exists

These are the Phase 3 scope. Note the ordering constraint: FB-026 research can start immediately; FB-020 research can start immediately; FB-033 research cannot start until FB-032 has been tried (Phase 4 → then Phase 3).

### Direct implementation candidates (Phase 4)

Baseline Phase 4 list (subject to triage refinement):
- FB-011, FB-015, FB-017 (existing `ready`)
- FB-019, FB-021, FB-022, FB-023, FB-024, FB-025, FB-027, FB-028, FB-029, FB-030, FB-031 (best-practices intake, direct)
- FB-032, FB-034, FB-035, FB-036 (usage-report intake, direct)
- FB-037 deferred — waits on FB-026 resolution (still `ready` but blocked)

---

## Execution Steps

### Step 1: Verify carryover items

For each of FB-010, FB-012, FB-013: confirm the absorbing decision is closed (status `approved` in frontmatter, `decided` date set). Read `decisions/decision-004-*.md`, `decisions/decision-005-*.md`, `decisions/decision-006-*.md` for verification. Move each confirmed item to `archive.md` with:

```markdown
## FB-NNN: [title]

**Status:** absorbed
**Captured:** [original date]
**Absorbed:** 2026-04-17
**Absorbed into:** DEC-NNN
**Reason:** [1-line — e.g., "DEC-004 implemented the subagent capability contract that addressed this item."]

[Preserve the original body]
```

Remove the entry from `feedback.md`.

### Step 2: Triage new items (FB-019–FB-037)

For each item, decide one of: `ready` / `refined` / `absorbed` / `closed` / `archived`. Use the pre-analysis above as hints. Update the status line in `feedback.md` and append:

```markdown
**Assessed:** 2026-04-17 — [impact scope: files affected, sections]. Scope: [corrective / additive / exploratory]. [Dependencies or overlap notes]. Route: [Phase 3 research / Phase 4 direct / deferred (reason)]. [Conflict flags if any — e.g., "Conflict: existing root CLAUDE.md section X requires consideration."]
```

Match the format of the existing `**Assessed:**` lines on FB-010/011/012/013/015/017 for consistency.

For items moved to `absorbed` / `closed` / `archived`: move to `archive.md`, remove from `feedback.md`.

### Step 3: Update File Collision Map

For each `ready` item, populate the Best-prac or Usage column entry on each affected file's row. Use short descriptors (e.g., `FB-032 propose output`, `FB-034 behavior + FB-035 Tool Prefs`) — not full `**Assessed:**` blocks, which go in `feedback.md`.

Add new rows for any files not already in the map. Look for hot-file promotions (3+ in-flight items).

**Files likely to need new rows:** `.claude/support/reference/automation.md` (new — from FB-029/FB-030 if approved), `.claude/support/reference/permissions.md` (new — from FB-026 research if approved).

### Step 4: Classify Phase 3 vs Phase 4

Populate the tracker's Phase 3 section (currently "TBD — populate after Phase 2 triage"). List:

- Each research item and its candidate DEC-NNN
- Ordering constraints (e.g., FB-033 research blocked on FB-032 trial)
- Cross-cutting concerns (e.g., FB-020 + FB-026 both affect settings/subagent architecture; worth noting whether they should share a research session)

Confirm Phase 4's existing list (FB-011, FB-015, FB-017) matches the triage outcome. Add new direct-implementation items.

### Step 5: Update tracker Current State and Session Log

- **Current State:** advance to *"Phase 2 complete — Phase 3 research scope determined"* (or similar, depending on triage outcome).
- **Session Log:** append entry for "Phase 2 triage". Include: items archived (carryover absorbs), items set to `ready`, items refined/closed/archived, Phase 3 research scope, Phase 4 direct-implementation count, any surprises or judgment calls.
- **Phase 2 final checkbox:** mark `[x]` the `/feedback review` triage sub-item.
- **Phase 3 section:** replace the TBD placeholder with the classified research list.

### Step 6: Commit

One commit per logical unit per the tracker's commit cadence. Suggested title:

```
Phase 2 close: triage FB-019 through FB-037 — N promoted to ready, M absorbed, P refined/closed
```

Body follows the pattern of `cb7fbc4` (Phase 2 prep) and `d5f5ce1` (usage-report intake): concise enumeration of changes with per-item reasoning.

### Step 7: Hand off

After commit, propose Phase 3 or Phase 4 as the next step:
- If Phase 3 research is needed (FB-020, FB-026 ready): offer to write research plans. These should probably NOT be fresh-session executions — research is iterative and benefits from keeping the conversation. But decision records go in root `decisions/` per the template-decisions-at-root memory rule.
- If Phase 4 direct implementation is ready (any items classified as Phase 4): offer to batch by file (per the tracker's implementation-grouping rule). Hot files first.

Ask Erik which to start with; do not assume.

---

## What NOT to Do

- **Don't** invoke `/feedback review` as an interactive 3-phase command. The tracker's triage blends the standard review with Phase-3/4 classification and File Collision Map updates — run it as a single pass with direct file edits, consistent with how FB-019–FB-037 were captured (direct append, no command invocation).
- **Don't** write triage decisions to memory. Memory is for things that persist across projects/conversations; this triage is ephemeral project-state already captured in feedback.md + tracker.
- **Don't** second-guess the three filters applied during intake (Opus 4.7, auto mode, best-practices). Those filters determined what got captured; during triage the only question is how captured items relate to each other and to the existing backlog.
- **Don't** silently absorb items without a reason. Every `absorbed` state needs an `absorbed_into` pointer + reason line.
- **Don't** create new feedback items during triage. Triage only processes what's already in the inbox. If a new idea surfaces, capture it separately via `/feedback [text]` after triage commits.
- **Don't** advance Current State past "Phase 2 complete" in a single commit. Phase 3 scope determination is the closing act of Phase 2, not the opening of Phase 3.

---

## Verification Checklist (post-triage, pre-commit)

- [ ] Every FB-NNN in `feedback.md` has a current `**Assessed:**` line (dated 2026-04-17) OR is ready for move to archive (in which case it's out of `feedback.md` entirely).
- [ ] Every item in `archive.md` added today has `absorbed_into` / reason per the status.
- [ ] No ID collisions between `feedback.md` and `archive.md`.
- [ ] File Collision Map Best-prac and Usage columns populated for every file that has a `ready` item pointing to it; no lingering `TBD` for files involved in `ready` work.
- [ ] Phase 3 section in tracker lists candidate DEC-NNN research items with ordering constraints.
- [ ] Phase 4 section lists direct-implementation items grouped by file (hot-files flagged).
- [ ] Current State reflects completion of Phase 2.
- [ ] Session Log entry appended.
- [ ] Phase 2 triage checkbox `[x]`.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Tracker | `template-upgrade-2026-04.md` (root) |
| Feedback inbox | `.claude/support/feedback/feedback.md` |
| Feedback archive | `.claude/support/feedback/archive.md` |
| Feedback command definition (reference only) | `.claude/commands/feedback.md` |
| Closed decisions | `decisions/decision-004-*.md`, `decisions/decision-005-*.md`, `decisions/decision-006-*.md` (root) |
| Candidate lists (DELETE-AFTER) | `upgrade-candidates-best-practices.md`, `upgrade-candidates-usage-report.md` (root) |
| Root CLAUDE.md (template maintenance) | `./CLAUDE.md` |
| Environment CLAUDE.md (template-owned) | `.claude/CLAUDE.md` |
