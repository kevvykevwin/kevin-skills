#!/usr/bin/env python3
"""
Report Builder for GEO SEO Agent

Compiles audit results into final markdown report.

Usage:
    python report_builder.py --data audit_data.json --output report.md
"""

import argparse
import json
from datetime import datetime

# Score calculation weights - used to compute weighted averages across categories
# Content scoring weights (lines 28-32)
WEIGHT_ANSWER_CAPSULE = 0.35  # Most critical for AI extraction
WEIGHT_STRUCTURE = 0.25       # Clear hierarchy helps parsing
WEIGHT_ENTITY_CLARITY = 0.20  # Entity recognition importance
WEIGHT_FAQ_HOWTO = 0.20       # Structured Q&A content

# Citation scoring weights (line 41)
WEIGHT_CHATGPT_CITATION = 0.6   # ChatGPT has higher market share
WEIGHT_GOOGLE_AIO_CITATION = 0.4

# Overall score weights (lines 44-48)
WEIGHT_TECHNICAL = 0.25      # Foundation for AI accessibility
WEIGHT_CONTENT = 0.30        # Highest impact on citations
WEIGHT_PRESENCE = 0.20       # Third-party validation
WEIGHT_CITATION = 0.25       # Direct measure of success


def calculate_overall_scores(data: dict) -> dict:
    """Calculate weighted overall scores from component scores."""
    
    technical = data.get('technical_scores', {})
    content = data.get('content_scores', {})
    presence = data.get('presence_scores', {})
    citation = data.get('citation_scores', {})
    
    # Technical score (already calculated in technical_audit.py)
    tech_overall = technical.get('overall', 0)
    
    # Content score
    content_overall = (
        content.get('answer_capsule', 0) * WEIGHT_ANSWER_CAPSULE +
        content.get('structure', 0) * WEIGHT_STRUCTURE +
        content.get('entity_clarity', 0) * WEIGHT_ENTITY_CLARITY +
        content.get('faq_howto', 0) * WEIGHT_FAQ_HOWTO
    )

    # Presence score (direct)
    presence_overall = presence.get('overall', 0)

    # Citation score (from metrics)
    chatgpt_rate = citation.get('chatgpt', {}).get('citation_rate', 0)
    google_rate = citation.get('google_aio', {}).get('citation_rate', 0)
    citation_overall = (chatgpt_rate * WEIGHT_CHATGPT_CITATION + google_rate * WEIGHT_GOOGLE_AIO_CITATION)

    # Weighted composite
    overall = (
        tech_overall * WEIGHT_TECHNICAL +
        content_overall * WEIGHT_CONTENT +
        presence_overall * WEIGHT_PRESENCE +
        citation_overall * WEIGHT_CITATION
    )
    
    return {
        'technical': tech_overall,
        'content': content_overall,
        'presence': presence_overall,
        'citation': citation_overall,
        'overall': overall
    }


def score_to_grade(score: float) -> str:
    """Convert numeric score to letter grade."""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B+'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C+'
    elif score >= 50:
        return 'C'
    elif score >= 40:
        return 'D'
    else:
        return 'F'


def score_to_status(score: float) -> str:
    """Convert numeric score to status indicator."""
    if score >= 70:
        return '🟢 Good'
    elif score >= 50:
        return '🟡 Needs Work'
    else:
        return '🔴 Critical'


def generate_executive_summary(data: dict, scores: dict) -> str:
    """Generate executive summary paragraph."""
    
    brand = data.get('brand', 'This brand')
    overall = scores['overall']
    
    if overall >= 70:
        status = "has a solid foundation for AI visibility"
        focus = "optimization and growth"
    elif overall >= 50:
        status = "has moderate AI visibility with significant room for improvement"
        focus = "addressing content gaps and building third-party presence"
    else:
        status = "has limited AI visibility and requires foundational work"
        focus = "technical fixes and establishing baseline presence"
    
    # Find biggest gap
    score_items = [
        ('technical infrastructure', scores['technical']),
        ('content structure', scores['content']),
        ('third-party presence', scores['presence']),
        ('AI citation rate', scores['citation'])
    ]
    weakest = min(score_items, key=lambda x: x[1])
    strongest = max(score_items, key=lambda x: x[1])
    
    summary = f"{brand} {status}. "
    summary += f"The primary focus should be on {focus}. "
    summary += f"Current strongest area is {strongest[0]} ({strongest[1]:.0f}/100). "
    summary += f"Biggest opportunity is in {weakest[0]} ({weakest[1]:.0f}/100)."
    
    return summary


