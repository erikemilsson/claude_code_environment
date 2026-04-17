# Plan — FB-019: `@path` imports in `.claude/CLAUDE.md`

**Purpose:** Make rules-file loading declarative in `.claude/CLAUDE.md` using Claude Code's `@path/to/import` syntax, instead of relying on implicit harness behavior. Single-file edit; corrective scope.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Source feedback item:** FB-019 (line 57) in `.claude/support/feedback/feedback.md`
**Related decision:** none — direct-implementation FB item
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in same commit as this plan)
**Tracker status line to advance:** `Phase 4 — FB-019 implemented (explicit @imports in .claude/CLAUDE.md); FB-028 + FB-029/030 + FB-011 remaining`

---

## Scope

| Item | Touch site | Edit type |
|------|-----------|-----------|
| FB-019 | `.claude/CLAUDE.md § "Workflow Rules"` (~lines 70–79) | Add `@import` lines before the existing bulleted list |

### Out of scope

- Reorganizing `.claude/rules/*.md` files themselves — FB-019 is only about making the load declarative. If a rule file is too long and benefits from chunking, that's a separate item.
- Removing the bulleted descriptions — the bullet list is a scannable index for human readers; `@` imports are the harness-level directive. Both layers keep their purpose.
- Adding `@imports` anywhere else in `.claude/CLAUDE.md` (e.g., pulling `shared-definitions.md` or `task-schema.md` into the Critical Invariants block). Possibly a future improvement, but out of scope for this item.
- `root CLAUDE.md` changes. That file is template-maintenance-only and gets replaced on project setup — no ship impact.

---

## Context to Load Before Executing

1. **`.claude/CLAUDE.md`** — full file (~84 lines). The "Workflow Rules" section lives near the bottom. Load once.
2. **`.claude/support/feedback/feedback.md`** lines 57–69 (FB-019) — confirm Assessed line hasn't drifted.
3. **`.claude/rules/*.md`** — confirm the seven rule files still exist with their current names:
   - `task-management.md`, `spec-workflow.md`, `decisions.md`, `dashboard.md`, `agents.md`, `archiving.md`, `session-management.md`
4. **`template-upgrade-2026-04.md`** — Current State + File Collision Map `.claude/CLAUDE.md` row (Best-prac column currently lists `FB-019 @path imports`).

**Best-practices doc reference:** CLAUDE.md supports `@path/to/import` syntax. Imports are auto-loaded by the harness — content of the referenced file is injected into context as if inlined. Relative paths resolve relative to the CLAUDE.md that contains the import.

Auto-memory: no specific entry is load-bearing.

---

## Implementation Steps

### Step 1: Add `@import` lines at the top of the Workflow Rules section

Locate `.claude/CLAUDE.md § "Workflow Rules"`. Current content:

```markdown
## Workflow Rules

Detailed workflow rules are in `.claude/rules/`:
- `task-management.md` — statuses, difficulty, ownership, parallel execution
- `spec-workflow.md` — spec lifecycle, propose-approve-apply, vision documents
- `decisions.md` — decision records, inflection points
- `dashboard.md` — navigation hub, interaction modes, regeneration strategy
- `agents.md` — agent separation, tool preferences, model requirement
- `archiving.md` — file placement, archive locations, credentials
- `session-management.md` — ending sessions, resuming, plans, context survival
```

Replace with:

```markdown
## Workflow Rules

Rules files are loaded via explicit imports (Claude Code auto-reads `@path` references in CLAUDE.md):

@.claude/rules/task-management.md
@.claude/rules/spec-workflow.md
@.claude/rules/decisions.md
@.claude/rules/dashboard.md
@.claude/rules/agents.md
@.claude/rules/archiving.md
@.claude/rules/session-management.md

Summary of each:
- `task-management.md` — statuses, difficulty, ownership, parallel execution
- `spec-workflow.md` — spec lifecycle, propose-approve-apply, vision documents
- `decisions.md` — decision records, inflection points
- `dashboard.md` — navigation hub, interaction modes, regeneration strategy
- `agents.md` — agent separation, tool preferences, model requirement
- `archiving.md` — file placement, archive locations, credentials
- `session-management.md` — ending sessions, resuming, plans, context survival
```

**Why keep the bulleted descriptions:** They're a scannable index for human readers browsing CLAUDE.md. The `@import` lines are the harness-level directive (load the file contents); the bulleted one-liners are the human-level index (what's in each file). Both serve different purposes. Removing the bullets would lose the "at-a-glance" view.

**Why the `@imports` go first:** Declarative directives at the top of the section make the load behavior obvious. The descriptive block below reads as commentary on what was loaded.

**Path format:** Use full repo-relative paths (`.claude/rules/...`) rather than bare names. Claude Code resolves `@` imports relative to the CLAUDE.md file, but explicit paths are unambiguous across IDE integrations and sub-project contexts (if a downstream project ever adds nested CLAUDE.md files).

