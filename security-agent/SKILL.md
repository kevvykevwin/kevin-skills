---
name: security-agent
description: Comprehensive security scanning and auditing for e-commerce apps and websites. Two modes: (1) quick-scan for fast pre-deploy code checks (secrets, injection, dependencies), (2) full-audit for comprehensive infrastructure review (anti-carding, WAF, payment gateway, platform-specific). Supports Shopify, WooCommerce, BigCommerce, and custom (Next.js) stacks. Outputs markdown reports and GitHub issues.
---

# Security Agent

Two-mode security workflow for e-commerce infrastructure.

## Modes

### 1. Quick Scan (Pre-Deploy)
Fast code-level checks. Run before every deploy.

**Triggers**: "quick scan", "security check", "pre-deploy scan", "check for vulnerabilities"

**What it checks**:
- Secrets in code (API keys, passwords, tokens)
- Injection vulnerabilities (SQL, NoSQL, XSS, command injection)
- Dangerous functions (eval, innerHTML, exec)
- Auth bypass risks
- Dependency vulnerabilities (npm audit, pip-audit)
- HTTPS/security headers

**Output**: Pass/fail with critical issues. ~30 seconds.

### 2. Full Audit (Periodic)
Comprehensive infrastructure review. Run weekly or before client handoffs.

**Triggers**: "full audit", "security audit", "anti-carding audit", "comprehensive security review"

**What it checks**:
- Everything in quick-scan PLUS:
- Anti-carding stack configuration (see references/anti-carding-stack.md)
- WAF/CDN settings (Cloudflare, etc.)
- Payment gateway fraud controls (Stripe Radar, Braintree, etc.)
- Bot mitigation status
- Device fingerprinting implementation
- Platform-specific vulnerabilities
- Logging and monitoring gaps

**Output**: Full markdown report + GitHub issues. ~5-10 minutes.

---

## Quick Scan Workflow

Run these checks in sequence. Stop and report on first CRITICAL finding.

### Step 1: Secrets Detection
```bash
# Run from project root
grep -rn --include="*.{js,ts,jsx,tsx,py,go,env,json,yaml,yml}" \
  -E "(password|secret|api_key|apikey|token|private_key|aws_|stripe_sk|sk_live|sk_test)" . \
  | grep -v node_modules | grep -v ".git"
```
**CRITICAL if**: Any matches in committed code (not .env)

### Step 2: Dangerous Functions
```bash
# JavaScript/TypeScript
grep -rn --include="*.{js,ts,jsx,tsx}" \
  -E "(eval\(|dangerouslySetInnerHTML|innerHTML\s*=|document\.write|exec\(|Function\()" . \
  | grep -v node_modules

# Python
grep -rn --include="*.py" -E "(eval\(|exec\(|os\.system|subprocess\.call.*shell=True)" .
```
**CRITICAL if**: User input flows to these functions

### Step 3: SQL/NoSQL Injection
```bash
# Raw query patterns (JS/TS)
grep -rn --include="*.{js,ts}" -E "(query\(|execute\(|raw\()" . | grep -v node_modules

# Check for string concatenation in queries
grep -rn --include="*.{js,ts,py}" -E "(\+.*SELECT|\+.*INSERT|\+.*UPDATE|f\".*SELECT|f\".*INSERT)" .
```
**CRITICAL if**: String concatenation with user input in queries

### Step 4: Auth Checks
Review manually:
- [ ] Protected routes have auth middleware
- [ ] Server validates auth (not just client)
- [ ] Session tokens use HttpOnly, Secure flags
- [ ] Rate limiting on login/register endpoints

### Step 5: Dependency Audit
```bash
# Node.js
npm audit --audit-level=high 2>/dev/null || echo "npm audit failed or not a node project"

# Python
pip-audit 2>/dev/null || echo "pip-audit not available"
```
**HIGH if**: Any high/critical vulnerabilities

### Step 6: Security Headers Check
If URL available:
```bash
curl -sI "$URL" | grep -iE "(strict-transport|content-security|x-frame|x-content-type)"
```
**HIGH if**: Missing HSTS, CSP, X-Frame-Options

