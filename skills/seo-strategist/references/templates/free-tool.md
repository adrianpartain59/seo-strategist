# Template: new free tool page (calculator, chart, maker, generator, template, checker, timer)

"The tool sits at the top, with copy and what to include around it."
9 sections (H1 + 8 H2), ~35 H3s, ~1,500 words of copy.

## Choosing free tools (strategy phase)

Keep keywords matching `* calculator | * chart | * converter | * generator |
* maker | * template | * checker | * timer | how long does * | * percentage`
when the tool's logic is transparent (a formula from a citable public source,
or rules you can state in plain text, like "fit tasks between wake and sleep
time with a 10-minute buffer"), difficulty is low (KD ≤ ~30 or `Easy`), and it
ties clearly to the audience and the product. The results page should show
tools, not only articles; if it shows only design templates or articles, a
working tool is the angle. Drop any
tool that would give individual advice (dosing, legal, tax filing) or that the
client's rules forbid. "Chart" and "calculator" are different intents: a chart
page gets a full-width chart hero and a reading guide. For entity families
(one generic, several brands), build hub → generic → brand pages only when each
brand has its own fact, and give every page a control unique to it.

## Section order

| # | Section | H3s | CTA |
|---|---|---|---|
| 1 | H1 + the tool. One H3 promise ("See How Much of Your X May Still Be Working") with usage folded into the bullets | 1 | primary CTA |
| 2 | Short answer facts: "How Long X Stays in Your System" / "<Thing> at a Glance" (stat tiles or a table, each fact sourced) | 3–4 | Try the Calculator Above |
| 3 | Method: "How the Estimate Is Calculated" or "How the <Tool> Works" (formula or rules in plain text, a worked example, a table, what to enter, privacy) | 4 | Try the Calculator Above |
| 4 | Page-unique angle (form A vs form B, how to read the chart, why repeated use builds up, the audience twist) | 4 | Try / Build Your Chart Above |
| 5 | Limits: "What the Estimate Can and Cannot Tell You" (not a measurement, never advice, one published number) | 3–4 | Try the Calculator Above |
| 6 | Product bridge 1: "Track <Thing> in <Brand>" | 4–5 | primary CTA |
| 7 | Product bridge 2, a different angle (report, timeline, progress) + one review quote | 4 | primary CTA |
| 8 | "Related Calculators and Trackers" (4 link cards: siblings, parent, hub, tracker) | 4 | See All Calculators |
| 9 | FAQ (7) | 7 | primary CTA |

## Tool spec (section 1, Key Components, always in this order)

1. "The calculator directly under the H1:" its inputs, defaults, units, the
   add-another-row control if any, validation, and **the one control unique to
   this page**.
2. Results: the outputs (list each stat), the chart (axes, range), and a
   one-line plain-language summary of the result.
3. Privacy line: "Calculated on your device. Nothing is stored or sent, and
   nothing is added to the web address."
4. Disclaimer line: "Estimate only, not a <measurement/advice>; <Brand> is not
   affiliated with <maker>" where relevant.

For tools without a formula (makers, generators, timers), section 3 becomes
"How the <Tool> Works": the rules it applies, in plain text, with one worked
example. Either way, the method in section 3 must be exactly what the tool
computes. Say a phone
calculator can check it, and give one worked example with real numbers.

## Rules

- Every number: "about"/"approximately", its source and the source's revision
  date. Separate label/official facts from rules of thumb, and say which is
  which.
- The exact keyword appears once in body copy, inside an FAQ answer, spelled as
  searched.
- Title `<Keyword>: <concrete promise>` 45–60 chars, meta 140–160 ending with a
  privacy or offer line ("Private, no sign-up."), H1 47–64 chars.
- Schema: FAQPage + WebApplication (`isAccessibleForFree: true`, category,
  disclaimer in the description) + Organization.
