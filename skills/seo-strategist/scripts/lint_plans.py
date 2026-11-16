#!/usr/bin/env python3
"""Lint an seo-plan folder: strategy.csv, blog.csv and every plans/*.md page plan.

Usage:
  python3 lint_plans.py seo-plan/<domain> [--strict]

Errors (exit 1) break the format or a hard copy rule. Warnings are rhythm and length
drift worth a look. --strict turns warnings into errors.
"""
import argparse, csv, json, os, re, sys, urllib.request
from collections import Counter

HEADER = ["SEO Plan for:", "Page Type:", "Plan Type:", "Company Type:", "Page URL:", "Target Keyword:"]
DESIGN = ["Full-width hero", "Centered hero", "Two-column split", "Three-column layout", "Grid of cards",
          "Feature cards", "Alternating panels", "Dashboard preview", "Horizontal timeline",
          "Process flow with phases", "Checklist / steps list", "Stat row", "Stat/metric tiles",
          "Trust indicator strip", "Testimonial cards", "Comparison table", "Side-by-side comparison",
          "Tabbed content", "Accordion", "CTA banner"]
HYPE = ["journey", "unlock", "seamless", "effortless", "revolutionary", "empower", "game-changer",
        "game changer", "supercharge", "best-in-class", "world-class", "cutting-edge", "guarantee"]
CONTRACTION = re.compile(r"\b\w+(?:n't|'re|'ll|'ve|'d|'m)\b|\b(?:it|that|there|what|here|who|let)'s\b", re.I)
SENT_SPLIT = re.compile(r"(?<=[.?!])[\"”’)]?\s+(?=[A-Z0-9\"“(])")
STRATEGY_COLS = ["Target Keyword", "Page Type", "Plan Type", "Status", "URL", "Why This Page", "Demand", "Difficulty"]


def norm(s):
    return re.sub(r"[®™]", "", s or "").lower().strip()


def sentences(text):
    text = re.sub(r"\b(e\.g|i\.e|vs|etc|approx|U\.S|Dr|Mr|Ms|No)\.", lambda m: m.group(0).replace(".", "§"), text)
    parts = [p for p in SENT_SPLIT.split(text.strip()) if p.strip()]
    return parts


def strip_quotes(text):
    return re.sub(r"[\"“][^\"”]*[\"”]", "", text)


class Report:
    def __init__(self):
        self.items = []

    def err(self, where, msg):
        self.items.append(("ERROR", where, msg))

    def warn(self, where, msg):
        self.items.append(("warn", where, msg))


def parse_plan(text):
    """Return header fields, meta, sections (list of dicts), json blocks, sources flag."""
    lines = text.splitlines()
    hdr = {}
    for l in lines[:20]:
        for h in HEADER:
            if l.startswith(h) or l.startswith("# " + h):
                hdr[h] = l.split(":", 1)[1].strip()
    meta = {}
    m = re.search(r"^Page Title:\s*(.+)$", text, re.M)
    if m:
        meta["title"] = m.group(1).strip()
    m = re.search(r"^Page Meta Description:\s*(.+)$", text, re.M)
    if m:
        meta["desc"] = m.group(1).strip()
    # existing-page revisions
    for sec, key in (("title", "title"), ("meta-description", "desc")):
        m = re.search(rf"^Section:\s*{sec}\s*\nOriginal Content:\s*\n?(.*?)\nSuggested Revision:\s*\n?(.*?)(?:\n\s*\n|\Z)",
                      text, re.M | re.S)
        if m:
            meta[key] = m.group(2).strip().splitlines()[0].strip()

    sections, cur, mode, h3 = [], None, None, None
    for l in lines:
        if l.startswith("## "):
            title = l[3:].strip()
            if title.startswith(("Suggested Meta Data", "Page Overview", "Current Page Optimization",
                                 "Missing Sections to Add", "Recommended Structured Data", "Sources")):
                cur, mode = None, None
                continue
            cur = {"title": re.sub(r"^\d+\.\s*", "", title), "raw": title, "h3": [], "fields": set(),
                   "heading_type": None, "design": None, "kind": "new" if re.match(r"^\d+\.", title) else
                   ("merge" if title.startswith("Add to Existing Section") else "added")}
            sections.append(cur)
            mode = None
            continue
        if cur is None:
            continue
        s = l.strip()
        for f in ("Heading Type:", "Recommended Heading Type:", "Rationale:", "Why Include:", "CTA Recommendations:",
                  "Key Components to Include:", "Design Suggestions:", "Placement:", "Sub-Headings (H3)"):
            if s.startswith(f):
                cur["fields"].add(f.rstrip(":"))
                if f in ("Heading Type:", "Recommended Heading Type:"):
                    cur["heading_type"] = s.split(":", 1)[1].strip().lower()
                mode = f
        if s.startswith("### "):
            h3 = {"title": s[4:].strip(), "bullets": []}
            cur["h3"].append(h3)
            mode = "copy"
            continue
        if mode == "copy" and re.match(r"^[-*]\s+", s) and h3 is not None:
            h3["bullets"].append(re.sub(r"^[-*]\s+", "", s))
        elif mode in ("CTA Recommendations:", "Key Components to Include:"):
            pass
        elif mode == "Design Suggestions:" and s and not s.startswith("Design Suggestions"):
            cur["design"] = cur["design"] or s
    blocks = re.findall(r"```json\s*\n(.*?)\n```", text, re.S)
    return hdr, meta, sections, blocks


