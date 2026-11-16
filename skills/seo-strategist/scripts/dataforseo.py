#!/usr/bin/env python3
"""Optional: volume, CPC and keyword difficulty from DataForSEO (paid, ~$1-2 per study).

Needs DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD in the environment.

Usage:
  python3 dataforseo.py keywords.txt --out metrics.csv [--location 2840 --language en]

keywords.txt: one keyword per line (max 1,000). Location 2840 = United States.
Writes keyword, volume_us, kd, cpc, competition, source, date. Prints the cost reported by
the API. Never run it without the user's go-ahead: it spends their credits.
"""
import argparse, base64, csv, datetime, json, os, sys, urllib.request

API = "https://api.dataforseo.com/v3"


def post(path, payload, auth):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode(), method="POST",
                                 headers={"Authorization": "Basic " + auth, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords")
    ap.add_argument("--out", default="metrics.csv")
    ap.add_argument("--location", type=int, default=2840)
    ap.add_argument("--language", default="en")
    a = ap.parse_args()
    login, pw = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    if not (login and pw):
        sys.exit("Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD (https://app.dataforseo.com/api-access).")
    auth = base64.b64encode(f"{login}:{pw}".encode()).decode()
    kws = [l.strip() for l in open(a.keywords) if l.strip()][:1000]

    vol = post("/keywords_data/google_ads/search_volume/live",
               [{"keywords": kws, "location_code": a.location, "language_code": a.language}], auth)
    kd = post("/dataforseo_labs/google/bulk_keyword_difficulty/live",
              [{"keywords": kws, "location_code": a.location, "language_code": a.language}], auth)
    cost = (vol.get("cost") or 0) + (kd.get("cost") or 0)

    rows = {}
    for t in vol.get("tasks", []):
        for it in t.get("result") or []:
            rows[it["keyword"].lower()] = {"volume_us": it.get("search_volume"), "cpc": it.get("cpc"),
                                           "competition": it.get("competition")}
    for t in kd.get("tasks", []):
        for res in t.get("result") or []:
            for it in res.get("items") or []:
                rows.setdefault(it["keyword"].lower(), {})["kd"] = it.get("keyword_difficulty")
    today = datetime.date.today().isoformat()
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["keyword", "volume_us", "kd", "cpc", "competition", "global_volume", "source", "date"])
        for k in kws:
            r = rows.get(k.lower(), {})
            w.writerow([k, r.get("volume_us", ""), r.get("kd", ""), r.get("cpc", ""), r.get("competition", ""),
                        "", "DataForSEO", today])
    print(f"{len(kws)} keywords -> {a.out}. API cost: ${cost:.4f}")


if __name__ == "__main__":
    main()
