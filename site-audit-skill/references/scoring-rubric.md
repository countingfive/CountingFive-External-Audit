# Site Audit Scoring Rubric

## Letter Grade Conversion

Convert the average of all sub-scores (each rated 1–10) to a letter grade:

| Average Sub-Score | Letter Grade |
|-------------------|-------------|
| 9.5 – 10.0        | A+          |
| 9.0 – 9.4         | A           |
| 8.5 – 8.9         | A-          |
| 8.0 – 8.4         | B+          |
| 7.5 – 7.9         | B           |
| 7.0 – 7.4         | B-          |
| 6.5 – 6.9         | C+          |
| 6.0 – 6.4         | C           |
| 5.5 – 5.9         | C-          |
| 5.0 – 5.4         | D+          |
| 4.0 – 4.9         | D           |
| 0.0 – 3.9         | F           |

## Overall Grade

The overall report grade is the average of all 7 section averages (not the average of all individual sub-scores).

---

## Section 1: Mobile Responsiveness

**Data source:** Google PageSpeed API (mobile strategy)

| Sub-Score | What to Measure | 10 | 7–9 | 4–6 | 1–3 |
|-----------|----------------|-----|-----|-----|-----|
| Mobile Performance Score | PageSpeed mobile score 0–100 | 90+ | 70–89 | 50–69 | <50 |
| Viewport Configuration | `<meta name="viewport">` present and correct | Yes | Minor issues | Partial | Missing |
| Touch Target Sizing | Buttons/links ≥48px tap target | All pass | Most pass | Some fail | Many fail |
| Text Readability | Font ≥16px on mobile, no horizontal scroll | Excellent | Good | Passable | Poor |
| LCP Mobile | Largest Contentful Paint on mobile | <2.5s | 2.5–3s | 3–4s | >4s |
| CLS Mobile | Cumulative Layout Shift on mobile | <0.1 | 0.1–0.15 | 0.15–0.25 | >0.25 |

**Narrative guidance:** Explain that more than half of web traffic is mobile, and Google ranks mobile-first. A poor mobile experience directly loses clients before they ever contact the firm.

---

## Section 2: Site Speed & Performance

**Data source:** Google PageSpeed API (desktop strategy)

| Sub-Score | What to Measure | 10 | 7–9 | 4–6 | 1–3 |
|-----------|----------------|-----|-----|-----|-----|
| Desktop Performance Score | PageSpeed desktop score 0–100 | 90+ | 75–89 | 55–74 | <55 |
| Time to First Byte (TTFB) | Server response time | <200ms | 200–500ms | 500ms–1s | >1s |
| Largest Contentful Paint | Time for main content to load | <2.5s | 2.5–3.5s | 3.5–5s | >5s |
| Cumulative Layout Shift | Visual stability score | <0.1 | 0.1–0.15 | 0.15–0.25 | >0.25 |
| Image Optimization | Images compressed, WebP/AVIF, lazy loaded | All optimized | Mostly | Some | Not at all |
| Render-Blocking Resources | CSS/JS blocking page paint | None | 1–2 | 3–4 | 5+ |

**Narrative guidance:** Site speed directly affects both SEO rankings and conversion. Studies show a 1-second delay in load time reduces conversions by 7%. For a tax or accounting firm, a slow site signals unreliability.

---

## Section 3: SEO / AIO / GEO Health

**Data source:** Firecrawl content analysis

| Sub-Score | What to Measure | 10 | 7–9 | 4–6 | 1–3 |
|-----------|----------------|-----|-----|-----|-----|
| Title Tags & Meta Descriptions | Present, unique, correct length (50–60 chars title, 150–160 meta) | All pages | Most pages | Some pages | Missing/duplicate |
| H1–H6 Heading Structure | One H1 per page, logical hierarchy, keyword-rich | Perfect | Minor issues | Inconsistent | Poor/missing |
| JSON-LD / Schema Markup | LocalBusiness, AccountingService, FAQPage schema present | Comprehensive | Some schema | Minimal | None |
| Open Graph / Social Tags | OG title, description, image on key pages | All present | Most present | Some | Missing |
| Sitemap & Robots.txt | XML sitemap exists, robots.txt present and correct | Both present | One present | Partial | Neither |
| Internal Linking | Pages interconnected, anchor text descriptive | Strong | Moderate | Weak | Broken/missing |
| Keyword Alignment | Target keywords (CPA, accounting, tax) appear in content naturally | Well-targeted | Moderate | Thin | Not targeted |

