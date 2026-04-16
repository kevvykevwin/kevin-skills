# Custom Stack (Next.js / React) Security Checks

## Detection
- `next.config.js` or `next.config.mjs`
- `pages/` or `app/` directory structure
- No platform-specific dependencies

## Audit Checklist

### Environment Variables
- [ ] No secret keys in `NEXT_PUBLIC_*` variables
- [ ] Server-only secrets never passed through `env` in next.config.js
- [ ] `.env.local` in `.gitignore`
- [ ] Client-safe vars use `NEXT_PUBLIC_` prefix exclusively

### API Route Security
- [ ] HTTP method validation on all API routes
- [ ] CSRF token validation on state-changing endpoints
- [ ] Input validation and sanitization (Zod or equivalent)
- [ ] Rate limiting on sensitive endpoints (login, checkout, payment)
- [ ] Proper error responses (no stack traces to client)

### Authentication
- [ ] Protected routes have auth middleware
- [ ] Server-side session validation (not just client checks)
- [ ] Session expiry enforced
- [ ] Redirect to login on invalid/expired session

### Security Headers
Verify in next.config.js `headers()`:
- [ ] `Strict-Transport-Security` with includeSubDomains and preload
- [ ] `X-Frame-Options: SAMEORIGIN`
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] `Content-Security-Policy` restricting script/frame sources

### Server Components Security (App Router)
- [ ] Server-only secrets accessed only in Server Components
- [ ] `'use client'` components cannot access server secrets
- [ ] No sensitive data leaked through Server Component props to Client Components
- [ ] Server Actions validate auth and input

### Input Validation
- [ ] Schema validation on all API route inputs (Zod recommended)
- [ ] Proper type coercion (e.g., `z.number().int().positive()`)
- [ ] Address/email/phone fields validated with appropriate patterns
- [ ] Array inputs bounded (max length)

## Custom Stack Vulnerabilities
- Server/client boundary leaks
- CORS misconfiguration
- Missing CSRF protection
- Improper session management
- SSR hydration mismatches exposing data
