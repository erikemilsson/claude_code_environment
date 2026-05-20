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

**Status:** deferred — re-assess on/after 2026-06-02
**Captured:** 2026-05-19
**Source:** video https://www.youtube.com/watch?v=6BB6exR8Zd8 reviewed 2026-05-19; repo `mattpocock/skills` (clone at `/Users/erikemilsson/Downloads/skills-main` as of 2026-05-19; mirror github.com/mattpocock/skills).

**Reason for deferral:** Wave 1 (FB-068 + FB-069 + FB-070 + FB-071) ships first. Wave 2 candidates depend on Wave 1 signal — some compound only with their Wave 1 sibling in place.

**Wave 2 candidates to re-evaluate:**

- **`/tdd` skill** — vertical-slice red-green-refactor + anti-horizontal-slicing discipline. Pocock files at `skills/engineering/tdd/SKILL.md` + `tests.md` + `mocking.md` + `interface-design.md` + `deep-modules.md` + `refactoring.md`. Open question: does CCE's verify-agent already cover the "correctness" angle sufficiently?
- **`/prototype` skill** — throwaway design exploration. Two branches: terminal app for state/logic, multi-variation UI on one route. Trigger to ship: how often CCE work hits "I don't know what shape this should be."
- **`/improve-codebase-architecture` skill** — complement to `/audit-coherence`. Architectural vocabulary (Module/Interface/Depth/Seam/Adapter/Leverage/Locality) + deletion test heuristic. Most valuable AFTER CONTEXT.md (FB-068) and AFTER `/diagnose` (FB-069) — `/diagnose`'s Phase 6 post-mortem explicitly hands off here.
- **`/caveman` ultra-compressed mode** — ~75% token cut. Niche; ship only if cost pressure becomes a recurring concern.
- **Hard-vs-soft dependency cleanup pass** — apply Pocock's ADR-0001 pattern across CCE command files. Distinguish load-bearing cross-references from advisory. Cosmetic.
- **Bucketed skill organization** (`engineering/` / `productivity/` / `misc/` / etc.) — only worth considering if skill count grows much further.

**Trigger to escalate from deferred → ready:**
1. Any Wave 1 ship produces signal that a specific Wave 2 sibling compounds. Concrete example: `/diagnose` Phase 6 post-mortems repeatedly identify architectural friction → `/improve-codebase-architecture` becomes load-bearing.
2. The 2-week recheck on 2026-06-02 (default if no earlier signal).
3. Separate user request to re-evaluate.

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

## FB-072: Command routing as a UX pattern (interpretive vs explicit-arg dispatch + boundary survey)

**Status:** ready (research-first; trial-gated DEC candidate)
**Captured:** 2026-05-20
**Source:** session-level reflection after shipping FB-068 (`/grill` as standalone command rather than `/iterate grill` sub-mode). User observed 2026-05-20: *"from a UX perspective it is one more command to remember. I think we should look into making `/iterate` a router that routes to other commands depending on what is being asked. ... I guess the larger question is how effective routing is at all, and perhaps that is something to do research on."*

