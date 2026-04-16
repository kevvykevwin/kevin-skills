# Shopify Security Checks

## Detection
- `shopify` in package.json (Hydrogen/custom storefronts)
- `.shopify/` directory
- `*.liquid` template files
- `shopify.config.js` or `shopify.app.toml`

## Built-in Protections
- PCI DSS Level 1 compliant
- Automatic fraud analysis
- 3D Secure available
- SSL/TLS enforced

## Audit Checklist

### Shopify Payments Fraud Settings
Path: `Admin > Settings > Payments > Manage > Fraud Prevention`
- [ ] AVS verification enabled
- [ ] CVV verification required
- [ ] Address match requirement configured
- [ ] Fulfillment hold for high-risk orders enabled

### Third-Party Payment Providers
- [ ] Provider has equivalent fraud controls to Shopify Payments
- [ ] Webhook signatures validated (HMAC-SHA256 with timing-safe comparison)
- [ ] API keys stored in Shopify Secrets (not in theme code)

### Storefront API Security (Hydrogen/Headless)
- [ ] Admin API token never exposed in client bundle
- [ ] Only Storefront API with public token used client-side
- [ ] Server-side API calls use environment variables

### App Permissions Audit
Path: `Admin > Settings > Apps and sales channels > Develop apps`
- [ ] OAuth scopes reviewed for each app
- [ ] Unused apps removed
- [ ] Apps with `write_orders`, `write_customers`, `write_products` justified

### Webhook Security
- [ ] Webhook HMAC signature verified on all endpoints
- [ ] Timing-safe comparison used for signature validation
- [ ] Raw body used for HMAC computation (not parsed JSON)

### Theme Security (Liquid)
- [ ] User input escaped in Liquid templates (use `| escape` filter)
- [ ] JSON data properly escaped before injection into `<script>` tags
- [ ] Metafield values sanitized before rendering

## Shopify-Specific Vulnerabilities
- Theme code injection via metafields
- Unauthenticated Storefront API abuse
- Cart manipulation attacks
- Gift card brute-forcing
