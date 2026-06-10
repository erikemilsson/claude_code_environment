# Scenario 40: Handoff Schema Cap (bounded index, not a memoir)

Verify the handoff bounds shipped v4.21.1 (Plan 3 T4a): `.handoff.json` stays a bounded index (~≤2.5KB; `session_knowledge` ≤ ~10 bullets; `recovery_action` ≤ ~3 sentences); overflow goes to a workspace file the handoff points at via `overflow_ref`.

## Context

Observed failure mode (styler, 2026-06-10 analysis): a 7.8KB hand-curated free-prose handoff blob — write-expensive, read-unreliable, and a hiding place for blocking questions (the T3 queue contract, v4.14.0, moved those to dashboard rows; this cap bounds what remains).

## State (Base)

A long session ends with `/work pause`: one partial task (7), two unanswered user questions (already swept to Action Required rows per the T3 contract), and ~18 distinct conversation insights worth preserving.

---

## Trace 40A: Rich session → bounded handoff + overflow file

- **Path:** `/work pause` → Path A → handoff write per `context-transitions.md § Schema` + `§ Bounds and Overflow`

### Expected

- `session_knowledge` written as an ARRAY of ≤ ~10 bullets (the most load-bearing of the 18), each ≤ ~25 words
- Excess insights land in `.claude/support/workspace/handoff-overflow-{date}.md`, organized by field name; `overflow_ref` set to that path
- `open_question_refs` holds POINTERS to the two Action Required rows — not the question text + discussion
- `recovery_action` ≤ ~3 sentences; total handoff ≈ ≤2.5KB

### Pass criteria

- [ ] Handoff is a bounded index; no field blows its cap
- [ ] Overflow file exists ONLY because content genuinely exceeded a bound
- [ ] Questions live in dashboard rows; handoff carries refs only

### Fail indicators

- A multi-KB `session_knowledge` prose blob (old shape)
- Insights silently dropped instead of overflowed
- `overflow_ref` null while bullets were truncated away

## Trace 40B: Typical session fits — no overflow ceremony

- **Path:** same, but the session yields 4 insights and no open questions

### Expected

- `session_knowledge`: 4 bullets; `open_question_refs` absent or empty; `overflow_ref` null; NO overflow file created preemptively

### Pass criteria

- [ ] No workspace overflow file when everything fits
- [ ] Legacy string-form `session_knowledge` in an old handoff still parses on read (additive union, `partial_notes` precedent)

### Fail indicators

- Empty overflow file created "just in case"
- Reader rejecting an old string-form handoff
