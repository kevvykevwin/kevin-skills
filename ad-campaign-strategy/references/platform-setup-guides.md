# Platform Setup Guides

Detailed campaign setup instructions for major advertising platforms with best practices and platform-specific nuances.

## Meta (Facebook & Instagram)

### Campaign Structure

**Initiative-Based Organization (Recommended):**
```
Campaign Level: Always On - Prospecting
├── Ad Set 1: Core Audience - Age 25-44
├── Ad Set 2: Lookalike - 1% Website Visitors
└── Ad Set 3: Interest - Sustainable Living

Campaign Level: Q1 Lead Gen - Product Launch
├── Ad Set 1: Custom Audience - Email List
├── Ad Set 2: Lookalike - 1% Customers
└── Ad Set 3: Engaged Users - 90 days
```

**ABO vs CBO:**
- **Use ABO** when running initiative-based campaigns with distinct audiences
- **Use CBO** when testing multiple audiences with same objective and letting algorithm optimize budget
- No universal preference - choose based on campaign structure

### Campaign Settings

**Objective Selection:**
- Awareness: Brand awareness, Reach
- Consideration: Traffic, Engagement, App installs, Video views, Lead generation
- Conversion: Conversions, Catalog sales, Store traffic

**Buying Type:**
- Auction (default, recommended for most)
- Reach & Frequency (only for awareness with guaranteed delivery needs)

**Campaign Budget Optimization:**
- Enable if using CBO
- Set bid strategy (Lowest cost, Cost cap, Bid cap)
- Daily vs Lifetime budget

**Special Ad Categories:**
- Housing, Employment, Credit → Restricted targeting
- Political/Social → Disclaimers required

### Ad Set Settings

**Budget & Schedule:**
- Daily budget: Recommended for always-on
- Lifetime budget: Use for specific flight dates
- Schedule: Run continuously vs specific hours

**Audience:**
- Custom Audiences (your data)
- Lookalike Audiences (1%, 3%, 5%, 10%)
- Saved Audiences (interests, behaviors, demographics)
- Layer thoughtfully - avoid over-restricting

**Placements:**
- Advantage+ (automatic, recommended for reach)
- Manual (specific feeds, stories, reels, etc.)
- Remove Audience Network if concerned about quality

**Optimization & Delivery:**
- Conversion event selection
- Attribution window (7-day click, 1-day view standard)
- Delivery optimization (conversions, link clicks, impressions, etc.)

### Creative Best Practices

**Image/Video Specs:**
- Feed: 1080x1080 (1:1), 1080x1350 (4:5)
- Stories: 1080x1920 (9:16)
- Reels: 1080x1920 (9:16), <90 seconds
- Text limit: 125 characters primary, 27 headline

**Creative Strategy:**
- Mobile-first design
- Hook in first 3 seconds
- Test 3-5 creative variations per ad set
- Rotate creative every 2-4 weeks to avoid fatigue

### Geo Targeting Nuances

**Location Types:**
- People living in this location (most restrictive, best for local)
- People recently in this location (includes travelers)
- People traveling to this location
- People living in or recently in this location (broadest)

**Radius Targeting:**
- Available for local businesses
- 10-50 mile radius from address
- Layer with demographic/interest targeting

---

## Google Search

### Hagakure Campaign Structure

**Philosophy:** Simplified structure with fewer, high-performing campaigns
- Consolidate similar keywords into single ad groups
- Use broad match with audience signals
- Let Google's algorithm optimize

**Structure:**
```
Campaign: Brand Terms
└── Ad Group: All Brand Keywords (broad match)

Campaign: Core Product - [Product Category]
└── Ad Group: Product Keywords (broad match + audience)

Campaign: Competitors
└── Ad Group: Competitor Keywords
```

**Benefits:**
- Better data aggregation for machine learning
- Faster exit from learning phase
- Simpler management
- More auction participation

### Campaign Settings

**Geo Targeting - CRITICAL NUANCES:**

**Option 1: "Presence or Interest" (Default)**
- Shows ads to people IN your target location
- AND people searching FOR your target location (from elsewhere)
- Example: Someone in NYC searching "Denver hotels" sees your Denver ad