---

### Step 2: Verify no duplicate load happens

After the edit, the rule files should appear in loaded context via the `@imports`. If the harness was already loading them through another mechanism (e.g., implicit "always load `.claude/rules/`"), we need to confirm there's no double-load.

**Verification approach:**
1. Commit the change.
2. Start a fresh Claude Code session in this repo (or run `/clear`).
3. Ask a simple question about a rule that's only defined in one of the imported files (e.g., "what are the 8 task statuses?" — answered by `task-management.md`).
4. If the answer is correct AND the system-reminder block shows the rules file content exactly once, the import is working without duplication.

If duplication is observed, that's a harness behavior worth investigating — but it's not a blocker for this change, since the cost is a small amount of re-injected tokens, and the behavior-clarification benefit stands.

**Note:** This verification is advisory. Don't block the commit on it.

---

### Step 3: Tracker bookkeeping

Update `template-upgrade-2026-04.md`:

**3a. Status line:** → `**Status:** Phase 4 — FB-019 implemented (explicit @imports in .claude/CLAUDE.md); FB-028 + FB-029/030 + FB-011 remaining`

**3b. Current State:** add new bullet:

```
- **FB-019 implemented 2026-04-17:** `.claude/CLAUDE.md § "Workflow Rules"` now uses explicit `@.claude/rules/*.md` imports at the top of the section, followed by the existing bulleted one-liner index. Declarative harness directive + human-readable summary preserved. All seven rule files explicitly imported (task-management, spec-workflow, decisions, dashboard, agents, archiving, session-management).
```

**3c. Next action bullet:** update to reflect remaining items (FB-028, FB-029/030, FB-011).

**3d. Phase 4 Single-item section:** flip the FB-019 row to `[x]` with date.

**3e. File Collision Map:** strike the `.claude/CLAUDE.md` row Best-prac column:
- `.claude/CLAUDE.md` row Best-prac: `FB-019 @path imports` → `~~FB-019 @path imports~~ ✓`

**3f. Cleanup Manifest:** add row:
```
| `plan-fb-019-claude-md-imports.md` | DELETE-AFTER | FB-019 CLAUDE.md @imports implementation plan for fresh-session execution |
```

**3g. Session Log entry:** Done / Judgment calls / Next / Open questions. Judgment calls to cover: (1) keeping bulleted descriptions alongside `@imports` rather than replacing; (2) full repo-relative paths over bare names; (3) not adding `@imports` for other files (task-schema, shared-definitions) in this scope.

---

### Step 4: Commit

Single commit. Pre-commit hook will warn about `version.json` (`.claude/CLAUDE.md` is sync-category).

Commit message (HEREDOC):

```
Phase 4: FB-019 — explicit @imports in .claude/CLAUDE.md

Replace implicit rules-file loading with explicit @path imports per
Claude Code's documented CLAUDE.md syntax. All seven rules files
(task-management, spec-workflow, decisions, dashboard, agents,
archiving, session-management) now loaded declaratively. Bulleted
one-liner index preserved below the imports as a human-readable
summary. No behavior change for the loaded content — just makes the
harness-level load directive explicit.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Verification Checklist (post-edit, pre-commit)

- [ ] `.claude/CLAUDE.md § "Workflow Rules"` contains seven `@.claude/rules/*.md` lines (one per rule file)
- [ ] `@imports` appear above the bulleted description list, not interleaved
- [ ] Bulleted description list preserved unchanged
- [ ] No other sections of `.claude/CLAUDE.md` modified
- [ ] Tracker: status, Current State bullet, Phase 4 single-item `[x]`, File Collision Map strike, Cleanup Manifest row, Session Log entry
- [ ] Pre-commit hook shows `version.json` warning (expected)

---

## What NOT to Do

- **Don't** delete the bulleted descriptions — they're the scannable index.
- **Don't** add `@imports` for `.claude/support/reference/*.md` files. Those are on-demand references loaded by specific commands, not always-in-context.
- **Don't** add `@imports` to the project root `./CLAUDE.md` (replaced on project setup; template-maintenance-only).
- **Don't** reorganize the rules files themselves.
- **Don't** bump `.claude/version.json` — Phase 5 handles scope.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Target | `.claude/CLAUDE.md § "Workflow Rules"` |
| Files being imported | `.claude/rules/*.md` (seven files) |
| Tracker | `template-upgrade-2026-04.md` (root) |
| Source feedback | `.claude/support/feedback/feedback.md` line 57 |

---

## Post-Commit: What Happens Next

- One Phase 4 single-file item closed. Remaining: FB-028 (setup-checklist CLI installs), FB-029/030 (new `automation.md`), FB-011 (scripts inventory).
- Version bump tally for Phase 5: DEC-007 + DEC-008 + FB-037 + work.md batch + FB-015 primary + session-management batch + iterate batch + agents batch + FB-019.
