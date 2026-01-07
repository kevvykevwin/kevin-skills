# Targeting Strategy

Framework for building effective targeting strategies across platforms, with emphasis on understanding when to use audience vs contextual vs behavioral targeting.

## Core Targeting Philosophy

**The Golden Rule:**
Different platforms have different targeting strengths. Match your targeting strategy to the platform's algorithm and data advantages.

**Three Targeting Categories:**
1. **Audience** - WHO they are (your data + platform data about people)
2. **Contextual** - WHERE they are / WHAT they're doing (content, keywords, placements)
3. **Interests/Behavioral** - WHAT they like / HOW they act (platform-inferred preferences)

## Platform-Specific Targeting Hierarchy

### Google Search: Contextual is King

**PRIMARY: Contextual (95% of strategy)**
- Keywords (search queries)
- Search intent signals
- Ad position/placement

**SECONDARY: Audience (5% of strategy)**
- Remarketing lists for search ads (RLSA)
- Customer Match
- Similar audiences
- In-market audiences (as signals, not sole targeting)

**Why Contextual Wins on Search:**
- User explicitly declares intent via search query
- Keyword = strongest signal of what they want right now
- Audience layering can improve, but keyword is foundation

**Search Targeting Framework:**

**1. Build Keyword Structure**
```
Brand Keywords
├── Exact brand name
├── Brand + product
└── Brand misspellings

Category Keywords
├── Product type (broad)
├── Product type + modifier
└── Product type + intent (buy, best, cheap, etc.)

Competitor Keywords
├── Competitor name
└── Competitor + alternative
```

**2. Match Type Strategy**
- Start with Phrase or Exact for control
- Expand to Broad with audience signals (Hagakure approach)
- Always maintain robust negative keyword list

**3. Layer Audiences (Optional Enhancement)**
- Add remarketing audiences with bid adjustments
- Use Customer Match for RLSA campaigns
- Test in-market audiences as observation

---

### Meta & TikTok: Audience Graph Dominance

**PRIMARY: Audience (70% of strategy)**
- Custom Audiences (your first-party data)
- Lookalike/Similar Audiences
- Platform's behavioral graph

**SECONDARY: Interests/Behavioral (25% of strategy)**
- Interest categories
- Behaviors
- Life events
- Engagement patterns

**TERTIARY: Contextual (5% of strategy)**
- Placement selection
- Topic/content alignment (minimal impact)

**Why Audience Wins on Social:**
- Platforms have massive behavioral datasets
- Social graph reveals preferences better than declared interests
- Lookalikes leverage network effects
- Algorithm optimizes within audience parameters

**Social Targeting Framework:**

**1. Start with Your Data (Warmest Audiences)**
```
Tier 1: Recent Customers
├── Purchased last 30 days
├── High LTV customers
└── Repeat purchasers

Tier 2: Engaged Prospects
├── Website visitors (last 30/60/90 days)
├── Add to cart (didn't purchase)
├── Video viewers (75%+)
└── Instagram/Facebook engagers

Tier 3: Email/CRM
├── Email subscribers
├── App users
└── Lead form submissions
```

**2. Build Lookalikes (Scale Your Best)**
```
1% Lookalike (most similar, smallest reach)
├── Source: Purchasers
├── Source: High LTV customers
└── Source: Engaged website visitors

3% Lookalike (balanced similarity/reach)
5% Lookalike (broader reach)
10% Lookalike (maximum reach, least similar)
```

**3. Layer Interests (Expansion)**
- Use to expand beyond lookalikes
- Test 3-5 interest combinations
- Avoid over-layering (restricts delivery)

**Example Layering:**
- Base: Lookalike 1-3% Website Visitors
- Add: Interest in "Sustainable Living" AND "Organic Products"
- Geography: US
- Age: 25-54

---

### LinkedIn: Professional Attributes Reign

**PRIMARY: Professional Targeting (80% of strategy)**
- Job titles
- Job functions
- Seniority levels
- Company names/sizes
- Industries

**SECONDARY: Firmographics (15% of strategy)**
- Company size (employees)
- Company revenue
- Company growth rate
- Industry classifications

**TERTIARY: Interests/Education (5% of strategy)**
- Skills
- Groups
- Degrees/schools

**Why Professional Wins on LinkedIn:**
- Self-reported, verified work information
- B2B buying decisions are role-based
- Professional context = high signal

