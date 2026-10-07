# /work Recovery Procedures

<!-- Loaded on demand by commands/work.md: read only when the trigger line in /work points here. -->

Conditional `/work` procedures that run only when a prior session left something behind. `/work` states each trigger; read the matching section then.

## Friction-Marker Catchup (Step 0d)

Reconcile any friction markers persisted to the transient pending buffer in a prior session that never reached the canonical log (DEC-011 Option ABp). Runs once per `/work` invocation, before any agent dispatch.

**Procedure:**

1. If `.claude/support/workspace/.pending-markers.jsonl` does not exist, this step is a no-op — proceed to Step 1.
2. Read both files (create `.session-log.jsonl` empty if missing):
   - `.pending-markers.jsonl` — append-only buffer dual-written at agent-return time
   - `.session-log.jsonl` — canonical log
3. Build a dedup set from `.session-log.jsonl` entries using the composite key: `(task_id, timestamp, type, sha256(details))`. For entries missing any of these fields, fall back to `sha256(full_json_line)`.
4. Iterate `.pending-markers.jsonl` entries. For each entry NOT already in the dedup set, append to `.session-log.jsonl`.
5. Count appended entries. If count > 0, surface inline: `Step 0d: Caught up {N} friction markers from prior session.` (Inform — not an error.)
6. After successful merge, truncate `.pending-markers.jsonl` (write empty file) — the canonical log now holds the entries.
7. If the merge fails (read error, write error), do NOT truncate. Surface inline: `Step 0d: Catchup failed ({error}). Pending buffer preserved for retry.`

**Why this exists:** The "After implement-agent returns" protocol Step 2 dual-writes markers to both the pending buffer and the canonical log immediately upon agent return. The pending buffer's purpose is purely the sub-second window where the orchestrator could be terminated between agent return and writes completing. Step 0d guarantees that any markers in the pending buffer that didn't make it to the canonical log are reconciled before the next agent dispatch.

**Composability with PreCompact hook:** `.claude/hooks/pre-compact-handoff.sh` runs the same catchup before its Track 1 export compile. The two entry points (here + PreCompact) cover both "normal /work resume" and "compaction-triggered wind-down" paths.

## Stale Track 2 Recovery (Step 0f)

Recover from a prior session's interrupted `/work pause` that left `.claude/support/workspace/.interaction-assessment.json` on disk. Without recovery, next session's Write tool fails on that path because the file exists but hasn't been Read.

**Procedure:**

1. If `.claude/support/workspace/.interaction-assessment.json` does not exist, this step is a no-op — proceed to Step 1.
2. Read the file. If invalid JSON, surface inline `Step 0f: Stale Track 2 capture malformed — discarded.`, delete, proceed to Step 1.
3. Read `.claude/support/workspace/.session-log.jsonl` if present (Track 1 markers also orphaned from same interrupted pause), plus each `.pending-markers.jsonl` entry it lacks, deduped on the Step 0d key above (normally none, since Step 0d ran first; folding covers a failed catchup, so step 9 can clear the buffer losslessly, FB-120).
4. Read `.claude/version.json` for `template_version` + `template_inbox_path`.
5. Compile a recovered export matching `/work pause § Session Export` shape:
   ```json
   {
     "export_version": 1,
     "source_project": "[project name]",
     "template_version": "[from version.json]",
     "session_date": "[YYYY-MM-DD from current date]",
     "automated_markers": [/* from step 3, else [] */],
     "session_metrics": {
       "tasks_completed": [computed from current task files],
       "verification_pass_rate": [computed; null when no task has a verification result],
       "recovery_events": 0
     },
     "claude_assessment": [/* parsed Track 2 JSON */],
     "export_quality": "recovered"
   }
   ```
6. Compute timestamp `YYYY-MM-DD-HHMM` (minute-granular per FB-079).
7. Write the recovered export to `.claude/support/workspace/.session-export-{timestamp}-recovered.json`.
8. If `template_inbox_path` is configured, copy the export to the inbox via the deterministic helper (FB-109) — pass `--suffix recovered` so the inbox copy carries the `-recovered` marker:
   ```bash
   python3 .claude/scripts/persist-session-export.py --source .claude/support/workspace/.session-export-{timestamp}-recovered.json --suffix recovered
   ```
   Never `cp` the dot-prefixed working filename to the inbox verbatim (see `context-transitions.md § "Session Export"` step 6).
