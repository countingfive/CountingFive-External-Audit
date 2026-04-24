# Site Audit Skill — Design Document
**Date:** 2026-04-06
**Project:** CountingFive Site Audit
**Status:** Approved — Ready for Implementation

---

## Overview

A Cowork skill that takes a prospect's website URL as input and produces a branded PDF report and a Markdown file. The audit is designed as a client-facing sales tool — persuasive, accessible, and non-technical in tone — used by CountingFive to demonstrate value to prospects in the tax and accounting space.

---

## Goals

- Give CountingFive a repeatable, professional way to audit a prospect's site before or during a sales conversation
- Surface problems with the prospect's current site in a way that naturally maps to CountingFive's services
- Produce two artifacts automatically: a branded PDF and a `.md` file
- Run fully in Cowork — paste URL, walk away, come back to finished reports

---

## Architecture: Parallel Dispatch (Option B)

The skill uses parallel sub-agents to gather data simultaneously, then a synthesis agent scores and writes the report.

```
User pastes URL into Cowork
        ↓
Claude reads SKILL.md + config.json
        ↓
  ┌─────────────────────────────────────────────────────┐
  │              PARALLEL AGENTS                        │
  │                                                     │
  │  Agent A              Agent B          Agent C      │
  │  Google PageSpeed     Firecrawl        Google       │
  │  - Mobile score       - Full crawl     Search API   │
  │  - Core Web Vitals    - H1–H6 tags     - Keyword    │
  │  - Performance        - Schema/JSON-LD   rankings   │
  │  - Accessibility      - Tech stack     - Competitor │
  │                       - Broken links     positions  │
  │                       - Meta/OG tags               │
  │                       - Content audit  Agent D      │
  │                                        WHOIS        │
  │                                        - Domain age │
  │                                        - Registrar  │
  └─────────────────────────────────────────────────────┘
        ↓
Synthesis agent scores all results → letter grades + sub-scores
        ↓
  ┌──────────────────────────────┐
  │  OUTPUT (generated together) │
  │  Branded PDF                 │
  │  Markdown file               │
  └──────────────────────────────┘
```

---

## Config File (`config.json`)

All API keys and firm settings live in a single config file in the skill directory. Set once, never touch again.

```json
{
  "firm": {
    "name": "CountingFive",
    "tagline": "Turning Accounting Expertise Into Online Authority",
    "url": "https://countingfive.com",
    "logo_path": "assets/CountingFive-Logo-040125.png",
    "contact_email": "",
    "contact_phone": ""
  },
  "brand": {
    "primary_color": "#1B3A6B",
    "accent_color": "#00AEDB",
    "text_color": "#333333",
    "body_color": "#666666",
    "background_color": "#FFFFFF",
    "font_family": "Open Sans"
  },
  "target_industry": {
    "keywords": ["tax firm", "CPA", "accounting firm", "bookkeeper", "tax accountant", "enrolled agent"],
    "location_modifier": ""
  },
  "apis": {
    "firecrawl_api_key": "",
    "google_pagespeed_api_key": "",
    "google_search_api_key": "",
    "google_search_cx": "",
    "whois_api_key": "",
    "builtwith_api_key": ""
  },
  "output": {
    "pdf_dir": "pdf/",
    "md_dir": "md/",
    "filename_prefix": "audit"
  }
}
```

---

## Audit Sections

Each section (1–7) receives a **letter grade (A–F)** compiled from **numeric sub-scores (x/10)**. Each section also includes a short plain-language narrative (3–5 sentences) explaining what the section measures and why it matters to the client.

### 1. 📱 Mobile Responsiveness
**Data source:** Google PageSpeed API (mobile)
**Sub-scores:**
- Mobile performance score (0–100 → /10)
- Viewport configuration (/10)
- Touch target sizing (/10)
- Text readability on small screens (/10)
- Mobile Core Web Vitals: LCP, CLS, FID (/10 each)

### 2. ⚡ Site Speed & Performance
**Data source:** Google PageSpeed API (desktop)
**Sub-scores:**
- Desktop performance score (/10)
- Time to First Byte (/10)
- Largest Contentful Paint (/10)
- Cumulative Layout Shift (/10)
- Image optimization (/10)
- Render-blocking resources (/10)

### 3. 🔍 SEO / AIO / GEO Health
**Data source:** Firecrawl
**Sub-scores:**
- Title tags & meta descriptions (/10)
- H1–H6 heading structure (/10)
- JSON-LD / schema markup presence (/10)
- Open Graph / social tags (/10)
- Sitemap & robots.txt (/10)
- Internal linking structure (/10)
- Keyword density for target terms (/10)

