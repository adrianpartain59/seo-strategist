#!/usr/bin/env python3
"""Crawl a site's sitemap and record the on-page SEO basics for every URL.

Usage:
  python3 crawl_site.py https://example.com --out crawl.csv [--limit 300]

Writes a CSV (url, status, final_url, redirected, title, title_len, meta_description,
meta_len, h1, h1_count, h2_count, canonical, noindex, words, jsonld_types) and prints a
summary of issues: shared/missing titles and descriptions, over-length tags, soft 404s,
redirects, duplicate H1s, thin pages. Standard library only.
"""
import argparse, csv, gzip, io, json, random, re, string, sys, urllib.error, urllib.parse, urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36 seo-strategist"


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            if r.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz"):
                try:
                    data = gzip.decompress(data)
                except OSError:
                    pass
            return r.status, r.geturl(), data.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:  # network errors are data, not crashes
        return 0, url, f"ERROR {e}"


def sitemap_urls(root, limit):
    seen, urls, queue = set(), [], [root.rstrip("/") + "/sitemap.xml"]
    status, _, robots = fetch(root.rstrip("/") + "/robots.txt")
    if status == 200:
        queue = [m.strip() for m in re.findall(r"(?im)^sitemap:\s*(\S+)", robots)] or queue
    while queue and len(urls) < limit * 20:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        status, _, body = fetch(sm)
        if status != 200:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
        if "<sitemapindex" in body:
            queue.extend(locs)
        else:
            urls.extend(locs)
    urls = list(dict.fromkeys(urls))
    # Shallow, marketing-style paths first so a --limit keeps the key pages,
    # not the first N help-center articles.
    deep = ("/help/", "/docs/", "/blog/", "/support/", "/kb/", "/changelog")
    urls.sort(key=lambda u: (any(d in u for d in deep), urllib.parse.urlparse(u).path.count("/")))
    return urls[:limit]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.meta, self.canonical, self.robots = "", "", "", ""
        self.h1, self.h2 = [], 0
        self._in, self._buf, self.text, self.jsonld, self.links = None, [], [], [], []
        self._skip = 0
        self._svg = 0
        self.imgs, self.no_alt = 0, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self._skip += 1
            if tag == "script" and a.get("type") == "application/ld+json":
                self._in, self._buf = "jsonld", []
        if tag == "svg":
            self._svg += 1
        if tag == "title" and not self._svg and not self.title:
            self._in, self._buf = "title", []
        elif tag == "h1":
            self._in, self._buf = "h1", []
        elif tag == "h2":
            self.h2 += 1
        elif tag == "meta":
            n = (a.get("name") or a.get("property") or "").lower()
            if n == "description":
                self.meta = a.get("content", "") or ""
            if n == "robots":
                self.robots = a.get("content", "") or ""
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href", "") or ""
        elif tag == "img":
            self.imgs += 1
            if not (a.get("alt") or "").strip():
                self.no_alt += 1
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "svg":
            self._svg = max(0, self._svg - 1)
        if tag in ("script", "style", "noscript"):
            self._skip = max(0, self._skip - 1)
            if self._in == "jsonld":
                self.jsonld.append("".join(self._buf))
                self._in = None
        if tag == "title" and self._in == "title":
            self.title = " ".join("".join(self._buf).split())
            self._in = None
        elif tag == "h1" and self._in == "h1":
            self.h1.append(" ".join("".join(self._buf).split()))
            self._in = None

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)
        if not self._skip:
            self.text.append(data)


def jsonld_types(blocks):
    types = []
    for b in blocks:
        try:
            d = json.loads(b)
        except Exception:
            types.append("INVALID")
            continue
        stack = [d]
        while stack:
            x = stack.pop()
            if isinstance(x, list):
                stack.extend(x)
            elif isinstance(x, dict):
                t = x.get("@type")
                if t:
                    types.extend(t if isinstance(t, list) else [t])
                stack.extend(v for k, v in x.items() if k == "@graph")
    return "|".join(sorted(set(types)))


def audit(url):
    status, final, body = fetch(url)
    p = PageParser()
    try:
        p.feed(body)
    except Exception:
        pass
    words = len(re.findall(r"[A-Za-z0-9']+", " ".join(p.text)))
    return {
        "url": url, "status": status, "final_url": final,
        "redirected": "yes" if final.rstrip("/") != url.rstrip("/") else "",
        "title": p.title, "title_len": len(p.title),
        "meta_description": p.meta, "meta_len": len(p.meta),
        "h1": " || ".join(p.h1), "h1_count": len(p.h1), "h2_count": p.h2,
        "canonical": p.canonical, "noindex": "yes" if "noindex" in p.robots.lower() else "",
        "words": words, "jsonld_types": jsonld_types(p.jsonld),
        "images": p.imgs, "images_no_alt": p.no_alt,
        "_links": p.links,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--out", default="crawl.csv")
    ap.add_argument("--limit", type=int, default=300)
    args = ap.parse_args()
    root = args.site if args.site.startswith("http") else "https://" + args.site
    root = root.rstrip("/")

    urls = sitemap_urls(root, args.limit)
    home = audit(root + "/")
    if not urls:
        host = urllib.parse.urlparse(root).netloc
        found = [urllib.parse.urljoin(root + "/", h).split("#")[0] for h in home["_links"]]
        urls = [root + "/"] + sorted({u for u in found if urllib.parse.urlparse(u).netloc == host})
        print(f"No sitemap found; using {len(urls)} links from the homepage.")
    with ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(audit, urls))

    junk = "".join(random.choice(string.ascii_lowercase) for _ in range(12))
    soft = audit(f"{root}/{junk}-not-a-page")

    fields = [k for k in rows[0].keys() if not k.startswith("_")] if rows else []
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    ok = [r for r in rows if r["status"] == 200]
    print(f"Crawled {len(rows)} URLs ({len(ok)} returned 200). CSV: {args.out}")
    if soft["status"] == 200:
        same = soft["title"] == home["title"]
        print(f"SOFT 404: an unknown URL returns 200{' with the homepage title' if same else ''}. "
              "Unknown and planned URLs look live; pages without their own meta inherit the homepage's.")
    for field, label in (("title", "title"), ("meta_description", "meta description"), ("h1", "H1")):
        groups = defaultdict(list)
        for r in ok:
            groups[r[field]].append(r["url"])
        for val, us in groups.items():
            if len(us) > 1:
                shown = ", ".join(us[:6]) + (" …" if len(us) > 6 else "")
                print(f"SHARED {label} on {len(us)} URLs: {val[:70]!r} -> {shown}")
    for r in ok:
        issues = []
        if not r["title"]:
            issues.append("no title")
        elif r["title_len"] > 60:
            issues.append(f"title {r['title_len']} chars")
        if not r["meta_description"]:
            issues.append("no meta description")
        elif r["meta_len"] > 160:
            issues.append(f"meta {r['meta_len']} chars")
        if r["h1_count"] != 1:
            issues.append(f"{r['h1_count']} H1s")
        if r["words"] < 250:
            issues.append(f"thin ({r['words']} words)")
        if r["noindex"]:
            issues.append("noindex")
        if r["images_no_alt"]:
            issues.append(f"{r['images_no_alt']}/{r['images']} images without alt text")
        if issues:
            print(f"  {r['url']}: {', '.join(issues)}")
    for r in rows:
        if r["redirected"]:
            print(f"REDIRECT {r['url']} -> {r['final_url']} (sitemap lists a redirecting URL)")
        elif r["status"] != 200:
            print(f"STATUS {r['status']} {r['url']}")


if __name__ == "__main__":
    main()
