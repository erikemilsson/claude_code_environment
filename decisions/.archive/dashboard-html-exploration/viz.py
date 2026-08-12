#!/usr/bin/env python3
"""Dashboard v2 — single-file, read-only, visualization-forward, curated.

Usage: python3 viz.py [source_dashboard.md] [output.html]
Defaults to styler. Generalized so it can render any project's dashboard —
e.g. a mid-flight one where the dependency graph + timeline have something to show.

Direction (user, 2026-06-23): one HTML file IS the dashboard (the .md can go);
read-only (overview; act via CLI); cut bloat; lead with visualizations.
Iteration 2 changes: drop the explanatory note + bare sparkline; Recent gets
task descriptions; Decisions fully collapsed-by-default but openable + searchable;
add a Flow/critical-path graph (mermaid.js, themed) + Timeline when present.
"""
import re, html, math, sys, pathlib
HERE = pathlib.Path(__file__).parent
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "styler-dashboard.md"
OUT = HERE / (sys.argv[2] if len(sys.argv) > 2 else "dashboard-v2.html")
RAW = SRC.read_text(encoding="utf-8")

# ---- parse helpers -----------------------------------------------------------
def sec(name):
    parts = re.split(r"^(## .*)$", RAW, flags=re.M)
    for i in range(1, len(parts), 2):
        if name.lower() in parts[i].lower():
            return parts[i+1]
    return ""
def subsec(block, name):
    m = re.search(r"### .*?"+re.escape(name)+r".*?\n(.*?)(?=\n### |\n## |\Z)", block, re.S)
    return m.group(1) if m else ""
def rows(block):
    out=[]
    for ln in block.splitlines():
        ln=ln.strip()
        if not ln.startswith("|"): continue
        c=[x.strip() for x in ln.strip("|").split("|")]
        if set("".join(c))<=set("-: "): continue
        out.append(c)
    return out[1:] if out else []
def mdi(s):
    s=html.escape(s)
    s=re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank">\1</a>', s)
    s=re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s=re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s

meta=dict(re.findall(r"^([a-z_]+):\s*(.*)$", re.search(r"<!-- DASHBOARD META(.*?)-->",RAW,re.S).group(1), re.M))
pname=re.search(r"^\*\*(.+?)\*\*\s*·", RAW, re.M).group(1)
complete=int(re.search(r"\*\*(\d+)% complete", RAW).group(1))
prog=sec("Progress")
status=[(m[0],int(m[1])) for m in re.findall(r"^\| (Finished|Pending|In Progress|Blocked|On Hold|Absorbed) \| (\d+) \|", prog, re.M)]
phases=[{"name":m.group(1),"n":m.group(1).split("—")[0].strip().replace("Phase ",""),
         "done":int(m.group(2)),"total":int(m.group(3)),"status":m.group(4)}
        for m in re.finditer(r"^\| (Phase .*?|Unphased) \| (\d+) \| (\d+) \| (.*?) \|$", prog, re.M)]
recent=re.findall(r"^- \*\*(\d{4}-\d\d-\d\d)\*\* — (?:Task (\d+) — )?(?:Finished: )?(.*?)$", prog, re.M)
your_tasks=re.findall(r"^- \*\*(T?\d+)\*\* — (.*?)$", sec("Action Required"), re.M)
# full decisions
decisions=[]
for c in rows(sec("Decisions")):
    if len(c)<4: continue
    lm=re.match(r"\[(.*)\]\((.*)\)$", c[3], re.S)
    decisions.append({"id":c[0],"title":c[1],"status":c[2],
                      "sel":lm.group(1) if lm else c[3],"link":lm.group(2) if lm else ""})
