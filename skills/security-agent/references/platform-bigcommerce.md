# BigCommerce Security Checks

## Detection
- `@bigcommerce/` packages in package.json
- Stencil CLI (`stencil.conf.js`)
- BigCommerce API endpoints in code

## Built-in Protections
- PCI DSS Level 1 compliant
- DDoS protection
- SSL enforced
- SaaS model (limited attack surface)

## Audit Checklist

### Store Settings
Path: `Settings > Security`
- [ ] 2FA enabled for all admin users
- [ ] IP allowlisting for admin (if available)
- [ ] Customer password requirements strong

### API Credentials
Path: `Settings > API > API accounts`
- [ ] Unused API accounts deleted
- [ ] OAuth scopes minimized per account
- [ ] Store API credentials rotated periodically
- [ ] Credentials never in frontend code (server-side only via env vars)

### Stencil Theme Security
- [ ] User input uses double-braces `{{}}` (escaped) not triple-braces `{{{}}}`
- [ ] JSON injection prevented in `<script>` tags
- [ ] Custom fields properly escaped before rendering

### Webhook Security
- [ ] Webhook signature verified (HMAC-SHA256 with client secret)
- [ ] Signature compared against `x-bc-webhook-signature` header
- [ ] Webhook payloads validated before processing

### Checkout Security
- [ ] Custom checkout scripts reviewed for data leaks
- [ ] No tracking pixels on payment step
- [ ] No localStorage/sessionStorage of card data

### App Permissions
Path: `Apps > My Apps`
- [ ] Each installed app reviewed
- [ ] OAuth scopes granted are minimal
- [ ] Unused apps removed

## BigCommerce-Specific Vulnerabilities
- API over-permissioning
- Stencil template injection
- Abandoned cart data exposure
- Third-party app data leaks
