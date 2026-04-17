# Plan — DEC-008 Option D Implementation

**Purpose:** Implement DEC-008 Option D — narrow `.claude/settings.json` from 15 to 8 entries and add auto-mode documentation to `.claude/README.md`. Preserves DEC-005's layered two-file model.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Upstream decision:** `decisions/decision-008-auto-mode-permissions-reevaluation.md` (approved 2026-04-17, Option D)
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in the same commit as this plan)
**Tracker status line to advance:** "Phase 4 — DEC-007 Option B implemented; DEC-008 Option D and remaining direct items next" → "Phase 4 — DEC-007 + DEC-008 implemented; remaining direct items next"

---

## Context to Load Before Executing

Read in this order at session start:

1. **`decisions/decision-008-auto-mode-permissions-reevaluation.md`** — the approved decision. Read the frontmatter (confirm `status: approved`, `decided: 2026-04-17`), the `## Select an Option` block (confirm `[x] Option D`), the `### Option D: Narrow AND document auto mode as recommended primary` section, and `### Q5: DEC-005 entry-by-entry redundancy analysis` table. The 15→8 narrowing rationale lives in Q5.

2. **`template-upgrade-2026-04.md`** — read the Current State block + the latest Session Log entry (2026-04-17 Phase 4: DEC-007 Option B). The Phase 4 section has a "DEC-008 implementation" sub-checklist with the exact items to tick off after executing this plan.

3. **`.claude/settings.json`** — current state captured below (15 entries). The file is small; Read it at session start to confirm the current entry set matches this plan's assumption before editing.

4. **`.claude/README.md`** — current `### Settings` subsection exists (lines roughly 67-76 — grep for `### Settings` to locate exactly). The new `### Auto Mode` subsection inserts immediately after it, before `### Skills`.

5. **`.claude/CLAUDE.md`** — `## Critical Invariants` section has 8 bullets; the settings bullet is the 8th. Exact current text captured in Step 3 below.

6. **`.claude/commands/health-check.md` Part 5c** — verified during planning (grepped on 2026-04-17): wording is entry-count-agnostic. No edit needed. Re-verify at execution time by Grep; adjust only if wording drifted.

Auto-memory: no specific entry is load-bearing for this plan beyond what's already baked in.

---

## Implementation Steps

### Step 1: Narrow `.claude/settings.json`

Current state (15 entries, as of 2026-04-17 planning time):

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git branch:*)",
      "Bash(git check-ignore:*)",
      "Bash(git ls-tree:*)",
      "Bash(ls:*)",
      "Bash(tree:*)",
      "Bash(wc:*)",
      "Bash(head:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(test:*)",
      "Bash(sort:*)",
      "Bash(shasum:*)"
    ]
  }
}
```

**Target state (8 entries, per DEC-008 Research Finding Q5 keep-set):**

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(ls:*)",
      "Bash(grep:*)",
      "Bash(test:*)",
      "Bash(head:*)",
      "Bash(wc:*)"
    ]
  }
}
```

**Dropped 7 entries (with one-line rationale from Q5):**
- `Bash(git branch:*)` — low hook/CI usage; classifier covers read-only case
- `Bash(git check-ignore:*)` — specialized, rarely used
- `Bash(git ls-tree:*)` — specialized, rarely used
- `Bash(tree:*)` — covered by `ls -R` or the classifier
- `Bash(find:*)` — Glob tool preferred for file discovery
- `Bash(sort:*)` — pipe-side utility, low frequency
- `Bash(shasum:*)` — specialized, rarely used outside specific flows

**Implementation:** Write the new JSON. Preserve the exact outer `{ "permissions": { "allow": [...] } }` structure. Order the kept entries as in the target block above (git triplet first, then common utilities in descending frequency).

### Step 2: Add `### Auto Mode` subsection to `.claude/README.md`

Locate the existing `### Settings` subsection (grep `^### Settings` in `.claude/README.md`). The subsection ends with the paragraph:

> "If you accidentally add permissions to `.claude/settings.json`, `/health-check` will warn you and offer to move them to `.claude/settings.local.json`."

