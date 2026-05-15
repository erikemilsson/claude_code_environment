# Archived Feedback

All resolved feedback items. Each entry preserves its final status and reason.

- **promoted** — Incorporated into the spec via `/iterate`
- **absorbed** — Combined into another item (has `absorbed_into` pointer)
- **closed** — Investigated but decided against
- **archived** — Not relevant (quick triage)

---

## FB-002: `decomposition-heuristics` skill needs a "Research-spike pattern" section — methodology→empirical→analysis task shape doesn't fit the `owner` enum cleanly

**Status:** promoted
**Captured:** 2026-05-15
**Refined:** 2026-05-15 — Template skill edit: add a "Research-spike pattern" section to `.claude/skills/decomposition-heuristics/SKILL.md` covering the methodology→empirical-loop→analysis task shape. Documents trigger (task shape combines methodology + empirical loop + analysis), decomposition (TXXXa claude-methodology blocks TXXXb human-loop blocks TXXXc claude-analysis), collapse rule for trivial spikes (single Claude task with in-prose hand-off), description discipline (TXXXb carries the empirical-prompt; TXXXc carries the analysis shell), and verification convention (TXXXa/TXXXc normal verify; TXXXb self-attests via `/work complete`). Per styler DEC-082 Option ε. Zero schema churn (uses existing `/breakdown` primitive and 3-value `owner` enum). Optional companion edit: a worked example in `.claude/commands/breakdown.md`. **Mirror constraint:** per DEC-007 Option B (Skills trial), the same section must also land in `.claude/support/reference/decomposition.md` until one file is retired.
**Assessed:** 2026-05-15 — Scope: additive (one new section in SKILL.md + mirror in `decomposition.md`; optional worked example in `commands/breakdown.md`). No conflicts with resolved decisions; aligns with downstream styler DEC-082 Option ε. Template version bump on promotion: MINOR (new feature in a shipped skill). No interaction with current Active Follow-ups (FB-011 Families C/D/E, FB-033 / DEC-009, DEC-013 audit-family follow-ups).
**Promoted:** 2026-05-15 — Applied as template-maintenance edit (no spec involvement; template repo has no project spec per CLAUDE.md). New "Research-spike Pattern" section added to BOTH `.claude/skills/decomposition-heuristics/SKILL.md` AND its mirror `.claude/support/reference/decomposition.md` (DEC-007 Option B mirror constraint honored). Sub-sections: Trigger, Decomposition, Collapse rule, Description discipline, Verification convention, Why this shape. Optional companion edit in `.claude/commands/breakdown.md` deferred — can be added later if a worked example proves useful. Template version bumped 3.12.0 → 3.13.0. Downstream projects (e.g., styler) inherit via `/health-check` sync.
**Source:** styler project (`/Users/erikemilsson/Developer/styler/`) — surfaced via FB-162 (2026-05-06 audit), formalized via DEC-082 (decided 2026-05-15 with Option ε). The decision record + research archive live in styler at `.claude/support/decisions/decision-082-task-owner-field-refinement.md` + `.claude/support/decisions/.archive/decision-082-research-2026-05-15.md` for the full reasoning. **This feedback exists in the template repo because the implementation surface — `.claude/skills/decomposition-heuristics/SKILL.md` — is template-owned and the pattern generalises across forks.**

### The structural finding

The `owner` field uses a 3-value enum (`claude | human | both`) per `.claude/rules/task-management.md`. Today's enum encodes **who is responsible**, conflated with **who executes the work**. For most tasks the two are the same. For a specific task shape — **methodology → empirical loop → analysis** — they split cleanly.

**Concrete example (styler T610):** a research spike investigated `pngpaste` / AppleScript clipboard reliability. The task was filed as `owner: claude` because the deliverable was a workspace markdown report (Claude-authorable artifact). But the **empirical test loop** required the user to paste images into the Claude Code conversation under various conditions — something only a human can do. `owner: claude` was misleading; the spike's structural shape was "Claude authors methodology → human runs empirical loop → Claude analyzes results and writes report."

