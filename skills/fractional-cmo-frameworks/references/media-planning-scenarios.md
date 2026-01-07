# Media Planning Scenarios

Framework for evaluating channels and building media plans with scenario-based projections.

## Scenario Modeling Framework

For every channel consideration, model three scenarios to show range of possibilities and help stakeholders understand risk/reward tradeoffs.

### Three-Scenario Approach

**Conservative:**
- Higher CPMs (premium placements, guaranteed delivery)
- Lower performance assumptions
- Minimum expected outcome
- Lowest risk

**Moderate:**
- Mid-range CPMs
- Historical benchmark performance
- Most likely outcome
- Balanced risk/reward

**Aggressive:**
- Lower CPMs (programmatic, auction-based)
- Optimistic performance assumptions
- Best-case outcome
- Higher optimization required

## Calculation Method

### Step 1: Determine Budget
Start with allocated spend for the channel: **$X,XXX**

### Step 2: CPM Assumptions
Research typical CPMs for your audience on this channel:
- Check platform rate cards
- Review historical performance
- Factor in audience specificity (more targeting = higher CPM)

**Example CPM Ranges by Channel:**
- YouTube: $3-8
- Spotify Audio: $18-28
- Hulu/Disney+: $25-34
- Podcast (Programmatic): $20-32
- Podcast (Host-read): $32-50+

### Step 3: Calculate Impressions
```
Impressions = (Budget / CPM) × 1,000
```

**Example:** $9,100 budget ÷ $8 CPM = 1,137,500 impressions

### Step 4: Impression-to-Visit Rate
Apply channel-specific conversion assumptions:

**Typical Ranges:**
- YouTube (clickable): 1.0-1.5%
- Podcast: 1.5-2.0%
- Spotify: 0.5-0.7%
- Display/Video: 0.3-0.5%
- Social: 0.5-1.0%

**Factors affecting rate:**
- Creative quality
- Offer strength
- Audience targeting precision
- Channel engagement level

```
Visits = Impressions × (Imp-to-Visit %)
```

### Step 5: Visit-to-Purchase Rate
Apply your historical conversion rate or industry benchmarks:

**Typical E-commerce Rates:**
- D2C brands: 2-4%
- High-ticket items: 0.5-2%
- Impulse purchases: 3-6%

```
Purchases = Visits × (Conversion %)
```

### Step 6: Revenue Projection
```
Revenue = Purchases × AOV (Average Order Value)
```

### Step 7: Calculate ROAS
```
ROAS = Revenue ÷ Budget
```

## Channel-Specific Examples

### YouTube

| Scenario | CPM | Budget | Impressions | Visits (1%) | Purchases (3.4%) | Revenue | ROAS |
|----------|-----|--------|-------------|-------------|------------------|---------|------|
| Conservative | $8 | $9,100 | 1,138,500 | 11,385 | 389 | $28,559 | 3.1x |
| Moderate | $5 | $9,100 | 1,821,600 | 18,216 | 623 | $45,697 | 5.0x |
| Aggressive | $3 | $9,100 | 3,036,000 | 30,360 | 1,038 | $76,137 | 8.4x |

**Strategic Note:** YouTube does heavy lifting due to clickable format. Direct response capability drives higher visit rates.

**AOV Assumption:** $73.40

### Podcast (Vox Network)

| Scenario | CPM | Budget | Impressions | Visits (1.5%) | Purchases (3.4%) | Revenue | ROAS |
|----------|-----|--------|-------------|---------------|------------------|---------|------|
| Programmatic | $20 | $9,100 | 455,400 | 6,831 | 234 | $17,164 | 1.9x |
| Mixed 60/40 | $26 | $9,100 | 350,308 | 5,255 | 180 | $13,203 | 1.5x |
| Host-Read | $32 | $9,100 | 284,625 | 4,269 | 146 | $10,709 | 1.2x |

**Strategic Note:** Endorsement effect from host-read doesn't show up directly in imp-to-visit rates but may drive higher consideration and repeat purchases. Consider brand lift measurement.

### Spotify