Immediately after that paragraph (before `### Skills`), insert the following exact content:

```markdown
### Auto Mode

Claude Code supports a `--permission-mode auto` flag (available on Max, Team, Enterprise, and API plans with Opus 4.7). In auto mode, a classifier model approves safe tool calls at runtime without prompting — read-only operations, file edits inside the working directory, and lock-file-driven dependency installs pass through; potentially destructive actions (force push to main, mass cloud deletions, `curl | bash`, IAM grants) are blocked.

**Composition with `permissions.allow`:**

- Rules in `.claude/settings.json` and `.claude/settings.local.json` are evaluated **before** the classifier. An explicit `allow` rule short-circuits the classifier entirely, saving a server round-trip and the token cost of classifier review.
- Broad rules like `Bash(*)` are dropped when auto mode activates; narrow rules like the template's `Bash(git status:*)` carry through.
- Classifier coverage overlaps substantially with the template's base allowlist, but the allowlist remains useful for: hot paths (repeated read-only operations), hooks (which don't get classifier intelligence), and `dontAsk` / CI contexts (where auto mode isn't available).

**Recommended setup for Max + Opus 4.7:** enable auto mode for interactive sessions (`claude --permission-mode auto`, or persist via `settings.local.json`) and keep the template's base `permissions.allow` for latency-sensitive paths and hook compatibility. Users on Pro plans, on Sonnet/Haiku, or in `dontAsk` / CI contexts should extend the base allowlist in `settings.local.json` as needed — auto mode is not available there.

See Claude Code's permission-modes documentation (`https://code.claude.com/docs/en/permission-modes`) for full classifier behavior, fallback conditions, and plan availability.
```

Leave a blank line between this new subsection and the `### Skills` heading below.

### Step 3: Update Critical Invariants bullet in `.claude/CLAUDE.md`

Current bullet 8 (verbatim — confirm by Read before editing):

```
- Settings layering: `.claude/settings.json` is template-owned (base `permissions.allow` only); put hooks, env vars, theme, and any additional permissions in `.claude/settings.local.json`. Claude Code merges both at runtime.
```

Replace with:

```
- Settings layering: `.claude/settings.json` is template-owned (base `permissions.allow` only); put hooks, env vars, theme, and any additional permissions in `.claude/settings.local.json`. Claude Code merges both at runtime. Under `--permission-mode auto`, these rules short-circuit the runtime classifier — see `.claude/README.md` § Auto Mode for composition.
```

Only that bullet changes; do not touch the rest of the Critical Invariants list.

### Step 4: Verify `commands/health-check.md` Part 5c (no edit expected)

Read `.claude/commands/health-check.md` § Part 5c. Confirm the wording:

- Does **not** reference a specific entry count (e.g., "15 entries")
- Does **not** list specific dropped entries
- Describes the boundary contract in entry-count-agnostic terms

If all three hold: skip edit. If any reference is found: remove or reword to stay entry-agnostic. (During planning, wording was verified entry-agnostic, so no edit is expected.)

### Step 5: Tracker bookkeeping

Update `template-upgrade-2026-04.md`:

**5a. Status line** (top of file):

- Replace `**Status:** Phase 4 — DEC-007 Option B implemented (skills trial live); DEC-008 Option D and remaining direct items next`
- With: `**Status:** Phase 4 — DEC-007 + DEC-008 implemented; remaining direct items next (hot-file batches)`

**5b. Current State block:** replace the DEC-008 Option D pending-implementation paragraph with a "DEC-008 Option D implemented 2026-04-17" paragraph that lists what changed (settings.json narrowed, README auto-mode section added, CLAUDE.md invariant refreshed, Part 5c verified unchanged). Parallel structure to the existing DEC-007 paragraph. Advance **Next action** to: "remaining Phase 4 hot-file batches or FB-037 implementation (now unblocked)".

