#!/usr/bin/env python3
"""
Technical Audit Script for GEO SEO Agent

Checks:
- robots.txt crawler access
- Schema markup detection
- Basic page structure analysis
- llms.txt presence
- Sitemap validation

Usage:
    python technical_audit.py https://example.com

Output:
    JSON results to stdout, or specify --output file.json
"""

import argparse
import json
import re
import sys
from urllib.parse import urlparse
from datetime import datetime

# For actual implementation, these would use requests/httpx
# This script is designed to be run with Claude Code which has web_fetch

# Constants
MIN_WORD_COUNT_THRESHOLD = 200
MIN_SITEMAP_URL_COUNT = 10
CRAWLER_ACCESS_WEIGHT = 0.30
SCHEMA_WEIGHT = 0.30
JS_RENDERING_WEIGHT = 0.25
SITEMAP_WEIGHT = 0.10
LLMS_TXT_WEIGHT = 0.05


def parse_robots_txt(content: str) -> dict:
    """Parse robots.txt content and extract bot permissions."""
    
    bots_to_check = [
        'GPTBot',
        'Bingbot', 
        'Googlebot',
        'Google-Extended',
        'PerplexityBot',
        'ClaudeBot',
        'Anthropic-ai',
        '*'  # Catch-all
    ]
    
    results = {}
    current_agent = None
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
            
        # Parse User-agent
        if line.lower().startswith('user-agent:'):
            agent = line.split(':', 1)[1].strip()
            current_agent = agent
            if agent not in results:
                results[agent] = {'disallow': [], 'allow': []}
                
        # Parse Disallow
        elif line.lower().startswith('disallow:') and current_agent:
            path = line.split(':', 1)[1].strip()
            if path:
                results[current_agent]['disallow'].append(path)
                
        # Parse Allow
        elif line.lower().startswith('allow:') and current_agent:
            path = line.split(':', 1)[1].strip()
            if path:
                results[current_agent]['allow'].append(path)
    
    # Determine status for each bot we care about
    bot_status = {}
    
    for bot in bots_to_check:
        if bot == '*':
            continue
            
        # Check specific bot rules first, then fall back to *
        rules = results.get(bot, results.get('*', {'disallow': [], 'allow': []}))
        
        # If disallow: / exists, bot is blocked
        if '/' in rules['disallow']:
            bot_status[bot] = 'blocked'
        elif rules['disallow']:
            bot_status[bot] = 'partial'
        else:
            bot_status[bot] = 'allowed'
    
    return {
        'raw_rules': results,
        'bot_status': bot_status
    }


def detect_schema(html_content: str) -> dict:
    """Detect JSON-LD schema markup in HTML."""

    schema_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    matches = re.findall(schema_pattern, html_content, re.DOTALL | re.IGNORECASE)

    schemas = []
    schema_types = []
    parse_errors = 0

    for match in matches:
        try:
            data = json.loads(match.strip())
            schemas.append(data)

            # Extract @type
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and '@type' in item:
                        schema_types.append(item['@type'])
            elif isinstance(data, dict) and '@type' in data:
                schema_types.append(data['@type'])

        except (json.JSONDecodeError, ValueError):
            parse_errors += 1
            continue

    return {
        'found': len(schemas) > 0,
        'count': len(schemas),
        'types': list(set(schema_types)),
        'schemas': schemas,
        'parse_errors': parse_errors
    }