**Option 2: "Presence" (Recommended for local)**
- Shows ads ONLY to people physically IN your target location
- Filters out "searching for" traffic
- Better for local businesses, service areas

**Search Network Only:**
- **Enable:** Search partners (extends reach, usually good quality)
- **DISABLE:** Display Network
- Never run Search + Display in same campaign (different optimization)

**Search + Display = BAD:**
- Different user intent
- Different creative requirements
- Diluted performance data
- Hard to optimize
- → Always separate campaigns

### Ad Group Structure

**Keyword Match Types:**
- Broad match (preferred with Hagakure + audience signals)
- Phrase match (more control, smaller reach)
- Exact match (most control, smallest reach)
- Negative keywords (essential for all)

**Keyword Organization:**
- 5-20 keywords per ad group
- Group by theme/intent
- Include negative keywords list

### Ad Copy Best Practices

**Responsive Search Ads (RSAs):**
- 3-5 headlines minimum (15 max)
- 2-4 descriptions (4 max)
- Pin critical messaging (e.g., brand name, key value prop)
- Include keywords in headlines
- Test emotional vs rational messaging

**Extensions (Use All):**
- Sitelinks (4-6)
- Callouts (4-6)
- Structured snippets
- Call extensions
- Location extensions
- Price extensions

### Conversion Tracking

**Setup Requirements:**
- Google Tag in <head>
- Conversion events tagged
- Import from GA4 if available
- Set conversion values
- Choose primary conversion for optimization

### Bidding Strategy

**Options:**
- Maximize Conversions (learning/testing phase)
- Target CPA (once you have data)
- Target ROAS (for e-commerce with value tracking)
- Manual CPC (advanced, full control)

**Learning Period:**
- 7-14 days or 50 conversions
- Don't make changes during learning
- Fund appropriately for learning

---

## TikTok

### Campaign Structure

**Creative-First Approach:**
- TikTok optimizes for creative performance
- Test multiple creatives per ad group
- Refresh creative frequently (weekly)

**Structure:**
```
Campaign: Always On - Prospecting
├── Ad Group 1: Custom Audience - Website Visitors
├── Ad Group 2: Lookalike - Video Viewers
└── Ad Group 3: Interest - Beauty & Personal Care
```

### Campaign Settings

**Objective:**
- Awareness: Reach, Video views
- Consideration: Traffic, App installs, Lead generation
- Conversion: Website conversions, Catalog sales

**Budget:**
- Campaign budget (CBO equivalent)
- Ad group budget (ABO equivalent)
- Minimum: $50/day ad group, $20/day campaign

**Optimization Location:**
- Optimize at campaign level (recommended)
- Or ad group level for more control

### Ad Group Settings

**Placements:**
- TikTok only (purest, recommended)
- TikTok + partners (broader reach, may dilute quality)

**Automated Creative Optimization:**
- Enable to test multiple video + text combinations
- Platform tests and serves best performers

### Creative Best Practices

**Video Specs:**
- 9:16 vertical (1080x1920)
- 9-15 seconds ideal
- 60 seconds max
- Hook in first 1-2 seconds

**Creative Strategy:**
- Native content > polished ads
- Sound-on optimization (80% watch with sound)
- Fast-paced editing
- Authentic, relatable content
- User-generated content style
- Trending sounds/effects

**Text:**
- 100 characters max
- Direct, conversational tone
- Include CTA

### Targeting

**Custom Audiences:**
- Website visitors (pixel)
- App activity
- Customer file
- Engagement (video views, profile visits)

**Lookalike Audiences:**
- 1-10% similarity
- Based on source audience

**Interest & Behavior:**
- 20+ predefined categories
- Layer multiple for precision

---

## LinkedIn

### Campaign Structure

**B2B Focus:**
- Professional targeting is LinkedIn's strength
- Higher CPMs but higher-quality B2B leads
- Best for: Decision-makers, enterprise sales, professional services

**Structure:**
```
Campaign: Content Syndication - Executives
├── Ad Group 1: C-Suite - Tech Industry
├── Ad Group 2: Directors - Healthcare
└── Ad Group 3: VPs - Financial Services
```

### Campaign Settings

**Objective:**
- Awareness: Brand awareness, Website visits
- Consideration: Engagement, Video views, Website visits
- Conversion: Lead generation, Website conversions, Job applicants

