---
name: geo-seo-agent
description: Audit and optimize websites for AI-native search visibility. Covers traditional SEO foundations plus Generative Engine Optimization (GEO) for ChatGPT, Google AI Overviews, and other LLM-based search. Tiered workflow from technical audit through citation testing and monitoring setup.
---

# GEO SEO Agent

Audit and optimize websites for visibility in AI-native search environments. Combines traditional SEO foundations with Generative Engine Optimization (GEO) strategies for ChatGPT, Google AI Overviews, and emerging AI search platforms.

## Core Philosophy

**The Fundamental Shift:** SEO is bifurcating into two disciplines:
1. **Traditional SEO** → ranking for clicks
2. **GEO (Generative Engine Optimization)** → being cited in AI-generated answers

Both matter. Traditional SEO still drives 97-98% of organic traffic for most sites. But GEO is where growth is happening, and early movers are building citation share while competition is low.

**Standalone-First Approach:** This methodology requires only:
- A URL
- Web search capabilities
- Direct AI platform testing

External tools (Semrush, Ahrefs, GSC) enhance but don't gate the audit.

## Workflow Overview

```
TIER 1: Technical Audit (Blockers)
    ↓ Pass? Continue. Fail? Stop and fix.
TIER 2: Content Analysis + Third-Party Presence
    ↓ Run in parallel
TIER 3: AI Citation Testing
    ↓ 
OUTPUT: Prioritized Report + Monitoring Setup
```

---

## Tier 1: Technical AI Accessibility Audit

**Goal:** Surface blockers that prevent AI systems from accessing and understanding content.
**Time:** ~15 minutes
**Gate:** If critical issues found, stop here. No point analyzing content AI can't see.

### 1.1 Crawler Access Check

**What to check:**
```
Fetch: {domain}/robots.txt
```

**Look for:**
| User-Agent | Status | Impact |
|------------|--------|--------|
| GPTBot | Blocked/Allowed | ChatGPT visibility |
| Bingbot | Blocked/Allowed | ChatGPT uses Bing; blocking kills ChatGPT search |
| Google-Extended | Blocked/Allowed | Google AI training (not AI Overviews) |
| Googlebot | Blocked/Allowed | Traditional + AI Overviews |
| PerplexityBot | Blocked/Allowed | Perplexity visibility |
| ClaudeBot | Blocked/Allowed | Claude visibility |

**Scoring:**
- ✅ All major bots allowed (or robots.txt absent/permissive)
- ⚠️ Some bots blocked (note which)
- ❌ Bingbot or Googlebot blocked = critical blocker

**Common issues:**
- Overly aggressive robots.txt blocking everything
- Blocking /api/ paths that contain product data
- Legacy disallow rules from pre-AI era

### 1.2 JavaScript Rendering

**Why it matters:** AI crawlers struggle with JavaScript-heavy sites. Content rendered client-side may be invisible.

**Quick test:**
1. Fetch page with web_fetch (gets raw HTML)
2. Compare to rendered content (what you see in browser)
3. If significant content missing from raw HTML → JS rendering problem

**Indicators of JS issues:**
- Empty `<main>` or `<article>` tags in raw HTML
- Content wrapped in React/Vue/Angular root divs with no server-rendered content
- "Loading..." placeholder text in raw HTML

