# Plan — FB-029 + FB-030: New `automation.md` reference doc

**Purpose:** Create a new reference document covering `claude -p` (non-interactive mode) as the automation primitive (FB-029) and the fan-out pattern for batch workloads (FB-030). Bundle: both items land in the same new file. Additive scope; no existing-file behavioral change except for a small sync-manifest entry and cross-reference pointers.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Source feedback items:** FB-029 (line 168), FB-030 (line 182) in `.claude/support/feedback/feedback.md`
**Related decisions:** none directly. Connects to FB-011 (scripts as alternative) — some FB-011 candidates may collapse to `claude -p` one-liners rather than bash scripts; this bundle should land before FB-011 so that inventory can route candidates to the right primitive.
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in same commit as this plan)
**Tracker status line to advance:** `Phase 4 — FB-029/030 implemented (new support/reference/automation.md); FB-011 ready next (scripts inventory can now route to claude -p primitive)`

---

## Scope

| Item | Touch site | Edit type |
|------|-----------|-----------|
| FB-029 | new `.claude/support/reference/automation.md` | New file — `claude -p` primitive section |
| FB-030 | same new file | New file — fan-out pattern section |
| Cross-ref | `.claude/support/reference/parallel-execution.md` | One-line "See also" pointer |
| Cross-ref | `.claude/support/reference/README.md` | One row added to `## Guides` table |
| Sync | `.claude/sync-manifest.json` | One entry added to `sync` array |
| Cross-ref (opt.) | `.claude/README.md` | Optional: mention automation.md in "Where to Find Things" |

### Out of scope

- Actually adopting fan-out or `claude -p` anywhere in the template's commands/agents. This doc is a user-facing reference — not a template feature. Template parallelism stays intra-session (Task dispatch coordinated by `/work`).
- FB-011 (scripts inventory). Separate item; this bundle lands first so FB-011 can route candidates to `claude -p` vs bash-script vs do-nothing.
- Updating `commands/work.md` to mention `claude -p`. Not load-bearing — users discover the doc via the README guides table.

---

## Context to Load Before Executing

1. **`.claude/support/reference/README.md`** — full file. New `automation.md` row lands in the `## Guides` table.
2. **`.claude/support/reference/parallel-execution.md`** — locate a natural place for a "See also" pointer (probably at the end of `## Parallelism Eligibility Assessment` or as a closing note).
3. **`.claude/sync-manifest.json`** — insert `.claude/support/reference/automation.md` into the `sync` array.
4. **`.claude/README.md`** — optional — the "Where to Find Things" table could gain an `automation.md` row.
5. **`.claude/support/feedback/feedback.md`** lines 168–194 (FB-029 + FB-030) — confirm Assessed lines haven't drifted.
6. **`template-upgrade-2026-04.md`** — Current State + File Collision Map `support/reference/automation.md` row (new file row already exists in the map).

Best-practices doc references (quoted in the feedback items):
- `claude -p "prompt"` runs without a session.
- With `--output-format json`/`stream-json` and `--allowedTools`, it's the building block for CI, pre-commit hooks, scripts, and fan-out patterns.
- Fan-out example: `for file in $(...); do claude -p "Migrate $file..." --allowedTools "Edit,Bash(git commit *)"; done`

Auto-memory: no specific entry is load-bearing.

---

## Implementation Steps

### Step 1: Create `.claude/support/reference/automation.md`

Write the new file at `.claude/support/reference/automation.md` with the following content:

```markdown
# Automation

Reference for users who want to automate template workflows or run Claude Code non-interactively. Covers two complementary tools: the `claude -p` primitive (a single prompt, no session) and the fan-out pattern (many `claude -p` calls in parallel for batch workloads).

**Scaling axes.** The template's parallel execution is *intra-session*: one `/work` orchestrator dispatches multiple `Task` agents in the same conversation, with file-conflict detection and verification gating. Automation is *inter-session*: many independent `claude` processes run outside any `/work` orchestrator. The two axes are complementary — use intra-session parallelism for spec-driven task batches (the default); use inter-session fan-out for very large or schedule-based workloads.

---

## `claude -p` — the automation primitive (FB-029)

Non-interactive mode runs a single prompt and exits. No session state, no dashboard, no `/work` — just prompt in, output out. It's the building block for CI checks, pre-commit hooks, scheduled jobs, and shell-driven batch pipelines.

**Basic form:**

```bash
claude -p "Summarize the changes in the last three commits."
```

**Structured output:**

```bash
claude -p "List all tasks with status Blocked." --output-format json
claude -p "Explain this code." --output-format stream-json
```

- `--output-format json` — single JSON response. Good for pipelines parsing a final answer.
- `--output-format stream-json` — newline-delimited events. Good for watching tool use in real time.

**Scoping tool permissions:**

```bash
claude -p "Regenerate the dashboard." --allowedTools "Read,Write,Grep"
claude -p "Commit the staged changes with a useful message." --allowedTools "Bash(git *)"
```

- `--allowedTools` restricts which tools the run may use. Use it aggressively for automation — an unattended run should not be able to touch tools you didn't intend.
- Tool patterns support globs (e.g., `Bash(git *)` allows any `git` subcommand via Bash but nothing else).

**Working-directory and model:**

```bash
claude -p "..." --cwd /path/to/project --model claude-opus-4-7
```

### When to reach for `claude -p`

| Scenario | Fits `claude -p`? |
|----------|-------------------|
| Nightly `/health-check` run in CI | Yes — scheduled, no user sitting there |
| Pre-commit hook that checks for TODOs in staged files | Yes — one-shot, structured response |
| Batch dashboard regen across many projects | Yes — use fan-out (below) |
| Interactive spec iteration with user | No — use `claude` / `/work` / `/iterate` |
| Anything that needs the handoff file or session history | No — `claude -p` has no session |

### When NOT to reach for `claude -p`

- The task requires conversational back-and-forth. `claude -p` is a single turn.
- The task must read the dashboard or task state AS IT EVOLVES. `claude -p` has no awareness of in-progress `/work` sessions.
- The task needs user approval. Non-interactive runs cannot prompt.

---

## Fan-out — parallel batch execution (FB-030)

When a workload is "same operation, many inputs," spawn many `claude -p` processes in parallel. This is how you scale past what one session (intra-session Task dispatch) can coordinate.

**Minimal pattern:**

```bash
for file in $(git ls-files '*.py'); do
  claude -p "Refactor $file to use the new logger API. Make one commit." \
    --allowedTools "Read,Edit,Bash(git add *),Bash(git commit *)" &
done
wait
```

**With a concurrency cap (prevents CPU/memory exhaustion):**

```bash
ls src/**/*.py | xargs -n 1 -P 4 -I {} \
  claude -p "Migrate {} to the new schema. Commit the change." \
  --allowedTools "Read,Edit,Bash(git add *),Bash(git commit *)"
```

- `-P 4` — four concurrent processes. Tune to your machine; 4–8 is a reasonable starting range.
- Each process runs independently — no shared session state.

### When fan-out fits

- **Large migrations** — "change every file like this" across hundreds of files.
- **Report generation** — "produce a summary for each row in this dataset."
- **Scheduled sweeps** — nightly validation across many project directories.

### When fan-out does NOT fit

- Tasks that interact with each other (one's output is another's input). Serial execution or intra-session `/work` is the right tool.
- Tasks that write to the same file. Concurrent writes without coordination corrupt state. Partition the work so each process owns its files.
- Tasks that require `.claude/` task-JSON updates or dashboard regeneration. `.claude/` writes in a fan-out are uncoordinated and will race.

### Coordination at the boundary

Fan-out workers should each produce an artifact (a commit, a file, an output line). The main process collects artifacts after `wait`. Do NOT have workers update shared state mid-run.

**Good pattern:**
```bash
for file in $(...); do
  claude -p "Process $file. Write result to out/$(basename $file).json." ... &
