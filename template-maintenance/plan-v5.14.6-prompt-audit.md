# v5.14.6: prompt-audit fixes (text written for older models)

**Status:** built and reviewed; release bookkeeping done; awaiting the user's OK to commit, tag and push.

## Source

`/checkup prompt-audit` run 2026-10-10 against Opus 5.5 over root `CLAUDE.md`, `.claude/CLAUDE.md`, 8 rules, 14 commands, 3 agents. `support/reference/` was outside the command's scope; four `/work`-loop reference files got a signal-search pass by hand afterwards.

## Decisions (user, 2026-10-10)

1. Root `CLAUDE.md` decision-count line fixed now (22 records, three `approved`).
2. Release findings 2, 3, 4 and 6; hold finding 5 (emphasis on `work.md:397,663,707`) until downstream transcripts are checked for skipped gates.
3. Finding 7 (template ids in shipped files) logged as FB-137, not built.
4. Hand pass over `work-procedures.md`, `parallel-execution.md`, `drift-reconciliation.md`, `phase-decision-gates.md`; bring a second list.

## Build contract

- `agents/verify-agent.md`: "Using the Think Tool" section removed (no such tool in Claude Code); "Reasoning Effort" reduced to the re-evaluate-after-each-check sentence and the phase-level `ultrathink` note.
- `agents/implement-agent.md`: "Reasoning Effort" becomes "By Difficulty", two bullets (1-2 and 5-6), no thinking-depth prose.
- `agents/research-agent.md`: "Reasoning Effort" section removed.
- Migration-relative wording rewritten as current fact: `rules/agents.md` (three "Moved to" stubs), `rules/session-management.md`, `.claude/CLAUDE.md` (Plans line), `commands/work.md:312`, `commands/audit-ui.md:186`.
- Incident and dated-model narrative dropped, reasons kept: `.claude/CLAUDE.md:7`, `rules/agents.md` (negative findings), `rules/task-management.md` (audit tasks), `rules/dashboard.md` (scaling).
- No behaviour, script or schema change. No test change expected.

## Amendments

1. `research-agent.md` was not in the audit report (the signal search missed its section); found by the pre-edit search for other "Reasoning Effort" sections and included under finding 3.
2. User decision 2026-10-10: three reference-file findings join the release. `work-procedures.md:3` (extraction history dropped, load rule kept), `drift-reconciliation.md:100` (old-fallback history dropped, reason kept), `parallel-execution.md:163` (incident becomes an unnamed example). Held with finding 5: the emphasis in `work-procedures.md:57`.
3. Review (one independent read-only pass, no blocker). Applied after its pass, which it did not see: scenario 44's quote of `work.md:312` updated; the last "interleaved thinking" clause removed (`implement-agent.md:59`); the `session-management.md` lead-in that duplicated its heading removed; `rules/agents.md` third stub names `mcp-patterns.md` again. The feedback id was wrong (193 came from a downstream id quoted in the archive); corrected to FB-137.
4. Reviewer's same-kind leftovers, not built (await a user decision): incident ids in `verify-agent.md:94`, `implement-agent.md:37,288`, `parallel-execution.md:203-204`, `session-management.md:24`; "originally validated on Opus 4.7" in `.claude/README.md:5` and `shared-definitions.md:18`; the "Reasoning Effort" heading in `verify-agent.md`.
5. User decision 2026-10-10 (leftovers, built after the review, not seen by the reviewer): `verify-agent.md` budget-guideline incident reduced to its fact and the heading renamed "Reasoning Across Checks"; `implement-agent.md:288` task id dropped; `session-management.md:24` "observed downstream" becomes an example; "originally validated on Opus 4.7" dropped from `.claude/README.md` and `shared-definitions.md`. Left as is: `implement-agent.md:37` (a reason, no incident id) and the `T463`/`T462` ids in `parallel-execution.md`'s sample blocks (illustrative values in a format example).
6. User decision 2026-10-10: finding 5 closed with no change. Measured on the transcripts on disk: the `work-procedures.md` body was read before the second dispatch in 14 of 15 Opus 5.5 `/work` sessions (7 of 12 on Opus 5); no ticked-but-unresolved decision in 232 records; both `complete` specs have a passing phase result. Numbers are under FB-137 in `feedback.md`.
