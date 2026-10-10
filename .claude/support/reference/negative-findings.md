# Negative Findings and Absence Probes

The full contract behind `rules/agents.md § "Negative Findings Require a Positive Control"`. Lazy, not auto-loaded. **Read this before persisting an absence claim, closing a finding with an absence sweep, or mutation-testing a guard.**

Origin: styler FR-040 (2026-06-10), where a silent grep failure became a false "engine dormant" finding that reached the handoff, dashboard and memory. The rule was widened after three projects showed its mechanism defeated: controls that returned nothing, a mandated `Grep` tool that wasn't there, and result sets that didn't match the claim.

## When it applies

- **Persisted absence claims:** "X is absent / dormant / unused / has no consumer / never fires / never existed", written anywhere durable: friction register, handoff, dashboard, a verification result or report (`issues[]`, `friction_markers[]`, `notes`), task notes, memory, decision or research records, retirement proposals.
- **Closure sweeps:** a search whose empty result closes a finding, passes a check, or ticks a criterion ("no stale references left", "no other callers"). The sweep is itself an absence claim.
- **New guards and checks** you're about to rely on: see § "Fail before trust".

An exploratory search whose empty result you neither record nor act on needs no control.

## The rule

Every absence probe carries a **positive control that returns a hit**: a target known to be present in the same universe, found by the same tool with the same flags, root, globs and filters, in the same command where practical.

- A control that returns nothing means the probe is broken, not that the target is absent. Fix the probe before claiming anything.
- A control run with a different tool, root or filter proves nothing about the probe.
- Match the control to the target's shape: same file type, same directory class, gitignored if the target might be, a directory if the target is one.
- No working control: report "unverified absence" and write nothing to state.

One command, one row per pattern; the second pattern is the control and must count at least 1. Report both counts with the claim:

```bash
for p in 'legacyScoreFormat' 'ScorePill'; do printf '%s: ' "$p"; rg -uu -l -g '!.git' "$p" . | wc -l; done
```

## Harness search facts (observed 2026-10)

- **There may be no `Grep` or `Glob` tool.** In auto mode the harness offers neither, loaded or deferred, and its prompt directs search through Bash; sessions in three projects, subagents included, ran without them.
- **Bash `grep` is a wrapper.** In the Claude Code shell, `grep` is a shell function (from `~/.claude/shell-snapshots/`) that runs an embedded ugrep with `--ignore-files -I`: it **skips gitignored and binary files**. `rg` and `find` are wrapped too (the `find` wrapper skips nothing); `type grep` shows what you have. Measured in the template repo: `grep -rl` found none of the 23 gitignored files that `/usr/bin/grep -rl` found. Searching `.`, it prints paths without the leading `./` that `/usr/bin/grep` keeps, so normalise paths before diffing the two outputs.
- **`rg` skips hidden and gitignored paths by default**, so a repo-root `rg` never sees `.claude/` (`rg --files` listed none of its files; `-uu` listed all). The `Grep` tool is ripgrep and honours `.gitignore` too. When the target may be hidden, gitignored or binary, use `rg -uu` (`-uuu` adds binary files; `-g '!.git'` skips git internals), `/usr/bin/grep -r`, or the file's direct path. A file you name is always searched. A directory you name is searched even when it or a parent is hidden or gitignored (`rg --files interaction-logs` lists the template repo's gitignored logs), but inside it `rg` still skips hidden entries and those an ignore rule matches (`*.pyc`).
- **BSD grep** (`/usr/bin/grep` on macOS) bypasses the wrapper's filters but can return nothing on some files without an error (FR-040). It needs its control like anything else.
- **Quote every glob.** zsh expands an unquoted glob before the search tool sees it. `--include=*.md` matches no file, so zsh prints `no matches found` and the search never runs; inside a pipeline (`| wc -l`, `| head`) that reads as an empty result with exit 0. `-g *.md` turns into the `.md` files in the current directory, which can shift your pattern into the path list.
- **Dotfiles and directories.** Shell globs, plain `ls` and the Glob tool skip leading-dot names, and `rg --files` lists files only, never directories. Enumerate with `find <root> -name '<pattern>'` (add `-type d` for directories) or `ls -a`.

## Result set