def analyze_content_structure(html_content: str) -> dict:
    """Analyze HTML structure for AI readability."""
    
    # Check for headings
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL | re.IGNORECASE)
    h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', html_content, re.DOTALL | re.IGNORECASE)
    h3_matches = re.findall(r'<h3[^>]*>(.*?)</h3>', html_content, re.DOTALL | re.IGNORECASE)
    
    # Check for main content areas
    has_main = bool(re.search(r'<main[^>]*>', html_content, re.IGNORECASE))
    has_article = bool(re.search(r'<article[^>]*>', html_content, re.IGNORECASE))
    
    # Check for JS framework indicators
    js_framework_indicators = {
        'react': bool(re.search(r'data-reactroot|_react|__NEXT_DATA__', html_content)),
        'vue': bool(re.search(r'data-v-|__NUXT__', html_content)),
        'angular': bool(re.search(r'ng-version|_nghost', html_content)),
    }
    
    # Check if content appears to be JS-rendered (empty main tags, loading states)
    empty_main = bool(re.search(r'<main[^>]*>\s*</main>', html_content, re.IGNORECASE))
    loading_indicators = bool(re.search(r'loading\.\.\.|spinner|skeleton', html_content, re.IGNORECASE))
    
    # Estimate content visibility in raw HTML
    # Strip tags and check content length
    text_content = re.sub(r'<[^>]+>', ' ', html_content)
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    word_count = len(text_content.split())
    
    return {
        'headings': {
            'h1_count': len(h1_matches),
            'h2_count': len(h2_matches),
            'h3_count': len(h3_matches),
            'h1_text': [re.sub(r'<[^>]+>', '', h).strip() for h in h1_matches[:3]]
        },
        'semantic_elements': {
            'has_main': has_main,
            'has_article': has_article
        },
        'js_framework': js_framework_indicators,
        'js_rendering_risk': {
            'empty_main': empty_main,
            'loading_indicators': loading_indicators,
            'low_content': word_count < MIN_WORD_COUNT_THRESHOLD
        },
        'content_stats': {
            'word_count_estimate': word_count
        }
    }


def check_sitemap(sitemap_content: str) -> dict:
    """Validate sitemap XML structure."""
    
    if not sitemap_content:
        return {'valid': False, 'error': 'Empty or missing sitemap'}
    
    # Check for sitemap index vs urlset
    is_index = '<sitemapindex' in sitemap_content.lower()
    is_urlset = '<urlset' in sitemap_content.lower()
    
    if not (is_index or is_urlset):
        return {'valid': False, 'error': 'Not a valid sitemap format'}
    
    # Count URLs
    url_count = len(re.findall(r'<loc>', sitemap_content, re.IGNORECASE))
    
    # Check for lastmod dates
    lastmod_matches = re.findall(r'<lastmod>(.*?)</lastmod>', sitemap_content, re.IGNORECASE)
    
    # Find most recent lastmod
    most_recent = None
    for date_str in lastmod_matches:
        try:
            # Handle various date formats
            date_str = date_str.strip()[:10]  # Get YYYY-MM-DD portion
            if most_recent is None or date_str > most_recent:
                most_recent = date_str
        except Exception:
            continue
    
    return {
        'valid': True,
        'type': 'index' if is_index else 'urlset',
        'url_count': url_count,
        'has_lastmod': len(lastmod_matches) > 0,
        'most_recent_lastmod': most_recent
    }


