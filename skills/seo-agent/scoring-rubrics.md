# GEO Audit Scoring Rubrics

Detailed scoring criteria for all audit elements. Use for consistent evaluation.

---

## Tier 1: Technical Scores

### Crawler Access Score (0-100)

| Score | Criteria |
|-------|----------|
| **100** | All major bots allowed (GPTBot, Bingbot, Googlebot), no restrictive rules |
| **80** | Core bots allowed, minor restrictions on non-essential paths |
| **60** | Some bots blocked but Googlebot + Bingbot allowed |
| **40** | Bingbot blocked (impacts ChatGPT) but Googlebot allowed |
| **20** | Googlebot blocked or severely restricted |
| **0** | robots.txt blocks all crawlers or returns error |

**Weight in Technical Score:** 30%

---

### JavaScript Rendering Score (0-100)

| Score | Criteria |
|-------|----------|
| **100** | All key content visible in raw HTML source |
| **80** | Main content in HTML, secondary elements JS-rendered |
| **60** | Navigation and some content JS-rendered, core text visible |
| **40** | Product/article content partially JS-dependent |
| **20** | Primary content requires JS to render |
| **0** | Site is entirely JS-rendered (SPA with no SSR) |

**How to test:**
1. View page source (not DevTools)
2. Search for key heading text
3. Check if product names/prices visible in raw HTML
4. Look for content inside `<noscript>` tags

**Weight in Technical Score:** 25%

---

### Schema Implementation Score (0-100)

| Score | Criteria |
|-------|----------|
| **100** | Appropriate schema on all key pages, validates without errors |
| **80** | Schema on most pages, minor validation warnings |
| **60** | Schema on homepage + some key pages |
| **40** | Schema present but wrong type or significant errors |
| **20** | Minimal schema (only basic Organization) |
| **0** | No schema markup detected |

**Schema presence by page type:**

| Page | Minimum Schema | Full Credit |
|------|----------------|-------------|
| Homepage | Organization | Org + BreadcrumbList |
| Product | Product | Product + AggregateRating + Review |
| Article | Article | Article + Author + FAQPage |
| FAQ | FAQPage | FAQPage |
| Category | BreadcrumbList | BreadcrumbList + ItemList |

**Weight in Technical Score:** 30%

---

### Site Structure Score (0-100)

| Score | Criteria |
|-------|----------|
| **100** | Valid sitemap, llms.txt present, clean URL structure |
| **80** | Valid sitemap, clean URLs, no llms.txt |
| **60** | Sitemap present with minor issues, decent URL structure |
| **40** | Sitemap outdated or errors, messy URLs |
| **20** | Sitemap missing or broken |
| **0** | No sitemap, chaotic URL structure, blocking issues |

**Weight in Technical Score:** 15%

---

### Technical Score Calculation

```
Technical Score = (Crawler × 0.30) + (JS × 0.25) + (Schema × 0.30) + (Structure × 0.15)
```

**Interpretation:**
- 80-100: Strong technical foundation, proceed to Tier 2
- 60-79: Minor issues, note but proceed
- 40-59: Significant issues, prioritize fixes before Tier 2
- 0-39: Critical blockers, stop and remediate

---

## Tier 2: Content Scores

### Answer Capsule Score (0-100)

| Score | Criteria | Example |
|-------|----------|---------|
| **100** | Clear definition/answer in first 50 words, extractable, includes differentiator | "Organic cotton is cotton grown without synthetic pesticides. It's softer and safer for sensitive skin. Maggie's Organics offers GOTS-certified organic cotton." |
| **80** | Answer in first 100 words, mostly extractable | Opens with benefit statement, definition follows |
| **60** | Answer present but buried in first paragraph | Starts with brand story, gets to point by sentence 3-4 |
| **40** | Answer requires reading multiple paragraphs | Definition scattered across intro section |
| **20** | Answer exists on page but not prominently placed | Definition in middle or end of content |
| **0** | No clear answer/definition on page | Pure marketing fluff, no informational content |

**Per-page scoring, then average across key pages.**

---

### Semantic Structure Score (0-100)

| Score | Criteria |
|-------|----------|
| **100** | One idea per paragraph, logical H1→H2→H3 flow, appropriate list usage |
| **80** | Good structure, occasional long paragraph or heading skip |
| **60** | Decent structure, 2-3 issues per page |
| **40** | Structure problems: walls of text, heading hierarchy issues |
| **20** | Poor structure: inconsistent headings, very long paragraphs |
| **0** | No structure: single block of text, no headings |

**Check for:**
- Paragraph length (ideal: 2-4 sentences)
- Heading hierarchy (no skipping H2→H4)
- List usage (appropriate, not excessive)
- White space and scanability

---

### Entity Clarity Score (0-100)

| Score | Criteria |
|-------|----------|
| **100** | Key terms defined on first use, consistent naming, synonyms stated |
| **80** | Most terms clear, minor inconsistencies |
| **60** | Some terms undefined, occasional naming switches |
| **40** | Assumes reader knowledge, inconsistent terminology |
| **20** | Jargon-heavy, no definitions, confusing naming |
| **0** | Incomprehensible without prior knowledge |