**LinkedIn Targeting Framework:**

**For B2B Lead Gen:**
```
Job Function: Marketing
├── Seniority: Director, VP, C-Suite
├── Company Size: 200-10,000 employees
└── Industry: Technology, Software

OR

Job Titles: ["CMO", "VP Marketing", "Director of Marketing"]
└── Company Names: [Target account list]
```

**Layering Strategy:**
1. Start with job function + seniority
2. Add company size OR industry
3. Test without demographic restrictions
4. Let LinkedIn's algorithm optimize within professional parameters

---

### Display/Programmatic: Balanced Approach

**BALANCED: Contextual + Audience (50/50)**
- Contextual targeting finds right moments
- Audience targeting finds right people
- Combination = best performance

**Contextual Signals:**
- Website topics/categories
- Keyword conte

xts (not search, but page content)
- Placement lists (specific sites)
- Content safety/brand safety

**Audience Signals:**
- Retargeting
- CRM audiences
- Third-party data segments
- Behavioral categories

**Programmatic Targeting Framework:**

**1. Contextual Foundation**
```
Topic Categories
├── Relevant content verticals
├── Exclude: News, politics (if brand-sensitive)
└── Include: Brand-safe environments

Site/App Lists
├── Whitelist: Premium publishers
├── Blacklist: Low-quality, unsafe
└── Private marketplaces (PMPs)
```

**2. Audience Layer**
```
First-Party Data
├── Website retargeting
├── CRM upload
└── App activity

Third-Party Segments
├── In-market shoppers
├── Demographic segments
└── Interest segments
```

**3. Combine for Precision**
- Retargeting + Content category = High intent + relevant moment
- Lookalike + Premium sites = Scale + quality
- In-market + Competitor content = Intercept strategy

---

### Pinterest: Visual Intent + Interest

**PRIMARY: Interest + Keyword (60% of strategy)**
- Interest categories (visual preferences)
- Keyword targeting (active search)
- Shopping behaviors

**SECONDARY: Audience (40% of strategy)**
- Actalikes (Pinterest lookalikes)
- Retargeting
- Customer Match

**Why This Balance on Pinterest:**
- Users actively search with keywords (like Google)
- But in visual/inspirational context (like Instagram)
- Hybrid: Declared intent + inferred preferences

**Pinterest Targeting Framework:**

**1. Keyword + Interest Combo**
```
Keywords: "organic baby clothes"
├── Interests: Parenting, Eco-friendly, Baby
└── Shopping behavior: Frequent buyers

Keywords: "minimalist home decor"
├── Interests: Home decor, Interior design
└── Shopping behavior: Planning a project
```

**2. Audience Retargeting**
```
Engaged Pinners
├── Saved your pins
├── Clicked your ads
└── Visited website

Actalike Audiences
├── Source: Website purchasers
├── Source: Engaged pinners
└── Percentage: 1-10%
```

---

## Targeting Best Practices by Goal

### Goal: Brand Awareness (Top of Funnel)

**Platform Recommendations:**
1. **Meta:** Broad lookalikes (5-10%), interest categories
2. **TikTok:** Interest targeting, video views objective
3. **LinkedIn:** Job function + industry (broad)
4. **YouTube:** Topic targeting, demographic overlays
5. **Pinterest:** Interest categories, keyword discovery

**Targeting Approach:**
- Cast wider net
- Focus on reach over precision
- Test multiple audience segments
- Accept lower conversion rates
- Measure brand lift, not just conversions

### Goal: Lead Generation (Middle of Funnel)

**Platform Recommendations:**
1. **Meta:** Lookalikes 1-3%, engaged website visitors
2. **LinkedIn:** Specific job titles + company size
3. **Google Search:** High-intent keywords (comparison, review, demo)
4. **Pinterest:** Actalikes + keyword targeting

**Targeting Approach:**
- Balance reach and relevance
- Layer audiences strategically
- Test multiple messaging angles
- Measure cost per qualified lead
- Optimize for lead quality, not just volume

### Goal: Direct Response (Bottom of Funnel)

**Platform Recommendations:**
1. **Google Search:** Brand + competitor keywords
2. **Meta:** Retargeting + customer lookalikes 1%
3. **Pinterest:** Shopping behavior + actalikes
4. **LinkedIn:** Named accounts (ABM)