- **Repo-wide by default**, including `.claude/` and gitignored paths when they could hold the target. If you narrow the root (`docs/` only) or exclude paths (`-g '!node_modules'`), say so in the claim and why the excluded paths can't hold the target.
- **No truncation.** No `| head`, `| tail` or `--max-count` on an absence or completeness probe: count first (`rg -c`, `| wc -l`), then page.
- **An enumeration you checked is a sample, not the population.** "The 12 files I read are clean" doesn't show that no file has it; run the probe over the whole root.
- **For whole-file absence** ("no test covers X", "no doc still describes Y"), enumerate and classify: list every candidate file (`find`, or `rg --files -uu -g '<glob>'`) and classify each one, rather than trusting a single pattern match.
- **Search by subject, not the old literal.** A guessed vocabulary under-matches: task-062's sweep for `tasks|tests|measures|checks|tables` missed a reference worded with `entries`. Search for what the claim is about (IDs, entity or column names, the figure). For closure sweeps see `agents/verify-agent.md` Step T2c item 4.

## Historical claims

A working-tree probe can't see deleted files, so "never existed" or "was never added" needs history (task-058: a "never existed" claim was checked against the working tree, but the file had existed as 389 lines until two days earlier).

- Path ever committed: `git log --all --oneline -- '*<name>*'` lists every commit touching a matching path, in any directory, renames included.
- Deleted paths: `git log --all --diff-filter=D --name-only --format= | rg '<name>'`.
- Content: `git log --all --oneline -S'<text>'`.
- Control: run the same command for a file known to have been deleted (`git log --all --diff-filter=D --name-only --format=` lists candidates) and see it hit.

History holds only committed files. For gitignored or never-committed data there is no history to ask, so say that rather than claiming "never existed".

## Artifacts that aren't plain files

Directories, symlinks, notebook cells, database tables, deployed models and live APIs need a probe that can see that class of artifact, and a control of the same class. Fabric items such as `*.CopyJob` are directories, so `rg --files -g '*.CopyJob*'` returned nothing for the target and the control alike (task-033); `find . -type d -name '*.CopyJob*'` would have listed both. A repo search can't establish absence in live state: query the live system (`rules/agents.md § "Orchestrator-Authored State Claims"`).

## Fail before trust

Trust a new guard, check, test or control only after seeing it fail on the regression it exists to catch: run it against the pre-fix state, or a mutated copy, and see it fail; then against the fixed state and see it pass. A check that passes both ways is vacuous (task-060: a synthetic test control passed while the real guard scored 0 against the actual pre-fix file). For a check that asserts "0 violations", plant one violation in a copy and confirm the check reports it.

## Extractors and derivation scripts are probes

A hand-written regex extractor, parser or derivation script that produces a list or a count is a probe: anything it can't parse is silently missing from its output (PortfolioWebsite: a derivation script's regex couldn't match multi-line template literals). Before trusting its output, include a known item of each shape among its inputs (multi-line, quoted, nested) and reconcile its count with an independent one (`rg -c`, or a hand count on one file).

## Mutation testing: the restore contract

Mutating a file to show a guard fails is safe only with a byte-exact restore:

1. Copy the file outside the repo and record its hash: `T=$(mktemp -d); cp <file> "$T/"; shasum -a 256 <file>` (or `sha256sum`; subagents can't write under `.claude/`).
2. Mutate, run the guard, and record that it failed.
3. Restore by copy (`cp "$T/<name>" <file>`), re-hash, and confirm the hash matches the recorded one.
4. **Never restore with `git checkout -- <file>` or `git restore <file>`** while the file has unstaged changes. Both restore from the index, which for unstaged work is HEAD, so the uncommitted implementation is lost (task-038_3: 269 lines destroyed, recovered only through the pre-mutation hash and an in-context diff).

## See also

- `rules/agents.md § "Negative Findings Require a Positive Control"`: the always-loaded rule this expands.
- `rules/feature-retirement.md § "Pre-Retirement Engine-Consumer Audit"`: *which* name variants to search before a "no consumer" claim. This doc covers whether the probe works.
- `agents/verify-agent.md` Step T2c item 4: closure sweeps by subject.
- `support/reference/claude-code-authoring.md § "Search tools: Grep/Glob may be absent, grep and rg skip files"`: the platform facts, for authors.