**Narrative guidance:** SEO, AIO (AI-optimized content for LLM search), and GEO (generative engine optimization for ChatGPT/Perplexity/Gemini) are now three separate battlegrounds. A site optimized only for Google misses an increasingly large share of how prospects find service providers.

---

## Section 4: Target Market Clarity

**Data source:** Firecrawl content analysis (homepage + key pages)

| Sub-Score | What to Measure | 10 | 7–9 | 4–6 | 1–3 |
|-----------|----------------|-----|-----|-----|-----|
| Who They Serve | Is the niche/target client explicitly stated above the fold? | Crystal clear | Clear | Vague | Not stated |
| Niche Specificity | Generic "accounting services" vs. specific "tax planning for dental practices" | Very specific | Somewhat | Generic | None |
| CTA Alignment | Calls-to-action match the intended visitor's next step | Well aligned | Mostly | Off | Missing/confusing |
| Trust Signals | Testimonials, case studies, certifications, years in business, client logos | Strong | Moderate | Weak | None |

**Narrative guidance:** A prospect landing on an accounting firm's website needs to know immediately: "This firm serves people like me." Without that clarity, visitors bounce — even if the firm is a perfect fit. This is especially critical for firms targeting specific niches (e.g., real estate investors, medical practices, restaurants).

---

## Section 5: Competitive Search Visibility

**Data source:** Google Custom Search API

Scoring approach: Search for 3–5 target keywords relevant to this firm's niche. For each keyword, check if the site appears in the top 10 results (score 10), top 20 (score 7), top 30 (score 5), or not found (score 2). Also check for AI search visibility.

| Sub-Score | What to Measure | 10 | 7–9 | 4–6 | 1–3 |
|-----------|----------------|-----|-----|-----|-----|
| Keyword 1 Ranking | Top result position for primary keyword | Top 5 | 6–10 | 11–20 | 21+ or absent |
| Keyword 2 Ranking | Top result position for secondary keyword | Top 5 | 6–10 | 11–20 | 21+ or absent |
| Keyword 3 Ranking | Top result position for tertiary keyword | Top 5 | 6–10 | 11–20 | 21+ or absent |
| Local SEO Signals | NAP consistency, Google Business Profile signals, local schema | Strong | Moderate | Weak | Missing |
| AI Search Presence | Site content likely indexed/cited in AI search results | Likely cited | Possibly | Unlikely | No structured content |

**Narrative guidance:** Ranking for the right keywords in the right geography is the most direct driver of inbound leads. We check not just Google but also signals for AI-powered search tools (ChatGPT, Perplexity, Gemini) which are increasingly how professionals research service providers.

---

## Section 6: Technology Stack Assessment

**Data source:** Firecrawl + HTTP header analysis

| Sub-Score | What to Measure | 10 | 7–9 | 4–6 | 1–3 |
|-----------|----------------|-----|-----|-----|-----|
| CMS / Platform Modernity | Modern, maintained CMS vs. outdated or abandoned | Modern & updated | Slightly dated | Outdated | End-of-life |
| Page Builder Dependency | Heavy page-builder bloat (Divi, Elementor) vs. lean code | No builder / lean | Light builder | Heavy builder | Severely bloated |
| Hosting Quality Signals | Response time, server headers, CDN presence | Fast CDN | Good hosting | Average | Slow/poor |
| SSL & Security Headers | HTTPS, HSTS, X-Frame-Options, CSP present | All present | Most present | HTTPS only | Missing SSL |
| Plugin / Dependency Bloat | Number of JS/CSS files, third-party scripts | Lean (<10) | Moderate | Heavy | Excessive |
| Accessibility Signals | ARIA labels, alt text presence, color contrast indicators | Strong | Moderate | Weak | Missing |

