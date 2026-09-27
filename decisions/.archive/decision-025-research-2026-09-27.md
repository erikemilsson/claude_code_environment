# DEC-025 Research Archive — Per-task verification scaling for low-difficulty tasks (Opus 5.5 recalibration)

**Decision:** `decisions/decision-025-low-difficulty-verification-scaling.md`
**Date:** 2026-09-27
**Investigator:** research-agent (general-purpose, Opus 5.5), template-maintenance adaptation of `/research`
**Related:** DEC-004 (subagent capability contract / fresh-eyes), DEC-011, FB-119 (orchestrator unverified actor), v5.5.2 (self-review removal + `verification_history[].cost`)

---

## Methodology

**Shipped machinery read:** `.claude/agents/verify-agent.md` (Per-Task Workflow T1–T8, Turn Budget, Phase-Level Step 1); `.claude/commands/work.md` (routing algorithm Step 3, § If Executing, § If Verifying (Per-Task), Empirical Evidence Gate, autonomous batch heartbeat, § If Verifying (Phase-Level)); `.claude/support/reference/work-procedures.md` § State Persistence Protocol (incl. the uncommitted v5.5.2 `cost` edit); `parallel-execution.md` (per-implement verify dispatch loop); `task-schema.md` (`verification_history`); `rules/agents.md` (Context Separation, Dispatch Convention); `rules/task-management.md` ("Awaiting Verification is transitional"); `claude-code-authoring.md` (effort frontmatter, line ~151); `.claude/scripts/dashboard-render.py` (verification-debt computation); DEC-004; FB-119.

**Downstream data (read-only):** all `task-*.json` + `archive/*.json` under `/Users/erikemilsson/Developer/*/.claude/tasks/` (1,608 task files, 13 projects; 1,347 Finished-with-pass tasks carrying a difficulty); git history of every downstream `.claude/verification-result.json` (`git log` + `git show`, read-only); the styler auto-memory `feedback_inline_vs_agent_dispatch.md`; session exports in `interaction-logs/processed/` (keyword scans for verification-cost friction).

**External:** Anthropic "Prompting Claude Opus 5" (§ Task scope and over-verification, § Controlling subagent spawning, § Capability improvements — code review) and "Prompting Claude Opus 5.5" (§ Calibrate effort), both fetched 2026-09-27.

Mining script kept in the session scratchpad (not committed). "Caught" = any `verification_history` entry with `result: fail`, or `verification_attempts > 1` — same heuristic as the Background table, reproduced within ±2 (d3–4: 38 vs 40).

---

## Findings

### F1 — The low d1–2 catch rate is real, not noise (value evidence, moderate)

| Band | Verified tasks | Caught | Rate | 95% Wilson CI |
|---|---|---|---|---|
| d1–2 | 187 (167 non-human) | 3 | 1.6% | 0.55%–4.6% |
| d3–6 | 1,148 | 62 | 5.4% | 4.2%–6.9% |

One-sided Fisher exact test (d1–2 rate this low by chance, given the d3–6 rate): **p ≈ 0.012**. Difficulty at decomposition time *does* discriminate verification yield. However, the 3 catches were not noise: PortfolioWebsite #161 (Netlify form 404 at runtime), #172 (unsupported "€430M+" figure carried forward from a stale doc), OEMMatInsightBI task-039 (an acceptance criterion unmet: a marker not recorded outside `fabric/`).

### F2 — d1–2 is not "trivial docs"; the recent mix is mostly runtime-surface UI fixes (decisive for hybrids)

Of the 167 non-human d1–2 tasks, **71 (43%) had `runtime_validation` pass/partial**, 87 touched code/config (69 docs-only), and 27 touched ≥3 files. The **September 2026 d1–2 tasks** (the only Opus-5.5-era slice, n=24) are almost all PortfolioWebsite one-file web-UI fixes derived from `/audit-ui` findings (contrast ratios, nonexistent tokens, overflow on phones) — 21 of 23 claude-owned ones had `runtime_validation: pass`. So any "exempt runtime-surface tasks" escape hatch would exclude most of *current* d1–2 volume.

### F3 — The ceiling on savings is small in dispatch-count terms

Verify dispatches (≈ `len(verification_history)`), non-human tasks: **1,396 total, ~191 at d1–2 (13%)**. Simulating one batched verify per (project, completion-day):