### 4. 🎯 Target Market Clarity
**Data source:** Firecrawl (content analysis)
**Sub-scores:**
- Clarity of who the site serves (/10)
- Specificity of niche messaging (/10)
- CTA alignment (/10)
- Trust signals (testimonials, certifications, case studies) (/10)

### 5. 📊 Competitive Search Visibility
**Data source:** Google Search API
**Sub-scores:**
- Ranking for 3–5 target keywords (/10 each)
- Presence in AI-generated search results (/10)
- Local SEO signals (/10)

### 6. 🛠 Technology Stack Assessment
**Data source:** Firecrawl + HTTP header analysis
**Sub-scores:**
- CMS/platform modernity (/10)
- Page builder dependency (/10)
- Hosting quality signals (/10)
- SSL & security headers (/10)
- Plugin/dependency bloat (/10)
- Accessibility tooling (/10)

### 7. 🕰 Site Age, Health & Errors
**Data source:** WHOIS API + Firecrawl
**Sub-scores:**
- Domain age (/10)
- Broken links count (/10)
- Crawl errors (/10)
- Redirect chains (/10)
- Missing alt text (/10)
- Console errors (/10)

### 8. 💡 Recommendations & Next Steps
**No grade — narrative only.**
Maps each finding to a specific CountingFive service. Soft CTA at the end.

---

## Grading Scale

| Score Average | Letter Grade |
|---------------|-------------|
| 9.0 – 10.0    | A+          |
| 8.5 – 8.9     | A           |
| 8.0 – 8.4     | A-          |
| 7.5 – 7.9     | B+          |
| 7.0 – 7.4     | B           |
| 6.5 – 6.9     | B-          |
| 6.0 – 6.4     | C+          |
| 5.5 – 5.9     | C           |
| 5.0 – 5.4     | C-          |
| 4.0 – 4.9     | D           |
| 0.0 – 3.9     | F           |

---

## Output Format

### Branded PDF (8–12 pages)
- **Colors:** Navy `#1B3A6B` + Cyan `#00AEDB` + White
- **Font:** Open Sans
- **Logo:** CountingFive logo on every page

**Page structure:**
1. Cover — logo, "Website Audit Report", client URL, date, CountingFive tagline
2. Executive Summary — overall letter grade, section scorecard, 2–3 sentence plain-English summary
3–9. One page per audit section — grade badge, sub-scores, narrative
10. Recommendations & Next Steps — top 3–5 action items mapped to CountingFive services
11. Back Cover — CountingFive contact info

### Markdown File
- Mirrors PDF content in clean `.md` format
- Same sections, scores, and narrative
- Portable: suitable for email, proposals, or future client portal

### File Naming
```
audit-[domain]-[YYYY-MM-DD].pdf   → saved to pdf/
audit-[domain]-[YYYY-MM-DD].md    → saved to md/
```

---

## APIs Required

| API | Purpose | Cost | Status |
|-----|---------|------|--------|
| Firecrawl | Full site crawl, content & structure analysis | Paid (have it) | ✅ Ready |
| Google PageSpeed Insights | Performance + Core Web Vitals | Free | ✅ Ready to get |
| Google Custom Search | Keyword rankings, competitor research | Free (100/day) | ✅ Ready to get |
| WHOIS API | Domain age, registration history | Low cost | 🔲 To set up |
| BuiltWith or Wappalyzer | Tech stack detection | Varies | 🔲 Optional |

---

## Skill File Structure

```
/skills/site-audit/
  SKILL.md          ← main skill instructions (what Claude reads to run the audit)
  config.json       ← all API keys + firm settings (edit once)
  brand.json        ← CountingFive brand guidelines (auto-generated)
  README.md         ← setup instructions for API keys
```

---

## Brand Guidelines (CountingFive)

Derived from countingfive.com and logo analysis:

- **Primary Navy:** `#1B3A6B` — used for headings, cover, section headers
- **Accent Cyan:** `#00AEDB` — used for grade badges, highlights, accents
- **Body Text:** `#666666`
- **Heading Text:** `#333333`
- **Background:** `#FFFFFF`
- **Font:** Open Sans (weights: 400 regular, 600 semibold, 700 bold)
- **Tone:** Professional, authoritative, plain-English — never condescending

---

## Implementation Notes

- The skill triggers when the user pastes a URL and asks to run an audit
- The skill reads `config.json` first to load all API keys and brand settings
- Parallel agents are dispatched using the `dispatching-parallel-agents` skill pattern
- PDF generation uses the `pdf` skill
- WHOIS can fall back to free WHOIS lookup if no API key is configured
- If BuiltWith/Wappalyzer key is absent, tech stack detection falls back to Firecrawl header/script analysis
- Google Custom Search requires a Search Engine ID (`cx`) in addition to the API key

---

*Design approved 2026-04-06. Proceed to implementation.*
