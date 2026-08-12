#!/usr/bin/env python3
"""Sweep every downstream dashboard for the edge-case features the HTML
prototype was never tested against. Sources REAL examples for the shakedown
corpus. Python regex = reliable empty-vs-match semantics (no BSD-grep quirk);
SECTION-TOGGLES presence is the positive control."""
import re, glob, os

FILES = sorted(glob.glob("/Users/erikemilsson/Developer/*/.claude/dashboard.md"))

def proj(p): return p.split("/Developer/")[1].split("/")[0]

# feature -> regex. Ordered by the cleave: INTERACTION features first
# (the ones a read-only HTML view structurally can't host), then DISPLAY-only.
FEATURES = [
  ("INTERACTION", "phase_gate",        r"PHASE GATE|Approve transition|Phase \d+ ?→ ?Phase \d+ Transition"),
  ("INTERACTION", "out_of_spec_review",r"out.of.spec|Review and approve|### .*Reviews|🔍 Reviews"),
  ("INTERACTION", "inline_feedback",   r"<!-- FEEDBACK:"),
  ("INTERACTION", "audit_digest",      r"AUDIT DIGEST|🔍 Audit Findings|\[Fix it\]"),
  ("INTERACTION", "section_toggle_off",r"- \[ \] (Decisions|Custom Views|Progress|Tasks|Action Required|Notes)"),
  ("INTERACTION", "both_await_review", r"awaiting your (review|sign.off)|user_review_pending|Verified — awaiting"),
  ("INTERACTION", "decision_pending",  r"\| Pending \|.*decision|❓ .*[Dd]ecision|Resolve DEC"),
  ("DISPLAY",     "overdue_timeline",  r"OVERDUE|~~\d{4}-\d\d-\d\d~~"),
  ("DISPLAY",     "timeline",          r"### Timeline|\| Date \| Item"),
  ("DISPLAY",     "external_dep",      r"External:|Contact:|external_dependency"),
  ("DISPLAY",     "mermaid",           r"```mermaid"),
  ("DISPLAY",     "blocked_phase",     r"Blocked \(|⏳ \d+ tasks? awaiting"),
  ("DISPLAY",     "partially_action",  r"Partially Actionable"),
  ("DISPLAY",     "on_hold",           r"On Hold|⏸️"),
  ("DISPLAY",     "absorbed",          r"Absorbed"),
  ("DISPLAY",     "retired_features",  r"Retired Features|Retired \(\d{4}"),
  ("DISPLAY",     "cross_phase",       r"\(cross-phase\)"),
  ("DISPLAY",     "repair_retries",    r"\(\d+ retr(y|ies)\)|retries\)"),
  ("DISPLAY",     "verification_debt", r"Verification Debt|verification_debt: [1-9]"),
  ("DISPLAY",     "verif_pending",     r"Verification Pending|verification will run"),
  ("DISPLAY",     "spec_drift",        r"Spec Drift|drift_deferrals: [1-9]|deferred \d+ days"),
  ("DISPLAY",     "acceptance_crit",   r"### Acceptance Criteria"),
  ("DISPLAY",     "status_summary",    r"\| Status \| Count \|"),
  ("DISPLAY",     "custom_views",      r"## 👁️ Custom Views|CUSTOM VIEWS INSTRUCTIONS"),
  ("CONTROL",     "section_toggles",   r"SECTION TOGGLES"),   # positive control: must hit ALL
]

data = {}
sizes = {}
for f in FILES:
    txt = open(f, encoding="utf-8").read()
    data[proj(f)] = txt
    sizes[proj(f)] = (txt.count("\n")+1, len(txt))

projects = list(data.keys())
print(f"{len(projects)} dashboards:")
for p in projects:
    print(f"   {p:34s} {sizes[p][0]:>4} lines  {sizes[p][1]:>7} chars")
print()

def first_example(rx, txt):
    for i, line in enumerate(txt.splitlines(), 1):
        if re.search(rx, line):
            return i, line.strip()[:96]
    return None

print("FEATURE PRESENCE  (cleave | feature : projects that have it)\n" + "="*72)
last_cleave = None
for cleave, name, rx in FEATURES:
    if cleave != last_cleave:
        print(f"\n--- {cleave} " + "-"*(68-len(cleave)))
        last_cleave = cleave
    hits = []
    for p in projects:
        c = len(re.findall(rx, data[p]))
        if c: hits.append(f"{p}({c})")
    mark = "✓" if hits else "·"
    print(f"{mark} {name:20s} {len(hits):>2}/{len(projects)}  {', '.join(hits) if hits else '— none —'}")

print("\n\nREAL EXAMPLE LINES  (one per feature, sourced for the corpus)\n" + "="*72)
for cleave, name, rx in FEATURES:
    if name == "section_toggles": continue
    for p in projects:
        ex = first_example(rx, data[p])
        if ex:
            print(f"[{name}] {p}:{ex[0]}\n    {ex[1]}")
            break