| Variant | Eligible tasks | Catches inside eligible set | Dispatches saved | Share of all verify dispatches |
|---|---|---|---|---|
| B (all d1–2) | 167 | 3 | 89 | **6.4%** |
| B-hybrid (exclude runtime pass/partial, exclude ≥3 files) | 82 | 1 | 35 | **2.5%** |

d1–2 tasks cluster moderately: 83 project-days, 45 of them with a single d1–2 task (no batching gain there).

### F4 — But per-dispatch cost is probably dominated by fixed overhead (cost evidence, weak — estimate only)

Every per-task verify dispatch reads `verify-agent.md` in full (43.5 KB ≈ 11K tokens; roughly half is the Phase-Level workflow, irrelevant in per-task mode) on top of the auto-loaded `.claude/CLAUDE.md` + 7 imported rules (~56 KB ≈ 14K tokens) and the project root `CLAUDE.md`. So a d1–2 verify likely spends ≥25K tokens before touching the task. **This is a chars/4 estimate; prompt caching may discount it substantially; no measured data exists** — the v5.5.2 `cost` field is exactly what will settle it. Implication: batching's saving per avoided dispatch may be larger than a "d1–2 is small" intuition suggests — *and* the same overhead could be cut for every difficulty without touching coverage (→ Option E).

### F5 — Where the d1–2 catches came from is exactly what Option C would trim

The catch taxonomy (Background: stale cross-file refs / runtime behavior / unsupported claims) maps onto **T2c (cross-file consistency)** and **T4b (runtime validation)** — the two steps a "lightweight profile" would skip unless triggered. Two of three d1–2 catches came through those channels (#161 runtime; #172 stale carried-forward figure). Opus 5 guide also warns that review prompts saying "only report high-severity issues" / "be conservative" are followed literally and report less — a "light" framing risks suppressing findings, not just steps.

### F6 — Phase-level verification is a weak backstop for d1–2-class defects (unmeasured, directional)

Git history of downstream `verification-result.json`: 27 recoverable versions across 7 projects; **only OEMMatInsightBI's phase-level runs ever created fix tasks** (13: 057–063, 076–081). None trace to a d1–2 originating task; they are spec-drift, live-state, and cross-artifact findings. A heuristic scan of later "fix/stale/wrong/…"-titled tasks referencing an earlier verified task found 1 referencing a d1–2 task vs 30 (d3–4) and 28 (d5–6) — consistent with d1–2 escaping rarely, but also showing phase-level focuses on acceptance criteria, not per-file detail (verify-agent Phase-Level Step 1 explicitly *leans on* per-task results as evidence). One instructive case: OEM task-078 — a defect per-task verify flagged only as *minor* on d4 task-074, which phase-level later re-derived and escalated. So "passed with minor issues" (21% at d1–2) is a real leak path independent of this decision.

### F7 — Orchestrators are already routing around per-task dispatch for small work (drift evidence)

styler's auto-memory `feedback_inline_vs_agent_dispatch.md` (scope <500 LOC / <5 files → implement inline, "run verification yourself (or skip if the task explicitly doesn't need it)"). `verification_history` entries include `"method": "inline (subagent tool unavailable)"`, `"verifier": "orchestrator rollup"`, `"implement-agent collaborative self-attestation"`. FB-119 documents the resulting harm (inline work failing verification on the exact defect class). **Implication:** leaving the d1–2 cost unaddressed doesn't preserve the invariant in practice — it pushes projects to invent unsanctioned shortcuts. A sanctioned cheaper path (B) or a cheaper dispatch (E) is arguably *safer* than status quo drift. This is the strongest argument against pure A/D-forever.

### F8 — Anthropic guidance cuts both ways

- *For keeping a separate verifier:* "Claude Opus 5 coordinates teams of subagents well, with effective writer-verifier patterns." The anti-verification guidance targets *self*-verification instructions and "legacy harness scaffolding that adds separate verification steps" — verify-agent is independent-context, which DEC-004 treats as the load-bearing property.
- *For reducing dispatch count:* "Delegation … multiplies cost and time when applied to small tasks… Do not delegate work you can finish yourself in a handful of tool calls." A d1–2 verification is often a handful of tool calls.
- *For a lower-effort pass:* Opus 5 code review "accuracy holds at lower effort settings, which supports a fast pass at review time and a more thorough pass later"; Opus 5.5 at `medium` (its default) ≈ Opus 5 at `high`.
- *Mechanism constraint:* per `claude-code-authoring.md`, effort is settable only via a named agent definition's `effort:` frontmatter; the template dispatches `subagent_type: "general-purpose"` (Dispatch Convention, named types deferred pending a validation gate). So C's effort lever requires either that migration or a second named definition. Under Opus 5.5, dispatches already inherit session effort (default `medium`), so the marginal effort saving is smaller than it was on Opus 5.

