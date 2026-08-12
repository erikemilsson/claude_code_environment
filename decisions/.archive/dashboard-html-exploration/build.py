#!/usr/bin/env python3
"""
Dashboard HTML render-target prototype.

Reads a real template Markdown dashboard (styler-dashboard.md, 269 tasks /
141 decisions / 53 phases) and emits two render targets from the SAME source
data, so the difference is presentation, not content:

  - before.html : the dashboard.md rendered the way a Markdown viewer shows it
                  (marked.js + github-markdown-css). This is the status quo
                  "rendered Markdown" experience.
  - dashboard.html : an HTML "project console" render target — the same data,
                  with collapse / search / filter / progress-bar affordances
                  that raw Markdown cannot express.

This mirrors how the real .claude/scripts/dashboard-render.py works: parse the
structured task/decision/phase data, emit a render target. Here the target is
HTML instead of Markdown. Stdlib only; no third-party Python deps.
"""

import re
import html
import json
import pathlib

HERE = pathlib.Path(__file__).parent
SRC = HERE / "styler-dashboard.md"
RAW = SRC.read_text(encoding="utf-8")


# ---------------------------------------------------------------- parse helpers
def section(name):
    """Return the body under the `## ` heading whose text contains {name}.

    Split on line-anchored `## ` headings (no DOTALL) so a level-3 'Your Tasks'
    inside Action Required can't be mistaken for the `## Tasks` section.
    """
    parts = re.split(r"^(## .*)$", RAW, flags=re.M)
    for i in range(1, len(parts), 2):
        if name.lower() in parts[i].lower():
            return parts[i + 1]
    return ""


def table_rows(block):
    """Yield cell-lists for each data row of the first markdown table in block."""
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):   # separator row
            continue
        rows.append(cells)
    return rows[1:] if rows else []              # drop header row


def md_inline(s):
    """Minimal inline markdown -> HTML (escape first, then re-introduce tags)."""
    s = html.escape(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"(?<![\*\w])\*([^*]+)\*(?![\*\w])", r"<em>\1</em>", s)
    return s


def md_block(block):
    """Convert a freeform markdown block (headings / lists / paras) to HTML."""
    out, buf = [], []

    def flush():
        if buf:
            out.append("<ul>" + "".join(f"<li>{md_inline(x)}</li>" for x in buf)
                       + "</ul>")
            buf.clear()

    for line in block.splitlines():
        t = line.strip()
        if not t:
            flush()
            continue
        if t.startswith("<!--") or t.startswith("-->") or t == "---":
            continue
        h = re.match(r"^(#{2,4})\s+(.*)", t)
        if h:
            flush()
            lvl = len(h.group(1))
            out.append(f"<h{lvl} class='nb'>{md_inline(h.group(2))}</h{lvl}>")
            continue
        if t.startswith("- "):
            buf.append(t[2:])
            continue
        flush()
        out.append(f"<p>{md_inline(t)}</p>")
    flush()
    return "\n".join(out)


# ------------------------------------------------------------------- meta + head
meta = dict(re.findall(r"^([a-z_]+):\s*(.*)$",
                       re.search(r"<!-- DASHBOARD META(.*?)-->", RAW, re.S).group(1),
                       re.M))
title = re.search(r"^\*\*(.+?)\*\*\s*·\s*(.+?)\s*·\s*(.+)$", RAW, re.M)
project_name, phase_label, started = title.group(1), title.group(2), title.group(3)
complete = re.search(r"\*\*(\d+)% complete\*\*", RAW).group(1)


# --------------------------------------------------------------------- progress
prog = section("Progress")
status_counts = []
phases = []
for cells in table_rows(prog):
    if len(cells) == 2 and cells[1].isdigit():
        status_counts.append((cells[0], int(cells[1])))
for m in re.finditer(r"^\| (Phase .*?|Unphased) \| (\d+) \| (\d+) \| (.*?) \|$",
                     prog, re.M):
    name, done, total, st = m.groups()
    phases.append({"name": name, "done": int(done), "total": int(total),
                   "status": st})

