#!/usr/bin/env python3
"""
Citation Tester for GEO SEO Agent

Manages test prompts and tracks citation results over time.

Features:
- Generate test prompts from templates
- Log citation test results
- Track trends over time
- Calculate citation scores

Usage:
    python citation_tester.py generate --brand "Brand Name" --category "product category"
    python citation_tester.py log --client "client-id" --results results.json
    python citation_tester.py report --client "client-id"
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


# Default data directory
DATA_DIR = Path.home() / '.geo-seo-agent' / 'citation-data'

# Constants
MAX_COMPETITORS = 3
CITATION_RATE_THRESHOLD = 5  # For trend analysis


def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_client_id(client_id: str) -> str:
    """
    Sanitize client_id to prevent path traversal attacks.
    Only allows alphanumeric, dash, and underscore characters.
    """
    if not client_id:
        raise ValueError("Client ID cannot be empty")

    # Only allow alphanumeric, dash, and underscore
    if not re.match(r'^[a-zA-Z0-9_-]+$', client_id):
        raise ValueError(
            f"Invalid client ID: '{client_id}'. "
            "Only alphanumeric characters, dashes, and underscores are allowed."
        )

    return client_id


def escape_markdown(text: str) -> str:
    """Escape special markdown characters in text for table cells."""
    # Escape pipe character which breaks markdown tables
    return text.replace('|', '\\|')


def generate_prompts(brand: str, category: str, competitors: list = None, 
                     client_type: str = 'D2C') -> dict:
    """Generate test prompts for a brand."""
    
    competitors = competitors or []
    
    prompts = {
        'brand_queries': [
            f"What is {brand}?",
            f"{brand} reviews",
            f"Is {brand} legit?",
        ],
        'category_queries': [
            f"Best {category} brands",
            f"Top {category} recommendations",
            f"Where to buy {category}",
            f"Best {category} for quality",
            f"{category} buying guide",
        ],
        'comparison_queries': [
            f"{brand} alternatives",
        ],
        'problem_queries': [
            f"How to choose {category}",
            f"What to look for in {category}",
        ]
    }
    
    # Add competitor comparisons
    for comp in competitors[:MAX_COMPETITORS]:
        prompts['comparison_queries'].append(f"{brand} vs {comp}")
    
    # Add client-type specific prompts
    if client_type == 'D2C':
        prompts['problem_queries'].extend([
            f"Best {category} for the price",
            f"Quality {category} brands",
        ])
    elif client_type == 'B2B':
        prompts['category_queries'].extend([
            f"Best {category} for business",
            f"{category} for enterprise",
        ])
        prompts['problem_queries'].extend([
            f"How to evaluate {category}",
            f"{category} implementation guide",
        ])
    
    return {
        'brand': brand,
        'category': category,
        'competitors': competitors,
        'client_type': client_type,
        'generated_at': datetime.now().isoformat(),
        'prompts': prompts,
        'total_prompts': sum(len(v) for v in prompts.values())
    }


def create_test_template(prompts: dict) -> str:
    """Create a markdown template for manual testing."""

    # Escape brand name for markdown
    brand_escaped = escape_markdown(prompts['brand'])
    category_escaped = escape_markdown(prompts['category'])

    template = f"""# Citation Test Template

**Brand:** {brand_escaped}
**Category:** {category_escaped}
**Date:** {datetime.now().strftime('%Y-%m-%d')}

---

## Instructions

For each prompt below:
1. Test in ChatGPT (with browsing enabled)
2. Test in Google (check for AI Overview)
3. Record results in the table

### Scoring Guide

| Score | Meaning |
|-------|---------|
| 5 | Primary recommendation ("The best...", "I recommend...") |
| 4 | Strong mention ("Top options include...") |
| 3 | Listed among options ("...is one of several...") |
| 2 | Mentioned with caveats |
| 1 | Negative mention |
| 0 | Not mentioned |

---

## Brand Queries

| Prompt | ChatGPT Mentioned | ChatGPT Score | Google AIO | Google Score | Notes |
|--------|-------------------|---------------|------------|--------------|-------|
"""

    for prompt in prompts['prompts']['brand_queries']:
        escaped_prompt = escape_markdown(prompt)
        template += f"| {escaped_prompt} | Y/N | 0-5 | Y/N | 0-5 | |\n"
    
    template += """
---

## Category Queries

| Prompt | ChatGPT Mentioned | ChatGPT Score | Google AIO | Google Score | Competitors Seen | Notes |
|--------|-------------------|---------------|------------|--------------|------------------|-------|
"""

    for prompt in prompts['prompts']['category_queries']:
        escaped_prompt = escape_markdown(prompt)
        template += f"| {escaped_prompt} | Y/N | 0-5 | Y/N | 0-5 | | |\n"

    template += """
