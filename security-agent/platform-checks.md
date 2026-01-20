# Platform-Specific Security Checks

Security considerations unique to each e-commerce platform.

---

## Shopify

### Detection
- `shopify` in package.json (Hydrogen/custom storefronts)
- `.shopify/` directory
- `*.liquid` template files
- `shopify.config.js` or `shopify.app.toml`

### Built-in Protections
Shopify handles most payment security automatically:
- ✅ PCI DSS Level 1 compliant
- ✅ Automatic fraud analysis
- ✅ 3D Secure available
- ✅ SSL/TLS enforced

### What to Check

**1. Shopify Payments Fraud Settings**
```
Admin → Settings → Payments → Manage → Fraud Prevention
```
- [ ] AVS verification enabled
- [ ] CVV verification required
- [ ] Address match requirement configured
- [ ] Fulfillment hold for high-risk orders enabled

**2. Third-Party Payment Providers**
If using non-Shopify payments:
- [ ] Provider has equivalent fraud controls
- [ ] Webhook signatures validated
- [ ] API keys stored in Shopify Secrets (not theme code)

**3. Storefront API Security (Hydrogen/Headless)**
```javascript
// BAD: Exposing admin API token
const client = new Shopify.Clients.Rest(
  shop,
  process.env.SHOPIFY_ADMIN_API_TOKEN // Never in client bundle!
);

// GOOD: Use Storefront API with public token
const client = createStorefrontClient({
  storeDomain: process.env.PUBLIC_STORE_DOMAIN,
  publicStorefrontToken: process.env.PUBLIC_STOREFRONT_TOKEN,
});
```

**4. App Permissions Audit**
```
Admin → Settings → Apps and sales channels → Develop apps
```
- [ ] Review OAuth scopes for each app
- [ ] Remove unused apps
- [ ] Check for apps with `write_orders`, `write_customers`, `write_products`

**5. Webhook Security**
```javascript
// Verify Shopify webhook signature
import crypto from 'crypto';

function verifyShopifyWebhook(req, secret) {
  const hmac = req.headers['x-shopify-hmac-sha256'];
  const hash = crypto
    .createHmac('sha256', secret)
    .update(req.rawBody, 'utf8')
    .digest('base64');
  return crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(hash));
}
```

**6. Theme Security (Liquid)**
```liquid
<!-- BAD: Unescaped user input -->
{{ customer.note }}

<!-- GOOD: Escaped by default, but verify -->
{{ customer.note | escape }}

<!-- BAD: JSON without escaping -->
<script>
  var data = {{ product | json }};
</script>

<!-- GOOD: Proper JSON escaping -->
<script>
  var data = JSON.parse({{ product | json | escape }});
</script>
```

### Shopify-Specific Vulnerabilities
- Theme code injection via metafields
- Unauthenticated Storefront API abuse
- Cart manipulation attacks
- Gift card brute-forcing

---

## WooCommerce

### Detection
- `wp-content/plugins/woocommerce/` directory
- `wc-` prefixed database tables
- `woocommerce` in functions.php or plugin files

### Baseline Security (WordPress)
- [ ] WordPress core up to date
- [ ] WooCommerce plugin up to date
- [ ] PHP 8.x (not 7.x or lower)
- [ ] Strong admin passwords + 2FA
- [ ] File permissions (644 files, 755 directories)
- [ ] `wp-config.php` above web root or protected

### What to Check

**1. Payment Gateway Configuration**
```
WooCommerce → Settings → Payments
```
- [ ] Stripe/Braintree fraud tools enabled
- [ ] Test mode disabled in production
- [ ] API keys in wp-config.php, not database

**2. WooCommerce Security Settings**
```
WooCommerce → Settings → Advanced → Webhooks
```
- [ ] Webhook secrets are strong
- [ ] Unused webhooks deleted

```
WooCommerce → Settings → Accounts & Privacy
```
- [ ] Account creation requires strong password
- [ ] Guest checkout implications understood

