# Incident Response Playbooks

---

## Playbook 1: Active Carding Attack

**Trigger**: >50 declines in 10 min OR >20 unique cards from single IP/device

### Immediate (0-5 min)
1. Enable Cloudflare "Under Attack" mode
2. Reduce velocity limits to 3 attempts per IP per 10 min
3. Enable 3DS on all transactions
4. Alert on-call team

### Investigation (5-30 min)
1. Identify attack source (IP range, ASN, device fingerprints)
2. Check for successful transactions from same source
3. Review accounts created during attack window

### Blocking
1. Add identified IPs to WAF blocklist
2. Block identified device fingerprints
3. Report to payment processor

### Post-Incident
1. Analyze attack patterns for rule updates
2. Update detection rules and thresholds
3. Document in incident log

---

## Playbook 2: Account Takeover Attempt

**Trigger**: >10 failed logins for single account OR credential stuffing pattern

### Immediate
1. Lock affected account
2. Invalidate all active sessions
3. Send notification to account owner
4. Enable step-up auth for account

### Investigation
1. Check for successful logins during attack window
2. Review any changes made to account (email, password, address)
3. Check for orders placed during window

### Recovery
1. Force password reset
2. Review and revert unauthorized changes
3. Monitor account for follow-up attempts

---

## Playbook 3: Successful Fraudulent Transaction

**Trigger**: Chargeback received OR fraud flag from processor

### Immediate
1. Block associated card/device/IP
2. Hold pending orders from same source
3. Preserve all transaction data (forensic evidence)

### Investigation
1. Build full transaction timeline
2. Identify all associated accounts
3. Check delivery status (stop shipment if possible)

### Recovery
1. Document evidence for chargeback response
2. Update fraud rules to prevent recurrence
3. Report to law enforcement if significant loss
