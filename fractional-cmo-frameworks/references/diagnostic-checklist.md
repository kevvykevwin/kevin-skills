# Diagnostic Checklist

Decision tree for determining whether business issues stem from marketing, operations, or both.

## When to Use This Framework

**Trigger Scenarios:**
- Revenue below forecast
- Conversion rates declining
- Marketing spend increasing without proportional return
- C-suite asks "Is this a marketing problem?"
- Customer complaints increasing
- Sales team says leads aren't converting

## Diagnostic Process

### Step 1: Define the Problem Precisely

**What specifically is happening?**
- Revenue down X% vs [time period/forecast]
- Traffic down X%
- Conversion down X%
- Customer acquisition cost up X%
- Customer complaints up X%

**Over what timeframe?**
- Sudden drop (1-2 weeks) → Look for technical issues or external shocks
- Gradual decline (4-8 weeks) → Market or competitive shifts
- Sustained underperformance (8+ weeks) → Structural issues

**Compared to what baseline?**
- Previous year same period (accounts for seasonality)
- Previous quarter
- Forecast/target
- Industry benchmarks

### Step 2: Gather Data

**Marketing Metrics:**
- Traffic volume (overall and by channel)
- Traffic quality (bounce rate, time on site, pages per session)
- Click-through rates
- Cost per click / Cost per impression
- Landing page performance
- Campaign performance trends

**Funnel Metrics:**
- Homepage → Product page conversion
- Product page → Add to cart
- Add to cart → Checkout initiated
- Checkout initiated → Purchase completed
- Each stage: volume and conversion rate

**Operational Metrics:**
- Inventory availability
- Out-of-stock rate
- Average delivery time
- Delivery success rate
- Customer service ticket volume
- Return/refund rate
- Site speed/performance
- Checkout error rate

**External Factors:**
- Competitive activity
- Market trends
- Seasonality
- Economic indicators
- Platform/algorithm changes

### Step 3: Run the Diagnostic

## Marketing vs Operations Decision Tree

### Question 1: Is traffic down?

**YES - Traffic is down significantly**
→ **This is primarily a MARKETING problem**

**Drill down:**
- Which channels are down?
- Is it all channels or specific ones?
- Did we reduce spend?
- Did ad performance decline (CTR, CPM increasing)?
- Did algorithm/platform changes occur?
- Did competitors increase activity?

**Common causes:**
- Reduced marketing spend
- Creative fatigue
- Audience saturation
- Competitive pressure
- Platform algorithm changes
- Seasonal decline
- Brand reputation issues

**Actions:**
- Increase/optimize marketing spend
- Refresh creative
- Test new audiences
- Analyze competitive landscape
- Check brand health metrics

**NO - Traffic is normal or up**
→ Continue to Question 2

---

### Question 2: Is overall conversion rate down?

**YES - Conversion rate across the funnel is down**
→ **This is likely an OPERATIONS problem**

**Drill down:**
- Where in the funnel is the drop-off?
- Is it consistent across all traffic sources?
- Are there site errors or technical issues?
- Has pricing changed?
- Has product availability changed?

**Common causes:**
- Site performance issues (slow load times)
- Technical bugs
- Pricing increases
- Inventory/stock issues
- Competitive pricing pressure
- Product quality concerns
- Poor user experience

**NO - Conversion rate is normal**
→ Continue to Question 3

---

### Question 3: Where specifically is the problem?

**Analyze by funnel stage:**

#### Scenario A: High traffic, low product page visits
**Problem:** Homepage isn't engaging or directing users

**Diagnosis:** Could be marketing or operations
- Marketing: Wrong audience, poor messaging match
- Operations: Site UX issues, unclear navigation
- Both: Landing page experience doesn't match ad promise

**Actions:**
- A/B test homepage layout
- Audit message match (ads → landing page)
- Check mobile experience
- Review navigation clarity

---

#### Scenario B: High product views, low add-to-cart
**Problem:** Products aren't compelling or trust is low

**Diagnosis:** Usually operations, sometimes marketing
- Operations: Pricing too high, product details unclear, no social proof, images poor quality
- Marketing: Wrong audience seeing products, messaging disconnect

**Actions:**
- Review pricing vs competitors
- Audit product page content (images, descriptions, reviews)
- Test trust signals (guarantees, returns policy, reviews)
- Check audience targeting quality

---

#### Scenario C: High add-to-cart, low checkout initiation
**Problem:** Something stopping users from starting checkout

**Diagnosis:** Usually operations
- Shipping costs revealed too late
- Limited payment options
- Checkout looks complicated
- Security concerns
- Unexpected fees

