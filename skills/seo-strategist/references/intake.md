# Phase 1: Intake

Goal: one file, `seo-plan/<domain>/intake.md`, that holds every fact a plan is
allowed to state. Plans quote it; they never improvise product claims.

## Find it yourself first

Read before asking. Sources, in order:
1. The site: homepage, features/pricing/FAQ pages, footer (legal name), any
   existing guides. Use `scripts/crawl_site.py` output from phase 2 if it
   already exists.
2. The app-store listings (App Store, Google Play) or marketplace listing:
   rating, rating count, downloads, platforms, verbatim reviews.
3. The repo, if you are in one: feature names exactly as the UI says them
   (i18n files, screen titles), pricing/trial logic, supported integrations.
4. The help center and docs, especially articles on plans, pricing and
   free-vs-paid features by platform (third-party sites often get these wrong),
   plus the changelog and press kit.

## Then ask, in one message, only what is still missing

Ask with a single multi-part question (AskUserQuestion where the answers can
be listed). The items an agency's intake form covers:

| Item | Why it matters |
|---|---|
| **No-go list**: topics, claims, words, page types to never publish | Rows that break it are never proposed |
| **Feature ranking**: top features by importance to the business | Feature pages are planned in this order; the #1 feature gets a page |
| **Competitors**: 3–8 names or domains | Competitor gap map, comparison pages |
| **Pricing truth**: what is free, trial length, what needs payment | Decides "free" vs "free to try" wording everywhere |
| **Primary CTA**: download, start trial, book demo, buy | The button every landing section ends on |
| **CMS / how pages get built**, blog location | Rollout plan; whether `/blog` exists |
| **Search Console export** (Performance → Pages and Queries, 12 months) | Protects ranking URLs; finds striking-distance queries |
| **Keyword tool access**: Ahrefs/Semrush export, DataForSEO credentials | Exact volume and difficulty instead of estimates |
| **Audience and markets**: country, language | Volume country, spelling, units |

When the client cannot give a feature ranking, infer it from the order of
the store listing and the homepage, write "(inferred)" next to the ranking in
`intake.md`, and say "in our inferred ranking" in the notes that rely on it.

When sources disagree on a proof number (the store shows 169K ratings, the
site's schema says 100K), use the primary live source with its check date,
never the larger unverified figure, and list the mismatch as a fix for the
client.

If the user cannot answer now, proceed with what you have and mark the gaps in
`intake.md` under `## Open questions`. Questions that only matter for one page
go in that row's note as "Question for you: …" instead of blocking.

## intake.md layout

```markdown
# Intake: <Brand> (<domain>)
Checked: <YYYY-MM-DD>

## Company
Legal name / brand name / what it is in one sentence / company type
(Mobile Apps | SaaS | E-commerce | Local Service | Marketplace | Content)
Platforms / markets / primary CTA label

## Pricing truth
Exact wording to use (e.g. "free to try: free download and a 7-day free trial;
<feature> needs a subscription after the trial"). Never "free" if it isn't.

## Features (ranked)
1. <Exact in-product name>: what it does, in 1–2 factual sentences. Unique vs
   competitors? (yes/no, which competitors lack it)
2. ...

## Proof bank (use verbatim, nothing else)
- Rating: 4.7 on the App Store from 4,000+ ratings (checked <date>)
- Downloads/users: ...
- Reviews (verbatim, with source and the feature each one speaks to):
  - "..." (App Store review, <month year>) → feature: <name>

## Rules
- No-go topics/pages: ...
- Banned words/claims: ...  (always: no superlatives you cannot prove, no "#1"
  unless a cited source says it)
- Required wording: naming of features, trademark symbols, disclaimers
- Regulated topic? yes/no → if yes, read references/regulated-topics.md and
  list the primary sources (labels, standards, official docs) here

## Competitors
| Name | Domain | Positioning in their own words | Pages worth noting |

## Page map (filled in phase 2)
| URL | Status (live/planned) | Page type | Job (one sentence) |

## Open questions
```

## Exit check

- Every feature has its exact in-product name.
- The proof bank has a check date on every number.
- The no-go list exists, even if it says "none given".
