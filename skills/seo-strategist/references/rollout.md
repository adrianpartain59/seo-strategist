# Phase 6: Deliver and roll out

## Build the review site

```bash
python3 <SKILL_DIR>/scripts/build_report.py seo-plan/<domain>
python3 -m http.server 8765 --directory seo-plan/<domain>   # run in the background
```

`index.html` has the breakdown (counts, what was left out, metric sources),
the strategy table with a link to each page plan and each live/target page,
the blog plan, redirects and meta fixes. Each plan renders as its own page with
copy buttons. Give the user `http://localhost:8765/`. If the port is taken, use
another and say which.

## Rollout order to recommend

1. **Redirects and meta fixes** (minutes, no copy work). Collapse chains.
2. **Existing pages**, highest Search Console impressions first. They already
   rank; tuning them moves fastest.
3. **New landing pages** in the sheet's order, so hub pages land before spokes
   and every "(planned)" link target exists before the page linking to it.
4. **Calculators and pillar guides.**
5. **Blog Month 1**, a steady cadence (2–3 posts a week), each linking to its
   pillar and money page.
6. **Backlinks only after the on-page work is live.** Pillars with KD above the
   site's authority need them; plan outreach to the guides and free tools
   (they are the linkable assets).

## How to apply a plan

"Open a page plan and hand it to your developer, or paste it into your AI
coding tool together with the current page, and ask it to apply every change
while keeping the design. Review, then publish. One page at a time works
best." If the AI is you, in the site's repo: apply one plan, show the diff,
check the page renders, then move to the next.

## Build checklist (every page)

- Title, meta description and H1 exactly as the plan says; one H1.
- Every `(planned)` link left out until its target is live; every other link
  returns 200.
- JSON-LD validates (Rich Results Test) and matches the visible FAQ and rating.
- Images have descriptive alt text; the page is in the sitemap; canonical
  points to itself; the old URL redirects in one hop if the slug changed.
- Mobile layout checked; the CTA works on iPhone and Android.

## Measuring

- Search Console: impressions and clicks per URL (the sheet's baseline
  columns), non-branded queries, the Generative AI / AI Overviews report.
- Bing Webmaster Tools AI Performance (Copilot citations).
- Ask ChatGPT, Perplexity and Gemini the questions the pages target ("best
  <category> app for <audience>") and note whether the site is cited, before
  and after.
- Re-check after 4–8 weeks; pages that gained impressions but not clicks need
  title/meta work; pillars stuck past page 2 need links.
