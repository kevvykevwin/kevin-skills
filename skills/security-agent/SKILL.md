---
name: security-agent
description: Multi-mode security workflow. Quick scan (pre-deploy) or full audit with sub-agents. Covers helper-function review, AI/LLM code risks, and e-commerce platform modules (Shopify, WooCommerce, BigCommerce, Next.js).
argument-hint: [project_path] [--with-helpers] [--verbose]
---

# Security Agent — Dispatcher

## Mode Detection

| Mode | Triggers |
|------|----------|
| **Quick Scan** | "quick scan", "security check", "pre-deploy scan", "check for vulnerabilities" |
| **Full Audit** | "full audit", "security audit", "anti-carding audit", "comprehensive security review" |

---

## Flags

| Flag | Effect |
|------|--------|
| `--with-helpers` | Enable Check 7 (helper file triage → MANUAL-REVIEW findings). Default: off. |
| `--verbose` | Expand npm/pip audit output in the scan report. Default: off. |

The first positional argument is the project path (defaults to `.`). Flags may appear before or after the path.

---

## Quick Scan Flow

1. **Run scanner** — Execute `scripts/quick-scan.sh [project_path] [flags]` via Bash. Do NOT read the script into context.
2. **Follow up** — For any flagged files, run targeted Grep to confirm true/false positives. MANUAL-REVIEW findings are review prompts, not deploy blockers.
3. **Output** — Report pass/fail directly using the output format below. No sub-agents needed.

---

## Full Audit Flow

### Phase 1: Quick Scan
Run `scripts/quick-scan.sh [project_path] --with-helpers` via Bash. Capture findings and stdout. Grep the output for the line `AI_DEPS_DETECTED=1` — presence signals LLM/AI dependencies in the project.

### Phase 2: Platform Detection
Detect platform using quick globs:

| Platform | Detection |
|----------|-----------|
| Shopify | `shopify` in package.json, `.shopify/` dir, `*.liquid` files |
| WooCommerce | `wp-content/plugins/woocommerce/`, `wc-` prefixed files |
| BigCommerce | `@bigcommerce/` in package.json, `stencil.conf.js` |
| Next.js (Custom) | `next.config.js`/`next.config.mjs`, no platform-specific deps |

### Phase 3: Parallel Sub-Agents

Always spawn in parallel (sonnet model, general-purpose type):

**1. `platform-auditor`** — Prompt:
> Read `references/platform-{detected}.md` and `references/platform-cross.md`. Audit the project against every checklist item. Return structured findings with severity, location, and remediation for each failed check.

**Conditional sub-agents** — spawn only when their trigger fires:

**2. `anticarding-auditor`** (only if platform ∈ {shopify, woocommerce, bigcommerce}) — Prompt:
> Read `references/anti-carding-checklist.md`. Assess each layer (0-5) against the project. Return structured findings: which controls are present, missing, or misconfigured. Include severity for each gap.

**3. `threat-analyst`** (only if platform ∈ {shopify, woocommerce, bigcommerce}) — Prompt:
> Read `references/threat-patterns.md` and `references/threat-queries.md`. Analyze the project for exposure to known attack patterns. Check if detection queries or equivalent monitoring exists. Return findings with severity.

**4. `helper-reviewer`** (only if Phase 1 produced MANUAL-REVIEW findings from Check 7) — Prompt:
> Read `references/helper-inspection.md`. For each helper file the scanner flagged as MANUAL-REVIEW, read the helper function and its call sites, then judge whether the advertised safety property of the helper actually holds.
>
> **Required structured output per finding**:
> - `file:line`
> - `broken-invariant` (one sentence describing what safety property is violated)
> - `example-bypass-input` (one concrete input that defeats the broken helper)
> - `confidence` ∈ {high, med, low}
>
> Reject your own output if any of the four fields is missing. Do not emit free-form prose verdicts. If a helper is safe, return `confidence: high` + `broken-invariant: none` + `example-bypass-input: n/a`.

**5. `ai-code-reviewer`** (only if Phase 1 output contains `AI_DEPS_DETECTED=1`) — Prompt:
> Read `references/ai-code-threats.md`. Audit the project against each section: prompt-injection sinks, LLM output handling, model-loading / pickle RCE, MCP / agentic tool-use, AI-supply-chain and slopsquat, committed dev-tool leakage, rate-limiting. Return findings in the format specified at the end of the reference file: `file:line`, `risk-class`, `severity`, `broken-invariant`, `fix-suggestion`.

### Phase 4: Consolidate & Report
Merge quick scan results + all sub-agent findings. Spawn **report-generator** sub-agent (haiku model, general-purpose type):
> Read `references/audit-report-template.md`. Using the consolidated findings provided, fill in the template. Output the complete markdown report.

### Phase 5: GitHub Issues (Optional)
For HIGH/CRITICAL findings, offer to run:
```bash
python scripts/create-github-issues.py --repo OWNER/REPO --findings findings.json
```

---

## Severity Definitions

| Level | Meaning | Action |
|-------|---------|--------|
| CRITICAL | Actively exploitable, data at risk | Block deploy. Fix immediately. |
| HIGH | Significant risk, easy to exploit | Fix before deploy. |
| MEDIUM | Moderate risk, requires conditions | Track, fix in next sprint. |
| MANUAL-REVIEW | Pattern match warrants human/LLM review; not automatically exploitable | Review via helper-reviewer sub-agent or manual inspection. Does not block deploy. |
| LOW | Minor issue, defense in depth | Document, fix when convenient. |

---

## Output Format (Quick Scan)

```markdown
## Quick Security Scan Results
**Project**: [name] | **Date**: [timestamp] | **Status**: PASS / FAIL

### Critical Issues (Block Deploy)
| Issue | Location | Fix |
|-------|----------|-----|

### High Issues (Fix Before Deploy)
| Issue | Location | Fix |
|-------|----------|-----|

### Manual Review (Non-Blocking)
| Category | File | Playbook |
|----------|------|----------|

### Passed Checks
- [x] No secrets in code
- [x] No dangerous functions with user input
- [x] Parameterized queries used
- [x] Auth middleware present
- [x] No critical dependency vulnerabilities
- [x] No AI/ML P1 patterns (trust_remote_code, unsafe yaml.load, pickle.loads, torch.load without weights_only)
- [x] No weak randomness in security context
- [x] JWT algorithm whitelist present
- [x] No expanded env/MCP config leakage
- [x] No unguarded deep-merge helpers
- [x] No open-redirect patterns
```

---

## Integration
- `spec-writing` — Security requirements in acceptance criteria
- `backend-engineering` — TLS/JWT/OAuth implementation patterns
- `code-reviewer` — Structural review of helper functions flagged by MANUAL-REVIEW
- `compound-docs` — Capture recurring security findings as institutional knowledge
- `verification-loop` — Include security scan in verification pass

## Companion Skill
- `security-deep-audit` (scaffold only, not yet implemented) — commercial-SAST-grade pipeline with Semgrep + Gitleaks + OSV-Scanner + modelscan + SARIF aggregation. See `~/.claude/skills/security-deep-audit/README.md`. Build only if this lightweight skill misses findings across ≥3 incidents.