_LIVE = {}


def is_live(url):
    """GET the URL once (cached); True if it returns 200 without redirecting to the homepage."""
    if url not in _LIVE:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "seo-strategist-lint"})
            with urllib.request.urlopen(req, timeout=10) as r:
                final = r.geturl().rstrip("/")
                home = re.match(r"https?://[^/]+", url).group(0)
                _LIVE[url] = r.status == 200 and (final != home or url.rstrip("/") == home)
        except Exception:
            _LIVE[url] = False
    return _LIVE[url]


def lint_plan(path, rep, page_urls, planned=frozenset(), online=False):
    name = os.path.relpath(path)
    text = open(path, encoding="utf-8").read()
    hdr, meta, sections, blocks = parse_plan(text)
    for h in HEADER:
        if h not in hdr:
            rep.err(name, f"missing header field '{h}'")
    existing = hdr.get("Page Type:", "").lower().startswith("existing")
    plan_type = hdr.get("Plan Type:", "")
    kw = norm(hdr.get("Target Keyword:", ""))

    if "## Page Overview" not in text:
        rep.warn(name, "no Page Overview")
    if not existing:
        for k, lo, hi, label in (("title", 45, 60, "Page Title"), ("desc", 140, 160, "Meta description")):
            v = meta.get(k)
            if not v:
                rep.err(name, f"missing {label}")
            elif not lo <= len(v) <= hi:
                (rep.err if len(v) > hi else rep.warn)(name, f"{label} is {len(v)} chars (want {lo}-{hi}): {v!r}")
    else:
        if "## Current Page Optimization Suggestions" not in text:
            rep.err(name, "existing page plan lacks '## Current Page Optimization Suggestions'")
        if "## Missing Sections to Add" not in text:
            rep.err(name, "existing page plan lacks '## Missing Sections to Add'")
        for k, hi, label in (("title", 60, "Suggested title"), ("desc", 160, "Suggested meta description")):
            if meta.get(k) and len(meta[k]) > hi:
                rep.err(name, f"{label} is {len(meta[k])} chars (max {hi})")
    t = norm(meta.get("title", ""))
    if t and kw and kw not in t and not existing:
        rep.err(name, f"target keyword '{kw}' not in title")
    elif t and kw and not t.startswith(kw) and not existing:
        rep.warn(name, "title does not start with the target keyword")

    h1s = [s for s in sections if s["heading_type"] == "h1"]
    if not existing and len(h1s) != 1:
        rep.err(name, f"{len(h1s)} H1 sections (want exactly 1)")
    if not existing and h1s and kw and kw not in norm(h1s[0]["title"]) and plan_type != "Blog":
        rep.warn(name, "H1 does not contain the target keyword")
    kw_h2 = sum(1 for s in sections if s["heading_type"] == "h2" and kw and kw in norm(s["title"]))
    if kw_h2 > 1:
        rep.warn(name, f"target keyword appears in {kw_h2} H2s (H2s should carry sub-intents)")

    faq = [s for s in sections if "frequently asked questions" in s["title"].lower() or s["title"].lower().endswith("faq")]
    if not faq:
        rep.err(name, "no FAQ section")
    elif existing:
        n = len(faq[-1]["h3"])
        if not 3 <= n <= 5:
            rep.warn(name, f"FAQ merge adds {n} questions (want 3-5 new ones)")
    else:
        n = len(faq[-1]["h3"])
        if plan_type == "Blog":
            if not 5 <= n <= 7:
                rep.warn(name, f"blog FAQ has {n} questions (want 5-7)")
        elif n != 7:
            rep.err(name, f"FAQ has {n} questions (want 7)")
        if sections and sections[-1] is not faq[-1]:
            rep.warn(name, "FAQ is not the last section")

    for s in sections:
        where = f"{name} § {s['title'][:40]}"
        need = ["Key Components to Include", "Design Suggestions"]
        if s["kind"] == "new":
            need += ["Heading Type", "Rationale", "CTA Recommendations", "Sub-Headings (H3)"]
        else:
            need += ["Why Include", "Sub-Headings (H3)"]
            if s["kind"] == "added":
                need.append("Placement")
        for f in need:
            if f not in s["fields"]:
                rep.err(where, f"missing '{f}'")
        if s["design"] and not any(s["design"].lower().startswith(p.lower()) for p in DESIGN):
            rep.warn(where, f"design suggestion not from the pattern list: {s['design'][:50]!r}")
        if s["heading_type"] == "h1" and len(s["h3"]) != 1:
            rep.warn(where, f"H1 section has {len(s['h3'])} H3s (want 1)")

    bullets = [b for s in sections for h in s["h3"] for b in h["bullets"]]
    h3s = [h for s in sections for h in s["h3"]]
    if not bullets:
        rep.err(name, "no copy bullets found under '### ' H3 headings")
        return
    sent_counts = Counter(min(len(sentences(b)), 4) for b in bullets)
    two = sent_counts.get(2, 0) / len(bullets)
    if two < 0.7:
        rep.warn(name, f"only {two:.0%} of bullets are 2 sentences (want most); distribution {dict(sent_counts)}")
    bad_h3 = [h["title"] for h in h3s if not 1 <= len(h["bullets"]) <= 2]
    if bad_h3:
        rep.warn(name, f"{len(bad_h3)} H3s without 1-2 bullets, e.g. {bad_h3[0]!r}")
    words = [len(b.split()) for b in bullets]
    sents = [len(x.split()) for b in bullets for x in sentences(b)]
    if sum(sents) / len(sents) > 18:
        rep.warn(name, f"average sentence is {sum(sents)/len(sents):.1f} words (want 12-16)")
    total = sum(words)
    lo, hi = (500, 2200) if existing else (800, 2200)
    if not lo <= total <= hi:
        rep.warn(name, f"{total} words of copy (typical {lo}-{hi})")

    all_sents = Counter(" ".join(x.split()) for b in bullets for x in sentences(b) if len(x.split()) >= 5)
    rep_s = [(t, n) for t, n in all_sents.items() if n >= 2]
    if rep_s:
        t, n = max(rep_s, key=lambda x: x[1])
        rep.warn(name, f"{len(rep_s)} sentences repeated on the page, e.g. {n}x {t[:70]!r}")
    brand = (hdr.get("SEO Plan for:") or "").strip()
    if brand:
        run = best = 0
        for b in bullets:
            run = run + 1 if b.startswith(brand) else 0
            best = max(best, run)
        if best > 3:
            rep.warn(name, f"{best} bullets in a row start with {brand!r} (vary openings)")
    copy = "\n".join(bullets + [h["title"] for h in h3s] + [s["title"] for s in sections])
    for ch, label in (("—", "em dash"), ("–", "en dash"), ("!", "exclamation mark"), (";", "semicolon")):
        n = copy.count(ch)
        if n:
            rep.err(name, f"{n} {label}(s) in copy")
    hype = [w for w in HYPE if re.search(rf"\b{re.escape(w)}\b", copy, re.I)]
    if hype:
        rep.err(name, f"hype words in copy: {', '.join(hype)}")
    if re.search(r"#1\b", copy):
        rep.warn(name, "'#1' in copy: only with a cited source")
    contr = CONTRACTION.findall(strip_quotes("\n".join(bullets)))
    if contr:
        rep.warn(name, f"{len(contr)} contractions outside quotes, e.g. {contr[0]!r}")
    for h in [s["title"] for s in sections] + [h["title"] for h in h3s]:
        if "&" in h:
            rep.err(name, f"'&' in heading {h!r}")

    if len(blocks) < 2:
        rep.err(name, f"{len(blocks)} JSON-LD blocks (want 3: FAQPage, page type, Organization)")
    types = []
    for b in blocks:
        try:
            d = json.loads(b)
            types.append(d.get("@type") if isinstance(d, dict) else "list")
            if isinstance(d, dict) and d.get("@type") == "FAQPage" and faq and not existing:
                qs = [norm(q.get("name", "")) for q in d.get("mainEntity", [])]
                visible = [norm(h["title"]) for h in faq[-1]["h3"]]
                if visible and qs[:len(visible)] != visible and set(visible) - set(qs):
                    rep.warn(name, "FAQPage questions do not match the visible FAQ")
        except Exception as e:
            rep.err(name, f"invalid JSON-LD: {e}")
    if blocks and "FAQPage" not in types:
        rep.err(name, "no FAQPage JSON-LD")
    if plan_type in ("Informational", "Blog") and "## Sources" not in text:
        rep.err(name, "informational plan without a '## Sources' section")

    if page_urls:
        host = re.match(r"https?://([^/]+)", hdr.get("Page URL:", "") or "")
        if host:
            own = re.findall(rf"https?://{re.escape(host.group(1))}[^\s)\"'<>,]*", "\n".join(bullets))
            for u in sorted(set(own)):
                u2 = u.rstrip(".")
                if u2.rstrip("/") not in page_urls and not (online and is_live(u2)):
                    rep.warn(name, f"links to {u2}, which is not in the page map"
                             + (" and did not load" if online else " (run with --online to check it live)"))
            body = "\n".join(bullets)
            for u in sorted(planned):
                for m in re.finditer(re.escape(u) + r"/?(?![\w/-])", body):
                    if "(planned)" not in body[m.end():m.end() + 12]:
                        rep.warn(name, f"link to planned page {u} without '(planned)' after it")
                        break


