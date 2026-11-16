# Template: new landing page (core product, feature, entity)

Conversion pages that walk the visitor to the primary CTA. 8–9 sections,
~1,100 words (single feature) to ~1,800 (commercial or entity page) of copy.

## Section order

| # | Slot | H3s | Notes |
|---|---|---|---|
| 1 | **Hero (H1)** | 1 | 2 bullets: what it does in one line, the honest limit or reassurance, the pricing truth. Key Components: store badges/CTA, mockup of a named screen, proof strip, "free to try" (or the true offer) line |
| 2 | **Frame the job** | 3–6 | One of: what each entry records; the problem it solves; the entity's own routine from its official source (entity pages); buyer criteria (best); what it replaces (free) |
| 3 | **How it works** | 3–4 | Numbered steps, setup, or the official schedule table. One soft CTA ("See How It Works") |
| 4–5 | **Feature depth** | 3–4 each | The feature shown next to the rest of the product ("on one timeline"); scenario cards ("Moments When <X> Matters") |
| 6 | **Report / export / share** | 3 | If the product has one: who you share it with and what it shows |
| 7 | **Coverage** | 3 | Platforms (phone, web, watch, widgets), entities supported, not-affiliated line |
| 8 | **Social proof** | 3 | Stat row + 1–2 reviews matched to the feature |
| 9 | **Limits** | 3 | What it never does ("A <Thing> Log, Not <Advice>"); can be an H3 inside another section on non-regulated topics |
| (10) | **Hand-off** | 2–3 | Only when siblings overlap heavily: "<X> and <Y> Have Their Own Pages" with link cards |
| last | **FAQ** | 7 | Then a CTA banner |

Slots 1–3 and the FAQ are fixed. Slots 6–9 may reorder.

## Rules by intent

- **Feature page**: the page owns one noun (history, schedule, rotation, scan).
  Shape the H2s around it; mention sibling features once each, with a link.
- **Entity page** ("<Brand> app"): section 2 quotes the entity's official
  source with its date; add the entity's unique fact as its own section;
  link to the generic hub and the entity's guide/calculator.
- **Audience page** ("<category> app for <audience>"): section 2 names the
  audience's three or four real problems in their words (from forums and
  reviews), sections 3–5 map each problem to a feature, social proof comes from
  that audience where the proof bank has it, and any limits line ("a tool, not
  treatment/advice") is stated once. Link to the audience guide if one exists.
- **"Best <category> app"**: a buyer's guide, not a ranking. The H3 under the
  H1 discloses authorship ("We Make <Brand>, So Here Is How to Judge Any App
  Fairly"). Order: 5–6 neutral criteria ("a good app should…") → "Popular
  <Category> Apps at a Glance" (competitors grouped by focus, each with a
  "suits people who…" line and one honest limitation, no prices, no criticism,
  a "details checked <Month YYYY>" stamp, links to their listings) → "Where
  <Brand> Stands Out" → red flags to watch for → platforms → reviews → FAQ.
  The FAQ answers "Is <Brand> the best?" with "not for everyone" and says who
  should pick something else.
- **"Free <category> app"** when the product is not free: title reframes to
  "free to try", the hero states what is paid, then a trial plan (Day 1, Day 2,
  … Then Decide), "Who <Brand> Fits, and Who It Might Not", and cancellation
  FAQs.

## Head tags

Title `<Keyword>: <concrete angle> | <Brand>` (45–60 chars). Meta 140–160
chars, question-led for commercial modifiers, otherwise action-led with the
keyword in sentence 2, ending "Free to try." or the proof line. H1 "The
<Keyword> That <outcome>" or "<Keyword> for <every X, Y and Z>".

## FAQ slots

cost/trial · platforms · "does it tell me what to do/take/eat" (honest answer) ·
sharing/export · accuracy/estimates · one question with the exact keyword · one
page-specific question.

## Schema

FAQPage + SoftwareApplication/MobileApplication (page-specific description,
`operatingSystem`, `applicationCategory`, publisher by `@id`; for SaaS use
`WebApplication`) + Organization.

## Example section

~~~markdown
## 3. Set Up a Habit Once
Heading Type: h2
Recommended Heading: Set Up a Habit Once

Rationale:
People who have abandoned habit apps worry about daily busywork. Showing that a habit is set up once and then runs on its own removes that worry.

Sub-Headings (H3). Bullets below each subheading are ready-to-use copy (can be implemented as paragraphs, bullets or any other text-style):

### Choose the Days That Count
- Habitly asks which days a habit belongs to, so a gym habit on Monday, Wednesday and Friday never breaks on a Tuesday. Rest days are marked for you.
- If your routine changes, you edit the days once. Your past streaks keep the schedule they were built on.

CTA Recommendations:
- See How It Works

Key Components to Include:
- Phone mockup of the habit setup screen with three weekdays selected
- Short line: "Habitly never sells your data"
- App Store and Google Play badges

Design Suggestions:
Process flow with phases: three phases left to right, each with a phone screen and one line of copy.
~~~
