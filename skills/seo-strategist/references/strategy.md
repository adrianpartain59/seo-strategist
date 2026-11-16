# Phase 3: The strategy sheet

Deliverables: `strategy.csv`, `blog.csv`, `redirects.csv`, `meta-fixes.md`,
and `summary.md` (the review-stop content below, plus the rollout order from
`rollout.md`), which you show the user before any page plan is written. The
review site renders `summary.md` at the top of its index.

## strategy.csv columns (in this order)

| Column | Holds |
|---|---|
| Target Keyword | One primary keyword, Title Case, spelled as people search it |
| Page Type | One of the types below |
| Plan Type | `Landing` (walks the visitor to the CTA) or `Informational` (sourced guide copy) |
| Status | `Existing page (update)` or `New page` |
| URL | Full absolute URL. Existing pages keep their live slug |
| Why This Page | The note (see "Writing the note") |
| Demand | `High` / `Medium` / `Low`. Always filled. From volume when you have it (≥1,000 High, 100–999 Medium, <100 Low); otherwise from autocomplete breadth and the results page, with `est.` in Metric Source |
| Difficulty | `Easy` / `Medium` / `Hard`. Always filled. From KD when you have it (≤15 Easy, 16–35 Medium, >35 Hard); otherwise from the results-page read in `research/serp.md` |
| Monthly Search Volume (US) | From `research/metrics.csv`; blank if unknown (use the market's country if not US, and rename the column) |
| KD | Keyword difficulty 0–100, blank if unknown |
| CPC | USD |
| Traffic Value | Volume × CPC: the computed number, or a spreadsheet formula that references the Volume and CPC cells of the same row. Monthly ad cost of the traffic: a ceiling |
| Global Volume | |
| Your Google Views (12 mo) | Search Console impressions for this URL; 0 for new pages; blank if no export |
| Your Clicks (12 mo) | Search Console clicks |
| Metric Source | e.g. `Ahrefs US, Nov 2026` / `DataForSEO, 2026-11-16` / `est.` |
| Page Plan | Relative link `plans/<slug>.md`, filled in phase 4 |

No approval or reviewer-notes columns: the user reviews in chat.

## Page types

| Page Type | Plan Type | Template | What it targets |
|---|---|---|---|
| Homepage | Landing | existing-page (or landing-page if rebuilt) | The head category term, "<category> app/software/tool" |
| Core product page | Landing | landing-page | Commercial modifiers: "best <category> app", "free <category> app", "<category> app for <platform>", and brand + modifier searches others answer today ("<brand> pricing", "<brand> for windows") |
| Feature page | Landing | landing-page | One per product feature, in the client's feature ranking, plus every feature competitors lack |
| Entity page | Landing | landing-page | The product for a specific brand, model, integration, platform or use case ("<brand> app", "<integration> planner", "<entity> tracker") |
| Free tool | Landing | free-tool | "<thing> calculator / chart / converter / generator / maker / template / checker / timer": a free interactive tool with transparent logic |
| Comparison page | Informational | comparison | "A vs B", "switching from A to B", "<competitor> alternative" |
| Pillar guide | Informational | pillar-guide | High-volume informational head terms in the product's world ("<entity> side effects", "how <thing> works") |
| Audience page | Landing | landing-page | Commercial "<category> app for <audience>" searches ("ADHD planner app", "CRM for realtors"): a landing page for that audience, product from section 2 |
| Audience guide | Informational | audience-guide | Informational "<topic> and <audience / life stage / condition>" questions ("time blocking with ADHD", "period tracking in perimenopause"), often asked of AI assistants |
| List guide | Informational | list-guide | Checklists, templates, shopping or packing lists, printable linkable assets |

Every existing page uses the existing-page template regardless of type.

## Choosing keywords: the barbell

1. **Low-difficulty pages with purchase or feature intent (most rows).** App,
   feature, entity and core-product terms, KD ≤ ~20, even at 0–200 searches.
   Kept for conversion intent, for a unique feature, or because people ask AI
   assistants that question. A zero/blank-volume row needs one of those reasons
   written in its note.
2. **A handful of high-volume pillars.** Guides and comparisons on the biggest
   informational terms in the category, KD up to ~60. Their difficulty is above
   what the domain wins today; the note says they grow with backlinks.
3. **Free tools in the middle.** Calculators and other free tools on generic terms with real volume
   and very low KD that the audience needs.

Without tool numbers, apply the same barbell to the tiers: most rows
`Easy` with purchase or feature intent at any demand; a few `Hard` pillars
with `High` demand; free tools at `Medium`/`High` demand and `Easy`.

Difficulty vs authority, when you have both numbers: new pages at
KD ≤ max(10, 0.7 × the site's DR); pages that already get impressions up to
DR + 10; the head term goes to the homepage only. When you have only SERP reads,
use the easy/hard read from research.md.

Drop a candidate when: it breaks a client rule; the results page is a format
you won't build (pure video, pure maps, pure shopping); it needs advice or claims
you cannot source; or another row already owns its intent.

## Overlap rules (resolve every one before the sheet ships)

- **The head term belongs to the homepage.** Any other page targeting it is
  301-redirected to `/` (row in `redirects.csv`), and every older redirect that
  pointed at that page is re-pointed straight to the final target: no chains.
- **Two tools or pages for one query**: keep the stronger URL (impressions,
  links), 301 the other to it.
- **Overlapping features**: split by intent, not by merging. Each page owns one
  noun (e.g. reminders vs history vs site rotation), states it in its note, and
  cross-links the siblings.
- **A variant of an existing page's keyword**: put the variant in that page's
  title/H1/copy; never a second page.
- **An existing article on the topic**: expand it (Month 2 refresh) instead of
  writing a near-duplicate.
- **Brand vs generic families**: brand name + the modifier people type for that
  brand ("<Brand> App", "<Brand> Half Life Chart"); the generic/ingredient name
  gets the hub ("<Generic> Tracker"). A brand page exists only when the brand
  has at least one fact of its own.

Leave pages with no keyword job alone. Don't add rows for legal or utility
pages; fix their meta in `meta-fixes.md`.

## Slugs

Lowercase, hyphenated, at the root (`/time-blocking-app`, not
`/features/time-blocking-app`), usually the keyword verbatim; "app" can be
dropped when the slug reads better. Never change a live slug. Blog posts go under the
site's existing blog or resources path (`/blog/<slug>` if there is none; say
so in summary.md if the blog has to be set up first).

## Writing the note (Why This Page)

15–40 words, plain English, second person, no SEO jargon ("compete", not
"cannibalize"; "showed up on Google", not "impressions"). Shape:
1. Existing pages open with a verdict: `Keep.` / `Keep and tune for "<variant>".`
   / `Keep and refresh.`
2. One fact about how people search ("People search 'habit tracker app' more
   than 'habit app'…"), a feature-rank tie ("Streaks are your #1 feature…"), or the AI angle ("People ask AI tools which app…").
3. What the page will do, and where it links.
4. Optional: `Question for you: …` for anything only the client can answer.

The note's claims must match the numbers beside it. Never call a row "strong"
when its volume is blank.

## Row order

By site architecture and funnel, not by volume: Homepage → Core product →
Feature pages (in the client's ranking) → Entity pages → Audience pages → Free
tools (existing first) → Comparison pages → Pillar guides → Audience guides → List guides.

## blog.csv

Columns: `Target Keyword, Month, Why This Post, Demand, Difficulty, Monthly
Search Volume (US), KD, CPC, Traffic Value, Global Volume, Links To, URL,
Page Plan`. Traffic Value is volume × CPC here too. Blog posts use Plan Type
`Blog` in their page plans.

- **Month 1 = one tight cluster of ~10 posts**: long-tail questions under one
  pillar, the lowest-difficulty pocket with real volume (median KD ≤ 10, or
  mostly `Easy` tiers),
  phrased the way people search (brand names over generic names when people
  search the brand). Each post links up to its pillar and across to one money
  page (named in Links To).
- **Month 2 = refresh + new**: rewrite existing informational and comparison
  pages to the current standard (short answer at the top, FAQ, cited sources,
  comparison table where it fits), plus ~10 new posts from the next cluster.
- Rule of thumb for where a keyword goes: head term or tool → root landing page;
  long-tail question → blog post.

## redirects.csv

`From, To, Type, Why`. One hop each.

## meta-fixes.md

For every live page outside the sheet whose title or description is missing,
duplicated (often the homepage's, inherited by every route) or over length:
current values once at the top, then per URL a suggested title and
description following the meta rules in `page-plans.md` (legal/utility pages:
`<Page Name> | <Brand>`). Mark fixes that depend on something not built yet
("apply when the blog exists").

## Technical fixes

List in `summary.md` the site problems the crawl and research found that are
not page copy: dead store or app links, duplicate hosts (www and apex both
serving 200), FAQ or body text that only exists in JavaScript, images without
alt text, schema that disagrees with the page, broken H1s, third-party sites
stating wrong facts about the product (an outreach list). These are often the
fastest wins.

## The review stop

Before phase 4, show the user:
- Counts: rows by status and page type, blog posts, redirects, meta fixes.
- What you left out and why (rules, formats you won't build, duplicates).
- Any "Question for you" items.
- Where the numbers came from and how confident they are.

Ask what to cut or change. Delete rejected rows (don't strike them), apply the
answers to the notes **and** carry them into the plans.