# timeline rows (Date|Item|Status|Notes)
timeline=[c for c in rows(subsec(prog,"Timeline")) if len(c)>=3]
# mermaid block (the dependency / project-overview graph)
mm=re.search(r"```mermaid\n(.*?)```", RAW, re.S)
mermaid=mm.group(1).strip() if mm else ""
# spec (collapsible browser) — render the project's spec_v{N}.md as collapsible HTML sections
spec_files=sorted(SRC.parent.glob("spec_v*.md"))
spec_html=""
if spec_files:
    sp=spec_files[-1]; stxt=sp.read_text(encoding="utf-8")
    sparts=re.split(r"^(## .+)$", stxt, flags=re.M)
    secs=[(sparts[i].lstrip('# ').strip(), sparts[i]+"\n"+sparts[i+1]) for i in range(1,len(sparts),2)]
    def esc_md(t): return re.sub(r"</(script)", r"<\\/\1", t, flags=re.I)
    if secs:
        spc="".join(f'<details class="spc" data-h="{html.escape(t.lower(),quote=True)}"><summary>{html.escape(t)}</summary>'
                    f'<div class="specbody"></div><script type="text/markdown" class="src">{esc_md(raw)}</script></details>'
                    for t,raw in secs)
        spec_html=(f'<details class="specwrap"><summary><b>📄 Specification</b> <span class="pill">{sp.stem}</span>'
                   f'<span class="decsum">{len(secs)} sections · rendered &amp; browsable</span><span class="open">browse ▾</span></summary>'
                   f'<div class="decin"><div class="dtools"><input id="sq" placeholder="filter {len(secs)} spec sections…" oninput="specFilter()"></div>'
                   f'<div class="declist speclist">{spc}</div></div></details>')

def scls(s):
    s=s.lower()
    if "complete" in s: return "ok"
    if "active" in s: return "active"
    if "partial" in s: return "warn"
    if "blocked" in s: return "bad"
    if "hold" in s: return "hold"
    return "mute"
status_col={"Finished":"#2f7d4f","Pending":"#9a6212","In Progress":"#1565c0","Blocked":"#a8331f","On Hold":"#5a6b86","Absorbed":"#b8ad97"}

# ---- SVG charts --------------------------------------------------------------
def polar(cx,cy,r,f):
    a=2*math.pi*f-math.pi/2; return cx+r*math.cos(a),cy+r*math.sin(a)
def donut(segs,size=128,th=22):
    cx=cy=size/2; r=(size-th)/2; tot=sum(v for _,v,_ in segs) or 1; out=[]; acc=0.0
    for _,v,col in segs:
        if v==0: continue
        f0,f1=acc/tot,(acc+v)/tot; acc+=v
        x0,y0=polar(cx,cy,r,f0); x1,y1=polar(cx,cy,r,f1); lg=1 if f1-f0>0.5 else 0
        out.append(f'<path d="M {x0:.1f} {y0:.1f} A {r:.1f} {r:.1f} 0 {lg} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" stroke-width="{th}"/>')
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">{"".join(out)}</svg>'
def ring(f,size=150,th=14):
    cx=cy=size/2; r=(size-th)/2; C=2*math.pi*r
    return (f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" class="ring">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="var(--paper-2)" stroke-width="{th}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#g)" stroke-width="{th}" stroke-linecap="round" '
            f'stroke-dasharray="{C:.1f}" stroke-dashoffset="{C*(1-f):.1f}" transform="rotate(-90 {cx} {cy})"/>'
            f'<text x="50%" y="48%" class="ringn">{int(f*100)}<tspan class="rp">%</tspan></text>'
            f'<text x="50%" y="63%" class="ringl">COMPLETE</text></svg>')

# ---- build sections ----------------------------------------------------------
cells=""
for p in phases:
    pct=round(100*p["done"]/p["total"]) if p["total"] else 100; lab=p["n"] if p["n"].isdigit() else "U"
    cells+=(f'<div class="cell {scls(p["status"])}" title="Phase {p["n"]} — {html.escape(p["name"].split("—")[-1].strip())} · {p["done"]}/{p["total"]} · {html.escape(p["status"])}">'
            f'<span class="cn">{lab}</span><span class="cbar"><i style="height:{pct}%"></i></span></div>')