acc = re.findall(r"^- \[([ x])\] (.*?) — \*(.*?)\*$", prog, re.M)
acc_summary = (re.search(r"\*\*(\d+/\d+) criteria passed\*\*", prog) or
               re.search(r"(\d+/\d+) criteria", prog))
acc_summary = acc_summary.group(1) if acc_summary else f"{len(acc)} criteria"

recent = re.findall(r"^- \*\*(\d{4}-\d\d-\d\d)\*\* — (.*?)$", prog, re.M)


# ------------------------------------------------------------------------ tasks
tasks_sec = section("Tasks")
task_phases = []
for blk in re.split(r"^### ", tasks_sec, flags=re.M)[1:]:
    head, _, body = blk.partition("\n")
    name = head.strip()
    finished = re.search(r"✅ (\d+) tasks? finished\s*(\([^)]*\))?", body)
    rows = []
    for c in table_rows(body):
        if len(c) >= 6:
            rows.append({"id": c[0], "title": c[1], "status": c[2],
                         "diff": c[3], "owner": c[4], "deps": c[5]})
    task_phases.append({"name": name,
                        "finished": int(finished.group(1)) if finished else 0,
                        "extra": (" " + finished.group(2)) if finished and
                        finished.group(2) else "",
                        "tasks": rows})


# -------------------------------------------------------------------- decisions
decisions = []
for c in table_rows(section("Decisions")):
    if len(c) < 4:
        continue
    did, dtitle, dstatus, sel = c[0], c[1], c[2], c[3]
    lm = re.match(r"\[(.*)\]\((.*)\)$", sel, re.S)
    sel_text = lm.group(1) if lm else sel
    sel_link = lm.group(2) if lm else ""
    decisions.append({"id": did, "title": dtitle, "status": dstatus,
                      "sel_text": sel_text, "link": sel_link})


# ----------------------------------------------------- freeform: action + notes
action_html = md_block(section("Action Required"))
notes_block = re.search(r"<!-- USER SECTION -->(.*?)<!-- END USER SECTION -->",
                        section("Notes"), re.S)
notes_html = md_block(notes_block.group(1) if notes_block else section("Notes"))


# ============================================================ EMIT: dashboard.html
def status_class(s):
    s = s.lower()
    if any(k in s for k in ("finished", "complete", "decided", "pass")):
        return "ok"
    if any(k in s for k in ("pending", "active", "partially", "awaiting")):
        return "warn"
    if "blocked" in s:
        return "bad"
    if "hold" in s:
        return "hold"
    if any(k in s for k in ("superseded", "absorbed")):
        return "mute"
    return "mute"


def owner_badge(o):
    o = o.lower()
    return {"claude": "🤖", "human": "❗", "both": "👥"}.get(o, "·") + " " + o