### F9 — Batching collides with several existing mechanics (blast radius / failure modes)

- **Routing + rules:** `work.md` routing step 3 ("Any spec task in Awaiting Verification → verify first; priority order matters") and `task-management.md` ("Awaiting Verification is transitional — must proceed to verification immediately") must both change.
- **Dependents stall:** 58 of 167 d1–2 tasks (35%) are a dependency of another task; dependency satisfaction requires `Finished`. A batch must flush before any dependent dispatches, or deps semantics must change.
- **Dashboard false alarm:** `dashboard-render.py` counts `Awaiting Verification` as *verification debt* (META + Needs-you) — a deliberately waiting batch would surface as debt unless the renderer learns the batch state.
- **Scope-validation attribution:** T2b computes undeclared files via `git diff` of the whole tree; with N tasks in one verifier context, an undeclared file cannot be attributed to a specific task → the scope check weakens.
- **Timeout blast:** one verifier timeout (`max_turns`) marks *every* batched task Blocked/`[VERIFICATION TIMEOUT]`; turn budget must scale with N.
- **Fail attribution itself is fine** if the report is an array of per-task reports (each task keeps its own `task_verification`, attempts, reopen). The risk is context-dilution, not ambiguity.
- **Cost measurement:** v5.5.2 records `cost` per dispatch per task; a batch dispatch covers N tasks, so cost must be apportioned or tagged with a batch id — shipping B *now* would muddy the very data this decision is waiting for.
- **Pause/recovery:** session-recovery Case 1 re-spawns per task; a half-accumulated batch at `/work pause` needs defined flush semantics. `Awaiting Verification` is referenced in 18 shipped files (task-schema 7, dashboard-render.py 5, status 4, health-check 4, …).

---

## Options

- **A — Status quo.** One verify dispatch per task, all difficulties.
- **B — Batched verification for d≤2** (optionally hybrid: runtime-surface / ≥3-file / has-pending-dependents tasks stay per-task). One verify dispatch returns an array of per-task reports.
- **C — Lightweight verify profile for d≤2.** Still one dispatch per task; reduced step set (skip T2c/T4b unless triggered) and/or lower-effort named agent.
- **D — Defer with explicit recheck gate.** Status quo until `cost` data exists on Opus 5.5.
- **E — Trim fixed per-dispatch overhead (added by research).** Split `verify-agent.md` so per-task dispatches read only the per-task workflow (~half the file); optionally slim what a verifier must load. Applies to all difficulties; zero coverage/invariant change. Added because F4 suggests fixed overhead, not d1–2 task content, is where per-task cost likely concentrates. Complementary to D.

**Considered and dropped:** *Orchestrator-inline verification for d1–2* — violates DEC-004 context separation and is the FB-119 failure mode; *skip per-task verification entirely for d1–2 and rely on phase-level* — breaks the Finished invariant and F6 shows phase-level is a weak backstop; *self-attestation by implement-agent* — same-context "double-check" the Opus guides name as wasteful, and it is not independent.

## Comparison (✓✓ strong / ✓ adequate / – neutral / ✗ weak)

| Criterion | A | B (plain) | B-hybrid | C | D | E |
|---|---|---|---|---|---|---|
| Defect-catch coverage retained | ✓✓ | ✓ same checks, context dilution | ✓✓ runtime/multi-file stay per-task | ✗ trims T2c/T4b = where d1–2 catches came from (F5) | ✓✓ | ✓✓ |
| Cost / dispatch savings | – baseline | ✓ ≤6.4% dispatches | – ≤2.5% dispatches | ? per-dispatch saving unmeasured; effort lever weaker on 5.5 | – none now | ✓ est. ~5K tokens × every per-task dispatch (unmeasured) |
| Invariant integrity (Finished ⇔ pass) | ✓✓ | ✓ preserved if per-task results written | ✓ | ✓ preserved, but "pass" means less at d≤2 | ✓✓ | ✓✓ |
| Implementation complexity / blast radius | ✓✓ none | ✗ routing, rule text, deps, dashboard debt, schema, recovery, 18 files | ✗ same + eligibility logic | – verify-agent profile + named-agent migration or new definition | ✓✓ one recheck gate line | ✓ verify-agent split + dispatch prompts |
| Failure-mode risk | ✓✓ known | ✗ timeout blasts N tasks; scope attribution; dependent stalls | – same, smaller N | – silent under-verification | ✓✓ | ✓✓ |
| User-facing UX | ✓✓ nothing new | ✗ tasks wait visibly in Awaiting Verification; "debt" on Needs-you; flush concept | ✗ same + "why was this one batched?" | ✓✓ invisible | ✓✓ | ✓✓ invisible |
| Evidence strength | n/a | value: weak (no cost data); safety: moderate | value: weak; safety: moderate-high | value: weak; safety: weak (F5 against) | ✓✓ matches evidence state | value: weak (estimate); safety: high |
| Addresses FB-119-style drift (F7) | ✗ | ✓ sanctioned cheap path | ✓ | ✓ | – temporarily ✗ | ✓ cheaper dispatch |

