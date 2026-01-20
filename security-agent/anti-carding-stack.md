# Anti-Carding Security Stack (2025)

Comprehensive defense-in-depth architecture for e-commerce fraud prevention.

## Architecture Overview

```
Internet Traffic
      ↓
┌─────────────────────────────┐
│  Layer 1: CDN/WAF           │  Cloudflare, Fastly, AWS WAF
│  - Rate limiting            │
│  - Bot challenges           │
│  - Geo/ASN filtering        │
└─────────────────────────────┘
      ↓
┌─────────────────────────────┐
│  Layer 2: Bot Mitigation    │  DataDome, HUMAN, Kasada, Arkose
│  - ML-based detection       │
│  - Behavioral analysis      │
│  - Challenge escalation     │
└─────────────────────────────┘
      ↓
┌─────────────────────────────┐
│  Layer 3: Application       │  Your code
│  - Device fingerprinting    │
│  - Velocity controls        │
│  - Honeypots               │
│  - Behavioral biometrics    │
└─────────────────────────────┘
      ↓
┌─────────────────────────────┐
│  Layer 4: Payment Gateway   │  Stripe, Braintree, Adyen
│  - AVS/CVV verification     │
│  - Fraud scoring            │
│  - 3D Secure               │
│  - Decline code analysis    │
└─────────────────────────────┘
      ↓
┌─────────────────────────────┐
│  Layer 5: Logging/Alerting  │  ELK, Datadog, Grafana
│  - Pattern detection        │
│  - Spike alerting           │
│  - Forensic analysis        │
└─────────────────────────────┘
```

---

## Layer 0: Payment Processor Controls (MANDATORY)

These are table-stakes. If missing, stop everything and fix.

### AVS (Address Verification System)
- Compares billing address with card issuer records
- Available in US, Canada, UK
- Configuration: Reject on full mismatch, flag on partial

**Stripe**:
```javascript
// stripe.confirmCardPayment with AVS
const paymentIntent = await stripe.paymentIntents.create({
  amount: 1000,
  currency: 'usd',
  payment_method_options: {
    card: {
      request_three_d_secure: 'automatic',
    },
  },
});
// Check result.charges.data[0].payment_method_details.card.checks.address_line1_check
```

**Braintree**:
```javascript
// AVS response codes in transaction result
// transaction.avsPostalCodeResponseCode
// transaction.avsStreetAddressResponseCode
// M = Match, N = No Match, U = Unavailable
```

### CVV Verification
- 3-4 digit code on card
- Must NEVER be stored
- Always require on first transaction

### Velocity Controls
Configure at processor level:

| Rule | Threshold | Action |
|------|-----------|--------|
| Same card, multiple attempts | 3 in 10 min | Block 1 hour |
| Same IP, different cards | 5 in 1 hour | Challenge + review |
| Same device, new cards | 3 in 24 hours | Block device |
| High-value first order | >$500 new customer | 3DS or manual review |

### BIN/IP Geolocation Mismatch
- BIN (first 6 digits) indicates issuing country
- Compare to IP geolocation
- Flag if mismatch >1000 miles

### Fraud Scoring

**Stripe Radar**:
- Built-in ML scoring
- Default rules + custom rules
- Score 0-100 (higher = riskier)
- Recommended: Block >75, review 50-75

**Braintree Fraud Protection Advanced**:
- Risk threshold configuration
- Anti-carding velocity filters
- Device fingerprinting integration

**Adyen Risk**:
- ShopperReference tracking
- Risk score with custom rules
- RevenueProtect module

---

## Layer 1: CDN/WAF Configuration

### Cloudflare Hardening Checklist

**Bot Fight Mode**: Enable in Security → Bots
- Challenges known bot signatures
- Free tier available

**Turnstile (Recommended over reCAPTCHA)**:
```html
<!-- Invisible challenge on checkout -->
<div class="cf-turnstile" data-sitekey="YOUR_SITE_KEY" data-callback="onTurnstileSuccess"></div>
```

**WAF Rules for Checkout**:
```
# Block known carding user agents
(http.user_agent contains "curl") or 
(http.user_agent contains "python-requests") or
(http.user_agent contains "wget") or
(http.user_agent eq "")

# Challenge high-risk ASNs (data centers, VPNs)
# AS14061 (DigitalOcean), AS16509 (AWS), AS15169 (Google Cloud)
(ip.geoip.asnum in {14061 16509 15169 13335})

# Rate limit checkout endpoint
# 10 requests per minute per IP
(http.request.uri.path contains "/checkout" or 
 http.request.uri.path contains "/cart/add" or
 http.request.uri.path contains "/api/payment")
```

**JS Challenge on Payment Endpoints**:
- Forces browser execution
- Blocks headless scrapers
- Configure in Page Rules or WAF

