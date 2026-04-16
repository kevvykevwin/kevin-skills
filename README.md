# Kevin's Claude Code Skills

Custom Claude Code skills for security scanning, software specs, marketing strategy, and research.

## Skills

| Skill | Description |
|-------|-------------|
| `security-agent` | Multi-mode security workflow — quick scan (pre-deploy) or full audit. Covers helper-function review, AI/LLM code risks, and e-commerce platform modules (Shopify, WooCommerce, BigCommerce, Next.js). |
| `security-deep-audit` | **Scaffold only.** Commercial-SAST-grade pipeline (Semgrep + Gitleaks + OSV-Scanner + modelscan + SARIF). Design captured, not implemented — build only if the lightweight `security-agent` misses findings across ≥3 incidents. |
| `ad-campaign-strategy` | Paid media campaign planning for Meta, Google, TikTok, LinkedIn. |
| `brand-discovery` | Brand health assessment and creative gap analysis. |
| `fractional-cmo-frameworks` | C-suite marketing leadership frameworks and planning. |
| `google-ads-strategy` | Google Ads campaign structure and keyword research. |
| `research-assistant` | Deep-dive research for writing projects. |
| `seo-agent` | SEO audit and technical-SEO implementation guidance. |
| `spec-writing` | Verifiable software specs with testable acceptance criteria. |
| `test-generator` | Generate executable tests from spec test cases. |

## Installation

### Option 1 — Claude Code plugin (recommended)

```
/plugin install kevvykevwin/kevin-skills
```

The repository ships `.claude-plugin/plugin.json`, so Claude Code's plugin system can install all skills in one command.

### Option 2 — Manual install of a single skill

```sh
git clone https://github.com/kevvykevwin/kevin-skills.git
cp -r kevin-skills/skills/security-agent ~/.claude/skills/
chmod +x ~/.claude/skills/security-agent/scripts/quick-scan.sh
```

Replace `security-agent` with any other skill name to install just that one.

### Option 3 — Symlink (get updates via `git pull`)

```sh
git clone https://github.com/kevvykevwin/kevin-skills.git ~/kevin-skills
ln -s ~/kevin-skills/skills/security-agent ~/.claude/skills/security-agent
```

## Repository Structure

```
kevin-skills/
├── .claude-plugin/
│   └── plugin.json
├── README.md
└── skills/
    ├── security-agent/
    │   ├── SKILL.md
    │   ├── references/      (platform checklists, threat patterns, helper & AI playbooks)
    │   └── scripts/
    │       ├── quick-scan.sh
    │       └── create-github-issues.py
    ├── security-deep-audit/
    │   └── README.md         (scaffold only, not implemented)
    ├── ad-campaign-strategy/
    ├── brand-discovery/
    ├── fractional-cmo-frameworks/
    ├── google-ads-strategy/
    ├── research-assistant/
    ├── seo-agent/
    ├── spec-writing/
    └── test-generator/
```

## Featured: `security-agent`

Two modes:

- **Quick Scan** — `scripts/quick-scan.sh [path] [--with-helpers]`. Zero-dependency bash scanner. 14 checks covering secrets, dangerous functions, SQL injection, env-file leakage, npm/pip audit, helper-function triage, AI/ML P1 patterns (`trust_remote_code`, `yaml.load`, `pickle.loads`, `torch.load` without `weights_only`), weak randomness in security context, JWT algorithm confusion, MCP/AI-tool config leakage, prototype-pollution sinks, open redirects, and LLM dependency detection. Runs in under a second on typical projects.
- **Full Audit** — Phase 1 runs the quick scan, then parallel sonnet sub-agents handle helper review, AI/LLM code review (conditional on LLM deps detected), platform checks, and e-commerce threat analysis. Consolidated into a markdown report; optional GitHub issue creation for HIGH/CRITICAL findings.

Designed to run anywhere with zero install. If you need Semgrep/Gitleaks/OSV-Scanner-grade depth, see the `security-deep-audit` scaffold.

## License

MIT (see repo root LICENSE if present, else all skills usable under permissive terms).

## Author

[Kevin Nguyen](https://github.com/kevvykevwin)
