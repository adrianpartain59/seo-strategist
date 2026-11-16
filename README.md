# SEO Strategist

An SEO and AI-answer (GEO) agency, packaged as a Claude Code skill.

Point it at a website. It researches the site, its competitors and its
keywords, then delivers what a product-led SEO agency delivers:

1. **A strategy sheet**: one keyword per page, for the existing pages to
   update and the new pages to build, each with the search numbers, the page
   type and a plain-English reason. Plus a first blog cluster, the redirects
   that remove duplicate pages, and title and description fixes for every page
   that needs them.
2. **A page plan for every page**: section by section, the headings, the
   ready-to-paste copy, the buttons, what each section must show and how to lay
   it out, the FAQ and the structured data. Hand a plan to a developer, or paste
   it into your AI coding tool with the current page and ask it to apply every
   change while keeping your design.
3. **A review site** on localhost: the whole plan as a sortable table with a
   link to every page plan and every live page, a Google-snippet preview for
   each title and description, and a copy button on every section.

Every page is written to rank on Google and to be quoted by AI answers
(ChatGPT, Perplexity, Gemini, Google AI Overviews): a short answer near the top,
one claim per sentence, sourced and dated facts, honest comparisons, and a FAQ
written the way people ask.

## Install

```bash
claude plugin marketplace add adrianpartain59/seo-strategist
claude plugin install seo-strategist@seo-strategist
```

Or copy `skills/seo-strategist/` into `~/.claude/skills/`.

## Use

In Claude Code, in any folder (your site's repo is best):

> Improve the SEO for https://example.com

or `/seo-strategist https://example.com`. It asks once for what it cannot
find on its own (topics you never want published, your feature ranking,
competitors, pricing wording, a Search Console export), shows you the strategy
before writing any page plan, then writes the plans and gives you a
`http://localhost:8765/` link to review them.

Output lands in `seo-plan/<domain>/`:

```
intake.md        facts the copy may use (features, proof, pricing, rules)
research/        crawl, keyword pulls, results-page notes, metric sources
strategy.csv     the landing-page plan (opens in Sheets or Excel)
blog.csv         Month 1 cluster and Month 2 refreshes
redirects.csv    one-hop 301s
meta-fixes.md    titles and descriptions for pages outside the plan
summary.md       counts, what was left out and why, rollout order
plans/*.md       one page plan per page
index.html       the review site
```

## Data sources

It works with no paid tools: it crawls your site, expands keywords through
Google, Bing and DuckDuckGo autocomplete, and reads the live results for every
keyword. It gets sharper with:

- a **Google Search Console** export (protects pages that already rank, finds
  queries on page 2),
- an **Ahrefs or Semrush** keyword export (exact volume and difficulty),
- **DataForSEO** credentials in `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD`
  (about $1–2 per full study).

Every number in the sheet says where it came from; estimates are labelled.

## Scripts

Standard-library Python, no installs:

| Script | Does |
|---|---|
| `crawl_site.py` | Sitemap crawl: titles, descriptions, H1s, schema, shared meta, soft 404s, thin pages |
| `suggest.py` | Autocomplete keyword expansion across three engines |
| `dataforseo.py` | Optional volume, CPC and difficulty |
| `lint_plans.py` | Checks every plan against the format and copy rules |
| `build_report.py` | Builds the review site |

## License

MIT