def generate_recommendations(data: dict, scores: dict) -> dict:
    """Generate prioritized recommendations."""
    
    critical = []
    quick_wins = []
    strategic = []
    
    # Technical recommendations
    tech = data.get('technical_scores', {})
    if tech.get('crawler_access', 0) < 80:
        critical.append({
            'title': 'Fix Crawler Access',
            'description': 'Update robots.txt to allow GPTBot and Bingbot',
            'impact': 'High',
            'effort': 'Low'
        })

    if tech.get('schema', 0) < 60:
        quick_wins.append({
            'title': 'Implement Schema Markup',
            'description': 'Add Organization schema to homepage, Product/Article schema to key pages',
            'impact': 'High',
            'effort': 'Medium'
        })

    if tech.get('js_rendering', 0) < 60:
        critical.append({
            'title': 'Address JavaScript Rendering',
            'description': 'Implement server-side rendering or ensure key content in raw HTML',
            'impact': 'High',
            'effort': 'High'
        })

    # Content recommendations
    content = data.get('content_scores', {})
    if content.get('answer_capsule', 0) < 60:
        quick_wins.append({
            'title': 'Add Answer Capsules',
            'description': 'Add clear, extractable definitions/answers to first paragraph of key pages',
            'impact': 'High',
            'effort': 'Low'
        })

    if content.get('faq_howto', 0) < 60:
        strategic.append({
            'title': 'Create FAQ Content',
            'description': 'Build FAQ page targeting "People Also Ask" queries with FAQPage schema',
            'impact': 'Medium',
            'effort': 'Medium'
        })
    
    # Presence recommendations
    presence = data.get('presence_scores', {})
    presence_gaps = data.get('presence_gaps', [])

    if presence.get('overall', 0) < 60:
        # Safely handle potentially empty list
        if presence_gaps:
            for platform in presence_gaps[:2]:  # Top 2 gaps
                strategic.append({
                    'title': f'Build Presence on {platform}',
                    'description': f'Establish active presence on {platform} where competitors are visible',
                    'impact': 'Medium',
                    'effort': 'Medium'
                })
    
    # Citation recommendations
    citation = data.get('citation_scores', {})
    if citation.get('chatgpt', {}).get('citation_rate', 0) < 50:
        strategic.append({
            'title': 'Improve ChatGPT Visibility',
            'description': 'Focus on category and comparison content; build presence on sites ChatGPT cites',
            'impact': 'High',
            'effort': 'High'
        })
    
    return {
        'critical': critical,
        'quick_wins': quick_wins,
        'strategic': strategic
    }


def build_report(data: dict) -> str:
    """Build full markdown report from audit data."""
    
    scores = calculate_overall_scores(data)
    recommendations = generate_recommendations(data, scores)
    summary = generate_executive_summary(data, scores)
    
    brand = data.get('brand', 'Unknown Brand')
    domain = data.get('domain', 'unknown.com')
    client_type = data.get('client_type', 'D2C')
    date = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""# GEO Audit Report: {brand}

**Domain:** {domain}
**Date:** {date}
**Client Type:** {client_type}
**Overall Grade:** {score_to_grade(scores['overall'])} ({scores['overall']:.0f}/100)

---

## Executive Summary

{summary}

---

## Scores Overview

| Category | Score | Status |
|----------|-------|--------|
| Technical Accessibility | {scores['technical']:.0f}/100 | {score_to_status(scores['technical'])} |
| Content Structure | {scores['content']:.0f}/100 | {score_to_status(scores['content'])} |
| Third-Party Presence | {scores['presence']:.0f}/100 | {score_to_status(scores['presence'])} |
| AI Citation Rate | {scores['citation']:.0f}/100 | {score_to_status(scores['citation'])} |
| **Overall** | **{scores['overall']:.0f}/100** | **{score_to_status(scores['overall'])}** |

---

## Critical Issues (Fix First)

"""
    
    if recommendations['critical']:
        for rec in recommendations['critical']:
            report += f"""### 🚨 {rec['title']}

{rec['description']}