active=[p for p in phases if "Complete" not in p["status"]]
front="".join(f'<div class="af"><div class="afh"><b>Phase {p["n"]}</b> <span class="bdg {scls(p["status"])}">{html.escape(p["status"])}</span>'
              f'<span class="affrac">{p["done"]}/{p["total"]}</span></div><div class="afn">{html.escape(p["name"].split("—",1)[-1].strip())}</div>'
              f'<div class="afbar"><i style="width:{round(100*p["done"]/p["total"]) if p["total"] else 100}%"></i></div></div>' for p in active)
segs=[(s,v,status_col.get(s,"#b8ad97")) for s,v in status]
legend="".join(f'<div class="lg"><span class="dot" style="background:{status_col.get(s,"#b8ad97")}"></span><span class="lgn">{s}</span><b>{v}</b></div>' for s,v in status)
att="".join(f'<li><span class="tid">{tid}</span>{mdi(desc[:130])}</li>' for tid,desc in your_tasks[:6])
done_ph=len([p for p in phases if "Complete" in p["status"]])

# Recent — now WITH descriptions
recent_rows=""
for d,t,desc in recent[:6]:
    desc=re.sub(r"^(?:Finished:\s*)?§?\s*[\d.]+\s*—\s*","",desc).strip()  # trim "Finished:"/"§50.2 —"
    recent_rows+=(f'<div class="rr"><span class="rd">{d[5:]}</span>'
                  f'{f"<span class=tid>T{t}</span>" if t else ""}<span class="rt">{html.escape(desc[:64])}</span></div>')

# Decisions — collapsed by default, openable + searchable
dec_rows=""
for d in decisions:
    st="superseded" if d["status"].lower()=="superseded" else "decided"
    search=html.escape((d["id"]+" "+d["title"]+" "+d["sel"]).lower(), quote=True)
    link=f'<a href="{html.escape(d["link"])}" target="_blank">open record →</a>' if d["link"] else ""
    dec_rows+=(f'<details class="dec" data-status="{st}" data-search="{search}"><summary>'
               f'<span class="did">{html.escape(d["id"])}</span><span class="dt">{html.escape(d["title"])}</span>'
               f'<span class="bdg {scls(d["status"])}">{html.escape(d["status"])}</span></summary>'
               f'<div class="dbody"><span class="sel">{mdi(d["sel"])}</span>{link}</div></details>')
ndec=len(decisions); nsup=sum(1 for d in decisions if d["status"].lower()=="superseded")
decisions_block=(f'<details class="decwrap"><summary><b>📋 Decisions</b> '
                 f'<span class="pill">{ndec}</span><span class="decsum">{ndec-nsup} decided · {nsup} superseded</span>'
                 f'<span class="open">browse ▾</span></summary><div class="decin">'
                 f'<div class="dtools"><input id="dq" placeholder="search {ndec} decisions… ( / )" oninput="decFilter()">'
                 f'<button class="fbtn on" data-f="all">all</button><button class="fbtn" data-f="decided">decided</button>'
                 f'<button class="fbtn" data-f="superseded">superseded</button><span class="pill" id="dcount">{ndec}</span></div>'
                 f'<div class="declist">{dec_rows}<div class="empty" id="dempty" style="display:none">no match</div></div>'
                 f'</div></details>') if decisions else ""

# Flow / critical-path graph (mermaid, themed) — only when the source has one
flow=(f'<section><h2 class="st">Flow · dependency &amp; critical path</h2>'
      f'<div class="flowcard"><pre class="mermaid">{html.escape(mermaid)}</pre></div>'
      f'<div class="cap">Rendered with mermaid.js + themed — the same graph that renders flaky / not-at-all in a Markdown viewer. Owners: ❗ you · 🤖 Claude · 👥 both.</div></section>') if mermaid else ""

