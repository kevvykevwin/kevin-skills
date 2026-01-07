---
name: google-ads-strategy
description: Google Ads campaign strategy, setup, and keyword research. Use for Search campaign planning, Hagakure-style campaign structure, keyword categorization (brand/non-brand/long-tail), bidding strategy, and account configuration. Covers budget recommendations, match type strategy, and campaign naming conventions.
---

# Google Ads Campaign Strategy

Methodology for planning, structuring, and launching Google Ads campaigns with focus on Search.

## Strategy Decision Framework

### Campaign Type Selection

| Type | When to Use | Budget Allocation |
|------|-------------|-------------------|
| **Search** | Always. 70-90% of recommendation. | Primary spend |
| **Performance Max** | Gap coverage, reach extension | Capped budget |
| **YouTube** | Brand awareness only, client understands tracking limitations | Secondary |
| **Display** | Almost never. Only Fortune 500 or via PMax | Avoid for SMB |

### Budget Threshold

**Ideal range:** $6k-10k/month minimum

Below this threshold, assess:
- Current marketing mix and gaps
- Industry competitiveness
- Whether paid search is the right channel

## Campaign Setup (Hagakure Structure)

### Account-Level Settings

Before creating campaigns:
- Set conversion goals at account level
- Ensure conversion tracking is properly configured

### Campaign Settings Checklist

| Setting | Configuration |
|---------|---------------|
| Search Partners | OFF |
| Display Partners | OFF |
| Start Date | Today |
| End Date | None |
| Location | US or localized per business |
| Location Targeting | "People in or regularly in your targeted locations" |

### Campaign Structure

**Hagakure approach:** Theme-based campaigns, not SKAGs

```
Account
├── Campaign: [Theme A]
│   ├── Ad Group: [Subtopic 1] - Exact/Phrase
│   └── Ad Group: [Subtopic 2] - Exact/Phrase
├── Campaign: [Theme B]
│   └── Ad Groups...
└── Campaign: [Broad/PMax] - Reach extension (capped)
```

### Naming Convention

`campaign_ad.group_match.type`

Examples:
- `organic-apparel_womens-tees_exact`
- `brand_core-terms_phrase`
- `pmax_all-products_auto`

### Match Type Strategy

| Match Type | Use Case | Structure |
|------------|----------|-----------|
| **Exact** | High-intent, proven converters | Primary ad groups |
| **Phrase** | Discovery within themes | Paired with exact |
| **Broad** | Controlled reach extension | Isolated campaign OR PMax only |

### Bidding Ladder

Progress through as data accumulates:

1. **Maximize Conversions** → Start here, gather conversion data
2. **Target CPA** → Once you have 15-30 conversions, set target
3. **Target ROAS** → When revenue tracking is solid

## Keyword Research

### Tools

- **Primary:** Google Keyword Planner, SpyFu
- **Optional:** SEMrush (if budget allows)

### Categorization Framework

| Category | Definition | Priority |
|----------|------------|----------|
| **Brand** | Company/product name terms | Protect, low CPC |
| **Non-Brand** | Category/solution terms | Primary growth driver |
| **Long-Tail** | 3+ word specific queries | High intent, lower volume |
| **Product/Service** | Specific offerings | Break out if themes are robust |

### Keyword Research Process

1. **Seed list** → Client's products, services, solutions they provide
2. **Expand via Keyword Planner** → Related terms, search volume, competition
3. **Competitive intel via SpyFu** → What competitors bid on
4. **Categorize** → Brand / Non-Brand / Long-Tail / Product
5. **Prioritize** → Start with highest intent, expand from there

### Negative Keywords

**Initial setup:** Flag obvious non-fits for the business
- Free, DIY, jobs, careers (unless relevant)
- Competitor brand terms (unless conquesting)
- Irrelevant modifiers

**Ongoing:** Review search terms report weekly post-launch, add negatives based on actual queries

## Launch Checklist

See references/launch-checklist.md for pre-launch verification steps.

## Client Type Notes

Strategy applies universally across:
- D2C ecommerce
- B2B lead gen
- Local services

**Pharma/Healthcare:** Same approach, but audit against Google's healthcare policies before launch. May require certification or have restricted targeting.
