# Plan — rules/agents.md + implement-agent.md Batch (FB-022 + FB-034 + FB-035 + FB-031)

**Purpose:** Apply four feedback items that land in the two hottest agent-touching files. All four are doc-level additions: three behavioral rules plus a short pattern mention. Zero implementation risk; rules + agent instructions only.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Source feedback items:** FB-022 (line 85), FB-031 (line 196), FB-034 (line 248), FB-035 (line 266) in `.claude/support/feedback/feedback.md`
**Related decision:** none — direct-implementation FB items
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in same commit as this plan)
**Tracker status line to advance:** `Phase 4 — agents group implemented (FB-022 + FB-031 + FB-034 + FB-035); plus FB-032 verify-agent matching check carried over from iterate batch`

---

## Scope

| Item | Primary touch site | Edit type |
|------|--------------------|-----------|
| FB-022 (root cause) | `rules/agents.md` new § "Root Cause Over Symptom" | New section in rules file (broad rule across all agents) |
| FB-022 (reinforce) | `implement-agent.md § "Implementation Guidelines"` | One new sub-section — 4 lines |
| FB-022 (verify matching check) | `agents/verify-agent.md § "Per-Task Verification"` | New line in the checks list |
| FB-034 (respect kills — behavior) | `rules/agents.md` new § "Behavioral Rules" | New section (paragraph + 3-bullet rule) |
| FB-034 (Critical Invariant) | `.claude/CLAUDE.md § "Critical Invariants"` | New 9th bullet |
| FB-035 (large-file Read) | `implement-agent.md § "Tool Preferences"` | New paragraph |
| FB-031 (Writer/Reviewer pattern) | `rules/agents.md § "Separated Concerns"` | New short paragraph |
| FB-032 matching check (carryover from iterate batch) | `agents/verify-agent.md § "Per-Task Verification"` check list | New line verifying spec-change tasks contain the `## Decisions in This Proposal` section |

### Out of scope

- Duplication of any rule across multiple files. Each rule has ONE primary home. Use references when needed.
- `.claude/README.md` FB-031 alt-site — skip. Rules/agents.md is the primary; README would duplicate.
- Implement-agent FB-031 mention — skip. Rules file is loaded; no need to duplicate.

---

## Context to Load Before Executing

1. **`.claude/rules/agents.md`** — full file (~35 lines). Two new sections land here. Keep in context.
2. **`.claude/agents/implement-agent.md`** — full file (~260 lines). Tool Preferences section (lines 22–40) and Implementation Guidelines (lines 168–221) gain additions.
3. **`.claude/agents/verify-agent.md`** — full file. Two new checks added to the per-task workflow. Locate the existing check list first.
4. **`.claude/CLAUDE.md`** — confirm the Critical Invariants bullet list (already at 8 bullets). New bullet becomes the 9th.
5. **`.claude/support/feedback/feedback.md`** lines 85–97 (FB-022), 196–208 (FB-031), 248–265 (FB-034), 266–278 (FB-035) — confirm Assessed lines haven't drifted.
6. **`template-upgrade-2026-04.md`** — Current State + File Collision Map `rules/agents.md`, `implement-agent.md`, `verify-agent.md`, `.claude/CLAUDE.md` rows.

**If this plan runs BEFORE the iterate batch:** drop the FB-032 verify-agent matching check from Step 6 below. The check is a carryover from the iterate plan.

**If the iterate batch ran but did NOT add the FB-032 matching check** (per its instruction to defer): include Step 6 here.

---

## Implementation Steps

### Step 1: FB-022 — Root Cause Over Symptom (rules/agents.md primary + implement-agent reinforce)

Locate `rules/agents.md`. After the existing `## State Ownership` section and before `## Tool Preferences`, insert:

```markdown
## Root Cause Over Symptom

When a test fails, a build breaks, a type error surfaces, or a runtime error occurs: fix the underlying cause, not the symptom.

**Symptom-only fixes that verify-agent rejects:**
- `try/except` (or equivalent) that silently swallows the error without handling it
- Suppressed linter/compiler warnings (e.g., `# type: ignore`, `@ts-ignore` without explanation)
- Skipped or deleted failing tests
- Magic-number overrides that work around a computed value rather than fixing the computation
- Mocks that paper over a real integration problem
- Catch-all error handlers that hide the specific failure

**The rule:** An implementation that makes an error disappear without understanding why the error occurred is not a completed task. If the root cause can't be fixed in the current task's scope, return `implementation_status: "blocked"` (not `completed`) with an `issues_discovered` entry explaining the underlying cause. Verify-agent rejects `completed` reports that suppress symptoms.

**When suppression IS acceptable:**
- The "error" is a spec-level design choice (e.g., the spec says "ignore malformed rows")
- A third-party library bug with a documented workaround (include a comment linking to the issue)
- Time-boxed mitigation with an explicit `issues_discovered` follow-up task