# Timeline — only when present
tl_rows=""
for c in timeline:
    date,item,st=c[0],c[1],c[2]; note=c[3] if len(c)>3 else ""
    over="over" if ("OVERDUE" in item or "~~" in date) else ""
    date=date.replace("~~",""); item=re.sub(r"⚠️ OVERDUE:\s*","",item)
    tl_rows+=(f'<div class="tlr {over}"><span class="tld">{html.escape(date)}</span>'
              f'<span class="tli">{html.escape(item)}</span><span class="bdg {scls(st)}">{html.escape(st)}</span>'
              f'{f"<span class=tln>{html.escape(note)}</span>" if note else ""}</div>')
timeline_block=(f'<section><h2 class="st">Timeline</h2><div class="tlcard">{tl_rows}</div></section>') if tl_rows else ""

CSS=r"""
*{box-sizing:border-box} html{scroll-behavior:smooth}
:root{--paper:#f4f1ea;--paper-2:#e6dfd0;--card:#fbf9f4;--ink:#211d17;--soft:#5d564a;--line:#ddd5c5;--line2:#cabfa8;
 --brand:#0f5f54;--brand2:#27a18c;--brandink:#0a4138;--ok:#2f7d4f;--active:#1565c0;--warn:#9a6212;--bad:#a8331f;--hold:#5a6b86;--mute:#b8ad97;
 --sh:0 1px 0 #fff inset,0 1px 3px rgba(40,32,16,.07),0 10px 30px rgba(40,32,16,.05);}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:14.5px;line-height:1.5}
.mono,code{font-family:"IBM Plex Mono",ui-monospace,monospace} a{color:var(--brandink)}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px 90px}
header.mast{position:sticky;top:0;z-index:20;background:rgba(244,241,234,.86);backdrop-filter:blur(10px);border-bottom:1px solid var(--line2)}
.mast-in{max-width:1080px;margin:0 auto;padding:11px 22px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.mast .crumb{font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:var(--soft);font-weight:600}
.mast h1{font-family:"Fraunces",Georgia,serif;font-weight:600;font-size:18px;margin:0}
.mast .tv{margin-left:auto;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--soft)}
h2.st{font-family:"Fraunces",serif;font-size:13px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--soft);margin:0 0 12px;display:flex;align-items:center;gap:9px}
h2.st::after{content:"";flex:1;height:1px;background:var(--line2)}
section{margin:28px 0}
.pulse{display:grid;grid-template-columns:auto auto 1fr;gap:26px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 26px;box-shadow:var(--sh)}
.ring .ringn{font-family:"Fraunces",serif;font-weight:600;font-size:38px;fill:var(--ink);text-anchor:middle}
.ring .rp{font-size:18px;fill:var(--soft)} .ring .ringl{font-size:9px;letter-spacing:.18em;fill:var(--soft);text-anchor:middle;font-family:"IBM Plex Mono",monospace}
.donwrap{display:flex;align-items:center;gap:16px} .legend{display:flex;flex-direction:column;gap:3px}
.lg{display:flex;align-items:center;gap:8px;font-size:12.5px} .lg b{margin-left:auto;font-family:"IBM Plex Mono",monospace} .dot{width:10px;height:10px;border-radius:3px} .lgn{color:var(--soft)}
.pmeta{display:flex;flex-direction:column;gap:10px;justify-self:end;text-align:right} .pmeta .big{font-family:"Fraunces",serif;font-size:30px;font-weight:600;line-height:1}
.pmeta .lbl{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--soft)} .pmeta .row{display:flex;gap:18px;justify-content:flex-end}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(46px,1fr));gap:6px}
.cell{position:relative;aspect-ratio:1;border-radius:8px;border:1px solid var(--line);background:var(--card);display:flex;align-items:center;justify-content:center;overflow:hidden;transition:transform .1s}
.cell:hover{transform:translateY(-2px);box-shadow:var(--sh);z-index:2} .cell .cn{font-family:"IBM Plex Mono",monospace;font-size:12px;font-weight:600;z-index:2}
.cell .cbar{position:absolute;inset:0;display:flex;align-items:flex-end;opacity:.5} .cell .cbar>i{width:100%}
.cell.ok{border-color:#bcdcc4}.cell.ok .cbar>i{background:var(--ok)}.cell.ok .cn{color:#1d5435}
.cell.active{border-color:#aecbeb}.cell.active .cbar>i{background:var(--active)}.cell.active .cn{color:#0d3f7a}
.cell.warn .cbar>i{background:var(--warn)}.cell.warn{border-color:#e6cfa0}
.cell.bad{border-color:#e3b6ac}.cell.bad .cbar>i{background:var(--bad)}.cell.bad .cn{color:#7a2417}
.cell.hold .cbar>i{background:var(--hold)} .cell.mute .cbar>i{background:var(--mute)}
.glegend{display:flex;gap:16px;margin-top:12px;font-size:11.5px;color:var(--soft)} .glegend span b{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px}
.front{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:16px}
.af{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:13px 15px;box-shadow:var(--sh)}
.afh{display:flex;align-items:center;gap:8px;font-size:13px}.affrac{margin-left:auto;font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--soft)}
.afn{font-size:12.5px;color:var(--soft);margin:6px 0 9px;min-height:2.4em}
.afbar{height:6px;border-radius:99px;background:var(--paper-2);overflow:hidden}.afbar>i{display:block;height:100%;background:linear-gradient(90deg,var(--brand),var(--brand2))}
.bdg{font-family:"IBM Plex Mono",monospace;font-size:10.5px;font-weight:600;padding:1px 7px;border-radius:5px;white-space:nowrap}
.bdg.ok{color:var(--ok);background:#e3efe3}.bdg.active{color:var(--active);background:#e2ecf7}.bdg.warn{color:var(--warn);background:#f6ead0}.bdg.bad{color:var(--bad);background:#f4ddd5}.bdg.hold{color:var(--hold);background:#e4e8f0}.bdg.mute{color:var(--soft);background:#eae5da}
.two{display:grid;grid-template-columns:1.4fr 1fr;gap:22px}@media(max-width:760px){.two{grid-template-columns:1fr}.pulse{grid-template-columns:1fr;text-align:center}.pmeta{justify-self:center;text-align:center}.pmeta .row{justify-content:center}}
.att{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:6px 18px 14px;box-shadow:var(--sh)} .att ul{list-style:none;margin:0;padding:0}
.att li{padding:11px 0;border-bottom:1px solid var(--line);font-size:13px}.att li:last-child{border:0}
.tid{font-family:"IBM Plex Mono",monospace;font-weight:600;color:var(--brandink);margin-right:8px}
.side{display:flex;flex-direction:column;gap:18px} .mini{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:15px 18px;box-shadow:var(--sh)}
.mini h3{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--soft);margin:0 0 10px}
.rr{display:flex;gap:9px;align-items:baseline;padding:6px 0;border-bottom:1px solid var(--line);font-size:12.5px}.rr:last-child{border:0}
.rd{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--soft);white-space:nowrap} .rt{color:var(--ink)}
/* decisions collapsed */
.decwrap{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--sh);overflow:hidden}
.decwrap>summary{cursor:pointer;list-style:none;padding:14px 18px;display:flex;align-items:center;gap:10px}
.decwrap>summary::-webkit-details-marker{display:none} .decwrap>summary:hover{background:var(--paper-2)}
.decsum{color:var(--soft);font-size:12.5px} .decwrap .open{margin-left:auto;font-size:12px;color:var(--brandink);font-weight:600}
.decwrap[open] .open::after{content:" (close)"} .pill{font-family:"IBM Plex Mono",monospace;font-size:11px;padding:1px 7px;border-radius:99px;border:1px solid var(--line2);color:var(--soft)}
.decin{padding:4px 14px 14px;border-top:1px solid var(--line)} .dtools{display:flex;gap:8px;align-items:center;margin:10px 0;flex-wrap:wrap}
.dtools input{flex:1;min-width:160px;font-size:13px;padding:7px 12px;border:1px solid var(--line2);border-radius:8px;background:var(--card);font-family:inherit}
.dtools input:focus{outline:2px solid var(--brand)} .fbtn{font-family:"IBM Plex Mono",monospace;font-size:11px;padding:5px 11px;border-radius:99px;border:1px solid var(--line2);background:var(--card);color:var(--soft);cursor:pointer}
.fbtn.on{background:var(--brand);color:#fff;border-color:var(--brand)} .declist{max-height:460px;overflow:auto}
.dec{border-bottom:1px solid var(--line)} .dec>summary{cursor:pointer;list-style:none;padding:9px 4px;display:grid;grid-template-columns:64px 1fr auto;gap:10px;align-items:center}
.dec>summary::-webkit-details-marker{display:none} .dec>summary:hover{background:var(--paper-2)} .did{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:12px;color:var(--brandink)} .dt{font-size:12.5px}
.dbody{padding:2px 4px 12px 78px;font-size:12.5px;color:var(--soft)} .sel{display:block;background:var(--paper-2);color:var(--ink);padding:8px 11px;border-radius:7px;margin-bottom:6px} .empty{padding:16px;text-align:center;color:var(--soft)}
/* flow + timeline */
.flowcard{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--sh);padding:18px;overflow:auto;text-align:center}
.cap{font-size:12px;color:var(--soft);font-style:italic;margin-top:8px} .mermaid{margin:0}
.tlcard{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--sh);padding:6px 18px}
.tlr{display:flex;gap:12px;align-items:baseline;padding:11px 0;border-bottom:1px solid var(--line);font-size:13px}.tlr:last-child{border:0}
.tld{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--soft);white-space:nowrap;min-width:84px} .tli{flex:1} .tln{color:var(--soft);font-size:12px}
.tlr.over .tld{color:var(--bad);text-decoration:line-through} .tlr.over{background:#fbf0ec;margin:0 -18px;padding-left:18px;padding-right:18px}
.specwrap{margin-top:18px} .speclist{max-height:540px}
.spc{border-bottom:1px solid var(--line)} .spc>summary{cursor:pointer;list-style:none;padding:9px 4px;font-size:12.5px;font-weight:500}
.spc>summary::-webkit-details-marker{display:none} .spc>summary::before{content:"▸ ";color:var(--soft)} .spc[open]>summary::before{content:"▾ "} .spc>summary:hover{background:var(--paper-2)}
.specbody{padding:4px 4px 14px 12px;font-size:12.5px;line-height:1.6}
.specbody h1,.specbody h2,.specbody h3,.specbody h4{font-family:"Fraunces",serif;margin:13px 0 6px;line-height:1.2}
.specbody h1{font-size:18px}.specbody h2{font-size:15px}.specbody h3{font-size:13.5px}
.specbody code{background:var(--paper-2);padding:1px 5px;border-radius:4px;font-size:11.5px}
.specbody pre{background:var(--paper-2);padding:10px;border-radius:8px;overflow:auto}.specbody pre code{background:none;padding:0}
.specbody table{border-collapse:collapse;font-size:11.5px;margin:6px 0}.specbody td,.specbody th{border:1px solid var(--line);padding:4px 8px;text-align:left}
.specbody ul,.specbody ol{padding-left:20px}.specbody blockquote{border-left:3px solid var(--line2);margin:6px 0;padding-left:12px;color:var(--soft)}
footer{margin-top:34px;padding-top:14px;border-top:1px solid var(--line2);color:var(--mute);font-family:"IBM Plex Mono",monospace;font-size:11px}
"""
JS=r"""
function decFilter(){const q=(document.getElementById('dq').value||'').toLowerCase();
 const f=document.querySelector('.fbtn.on').dataset.f;let n=0;
 document.querySelectorAll('.dec').forEach(d=>{const ok=(f==='all'||d.dataset.status===f)&&(!q||d.dataset.search.includes(q));d.style.display=ok?'':'none';if(ok)n++;});
 document.getElementById('dcount').textContent=n;document.getElementById('dempty').style.display=n?'none':'';}
document.addEventListener('click',e=>{if(e.target.classList.contains('fbtn')){document.querySelectorAll('.fbtn').forEach(b=>b.classList.remove('on'));e.target.classList.add('on');decFilter();}});
document.addEventListener('keydown',e=>{if(e.key==='/'&&e.target.tagName!=='INPUT'){e.preventDefault();const dq=document.getElementById('dq');if(dq){dq.closest('details').open=true;dq.focus();}}});
function specFilter(){const q=(document.getElementById('sq').value||'').toLowerCase();document.querySelectorAll('.spc').forEach(s=>{s.style.display=(!q||s.dataset.h.includes(q))?'':'none';});}
document.addEventListener('toggle',e=>{const s=e.target;if(s.classList&&s.classList.contains('spc')&&s.open&&!s.dataset.r){const src=s.querySelector('.src'),body=s.querySelector('.specbody');if(src&&body&&window.marked){body.innerHTML=marked.parse(src.textContent);s.dataset.r='1';}}},true);
"""
MERMAID = (r'''<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
mermaid.initialize({startOnLoad:true,theme:"base",themeVariables:{fontFamily:"IBM Plex Sans",primaryColor:"#fbf9f4",primaryBorderColor:"#cabfa8",primaryTextColor:"#211d17",lineColor:"#9a8f78",fontSize:"14px"}});</script>''') if mermaid else ""
MARKED='<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>' if spec_html else ""

