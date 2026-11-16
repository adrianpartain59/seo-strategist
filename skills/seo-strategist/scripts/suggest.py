#!/usr/bin/env python3
"""Expand seed keywords with free autocomplete sources (no API key).

Usage:
  python3 suggest.py "seed one" "seed two" [--modifiers] [--questions] [--hl en --gl us] --out suggest.csv

Sources: Google (client=chrome, with relevance), Bing, DuckDuckGo. --modifiers adds a-z
after each seed; --questions adds question and intent prefixes. Output columns:
keyword, sources (how many engines returned it), seeds (how many seed queries
produced it), google_relevance (max), first_seen_for. More sources and seeds = a broader
signal of real demand. These are NOT search volumes.
"""
import argparse, csv, json, string, sys, time, urllib.parse, urllib.request
from collections import defaultdict

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) seo-strategist"
QUESTION_PREFIXES = ["how to", "what is", "why does", "can you", "is", "best", "free", "vs", "for", "without", "app"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read().decode("utf-8", "replace")


def google(q, hl, gl):
    u = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(
        {"client": "chrome", "hl": hl, "gl": gl, "q": q})
    d = json.loads(get(u))
    sugg = d[1]
    rel = (d[4].get("google:suggestrelevance") if len(d) > 4 and isinstance(d[4], dict) else None) or [0] * len(sugg)
    return list(zip(sugg, rel))


def bing(q, hl, gl):
    u = "https://api.bing.com/qsonhs.aspx?" + urllib.parse.urlencode({"type": "cb", "q": q, "mkt": f"{hl}-{gl.upper()}"})
    d = json.loads(get(u))
    out = []
    for res in d.get("AS", {}).get("Results", []) or []:
        for s in res.get("Suggests", []) or []:
            out.append((s.get("Txt", ""), 0))
    return out


def ddg(q, hl, gl):
    u = "https://duckduckgo.com/ac/?" + urllib.parse.urlencode({"q": q, "type": "list"})
    d = json.loads(get(u))
    return [(s, 0) for s in (d[1] if isinstance(d, list) and len(d) > 1 else [])]


ENGINES = {"google": google, "bing": bing, "ddg": ddg}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seeds", nargs="+")
    ap.add_argument("--modifiers", action="store_true", help="append a-z to each seed")
    ap.add_argument("--questions", action="store_true", help="prefix question/intent words")
    ap.add_argument("--hl", default="en")
    ap.add_argument("--gl", default="us")
    ap.add_argument("--engines", default="google,bing,ddg")
    ap.add_argument("--sleep", type=float, default=0.15)
    ap.add_argument("--out", default="suggest.csv")
    a = ap.parse_args()

    queries = []
    for s in a.seeds:
        queries.append(s)
        if a.modifiers:
            queries += [f"{s} {c}" for c in string.ascii_lowercase]
        if a.questions:
            queries += [f"{p} {s}" for p in QUESTION_PREFIXES]

    sources, seeds, rel, first = defaultdict(set), defaultdict(set), defaultdict(int), {}
    failures = defaultdict(int)
    for q in queries:
        for name in a.engines.split(","):
            try:
                for kw, r in ENGINES[name](q, a.hl, a.gl):
                    kw = " ".join(kw.lower().split())
                    if not kw:
                        continue
                    sources[kw].add(name)
                    seeds[kw].add(q)
                    rel[kw] = max(rel[kw], int(r or 0))
                    first.setdefault(kw, q)
            except Exception:
                failures[name] += 1
            time.sleep(a.sleep)

    rows = sorted(sources, key=lambda k: (-len(sources[k]), -len(seeds[k]), -rel[k], k))
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["keyword", "sources", "seeds", "google_relevance", "engines", "first_seen_for"])
        for k in rows:
            w.writerow([k, len(sources[k]), len(seeds[k]), rel[k], "|".join(sorted(sources[k])), first[k]])
    print(f"{len(rows)} unique suggestions from {len(queries)} queries -> {a.out}")
    if failures:
        print("Failed calls per engine:", dict(failures), file=sys.stderr)
    for k in rows[:25]:
        print(f"  {len(sources[k])} src  {len(seeds[k]):>2} seeds  {k}")


if __name__ == "__main__":
    main()