**Examples:**
- Good: "GOTS certification (Global Organic Textile Standard) ensures..."
- Bad: "Our GOTS-certified products meet the highest standards..." (assumes reader knows GOTS)

---

### FAQ/How-To Score (0-100)

| Score | Criteria |
|-------|----------|
| **100** | Dedicated FAQ section with schema, questions match real searches |
| **80** | FAQ content with schema, good question variety |
| **60** | FAQ content without schema, or schema with weak questions |
| **40** | Some Q&A content but poorly structured |
| **20** | Minimal Q&A, not formatted as FAQ |
| **0** | No question-answering content |

**Quality indicators:**
- Questions phrased as users actually search
- Answers are direct and extractable
- FAQPage schema implemented correctly

---

### Content Score Calculation

```
Content Score = (Capsule × 0.35) + (Structure × 0.25) + (Entity × 0.20) + (FAQ × 0.20)
```

---

## Tier 2: Third-Party Presence Score

### Platform Presence Score (0-100)

Score based on presence across relevant platforms for client type.

**D2C Scoring:**

| Score | Criteria |
|-------|----------|
| **100** | Active presence on Reddit + reviews (Amazon/Trustpilot) + 2+ other platforms |
| **80** | Present on Reddit + one review platform, mentions elsewhere |
| **60** | Present on 2 platforms but limited engagement |
| **40** | Present on 1 platform, minimal presence elsewhere |
| **20** | Sporadic mentions, no consistent presence |
| **0** | Brand essentially invisible on third-party platforms |

**B2B Scoring:**

| Score | Criteria |
|-------|----------|
| **100** | Active LinkedIn + G2/Capterra presence + industry publications |
| **80** | LinkedIn + G2 presence, some industry mentions |
| **60** | Present on 2 platforms, limited reviews/engagement |
| **40** | LinkedIn presence only, minimal reviews |
| **20** | Sparse presence, few or no reviews |
| **0** | No meaningful third-party presence |

---

### Recency Adjustment

Apply modifier based on how recent mentions are:

| Last Mention | Modifier |
|--------------|----------|
| Within 3 months | ×1.0 (no change) |
| 3-6 months | ×0.9 |
| 6-12 months | ×0.8 |
| 1-2 years | ×0.6 |
| 2+ years | ×0.4 |

---

### Sentiment Adjustment

| Sentiment | Modifier |
|-----------|----------|
| Primarily positive | ×1.0 |
| Mixed | ×0.8 |
| Primarily negative | ×0.5 |

---

### Third-Party Score Calculation

```
Third-Party Score = Platform Score × Recency Modifier × Sentiment Modifier
```

---

## Tier 3: Citation Scores

### Individual Prompt Score (0-5)

| Score | Meaning | Indicator |
|-------|---------|-----------|
| **5** | Primary recommendation | "The best option is..." "I recommend..." |
| **4** | Strong mention | "Top choices include [brand]..." |
| **3** | Listed among options | "[Brand] is one of several options..." |
| **2** | Mentioned with caveats | "[Brand], though [caveat]..." |
| **1** | Negative or dismissive mention | "Unlike [brand]..." "Better alternatives to [brand]..." |
| **0** | Not mentioned | Brand absent from response |

---

### Citation Rate Calculation

```
Citation Rate = (Prompts where brand mentioned / Total prompts tested) × 100
```

**Interpretation:**
- 80-100%: Strong AI visibility
- 60-79%: Good visibility, room for improvement
- 40-59%: Moderate visibility, significant gaps
- 20-39%: Low visibility, major work needed
- 0-19%: Essentially invisible to AI

---

### Citation Quality Score

Average of individual prompt scores:

```
Citation Quality = Sum of all prompt scores / Number of prompts
```

**Interpretation:**
- 4.0-5.0: Excellent (brand is primary recommendation)
- 3.0-3.9: Good (brand appears prominently)
- 2.0-2.9: Fair (brand mentioned but not featured)
- 1.0-1.9: Poor (mentioned negatively or with caveats)
- 0-0.9: Very poor (rarely mentioned)

---

## Overall Audit Score

### Weighted Composite

```
Overall Score = (Technical × 0.25) + (Content × 0.30) + (Third-Party × 0.20) + (Citation × 0.25)
```

**Interpretation:**

| Score | Rating | Meaning |
|-------|--------|---------|
| 80-100 | Excellent | Strong AI visibility, focus on optimization |
| 65-79 | Good | Solid foundation, targeted improvements needed |
| 50-64 | Fair | Significant gaps, prioritized action required |
| 35-49 | Poor | Major issues across multiple areas |
| 0-34 | Critical | Fundamental problems, comprehensive overhaul needed |

---

## Score Presentation

### For Internal Use

Show all raw scores with breakdowns for diagnostic purposes.

### For Client Presentation

Simplify to:
- Overall letter grade (A/B/C/D/F)
- Category scores (Technical/Content/Presence/Citations)
- Top 3 issues
- Top 3 opportunities

Avoid overwhelming with granular scores unless client is technical.
