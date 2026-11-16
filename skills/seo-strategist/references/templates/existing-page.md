# Template: existing page (on-page optimization)

Use for every `Existing page (update)` row, whatever its page type. The plan is
a **diff against the live page**: it never rewrites the page, never
re-specifies a working tool, and leaves intro, hero and CTA copy alone unless a
rule below says otherwise.

## Steps

1. **Capture the live page.** Fetch the rendered page (not the source template)
   and record title, meta description, H1, every H2/H3, card titles, FAQ
   questions and answers, and the JSON-LD. "Original Content" is copied
   verbatim from this, including special characters.
2. **Head-tag audit.** Produce a `Section:` block only for what breaks a rule:
   - title: over 60 characters; keyword not first (the homepage may lead with
     the brand); contains "&", an em dash, "#1" or another unprovable
     superlative; or no longer matches the page's job. Rewrite to
     `<Exact Keyword>: <2–3 concrete things> | <Brand>`, 45–60 characters
     (prefer 54–60 to use the space). Cut a
     benefit before you cut the brand suffix.
   - meta-description: over 160 characters, or missing the keyword. Rewrite to
     140–160 characters: verb-led benefit, the keyword, a proof line, the offer.
   - h1 / first h2: only to remove an unsupported claim, add the keyword or a
     missing scope, or fix the angle.
   If nothing breaks a rule, write no `Section:` blocks; put this one line
   under the heading instead: "No head-tag changes: the title and meta
   description already meet the rules." Don't churn ranking pages.
3. **Gap analysis.** List every fact from `intake.md` and the sources that
   serves this page's job and that the page never states. Add the modules the
   page lacks: how-it-works steps (under the hero), what each entry/record
   holds, the sourced facts block, the report/export, platforms, social proof
   (just above the FAQ), a sibling hand-off.
4. **Write 3–5 `New Section` blocks and 1–3 `Add to Existing Section`
   merges**, six blocks in total is typical. The FAQ is always a merge: append
   4 new questions (3 on brand/entity pages) below the live ones in the same
   style. Lead with the cost question unless the page already answers it;
   include one question with the exact keyword. A merge names the live heading
   verbatim and uses the fixed sentence "The page already has a "<heading>"
   section. Merge the additions below into it; do not create a duplicate
   section."
5. **Each New Section**: `Placement:` (after which live section), `Why
   Include:` as two sentences ("The page <explains X> but never <shows Y>."
   then the benefit to the visitor or to AI answers), 3 H3s (max 4) of 2×2
   copy, 3 Key Components (a visual, a trust line, a conversion or navigation
   element), one Design Suggestion. When merging into a card section, say
   "same card style as the existing cards".
6. **Hand-offs.** One sentence per adjacent sub-topic owned by a sibling:
   "…is covered at <URL>. This page stays focused on <job>." 2–4 per page.
7. **Schema.** FAQPage with the new questions first, then the live ones (fix
   any live answer that now contradicts the facts). Keep and extend the live
   page schema; never swap a richer type for a poorer one or drop a
   BreadcrumbList.

## Homepage

The homepage owns the head category term. Title may lead with the brand
("<Brand>: The <Category> App for <audience>"); H1 carries the category term.
Typical additions: a "what it tracks/does" overview with links to every feature
page, the proof section, a platforms section, and a FAQ merge. If another page
targets the head term, that page is redirected here (strategy.md).

## Entity pages (brand vs generic)

- Brand page: opens with that brand's own facts (its official source, its
  schedule, its form), links up to the generic hub.
- Generic hub: opens with "One <thing>, <N> names/brands" (each brand's use +
  link to each brand page), gives only the shared facts, and owns one angle the
  brand pages don't (e.g. the calculator or the comparison).

## Free tools and calculators (existing)

Leave the tool alone (a wording fix like "plotter" → "calculator" is fine).
New sections follow a fixed recipe:
- Formula/data tools: (a) a direct-answer box "<Thing> at a Glance"; (b) a
  worked numeric table or "Three Real-Life Examples"; (c) "What This Estimate
  Leaves Out".
- Health/finance/everyday calculators: (a) method plus a worked example ("How
  the Daily Target Is Worked Out"); (b) a bridge to the product's audience
  ("<Thing> When <Audience Situation>"); (c) practical guidance or limits.
Then merges into the app panel, the "more free tools" block and the FAQ.

## Example block

~~~markdown
## New Section: Set a Reminder in Two Taps
Recommended Heading Type: h2
Suggested Heading Name: Set a Reminder in Two Taps
Placement: after the intro paragraphs

Why Include:
The page explains why habits slip but never shows a reminder being set. A short flow makes the feature tangible and gives search and AI answers a clear how-to for habit reminder queries.

Sub-Headings (H3). Bullets below each subheading are ready-to-use copy (can be implemented as paragraphs, bullets or any other text-style):

### Pick the Habit, Pick the Time
- Tap a habit and choose when Habitly should remind you. The reminder repeats on the days you picked.
- It takes a few seconds and replaces the sticky note. Habitly sends the nudge even when the app is closed.

Key Components to Include:
- Three phone screens: choosing the habit, choosing the time, the reminder on the Lock Screen
- Caption under each screen naming the step
- App Store and Google Play badges under the steps

Design Suggestions:
Horizontal timeline: three phone screens left to right with a step under each, collapsing to a vertical list on mobile.
~~~
