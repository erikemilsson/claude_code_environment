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

## FB-072: [CLOSED — moved to `template-maintenance/feedback-archive.md`]

**Status:** closed 2026-05-24 — DEC-018 resolved to **Option B** (status quo, explicit-arg dispatch); the interpretive-router proposal was declined after a value deep-dive (CCE's own 26-session usage logs showed near-absent recall-the-token friction → marginal value vs. permanent costs). Decision: `decisions/decision-018-command-routing-interpretive-vs-explicit.md` (`approved`). Re-open condition in DEC-018 Impact if Wave 2 grows the command surface. Durable records: that DEC + `decisions/.archive/decision-018-research-2026-05-24.md` + `.claude/support/workspace/router-survey.md`. See archive for the full closure record.

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

**Status:** mitigation 1 shipped (v4.15.0) — production-build check runs in `/work`'s Empirical Evidence Gate when a task touches client-marked files and root `./CLAUDE.md § Verification Hooks` declares a build command (catches failure mode 1, the client/server bundle boundary). Mitigations 2 (ESLint client-import rule) + 3 (live-data cross-reference — failure mode 2) remain deferred, research-gated.
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

## FB-087: Playwright MCP large-DOM token-limit pattern — prefer browser_evaluate over browser_snapshot

**Status:** cheap-action-shipped
**Captured:** 2026-05-24
**Shipped:** 2026-05-24 (v4.7.3) — new `## MCP and Result-Size Constraints` section added to `.claude/rules/agents.md` between "## MCP and Parallel Execution" and "## Tool Preferences". Documents that `browser_snapshot` on long-scroll pages (~10K+ char DOM) exceeds per-tool-call token budgets and truncates silently; prefers `browser_evaluate` with targeted DOM queries. Optional project-side helper follow-up deferred unless a multi-project signal emerges.
**Source:** Bridged from styler 2026-05-21 session (template_version 4.6.3) via `/health-check` Part 7 aggregation.

## Observation

Playwright MCP `browser_wait_for` and `browser_snapshot` return 105K+ character snapshots for large pages (the styler `/style` page is ~36000px tall with many sections), exceeding the result token limit. The model can't process the snapshot — tool result truncates or fails outright.

The workaround styler used: replace `browser_snapshot` with `browser_evaluate` containing targeted DOM queries (`document.querySelector(...).textContent`, etc.). The pattern is reusable for any large-DOM page where the audit/verification only needs specific elements.

## Meta-pattern

The current `agents.md § "MCP and Parallel Execution"` section covers the parallel-execution constraint (single-instance MCPs can't fan out) but doesn't cover the per-call result-size constraint. `browser_snapshot` is the default tool the model reaches for, and on large pages it fails silently from the model's perspective (token limit exceeded → degraded behavior).

## Proposed template surface

One-paragraph addition to `.claude/rules/agents.md § "MCP and Parallel Execution"` (or a sibling sub-section "MCP and Result-Size Constraints"):

> Playwright MCP `browser_snapshot` returns the full accessibility tree of the current page. For pages over ~10K characters of DOM (long-scroll pages, sites with many sections), the result can exceed the model's per-tool-call token budget and truncate silently. For audits/verifications that only need specific elements, prefer `browser_evaluate` with targeted DOM queries (e.g., `document.querySelectorAll('h2').forEach(...)`). Reserve `browser_snapshot` for small pages or when you genuinely need the full tree.

## Triage recommendation

**Cheap action:** one-paragraph addition to `agents.md`. No DEC needed. Catches future "why is my Playwright snapshot empty" debugging cycles across all projects.

**Optional follow-up:** project-side helpers under `.claude/scripts/` that wrap common Playwright-evaluate patterns (e.g., extract-all-headings, count-elements-by-selector) — but these are project-specific and not worth template-shipping unless a multi-project pattern emerges.

## Relationship to existing template content

- `.claude/rules/agents.md § "MCP and Parallel Execution"` covers cross-call state collision; this FB covers per-call result size.
- DEC-005 / auto-mode covers permission gating, not result-size.
- No existing template surface addresses this.

## Source trace

- Bridged from `interaction-logs/processed/.session-export-2026-05-21.json` § `claude_assessment.workflow_friction_notes[3]`.
- Single-session signal. Cheap-action threshold is low — one paragraph addition. Capture now, ship in next template patch.

Tags: template-side, mcp, playwright, result-size, browser-snapshot, browser-evaluate, agents-md-extension, cheap-action-candidate, single-project-signal

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

## FB-095: Spec-scale ceiling — single-file spec architecture strains at large-project scale (styler at 837KB)

**Status:** open — research-gated (recommend `/research` → DEC before any mechanism ships)
**Captured:** 2026-06-10
**Source:** template-side cross-repo usage analysis (2026-06-10 session: styler project state + 47-export `interaction-logs/` corpus + ship-log classification). Captured directly in the maintenance queue per the FB-062 convention (template-side session; design-discussion-needed item). The same analysis produced three temporary root-level ship-plan files (`ship-plan-{1,2,3}-*.md`) covering separate findings; this item is independent of them.

## Observation

The template's spec workflow assumes a monolithic spec readable in one pass. styler — the most active downstream project — has outgrown that assumption:

- `spec_v15.md` = **837,049 chars (~200K+ tokens)** — larger than a 200K context window outright; even at 1M-context economics it cannot be casually re-read, and combined with code it dominates any working set.
- 15 prior spec versions archived (56 files incl. decomposed snapshots); 132 decision records.
- Friction register: **22 of 39 markers are `spec_implementation_gap`**, and 8 of the 10 currently-open markers are spec-vs-code gaps.
- 35 of 391 hand-written session-export friction notes are spec-drift-themed.
- `/iterate` is the #2 command by usage (59 mentions vs `/work`'s 87 across the 47-export corpus), and 38% of sessions are zero-task meta-sessions — a substantial share of Erik's time is spec upkeep on a file no agent can hold whole.

## Why this is template-level (not just a styler problem)

- `.claude/CLAUDE.md § Critical Invariants` mandates **"Exactly one `spec_v{N}.md` exists in `.claude/` at any time"** — the invariant itself is the scaling bottleneck.
- The tooling assumes the monolith: `/iterate` proposes against the whole file; `fingerprint.py --sections` hashes per-`##`-section of one path; `/audit-coherence` lenses, decomposition provenance fields, and `/shakedown` Phase 0 grounding all address a single spec path.
- Every long-running project trends this way: the spec grows monotonically by design (feature retirement *annotates* rather than excises, per `rules/feature-retirement.md` — correct for drift detection, but it means specs only grow).

## Candidate directions (for `/research`; not pre-decided)

1. **Sharded spec:** `spec/` directory with per-domain files + a generated index/manifest (the invariant becomes "exactly one spec manifest").
2. **Single file + mandatory generated index:** keep the invariant; add a compiled TOC/section-index artifact and section-scoped read discipline (tooling change only).
3. **Tiered spec:** stable-core file + active-surface file, with periodic merge (mirrors task-archive tiering).
4. **Status quo + spec-diet discipline:** `/iterate hygiene` gains a "move historical/retired detail to archive" pass — cheapest; may only delay the ceiling.

## Research questions

- **Threshold:** at what spec size does quality measurably degrade (proposal accuracy, drift-detection reliability, token cost)? styler's history can calibrate; survey other downstream projects' spec sizes for the growth curve.
- **Drift detection:** can section fingerprints span multiple files — does `fingerprint.py` need a manifest mode? What happens to existing provenance fields in task JSON?
- **Migration:** cost and procedure for an existing 837KB `spec_v15.md` (fingerprints, task provenance, decision cross-refs, retirement markers).
- **Blast radius:** `/work` spec-discovery glob, all `/iterate` modes, audit lenses, `/shakedown` grounding, decomposition, DEC-016 path patterns in `settings.json` `permissions.ask`.
- **Interaction with FB-093/`/shakedown`:** capability-boundary corpora absorb some "where the system is" duty — does that relieve spec growth pressure or add a parallel surface?

## Triage recommendation

**`/research`** (template-level → root `decisions/`, next free DEC number). This touches a Critical Invariant plus drift fingerprinting plus `/iterate` — inflection-point-shaped, not a direct edit. If research concludes direction 4 (discipline only), no DEC needed per the FB-085 reversibility precedent; directions 1–3 warrant the full record.

Tags: template-side, spec-workflow, scale, research-gated, dec-candidate, iterate, drift-detection, fingerprinting, styler-evidence

## FB-096: Model-surface refresh — authoring-doc Agent-model enum drift (`fable`) + deliberate pin re-evaluation

**Status:** open — sub-issue A verify-then-fix (Part 2d `[V]` candidate); sub-issue B user-decision-gated
**Captured:** 2026-06-10
**Source:** surfaced during the v4.13.1 pointer-rot sweep (Plan 2 P1; root `ship-plan-2-prose-diet-and-mechanization.md`, temporary working file). Both sub-issues touch the model surface centralized in `.claude/CLAUDE.md § Model Requirement` by v4.13.1.

### Sub-issue A — capability-doc drift: Agent tool `model` enum missing `fable`

`claude-code-authoring.md § "Tool & Dispatch Surface"` (~line 133) states the Agent tool's `model` parameter exposes only `sonnet | opus | haiku`. Observed in the live harness this session (template repo, Claude Code running Fable 5): the parameter enum also includes `fable`. Route per DEC-017 discipline (FB-094 verified-then-fixed precedent): verify against official Claude Code docs via `/health-check` Part 2d `[V]` (or a manual verify-then-fix pass), then update the enum + footer `Last verified`. Do NOT edit from session observation alone.

### Sub-issue B — pin re-evaluation: should the environment stay pinned to Opus 4.7?

v4.13.1 made `.claude/CLAUDE.md § Model Requirement` the single canonical source for both the design pin (Opus 4.7) and the `Task` dispatch value (`"opus[1m]"`), and documented honestly that the alias floats with the latest Opus while the pin records the tested version. With Opus 4.8 and Fable 5 released, pin and alias have **already diverged** — dispatches today run newer-than-pin. Decision needed (user's):

- **(a) Ratify the float** — restate the pin as "current Opus tier"; spot-check the difficulty-calibration note in `shared-definitions.md` still holds.
- **(b) Pin explicitly to 4.7** — switch dispatch values to the explicit ID; FIRST verify the `Task`/Agent `model` param accepts full model IDs (sub-issue A's verification covers this).
- **(c) Move the pin forward deliberately** (4.8 or Fable) — after a `/shakedown`-style pass on agent behavior at the new tier.

Affected on any outcome: `.claude/CLAUDE.md § Model Requirement` (canonical), `shared-definitions.md` calibration note, `.claude/README.md` design-target line, agent-file capability prose ("Opus 4.7's interleaved/adaptive thinking") ×3.

**Ordering:** A precedes B — option (b)'s feasibility depends on what the param actually accepts, which A's verification establishes.

**Triage recommendation:** one session: run Part 2d `[V]` on the authoring doc (resolves A), then decide B with verified facts in hand. A is cheap-mechanical; B is decision-gated (no `/research` unless option (c)'s shakedown surfaces surprises).

Tags: template-side, model-pin, capability-doc, dec-017, part-2d, fable, verify-then-fix, user-decision-gated

## FB-097: Spec acceptance-criteria boxes never reconciled with phase-level verification

**Status:** new
**Captured:** 2026-05-24 (bridged into the maintenance queue 2026-06-11 via `/health-check` Part 7 step 3c)
**Source:** Bridged from flirty-gym (template_version 4.7.1) via `/feedback template:` — direct inbox write, no local flirty-gym FB entry (per user choice 2026-05-24).

The template keeps two representations of phase acceptance-criteria state and never reconciles them: (1) the spec's inline `- [ ]` per-phase acceptance boxes (the authored definition of done), and (2) `verification-result.json`'s `criteria[]`, which verify-agent writes and the dashboard renders as a [x]/[ ] checklist. After phase-level verification PASSES, the documented completion flow updates verification-result.json, the dashboard, and — at the final phase only — the spec `status:` frontmatter, but it NEVER touches the spec's inline acceptance boxes. Three things are left undefined:

- **Authority:** which artifact is the source of truth for "this phase's acceptance criteria are met"? spec-workflow.md calls the spec "the living source of truth" (which implies the inline boxes), yet nothing keeps them in sync with the verifier — so the source-of-truth document silently goes stale/false.
- **Tick responsibility:** if the inline boxes are meant to be ticked post-verification, by whom and at what step? verify-agent can't write the spec; the /work orchestrator's completion flow doesn't do it.
- **DEC-016 classification:** ticking a `- [ ]` → `- [x]` in spec BODY text is, by DEC-016's literal carveout (which names only archiving / version transitions / frontmatter), a substantive text edit → routes through /iterate. That couples routine phase-closure box-ticking to a full /iterate cycle — almost certainly not the intent, and undocumented.

No /health-check or /audit-coherence lens detects spec-box vs verification-result.json divergence, so it accrues silently.

**Evidence (real bite):** In flirty-gym (template v4.7.1), Phase 1's spec acceptance boxes are all [x] but Phase 2's are all [ ] — despite BOTH phases having a recorded phase-level verification-result.json PASS (Phase 2 = 7/7, all per-task verifications passing, all friction markers resolved). The spec asserts Phase 2 is incomplete while every other artifact says it passed. The split arose precisely because the template gives no rule: Phase 1 got ticked (manually, under spec_v2), Phase 2 didn't. Any multi-phase project hits this.

**Possible directions (from the capture — not prescribing):** (A) declare the inline boxes authored-only and verification-result.json authoritative, document it, add a /health-check note that inline boxes are informational (lowest churn; leaves the source-of-truth doc visibly stale). (B) the /work orchestrator ticks the spec's phase boxes at phase-level PASS as an infrastructure operation (state-reflection of a verifier result — same class as the `status:` flip), with an explicit DEC-016 carveout clause for "acceptance-box state-sync" (keeps the source of truth honest without an /iterate cycle; needs the DEC-016 amendment). (C) detection-only: a /health-check or /audit-coherence lens that flags spec-box vs verification-result.json divergence and prompts reconciliation (catches drift without deciding authority; weakest).

**Triage recommendation:** likely `/research` → decision record (root `decisions/`, next free DEC number) — option (B) amends DEC-016's carveout list, which shouldn't happen as a direct edit.

Tags: template-side, spec-workflow, verification, dec-016-boundary, dec-candidate, flirty-gym-evidence, bridged

## FB-098: persist-friction.py — mechanize the friction dual-write + FR-NNN assignment

**Status:** new
**Captured:** 2026-06-11
**Source:** Insight aggregation over the 70-export corpus (first pipeline stage-4 run since 2026-03-30) — full evidence in `interaction-logs/insights/2026-06-11_work_friction-persistence-bookkeeping-weight.md` (gitignored working doc, template repo only). 5 occurrences across styler (v4.7.1–v4.11.0, ×3) + Personal (v4.11.0) + flirty-gym (v4.7.1 collision incident); a 6th styler note asks for exactly this script by name.

The State Persistence Protocol's per-marker bookkeeping (`.session-log.jsonl` + `.pending-markers.jsonl` dual-write, plus `friction.jsonl` projection with FR-NNN assignment for audit-eligible kinds) is orchestrator-side hand-written Python-in-Bash. Observed failure modes at build scale: outright deferral (Personal 06-03 — three markers parked in task notes/handoff and never reached the register), duplicate FR ids from naive max+1 (flirty-gym FR-001 collision; styler FR-031 textual-reference collision), and per-marker verbosity ("three writes per marker").

**Proposal:** `.claude/scripts/persist-friction.py` per the scripts invocation contract (stdlib-only, structured stdout, orchestrator-invoked — subagents still return markers in reports). Takes a marker batch (stdin JSON or args); performs the dual-write + audit projection; assigns collision-safe FR-NNN by reading BOTH `friction.jsonl` ids and textual `FR-\d+` references; returns assigned ids for the orchestrator to echo into task notes. Composes with the parked Family F checker (scripts-candidates.md): helper makes compliance cheap, checker catches non-compliance.

**Triage recommendation:** direct template edit (script + tests, Family A/B precedent — v3.0.0/v3.1.1). Above the 3-occurrence mechanization bar; no DEC (advisory script, trivially reversible).

Tags: template-side, scripts, friction-register, state-persistence, work, mechanization, insights-derived

## FB-099: Gitignored `.claude/` state — surface the un-backed-up-source-of-truth hazard

**Status:** new
**Captured:** 2026-06-11
**Source:** Insight aggregation (first stage-4 run) — full evidence in `interaction-logs/insights/2026-06-11_work_gitignored-claude-state-hazard.md`. 5 occurrences across styler (v4.0.0–v4.11.0) + Personal (v4.11.0); in-corpus ask: "/health-check could surface this so the user knows" (styler 05-27).

When a project gitignores `.claude/**` (styler's deliberate fork convention), the spec, decisions, tasks, dashboard, and friction register are untracked — never committed, invisible to git safety nets. Observed bites: `/iterate` spec edits that "live only as working state"; a session asserting "spec_v15.md is tracked, just commit it" with the premise inverted by the gitignore; `/work pause` Step 0e excluding ALL `.claude/` paths from the uncommitted-work check, which also hides git-TRACKED `.claude/vision/*.md` edits (the filter assumes `.claude/` is state-not-source). The template repo itself has the same shape: `interaction-logs/` insights are gitignored working data.

**Proposal (both cheap, report-level):** (a) `/health-check` informational check — if `.claude/spec_v*.md` / `tasks/` / `support/decisions/` match the project's gitignore, report once per run: "template state is untracked — deliberate? consider a backup convention"; (b) `/work pause` Step 0e — scope the exclusion to *gitignored* `.claude/` paths only, so tracked `.claude/` files participate in the uncommitted-work check. Neither forces behavior on projects with deliberate conventions. Distinct from FB-063 (worktree reads of gitignored state).

**Triage recommendation:** direct template edit (two small additions; PATCH-to-MINOR).

Tags: template-side, health-check, work-pause, gitignore, data-safety, insights-derived

## FB-100: `owner: both` tasks lack a templated routing predicate + completion path

**Status:** new
**Captured:** 2026-06-11
**Source:** Insight aggregation (first stage-4 run) — full evidence in `interaction-logs/insights/2026-06-11_work_owner-both-completion-path.md`. 4 occurrences across styler (v3.13.0, v4.10.2 ×2) + OEMMatInsightBI (v4.0.0).

The completion machinery is two-track (claude: implement→verify; human: self-attestation via `/work complete`); `owner: both` falls between. Observed: the self-attestation auto-generate rule is documented for `owner: human` only — both-owned "lived gates where Claude's half is done" have no clean close (styler 05-28); Step 1d's fast-path predicate (`owner == human OR Blocked OR On Hold`) misses both-owned tasks user-gated on physical-world prerequisites — found independently in two projects; both-owned capture flows run as conversational design-partner work the routing model doesn't anticipate (styler T751).

**Partial coverage shipped:** v4.14.0's waiting-on-you queue enumerates `owner: both` awaiting review (visibility half done). Not covered: routing (Step 1d predicate) and completion shape.

**Proposal:** (a) extend Step 1d's fast-path predicate with `owner == "both" AND user_review_pending` (or equivalent user-gated condition); (b) document the `owner: both` completion shape in `/work complete` — Claude's half verified by verify-agent as usual; user's half closes via the same self-attestation mechanism as `owner: human` (one rule extension, no new schema).

**Triage recommendation:** direct template edit (MINOR — routing behavior change); low urgency given the v4.14.0 visibility half.

Tags: template-side, work, routing, owner-both, task-completion, insights-derived
