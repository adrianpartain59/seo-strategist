# Phase 4: Page plans (shared format and copy rules)

A page plan is a build sheet. A developer, or an AI given the plan plus the
current page, applies it without asking questions: every heading, every line of
copy, every button, what each section must show, and how it is laid out. Copy is
final, not a brief.

Read this file, then the template for the row's page type in `templates/`.

## Inputs for every plan

- The strategy row (keyword, type, status, URL, note).
- `intake.md`: fact sheet, proof bank, rules, pricing truth, primary CTA.
- The full page map, so siblings can be linked and handed off.
- For existing pages: the rendered live page (title, meta, H1–H3, card titles,
  FAQ Q&A, JSON-LD). Fetch it; copy "Original Content" verbatim from it.
- `research/serp.md` for this keyword: result type, facets, questions, the gap.
- For guides/comparisons/calculators: the primary sources, with revision dates.

## File format

`plans/<slug>.md`, Markdown with these exact labels. In the plan header,
`Page Type` is `New Page` or `Existing Page` (the row's Status); the strategy's
page type (feature, free tool, comparison…) only decides which template you
follow. `###` lines are H3 copy
headings; everything under "Sub-Headings (H3)…" until "CTA Recommendations:"
is ready-to-use copy.

### New page

~~~markdown
# SEO Plan for: <Brand>

Page Type: New Page
Plan Type: <Landing | Informational | Blog>
Company Type: <Mobile Apps | SaaS | E-commerce | ...>
Page URL: <absolute URL>
Target Keyword: <Keyword>

## Suggested Meta Data
Page Title: <title>
Page Meta Description: <description>

## Page Overview
<2 sentences: the page's one job and the angle it owns; which sibling pages own
the adjacent topics.>

## 1. <H1 text>
Heading Type: h1
Recommended Heading: <H1 text>

Rationale:
<2 sentences: what the searcher wants, then why this section serves it.>

Sub-Headings (H3). Bullets below each subheading are ready-to-use copy (can be implemented as paragraphs, bullets or any other text-style):

### <H3 text>
- <bullet: 2 sentences>
- <bullet: 2 sentences>

CTA Recommendations:
- <one button label>

Key Components to Include:
- <component>
- <component>
- <component>

Design Suggestions:
<Pattern>: <one sentence on arrangement and placement>

## 2. <H2 text>
Heading Type: h2
...

## N. Frequently Asked Questions
...

## Recommended Structured Data
Insert this structured data (JSON-LD) at the end of your <head> tag, or start of your <body> tag.

```json
{ ...FAQPage... }
```
```json
{ ...page-type block... }
```
```json
{ ...Organization... }
```

## Sources
- <Source name>, <publisher>, revised/checked <Month YYYY>: <URL>
~~~

### Existing page

~~~markdown
# SEO Plan for: <Brand>

Page Type: Existing Page
Plan Type: ...
Company Type: ...
Page URL: ...
Target Keyword: ...

## Page Overview
<2 sentences: the page's job after this change and what it hands to siblings.>

## Current Page Optimization Suggestions

Section: title
Original Content:
<live text, verbatim>
Suggested Revision:
<new text>

Section: meta-description
...

## Missing Sections to Add

## New Section: <Heading>
Recommended Heading Type: h2
Suggested Heading Name: <Heading>
Placement: <after which live section>

Why Include:
<2 sentences: "The page <has X> but never <Y>." then the visitor or AI-answer benefit.>

Sub-Headings (H3). Bullets below each subheading are ready-to-use copy (can be implemented as paragraphs, bullets or any other text-style):

### <H3>
- ...

Key Components to Include:
- ...

Design Suggestions:
<Pattern>: <sentence>

## Add to Existing Section: <exact live heading>
The page already has a "<exact live heading>" section. Merge the additions below into it; do not create a duplicate section.
Suggested additions: <what is added>
Recommended Heading Type: h3
...same blocks...

## Recommended Structured Data
...
## Sources
...
~~~

The `Placement:` line and the `## Sources` section are additions to the agency
format: keep them. The linter (`scripts/lint_plans.py`) parses these labels, so
spell them exactly.

## Section and copy rhythm

- **Each H3 = 2 bullets, each bullet = 2 sentences.** Sentence 1 states the fact
  or feature; sentence 2 gives the payoff, the reassurance or the limit.
  ~25 words per bullet, ~12–16 words per sentence, reading grade 6–9.
  Guides may use one 2-sentence bullet per H3.
- Body sections carry 3–4 H3s (up to 5–6 for a "what it records" or criteria
  section). The H1 section carries exactly 1 H3.
- Second person for the reader; the brand is the grammatical subject of many
  product bullets ("<Brand> records each…"), so AI answers tie each fact to
  the brand. Vary openings: no more than three bullets in a row start with the
  brand name. No "we/our" except in an honest
  disclosure line.
- No contractions (outside quoted reviews), no exclamation marks, no em or en
  dashes, no semicolons, no "&" in headings.
- No hype words: journey, unlock, seamless, effortless, revolutionary, empower,
  game-changer, supercharge, best-in-class, guarantee, #1 (unless a cited source
  says it).