---

## Comparison Queries

| Prompt | ChatGPT Mentioned | ChatGPT Score | Google AIO | Google Score | Context | Notes |
|--------|-------------------|---------------|------------|--------------|---------|-------|
"""

    for prompt in prompts['prompts']['comparison_queries']:
        escaped_prompt = escape_markdown(prompt)
        template += f"| {escaped_prompt} | Y/N | 0-5 | Y/N | 0-5 | | |\n"

    template += """
---

## Problem Queries

| Prompt | ChatGPT Mentioned | ChatGPT Score | Google AIO | Google Score | Competitors Seen | Notes |
|--------|-------------------|---------------|------------|--------------|------------------|-------|
"""

    for prompt in prompts['prompts']['problem_queries']:
        escaped_prompt = escape_markdown(prompt)
        template += f"| {escaped_prompt} | Y/N | 0-5 | Y/N | 0-5 | | |\n"
    
    template += """
---

## Summary

**Total Prompts Tested:** ___

**ChatGPT Results:**
- Mentioned: ___ / ___
- Average Score: ___
- Citation Rate: ___%

**Google AI Overview Results:**
- AIO Appeared: ___ / ___
- Mentioned in AIO: ___ / ___
- Average Score: ___

**Key Findings:**
- 
- 
- 

**Top Competitors Seen:**
1. 
2. 
3. 
"""
    
    return template


def log_results(client_id: str, results: dict):
    """Log citation test results for a client."""

    ensure_data_dir()

    # Sanitize client_id to prevent path traversal
    safe_client_id = sanitize_client_id(client_id)

    client_dir = DATA_DIR / safe_client_id
    client_dir.mkdir(exist_ok=True)

    # Add timestamp
    results['logged_at'] = datetime.now().isoformat()

    # Save to dated file
    date_str = datetime.now().strftime('%Y-%m-%d')
    results_file = client_dir / f'results-{date_str}.json'

    # Append if file exists for same day
    existing = []
    if results_file.exists():
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
                if not isinstance(existing, list):
                    existing = [existing]
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to read existing results file: {e}")

    existing.append(results)

    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=2)
    except IOError as e:
        raise RuntimeError(f"Failed to write results file: {e}")

    # Update latest pointer
    latest_file = client_dir / 'latest.json'
    try:
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
    except IOError as e:
        raise RuntimeError(f"Failed to write latest file: {e}")

    return str(results_file)


def load_client_history(client_id: str) -> list:
    """Load all historical results for a client."""

    ensure_data_dir()

    # Sanitize client_id to prevent path traversal
    safe_client_id = sanitize_client_id(client_id)

    client_dir = DATA_DIR / safe_client_id
    if not client_dir.exists():
        return []

    all_results = []

    for results_file in sorted(client_dir.glob('results-*.json')):
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_results.extend(data)
                else:
                    all_results.append(data)
        except (IOError, json.JSONDecodeError) as e:
            # Log warning but continue with other files
            print(f"Warning: Failed to read {results_file}: {e}", file=sys.stderr)
            continue

    return all_results


def calculate_metrics(results: dict) -> dict:
    """Calculate citation metrics from test results."""
    
    metrics = {
        'chatgpt': {
            'total_prompts': 0,
            'mentioned': 0,
            'scores': [],
            'citation_rate': 0,
            'avg_score': 0
        },
        'google_aio': {
            'total_prompts': 0,
            'aio_appeared': 0,
            'mentioned': 0,
            'scores': [],
            'citation_rate': 0,
            'avg_score': 0
        }
    }
    
    # Process results by category
    for category, prompts in results.get('results', {}).items():
        for prompt_result in prompts:
            # ChatGPT metrics
            if 'chatgpt' in prompt_result:
                metrics['chatgpt']['total_prompts'] += 1
                if prompt_result['chatgpt'].get('mentioned'):
                    metrics['chatgpt']['mentioned'] += 1
                score = prompt_result['chatgpt'].get('score', 0)
                metrics['chatgpt']['scores'].append(score)
            
            # Google AIO metrics
            if 'google_aio' in prompt_result:
                metrics['google_aio']['total_prompts'] += 1
                if prompt_result['google_aio'].get('appeared'):
                    metrics['google_aio']['aio_appeared'] += 1
                if prompt_result['google_aio'].get('mentioned'):
                    metrics['google_aio']['mentioned'] += 1
                score = prompt_result['google_aio'].get('score', 0)
                metrics['google_aio']['scores'].append(score)
    
    # Calculate rates and averages
    for platform in ['chatgpt', 'google_aio']:
        total = metrics[platform]['total_prompts']
        if total > 0:
            mentioned = metrics[platform]['mentioned']
            metrics[platform]['citation_rate'] = (mentioned / total) * 100
            
            scores = metrics[platform]['scores']
            if scores:
                metrics[platform]['avg_score'] = sum(scores) / len(scores)
    
    return metrics


def generate_trend_report(client_id: str) -> str:
    """Generate a trend report from historical data."""
    
    history = load_client_history(client_id)
    
    if not history:
        return f"No historical data found for client: {client_id}"
    
    report = f"""# Citation Trend Report

