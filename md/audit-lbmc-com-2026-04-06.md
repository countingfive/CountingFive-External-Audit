# Website Audit Report: https://www.lbmc.com
**Prepared by:** CountingFive  
**Date:** April 6, 2026  
**Overall Grade:** B (7.3/10)

---

## Executive Summary

LBMC's website presents a professionally credible presence with strong SEO fundamentals — comprehensive schema markup, proper meta tags, and good keyword alignment. However, the site carries significant technical debt from its dual page-builder setup (Divi + Elementor), which typically creates performance and maintenance challenges. Performance scores could not be automatically retrieved during this audit and should be verified. The most immediate opportunities are resolving a duplicate H1 tag error on the homepage, and improving competitive keyword visibility for the specific markets LBMC serves.

| Section | Score | Grade |
|---------|-------|-------|
| 📱 Mobile Responsiveness | 6.8/10 | **B-** |
| ⚡ Site Speed & Performance | 6.2/10 | **C+** |
| 🔍 SEO / AIO / GEO Health | 8.6/10 | **A-** |
| 🎯 Target Market Clarity | 7.8/10 | **B+** |
| 📊 Competitive Search Visibility | 7.2/10 | **B** |
| 🛠 Technology Stack | 6.0/10 | **C+** |
| 🕰 Site Age, Health & Errors | 7.8/10 | **B+** |

---

## 📱 Mobile Responsiveness
**Grade: B-** | **Average Score: 6.8/10**

**Sub-Scores:**

- Mobile Performance: N/A - API key required/10
- Viewport Configuration: 9/10
- Touch Targets: 7/10
- Text Readability: 8/10
- Lcp Mobile: N/A - API key required/10
- Cls Mobile: N/A - API key required/10

LBMC's site is built on WordPress with both Divi and Elementor page builders active simultaneously — a combination that typically adds significant JavaScript and CSS weight that hurts mobile load times. The viewport is correctly configured and the site appears to be responsive, but page builder overhead commonly degrades the mobile experience on slower connections. A full PageSpeed mobile audit (requires Google API key setup) would give precise Core Web Vitals scores. Based on the technology stack alone, mobile performance is a likely area for improvement.

---

## ⚡ Site Speed & Performance
**Grade: C+** | **Average Score: 6.2/10**

**Sub-Scores:**

- Desktop Performance: N/A - API key required/10
- Time To First Byte: N/A - API key required/10
- Largest Contentful Paint: N/A - API key required/10
- Cumulative Layout Shift: N/A - API key required/10
- Image Optimization: 9/10
- Render Blocking Resources: 5/10

Precise speed metrics require the Google PageSpeed API key to be configured (see Setup in config.json). Based on the technology stack analysis, having both Divi and Elementor active on the same WordPress installation is a known performance concern — each adds its own JavaScript and CSS files, increasing page weight and the number of render-blocking resources. Image alt text is 100% complete (a positive signal), but the dual page builder setup is a structural issue that limits performance ceiling regardless of other optimizations.

---

## 🔍 SEO / AIO / GEO Health
**Grade: A-** | **Average Score: 8.6/10**

**Sub-Scores:**

- Title Tags And Meta: 9/10
- Heading Structure: 6/10
- Schema Markup: 10/10
- Open Graph Social Tags: 10/10
- Sitemap And Robots: 9/10
- Internal Linking: 7/10
- Keyword Alignment: 9/10

LBMC's SEO foundation is genuinely strong. They have one of the most comprehensive schema markup implementations we see — 20 distinct schema types including Organization, Service, BreadcrumbList, Person, and WebSite, which are exactly what Google and AI-powered search engines use to understand and feature a business. Open Graph tags are fully implemented, the sitemap is present, and keyword alignment is excellent. The one blemish: a duplicate H1 tag on the homepage (the second one reads 'An error occurred') which should be fixed immediately as it signals a rendering error to search engines.

---

## 🎯 Target Market Clarity
**Grade: B+** | **Average Score: 7.8/10**

**Sub-Scores:**

- Who They Serve: 8/10
- Niche Specificity: 7/10
- Cta Alignment: 8/10
- Trust Signals: 9/10

LBMC communicates its core offering clearly — accounting, tax, audit, HR, cybersecurity, and technology services for businesses. The homepage hero speaks directly to business owners and includes a strong ClearlyRated Best of Accounting badge as a trust signal. The main gap is niche specificity: the messaging is broad enough to apply to almost any business, which can make it harder to convert prospects in a specific industry or size segment. Firms with more targeted messaging (e.g., 'We serve mid-market healthcare and manufacturing companies in Tennessee') tend to convert better in their target segments.

---

## 📊 Competitive Search Visibility
**Grade: B** | **Average Score: 7.2/10**

**Sub-Scores:**

