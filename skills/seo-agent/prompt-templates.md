# AI Citation Test Prompt Templates

Generate test prompts by industry and client type. Use for Tier 3 citation testing.

---

## Prompt Structure

Every test battery should include:

1. **Brand Queries (2-3)** - Baseline: Does AI know the brand?
2. **Category Queries (3-5)** - Discovery: Does brand appear in category searches?
3. **Comparison Queries (2-3)** - Consideration: How does brand compare?
4. **Problem Queries (3-5)** - Solution: Does brand solve searcher's problem?

---

## D2C E-Commerce

### Apparel / Fashion

**Brand Queries:**
- "What is {{Brand}}?"
- "{{Brand}} reviews"
- "Is {{Brand}} legit?"

**Category Queries:**
- "Best {{product type}} brands"
- "Where to buy {{product type}} online"
- "Top {{attribute}} {{product type}}" (e.g., "sustainable clothing")
- "{{Product type}} for {{use case}}" (e.g., "workout clothes for hot weather")
- "Affordable {{product type}} that lasts"

**Comparison Queries:**
- "{{Brand}} vs {{Competitor}}"
- "{{Brand}} compared to {{Competitor}}"
- "{{Brand}} alternatives"

**Problem Queries:**
- "Best {{product}} for {{problem}}" (e.g., "best jeans for thick thighs")
- "How to find {{attribute}} {{product}}"
- "What to look for in {{product type}}"
- "{{Product}} that doesn't {{pain point}}"

### Food / Beverage / CPG

**Brand Queries:**
- "What is {{Brand}}?"
- "{{Brand}} ingredients"
- "Is {{Brand}} healthy?"

**Category Queries:**
- "Best {{product category}}"
- "Healthiest {{product type}}"
- "{{Attribute}} {{product}} brands" (e.g., "organic coffee brands")
- "Where to buy {{product type}}"

**Comparison Queries:**
- "{{Brand}} vs {{Competitor}}"
- "{{Brand}} nutrition vs {{Competitor}}"
- "Best {{product}} brand comparison"

**Problem Queries:**
- "Best {{product}} for {{dietary need}}" (e.g., "best protein powder for vegans")
- "{{Product}} without {{ingredient}}"
- "Low {{attribute}} {{product}} options"

### Beauty / Skincare

**Brand Queries:**
- "What is {{Brand}}?"
- "{{Brand}} reviews"
- "Is {{Brand}} cruelty free?"

**Category Queries:**
- "Best {{product type}} for {{skin type}}"
- "Top {{attribute}} skincare brands"
- "{{Product type}} recommendations"
- "Dermatologist recommended {{product}}"

**Comparison Queries:**
- "{{Brand}} vs {{Competitor}}"
- "{{Brand}} {{product}} vs {{Competitor}} {{product}}"
- "{{Brand}} dupes"

**Problem Queries:**
- "How to {{solve skin issue}}"
- "Best {{product}} for {{condition}}"
- "{{Product}} for {{age group}}"
- "Skincare routine for {{skin concern}}"

---

## B2B / SaaS

### Software / Tools

**Brand Queries:**
- "What is {{Product}}?"
- "{{Product}} reviews"
- "{{Product}} pricing"

**Category Queries:**
- "Best {{software category}} tools"
- "Top {{software category}} for {{company size}}"
- "{{Software category}} comparison"
- "{{Use case}} software recommendations"

**Comparison Queries:**
- "{{Product}} vs {{Competitor}}"
- "{{Product}} vs {{Competitor}} pros and cons"
- "{{Product}} alternatives"
- "{{Product}} competitors"

**Problem Queries:**
- "How to {{job to be done}}"
- "Best way to {{business process}}"
- "{{Pain point}} solutions"
- "Tools for {{workflow}}"

### Professional Services

**Brand Queries:**
- "What is {{Company}}?"
- "{{Company}} reviews"
- "Is {{Company}} good?"

**Category Queries:**
- "Best {{service type}} companies"
- "Top {{service type}} firms in {{location}}"
- "{{Service type}} agencies for {{company type}}"
- "{{Industry}} {{service type}} specialists"