In those cases, the suppression is the fix — not a symptom hiding a bug.
```

**Then add a short sub-section to `implement-agent.md § "Implementation Guidelines"`** (after `### Scope Discipline` and before `### Progress Tracking`):

```markdown
### Root Cause Over Symptom

When an error surfaces during implementation, fix the underlying cause rather than silencing it. Suppressing warnings, skipping tests, adding try/except with empty bodies, or using magic-number overrides to paper over a problem is not completion — it's a deferred bug. If you cannot fix the root cause in this task's scope, return `implementation_status: "blocked"` with an `issues_discovered` entry describing the cause. See `.claude/rules/agents.md § "Root Cause Over Symptom"` for the full rule and exceptions.
```

---

### Step 2: FB-034 — Respect User Kills (rules/agents.md + CLAUDE.md Invariants)

**2a. `rules/agents.md`:** after the new `## Root Cause Over Symptom` section, add:

```markdown
## Behavioral Rules

**Respect prior kills.** When the user kills a long-running process (dev server, file watcher, batch loop, mass-file processor, external-API scan), do not restart it in the same session without renewed approval. "Kill" signals: explicit user message ("kill it", "stop the server", "cancel"), pressing Ctrl+C in a captured terminal, `/work pause`, or any explicit halt instruction.

The rule applies to the killed process AND to semantically equivalent replacements (killing `npm run dev` then starting `pnpm dev` on the same port IS a restart). Before re-initiating any halted long-running process, confirm with the user.

This complements DEC-005's permission-layer gate (which stops unauthorized tool calls): that gate catches unapproved starts; this rule catches authorized-but-destructive re-starts after an explicit halt. Behavioral rule, not a permission — auto mode (which approves tool calls by classifier) does not absorb it.

Note: starting a dev server for UI verification is a feature (per root `CLAUDE.md` guidance on UI testing), not a violation. The rule applies to *restarting after a kill*, not to initial starts.
```

**2b. `.claude/CLAUDE.md § "Critical Invariants"`:** append a new 9th bullet after the Settings layering bullet:

```markdown
- Respect prior kills: when the user halts a long-running process (dev server, watcher, batch loop), do not restart it in the same session without renewed approval. See `.claude/rules/agents.md § "Behavioral Rules"` for the full rule.
```

---

### Step 3: FB-035 — Large-file Read guidance in implement-agent.md

Locate `implement-agent.md § "Tool Preferences"` (lines 22–40). After the existing "Editing strategy for structured documents" block (ending with "these are error-prone for structured content"), add:

```markdown
**Large-file strategy:**

- **Prefer `Grep` / `Glob`** over `Read` when looking up content in files you don't need whole. A targeted pattern search returns relevant lines; reading a whole file to find one definition wastes tokens and risks hitting the file-size cap.
- **Use `Read` with `offset` / `limit`** when a file is known or suspected to be large (thousands of lines, hundreds of KB). Read the relevant range, not the whole file.
- **File-too-large errors:** when `Read` fails with a size cap, do NOT read the file in multiple full calls. Either (a) re-target with `Grep` to find the relevant section, then `Read` that offset/limit range, or (b) ask the user if the file should actually be this large — it may be a committed log file or dataset that belongs elsewhere.

This is a quantified friction reduction: "File Too Large" has been the single largest tool-error category in observed sessions.
```

---

### Step 4: FB-031 — Writer/Reviewer parallel-session pattern in rules/agents.md

Locate `rules/agents.md § "Separated Concerns"` (lines 3–8). After the existing 3-agent bullet list, add a new paragraph:

```markdown
**Writer/Reviewer scales further with parallel sessions.** Within a single session, implement-agent and verify-agent already provide the writer/reviewer separation. For higher-rigor review — security audit, architectural review, independent quality pass — you can run two separate `claude` instances: Session A implements; Session B (fresh context, no implementation memory) reviews the finished code. This is optional and external to the template; the existing implement-agent / verify-agent split is sufficient for most work.
```

---

### Step 5: FB-022 verify-agent matching check