**Observation:** CCE currently dispatches sub-modes via explicit string args (`/iterate distill`, `/work complete`, `/work pause`, `/feedback review`). Each multi-mode command grows its own file (e.g., `iterate.md` ~700 lines covering distill/propose/hygiene/no-args; `work.md` ~1700 lines covering many sub-modes). Adding new spec-adjacent commands (FB-068's `/grill`, FB-069's `/diagnose`, FB-070's `/zoom-out`, likely Wave 2 entries) increases the surface area users have to remember.

**The router pattern (proposed by user 2026-05-20):**

`/iterate` becomes an interpretive umbrella for "everything that has to do with nailing down the single source of truth spec." Sub-purposes dispatch based on Claude's interpretation of intent:

- `/iterate "I want to stress-test this plan"` → router invokes `/grill` internally
- `/iterate "let's distill a buildable spec from this vision"` → router invokes the distill sub-flow
- `/iterate "the spec is fuzzy on cancellation semantics"` → router invokes the propose sub-flow
- `/iterate "check the spec against the registry"` → router invokes the hygiene sub-flow

Sub-flows can live in separate files (per-purpose, focused) or stay in `iterate.md`. The key difference from current explicit-arg dispatch: **the user doesn't need to know the sub-mode name**; Claude classifies from natural language.

**Two interesting twists:**

1. **Interpretive vs explicit-arg dispatch.** Current pattern is structural: user types `/iterate distill`, matcher fires. Proposed pattern is interpretive: user types `/iterate <natural language>`, Claude classifies intent before firing. Failure mode: wrong sub-mode runs silently. Mitigation candidate: router announces its interpretation (*"I read this as a distill request — proceeding with `/iterate distill` flow. Say 'no' to redirect."*) before any substantive action.

2. **Boundary discovery comes first.** Worth surveying which CCE commands have clean "umbrella" semantics before committing to the architecture. Concrete candidates:
   - **`/iterate` as spec-source-of-truth umbrella** — covers distill / propose / hygiene / grill / possibly research-dispatch for spec-adjacent decisions
   - **`/work`** — currently covers many concerns (decomposition, agent routing, parallel batching, completion, pause); some might split out under interpretive routing
   - **`/research` and `/iterate` overlap** — both touch decisions and spec adjacency. Unified umbrella, or correctly distinct?
   - **`/audit-coherence` and `/audit-ui`** — already dispatched from `/health-check` Part 8 menu (different pattern: menu-based). Similar umbrella-vs-discrete tension.
   - **Help-me-think family** — `/zoom-out`, `/grill`, `/diagnose`. Pattern: *user-asks-for-help-in-a-specific-mode*. Loose grouping ("I need broader context" / "I need to be interrogated about this plan" / "I need to debug rigorously"). Less obviously umbrella-shaped than `/iterate` (the family is small and the modes are quite distinct), but worth surveying for whether a single `/help` or `/think` entry point + interpretive dispatch produces a better UX than three discrete commands. Surfaced 2026-05-20 during FB-069 ship (post-FB-068/FB-070 reflection — three help-me-think commands now exist, none has a natural umbrella home).

**Research questions:**

- **Accuracy of intent classification.** Can Claude correctly classify the sub-mode from user input across candidate umbrellas? Failure rate? Recovery cost when wrong?
- **Discoverability.** Do users learn the umbrella surface (one command, many sub-purposes) faster than the discrete surface (many commands)? Or does the umbrella obscure capability?
- **Latency / cost.** Does interpretive routing add a noticeable LLM pass? Sub-modes have their own context loads (iterate.md is large) — is the router pass cheap or expensive?
- **Boundary clarity.** When should a piece of work be a sub-mode of an umbrella vs a standalone command? Are there cases where an umbrella forces unnatural couplings?

**Deliverables (if pursued):**

1. **Boundary survey** (`.claude/support/workspace/router-survey.md` or similar) — for each candidate umbrella, list sub-purposes that would route through it; flag any that don't fit cleanly. ~1-2 sessions.
2. **Prototype** — pick one umbrella (likely `/iterate`, the immediate driver) and implement interpretive routing as proof-of-concept. Trial in a real downstream session.
3. **Effectiveness data** — track router accuracy, recovery cost, and user feedback across N sessions. Threshold candidate: ≥ ~85% classification accuracy with ≤ 1 redirect per recovery to justify the pattern.
4. **DEC candidate** — if survey + prototype + data are favorable, `/research` opens a DEC. If unfavorable, FB-072 closes; explicit-arg pattern stays.

**Dependencies / interactions:**

- **FB-071 (Command Invocation Gates):** if `/iterate` becomes a router, the gating story stays — `disable-model-invocation: true` blocks ambient autonomous fire of the umbrella. Sub-modes don't need individual gates because the router gates them collectively. Potentially *simplifies* the FB-071 sub-mode coupling trade-off.
- **DEC-016 (spec/decision/vision Edit/Write ask):** unchanged. The permission-layer ask fires at the write boundary regardless of how the write was reached.
- **FB-068 (`/grill` as standalone):** if FB-072 ships favorably, `/grill` could migrate to `/iterate grill` as a sub-mode. The standalone command file stays as the dispatch target; only the entry point shifts. No re-work of `/grill` itself.
- **FB-070 (`/zoom-out`):** standalone micro-command; doesn't obviously belong under an umbrella (no "zoom-out family" of related commands). If router shipping reveals a help-the-user umbrella, revisit. Most likely outcome: `/zoom-out` stays standalone.

**Trial-gate:** the research-first nature is important. The user explicitly said *"perhaps that is something to do research on."* Do NOT implement before:
- Boundary survey is complete (which commands have clean umbrella semantics?)
- At least one prototype is trialed in a real session
- Effectiveness data accumulates

**Likely route:** research-light (boundary survey) → prototype → `/research` opens DEC if signal is positive. No template change in the first session; the survey is a workspace doc, not a template artifact.

**Impact scope if pursued:** large — touches `iterate.md` (router refactor), possibly `work.md` and `research.md`, `/grill` (entry-point migration), `/health-check` Part 8 menu (if `/audit-*` commands also umbrella-ize), and the Command Invocation Gates story.

**Likely outcome:** candidate DEC after survey + prototype + data accumulate.

## FB-073: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

See `feedback-archive.md` for full entry.

## FB-074: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

See `feedback-archive.md` for full entry.

## FB-075: TaskCreate/TaskUpdate harness reminder fires in projects that explicitly forbid built-in task tools

**Status:** cheap-action-shipped + deferred (structural fix upstream-gated)
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

**Status:** deferred (single-project signal; research-gated)
**Captured:** 2026-05-20
**Defer condition:** Re-assess when (a) 2nd project signals the same verification gap, OR (b) FB-066 downstream telemetry suggests broader runtime_validation hardening is needed. Single-project signal (styler T667) doesn't justify the design work (build-command discovery + catalog-path declaration; mitigations 1+3 are not as mechanical as FB-066's regex+grep). If signal escalates: route through `/research` for design — similar to FB-072's trial-gated DEC candidate path. Tracked in root CLAUDE.md § Active Follow-ups as of v4.6.1.
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