**Ad Format:**
- Single image
- Carousel
- Video
- Text ads (right rail)
- Sponsored messaging (InMail)
- Lead gen forms (native)

### Targeting - LinkedIn's Superpower

**Professional Attributes (Use These):**
- Job title (specific or broad)
- Job function (Marketing, Finance, IT, etc.)
- Seniority level (Entry, Manager, Director, VP, C-Suite)
- Company name (target specific companies)
- Company size (employees, revenue)
- Industry (25+ categories)
- Skills

**Education & Experience:**
- Degree
- Field of study
- School
- Years of experience

**Member Interests:**
- Groups
- Member traits

**Layering Strategy:**
- Start with job function + seniority
- Add industry or company size
- Test removing demographics (LinkedIn will optimize)

### Budget & Bidding

**Minimum Spend:**
- $10/day campaign budget
- Realistically need $50-100/day for learning

**Bid Strategy:**
- Maximum delivery (automated, default)
- Cost cap (once you have CPA target)
- Manual bid (advanced)

**Expected CPMs:**
- $30-80 depending on targeting specificity
- More specific = higher CPM
- C-Suite always highest

---

## Pinterest

### Campaign Structure

**Visual Search Platform:**
- Users have high purchase intent
- Longer conversion windows (28-day standard)
- Best for: E-commerce, home, fashion, beauty, food

**Structure:**
```
Campaign: Always On - Shopping
├── Ad Group 1: Actalike - Website Purchasers
├── Ad Group 2: Interest - Home Decor
└── Ad Group 3: Keyword - "Organic Cotton Clothing"
```

### Campaign Settings

**Objective:**
- Awareness: Brand awareness, Video views
- Consideration: Consideration (traffic)
- Conversion: Conversions, Catalog sales

**Budget:**
- Campaign budget optimization (recommended)
- Ad group budgets (more control)
- Minimum: $10/day ad group

### Targeting

**Audience:**
- Actalikes (Pinterest's lookalikes)
- Customer lists
- Website visitors
- Engagement audiences

**Interest & Keyword:**
- 400+ interest categories
- Keyword targeting (unique to Pinterest)
- Search terms users are actively using

**Demographics:**
- Age, gender, location
- Device type
- Language

### Creative Best Practices

**Pin Specs:**
- 2:3 aspect ratio (1000x1500) ideal
- 1:1, 9:16 also supported
- Static or video
- Multiple pins per ad group

**Creative Strategy:**
- Lifestyle imagery
- Product in context
- DIY/tutorial content
- Seasonal/inspirational
- Text overlay (brief)
- High-quality, vertical images

**Shopping Behavior:**
- Users plan purchases weeks in advance
- Long consideration period
- Multiple sessions before converting
- 28-day attribution window standard

---

## Platform Comparison Quick Reference

| Platform | Best For | Targeting Strength | Typical CPM | Min Budget/Day |
|----------|----------|-------------------|-------------|----------------|
| Meta | D2C, Local, Broad reach | Audience graph, Behaviors | $5-15 | $5 |
| Google Search | High intent, Direct response | Keywords, Search intent | $10-50 | $10 |
| TikTok | Gen Z, Brand awareness, Viral | Creative performance | $8-20 | $50 |
| LinkedIn | B2B, Professional services | Job title, Company, Industry | $30-80 | $10 ($50+ realistic) |
| Pinterest | E-commerce, Planning | Visual search, Shopping intent | $5-10 | $10 |

## Universal Best Practices

**All Platforms:**
1. Install conversion tracking before launching
2. Test multiple audiences in separate ad sets
3. Run for 7-14 days before optimizing
4. Refresh creative regularly
5. Monitor daily for first week, then weekly
6. Document all changes for learning
7. Compare performance to benchmarks (see fractional-cmo-frameworks)

**Budget Allocation:**
- 70-80% to proven performers
- 20-30% to testing new audiences/creative
- Never put all budget in one ad set/campaign

**Optimization Cadence:**
- Daily: Monitor pacing, catch errors
- Weekly: Performance review, minor adjustments
- Monthly: Major optimization, budget reallocation
- Quarterly: Strategic review, new initiatives