9. Delete `.interaction-assessment.json`, `.session-log.jsonl` AND `.pending-markers.jsonl`. Delete the step 7 working copy too when step 8 ran and the script exited `0` printing `"copied": true`; otherwise keep it — it is then the only copy (mirrors `context-transitions.md § "Session Export"` step 7).
10. Surface inline: `Step 0f: Recovered stale Track 2 capture from interrupted pause → {the inbox file, or the kept .session-export-{timestamp}-recovered.json}` (Inform — not an error.)
11. Proceed to Step 1.

**Why this exists:** `/work pause § Session Export step 7` cleans up `.interaction-assessment.json` after compiling the export. If pause is interrupted between the write (Interaction Assessment sub-section) and step 7 cleanup — usage limit, user `Ctrl+C`, harness crash — the file persists. Observed in echothread 2026-05-17.

**Why `export_quality: "recovered"` is a new enum value:** distinguishes recovered exports (`session_metrics` computed at recovery time, not at original pause time — lossy property) from canonical exports. Coexists with `"full"` (canonical `/work pause`) and `"markers_only"` (PreCompact hook fallback).

**No PreCompact hook coordination needed:** the hook never reads `.interaction-assessment.json` (it writes `claude_assessment: None` and produces markers-only exports). Step 0f and the hook operate on disjoint Track 2 territory — no double-ingestion risk.

**`.session-log.jsonl` standalone case:** if Track 2 is absent but Track 1 markers exist, Step 0f does NOT trigger recovery — Step 0d's catchup already handles the pending-buffer half, and the PreCompact hook is the canonical disposal mechanism for orphan logs.

## Resume-Pending Dispatch (DEC-010)

**Resume-pending check (per DEC-010):** if the selected task JSON has a `partial_completion` field from a previous dispatch:

1. Read the envelope's `completed_subtargets`, `remaining_subtargets`, `resume_instructions`, `confidence`
2. Run a git-diff audit on the task's declared `files_affected`:
   - `git diff --name-only` (combined with `--cached` if needed)
   - If files in `files_affected` show no diff since the partial dispatch, surface inline: `⚠ Task {id} resume: declared-completed sub-targets show no file changes since partial. Audit may have rolled back. Continue? [Y/N]`
   - If files outside `files_affected` show diffs, surface inline: `⚠ Task {id} resume: {N} files modified since partial — review before resuming.`
   - Run the residue check (`work-procedures.md § "Residue check"`) for the dispatch that was cut, unless it already ran when that agent returned in this session: an agent that hit a limit may have left a server listening or probe files behind. When the cut dispatch belongs to an earlier session (a limit cutoff or crash ended it), there is no baseline and no report, so the check only reports (that section, "When the check only reports"): this session can't tell what that agent started. `session-recovery.md § "Residue From a Previous Session"` runs the same look during a full recovery scan, whether or not a task has `partial_completion`; if it already ran in this session, don't repeat it here.
3. When `confidence: low`, surface: `⚠ Task {id} resume: previous dispatch flagged low confidence in partial state. Spot-check before continuing.`
4. Inject the envelope content into the dispatch prompt for the re-dispatched implement-agent:
   ```
   RESUME-PENDING TASK. Previously completed sub-targets: {completed_subtargets}.
   Remaining sub-targets: {remaining_subtargets}.
   Resume instructions from previous dispatch: {resume_instructions}.
   Confidence in prior state: {confidence}.
   Before continuing, spot-check that the declared completed sub-targets are
   actually present in the deliverable. If any are missing, treat them as
   remaining_subtargets instead.
   ```
5. **After re-dispatch returns** `completed` or a fresh `partial_resume_pending`: clear the `partial_completion` field from the task JSON. (For fresh `partial_resume_pending`, the new envelope replaces the old.) The return is an agent return like any other: the residue check runs for it (`work-procedures.md § "Residue check"`).