**Actions:**
- Test showing shipping costs earlier
- Add payment options
- Simplify checkout flow
- Add security badges
- Review return/exchange policy clarity

---

#### Scenario D: High checkout initiation, low completion
**Problem:** Checkout process has friction

**Diagnosis:** Almost always operations
- Too many form fields
- Payment processing errors
- Unexpected charges at final step
- Site technical issues
- Abandoned cart due to shipping time

**Actions:**
- Technical audit of checkout
- Reduce form fields
- Test guest checkout
- Review error messages
- Check payment gateway issues
- Show delivery times earlier

---

## Special Diagnostic Scenarios

### Scenario: High brand awareness lift, but low purchases

**Diagnosis:** Marketing did its job (built awareness), but product/market fit issue

**This suggests:**
- Messaging is working (people remember you)
- Product or offer isn't compelling enough to convert
- Price too high for perceived value
- Product quality concerns
- Availability issues

**This is a PRODUCT/OPERATIONS problem**

**Actions:**
- Product market research
- Competitive analysis on pricing/features
- Review customer feedback
- Test promotional offers
- Audit product quality

---

### Scenario: Traffic and conversion normal, but revenue down

**Diagnosis:** Average order value (AOV) is declining

**Check:**
- Are higher-priced items out of stock?
- Has product mix shifted to lower-priced items?
- Are discount codes being overused?
- Has repeat purchase rate declined?

**This is usually OPERATIONS (inventory/merchandising)**

**Actions:**
- Inventory analysis
- Promote higher-value items
- Create bundles
- Audit discounting strategy
- Review merchandising

---

### Scenario: Everything looks good but revenue still down

**Diagnosis:** Check if the problem is in attribution or measurement

**Investigate:**
- Attribution window changes
- Tracking implementation issues
- Platform reporting discrepancies
- Offline/online mix shifting

**This is a MEASUREMENT problem**

**Actions:**
- Audit tracking implementation
- Reconcile revenue across systems
- Check cookie/pixel firing
- Review attribution model

---

## Complex Diagnosis: Both Marketing & Operations

### Signals that it's both:
- Traffic is down **AND** conversion is down
- Some channels performing well, others poorly **AND** overall conversion declining
- New customer acquisition fine, but repeat purchase rate down

### Approach:
1. Fix the bigger problem first (usually operations if conversion is broken)
2. Can't fix traffic issues if site doesn't convert
3. Prioritize based on impact magnitude

### Example:
```
Traffic down 20% (Marketing)
Conversion down 30% (Operations)

Fix order:
1. Fix operations (conversion) first - biggest impact
2. Then increase traffic - will see full benefit once conversion fixed
```

---

## Diagnostic Output Template

### Problem Statement
[Clear description of what's not working]

### Data Summary
- Traffic: [trend]
- Conversion by stage: [metrics]
- Key anomalies: [findings]

### Diagnosis
**Primary Issue:** [Marketing / Operations / Both]
**Confidence Level:** [High / Medium / Low]

**Evidence:**
- [Supporting data point 1]
- [Supporting data point 2]
- [Supporting data point 3]

### Root Cause Hypothesis
[Specific theory about what's causing the problem]

### Recommended Actions
1. [Immediate action - fix the critical issue]
2. [Short-term - address contributing factors]
3. [Long-term - prevent recurrence]

### What to Measure
[Specific metrics to track to validate diagnosis and measure improvement]

### Timeline
[Expected timeline to see improvement]

---

## Red Flags by Category

### Marketing Red Flags
- CTR declining across channels
- CPM/CPC increasing significantly
- Ad relevance scores dropping
- Brand search volume declining
- Competitive share of voice shrinking
- Audience saturation (frequency >5)

### Operations Red Flags
- Site speed deteriorating
- Mobile performance issues
- Checkout error rate increasing
- Customer service tickets spiking
- Delivery time complaints
- Product return rate increasing
- Inventory turnover slowing

### Market/External Red Flags
- Competitor launches
- Category-wide trends
- Economic indicators
- Platform algorithm changes
- Seasonal patterns
- Supply chain disruptions

---

## Prevention: Early Warning System

**Set up alerts for:**
- Conversion rate drop >10% week-over-week
- Traffic drop >15% week-over-week (excluding expected seasonality)
- ROAS decline >20% week-over-week
- Cart abandonment rate increase >10%
- Site error rate increase
- Customer service ticket spike

**Monitor leading indicators:**
- Ad performance trends
- Site performance metrics
- Inventory levels
- Competitive activity
- Customer feedback sentiment

**Regular health checks:**
- Weekly: Funnel performance review
- Monthly: Full diagnostic if metrics off track
- Quarterly: Comprehensive audit even if performing well
