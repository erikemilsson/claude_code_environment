# Scenario 40: Handoff Schema Cap (bounded index, not a memoir)

Verify the handoff bounds shipped v4.21.1 (Plan 3 T4a): `.handoff.json` stays a bounded index (`session_knowledge` ≤ ~10 bullets; `recovery_action` ≤ ~3 sentences); overflow goes to a workspace file the handoff points at via `overflow_ref`. From v5.14.0 the whole file is also measured after each write (at most 2560 bytes), and the overflow file is named to the minute.

## Context

Observed failure mode (styler, 2026-06-10 analysis): a 7.8KB hand-curated free-prose handoff blob — write-expensive, read-unreliable, and a hiding place for blocking questions (the T3 queue contract, v4.14.0, moved those to dashboard rows; this cap bounds what remains).

## State (Base)

A long session ends with `/work pause`: one partial task (7), two unanswered user questions (already swept into sidecar `augment_rows[]`, rendered as Action Required rows, per the T3 contract), and ~18 distinct conversation insights worth preserving.

---

## Trace 40A: Rich session → bounded handoff + overflow file

- **Path:** `/work pause` (at 14:32 on 2026-10-07) → Path A → handoff write per `context-transitions.md § Schema` + `§ Bounds and Overflow`

### Expected

- `session_knowledge` written as an ARRAY of ≤ ~10 bullets (the most load-bearing of the 18), each ≤ ~25 words
- Excess insights land in `.claude/support/workspace/handoff-overflow-2026-10-07-1432.md`, organized by field name; `overflow_ref` set to that path
- `open_question_refs` holds POINTERS to the two Action Required rows — not the question text + discussion
- `recovery_action` ≤ ~3 sentences
- After the write, `wc -c < .claude/tasks/.handoff.json` prints 2310: within 2560, so the total check ends there

### Pass criteria

- [ ] Handoff is a bounded index; no field blows its cap
- [ ] The file was measured after the write, and the measured size is 2560 bytes or fewer
- [ ] Overflow file exists ONLY because content genuinely exceeded a bound
- [ ] Questions live in `augment_rows[]` (rendered as dashboard rows); handoff carries refs only

### Fail indicators

- A multi-KB `session_knowledge` prose blob (old shape)
- Insights silently dropped instead of overflowed
- `overflow_ref` null while bullets were truncated away
- An overflow file named by date only (`handoff-overflow-2026-10-07.md`)

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

## Trace 40C: Every field within its cap, total over — the measurement triggers overflow

- **Path:** `/work pause` (at 16:05 on 2026-10-07, the same day as Trace 40A) → Path A step 5 → `context-transitions.md § Bounds and Overflow`, Total check

### Scenario

The session yields exactly 10 `session_knowledge` bullets of 22–25 words each (about 1.6KB), one partial task whose `partial_notes` is 6 sentences (about 620 bytes), a 3-sentence `recovery_action`, a 2-sentence `phase_context` and two `open_question_refs` pointers. No field exceeds its cap, so the per-field overflow procedure has nothing to do and `overflow_ref` is null after the first write.

### Expected

1. The handoff is written. `wc -c < .claude/tasks/.handoff.json` prints 3040: over 2560.
2. The longest field is `session_knowledge`. Its three least load-bearing bullets move to `.claude/support/workspace/handoff-overflow-2026-10-07-1605.md` under a `session_knowledge` heading; seven stay inline; `overflow_ref` is set to that path; the handoff is rewritten.
3. Second measurement: 2590. Still over.
4. The longest remaining field is `active_work[0].partial_notes`. Its last three sentences move to the same overflow file under `partial_notes`; the handoff is rewritten.
5. Third measurement: 2290. Done.
6. `handoff-overflow-2026-10-07-1432.md` from the earlier pause is untouched.

### Pass criteria

- [ ] The file is measured after the write even though no field exceeded its cap
- [ ] Content moves out largest field first, and the file is measured again after each rewrite, until it is 2560 bytes or fewer
- [ ] Everything moved out is in the overflow file under its field's name; `overflow_ref` points at it
- [ ] `open_question_refs`, the task id and `ready_for_verify` in `active_work`, and the required fields are unchanged
- [ ] The overflow file's name carries the minute, so the day's two pauses have two files

### Fail indicators

- A 3040-byte handoff left as written because every field was within its cap (the pre-v5.14.0 behaviour)
- Bullets deleted to get under the total, with no overflow file
- `open_question_refs` shortened or dropped to save bytes
- The second pause writing over, or appending to, the first pause's overflow file
- The size estimated from the field lengths with no `wc -c` on the written file