- Headings in Title Case, 3–9 words, built from a concrete user moment, number
  or outcome ("Fifty Workouts a Year Blur Together", "From Plate to Log in Three
  Steps"). Takeaway H3s are full claims.
- Name the entity inside the sentence (brand, product, source) instead of a
  pronoun, so any sentence quoted alone still makes sense.
- Every model-derived or computed number is called an **estimate**.
- Every product claim traces to `intake.md`. Every external fact names its
  source and date in the sentence ("The <Source> (revised <Month YYYY>) says…").

## Head tags

These lengths are the single source of truth; templates only add a preferred
pattern. The linter enforces them.

- **Title**: 45–60 characters. Exact keyword first, then `: <concrete angle> |
  <Brand>`. Drop `| <Brand>` on long guide and vs titles rather than cutting the
  angle. "and", not "&". Commercial-modifier keywords may use a question plus an
  answer ("Free X App? <Brand> Is Free to Try").
- **Meta description**: 140–160 characters. Either question-led (commercial
  modifiers), action-led with the keyword in sentence 2, or opening with the
  strongest sourced statistic (guides) or a contrast (comparisons). Close with
  the offer or proof ("Free to try.", "Rated 4.7 stars.").
- **H1**: differs from the title. Title states the angle; H1 states the outcome.
  Patterns: "The <Keyword> That <outcome>", "<Keyword> for <every X, Y and Z>",
  "<Keyword>: <two-part promise>".
- **Keyword placement**: title, H1, meta, one or two FAQ questions, the schema
  description. H2s carry sub-intents and related entities, not the keyword.

## Recurring sections

- **Short answer** (guides, comparisons, calculators: section 2): four
  standalone takeaway H3s, each a full claim with a 2-sentence answer, written
  so an AI answer can quote any one of them alone.
- **FAQ** (always last): on new pages exactly 7 questions (blog posts 5–7);
  on existing pages a merge of 3–5 new questions below the live ones. Questions
  in Title Case, phrased the way
  people search (from autocomplete, related questions, forums). Answers open
  with "Yes." / "No." or the fact, stand alone, run under 60 words. Landing
  pages include: cost/trial, platform, "does it tell me what to do" (answered
  honestly), sharing/export, accuracy, plus one question containing the exact
  keyword. Guides put the safety or escalation question last; audience and list
  guides end with the pricing question. The FAQ is followed by a CTA banner.
- **Social proof**: only the proof bank, verbatim. Stat row (rating, rating
  count, downloads) in the hero and once more in its own section; 1–2 reviews
  that speak to this page's feature. Vary how each review is introduced; no
  lead-in sentence appears twice on a page.
- **Limits** ("A <Thing> Log, Not <Advice>", "What the Estimate Cannot Tell
  You"): what the product will never do. Required on regulated topics, useful
  everywhere.

## CTAs

One CTA label per section. The primary CTA from intake ("Get the App", "Start
Free Trial", "Book a Demo") is the default; the trial CTA goes on cost-intent
pages and at the FAQ end; one soft on-page CTA early ("See How It Works", "Try
the Calculator Above", "Jump to the Full Table"). Prices appear only where
`intake.md`'s pricing truth allows: on a pricing page or a pricing FAQ, taken
from the official site or store, with "checked <Month YYYY>" and a note when
prices vary by country. Elsewhere, point to the pricing page. Guides use about half on-page actions, half product CTAs.

## Internal links

Written into the copy as full URLs in the second sentence of a bullet: "…is
covered at <URL>." Each page links 2–5 siblings:
- broad → narrow (hub → every spoke; generic → each brand), tracker → its
  calculator, guide → the feature page that acts on it, vs ↔ switching ↔ sibling
  vs, blog post → its pillar and one money page;
- never to a page competing for the same intent;
- a link to a planned page that is not live yet gets `(planned)` after the URL.
  The implementer adds a `(planned)` link only once that page is live; until
  then the sentence stays and the link is left out. Keep `(planned)` links to
  the 2–5 that matter; a pillar does not need to link every future post.
A cluster page with heavy overlap ends with a hand-off H2 ("<X> and <Y> Have
Their Own Pages") with link cards.

## Key Components and Design Suggestions

- 2–4 Key Components per section: one visual (a phone/browser mockup of a
  **named real screen**, annotated screenshot, table, chart), one trust line
  (source line, disclaimer, "estimate" tag, trademark/not-affiliated note) and
  one conversion or navigation element (store badges, CTA, link cards).
- Design Suggestions: `<Pattern>: <one sentence>`, pattern chosen from this list
  and matched to the content's shape: Full-width hero, Centered hero, Two-column
  split, Three-column layout, Grid of cards, Feature cards, Alternating panels,
  Dashboard preview, Horizontal timeline, Process flow with phases,
  Checklist / steps list, Stat row, Stat/metric tiles, Trust indicator strip,
  Testimonial cards, Comparison table, Side-by-side comparison, Tabbed content,
  Accordion, CTA banner. Steps → Horizontal timeline; fields → Dashboard
  preview with numbered callouts; scenarios → Grid of cards; devices →
  Three-column layout; reviews → Stat row + Testimonial cards.

## Structured data

Three JSON-LD blocks, valid JSON:
1. `FAQPage` with the FAQ text verbatim (existing pages: new questions first,
   then the live ones, with any live answer that contradicts current facts
   corrected).
2. The page block: `SoftwareApplication` / `MobileApplication` (app pages;
   page-specific `description`, `operatingSystem`, `applicationCategory`,
   `publisher: {"@id": ".../#organization"}`; include `aggregateRating` only
   when it matches a verified store rating and count shown on the page, and
   update a stale live one rather than deleting it: software-app rich results
   need it),
   `WebApplication` (calculators, `isAccessibleForFree: true`), `Article` or
   `WebPage` (guides; `MedicalWebPage` with `about` on health topics) with
   `dateModified`/`lastReviewed` and, when one exists, a named `reviewedBy`.
3. `Organization` with `@id`, `name`, `legalName`, `url`.
On existing pages, never downgrade live schema: keep a live BreadcrumbList,
MobileApplication or richer Organization and merge.

## Fanning out to subagents

For more than ~6 plans, dispatch subagents grouped by template, 4–8 plans per
agent (combine small template groups so you run no more than ~5 agents). Give each: this file, its template, `intake.md`, the full
strategy.csv (the page map), `research/serp.md`, the sources, and the slugs it
owns. Tell it to write `plans/<slug>.md` files only. Reused copy (proof lines,
pricing line, limits lines) comes from `intake.md` so every agent writes the
same words. If a subagent's file-writing tool is blocked, it writes with a
shell heredoc instead.

## Cluster pass (after lint)

- Siblings in one family (brands, features, vs pages) differ in angle, unique
  section and FAQ questions; no shared boilerplate paragraph.
- Every hub links to every spoke; every spoke links to its hub.
- No two plans claim the same owned noun.
- Facts agree across plans (same number, same source date, same assumptions).
- Every internal URL is in the page map; planned targets are marked.
- Old FAQ answers merged into schema don't contradict new copy.
