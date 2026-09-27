---
id: DEC-025
title: Per-task verification scaling for low-difficulty tasks (Opus 5.5 recalibration)
status: approved
category: process
created: 2026-09-27
decided: 2026-09-27
related:
  tasks: []
  decisions: [DEC-004, DEC-011]
  feedback: [FB-119]
implementation_anchors:
  - file: "CLAUDE.md"
    description: "Active Follow-ups — DEC-025 recheck gate entry"
  - file: ".claude/support/reference/work-procedures.md"
    description: "verification_history[].cost capture (v5.5.2) — the gate's data source"
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Per-task verification scaling for low-difficulty tasks (Opus 5.5 recalibration)

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Status quo — one independent verify dispatch per task, all difficulties
- [ ] Option B: Batched verification for difficulty ≤2 (plain, or hybrid with per-task escape hatches for runtime-surface / ≥3-file / has-dependents tasks)
- [ ] Option C: Lightweight verify profile for difficulty ≤2 (reduced step set and/or lower-effort named agent)
- [x] Option D: Defer with an explicit, data-driven recheck gate on `verification_history[].cost` *(research recommendation — optionally paired with E)*
- [ ] Option E: Trim fixed per-dispatch overhead for all difficulties (per-task/phase-level split of `verify-agent.md`) *(added by research; complementary to D)*

*Check one box above (D+E may be selected together), then fill in the Decision section below. Research populated evidence only — the selection is yours.*

## Background

Every task, including difficulty 1–2, currently gets its own independent verify-agent dispatch (fresh context, full T1–T8 workflow) before it can reach Finished (`task_verification.result == "pass"` is a structural invariant). The Opus 5 and Opus 5.5 prompting guides say the model now verifies its own work unprompted and that verification instructions and legacy harness verification steps cause over-verification. They endorse separate-agent writer/verifier patterns, but they also say to cap delegation for small tasks ("do not delegate work you can finish yourself in a handful of tool calls").

v5.5.2 already removed the implement-agent's self-review ceremony (the same-context "double-check" pattern the guides name) and added `verification_history[].cost` logging (tokens, tool uses, duration per verify dispatch). This decision covers the remaining question: **does per-task independent verification still pay for itself on difficulty 1–2 tasks, and if not, what replaces it without weakening the Finished invariant?**

**Evidence gathered 2026-09-27** (11 downstream projects, ~1,350 Finished tasks with `task_verification`; "caught" = verify-agent failed the task at least once, detected heuristically from `verification_history` / attempt counters, whose field names vary across projects):

| Difficulty | Tasks | Caught by verify-agent | Passed with minor issues noted |
|---|---|---|---|
| 1–2 | 187 | 3 (1.6%) | 21% |
| 3–4 | 668 | 40 (6.0%) | 29% |
| 5–6 | 479 | 24 (5.0%) | 36% |

The 41 recorded failure summaries cluster into (a) stale references in other files, (b) runtime behavior (crash on load, form 404, device gesture conflicts), and (c) unsupported claims or figures. Two of the three d1–2 catches were real defects (a Netlify form 404 at runtime; a stale unsupported figure carried forward).

**Known gaps:** almost all data predates Opus 5.5 (September 2026 has 60 tasks, 1 catch). No token-cost data exists yet; the `cost` field starts accruing with v5.5.2. Phase-level verification exists as a later backstop, but its catch rate for defects that per-task verification would have caught is unmeasured.

## Additional evidence (research, 2026-09-27)

Full methodology and findings: `decisions/.archive/decision-025-research-2026-09-27.md`. Headlines beyond the Background:

