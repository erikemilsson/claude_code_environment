# Plan — FB-028: CLI-tool installation hints in `setup-checklist.md`

**Purpose:** Add a spec-signal → CLI-tool hint check to the decomposition-time setup checklist, so users are warned when their spec implies an external integration whose CLI isn't installed. Single-file edit; additive scope.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Source feedback item:** FB-028 (line 154) in `.claude/support/feedback/feedback.md`
**Related decision:** none — direct-implementation FB item
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in same commit as this plan)
**Tracker status line to advance:** `Phase 4 — FB-028 implemented (CLI-tool hints in setup-checklist.md); FB-019 + FB-029/030 + FB-011 remaining (or update depending on ordering)`

---

## Scope

| Item | Touch site | Edit type |
|------|-----------|-----------|
| FB-028 | `.claude/support/reference/setup-checklist.md` between Check 3 and `## Output` | New `### 4. External CLI Tools` check + signal→CLI mapping table |

### Out of scope

- Actually running the CLI detection during `/work` Step 1 (decomposition). The checklist is advisory; the check wording tells Claude what to look for, but enforcement is Claude reading the checklist at decomposition time.
- Bundling install commands into a script. Signal → install-command table is a human-readable reference; users run installs themselves.
- Expanding to the full universe of CLIs (`docker`, `kubectl`, `terraform`, etc.). Start with the high-signal set from the best-practices source: `gh`, `aws`, `gcloud`, `sentry-cli`. Users can extend per project.
- Migrating the FB-037 Optional Hooks appendix — it stays separate. FB-028 and FB-037 share the file but not the section.

---

## Context to Load Before Executing

1. **`.claude/support/reference/setup-checklist.md`** — full file (~97 lines). New check lands between existing Check 3 (line 27) and `## Output` (line 41). The `## Optional Hooks` appendix (FB-037, starts line 53) stays untouched.
2. **`.claude/support/feedback/feedback.md`** lines 154–166 (FB-028) — confirm Assessed line hasn't drifted.
3. **`template-upgrade-2026-04.md`** — Current State + File Collision Map `support/reference/setup-checklist.md` row (Best-prac column currently lists `FB-028 CLI installs`).
4. **`.claude/spec_v1.md`** (optional — template placeholder spec) — only if you want to verify signal-detection vocabulary matches something the spec format allows. Not load-bearing.

Auto-memory: no specific entry is load-bearing.

---

## Implementation Steps

### Step 1: Add Check 4 — External CLI Tools

Locate `.claude/support/reference/setup-checklist.md` between Check 3's closing lines (line 39: `⚠ Warn: File missing or `template_repo` is empty`) and `## Output` (line 41).

Insert the following new check:

```markdown
### 4. External CLI Tools

Scan the spec and (if present) `./CLAUDE.md` for signals that the project integrates with external services. When a signal matches, check whether the corresponding CLI is on `PATH` — warn if missing.

| Spec signal (keywords, case-insensitive) | Recommended CLI | Install (macOS) | Install (Linux) |
|------------------------------------------|-----------------|-----------------|-----------------|
| `github`, `pull request`, `PR`, `gh issue`, `gh.com` | `gh` | `brew install gh` | `sudo apt install gh` or see cli.github.com |
| `aws`, `s3://`, `lambda`, `ec2`, `cloudformation` | `aws` | `brew install awscli` | `pip install awscli` or AWS installer |
| `gcp`, `google cloud`, `gcs://`, `cloud run`, `bigquery` | `gcloud` | `brew install --cask google-cloud-sdk` | see cloud.google.com/sdk/docs/install |
| `sentry`, `error tracking` (when release tagging is implied) | `sentry-cli` | `brew install getsentry/tools/sentry-cli` | `curl -sL https://sentry.io/get-cli/ \| bash` |
| `vercel deploy`, `vercel env`, `v0.dev` | `vercel` | `npm install -g vercel` | `npm install -g vercel` |
| `netlify deploy`, `netlify build` | `netlify` | `npm install -g netlify-cli` | `npm install -g netlify-cli` |

**How to check presence:** `command -v <cli> >/dev/null 2>&1` (shell-builtin, works in bash/zsh/sh). If the check returns non-zero for a matched signal, emit a warning row.

**Signal detection scope:** Read the spec's stated integrations, dependencies, and acceptance criteria. Do NOT infer from generic mentions — a spec that says "authenticate with GitHub OAuth" is a `gh` signal only if PR/issue/release operations are also in scope. When ambiguous, emit the warning anyway — a false positive here is cheaper than a mid-implementation friction.

✓ Pass: No external-service signals detected, OR all matched signals have their CLI on `PATH`
⚠ Warn: One or more matched signals missing a CLI — list each with the install command

**Why this check exists:** Authenticated CLI tools return structured data with fewer rate-limit issues than unauthenticated API calls. When spec work depends on (for example) reading GitHub issues or uploading to S3, having the CLI installed and authenticated at decomposition time prevents mid-implementation context loss from repeated unauthenticated failures.
```

---

### Step 2: Update the Output block to include the new check

Locate `## Output` (line 41). The sample output block currently shows only Checks 1–3:

```
Setup check:
  ✓ CLAUDE.md customized
  ⚠ version.json — file missing
```

Extend with a representative Check 4 line:

```
Setup check:
  ✓ CLAUDE.md customized
  ✓ Flat layout
  ⚠ version.json — file missing
  ⚠ CLI tools — `gh` missing (spec mentions GitHub PRs); install: brew install gh
```

Add one short sentence after the sample block:

```
CLI-tool warnings are advisory — decomposition proceeds. The user installs flagged tools when convenient.
```

---

### Step 3: Tracker bookkeeping

Update `template-upgrade-2026-04.md`:

**3a. Status line:** update to reflect FB-028 complete and what's remaining.

**3b. Current State:** add new bullet:

```
- **FB-028 implemented 2026-04-17:** `support/reference/setup-checklist.md` gained a new `### 4. External CLI Tools` check between Check 3 and `## Output`. Signal → CLI → install-command table covers the high-signal set (`gh`, `aws`, `gcloud`, `sentry-cli`, `vercel`, `netlify`) with spec keyword triggers and `command -v` presence checks. Sample Output block extended with a CLI warning line. Decomposition proceeds regardless of warnings (advisory, not blocking). `## Optional Hooks` appendix from FB-037 untouched — same file, different section.
```

**3c. Next action bullet:** update remaining items.

**3d. Phase 4 Single-item section:** flip the FB-028 row to `[x]` with date.

**3e. File Collision Map:** strike the `support/reference/setup-checklist.md` row Best-prac column:
- `support/reference/setup-checklist.md` row Best-prac: `FB-028 CLI installs` → `~~FB-028 CLI installs~~ ✓`

**3f. Cleanup Manifest:** add row:
```
| `plan-fb-028-setup-checklist-clis.md` | DELETE-AFTER | FB-028 setup-checklist CLI hints implementation plan for fresh-session execution |
```

**3g. Session Log entry:** Done / Judgment calls / Next / Open questions. Judgment calls to cover: (1) table shape (signal → CLI → install) rather than prose; (2) starter CLI set (gh/aws/gcloud/sentry-cli/vercel/netlify) — common cloud+deploy CLIs from best-practices doc, not exhaustive; (3) advisory (not blocking) check behavior consistent with checks 1–3; (4) placement after Check 3, before `## Output` — keeps checks contiguous, Optional Hooks stays appendix-only.

---

### Step 4: Commit

Single commit. Pre-commit hook: `setup-checklist.md` is sync-category — hook will warn about `version.json`.

Commit message (HEREDOC):

```
Phase 4: FB-028 — CLI tool hints in setup-checklist.md

New ### 4. External CLI Tools check inserted between Check 3 and
Output. Table maps spec-signal keywords to recommended CLIs and
install commands (gh, aws, gcloud, sentry-cli, vercel, netlify),
with a command -v presence check and an advisory warning when a
matched signal's CLI is missing. Sample Output block extended with
a representative warning. Check is advisory — decomposition
proceeds regardless.

Rationale: authenticated CLIs return structured output with fewer
rate-limit issues than unauthenticated API calls; catching missing
installs at decomposition time prevents mid-implementation friction.

FB-037 Optional Hooks appendix (same file, different section)
untouched.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Verification Checklist (post-edit, pre-commit)

- [ ] `setup-checklist.md` has new `### 4. External CLI Tools` section between Check 3 and `## Output`
- [ ] Table has at least 6 rows: `gh`, `aws`, `gcloud`, `sentry-cli`, `vercel`, `netlify`
- [ ] Each row has spec signal + CLI name + macOS install + Linux install columns
- [ ] Presence-check approach uses `command -v`
- [ ] `## Output` sample block includes a representative CLI warning line
- [ ] `## Optional Hooks` appendix (FB-037 content) unchanged
- [ ] Tracker: status, Current State, Phase 4 single-item `[x]`, File Collision Map strike, Cleanup Manifest row, Session Log entry
- [ ] Pre-commit hook shows `version.json` warning (expected)

---

## What NOT to Do

- **Don't** make this check blocking — decomposition proceeds on warnings, matching Checks 1–3.
- **Don't** bundle the install commands into a script. Users run installs themselves, at their preferred time.
- **Don't** expand to every possible CLI. Starter set of 6 covers the high-signal integrations from the best-practices source; users extend per project.
- **Don't** touch the `## Optional Hooks` appendix (FB-037's content).
- **Don't** add the check to `commands/work.md` Step 1 — decomposition already reads `setup-checklist.md`; the new check lands as part of that existing read.
- **Don't** bump `.claude/version.json` — Phase 5 handles scope.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Target | `.claude/support/reference/setup-checklist.md` (insert between lines 39 and 41 in current file) |
| Read by | `commands/work.md` Step 1 during decomposition |
| Tracker | `template-upgrade-2026-04.md` (root) |
| Source feedback | `.claude/support/feedback/feedback.md` line 154 |

---

## Post-Commit: What Happens Next

- One more Phase 4 single-file item closed. Remaining: FB-019 (or closed if ordered first), FB-029/030 (new `automation.md`), FB-011 (scripts inventory).
- Version bump tally for Phase 5 gains FB-028.