def calculate_scores(results: dict) -> dict:
    """Calculate scores based on audit results."""
    
    scores = {}
    
    # Crawler Access Score
    bot_status = results.get('robots', {}).get('bot_status', {})
    critical_bots = ['Googlebot', 'Bingbot']
    ai_bots = ['GPTBot', 'PerplexityBot', 'ClaudeBot']
    
    blocked_critical = sum(1 for b in critical_bots if bot_status.get(b) == 'blocked')
    blocked_ai = sum(1 for b in ai_bots if bot_status.get(b) == 'blocked')
    
    if blocked_critical >= 2:
        scores['crawler_access'] = 0
    elif blocked_critical == 1:
        scores['crawler_access'] = 20
    elif bot_status.get('Bingbot') == 'blocked':
        scores['crawler_access'] = 40
    elif blocked_ai >= 2:
        scores['crawler_access'] = 60
    elif blocked_ai == 1:
        scores['crawler_access'] = 80
    else:
        scores['crawler_access'] = 100
    
    # Schema Score
    schema = results.get('schema', {})
    if not schema.get('found'):
        scores['schema'] = 0
    else:
        count = schema.get('count', 0)
        if count >= 3:
            scores['schema'] = 100
        elif count >= 2:
            scores['schema'] = 80
        elif count >= 1:
            scores['schema'] = 60
        else:
            scores['schema'] = 20
    
    # JS Rendering Risk Score
    structure = results.get('structure', {})
    js_risk = structure.get('js_rendering_risk', {})
    
    if js_risk.get('empty_main') and js_risk.get('low_content'):
        scores['js_rendering'] = 20
    elif js_risk.get('loading_indicators'):
        scores['js_rendering'] = 40
    elif js_risk.get('low_content'):
        scores['js_rendering'] = 60
    elif any(structure.get('js_framework', {}).values()):
        scores['js_rendering'] = 80
    else:
        scores['js_rendering'] = 100
    
    # Sitemap Score
    sitemap = results.get('sitemap', {})
    if not sitemap.get('valid'):
        scores['sitemap'] = 0
    elif sitemap.get('has_lastmod') and sitemap.get('url_count', 0) > MIN_SITEMAP_URL_COUNT:
        scores['sitemap'] = 100
    elif sitemap.get('url_count', 0) > MIN_SITEMAP_URL_COUNT:
        scores['sitemap'] = 80
    elif sitemap.get('valid'):
        scores['sitemap'] = 60
    else:
        scores['sitemap'] = 40
    
    # llms.txt Score (binary for now)
    scores['llms_txt'] = 100 if results.get('llms_txt', {}).get('found') else 0
    
    # Calculate overall technical score
    scores['overall'] = (
        scores['crawler_access'] * CRAWLER_ACCESS_WEIGHT +
        scores['schema'] * SCHEMA_WEIGHT +
        scores['js_rendering'] * JS_RENDERING_WEIGHT +
        scores['sitemap'] * SITEMAP_WEIGHT +
        scores['llms_txt'] * LLMS_TXT_WEIGHT
    )
    
    return scores


