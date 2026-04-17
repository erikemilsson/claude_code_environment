# Plan — rules/session-management.md Batch (FB-023 + FB-024 + FB-025)

**Purpose:** Add three session-management tools (`/btw`, `/rewind` + Esc+Esc, `/rename`) to `.claude/rules/session-management.md` as documented in the Claude Code best-practices doc. Single-file, additive, low-risk.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Source feedback items:** FB-023, FB-024, FB-025 (in `.claude/support/feedback/feedback.md`)
**Related decision:** none — direct-implementation FB items
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in same commit as this plan)
**Tracker status line to advance:** current (`Phase 4 — FB-015 primary landed in dashboard-regeneration.md …`) → `Phase 4 — session-management.md group implemented (FB-023 + FB-024 + FB-025); remaining direct items next`

---

## Scope

| Item | Touch site | Edit type |
|------|-----------|-----------|
| FB-023 `/btw` | `session-management.md § "Managing Context Pressure"` | New bullet in existing list |
| FB-024 `/rewind` + Esc+Esc | `session-management.md` new `## Checkpointing and Rewind` section after `## What Survives What` table | New section (~12 lines) |
| FB-025 `/rename` | `session-management.md § "Resuming Sessions"` | New row in existing table (or a one-liner after it) |

All three live in one file — single bundled edit pass.

### Out of scope

- Any touch to `.claude/rules/*.md` beyond session-management.md
- Any behavior change — these are purely user-facing doc additions

---

## Context to Load Before Executing

1. **`.claude/rules/session-management.md`** — full file (~120 lines). All three edits land here. Read once, hold in context.
2. **`.claude/support/feedback/feedback.md`** lines 99–139 (FB-023, FB-024, FB-025) — confirm Assessed lines haven't drifted.
3. **`template-upgrade-2026-04.md`** — Current State + File Collision Map `rules/session-management.md` row + Cleanup Manifest.

No other files needed — this is a self-contained single-file edit.

---

## Implementation Steps

### Step 1: FB-023 — `/btw` bullet in Managing Context Pressure

Locate `## Managing Context Pressure` section. Currently has three bullets (`/compact focus on …`, `/clear`, "CLAUDE.md and rules files", "Auto-memory").

**Insert a new bullet between `/clear` and "CLAUDE.md and rules files":**

```markdown
- **`/btw {question}`** — ask a quick side question without polluting conversation history. The answer appears in a dismissible overlay and is NOT added to the transcript. Useful when you want to check something (e.g., "what's the syntax for ...") mid-work without derailing the current thread or bloating context.
```

---

### Step 2: FB-024 — New Checkpointing and Rewind section

Locate `## What Survives What` section (it ends with a table of survival matrices). Find the next `---` or `##` after it.

**Insert a new section immediately after the What Survives What table, before the next `##` heading:**

```markdown
## Checkpointing and Rewind

Every Claude action creates a checkpoint. Two ways to access them:

- **`Esc+Esc`** — opens the rewind menu immediately (press Escape twice)
- **`/rewind`** — opens the rewind menu as a slash command

From the rewind menu, you can restore:
- **Conversation only** — Claude forgets what it said, code changes preserved
- **Code only** — conversation preserved, file changes rolled back
- **Both** — full time-travel to the selected checkpoint

Checkpoints persist across sessions, so you can rewind even after closing and reopening. This is the complementary recovery mechanism to `/work pause` and handoff files: use handoff for planned wind-downs, checkpoints for recovering from an agent misstep or a wrong turn.

---
```

(Trailing `---` is a new horizontal rule separating Checkpointing from the following section.)

---

### Step 3: FB-025 — `/rename` in Resuming Sessions

Locate `## Resuming Sessions` section. It contains a table of resume methods (`claude --continue`, `claude --resume`, `Fresh /work`, `/clear then /work`).

**Add a brief paragraph immediately AFTER the resume-methods table (before the "Which Persistence Mechanism When" heading or next section heading):**

```markdown
**Naming sessions with `/rename`:** By default sessions are listed by timestamp + first message. For long-running projects or multiple concurrent threads, run `/rename {descriptive-name}` to give the session a findable name (e.g., `oauth-migration`, `debugging-memory-leak`). Named sessions surface by name in `claude --resume` pickers.
```

---

### Step 4: Tracker bookkeeping

Update `template-upgrade-2026-04.md`:

**4a. Status line:**
- Replace: `**Status:** Phase 4 — FB-015 primary landed in dashboard-regeneration.md (FB-015 complete pending health-check secondary); remaining direct items next`
- With: `**Status:** Phase 4 — session-management.md group implemented (FB-023 + FB-024 + FB-025); remaining direct items next`

**4b. Current State block:** add new bullet after the most recent `FB-015 primary implemented` bullet:

```
- **session-management.md group implemented 2026-04-17:** Three session-management tools documented in `.claude/rules/session-management.md`: `/btw` bullet added to § "Managing Context Pressure" (FB-023); new `## Checkpointing and Rewind` section after § "What Survives What" covering `Esc+Esc`/`/rewind` with conversation/code/both restore options (FB-024); `/rename` paragraph after the § "Resuming Sessions" table covering named-session discovery in `claude --resume` (FB-025). All three bundled in one commit per the file-grouping rule.
```

**4c. Next action bullet:** Update to suggest the next batch (iterate or agents).

**4d. Phase 4 Hot files block:** flip the session-management.md line:
- Replace: `- [ ] **\`.claude/rules/session-management.md\`** — FB-023 (\`/btw\`), FB-024 (\`/rewind\`/Esc+Esc), FB-025 (\`/rename\`). Single bundled edit.`
- With: `- [x] **\`.claude/rules/session-management.md\`** — FB-023 (\`/btw\` bullet), FB-024 (Checkpointing and Rewind section), FB-025 (\`/rename\` paragraph). Implemented 2026-04-17.`