**Narrative guidance:** The technology stack is the foundation everything else is built on. An outdated or bloated stack slows the site, creates security vulnerabilities, and limits what's possible with future improvements — without the client necessarily knowing it's happening.

---

## Section 7: Site Age, Health & Errors

**Data source:** WHOIS lookup + Firecrawl crawl

| Sub-Score | What to Measure | 10 | 7–9 | 4–6 | 1–3 |
|-----------|----------------|-----|-----|-----|-----|
| Domain Age | Years since registration (older = more authoritative) | 10+ years | 5–10 years | 2–5 years | <2 years |
| Broken Links | Number of 404 errors found during crawl | 0 | 1–2 | 3–5 | 6+ |
| Redirect Chains | Number of pages with multi-hop redirects (301→301→301) | None | 1–2 | 3–4 | 5+ |
| Missing Alt Text | Images without alt attributes | 0% | <10% | 10–25% | >25% |
| Crawl Coverage | Are important pages crawlable, indexed, not blocked? | Fully crawlable | Mostly | Partially blocked | Severely blocked |
| Last Updated | Evidence of recent content updates (dates, freshness signals) | Within 30 days | 1–3 months | 3–12 months | 1+ year |

**Narrative guidance:** A site's health determines whether search engines trust it enough to rank it. Broken links, redirect chains, and missing alt text are the equivalent of a broken sign on a storefront — they quietly erode credibility with both visitors and Google.

---

## Section 8: Niche & Services Intelligence

**Data source:** Agent E — Firecrawl targeted page scrapes (/services, /about, /industries, /clients, /who-we-serve)

This section scores how clearly and deliberately the firm communicates its niche identity. It expands upon the broad market clarity signals in Section 4 with deeper, page-level content analysis.

| Sub-Score | What to Measure | 10 | 7–9 | 4–6 | 1–3 |
|-----------|----------------|-----|-----|-----|-----|
| Niche-Specific Language | Use of industry-specific terminology, job titles, or sector vocabulary in headlines and body copy | Highly specific throughout | Present on most pages | Occasional mentions | Generic only |
| Pain Points in Headlines | Industry pain points called out explicitly in H1s, H2s, and above-the-fold copy | Multiple specific pain points | 1–2 addressed | Vague references | Not addressed |
| Outcome Framing | Services described in terms of client results vs. internal process descriptions | All outcome-focused | Mostly | Mixed | Process-only |
| Niche Testimonials & Social Proof | Testimonials, case studies, or client logos from identifiable niche industries | Multiple specific examples | 1–2 present | Generic testimonials | None |
| Niche-Specific CTAs | Calls-to-action tailored to niche (e.g., "Built for dental practices") vs. generic ("Contact us") | Fully niche-tailored | Mostly | Some | Generic only |
| Visual Language Signals | Alt text, image filenames, icon labels, and visual metaphors that reflect the industries served | Strong and consistent | Moderate | Weak | Absent or mismatched |

**Narrative guidance:** Niche clarity is the single biggest conversion lever for accounting and tax firms. A prospect who immediately recognizes "this firm serves businesses like mine" is 3–5× more likely to inquire than one who sees generic messaging. This section measures the depth and consistency of niche communication across the entire site — not just the homepage.

---

## Section 9: Recommendations & Next Steps

This section has no grade. It is a narrative-only section that:
1. Lists the top 3–5 most impactful issues found across all sections
2. Briefly explains the business impact of each issue in plain language
3. Maps each issue to a specific CountingFive service
4. Closes with a soft, non-pushy CTA

**Format:**
- Issue title + section it came from
- One-sentence plain-language impact statement
- "CountingFive can help by..." (one line, specific service)

**CTA:** "Ready to turn these findings into results? CountingFive specializes in web design, development, hosting, and targeted content for accounting and tax professionals. Let's talk about what's possible for [firm name]."