**5c. Phase 4 DEC-008 checklist** (lines that read "DEC-008 implementation (Option D — narrow allowlist + document auto mode):"): check `[x]` for:
- `.claude/settings.json` — narrow from 15 to 8 entries
- `.claude/README.md` — auto-mode subsection
- `.claude/CLAUDE.md` — Settings invariant wording
- `commands/health-check.md` Part 5c — verify (no edit needed, confirmed)
- Unblocks FB-037 (keep as checkbox; the unblock already happened at Phase 3 close, but the formal implementation closure lives here)

**5d. Session Log:** append a new entry at the bottom:

```markdown
### 2026-04-17 — Phase 4: DEC-008 Option D implementation

**Done:**
- Narrowed `.claude/settings.json` from 15 to 8 entries per DEC-008 Q5 analysis. Kept: `git status`, `git log`, `git diff`, `ls`, `grep`, `test`, `head`, `wc`. Dropped: `git branch`, `git check-ignore`, `git ls-tree`, `tree`, `find`, `sort`, `shasum`.
- Added `### Auto Mode` subsection to `.claude/README.md` between the existing `### Settings` and `### Skills` subsections. Explains classifier behavior, composition with `permissions.allow` (rules short-circuit classifier; broad rules dropped; narrow rules persist), and recommended setup for Max + Opus 4.7 vs Pro/Sonnet/Haiku vs dontAsk/CI contexts.
- Appended an auto-mode composition reference to the Settings Critical Invariant bullet in `.claude/CLAUDE.md`.
- Verified `commands/health-check.md` Part 5c wording remains accurate — entry-agnostic contract language; no edit needed.
- Pre-commit hook warned about `version.json` not being bumped (expected; version bump deferred to Phase 5 cleanup per tracker policy).

**Next:** Phase 4 continues with remaining direct items. Suggested ordering: FB-037 (now unblocked — optional PreToolUse hook recipe in `setup-checklist.md`) is a natural follow-on since the auto-mode section just written is its documentation neighbor. Alternative: hot-file batches starting with `commands/work.md` (FB-015 + FB-017 + FB-027 + FB-036).

**Open questions for later:** None blocking. Version bump tallies now include DEC-007 Option B + DEC-008 Option D — still deferred to Phase 5.
```

### Step 6: Commit

Commit message (use HEREDOC per existing convention):

```
Phase 4: DEC-008 Option D — narrow settings.json to 8 entries + document auto mode

Implements DEC-008 Option D (approved 2026-04-17). DEC-005's layered two-file
model is preserved — only the entry count of the template-owned
permissions.allow shrinks, and auto-mode documentation is added so users know
about the platform capability that composes with the allowlist.

.claude/settings.json:
- Narrow from 15 entries to 8
- Dropped: git branch, git check-ignore, git ls-tree, tree, find, sort, shasum
- Kept: git status, git log, git diff, ls, grep, test, head, wc
- Each kept entry has hook/CI usage, verify-agent common path, or
  high-frequency interactive use (per DEC-008 Research Finding Q5).
- Dropped entries are covered by the auto-mode classifier, redundant with
  dedicated tools (Glob replaces find), or rarely used (shasum, sort, tree).

.claude/README.md: new "### Auto Mode" subsection between Settings and Skills.
Explains classifier behavior, composition with permissions.allow (rules
short-circuit classifier; broad rules dropped in auto mode; narrow rules
persist), and recommended setup across Max + Opus 4.7, Pro/Sonnet/Haiku, and
dontAsk/CI contexts.

.claude/CLAUDE.md Critical Invariants bullet 8: appended an auto-mode
composition reference pointing to the new README section.

.claude/commands/health-check.md Part 5c: verified wording is entry-count
agnostic — no edit needed.

Unblocks FB-037 (optional PreToolUse hook recipe in setup-checklist.md). The
layered model is confirmed preserved, so the hook recipe will reference
.claude/settings.local.json under the hooks key as originally assessed.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

Pre-commit hook will warn about `version.json` not being bumped (`settings.json` is a sync-category file). Expected. Commit anyway — version bump deferred to Phase 5 cleanup per existing tracker policy, matching prior DEC-005/006/007 commits.

---