**3. Plugin Security Audit**
```bash
# Check for known vulnerable plugins
wp plugin list --status=active --format=csv | while read plugin; do
  echo "Checking: $plugin"
  # Cross-reference with WPScan vulnerability database
done
```

Critical plugins to audit:
- Any payment gateway plugin
- Any plugin handling customer data
- Form plugins (Contact Form 7, WPForms, etc.)
- SEO plugins (can leak data)

**4. REST API Security**
```php
// Restrict REST API access
add_filter('rest_authentication_errors', function($result) {
  if (!is_user_logged_in()) {
    // Allow specific public endpoints only
    $allowed = ['/wp/v2/products', '/wc/store/'];
    $request_uri = $_SERVER['REQUEST_URI'];
    foreach ($allowed as $endpoint) {
      if (strpos($request_uri, $endpoint) !== false) {
        return $result;
      }
    }
    return new WP_Error('rest_forbidden', 'Authentication required', ['status' => 401]);
  }
  return $result;
});
```

**5. Checkout Security**
```php
// Add rate limiting to checkout
add_action('woocommerce_before_checkout_process', function() {
  $ip = $_SERVER['REMOTE_ADDR'];
  $transient_key = 'checkout_attempts_' . md5($ip);
  $attempts = get_transient($transient_key) ?: 0;
  
  if ($attempts > 5) {
    wp_die('Too many checkout attempts. Please try again later.');
  }
  
  set_transient($transient_key, $attempts + 1, 300);
});
```

**6. Database Security**
```sql
-- Check for exposed customer data
SELECT * FROM wp_options WHERE option_name LIKE '%api_key%' OR option_name LIKE '%secret%';

-- Verify no plaintext passwords
SELECT ID, user_login FROM wp_users WHERE user_pass NOT LIKE '$P$%' AND user_pass NOT LIKE '$2y$%';
```

### WooCommerce-Specific Vulnerabilities
- Plugin conflicts exposing data
- REST API enumeration
- Order manipulation via cart
- Coupon code abuse
- Object injection in serialized data

---

## BigCommerce

### Detection
- `@bigcommerce/` packages in package.json
- Stencil CLI (`stencil.conf.js`)
- BigCommerce API endpoints in code

### Built-in Protections
- ✅ PCI DSS Level 1 compliant
- ✅ DDoS protection
- ✅ SSL enforced
- ✅ SaaS model (limited attack surface)

### What to Check

**1. Store Settings**
```
Settings → Security
```
- [ ] 2FA enabled for all admin users
- [ ] IP allowlisting for admin (if available)
- [ ] Customer password requirements strong

**2. API Credentials**
```
Settings → API → API accounts
```
- [ ] Unused API accounts deleted
- [ ] OAuth scopes minimized
- [ ] Store API credentials rotated periodically

```javascript
// Secure API credential handling
// BAD: Credentials in frontend code
const client = new BigCommerce({
  clientId: 'abc123',  // Never expose!
  accessToken: 'xyz789'
});

// GOOD: Server-side only
// api/bigcommerce.js (server route)
const client = new BigCommerce({
  clientId: process.env.BC_CLIENT_ID,
  accessToken: process.env.BC_ACCESS_TOKEN
});
```

**3. Stencil Theme Security**
```handlebars
{{!-- BAD: Unescaped output --}}
{{{customer.custom_field}}}

{{!-- GOOD: Escaped by default --}}
{{customer.custom_field}}

{{!-- Careful with JSON injection --}}
<script>
  // Ensure proper escaping
  var config = {{{json settings}}};
</script>
```

**4. Webhook Security**
```javascript
// Verify BigCommerce webhook
import crypto from 'crypto';

function verifyBigCommerceWebhook(req, clientSecret) {
  const payload = JSON.stringify(req.body);
  const signature = crypto
    .createHmac('sha256', clientSecret)
    .update(payload)
    .digest('base64');
  return signature === req.headers['x-bc-webhook-signature'];
}
```

**5. Checkout Security (Optimized One-Page Checkout)**
- Review custom checkout scripts
- Validate no tracking pixels on payment step
- Ensure no localStorage of card data