### Quick Scan Output Template
```markdown
## Quick Security Scan Results

**Project**: [name]
**Date**: [timestamp]
**Status**: ✅ PASS / ❌ FAIL

### Critical Issues (Block Deploy)
| Issue | Location | Fix |
|-------|----------|-----|
| [finding] | [file:line] | [remediation] |

### High Issues (Fix Before Deploy)
| Issue | Location | Fix |
|-------|----------|-----|

### Passed Checks
- [x] No secrets in code
- [x] No dangerous functions with user input
- [x] Parameterized queries used
- [x] Auth middleware present
- [x] No critical dependency vulnerabilities
```

---

## Full Audit Workflow

### Phase 1: Run Quick Scan
Execute all quick scan checks first.

### Phase 2: Platform Detection
Identify the e-commerce platform:

| Platform | Detection Method |
|----------|------------------|
| Shopify | `shopify` in package.json, `.shopify/` dir, Liquid templates |
| WooCommerce | `wp-content/plugins/woocommerce`, `wc-` prefixed files |
| BigCommerce | `bigcommerce` in package.json, Stencil CLI |
| Custom (Next.js) | `next.config.js`, no platform-specific files |

Then load platform-specific checks from `references/platform-checks.md`.

### Phase 3: Anti-Carding Stack Audit
Reference: `references/anti-carding-stack.md`

Assess each layer:

**Layer 0: Payment Processor (MANDATORY)**
- [ ] AVS enabled and enforced
- [ ] CVV required on all transactions
- [ ] Velocity rules configured (per card/IP/device)
- [ ] BIN/IP mismatch blocking enabled
- [ ] Fraud scoring active (Stripe Radar score threshold, Braintree FPA, etc.)

**Layer 1: CDN/WAF**
- [ ] Cloudflare (or equivalent) active
- [ ] Bot Fight Mode enabled
- [ ] Turnstile/reCAPTCHA on checkout
- [ ] High-risk ASN challenges configured
- [ ] JS challenges on payment endpoints

**Layer 2: Bot Mitigation**
- [ ] Managed solution in place (DataDome, HUMAN, Arkose, Kasada)?
- [ ] If not, self-hosted alternative (Fail2Ban, custom velocity)?

**Layer 3: Device Fingerprinting**
- [ ] FingerprintJS or equivalent implemented
- [ ] Fingerprint tied to transaction logging
- [ ] Repeat fingerprint detection active

**Layer 4: Logging & Monitoring**
- [ ] Failed payment logging (spikes detectable)
- [ ] Checkout POST pattern analysis
- [ ] Alerting configured (threshold-based)
- [ ] Dashboard for fraud metrics

**Layer 5: Checkout Hardening**
- [ ] Honeypot fields present
- [ ] Dynamic/rotating form field names
- [ ] CSRF tokens on all forms
- [ ] Behavioral detection (typing cadence, pointer movement)?

### Phase 4: Generate Report
Use template from `assets/audit-report-template.md`

### Phase 5: Create GitHub Issues
For each HIGH or CRITICAL finding, generate issue using `scripts/create-github-issues.py`

---

## File References

| File | Purpose | When to Load |
|------|---------|--------------|
| `references/anti-carding-stack.md` | Full anti-carding knowledge base | Full audit, Phase 3 |
| `references/platform-checks.md` | Platform-specific security checks | Full audit, Phase 2 |
| `references/threat-intel.md` | Current attack patterns & mitigations | Full audit, context |
| `assets/audit-report-template.md` | Client-facing report template | Full audit, Phase 4 |
| `scripts/create-github-issues.py` | GitHub issue generator | Full audit, Phase 5 |
| `scripts/quick-scan.sh` | Automated quick scan | Quick scan mode |

---

## Severity Definitions

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 CRITICAL | Actively exploitable, data at risk | Block deploy. Fix immediately. |
| 🟠 HIGH | Significant risk, easy to exploit | Fix before deploy. |
| 🟡 MEDIUM | Moderate risk, requires conditions | Track, fix in next sprint. |
| 🟢 LOW | Minor issue, defense in depth | Document, fix when convenient. |

---

## Integration

This skill complements:
- `security-scan` skill (code review focus)
- `spec-writing` skill (security requirements in acceptance criteria)

For active infrastructure testing beyond this audit, recommend:
- OWASP ZAP for dynamic scanning
- Burp Suite for penetration testing