- **The low d1–2 rate is statistically real** (1.6%, 95% CI 0.55–4.6%, vs 5.4% at d3–6; one-sided Fisher p ≈ 0.012). Difficulty does discriminate verification yield.
- **d1–2 is not "trivial docs."** 43% of non-human d1–2 tasks had a runtime surface (`runtime_validation` pass/partial). The September (Opus 5.5-era) d1–2 tasks are nearly all one-file web-UI fixes from `/audit-ui` findings: 21 of 23 had runtime validation.
- **Savings are capped.** One batch per project-day would save ≤89 of 1,396 verify dispatches (**6.4%**). The safe hybrid saves 35 (**2.5%**).
- **Fixed per-dispatch overhead is probably the real cost driver.** This is an estimate, not a measurement. Every verify dispatch reads all of `verify-agent.md` (43.5 KB, about half of it the phase-level workflow) plus about 56 KB of auto-loaded CLAUDE.md and rules. That is roughly 25K tokens before any task work, and prompt caching may discount it.
- **The d1–2 catches came through T2c (stale cross-file references) and T4b (runtime)**, which are the steps a "lightweight profile" would skip.
- **Phase-level verification is a weak backstop for this defect class.** Across the downstream git history, only one project's phase-level runs ever created fix tasks (13), and none traced back to a d1–2 task. Phase-level verification leans on per-task results as evidence.
- **The status quo is already being routed around.** styler has an auto-memory rule to implement inline and "run verification yourself (or skip…)" for small scope. `verification_history` has `"orchestrator rollup"` and `"inline (subagent tool unavailable)"` entries. This is FB-119's failure mode.
- **Batching collides with existing mechanics.** "Awaiting Verification is transitional" (task-management rule) and the routing priority would both change. 35% of d1–2 tasks are dependencies of other tasks, and those dependents stall. `dashboard-render.py` counts Awaiting Verification as *verification debt*, so a waiting batch shows up on the Needs-you card. T2b scope attribution across N tasks is lost. One timeout blocks all N tasks. Batching also muddies the per-dispatch `cost` data this decision is waiting on.

## Options Comparison

Scoring: ✓✓ strong / ✓ adequate / – neutral / ✗ weak / ? unmeasured.

| Criteria | A — Status quo | B — Batched d≤2 (plain / hybrid) | C — Lightweight profile | D — Defer + gate | E — Trim fixed overhead |
|----------|:--:|:--:|:--:|:--:|:--:|
| Defect-catch coverage retained | ✓✓ | ✓ plain (same checks, diluted context) / ✓✓ hybrid | ✗ trims the steps that caught d1–2 defects | ✓✓ | ✓✓ |
| Cost / dispatch savings | – baseline | ✓ ≤6.4% plain / – ≤2.5% hybrid | ? unmeasured; effort lever weaker on 5.5 | – none until gate | ✓ ~5K tokens off *every* per-task dispatch (est.) |
| Invariant integrity (Finished ⇔ pass) | ✓✓ | ✓ if per-task results are written | ✓ formally; a d≤2 "pass" means less | ✓✓ | ✓✓ |
| Complexity / blast radius | ✓✓ none | ✗ routing, rules, deps, dashboard, schema, recovery (~18 files reference Awaiting Verification) | – profile + named-agent migration or new definition | ✓✓ one gate line | ✓ verify-agent split + 3 dispatch prompts |
| Failure-mode risk | ✓✓ known | ✗ timeout blocks N tasks; scope attribution lost; dependents stall | – silent under-verification | ✓✓ | ✓✓ |
| User-facing UX | ✓✓ nothing new | ✗ visible waiting state, "debt" on Needs-you, flush concept | ✓✓ invisible | ✓✓ invisible | ✓✓ invisible |
| Evidence strength | n/a | value weak / safety moderate | value weak / safety weak | ✓✓ matches evidence | value weak (estimate) / safety high |
| Counters FB-119-style drift | ✗ | ✓ sanctioned cheap path | ✓ | – temporarily ✗ | ✓ cheaper dispatch |
| **Overall** | viable fallback | **not yet** (cost/benefit unproven, large surface) | **not recommended** | **▲ recommended** | **▲ optional companion** |

**Recommendation (not a selection): D, optionally paired with E.** Confidence is **high** on rejecting C, **moderate** on D over B, and **low-moderate** on shipping E before cost data exists.

- **Safety:** every option except C keeps the full check set. C removes the steps that produced the d1–2 catches.
- **Value:** B's best case is 2.5–6.4% of dispatches. Its token value is unknown, and the v5.5.2 `cost` field will measure it. Shipping B now would also corrupt that measurement.
- **E** targets the likely real cost driver with no coverage or invariant change.