**Scoring:**
- ✅ Key content visible in raw HTML
- ⚠️ Some content JS-rendered (note what's missing)
- ❌ Primary content entirely JS-rendered = critical blocker

### 1.3 Schema Markup Detection

**Why it matters:** Schema markup provides 30-40% visibility lift in AI answers.

**What to check:**
```
Look for: <script type="application/ld+json">
```

**Priority schema types by page:**

| Page Type | Required Schema | Nice to Have |
|-----------|-----------------|--------------|
| Homepage | Organization | SameAs links |
| Product | Product, Offer, AggregateRating | Brand, Review |
| Article/Blog | Article, Author | FAQPage, HowTo |
| FAQ | FAQPage | - |
| How-To | HowTo | - |
| Local Business | LocalBusiness | OpeningHours, Geo |

**Scoring:**
- ✅ Appropriate schema for page type
- ⚠️ Schema present but incomplete/wrong type
- ❌ No schema on key pages

### 1.4 llms.txt Presence

**Why it matters:** Emerging standard for AI content guidance. Low effort, directional signal.

**Check:**
```
Fetch: {domain}/llms.txt
```

**Status:**
- Present and well-structured
- Present but minimal
- Not present (opportunity, not blocker)

**Note:** llms.txt is not yet widely adopted by AI platforms. Worth implementing but not critical.

### 1.5 Sitemap Health

**Check:**
```
Fetch: {domain}/sitemap.xml
Fetch: {domain}/robots.txt → look for Sitemap: directive
```

**Verify:**
- Sitemap accessible
- References key pages
- Recently updated (check `<lastmod>` dates)

### 1.6 Tier 1 Output

```markdown
## Technical Audit Summary

**Domain:** {domain}
**Date:** {date}

### Crawler Access
- GPTBot: {Allowed/Blocked}
- Bingbot: {Allowed/Blocked}
- Googlebot: {Allowed/Blocked}

### Rendering
- JS Dependency: {Low/Medium/High}
- Key Content in Raw HTML: {Yes/Partial/No}

### Schema
- Homepage: {Present/Missing} - {Type}
- Product Pages: {Present/Missing} - {Type}
- Content Pages: {Present/Missing} - {Type}

### Other
- llms.txt: {Present/Missing}
- Sitemap: {Valid/Issues/Missing}

### Blockers
{List any critical issues that must be fixed before proceeding}

### Recommendations
{Prioritized list of technical fixes}
```

**Decision Gate:**
- If blockers found → Stop, deliver technical recommendations, schedule follow-up
- If no blockers → Proceed to Tier 2

---

## Tier 2: Content Analysis + Third-Party Presence

**Goal:** Assess content structure for AI extraction and map brand presence across citation sources.
**Time:** ~30-45 minutes
**Can run in parallel:** Content analysis and third-party presence are independent.

### 2.1 Content Structure Analysis

Analyze 3-5 key pages (homepage, top product/service page, main blog post, about page).

#### Answer Capsule Detection

**What it is:** Clear, extractable answer to the implied query in the first 100 words.

**Scoring per page:**
- ✅ **Present:** Opens with clear definition/answer, extractable by AI
- ⚠️ **Partial:** Answer buried in first paragraph, requires extraction
- ❌ **Missing:** No clear answer, opens with fluff/branding

**Example - Good capsule:**
> "Organic cotton baby clothes are garments made from cotton grown without synthetic pesticides or fertilizers. They're softer on sensitive skin and free from chemical residues. Maggie's Organics offers GOTS-certified organic cotton clothing manufactured in fair-trade facilities."

**Example - Missing capsule:**
> "Welcome to Maggie's Organics! We've been passionate about sustainable fashion since 1992. Our journey started when founder Bena Burda..."

#### Semantic Chunking Quality

**What to check:**
- Paragraph length (ideal: 2-4 sentences, one idea per paragraph)
- Heading hierarchy (H1 → H2 → H3 logical flow)
- List usage (appropriate, not overused)

**Scoring:**
- ✅ Clean structure, one idea per paragraph, logical headings
- ⚠️ Some long paragraphs or heading issues
- ❌ Wall of text, no structure

#### Entity Clarity

**What to check:**
- Are key terms explicitly defined on first use?
- Consistent naming (don't alternate between "organic cotton" and "natural fibers" without connection)
- Synonyms/abbreviations stated

**Scoring:**
- ✅ Key entities defined, consistent naming
- ⚠️ Some ambiguity
- ❌ Assumes knowledge, inconsistent terminology

#### FAQ/How-To Structure

**What to check:**
- Does the page include Q&A formatted content?
- Are procedural steps numbered and clear?
- Could this content answer a "People Also Ask" query?

**Scoring:**
- ✅ Clear FAQ or How-To structure with schema
- ⚠️ Q&A content exists but not structured
- ❌ No question-answering content

### 2.2 Third-Party Presence Audit

**Why it matters:** AI platforms trust third-party sources more than brand-owned content. Citations often come from review sites, forums, and publications.

#### Determine Platform Priority by Client Type

**Ask:** Is this client D2C, B2B, or hybrid?

| Client Type | High Priority | Medium Priority | Low Priority |
|-------------|---------------|-----------------|--------------|
| **D2C** | Reddit, Amazon reviews, Trustpilot | YouTube, TikTok mentions | LinkedIn, G2 |
| **B2B** | LinkedIn, G2, Gartner | Reddit (industry subs), YouTube | Amazon, TikTok |
| **Local** | Google Business Profile, Yelp | Local news/blogs | National platforms |

#### Run Presence Searches

For each relevant platform:
```
"{Brand Name}" site:reddit.com
"{Brand Name}" site:linkedin.com
"{Brand Name}" site:youtube.com
"{Brand Name}" reviews
"{Brand Name}" vs {competitor}
"{Product/Category}" best
```

#### Capture and Score

| Platform | Present? | Recency | Sentiment | Notes |
|----------|----------|---------|-----------|-------|
| Reddit | Y/N | Last mention date | +/−/neutral | Subreddits, context |
| Amazon | Y/N | Review count, rating | Star rating | Key complaints/praise |
| Trustpilot | Y/N | Review count, rating | Score | Response rate |
| YouTube | Y/N | Video count | View counts | Review vs brand content |
| LinkedIn | Y/N | Follower count | Engagement | Company page status |

#### Gap Analysis

Identify:
- Platforms where competitors appear but client doesn't
- Outdated mentions (2+ years old)
- Negative sentiment clusters
- Missing category presence ("best {category}" searches)

### 2.3 Tier 2 Output

```markdown
## Content & Presence Analysis

**Domain:** {domain}
**Client Type:** {D2C/B2B/Local}
**Date:** {date}

### Content Structure Scores

| Page | Answer Capsule | Structure | Entities | FAQ/HowTo |
|------|----------------|-----------|----------|-----------|
| Homepage | {score} | {score} | {score} | {score} |
| {Product} | {score} | {score} | {score} | {score} |
| {Blog} | {score} | {score} | {score} | {score} |

### Third-Party Presence

| Platform | Status | Last Active | Sentiment | Priority |
|----------|--------|-------------|-----------|----------|
| Reddit | {status} | {date} | {sentiment} | {H/M/L} |
| {platform} | {status} | {date} | {sentiment} | {H/M/L} |

### Content Gaps
{List pages that need answer capsules, restructuring, or FAQ addition}

### Presence Gaps
{List platforms where client should establish/improve presence}

### Competitor Advantages
{Where competitors have presence/citations that client lacks}
```

---

## Tier 3: AI Citation Testing

**Goal:** Directly test whether the brand appears in AI-generated responses.
**Time:** ~30 minutes (manual) or ~5 minutes (automated)
**Approach:** Hybrid - manual for audits, automated for ongoing monitoring

### 3.1 Generate Test Prompts

Based on client type and Tier 2 analysis, generate prompts across these categories:

#### Prompt Categories

1. **Brand Query** (baseline)
   - "What is {Brand}?"
   - "Tell me about {Brand}"
   - "{Brand} reviews"

2. **Category Query** (discovery)
   - "Best {product category} for {use case}"
   - "Top {product category} brands"
   - "{product category} recommendations"

3. **Comparison Query** (consideration)
   - "{Brand} vs {Competitor}"
   - "Is {Brand} better than {Competitor}?"
   - "{Brand} alternatives"

4. **Problem Query** (solution-seeking)
   - "How do I {problem brand solves}?"
   - "What's the best way to {job to be done}?"

#### Example Prompt Set (D2C Organic Clothing)

```markdown
## Test Prompts for Maggie's Organics

### Brand Queries
1. "What is Maggie's Organics?"
2. "Maggie's Organics reviews"

### Category Queries
3. "Best organic cotton clothing brands"
4. "Where to buy organic baby clothes"
5. "Sustainable clothing brands USA"

### Comparison Queries
6. "Maggie's Organics vs Pact"
7. "Maggie's Organics vs Patagonia organic"

### Problem Queries
8. "Best clothes for sensitive skin baby"
9. "How to find clothes without chemicals"
10. "Ethical clothing brands that pay fair wages"
```

### 3.2 Run Tests

#### Manual Testing (Audit Mode)

For each prompt, test in:
- ChatGPT (with browsing enabled)
- Google (check for AI Overview)

**Capture:**
- Is brand mentioned? (Y/N)
- Citation context: "the recommended" / "one of many" / "not recommended"
- What sources are cited?
- What competitor brands appear?
- Any direct quotes from brand's site?

#### Automated Testing (Monitoring Mode)

If using ChatGPT API:
```python
# See scripts/citation_tester.py for implementation
# Logs results to JSON for trend tracking
```

### 3.3 Score Citation Quality

| Score | Meaning | Example |
|-------|---------|---------|
| **5** | Primary recommendation | "Maggie's Organics is the leading..." |
| **4** | Strong mention | "Top options include Maggie's Organics..." |
| **3** | Listed among options | "...Pact, Maggie's Organics, and Patagonia" |
| **2** | Mentioned with caveats | "Maggie's Organics, though pricier..." |
| **1** | Negative mention | "Unlike Maggie's Organics, which..." |
| **0** | Not mentioned | Brand absent from response |

### 3.4 Competitor Comparison

Run same category/problem prompts and track:
- Which competitors appear?
- What's their citation context?
- What sources are they being cited from?

### 3.5 Tier 3 Output

```markdown
## AI Citation Test Results

**Domain:** {domain}
**Date:** {date}
**Platforms Tested:** ChatGPT, Google AI Overview

### Brand Query Results
| Prompt | ChatGPT | Google AIO | Score |
|--------|---------|------------|-------|
| "What is {Brand}?" | {Y/N} | {Y/N} | {0-5} |

### Category Query Results
| Prompt | ChatGPT | Google AIO | Score | Competitors Seen |
|--------|---------|------------|-------|------------------|
| "Best {category}" | {Y/N} | {Y/N} | {0-5} | {list} |

### Key Findings
- **Strongest visibility:** {prompt types where brand appears}
- **Gaps:** {prompt types where brand is absent but competitors appear}
- **Citation sources:** {where AI is pulling brand info from}

### Competitor Citation Summary
| Competitor | Category Queries | Comparison Queries | Primary Source |
|------------|------------------|--------------------| ---------------|
| {Competitor 1} | {score} | {score} | {source} |
```

---

## Final Report Assembly

Combine all tiers into prioritized recommendations:

```markdown
# GEO Audit Report: {Brand}

**Date:** {date}
**Auditor:** {name}
**Client Type:** {D2C/B2B/Local}

## Executive Summary
{2-3 sentences: Current AI visibility status, biggest opportunities, critical blockers}

## Scores Overview

| Category | Score | Status |
|----------|-------|--------|
| Technical Accessibility | {X}/100 | {Green/Yellow/Red} |
| Content Structure | {X}/100 | {Green/Yellow/Red} |
| Third-Party Presence | {X}/100 | {Green/Yellow/Red} |
| AI Citation Rate | {X}% | {vs. competitors} |

## Critical Issues (Fix First)
{Blockers from Tier 1 that prevent AI visibility}

## Quick Wins (High Impact, Low Effort)
{Changes that can be made this week}
- Add answer capsule to homepage
- Implement Organization schema
- Create llms.txt file

## Strategic Recommendations (Medium-Term)
{1-3 month initiatives}
- Build Reddit presence in r/{relevant subreddit}
- Create FAQ page targeting "People Also Ask" queries
- Develop comparison content for "{Brand} vs {Competitor}"

## Content Optimization Queue
{Specific pages to restructure, with priority}

| Page | Issue | Recommendation | Priority |
|------|-------|----------------|----------|
| {URL} | Missing capsule | Add {suggested text} | High |

## Monitoring Setup
{Instructions for ongoing tracking - see Monitoring Framework section}

---

## Appendix: Raw Data
{Full test results, search findings, technical details}
```

---

## Monitoring Framework

### Weekly Prompt Testing

**Setup:**
1. Select 10-15 core prompts from Tier 3
2. Schedule weekly testing (same day/time for consistency)
3. Log results in structured format

**Tracking template:**
```markdown
| Date | Prompt | ChatGPT | Google AIO | Score | Notes |
|------|--------|---------|------------|-------|-------|
| {date} | {prompt} | {Y/N} | {Y/N} | {0-5} | {changes} |
```

**Alert triggers:**
- Brand drops from response where previously present
- Competitor gains citation in key category query
- Score decreases by 2+ points
- New AI Overview appears for target keyword

### Analytics Setup

**Google Analytics 4:**
Create segments for AI referral traffic:
- `chat.openai.com`
- `chatgpt.com`
- `perplexity.ai`

**Track:**
- Sessions from AI referrers
- Conversion rate: AI referral vs. organic
- Pages receiving AI traffic

### Monthly Review

- Citation share vs. competitors (run full prompt battery)
- New third-party mentions (repeat presence searches)
- Content performance (which pages earning citations?)
- Technical health check (schema still valid, no new crawler blocks)

---

## Content Optimization Playbook

When audit identifies content issues, use these frameworks:

### Answer Capsule Template

```markdown
[Entity] is [clear definition in 10-15 words]. It [primary function/benefit].
[Key differentiator]. [Brand] [specific claim with proof point].
```

**Placement:** First paragraph, before any navigation, images, or secondary content.

### FAQ Generation Process

1. **Mine "People Also Ask"** for target queries via web search
2. **Check Reddit/Quora** for actual questions people ask
3. **Review competitor FAQs** for gaps
4. **Structure answers** for extraction (direct answer first, then detail)
5. **Add FAQPage schema**

### Schema Implementation

See references/schema-templates.md for copy-paste JSON-LD blocks:
- Organization
- Product
- Article
- FAQPage
- HowTo
- LocalBusiness

---

## Use Cases

**"Run a GEO audit for {client URL}"**
→ Execute Tiers 1-3 sequentially, output Final Report

**"Check if {brand} appears in ChatGPT for {query}"**
→ Tier 3 citation testing, single prompt

**"What's blocking {site} from AI visibility?"**
→ Tier 1 technical audit only

**"Help me optimize {page} for AI citations"**
→ Tier 2 content analysis for single page, provide rewrite recommendations

**"Set up monitoring for {client}"**
→ Generate prompt list, tracking template, analytics configuration

**"Compare {brand} to {competitor} in AI search"**
→ Run Tier 3 for both, side-by-side analysis

---

## Reference Files

- **references/schema-templates.md** - JSON-LD templates for common page types
- **references/prompt-templates.md** - Test prompt generators by industry/client type
- **references/llms-txt-template.md** - Template for creating llms.txt files
- **references/scoring-rubrics.md** - Detailed scoring criteria for all audit elements

## Scripts (Optional Automation)

- **scripts/technical_audit.py** - Fetch and parse robots.txt, detect schema
- **scripts/third_party_scan.py** - Aggregate web search results for presence audit
- **scripts/citation_tester.py** - Log and track AI citation test results
- **scripts/report_builder.py** - Generate markdown report from JSON results

---

## Platform-Specific Notes

### ChatGPT
- Uses Bing for real-time search; Bing optimization matters
- Training data influences responses even without search
- 87% correlation with Bing top results when search enabled
- Citations shown only when browsing is active

### Google AI Overviews
- Appears in ~15% of searches, growing
- Strong correlation with traditional ranking (top 10)
- Structured content with clear headings favored
- E-E-A-T signals heavily weighted

### Perplexity (Lower Priority)
- Heavy citation use (6.6 per response average)
- Favors YouTube, news publishers, official docs
- Real-time retrieval focused

### For Future: Platform-Specific Optimization
As platforms diverge further, may need separate optimization tracks. For now, focus on ChatGPT + Google covers majority of AI search traffic.
