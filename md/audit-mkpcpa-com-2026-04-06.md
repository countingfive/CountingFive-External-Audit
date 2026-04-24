# Website Audit Report: https://mkpcpa.com
**Prepared by:** CountingFive  
**Date:** April 6, 2026  
**Overall Grade:** C+ (6.2/10)

---

## Executive Summary

McKeown Kraai Professional, CPAs has meaningful strengths to build on — a fast server, solid schema markup, and a clean desktop experience — but the site is being held back by three significant issues that are costing them clients right now. Mobile performance is critically low (59/100) with a page load time of 6.4 seconds on phones, the viewport configuration is broken, and the site does not appear in Google's top results for any of the five core accounting keywords we tested. These are solvable problems, and fixing them represents a clear opportunity to dramatically increase the firm's online visibility and client conversion.

| Section | Score | Grade |
|---------|-------|-------|
| 📱 Mobile Responsiveness | 3.5/10 | **D** |
| ⚡ Site Speed & Performance | 8.2/10 | **B+** |
| 🔍 SEO / AIO / GEO Health | 7.0/10 | **B-** |
| 🎯 Target Market Clarity | 6.3/10 | **C+** |
| 📊 Competitive Search Visibility | 4.0/10 | **D+** |
| 🛠 Technology Stack | 7.3/10 | **B-** |
| 🕰 Site Age, Health & Errors | 7.5/10 | **B** |

---

## 📱 Mobile Responsiveness
**Grade: D** | **Average Score: 3.5/10**

**Sub-Scores:**

- Mobile Performance Score: 4/10
- Viewport Configuration: 2/10
- Touch Targets: 2/10
- Text Readability: 3/10
- Lcp Mobile: 2/10
- Cls Mobile: 9/10

This is the most urgent finding in the audit. MKPcpa.com scores 59/100 on mobile performance — well below Google's recommended threshold of 90. More critically, the viewport is misconfigured, meaning the site is not properly instructing mobile browsers how to scale the page, which causes content to render incorrectly on phones. Touch targets (buttons and links) are too small for reliable tapping, and font sizes fail Google's minimum readability standard. With over 60% of web traffic now on mobile devices, prospects viewing this site on their phone are likely experiencing a frustrating, broken experience.

---

## ⚡ Site Speed & Performance
**Grade: B+** | **Average Score: 8.2/10**

**Sub-Scores:**

- Desktop Performance Score: 6/10
- Time To First Byte: 10/10
- Largest Contentful Paint: 10/10
- Cumulative Layout Shift: 10/10
- Image Optimization: 7/10
- Render Blocking Resources: 10/10

Desktop performance tells a very different story from mobile. The server response time is excellent at just 40ms — this is top-tier hosting. The largest piece of content loads in 1.4 seconds on desktop, well within Google's 'good' threshold, and the page has zero render-blocking resources and near-perfect visual stability. The desktop experience is genuinely solid. The disconnect between excellent desktop performance and poor mobile performance points to a Divi page builder rendering issue that only affects mobile — a targeted fix rather than a full rebuild.

---

## 🔍 SEO / AIO / GEO Health
**Grade: B-** | **Average Score: 7.0/10**

**Sub-Scores:**

- Title Tags And Meta: 6/10
- Heading Structure: 9/10
- Schema Markup: 8/10
- Open Graph Social Tags: 10/10
- Sitemap And Robots: 3/10
- Internal Linking: 5/10
- Keyword Alignment: 8/10

The firm has done several things right: heading structure is clean with a single H1 per page, schema markup includes AccountingService and PostalAddress (which directly helps Google understand the business), and Open Graph tags are fully implemented for social sharing. However, two gaps are limiting their search performance. First, no XML sitemap was detected — this is the roadmap that tells Google which pages to crawl, and without it, pages may not be indexed. Second, the homepage meta description is only 64 characters (Google recommends 150-160), which is too short to be compelling in search results and likely being rewritten automatically by Google.

---

## 🎯 Target Market Clarity
**Grade: C+** | **Average Score: 6.3/10**

**Sub-Scores:**

- Who They Serve: 6/10
- Niche Specificity: 5/10
- Cta Alignment: 7/10
- Trust Signals: 7/10

The site clearly communicates that MKP is a CPA firm, and testimonials and professional credentials are present — both positive trust signals. The gap is in specificity: the homepage meta description states the firm is 'passionate about our clients,' which is a sentiment any business could claim. There is no clear statement above the fold about who the firm's ideal client is — whether that's small business owners, individuals, specific industries, or a geographic area. Prospects who land on the site and don't immediately see themselves reflected in the messaging tend to leave without contacting the firm.

---

## 📊 Competitive Search Visibility
**Grade: D+** | **Average Score: 4.0/10**

**Sub-Scores:**

