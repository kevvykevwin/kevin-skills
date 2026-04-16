#!/usr/bin/env python3
"""
GitHub Issue Generator for Security Findings

Creates GitHub issues from security audit findings.
Requires: GITHUB_TOKEN environment variable with repo scope.

Usage:
    python create-github-issues.py --repo owner/repo --findings findings.json
    python create-github-issues.py --repo owner/repo --interactive
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


@dataclass
class Finding:
    """Security finding to convert to GitHub issue."""
    id: str
    title: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str
    description: str
    location: Optional[str] = None
    impact: Optional[str] = None
    remediation: Optional[str] = None
    effort: Optional[str] = None  # hours, days, sprint


SEVERITY_LABELS = {
    "CRITICAL": "security:critical",
    "HIGH": "security:high", 
    "MEDIUM": "security:medium",
    "LOW": "security:low"
}

SEVERITY_EMOJI = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🟢"
}


def get_github_token() -> str:
    """Get GitHub token from environment."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Create a token at: https://github.com/settings/tokens")
        print("Required scope: repo")
        sys.exit(1)
    return token


def ensure_labels_exist(repo: str, token: str) -> None:
    """Create security labels if they don't exist."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    labels_to_create = [
        {"name": "security:critical", "color": "B60205", "description": "Critical security issue - immediate action required"},
        {"name": "security:high", "color": "D93F0B", "description": "High severity security issue"},
        {"name": "security:medium", "color": "FBCA04", "description": "Medium severity security issue"},
        {"name": "security:low", "color": "0E8A16", "description": "Low severity security issue"},
        {"name": "security-audit", "color": "5319E7", "description": "From security audit"},
    ]
    
    for label in labels_to_create:
        response = requests.post(
            f"https://api.github.com/repos/{repo}/labels",
            headers=headers,
            json=label
        )
        if response.status_code == 201:
            print(f"Created label: {label['name']}")
        elif response.status_code == 422:
            # Label already exists
            pass
        else:
            print(f"Warning: Could not create label {label['name']}: {response.text}")


def create_issue(repo: str, token: str, finding: Finding, dry_run: bool = False) -> Optional[str]:
    """Create a GitHub issue from a security finding."""
    
    severity_emoji = SEVERITY_EMOJI.get(finding.severity, "⚪")
    severity_label = SEVERITY_LABELS.get(finding.severity, "security:medium")
    
    # Build issue title
    title = f"{severity_emoji} [{finding.severity}] {finding.title}"
    
    # Build issue body
    body_parts = [
        f"## Security Finding: {finding.title}",
        "",
        f"**Severity:** {severity_emoji} {finding.severity}",
        f"**Category:** {finding.category}",
        f"**Finding ID:** {finding.id}",
        "",
        "---",
        "",
        "### Description",
        finding.description,
    ]
    
    if finding.location:
        body_parts.extend([
            "",
            "### Location",
            f"```\n{finding.location}\n```",
        ])
    
    if finding.impact:
        body_parts.extend([
            "",
            "### Impact",
            finding.impact,
        ])
    
    if finding.remediation:
        body_parts.extend([
            "",
            "### Remediation",
            finding.remediation,
        ])
    
    if finding.effort:
        body_parts.extend([
            "",
            f"**Estimated Effort:** {finding.effort}",
        ])
    
    body_parts.extend([
        "",
        "---",
        "*This issue was automatically created by Security Agent from a security audit.*",
    ])
    
    body = "\n".join(body_parts)
    
    # Labels
    labels = ["security-audit", severity_label]
    
    if dry_run:
        print(f"\n{'='*60}")
        print(f"ISSUE: {title}")
        print(f"LABELS: {', '.join(labels)}")
        print(f"{'='*60}")
        print(body)
        return None
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers=headers,
        json={
            "title": title,
            "body": body,
            "labels": labels
        }
    )
    
    if response.status_code == 201:
        issue_url = response.json()["html_url"]
        print(f"✓ Created issue: {issue_url}")
        return issue_url
    else:
        print(f"✗ Failed to create issue: {response.text}")
        return None


def load_findings_from_file(filepath: str) -> list[Finding]:
    """Load findings from JSON file."""
    with open(filepath, "r") as f:
        data = json.load(f)
    
    findings = []
    for item in data:
        findings.append(Finding(
            id=item.get("id", "UNKNOWN"),
            title=item["title"],
            severity=item["severity"],
            category=item.get("category", "General"),
            description=item["description"],
            location=item.get("location"),
            impact=item.get("impact"),
            remediation=item.get("remediation"),
            effort=item.get("effort"),
        ))
    
    return findings


def interactive_finding() -> Finding:
    """Interactively create a finding."""
    print("\n--- Create Security Finding ---")
    
    id = input("Finding ID (e.g., SEC-001): ").strip()
    title = input("Title: ").strip()
    
    print("Severity (1=CRITICAL, 2=HIGH, 3=MEDIUM, 4=LOW): ", end="")
    severity_map = {"1": "CRITICAL", "2": "HIGH", "3": "MEDIUM", "4": "LOW"}
    severity = severity_map.get(input().strip(), "MEDIUM")
    
    category = input("Category (e.g., Injection, Auth, Secrets): ").strip()
    description = input("Description: ").strip()
    location = input("Location (file:line, optional): ").strip() or None
    impact = input("Impact (optional): ").strip() or None
    remediation = input("Remediation (optional): ").strip() or None
    effort = input("Effort estimate (optional, e.g., '2 hours'): ").strip() or None
    
    return Finding(
        id=id,
        title=title,
        severity=severity,
        category=category,
        description=description,
        location=location,
        impact=impact,
        remediation=remediation,
        effort=effort,
    )


def main():
    parser = argparse.ArgumentParser(description="Create GitHub issues from security findings")
    parser.add_argument("--repo", required=True, help="Repository (owner/repo)")
    parser.add_argument("--findings", help="JSON file with findings")
    parser.add_argument("--interactive", action="store_true", help="Create findings interactively")
    parser.add_argument("--dry-run", action="store_true", help="Print issues without creating")
    parser.add_argument("--skip-labels", action="store_true", help="Skip label creation")
    
    args = parser.parse_args()
    
    token = get_github_token()
    
    # Ensure labels exist
    if not args.dry_run and not args.skip_labels:
        print("Ensuring labels exist...")
        ensure_labels_exist(args.repo, token)
    
    findings = []
    
    if args.findings:
        findings = load_findings_from_file(args.findings)
        print(f"Loaded {len(findings)} findings from {args.findings}")
    
    if args.interactive:
        while True:
            findings.append(interactive_finding())
            if input("\nAdd another finding? (y/n): ").strip().lower() != "y":
                break
    
    if not findings:
        print("No findings to process. Use --findings or --interactive")
        sys.exit(1)
    
    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    findings.sort(key=lambda f: severity_order.get(f.severity, 99))
    
    print(f"\nCreating {len(findings)} issues...")
    
    created_urls = []
    for finding in findings:
        url = create_issue(args.repo, token, finding, dry_run=args.dry_run)
        if url:
            created_urls.append(url)
    
    if not args.dry_run:
        print(f"\n✓ Created {len(created_urls)} issues")


if __name__ == "__main__":
    main()


# Example findings.json format:
"""
[
    {
        "id": "SEC-001",
        "title": "API Key exposed in source code",
        "severity": "CRITICAL",
        "category": "Secrets",
        "description": "Stripe API key is hardcoded in checkout.js",
        "location": "src/checkout.js:42",
        "impact": "Attacker could charge cards or access customer data",
        "remediation": "Move to environment variable, rotate the exposed key",
        "effort": "1 hour"
    },
    {
        "id": "SEC-002",
        "title": "Missing rate limiting on login",
        "severity": "HIGH",
        "category": "Authentication",
        "description": "Login endpoint has no rate limiting, vulnerable to brute force",
        "location": "pages/api/auth/login.js",
        "impact": "Account takeover via credential stuffing",
        "remediation": "Add rate limiting middleware (e.g., express-rate-limit)",
        "effort": "2 hours"
    }
]
"""