**Proposed gate for D (the thresholds are the user's to set):** re-open at ≥50 d1–2 verify dispatches with `cost` on Opus 5.5, or on 2026-12-31, whichever comes first. **Flip to B-hybrid** only if all three hold:

- d1–2 tasks take >~10% of total verify tokens.
- The d1–2 median cost is ≥70% of the d3–6 median, which would mean cost is dominated by fixed overhead.
- The d1–2 catch rate stays ≤2%.

Otherwise, close as A.

**Flip conditions:**

- **B-hybrid now** if serial-dispatch latency in autonomous batches is the real pain and you accept the UX and blast-radius cost.
- **E alone, no gate** if you'd rather not revisit this at all.

## Option Details

### Option A — Status quo
**Description:** One fresh-context verify-agent dispatch per task, full T1–T8, all difficulties.
**Strengths:** Maximum coverage. It is the known, tested path, and nothing changes for the user. It matches the Opus guides' endorsement of the independent writer-verifier pattern (their anti-verification guidance targets *self*-verification).
**Weaknesses:** Per the Opus 5 guide, delegating small tasks "multiplies cost and time". The status quo is already producing unsanctioned inline shortcuts downstream (FB-119, the styler memory rule).
**Would touch:** nothing.
**Research Notes:** archive § F7, F8.

### Option B — Batched verification for d≤2
**Description:** d≤2 tasks accumulate in Awaiting Verification. One verify-agent dispatch covers the batch and returns an **array of per-task reports**, so each task keeps its own `task_verification`, attempts, and reopen. The batch flushes at the batch end, before phase-level verification, at a count threshold, or when a dependent task needs dispatch. The **hybrid** keeps these tasks on the per-task path: runtime-surface tasks (T4b applicable), ≥3-file tasks, and tasks with pending dependents.
**Strengths:** Removes repeated fixed overhead and serial waits. Keeps the full check set and the independent context. Fail attribution stays per task.
**Weaknesses:**
- Savings are capped at 6.4% of dispatches (2.5% for the hybrid).
- Breaks the "Awaiting Verification is transitional" contract and the routing priority rule.
- Stalls dependents: 35% of d1–2 tasks have dependents.
- The dashboard shows a waiting batch as verification debt.
- T2b scope validation can't attribute undeclared files to a specific task.
- One timeout blocks every task in the batch.
- Muddies the per-dispatch `cost` data.
- The hybrid exempts most current d1–2 volume, which is runtime UI fixes.

**Would touch:**
- `commands/work.md`: routing step 3, § If Verifying (Per-Task), auto-continuation
- `support/reference/work-procedures.md`: per-task persistence loop, cost apportioning
- `agents/verify-agent.md`: a new batch mode, schema and turn budget
- `support/reference/parallel-execution.md`
- `rules/task-management.md`
- `support/reference/task-schema.md` + `shared-definitions.md`: a batch id
- `scripts/dashboard-render.py`: debt semantics, plus tests
- `support/reference/session-recovery.md` + `context-transitions.md`: pause/flush
- `commands/status.md`, `commands/health-check.md`
- `tests/scenarios/`

**Research Notes:** archive § F3, F9.

### Option C — Lightweight verify profile for d≤2
**Description:** Still one dispatch per d≤2 task, with a reduced step set (for example, T2c and T4b only when triggered) and/or a lower-effort custom agent definition.
**Strengths:** No new states and nothing visible to the user. The Opus 5 guide says review accuracy "holds at lower effort settings".
**Weaknesses:**
- The trimmed steps (T2c stale references, T4b runtime) are where two of the three d1–2 catches came from.
- "Light" framing risks literal under-reporting (Opus 5 guide: "be conservative" → reports less).
- The effort lever needs a named agent definition, which conflicts with the `general-purpose` Dispatch Convention and its pending migration gate.
- Opus 5.5 already inherits `medium` session effort (≈ Opus 5 `high`), so the marginal saving is small.
- A d≤2 "pass" would silently mean less.

**Would touch:** `agents/verify-agent.md` (profile section) or a new `agents/verify-agent-lite.md` with `effort:`; the dispatch site in `work.md` + `parallel-execution.md`; `rules/agents.md § Dispatch Convention`.
**Research Notes:** archive § F5, F8.

### Option D — Defer with explicit recheck gate
**Description:** Keep the status quo. Record a dated, measurable gate: ≥50 d1–2 dispatches with `cost` on Opus 5.5, or 2026-12-31. Re-decide from token share, median cost ratio and catch rate, as set out in the Recommendation.
**Strengths:** No surface change. It lets v5.5.2's `cost` field supply the missing value evidence, which matches the maintainer's "empirical validation before adopting" preference and keeps safety confidence separate from value confidence.
**Weaknesses:** The FB-119 drift continues until the gate fires. It needs someone to actually run the recheck, so it should be a dated Active Follow-ups entry.
**Would touch:** root `CLAUDE.md` § Active Follow-ups (the gate entry); this record.
**Research Notes:** archive § Recommendation.

### Option E — Trim fixed per-dispatch overhead (added by research)
**Description:** Split `verify-agent.md` so per-task dispatches read only the per-task workflow, for example by moving phase-level into its own file read only in phase-level mode. That removes roughly 5K tokens (estimated) from every per-task dispatch. Optionally, audit what else a verifier must load.
**Strengths:** Cheaper verification at every difficulty, with no change to coverage, the invariant or UX. It is independent of the d1–2 question and may make it moot.
**Weaknesses:** The value is an unmeasured estimate, and caching may already absorb it. It is a moderate doc refactor, and cross-references to verify-agent section names need a sweep.
**Would touch:** `agents/verify-agent.md` (+ a new phase-level file); the three dispatch prompts in `work.md` / `parallel-execution.md`; references to `verify-agent.md § Step 7` / phase-level sections (for example `work-procedures.md`, `rules/spec-workflow.md`, `dashboard-regeneration.md`); `tests/scenarios/`.
**Research Notes:** archive § F4.

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision. This section is yours — Claude reads it but never overwrites it.*

**Constraints:**
- 

**Questions:**
- 


## Decision

**Selected:** Option D — Defer with an explicit recheck gate. Gate thresholds as proposed in the Recommendation. Option E deferred to the same gate rather than shipped now.

**Rationale:**
The evidence supports safety (the full check set catches real defects at d1–2, via T2c and T4b), but the value case for changing anything is unproven: B saves at most 2.5–6.4% of dispatches, C removes the steps that produced the d1–2 catches, and no cost data exists yet. v5.5.2's `verification_history[].cost` field supplies that data. E was weighed down on closer reading: most of the ~25K-token fixed overhead is auto-loaded CLAUDE.md and rules, which E doesn't touch; E removes an estimated ~5K tokens per dispatch, so it waits for the same cost data. The more urgent finding is the downstream bypass of per-task verification (styler memory rule, "orchestrator rollup" entries), which is FB-119's territory and is addressed there, not here.


## Trade-offs

**Gaining:**
- No surface change or new UX; the decision is made on measured cost instead of estimates.

**Giving Up:**
- Any d1–2 dispatch savings until the gate fires (at most 2.5–6.4% of dispatches).
- FB-119-style drift continues until FB-119 is resolved separately.

## Impact

**Implementation Notes:**
No shipped-file change. Add the gate to root `CLAUDE.md § Active Follow-ups`. At recheck: mine downstream `verification_history[].cost` by difficulty and apply the Recommendation's three conditions (flip to B-hybrid only if all hold; otherwise close as A). Re-evaluate E with the same data.

**Affected Areas:**
- *(Research note, not a decision: per-option file surfaces are listed under each option's "Would touch" in Option Details.)*

**Risks:**
- The gate is only as good as downstream projects syncing v5.5.2 and logging `cost`. If fewer than 50 costed d1–2 dispatches exist by 2026-12-31, re-decide on what exists rather than extend silently. 