**4e. File Collision Map:** in the `rules/session-management.md` row, strike-through the Best-prac column:
- `FB-023 \`/btw\`; FB-024 \`/rewind\`; FB-025 \`/rename\`` → `~~FB-023 \`/btw\`~~ ✓; ~~FB-024 \`/rewind\`/Esc+Esc~~ ✓; ~~FB-025 \`/rename\`~~ ✓`

**4f. Cleanup Manifest:** add row for this plan file:
```
| `plan-session-management-batch.md` | DELETE-AFTER | rules/session-management.md group (FB-023/024/025) implementation plan for fresh-session execution |
```

**4g. Session Log:** append entry:

```markdown
### 2026-04-17 — Phase 4: session-management.md group (FB-023 + FB-024 + FB-025)

**Done:**
- **FB-023 (`/btw`):** New bullet added to `§ "Managing Context Pressure"` explaining `/btw` as a dismissible-overlay side-question tool that doesn't enter conversation history.
- **FB-024 (Checkpointing):** New `## Checkpointing and Rewind` section added after `§ "What Survives What"` covering `Esc+Esc` / `/rewind` flow, three restore modes (conversation / code / both), cross-session persistence, and relationship to `/work pause` (complementary, not overlapping).
- **FB-025 (`/rename`):** New paragraph after the Resuming Sessions table covering `/rename {name}` for findable sessions in `claude --resume`.
- Tracker bookkeeping: status line, Current State, Phase 4 Hot files `[x]`, File Collision Map strikes, Cleanup Manifest row, Session Log entry.
- Pre-commit hook: `rules/session-management.md` is sync-category — hook will warn about version.json (expected).

**Judgment calls:**
- Chose bullet placement for FB-023 between `/clear` and "CLAUDE.md and rules files" rather than at the end of the list — groups with the other slash-command context tools (/compact, /clear) rather than the passive survival mechanisms.
- FB-024 as a new section rather than a bullet in "What Survives What" — it's a recovery mechanism, not a survival matrix entry. Different shape.
- FB-025 as a short paragraph after the resume table rather than a new row in the table — the table columns (Method / What you get / When to use) don't fit `/rename` (which isn't a resume method but a naming-for-findability). Paragraph reads better.

**Next:** Erik chooses the next Phase 4 unit. Strong candidates: `commands/iterate.md` group (FB-021 + FB-032); `rules/agents.md` + `implement-agent.md` group (FB-022 + FB-034 + FB-035 + FB-031).

**Open questions for later:**
- Whether to cross-reference the new Checkpointing section from the "Which Persistence Mechanism When" table (checkpoints could be a fourth row). Deferred — would require re-architecting the table; current 3-mechanism framing is cleaner. Revisit if users confuse checkpoints with handoff.
```

---

### Step 5: Commit

Single commit. Pre-commit hook warns about `version.json` (`rules/session-management.md` is sync-category); commit anyway.

Commit message (HEREDOC):

```
Phase 4: rules/session-management.md group — FB-023 + FB-024 + FB-025

Adds three session-management tool descriptions from the Claude Code
best-practices doc to the template's session-management rules file.
All three tools existed in the harness but were undocumented in the
template.

FB-023: new bullet in § "Managing Context Pressure" covering /btw
- /btw {question} — dismissible-overlay side question that does NOT
  enter conversation history. Useful for checking syntax / quick
  lookups mid-work without bloating context.

FB-024: new § "Checkpointing and Rewind" section after § "What
Survives What" covering Esc+Esc / /rewind.
- Every Claude action creates a checkpoint
- Rewind menu offers conversation-only / code-only / both
- Checkpoints persist across sessions
- Complementary to /work pause: handoff for planned wind-down,
  checkpoints for recovery from missteps

FB-025: /rename paragraph after the Resuming Sessions table
- /rename {name} gives sessions findable names for claude --resume
- Useful for long-running projects or multiple concurrent threads

Pure documentation, no behavior change. Single-file bundled edit
per the File Collision Map's hot-files rule.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Verification Checklist (post-edit, pre-commit)

- [ ] `rules/session-management.md § "Managing Context Pressure"` has a new `/btw` bullet between `/clear` and "CLAUDE.md and rules files"
- [ ] `rules/session-management.md` has a new `## Checkpointing and Rewind` section with `Esc+Esc` / `/rewind` / three restore modes / cross-session persistence / relationship to `/work pause`
- [ ] `rules/session-management.md § "Resuming Sessions"` has a `/rename` paragraph after the resume-methods table
- [ ] No other files modified
- [ ] Tracker: status line, Current State, Phase 4 hot files `[x]`, File Collision Map strikes, Cleanup Manifest row, Session Log entry
- [ ] Pre-commit hook output shows `version.json` warning (expected)

---

## What NOT to Do

- **Don't** touch any file besides `rules/session-management.md` and `template-upgrade-2026-04.md`.
- **Don't** restructure the existing sections — all three edits are additive.
- **Don't** add `/btw`, `/rewind`, or `/rename` to the top-level "Environment Commands" table in `.claude/CLAUDE.md` — those are project-scoped workflow commands (`/work`, `/iterate`, etc.). The harness-level slash commands stay in session-management rules.
- **Don't** add behavior changes — purely doc additions.
- **Don't** bump `.claude/version.json` — Phase 5 handles scope.
- **Don't** archive FB-023/024/025 in `feedback.md` — same convention as prior direct-implementation items.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Target file | `.claude/rules/session-management.md` |
| Tracker | `template-upgrade-2026-04.md` (root) |
| Source feedback items | `.claude/support/feedback/feedback.md` (FB-023 line 99, FB-024 line 113, FB-025 line 127) |
