# DEC-005 Implementation Plan — Layered Settings (Option E)

**Purpose:** Execute DEC-005 Option E across ~6 files. Ship a template-owned `.claude/settings.json` containing only a base `permissions.allow` set; keep `.claude/settings.local.json` as the sole user-owned settings file; rely on Claude Code's runtime merge to concatenate the two. A fresh session can read this plan and execute without re-deriving context.

**Status:** Ready to execute
**Created:** 2026-04-17
**Upstream:** Template upgrade tracker `template-upgrade-2026-04.md`, Phase 1
**Cleanup tag:** DELETE-AFTER (tracked in upgrade tracker's Cleanup Manifest)

---

## Context to Load Before Executing

Read these in order at session start:

1. `template-upgrade-2026-04.md` — upgrade phase state
2. `decisions/decision-005-base-allowedtools-shipping-policy.md` — decision + full research
3. Current state of the 5 target files listed in Per-File Change Specs (+ the new `settings.json` to create)

Then execute this plan.

---

## Approved Context

### The decision (locked)

DEC-005 Option E: **Ship base set as fully template-owned `.claude/settings.json`; require user additions in `.claude/settings.local.json`** (layered).

### Why Option E works (verified research, still current)

- Claude Code concatenates `permissions.allow[]` across settings layers at runtime (managed → CLI → local → project → user). This is documented platform behavior, not a workaround.
- No merge logic needed in `/health-check` — two separate files, each with an unambiguous owner.
- No new `sync-manifest.json` category needed — `settings.json` slots into existing `sync`; `settings.local.json` stays in `ignore` (gitignored; user-owned).
- Tightening works trivially: template removes an entry, sync replaces the file, user's local entries stay.

### Approved judgment calls (implicit in option selection)

1. **Team-shared permissions:** per-developer customization via `settings.local.json` is acceptable. A future project-level extension (e.g., `settings.project.json`) is out of scope.
2. **"Edit-the-wrong-file" failure mode:** acceptable with a clear `/health-check` warning directing the user to move custom entries to `settings.local.json`.
3. **Base set scope:** 15 universally safe, read-only/local-inspecting Bash commands (per research Q1). Write operations, language runners, network access, and any `WebSearch` / `WebFetch` stay user-opt-in in `settings.local.json`.

---

## Design Contract — Shipped Base Set

The template ships `.claude/settings.json` with exactly this shape. It contains **only** `permissions.allow`. No hooks, no env vars, no theme — those stay user-owned in `settings.local.json`.

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

**Rationale for each entry:** all are read-only or strictly local-inspecting. None modify the filesystem beyond temporary test scaffolding (`test`), none make network requests, none execute foreign code. This is the smallest set that eliminates the most common acceptEdits-mode permission prompts.

**Deliberately excluded from base (user opts in via `settings.local.json`):**
- Write-class git (`git add`, `commit`, `push`, `rm`, `checkout`, `init`)
- Language runners (`python3`, `npm`, `node`, `cargo`, `go`)
- Filesystem writes (`chmod`, `unzip`, `mkdir`, `mv`, `cp`, `rm`)
- Network (`WebSearch`, `WebFetch`, `curl`, `wget`)

---

## Per-File Change Specs

### File 1: `.claude/settings.json` (NEW)

**Editing strategy:** `Write` tool to create. Content exactly as shown in the Design Contract above. No leading/trailing whitespace in the JSON, 2-space indentation, trailing newline.

**Verify after creation:** file parses as valid JSON; contains exactly the `permissions.allow` key and nothing else.

---

### File 2: `.claude/sync-manifest.json`

**Editing strategy:** Targeted `Edit`. Two changes:

1. Add `".claude/settings.json"` to the `sync` array — place alphabetically near `.claude/CLAUDE.md` (the template-owned config siblings sit together for scannability). Suggested position: immediately after `.claude/CLAUDE.md`.
2. Confirm `.claude/settings.local.json` remains in the `ignore` array (it already is — no change needed, just verify).
3. Update the `notes` field (last key) to clarify the layered settings pattern. New notes value:
   > "Paths relative to template root. Use glob patterns. User-created rule files (project-*.md) and reference docs (project-*.md) are ignored by sync. The settings file is layered: `.claude/settings.json` is template-owned (in `sync`) and contains only the base `permissions.allow`; `.claude/settings.local.json` is user-owned (in `ignore`) and holds user additions, hooks, env vars, and theme. Claude Code merges both layers at runtime."

---

### File 3: `.claude/commands/health-check.md` — Part 5c

**Editing strategy:** Full rewrite of Part 5c (Settings Conflict Detection) via targeted `Edit`. Part 5 narrative stays the same — `settings.json` is already covered by the generic sync-category flow once it's in `sync-manifest.json`.

**Replace** the current Part 5c body (lines 571-580) with:

```markdown
## Part 5c: Settings Boundary Validation

Validates the layered-settings contract: `.claude/settings.json` is template-owned (base `permissions.allow` only); `.claude/settings.local.json` is user-owned (all user additions, hooks, env vars, theme). Enforcing the boundary prevents template sync from silently clobbering user edits.

### Process

1. **Check for presence:**
   - If `.claude/settings.json` is missing: informational only (will be created by next template sync).
   - If `.claude/settings.local.json` is missing: informational only (user has no overrides yet — fine).

2. **Validate template-owned `settings.json` scope:**
   - Parse `.claude/settings.json` as JSON.
   - If parse fails: ❌ error — "`.claude/settings.json` is not valid JSON. Sync may have been interrupted; re-run `/health-check` to re-sync."
   - Check that the file contains **only** `permissions.allow`:
     - ✅ Pass: the top-level object has exactly one key (`permissions`) whose value has exactly one key (`allow`).
     - ⚠️ Warn if any of the following are present: `permissions.deny`, `permissions.ask`, `hooks`, `env`, `theme`, or any other top-level key.
     - Warning message:
       ```
       ⚠️ Found non-base entries in `.claude/settings.json` (template-owned file).
          Unexpected keys: {list}
          These will be overwritten on next template sync.
          Move them to `.claude/settings.local.json` to preserve them.
          [M] Move automatically  [S] Skip (accept overwrite on next sync)
       ```
     - On `[M]`: merge the unexpected entries into `.claude/settings.local.json` (create if missing, concatenate+dedupe for array fields like `permissions.allow`, preserve existing keys for object fields like `hooks`), then strip them from `.claude/settings.json`. On `[S]`: leave files as-is; next sync will overwrite.

3. **Validate base-set drift (template vs. local):**
   - Read the template's `.claude/settings.json` from the template remote (if configured and reachable — same fetch as Part 5). Skip this check if offline.
   - Compare the local `permissions.allow` array against the template's.
   - If entries differ: this is normal (user has not yet synced, or template has been updated). Part 5's sync flow will offer the update — no Part 5c action needed.
   - This check exists purely to reassure users that additions/removals from the template base will propagate through normal sync.

4. **Report:**
   - Pass: `✓ Settings layer valid (template-owned base + user-owned local)`
   - Warnings: emit the warning block from step 2 above.

### Rationale

Claude Code's runtime concatenates `permissions.allow[]` across all settings layers, so the user's additions in `settings.local.json` combine automatically with the template's base in `settings.json`. The template-owned file exists for one job only: shipping a conservative base set. Everything else belongs in the user-owned file.
```

**Also update** the "Part 5 bullet summary" if present near the end of the file. Search for `Part 5c: Settings` or `Settings Conflict Detection` references and update to `Settings Boundary Validation`.

---

### File 4: `.claude/CLAUDE.md`

**Editing strategy:** Targeted `Edit`. One small addition to the "Critical Invariants" section.

**Replace** the existing "Critical Invariants" block (currently 7 bullets) with the same 7 bullets plus a new 8th:

> - Settings layering: `.claude/settings.json` is template-owned (base `permissions.allow` only); put hooks, env vars, theme, and any additional permissions in `.claude/settings.local.json`. Claude Code merges both at runtime.

Place this new bullet immediately after "Never create working documents in the project root — use `.claude/support/workspace/`."

No other changes to `.claude/CLAUDE.md`.

---

### File 5: `system-overview.md`

**Editing strategy:** Three targeted `Edit` calls.

**Edit 1 — Pending Template Decisions (line ~24):** remove the DEC-005 bullet since the decision is now being implemented and its conclusions land in this commit. After removal, the Pending Template Decisions list should contain only the DEC-004 and DEC-006 bullets (DEC-004 will be removed when its decision file is cleaned up in Phase 5; removing the DEC-005 bullet now is correct because Phase 5 cleanup deletes the decision file for the same reason).

   **Before:**
   ```
   - **Subagent capability contract** — whether subagents spawned by `/work` own task state transitions (implement-agent Steps 6a/6b) or the orchestrator does. Relates to FB-010.
   - **Base `allowedTools` shipping policy** — whether the template ships `.claude/settings.json` with a base `allowedTools` set, and what merge strategy `/health-check` uses. Relates to FB-012.
   - **Phase gate flexibility** — how to let long-running human-owned tasks cross phase boundaries without breaking the software-domain invariant. Relates to FB-013.
   ```

   **After:**
   ```
   - **Subagent capability contract** — whether subagents spawned by `/work` own task state transitions (implement-agent Steps 6a/6b) or the orchestrator does. Relates to FB-010.
   - **Phase gate flexibility** — how to let long-running human-owned tasks cross phase boundaries without breaking the software-domain invariant. Relates to FB-013.
   ```

   (The DEC-004 bullet reads as stale too — that decision was resolved in commit `c5805b8`. Leave it for now; it gets removed alongside the DEC-004 decision file in Phase 5 cleanup per the existing rule at the bottom of this section. Do not change it in this commit.)

**Edit 2 — File Map table (line ~638):** update the `.claude/settings.local.json` row and add a new row for `.claude/settings.json`.

   **Before:**
   ```
   | `.claude/settings.local.json` | Pre-approved Bash permissions for Claude Code | Template (user-customizable) |
   ```

   **After (two rows — put the template-owned row first for alphabetical parity with the source of truth):**
   ```
   | `.claude/settings.json` | Template-owned base `permissions.allow` — shipped read-only set | Template (sync) |
   | `.claude/settings.local.json` | User-owned settings — additional permissions, hooks, env, theme; merges with base at runtime | User |
   ```

**Edit 3 — Instruction Architecture section (if it references settings):** search for any mention of `settings.json` or `settings.local.json` in the "Instruction Architecture (CLAUDE.md, Rules, Ownership)" section. If found, add a single parenthetical clarifying the layering. If not found, no edit needed.

---

### File 6: `.claude/README.md`

**Editing strategy:** Targeted `Edit`. Add settings to the "File Ownership" section.

**In "Template-owned"** list, add:
- `.claude/settings.json` (base `permissions.allow` — never edit; template sync replaces it)

**In "Project-owned"** list, add:
- `.claude/settings.local.json` (your permission additions, hooks, env vars, theme)

**Also add** a short new paragraph at the end of the "File Ownership" section (or as a new "## Settings" subsection just after File Ownership):

> ### Settings
>
> Claude Code reads permissions, hooks, and theme from two files that merge at runtime:
>
> - **`.claude/settings.json`** — template-owned. Ships a conservative base `permissions.allow` set (safe read-only git/filesystem commands) that eliminates the most common acceptEdits permission prompts. Updated via template sync. **Don't edit this file.**
> - **`.claude/settings.local.json`** — yours. Add additional permissions (language runners, write-class git, anything project-specific), hooks, env vars, and theme here. Claude Code concatenates `permissions.allow` across both files automatically.
>
> If you accidentally add permissions to `.claude/settings.json`, `/health-check` will warn you and offer to move them to `.claude/settings.local.json`.

---

## Execution Order

Recommended order (File 1 must come before File 2; Files 3–6 are independent once File 1 exists):

1. **Read** DEC-005, tracker, current state of Files 2–6, and `.claude/settings.local.json` for reference
2. **File 1** (`.claude/settings.json`) — create via `Write`
3. **File 2** (`sync-manifest.json`) — add to `sync` category + update notes
4. **File 3** (`health-check.md`) — rewrite Part 5c
5. **File 4** (`.claude/CLAUDE.md`) — add Critical Invariant bullet
6. **File 5** (`system-overview.md`) — remove Pending Decisions bullet + update File Map table
7. **File 6** (`.claude/README.md`) — add to File Ownership + new Settings subsection
8. **Verify:** parse `.claude/settings.json` as JSON; parse `sync-manifest.json`; grep for "Settings Conflict Detection" to confirm old name is gone from active docs; confirm the DEC-005 Pending bullet is gone from system-overview.md
9. **Update tracker:** Session Log entry, Current State → DEC-006 next, mark DEC-005 checkbox done, strike DEC-005 column entries in File Collision Map
10. **Commit:** see commit message below

---

## Verification Checklist (Post-Execution)

Before commit, confirm:

- [ ] `.claude/settings.json` exists, is valid JSON, contains exactly `permissions.allow` with the 15-entry base set
- [ ] `.claude/sync-manifest.json` lists `.claude/settings.json` in `sync`, keeps `.claude/settings.local.json` in `ignore`; notes field updated
- [ ] `health-check.md` Part 5c is rewritten as "Settings Boundary Validation" with scope-check logic and `[M]`/`[S]` prompt
- [ ] `.claude/CLAUDE.md` has the new 8th Critical Invariants bullet about settings layering
- [ ] `system-overview.md` Pending Template Decisions list no longer contains the DEC-005 bullet
- [ ] `system-overview.md` File Map has two rows for settings (template-owned + user-owned)
- [ ] `.claude/README.md` File Ownership and new Settings subsection reflect the two-file model
- [ ] No lingering references to "template doesn't ship settings files" in active docs (check `health-check.md`, `CLAUDE.md`, `README.md`, `system-overview.md`)
- [ ] `.claude/settings.local.json` (template's own) is unchanged — that's user-local and not in this commit's scope
- [ ] Pre-commit hook warning about version.json is expected — version bump deferred to Phase 5

---

## Commit Message

```
DEC-005: ship template-owned settings.json with base permissions.allow

Per Option E (layered two-file model), the template now ships
`.claude/settings.json` containing a conservative base `permissions.allow`
set (15 read-only/local-inspecting entries). User additions — extra
permissions, hooks, env vars, theme — stay in `.claude/settings.local.json`
(gitignored, user-owned). Claude Code concatenates `permissions.allow[]`
across settings layers at runtime, so no merge logic is needed in the
template.

Rationale: eliminates the common acceptEdits permission prompts for safe
read-only commands (git status/diff/log, ls, grep, find, etc.) without
clobbering user-specific additions. Tightening the base set works
trivially via normal template sync. Option A's drift problem is avoided;
Option B's origin-tracking sidecar is avoided; Option C's clobber
behavior is avoided.

Closes FB-012.

Changes:
- .claude/settings.json (new): base permissions.allow set
- .claude/sync-manifest.json: add settings.json to sync category, update notes
- .claude/commands/health-check.md: Part 5c rewritten as boundary validation
- .claude/CLAUDE.md: new Critical Invariants bullet on settings layering
- system-overview.md: remove DEC-005 from pending decisions; File Map updated
- .claude/README.md: File Ownership + new Settings subsection

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Post-Execution Tracker Updates

After successful commit:

1. Update `template-upgrade-2026-04.md`:
   - Add Session Log entry for DEC-005 execution
   - Update Current State → "Phase 1 — DEC-006 next"
   - Mark DEC-005 checkbox in Phase 1 as `[x]` with commit SHA
   - Update File Collision Map: strike through DEC-005 column entries (done)
2. Confirm this plan file is already in the Cleanup Manifest as DELETE-AFTER (add the entry if missing)
