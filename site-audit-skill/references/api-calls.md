# API Call Reference

This file contains the exact API call patterns used by the site audit agents.
Claude reads this file to construct the correct API calls for each data-gathering agent.

---

## Agent A: Google PageSpeed Insights

**Mobile Audit:**
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_ENCODED_URL&key=API_KEY&strategy=mobile&category=performance&category=accessibility&category=seo" \
  -o /tmp/pagespeed_mobile.json
```

**Desktop Audit:**
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_ENCODED_URL&key=API_KEY&strategy=desktop&category=performance&category=accessibility&category=seo" \
  -o /tmp/pagespeed_desktop.json
```

**Key fields to extract from response:**
```
lighthouseResult.categories.performance.score          → multiply by 100 for 0–100 score
lighthouseResult.categories.accessibility.score
lighthouseResult.categories.seo.score
lighthouseResult.audits.largest-contentful-paint.displayValue
lighthouseResult.audits.cumulative-layout-shift.displayValue
lighthouseResult.audits.total-blocking-time.displayValue
lighthouseResult.audits.speed-index.displayValue
lighthouseResult.audits.time-to-interactive.displayValue
lighthouseResult.audits.server-response-time.displayValue
lighthouseResult.audits.uses-optimized-images.score
lighthouseResult.audits.render-blocking-resources.details.items  (count items)
lighthouseResult.audits.viewport.score                → 1.0 = pass, 0 = fail
lighthouseResult.audits.tap-targets.score
lighthouseResult.audits.font-size.score
```

---

## Agent B: Firecrawl Site Crawl

**Crawl the site (up to 15 pages):**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/crawl" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer FIRECRAWL_API_KEY" \
  -d '{
    "url": "TARGET_URL",
    "limit": 15,
    "scrapeOptions": {
      "formats": ["markdown", "links", "rawHtml"],
      "includeTags": ["title", "meta", "h1", "h2", "h3", "h4", "h5", "h6", "script", "link"],
      "excludeTags": ["footer", "nav"]
    }
  }' \
  -o /tmp/firecrawl_crawl.json
```

**Then poll for results (Firecrawl crawl is async):**
```bash
# Get crawl ID from initial response, then poll:
CRAWL_ID=$(cat /tmp/firecrawl_crawl.json | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
curl -s "https://api.firecrawl.dev/v1/crawl/$CRAWL_ID" \
  -H "Authorization: Bearer FIRECRAWL_API_KEY" \
  -o /tmp/firecrawl_results.json
```

**Alternatively, scrape just the homepage for faster results:**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer FIRECRAWL_API_KEY" \
  -d '{
    "url": "TARGET_URL",
    "formats": ["markdown", "links", "rawHtml"],
    "actions": []
  }' \
  -o /tmp/firecrawl_homepage.json
```

**Key things to extract from Firecrawl results:**
- All H1, H2, H3, H4, H5, H6 tags and their text
- `<title>` tag content for each page
- `<meta name="description">` content for each page
- `<meta property="og:*">` tags
- `<script type="application/ld+json">` content (schema markup)
- All internal links (for internal linking analysis)
- All external links (check for broken ones)
- `<link rel="sitemap">` presence
- Image `alt` attributes (count missing)
- Main body text for content/keyword analysis
- Any `<meta name="robots">` tags
- HTTP headers if available (X-Powered-By, Server, etc.)

---

## Agent C: Serper.dev (Google Search Rankings)

**Search for each keyword:**
```bash
curl -s -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "KEYWORD HERE", "num": 10}' \
  -o /tmp/search_keyword_1.json
```

**For local keyword searches (if location_modifier set in config):**
```bash
curl -s -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "KEYWORD HERE LOCATION HERE", "num": 10, "gl": "us", "hl": "en"}' \
  -o /tmp/search_keyword_local_1.json
```

**Check if target site appears in results:**
```python
import json

with open('/tmp/search_keyword_1.json') as f:
    data = json.load(f)

items = data.get('organic', [])
for i, item in enumerate(items):
    if 'TARGET_DOMAIN' in item.get('link', ''):
        print(f"Found at position {i+1}: {item.get('title')}")
        break
else:
    print("Not found in top 10")

# Capture competing domains for context
competing = [item.get('link', '').split('/')[2] for item in items[:5]]
print(f"Top results: {competing}")
```

**Keywords to search (from config.json target_industry.primary_keywords + firm's apparent niche):**
Use the first 5 keywords from config plus any niche-specific keywords discovered from the Firecrawl content analysis.

**Note:** Serper free trial includes 2,500 searches (~500 audits). Paid plans are $50/50,000 searches.

---

## Agent D: WHOIS Domain Lookup

**Using system whois command:**
```bash
whois TARGET_DOMAIN 2>/dev/null | head -50 > /tmp/whois_raw.txt
```

**Extract creation date with Python:**
```python
import subprocess
import re
from datetime import datetime

domain = "TARGET_DOMAIN"
result = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=15)
text = result.stdout.lower()

# Try common date patterns
patterns = [
    r'creation date:\s*(.+)',
    r'created:\s*(.+)',
    r'registered on:\s*(.+)',
    r'domain registered:\s*(.+)',
]

for pattern in patterns:
    match = re.search(pattern, text)
    if match:
        print(f"Raw date: {match.group(1).strip()}")
        break
```

**If whois is unavailable or rate-limited**, fall back to:
- Check the Wayback Machine: `https://archive.org/wayback/available?url=TARGET_DOMAIN`
- Use HTTP header analysis from Firecrawl results for "Last-Modified"
- Check copyright year in site footer from Firecrawl content

---

## Graceful Degradation

If any API key is missing or a call fails:

| Missing Key | Fallback |
|-------------|---------|
| `google_pagespeed_api_key` | Use PageSpeed without key (rate-limited but works for occasional use) |
| `firecrawl_api_key` | Use WebFetch to scrape homepage only; note limited crawl depth |
| `google_search_api_key` | Note "ranking data unavailable" in that section; score as N/A |
| `whois_api_key` (optional) | Use system `whois` command instead |

For any section where data collection fails, mark that section's sub-scores as "N/A" and explain in the narrative that this data could not be collected, with a recommendation to investigate manually.
