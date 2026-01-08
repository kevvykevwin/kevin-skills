# llms.txt Template

A template for creating llms.txt files to help AI systems understand site content.

---

## What is llms.txt?

A markdown file at your site root (`https://domain.com/llms.txt`) that provides AI systems with:
- Structured summary of site content
- Pointers to key pages
- Context about the organization

**Status:** Emerging standard, not yet widely adopted by AI platforms. Low effort to implement, directional benefit.

---

## Basic Template

```markdown
# {{Company Name}}

> {{One paragraph description of what the company does, who it serves, and its key value proposition.}}

## Main Pages

- [Homepage](https://{{domain}}/): {{Brief description}}
- [About](https://{{domain}}/about): {{Brief description}}
- [Products](https://{{domain}}/products): {{Brief description}}
- [Contact](https://{{domain}}/contact): {{Brief description}}

## Products / Services

- [{{Product 1}}](https://{{domain}}/products/{{slug}}): {{What it is, who it's for}}
- [{{Product 2}}](https://{{domain}}/products/{{slug}}): {{What it is, who it's for}}
- [{{Service 1}}](https://{{domain}}/services/{{slug}}): {{What it is, who it's for}}

## Resources

- [Blog](https://{{domain}}/blog): {{Topics covered}}
- [FAQ](https://{{domain}}/faq): {{Common questions answered}}
- [Help Center](https://{{domain}}/help): {{Support documentation}}

## Key Information

- **Founded:** {{Year}}
- **Headquarters:** {{City, State/Country}}
- **Industry:** {{Industry}}
- **Contact:** {{email}} | {{phone}}
```

---

## E-Commerce Template

```markdown
# {{Store Name}}

> {{Store Name}} is an online retailer specializing in {{product category}}. We serve {{target audience}} with {{key differentiator/value prop}}.

## Shop

- [All Products](https://{{domain}}/shop): Browse our full catalog
- [{{Category 1}}](https://{{domain}}/collections/{{slug}}): {{Description}}
- [{{Category 2}}](https://{{domain}}/collections/{{slug}}): {{Description}}
- [Best Sellers](https://{{domain}}/collections/best-sellers): Our most popular items
- [New Arrivals](https://{{domain}}/collections/new): Latest additions

## Featured Products

- [{{Product Name}}](https://{{domain}}/products/{{slug}}): {{Brief description, price point}}
- [{{Product Name}}](https://{{domain}}/products/{{slug}}): {{Brief description, price point}}

## Customer Information

- [Shipping & Returns](https://{{domain}}/policies/shipping): {{Key policies summary}}
- [Size Guide](https://{{domain}}/pages/size-guide): How to find your size
- [FAQ](https://{{domain}}/pages/faq): Common questions
- [Contact Us](https://{{domain}}/pages/contact): {{Support hours, methods}}

## About

- [Our Story](https://{{domain}}/pages/about): {{Brief company background}}
- [Sustainability](https://{{domain}}/pages/sustainability): {{If applicable}}
- [Reviews](https://{{domain}}/pages/reviews): Customer testimonials

## Key Information

- **Founded:** {{Year}}
- **Based in:** {{Location}}
- **Specializes in:** {{Product focus}}
- **Ships to:** {{Regions}}
```

---

## SaaS / B2B Template

```markdown
# {{Product Name}}

> {{Product Name}} is a {{product category}} that helps {{target users}} {{key benefit}}. {{Brief differentiator}}.

## Product

- [Features](https://{{domain}}/features): Core capabilities
- [Pricing](https://{{domain}}/pricing): Plans and pricing
- [Integrations](https://{{domain}}/integrations): Connected tools
- [Security](https://{{domain}}/security): Data protection and compliance
- [Changelog](https://{{domain}}/changelog): Recent updates

## Solutions

- [For {{Use Case 1}}](https://{{domain}}/solutions/{{slug}}): {{How product addresses this}}
- [For {{Industry 1}}](https://{{domain}}/industries/{{slug}}): {{Industry-specific benefits}}
- [For {{Team Type}}](https://{{domain}}/teams/{{slug}}): {{Team-specific features}}

## Resources

- [Documentation](https://{{domain}}/docs): Technical guides and API reference
- [Blog](https://{{domain}}/blog): Industry insights and product updates
- [Case Studies](https://{{domain}}/customers): Customer success stories
- [Webinars](https://{{domain}}/resources/webinars): Educational content

## Support

- [Help Center](https://{{domain}}/help): Self-service support
- [API Reference](https://{{domain}}/docs/api): Developer documentation
- [Status Page](https://status.{{domain}}): System status
- [Contact Support](https://{{domain}}/contact): Get help

## Company

- [About Us](https://{{domain}}/about): Our mission and team
- [Careers](https://{{domain}}/careers): Open positions
- [Press](https://{{domain}}/press): News and media

## Key Information

- **Category:** {{Software category}}
- **Best for:** {{Primary use case}}
- **Pricing:** {{Starting price or model}}
- **Free trial:** {{Yes/No, duration}}
```

---

## Local Business Template

```markdown
# {{Business Name}}

> {{Business Name}} is a {{business type}} located in {{City, State}}. We {{primary service/offering}} for {{target customers}}.

## Services

- [{{Service 1}}](https://{{domain}}/services/{{slug}}): {{Description}}
- [{{Service 2}}](https://{{domain}}/services/{{slug}}): {{Description}}
- [All Services](https://{{domain}}/services): Complete service list

## Location & Hours

- **Address:** {{Full address}}
- **Phone:** {{Phone number}}
- **Hours:** {{Operating hours}}
- [Directions](https://{{domain}}/directions): How to find us
- [Book Appointment](https://{{domain}}/book): Schedule online

## About

- [Our Team](https://{{domain}}/team): Meet our staff
- [Reviews](https://{{domain}}/reviews): Customer testimonials
- [About Us](https://{{domain}}/about): Our story

## Resources

- [FAQ](https://{{domain}}/faq): Common questions
- [Blog](https://{{domain}}/blog): Tips and news
- [Contact](https://{{domain}}/contact): Get in touch

## Key Information

- **Type:** {{Business category}}
- **Serving:** {{Service area}}
- **Established:** {{Year}}
- **Specialties:** {{Key services}}
```

---

## Implementation Steps

### 1. Create the file
Save as `llms.txt` in your site's root directory.

### 2. Verify accessibility
Test: `https://yourdomain.com/llms.txt` should load the file.

### 3. Keep it updated
Review quarterly or when major site changes occur.

---

## Best Practices

**Do:**
- Keep descriptions concise (1-2 sentences max)
- Link to actual pages (not just anchors)
- Include only public, important pages
- Update when site structure changes
- Use consistent formatting

**Don't:**
- Include every page (prioritize key content)
- Add marketing fluff
- Include login-required pages
- Use complex markdown (keep it simple)
- Let it get stale

---

## Validation

After creating, check:
1. File is accessible at root URL
2. All links work
3. Descriptions are accurate
4. Format renders correctly

---

## Related Files

llms.txt complements but doesn't replace:
- **robots.txt** - Crawler access rules
- **sitemap.xml** - Full URL inventory
- **Schema markup** - Structured data on pages

Think of llms.txt as the "executive summary" that points AI to your most important content.