**6. App Permissions**
```
Apps → My Apps
```
- [ ] Review each installed app
- [ ] Check OAuth scopes granted
- [ ] Remove unused apps

### BigCommerce-Specific Vulnerabilities
- API over-permissioning
- Stencil template injection
- Abandoned cart data exposure
- Third-party app data leaks

---

## Custom Stack (Next.js / React)

### Detection
- `next.config.js` or `next.config.mjs`
- `pages/` or `app/` directory structure
- No platform-specific dependencies

### What to Check

**1. Environment Variables**
```javascript
// next.config.js
module.exports = {
  env: {
    // BAD: Exposes to client
    STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
    
    // GOOD: Public prefix for client-safe vars
    NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY,
  }
};
```

**2. API Route Security**
```javascript
// pages/api/checkout.js
export default async function handler(req, res) {
  // 1. Validate HTTP method
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  // 2. Validate CSRF token
  const csrfToken = req.headers['x-csrf-token'];
  if (!verifyCsrfToken(csrfToken, req.cookies.csrf)) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  
  // 3. Validate and sanitize input
  const { amount, currency, paymentMethod } = req.body;
  if (!Number.isInteger(amount) || amount <= 0) {
    return res.status(400).json({ error: 'Invalid amount' });
  }
  
  // 4. Rate limiting
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  if (await isRateLimited(ip)) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  
  // 5. Process payment...
}
```

**3. Authentication**
```javascript
// Middleware for protected routes
import { getServerSession } from 'next-auth';
import { authOptions } from './auth';

export async function middleware(req) {
  const session = await getServerSession(authOptions);
  
  if (!session) {
    return NextResponse.redirect('/login');
  }
  
  // Verify session is valid and not expired
  if (session.expires && new Date(session.expires) < new Date()) {
    return NextResponse.redirect('/login');
  }
  
  return NextResponse.next();
}
```

**4. Security Headers**
```javascript
// next.config.js
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Content-Security-Policy', value: "default-src 'self'; script-src 'self' 'unsafe-inline' https://js.stripe.com; frame-src https://js.stripe.com https://hooks.stripe.com;" },
];

module.exports = {
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  }
};
```

**5. Server Components Security (App Router)**
```javascript
// app/checkout/page.js
// Server component - safe for secrets
async function CheckoutPage() {
  // This runs on server only
  const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
  
  // Fetch data server-side
  const products = await getProducts();
  
  return <CheckoutForm products={products} />;
}

// 'use client' components can't access server secrets
```

**6. Input Validation**
```javascript
import { z } from 'zod';

const checkoutSchema = z.object({
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().int().positive().max(100),
  })),
  email: z.string().email(),
  shippingAddress: z.object({
    line1: z.string().min(1).max(200),
    city: z.string().min(1).max(100),
    state: z.string().length(2),
    postal_code: z.string().regex(/^\d{5}(-\d{4})?$/),
    country: z.string().length(2),
  }),
});

// In API route
const result = checkoutSchema.safeParse(req.body);
if (!result.success) {
  return res.status(400).json({ errors: result.error.issues });
}
```

### Custom Stack Vulnerabilities
- Server/client boundary leaks
- CORS misconfiguration
- Missing CSRF protection
- Improper session management
- SSR hydration mismatches exposing data

---

## Cross-Platform Checks

Regardless of platform, always verify:

1. **HTTPS Everywhere**
   - No mixed content
   - HSTS enabled
   - Certificate valid and not expiring soon

2. **Third-Party Scripts**
   - Audit all external scripts
   - Verify script integrity (SRI)
   - No unnecessary tracking on checkout

3. **Content Security Policy**
   - Restrict script sources
   - Block inline scripts where possible
   - Report-only mode for testing

4. **Cookie Security**
   - HttpOnly on session cookies
   - Secure flag on all auth cookies
   - SameSite=Strict or Lax

5. **Error Handling**
   - No stack traces to client
   - Generic error messages
   - Detailed logging server-side
