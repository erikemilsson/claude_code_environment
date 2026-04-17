# Plan — Usage Insights Report Intake (Phase 2, usage-report bundle)

**Purpose:** Produce the candidate list from Erik's Claude Code usage insights report (`file:///Users/erikemilsson/.claude/usage-data/report.html`), collect Erik's per-item decisions, then capture approved/edited items into `.claude/support/feedback/feedback.md`. Mirror the format and conventions established in the committed best-practices intake.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Upstream:** Template upgrade tracker `template-upgrade-2026-04.md` — Phase 2
**Cleanup tag:** DELETE-AFTER (tracked in upgrade tracker's Cleanup Manifest)

---

## Context to Load Before Executing

Read in this order at session start:

1. **`template-upgrade-2026-04.md`** — tracker. Confirm **Current State** reads "Phase 2 — usage-report bundle remaining". Read the most recent Session Log entry ("Phase 2 best-practices intake") — it gives you the pattern and the open-research-item anchors (FB-020, FB-026) you'll need for cross-referencing.
2. **`upgrade-candidates-best-practices.md`** — the committed best-practices candidate list. **This is your format exemplar.** Your usage-report candidate list must mirror it: same four sections (A/B/C/D), same per-candidate shape (Description / Impact scope / Relevance rationale / Decision line), top note on preemptively dropped items, "Already covered in template" section at the bottom. Do not invent a different format.
3. **`.claude/support/feedback/feedback.md`** — tail-read FB-019 through FB-031 to see the capture format you'll use for approved items. Match it (compact: Source line + body + Impact scope + Why).
4. **Auto-memory (already loaded)** — two relevant entries should be in your context from MEMORY.md: the candidate-list format convention, and the Opus 4.7 + 1M + Max-plan filtering principle. If those aren't present, something went wrong with memory — pause and tell Erik before continuing.

Then execute this plan.

---

## Source and Output

- **Source:** `file:///Users/erikemilsson/.claude/usage-data/report.html` — Erik's personal Claude Code usage insights report. Fetch with **WebFetch** using a structured-extraction prompt (see "Execution Steps" below). This is a local file URL; WebFetch supports `file://`.
- **Output file:** `upgrade-candidates-usage-report.md` at **project root** (not `.claude/support/workspace/` — that's template content). Tagged DELETE-AFTER. Its Cleanup Manifest entry is already in the tracker.

---

## Preemptive Filter Rules

Apply before listing any candidate. Call out what was dropped in a top note so Erik can override.

1. **Opus 4.7 + 1M context absorbs 200K-era concerns.** If a report insight boils down to "your CLAUDE.md is bloated / your context fills too fast / compaction is triggering", drop or demote. Erik's context budget is 1M and degradation is graceful below ~700K. Same for IMPORTANT/YOU MUST emphasis tricks — Opus 4.7 follows clear instructions without them.
2. **Max plan has auto mode since mid-April 2026.** If the report surfaces permission-prompt friction, route to **FB-026** (open research item on permissions/auto-mode reevaluation; potential DEC-008) rather than proposing a new direct fix. Mark as "overlaps with FB-026 — likely absorbs."
3. **Template is personal-use only.** Reject team-collaboration shapes (shared notes, multi-user workflows, `.local`-style per-user files). Erik rejected `CLAUDE.local.md` on these grounds during best-practices intake.
4. **Domain-agnostic template.** Reject insights tied to specific domains (UI/frontend, specific SaaS, specific languages) unless they generalize. The template must work for software, research, procurement, and renovation projects equally.
5. **Template content vs. user behavior.** Reject meta-advice that belongs in upstream Claude Code docs (course-correction keys, general prompt-engineering tips). Keep items that affect template files, rules, commands, or conventions.

---

## Cross-Reference Existing Feedback (absorb, don't duplicate)

Usage-report findings often overlap with existing feedback. When a candidate matches an existing item, **do not create a new FB-NNN** — instead, flag it in the candidate's Decision line as "overlaps with FB-NNN — route through triage as absorb candidate." Existing anchors:

- **FB-011** — scripts as alternative to commands/skills (deterministic automation)
- **FB-015** — Action Required dashboard cleanup (informational clutter)
- **FB-017** — `/work` Step 2b decision checkbox detection reliability
- **FB-020** — Skills architectural research (sub-agent context-window concern; research-first; candidate DEC-007)
- **FB-026** — permissions / auto-mode reevaluation (inflection-point candidate; may impact DEC-005; candidate DEC-008)

If the usage report surfaces, e.g., "you're spending lots of time on permission prompts" → absorb into FB-026. "You re-read the dashboard often" → absorb into FB-015. If a finding is genuinely novel, create a new FB-NNN starting from **FB-032**.

---

## Execution Steps

### Step 1: Fetch the report

Use WebFetch with this structured-extraction prompt (adapt as needed):

```
Extract every actionable insight, recommendation, or observed inefficiency
from this Claude Code usage report. For each, give:

1. Short title (5-8 words)
2. The insight / recommendation (1-3 sentences, faithful to the report —
   include the underlying data point if the report quantifies it, e.g.,
   "48% of sessions exceed 200K tokens")
3. The category (context management, tool use, workflow, permissions,
   automation, commands, subagents, cost, other)
4. Any specific Claude Code feature/command/setting referenced

Also extract:
- Any explicit recommendations the report makes to the user
- Any patterns the report surfaces as "you could improve by..."
- Any anomalies the report flags (unusual patterns, unused features,
  high-cost operations)

Return as a numbered list. Be exhaustive — include all insights even if
they seem minor. If the report has multiple sections, walk through each
one completely.
```

Verify the WebFetch succeeded against a `file://` URL. If it fails, try Bash `cat` to read the HTML then parse locally.

### Step 2: Apply the preemptive filter

Walk each extracted insight through the five filter rules. Keep a running list of what you dropped and why — this becomes the top note.

### Step 3: Group remaining candidates into A/B/C/D

- **A** — template/architecture changes (new directories, schema changes, agent-contract changes)
- **B** — doc and rules tweaks (new sections in existing rules/docs, no behavioral change)
- **C** — user-facing tips and setup (README additions, setup-checklist items, automation hints)
- **D** — preemptively rejected, 1-line reasons

### Step 4: Cross-reference for overlap

For each A/B/C candidate, check against FB-011/015/017/020/026. Mark overlaps in the Decision line.

### Step 5: Write `upgrade-candidates-usage-report.md` at project root

Structure (mirror best-practices file exactly):

```markdown
# Upgrade Candidates — Claude Code Usage Insights Report

**Source:** file:///Users/erikemilsson/.claude/usage-data/report.html (fetched 2026-04-17)
**Tag:** DELETE-AFTER (cleanup in Phase 5)
**Status:** Awaiting per-item user review

---

## How to use this file
[Same intro as best-practices file]

> **Note:** [Top note listing preemptively dropped insights with 1-line reasons]

---

## A. Template / architecture changes
[Candidates with Description / Impact scope / Relevance rationale / Decision line]

## B. Doc and rules tweaks
[...]

## C. User-facing tips and setup
[...]

## D. Preemptively rejected (override if you disagree)
[1-line reasons]

---

## Already covered in template (no action needed)
[Transparency section — insights confirmed already addressed, with pointers to where]
```

### Step 6: Present to Erik

Offer to open the file on his Mac (`open <path>`). Pause for him to mark decisions. Do not capture anything yet.

### Step 7: After Erik marks decisions — capture approved + edited items

Append to `.claude/support/feedback/feedback.md`, continuing from **FB-032**. Use the same compact format as FB-019–FB-031: `## FB-NNN: Title` / `**Status:** new` / `**Captured:** 2026-04-17` / Source line / body / Impact scope / Why.

- For items marked "overlaps with FB-NNN" — do **not** capture as new. The Decision is the routing note; next `/feedback review` absorbs during triage.
- For items marked with edits that convert them into research/decision-flavored questions (like FB-020 and FB-026 did during best-practices intake), write the body to reflect that framing: enumerate the questions to answer, note likely decision-record candidacy.

### Step 8: Update the tracker

- **Session Log:** append entry for "Phase 2 usage-report intake"
- **Current State:** "Phase 2 intake complete — `/feedback review` triage next"
- **Phase 2 usage-report checkboxes:** mark `[x]`
- **File Collision Map:** populate "Usage" column with `**Assessed:**`-style entries per captured item (tracker instructs this in Phase 2 description)

### Step 9: Commit

One commit per logical unit per tracker's commit cadence ("each new-input bundle"). Suggested title:

```
Phase 2: usage-report intake — N candidates captured (FB-032 through FB-0NN)
```

Follow the structure of the best-practices intake commit (`9eaad76`) for the message body: list each FB-NNN, note any routed-as-absorb items, note what was preemptively dropped.

### Step 10: Hand off

After commit, Phase 2's remaining work is `/feedback review` triage:
- Check overlap with existing `ready` items (FB-011, FB-015, FB-017 especially; also FB-020 and FB-026 for usage-report absorbs)
- Absorb duplicates (mark `absorbed_into`)
- Update **File Collision Map** with new `**Assessed:**` entries
- Decide which new items need `/research` (Phase 3) vs direct implementation (Phase 4)

Tell Erik Phase 2 is done and offer to start `/feedback review` triage immediately or defer.

---

## What NOT to Do

- **Don't** write the candidate file to `.claude/support/workspace/` — that's template content. Use project root.
- **Don't** re-derive format conventions from scratch. Mirror `upgrade-candidates-best-practices.md` exactly.
- **Don't** trigger the full `/feedback` skill per capture — that interactive 3-phase flow isn't what we want. Direct append to `feedback.md` matches FB-019–FB-031.
- **Don't** commit before Erik marks decisions. Capture happens after review.
- **Don't** create new FB items for findings that overlap with FB-011/015/017/020/026 — route as absorbs.
- **Don't** forget the "Already covered in template" section — Erik asked for it for transparency during best-practices intake.
- **Don't** preemptively reject silently. Every drop gets a 1-line reason either in the top note or the D section.

---

## Verification Checklist (post-output, pre-presentation)

- [ ] Candidate file exists at project root (`upgrade-candidates-usage-report.md`)
- [ ] Top note lists preemptively dropped items with reasons
- [ ] Every candidate has Description + Impact scope + Relevance rationale + Decision line
- [ ] D section entries each have a 1-line reject reason
- [ ] Overlapping candidates flagged with "overlaps with FB-NNN" in their Decision line (not duplicated)
- [ ] "Already covered in template" section at the bottom
- [ ] No new files written to `.claude/support/workspace/`
- [ ] Next FB-NNN is FB-032 (confirm by grepping `feedback.md` and `archive.md` for highest existing ID)

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Tracker | `template-upgrade-2026-04.md` (root) |
| Best-practices exemplar | `upgrade-candidates-best-practices.md` (root) |
| Feedback inbox | `.claude/support/feedback/feedback.md` |
| Feedback archive | `.claude/support/feedback/archive.md` |
| Feedback command definition (reference only — don't invoke) | `.claude/commands/feedback.md` |
| Root CLAUDE.md (template maintenance context) | `./CLAUDE.md` |
| Environment CLAUDE.md (rules that apply to this template when it runs as a project) | `.claude/CLAUDE.md` |
