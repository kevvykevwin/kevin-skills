# Schema Templates for GEO

Copy-paste JSON-LD templates for common page types. Place in `<head>` or before closing `</body>`.

---

## Organization Schema (Homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{{Company Name}}",
  "url": "https://{{domain}}",
  "logo": "https://{{domain}}/logo.png",
  "description": "{{One sentence description of what company does}}",
  "foundingDate": "{{YYYY}}",
  "sameAs": [
    "https://www.linkedin.com/company/{{company}}",
    "https://twitter.com/{{handle}}",
    "https://www.facebook.com/{{page}}",
    "https://www.instagram.com/{{handle}}"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "{{+1-XXX-XXX-XXXX}}",
    "contactType": "customer service",
    "availableLanguage": ["English"]
  }
}
```

**When to use:** Homepage, About page
**AI benefit:** Establishes entity identity, helps AI understand what the company is

---

## Product Schema (Product Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{Product Name}}",
  "description": "{{Product description - 1-2 sentences}}",
  "image": "https://{{domain}}/images/{{product}}.jpg",
  "brand": {
    "@type": "Brand",
    "name": "{{Brand Name}}"
  },
  "sku": "{{SKU}}",
  "offers": {
    "@type": "Offer",
    "url": "https://{{domain}}/products/{{product-slug}}",
    "priceCurrency": "USD",
    "price": "{{XX.XX}}",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "{{Company Name}}"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{X.X}}",
    "reviewCount": "{{XXX}}"
  }
}
```

**When to use:** All product pages
**AI benefit:** Clear product entity definition, pricing, availability signals

---

## Product with Reviews

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{Product Name}}",
  "description": "{{Product description}}",
  "image": "https://{{domain}}/images/{{product}}.jpg",
  "brand": {
    "@type": "Brand",
    "name": "{{Brand Name}}"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{X.X}}",
    "reviewCount": "{{XXX}}"
  },
  "review": [
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "{{Reviewer Name}}"
      },
      "datePublished": "{{YYYY-MM-DD}}",
      "reviewBody": "{{Review text}}",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "{{X}}",
        "bestRating": "5"
      }
    }
  ]
}
```

---

## Article Schema (Blog Posts)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{Article Title}}",
  "description": "{{Meta description - 150-160 chars}}",
  "image": "https://{{domain}}/images/{{article-image}}.jpg",
  "datePublished": "{{YYYY-MM-DD}}",
  "dateModified": "{{YYYY-MM-DD}}",
  "author": {
    "@type": "Person",
    "name": "{{Author Name}}",
    "url": "https://{{domain}}/about/{{author-slug}}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{{Company Name}}",
    "logo": {
      "@type": "ImageObject",
      "url": "https://{{domain}}/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://{{domain}}/blog/{{article-slug}}"
  }
}
```

**When to use:** All blog posts, articles, guides
**AI benefit:** E-E-A-T signals via author attribution, recency via dates

---

## FAQPage Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{{Question 1}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{Answer 1 - can include basic HTML}}"
      }
    },
    {
      "@type": "Question",
      "name": "{{Question 2}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{Answer 2}}"
      }
    },
    {
      "@type": "Question",
      "name": "{{Question 3}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{Answer 3}}"
      }
    }
  ]
}
```

**When to use:** FAQ pages, product pages with common questions, category pages
**AI benefit:** Direct Q&A extraction, high citation potential for question-based queries

**Pro tip:** Mine "People Also Ask" for question phrasing. Use exact phrasing users search for.

---

## HowTo Schema

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "{{How to [Task]}}",
  "description": "{{Brief description of what this guide teaches}}",
  "image": "https://{{domain}}/images/{{guide-image}}.jpg",
  "totalTime": "PT{{X}}M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "{{XX}}"
  },
  "step": [
    {
      "@type": "HowToStep",
      "name": "{{Step 1 Title}}",
      "text": "{{Step 1 detailed instructions}}",
      "image": "https://{{domain}}/images/step1.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "{{Step 2 Title}}",
      "text": "{{Step 2 detailed instructions}}"
    },
    {
      "@type": "HowToStep",
      "name": "{{Step 3 Title}}",
      "text": "{{Step 3 detailed instructions}}"
    }
  ]
}
```

**When to use:** Tutorial content, guides, instruction pages
**AI benefit:** Structured steps are easily extracted for procedural queries

---

## LocalBusiness Schema

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{{Business Name}}",
  "description": "{{What the business does}}",
  "image": "https://{{domain}}/images/storefront.jpg",
  "url": "https://{{domain}}",
  "telephone": "{{+1-XXX-XXX-XXXX}}",
  "email": "{{email@domain.com}}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{123 Main St}}",
    "addressLocality": "{{City}}",
    "addressRegion": "{{ST}}",
    "postalCode": "{{XXXXX}}",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "{{XX.XXXXXX}}",
    "longitude": "{{-XX.XXXXXX}}"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "priceRange": "{{$$}}"
}
```

**When to use:** Local businesses, businesses with physical locations
**AI benefit:** Location-specific queries, "near me" searches

---

## BreadcrumbList Schema

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://{{domain}}"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "{{Category}}",
      "item": "https://{{domain}}/{{category}}"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{{Page Name}}",
      "item": "https://{{domain}}/{{category}}/{{page}}"
    }
  ]
}
```

**When to use:** All pages with hierarchical navigation
**AI benefit:** Site structure clarity, helps AI understand page relationships

---

## Validation

Always validate schema before deployment:
- **Google Rich Results Test:** https://search.google.com/test/rich-results
- **Schema.org Validator:** https://validator.schema.org/

Common errors:
- Missing required fields
- Invalid date formats (use YYYY-MM-DD)
- Broken image URLs
- Price without currency

---

## Implementation Notes

**Placement options:**
1. In `<head>` (preferred for most)
2. Before `</body>` (if head is constrained)
3. Multiple schemas on same page (separate `<script>` tags)

**For dynamic sites:**
- Ensure schema is server-rendered, not JS-injected
- Test with "View Source" not DevTools

**Combining schemas:**
For a product page with FAQ:
```json
[
  { "@context": "https://schema.org", "@type": "Product", ... },
  { "@context": "https://schema.org", "@type": "FAQPage", ... }
]
```