CSS = r"""
:root{
  --paper:#f4f1ea; --paper-2:#ece7dc; --card:#fbf9f4; --ink:#211d17;
  --ink-soft:#5d564a; --line:#ddd5c5; --line-2:#cabfa8;
  --brand:#0f5f54; --brand-ink:#0a4138;
  --ok:#2f7d4f; --ok-bg:#e3efe3; --warn:#9a6212; --warn-bg:#f6ead0;
  --bad:#a8331f; --bad-bg:#f4ddd5; --hold:#5a6b86; --hold-bg:#e4e8f0;
  --mute:#8a8275; --mute-bg:#eae5da;
  --shadow:0 1px 0 #fff inset, 0 1px 3px rgba(40,32,16,.08), 0 8px 24px rgba(40,32,16,.05);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:"IBM Plex Sans",-apple-system,system-ui,sans-serif;
  font-size:14.5px; line-height:1.55;
  background-image:radial-gradient(transparent 0,transparent 0),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.025'/%3E%3C/svg%3E");
}
code,.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace}
a{color:var(--brand-ink); text-decoration:none; border-bottom:1px solid var(--line-2)}
a:hover{border-color:var(--brand)}
.wrap{max-width:1060px; margin:0 auto; padding:0 22px 120px}

/* ---- masthead ---- */
header.mast{
  position:sticky; top:0; z-index:40; background:rgba(244,241,234,.86);
  backdrop-filter:blur(10px); border-bottom:1px solid var(--line-2);
}
.mast-in{max-width:1060px; margin:0 auto; padding:11px 22px;
  display:flex; align-items:center; gap:18px; flex-wrap:wrap}
.mast h1{font-family:"Fraunces",Georgia,serif; font-weight:600;
  font-size:18px; margin:0; letter-spacing:-.01em; line-height:1.1}
.mast .crumb{color:var(--ink-soft); font-size:11.5px; text-transform:uppercase;
  letter-spacing:.13em; font-weight:600}
.chips{display:flex; gap:7px; margin-left:auto; flex-wrap:wrap}
.chip{font-family:"IBM Plex Mono",monospace; font-size:11.5px; padding:3px 9px;
  border-radius:999px; background:var(--card); border:1px solid var(--line-2);
  color:var(--ink-soft); white-space:nowrap}
.chip b{color:var(--ink); font-weight:600}
.chip.good b{color:var(--ok)} .chip.zero{opacity:.6}

/* ---- hero progress ---- */
.hero{padding:34px 0 16px}
.hero .ttl{font-family:"Fraunces",Georgia,serif; font-size:33px; font-weight:600;
  letter-spacing:-.02em; margin:0 0 4px}
.hero .sub{color:var(--ink-soft); font-size:13px; margin-bottom:18px}
.bigbar{height:12px; border-radius:999px; background:var(--paper-2);
  overflow:hidden; box-shadow:inset 0 1px 2px rgba(40,32,16,.12)}
.bigbar>i{display:block; height:100%; border-radius:999px;
  background:linear-gradient(90deg,var(--brand),#27a18c)}
.bigbar-row{display:flex; align-items:baseline; gap:12px; margin-top:8px}
.bigbar-row .pct{font-family:"Fraunces",serif; font-size:20px; font-weight:600}
.bigbar-row .meta{color:var(--ink-soft); font-size:12.5px}

/* ---- section scaffold ---- */
nav.sub{position:sticky; top:48px; z-index:30; display:flex; gap:4px;
  flex-wrap:wrap; padding:9px 0; margin-bottom:8px;
  background:linear-gradient(var(--paper) 70%,transparent);
}
nav.sub a{font-size:12px; font-weight:600; color:var(--ink-soft);
  padding:4px 11px; border-radius:999px; border:1px solid transparent}
nav.sub a:hover{background:var(--card); border-color:var(--line); color:var(--ink)}
section.blk{margin:30px 0}
.h-sec{display:flex; align-items:center; gap:10px; margin:0 0 14px}
.h-sec h2{font-family:"Fraunces",serif; font-size:22px; font-weight:600;
  margin:0; letter-spacing:-.01em}
.h-sec .ct{font-family:"IBM Plex Mono",monospace; font-size:12px;
  color:var(--ink-soft); background:var(--paper-2); padding:1px 8px;
  border-radius:6px}
.h-sec .rule{flex:1; height:1px; background:var(--line-2)}

.card{background:var(--card); border:1px solid var(--line); border-radius:13px;
  box-shadow:var(--shadow)}
.pad{padding:16px 18px}

/* ---- badges ---- */
.bdg{display:inline-block; font-family:"IBM Plex Mono",monospace; font-size:11px;
  font-weight:600; padding:1.5px 8px; border-radius:6px; white-space:nowrap}
.bdg.ok{color:var(--ok); background:var(--ok-bg)}
.bdg.warn{color:var(--warn); background:var(--warn-bg)}
.bdg.bad{color:var(--bad); background:var(--bad-bg)}
.bdg.hold{color:var(--hold); background:var(--hold-bg)}
.bdg.mute{color:var(--mute); background:var(--mute-bg)}
.pill{display:inline-block; font-family:"IBM Plex Mono",monospace; font-size:11px;
  padding:1px 7px; border-radius:999px; border:1px solid var(--line-2);
  color:var(--ink-soft)}

/* ---- action required ---- */
.action h3.nb{font-size:13px; text-transform:uppercase; letter-spacing:.06em;
  color:var(--brand-ink); margin:16px 0 7px}
.action h3.nb:first-child{margin-top:0}
.action ul{margin:6px 0; padding-left:18px} .action li{margin:4px 0}
.action p{margin:8px 0}
.banner{border-left:3px solid var(--brand); background:#eef4f0; padding:10px 14px;
  border-radius:0 9px 9px 0; margin-bottom:6px; font-size:13.5px}

/* ---- status strip ---- */
.stats{display:flex; gap:9px; flex-wrap:wrap; margin-bottom:16px}
.stat{flex:1; min-width:88px; background:var(--card); border:1px solid var(--line);
  border-radius:11px; padding:11px 13px; box-shadow:var(--shadow)}
.stat .n{font-family:"Fraunces",serif; font-size:25px; font-weight:600; line-height:1}
.stat .l{font-size:11px; text-transform:uppercase; letter-spacing:.05em;
  color:var(--ink-soft); margin-top:3px}
.stat.ok .n{color:var(--ok)} .stat.warn .n{color:var(--warn)}
.stat.bad .n{color:var(--bad)} .stat.hold .n{color:var(--hold)}
.stat.mute .n{color:var(--mute)}

/* ---- phase rows ---- */
.phase{display:grid; grid-template-columns:1fr auto; gap:4px 12px;
  align-items:center; padding:9px 14px; border-bottom:1px solid var(--line)}
.phase:last-child{border-bottom:0}
.phase .pn{font-size:13px; font-weight:500}
.phase .pbar{grid-column:1/3; height:5px; border-radius:999px;
  background:var(--paper-2); overflow:hidden}
.phase .pbar>i{display:block; height:100%; background:var(--brand); border-radius:999px}
.phase .frac{font-family:"IBM Plex Mono",monospace; font-size:11.5px;
  color:var(--ink-soft)}

details.disc>summary{cursor:pointer; list-style:none; padding:11px 16px;
  display:flex; align-items:center; gap:9px; font-weight:600; font-size:13px}
details.disc>summary::-webkit-details-marker{display:none}
details.disc>summary::before{content:"▸"; color:var(--ink-soft);
  transition:transform .15s; font-size:11px}
details.disc[open]>summary::before{transform:rotate(90deg)}
details.disc>summary:hover{background:var(--paper-2)}
.disc .body{padding:2px 16px 14px}

/* ---- tasks ---- */
.task{padding:11px 0; border-top:1px solid var(--line)}
.task:first-child{border-top:0}
.task .tt{font-size:13px; margin:0 0 5px}
.task .tid{font-family:"IBM Plex Mono",monospace; color:var(--brand-ink);
  font-weight:600; margin-right:6px}
.task .row{display:flex; gap:6px; align-items:center; flex-wrap:wrap}

/* ---- decisions (the showcase) ---- */
.dtools{display:flex; gap:9px; flex-wrap:wrap; align-items:center; margin-bottom:12px}
.dtools input{flex:1; min-width:180px; font-size:13.5px; padding:8px 13px;
  border:1px solid var(--line-2); border-radius:9px; background:var(--card);
  font-family:inherit; color:var(--ink)}
.dtools input:focus{outline:2px solid var(--brand); border-color:var(--brand)}
.fbtn{font-family:"IBM Plex Mono",monospace; font-size:12px; padding:6px 12px;
  border-radius:999px; border:1px solid var(--line-2); background:var(--card);
  color:var(--ink-soft); cursor:pointer}
.fbtn.on{background:var(--brand); color:#fff; border-color:var(--brand)}
.dec{border-bottom:1px solid var(--line)}
.dec>summary{cursor:pointer; list-style:none; padding:10px 14px; display:grid;
  grid-template-columns:62px 1fr auto; gap:11px; align-items:center}
.dec>summary::-webkit-details-marker{display:none}
.dec>summary:hover{background:var(--paper-2)}
.dec .did{font-family:"IBM Plex Mono",monospace; font-weight:600; font-size:12.5px;
  color:var(--brand-ink)}
.dec .dt{font-size:13px}
.dec .dbody{padding:0 14px 14px 87px; font-size:13px; color:var(--ink-soft)}
.dec .dbody .sel{color:var(--ink); background:var(--paper-2); padding:9px 12px;
  border-radius:8px; display:block; margin-bottom:7px}
.empty{padding:20px; text-align:center; color:var(--ink-soft); font-size:13px}

/* ---- notes ---- */
.notes h3.nb{font-family:"Fraunces",serif; font-size:15px; margin:16px 0 6px}
.notes h2.nb{font-family:"Fraunces",serif; font-size:17px; margin:14px 0 6px}
.notes ul{margin:5px 0; padding-left:18px} .notes li{margin:3px 0; font-size:13px}
.notes p{margin:7px 0; font-size:13px}
footer.ft{margin-top:40px; padding-top:16px; border-top:1px solid var(--line-2);
  color:var(--mute); font-family:"IBM Plex Mono",monospace; font-size:11.5px}
"""