HTMLDOC=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(pname)} — Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<!-- DASHBOARD META task_count={meta.get('task_count','?')} task_hash={meta.get('task_hash','')[:23]}… spec={meta.get('spec_version','?')} -->
<style>{CSS}</style>
<svg width="0" height="0"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="var(--brand)"/><stop offset="1" stop-color="var(--brand2)"/></linearGradient></defs></svg></head>
<body><header class="mast"><div class="mast-in"><span class="crumb">Execute</span><h1>{html.escape(pname)}</h1>
<span class="tv">{meta.get('task_count','?')} tasks · {len(phases)} phases · read-only view</span></div></header><div class="wrap">
<section><div class="pulse">{ring(complete/100)}
<div class="donwrap">{donut(segs)}<div class="legend">{legend}</div></div>
<div class="pmeta"><div class="row"><div><div class="big">{done_ph}<span style="color:var(--soft);font-size:18px">/{len(phases)}</span></div><div class="lbl">phases done</div></div>
<div><div class="big">{len(active)}</div><div class="lbl">active now</div></div></div>
<div class="row"><div><div class="big" style="color:var(--ok)">{meta.get('verification_debt','0')}</div><div class="lbl">verif debt</div></div>
<div><div class="big" style="color:var(--ok)">{meta.get('drift_deferrals','0')}</div><div class="lbl">drift</div></div></div></div></div></section>
<section><h2 class="st">Phase map · {len(phases)} phases</h2><div class="grid">{cells}</div>
<div class="glegend"><span><b style="background:var(--ok)"></b>complete</span><span><b style="background:var(--active)"></b>active</span>
<span><b style="background:var(--warn)"></b>partial</span><span><b style="background:var(--bad)"></b>blocked</span><span style="margin-left:auto">fill = % done · hover for detail</span></div>
<div class="front">{front}</div></section>
{flow}
{timeline_block}
<section><div class="two"><div><h2 class="st">Needs you</h2><div class="att"><ul>{att}</ul></div></div>
<div class="side"><div class="mini"><h3>Recent — last finished</h3>{recent_rows}</div></div></div></section>
<section>{decisions_block}</section>
<section>{spec_html}</section>
<footer>generated {meta.get('generated','')} · single read-only HTML view · state of record = task JSON</footer></div>
<script>{JS}</script>{MARKED}{MERMAID}</body></html>"""
OUT.write_text(HTMLDOC, encoding="utf-8")
print(f"{OUT.name}: {len(phases)} phases, {len(decisions)} decisions, {len(recent)} recent, "
      f"timeline={len(timeline)}, mermaid={'yes' if mermaid else 'no'}, {len(HTMLDOC)} bytes")
