# Feedback Log

Items are captured via `/feedback` and triaged via `/feedback review`.

---

## FB-011: Explore scripts as alternative to commands or within skills folders

**Status:** ready
**Captured:** 2026-04-08
**Refined:** 2026-04-14 — Identify command procedures where a deterministic script would outperform LLM-executed natural-language instructions — starting with the dashboard, where output variation across regenerations makes the artifact harder to comprehend. Scripts could live alongside commands or inside skills folders if that's a valid pattern. Gains: (1) consistency of standardized artifacts, (2) reduced error rate from procedure drift, (3) lower token cost. Scope is exploratory — inventory candidates and propose which procedures to extract before committing.
**Assessed:** 2026-04-14 — Primary target is dashboard regeneration (touching `.claude/support/reference/dashboard-regeneration.md`, `.claude/rules/dashboard.md`, and call sites in implement-agent Steps 3, 6a, 6c). Shipping scripts needs a new home (likely `.claude/scripts/` — root `scripts/` is template-maintenance and does not ship). Conflict: `rules/agents.md` restricts Bash, and scripts depend on it — connects to FB-010 (subagent Bash sandbox limits). Dependencies: FB-017 (checkbox detection is a concrete second candidate). Scope: start with a workspace inventory doc (`.claude/support/workspace/scripts-candidates.md`) listing candidates with tradeoffs; first extraction targets dashboard regen.

Look into where scripts could be used instead of commands, or even perhaps as part of skills folders if that is a valid use-case. Needs to be more robust or save tokens or minimize errors, improve quality etc.

## FB-033: Spec-auditor subagent + PreToolUse gate (research-first; trial FB-032 first; candidate DEC-009)

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects new `.claude/agents/spec-auditor.md` (subagent, not Skill — resolved by DEC-007), hook wiring, verify-agent integration. Scope: exploratory. Research-first AND trial-gated on FB-032 (only pursue if the structural output contract proves insufficient after real `/iterate` sessions under Opus 4.7). FB-020 dependency resolved by DEC-007 (subagent is the correct home). FB-026 dependency resolved by DEC-008 (layered settings stay; hook wiring goes in `settings.local.json` if pursued). Route: Phase 3 research — **deferred** until FB-032 trial data exists (candidate DEC-009).

Source: Claude Code usage insights report (fetched 2026-04-17) — "On the Horizon" section proposes an adversarial-reviewer subagent that intercepts every `Write`/`Edit` to `spec*.md` or `decisions/*.md`. User edit on capture: *"wait until A1 is trialed properly before deciding"* — this item is explicitly gated on FB-032's trial outcome.

A bigger-hammer version of FB-032. The spec-auditor would diff each proposed change against the prior version, extract new assertions/decisions, cross-reference them against the current session's explicit user instructions, emit a "user-requested vs agent-inferred" table, and block the write until agent-inferred items are approved.

**Trial-gate:** Do not pursue until FB-032's structural output contract is trialed across several real `/iterate` sessions under Opus 4.7. If FB-032 materially reduces silent-decision friction, FB-033 is unnecessary. If FB-032 proves insufficient — silent decisions still slip through, or the output contract is bypassed — FB-033 becomes the structural backstop.

**Watch note (2026-07-19, harvest):** adjacent signal in the styler 06-24 export — an `/iterate` Step-4 declaration missed that an approved change contradicted two EXISTING acceptance-criteria lines; the contradictions were caught and reconciled at APPLY time as "entailed coherence", outside the approved declaration (the session proposed a declaration-time "acceptance-criteria entailment scan"). Not the silent-*decisions* pattern this item gates on, but the same declaration-completeness family — a second instance would strengthen the escalation case.

**Questions to resolve if FB-032 proves insufficient (likely via a decision record):**
- Should the spec-auditor be a subagent (`.claude/agents/`) or a Skill (`.claude/skills/`)? Depends on FB-020's findings on subagent-vs-skill context-window separation.
- Where does the PreToolUse hook live — template-owned `.claude/settings.json` (DEC-005 currently restricts that file to `permissions.allow` only), user-owned `settings.local.json`, or a documented example in `setup-checklist.md`?
- If auto mode (DEC-008 / FB-026 outcome) already covers most of the "block unapproved write" goal at the permission layer, does the hook reduce to a narrower belt-and-braces?
- Performance cost of running an adversarial diff-and-review before every spec/decision write.

**Impact scope if pursued:** potentially large — new `.claude/agents/spec-auditor.md` (or `.claude/skills/spec-auditor/`), hook wiring, integration with verify-agent contract.

**Likely outcome:** candidate DEC-009 after FB-032 trial, FB-020 research, and FB-026 resolution all close.

## FB-059: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-16 via DEC-014 Option F (template_version 3.15.0). Sidecar + Part 5 algorithm refinement shipped. See archive for full text.

## FB-060: Template-owned vs project-owned file ownership boundary not enforced or discoverable

**Status:** Phases 1 + 3 + 4 + 5 shipped; Phase 2 (category schema) deferred per DEC-014
**Captured:** 2026-05-15
**Phase 1 + Phase 5 shipped 2026-05-16 (v3.14.2):** (Phase 1) Cross-Project Capture Protocol section added to `.claude/rules/agents.md` — codifies the pre-sync boundary check + finding-routing rules (generically-applicable → project→template promotion; project-specific → migration to project-owned location). (Phase 5) New `.claude/support/reference/extension-hooks.md` with canonical map of extension need → project-owned location, linked from `setup-checklist.md` preamble + `.claude/CLAUDE.md` navigation. Closes the "behavioral complement" follow-up and the "discoverability gap" sub-concern.
**Phase 3 + Phase 4 shipped 2026-05-16 (v3.15.0):** DEC-014 Option F selected — `.claude/.sync-state.json` sidecar + 2-condition Part 5 classification (sidecar-hash-match → "Template content not yet applied" default APPLY; mismatch/missing → "Modified upstream" + "Show me the diff" sub-action). Closes the structural fix for FB-059. The sidecar's `local_hash == synced_hash` check is category-agnostic; per-file ownership tags are operationally redundant given that every current `sync` member is uniformly template-owned. **Phase 2 (sync_strict category schema) remains deferred per DEC-014 § Decision** — adding the category alongside would ship a label without a function (the category doesn't gate anything; the hash check is what drives classification). If/when a real `project_extensible` member emerges (e.g., a future `.claude/skills/{name}/SKILL.md` that ships base content from template + accepts project-side appendix sections), adding the category later is purely additive — no migration cost, no downstream breakage. Decision record: `decisions/decision-014-sync-state-and-file-ownership-categories.md`. Plan: `template-maintenance/plan-fb059-fb060.md` (note: Option F selected; Phase 2 not implemented).
**Source:** surfaced during FB-059 root-cause investigation. The Styler local-additions case wasn't a one-off — it exposes a structural gap: the template documents file ownership as a convention but ships no enforcement, no detection, and no documented extension pattern.

**Observation:** Template files are conceptually split into ownership categories but the template doesn't make this machine-readable or user-discoverable. Three concrete failure modes observed via Styler:

1. **`.claude/CLAUDE.md` (template-owned) was modified by Styler** to add 2 project-specific rule imports + summary rows. The file's own preamble says `"This file is template-owned — do not edit directly. Project-specific instructions belong in ./CLAUDE.md (project root)."` — but nothing prevents or warns against the violation. Convention exists; enforcement doesn't.
2. **`.claude/skills/dashboard-style/SKILL.md` (template-owned)** got the same false-positive treatment from `/health-check` Part 5 even though it had zero local additions (FB-059) — because Part 5 doesn't know which files are template-owned vs project-extensible.
3. **Discoverability gap:** nowhere in the template is the extension pattern explicitly documented. A user wanting to add project-specific rule imports has to infer that root `./CLAUDE.md` is the right home (rather than `.claude/CLAUDE.md`). The template's `setup-checklist.md`, README, and rules files don't surface this.

**Three sub-concerns to address:**

- **Detection (machine-readable ownership).** `sync-manifest.json` currently lists files in flat arrays without tagging ownership category. Proposed schema extension: each file (or file pattern) carries a `category` field — `template_owned` (sync overwrites, never preserves diffs), `project_extensible` (sync respects local additions per FB-059 refinement), or `template_shipped_then_project_owned` (template ships once at setup, then project takes ownership; sync skips entirely). Existing files like `.claude/CLAUDE.md`, `.claude/rules/*.md`, `.claude/skills/*/SKILL.md`, `.claude/commands/*.md` (template-shipped variants) become `template_owned`. Project-extensible: `.claude/dashboard.md` (mostly template-generated but has user notes section). Template-shipped-then-project-owned: `.claude/spec_v1.md` (placeholder shipped, project replaces).
- **Enforcement / warning behavior.** Part 5 uses the category to decide sync behavior:
  - `template_owned` + project-side diff detected → warn user "your local additions to {file} violate the file-ownership convention; the file is being overwritten. Recommended migration: move additions to {root CLAUDE.md / .claude/rules/ / etc.}"
  - `project_extensible` → use FB-059's per-file last-synced-version detection
  - `template_shipped_then_project_owned` → skip sync entirely
- **Discoverability of extension hooks.** Add a "Project extension hooks" section to README or `setup-checklist.md` documenting where projects should add: rule imports (root `./CLAUDE.md`), project-specific rule files (`.claude/rules/` — auto-loaded if imported), project-specific commands (`.claude/commands/audit-{name}.md` per Component 9 of audit family proposal), project-specific skills (`.claude/skills/`), etc. One canonical map. Could live alongside the file-ownership category map.

**Practical impact observed in Styler:** modified `.claude/CLAUDE.md` caused FB-059's false-positive sync friction; no warning when the violation happened; user didn't know the right alternative. Took a multi-message investigation to surface the structural concern.