**Targeting Approach:**
- Narrow, high-intent audiences
- Prioritize retargeting
- Focus on conversion optimization
- Accept higher CPMs for quality
- Measure ROAS and CAC

---

## Common Targeting Mistakes

### Mistake 1: Over-Layering

**Bad:**
- Age: 25-34
- Gender: Female
- Interest: Fitness
- Behavior: Health & Wellness
- Location: Major cities
- Income: Top 25%

**Result:** Audience too small, can't learn or scale

**Fix:** Start with 1-2 primary signals, expand if performance allows

### Mistake 2: Ignoring Platform Strengths

**Bad:**
- Using only interests on Meta (ignoring lookalikes)
- Using only audiences on Google Search (ignoring keywords)
- Broad demographics on LinkedIn (ignoring job titles)

**Fix:** Lead with platform's core strength, layer others as secondary

### Mistake 3: Static Targeting

**Bad:**
- Set it and forget it
- Never test new audiences
- Keep underperforming audiences running

**Fix:**
- Regular audience performance review
- Always test 1-2 new audiences
- Pause/remove chronic underperformers
- Refresh lookalikes as source data grows

### Mistake 4: No Exclusions

**Bad:**
- Showing ads to recent purchasers
- No negative keywords
- No brand safety filters

**Fix:**
- Exclude converters (unless relevant)
- Maintain robust negative lists
- Set brand safety parameters
- Exclude employee/internal traffic

---

## Targeting Testing Framework

### Test Structure

**Control vs Test:**
- Always run proven audience as control
- Test one new audience at a time
- Equal budget allocation for fair test
- Run for 7-14 days minimum

**What to Test:**
```
Week 1-2: Audience Type
├── Control: Lookalike 1% Purchasers
└── Test: Interest - Sustainable Fashion

Week 3-4: Audience Expansion
├── Control: Lookalike 1%
└── Test: Lookalike 3%

Week 5-6: Layering
├── Control: Lookalike 3% (no layering)
└── Test: Lookalike 3% + Interest overlay
```

### Success Criteria

**Declare Winner When:**
- Statistical significance reached (varies by volume)
- Clear performance difference (>20% variance)
- Minimum: 50 conversions per variant
- Consistent over full test period

**Metrics to Compare:**
- CTR (engagement quality)
- CVR (conversion quality)
- CPA (efficiency)
- ROAS (return)
- Volume (scale potential)

---

## Advanced Targeting Strategies

### Sequential Targeting (Funnel-Based)

Build campaigns that progress users through journey:

**1. Awareness Campaign (Wide Targeting)**
- Objective: Reach, Video views
- Audience: Broad lookalikes, interests
- Creative: Educational, inspirational
- Budget: 40% of total

**2. Consideration Campaign (Mid Targeting)**
- Objective: Traffic, Engagement
- Audience: Video viewers (from step 1), engaged users
- Creative: Product benefits, social proof
- Budget: 30% of total

**3. Conversion Campaign (Narrow Targeting)**
- Objective: Conversions
- Audience: Website visitors, add-to-cart
- Creative: Offers, urgency, testimonials
- Budget: 30% of total

### Geo-Targeted Expansion

Test new markets systematically:

**Phase 1: Core Markets (Proven)**
- 60% of budget
- Optimize for efficiency

**Phase 2: Expansion Markets (Testing)**
- 30% of budget
- Higher CPAs acceptable for learning

**Phase 3: Experimental Markets (New)**
- 10% of budget
- Pilot programs, gather data

### Dayparting & Scheduling

Layer time-based targeting:

**B2B (LinkedIn, Professional):**
- Weekdays only
- Business hours (9 AM - 5 PM)
- Avoid weekends

**B2C (Meta, TikTok):**
- Evening peak (6 PM - 10 PM)
- Weekend mornings
- Test 24/7 for broader reach

**E-commerce (Always On):**
- 24/7 delivery
- Bid up during peak conversion times
- Don't restrict (algorithm will optimize)

---

## Targeting Documentation

**Always Document:**
- Audience definition and setup
- Platform and campaign name
- Test hypothesis
- Success criteria
- Results and learnings
- Next steps

**Use for:**
- Building institutional knowledge
- Avoiding repeat failed tests
- Scaling winning strategies
- Onboarding team members
- Client reporting and transparency