def generate_report(results: dict, scores: dict, domain: str) -> str:
    """Generate markdown report from results."""
    
    report = f"""# Technical Audit Report

**Domain:** {domain}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Overall Score:** {scores['overall']:.0f}/100

---

## Crawler Access

**Score:** {scores['crawler_access']}/100

| Bot | Status |
|-----|--------|
"""
    
    for bot, status in results.get('robots', {}).get('bot_status', {}).items():
        emoji = '✅' if status == 'allowed' else ('⚠️' if status == 'partial' else '❌')
        report += f"| {bot} | {emoji} {status} |\n"
    
    report += f"""
---

## Schema Markup

**Score:** {scores['schema']}/100

- **Found:** {'Yes' if results.get('schema', {}).get('found') else 'No'}
- **Count:** {results.get('schema', {}).get('count', 0)}
- **Types:** {', '.join(results.get('schema', {}).get('types', [])) or 'None'}

---

## JavaScript Rendering

**Score:** {scores['js_rendering']}/100

| Check | Status |
|-------|--------|
| Framework Detected | {', '.join(k for k, v in results.get('structure', {}).get('js_framework', {}).items() if v) or 'None'} |
| Empty Main Tag | {'⚠️ Yes' if results.get('structure', {}).get('js_rendering_risk', {}).get('empty_main') else '✅ No'} |
| Loading Indicators | {'⚠️ Yes' if results.get('structure', {}).get('js_rendering_risk', {}).get('loading_indicators') else '✅ No'} |
| Content Word Count | {results.get('structure', {}).get('content_stats', {}).get('word_count_estimate', 'N/A')} |

---

## Site Structure

**Sitemap Score:** {scores['sitemap']}/100

- **Valid:** {'Yes' if results.get('sitemap', {}).get('valid') else 'No'}
- **URL Count:** {results.get('sitemap', {}).get('url_count', 'N/A')}
- **Last Modified:** {results.get('sitemap', {}).get('most_recent_lastmod', 'Not specified')}

**llms.txt:** {'✅ Present' if results.get('llms_txt', {}).get('found') else '❌ Not found'}

---

## Content Structure

| Element | Count |
|---------|-------|
| H1 Tags | {results.get('structure', {}).get('headings', {}).get('h1_count', 0)} |
| H2 Tags | {results.get('structure', {}).get('headings', {}).get('h2_count', 0)} |
| H3 Tags | {results.get('structure', {}).get('headings', {}).get('h3_count', 0)} |
| Has <main> | {'Yes' if results.get('structure', {}).get('semantic_elements', {}).get('has_main') else 'No'} |
| Has <article> | {'Yes' if results.get('structure', {}).get('semantic_elements', {}).get('has_article') else 'No'} |

---

## Recommendations

"""
    
    # Generate recommendations based on scores
    if scores['crawler_access'] < 80:
        report += "### 🚨 Critical: Crawler Access\n"
        report += "- Review robots.txt and ensure GPTBot and Bingbot are not blocked\n"
        report += "- ChatGPT relies on Bing; blocking Bingbot severely impacts AI visibility\n\n"
    
    if scores['schema'] < 60:
        report += "### ⚠️ High Priority: Schema Markup\n"
        report += "- Implement JSON-LD schema on key pages\n"
        report += "- Start with Organization schema on homepage\n"
        report += "- Add Product/Article schema to relevant pages\n\n"
    
    if scores['js_rendering'] < 60:
        report += "### ⚠️ High Priority: JavaScript Rendering\n"
        report += "- AI crawlers may not see JS-rendered content\n"
        report += "- Consider server-side rendering or static generation\n"
        report += "- Test with 'View Source' to verify content visibility\n\n"
    
    if scores['sitemap'] < 60:
        report += "### 📋 Medium Priority: Sitemap\n"
        report += "- Ensure sitemap.xml is valid and accessible\n"
        report += "- Include lastmod dates for all URLs\n"
        report += "- Reference sitemap in robots.txt\n\n"
    
    if scores['llms_txt'] == 0:
        report += "### 📝 Low Priority: llms.txt\n"
        report += "- Consider adding llms.txt to root directory\n"
        report += "- Emerging standard, low effort to implement\n"
        report += "- See references/llms-txt-template.md for template\n\n"
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Technical audit for GEO SEO')
    parser.add_argument('url', help='URL to audit')
    parser.add_argument('--output', '-o', help='Output file (JSON)', default=None)
    parser.add_argument('--report', '-r', help='Output markdown report', default=None)

    args = parser.parse_args()

    # Parse and validate URL
    parsed = urlparse(args.url)

    # Add scheme if missing
    if not parsed.scheme:
        args.url = f"https://{args.url}"
        parsed = urlparse(args.url)

    domain = f"{parsed.scheme}://{parsed.netloc}"

    print(f"Auditing: {domain}", file=sys.stderr)

    # This is a template - actual fetching would be done by Claude Code
    # Print instructions for what to fetch

    print(f"""
=== FETCH INSTRUCTIONS ===

To complete this audit, fetch the following URLs:

1. robots.txt: {domain}/robots.txt
2. Homepage HTML: {domain}/
3. Sitemap: {domain}/sitemap.xml
4. llms.txt: {domain}/llms.txt

Then call the analysis functions with the content.

Example usage with Claude Code:

    # Fetch robots.txt
    robots_content = web_fetch("{domain}/robots.txt")
    robots_results = parse_robots_txt(robots_content)

    # Fetch homepage
    html_content = web_fetch("{domain}/")
    schema_results = detect_schema(html_content)
    structure_results = analyze_content_structure(html_content)

    # Fetch sitemap
    sitemap_content = web_fetch("{domain}/sitemap.xml")
    sitemap_results = check_sitemap(sitemap_content)

    # Check llms.txt
    llms_content = web_fetch("{domain}/llms.txt")
    llms_results = {{'found': llms_content is not None and len(llms_content) > 0}}

    # Compile results
    results = {{
        'domain': "{domain}",
        'robots': robots_results,
        'schema': schema_results,
        'structure': structure_results,
        'sitemap': sitemap_results,
        'llms_txt': llms_results
    }}

    # Calculate scores
    scores = calculate_scores(results)

    # Generate report
    report = generate_report(results, scores, "{domain}")
""")


if __name__ == '__main__':
    main()