JS = r"""
function decFilter(){
  const q=(document.getElementById('dq').value||'').toLowerCase();
  const f=document.querySelector('.fbtn.on').dataset.f;
  let n=0;
  document.querySelectorAll('.dec').forEach(d=>{
    const okF = f==='all' || d.dataset.status===f;
    const okQ = !q || d.dataset.search.includes(q);
    const show = okF && okQ; d.style.display = show?'':'none'; if(show)n++;
  });
  document.getElementById('dcount').textContent=n+' shown';
  document.getElementById('dempty').style.display=n?'none':'';
}
document.addEventListener('click',e=>{
  if(e.target.classList.contains('fbtn')){
    document.querySelectorAll('.fbtn').forEach(b=>b.classList.remove('on'));
    e.target.classList.add('on'); decFilter();
  }
});
document.addEventListener('keydown',e=>{
  if(e.key==='/' && e.target.tagName!=='INPUT'){e.preventDefault();
    document.getElementById('dq').focus();}
});
"""


def emit_dashboard():
    chips = (f'<span class="chip"><b>{meta["task_count"]}</b> tasks</span>'
             f'<span class="chip"><b>{meta["decision_count"]}</b> decisions</span>'
             f'<span class="chip {"zero good" if meta["verification_debt"]=="0" else "bad"}">'
             f'<b>{meta["verification_debt"]}</b> verif debt</span>'
             f'<span class="chip {"zero" if meta["drift_deferrals"]=="0" else "bad"}">'
             f'<b>{meta["drift_deferrals"]}</b> drift</span>')

    # status strip
    strip = "".join(
        f'<div class="stat {status_class(s)}"><div class="n">{c}</div>'
        f'<div class="l">{html.escape(s)}</div></div>'
        for s, c in status_counts)

    # phases: split complete vs not
    def phase_row(p):
        pct = round(100 * p["done"] / p["total"]) if p["total"] else 100
        return (f'<div class="phase"><div class="pn">{html.escape(p["name"])}</div>'
                f'<div class="frac">{p["done"]}/{p["total"]} · '
                f'<span class="bdg {status_class(p["status"])}">'
                f'{html.escape(p["status"])}</span></div>'
                f'<div class="pbar"><i style="width:{pct}%"></i></div></div>')
    active = [p for p in phases if "Complete" not in p["status"]]
    done_ph = [p for p in phases if "Complete" in p["status"]]
    phase_html = '<div class="card">' + "".join(phase_row(p) for p in active) + '</div>'
    phase_html += (f'<details class="disc card" style="margin-top:10px">'
                   f'<summary>{len(done_ph)} completed phases '
                   f'<span class="pill">{sum(p["done"] for p in done_ph)} tasks</span>'
                   f'</summary><div class="body"><div class="card">'
                   + "".join(phase_row(p) for p in done_ph) + '</div></div></details>')

    # acceptance criteria
    acc_items = "".join(
        f'<li>{"✅" if mark=="x" else "⬜"} {md_inline(name)} '
        f'<span style="color:var(--ink-soft)">— {md_inline(note)}</span></li>'
        for mark, name, note in acc)
    acc_html = (f'<details class="disc card"><summary>Acceptance Criteria '
                f'<span class="pill">{acc_summary}</span></summary>'
                f'<div class="body"><ul style="margin:0;padding-left:18px;'
                f'font-size:12.5px;line-height:1.7">{acc_items}</ul></div></details>')

    # recent activity
    rec_html = '<div class="card pad" style="margin-top:10px"><h3 class="nb" '
    rec_html += ('style="font-size:12px;text-transform:uppercase;letter-spacing:.06em;'
                 'color:var(--ink-soft);margin:0 0 8px">Recent activity</h3>')
    rec_html += "".join(
        f'<div style="font-size:12.5px;padding:3px 0;border-bottom:1px solid var(--line)">'
        f'<span class="mono" style="color:var(--ink-soft)">{d}</span> &nbsp;{md_inline(t)}</div>'
        for d, t in recent) + '</div>'

    # tasks
    def task_phase(tp):
        if not tp["tasks"]:
            return (f'<details class="disc"><summary>{html.escape(tp["name"])} '
                    f'<span class="pill" style="margin-left:auto">✅ {tp["finished"]} '
                    f'finished{html.escape(tp["extra"])}</span></summary></details>')
        rows = ""
        for t in tp["tasks"]:
            rows += (f'<div class="task"><p class="tt"><span class="tid">T{t["id"]}</span>'
                     f'{md_inline(t["title"])}</p><div class="row">'
                     f'<span class="bdg {status_class(t["status"])}">{html.escape(t["status"])}</span>'
                     f'<span class="pill">diff {t["diff"]}</span>'
                     f'<span class="pill">{owner_badge(t["owner"])}</span>'
                     + (f'<span class="pill">deps {html.escape(t["deps"])}</span>'
                        if t["deps"] not in ("—", "") else "") + '</div></div>')
        return (f'<details class="disc card" open style="margin-bottom:8px">'
                f'<summary>{html.escape(tp["name"])} '
                f'<span class="pill" style="margin-left:auto">{len(tp["tasks"])} active</span>'
                f'</summary><div class="body">{rows}</div></details>')
    active_tp = [tp for tp in task_phases if tp["tasks"]]
    done_tp = [tp for tp in task_phases if not tp["tasks"]]
    tasks_html = "".join(task_phase(tp) for tp in active_tp)
    tasks_html += (f'<details class="disc card"><summary>{len(done_tp)} completed phases '
                   f'<span class="pill" style="margin-left:auto">'
                   f'{sum(tp["finished"] for tp in done_tp)} finished tasks</span></summary>'
                   f'<div class="body">' + "".join(task_phase(tp) for tp in done_tp)
                   + '</div></details>')

    # decisions
    dec_rows = ""
    for d in decisions:
        st = "superseded" if d["status"].lower() == "superseded" else "decided"
        search = (d["id"] + " " + d["title"] + " " + d["sel_text"]).lower()
        link = (f'<a href="{html.escape(d["link"])}" target="_blank" rel="noopener">'
                f'open record →</a>' if d["link"] else "")
        dec_rows += (
            f'<details class="dec" data-status="{st}" '
            f'data-search="{html.escape(search, quote=True)}">'
            f'<summary><span class="did">{html.escape(d["id"])}</span>'
            f'<span class="dt">{html.escape(d["title"])}</span>'
            f'<span class="bdg {status_class(d["status"])}">{html.escape(d["status"])}</span>'
            f'</summary><div class="dbody"><span class="sel">{md_inline(d["sel_text"])}</span>'
            f'{link}</div></details>')
    n_dec = len(decisions)
    n_sup = sum(1 for d in decisions if d["status"].lower() == "superseded")
    dec_html = f"""
    <div class="dtools">
      <input id="dq" placeholder="Search {n_dec} decisions by id, title, or rationale…   ( / )"
             oninput="decFilter()">
      <button class="fbtn on" data-f="all">All {n_dec}</button>
      <button class="fbtn" data-f="decided">Decided {n_dec-n_sup}</button>
      <button class="fbtn" data-f="superseded">Superseded {n_sup}</button>
      <span class="pill" id="dcount">{n_dec} shown</span>
    </div>
    <div class="card">{dec_rows}
      <div class="empty" id="dempty" style="display:none">No decisions match.</div>
    </div>"""

    def hsec(title, count, anchor):
        return (f'<div class="h-sec" id="{anchor}"><h2>{title}</h2>'
                f'<span class="ct">{count}</span><span class="rule"></span></div>')

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(project_name)} — Console</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>
<header class="mast"><div class="mast-in">
  <span class="crumb">{html.escape(phase_label)}</span>
  <h1>{html.escape(project_name)}</h1>
  <div class="chips">{chips}</div>