**Comparison Queries:**
- "{{Company}} vs {{Competitor}}"
- "{{Service type}} agency comparison"
- "{{Company}} alternatives"

**Problem Queries:**
- "How to {{business challenge}}"
- "When to hire a {{service provider}}"
- "{{Service type}} for {{specific need}}"
- "How much does {{service}} cost?"

---

## Local Business

### Retail / Restaurant / Service

**Brand Queries:**
- "{{Business Name}} {{City}}"
- "{{Business Name}} reviews"
- "{{Business Name}} hours"

**Category Queries:**
- "Best {{business type}} in {{City}}"
- "{{Business type}} near me" (test from relevant location context)
- "Top rated {{business type}} {{City}}"
- "{{Attribute}} {{business type}} in {{neighborhood}}"

**Comparison Queries:**
- "{{Business}} vs {{Competitor}} {{City}}"
- "{{Business type}} comparison {{City}}"

**Problem Queries:**
- "Where to {{need}} in {{City}}"
- "{{Business type}} open {{time}}" (e.g., "restaurants open late")
- "{{Business type}} for {{occasion}}"
- "{{Business type}} that {{attribute}}" (e.g., "restaurants that take reservations")

---

## Industry-Specific Additions

### Healthcare / Wellness

Add compliance-aware queries:
- "Is {{treatment/product}} safe?"
- "{{Product}} side effects"
- "{{Condition}} treatment options"

**Note:** AI platforms are cautious with health claims. Focus on informational, not medical advice queries.

### Finance / Fintech

Add trust-focused queries:
- "Is {{Company}} legitimate?"
- "{{Company}} security"
- "{{Product}} fees"
- "{{Company}} FDIC insured?" (if applicable)

### Education / Courses

Add outcome-focused queries:
- "Is {{Course/School}} worth it?"
- "{{Course}} reviews from students"
- "{{Topic}} courses that lead to jobs"
- "Best way to learn {{skill}}"

---

## Prompt Testing Protocol

### For Each Prompt:

1. **Run in ChatGPT** (with browsing enabled)
   - Note: Enable "Search the web" or use ChatGPT-4 with browsing
   
2. **Run in Google** (check for AI Overview)
   - Note: AI Overviews appear above organic results
   - May need to be logged into Google account
   - Not all queries trigger AI Overview

### Capture for Each:

```markdown
| Prompt | Platform | Brand Mentioned? | Citation Context | Sources Cited | Competitors Mentioned |
|--------|----------|------------------|------------------|---------------|----------------------|
| {{prompt}} | ChatGPT | Y/N | Primary/Listed/Absent | {{sources}} | {{competitors}} |
| {{prompt}} | Google AIO | Y/N | Primary/Listed/Absent | {{sources}} | {{competitors}} |
```

### Citation Context Definitions:

- **Primary:** Brand is the main recommendation or answer
- **Listed:** Brand appears in a list of options
- **Mentioned:** Brand referenced but not recommended
- **Absent:** Brand not mentioned at all

---

## Generating Custom Prompts

### Template Formula:

**Category queries:**
```
Best [product/service category] [qualifier]
Top [product/service] for [use case/audience]
[Attribute] [product/service] [location/context]
```

**Problem queries:**
```
How to [job to be done]
Best [product/service] for [specific problem]
[Problem] solutions for [audience]
```

**Comparison queries:**
```
[Brand] vs [Competitor]
[Brand] compared to [Competitor] for [use case]
[Brand] alternatives for [specific need]
```

### Discovering Real Queries:

1. **Google Autocomplete:** Start typing category terms, note suggestions
2. **People Also Ask:** Check related questions in Google results
3. **Reddit/Quora:** Search for actual questions people ask
4. **AnswerThePublic:** Generate question variations (free tier available)
5. **Client customer service:** What do customers actually ask?

---

## Monitoring Prompt Selection

For ongoing monitoring, select 10-15 prompts:

- 2 brand queries (baseline)
- 5 category queries (highest volume opportunities)
- 3 comparison queries (vs. top competitors)
- 5 problem queries (aligned to key use cases)

**Rotate quarterly:** Add new prompts based on:
- New products/services launched
- New competitors emerging
- Seasonal relevance
- Trending topics in category