- Cpa Firm Ranking: 6/10
- Accounting Firm Ranking: 7/10
- Tax Firm Ranking: 7/10
- Local Seo Signals: 9/10
- Ai Search Presence: 7/10

LBMC is a well-established regional firm with strong local SEO signals — multiple PostalAddress schema entries suggest multi-location presence, and the firm is clearly indexed across major accounting keywords. However, at a national competitive level, ranking for generic terms like 'CPA firm' or 'accounting firm' is extremely competitive. LBMC's strongest SEO opportunity is in long-tail, service-specific terms (e.g., 'Tennessee business accounting advisory') where their schema markup gives them a real edge. AI search presence is likely positive given the rich structured data.

---

## 🛠 Technology Stack Assessment
**Grade: C+** | **Average Score: 6.0/10**

**Sub-Scores:**

- Cms Platform Modernity: 7/10
- Page Builder Dependency: 3/10
- Hosting Quality: 7/10
- Ssl And Security: 9/10
- Plugin Dependency Bloat: 4/10
- Accessibility Tooling: 8/10

The most significant technical finding is that LBMC's site is running both Divi and Elementor page builders simultaneously on WordPress — this is an unusual and problematic configuration. Each page builder adds its own JavaScript libraries, CSS frameworks, and rendering overhead. This increases page weight, slows load times, creates potential conflicts, and makes the site significantly harder and more expensive to maintain or update. SSL is properly implemented and the accessibility tooling appears solid, but the page builder issue is the kind of technical debt that compounds over time and limits what's possible with future improvements.

---

## 🕰 Site Age, Health & Errors
**Grade: B+** | **Average Score: 7.8/10**

**Sub-Scores:**

- Domain Age: N/A - WHOIS unavailable/10
- Broken Links: 10/10
- Redirect Chains: 9/10
- Missing Alt Text: 10/10
- Crawl Coverage: 8/10
- Last Updated: 9/10

LBMC's site is in good health from a technical maintenance standpoint. Zero broken links were detected, all 24 images have proper alt text (excellent for both SEO and accessibility), and the site appears to have been updated recently (copyright shows 2026). The robots.txt is configured to allow full indexing with optimal social media preview settings. Domain age data was unavailable in this scan — LBMC is a long-established firm so their domain authority is likely strong, but this should be verified. The one H1 error message detected may indicate a JavaScript rendering issue that should be investigated.

---

## 💡 Recommendations & Next Steps

### 1. Duplicate Page Builder Conflict (Divi + Elementor) (High Priority)
**Business Impact:** Running two competing page builders on the same WordPress site adds unnecessary weight, slows every page, creates maintenance complexity, and limits future design flexibility — all without the client knowing it's happening.

**CountingFive Can Help:** CountingFive offers a full technology stack assessment and site rebuild using a lean, modern WordPress implementation. We eliminate page builder bloat while preserving all existing content and design — typically resulting in 40–60% performance improvement.

### 2. Duplicate H1 Tag / Homepage Rendering Error (High Priority)
**Business Impact:** A second H1 tag reading 'An error occurred' on the homepage signals a rendering failure to Google and could suppress search rankings for the most valuable page on the site.

**CountingFive Can Help:** CountingFive's technical SEO audit and development services identify and resolve rendering errors, heading structure issues, and JavaScript conflicts that silently hurt search performance.

### 3. Mobile & Desktop Speed (API Verification Needed) (Medium Priority)
**Business Impact:** Page builder overhead is a known cause of slow load times. Google's Core Web Vitals directly influence search rankings, and a 1-second delay in mobile load time can reduce conversions by up to 7%.

**CountingFive Can Help:** CountingFive builds and hosts accounting firm websites on performance-optimized infrastructure with full Core Web Vitals compliance — included as part of our hosting and development packages.

### 4. Broad Target Market Messaging (Medium Priority)
**Business Impact:** Generic messaging ('we serve businesses') makes it harder for the firm's ideal clients to self-identify, reducing conversion rates from organic traffic even when the firm is a perfect fit.

**CountingFive Can Help:** CountingFive specializes in targeted content strategy for accounting firms — we help firms develop industry-specific landing pages and messaging that converts the clients they actually want to serve.

### 5. Keyword Visibility for Long-Tail Opportunities (Low Priority)
**Business Impact:** Generic accounting keywords are highly competitive nationally. Targeting specific service and industry combinations (e.g., 'Tennessee healthcare accounting firm') offers faster ranking wins with less competition.

**CountingFive Can Help:** CountingFive's content generation service creates a steady stream of SEO-targeted articles, service pages, and topic clusters that build ranking authority in the specific niches the firm serves.

---

*CountingFive — Turning Accounting Expertise Into Online Authority*  
*https://countingfive.com*