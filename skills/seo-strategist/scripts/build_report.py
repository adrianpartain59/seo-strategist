#!/usr/bin/env python3
"""Build the local review site for an seo-plan folder.

Usage:
  python3 build_report.py seo-plan/<domain>

Reads strategy.csv, blog.csv, redirects.csv, summary.md, meta-fixes.md and plans/*.md and
writes index.html plus plans/<slug>.html (and meta-fixes.html). Open it with
  python3 -m http.server 8765 --directory seo-plan/<domain>
Standard library only; works offline.
"""
import csv, datetime, html, json, os, re, sys

CSS = """
:root{--bg:#fbfbfa;--fg:#1d1d1f;--mut:#6b6b70;--line:#e4e4e2;--card:#fff;--acc:#2f6fed;--accbg:#eaf1ff;--ok:#1f8a4c;--warn:#b26b00;--code:#f4f4f2}
@media (prefers-color-scheme:dark){:root{--bg:#141416;--fg:#ececee;--mut:#9c9ca3;--line:#2c2c30;--card:#1c1c1f;--acc:#7aa5ff;--accbg:#1f2a44;--ok:#5cc98a;--warn:#e0a54a;--code:#232327}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Inter","Segoe UI",sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:28px 16px 80px}a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:28px;margin:0 0 4px;letter-spacing:-.02em}h2{font-size:20px;margin:36px 0 12px}h3{font-size:16px;margin:22px 0 6px}
.mut{color:var(--mut)}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:18px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}.card b{display:block;font-size:22px}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--card)}table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}th{position:sticky;top:0;background:var(--card);font-weight:600;white-space:nowrap;cursor:pointer}
td.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}td.note{min-width:280px;max-width:420px}
.pill{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;background:var(--accbg);color:var(--acc);white-space:nowrap}
.pill.ex{background:transparent;border:1px solid var(--line);color:var(--mut)}
.filters{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}.filters button{border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:99px;padding:4px 12px;font:inherit;font-size:13px;cursor:pointer}
.filters button.on{background:var(--acc);border-color:var(--acc);color:#fff}input.q{border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:99px;padding:5px 12px;font:inherit;font-size:13px;min-width:200px}
.md p{margin:8px 0}.md ul{margin:6px 0 6px 20px;padding:0}.md li{margin:3px 0}pre{background:var(--code);padding:12px;border-radius:10px;overflow-x:auto;font-size:12.5px}code{background:var(--code);padding:1px 4px;border-radius:4px;font-size:.92em}
.sec{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:6px 18px 14px;margin:14px 0;position:relative}
.sec .copy{position:absolute;top:12px;right:12px;border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:8px;padding:3px 10px;font-size:12px;cursor:pointer}
.lbl{font-weight:600;color:var(--mut);font-size:12.5px;text-transform:uppercase;letter-spacing:.04em;margin-top:12px}
.serp{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;max-width:640px}.serp .u{font-size:12.5px;color:var(--mut)}
.serp .t{font-size:19px;color:#1a0dab;margin:2px 0}@media (prefers-color-scheme:dark){.serp .t{color:#8ab4f8}}.serp .d{font-size:13.5px;color:var(--mut)}
.len{font-size:12px}.len.bad{color:var(--warn)}.len.good{color:var(--ok)}nav.top{font-size:13px;margin-bottom:14px}
.h1tag{display:inline-block;font-size:11px;border:1px solid var(--line);border-radius:6px;padding:0 6px;margin-right:6px;color:var(--mut);vertical-align:middle}
"""

JS = """
function copySec(b){const s=b.closest('.sec');const t=s.querySelectorAll('[data-copy]');let out=[];t.forEach(e=>out.push(e.innerText));navigator.clipboard.writeText(out.join('\\n\\n')).then(()=>{b.textContent='Copied';setTimeout(()=>b.textContent='Copy copy',1200)})}
function filt(){const q=(document.getElementById('q')||{}).value||'';const on=[...document.querySelectorAll('.filters button.on')].map(b=>b.dataset.f);
document.querySelectorAll('#strategy tbody tr').forEach(r=>{const okF=on.length===0||on.every(f=>r.dataset.tags.includes(f));const okQ=!q||r.innerText.toLowerCase().includes(q.toLowerCase());r.style.display=okF&&okQ?'':'none'})}
function tog(b){b.classList.toggle('on');filt()}
function sortBy(th){const tb=th.closest('table').tBodies[0];const i=[...th.parentNode.children].indexOf(th);const asc=th.dataset.asc!=='1';th.dataset.asc=asc?'1':'0';
const rows=[...tb.rows];rows.sort((a,b)=>{let x=a.cells[i].dataset.v??a.cells[i].innerText,y=b.cells[i].dataset.v??b.cells[i].innerText;const nx=parseFloat(x),ny=parseFloat(y);
if(!isNaN(nx)&&!isNaN(ny))return asc?nx-ny:ny-nx;if(isNaN(nx)&&!isNaN(ny))return 1;if(!isNaN(nx)&&isNaN(ny))return -1;return asc?x.localeCompare(y):y.localeCompare(x)});rows.forEach(r=>tb.appendChild(r))}
"""


