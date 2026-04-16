# Cross-Platform Security Checks

Verify regardless of platform:

## HTTPS
- [ ] No mixed content warnings
- [ ] HSTS enabled with appropriate max-age
- [ ] Certificate valid and not expiring within 30 days

## Third-Party Scripts
- [ ] All external scripts audited and justified
- [ ] Subresource Integrity (SRI) on external scripts
- [ ] No unnecessary tracking scripts on checkout/payment pages

## Content Security Policy
- [ ] Script sources restricted (no `unsafe-eval` in production)
- [ ] Inline scripts minimized or nonced
- [ ] Report-only mode tested before enforcing

## Cookie Security
- [ ] HttpOnly on all session cookies
- [ ] Secure flag on all auth cookies
- [ ] SameSite=Strict or SameSite=Lax configured

## Error Handling
- [ ] No stack traces or debug info sent to client
- [ ] Generic error messages for users
- [ ] Detailed error logging server-side only
