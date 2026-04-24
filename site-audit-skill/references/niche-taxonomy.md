# Niche Taxonomy Reference

## Purpose
This file defines the standard niche categories Agent E uses when detecting which industries a firm currently serves and identifying invisible opportunities. Detect presence by looking for industry-specific vocabulary, pain points, job titles, and service framings in the crawled content.

---

## Standard Niche Categories

### 1. Real Estate & Construction
**Detection signals:** landlords, property investors, flips, short-term rentals, Airbnb, REIT, cost segregation, 1031 exchange, contractor, developer, builder, subcontractor, hard money, depreciation
**Common pain points:** passive loss rules, depreciation recapture, entity structure for properties, quarterly estimated taxes

### 2. Healthcare & Medical Practices
**Detection signals:** physician, doctor, medical practice, HIPAA, NPI, insurance billing, Medicare, Medicaid, medical group, hospital, healthcare provider, clinical, practice management
**Common pain points:** billing complexity, practice buy-ins, retirement plans for owners, revenue cycle management

### 3. Restaurants & Hospitality
**Detection signals:** restaurant, bar, cafe, brewery, food service, tips, POS system, food cost, catering, hotel, hospitality, franchise
**Common pain points:** tip reporting, food cost tracking, payroll complexity, cash flow seasonality

### 4. Dental Practices
**Detection signals:** dentist, dental practice, DSO, dental group, hygienist, orthodontist, oral surgeon, dental office, practice acquisition
**Common pain points:** practice purchase financing, buy-in/buy-out, equipment depreciation, owner compensation structure

### 5. Law Firms & Legal Professionals
**Detection signals:** attorney, law firm, lawyer, legal, IOLTA, trust accounting, partner compensation, bar association, billable hours, contingency
**Common pain points:** trust account compliance, partner draws, origination credit, multi-state practice

### 6. E-Commerce & Online Sellers
**Detection signals:** Amazon, eBay, Shopify, seller, FBA, online store, inventory, e-commerce, dropship, marketplace, sales tax nexus, reseller
**Common pain points:** sales tax nexus, inventory accounting, platform fee reconciliation, COGS tracking

### 7. Professional Services (Consultants, Coaches, Agencies)
**Detection signals:** consultant, coach, agency, freelancer, independent contractor, retainer, project-based, B2B services, professional services
**Common pain points:** quarterly estimated taxes, home office deduction, retirement plan setup, self-employment tax

### 8. Home Services (Contractors, Trades)
**Detection signals:** plumber, electrician, HVAC, roofer, landscaper, painter, contractor, handyman, trade, service company, fleet vehicle
**Common pain points:** job costing, vehicle deductions, subcontractor 1099s, cash flow management

### 9. Trucking & Logistics
**Detection signals:** trucking, logistics, fleet, owner-operator, DOT, CDL, carrier, freight, IFTA, per diem, transportation
**Common pain points:** IFTA reporting, per diem deductions, owner-operator entity structure, fleet depreciation

### 10. Tech Startups & SaaS
**Detection signals:** startup, SaaS, software, VC, venture, seed, Series A, ARR, MRR, equity, stock options, R&D credit, cap table
**Common pain points:** R&D tax credits, equity compensation, investor reporting, burn rate management

### 11. Creative Agencies & Marketing Firms
**Detection signals:** agency, creative, marketing, design, branding, PR, media, production, creative director, retainer clients
**Common pain points:** project profitability, owner compensation, S-corp election, multi-member LLC structure

### 12. Nonprofits
**Detection signals:** nonprofit, 501(c)(3), foundation, charity, donation, grant, fundraising, board of directors, Form 990, tax-exempt
**Common pain points:** Form 990 compliance, grant tracking, unrelated business income, board reporting

### 13. High-Net-Worth Individuals (HNWIs)
**Detection signals:** high net worth, wealth management, estate planning, trust, inheritance, family office, investment portfolio, multi-state, gift tax, charitable giving
**Common pain points:** estate planning, gift tax strategy, charitable structures, multi-state residency

---

## Detection Guidelines for Agent E

When analyzing crawled content:

1. **Confirmed niche** — Two or more detection signals are present, OR a service is explicitly named for the industry (e.g., "accounting for dental practices")
2. **Hinted niche** — One signal is present but not reinforced; note as "weak signal"
3. **Invisible niche** — No signals detected; evaluate whether the firm's general profile suggests this niche would be a natural fit (e.g., a rural firm near agricultural businesses might be a natural fit for farm accounting)

Always flag any niche signals not covered by this taxonomy. Add them to the `niches_detected` array with a note explaining the signal.