**`owner: both` doesn't fit either.** Today's `both` is documented (`.claude/support/reference/task-schema.md:160-162`) for **review-shaped** work: "design work (human provides direction, Claude implements)" / "content requiring human judgment (Claude drafts, human refines)." A research spike's human empirical loop is NOT a review — the user IS the experimental apparatus.

### The pattern recurs

Two known instances in styler's 525-task corpus (T610 + T456). The pattern generalises beyond styler to:
- Onboarding sniff tests (Claude designs the sniff; human runs it; Claude analyzes friction signals)
- Perceptual A/Bs (Claude generates A vs B; human picks; Claude synthesizes the preference)
- Brand-new feature dogfooding cycles (Claude scaffolds the feature; human uses it for N days; Claude reviews observed friction)
- Any task whose validation step requires human-only sensors (taste, perception, in-the-moment judgment)

### The decision (DEC-082 → Option ε, decided 2026-05-15)

Five options were evaluated against 9 criteria (full matrix in styler's DEC-082). **Option ε won:** instead of changing the `owner` enum or adding new fields, **decompose research-spike tasks at decomposition time** via the existing `/breakdown` primitive:

```
TXXXa (owner: claude)            — authors methodology + drafts the empirical-prompt + leaves analysis shell
   ↓ blocks
TXXXb (owner: human)             — runs the empirical loop, reports results in conversation; self-attests via /work complete
   ↓ blocks
TXXXc (owner: claude, deps: [TXXXa, TXXXb]) — synthesizes results into the final report
```

For tiny spikes where the empirical step is "paste one image", **collapse to a single Claude task** with an in-prose hand-off (today's de-facto pattern, called α in DEC-082). The paired-sub-task structure is for spikes where the empirical loop is independently worth tracking.

**Why ε won:** zero schema churn (uses existing `/breakdown`); surfaces the human empirical loop as a first-class dashboard artifact (TXXXb appears in "Your Tasks" with `❗`); each sub-task gets native verification routing (TXXXa/TXXXc via verify-agent's 7-check suite; TXXXb via self-attestation); generalises broadly. Trade-off: 1 task → 2-3 sub-tasks of bookkeeping for low-difficulty work.

Worst options (ranked low in DEC-082): γ (split `owner` + `executor` fields) had highest contract-surface impact; β (sub-token `both:research`) overloads the enum with a separator; α (convention-only) leaves the empirical step invisible to dispatch + dashboard.

### Implementation surface (template-owned)

**Single edit:** add a "Research-spike pattern" section to `.claude/skills/decomposition-heuristics/SKILL.md` documenting:

1. **Trigger** — task shape is methodology + empirical loop + analysis (research spikes, perceptual A/Bs, sniff tests, dogfood cycles).
2. **Decomposition** — split into TXXXa (claude methodology, drafts empirical-prompt), TXXXb (human empirical loop, self-attests via `/work complete`), and optionally TXXXc (claude analysis with `deps: [TXXXa, TXXXb]`).
3. **Collapse rule** — if the empirical step is trivial (~1 user action, no iteration), single Claude task with in-prose hand-off is fine. The paired pattern is for spikes where the empirical loop is independently worth tracking.
4. **Description discipline** — TXXXb's description must include the empirical-prompt template TXXXa drafted (so user knows what to test); TXXXc's description must include the analysis shell TXXXa stubbed.
5. **Verification convention** — TXXXa/TXXXc verified normally; TXXXb self-attests via `/work complete`. Acceptance for TXXXa is "did Claude produce a methodology that matches the spike's directional question?", not "did the empirical loop produce a specific answer?"

**Optional second edit:** `.claude/commands/breakdown.md` could gain a worked example mirroring this pattern (decomposition-time call).

### Why this fits the template, not the project

- The owner-enum semantics + decomposition heuristics are template-owned (`.claude/rules/`, `.claude/skills/`).
- The pattern applies to ANY Claude Code project that runs research spikes, perceptual tests, sniff tests, or dogfood cycles — not just styler.
- DEC-082 itself stays in styler's decision log (the friction surfaced there; the reasoning trail belongs with the surfacing context) — but the implementation lands in the template so all forks inherit the convention.

### Erik's plan

Capture this feedback in the template repo; let template-side Claude `/feedback review` triage it on its own schedule. After the SKILL.md edit lands in the template, Erik runs `/health-check` in styler to sync the updated template files back into styler's working tree.

### Pointers for template-side Claude

- **Full reasoning + research archive:** `/Users/erikemilsson/Developer/styler/.claude/support/decisions/decision-082-task-owner-field-refinement.md` (decision record, 240 lines, status: approved, includes 5 options × 9 criteria matrix + per-option Details + 4 open research questions). Research archive: `/Users/erikemilsson/Developer/styler/.claude/support/decisions/.archive/decision-082-research-2026-05-15.md` (187 lines, per-contract-site grep findings, dispatch spike per option, prior art from Jira/Linear/Asana).
- **Source feedback:** styler's FB-162 (now archived as `promoted` in styler's `archive.md` with reference to DEC-082).
- **The motivating concrete case:** styler T610 (Finished, owner:claude, but the empirical loop was structurally human-driven). T456 is a second, structurally similar instance.

### Out of scope for this feedback

- No changes to `.claude/rules/task-management.md` (3-value `owner` enum stays).
- No changes to `.claude/support/reference/task-schema.md`.
- No changes to `.claude/agents/implement-agent.md` or `.claude/agents/verify-agent.md`.
- No retroactive migration of existing tasks — pattern is forward-only.
- No new task statuses or sub-statuses introduced.
- A future `task_kind` field (option δ in DEC-082) could land alongside as a complement if drift surfaces — explicitly NOT part of this feedback; if it becomes worthwhile, capture as a fresh feedback item.

### Tags

decomposition-heuristics, task-schema, owner-field, research-spikes, skill-edit, template-fix, derived-from-styler-DEC-082

---

## FB-001: `mcp-server-git` leaves stale empty `.git/index.lock` on crash — blocks git in affected repos

**Status:** closed
**Captured:** 2026-05-15
**Closed:** 2026-05-15 — Out of template scope. Both proposed fixes (Option A: remove `mcp-server-git` from user-level Claude Code config; Option B: user-level `SessionStart` hook clearing verified-stale locks) live in `~/.claude/`, not in template-shipped `.claude/`. Nothing for the template to ship. Erik can apply Option A in his personal setup directly. Preserved here for cross-project audit trail; if the pattern recurs in another project, re-open as a template-side troubleshooting doc.
**Source:** observed in two projects (`styler/` and `styler-phone/`) during a single Claude Code session on 2026-05-15. Both repos had zero-byte `.git/index.lock` files dated **exactly `May 15 08:42`** (same minute, both 0 bytes, no holding process). Required manual `rm .git/index.lock` to unblock subsequent git commits. Surfaced twice in one day from a single crash event.

### The observation

The Anthropic-shipped `mcp-server-git` MCP server (Python, `~/.local/bin/mcp-server-git`) creates `.git/index.lock` at the start of any git operation that modifies the index (add, commit, etc.). If the server process crashes or is killed mid-operation, the lock stays behind. Subsequent git commands fail with:

```
fatal: Unable to create '/path/to/.git/index.lock': File exists.

Another git process seems to be running in this repository, e.g.
an editor opened by 'git commit'. Please make sure all processes
are terminated then try again.
```

**Detection signal — distinguishes stale from real:**
- Stale lock: zero bytes (`stat` shows `size=0`)
- Stale lock: minutes-to-hours old
- Stale lock: no active git process holding it (`ps aux | grep "git "` shows nothing besides idle `mcp-server-git` MCP-tool-host instances)
- Real lock during active git operation: non-zero size, very fresh (sub-second old), `git` process visible in `ps`

### Evidence from the 2026-05-15 incident

```
$ ls -la /Users/erikemilsson/Developer/styler/.git/index.lock \
        /Users/erikemilsson/Developer/styler-phone/.git/index.lock
-rw-r--r--  1 erikemilsson  staff  0  May 15 08:42  styler/.git/index.lock
-rw-r--r--  1 erikemilsson  staff  0  May 15 08:42  styler-phone/.git/index.lock

$ ps aux | grep "git " | grep -v grep
(nothing besides idle mcp-server-git instances — no active git process)
```

Same minute, both repos, zero bytes. Single crash event affected two repos because one `mcp-server-git` instance was touching both (or two instances crashed in lock-step). The locks survived ~7 hours into the day's work before being noticed at commit time.

### Two fix options

**Option A — Disable `mcp-server-git`, fall back to Bash (recommended — root-cause).**

The MCP server is configured at the user level (`~/.claude/...`) and spawns one instance per Claude Code session. In observed workflows, Claude reaches for the Bash tool for git operations (clearer permission rules per project CLAUDE.md preferences), leaving the MCP server idle. Removing its entry from the relevant Claude Code config (`~/.claude/settings.json` or the MCP-server registry, depending on installation) eliminates the crash class entirely.

- **Pro:** zero stale-lock surface (no crashing process = no stale locks); lighter memory footprint (fewer Python processes resident across sessions); cleaner permission model.
- **Con:** any workflow that explicitly invokes `mcp__git__*` tools would need to fall back to Bash. Unknown without inspecting individual workflows; for sessions observed during the incident, no such workflow existed.
- **Implementation:** edit user-level Claude Code config to remove the `git` MCP server entry; restart sessions.

**Option B — `SessionStart` hook that auto-clears verified-stale locks (belt-and-suspenders).**

A hook that scans known repos at session start and removes `.git/index.lock` files that are (a) zero bytes AND (b) older than ~60 seconds AND (c) not held by any active git process. Safe because real git operations don't satisfy all three conditions simultaneously — real locks always have content and are fresh.

- **Pro:** neutralizes the symptom regardless of which MCP/tool crashed; doesn't require removing functionality.
- **Con:** another moving part; needs a list of known repos to scan (or it scans nothing and is useless); doesn't address why `mcp-server-git` crashes.
- **Implementation:** add a `SessionStart` hook in `~/.claude/settings.json` invoking a small bash script under `~/.claude/scripts/`. ~10 lines of bash.

### Recommendation

Ship Option A as the primary fix. Add Option B if and only if some other tool ever exhibits the same crash-leaves-lock pattern. For Erik's setup specifically, Option A is a one-line config change with no observed downside.

### Investigation worth doing alongside

Why does `mcp-server-git` crash? Two repos at the exact same minute suggests one of:
- A signal (SIGKILL/SIGTERM) hit the process — system suspend, hibernation, OOM, manual kill — that the server didn't handle with a cleanup phase.
- An exception in the server's git-invoking code path that escaped without releasing the lock.

If Claude Code keeps logs of MCP server lifecycle events (start/crash/exit), check `~/.claude/logs/` or equivalent for entries near `08:42` on the incident date. Could be a one-off (machine suspended mid-operation) or a repeatable bug.

### Related signals

- The MCP server itself is part of the Anthropic-shipped `mcp-server-git` package (or its successor). If the crash is reproducible, worth a bug report upstream.
- Empirically: stale locks DO happen with regular `git` CLI usage too (e.g., killing a `git rebase -i` mid-edit), but those typically have content in the lock file and are easy to distinguish.

### Tags

mcp, mcp-server-git, git-lock, stale-lock, claude-code-environment, crash-cleanup

---