done
wait
# Now collect results
cat out/*.json | jq -s '.' > summary.json
```

**Bad pattern:**
```bash
for file in $(...); do
  claude -p "Process $file and append to shared.log." ... &  # race: concurrent writes to shared.log
done
```

---

## Interaction with the template

- **Intra-session parallel execution** (`parallel-execution.md`) is the default for spec tasks. Use it when tasks are in the spec, file-conflict detection matters, and verification should happen per task.
- **Fan-out** is for ad-hoc or scheduled work outside the spec. Use it when the coordination overhead of `/work` is more than the job requires.
- **`claude -p`** is the building block for both ad-hoc automation and fan-out.

The template does NOT ship any fan-out scripts. This doc is reference for users who want to build their own.

## Related

- `.claude/support/reference/parallel-execution.md` — intra-session parallel Task dispatch (the `/work` orchestrator's path).
- `.claude/commands/health-check.md` — candidate for nightly `claude -p` automation.
- Claude Code docs — full `claude -p` CLI flag reference.
```

---

### Step 2: Add cross-reference from `parallel-execution.md`

Locate `.claude/support/reference/parallel-execution.md`. At the end of the top-level `# Parallel Execution` intro block (after "These run inline during `/work` Steps 2c and 4.", ~line 4), add one short paragraph:

```markdown
**Scope:** this doc covers *intra-session* parallelism — multiple `Task` agents coordinated by one `/work` orchestrator within a single conversation. For *inter-session* parallelism (many independent `claude` processes for batch workloads), see `.claude/support/reference/automation.md`.
```

Place this between the intro and the first `---` separator. Keep it one paragraph — don't expand.

---

### Step 3: Add row to `.claude/support/reference/README.md`

Locate the `## Guides` table (lines 31–39 in current file). Add a new row for `automation.md`:

```markdown
| `automation.md` | `claude -p` primitive + fan-out pattern for inter-session automation |
```

Place this row after `setup-checklist.md` and before `desktop-project-prompt.md` — rough alphabetical-ish ordering consistent with nearby rows.

---

### Step 4: Add entry to `sync-manifest.json`

Locate `.claude/sync-manifest.json`. In the `sync` array, add `.claude/support/reference/automation.md` immediately after `setup-checklist.md` (maintains the alphabetical-ish order within the `support/reference/` block):

```json
      ".claude/support/reference/setup-checklist.md",
      ".claude/support/reference/automation.md",
      ".claude/support/reference/known-issues.md",
```

---

### Step 5: (Optional) Add row to `.claude/README.md` "Where to Find Things"

If `.claude/README.md` has a "Where to Find Things" table with references to other reference docs, add an `automation.md` row. Locate the table by grep; if it exists, add:

```markdown
| Non-interactive automation (CI, pre-commit, fan-out) | `.claude/support/reference/automation.md` |
```

If no such table exists or adding it would require restructuring, skip this step. The file is discoverable via `support/reference/README.md`.

---

### Step 6: Tracker bookkeeping

Update `template-upgrade-2026-04.md`:

**6a. Status line:** update to reflect the bundle complete.

**6b. Current State:** add new bullet:

```
- **FB-029/030 implemented 2026-04-17:** New `.claude/support/reference/automation.md` documenting the `claude -p` primitive (FB-029) and fan-out pattern (FB-030). Doc clarifies the intra- vs inter-session parallelism distinction, scopes `claude -p` with concrete examples (output formats, allowedTools scoping, working-dir/model flags), and covers fan-out with concurrency caps and the shared-state coordination rule (workers produce artifacts, main collects; never shared-write). Cross-referenced from `support/reference/parallel-execution.md` (one-paragraph scope note) and added to `support/reference/README.md § Guides` + `sync-manifest.json § sync`. Template itself does not adopt fan-out — this is user-facing reference.
```

**6c. Next action bullet:** FB-011 ready (automation primitive now available for routing scripts-inventory candidates).

**6d. Phase 4 Single-item section:** flip the FB-029 + FB-030 row to `[x]` with date.

**6e. File Collision Map:** strike the `support/reference/automation.md` row:
- `support/reference/automation.md (new file)` row Best-prac: `FB-029 claude -p; FB-030 fan-out` → `~~FB-029 claude -p~~ ✓; ~~FB-030 fan-out~~ ✓`
- Also strike the alt-site marker on `support/reference/parallel-execution.md` row Usage: `FB-030 fan-out (alt site)` → `~~FB-030 landed in automation.md; parallel-execution.md gained scope pointer~~ ✓`
- If `.claude/README.md` row was touched, strike its `FB-029 mention (alt site)` marker similarly.

**6f. Cleanup Manifest:** add row:
```
| `plan-automation-md-bundle.md` | DELETE-AFTER | FB-029 + FB-030 automation.md bundle implementation plan for fresh-session execution |
```

**6g. Session Log entry:** Done / Judgment calls / Next / Open questions. Judgment calls to cover: (1) shape of the doc (primitive first, then pattern — fan-out depends on understanding `claude -p`); (2) intra-vs-inter-session framing — makes it explicit that this doc is NOT overlap with parallel-execution.md; (3) examples use realistic tool-scoping (`--allowedTools "Bash(git *)"`) rather than permissive defaults; (4) shared-write coordination warning explicit with good/bad code blocks; (5) optional README row left to judgement (add if fits).

---

### Step 7: Commit

Single commit. Pre-commit hook: `parallel-execution.md` and the new `automation.md` are sync-category; `sync-manifest.json` and `support/reference/README.md` also touched. Hook will warn about `version.json`.

Commit message (HEREDOC):

```
Phase 4: FB-029 + FB-030 — new automation.md reference doc

New .claude/support/reference/automation.md bundling FB-029 (claude
-p non-interactive primitive) and FB-030 (fan-out pattern for batch
workloads). Explicitly frames the intra- vs inter-session
parallelism distinction — template's /work-coordinated Task
dispatch stays the default; fan-out is the user's tool for ad-hoc
or scheduled batch work outside the spec.

claude -p section covers structured output (--output-format
json/stream-json), tool scoping (--allowedTools "Bash(git *)"),
and working-dir/model flags, plus a fits/does-not-fit decision
table.

Fan-out section gives minimal and concurrency-capped patterns
(for-loop with &/wait; xargs -P 4), fit/no-fit cases, and an
explicit shared-state coordination rule (workers produce
artifacts; main collects after wait; never shared-write mid-run).

Cross-refs: parallel-execution.md gets a one-paragraph scope
pointer; support/reference/README.md § Guides gets a new row;
sync-manifest.json gets the new file entered in the sync array.

Template itself does not adopt fan-out — user-facing reference
only. Unblocks FB-011 scripts inventory (some candidates may route
to claude -p one-liners rather than bash scripts).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Verification Checklist (post-edit, pre-commit)

- [ ] `.claude/support/reference/automation.md` exists and contains: intro + `## claude -p` section + `## Fan-out` section + `## Interaction with the template` + `## Related`
- [ ] `claude -p` section has: basic form, structured output (`json`/`stream-json`), `--allowedTools` scoping, working-dir/model flags, When-to-reach-for / When-NOT tables
- [ ] Fan-out section has: minimal pattern (`for/& /wait`), concurrency cap pattern (`xargs -P`), fit / no-fit cases, shared-state coordination rule with good/bad examples
- [ ] `parallel-execution.md` has one-paragraph "Scope" pointer at top (intra- vs inter-session)
- [ ] `support/reference/README.md § Guides` has a new `automation.md` row
- [ ] `sync-manifest.json sync` array has `.claude/support/reference/automation.md`
- [ ] Tracker: status, Current State, Phase 4 single-item `[x]`, File Collision Map strikes (automation.md row + parallel-execution.md alt-site + optional README), Cleanup Manifest row, Session Log entry
- [ ] Pre-commit hook shows `version.json` warning (expected)

---

## What NOT to Do

- **Don't** make the template itself use fan-out. This is a user-facing reference; no command or agent changes.
- **Don't** duplicate content from `parallel-execution.md`. The automation doc's job is the *inter-session* axis; `parallel-execution.md` remains the authority for *intra-session*. Cross-reference, don't copy.
- **Don't** use permissive tool scoping in examples (`--allowedTools "*"` or unrestricted Bash). Examples should model secure defaults.
- **Don't** include real credentials, GitHub tokens, or AWS ARNs in examples.
- **Don't** land FB-011 in the same commit — separate item, separate commit.
- **Don't** bump `.claude/version.json` — Phase 5 handles scope.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| New file | `.claude/support/reference/automation.md` |
| Cross-ref target | `.claude/support/reference/parallel-execution.md` (top intro block) |
| Index update | `.claude/support/reference/README.md § Guides` |
| Sync manifest | `.claude/sync-manifest.json sync` array |
| Tracker | `template-upgrade-2026-04.md` (root) |
| Source feedback | `.claude/support/feedback/feedback.md` lines 168 (FB-029), 182 (FB-030) |

---

## Post-Commit: What Happens Next

- FB-029 and FB-030 both closed. Phase 4 remaining: FB-011 (scripts inventory — now unblocked with `claude -p` primitive available as a routing option), and whichever of FB-019 / FB-028 haven't landed yet.
- FB-011 can now inventory candidates and route each to: (a) bash script, (b) `claude -p` one-liner, (c) stay as a command procedure. The presence of this doc lets FB-011 make that routing call.
- Version bump tally for Phase 5 gains FB-029 + FB-030 (new file + minor cross-references).