| Scenario | CPM | Budget | Impressions | Visits (0.7%) | Purchases (3.4%) | Revenue | ROAS |
|----------|-----|--------|-------------|---------------|------------------|---------|------|
| Video Focus | $28 | $9,100 | 325,286 | 2,277 | 78 | $5,721 | 0.6x |
| Audio + Video | $22 | $9,100 | 414,000 | 2,898 | 99 | $7,262 | 0.8x |
| Audio Focus | $18 | $9,100 | 506,000 | 3,542 | 121 | $8,875 | 1.0x |

**Strategic Note:** Audio typically more cost-effective but requires strong audio creative. Video commands premium but may drive higher brand recall.

### Disney+/Hulu

| Scenario | CPM | Budget | Impressions | Visits (0.4%) | Purchases (3.4%) | Revenue | ROAS |
|----------|-----|--------|-------------|---------------|------------------|---------|------|
| Disney+ Focus | $34 | $9,100 | 267,882 | 1,072 | 37 | $2,714 | 0.3x |
| Mix 70/30 | $28 | $9,100 | 325,286 | 1,391 | 44 | $3,227 | 0.4x |
| Hulu Only | $25 | $9,100 | 364,320 | 1,457 | 50 | $3,668 | 0.4x |

**Strategic Note:** Non-skippable premium content. Better for brand building than direct response. Consider lift measurement vs direct attribution.

## Building a Complete Media Plan

### Step 1: Allocate Total Budget by Funnel Stage

**Example $50k quarterly budget:**
- Awareness (40%): $20k → YouTube, Podcast, Display
- Consideration (30%): $15k → Social, Content, Influencer
- Conversion (30%): $15k → Search, Retargeting, Email

### Step 2: Allocate Within Each Stage

**Awareness ($20k):**
- YouTube: $9k
- Podcast: $6k
- Spotify: $5k

### Step 3: Model Each Channel
Run 3-scenario analysis for each allocation.

### Step 4: Create Portfolio View

| Channel | Budget | Conservative Rev | Moderate Rev | Aggressive Rev |
|---------|--------|------------------|--------------|----------------|
| YouTube | $9k | $28k | $46k | $76k |
| Podcast | $6k | $7k | $9k | $11k |
| Spotify | $5k | $4k | $5k | $6k |
| **Total** | **$20k** | **$39k** | **$60k** | **$93k** |

**Portfolio ROAS Range:** 1.95x - 4.65x

### Step 5: Recommend Mix
Based on:
- Risk tolerance
- Historical performance
- Strategic priorities (brand vs performance)
- Testing capacity

## Channel Evaluation Criteria

When deciding which channels to include:

**1. Audience Alignment**
- Does our target audience use this channel heavily?
- What's the usage index vs general population?

**2. Format Suitability**
- Does our message work in this format?
- Do we have appropriate creative assets?

**3. Attribution Capability**
- Can we measure results?
- Is measurement direct or via lift studies?

**4. Budget Efficiency**
- What's the minimum viable spend?
- Can we achieve meaningful reach?

**5. Strategic Fit**
- Brand building or performance?
- Awareness or conversion?
- Where in customer journey?

## Advanced Techniques

### Incremental Lift Testing
For channels where direct attribution is difficult (e.g., podcast, TV, OOH):

1. Split test markets into exposed vs control
2. Measure lift in brand searches, site visits, or sales
3. Calculate incremental value beyond baseline

### Mix Modeling
For ongoing optimization:
- Track performance weekly
- Adjust allocation toward winning channels
- Maintain testing budget (10-20%) for new channels
- Reforecast based on actual results

### Sequential Strategy
Build campaigns that leverage channel strengths:
1. **Awareness** → YouTube, Podcast to build consideration
2. **Retargeting** → Social, Display to those exposed
3. **Conversion** → Search, Email to close

## Presentation Tips

**For C-Suite:**
- Lead with portfolio ROAS range
- Show total projected revenue by scenario
- Highlight key strategic choices (risk vs reward)
- Tie to business objectives

**For Operators:**
- Provide detailed assumptions
- Include CPM sources
- Document testing roadmap
- Specify success metrics

**Always Include:**
- Assumption documentation
- Performance benchmarks
- Optimization triggers ("if ROAS < X, then...")
- Measurement approach