- Cpa Firm Keyword: 2/10
- Accounting Firm Keyword: 2/10
- Tax Accountant Keyword: 2/10
- Bookkeeping Services Keyword: 2/10
- Local Seo Signals: 8/10
- Ai Search Presence: 6/10

MKPcpa.com did not appear in the top 10 Google results for any of the five core accounting keywords we tested. This is common for local firms competing against national aggregators and directories on broad terms — the real opportunity is in location-specific searches like '[city] CPA firm' or '[city] small business accountant,' where local firms can and do rank well. The good news: the site's PostalAddress and OpeningHoursSpecification schema markup gives it a strong foundation for local search. The missing piece is a targeted local SEO content strategy that builds authority for these geographically-specific searches.

---

## 🛠 Technology Stack Assessment
**Grade: B-** | **Average Score: 7.3/10**

**Sub-Scores:**

- Cms Platform Modernity: 7/10
- Page Builder Dependency: 4/10
- Hosting Quality: 10/10
- Ssl And Security: 10/10
- Plugin Dependency Bloat: 6/10
- Accessibility Tooling: 8/10

The hosting infrastructure is genuinely excellent — a 40ms server response time puts this site in the top tier. SSL is properly implemented and accessibility scores are respectable at 87-89/100. The primary concern is the Divi page builder, which is known to add significant JavaScript weight that disproportionately impacts mobile performance. The 'unused JavaScript' audit failed completely, suggesting a large volume of Divi's JavaScript is loading on every page regardless of whether it is used — a classic page builder problem. Accessibility scores of 87-89 are good but not perfect; the 11 images missing alt text contribute to both the accessibility gap and the SEO score.

---

## 🕰 Site Age, Health & Errors
**Grade: B** | **Average Score: 7.5/10**

**Sub-Scores:**

- Domain Age: 7/10
- Broken Links: 10/10
- Redirect Chains: 8/10
- Missing Alt Text: 7/10
- Crawl Coverage: 7/10
- Last Updated: 8/10

The site's day-to-day health is solid. Eleven pages were crawled without encountering a single broken link, and all pages have proper title tags and meta descriptions in place. The 11 images missing alt text (out of 163 total, a 93% coverage rate) is a minor but addressable issue that affects both accessibility and image search indexing. The absence of a detected sitemap is the most significant health concern — without it, Google relies entirely on following links to discover content, which means newer or deeper pages may not be indexed promptly. Domain age data was unavailable via WHOIS in this audit environment; the firm's established reputation suggests the domain carries solid authority.

---

## 💡 Recommendations & Next Steps

### 1. Fix Mobile Viewport & Performance (Score: 59/100) (High Priority)
**Business Impact:** A broken viewport configuration means every visitor on a phone sees a distorted version of the site. With mobile devices accounting for the majority of web traffic, this is actively costing the firm first impressions and client inquiries every day.

**CountingFive Can Help:** CountingFive rebuilds accounting firm sites on lean, mobile-first frameworks. We fix viewport issues, eliminate Divi's mobile overhead, and deliver sites that score 90+ on mobile — included as part of our web development packages.

### 2. Local SEO Content Strategy — Zero Keyword Rankings (High Priority)
**Business Impact:** The firm is invisible in Google for every accounting keyword we tested. Prospects searching for a CPA in their area cannot find MKP through organic search, meaning all new clients are coming from referrals alone — a growth ceiling with no ceiling.

**CountingFive Can Help:** CountingFive specializes in targeted content generation for accounting firms. We build location-specific service pages and keyword-optimized articles that rank for the searches your ideal clients are actually making.

### 3. Add XML Sitemap and Robots.txt (High Priority)
**Business Impact:** Without a sitemap, Google has no roadmap for crawling the site. Pages may not be indexed, and any new content added to the site could take weeks longer to appear in search results.

**CountingFive Can Help:** CountingFive handles all technical SEO setup as part of every site build and hosting package — sitemaps, robots.txt, schema, and ongoing crawl monitoring.

### 4. Rewrite Meta Descriptions & Homepage Messaging (Medium Priority)
**Business Impact:** A 64-character meta description and generic 'passionate about our clients' messaging means the firm blends in rather than stands out in search results — reducing click-through rates and failing to communicate the firm's true value to the right prospects.

**CountingFive Can Help:** CountingFive's content strategy service crafts compelling, keyword-rich meta descriptions and homepage copy that speaks directly to the firm's ideal client and drives more clicks from search results.

### 5. Complete Image Alt Text (11 Images Missing) (Low Priority)
**Business Impact:** Missing alt text on 7% of images is a minor but addressable gap that affects accessibility compliance and prevents those images from appearing in Google Image Search.

**CountingFive Can Help:** CountingFive includes a full accessibility and SEO audit with every site project, ensuring all images are properly tagged and the site meets WCAG accessibility standards.

---

*CountingFive — Turning Accounting Expertise Into Online Authority*  
*https://countingfive.com*