**Client:** {client_id}
**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Data Points:** {len(history)}

---

## Historical Performance

| Date | ChatGPT Rate | ChatGPT Score | Google Rate | Google Score |
|------|--------------|---------------|-------------|--------------|
"""
    
    for result in history:
        metrics = calculate_metrics(result)
        date = result.get('logged_at', 'Unknown')[:10]
        
        chatgpt_rate = f"{metrics['chatgpt']['citation_rate']:.1f}%"
        chatgpt_score = f"{metrics['chatgpt']['avg_score']:.2f}"
        google_rate = f"{metrics['google_aio']['citation_rate']:.1f}%"
        google_score = f"{metrics['google_aio']['avg_score']:.2f}"
        
        report += f"| {date} | {chatgpt_rate} | {chatgpt_score} | {google_rate} | {google_score} |\n"
    
    # Calculate trends
    if len(history) >= 2:
        first_metrics = calculate_metrics(history[0])
        last_metrics = calculate_metrics(history[-1])
        
        chatgpt_change = last_metrics['chatgpt']['citation_rate'] - first_metrics['chatgpt']['citation_rate']
        google_change = last_metrics['google_aio']['citation_rate'] - first_metrics['google_aio']['citation_rate']
        
        report += f"""
---

## Trend Summary

**ChatGPT Citation Rate Change:** {chatgpt_change:+.1f}%
**Google AIO Citation Rate Change:** {google_change:+.1f}%

"""
        
        if chatgpt_change > CITATION_RATE_THRESHOLD:
            report += "✅ ChatGPT visibility improving\n"
        elif chatgpt_change < -CITATION_RATE_THRESHOLD:
            report += "⚠️ ChatGPT visibility declining\n"
        else:
            report += "➡️ ChatGPT visibility stable\n"

        if google_change > CITATION_RATE_THRESHOLD:
            report += "✅ Google AIO visibility improving\n"
        elif google_change < -CITATION_RATE_THRESHOLD:
            report += "⚠️ Google AIO visibility declining\n"
        else:
            report += "➡️ Google AIO visibility stable\n"
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Citation testing for GEO SEO')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate test prompts')
    gen_parser.add_argument('--brand', required=True, help='Brand name')
    gen_parser.add_argument('--category', required=True, help='Product/service category')
    gen_parser.add_argument('--competitors', nargs='+', help='Competitor names')
    gen_parser.add_argument('--type', choices=['D2C', 'B2B'], default='D2C', help='Client type')
    gen_parser.add_argument('--output', '-o', help='Output file')
    gen_parser.add_argument('--template', '-t', action='store_true', help='Output markdown template')
    
    # Log command
    log_parser = subparsers.add_parser('log', help='Log test results')
    log_parser.add_argument('--client', required=True, help='Client ID')
    log_parser.add_argument('--results', required=True, help='Results JSON file')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate trend report')
    report_parser.add_argument('--client', required=True, help='Client ID')
    
    args = parser.parse_args()

    # Exit with error if no command provided
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'generate':
            prompts = generate_prompts(
                brand=args.brand,
                category=args.category,
                competitors=args.competitors,
                client_type=args.type
            )

            if args.template:
                output = create_test_template(prompts)
            else:
                output = json.dumps(prompts, indent=2)

            if args.output:
                try:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(output)
                    print(f"Output written to: {args.output}")
                except IOError as e:
                    print(f"Error: Failed to write output file: {e}", file=sys.stderr)
                    sys.exit(1)
            else:
                print(output)

        elif args.command == 'log':
            try:
                with open(args.results, 'r', encoding='utf-8') as f:
                    results = json.load(f)
            except FileNotFoundError:
                print(f"Error: Results file not found: {args.results}", file=sys.stderr)
                sys.exit(1)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in results file: {e}", file=sys.stderr)
                sys.exit(1)
            except IOError as e:
                print(f"Error: Failed to read results file: {e}", file=sys.stderr)
                sys.exit(1)

            filepath = log_results(args.client, results)
            print(f"Results logged to: {filepath}")

            metrics = calculate_metrics(results)
            print(f"\nChatGPT Citation Rate: {metrics['chatgpt']['citation_rate']:.1f}%")
            print(f"Google AIO Citation Rate: {metrics['google_aio']['citation_rate']:.1f}%")

        elif args.command == 'report':
            report = generate_trend_report(args.client)
            print(report)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
