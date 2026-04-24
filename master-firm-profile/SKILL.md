---
name: master-firm-profile
description: >
  Generate a Proposed Master Firm Profile (MFP) for a CPA firm website.
  The MFP is a strategic intelligence document — richer than the audit — that feeds
  the client review chat, content strategy, and site rebuild pipeline.
  Run this after a site audit OR independently from a URL alone.
  Triggers on: "run the MFP", "generate master firm profile", "create firm profile",
  "MFP for [URL]", "run firm profile", "build the MFP", "master firm profile for".
---

# CountingFive — Master Firm Profile Skill

## Overview

This skill generates a **Proposed Master Firm Profile (MFP)** for a CPA firm. The MFP is the second
stage of the CountingFive pipeline:

```
Audit → [Proposed MFP] → Client Review Chat → Content Strategy → Content Generation → Site Launch
```

The MFP is a strategic dossier — not a mirror of audit scores. It covers firm identity, positioning,
competitive context, team expertise, client profiles, content gaps, and a proposed site map with
redirect planning. It is labeled **Proposed** because the client confirms, edits, or removes items
in the subsequent review chat.

**Output:** `[workspace_base]/mfp/mfp-[domain]-[YYYY-MM-DD].md`

---

## Step 0: Setup

Read the main skill config to get API keys and workspace paths:

```
Config: /sessions/[session]/mnt/CountingFive-Site-Audit/site-audit-skill/config.json
```

If the config path is unclear, look for `config.json` in `site-audit-skill/` relative to this file's
directory (`../site-audit-skill/config.json`).

Extract:
- `firecrawl_api_key`
- `serper_api_key`
- `workspace_base` (output directory root)

Parse the target URL from the user's message. Extract the domain (e.g., `mkpcpa.com` from `https://www.mkpcpa.com`).

Set:
```
domain       = [extracted domain]
URL          = https://www.[domain]   (or exactly as provided)
output_path  = [workspace_base]/mfp/mfp-[domain]-[YYYY-MM-DD].md
```

---

## Step 1: Check for Existing Audit Data

Check whether a recent audit has already been run for this domain:

```bash
# Check if audit results exist and match this domain
python3 -c "
import json, os, sys
path = '/tmp/audit_results.json'
if not os.path.exists(path):
    print('NOT_FOUND')
    sys.exit()
with open(path) as f:
    d = json.load(f)
domain = d.get('domain', d.get('target_domain', ''))
print('MATCH' if '[domain]' in domain or domain in '[domain]' else 'MISMATCH:' + domain)
"
```

- **MATCH** → Use existing audit data. Extract `niche_intelligence` and `intelligence_brief` sections.
- **NOT_FOUND or MISMATCH** → Run lightweight site research in Step 2.

Either way, proceed through Steps 3–10 using whichever data source is available.

---

## Step 2: Lightweight Site Research (only if no audit data)

If audit data is **not available**, run the following targeted research. This replaces what Agents B, E,
and F would normally produce.

**Content & Niche Detection (replaces Agent E):**

Use Firecrawl `/v1/scrape` to fetch these pages (try each; skip 404s):
- `[URL]` (homepage)
- `[URL]/about`, `[URL]/about-us`, `[URL]/who-we-are`
- `[URL]/services`, `[URL]/what-we-do`
- `[URL]/industries`, `[URL]/who-we-serve`
- Any industry-specific pages linked from the above

From the content, identify:
- Confirmed industries/niches (named on a page or in navigation)
- Services offered
- Team members mentioned (names, titles, credentials)
- Tagline or primary value proposition

**Team & Digital Intelligence (replaces Agent F):**

Run Serper searches:
1. `"[Firm Name]" site:linkedin.com` → team members, credentials, prior employers
2. `"[Firm Name]" CPA [city]` → reviews, directory listings, press mentions
3. `"[Firm Name]" Google Business` → address, hours, rating

Save lightweight findings to `/tmp/lightweight_audit.json`:
```json
{
  "domain": "[domain]",
  "niche_intelligence": {
    "niches_detected": [...],
    "services_analysis": [...]
  },
  "intelligence_brief": {
    "personnel": [...],
    "reputation_signals": {}
  },
  "site_content_sample": "first 500 words of homepage body text"
}
```

---

## Step 3–10: Full MFP Research & Synthesis

Follow these steps from the main audit skill. All steps are documented there in full detail:

```
Reference: [skill_dir]/../site-audit-skill/SKILL.md
Steps to follow: 6A through 6K (the full MFP workflow)
```

**Quick reference — steps to run:**

| Step | Name | Data Source |
|---|---|---|
| 6A | Location & Contact Research | Web search + Firecrawl |
| 6B | History & Establishment Research | Web search + site About page |
| 6C | Deep Team Research | Serper searches per person |
| 6D | Additional Social & Digital | Serper searches |
| 6E | Positioning Extraction | Homepage content |
| 6F | Local Competitor Snapshot | Serper searches |
| 6G | Content Gap Analysis | Synthesis from above |
| 6H | Proposed Positioning | Synthesis — 3 options |
| 6I | Proposed Site Map | Synthesis |
| 6J | Current Site Map & Redirect Planning | Sitemap fetch + URL verification |
| 6K | Write the MFP File | All gathered data |

**Data source rules:**
- If audit data (`audit_results.json`) exists: use `niche_intelligence` and `intelligence_brief` from it for niche detection and team personnel list.
- If only lightweight data exists: use `lightweight_audit.json` for the same fields.
- All web research steps (6A, 6B, 6C, 6D, 6F) always run fresh regardless of audit data — these gather external intelligence not captured in the audit.

---

## Step 11: Confirm and Share

Once the MFP file is written, share it:

```
🗂 [View Proposed Master Firm Profile](computer://[output_path])

Proposed MFP ready for [Firm Name].

Positioning options: [A/B/C — brief note on each]
Key gaps identified: [top 2–3 in one line each]
Client review prep: [count] ❓ items need confirmation — see Section 11 (Before You Review)
```

---

## Error Handling

| Problem | Action |
|---|---|
| Config not found | Ask user to confirm workspace path; offer to locate config.json |
| No audit data AND Firecrawl fails | Fall back to homepage-only content; note degraded research in MFP |
| Serper quota hit | Note which team members couldn't be researched; mark as ❓ |
| Sitemap not found | Use Firecrawl crawl results for URL list; note source in Section 10A |
| Output directory missing | Create it: `mkdir -p [workspace_base]/mfp/` |
