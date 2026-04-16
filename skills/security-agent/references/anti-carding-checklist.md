# Anti-Carding Security Checklist

Defense-in-depth architecture for e-commerce fraud prevention.

## Architecture Overview

```
Internet Traffic
      |
+-----------------------------+
|  Layer 1: CDN/WAF           |  Cloudflare, Fastly, AWS WAF
|  - Rate limiting            |
|  - Bot challenges           |
|  - Geo/ASN filtering        |
+-----------------------------+
      |
+-----------------------------+
|  Layer 2: Bot Mitigation    |  DataDome, HUMAN, Kasada, Arkose
|  - ML-based detection       |
|  - Behavioral analysis      |
|  - Challenge escalation     |
+-----------------------------+
      |
+-----------------------------+
|  Layer 3: Application       |  Your code
|  - Device fingerprinting    |
|  - Velocity controls        |
|  - Honeypots               |
|  - Behavioral biometrics    |
+-----------------------------+
      |
+-----------------------------+
|  Layer 4: Payment Gateway   |  Stripe, Braintree, Adyen
|  - AVS/CVV verification     |
|  - Fraud scoring            |
|  - 3D Secure               |
|  - Decline code analysis    |
+-----------------------------+
      |
+-----------------------------+
|  Layer 5: Logging/Alerting  |  ELK, Datadog, Grafana
|  - Pattern detection        |
|  - Spike alerting           |
|  - Forensic analysis        |
+-----------------------------+
```

---

## Layer 0: Payment Processor Controls (MANDATORY)

Table stakes. If missing, stop and fix immediately.

### AVS (Address Verification System)
- [ ] AVS enabled and enforced
- [ ] Reject on full mismatch, flag on partial
- [ ] Available markets covered (US, Canada, UK)

### CVV Verification
- [ ] CVV required on all first transactions
- [ ] CVV never stored post-authorization

### Velocity Controls

| Rule | Threshold | Action |
|------|-----------|--------|
| Same card, multiple attempts | 3 in 10 min | Block 1 hour |
| Same IP, different cards | 5 in 1 hour | Challenge + review |
| Same device, new cards | 3 in 24 hours | Block device |
| High-value first order | >$500 new customer | 3DS or manual review |

### BIN/IP Geolocation Mismatch
- [ ] BIN country compared to IP geolocation
- [ ] Flag if mismatch >1000 miles

### Fraud Scoring
- [ ] Stripe Radar: block >75, review 50-75 (score 0-100)
- [ ] Braintree FPA: risk threshold + anti-carding velocity filters configured
- [ ] Adyen RevenueProtect: ShopperReference tracking + custom risk rules

---

## Layer 1: CDN/WAF

- [ ] Bot Fight Mode enabled (Cloudflare: Security > Bots)
- [ ] Turnstile or reCAPTCHA on checkout page
- [ ] WAF rules block known carding user agents (curl, python-requests, wget, empty UA)
- [ ] High-risk ASN challenges configured (datacenter IPs)
- [ ] JS challenge enabled on payment endpoints
- [ ] Rate limit on checkout/cart/payment API (e.g., 10 req/min/IP)

---

## Layer 2: Bot Mitigation

- [ ] Managed solution evaluated (DataDome, HUMAN, Kasada, Arkose, Cloudflare Bot Mgmt)
- [ ] If no managed solution: self-hosted alternative in place (Fail2Ban, custom velocity)
- [ ] Payment failure patterns trigger IP blocking

---

## Layer 3: Device Fingerprinting

- [ ] FingerprintJS or equivalent implemented
- [ ] Fingerprint sent with payment requests
- [ ] Fingerprint-to-transaction logging active
- [ ] Repeat fingerprint with multiple cards flagged
- [ ] New device = higher scrutiny on first transaction

---

## Layer 4: Checkout Hardening

- [ ] Honeypot fields present (hidden from real users)
- [ ] Bots filling honeypot silently rejected (no error revealed)
- [ ] Dynamic/rotating form field names per session
- [ ] CSRF tokens on all forms
- [ ] Behavioral biometrics considered (typing cadence, pointer movement)
- [ ] 3D Secure enabled for high-risk transactions

---

## Layer 5: Logging & Alerting

### Key Metrics

| Metric | Normal | Alert Threshold |
|--------|--------|-----------------|
| Decline rate | 5-10% | >20% in 1 hour |
| AVS mismatch rate | 2-5% | >15% in 1 hour |
| Same card attempts | 1-2/day | >5 in 10 minutes |
| New device % | 30-50% | >80% in 1 hour |
| Checkout abandonment | 60-70% | Context-dependent |

### Checklist
- [ ] Structured payment event logging (timestamp, outcome, fingerprints, IP, BIN)
- [ ] Decline spike detection configured
- [ ] Alerting thresholds set (Slack/PagerDuty)
- [ ] Fraud metrics dashboard operational
- [ ] Log retention meets compliance requirements