def lint_strategy(root, rep):
    path = os.path.join(root, "strategy.csv")
    urls, planned = set(), set()
    if not os.path.exists(path):
        rep.err("strategy.csv", "missing")
        return urls, planned
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    cols = rows[0].keys() if rows else []
    for c in STRATEGY_COLS:
        if c not in cols:
            rep.err("strategy.csv", f"missing column '{c}'")
    kws = Counter(norm(r.get("Target Keyword")) for r in rows)
    for k, n in kws.items():
        if n > 1:
            rep.err("strategy.csv", f"keyword {k!r} on {n} rows (one keyword per page)")
    us = Counter((r.get("URL") or "").rstrip("/") for r in rows)
    for u, n in us.items():
        if n > 1:
            rep.err("strategy.csv", f"URL {u} on {n} rows")
    for r in rows:
        urls.add((r.get("URL") or "").rstrip("/"))
        st = r.get("Status", "")
        if st == "New page":
            planned.add((r.get("URL") or "").rstrip("/"))
        if st not in ("Existing page (update)", "New page"):
            rep.err("strategy.csv", f"bad Status {st!r} for {r.get('Target Keyword')}")
        note = r.get("Why This Page", "")
        if len(note.split()) < 8:
            rep.warn("strategy.csv", f"thin note for {r.get('Target Keyword')!r}")
        plan = r.get("Page Plan", "")
        if plan and not os.path.exists(os.path.join(root, plan)):
            rep.err("strategy.csv", f"Page Plan {plan} does not exist")
        vol = (r.get("Monthly Search Volume (US)") or "").strip()
        for c in ("Demand", "Difficulty"):
            if c in cols and not (r.get(c) or "").strip():
                rep.warn("strategy.csv", f"no {c} tier for {r.get('Target Keyword')!r}")
        if not vol and "strong" in note.lower():
            rep.warn("strategy.csv", f"note calls {r.get('Target Keyword')!r} strong with no volume")
    blog = os.path.join(root, "blog.csv")
    if os.path.exists(blog):
        for r in csv.DictReader(open(blog, encoding="utf-8")):
            if r.get("URL"):
                urls.add(r["URL"].rstrip("/"))
                if (r.get("Month") or "").strip().lower().startswith("month 1"):
                    planned.add(r["URL"].rstrip("/"))
            plan = (r.get("Page Plan") or "").strip()
            if plan and not os.path.exists(os.path.join(root, plan)):
                rep.err("blog.csv", f"Page Plan {plan} does not exist")
    crawl = os.path.join(root, "research", "crawl.csv")
    if os.path.exists(crawl):
        for r in csv.DictReader(open(crawl, encoding="utf-8")):
            urls.add((r.get("url") or "").rstrip("/"))
            urls.add((r.get("final_url") or "").rstrip("/"))
    live = {(r.get("url") or "").rstrip("/") for r in csv.DictReader(open(crawl, encoding="utf-8"))} if os.path.exists(crawl) else set()
    return urls, planned - live


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--online", action="store_true", help="check links missing from the page map by loading them")
    a = ap.parse_args()
    rep = Report()
    urls, planned = lint_strategy(a.root, rep)
    pdir = os.path.join(a.root, "plans")
    plans = sorted(os.path.join(pdir, f) for f in os.listdir(pdir) if f.endswith(".md")) if os.path.isdir(pdir) else []
    if not plans:
        rep.warn(a.root, "no plans/*.md yet")
    for p in plans:
        lint_plan(p, rep, urls, frozenset(planned), a.online)
    errs = [i for i in rep.items if i[0] == "ERROR"]
    warns = [i for i in rep.items if i[0] == "warn"]
    for lvl, where, msg in rep.items:
        print(f"{lvl:5} {where}: {msg}")
    print(f"\n{len(plans)} plans checked: {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs or (a.strict and warns) else 0)


if __name__ == "__main__":
    main()
