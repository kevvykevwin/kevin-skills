---
name: humanizer-copy
version: 1.0.0
description: |
  Review and improve marketing copy by removing AI-isms while preserving persuasive intent.
  Adapted from the humanizer skill for copywriting contexts. Focuses on specificity,
  rhythm, filler removal, and converting vague claims into concrete proof points.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer for Copy: AI Pattern Removal for Marketing

Review marketing copy to remove AI-generated patterns while keeping persuasive power. Unlike general humanization, promotional language is often appropriate here — the goal is authentic promotion, not neutrality.

## Core Principle

Bad AI copy is vague, hedged, and rhythmically flat.
Good copy is specific, confident, and has pulse.

---

## WHAT TO FIX

### 1. Vague Claims → Concrete Proof

The #1 AI copy problem. Unsubstantiated claims destroy credibility.

**Before:**
> Trusted by thousands of companies worldwide. Industry experts agree it's the leading solution.

**After:**
> Used by 2,400 companies including Stripe, Notion, and Airbnb. Rated #1 in G2's 2025 automation category.

**Rule:** Every claim needs a number, name, or source.

---

### 2. Filler Phrases → Direct Statements

AI pads sentences. Cut ruthlessly.

| Kill this | Write this |
|-----------|------------|
| In order to | To |
| Due to the fact that | Because |
| Has the ability to | Can |
| It is important to note that | [Delete entirely] |
| At this point in time | Now |
| In the event that | If |
| Provides you with the ability to | Lets you |
| A wide range of | Many |
| On a daily basis | Daily |

---

### 3. False Ranges → Real Scope

AI loves "from X to Y" where X and Y mean nothing together.

**Before:**
> From startups to enterprises, from marketing to engineering, our platform scales with your needs.

**After:**
> Works for 5-person teams and 5,000-person orgs. Marketing, sales, and engineering templates included.

**Rule:** If you can't put X and Y on an actual spectrum, don't use "from...to."

---

### 4. Generic Conclusions → Concrete CTAs

AI endings are vague and upbeat. CTAs should be specific and actionable.

**Before:**
> The future of productivity is here. Take your workflow to the next level and unlock your team's potential today.

**After:**
> Free 14-day trial. No credit card. Takes 3 minutes to set up.

**Before:**
> Join thousands of satisfied customers on their journey to success.

**After:**
> 2,400 teams signed up last month. Start free →

---

### 5. Sycophantic Tone → Confident Statement

AI oversells emotions. Let benefits speak.

**Before:**
> You're going to absolutely love how easy this is! We're so excited to help you succeed!

**After:**
> Setup takes 3 minutes. Most teams see results in the first week.

**Rule:** Delete exclamation points. State facts. Trust the reader.

---

### 6. Hedge Words → Committed Claims

AI over-qualifies. Copy needs confidence.

**Before:**
> This could potentially help improve your workflow and may possibly increase productivity.

**After:**
> Cuts reporting time by 40%.

**Hedge words to cut:** potentially, possibly, might, may, could, somewhat, arguably, tends to, in some cases

**Exception:** Keep hedges for legally required disclaimers.

---

### 7. Flat Rhythm → Varied Cadence

AI writes metronomic sentences. Mix it up.

**Before (robotic):**
> Our platform offers powerful features. The dashboard shows real-time analytics. Teams can collaborate seamlessly. Reports are generated automatically.

**After (has pulse):**
> Real-time analytics. Automatic reports. And a dashboard your whole team will actually use — no training required.

**Techniques:**
- Fragment sentences for punch
- Use "and" to create flow
- Vary length dramatically
- End paragraphs on short notes

---

### 8. Abstract Benefits → Sensory Specifics

AI speaks in abstractions. Good copy creates mental images.

**Before:**
> Streamline your workflow and enhance productivity with our innovative solution.

**After:**
> Close your 47 open tabs. Everything's in one place now.

**Before:**
> Achieve better results with less effort.

**After:**
> Write the brief Monday morning. See three ad variants by lunch.

---

## WHAT TO KEEP (Or Use Deliberately)

