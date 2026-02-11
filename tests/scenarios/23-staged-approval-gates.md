# Scenario 23: Staged Approval Gates (Production Blocking)

Verify that `/work` respects explicit user-defined gates that block entire project stages until manual approval.

## Context

Some projects have hard gates between stages — a research project might require explicit user sign-off before moving from pilot to production, regardless of whether all pilot tasks are complete. These gates are stronger than phase transitions: they require documented approval, not just task completion.

## State

- Spec has 3 stages: Specification (complete), Pilot Evaluation (active), Production (blocked)
- A gate document defines conditions for production entry:
  - All pilot tasks complete
  - All pilot tests pass
  - User has explicitly approved production rollout
- All pilot tasks are complete and verified
- User has NOT given production approval (no checkbox checked in gate doc)

## Trace 23A: Gate blocks task creation in next stage

- **Path:** `/work` → task dispatch after pilot completion
- All pilot tasks: completed
- Production gate: not approved

### Expected

- `/work` recognizes the stage gate and does NOT create or dispatch production tasks
- Dashboard clearly shows the gate: what's needed, what's satisfied, what's pending
- Message to user explains that production is blocked pending their approval

### Pass criteria

- [ ] Stage gate blocks task creation in the blocked stage
- [ ] `/work` does not proceed past the gate without approval
- [ ] User is informed about what's blocking and what action is needed

### Fail indicators

- Production tasks are created or dispatched despite missing approval
- `/work` treats the gate like a regular phase transition (auto-proceeds)
- No indication to user that a gate exists or what it requires

---

## Trace 23B: Gate conditions are enumerated

- **Path:** dashboard.md → gate status display
- Gate has 3 conditions, 2 satisfied (tasks complete, tests pass), 1 pending (user approval)

### Expected

- Dashboard enumerates each gate condition with its status
- Satisfied conditions shown as complete (checkmarks)
- Pending conditions highlighted with required action
- User knows exactly what to do to unblock production

### Pass criteria

- [ ] Gate conditions are individually listed in the dashboard
- [ ] Satisfied vs. pending conditions are clearly distinguished
- [ ] User action required is clearly specified with instructions

### Fail indicators

- Gate shown as a single "blocked" status without condition breakdown
- User doesn't know what specific action will unblock the gate
- Conditions are listed but without clear status indicators

---

## Trace 23C: Gate cannot be bypassed

- **Path:** Various commands attempting to work past the gate
- User runs `/work complete` on a pilot task (already complete)
- User runs `/work` with a specific production task ID

### Expected

- `/work complete` on already-complete tasks does not affect the gate
- `/work {production-task-id}` refuses to dispatch a task past an unapproved gate
- No command sequence bypasses the gate without explicit approval in the gate document

### Pass criteria

- [ ] Gate cannot be bypassed by `/work complete` or other commands
- [ ] Direct task ID targeting doesn't circumvent the gate
- [ ] Only explicit approval in the gate document opens the stage

### Fail indicators

- Clever command usage can bypass the gate
- `/work` dispatches production tasks if given a specific task ID
- Gate is advisory rather than enforced