</div></header>

<div class="wrap">
  <div class="hero">
    <div class="sub">{html.escape(started)} · spec {meta['spec_version']} · template {meta['template_version']}</div>
    <div class="bigbar"><i style="width:{complete}%"></i></div>
    <div class="bigbar-row"><span class="pct">{complete}%</span>
      <span class="meta">complete — {meta['task_count']} tasks across {len(phases)} phases · {meta['decision_count']} decisions</span></div>
  </div>

  <nav class="sub">
    <a href="#action">🚨 Action</a><a href="#progress">📊 Progress</a>
    <a href="#tasks">📋 Tasks</a><a href="#decisions">📋 Decisions</a>
    <a href="#notes">💡 Notes</a>
  </nav>

  <section class="blk action">{hsec("🚨 Action Required","needs you","action")}
    <div class="card pad">{action_html}</div></section>

  <section class="blk">{hsec("📊 Progress",complete+"% complete","progress")}
    <div class="stats">{strip}</div>
    {phase_html}
    <div style="margin-top:10px">{acc_html}</div>
    {rec_html}
  </section>

  <section class="blk">{hsec("📋 Tasks",meta["task_count"]+" total","tasks")}
    {tasks_html}</section>

  <section class="blk">{hsec("📋 Decisions",meta["decision_count"]+" records","decisions")}
    {dec_html}</section>

  <section class="blk notes">{hsec("💡 Notes","","notes")}
    <div class="card pad">{notes_html}</div></section>

  <footer class="ft">generated {meta['generated']} · {meta['task_count']} tasks ·
    {meta['decision_count']} decisions · 0 drift · 0 verification debt ·
    <em>HTML render-target prototype — same data as dashboard.md</em></footer>
