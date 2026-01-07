---
name: security-scan
description: Security checklist for code review. Catches common vulnerabilities before deploy. Use after build, during code-review, or as part of verification-loop. Covers auth, injection, secrets, and data exposure.
---

# Security Scan Skill

Catch embarrassing security holes before they ship.

## Core Philosophy

1. **Checklist beats memory** - Security issues are pattern-based; don't rely on remembering
2. **Defense in depth** - Multiple layers; one miss shouldn't be catastrophic
3. **Assume breach** - What's the blast radius if this is exploited?
4. **Client work = higher stakes** - Your reputation is on the line

## When to Use

- After build, before deploy
- During code review
- As part of verification-loop
- When touching auth, payments, or user data

## Security Checklist

### 1. Secrets & Configuration

| Check | Severity | How to Verify |
|-------|----------|---------------|
| No secrets in code | 🔴 Critical | `grep -r "password\|secret\|api_key\|token" --include="*.{js,ts,py,go}"` |
| No secrets in git history | 🔴 Critical | Check `.gitignore`, review past commits |
| Secrets in environment variables | 🔴 Critical | Verify `.env` is gitignored, production uses secure vault |
| No hardcoded URLs with credentials | 🔴 Critical | Search for `://.*:.*@` patterns |
| Sensitive config not logged | 🟡 High | Check logging statements |

### 2. Authentication & Authorization

| Check | Severity | How to Verify |
|-------|----------|---------------|
| Auth required on protected routes | 🔴 Critical | Trace each endpoint, verify middleware |
| Password hashing (bcrypt/argon2) | 🔴 Critical | Check auth implementation, never plain text or MD5/SHA |
| Session tokens are secure | 🔴 Critical | HttpOnly, Secure flags, reasonable expiry |
| Auth checks can't be bypassed | 🔴 Critical | Test with missing/invalid/expired tokens |
| Rate limiting on auth endpoints | 🟡 High | Verify login/register have limits |
| No auth logic in client-side only | 🔴 Critical | Server must validate, not just UI |

### 3. Injection Attacks

| Check | Severity | How to Verify |
|-------|----------|---------------|
| SQL injection prevented | 🔴 Critical | Parameterized queries only, no string concatenation |
| NoSQL injection prevented | 🔴 Critical | Sanitize query operators (`$gt`, `$where`, etc.) |
| Command injection prevented | 🔴 Critical | No `exec()`, `system()`, `eval()` with user input |
| XSS prevented | 🔴 Critical | Output encoding, CSP headers, no `dangerouslySetInnerHTML` with user data |
| Path traversal prevented | 🟡 High | Validate file paths, no `../` in user input |

### 4. Data Exposure

| Check | Severity | How to Verify |
|-------|----------|---------------|
| Sensitive data not in URLs | 🟡 High | No tokens, passwords, PII in query params |
| API responses don't over-share | 🟡 High | Return only needed fields, not full DB objects |
| Error messages don't leak info | 🟡 High | Generic errors to client, detailed logs server-side |
| Debug mode off in production | 🟡 High | Check framework config |
| HTTPS enforced | 🔴 Critical | Redirect HTTP → HTTPS, HSTS header |

### 5. Input Validation

| Check | Severity | How to Verify |
|-------|----------|---------------|
| All user input validated server-side | 🔴 Critical | Client validation is UX, server validation is security |
| File uploads validated | 🔴 Critical | Check MIME type, extension, size limits |
| JSON/XML parsing safe | 🟡 High | Disable external entities (XXE), limit depth |
| Redirect URLs validated | 🟡 High | No open redirects to arbitrary domains |

### 6. Dependencies

| Check | Severity | How to Verify |
|-------|----------|---------------|
| No known vulnerable packages | 🟡 High | `npm audit` / `pip-audit` / `cargo audit` |
| Dependencies pinned | 🟢 Medium | Lock files committed, no `*` versions |
| Unused dependencies removed | 🟢 Medium | Smaller attack surface |

## Quick Scan Commands

```bash
# Secrets scan
grep -rn "password\|secret\|api_key\|token\|private_key" --include="*.{js,ts,py,jsx,tsx}" .

# Dangerous functions (JS/TS)
grep -rn "eval\|dangerouslySetInnerHTML\|innerHTML" --include="*.{js,ts,jsx,tsx}" .

# SQL injection risk (raw queries)
grep -rn "query\|execute\|raw" --include="*.{js,ts,py}" . | grep -v "parameterized"

# Dependency vulnerabilities
npm audit          # Node.js
pip-audit          # Python
cargo audit        # Rust
```

## Severity Response

| Severity | Action |
|----------|--------|
| 🔴 Critical | Block deploy. Fix immediately. |
| 🟡 High | Fix before deploy if possible. Document if not. |
| 🟢 Medium | Track for next iteration. |

## Scan Output Template

After scanning, report:

```markdown
## Security Scan Results

**Scanned:** [files/paths]
**Date:** [timestamp]

### Critical Issues (Block Deploy)
| Issue | Location | Remediation |
|-------|----------|-------------|
| [finding] | [file:line] | [how to fix] |

### High Issues (Fix Before Deploy)
| Issue | Location | Remediation |
|-------|----------|-------------|
| [finding] | [file:line] | [how to fix] |

### Medium Issues (Track)
| Issue | Location | Remediation |
|-------|----------|-------------|
| [finding] | [file:line] | [how to fix] |

### Passed Checks
- [x] No secrets in code
- [x] Auth on protected routes
- [x] ... (list what passed)

### Not Applicable
- [ ] [Check] - [reason, e.g., "no file uploads in this feature"]
```

## Common Fixes

| Issue | Quick Fix |
|-------|-----------|
| Secret in code | Move to `.env`, add to `.gitignore` |
| SQL injection | Use ORM or parameterized queries |
| XSS | Use framework's auto-escaping, add CSP header |
| Missing auth | Add middleware, verify on every protected route |
| Vulnerable dependency | `npm update [package]` or pin safe version |

## Integration

Pairs with:
- `verification-loop` skill - Include security scan in verification
- `code-review` - Security is part of review checklist
- `spec-writing` - Security requirements can be in acceptance criteria