- **Impact:** {rec['impact']}
- **Effort:** {rec['effort']}

"""
    else:
        report += "_No critical issues identified._\n\n"
    
    report += """---

## Quick Wins (High Impact, Low Effort)

"""
    
    if recommendations['quick_wins']:
        for rec in recommendations['quick_wins']:
            report += f"""### ⚡ {rec['title']}

{rec['description']}

- **Impact:** {rec['impact']}
- **Effort:** {rec['effort']}

"""
    else:
        report += "_No quick wins identified - foundation is solid._\n\n"
    
    report += """---

## Strategic Recommendations (Medium-Term)

"""
    
    if recommendations['strategic']:
        for rec in recommendations['strategic']:
            report += f"""### 📈 {rec['title']}

{rec['description']}

- **Impact:** {rec['impact']}
- **Effort:** {rec['effort']}

"""
    else:
        report += "_Focus on quick wins before strategic initiatives._\n\n"
    
    # Add detailed scores section
    report += """---

## Detailed Scores

### Technical Audit

"""
    
    tech = data.get('technical_scores', {})
    for key, value in tech.items():
        if key != 'overall':
            report += f"- **{key.replace('_', ' ').title()}:** {value}/100\n"
    
    report += """
### Content Analysis

"""
    
    content = data.get('content_scores', {})
    for key, value in content.items():
        report += f"- **{key.replace('_', ' ').title()}:** {value}/100\n"
    
    report += """
### Third-Party Presence

"""
    
    presence = data.get('presence_details') or {}
    for platform, details in presence.items():
        if not isinstance(details, dict):
            details = {}
        status = '✅' if details.get('present') else '❌'
        report += f"- **{platform}:** {status} "
        if details.get('notes'):
            report += f"- {details['notes']}"
        report += "\n"
    
    report += """
### AI Citation Results

"""
    
    citation = data.get('citation_scores', {})
    chatgpt = citation.get('chatgpt', {})
    google = citation.get('google_aio', {})
    
    report += f"""**ChatGPT:**
- Citation Rate: {chatgpt.get('citation_rate', 0):.1f}%
- Average Score: {chatgpt.get('avg_score', 0):.2f}/5

**Google AI Overview:**
- Citation Rate: {google.get('citation_rate', 0):.1f}%
- Average Score: {google.get('avg_score', 0):.2f}/5

"""
    
    # Monitoring setup section
    report += """---

## Monitoring Setup

### Recommended Test Prompts (Weekly)

"""
    
    monitoring_prompts = data.get('monitoring_prompts', [])
    if monitoring_prompts:
        for i, prompt in enumerate(monitoring_prompts[:15], 1):
            report += f"{i}. {prompt}\n"
    else:
        report += "_Generate test prompts using citation_tester.py_\n"
    
    report += """
### Analytics Configuration

Add these referrer segments in Google Analytics 4:
- `chat.openai.com`
- `chatgpt.com`
- `perplexity.ai`
- `gemini.google.com`

Track:
- Sessions from AI referrers
- Conversion rate comparison (AI vs organic)
- Landing pages receiving AI traffic

### Alert Thresholds

Set alerts for:
- Citation rate drops > 20% week-over-week
- Loss of citation in monitored prompts
- New competitor appearing in category queries

---

## Next Steps

1. Address any critical issues immediately
2. Implement quick wins this week
3. Schedule strategic initiatives for next 30-90 days
4. Set up monitoring and run first baseline test
5. Review results in 4 weeks

---

_Report generated by GEO SEO Agent_
_For questions or updates, contact [auditor]_
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Build GEO audit report')
    parser.add_argument('--data', '-d', required=True, help='Audit data JSON file')
    parser.add_argument('--output', '-o', help='Output markdown file')

    args = parser.parse_args()

    # Read input data with error handling
    try:
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found: {args.data}")
        return 1
    except PermissionError:
        print(f"Error: Permission denied reading: {args.data}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.data}: {e}")
        return 1

    report = build_report(data)

    # Write output with error handling
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report written to: {args.output}")
        except PermissionError:
            print(f"Error: Permission denied writing to: {args.output}")
            return 1
        except OSError as e:
            print(f"Error: Failed to write {args.output}: {e}")
            return 1
    else:
        print(report)

    return 0


if __name__ == '__main__':
    exit(main())