## Verification Checklist (post-edit, pre-commit)

- [ ] `.claude/settings.json` parses as JSON (`python3 -c "import json;json.load(open('.claude/settings.json'))"` exits 0)
- [ ] `.claude/settings.json` `permissions.allow` has exactly 8 entries
- [ ] Grep confirms absence of dropped entries in `.claude/settings.json`: `git branch`, `git check-ignore`, `git ls-tree`, `tree`, `find`, `sort`, `shasum`
- [ ] Kept entries present: `git status`, `git log`, `git diff`, `ls`, `grep`, `test`, `head`, `wc`
- [ ] `.claude/README.md` has a new `### Auto Mode` heading between `### Settings` and `### Skills` (grep confirms order)
- [ ] New subsection mentions: Max/Team/Enterprise/API plan + Opus 4.7 availability, composition with `permissions.allow`, three-way recommended setup (Max+Opus / Pro+Sonnet+Haiku / dontAsk+CI)
- [ ] `.claude/CLAUDE.md` bullet 8 now ends with the `--permission-mode auto` composition sentence referencing `.claude/README.md § Auto Mode`
- [ ] `commands/health-check.md` Part 5c still parses without entry-count references (grep verifies)
- [ ] Tracker Current State and Status line advanced
- [ ] Tracker DEC-008 checklist items `[x]`
- [ ] Tracker Session Log entry appended
- [ ] Pre-commit hook output shows version.json warning (expected — not an error)

---

## What NOT to Do

- **Don't** delete `.claude/settings.json` — Option D preserves the layered model; Option A was "full reversal" and was explicitly not selected.
- **Don't** add hook recipes or hook scaffolding. FB-037 is the item that does that; this commit only enables it.
- **Don't** touch `.claude/settings.local.json` — user-owned, gitignored. This plan only edits template-owned files.
- **Don't** bump `.claude/version.json` — Phase 5 cleanup handles version-bump scope once total change tally is known. The pre-commit warning is informational, not blocking.
- **Don't** update command or rule citation sites. No command or rule references specific allowlist entries; only the layering contract. Grep first to confirm if unsure (e.g., `grep -rn "shasum\|ls-tree" .claude/commands .claude/rules`).
- **Don't** update `system-overview.md` File Map — the two settings files are listed there, and ownership doesn't change.
- **Don't** modify `.claude/sync-manifest.json` — `.claude/settings.json` is already in the `sync` category, and its category doesn't change.
- **Don't** rewrite the `### Settings` subsection that already exists. The new `### Auto Mode` sits alongside it; the existing wording is still accurate.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Tracker | `template-upgrade-2026-04.md` (root) |
| Decision record (approved) | `decisions/decision-008-auto-mode-permissions-reevaluation.md` (root) |
| Related decision (preserved) | `decisions/decision-005-base-allowedtools-shipping-policy.md` (root) |
| Target: settings | `.claude/settings.json` |
| Target: README | `.claude/README.md` |
| Target: CLAUDE | `.claude/CLAUDE.md` |
| Verify-only: health-check | `.claude/commands/health-check.md` § Part 5c |
| Blocked feedback (will unblock) | `.claude/support/feedback/feedback.md` § FB-037 |

---

## Post-Commit: What Happens Next

After commit:
- FB-037 is formally unblocked (its Assessed line was already updated at Phase 3 close, but the DEC-008 implementation closes the dependency in practice).
- Erik chooses the next Phase 4 unit. Natural candidates:
  - **FB-037 implementation** — optional PreToolUse hook recipe in `setup-checklist.md`; lands adjacent to the auto-mode section just written; small scope.
  - **Hot-file batch: `commands/work.md`** — FB-015 (Action Required cleanup), FB-017 (Step 2b checkbox detection), FB-027 (skip-planning callout), FB-036 (pre-dispatch confirm). Four items, one file.
  - **Hot-file batch: `rules/session-management.md`** — FB-023/024/025 (`/btw`, `/rewind`, `/rename`) as a single bundled edit.
- Do not pick autonomously — ask Erik.
