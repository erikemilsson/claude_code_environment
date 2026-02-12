# Scenario 04: Pick-and-Go Decision Unblocks Without `/iterate`

Verify that a non-inflection decision unblocks tasks immediately, contrasting with the inflection point flow in Scenario 03.

## State

- Phase 1: 3 tasks, all "Finished"
- Phase 2: 3 tasks, all "Finished"
- Phase 3: 2 tasks, Pending, `decision_dependencies: ["DEC-002"]`
- DEC-001: `status: implemented` (already done)
- DEC-002: `status: approved`, selected: "matplotlib", `inflection_point: false`

## Trace: `/work` post-decision handling (pick-and-go)
- DEC-002: `inflection_point: false` → pick-and-go branch
- Unblock dependent tasks, continue to dispatch

### Expected

```
Decision DEC-002 (Charting Library) resolved: matplotlib selected.
Phase 3 tasks are now unblocked.
Dispatching Phase 3 work...
```

- Phase 3 tasks dispatched immediately
- No pause for `/iterate`
- No user confirmation needed

## Contrast with Scenario 03

| Aspect | Pick-and-go (this) | Inflection point (Scenario 03) |
|--------|-------------------|-------------------------------|
| After resolution | Unblock + execute | Pause + direct to /iterate |
| Spec changes needed? | No | Yes |
| User steps | 2 (resolve → /work) | 4+ (resolve → /work pause → /iterate → spec edit → /work) |
| Controlled by | `inflection_point: false` | `inflection_point: true` + `spec_revised` |

## Pass criteria

- [ ] DEC-002 resolution detected
- [ ] Does NOT pause for `/iterate`
- [ ] Phase 3 tasks dispatched immediately
- [ ] Decision acknowledged briefly before continuing
- [ ] Two-step flow: resolve → /work → execution starts

## Fail indicators

- Pauses and says "run /iterate" (wrong — not an inflection point)
- Doesn't mention the decision resolution (user confused why Phase 3 started)
- Asks user to confirm before proceeding
- Phase 3 tasks remain blocked
