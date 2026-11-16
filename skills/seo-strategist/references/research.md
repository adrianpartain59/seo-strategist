# Phase 2: Research

Output goes in `seo-plan/<domain>/research/`. Every metric you record carries
its source; this is what makes the strategy sheet trustworthy.

## 1. Crawl the site

```bash
python3 <SKILL_DIR>/scripts/crawl_site.py https://example.com --out seo-plan/example.com/research/crawl.csv
```

It reads the sitemap (falls back to links on the homepage), fetches every URL
and records status, final URL, title, meta description, H1, canonical, H2
count, word count, and flags. Read its summary for:
- **Shared or missing meta**: many URLs with the homepage's title or
  description (single-page-app fallback). These become `meta-fixes.md` rows.
- **Soft 404s**: the script requests a random path; a 200 with the homepage's
  title means unknown URLs don't 404. Note it; planned pages "work" before they
  exist and links to them look live.
- **Redirect chains**, duplicate titles, duplicate H1s, very thin pages.
- **Near-duplicate intents**: two URLs whose titles target the same thing
  (two calculators for one query, a feature page and an older page on the same
  feature).

Fill the page map in `intake.md`: every URL, its type, its one-sentence job.

## 2. Search Console (if the user gave an export)

- **Pages**, 12 months: impressions and clicks per URL → the strategy sheet's
  "Your Google views / clicks" columns. Any URL with impressions is protected:
  keep its slug, tune it.
- **Queries**: queries at average position 8–30 with impressions are
  striking-distance targets for the page that already ranks. Queries where two
  URLs both get impressions point to cannibalization.
- Branded vs non-branded: a very high CTR (20%+) on the homepage means brand
  traffic; non-branded growth is the goal.

No export: write "no Search Console data" in the sheet's summary and leave the
columns blank. Don't guess.

## 3. Competitor gap

For each competitor domain: fetch its sitemap or nav and bucket every URL into
the page types in `strategy.md` (feature, entity/use-case, calculator,
comparison, alternative, guide, blog). Note:
- Page types they have that the client lacks → candidates.
- Features only the client has → each gets its own feature page (an AI answer
  can only tie the feature to the brand if a page states it).
- Comparison and alternative pages that name the client.

## 4. Keyword discovery

Build the **entity list** first: product category terms, features (in the
words users use), integrations/platforms, brands or models the product works
with, audiences and life stages, problems it solves, competitor names. Then
expand each seed:

```bash
python3 <SKILL_DIR>/scripts/suggest.py "time blocking app" "daily planner app" --modifiers --out seo-plan/example.com/research/suggest.csv
```

It queries Google, Bing and DuckDuckGo autocomplete (no key needed), with
optional alphabet and question modifiers, and records how many sources and
seeds produced each suggestion (a rough demand signal). Add:
- **Templates × entities** for programmatic families: `<brand> app`,
  `<entity> tracker`, `<A> vs <B>`, `switching from <A> to <B>`,
  `<competitor> alternative`, `<thing> calculator`, `<thing> template`,
  `best <category> app`, `free <category> app`, `<category> for <audience>`.
- **Brand + modifier**: run `suggest.py "<brand>" "<brand> app" --modifiers`.
  Every modifier people attach to the brand (pricing, free vs pro, for
  windows/android/mac, alternatives, vs <competitor>, student discount, review)
  that a third-party site answers today is a page the client should own: a
  pricing page, platform pages, vs pages, an alternatives page. WebSearch each
  to see who answers it now and whether they get the facts wrong.
- **Questions people ask AI assistants**: "what app helps me …", "is there an
  app that …". These are kept even at zero measured volume (see strategy.md).
- Use WebSearch for "<seed>" and "<seed> reddit" to see the questions and the
  words real users use.

## 5. Volume, difficulty, CPC

Use the best source available, and record which one in `research/metrics.csv`
(`keyword, volume_us, kd, cpc, global_volume, source, date`):

| Tier | Source | How |
|---|---|---|
| Best | User's Ahrefs (or Semrush) export | Ask the user to export Keywords Explorer for your list. Ahrefs columns match the sheet: Volume, KD, CPC, Global volume |
| Good | DataForSEO (if `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` are set) | `python3 <SKILL_DIR>/scripts/dataforseo.py keywords.txt --out research/metrics.csv` (volume, CPC, difficulty, about $1–2 per study) |
| OK | Free manual tools the user runs | Ahrefs free Keyword Generator / KD checker, Google Keyword Planner ranges. Ask the user to paste the numbers |
| Fallback | Estimate | Leave volume, KD and CPC blank and set `source=est.`. Fill the sheet's Demand tier from autocomplete breadth (sources × seeds in suggest.csv, plus whether the term shows up for many seeds) and the Difficulty tier from the results-page read below. Say in the sheet summary that the tiers are estimates and which numbers a keyword tool would firm up |

Notes that keep numbers honest:
- Blank volume = not in the tool's database (new or tiny); 0 = measured 0–10.
- New products and new categories are undercounted: label their volumes
  "a floor".
- **Traffic value = volume × CPC.** It is the monthly ad cost of that traffic if
  you won every click: a ceiling, not a forecast.

## 6. Read the results page for every candidate

For each candidate keyword, WebSearch it (and WebFetch the top 3–5 results when
the outline matters). Record in `research/serp.md`:
- **Dominant result type**: tools, listicles, app-store listings, brand pages,
  long guides, forums. The page type you build must match it.
- **Who ranks**: big authority domains vs small sites, forums, Reddit. This is
  your difficulty check when no KD is available. WebSearch returns a
  summarized, partly unranked set, so treat counts as approximate and weight
  who holds the first three results most:
  ≥3 forum/small-site results in the top 10 ≈ easy (KD < 15);
  ≥7 major authority domains ≈ hard (KD > 40).
- **Facets every result covers** (these become sections) and **what they do
  that you won't** (claims you can't source, advice the rules forbid). The honest
  gap is often the angle.
- **Questions** shown on the page and in related searches → FAQ material.

## 7. Domain strength

Get the client's and competitors' authority from the best available source:
the user's Ahrefs Domain Rating (Ahrefs Webmaster Tools is free for verified
sites), Moz DA, or Open PageRank (free key). If none: judge from what they rank
for today (Search Console) and say so.

## 8. Intent and clustering

- Classify each keyword: informational, commercial investigation, transactional,
  navigational. Confirm with the results page, not with modifiers alone.
- Cluster keywords whose top 10 share 3+ URLs into one page. The cluster's
  primary keyword is the variant people type most (by volume, else autocomplete
  breadth); the rest are variants for that page's title/H1/copy.
- Assign each cluster to an existing URL if one already serves it (and has
  impressions); otherwise propose a new slug.

## Exit check

`research/` has crawl.csv, suggest.csv (or equivalent), metrics.csv with a
`source` on every row, and serp.md with a result-type and difficulty read for
every candidate that will reach the sheet.
