# Detection Queries

Pre-built queries for identifying carding attacks and fraud patterns.

---

## Elasticsearch/OpenSearch

### Carding Attack Detection
```json
{
  "query": {
    "bool": {
      "must": [
        { "range": { "@timestamp": { "gte": "now-1h" } } },
        { "term": { "event_type": "payment_attempt" } },
        { "term": { "outcome": "declined" } }
      ]
    }
  },
  "aggs": {
    "by_ip": {
      "terms": { "field": "ip_address", "min_doc_count": 5 }
    },
    "by_device": {
      "terms": { "field": "device_fingerprint", "min_doc_count": 3 }
    }
  }
}
```

### BIN Attack Detection
```json
{
  "query": {
    "bool": {
      "must": [
        { "range": { "@timestamp": { "gte": "now-15m" } } },
        { "term": { "outcome": "declined" } }
      ]
    }
  },
  "aggs": {
    "by_bin": {
      "terms": {
        "field": "card_bin",
        "min_doc_count": 5,
        "order": { "_count": "desc" }
      }
    }
  }
}
```

---

## SQL (Relational Databases)

### Find Potential Carding Attacks (Last Hour)
```sql
SELECT
  ip_address,
  COUNT(*) as attempts,
  COUNT(DISTINCT card_fingerprint) as unique_cards,
  SUM(CASE WHEN outcome = 'declined' THEN 1 ELSE 0 END) as declines
FROM payment_attempts
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY ip_address
HAVING COUNT(*) > 10 AND COUNT(DISTINCT card_fingerprint) > 3
ORDER BY attempts DESC;
```

### Find Velocity Violations
```sql
SELECT
  device_fingerprint,
  COUNT(*) as attempts,
  MIN(created_at) as first_attempt,
  MAX(created_at) as last_attempt,
  EXTRACT(EPOCH FROM (MAX(created_at) - MIN(created_at))) as duration_seconds
FROM payment_attempts
WHERE created_at > NOW() - INTERVAL '10 minutes'
GROUP BY device_fingerprint
HAVING COUNT(*) > 5
ORDER BY attempts DESC;
```