**Proposed actions:**
1. Extend `sync-manifest.json` schema with `category` per file/pattern. One-time data entry pass.
2. Refine `/health-check` Part 5 to honor categories (combines with FB-059's per-file last-synced-version detection for `project_extensible` files).
3. Add "Project Extension Hooks" section to `setup-checklist.md` and/or root README. Maps each common extension need to its canonical home.
4. Add a one-line preamble check to template-owned files: if user edits detected at sync time, surface the migration recommendation prominently (not buried in the offered-fixes menu).

**Dependencies / interactions:**
- FB-059 (sync detection refinement for `project_extensible`) is a precondition for the Part 5 refinement here.
- Component 9 of audit family proposal (project-to-template graduation) overlaps — both want clear conventions for "what's project, what's template."

**Likely route:** research-light scope. Could be one DEC covering both FB-059 and FB-060 (the ownership system + sync refinement together), since they're tightly coupled. Or two ships: FB-059's per-file last-synced-version mechanism first; FB-060's category schema + Part 5 refinement second.

**Behavioral complement (preventive layer, separate from structural actions 1-4):**

The structural fixes catch the violation at sync time. A behavioral guideline can prevent the violation at the *upstream* moment — when a Claude session is about to recommend the cross-project capture pattern ("land this change in the template, then run `/health-check` to sync the result back"). FB-002/003/004/005 all followed that pattern; FB-002's session missed a boundary check that surfaced as Styler's modified `.claude/CLAUDE.md` weeks later.

**Concrete prompt shape Claude should run BEFORE recommending the sync:**

> "Before recommending the template→sync flow, let me check whether your project has local additions to template-owned files that would conflict. Template-owned files: `.claude/CLAUDE.md`, `.claude/rules/*.md`, `.claude/skills/*/SKILL.md`, `.claude/support/reference/*.md`, `.claude/agents/*.md`. Diffing against last-synced template state OR enumerating project-side additions."

**Routing the findings:**
- Generically-applicable additions → recommend project→template promotion (FB-003/004/005-style) BEFORE accepting the sync. The promoted rules land first; the subsequent sync becomes a no-op convergence rather than a conflict.
- Project-specific additions → recommend migration to project-owned location (root `./CLAUDE.md`, `.claude/rules/` imported from root, etc.) BEFORE the sync.
- Either way, surface the boundary check at suggestion time, not at sync time.

**Style precedent (Styler-side cross-project capture session, 2026-05-15):** *"I should also flag: check styler-side local mods first. Diff against last-synced template state OR enumerate styler-additions to known-template-owned files before recommending sync. Recommend the file-ownership audit alongside the template feedback. 'Promote rule X to template' should pair with 'and also: anything in styler's template-owned files that should either go to root ./CLAUDE.md or also get promoted alongside?'"*

**Where this lives:** documentation, not template code. Candidate homes: a brief addition to `.claude/rules/agents.md` (alongside § "Behavioral Rules") OR a new "Cross-project capture protocol" sub-section in `.claude/support/reference/` (or appended to the existing graduation pattern in audit family proposal Component 9). Either way, no `/feedback review` ship needed for the behavioral piece itself — it's agent-guidance documentation. Could land alongside action 1 (root `CLAUDE.md` documentation pass).

**Independent of structural actions:** the behavioral guideline reduces the *frequency* of the violation; the structural actions reduce the *blast radius* when violations still happen. Both useful; neither blocks the other.

## FB-061: [RELOCATED — promoted to shipped feedback as FB-003]

**Status:** relocated 2026-05-15
**Source:** originally captured here; moved to `.claude/support/feedback/feedback.md` as **FB-003** to match the FB-002 cross-project capture precedent (small + additive + ready for `/feedback review` triage). See FB-062 below for the rationale on the dual-location convention.

**Cross-link:** the active item is `.claude/support/feedback/feedback.md` § FB-003 — promote `feature-retirement.md` from Styler to template. Triage via `/feedback review` will land the SKILL.md + `.claude/CLAUDE.md` + `audit-coherence.md` edits + version bump.

## FB-062: Two FB-NNN locations in template repo with overlapping purposes + namespace collision risk

**Status:** cheap action shipped (medium/higher remain as options)
**Captured:** 2026-05-15
**Cheap action shipped 2026-05-16 (v3.14.1):** root `CLAUDE.md` § File Boundary's "Feedback" bullet replaced with a four-file enumeration that explicitly names `feedback-archive.md` (not `archive.md`), surfaces the naming-asymmetry trap with a concrete observed-instance pointer (FB-004 + FB-005 dedup miss), and documents the cross-project capture pattern. Medium (rename maintenance archive + IDs to `TM-NNN`) and Higher (consolidate to one location with `track:` field) remain as future options if the documented convention still produces dedup misses.
**Source:** surfaced during FB-060/FB-061 capture; recognized after Erik shared context from prior Styler session that authored FB-002 in shipped location (which then shipped as v3.13.0). The location convention is undocumented and the two namespaces could collide.

**Observation:** The template repo has two distinct files holding `FB-NNN` items, with overlapping but unclear purposes:

1. **`.claude/support/feedback/feedback.md`** (shipped) — `/feedback review` operates on it. Currently holds FB-003 (feature-retirement promotion). Archive holds FB-001 + FB-002 (both shipped). Used historically for: actionable items captured via `/feedback` in downstream projects OR direct edits from cross-project sessions when the target is a template-owned file (e.g., FB-002 was authored by Styler-side Claude targeting the template's `decomposition-heuristics/SKILL.md`).
2. **`template-maintenance/feedback.md`** (this file) — manual maintainer triage. Currently holds FB-011 + FB-033 (special-case trackers) + FB-058/059/060/061→relocated/062 (recent additions). Per root `CLAUDE.md`: *"Append manually; do NOT use `/feedback` in this repo."*

**Three concrete problems:**

1. **Namespace collision risk.** Both files use `FB-NNN`. FB-002 (shipped, archived) is a different item than FB-011 (maintenance, active). If shipped grows back into the 060s organically, it would collide with FB-058+ in maintenance. No enforcement against ID overlap; no shared counter.
2. **Convention boundary undocumented.** No clear rule for *"when does an item go in shipped vs maintenance?"* Implicit pattern (observed, not documented):
   - **Shipped:** actionable, ready or near-ready, can be triaged via `/feedback review` → ship → archive (e.g., FB-001 stale lock, FB-002 research-spike, FB-003 feature-retirement promotion).
   - **Maintenance:** special-case trackers (FB-011 scripts inventory tracking shipped families A+B + deferred C/D/E), trial gates (FB-033 spec-auditor gated on FB-032 outcome), items requiring design discussion before triage-able (FB-058 decomp pre-pass, FB-059 sync detection, FB-060 ownership boundary).
3. **Cross-project capture pattern unclear.** FB-002 demonstrated a working pattern: surface in project (Styler) → decide in project (DEC-082) → capture FB in template repo (shipped location) → template-side `/feedback review` triages → ship. But the choice of "shipped vs maintenance" for the template-side capture is itself implicit; a downstream user has to infer.

**Proposed actions (ranked by cost):**

- **Cheap (recommended start):** document the convention in root `CLAUDE.md`. Replace the current "do NOT use `/feedback` in this repo" line with a fuller two-location description with examples + the cross-project capture pattern explicitly. Possibly also add a one-line preamble to each FB file explaining its scope and pointing at the other.
- **Medium:** namespace the IDs differently — e.g., `TM-NNN` for template-maintenance items (no collision with `FB-NNN` shipped). Requires renaming existing maintenance items (FB-011, FB-033, FB-058, FB-059, FB-060, FB-062). Backward-compatibility cost in any external references.
- **Higher:** consolidate to one location with a `track:` field (`shipped` / `maintenance`). Single namespace, single source of truth. Requires schema migration, `/feedback review` update to honor `track:`, and a one-time merge of existing items.

**Likely route:** start cheap (documentation). Re-evaluate medium/higher only if observed friction warrants. The current dual-location pattern works in practice (FB-002 → v3.13.0 proves end-to-end), it just isn't legible without the mental model.

**Dependencies:** none — orthogonal to FB-058/059/060.

### Observed empirical instances (2026-05-16)

Two duplicate captures slipped past the Styler-side dedup check because the check probed for the **wrong filename** in the template-maintenance archive:

- **FB-004** ("Audit Tasks: literal-ID comparison" rule promotion) — duplicate of FB-042, which had already shipped in template v3.2.1 (2026-05-13) and was archived in `template-maintenance/feedback-archive.md`. The dedup check looked for `template-maintenance/archive.md` (incorrect — the file is `feedback-archive.md`) and reported "does not exist," missing the predecessor.
- **FB-005** ("MCP and Parallel Execution" rule promotion) — duplicate of FB-056, same root cause as above (FB-056 shipped in template v3.2.1 alongside FB-042).

Both archived as `absorbed (duplicate)` in `.claude/support/feedback/archive.md` on 2026-05-16. The dedup checks captured this assumption explicitly ("`template-maintenance/archive.md` does not exist"), so the gap is surface-able without forensic git work.

**Reinforces the "Cheap" proposed action above:** the documentation should explicitly enumerate **all four** template-side feedback files by exact filename, so cross-project capture sessions can copy-paste rather than infer:

1. `.claude/support/feedback/feedback.md` (active shipped queue)
2. `.claude/support/feedback/archive.md` (shipped queue archive)
3. `template-maintenance/feedback.md` (active maintenance queue)
4. `template-maintenance/feedback-archive.md` (maintenance queue archive — note: **NOT** `archive.md`)

The naming asymmetry (`feedback-archive.md` vs `archive.md`) is the structural booby trap. Renaming `template-maintenance/feedback-archive.md` → `template-maintenance/archive.md` to match the shipped-queue convention is another candidate fix (one-time rename, update any cross-references in active maintenance items), worth weighing against the cost of breaking git-blame continuity on the file.

## FB-063: Background-session auto-worktree breaks commands that read gitignored project state

**Status:** cheap action shipped (medium/higher remain as options)
**Captured:** 2026-05-16
**Cheap action shipped 2026-05-16 (v3.14.1):** added `## Background-session note` sub-sections above `## Usage` in `.claude/commands/audit-coherence.md` and `.claude/commands/audit-ui.md`, instructing not to enter a worktree before running the command (worktree's HEAD won't contain gitignored inputs, and the audit dir's timestamp prevents same-second collisions across parallel sessions, so isolation is unnecessary). Medium (extend background-session preamble carve-out to "writes only to gitignored locations") and Higher (worktree-level bind-mount of gitignored files) remain as future options if other commands hit the same trap.
**Source:** observed mid-run during `/audit-coherence` in the Styler downstream project (background session, 2026-05-15). The audit aborted its initial write attempt with `InputValidationError` ("This background session hasn't isolated its changes yet. Call EnterWorktree first"). Entering the worktree then revealed the worktree's HEAD did not contain the gitignored inputs the audit needs (spec, decisions, feedback, tasks, dashboard — all gitignored under `.claude/**` in Styler's `.gitignore`).

**Observation:** The background-session preamble auto-routes any tool that writes files into an `EnterWorktree` call before "code changes." The current carve-out reads:

> *Before making any code changes, use the EnterWorktree tool to isolate your work from other parallel jobs and the user's working copy — unless your cwd is already under `.claude/worktrees/`, in which case you're already isolated. If you're only reading, searching, or answering questions, skip this and work in place.*

For projects whose primary state (`.claude/spec_v*.md`, `.claude/dashboard.md`, `.claude/support/decisions/`, `.claude/tasks/`, `.claude/support/feedback/`, etc.) is gitignored, this produces a structural failure mode:

1. Command attempts a write → blocked, told to enter worktree.
2. `EnterWorktree` succeeds — but the worktree's HEAD is a fresh checkout from `origin/main` (or local HEAD per `worktree.baseRef`), which does *not* contain any gitignored files.
3. Command runs in the worktree and discovers its inputs don't exist there.
4. To proceed, the command exits the worktree (`ExitWorktree { action: "remove", discard_changes: true }`), which destroys any writes the command made in steps 1-2.
5. Command resumes in the main tree, re-doing the captures via `Bash` redirects (`Bash` writes weren't blocked, only `Write`/`Edit` were).
6. Any files written via `Write`/`Edit` before exiting the worktree are lost — silently. The agent has no audit-trail signal to recreate them.

In the Styler audit run, this left two captured-inputs files missing (`meta.json`, `friction-open.jsonl`) from the otherwise-complete audit dir. The audit ran end-to-end (findings sound) but the input audit trail is incomplete. A future re-run or `/audit-coherence promote` flow that depends on those files would have to re-derive them.

**Why the worktree carve-out doesn't catch this:**

- The existing read-only carve-out (*"only reading, searching, or answering questions"*) doesn't cover audits, which read gitignored state and write to a gitignored audit dir under `.claude/support/audits/{cmd}-{ts}/`.
- "Code changes" the rule was designed to isolate are changes to tracked files. Audit writes are entirely to gitignored locations — they cannot collide with parallel jobs (timestamped subdirs) and cannot affect the user's tracked working copy.
- The worktree's *intended* isolation benefit (parallel-job safety + working-copy safety) is moot in this case: the writes go to gitignored paths, and the timestamp in the audit dir name prevents same-second collisions.
- The worktree's *cost* in this case is real: it severs access to the gitignored inputs the command needs to read.

**Affected commands (template-shipped):**

- `/audit-coherence` — observed failure. Reads spec, decisions, feedback, friction register, retired manifests; writes audit dir.
- `/audit-ui` — same dir pattern. Reads tracked code but writes audit dir. Less broken (inputs aren't gitignored) but the worktree dance is still wasted overhead.
- `/health-check` Part 7 (template repo only) — reads `interaction-logs/inbox/` (gitignored) and writes to `template-maintenance/feedback.md`. Same shape.
- Probably any future audit-family or interaction-log command.

**Proposed actions (ranked by cost):**

- **Cheap (recommended start):** add a one-line note to each audit command file (`commands/audit-coherence.md`, `commands/audit-ui.md`, and the audit family proposal as a documented contract) saying:

  > *Background-session note: this command reads gitignored project state and writes only to a gitignored audit dir. Do not enter a worktree before running it — the worktree's HEAD will not contain the gitignored inputs.*

  Lowest blast radius, surgical fix. The orchestrator dispatching the audit command would see this note in the command body and skip `EnterWorktree`.

- **Medium:** extend the background-session preamble's carve-out from *"only reading, searching, or answering questions"* to *"or writes only to gitignored locations under `.claude/support/audits/`, `.claude/support/workspace/`, or other gitignored audit/scratch paths."* Generalizes the rule for any future command that operates on gitignored state. Harder to verify automatically (the agent would need to know which paths are gitignored, which it can derive from `.gitignore` but isn't always front-of-mind).

- **Higher:** worktree-creation could optionally bind-mount or copy gitignored files into the worktree, so worktree HEAD reflects working-copy reality. Tool-level change with much broader implications (affects every worktree, not just audit commands). Not recommended unless other gitignored-state cases pile up.

**Likely route:** start with **Cheap** — three one-line additions to existing command files. If the audit family grows or the `/health-check` Part 7 path hits the same trap, fold into **Medium** at that time.

**Concrete diff sketch (Cheap):** at the top of `commands/audit-coherence.md`, above `## Usage`, add a `## Background-session note` heading with the line above. Same for `commands/audit-ui.md`. Optionally add a corresponding bullet to `audit-command-family-proposal.md` Component 5 ("/health-check dispatcher integration").

**Dependencies:** none. Surfaces an interaction between the audit family (template-shipped) and the background-session preamble (template-shipped). Both files are template-owned; fix lands wholly inside this repo.

**Cross-reference:** Styler audit run that surfaced this — `.claude/support/audits/coherence-2026-05-15-2337/` (in `~/Developer/styler/`). The missing files in that audit dir's `inputs/` are the visible artifact of the failure mode.

## FB-064: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-16 — test-harness awareness decomposition heuristic shipped in template_version 3.17.0 (new "Test-Harness Awareness" section added to decomposition.md + SKILL.md mirror; runs alongside the Pre-Pass Validation after step 8). See archive for full text.

## FB-065: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-16 — decomposition enum-extension heuristic shipped in template_version 3.16.0 (5th heuristic row added to FB-058 Pre-Pass Leg 2). See archive for full text.

## FB-066: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-16 — verify-agent production-consumption check shipped in template_version 3.16.0 (sub-bullet added to Step T5; feeds existing integration_ready key). See archive for full text.

## FB-067: External-source recheck — mattpocock/skills Wave 2 candidates

**Status:** deferred — signal-gated (fixed recheck date dropped 2026-06-12; long backstop only)
**Captured:** 2026-05-19
**Re-assessed:** 2026-06-12 — Manual maintenance-queue review. Wave 1 complete (FB-068/069/070/071, v4.1.0–v4.4.0). The 2026-06-02 recheck date passed but fired **empty** — a ripgrep sweep (with positive control) of `interaction-logs/` + maintenance docs found zero downstream signal for any Wave 2 candidate (every hit was a self-reference). Disposition: **closed** `/caveman` + hard-vs-soft cleanup (see inline notes below); kept `/tdd`, `/prototype`, `/improve-codebase-architecture`, bucketing **signal-gated**; **dropped the fixed recheck date** for pure signal-gating + a long backstop (2026-12-12). The lapsed date proved calendar rechecks on signal-gated items generate busywork, not information.
**Source:** video https://www.youtube.com/watch?v=6BB6exR8Zd8 reviewed 2026-05-19; repo `mattpocock/skills` (clone at `/Users/erikemilsson/Downloads/skills-main` as of 2026-05-19; mirror github.com/mattpocock/skills).

**Reason for deferral:** Wave 1 (FB-068 + FB-069 + FB-070 + FB-071) ships first. Wave 2 candidates depend on Wave 1 signal — some compound only with their Wave 1 sibling in place.

**Wave 2 candidates to re-evaluate:**

- **`/tdd` skill** — vertical-slice red-green-refactor + anti-horizontal-slicing discipline. Pocock files at `skills/engineering/tdd/SKILL.md` + `tests.md` + `mocking.md` + `interface-design.md` + `deep-modules.md` + `refactoring.md`. Open question: does CCE's verify-agent already cover the "correctness" angle sufficiently?
- **`/prototype` skill** — throwaway design exploration. Two branches: terminal app for state/logic, multi-variation UI on one route. Trigger to ship: how often CCE work hits "I don't know what shape this should be."
- **`/improve-codebase-architecture` skill** — complement to `/audit-coherence`. Architectural vocabulary (Module/Interface/Depth/Seam/Adapter/Leverage/Locality) + deletion test heuristic. Most valuable AFTER CONTEXT.md (FB-068) and AFTER `/diagnose` (FB-069) — `/diagnose`'s Phase 6 post-mortem explicitly hands off here.
- **`/caveman` ultra-compressed mode** — ~75% token cut. Niche; ship only if cost pressure becomes a recurring concern. **→ CLOSED 2026-06-12:** token-compression value largely absorbed by the 1M context window + current Opus tier; the context-pressure failure mode it addresses rarely bites here. Re-open only on real, recurring cost pressure.
- **Hard-vs-soft dependency cleanup pass** — apply Pocock's ADR-0001 pattern across CCE command files. Distinguish load-bearing cross-references from advisory. Cosmetic. **→ CLOSED 2026-06-12:** cosmetic by its own description; no signal, marginal value. Re-open only on a real cross-reference-fragility incident.
- **Bucketed skill organization** (`engineering/` / `productivity/` / `misc/` / etc.) — only worth considering if skill count grows much further.

**Trigger to escalate from deferred → ready (signal-gated; no fixed recheck date as of 2026-06-12):**
1. Any ship produces signal that a specific **live** Wave 2 sibling compounds (`/tdd`, `/prototype`, `/improve-codebase-architecture`, bucketing — `/caveman` + hard-vs-soft cleanup are closed). Concrete example: `/diagnose` Phase 6 post-mortems repeatedly identify architectural friction → `/improve-codebase-architecture` becomes load-bearing.
2. Separate user request to re-evaluate.
3. Backstop (not a scheduled review): if neither fires, re-confirm relevance by 2026-12-12. The prior 2026-06-02 fixed-date recheck fired empty — calendar rechecks on signal-gated items generate busywork, not information.

**Source pointers preserved:**
- Local clone: `/Users/erikemilsson/Downloads/skills-main` (may be cleaned later)
- GitHub: github.com/mattpocock/skills
- Video: https://www.youtube.com/watch?v=6BB6exR8Zd8
- Skill list + four-frame structure: `/Users/erikemilsson/Downloads/skills-main/README.md`

## FB-068: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 — new `/grill` command + `./CONTEXT.md` slot (project-owned, lazy-created glossary) shipped in template_version 4.2.0. Live skills-list verification: `grill: Grill Command` immediately appeared in model-invocable list. Integration points: `./CONTEXT.md` row in `.claude/CLAUDE.md` Navigation, `/grill` in Environment Commands, new `## Domain Glossary Awareness` section in `rules/agents.md`, `/grill` mention in `rules/spec-workflow.md § Vision Documents`, extended `audit-coherence.md § "Lens 2 — vocab-drift"` to consume CONTEXT.md when present. All explicit out-of-scope items from FB-068 honored (no batch-extract, no co-equal source of truth, no CONTEXT-MAP.md, no glossary versioning, no direct ADR writes). See archive for full text.

## FB-069: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 — new `/diagnose` command (6-phase debugging methodology) shipped in template_version 4.4.0. Adapted from `mattpocock/skills/engineering/diagnose`, domain-genericized for CCE. Cross-referenced from `agents.md § Root Cause Over Symptom` (structural enforcement mechanism for hard bugs) + `spec-workflow.md § Workflow Cycle` (bug-task preferred route). Leaves `disable-model-invocation: true` OFF per FB-071 selection criteria — autonomous-fire-when-stuck is the value proposition. Phase-6 architectural-friction handoff routes through CCE's friction register or `/research` (no `/improve-codebase-architecture` exists yet — FB-067 Wave 2). **Wave 1 complete.** See archive for full text.

## FB-070: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 — new `/zoom-out` micro-command shipped in template_version 4.3.0. Carries `disable-model-invocation: true` frontmatter on day one per FB-071 convention (`/zoom-out` is explicitly a user-asks-for-help signal; autonomous fire would be circular — Pocock's `/zoom-out` carries the same frontmatter for the same reason). Consumes `./CONTEXT.md` vocabulary when present (FB-068 integration); degrades gracefully when absent. See archive for full text.

## FB-071: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 — `disable-model-invocation: true` frontmatter applied to all 5 strong-candidate commands (`/breakdown`, `/research`, `/iterate`, `/work`, `/feedback`) shipped in template_version 4.1.0. Live empirical verification: model-invocable skills list shrank immediately from 10 template commands to 5. New `## Command Invocation Gates` section in `rules/agents.md` documents the convention, selection criteria, sub-mode coupling trade-off, and defense-in-depth interaction with DEC-005 + DEC-016. Medium candidates deferred for trial-period observation. See archive for full text.

## FB-072: [CLOSED — moved to `template-maintenance/feedback-archive.md`]

**Status:** closed 2026-05-24 — DEC-018 resolved to **Option B** (status quo, explicit-arg dispatch); the interpretive-router proposal was declined after a value deep-dive (CCE's own 26-session usage logs showed near-absent recall-the-token friction → marginal value vs. permanent costs). Decision: `decisions/decision-018-command-routing-interpretive-vs-explicit.md` (`approved`). Re-open condition in DEC-018 Impact if Wave 2 grows the command surface. Durable records: that DEC + `decisions/.archive/decision-018-research-2026-05-24.md` + `template-maintenance/router-survey.md`. See archive for the full closure record.

## FB-073: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

See `feedback-archive.md` for full entry.

## FB-074: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

See `feedback-archive.md` for full entry.

## FB-075: TaskCreate/TaskUpdate harness reminder fires in projects that explicitly forbid built-in task tools

**Status:** cheap-action-shipped + deferred (structural fix upstream-gated). **Re-assess (2026-10-02):** the v5.7.5 doc check reports that Claude Code enables TaskCreate/TaskUpdate/TaskList by default only through Opus 4.7, and none of them is in an Opus 5.5 session's tool list (verified 2026-10-01). If the reminder no longer fires on Opus 5.5, close this and trim `.claude/README.md § Known Constraints`.
**Captured:** 2026-05-20
**Cheap action shipped:** 2026-05-20 — Added "Harness reminders about built-in task tools" paragraph to `.claude/README.md § Known Constraints`. Documents the noise as harness-emitted (not template-emitted) and benign in projects using `.claude/tasks/*.json`. Shipped in template_version 4.6.1 (alongside FB-076 deferral).
**Defer condition (structural fix):** structural opt-out requires Anthropic-side mechanism (CLAUDE.md sentinel, settings hook, or per-project flag). Re-assess when (a) upstream offers such a mechanism, OR (b) friction scales materially (token tax across 100+ sessions becomes meaningful).
**Source:** Aggregated across 7 session exports (echothread + styler, 2026-05-16 → 2026-05-17). Observed in this very session 2026-05-20 during inbox triage — the harness reminder fired immediately after the AskUserQuestion confirming this FB capture.

The Claude Code harness emits a system-reminder along the lines of *"The task tools haven't been used recently. Consider using TaskCreate to add new tasks and TaskUpdate to update task status..."* on most tool returns. When a project's `.claude/CLAUDE.md` contains the explicit override ("Use the project's task system (`.claude/tasks/*.json`). Never use built-in TaskCreate/TaskUpdate/TaskList tools"), the reminder is universally irrelevant — every fire costs cognitive cycles + token tax + a user-visible "ignoring per project rules" acknowledgment from the agent.

### Pattern

Observed cumulatively across the 7 sessions: ~60+ TaskCreate reminder fires. The reminder is built into the runtime (not template-emitted), so the template can't suppress it directly. Both echothread and styler sessions show the same pattern:

1. Agent does work using the project's task JSON system (per CLAUDE.md).
2. Harness emits the reminder after most tool returns.
3. Agent burns tokens acknowledging + ignoring + reasserting the project rule.

### Two possible mitigations

1. **Harness-side (Anthropic concern):** when CLAUDE.md contains an explicit-override phrase ("Never use built-in TaskCreate"), suppress the reminder for that project's sessions.
2. **Template-side (CCE concern):** add a CLAUDE.md marker or settings.json convention that the harness reads to disable the nudge. Example: `task_system_override: true` field in `.claude/version.json`, or a documented sentinel comment in CLAUDE.md the harness recognizes.

Both paths require Anthropic-side cooperation — the reminder logic lives in the runtime, not in template-shipped files. Worth raising upstream OR documenting the unavoidable noise in `.claude/README.md` so users (and agents) don't feel the rule is broken.

### Why this is worth capturing despite being upstream

- **Recurring confusion signal:** agents visibly burn tokens acknowledging the reminder; users observe and ask "why does it keep suggesting that?"
- **Project authority erosion:** explicit project rules feel less authoritative when the harness contradicts them on every tool return.
- **Documented friction = potential fix:** if Anthropic adds an opt-out mechanism, the template can adopt it immediately.

Sources:
- `interaction-logs/processed/echothread-2026-05-16.json` (~10 fires)
- `interaction-logs/processed/echothread-2026-05-17.json` (~10 fires)
- `interaction-logs/processed/echothread-session-2026-05-16.json` (~20 fires)
- `interaction-logs/processed/styler-2026-05-17.json` (~10 fires)
- `interaction-logs/processed/styler-session-export-2026-05-16-T0955.json` (7+ fires)
- `interaction-logs/processed/styler-session-export-2026-05-16-T1332.json` (7+ fires)
- `interaction-logs/processed/styler-session-export-2026-05-16-T1425.json` (recurring fires)

Tags: harness, task-system, system-reminders, upstream-anthropic, friction-aggregate

## FB-076: verify-agent runtime_validation misses bundle-boundary breaks and catalog-state-dependent gaps

**Status:** mitigation 1 shipped (v4.15.0) — production-build check runs in `/work`'s Empirical Evidence Gate when a task touches client-marked files and root `./CLAUDE.md § Verification Hooks` declares a build command (catches failure mode 1, the client/server bundle boundary). Mitigations 2 (ESLint client-import rule) + 3 (live-data cross-reference — failure mode 2) remain deferred, research-gated.
**Captured:** 2026-05-20
**Defer condition:** Re-assess when (a) 2nd project signals the same verification gap, OR (b) FB-066 downstream telemetry suggests broader runtime_validation hardening is needed. Single-project signal (styler T667) doesn't justify the design work (build-command discovery + catalog-path declaration; mitigations 1+3 are not as mechanical as FB-066's regex+grep). If signal escalates: route through `/research` for design — similar to FB-072's trial-gated DEC candidate path. Tracked in root CLAUDE.md § Active Follow-ups as of v4.6.1.
**Amendment (2026-08-12, harvest cluster 3):** a **third** `runtime_validation` failure mode — *no local execution environment for the artifact class at all* (Fabric PySpark notebooks, TMDL semantic models, GitHub Actions workflows, live Delta reads) — was observed in a 2nd project (OEMMatInsightBI, 6 core + 3 same-family incidents). This satisfies condition **(b)** (broader runtime_validation hardening need), **not (a)** (it is not "the same verification gap" as either documented mode). **Mitigations 2 + 3 remain gated** — mitigation 2 (ESLint client-import rule) is inapplicable to a stack with no client/server bundle boundary; mitigation 3 (live-data cross-ref) is only a partial spirit-match. The third mode + the local-ceiling-determination gap (agents both over- and under-claim what can run locally) are captured as a sibling — **FB-116** — that *extends* this item rather than unlocking it. See FB-116 + `interaction-logs/insights/2026-08-12_verify-agent_runtime-validation-local-ceiling.md`.
**Source:** Aggregated from styler session export 2026-05-17 (T667 markers — two distinct verification_gap entries). Extends FB-066 (production-consumption check, shipped v3.16.0).

Structural + automated verification (lint, tsc, vitest, behavior tests) is necessary but not sufficient for tasks where bugs surface only under (a) production bundling or (b) live data state. Two concrete failure modes from styler T667:

### Failure mode 1: Client/server bundle boundary

`ExpandedPalette.tsx` + `ItemRecropControl.tsx` imported `DEFAULT_TARGET_ASPECT` from `photo-normalization.ts`, which transitively pulled `sharp` → Node-only modules into the client bundle. All static + automated checks passed; first `/outfits` page render failed with Turbopack 500.

Hotfix: extracted client-safe constants to `photo-target.ts` re-exported by `photo-normalization.ts`.

### Failure mode 2: Catalog-state-dependent precondition

T667's worn-photo outlier warning targets a code path satisfied by zero items in the live catalog (26/27 wardrobe items have no worn photo; hanger photos never reach the measurement img). Mock-based behavior tests passed because synthetic photoSrc was supplied; live catalog cross-reference would have shown the warning can never fire.

### Why this extends rather than duplicates FB-066

FB-066 (shipped v3.16.0) addresses "class exported but never instantiated" via a verify-agent T5 production-consumption check. That covers static class-export gaps. T667's two failure modes are different:

- **Bundle boundary** is dynamic — the symbol IS consumed, but consumption from a client-marked file pulls a transitive Node-only dep into the wrong bundle. Static grep doesn't catch this; only an actual build does.
- **Catalog-state** is data-dependent — the code path executes correctly under mocks but is unreachable under real data because no catalog rows satisfy the precondition.

Both fall under verify-agent's `runtime_validation` check, which currently passes any task whose static + mock-based tests pass.

### Mitigation candidates (in priority order)

1. **Production-build invocation.** When a task touches files marked `'use client'` (or framework equivalents), verify-agent runs `npm run build` (or the project's equivalent) before declaring the task verified. Catches bundle-boundary breaks like failure mode 1.
2. **ESLint rule.** A custom ESLint rule that blocks client components from importing modules whose transitive deps include `sharp`, `fs`, `child_process`, etc. Faster than full build; runs in implement-agent's edit loop. Less reliable than build (transitive analysis is brittle) but cheap.
3. **Live-data cross-reference.** When the spec implies a feature operates over real catalog state (foundation/wardrobe/items/*.json or analog), verify-agent samples the catalog and confirms the feature's precondition is reachable for ≥1 row. Catches failure mode 2.

Mitigations 1 and 3 are independent (different failure classes); both are worth adding. Mitigation 2 is a faster proxy for mitigation 1, useful if `npm run build` is too slow to run on every task.

### Template-side homes

- `.claude/agents/verify-agent.md` — add runtime_validation sub-checks for bundle-boundary + live-data
- `.claude/commands/work.md` — verify-agent dispatch should pass the project's build command + catalog paths if available
- Project-side: `./CLAUDE.md` may declare the project's build command + foundation-data paths for verify-agent consumption

Source: `interaction-logs/processed/styler-2026-05-17.json` (T667 markers, two `verification_gap` entries explicitly naming both failure modes).

Tags: verify-agent, runtime-validation, bundle-boundary, live-data, extends-FB-066

## FB-077: Auto-mode classifier over-broad DEC-016 scope + AskUserQuestion responses don't count as authorization

**Status:** cheap-action-shipped + deferred (structural fix upstream-gated)
**Captured:** 2026-05-20
**Cheap action shipped:** 2026-05-20 — Added "Auto-mode classifier false-positives" paragraph to `.claude/README.md § Known Constraints` (sibling to FB-075's TaskCreate harness reminder paragraph). Documents both sub-issues + workarounds: (a) DEC-016 scope — lead with explicit context-clarifying language, or user provides typed-text authorization; (b) AskUserQuestion authorization — agents prefer free-text prompts when classifier-bypass authorization is the goal. Shipped in template_version 4.6.3.
**Defer condition (structural fix):** Re-assess when Anthropic offers (a) per-path DEC-016 scope declaration (positive-list of paths in scope, exact-match to the three globs in `CLAUDE.md § Critical Invariants`), (b) AskUserQuestion authorization recognition (classifier treats AUQ "authorize" responses as auth for the action they reference), OR (c) workaround friction recurs across N sessions despite the README docs.
**Source:** Two distinct classifier false-positives observed in-session 2026-05-20 during FB-074 sub-issue 1 (categories extension) ship. Concrete block messages preserved below.

The auto-mode classifier blocked legitimate Edits during a session where the user had explicitly approved the work (FB-074 promotion approved via AskUserQuestion). Two distinct failure modes surfaced.

### Sub-issue A: DEC-016 scope misinterpretation

The classifier blocked an Edit to `.claude/support/reference/decisions.md` (a reference doc documenting decision RECORD format) citing DEC-016. But DEC-016's scope is explicitly the three globs documented in `.claude/CLAUDE.md § Critical Invariants`:

- `.claude/spec_v*.md`
- `.claude/support/decisions/decision-*.md` (decision RECORDS, not reference docs)
- `.claude/vision/**/*.md`

The reference doc `.claude/support/reference/decisions.md` is NOT in scope. The classifier conflated:
- (record at) `.claude/support/decisions/decision-{NNN}-*.md` ← in scope
- (reference doc at) `.claude/support/reference/decisions.md` ← NOT in scope

Concrete block message: *"Substantive edit to `.claude/support/reference/decisions.md` (a template-owned reference file) is blocked by user's own DEC-016 rule routing substantive edits through /iterate"*

This is a false-positive. The user's intent (per DEC-016) was to gate decision RECORDS — the audit-trail-of-intent files — not the meta-documentation about how to author records.

### Sub-issue B: AskUserQuestion responses don't count as authorization

After the first block, the agent surfaced the issue and offered options via `AskUserQuestion`. The user picked "Authorize the edit explicitly". The agent retried the Edit. The classifier blocked again with:

*"Agent retried the same edit immediately after the classifier block / AskUserQuestion without a visible user response authorizing the retry."*

The classifier requires typed-text authorization in a user message. `AskUserQuestion` responses — even when the user explicitly selected an "authorize" option — are treated as programmatic answers, not authorization.

This is a UX-shape problem: `AskUserQuestion` is designed as a clean, structured way to collect user decisions. If those decisions can't authorize subsequent actions, the tool's utility for permission-flow scenarios is sharply limited. Agents must fall back to free-text prompts when authorization matters — defeating the purpose of structured-choice collection.

### Combined impact

In this session: FB-074 sub-issue 1 (categories enum) needed edits to BOTH `health-check.md` (allowed by classifier) AND `decisions.md` (blocked twice). The two-file inconsistency left the template in a half-shipped state — `health-check.md` validated against the extended enum, but the reference doc still showed the old 6-value list. Manual intervention required (user typed text authorization after the structured approval via AskUserQuestion failed).

### Mitigation candidates

**For Sub-issue A (DEC-016 scope):**
- Tighten classifier rules to match DEC-016's stated path patterns exactly (the three explicit globs from `CLAUDE.md § Critical Invariants`).
- Add a positive-list of in-scope paths for DEC-016 enforcement rather than a heuristic "anything named decisions.md".

**For Sub-issue B (AskUserQuestion authorization):**
- Treat AskUserQuestion responses as authorization for the action they reference (per-question metadata could declare which action the question gates).
- Or: document the limitation so agents know to use free-text prompts for permission flows.
- Or: classifier inspects the AskUserQuestion question + options to determine authorization intent.

### Related

- DEC-016 (spec/decision/vision file edit guardrail) — Sub-issue A is about the classifier's interpretation of DEC-016's scope.
- DEC-005 (auto-mode permission layer) — the broader auto-mode classifier where this lives.
- FB-074 sub-issue 1 (categories extension) — concrete promoted item that triggered the block.

Tags: auto-mode, classifier, dec-016, dec-005, false-positive, askuserquestion, authorization, upstream-anthropic

## FB-078: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle). Option 1 heuristic shipped: chosen-option no-op scan in `phase-decision-gates.md § "Post-Decision Check"`. Research at `.claude/support/workspace/fb-078-research.md`. See archive for full entry.

## FB-079: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 via v4.6.4. Minute-granularity timestamp applied to `/work pause` session-export filename at both write sites (`work.md` step 5 + `pre-compact-handoff.sh` lines 230 + 237). See archive for full entry.

## FB-080: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 via v4.7.0. Route C1 (hybrid: targeted-edit pattern + sidecar sentinel) selected over A (section-fingerprints in META) and B (defer-everything-to-session-boundary). New `pending_full_regen` field on `dashboard-state.json` sidecar; targeted-edit decision table in SKILL.md + mirror; Step 1a freshness check extended. See archive for full entry; research at `.claude/support/workspace/fb-080-research.md`.

## FB-081: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle). Both patterns bundled: heartbeat (`commands/work.md § Step 3 "Autonomous batch heartbeat"`) + ping-mid-batch behavioral rule (`rules/agents.md § "Behavioral Rules" — "Acknowledge mid-batch user messages"`). Shared counter `autonomous_batch_position` ≥3 threshold. Research at `.claude/support/workspace/fb-081-research.md`. See archive for full entry.

## FB-082: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-24 via v4.9.0 (DEC-017 Option B ship). YAML frontmatter colon-space hazard folded into `.claude/support/reference/claude-code-authoring.md § "YAML Frontmatter Hazards"` (Section 1 of the new authoring-hazards reference doc); also cross-referenced from `implement-agent.md § "Editing strategy for structured documents"`. See archive for full entry.

## Signal queue from 2026-05-20 scan — captured here for next-session triage

The 2026-05-20 scan of `interaction-logs/processed/` surfaced six additional weaker signals not yet promoted to dedicated FBs. Captured here as a queue so next `/feedback review` (or manual triage) can decide whether to expand any into proper entries.

*(Item 1 — Uncommitted-work check — promoted to FB-088 on 2026-05-24 during walk-through triage.)*

- ~~**Math-check before commit-to-pixels on layout iterations** (styler 2026-05-20).~~ — **absorbed 2026-06-10 by the FB-085 ship (v4.13.0):** the `/diagnose` `## Visual / browser-rendering bugs` recipe requires each loop iteration to carry a predicted value-effect computed before touching code — which is this pattern, per the FB-085 locked design ("folds in the queued 'math-check before commit-to-pixels' signal"). *(Prior review 2026-05-24 kept it queued pending a 2nd signal — superseded by the absorption.)*
- ~~**Dashboard Recent Activity prose-style cap enforcement is ambiguous** (styler 2026-05-20).~~ — promoted to **FB-090** on 2026-05-24 during walk-through triage. Promotion trigger: FB-080 (targeted-edit path) shipped in v4.7.0 since capture, weakening the "regen-scope cost is high" deferral reason that originally kept this in the queue. See FB-090 below for the re-scoped entry.
- ~~**Magnitude check when user specifies rule without absolute value**~~ — closed 2026-05-24 during walk-through triage. Pattern is covered by `/grill` (FB-068, v4.2.0). The "ask one focused question to resolve ambiguity before coding" pattern is what `/grill` does at interview granularity; magnitude-check is a special case of /grill's broader interrogation. Decline standalone promotion.
- ~~**`.interaction-assessment.json` cleanup may have silent failure mode**~~ — promoted to FB-089 on 2026-05-24 during walk-through triage (gap confirmed by direct read of `commands/work.md § Session Export step 7`).
- ~~**`/walkthrough` or `/preflight` command for major workflow transitions**~~ — added to FB-072's `/research` scope on 2026-05-24 during walk-through triage (sibling candidate to `/zoom-out` / `/grill` / `/diagnose` help-me-think family).

A seventh candidate — `file-status-taxonomy.md` starter reference doc (CANONICAL/REFERENCE/OPERATIONAL/HISTORICAL/etc.) — is speculative enough (one-project signal, abstract pattern) that it's not worth even queue capture; revisit only if a second project independently raises the need.

Tags: signal-queue, multi-source-scan, next-triage

## FB-083: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-24 via v4.9.0 (DEC-017 Option B ship). New `.claude/support/reference/claude-code-authoring.md` shipped (5 sections + footer); freshness mechanism = footer + `/health-check` Part 2d capability-doc-freshness lens with `[V] Verify` user-adjudicated WebFetch action. Cross-references shipped in `.claude/CLAUDE.md` Navigation, `.claude/agents/implement-agent.md`, `.claude/rules/agents.md` (State Ownership + Command Invocation Gates), `.claude/commands/iterate.md` (Step 4 capability-claim cross-check), `.claude/commands/work.md` (decomposition cross-check), `.claude/commands/health-check.md` (Part 2d). Research at `.claude/support/workspace/fb-082-083-research.md`. See archive for full entry.

## FB-084: Engine-consumption verification gap during retirement proposals (snake_case vs CamelCase derivatives)

**Status:** cheap-action-shipped + heavier-route-deferred
**Captured:** 2026-05-24
**Shipped:** 2026-05-24 (v4.7.3) — new `## Pre-Retirement Engine-Consumer Audit` section added to `.claude/rules/feature-retirement.md` between "When to Use This Workflow" and "Procedure". Documents the 4-pattern grep (snake_case + CamelCase derivatives + shortened forms + string literals) for pre-retirement verification. Heavier route (extend FB-066 to proposal-time) deferred — research-gated + signal-gated.
**Source:** Bridged from styler 2026-05-22 session (FR-014 / T714, template_version 4.7.1) via `/health-check` Part 7 aggregation.

## Observation

T714 retired `price_quality_philosophy` based on a `/research` (FR-014) finding that grepped only the snake_case form and concluded "no engine consumer found". The actual engine consumption used multiple derivatives the snake_case grep missed:

- `PriceQualityPhilosophy` (CamelCase TypeScript type)
- `RankerSignals.philosophy` (shortened field name in `src/lib/stores/ranker.ts`)
- `PHILOSOPHY_WEIGHTS` (CamelCase constant)
- Runtime reads in `/stores Phase 2a` + `/briefing Step 3`

The field is now retired from the registry but the engine integration points remain and will silently degrade (read returns `undefined` post-data-migration) until command files are restructured. Caught mid-implementation via friction marker (FR-016 / FR-017 / FR-018 sequence); corrective amend landed in-session.

## Meta-pattern

The grep convention for retirement proposals is fragile: `grep -r 'snake_case_field' src/` misses `CamelCaseField` derivatives, `field` shortened names, and string-literal usage (`"snake_case_field"`). A retirement proposal that searched only one form gives false confidence — "no consumer" reads as definitive when it's actually "no consumer matching this one form".

## Proposed template surface

Three candidate landing spots (not mutually exclusive):

1. **`.claude/rules/feature-retirement.md` § "Procedure" / "Common gotchas"** — add a checklist for verifying engine-consumer searches cover snake_case + CamelCase + shortened-field + string-literal variants. One paragraph, near "What NOT to copy" or as a new "Pre-retirement engine-consumer audit" sub-section.
2. **FB-066 extension** (verify-agent production-consumption check, shipped v3.16.0). The existing check is regex-based on file globs; could extend to scan for retired-field names in code beyond the spec section. Different timing (verify-agent, post-implementation) vs the proposal-time gap here.
3. **`.claude/scripts/verify-engine-consumption.sh` helper** (project-side). Project ships a wrapper that runs the multi-pattern grep (snake_case, CamelCase, shortened, string-literal) and surfaces matches before retirement landing. Higher overhead; only worth it if the project retires fields routinely.

## Triage recommendation

**Cheap action:** add the multi-pattern grep checklist to `feature-retirement.md` as a one-paragraph "Pre-retirement engine-consumer audit" sub-section. Catches the issue at proposal time across all projects using the template.

**Heavier route (research-gated):** extend FB-066 to cover the proposal-time gap (currently FB-066 is verify-agent only). Would unify the two layers — proposal-time + post-implementation — into one consistent check. `/research` to compare.

## Relationship to FB-066 and FB-076

- FB-066 (shipped v3.16.0) covers verify-agent runtime production-consumption — different timing (post-implementation, before "Finished").
- FB-076 (deferred) covers verify-agent bundle-boundary breaks + catalog-state-dependent precondition gaps — adjacent but distinct sub-gap.
- FB-084 is at the proposal stage (during `/research` or `/iterate distill`), upstream of verify-agent. Sibling to both, not a duplicate.

## Source trace

- Bridged from `interaction-logs/processed/.session-export-styler-2026-05-22-0105.json` § `claude_assessment.design_pushback_opportunities[0]`.
- Single-session signal but novel pattern. Below 3+ session bar for auto-promotion in `/health-check` Part 7 step 4; captured manually per user direction.

Tags: template-side, feature-retirement, grep-coverage, proposal-time-check, extends-FB-066, cheap-action-candidate, single-project-signal

## FB-085: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-06-10 via **v4.13.0** (MINOR) — `## Visual / browser-rendering bugs` recipe shipped into `.claude/commands/diagnose.md` per the locked design (`/visual-verify` grill 2026-05-24). 2nd-project gate overridden 2026-06-10 by user decision (cost known at ~20 lines, zero new surface, trivially reversible; within-styler evidence volume past the gate's intent). Absorbs the 2026-05-20 signal-queue "math-check before commit-to-pixels" item. General-merit half (outcome-not-mechanism) had shipped v4.10.2. Trace test: `tests/scenarios/32-diagnose-visual-recipe.md`. See archive for full entry.

## FB-086: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle). Drift detection sub-check at `verify-agent.md § Step T2b step 4b` (existing `verification_gap` kind; pass-with-warning); orchestrator auto-update of `files_affected` at `commands/work.md § "After verify-agent returns" step 8`. Pre-pass parallel surface (FB-058 6th heuristic) deferred. Research at `.claude/support/workspace/fb-086-research.md`. See archive for full entry.

## FB-087: [ARCHIVED — moved to `template-maintenance/feedback-archive.md`]

**Status:** archived 2026-07-19 — cheap action shipped v4.7.3; optional helper remainder signal-gated with no signal (38-export harvest checked). Re-capture on a multi-project large-DOM signal. Full entry in archive.


## FB-088: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle). Step 0e inline uncommitted-work check at `commands/work.md § "Step 0e: Uncommitted-Work Check"`. Always runs; surface only when N≥3 finished tasks since last commit AND non-zero modified/untracked. Heuristic-only `.claude/` exclusion filter. Dashboard sentinel deferred. Research at `.claude/support/workspace/fb-088-research.md`. See archive for full entry.

## FB-089: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-24 via v4.8.0 (5-FB cheap-action bundle). Option 1.5 (recover-by-compile-then-cleanup) shipped as Step 0f in `commands/work.md § "Step 0f: Track 2 Stale-File Recovery"`. New `export_quality: "recovered"` enum value. PreCompact hook unchanged (disjoint Track 2 territory). Research at `.claude/support/workspace/fb-089-research.md`. See archive for full entry.

## FB-090: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-24 via v4.10.1 (cheap action). Made Recent Activity cap enforcement non-discretionary + added "cap-trim" as a targeted-edit-eligible pattern in `dashboard-style/SKILL.md` + `dashboard-regeneration.md` mirror (two edits each). Promotion trigger: FB-080 (targeted-edit path) shipped in v4.7.0, weakening the regen-cost deferral reason. See archive for full entry.

## FB-091: [CLOSED — moved to `template-maintenance/feedback-archive.md`]

**Status:** closed 2026-05-27 — declined during a `/feedback review` walk-through. Residual too thin: the common form (chaining edits via bash) is already discouraged by the Tool Preferences `Edit`-not-bash-chain rule; the genuine residual (a speculative probe short-circuiting a legit git/test/script batch) is narrow and unreproduced in session exports. Single-source signal (insights report). Sibling FB-092 closed in the same pass. Re-open on a real session-export reproduction. See archive for full entry.

## FB-092: [CLOSED — moved to `template-maintenance/feedback-archive.md`]

**Status:** closed 2026-05-27 — declined during a `/feedback review` walk-through. Core premise ("don't assume CWD persists across steps") is contradicted by the harness contract: the Bash tool's working directory *does* persist between calls; only shell *state* (env vars, functions) doesn't. Absolute-path discipline is already implied (dedicated tools take absolute paths; harness recommends absolute paths to avoid `cd` prompts). Only concrete residual was the `>`-vs-`>>` session-log sub-signal — too thin for a rule. Single-source signal (insights report). Sibling FB-091 closed in the same pass. See archive for full entry.

## FB-093: Empirical capability-probe workflow — brain-dump examples → verdict each against the live system → accumulate a snapshot-anchored capability-boundary corpus

**Status:** PROMOTED — shipped **v4.11.0** (2026-05-27). DEC-019 approved (Option A); `/shakedown` command + `.claude/support/shakedowns/` + integrations shipped. Records: `decisions/decision-019-shakedown-command.md`, `template-maintenance/shakedown-workflow-vision.md § "Resolution (post-grill, 2026-05-27)"`, research `.claude/support/workspace/fb-093-research.md`.
**Captured:** 2026-05-27
**Source:** Surfaced by Erik from two styler CLI transcripts (2026-05-27). A `/grill` session scaffolded `personal-style-rule-corpus-2026-05-27.md` (protocol + verdict legend + "Model so far" + seeded examples R-01..R-04); a fresh session then *ran the brain-dump* — Erik fed personal style rules one at a time, Claude broke each down against the engine's actual rule model, verdicted it (✓ expressible / ⚠ needs new capability / ✗ out-of-model / 🎨 dose-nuance / ❓ ambiguous), refined a shared "Model so far / Parked / Boundary criteria" between examples, steered toward edge-revealing inputs, and wrote each entry into the doc as the persistence layer. Companion `engine-rule-expressiveness-gap-2026-05-27.md` (both docs live in the styler repo, not CCE). Full transcripts + extracted meta-protocol in this session; design analysis in `.claude/support/workspace/fb-093-research.md`.

## The workflow (generalizable; domain-agnostic)

A structured probe of an **existing** system against the user's real / desired examples — "working from the end" (the built product) rather than forward from the spec. Six phases:

0. **Calibrate the lens** — read the current system (spec + code + glossary); state back, *before any input*: the dimensions each example is decomposed against, the verdict legend, the cleave/heuristic, what trips a "new dimension" finding, the per-example output contract. *(This is the "narrow down what it's checking my feedback for" preamble Erik flagged as essential.)*
1. **Probe loop** (per example) — plain restatement (+ flag if it forks into 2+ items) → structured breakdown → **ground against the actual system** (expressible? *why not*, precisely? is there an approximation, and does it *flatten* the intent?) → verdict → write the entry immediately (the doc is the persistence layer; survives `/clear`).
2. **Maintain the model** between examples — refine the shared "Model so far / Parked / Boundary criteria" as findings accumulate (model-*building*, not a checklist).
3. **Steer** — hypothesis-driven; request the highest-signal next input ("the model has never been tested on a relation between two items — I bet that's where it breaks").
4. **Stop signal** — saturation: stop when new examples stop revealing new dimensions; announce proximity.
5. **Defer & route** — batch hard sub-questions ("is this already in the engine?") to `/research` instead of breaking flow; surface genuine forks with a recommendation + record the user's call with attribution + date; exit → distill the model → `/research` the forks → `/iterate` → `/work`.

**Output is triple-duty + snapshot-anchored:** ✓ = acceptance probes (what works now); ⚠/✗ = gap analysis (what to build / what's out); Parked + boundary map = forward-direction. The dated doc = *"where the system is and where I want it, as of date X"* — direction for a large, long-running project.

**Genericization principle:** ship the *meta-protocol*; **derive the lens per-project** at Phase 0 (the styler dimensions — mechanism/bite/direction/when/unless — are an *instance*, not the spec). Same pattern as `/diagnose` shipping a methodology, not bug-knowledge.

## Design forks (full analysis in the research doc)

1. **Surface — the governing decision.** New `/probe` command vs `/grill` sub-mode vs fold-as-recipe-into-`/grill` vs document-as-workflow-pattern (rule/reference, no command). **Must clear the strong CCE prior:** DEC-018 declined the interpretive router after a value deep-dive; `/visual-verify` was *folded into `/diagnose`* rather than shipped (FB-085 § "Resolved design") — default is *fold unless standalone is earned*. The case FOR standalone: the probe is the **inverse flow** of grill (user *asserts* → Claude *verdicts*, vs grill's Claude *asks* → user *answers*) — not an instance of grill the way visual-verify was an instance of diagnose.
2. **Artifact home / type.** A new artifact (empirical, snapshot-anchored, triple-duty). Candidates: `.claude/vision/` sibling, new `.claude/support/probes/`, `.claude/support/learnings/`, or workspace-graduate. Styler put it in `workspace/` (scratch — wrong for a durable artifact).
3. **Genericization mechanism** — Phase 0 calibration is the seam (ship the instruction + verdict-legend schema + the styler lens as a marked illustration).
4. **Routing onward** — exit ramps from verdicts to `/iterate` / `/research` / FB items / `test_protocol` seeds.

## Triage recommendation

Research-gated → **likely DEC on fork #1** (surface) only if the resolution is *standalone command* (real surface, DEC-018-class). The CCE-native way to settle fork #1 is to **`/grill` the design itself** — exactly how `/visual-verify` was resolved (`template-maintenance/visual-verify-vision.md`) — seeded by a `template-maintenance/probe-workflow-vision.md`. If the grill concludes *fold / pattern-doc*, no DEC (trivially reversible, per FB-085's reasoning). Forks 2-4 resolve downstream of fork #1. Adjacent to FB-067 Wave 2 (`/prototype`, `/improve-codebase-architecture`) and the deferred "help-me-think umbrella" (`router-survey.md` § 5) — cross-check family membership before adding standalone surface.

Tags: workflow, new-command-candidate, grill-adjacent, vision-adjacent, capability-probe, gap-analysis, snapshot-anchored, surface-discipline, research-gated, dec-candidate, styler-bridge

## FB-094: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-27 — shipped **v4.12.1** (PATCH). `claude-code-authoring.md § "Skill listing budget"` rewritten to separate the dynamic total budget (~1% of context; `skillListingBudgetFraction` / `SLASH_COMMAND_TOOL_CHAR_BUDGET`) from the per-entry 1,536-char cap (`maxSkillDescriptionChars`), with overflow behavior + a `/doctor` + `/skills` observability note. Verified against `code.claude.com/docs/en/skills` (2026-05-27) before fixing; the unverified `/context`-as-load-inspector half of point 3 was dropped. Footer `Last verified` + `template_version` bumped. See archive for full entry.

## FB-095: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-06-12 — `/research` → **DEC-021 Option 2** (single file + generated spec section index + section-scoped read discipline) shipped in **v4.24.0**. `fingerprint.py --index` + `--sections --depth 3` (additive `### ` hashes); canonical `rules/spec-workflow.md § "Section-scoped spec reading"`; `work.md` Step 1b index-freshness; subagent scoped-read pointers. **Preserves the "exactly one `spec_v{N}.md`" Critical Invariant** (sharding/tiering declined on the blast-radius asymmetry). DEC-021 `implemented` (7 anchors); record `decisions/decision-021-spec-scale-architecture.md`; research archive `.archive/decision-021-research-2026-06-12.md`. See archive for full entry.

## FB-096: [RESOLVED — moved to `template-maintenance/feedback-archive.md`]

**Status:** resolved 2026-06-11 — sub-issue A (capability-doc model-surface drift) docs-verified + rewritten in v4.21.3; sub-issue B (pin re-evaluation) decided → option (a) ratify the float, shipped v4.21.4 (`.claude/CLAUDE.md § Model Requirement` now targets the current Opus tier via `opus[1m]` with an explicit-pin regression escape hatch). See archive for full entry + both resolution notes.

## FB-097: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-06-12 — `/research` → **DEC-022 (Option D = A+C)** shipped in **v4.26.0**. Declares `.claude/verification-result.json` `criteria[]` (dashboard `### Acceptance Criteria`) the authoritative phase acceptance-*status* surface; inline spec `- [ ]` boxes are authored input (not auto-ticked); new advisory `/audit-coherence` `acceptance-reconciliation` lens flags divergence. Research **declined** the FB-097-leaned Option B (unsafe `criteria[]`→box mapping, drift-fingerprint cost, RTM/BDD/DOORS anti-pattern). See archive for full entry + Q1–Q7 findings.

## FB-098: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-06-12 — shipped in **v4.23.0**. `.claude/scripts/persist-friction.py` (+ 11 tests, 65/65 suite green) mechanizes the friction dual-write + audit-register projection with collision-safe `FR-NNN` (max of register ids AND textual `FR-<n>` refs); read-only, orchestrator appends. Advisory wiring in `work-procedures.md § "State Persistence Protocol"` step 2 + `scripts/README.md` row; recorded against the parked Family F checker in `scripts-candidates.md`. See archive for full entry.

## FB-099: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-06-12 — shipped in **v4.23.0**. (a) `/work` Step 0e `.claude/`-exclusion scoped to gitignored paths only (tracked `.claude/` source now counts); (b) new `/health-check` Part 4 check 5 — informational `git check-ignore` report when spec/tasks/decisions are untracked ("deliberate? consider a backup convention"), never blocks. See archive for full entry.

## FB-100: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-06-12 — shipped in **v4.23.0**. (a) `/work` Step 1d fast-path predicate extended with `owner == "both" AND user_review_pending` + physical-prerequisite modeling note; (b) `work-procedures.md § "Task Completion"` documents the both-owned completion shape (user-half self-attests like `owner: human`; lived/conversational gates close without a verify-agent round-trip). Builds on v4.14.0's visibility half. See archive for full entry.

## FB-101: [CLOSED — moved to `template-maintenance/feedback-archive.md`]

**Status:** closed 2026-06-22 — declined during a `/feedback review` walk-through (same-day capture → triage). Value-validation gate unclearable from the source (no project attribution, no count, "500-token" report artifact) AND zero template-side reproduction: **0/66** `interaction-logs/processed/` exports show the death-marker `unclear_from_transcript` (positive-control grep sound: friction 69 / session 66 files), and every token/truncation mention is an already-shipped pattern (FB-087 Playwright) or successful 32K-budget self-regulation (FB-080 targeted-edit, script-first render). Cheap mitigation already substantially in place (the named cascades fan out + write to disk — see FB-102). FB-091/092 shape (single-source insights signal, residual covered). Re-open: an *attributed* template-cascade truncation death in a session export (via `/health-check` Part 7), not the aggregate report. See archive for full entry.

## FB-102: [CLOSED — moved to `template-maintenance/feedback-archive.md`]

**Status:** closed 2026-06-22 — named-sweep half declined during a `/feedback review` walk-through; thin ad-hoc usage-habit note also declined. Triage Q1 answered by reading the command defs: the named sweeps already fan the *analysis* phase out to subagents and capture inputs to disk; the inline part is deterministic capture of *enumerated* known paths that MUST stay inline (writes to `.claude/`, which subagents can't per DEC-004; Playwright MCP can't fan out). Nothing to "discover" → no pre-pass warranted. FB-101 triage (0 template-side deaths) confirms the fan-out coupling is already satisfied for template work. "Parallel Agents Per Spec Phase" stays a separate horizon item (adjacent FB-067 Wave 2), not folded in. See archive for full entry.

## FB-103: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-07-19 — shipped v5.3.0 (recovery branch + pre-flight budget checks). Full entry in archive.


## FB-104: Multi-session concurrency on one repo — no template model

**Status:** cheap slice shipped v5.3.0 (2026-07-19) — pre-dispatch `git status` re-check (parallel-execution.md), handoff preserve-not-consume exception (work.md Step 0a), Concurrent Sessions conventions section (rules/session-management.md). Full concurrency model remains research-gated on recurrence.
**Source:** harvest 2026-07-19; styler 06-13-2215, 06-16-0100, 06-25-0905; tinder 06-14-1540, 06-14-1605; flirty-gym 06-17 — 4+ sessions, 3 projects

**Problem.** The template assumes one session per repo. Observed with two concurrent sessions: `.handoff.json` overwrite/consume races (consuming a parallel thread's handoff would lose its context — handled ad-hoc by preserve-not-consume + later merge); git-index races ("modified since read"); a concurrent session's `git add` sweeping this session's tracked edits into its commit (entangled provenance); a verify-agent reporting files "modified" that a parallel session had touched (extra investigation pass); commit-ownership ambiguity for files a parallel session created but never committed.

**Cheap slice (direct edit):** (a) re-check `git status` immediately before parallel agent dispatch, not only at Step 0e session start (06-16 pushback: a concurrent retirement broke the tree mid-batch); (b) handoff preserve-not-consume when the handoff references another session's in-flight task; (c) a one-line "single-committer convention" note for overlapping sessions.
**Full model** (session registry, lease/lock, cross-session state signal): route through `/research` if recurrence continues after the cheap slice.

**Harvest 2026-10-03 evidence (+1, PortfolioWebsite, a fourth project, after the cheap slice shipped; cluster 15). Evidence only; the research gate is unchanged.** A second session on the same tree was found only from three unexplained modified files. The single-committer convention held (disjoint files, no `git add -A`, zero conflicts), but Step 0e can't attribute uncommitted files, so "another session is editing" reads like "you forgot to commit" (08-20-1330).

## FB-105: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-07-20 — shipped v5.4.0 (script-owned Action Required + augment slot). Full entry in archive.


## FB-106: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-07-20 — shipped v5.4.0 (pending_decomposition marker; doc half shipped v5.3.0). Full entry in archive.


## FB-107: Phase gates — distinguish build-blocking from validation (human real-use) gates

**Status:** captured 2026-07-19 (harvest Tier-2 E); single-project signal — second-signal-gated
**Source:** harvest 2026-07-19; tinder 06-27-0814

**Problem.** Phase 10's build became phase-gated behind T81 — a Phase-9 *real-use* acceptance task (`owner: human`) that needs live activity and cannot be forced on demand. Gating the next phase's BUILD behind an un-forceable human VALIDATION stalls the build; the only workaround was manually setting `cross_phase: true` on every build task.

**Proposed:** distinguish "build-blocking" from "validation" phase gates (schema or gate-metadata level — needs design), so a human real-use acceptance can remain open while the next phase's build proceeds. Cheap interim: document the `cross_phase` workaround in `phase-decision-gates.md`. Escalate to `/research` on a second project hitting it.

## FB-108: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-07-19 — shipped v5.3.0 (owner:both personal-data verification shape in work-procedures.md). Full entry in archive.

## FB-109: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-08-12 — shipped v5.5.0: new `.claude/scripts/persist-session-export.py` (+ 19 tests, 111/111 suite green) mechanizes the inbox copy-with-rename, invoked from `/work pause` Session Export step 6 + `/work` Step 0f step 8 (`--suffix recovered`). Never-dot-prefixed destination enforced structurally; the one shipped script that writes a file (external `template_inbox_path`, never `.claude/`). Wired in `context-transitions.md § "Session Export"` step 6 + `work.md`; `scripts-candidates.md § Family F` F2 records the ship (F1 stays parked). See archive for full entry.

## FB-110: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-08-12 — shipped v5.4.4: `#### Repo-type carve-out (template repo)` added to `commands/health-check.md` Part 2b; bloat thresholds skipped (advisory `ℹ️`) when the `template-maintenance/` sentinel is present. Mirrors Parts 5/5d/7. See archive for full text.

## FB-111: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-08-12 — shipped v5.4.4: `### Repo-type branch (template repo)` added to `commands/health-check.md` Part 3 + a branch on the Step 1 scan line; scans root `decisions/decision-*.md` when the `template-maintenance/` sentinel is present (the shipped `.claude/support/decisions/` is the empty placeholder here). Mirrors Parts 5/5d/7. See archive for full text.

## FB-112: Doc-hygiene trio — stale topology map, dead toggle in the sidecar schema, inconsistent anchor shapes

**Status:** (b) shipped v5.7.5 (2026-10-02); (a), (c) and (d) open — small independent sub-items, bundled per the FB-006 precedent
**Captured:** 2026-08-12 (health-check + impact-assessment side findings)
**Source:** template-repo `/health-check` 2026-08-12. None of these blocks anything; all three are drift between a doc and the thing it describes.

**(a) `template-maintenance/architecture-map.md` is four versions stale.** Its machine-read `**Current as of:** v5.1.1` line predates v5.2.0 → v5.4.3. v5.4.0 in particular added script→state derivation edges (FB-105's `_html_needs_you()` reads sidecar `phase_gates`, `drift-deferrals.json`, `audit_digest`, and parses `feedback.md`) that the dependency-edges table may not reflect. Reconcile the map against HEAD and bump the line. Note the map's own discipline: *"Update it when topology changes."*

**(b) `support/reference/dashboard-regeneration.md:96–103` documents a dead toggle.** The canonical `section_toggles` schema block still lists `tasks: true` as if it gates a section. Post-DEC-024 there is no standalone Tasks section (replaced by the phase heatmap / front-cards / dependency graph), and `dashboard-render.py` reads only four toggle keys — `action_required` (:1145), `decisions` (:1156), `custom_views` (:1160), `notes` (:1170). Unknown keys are silently ignored via `dict.get(key, default)`, so this is doc-only drift with no runtime effect — but it misleads anyone authoring a sidecar by hand. Verify the full key list against the script and correct the schema block.

**(c) `implementation_anchors` shape is inconsistent across the decision corpus.** Four styles in use across 21 records: bare path + trailing `#` YAML comment (the comment is parser-stripped, so the description survives only as raw text); bare path with no annotation; bare string with prose embedded in the value; and the `- file:` / `description:` mapping. **Only DEC-021/022/023 — 3 of 21 — use the shape `.claude/support/reference/decisions.md` actually prescribes.** No automated consumer parses the field (grepped `.claude/scripts/*.py`, `scripts/pre-commit-hook.sh`, `audit-coherence.md` — zero hits), so nothing is broken today; the cost is that a strict-YAML reader flags valid entries and the corpus can't be machine-audited. **Hazard when normalizing:** a plain scalar in a YAML block sequence cannot contain colon-space — that exact mistake invalidated four records' frontmatter mid-edit on 2026-08-12 and had to be walked back. Either quote the scalars or avoid `: ` entirely. Do this as its own pass; it was deliberately kept out of the v5.4.3 anchor-annotation ship to avoid multiplying that diff.

**(d) Template decision records fail `/health-check` Part 3 check 4** (added 2026-10-02). With the template-repo branch scanning root `decisions/`, 8 of 22 records lack `## Decision` and DEC-003 lacks `## Options Comparison` (verified by grep; the 14 records that have `## Decision` are the control). Normalize alongside (c).

## FB-113: `files_affected` derivation under-counts in a new domain — cross-artifact doc↔notebook parity + dispatch-brief re-sync

**Status:** cheap action shipped v5.7.0 (2026-09-27) — general "search for what the change invalidates" rule at decomposition + implement-agent Step 2; scope note as dispatch authority. Measure at 2026-12-31: verify-agent `files_affected` mismatch rate vs 13% baseline (16–29%/month Jul–Sep). Still open: `package.json` parallelism sub-issue; domain-specific heuristics only if the rate doesn't drop.
**Captured:** 2026-08-12 (harvest cluster 1; extends 2026-06-11 predecessor)
**Source:** 9 unique incidents across OEMMatInsightBI exports 2026-07-23 → 2026-08-11 (template_version 5.1.0–5.4.0). Full evidence + insight doc: `interaction-logs/insights/2026-08-12_implement-agent_files-affected-derivation.md`.

**Predecessor — extends, not newly discovered.** `interaction-logs/insights/2026-06-11_implement-agent_files-affected-ripple.md` deferred a new FB until *"post-v4.8.0 exports still show high reconciliation noise."* That trigger is now met: post-v4.8.0 (v5.1.0–5.4.0) exports still produce 9 distinct `files_affected`-derivation incidents in a three-week stretch. FB-086's auto-union is firing (residual cost is noise, not missed state), but the *prevention* layer is absent for this domain.

**Problem.** `files_affected` is derived once at decomposition and never re-derived, even when the task's own notes, the schema, or the implementation expands the surface. Four recurring shapes in this corpus:

1. **Schema-change tasks omit downstream readers.** A column/grain change falsifies the state-asserting schema doc (`gold_tables.md`), DAX measures (`quality_measures.dax`), SQL views (`create_quality_views.sql`), and the aggregating notebook — all absent from `files_affected`, forcing reactive multi-pass consumer sweeps. task-027 (1 declared / 4 modified), task-038_2 (grain-change; three reactive passes), task-038_4 (3→4; "two consecutive subtasks" on the same column list).
2. **Scope-note vs `files_affected` desync.** task-033's own newer scope note named two files the original decomposition omitted AND wrong-pathed them; the `/work` dispatch brief fences writes to `files_affected` alone, so the two instructions actively conflict — first dispatch shipped 7 of 9 files.
3. **Semantic-model changes omit `docs/architecture/semantic_model.md`.** task-061.
4. **Declared-vs-actual drift on in-scope extras.** task-029 (3→7), task-045 (1→2), task-049 (10→14, the marquee count). Detection fires only post-verification via verify-agent mismatch — *"an implementer who under-scopes and a verifier who under-checks would both miss it."*

**Dedup — not a duplicate.** FB-058 (decomposition pre-pass Leg 2, 5 ripple heuristics), FB-086 (verify-side drift detection + auto-union, v4.8.0), and v5.2.0's two ripple heuristics cover CSS / test-factory / enum-extension ripples. This is a different ripple domain: cross-artifact docs↔notebook parity (schema/DAX/SQL/notebook describing one column set; semantic-model → architecture doc) and dispatch-brief re-sync when a scope note post-dates `files_affected`. The "Synchronized Locations: Enums, Unions, Dispatchers" heuristic is the natural home for an extension to table-schema changes + downstream readers.

**Likely eventual blast radius:** `support/reference/decomposition.md` (Ripple Inference / Pre-Pass Leg 2 — extend Synchronized Locations to schema changes + downstream readers; add grain-change consumer inventory; add semantic-model → architecture-doc ripple); `commands/work.md` dispatch-brief construction (re-derive scope from the newest scope note, not the original `files_affected`). The predecessor's parked "project-recurring ripple memory" (≥3 reconciliations in one project → auto-include the class) now has a concrete trigger: the schema-change consumer-sweep shape reconciled 3× in this one project.

**Single-project caveat noted, does not gate — superseded 2026-09-25 (styler corroborates; see harvest evidence below).** The 2026-06-11 predecessor already established `files_affected` under-declaration as the single most recurrent friction class across 4 projects; this corpus shows the residual noise in a new domain post-v4.8.0, so the single-project framing here does not weaken the case.

**Harvest 2026-09-25 evidence (+6 incidents, now two projects — `template-maintenance/harvest-2026-09-25-triage.md` cluster 1).** oemmatinsightbi: prose docs that summarise a changed DAX/code pattern fell outside declared scope (task-065, 08-13: 2 declared → 4 actual), and a gold column-set change left two schema docs describing a removed column (task-074, 08-20). **styler (template 5.0.0), a new project for this item:** shared response types, a reused eligibility-helper signature, new test files, and **`package.json` test-script wiring** were under-counted on T866 (09-21), T870 + T869 (09-24), and T890 (09-24). `package.json` test wiring touches nearly every task, so it defeats the file-overlap parallelism heuristic unless it's exempted. A decomposition also split a type-narrowing task from the sibling task holding the consumer repair that the narrowing forces (09-21). **The single-project caveat above no longer applies.**

**Harvest 2026-10-03 evidence (+9; PortfolioWebsite is the third project; cluster 8).** The 5.4.0 shapes add: class-gating fixes that live in a shared stylesheet and layout (task 174); a `files_affected` naming the wrong component entirely (175); a prop threaded through a layout wrapper (196); collection renames (213); and validation-script wiring across `package.json`, README and root `CLAUDE.md` (201, 202), which is this item's open `package.json` sub-issue again. **First post-v5.7.0 data (5.7.4):** PortfolioWebsite task 230 (3 declared, 6 actual, including a higher-specificity duplicate rule); styler T898 (a registry-consumer edit also needed the zod enum, the TS union and the top-level consumers list, which is the Synchronized Locations heuristic's own domain). Feed both into the 2026-12-31 mismatch-rate check.

**Shared root with FB-115.** The 08-12 export named both items as one missing discipline: list what a change *invalidates*, not what it *edits*. FB-113 is the decomposition-time half (declared scope); FB-115 is the closure-time half (sweep scope). They stay separate because the fixes live in different files (`decomposition.md` vs `verify-agent.md`), but design either with the other in view.

Tags: implement-agent, decomposition, files_affected, cross-artifact-parity, dispatch-brief, extends-FB-058, extends-FB-086, extends-2026-06-11-predecessor, two-project-signal, cross-references-FB-115

## FB-114: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-10-03 — shipped v5.8.0 (tool-agnostic negative-findings rule + `support/reference/negative-findings.md`). See archive for full entry.

## FB-115: Closure sweeps verify the phrasings you changed, not the claim's full surface — lexical vs structural

**Status:** cheap action shipped v5.7.1 (2026-09-27) — verify-agent T2c item 4 (search by what the claim is about, task-ID status cross-reference, ungated mirrors, re-dated anchors) + `/iterate` Step 5 dated-anchor line. **Single-project caveat superseded 2026-10-04** (PortfolioWebsite and styler; see the 2026-10-03 harvest evidence). The drift-reconciliation fingerprint-blindness note (incident 2) **shipped v5.9.0** with FB-128 (`drift-reconciliation.md` § "What fingerprints can't see (FB-115)"); its second-project trigger was met by PortfolioWebsite 09-19-0210. Still open: the 2026-10-03 evidence's status-prose rot (2) and the rule-file mirror missed at `/iterate` apply (3).
**Captured:** 2026-08-12 (harvest cluster 5)
**Source:** 5 unique incidents across OEMMatInsightBI exports 2026-08-05 and 2026-08-10. Full evidence + insight doc: `interaction-logs/insights/2026-08-12_verify-agent_closure-sweep-lexical-vs-structural.md`.

**Problem.** Closing a finding by sweeping for stale status assertions reliably produces a false "clean" when the sweep is scoped to the phrasings the pass just rewrote. The implementer verifies its *changed* strings return 0 occurrences and passes — but stale assertions using *different vocabulary* survive three lines below an edited paragraph. The repeated response is to widen the **lexical** surface (phrasings changed → improvised status words → "canonical" word list) rather than switch to a **structural** cross-reference. Same lexical-vs-structural gap in two adjacent mechanisms:

1. **task-057 — the 14th stale assertion + three consecutive rounds.** Sweep verified the 13 phrasings it had *changed* returned 0, passed, missed a 14th stale assertion using vocabulary the pass never touched (`unobserved`). Three consecutive verification rounds each found exactly one more; each response was to widen the sweep vocabulary rather than switch to a structural task-ID cross-reference. *"A sweep scoped to the strings you edited is structurally blind to the ones you didn't — it confirms your edits landed, which is not the same as confirming the claim is now true everywhere."* Structural fix: cross-reference EVERY task-ID mentioned in the spec against that task's status; flag any line pairing a Finished/Absorbed task with incomplete-flavoured wording.
2. **Drift detection vs section fingerprints (08-05, phase-level).** Three of four false status assertions sit inside sections whose fingerprints are CURRENT, so drift reconciliation reports the spec aligned while it misdescribes shipped capability. *"Fingerprint-based drift detection is structurally blind to a claim that was already wrong when it was pinned."* Generalizes the project-side FR-052 (not a template FB) beyond its single instance. Adjacent to the DEC-021 section-fingerprint machinery.
3. **Ungated mirror surfaces (08-05, task-010).** When a task closes a criterion other documents describe as deferred, nothing ties the closure to ungated mirror surfaces. The descope was tracked against three DEC-016-gated surfaces (approval routing); the two ungated mirrors repeating the same deferral were not enumerated — *"the CHEAPER fixes were the ones missed."*

**Dedup — not a duplicate.** No existing rule or reference doc addresses the closure-sweep lexical-vs-structural gap as generalized guidance (verified: zero hits for `closure sweep|criterion vocabulary|task-ID cross-reference|ungated mirror|enumerate-and-classify` across `.claude/rules/`, `.claude/support/reference/`, shipped feedback). **Incident 5 (task-062 AC-sweep lexical under-match) is shared with FB-114 Adjacent B** — same lexical-vs-structural root, different surface. FB-114 owns the negative-findings-control framing (whether the probe's *pattern* is complete); FB-115 owns the closure-sweep framing (whether the sweep covers the *criterion's* vocabulary, not just the phrasings changed). Cross-referenced, not re-captured.

**Proposed.** Add a closure-sweep methodology sub-section to `.claude/agents/verify-agent.md`: a sweep closing a stale-assertion finding must cover the *criterion's* vocabulary (or cross-reference every task-ID against its status), not just the phrasings the pass rewrote — confirming edits landed ≠ confirming the claim is now true everywhere. Consider whether `support/reference/drift-reconciliation.md` should note the fingerprint-blindness sub-shape (a section can be fingerprint-current while misdescribing shipped capability).

**Likely eventual blast radius:** `.claude/agents/verify-agent.md` (closure-sweep methodology — primary home); possibly `support/reference/drift-reconciliation.md` (DEC-021 section-fingerprint machinery, adjacent for the fingerprint-blindness sub-shape).

**Single-project caveat.** 5 incidents, single project (OEMMatInsightBI), single five-day stretch — above the 3-occurrence floor but single-project. Framed like FB-076 / FB-084 / FB-107, not as an unqualified `ready`. Re-assess for promotion (drop the caveat) on a second project signaling the same closure-sweep gap.

**Harvest 2026-09-25 evidence (+3, all oemmatinsightbi, so the caveat stands — `template-maintenance/harvest-2026-09-25-triage.md` cluster 3).** (1) **Four sites in one session (08-12).** A friction-to-task translation normalised a name by assumption (FR-078). task-069's AC4 had five sites where the brief implied one. task-070 failed verification twice on file-scoped rather than value-scoped doc sweeps. An `/iterate` drain found a stale line because MQ-001's earlier fix had been section-scoped. (2) **New mechanism: re-dating re-certifies.** Moving a section's "measured YYYY-MM-DD" anchor silently re-certifies every count beneath it, turning an honestly stale claim into a falsely fresh one. This caused task-076's first verification failure (08-21: 45 vs 54). Cheapest fix: an `/iterate` spec-edit checklist line, "when moving a dated anchor, re-measure every figure it governs". (3) **Synonym-blind residue sweeps.** After correcting three "HQ relationship" claims, the residue sweep searched those three phrases and missed a fourth site ("rolled to supplier HQ country") falsified by the same correction; the verifier caught it (09-19). Same lexical-vs-structural root as incident 1 above. *(Stale annotations about live or orchestrator-written state are filed under FB-119, not here.)* See also FB-113 § "Shared root with FB-115".

**Harvest 2026-10-03 evidence (+9, PortfolioWebsite and styler, so the single-project caveat no longer applies; cluster 9).** (1) **Fingerprint blindness in a second project:** a spec bullet that was wrong the day it was written registered zero drift for eight days across four cleanup passes (PortfolioWebsite 09-19-0210). That meets the trigger for the deferred `drift-reconciliation.md` note (incident 2 above). (2) **Status prose rots one decision-close behind:** § Remaining Work went stale four times, and each cleanup wrote the next stale bullet (FR-049, FR-052, FR-068, line 190; 09-08-2329 → 09-19-1234). Decision records' Residual and Risks sections contradicted shipped behaviour within hours (09-19-0005, 09-19-1234). Fix suggested in the export (09-19-0110): the spec records standing constraints only and in-flight work lives in tasks, or `/iterate` sweeps such sections when a decision closes. (3) `/iterate` updated the spec but not the project rule file named in the decision's Impact section (styler 09-28-1923). The PortfolioWebsite evidence predates v5.7.1.

Tags: verify-agent, closure-sweep, lexical-vs-structural, drift-detection, section-fingerprints, ungated-mirrors, re-dating, cross-references-FB-114, cross-references-FB-113, single-project-signal

## FB-116: verify-agent runtime_validation — third failure mode (no local execution environment) + the local-ceiling-determination gap

**Status:** ready — sibling extending FB-076 (NOT a duplicate; FB-076 mitigations 2 + 3 stay gated)
**Captured:** 2026-08-12 (harvest cluster 3; extends 2026-06-11 predecessor)
**Source:** 6 core incidents + 3 same-family across 4 artifact classes, OEMMatInsightBI exports 2026-07-23 → 2026-08-12 (template_version 5.1.0–5.4.0). Full evidence + insight doc: `interaction-logs/insights/2026-08-12_verify-agent_runtime-validation-local-ceiling.md`.

**Relationship to FB-076 — extends, not duplicates.** FB-076 documents exactly two `runtime_validation` failure modes: (1) client/server bundle boundary (mitigation 1 shipped v4.15.0), (2) catalog-state-dependent precondition (mitigation 3, deferred). This item is a **third mode**: *no local execution environment for the artifact class at all.* It satisfies FB-076's defer condition **(b)** (broader `runtime_validation` hardening need), **not (a)** (the *same* verification gap). Same framing FB-076 used extending FB-066, and FB-084 used extending it again. FB-076 has been amended with a one-line note pointing here; the status of its mitigations 2 + 3 is unchanged.

**Why mitigations 2 + 3 stay gated.** Mitigation 2 (ESLint client-import rule) targets the client/server bundle boundary — a PySpark / Fabric / Power BI stack has **no client/server bundle boundary at all**, so unlocking mitigation 2 on this evidence is a category error that would scope real design work against inapplicable evidence. Mitigation 3 (live-data cross-reference for catalog-state preconditions) is only a partial spirit-match (closer in "can't fully trust a local pass") but still not its documented failure mode. Both remain research-gated on their own evidence.

**Problem.** Artifact classes with no local execution environment pass verify-agent's structural gates and break at runtime in the real environment. `runtime_validation` lands `"not_applicable"` and the real proof is deferred to a criterion no agent can mechanically discharge. Four artifact classes in this corpus:

1. **Fabric PySpark notebooks** — no Spark session, no lakehouse; every notebook-touching task lands `runtime_validation: "not_applicable"` (task-040, 07-23).
2. **TMDL semantic models** — no TMDL parser installed; `fabric-cicd` validates only at publish, and a push to main fires a real publish, so there is no safe dry-run. Verification fell back to byte-level indentation comparison + running the DAX as a `DEFINE MEASURE` via `executeQueries` (proves the expression parses, says nothing about the TMDL envelope) (task-061, 08-11).
3. **GitHub Actions workflows** — task-046's `deploy-fabric.yml` passed local YAML parse + `fabric-cicd` API inspection, then failed *every* real Actions run at `setup-python` (`cache: pip` requires a `requirements.txt`/`pyproject.toml` the repo lacks). The local ceiling for Actions is YAML syntax + API signatures; action-runtime behavior is invisible until a real runner executes it.
4. **Live Delta row counts + Delta writers** — spec assertions quoting 903 / 2,560 / 3,463 rows cannot be re-derived (no local lakehouse read path; the Fabric REST tables endpoint returns names only, no row counts) (task-057, 08-06); and a column-TYPE change invisible locally (no Delta writer invoked) took down `bronze_to_silver` on the first Fabric run (task-064, 08-12). `delta-spark` absent made a missing `overwriteSchema` on a schema-widening Delta overwrite structurally invisible — recurred in a file that already carried the guard twice (task-038_1, 07-30). A task can reach 39/39 local with its single safety-critical line unexecuted (task-038_2, 07-30).

**The under-claim half — the more important part of the lesson.** One 07-23 marker (task-027) records the **opposite** failure: the task notes AND the dispatch brief both assumed source-reading was the ceiling for PySpark, and that was **false** — pyspark 4.0.1 + OpenJDK 17 were installed, and a `local[1]` SparkSession over an in-memory fixture executed the criterion end-to-end in under a minute, turning *"the explode should yield 0..N rows"* from an argument into a 9/9 measurement. The genuine local ceiling was *narrower than assumed* (Delta MERGE / time travel / lakehouse I/O, not PySpark itself). The under-claim propagated through a handoff that was never checked: *"a 'this cannot be tested locally' claim in a handoff deserves a 30-second check before it is propagated into an agent brief, because once it is in the brief the agent inherits the blind spot."* verify-agent caught it only by ignoring its own brief.

**The gap, stated plainly:** nothing forces an *honest determination* of what the local ceiling actually is, so agents both **over-claim** (pass `not_applicable` when local execution is possible — the default, every notebook task) and **under-claim** (assume source-reading is the ceiling when the pure-function layer is executable — 07-23). The over-claim is recurring noise; the under-claim is the rarer but costlier miss, because it silently downgrades a measurement to an argument. And nothing forces the verifier to *enumerate which specific lines fell outside the local ceiling* — when verify-agent did this voluntarily (07-30) it was the most useful part of the report.

**Proposed mitigation (candidate, not scoped here).** Require an explicit **declare-the-local-ceiling** step in `verify-agent.md` Step T4b: for any artifact class claimed locally unverifiable, (a) state *what was tried* (not just what was assumed — an honest determination, including a 30-second check of whether the runtime is actually installed), (b) enumerate the specific lines/paths that fell outside the local ceiling, and (c) emit a deferred live-validation follow-up task rather than silently passing `not_applicable`. Plus: a domain-neutral **runtime-evidence hook** in `/work`'s Empirical Evidence Gate (the gate is currently web-UI-only; this project's equivalent need — proving a data transformation landed in the live warehouse — had no template hook and was satisfied ad hoc by driving Playwright to the SQL endpoint).

**Dedup — not a duplicate.** FB-076 (two modes, mitigations gated), FB-066 (static class-export gaps, v3.16.0), FB-114 (this harvest — *probe reliability*, whether a negative-finding probe works), and the 2026-07-19 Tier 3 BSD-grep closure are all distinct. This is the *ceiling-determination* framing: whether the verifier honestly established what can run locally. The 2026-06-11 predecessor flagged this re-assessment as a watch item; this corpus is the post-v4.15.0 evidence it was waiting for.

**Likely eventual blast radius:** `agents/verify-agent.md` (Step T4b — declare-the-local-ceiling step + the "state what was tried, not just what was assumed" honesty contract); `commands/work.md` (Empirical Evidence Gate — generalise the web-UI framing to a domain-neutral runtime-evidence hook); project `./CLAUDE.md` (verification-hook declaration for non-web artifact classes).

**Single-project caveat noted, does not gate.** 6 core + 3 same-family across 4 artifact classes, single project (OEMMatInsightBI). The 2026-06-11 predecessor already established structural-green/runtime-broken as a 2-project class (styler + echothread); this corpus adds the *third failure mode* and the *under-claim* half in a new domain post-v4.15.0, so the single-project framing does not weaken the case for capturing — but promotion to a ship should weigh whether the declare-the-local-ceiling step generalises before scoping the design work.

**Harvest 2026-09-25 evidence (+4, styler on template 5.0.0 — `template-maintenance/harvest-2026-09-25-triage.md` cluster 4). A related failure: the environment exists but is temporarily unavailable.** (1) The Empirical Evidence Gate was blocked twice because Playwright MCP was held by the user's own Chrome (process-singleton conflict), and no headless browser is bundled as a fallback (09-21, 09-24). (2) **There is no "verify PASS held pending evidence" / "not run" state.** The evidence schema is pass|fail only, so a held report was parked in a workspace file and cross-linked from task notes to survive the pause (09-24). This belongs with this item's point that the verifier should honestly state what was reached. (3) Unbounded `while` loops in `browser_evaluate` hung the MCP call for 2+ minutes; bounded loops should be the documented pattern in `mcp-patterns.md` (09-24). **This does not meet FB-076 condition (a); mitigations 2 + 3 stay gated.**

**Harvest 2026-10-03 evidence (+11, PortfolioWebsite is the third project; cluster 10). It does not meet FB-076 condition (a); mitigations 2 + 3 stay gated.** (1) Playwright held by the user's Chrome (the project's KI-003) blocked rendered checks for whole sessions, and an orphaned MCP Chrome held the `SingletonLock` (09-24-1238). Two agents fell back to headless Chrome over CDP (09-08-2329). (2) **Surfaces that render on zero live routes** (draft-only content, unused component states: 09-07-2032, 09-08-2329, 09-11-0757, 09-15-1510, 10-02-0820) needed throwaway probe routes until the project built a component-gallery fixture. There is no "verified by construction, render deferred to task N" state. Unlike FB-076 mode 2, no verifier passed on mocks, so this is a reachability limit, not the same gap. (3) Deploy-host parity has no local instrument (Netlify Node version, build-host ratchet, `netlify.toml` redirects: 09-15-1510, 09-19-0005, 09-24-1238). (4) **Both halves of the local-ceiling gap:** deploy-log evidence was promised before checking whether any connector could return logs (09-15-1510, 09-18-1805), and later a stored "not possible" memory proved wrong when `netlify logs --source deploy` worked (09-24-1839).

Tags: verify-agent, runtime-validation, no-local-environment, local-ceiling, fabric, pyspark, tmdl, github-actions, delta, empirical-evidence-gate, extends-FB-076, extends-FB-066, extends-2026-06-11-predecessor, single-project-signal

## FB-117: Task/AC authoring internal consistency — the criterion is wrong at creation, at two authoring sites (decomposition + phase-level fix tasks)

**Status:** ready — the single-project caveat below is **superseded 2026-10-04** (PortfolioWebsite corroborates; see the 2026-10-03 harvest evidence). Originally 9 incidents, OEMMatInsightBI, 07-22 → 08-11. **Step 1d slice shipped v5.9.0** (with FB-128): Step 1d first resolves ticked decisions, then lists decision-gated tasks under `Waiting on decisions:` instead of treating them as Claude-actionable. Everything else here stays open.
**Captured:** 2026-08-12 (harvest clusters 4+6 merged)
**Source:** 9 unique incidents across OEMMatInsightBI exports 2026-07-22 → 2026-08-11. Full evidence + insight doc: `interaction-logs/insights/2026-08-12_task-ac-authoring-internal-consistency.md`.

**Why clusters 4 and 6 merge.** They share an anchor instance (task-063) and are the same defect class at two different authoring sites — initial decomposition (`/breakdown`) and phase-level fix-task creation (the verify dispatch that opens a fix task after a phase-level result). Writing two thin overlapping docs manufactures a false split.

**Problem.** Acceptance criteria are authored wrong at creation in two structurally distinct ways:

**Sub-pattern A — AC vs `owner` mismatch.**
- **A1 (task-022, 07-22):** `owner:"both"` tasks with majority-remote acceptance have no structural way to record PARTIAL verification — the Claude-verified half is indistinguishable in `task_verification` from a fully verified task. Proposed: a per-criterion ownership tag (`claude`/`human`) on `acceptanceCriteria` so verify-agent can report scoped coverage.
- **A2 (task-058, 08-06):** AC5 ("a decision is recorded on whether to delete the four empty subdirectories") requires a USER decision but sits on an `owner:"claude"` task — no implement-agent pass can satisfy it; verification can only ever mark it open. Failing it routes back to an agent that structurally cannot close it. Cost: one verification cycle spent on a criterion that was never agent-reachable. Decomposition should either set `owner:"both"` when an AC requires a user decision, or word the AC as the agent-satisfiable action ("a recommendation is recorded and escalated").

**Sub-pattern B — phase-level fix-task authoring quality (criterion wrong at creation).**
- **B1 (task-058, 08-06):** title + AC1 both say "14 references"; the description enumerates 17; the actual repo count was 18 file-specific + 3 directory refs. Wrong at creation (phase-level verification, 2026-08-05); AC1 unfalsifiable as literally worded. *"A count in a title or AC should be derived from the enumeration in the same task body, or omitted."*
- **B2 (task-063, 08-10):** an AC authored by phase-level verification cited the DEC-002/task-032 notebook↔src parity contract for an asset with neither a `src/` mirror nor a function shape — unsatisfiable as written; cost the implementer a documented reinterpretation (FR-066). *"Phase-level fix-task authoring should ground a contract citation against the actual asset shape before mandating parity."*
- **B3 (phase-level, 08-07) — circular re-verification trigger:** a phase-level result is invalidated when the spec fingerprint changes, but the natural response to a phase-level result is to record it in the spec — which changes the fingerprint and invalidates the result just recorded. One full loop turn confirmed: `3909f351` pass → tasks 057–060 edit spec → `a475793a` → re-verify. DEC-022 implies the answer (`verification-result.json` owns status, spec owns criteria) but no rule states that spec prose must not restate the result.
- **B4 (task-038_1, 07-29):** AC2 self-contradictory — asks silver to apply "the same transformations the global table gets" then enumerates transformations the global table does NOT get in silver (they live in silver-to-gold2); the clauses cannot both be satisfied and the enumerated branch breaks AC3. `/breakdown` authored it from a layer-agnostic list without checking layer ownership.
- **B5 (task-067, 08-11):** mutually unsatisfiable AC pair — AC2 forbids editing the spec (DEC-016) while AC5 demands "zero remaining live references," a state only a spec edit can produce. AC5 was structurally un-closable from authoring; two verification attempts spent finding derivative misses inside a criterion that could never have literally closed. Sweep tasks whose target spans spec body text need AC wording that terminates at the merge-queue park + an explicit note that the defect closes at the `/iterate` drain, not at task completion.
- **B6 (task-023, 07-22):** AC invalidation from inside the same task — crit 6 asserted rowcount equality between fact and source; the territory-rollup fix approved *within* task-023 made that equality wrong by construction. *"A criterion that is never measured stays plausible indefinitely."*
- **B7 (task-048, 07-31):** AC written from code rather than behaviour — AC2 demanded a mechanism the pre-existing implementation never had (the dataflow's look-back branch was unreachable dead code). *"A criterion should describe behaviour to preserve, not code to mirror."*

**Dedup — not a duplicate.** FB-100 (shipped v4.23.0) fixed *routing* + *completion shape* for `owner: both`, not AC *authoring* quality. FB-107 is about phase *gating* (build-blocking vs validation), not fix-task *authoring*. DEC-022 is about AC *authority* (which surface owns acceptance *status*), not AC *authoring* quality — B3's circularity is adjacent (DEC-022 implies "spec must not restate the result") but DEC-022 doesn't state that rule. Verified: `support/reference/phase-decision-gates.md` contains zero mentions of `fingerprint`, `re-verif`, or `enumerat`. **FB-115 (this harvest, cluster 5)** owns the task-057 lexical-vs-structural *closure-sweep* framing — task-057 appears in this corpus's source files but is FB-115's incident, not re-captured here; the defect classes are distinct (closure-sweep methodology vs criterion-authored-wrong).

**Likely eventual blast radius:** `commands/breakdown.md` (AC-vs-owner consistency check + ground-the-citation + behaviour-not-code + count-derivation rules); `support/reference/task-schema.md` (per-criterion ownership tag for `owner:"both"` partial verification); `rules/task-management.md` (AC-authoring grounding cross-reference); `support/reference/phase-decision-gates.md` (circular re-verification rule — spec prose must not restate the result); `commands/work.md` (phase-level verify dispatch prompt — fix-task authoring quality).

**Single-project / single-timeframe caveat.** 9 unique incidents, single project (OEMMatInsightBI), ~3-week stretch (07-22 → 08-11; densest 08-06 → 08-11). Above the 3-occurrence floor but single-project and single-timeframe — framed like FB-076 / FB-084 / FB-107 / FB-115, not as an unqualified `ready`. Re-assess for promotion (drop the caveat) on a second project signaling the same authoring-grounding gap.

**Harvest 2026-09-25 evidence (+3, oemmatinsightbi — `template-maintenance/harvest-2026-09-25-triage.md` cluster 5). A third authoring shape: tasks whose only legal path is a user-typed gated command.** task-076 was `owner: both`, but its whole deliverable routes through `/iterate`, which only the user can invoke, so the two halves were never separable and `owner` carried no routing information (08-21). task-081 was `owner: claude` for the same reason (08-21, 09-19): `/work` auto-detect sees a Claude-owned Pending task, but no dispatch can complete it, since subagents can neither run a `disable-model-invocation` command nor write under `.claude/`. Only a prior handoff note prevented a doomed implement-agent dispatch. This is the FB-100 shape one layer up. Candidate authoring check: *if the only way to land the task is a user-typed gated command, set `owner: human`* (or `both` with an explicit user half). **Sub-pattern B, again:** a phase-level verifier opened task-080 on an untested premise (a page with a Drillthrough binding was called a drillthrough target, but no visual projects the bound field), which yielded an AC no implementation could meet. The verifier-authored fix task also carried no options for its design fork, so the orchestrator had to invent A/B/C (09-19).

**Harvest 2026-10-03 evidence (+8, PortfolioWebsite: a second project, so the single-project caveat above is superseded; cluster 11).** **User-gated work has no honest status.** Decision-gated `owner: both` tasks sit Pending without `user_review_pending`, so Step 1d's clauses (`work.md:263-303`) treat them as Claude-actionable and the fast exit never fires (08-28-0430, 08-30-0445). One such task nearly routed a session into writing guarded prose (09-09-0005). Neither Blocked nor On Hold honestly describes decision-gating. A follow-up filed before the user chose its timing was dispatchable at once (09-19-1705). Same family as this item's gated-command shape. **Criteria wrong at creation:** an AC that named a diagnostic code but not the identifier was unsatisfiable while its target was met (09-11-1510); both remediation options were arithmetically impossible (08-30-0445); a flip-test AC couldn't tell fixed from broken (09-24-1238); an ambiguous fix locus, and design notes mixed with acceptance (09-24-2254, 09-19-0005). **Design note:** FB-128 reworks Step 1d's exit, so settle how decision-gated tasks count there as part of FB-128.

Tags: task-schema, acceptance-criteria, decomposition, breakdown, phase-level-fix-tasks, owner-field, gated-command-ownership, phase-decision-gates, spec-fingerprint, circular-reverification, merge-queue, single-project-signal, cross-references-FB-115, cross-references-FB-100


## FB-118: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-10-03 — shipped v5.8.0 (Needs-you card derives every user-gated row; judgment rows persist in sidecar `augment_rows[]`). See archive for full entry.

## FB-119: The orchestrator is the one unverified actor — inline implementation and orchestrator-authored state annotations bypass self-review and verify-agent

**Status:** shipped v5.6.0 (2026-09-27) — (a)–(c) as adapted; see ship-log. **Not archivable (2026-10-01):** the first 5.7.4 cycles show friction in the inline contract (see the 2026-10-01 evidence below); amend it. A fourth gap, dispatch briefs that carry unchecked claims, was added 2026-10-04 from the 2026-10-03 harvest. Escalate to `/research` only if inline bypass or unmeasured state claims recur.
**Captured:** 2026-09-25 (harvest cluster 8)
**Source:** 6 exports, two projects: oemmatinsightbi 08-12, 08-19, 08-21 ×2; styler 09-20, 09-21. Triage: `template-maintenance/harvest-2026-09-25-triage.md`. Insight: `interaction-logs/insights/2026-09-25_work_orchestrator-unverified-actor.md`.

**Problem.** implement-agent's self-review and verify-agent's separate context both guard *subagent* output. Nothing guards the orchestrator's. Two shapes:

1. **Inline implementation.** The orchestrator implements a task itself instead of dispatching implement-agent, which silently skips implement-agent's self-review and sweep discipline. task-070 then failed verification twice on the exact defect class self-review targets (08-12). A styler routing change was labelled a "bug fix" without a before/after behaviour sweep and regressed one context from 5 outfits to 0; verify attempt 2 caught it (09-21). One harness carried a "don't call the Agent tool unless asked" instruction while `/work` prescribes dispatch for every task, which forced an improvised judgment about which dispatches are load-bearing (08-19). A spec/audit-heavy inline session produced zero Track-1 markers, so it was invisible to the friction register (09-20).
2. **Orchestrator-authored state.** The orchestrator wrote "The BUILD did not change" into a `verification-result.json` supersession annotation without checking commits after the verification timestamp; about 12 hours of commits had landed, including two notebooks (08-21, repeated in the follow-up session). The same session made four more annotation errors: a hash matching no real state, a misread numstat, a UTC clock with a +02:00 offset, and an inherited false premise. All were in annotations *about* state, not the state itself. A phase-level verifier also quoted a task record's description of *external* state into a new fix task without re-measuring it (08-21). Verify-agent caught these only because the work happened to be scoped as a task.

**Fix sketch (cheap first).** (a) Say in `rules/agents.md` which dispatches are **invariants** (verify-agent: always a separate agent) and which are **efficiency defaults** (implement-agent: inline allowed at difficulty ≤ N, *provided* the orchestrator runs the same self-review/sweep checklist and a before/after sweep for behaviour-changing edits). (b) Require any annotation that argues a stale result is still valid to cite the git range it checked (`git log <verified_at>..HEAD -- <paths>`). (c) Task records that describe external/live state are re-measured, not quoted, when carried into a new task. Escalate to `/research` only if this recurs after (a)–(c).

**Absorbs** the "records asserting live state go stale" sub-observation from the 2026-09-25 harvest (deliberately *not* added to FB-115, which stays about sweep scope).

**Likely blast radius:** `rules/agents.md` (Separated Concerns / Context Separation); `commands/work.md` (inline-implementation path; supersession-annotation protocol); `support/reference/work-procedures.md`.

**2026-10-01 evidence (5.7.4: styler 09-28, 10-01-1237, 10-01-1440; PortfolioWebsite 10-01-1809).** The invariant held: every inline task still got a separate verify-agent, and it caught both inline defects. Styler T894 failed spec_alignment because its fixtures were hand-written from type docs in the wrong id shape; T899 failed consistency_check because the stale-reference search used the retired literal rather than the claim's subject. The efficiency-default contract (`rules/agents.md § Dispatch Invariants vs Efficiency Defaults`) has three gaps: (1) it doesn't point inline work at the "search for what the change invalidates" / by-subject sweep that implement-agent Step 2 and verify-agent T2c item 4 carry; (2) it doesn't say that a task whose deliverable is a `.claude/` path is inline at any difficulty, since subagents can't write there (styler T898 at difficulty 5; PortfolioWebsite task 172, 08-26); (3) it doesn't say which rule wins against FB-103's post-limit no-re-dispatch rule (PortfolioWebsite implemented a difficulty-3, five-file task inline after a zero-token implement-agent return). Smaller: producer-consumer fixtures should come from the producer's own tests or emit path (T894).

**Harvest 2026-10-03 evidence: a fourth gap (+7, two projects; cluster 12). Dispatch briefs carry authority nobody earned.** Agents built on brief premises that turned out wrong: a config claim inferred from a grep hit (PortfolioWebsite 09-11-1510), a defective derived sweep set (09-08-2329), a vacuous prescribed control (09-15-1510), an untested worktree build route (09-19-1234), invented rationale returned as orchestrator edits (09-24-1238), and a DAX mechanism stated as fact (oemmat 08-11-1922). v5.6.0's rule covers claims written into `.claude/` and task records, not claims in briefs or relayed to the user (09-15-1510, 09-24-1238). A cheap fix is already working downstream: briefs mark the orchestrator's claims as unverified and invite challenge ("give them no authority"; agents corrected the orchestrator four times in 09-11-1945), and mechanism claims are measured first or labelled as hypotheses.

Tags: work, orchestrator, inline-implementation, verification-result, state-annotations, self-review, agent-dispatch-invariants, two-project-signal

## FB-120: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-10-02 — shipped v5.7.5 (Python 3.10 floor + guards + floor test; verify timeout excludes infrastructure terminations; export clears the pending-marker buffer and the working copy). See archive for full entry.

## FB-121: Nested subagent dispatch is now platform-supported — reconcile `rules/agents.md` + DEC-004's "no nested Task" fact, and decide whether any flow should use it

**Status:** shipped v5.7.1 (2026-09-27) — `rules/agents.md` both mentions now say platform-supported but template-avoided; DEC-004 annotated; `/health-check` `[V]` flow greps for restatements after an accepted change. Optional design question (use nesting deliberately) stays research-gated.
**Captured:** 2026-09-25 (`/health-check` Part 2d `[V]` pass on `claude-code-authoring.md`)
**Source:** docs `code.claude.com/docs/en/sub-agents.md` (fetched raw 2026-09-25): *"By default, a subagent can spawn subagents of its own, up to three layers below the main conversation. At the depth limit, Claude Code withholds the `Agent` tool from every subagent except a fork…"*; limit set by `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`.

**Problem.** The template states "subagents cannot spawn nested `Task` calls" as a *platform fact* in three places. The 2026-09-25 `[V]` pass corrected `claude-code-authoring.md` (now "platform-supported, template-avoided"), but two places remain:
- `.claude/rules/agents.md:20` (§ State Ownership "Capability grounding" list) and `:117` (§ Tool Preferences). This rule file **auto-loads every session**, so the stale fact is in context everywhere.
- `decisions/decision-004-subagent-capability-contract.md:145` (+ its research archive), which recorded it as "NO — not exposed even when listed in frontmatter `tools:` (#19077)". That was true in 2026-04; it's a historical record, so annotate it rather than rewrite it.

**Proposed (cheap).** Change the two `rules/agents.md` mentions from a platform prohibition to the template convention: *"the orchestrator performs all dispatch; nested dispatch is platform-supported on current harnesses (depth 3 by default) but the template doesn't rely on it — portability + state ownership."* Add a dated supersession note to DEC-004's line 145. Check `.claude/agents/*.md` and `commands/work.md` for any "cannot nest" wording (none found by the 2026-09-25 grep beyond the lines above).

**Optional design question (research-gated, don't bundle).** Should any flow deliberately use nesting? Candidates: `/audit-*` lens fan-out from a dispatched auditor; research-agent sub-investigations. Constraints that still hold: subagents can't write `.claude/` (DEC-004, harness-observed), so nested results still flow back through the orchestrator; downstream projects on older harnesses would break. Re-open only if an orchestrator-context-pressure signal appears that nesting would relieve.

**Related `[V]`-pass observation.** DEC-020's 2026-05-27 research already recorded the "first 5,000 tokens each" re-attachment detail as live (`decision-020…md:122`), but `claude-code-authoring.md` kept the misleading "~25K per skill" framing until this pass. A research finding marked "confirmed-consistent" can still carry a refinement that nobody applies back to the doc. Worth one line in the `[V]` flow: when a research archive notes a refinement, apply it to the doc body.

Tags: agents, subagents, nested-dispatch, DEC-004, capability-doc, rules-agents-md, reconciliation

## FB-122: Deterministic `/work` routing script (`work-state.py`) — Tier C of the work.md condensation

**Status:** new (research-gated)
**Captured:** 2026-09-27 (Opus 5.5 review #6, work.md condensation, v5.7.3)
**Source:** maintainer session 2026-09-27; v5.7.3 ship-log entry.

**Idea.** Much of `/work`'s startup and routing is deterministic over task JSON + a few state files: Step 3's routing algorithm, Step 1d's non-actionable fast path, Step 1a's dashboard freshness hash, Step 0e's uncommitted-work check, and the Step 0d/0f trigger conditions. A `work-state.py` (stdlib, read-only, per `.claude/scripts/README.md` contract) could return `{next_action, task_id, reason, surfaced_items[]}` as JSON, the way `dashboard-render.py` replaced hand-written dashboards (DEC-024). The orchestrator would run it and act on the result, keeping only judgment steps in prose.

**Why.** Shrinks the remaining 49K hot path further, and makes routing reproducible (no LLM re-derivation of a 10-branch algorithm each loop iteration). Fits the FB-011 scripts family.

**Open questions.** Which steps are purely mechanical vs judgment-bearing (Step 2b decision checkbox detection is mechanical; ambiguity surfacing is not). Dual-location risk while prose and script coexist (`.claude/scripts/README.md § "Dual-location risk"`). Test coverage for the routing matrix.

**Gate.** `/research` before building; no incident evidence of mis-routing yet, so the case is maintainability and context size, not a defect.

Tags: work, scripts, routing, FB-011-family, context-size

## FB-123: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-10-02 — shipped v5.7.5 (dispatch surface: `Agent` tool, `model: "opus"`, prompt-stated turn budgets, notification-driven parallel collection). See archive for full entry.

## FB-124: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-10-02 — shipped v5.7.5 (`/research`: the research-agent returns its artifacts and `research.md` Step 4 persists them, per DEC-004). See archive for full entry.

## FB-125: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-10-02 — shipped v5.7.5 (`/health-check` checks match the generated HTML dashboard, DEC-024). See archive for full entry.

## FB-126: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-10-05 — shipped v5.10.0 (Part 5 removes what the template retired; `sync-check.py`; commit offer). See archive for full entry.

## FB-127: v5.7.5 residuals — small follow-ups found while shipping (bundled per the FB-006 precedent)

**Status:** ready — independent small items; none blocks anything. (l) and (m) added 2026-10-04 from the 2026-10-03 harvest; (n)–(q) added 2026-10-05 from the v5.10.0 build.
**Captured:** 2026-10-02 (v5.7.5 implementation and review)

(a) **Pre-DEC-024 Markdown-dashboard text still in shipped docs:** `dashboard-regeneration.md § Section Display Rules / Per-Section Format` (Tasks and phase tables, `[Fix it]`, ticking); audit wording that implies ticking the dashboard (`audit-coherence.md:27,145`, the `audit-family-core.md` triage intro, `audit-ui.md`'s `promote {ts}` "ticked" mode). The `[Fix it]` path itself works through the CLI (`fix`, `triage` → `F`), so this is wording, not mechanism, and the audit telemetry gate can still accrue. Also `### Acceptance Criteria` in `rules/spec-workflow.md` and `audit-coherence.md:386,411`; `breakdown.md:52`; `health-check.md`'s escalation to FB-011 Family C (shipped v4.22.0, superseded by DEC-024); `dashboard-regeneration.md:52,417` "(Replacing Template Example)"; scenario 06 Trace D still models the pre-DEC-024 in-file checklist (`:102-109`, `:114-116`, `:123-124`).
(b) **Export residue outside the prose path:** `.claude/hooks/pre-compact-handoff.sh:232-239` copies its export to the inbox itself (bypassing `persist-session-export.py`) and never deletes its working copy; `persist-session-export.py` exits 1 with a traceback when the copy fails (its contract says 2); a project with a stale `.pending-markers.jsonl` gets one more duplicate export after upgrading.
(c) **The sequential implement-agent dispatch states no turn budget** (`work.md` Step 3), so implement-agent's "75% of your turn budget" wind-down has nothing to measure outside parallel mode.
(d) **Part 3 check 6** can't tell a decision's origin task from its dependents (`related.tasks`); v5.7.5 made its auto-fix report-only. Fix: an origin field, or skip the task a decision was made in.
(e) `support/reference/decisions.md` doesn't document `partially_superseded`, which the renderer, META and `/audit-coherence` use (`/health-check` accepts it since v5.7.5).
(f) Reported, not checked: `tests/scenarios/19-agent-crash-recovery.md:25` ("sequential mode runs inline") is out of date. *(Fixed in v5.7.5's review round.)*
(g) **Renderer crash paths left after v5.8.0:** a non-object `version.json` or `verification-result.json`, or a non-object `section_toggles` / `phase_gates` / `audit_digest` inside the sidecar, still raises (v5.8.0 guarded only a non-object sidecar). *v5.9.0 fixed one more: a bare-list or malformed `drift-deferrals.json` no longer crashes META or the Needs-you card.*
(h) **The `rg` fallback may prompt outside auto mode:** `settings.json` allows `Bash(grep:*)` but not `rg` or `find`. A blanket allow needs care: `rg --pre` and `find -exec`/`-delete` can run or delete things.
(i) **`audit-coherence.md`'s path-drift "exists via Glob" check** is an absence claim and needs a positive control under the v5.8.0 rule. Other `Grep`/`Glob` mentions (`work.md:98,196`, `health-check.md:343,947`, `automation.md:32`) rely on the rule's general fallback.
(j) **More pre-DEC-024 drift** found by the v5.8.0 docs pass: scenarios 06C (file links on task rows the script never renders), 06D, 07/07B, 08D, 16C steps 1–3; `drift-reconciliation.md:28` (notes-backup step; *removed in v5.9.0*); `shared-definitions.md:168` (FEEDBACK markers).
(k) **Architecture map:** v5.8.0 adds `negative-findings.md` (the "~29 reference docs" count, the lazy-docs list, and a `rules/agents.md` → `negative-findings.md` edge). Reconcile with FB-112(a).
(l) **`verification_history[].cost` arrives after the report** (harvest 2026-10-03 cluster 14). `work-procedures.md:50` copies `cost` "from the usage the harness reports", but on 5.7.4 that usage arrives in the task-completion notification, after the report (styler 10-01-1237, PortfolioWebsite 10-02-0820). Read literally, the step omits `cost`, and both orchestrators needed a second JSON write. The DEC-025 recheck gate counts difficulty 1–2 dispatches that carry `cost`, so say "backfill `cost` when the completion notification arrives".
(m) **The Custom Views fill is lost on every regen, and nothing catches an unfilled placeholder** (harvest 2026-10-03; listed under FB-118 in the draft, but v5.8.0 shipped FB-118 without it). Each regen emits a fresh `<!-- CLAUDE: fill … -->` slot (`dashboard-render.py:1246-1250`, `dashboard-regeneration.md:202`), so LLM-rendered views must be redone by hand after every regen, and the HTML is gitignored, so a lost fill can't be recovered (PortfolioWebsite 09-21-1452). Sessions left the slot unfilled with `custom_views` on; the placeholder check at `dashboard-regeneration.md:300` is prose that nothing runs (09-19-1705). Options: make the fill a required step of every regen while the toggle is on, with a scripted check for a leftover fill comment; or persist the rendered blocks in the sidecar, as `augment_rows[]` does. Custom Views is off by default.
(n) **The Notes card doesn't render headings.** `### X` in sidecar `user_notes` comes out as a literal `<p>### X</p>`, but the `_html_notes` docstring in `dashboard-render.py` and `dashboard-regeneration.md` (the `user_notes` row and § 5) say headers render. v5.10.0's retirement Step 5 uses a bold label instead. Fix the renderer or the docs.
(o) **`work-user-flows.md` overwrites `user_feedback`** when guided testing fails ("record failure in task's `user_feedback` field"), the same history loss FB-134(b) fixed for `notes`.
(p) **A shallow template history hides retirements.** `sync-check.py` reads deletions and old manifests from the template's history; with a shallow `--template-repo` clone it silently finds fewer. Part 5's `git fetch template` is full, so only manual runs are exposed. Candidate: warn when the repo is shallow (`git rev-parse --is-shallow-repository`).
(q) **Part 5 needs git.** LTP and escalation_map_training have no repository, so `/health-check` can't sync them; they were synced by hand on 2026-09-27.

Tags: residuals, dashboard, DEC-024, audit-wording, session-export, hooks, dispatch, health-check, decisions

## FB-128: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-10-04 — shipped v5.9.0 (deterministic drift check on every `/work`; reconciliation before Step 1d; `[V]` Re-verify and `[K]` Keep). See archive for full entry.

## FB-129: Agent-recorded decisions land `approved` before verification and never reach the user for ratification

**Status:** ready — verified. Candidate for the release after FB-128.
**Captured:** 2026-10-04 (harvest 2026-10-03 cluster 2; cluster 18 folded in)
**Source:** 9 exports, 3 projects: PortfolioWebsite 09-08-2329, 09-11-0757, 09-15-1510, 09-19-0005, 09-24-1758; oemmat 05-24-1930, 07-22-2017, 07-23-0130; styler 05-27-0045. Insight: `interaction-logs/insights/2026-10-03_work_agent-decisions-approved-unratified.md`. FB-052 (archived) created the field; its approval semantics were never revisited.

**Problem.** `implement-agent.md:249` tells the agent to "flag for human". But `work-procedures.md:41` (step 3) writes each `decisions_to_record[]` entry as `status: approved`, `decided_by: implement-agent`, before verify-agent runs (step 5). The renderer then counts it as resolved (`dashboard-render.py:241`) and lists only `draft`/`proposed` records (`UNRESOLVED_DECISION`, `:73`, used at `:1100`). This contradicts `rules/decisions.md` ("never resolve silently") and DEC-016.

Observed: a deferral recorded as an approved decision nobody made (09-08); a self-ticked checkbox (09-11, oemmat 07-22); an approved record for an approach that verification hadn't accepted, which the orchestrator held back by hand (09-19); three coupled choices became three records behind three DEC-016 prompts (09-15, oemmat 07-23); trivial choices minted as records despite `support/reference/decisions.md` § "Skip Records For" (09-24, oemmat 05-24, styler 05-27).

**Fix sketch.** Write agent decisions as `proposed` with a "ratify?" Needs-you row (or a distinct `recorded` status for documentary records of choices already shipped); persist them after the verify pass; one record per coupled decision; trivial choices go to task notes. Reword step 3's "Selected/Rationale/Options sections" to name the template's `## Decision` (`**Selected:**`) and `## Options Comparison`: PortfolioWebsite's 8 records used `## Selected` and fail `/health-check` Part 3 check 4 (`health-check.md:397-398`; 10-01-1243). **Folded in from cluster 18:** step 3 should link the numbering-namespace rule (`support/reference/decisions.md:161`). A project DEC-NNN collided with a template-cited ID (PortfolioWebsite 09-11-0757, oemmat 08-13-0916) even though the rule shipped in v5.2.0.

Tags: work, decisions, decisions_to_record, implement-agent, ratification, needs-you, DEC-016, extends-FB-052, verified-defect, three-project-signal

## FB-130: No defined path for a small fix after a verify pass

**Status:** ready — two projects arrived at the same workaround independently
**Captured:** 2026-10-04 (harvest 2026-10-03 cluster 3)
**Source:** 5 exports, 2 projects: PortfolioWebsite 09-27-1040, 10-02-0820; styler 09-28-1923, 10-01-1237, 10-01-1440. Four are on 5.7.4, after FB-119 made verify-agent an invariant (v5.6.0). No recurrence found in `processed/`. Insight: `interaction-logs/insights/2026-10-03_verify-agent_post-verify-delta-recheck.md`.

**Problem.** After a pass, a one-word fix, a comment, or a verifier-suggested minor change leaves two options: a full fresh verify dispatch (125–230K tokens per verify dispatch in this harvest: PortfolioWebsite 09-11-0757, 09-19-0005, 10-01-1809) or an inline edit nobody re-checks. Both projects independently resumed the *same* verifier with SendMessage for a delta re-check and recorded it as attempt N+1. Independence holds because that verifier never implemented anything (styler 10-01-1440).

**Fix sketch.** Name a "post-verify delta" path in `work-procedures.md` (After verify-agent returns). Allow it only for the verifier's own findings or a user-approved micro-edit: resume the same verifier with the diff, and record a new `verification_history[]` attempt with `cost`. Anything larger gets a fresh dispatch. Kept separate from FB-119, which could have taken it as a gap, because this is a verification-protocol question rather than an orchestrator-claims one.

Tags: work, verify-agent, post-verify-delta, sendmessage, verification-history, cost, DEC-025, two-project-signal

## FB-131: The handoff's ~2.5KB total bound is unenforced, and its overflow file collides on same-day pauses

**Status:** ready — verified; patch-sized
**Captured:** 2026-10-04 (harvest 2026-10-03 cluster 4)
**Source:** 5 exports, 3 projects: PortfolioWebsite 08-19-2300, 09-11-1945, 09-24-2254; oemmat 08-21-0642; styler 09-20-1916 (the last two were below the bar in the 2026-09-25 single-incident list). Insight: `interaction-logs/insights/2026-10-03_work_handoff-size-unenforced.md`.

**Problem.** `context-transitions.md:86` and `:180-190` target ~2.5KB in total, but the overflow procedure fires only when a single field exceeds its bound. The field caps sum past 2.5KB (ten 25-word bullets alone are about 1.5KB), and no pause step measures the file. Observed: 3.0KB with every field in bounds (08-19), 4.4KB and 4.2KB on consecutive pauses (09-11), 12% over (styler 09-20). `:190` names the overflow file `handoff-overflow-{YYYY-MM-DD}.md`, so a second pause on the same day collides with the first (09-24-2254). FB-079 fixed this shape for session exports in v4.6.4 with minute timestamps, but not here.

**Fix sketch.** After writing the handoff, measure it and run the overflow procedure on the total, not only per field; give the overflow file a minute-granularity name (`-HHMM`, as FB-079 did). Optional: point long-lived detail at auto-memory (oemmat 08-21).

Tags: work-pause, handoff, context-transitions, overflow, filename-collision, extends-FB-079, verified-defect, three-project-signal

## FB-132: Parallel eligibility ignores shared single-instance resources (Playwright MCP, build output directory)

**Status:** ready — a prose fix. FB-011 Family D's trigger (an LLM-*missed* conflict) is still unmet: every instance here was caught before dispatch.
**Captured:** 2026-10-04 (harvest 2026-10-03 cluster 5)
**Source:** 5 exports, 3 projects: PortfolioWebsite 09-11-0757, 09-24-1238, 10-01-1809 (5.7.4); oemmat 08-13-0916; styler 09-24-1745. Insight: `interaction-logs/insights/2026-10-03_work_parallel-shared-runtime-resources.md`. **Extends FB-056** (archived, shipped 2026-05-13): it documented the single-session MCP constraint and parked an `mcp_resource_overlap` batch check as "lower priority". This is the recurrence that check was waiting for.

**Problem.** `work.md:398` builds batches by "pairwise-comparing `files_affected`". `mcp-patterns.md:17` names the missing check (`mcp_resource_overlap`) but calls it "lower priority". When every UI task carries a rendered-verification criterion (PortfolioWebsite), nearly every UI batch needs the one Playwright session; parallel builds also share `dist/` or `.next`.

**Fix sketch.** Add one exclusion to the Step 2c summary and `parallel-execution.md`: two tasks that both need the browser MCP, or both rebuild the same output directory, are not parallel-eligible (or their verification runs sequentially). A task-schema flag such as `needs_browser` is optional. Drop "lower priority" from `mcp-patterns.md:17`.

Tags: work, parallel-execution, mcp, playwright, build-output, shared-resources, extends-FB-056, FB-011-family-D-adjacent, three-project-signal

## FB-133: Agents leave residue the orchestrator has to find — screenshots in the project root, live servers, probe routes

**Status:** ready (screenshots: two projects; leftover processes and probe routes: PortfolioWebsite only)
**Captured:** 2026-10-04 (harvest 2026-10-03 cluster 6)
**Source:** 6 exports, 2 projects: PortfolioWebsite 08-19-2300, 09-11-0757, 09-24-1238, 09-24-1839, 10-01-1809; oemmat 07-26-2045. Insight: `interaction-logs/insights/2026-10-03_agents_residue-after-return.md`.

**Problem.** `verify-agent.md:257` prescribes `browser_take_screenshot` with no output path, and the MCP resolves a bare filename against the project root. That breaks `.claude/CLAUDE.md`'s "never create working documents in the project root" (oemmat 07-26; PortfolioWebsite 08-19, 09-11). An implement-agent reported its preview server stopped while two were still listening (09-24-1839). Cutoffs left a probe route in `src/pages/` and a live server (09-11), and flipped drafts plus orphaned servers (09-24-1238). An orphaned MCP Chrome held the profile lock (09-24-1238). Verifiers share the orchestrator's scratchpad, where an `rm -rf` on a generic name could delete evidence (10-01-1809). No after-return or post-cutoff cleanup step exists in `work-procedures.md`, `work-recovery.md`, `parallel-execution.md` or `work.md` (re-checked at v5.8.0 with `grep -c -i -E 'residue|stray file|orphan|still listening|lsof|leftover server|kill the server|stop the server'`: zero hits except two in `work-recovery.md` about orphaned markers; positive control `zero-token` hits the other three files).

**Fix sketch.** Give screenshot paths explicitly (a per-agent scratchpad subfolder) in dispatch briefs and at `verify-agent.md:257`. After any agent returns, and after an infrastructure termination, check for servers the agent started, stray files in the project root and untracked probe files; clean them up or report them.

Tags: agents, verify-agent, implement-agent, playwright, screenshots, dev-servers, residue, recovery, two-project-signal

## FB-134: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-10-05 — shipped v5.10.0 (restore path, notes history, Step 0e by files, null pass rate, `resolves_friction`). See archive for full entry.

## FB-135: Most tasks in two projects carry no section provenance, so drift can't be checked for them

**Status:** new — measured 2026-10-04; split out of FB-128 by the maintainer (FB-128 design decision 6). For a later release.
**Captured:** 2026-10-04 (FB-128 design survey)
**Source:** read-only survey of 10 downstream repos, 2026-10-04 (`template-maintenance/plan-fb128-drift-detection.md` § Survey). PortfolioWebsite: 74 of 75 tasks have no `section_fingerprint`. OEMMatInsightBI: 19 of 20 current-version tasks have none, and all its `spec_section` values are bare headings without `## `. styler: 20 current-version tasks have none, and 47 have a `spec_section` that is not a current heading (mostly free-form values such as `§ 52.1 (…) + § 52.6 (…)`; one differs only by a trailing space).

**Problem.** Decomposition stamps full provenance (`decomposition.md` step 8) and `/breakdown` copies it, but tasks created any other way get none: phase-level fix tasks (`work-procedures.md`, phase-level step 2 writes the verifier's `task_json` payload as-is), tasks filed mid-session from user feedback or reviews (no defined command path; harvest 2026-10-03 single-incident list), and out-of-spec tasks. FB-128's drift check counts these as `no_provenance` and never flags them, so a spec edit under them stays invisible. In a project that creates tasks mostly ad hoc (PortfolioWebsite), drift detection covers almost nothing.

**Fix sketch.** (1) Every task-creation path stamps `spec_version`, `spec_section` (a real `## ` heading) and `section_fingerprint` when the task maps to a spec section (`fingerprint.py --sections`), and a task that maps to none says so explicitly, so the check can tell "unmapped" from "missing". (2) A one-time baseline offered by `/health-check` Part 1: for tasks whose `spec_section` resolves to a current heading but that carry no fingerprint, stamp the current hash once the user confirms that the current text is what they were built against (the same assertion as FB-128's `[K]`). (3) Optionally normalise free-form `spec_section` values. FB-128's drift JSON (`no_provenance`, `unmatched`) is the measurement before and after.

Tags: drift-detection, provenance, task-creation, spec_section, section_fingerprint, health-check, follow-up-to-FB-128

## FB-136: Part 5 calls unedited template copies "Modified upstream", and four smaller sync gaps

**Status:** new — measured 2026-10-05/06 during the v5.10.0 downstream sync (9 projects). Bundled per FB-006 precedent.
**Captured:** 2026-10-06 (template-side sync session)
**Source:** read-only classification of all 85 compare-set files in 9 downstream projects against tag `v5.10.0`, using `sync-check.py --template-repo` plus a session script that compared each local file's `git hash-object` id with the path's template blob history.

**Problem.**
- **(a) Missing sidecar entry is read as a local edit.** `health-check.md` Part 5 Step 2 classifies a differing file with no `.sync-state.json` entry as "Modified upstream" (show diff, user adjudicates). Step 4 records `synced_hash` only for files it writes, so a file that already matched the template at sync time never gets an entry. After the 2026-09-27 sync that left 26 of 85 files without one in conversation_opener, 25 in LTP, 20 in escalation_map_training, 9 in PortfolioWebsite, 5 in flirty-gym and 1 in styler; styler also had 4 entries with a stale hash. Every one of those files was byte-identical to an earlier template version of its path. Only 3 files across the 9 projects had real local edits (LTP and OEMMatInsightBI `dashboard-render.py`, OEMMatInsightBI `merge-queue.md`). Run as written, Part 5 would have asked the user to adjudicate about 90 diffs that contain no local change.
- **(b) `sync-check.py` returns patterns, not per-file status.** Step 2 still describes the per-file loop in prose (`git diff` per file, hash against the sidecar). The script already computes template blob ids per path for `uncommitted_sync` and `retired_files`, so it could emit the classification too.
- **(c) Local `customize` and `ignore` lists never update.** Step 4 rewrites only `sync`, and the manifest is itself in `ignore`. Five projects (difficult-conversation-simplifier, flirty-gym, OEMMatInsightBI, PortfolioWebsite, styler) still list `.claude/dashboard.md` instead of `.claude/dashboard.html`. Harmless for comparison (the upstream lists win) but the local file misdescribes the project.
- **(d) The sidecar is not gitignored everywhere.** conversation_opener has `.claude/.sync-state.json` untracked and not ignored; flirty-gym tracks it. Part 5 says it is gitignored and never checks.
- **(e) Project data stored at a template-owned path is found only by reading the diff.** OEMMatInsightBI kept its own merge queue (pending items, applied log) in `support/reference/merge-queue.md`, created 2026-08-10 because its synced `.claude/CLAUDE.md` named a file an incomplete sync had not delivered. The file is gitignored there, so overwriting it would have destroyed the only copy. Handled by hand this time (moved to `project-merge-queue.md`). This is the FB-059/FB-060 structural gap; noted here as a second observed instance (PortfolioWebsite `known-issues.md` was the first).

**Fix sketch.** (a)+(b): have `sync-check.py` emit a `files[]` list with one status per compare-set file: `up_to_date`, `new`, `template_copy` (local id is in the path's template blob history; carry the version) or `modified` (matches no template version). Part 5 treats `template_copy` as apply-by-default whatever the sidecar says, and Step 4 records `synced_hash` for every compare-set file that equals upstream after the run. With blob history as the test, the sidecar is only needed when the template repo's history is unavailable (shallow clone, FB-127 (p)). (c): Step 4 offers to set local `customize`/`ignore` to the upstream lists plus project-added entries, as it does for `sync`. (d): Part 5 checks `git check-ignore -q .claude/.sync-state.json` and queues a `.gitignore` row. (e): leave with FB-060; when a `modified` file shares little with any template version, say so in the row ("local content is not a variant of the template file").

Tags: health-check, part-5, sync-check, sync-state-sidecar, classification, manifest, gitignore, extends-FB-126, relates-FB-060
