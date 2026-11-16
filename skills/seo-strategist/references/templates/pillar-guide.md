# Template: pillar guide (informational head term)

"Sourced copy, section by section, ready to publish." For the biggest
informational searches in the product's world (in a health app: "<drug> side
effects"; in a planner app: "how time blocking works"; in a finance app: "<tax
form> explained"). 9 sections, ~38 H3s, ~1,250–1,400 words of copy.

## Research first

1. List the H2s of the top 5 results. Keep the facets that answer intent; drop
   facets that need advice you cannot give or claims you cannot source, and
   replace them with "when to get help / escalate" and "track and share".
2. Fetch the **primary source** (official label, standard, government data,
   vendor documentation) and record its revision date. Secondary sources only
   if the client approves them.
3. Mine questions (autocomplete, related questions, forums): at least 3 FAQs no
   sibling page uses.

## Section order

| # | Section | H3s |
|---|---|---|
| 1 | H1 hero: what the source says is most common/important + the timing or scope caveat; "This page covers X, Y, Z. All figures come from <source>, revised <Month YYYY>." | 1 |
| 2 | Short answer: 4 standalone takeaways (the top fact with its number, the pattern over time, how many stop/fail/drop, the serious risk or caveat) | 4 |
| 3 | The core facts with numbers and comparators (a table built from the source's table) | 5 |
| 4 | Serious or less common facts (warnings, edge cases, exceptions) | 5 |
| 5 | When to get help / escalate, in fixed parts: urgent, call the professional, before a procedure/deadline, questions about your plan (deflect) | 4 |
| 6 | Why it happens and when it changes (mechanism, timing) + one page-unique H3 | 4 |
| 7 | Product: track it (each H3 maps to a feature) | 4 |
| 8 | Product: share it + related reading (internal links in one H3) | 4 |
| 9 | FAQ (7), escalation question last | 7 |

Product copy appears only in sections 7–8 and the FAQ. Sections 1–6 may carry a
CTA button but never describe the product.

## Rules

- Attribute inside the sentence: "The <Source> lists…", "In <study/trial>, X
  was reported by A% compared with B% on <comparator>." Give the comparator and
  the population with every rate.
- Use the source's own hedges ("it is not known whether", "the label does not
  give a rate"). If something is not in the source, say "not listed" and route
  the reader to tracking and the professional.
- Never merge numbers from different studies into one ranking; say they cannot
  be directly compared.
- Plain words first, the technical term once in apposition ("burping, listed
  as eructation").
- Source line under the H1, at the end of each data section and at the end of
  the FAQ. Real outbound link to the primary source in `## Sources`.
- Sibling pillars (brand vs generic, product A vs product B) differ by source,
  population and one unique section; the generic page is the hub with a
  comparison table and a "Why the Numbers Differ" H3.
- Title `<Keyword>: <angle 3–6 words>`, 45–60 chars. Meta 140–160 chars opening
  with the strongest sourced statistic. H1 `<Keyword>: <What X Says> and <What
  to Track / When to Get Help>`.
- Schema: FAQPage + Article/WebPage (`MedicalWebPage` with `about` on health
  topics) with `dateModified`/`lastReviewed` and a named `reviewedBy` when the
  client has a qualified reviewer + Organization. Show a visible "Reviewed by /
  Last updated" line.

## Example H3

~~~markdown
### Most People Who Quit Do It in the First Two Weeks
- In the Habitly 2025 user survey of 2,140 adults, 41% of people who dropped a new habit stopped within the first 14 days, compared with 12% between days 15 and 30. The survey asked people to recall when they stopped, so the timing is self-reported.
~~~

Source line under the section: "Source: Habitly 2025 User Survey, n=2,140, fielded March 2025."