Unlike neutral writing, copy can use these patterns intentionally:

### Promotional Language — ALLOWED
Words like "powerful," "seamless," "beautiful" are fine IF backed by specifics.

**Bad:** Powerful features for modern teams.
**Good:** Powerful enough to handle 10M events/day. Stripe and Linear use it in production.

### Rule of Three — USE SPARINGLY
Triads work in copy when items are genuinely parallel.

**Good:** Fast. Reliable. Free.
**Bad:** Innovative, transformative, and industry-leading.

### Em Dashes — USE FOR PUNCH
One per paragraph max. For emphasis or pivot.

**Good:** Everything you need — nothing you don't.
**Bad:** Our platform — which integrates with Slack — provides real-time — and accurate — analytics.

---

## VOICE AND SOUL

Clean copy isn't enough. It needs personality.

### Signs of soulless copy:
- Every sentence same length
- No perspective or opinion
- Reads like it could be any company
- Safe, forgettable, interchangeable

### How to add voice:

**Have a point of view.**
> Not: "Project management for modern teams"
> But: "Spreadsheets are where projects go to die. This isn't a spreadsheet."

**Acknowledge the reader's reality.**
> Not: "Boost your productivity"
> But: "You've got 6 hours of meetings today. Let's make the other 2 count."

**Be specific about pain.**
> Not: "Simplify your workflow"
> But: "Stop asking 'which Slack channel was that in?'"

**Let some mess in.**
> Overly polished = obviously AI. A little roughness = human.

---

## PROCESS

1. **Read aloud** — Does it sound like a person? Or a press release?
2. **Check every claim** — Number, name, or source?
3. **Cut filler** — Read each sentence. Delete words until it breaks.
4. **Fix rhythm** — Vary sentence length. Add fragments. Remove parallel structure monotony.
5. **Strengthen CTA** — Specific action + specific outcome + specific timeframe
6. **Add one opinion** — What does this brand actually believe?

---

## OUTPUT FORMAT

Provide:
1. Revised copy
2. Brief change summary (what was cut/added)

---

## EXAMPLES

### Landing Page Hero

**Before:**
> Welcome to the future of team collaboration. Our innovative platform provides a seamless, intuitive, and powerful experience that helps teams of all sizes work together more effectively. Join thousands of satisfied customers who have transformed their workflows and unlock your team's true potential today.

**After:**
> Finally, a project tool your team will actually open.
>
> Linear is where 10,000 product teams plan, track, and ship. Not another app to check — the app that replaces five others.
>
> Free for teams up to 10. Setup takes 4 minutes.

**Changes:**
- Cut "welcome to the future" (generic)
- Cut "seamless, intuitive, powerful" (vague triad)
- Cut "teams of all sizes" (false range)
- Added specific number (10,000 teams)
- Added specific benefit (replaces five apps)
- Added concrete CTA (free, 10 users, 4 minutes)

---

### Email Subject Line

**Before:**
> Unlock Your Potential: Discover How Our Platform Can Transform Your Workflow Today!

**After:**
> Your Monday just got 2 hours shorter

**Changes:**
- Cut "unlock potential" (cliche)
- Cut "discover how" (filler)
- Cut exclamation (sycophantic)
- Added specific benefit (2 hours)
- Lowercase = feels personal

---

### Feature Description

**Before:**
> Our advanced analytics dashboard provides comprehensive insights that empower teams to make data-driven decisions. With real-time monitoring capabilities and customizable reports, you'll have everything you need to optimize performance and drive results.

**After:**
> See what's working. Fix what isn't.
>
> The dashboard updates every 30 seconds. Filter by campaign, channel, or date range. Export to CSV or schedule weekly emails to your team.

**Changes:**
- Cut "comprehensive insights" and "empower" (vague)
- Cut "data-driven decisions" (cliche)
- Added specific refresh rate (30 seconds)
- Listed actual features (filter, export, schedule)
- Short opener with parallel structure

---

## REFERENCE

Adapted from [humanizer](https://github.com/blader/humanizer) and Wikipedia's "Signs of AI writing" guide, modified for marketing contexts where persuasion is the goal.