TIER = {"Low": 1, "Medium": 2, "High": 3, "Easy": 1, "Hard": 3}


def esc(s):
    return html.escape(str(s or ""))


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"<i>\1</i>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<!href=")(?<!">)(https?://[^\s<)]+[^\s<).,])', r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)
    return s


def md(text):
    """Small Markdown renderer: headings, lists, tables, fences, paragraphs."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        l = lines[i]
        if re.match(r"^(```|~~~)", l):
            fence = l[:3]
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith(fence):
                buf.append(lines[j])
                j += 1
            out.append(f"<pre><code>{esc(chr(10).join(buf))}</code></pre>")
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", l)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n + 1}>{inline(m.group(2))}</h{n + 1}>")
            i += 1
            continue
        if l.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            hdr = [c.strip() for c in l.strip().strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            t = "<div class=tbl><table><thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in hdr) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(t + "</tbody></table></div>")
            i = j
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", l):
            tag = "ol" if re.match(r"^\s*\d+\.", l) else "ul"
            items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i]))
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if l.strip():
            buf = [l]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||```|~~~|\s*([-*]|\d+\.)\s)", lines[i]):
                buf.append(lines[i])
                i += 1
            out.append("<p>" + "<br>".join(inline(x) for x in buf) + "</p>")
            continue
        i += 1
    return "\n".join(out)


def page(title, body, depth=0):
    up = "../" * depth
    return (f"<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{esc(title)}</title><style>{CSS}</style></head><body><div class=wrap>{body}</div><script>{JS}</script></body></html>")


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(v):
    try:
        return float(str(v).replace(",", "").replace("$", ""))
    except ValueError:
        return None


def fmt(v, money=False):
    n = num(v)
    if n is None:
        return esc(v) if v and not str(v).startswith("=") else ""
    return (f"${n:,.2f}" if n < 100 else f"${n:,.0f}") if money else f"{n:,.0f}"


def slug_of(plan):
    return os.path.splitext(os.path.basename(plan))[0]


def len_badge(n, lo, hi):
    cls = "good" if lo <= n <= hi else "bad"
    return f"<span class='len {cls}'>{n} chars (target {lo}–{hi})</span>"


def render_plan(root, path, row):
    text = open(path, encoding="utf-8").read()
    slug = slug_of(path)
    hdr = dict(re.findall(r"^(Page Type|Plan Type|Company Type|Page URL|Target Keyword):\s*(.+)$", text, re.M))
    title = re.search(r"^Page Title:\s*(.+)$", text, re.M)
    desc = re.search(r"^Page Meta Description:\s*(.+)$", text, re.M)
    if not title:
        m = re.search(r"Section:\s*title\s*\nOriginal Content:\s*\n?.*?\nSuggested Revision:\s*\n?(.+)", text)
        title = m
    if not desc:
        m = re.search(r"Section:\s*meta-description\s*\nOriginal Content:\s*\n?.*?\nSuggested Revision:\s*\n?(.+)", text)
        desc = m
    body = [f"<nav class=top><a href='../index.html'>← All pages</a></nav>",
            f"<h1>{esc(hdr.get('Target Keyword', slug))}</h1>",
            f"<p class=mut><span class='pill{'' if 'New' in hdr.get('Page Type', '') else ' ex'}'>{esc(hdr.get('Page Type', ''))}</span> "
            f"<span class=pill>{esc(hdr.get('Plan Type', ''))}</span> &nbsp; "
            f"<a href='{esc(hdr.get('Page URL', ''))}' target=_blank rel=noopener>{esc(hdr.get('Page URL', ''))}</a></p>"]
    if row and row.get("Why This Page"):
        body.append(f"<p>{inline(row['Why This Page'])}</p>")
    if title or desc:
        t = title.group(1).strip() if title else ""
        d = desc.group(1).strip() if desc else ""
        body.append("<h2>How it shows on Google</h2><div class=serp>"
                    f"<div class=u>{esc(hdr.get('Page URL', ''))}</div><div class=t>{esc(t)}</div><div class=d>{esc(d)}</div></div>"
                    f"<p>{len_badge(len(t), 45, 60) if t else ''} &nbsp; {len_badge(len(d), 140, 160) if d else ''}</p>")
    # split into sections at "## "
    chunks = re.split(r"(?m)^(?=## )", text)
    for ch in chunks:
        if not ch.startswith("## "):
            continue
        head = ch.splitlines()[0][3:].strip()
        rest = "\n".join(ch.splitlines()[1:])
        is_copy = "Sub-Headings (H3)" in rest
        htype = re.search(r"(?:Heading Type|Recommended Heading Type):\s*(h\d)", rest)
        badge = f"<span class=h1tag>{esc(htype.group(1).upper())}</span>" if htype else ""
        inner = rest
        if is_copy:
            pre, _, post = rest.partition("Sub-Headings (H3)")
            post = post.split("\n", 1)[1] if "\n" in post else ""
            m = re.search(r"(?m)^(CTA Recommendations:|Key Components to Include:)", post)
            copy_part, tail = (post[:m.start()], post[m.start():]) if m else (post, "")
            pre = re.sub(r"(?m)^(Heading Type|Recommended Heading|Recommended Heading Type|Suggested Heading Name):.*\n?", "", pre)
            inner = (md(re.sub(r"(?m)^(Rationale|Why Include|Placement):", r"**\1:**", pre))
                     + "<div class=lbl>Ready-to-use copy</div><div data-copy>" + md(copy_part) + "</div>"
                     + md(re.sub(r"(?m)^(CTA Recommendations|Key Components to Include|Design Suggestions):", r"**\1:**", tail)))
            btn = "<button class=copy onclick='copySec(this)'>Copy copy</button>"
        else:
            inner = md(inner)
            btn = ""
        body.append(f"<div class='sec md'>{btn}<h2>{badge}{inline(head)}</h2>{inner}</div>")
    html_out = page(hdr.get("Target Keyword", slug), "\n".join(body), depth=1)
    with open(os.path.join(root, "plans", slug + ".html"), "w", encoding="utf-8") as f:
        f.write(html_out)
    return slug + ".html"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1].rstrip("/")
    domain = os.path.basename(root)
    rows = read_csv(os.path.join(root, "strategy.csv"))
    blog = read_csv(os.path.join(root, "blog.csv"))
    redirects = read_csv(os.path.join(root, "redirects.csv"))
    plan_dir = os.path.join(root, "plans")
    plans = sorted(f for f in os.listdir(plan_dir) if f.endswith(".md")) if os.path.isdir(plan_dir) else []

    by_plan = {}
    for r in rows + blog:
        p = (r.get("Page Plan") or "").strip()
        if p:
            by_plan[slug_of(p)] = r
    rendered = {}
    for p in plans:
        rendered[slug_of(p)] = render_plan(root, os.path.join(plan_dir, p), by_plan.get(slug_of(p)))

    def plan_link(r):
        p = (r.get("Page Plan") or "").strip()
        s = slug_of(p) if p else ""
        return f"<a href='plans/{rendered[s]}'>Open plan</a>" if s in rendered else "<span class=mut>not written</span>"

    status_n = {}
    type_n = {}
    for r in rows:
        status_n[r.get("Status", "")] = status_n.get(r.get("Status", ""), 0) + 1
        type_n[r.get("Page Type", "")] = type_n.get(r.get("Page Type", ""), 0) + 1
    vol = sum(num(r.get("Monthly Search Volume (US)")) or 0 for r in rows)
    sources = sorted({r.get("Metric Source", "") for r in rows if r.get("Metric Source")})
    b = [f"<h1>SEO plan: {esc(domain)}</h1>",
         f"<p class=mut>Built {datetime.date.today():%B %-d, %Y} · metrics: {esc(', '.join(sources) or 'see summary')}</p>",
         "<div class=cards>",
         f"<div class=card><b>{len(rows)}</b>landing pages</div>",
         f"<div class=card><b>{status_n.get('Existing page (update)', 0)}</b>existing to update</div>",
         f"<div class=card><b>{status_n.get('New page', 0)}</b>new to build</div>",
         f"<div class=card><b>{len(blog)}</b>blog posts</div>",
         f"<div class=card><b>{len(rendered)}</b>page plans written</div>",
         f"<div class=card><b>{vol:,.0f}</b>monthly searches targeted</div>" if vol else "",
         "</div>"]
    summ = os.path.join(root, "summary.md")
    if os.path.exists(summ):
        b.append("<div class=md>" + md(open(summ, encoding="utf-8").read()) + "</div>")

    b.append("<h2>Landing pages</h2><div class=filters>")
    for s in sorted(status_n):
        b.append(f"<button data-f='{esc(s)}' onclick='tog(this)'>{esc(s)} ({status_n[s]})</button>")
    for t in sorted(type_n):
        b.append(f"<button data-f='{esc(t)}' onclick='tog(this)'>{esc(t)} ({type_n[t]})</button>")
    b.append("<input id=q class=q placeholder='Search' oninput='filt()'></div>")
    cols = ["Target Keyword", "Page Type", "Status", "Page", "Why This Page", "Demand", "Difficulty", "Volume", "KD", "CPC", "Traffic value",
            "Your views (12 mo)", "Your clicks (12 mo)", "Plan"]
    b.append("<div class=tbl><table id=strategy><thead><tr>" + "".join(f"<th onclick='sortBy(this)'>{c}</th>" for c in cols)
             + "</tr></thead><tbody>")
    for r in rows:
        url = r.get("URL", "")
        path = re.sub(r"^https?://[^/]+", "", url) or "/"
        tv = r.get("Traffic Value", "")
        if not num(tv):
            v, c = num(r.get("Monthly Search Volume (US)")), num(r.get("CPC"))
            tv = v * c if v is not None and c is not None else ""
        tags = f"{r.get('Status', '')}|{r.get('Page Type', '')}"
        ex = " ex" if r.get("Status", "").startswith("Existing") else ""
        b.append(f"<tr data-tags='{esc(tags)}'><td><b>{esc(r.get('Target Keyword'))}</b></td><td>{esc(r.get('Page Type'))}</td>"
                 f"<td><span class='pill{ex}'>{'Update' if ex else 'New'}</span></td>"
                 f"<td><a href='{esc(url)}' target=_blank rel=noopener>{esc(path)}</a></td>"
                 f"<td class=note>{inline(r.get('Why This Page'))}</td>"
                 f"<td data-v='{TIER.get(r.get('Demand', ''), '')}'>{esc(r.get('Demand'))}</td>"
                 f"<td data-v='{TIER.get(r.get('Difficulty', ''), '')}'>{esc(r.get('Difficulty'))}</td>"
                 f"<td class=num data-v='{num(r.get('Monthly Search Volume (US)')) or ''}'>{fmt(r.get('Monthly Search Volume (US)'))}</td>"
                 f"<td class=num>{fmt(r.get('KD'))}</td><td class=num>{fmt(r.get('CPC'), True)}</td>"
                 f"<td class=num data-v='{num(tv) or ''}'>{fmt(tv, True)}</td>"
                 f"<td class=num>{fmt(r.get('Your Google Views (12 mo)'))}</td><td class=num>{fmt(r.get('Your Clicks (12 mo)'))}</td>"
                 f"<td>{plan_link(r)}</td></tr>")
    b.append("</tbody></table></div>")

    if blog:
        b.append("<h2>Blog plan</h2><div class=tbl><table><thead><tr>" + "".join(
            f"<th onclick='sortBy(this)'>{c}</th>" for c in ["Target Keyword", "Month", "Why This Post", "Demand", "Difficulty", "Volume", "KD", "Links To", "Plan"])
            + "</tr></thead><tbody>")
        for r in blog:
            b.append(f"<tr><td><b>{esc(r.get('Target Keyword'))}</b></td><td>{esc(r.get('Month'))}</td>"
                     f"<td class=note>{inline(r.get('Why This Post'))}</td><td>{esc(r.get('Demand'))}</td><td>{esc(r.get('Difficulty'))}</td>"
                     f"<td class=num>{fmt(r.get('Monthly Search Volume (US)'))}</td>"
                     f"<td class=num>{fmt(r.get('KD'))}</td><td>{inline(r.get('Links To'))}</td><td>{plan_link(r)}</td></tr>")
        b.append("</tbody></table></div>")
    if redirects:
        b.append("<h2>Redirects</h2><div class=tbl><table><thead><tr><th>From</th><th>To</th><th>Type</th><th>Why</th></tr></thead><tbody>")
        for r in redirects:
            b.append(f"<tr><td>{esc(r.get('From'))}</td><td>{esc(r.get('To'))}</td><td>{esc(r.get('Type'))}</td><td>{inline(r.get('Why'))}</td></tr>")
        b.append("</tbody></table></div>")
    mf = os.path.join(root, "meta-fixes.md")
    if os.path.exists(mf):
        with open(os.path.join(root, "meta-fixes.html"), "w", encoding="utf-8") as f:
            f.write(page("Meta fixes", "<nav class=top><a href='index.html'>← All pages</a></nav><div class=md>"
                         + md(open(mf, encoding="utf-8").read()) + "</div>"))
        b.append("<h2>Meta title and description fixes</h2><p><a href='meta-fixes.html'>Open the meta fixes</a> for pages outside the plan.</p>")
    b.append("<h2>Files</h2><p class=mut>strategy.csv and blog.csv open in Google Sheets or Excel. Every plan is also a Markdown file in plans/ you can paste into an AI coding tool with the current page.</p>")
    with open(os.path.join(root, "index.html"), "w", encoding="utf-8") as f:
        f.write(page(f"SEO plan: {domain}", "\n".join(b)))
    print(f"Wrote {os.path.join(root, 'index.html')} with {len(rows)} rows, {len(blog)} blog posts, {len(rendered)} plans.")


if __name__ == "__main__":
    main()