</div>
<script>{JS}</script>
</body></html>"""


# ============================================================ EMIT: before.html
def emit_before():
    md_json = json.dumps(RAW)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>dashboard.md (rendered Markdown)</title>
<link rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-light.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  body{{margin:0;background:#fff}}
  .markdown-body{{box-sizing:border-box;max-width:980px;margin:0 auto;padding:38px}}
  .note{{position:sticky;top:0;background:#fff8e6;border-bottom:1px solid #e6d8a8;
    font:13px/1.4 -apple-system,system-ui,sans-serif;color:#6b5a1f;padding:8px 16px;z-index:9}}
</style></head><body>
<div class="note">▼ <b>Status quo</b>: <code>.claude/dashboard.md</code> as a Markdown
  viewer (GitHub / VS&nbsp;Code preview) renders it — 640 lines, one flat scroll.</div>
<article class="markdown-body" id="md"></article>
<script>
  const src = {md_json};
  // strip the leading HTML META comment so it doesn't dump raw into the page
  document.getElementById('md').innerHTML =
    marked.parse(src.replace(/<!-- DASHBOARD META[\\s\\S]*?-->/, ''));
</script></body></html>"""


(HERE / "dashboard.html").write_text(emit_dashboard(), encoding="utf-8")
(HERE / "before.html").write_text(emit_before(), encoding="utf-8")
print(f"OK  parsed: {len(phases)} phases, {len(task_phases)} task-groups, "
      f"{len(decisions)} decisions, {len(status_counts)} status rows, "
      f"{len(acc)} criteria, {len(recent)} recent")
print("wrote dashboard.html, before.html")
