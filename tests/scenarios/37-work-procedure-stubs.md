# Scenario 37: /work Procedure Stubs (v4.18.0 split)

Verify that the four procedures extracted from `work.md` (State Persistence Protocol, `/work complete`, Auto-Archive → `work-procedures.md`; Interaction Assessment + Session Export → `context-transitions.md § Pause Follow-Through`) are read at their STOP gates and executed from the canonical bodies — never improvised from the stubs.

## Context

v4.18.0 split work.md (Plan 2 P3): the orchestrator file had ~20 ship-log patches tracing to prose procedures skipped under load. The stubs keep the original section names (so internal references resolve) plus a STOP-read trigger and a summary of hard invariants. Failure modes guarded: executing an after-return protocol from the stub summary alone; pause completing without the Track 2 artifacts; `/work complete` skipping verification enforcement.

## State (Base)

- Mid-`/work` session; implement-agent just returned `implementation_status: "completed"` for Task 9
- Task 12 is `owner: "human"`, In Progress, no `task_verification`; user runs `/work complete 12`
- Later, user runs `/work pause`; `template_inbox_path` is configured

---

## Trace 37A: Agent return triggers the procedure read, full protocol executes

- **Path:** implement-agent returns → work.md § State Persistence Protocol stub → `work-procedures.md`

### Expected

- Before any state write, the orchestrator reads `work-procedures.md § "State Persistence Protocol"` (first agent return of the session; subsequent returns reuse the in-context copy)
- ALL protocol steps execute — including the ones the stub only summarizes: the DEC-011 dual-write (markers to `.pending-markers.jsonl` AND `.session-log.jsonl`, immediately, never deferred), audit-register projection for eligible kinds, decision persistence, then verify-agent dispatch
- After verify-agent returns: attempts/history/`task_verification` (+`evidence[]` if the gate ran), status transition, FB-086 drift update when flagged

### Pass criteria

- [ ] Procedure file read before the first state write of the session
- [ ] Dual-write happens at the return, not batched to pause (the DEC-011 invariant the stub alone can't carry)
- [ ] No after-return step improvised from the stub summary

### Fail indicators

- Markers appended only to `.session-log.jsonl` (single-write — the stub's summary mentions dual-write but not the mechanics; acting without the read produces exactly this)
- Status written before the procedure file was ever read

---

## Trace 37B: `/work complete` enforces verification via the canonical process

- **Path:** `/work complete 12` → work.md § Task Completion stub → `work-procedures.md § "Task Completion (/work complete)"`

### Expected

- The 10-step Process runs from the procedure file: validation, **self-attestation auto-generated** for the human-owned task (`checks: {"self_attested": "pass"}`), deliverable validation (`[A]/[P]/[W]` on mismatch), the two-prompt notes collection (template-notes prompt SHOWN since `template_inbox_path` is set), dashboard-marker fallback, task update, parent auto-completion, regen + unblocked surfacing, archive check, Step 5 validation

### Pass criteria

- [ ] No "Finished" without `task_verification.result == "pass"` (self-attested here)
- [ ] Both note prompts appear, each independently skippable
- [ ] Steps run in the canonical order, none invented or dropped

### Fail indicators

- Task marked Finished with no verification record
- Template-notes prompt skipped despite the configured bridge (or shown without one)

---

## Trace 37C: Pause completes the Track 2 follow-through from context-transitions.md

- **Path:** `/work pause` → handoff (Path A) → work.md stub → `context-transitions.md § "Pause Follow-Through"`

### Expected

- After the handoff write: `.interaction-assessment.json` written (correct schema), session export compiled (`export_quality: "full"`, minute-granularity filename per FB-079), copied to the configured inbox, then `.session-log.jsonl` + `.interaction-assessment.json` deleted
- The export shape comes from the procedure file, not memory

### Pass criteria

- [ ] All three artifacts in sequence; cleanup last
- [ ] Export filename carries HHMM (no same-day collision)
- [ ] Inbox copy happens exactly when `template_inbox_path` is set

### Fail indicators

- Pause ends after the handoff with no assessment/export (the stub treated as informational)
- Export schema fields missing or invented (acting without the read)