### Alternative WAFs

**AWS WAF**:
- Managed rule groups: AWSManagedRulesCommonRuleSet, AWSManagedRulesBotControlRuleSet
- Rate-based rules for velocity

**Fastly**:
- Signal Sciences integration
- Custom VCL for advanced logic

---

## Layer 2: Managed Bot Mitigation

For serious e-commerce, managed solutions outperform DIY.

### Vendor Comparison (2025)

| Vendor | Strength | Best For | Pricing |
|--------|----------|----------|---------|
| DataDome | Real-time, low latency | High-traffic sites | $$$ |
| HUMAN Bot Defender | Behavioral analysis | Account takeover + carding | $$$ |
| Kasada | Proof-of-work challenges | Sophisticated attacks | $$$ |
| Arkose Labs | Adaptive challenges | User-friendly challenges | $$$ |
| Cloudflare Bot Mgmt | Integrated with CDN | Cloudflare users | $$ |

### Self-Hosted Alternatives

**Fail2Ban** (Linux):
```ini
# /etc/fail2ban/jail.local
[payment-failures]
enabled = true
port = http,https
filter = payment-failures
logpath = /var/log/app/payments.log
maxretry = 5
findtime = 300
bantime = 3600
```

```ini
# /etc/fail2ban/filter.d/payment-failures.conf
[Definition]
failregex = Payment failed.*IP: <HOST>
            Card declined.*IP: <HOST>
            AVS mismatch.*IP: <HOST>
```

**Custom Velocity Logic** (Node.js example):
```javascript
const redis = require('redis');
const client = redis.createClient();

async function checkVelocity(identifier, limit, windowSeconds) {
  const key = `velocity:${identifier}`;
  const count = await client.incr(key);
  if (count === 1) {
    await client.expire(key, windowSeconds);
  }
  return count <= limit;
}

// Usage in checkout
const cardAllowed = await checkVelocity(`card:${cardFingerprint}`, 3, 600);
const ipAllowed = await checkVelocity(`ip:${clientIP}`, 10, 3600);
const deviceAllowed = await checkVelocity(`device:${deviceFingerprint}`, 5, 86400);

if (!cardAllowed || !ipAllowed || !deviceAllowed) {
  throw new Error('Velocity limit exceeded');
}
```

---

## Layer 3: Device Fingerprinting

### FingerprintJS (Recommended)
```javascript
import FingerprintJS from '@fingerprintjs/fingerprintjs';

const fpPromise = FingerprintJS.load();

async function getFingerprint() {
  const fp = await fpPromise;
  const result = await fp.get();
  return result.visitorId; // Stable across sessions
}

// Send with payment request
const fingerprint = await getFingerprint();
fetch('/api/checkout', {
  method: 'POST',
  body: JSON.stringify({
    ...orderData,
    deviceFingerprint: fingerprint
  })
});
```

### Server-Side Fingerprint Validation
```javascript
// Track fingerprints in database
async function validateFingerprint(fingerprint, action) {
  const record = await db.fingerprints.findOne({ id: fingerprint });
  
  if (!record) {
    // New device - higher scrutiny
    await db.fingerprints.create({ 
      id: fingerprint, 
      firstSeen: new Date(),
      actions: [action]
    });
    return { risk: 'medium', isNew: true };
  }
  
  // Check for suspicious patterns
  const recentActions = record.actions.filter(
    a => a.timestamp > Date.now() - 3600000
  );
  
  if (recentActions.filter(a => a.type === 'payment_attempt').length > 5) {
    return { risk: 'high', reason: 'excessive_payment_attempts' };
  }
  
  return { risk: 'low' };
}
```

### Alternative: PantherJS
Open-source device fingerprinting. Less accurate but free.

---

## Layer 4: Checkout Hardening

### Honeypot Fields
```html
<form id="checkout">
  <!-- Visible fields -->
  <input type="text" name="email" required>
  <input type="text" name="card_number" required>
  
  <!-- Honeypot (hidden from real users) -->
  <div style="position: absolute; left: -9999px;">
    <input type="text" name="website" tabindex="-1" autocomplete="off">
  </div>
</form>
```

```javascript
// Server-side check
if (req.body.website) {
  // Bot detected - log and reject silently
  logSuspiciousActivity(req);
  return res.json({ success: true }); // Don't reveal detection
}
```

### Dynamic Field Names
```javascript
// Generate per-session field names
const sessionToken = crypto.randomBytes(16).toString('hex');
const fieldMap = {
  card_number: `cn_${sessionToken.slice(0, 8)}`,
  cvv: `cv_${sessionToken.slice(8, 16)}`,
  expiry: `ex_${sessionToken.slice(16, 24)}`
};

// Store mapping in session
req.session.fieldMap = fieldMap;

// Render form with dynamic names
res.render('checkout', { fieldMap });
```

