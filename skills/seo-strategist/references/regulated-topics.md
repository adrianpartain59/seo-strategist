# Regulated topics (health, medication, finance, legal, safety)

Two levels. Decide which in intake and write it in `intake.md` under Rules.

- **Full**: the product or its content touches medication, diagnosis,
  treatment, investments, taxes, legal rights or physical safety (a medication
  tracker, a budgeting app that projects returns, a legal-forms site). Every rule
  below applies.
- **Light**: the topic is health- or money-adjacent but the product makes no
  claims about it (a planner with an ADHD audience, a cycle-aware calendar, a
  savings-goal list). Apply only: facts about the condition or topic come from
  government or professional bodies with dates; a "<Product> is a tool, not
  treatment/advice" limits line; no claim the product improves the condition;
  recommend a qualified reviewer for the guide pages; crisis or emergency
  numbers only when the topic warrants them, labelled with their country.
  Trademark symbols are not needed at this level.

The rules below sit on top of the page-plan rules and win any conflict.

## Before research

- Get the client's no-go list (topics, products not yet approved, calculations
  that amount to advice). Never propose those rows; list them under "left out"
  in the strategy summary.
- Name the **primary source** for each entity: the official label/prescribing
  information, the regulator's page, the statute or official guidance, the
  standard. Record the revision date.

## In every plan

- **Facts only from the primary source**, attributed in the sentence with its
  revision date ("The <Brand>® label (revised <Month YYYY>) says…"). Numbers
  always with comparator and population. Secondary sources only with client
  approval.
- **Never advise.** No "what dose/amount/plan should I take", no conversions
  between products, no missed-step instructions. Quote steps from the source,
  follow with "your own plan may differ" and route decisions: "your
  <prescriber / accountant / attorney> decides". Use the professional's role
  word consistently (e.g. "prescriber"); use the everyday word ("doctor") only
  inside FAQ questions, because that is how people search.
- **The product is a record, not a treatment or a recommendation**: it logs,
  organizes, reminds, reports, estimates. Every computed number is "an
  estimate, not a <lab value / tax figure / legal opinion>".
- **A limits section** on every landing page ("A <Thing> Log, Not <Advice>"),
  and a **when-to-get-help** section on every guide (urgent / call the
  professional / before a procedure or deadline / questions about your plan).
- **Off-label or unofficial uses** are "not a listed use", never "people use it
  for".
- **Trademarks**: ® or ™ on every brand mention in copy (drop them inside
  JSON-LD `name`), plus a not-affiliated line naming the makers.
- **E-E-A-T**: a visible "Reviewed by <name, credential> / Last updated <date>"
  line when the client has a qualified reviewer, and `reviewedBy` +
  `lastReviewed` in schema. If there is none, say so in the plan's first Key
  Components and recommend one.
- **Pricing**: the exact approved wording, never "free" when there is a paid
  requirement.

## Why this wins

The live results for regulated head terms are full of pages that give
conversion charts, unsourced claims and advice. A page that stays inside the
primary source, dates every fact and hands decisions to the professional is the
page an AI answer can safely quote. That is the angle; say so in the rationale.
