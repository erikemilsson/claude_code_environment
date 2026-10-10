# v5.14.7: template `DEC-`/`FB-` ids removed from shipped instruction files (FB-137)

**Status:** built and reviewed; release bookkeeping done; awaiting the user's OK to commit, tag and push.

## Measured (2026-10-10, read-only)

- Shipped markdown instruction files carry 381 template ids: commands 147, `support/reference/` 158, rules 24, `.claude/CLAUDE.md` 13, agents 9, vision 6, `.claude/README.md` 5, `scripts/README.md` 17, two support READMEs 2. 31 headings carry an id.
- PortfolioWebsite numbers its decisions around the template's ids (gaps 4, 5, 10, 11, 13, 16, 17, 19, 21–24) and wrote template ids into project state (DEC-016 28 times, FB-103 16, DEC-004 11). The "Numbering namespace" rule in `support/reference/decisions.md` (since v5.2.0) did not prevent it. No session tried to open a template record. Detail under FB-137 in `feedback.md`.

## Decisions (user, 2026-10-10)

1. Strip the template ids from shipped files, keeping each sentence and its reason; rationale stays findable through the ship-log and `git blame`. Parallel agents on scratch mirrors, one reviewer.

## Build contract

- **In scope:** every `.md` under `.claude/` except `support/feedback/archive.md` (a record file). **Out of scope:** scripts, tests, the hook, `sync-manifest.json` (code and data, not instruction text), `tests/` scenarios' own id citations, all root files.
- **Remove:** a `DEC-NNN` or `FB-NNN` that names a template record (template decisions are 001–025; template FB ids are whatever the text cites as its own history). Parenthetical: delete; "per DEC-016": delete the phrase; a sentence that is only a pointer ("See DEC-004 for the full rationale"): delete; where the id is the only name for a mechanism, use the descriptive phrase.
- **Keep:** placeholders (`DEC-NNN`, `DEC-{NNN}`, `FB-XXX`); ids that illustrate *project* records in examples, sample output and templates; `FR-`, `KI-` and task ids; code blocks unless the id is plainly a template citation in a comment.
- **Headings:** agents do not edit heading lines; the main session renames the 31 id-bearing headings and every `§ "…"` citation of them in one deterministic pass afterwards.
- **`support/reference/decisions.md` "Numbering namespace":** restated without the template-citation clause (new records take the next number after the project's own highest, archive included).
- **Split (no shared files):** A `commands/`; B `support/reference/`; C `CLAUDE.md`, `rules/`, `agents/`, `vision/`, `README.md`, `scripts/README.md`, `support/shakedowns/README.md`, `support/retired/README.md`.
- No behaviour, script or schema change. Scenario quotes of changed sentences are updated by the main session after copy-back.

## Amendments
1. Agents returned (their own counts, summing to 86; the main session's recount after the heading pass is 54 ids left in instruction files, from 381): A commands 147 → 51, B reference 158 → 26, C rest 76 → 9. Remaining ids are project examples and sample data. Copy-back by owned file list: 11 + 22 + 14 files.
2. Heading pass by the main session: 24 headings and two quoted labels lost their id, with every citation in `.claude/` and `tests/` updated in the same pass (23 files; scenarios 42, 43, 47, 49, 52).
3. `decisions.md` "Numbering namespace" restated: next number after the project's own highest record, `.archive/` included. The `template DEC-NNN` citation convention is gone with it; scenario 49's variant restated to match.
4. `decomposition.md`: the "Pattern origin: styler `DEC-082`" pointer removed (a downstream project's id; same reason).
5. Left as is: `support/feedback/archive.md` (record file), ids in `.py`/`.sh`/`.json`, version numbers that stood next to a removed id (e.g. `audit-coherence.md` "(historical proxy — v4.27.0)").
6. Review (one independent read-only pass over every hunk, no blocker). Applied after its pass, which it did not see: the `.archive/` clause removed from "Numbering namespace" (research archives carry no record number; the clause was the main session's instruction, not the agent's); "next free" → "next" in `decisions.md` and `work-procedures.md`; scenario 49 narrowed to "shipped instruction files"; root-path pointers to template decision files removed from `merge-queue.md` and `shakedown.md`; the edit guardrail has one name, "the spec-edit guardrail", anchored at `rules/spec-workflow.md` Enforcement; dangling referents removed in `diagnose.md` and `health-check.md`.
7. Left (reviewer notes): "a future DEC" and "telemetry gate" wording in the audit reference files; four `template-maintenance/audit-command-family-proposal.md` pointers; root decision records 016 and 022 quote the old heading texts; small out-of-contract rewordings by the agents listed in the review (punctuation, one passive, one label rename).
