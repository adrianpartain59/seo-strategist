---
name: seo-strategist
argument-hint: "[website URL] [optional: Search Console export, keyword CSV, competitors]"
description: Use when someone wants to improve a website's SEO or get cited by AI answers (ChatGPT, Perplexity, Gemini, AI Overviews) — keyword research, an SEO strategy or keyword plan, "which pages should we build", landing page or feature page plans, on-page optimization of existing pages, meta titles and descriptions, comparison or "X vs Y" pages, calculator or free-tool pages, a blog topic cluster, content briefs, or a full agency-style SEO audit and roadmap for an app, SaaS, DTC or service website — even if they never say "SEO strategy" or "skill".
---

# SEO Strategist

Runs the full service of a product-led SEO + AI-answer (GEO) agency for one
website: research the site, its competitors and its keywords; deliver a
**strategy sheet** (one keyword → one page → one page type, for existing pages
to update and new pages to build, plus a first blog cluster); then deliver a
**page plan** for every row: ready-to-paste copy, section by section, that a
developer or an AI can apply to the page. Finish with a local review site the
user opens in their browser.

`<SKILL_DIR>` below is the directory containing this file. Scripts are run
through their interpreter (`python3 <SKILL_DIR>/scripts/x.py`); they use the
standard library only.

## Output

Everything goes in `seo-plan/<domain>/` under the current directory:

| File | What it is |
|---|---|
| `intake.md` | Fact sheet, proof bank, rules, competitors, page map (phase 1) |
| `research/` | Crawl, keyword pulls, SERP notes, metric sources (phase 2) |
| `strategy.csv` | The landing-page strategy sheet (phase 3) |
| `blog.csv` | Blog Month 1 cluster + Month 2 plan (phase 3) |
| `redirects.csv` | One-hop 301s that remove duplicate pages (phase 3) |
| `summary.md` | Counts, what was left out and why, open questions, metric sources, rollout order (phase 3) |
| `meta-fixes.md` | Title/description fixes for pages outside the sheet (phase 3) |
| `plans/<slug>.md` | One page plan per strategy row (phase 4) |
| `index.html`, `plans/*.html` | The review site (phase 6) |

The sheet is deliberately lean: no approval checkboxes or reviewer-notes
columns, because the user reviews with you in chat. Its job is a general
breakdown plus a link to every page plan and every live page, so the user can
review everything outside the chat.

## The phases

Work the phases in order. Each phase has a reference file: read it when you
reach that phase, not before.

1. **Intake** → `references/intake.md`. Build the fact sheet from the site,
   the app-store listing and the repo if there is one. Ask the user only for
   what you cannot find: no-go topics, the ranked feature list, competitors,
   pricing/trial wording, a Search Console export. **Collect the no-go rules
   before research**, so no off-limits page is ever proposed.
2. **Research** → `references/research.md`. Crawl the site
   (`scripts/crawl_site.py`), read Search Console, map competitor pages, expand
   keywords (`scripts/suggest.py`), get volume/difficulty from the best source
   available, review the live results for every candidate, classify intent,
   cluster.
3. **Strategy sheet** → `references/strategy.md`. Pick keywords on the barbell,
   assign page types and statuses, resolve every overlap (301, merge, or
   re-angle), write the "why" note per row, plan the blog cluster, list meta
   fixes. Then **stop and review with the user**: show the counts and the rows,
   ask what to cut or change, apply it, and only then write plans. If the user
   said up front to run straight through, skip the stop.
4. **Page plans** → `references/page-plans.md` (shared format and copy rules)
   plus the template for the row's page type in `references/templates/`.
   One plan per row. For more than ~6 rows, fan out to subagents in batches
   by page type, giving each the intake, the full page map and the template.
   Topics that touch health, money, legal rights or safety also follow
   `references/regulated-topics.md` (full or light level, decided in intake).
5. **Check** → run `python3 <SKILL_DIR>/scripts/lint_plans.py seo-plan/<domain> --online`
   and fix every error. Then do the cluster pass in `references/page-plans.md`
   (siblings differ, hubs link to every spoke, no link to a page that won't
   exist). Lint passing is required, not sufficient: read two plans end to end
   as the reader would.
6. **Deliver** → `python3 <SKILL_DIR>/scripts/build_report.py seo-plan/<domain>`
   builds `index.html`. Serve it (`python3 -m http.server 8765 --directory
   seo-plan/<domain>` in the background) and give the user
   `http://localhost:8765/`. Close with the rollout order from
   `references/rollout.md`.

## Rules that hold in every phase

- **One primary keyword per URL.** Close variants live in the same page's
  title, H1 and copy. Two keywords whose top-10 results share 3+ URLs are one
  page.
- **Every number has a source.** Metrics carry their tool and date (or
  `est.` when estimated); page copy carries its primary source and revision
  date. Never invent a volume, a rating, a review or a statistic. Product
  claims come only from the intake fact sheet and proof bank.
- **Never change an existing slug, and never delete or redirect a URL with
  Search Console impressions** unless another page already serves its intent.
- **The client's rules beat SEO upside.** Apply them before proposing, not
  after. Note what you left out and why in the strategy summary.
- **Honesty is the angle on commercial pages.** "Best X" pages are buyer's
  guides that disclose who wrote them; "free X" pages say what is free and what
  is paid in the hero; competitors are named factually, dated, without
  criticism or prices.
- **Never scrape Google result pages or solve CAPTCHAs.** Use the sources in
  `references/research.md`; when a number needs a tool behind a login, ask the
  user to paste it.

## Common mistakes

| Mistake | Instead |
|---|---|
| Proposing pages from keyword volume alone | Barbell: mostly low-difficulty pages with purchase or feature intent, a few high-volume pillars, free tools in the middle |
| A new page that competes with an existing one | Re-angle (each page owns one noun), merge, or put the variant on the existing page |
| Rewriting a whole existing page | Diff only: change head tags that break the rules, add 3–5 missing sections, merge into existing ones |
| Generic copy ("seamless", "powerful", "#1") | Product facts from the fact sheet, two-sentence bullets, brand as the subject |
| Keyword stuffed into every H2 | Keyword in title, H1, meta, one or two FAQ questions; H2s carry sub-intents |
| FAQ written from imagination | Questions mined from autocomplete, People Also Ask-style results and forums; answers open with Yes/No or the fact |
| Replacing richer live schema | Merge with what is live (BreadcrumbList, MobileApplication, Organization) |
| Writing plans before the user has seen the strategy | Phase 3 review first |