Locate `agents/verify-agent.md § "Per-Task Verification"` checklist (there's a list of checks the agent runs). Add one new check:

```markdown
- **Symptom-vs-root-cause check:** Inspect the implementation for symptom-hiding patterns — empty `try/except`, broad catch-all handlers, `@ts-ignore` / `# type: ignore` without a documented reason, skipped or deleted tests, suppressed warnings, magic-number overrides. If any present without an explicit exception (per `rules/agents.md § "Root Cause Over Symptom"` — spec-level design choice, third-party-library workaround with issue link, or `issues_discovered` follow-up), return `result: "fail"` with an `issues` entry pointing to the specific suppression.
```

---

### Step 6: FB-032 verify-agent matching check (carryover from iterate batch)

**Only include this step if the iterate batch has landed AND its Session Log notes this check as deferred-to-agents-batch.**

Locate `agents/verify-agent.md § "Per-Task Verification"` checklist. Add:

```markdown
- **Spec-change Decisions section check:** For tasks whose `spec_section` indicates a spec-change outcome (task modifies `spec_v*.md` or `.claude/spec_v*.md` is in `files_affected`), verify the `/iterate` proposal that drove this task included a `## Decisions in This Proposal` section with all `[NEEDS APPROVAL]` items resolved. If the task was applied without this contract being honored, return `result: "fail"` with an issue flagging the contract violation — silent design decisions should not reach the spec.
```

---

### Step 7: Tracker bookkeeping

Update `template-upgrade-2026-04.md`:

**7a. Status line:** → `**Status:** Phase 4 — agents group implemented (FB-022 + FB-031 + FB-034 + FB-035{+ FB-032 matching check if iterate batch landed}); FB-019 + FB-028 + FB-029/030 + FB-011 remaining`

**7b. Current State:** add new bullet:

```
- **agents group implemented 2026-04-17:** Four rules/agents.md + implement-agent.md + CLAUDE.md additions. Root-cause-over-symptom rule: new § in rules/agents.md (primary) + sub-section in implement-agent Implementation Guidelines (reinforcement) + matching check in verify-agent per-task checklist (FB-022). Respect-prior-kills behavioral rule: new § in rules/agents.md + new 9th Critical Invariant bullet in `.claude/CLAUDE.md` pointing to the rules file (FB-034). Large-file Read guidance: new paragraph in implement-agent § Tool Preferences covering Grep/Glob preference, offset/limit usage, and file-too-large recovery (FB-035). Writer/Reviewer parallel-session pattern: one-paragraph mention in rules/agents.md § Separated Concerns (FB-031). {If FB-032 check included: Also landed the deferred FB-032 verify-agent matching check for spec-change tasks requiring the Decisions section contract.} Auto mode does not absorb any of these — all are behavioral or rule-layer, not permission-layer.
```

**7c. Next action bullet:** update.

**7d. Phase 4 Hot files block:** flip the relevant rows to `[x]`:
- `rules/agents.md` / `implement-agent.md` row
- Add tracker note: "FB-022 also touched verify-agent.md; FB-034 also touched .claude/CLAUDE.md Critical Invariants."

**7e. File Collision Map:** strike affected cells:
- `rules/agents.md` row — Best-prac (FB-022 root-cause; FB-031 Writer/Reviewer) → `~~FB-022 Root Cause section~~ ✓; ~~FB-031 Writer/Reviewer paragraph~~ ✓`; Usage (FB-034 behavior; FB-035 Tool Prefs) → `~~FB-034 Behavioral Rules section~~ ✓; FB-035 landed in implement-agent.md Tool Preferences ✓`
- `.claude/agents/implement-agent.md` row — Best-prac (FB-022) → `~~FB-022 Root Cause sub-section~~ ✓`; Usage (FB-034, FB-035) → `FB-034 landed in rules/agents.md + CLAUDE.md ✓; ~~FB-035 large-file paragraph~~ ✓`
- `.claude/agents/verify-agent.md` row — Best-prac (FB-022 symptom-fix check) → `~~FB-022 symptom-vs-root-cause check~~ ✓`; if FB-032 check landed: Usage (FB-032 decisions check) → `~~FB-032 Decisions section check~~ ✓`
- `.claude/CLAUDE.md` row — Usage (FB-034 Critical Invariants) → `~~FB-034 Critical Invariant bullet 9~~ ✓`

**7f. Cleanup Manifest:** add row:
```
| `plan-agents-batch.md` | DELETE-AFTER | rules/agents.md + implement-agent.md group (FB-022/031/034/035) implementation plan for fresh-session execution |
```

**7g. Session Log entry:** Done / Judgment calls / Next / Open questions. Judgment calls to cover: (1) one primary home per rule vs duplication; (2) why CLAUDE.md Critical Invariant points to rules/agents.md instead of restating the rule (single source of truth); (3) FB-034's "restart-after-kill" narrow scope (avoids conflict with UI-verification feature); (4) FB-035's offset/limit guidance in implement-agent rather than rules/agents.md (agent-level tool usage, not cross-agent rule); (5) whether FB-032 check was included or deferred.

---

### Step 8: Commit

Single commit. Pre-commit hook will warn about `version.json` (`rules/agents.md`, `implement-agent.md`, `verify-agent.md`, `.claude/CLAUDE.md` all sync-category).

Commit message (HEREDOC):

```
Phase 4: agents group — FB-022 + FB-031 + FB-034 + FB-035

Four agent-surface additions landing in rules/agents.md,
implement-agent.md, verify-agent.md, and .claude/CLAUDE.md. All
rule-layer or behavioral additions — no implementation risk.

FB-022 (root cause over symptom): new § in rules/agents.md defining
symptom-only fixes (empty try/except, suppressed warnings, skipped
tests, magic numbers) as grounds for verify-agent rejection. Short
reinforcement sub-section in implement-agent.md Implementation
Guidelines. Matching symptom-vs-root-cause check added to
verify-agent.md per-task checklist so verify has an unambiguous
grounds to fail symptom-fix reports.

FB-034 (respect prior kills): new § "Behavioral Rules" in
rules/agents.md defining the rule and its scope (restart after an
explicit kill requires renewed approval — not initial starts, which
are features per root CLAUDE.md UI-verification guidance). New 9th
bullet in .claude/CLAUDE.md § "Critical Invariants" pointing to the
rules file. Auto mode does not absorb this — behavioral, not
permission.

FB-035 (large-file Read strategy): new paragraph in
implement-agent.md § Tool Preferences covering Grep/Glob preference
over whole-file Read, offset/limit usage for known-large files, and
recovery from File-Too-Large errors. Addresses the single largest
tool-error category observed.

FB-031 (Writer/Reviewer parallel sessions): one-paragraph mention in
rules/agents.md § Separated Concerns noting that the
implement-agent / verify-agent split already provides
writer/reviewer, and that users can scale further by running two
separate claude sessions for independent review.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Verification Checklist (post-edit, pre-commit)

- [ ] `rules/agents.md` has new `## Root Cause Over Symptom` section (between State Ownership and Tool Preferences)
- [ ] `rules/agents.md` has new `## Behavioral Rules` section with the respect-prior-kills rule
- [ ] `rules/agents.md § "Separated Concerns"` has the Writer/Reviewer paragraph
- [ ] `implement-agent.md § "Implementation Guidelines"` has `### Root Cause Over Symptom` sub-section
- [ ] `implement-agent.md § "Tool Preferences"` has the "Large-file strategy" block
- [ ] `verify-agent.md § "Per-Task Verification"` check list includes the symptom-vs-root-cause check (and optionally the FB-032 Decisions section check)
- [ ] `.claude/CLAUDE.md § "Critical Invariants"` has a 9th bullet referencing the behavioral rule
- [ ] Tracker: status, Current State, Phase 4 hot files `[x]`, File Collision Map strikes, Cleanup Manifest row, Session Log entry
- [ ] No edits to `.claude/README.md` (FB-031 primary is rules/agents.md)
- [ ] Pre-commit hook shows `version.json` warning (expected)

---

## What NOT to Do

- **Don't** duplicate the root-cause rule across `rules/agents.md` and `implement-agent.md` — the implement-agent sub-section points back; no re-statement of the full rule + exceptions.
- **Don't** broaden FB-034 to "don't start long-running processes" — that conflicts with root `CLAUDE.md`'s UI-verification guidance. Narrow scope is "restart after explicit kill."
- **Don't** move FB-035 into `rules/agents.md` — it's implement-agent-specific tool usage, not a cross-agent rule.
- **Don't** add FB-031 to `.claude/README.md` (alt-site) — skip the duplication.
- **Don't** add the FB-032 matching check if the iterate batch has NOT landed yet (check tracker Session Log before running this plan).
- **Don't** restructure the existing implement-agent or verify-agent workflow steps — these are additive.
- **Don't** bump `.claude/version.json` — Phase 5 handles scope.
- **Don't** archive FB items in `feedback.md` — same convention as prior direct-implementation items.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Primary rules target | `.claude/rules/agents.md` |
| Implement-agent target | `.claude/agents/implement-agent.md` |
| Verify-agent target | `.claude/agents/verify-agent.md` |
| CLAUDE.md target | `.claude/CLAUDE.md § "Critical Invariants"` |
| Tracker | `template-upgrade-2026-04.md` (root) |
| Source feedback | `.claude/support/feedback/feedback.md` (FB-022 line 85, FB-031 line 196, FB-034 line 248, FB-035 line 266) |

---

## Post-Commit: What Happens Next

- Tracker shows agent-file hot-files row `[x]`. Remaining Phase 4 single-file items: FB-019 (`@path` imports in `.claude/CLAUDE.md`), FB-028 (CLI-tool hints in `setup-checklist.md`), FB-029 + FB-030 (new `automation.md`), FB-011 (scripts inventory).
- All four Phase 4 hot-file batches complete (work.md, session-management.md, iterate.md, agents). Phase 4 enters single-file mode.
- FB-033 trial-gate data now accumulating via FB-032's contract; decide whether to pursue FB-033 research after enough trial data.
- Version bump tally for Phase 5: DEC-007 + DEC-008 + FB-037 + work.md batch + FB-015 primary + session-management batch + iterate batch + agents batch.