**Status:** new
**Captured:** 2026-05-20
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

## FB-078: /work Step 2b post-decision check fires /iterate based on `inflection_point` flag alone, ignoring chosen-option spec_impact intent

**Status:** new
**Captured:** 2026-05-20
**Source:** Surfaced 2026-05-20 during FB-011 Family E re-assessment — bridged from styler session export 2026-05-16 (`interaction-logs/processed/styler-session-2026-05-16.json` § `workflow_friction_notes`). Not surfaced in the inbox triage subagent's earlier analysis (this session's Phase 3 missed it); discovered during the Family E `Step 2b` cross-reference check.

DEC-083 (styler decision) correctly flagged `inflection_point: true` because the option space contained spec-impacting candidates. The user selected option δ (close) which has explicit NO spec impact. But `/work` Step 2b's post-decision check fires the `/iterate` suggestion based on the decision-level `inflection_point` flag alone — it does NOT read the chosen option's text for spec_revised intent. Result: false-positive `/iterate` suggestion on the next `/work` run.

### The structural gap

`inflection_point` is a property of the **decision** (was the option space spec-shaping?). But spec-impact is a property of the **selected option** (does the chosen path require a spec amendment?). The current check conflates the two — it treats the decision-level flag as the trigger, ignoring whether the actual selection has spec consequences.

### Mitigation candidates (from the session)

1. **Read the chosen option's text for `'no spec amendment'` markers.** When the option detail explicitly says no spec impact, skip the `/iterate` suggestion. Heuristic-based; tolerant of varied phrasing; no schema change.
2. **Add per-option `spec_impact` flag to the decision schema.** Author marks each option with `spec_impact: true | false | unclear` at decision creation. Step 2b reads the chosen option's flag deterministically. Cleaner; requires schema change + authoring burden.

Option 1 is cheaper (no schema change) but heuristic-shaped. Option 2 is more deterministic but requires authoring change. Could ship Option 1 first as a quick fix; escalate to Option 2 if heuristic false-negatives accumulate.

### Boundary with FB-017

FB-017 (shipped via inlining fix) was about Step 2b's **decision auto-finalization** sub-feature (checkbox detection → `status: approved`). This issue (FB-078) is about Step 2b's **post-decision check** sub-feature (does the chosen option warrant `/iterate`?). Same Step 2b function, different sub-paths; no overlap. The cross-reference to FB-017 in the styler session was a textual false-positive (matched "Step 2b") that surfaced this issue during the Family E re-assessment grep.

### Scope

- `.claude/commands/work.md` Step 2b post-decision check logic (primary)
- If Option 2 chosen: `.claude/support/reference/decisions.md` (decision record template + option authoring guidance) + decision-record schema enforcement

### Signal strength

Single-project signal (styler 2026-05-16). Low frequency expected — most `inflection_point: true` decisions DO have spec impact in their chosen option. The false-positive happens specifically when an inflection-eligible decision lands on a "close / defer / no-op" option. Could promote now (Option 1 cheap fix) or wait for 2nd-project signal.

Tags: workflow, work-step-2b, post-decision-check, false-positive, inflection-point, decisions-schema
