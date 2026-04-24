# CountingFive Site Audit Skill

Generates a branded PDF and Markdown website audit report for prospects in the tax and accounting space.

## Setup (One-Time)

### 1. Add your API keys to `config.json`

Open `config.json` and fill in the `apis` section:

| Key | How to Get It | Cost |
|-----|--------------|------|
| `firecrawl_api_key` | Already set | Paid plan |
| `google_pagespeed_api_key` | [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Enable "PageSpeed Insights API" → Credentials → Create API Key | Free |
| `google_search_api_key` | Same Google Cloud Console project → Enable "Custom Search API" → same API Key | Free (100 searches/day) |
| `google_search_cx` | [Programmable Search Engine](https://programmablesearchengine.google.com/) → Create engine → Search the entire web → Copy "Search engine ID" | Free |

### 2. Update firm contact info

In `config.json` → `firm`, fill in:
- `contact_email`
- `contact_phone`

### 3. Optionally set a location modifier

In `config.json` → `target_industry` → `location_modifier`, you can add a city or region (e.g., `"Dallas TX"`) to localize keyword searches for prospects in specific markets. Leave blank for national searches.

---

## Usage

In Cowork, simply say:

> "Audit [URL]"
> "Run a site audit on https://example-cpafirm.com"
> "Pull a report on this prospect's website: https://smithaccounting.com"

The skill will:
1. Gather data from PageSpeed, Firecrawl, Google Search, and WHOIS simultaneously
2. Score the site across 7 dimensions
3. Generate a branded PDF and Markdown report
4. Save both files to the `pdf/` and `md/` folders

---

## Output Files

Reports are saved to:
```
pdf/audit-[domain]-[date].pdf
md/audit-[domain]-[date].md
```

---

## Troubleshooting

**"PageSpeed API key invalid"** → Go to Google Cloud Console, check the API key is unrestricted or allowed for PageSpeed Insights API.

**"Firecrawl returned no results"** → Check your Firecrawl API key and plan limits. The skill will fall back to homepage-only scraping.

**"Google Search returned no results"** → Verify your `google_search_cx` Search Engine ID. Make sure the engine is set to "Search the entire web."

**Slow audits** → Firecrawl crawling 15 pages can take 30–60 seconds. This is normal. The skill runs PageSpeed and WHOIS in parallel so overall time is usually under 90 seconds.
