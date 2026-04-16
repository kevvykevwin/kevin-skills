# WooCommerce Security Checks

## Detection
- `wp-content/plugins/woocommerce/` directory
- `wc-` prefixed database tables
- `woocommerce` in functions.php or plugin files

## Baseline Security (WordPress)
- [ ] WordPress core up to date
- [ ] WooCommerce plugin up to date
- [ ] PHP 8.x (not 7.x or lower)
- [ ] Strong admin passwords + 2FA enabled
- [ ] File permissions correct (644 files, 755 directories)
- [ ] `wp-config.php` above web root or access-protected

## Audit Checklist

### Payment Gateway Configuration
Path: `WooCommerce > Settings > Payments`
- [ ] Stripe/Braintree fraud tools enabled
- [ ] Test mode disabled in production
- [ ] API keys stored in wp-config.php, not in database

### WooCommerce Security Settings
- [ ] Webhook secrets are strong and rotated
- [ ] Unused webhooks deleted
- [ ] Account creation requires strong password
- [ ] Guest checkout security implications documented

### Plugin Security Audit
- [ ] All active plugins checked against WPScan vulnerability database
- [ ] Payment gateway plugins audited
- [ ] Plugins handling customer data reviewed
- [ ] Form plugins and SEO plugins checked for data leaks
- [ ] Unused plugins deactivated and removed

### REST API Security
- [ ] REST API access restricted to authenticated users (except public endpoints)
- [ ] Only necessary public endpoints allowed (`/wp/v2/products`, `/wc/store/`)
- [ ] Unauthenticated requests return 401 for restricted endpoints

### Checkout Security
- [ ] Rate limiting applied to checkout process
- [ ] IP-based velocity controls on payment attempts
- [ ] Transient-based or Redis-based rate limiting (not just session)

### Database Security
- [ ] No API keys or secrets stored in wp_options as plaintext
- [ ] No plaintext passwords in wp_users (all should be hashed)
- [ ] Database prefix changed from default `wp_`

## WooCommerce-Specific Vulnerabilities
- Plugin conflicts exposing data
- REST API user enumeration
- Order manipulation via cart
- Coupon code abuse
- Object injection in serialized data