## Recommendation

**D (defer with an explicit, data-driven recheck gate), optionally paired with E now.** Confidence: **high on rejecting C**, **moderate on D over B**, **low-moderate on whether E is worth shipping before the cost data lands**.

Reasoning:
1. **Safety vs value separated.** Safety: all options but C keep full checks; C cuts exactly the steps (T2c/T4b) that produced d1–2 catches. Value: the realistic upside of B is 2.5–6.4% of verify dispatches; its token upside is unknown and is precisely what `verification_history[].cost` (v5.5.2) will measure. Shipping B now would also corrupt that measurement (a dispatch covering N tasks).
2. **B's blast radius is disproportionate to a ≤6.4% saving**: it rewrites the "Awaiting Verification is transitional" contract, routing priority, dependency flow, dashboard debt semantics, and recovery — and adds a user-visible "batch waiting" state.
3. **The recent d1–2 population is runtime-surface UI work (F2)**, so the safe hybrid saves only ~2.5% — the hybrid is where B is safe, and it's where B is least worth it.
4. **E attacks the likely real cost driver (F4) without any coverage or invariant change**, and makes every dispatch cheaper including d1–2. It is optional: if the cost data shows caching already neutralizes fixed overhead, E is unnecessary.
5. **Why not A-forever:** F7 shows the status quo already drives unsanctioned inline shortcuts; the gate must be real, with a date.

**Proposed recheck gate (for D):** re-open when either (a) ≥50 d1–2 verify dispatches carry `cost` on Opus 5.5, or (b) 2026-12-31 — whichever first. Measure: d1–2 share of total verify tokens and median d1–2 tokens/dispatch vs d3–6. **Flip to B-hybrid** if d1–2 exceed ~10% of verify tokens *and* d1–2 median cost is ≥70% of d3–6 median (fixed-overhead-dominated) *and* the d1–2 catch rate stays ≤2%. Otherwise close as A. (Thresholds are research proposals — the user should set them.)

**Flip conditions:** choose **B-hybrid now** if you weight dispatch latency in long autonomous batches heavily (each avoided dispatch is a serial wait) and accept the UX/blast-radius cost. Choose **E alone** (no gate) if you'd rather stop revisiting this and just make every dispatch cheaper.

## Open questions for the user

1. Is latency (serial waits in autonomous batches) or token/usage-limit cost the pain you're actually feeling? B helps latency; E helps tokens; neither helps much if the pain is elsewhere.
2. Accept the proposed recheck gate numbers (50 dispatches / 2026-12-31; 10% token share; ≤2% catch rate), or set your own?
3. Ship E now, or wait for cost data to show fixed overhead matters (caching may already absorb it)?
4. Should FB-119's "which dispatches are invariants" rule (verify-agent always separate) be written first, so any later B/C lands inside an explicit invariant?
5. Separately from this decision: the 21% "passed with minor issues" rate at d1–2 (and OEM task-074→078) suggests minor issues are a leak path — worth a follow-up FB?

## Sources

- Anthropic, Prompting Claude Opus 5: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 — § Task scope and over-verification; § Controlling subagent spawning; § Capability improvements (code review at lower effort; writer-verifier patterns).
- Anthropic, Prompting Claude Opus 5.5: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 — § Calibrate effort (medium default; medium ≈ Opus 5 high).
- Downstream task data: 13 projects under `/Users/erikemilsson/Developer/*/.claude/tasks/` (read-only), mined 2026-09-27.