### Behavioral Biometrics
```javascript
// Track typing patterns
let keyTimings = [];
let lastKeyTime = null;

document.getElementById('card-number').addEventListener('keydown', (e) => {
  const now = Date.now();
  if (lastKeyTime) {
    keyTimings.push(now - lastKeyTime);
  }
  lastKeyTime = now;
});

// Track mouse movement
let mouseMovements = [];
document.addEventListener('mousemove', (e) => {
  mouseMovements.push({ x: e.clientX, y: e.clientY, t: Date.now() });
});

// Analyze before submit
function analyzeBehavior() {
  // Bots type too fast and too consistently
  const avgTypingSpeed = keyTimings.reduce((a, b) => a + b, 0) / keyTimings.length;
  const typingVariance = calculateVariance(keyTimings);
  
  // Bots have no or robotic mouse movement
  const hasNaturalMouse = mouseMovements.length > 10 && 
    !isLinearPath(mouseMovements);
  
  return {
    avgTypingSpeed,
    typingVariance,
    hasNaturalMouse,
    isSuspicious: avgTypingSpeed < 50 || typingVariance < 10 || !hasNaturalMouse
  };
}
```

### 3D Secure Implementation
```javascript
// Stripe 3DS
const { error, paymentIntent } = await stripe.confirmCardPayment(
  clientSecret,
  {
    payment_method: {
      card: cardElement,
      billing_details: { name: 'Customer Name' }
    }
  }
);

// Handle 3DS challenge
if (error) {
  if (error.type === 'card_error' && error.code === 'authentication_required') {
    // 3DS challenge needed - Stripe handles UI
  }
}
```

---

## Layer 5: Logging & Alerting

### Key Metrics to Track

| Metric | Normal | Alert Threshold |
|--------|--------|-----------------|
| Decline rate | 5-10% | >20% in 1 hour |
| AVS mismatch rate | 2-5% | >15% in 1 hour |
| Same card attempts | 1-2/day | >5 in 10 minutes |
| New device % | 30-50% | >80% in 1 hour |
| Checkout abandonment | 60-70% | N/A (context-dependent) |

### Log Schema (Structured)
```json
{
  "timestamp": "2025-01-08T10:30:00Z",
  "event": "payment_attempt",
  "outcome": "declined",
  "decline_reason": "avs_mismatch",
  "amount": 49.99,
  "currency": "USD",
  "card_fingerprint": "abc123...",
  "device_fingerprint": "def456...",
  "ip_address": "203.0.113.42",
  "ip_country": "US",
  "ip_asn": 12345,
  "bin_country": "CA",
  "user_agent": "Mozilla/5.0...",
  "session_id": "sess_xyz",
  "behavioral_score": 0.7
}
```

### Alerting Rules (Grafana/Datadog)

```yaml
# Alert: Decline spike
- name: payment_decline_spike
  condition: rate(payment_declines[5m]) > 2 * avg(rate(payment_declines[1h]))
  severity: high
  notify: [slack-security, pagerduty]

# Alert: Carding attack pattern
- name: carding_attack_detected
  condition: |
    count(payment_attempts{outcome="declined"} by card_fingerprint)[10m] > 3
    AND count(distinct(card_fingerprint))[10m] > 10
  severity: critical
  notify: [slack-security, pagerduty, email-oncall]
```

---

## Implementation Timeline

### Week 1: Foundation
- [ ] Audit current payment processor settings
- [ ] Enable AVS, CVV requirements
- [ ] Configure basic velocity rules
- [ ] Set up Cloudflare (if not present)
- [ ] Create monitoring dashboard

### Week 2: Bot Mitigation
- [ ] Deploy Turnstile on checkout
- [ ] Implement device fingerprinting
- [ ] Add backend velocity controls
- [ ] Enable WAF rules for checkout

### Week 3: Logging Stack
- [ ] Deploy structured logging
- [ ] Set up alerting thresholds
- [ ] Configure Fail2Ban (if applicable)
- [ ] Create incident response playbook

### Week 4: Hardening & Testing
- [ ] Add honeypots to forms
- [ ] Implement behavioral detection
- [ ] Test with simulated attacks
- [ ] Tune false positive rates
- [ ] Document final architecture

---

## Incident Response

When attack detected:

1. **Immediate** (0-5 min)
   - Enable stricter rate limits
   - Block identified IPs/ASNs
   - Enable 3DS on all transactions

2. **Short-term** (5-30 min)
   - Analyze attack patterns
   - Block identified fingerprints
   - Notify payment processor

3. **Post-incident** (1-24 hours)
   - Full forensic analysis
   - Update WAF rules
   - Document lessons learned
   - Adjust alerting thresholds
