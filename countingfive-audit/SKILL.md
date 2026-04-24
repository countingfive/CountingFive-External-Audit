---
name: countingfive-audit
description: >
  Runs the full CountingFive website audit pipeline — 6 data-gathering agents (PageSpeed,
  Firecrawl crawl, Serper keyword rankings, WHOIS domain age, niche intelligence, digital
  intelligence brief) → scored audit_results.json → branded HTML report via generate_report.py
  → Proposed Master Firm Profile. Produces three client-ready deliverables.

  ALWAYS use this skill instead of the generic internal-audit when the user says: "run the
  CountingFive audit", "full audit", "CF audit", "full site audit", "run the audit pipeline",
  "run the client audit", "audit this prospect", "pull the full report", or provides a URL
  alongside words like "client", "prospect", "report", or "deliverable". This skill produces
  the rich branded report with Digital Intelligence Brief and team profiles — the internal-audit
  skill does not. When in doubt between the two, always choose this one.
---

# CountingFive Full Audit Skill

This skill runs the **complete CountingFive audit pipeline** and produces a rich branded report.
It is the correct skill for any client-facing or prospect audit work.

> ⚠️ Do NOT use `internal-audit/scripts/audit.py` for this workflow — that script produces a
> stripped-down report missing the Digital Intelligence Brief, team profiles, narratives, and
> per-section bar charts. Always use `generate_report.py` from the site-audit-skill.

---

## Step 0 — Setup

Read the config and the full workflow instructions:

```
Config:    /Users/webhank/LocalSites/CountingFive-Site-Audit/site-audit-skill/config.json
Workflow:  /Users/webhank/LocalSites/CountingFive-Site-Audit/site-audit-skill/SKILL.md
```

Extract from config:
- `firecrawl_api_key`
- `google_pagespeed_api_key`
- `serper_api_key`
- `workspace_base` (note: this path may use an old session ID — translate to the current session mount path as needed)

Parse the target URL from the user's message. Extract the bare domain for file naming.

Set output paths:
```
HTML report:  [workspace_base]/reports/audit-[domain]-[YYYY-MM-DD].html
MD report:    [workspace_base]/md/audit-[domain]-[YYYY-MM-DD].md
MFP:          [workspace_base]/mfp/mfp-[domain]-[YYYY-MM-DD].md
```

---

## Step 1 — Follow the site-audit-skill SKILL.md

Read `/Users/webhank/LocalSites/CountingFive-Site-Audit/site-audit-skill/SKILL.md` now and
follow it from **Step 1 through Step 6** in full.

Key steps in that workflow:
- **Step 2**: Launch 6 parallel data-gathering agents (A=PageSpeed, B=Firecrawl, C=Serper, D=WHOIS, E=Niche, F=Digital Intel)
- **Step 3**: Collect agent results and cross-synthesize niche gap analysis
- **Step 4**: Score all 8 sections and build `audit_results.json`
- **Step 5**: Run `generate_report.py` to produce the HTML + MD reports
- **Step 6**: Run the MFP agentic research and write the MFP file

---

## Step 2 — Run generate_report.py (not audit.py)

```bash
python3 /Users/webhank/LocalSites/CountingFive-Site-Audit/site-audit-skill/scripts/generate_report.py \
  --data /path/to/audit_results.json \
  --config /Users/webhank/LocalSites/CountingFive-Site-Audit/site-audit-skill/config.json \
  --output-html [workspace_base]/reports/audit-[domain]-[YYYY-MM-DD].html \
  --output-md [workspace_base]/md/audit-[domain]-[YYYY-MM-DD].md
```

Save intermediate agent JSON files to the outputs working directory, not `/tmp/`, to avoid
permission errors. Use `/sessions/[session]/mnt/outputs/` for scratch files.

---

## Step 3 — Deliver all three files

Once all files are generated, share links to all three and give a brief verbal summary:

```
[View Audit Report](computer://[path to HTML])
[View Markdown Report](computer://[path to MD])
[View Proposed MFP](computer://[path to MFP])
```

Verbal summary should include:
- Overall score and grade
- Top 2–3 critical findings (🔴)
- Single fastest win
- Note that the MFP is ready for client review prep

---

## Common Pitfalls to Avoid

| Pitfall | Fix |
|---|---|
| Using `audit.py` instead of `generate_report.py` | Always use `generate_report.py` — it produces the rich report |
| Saving agent scratch files to `/tmp/` | Save to `/sessions/[session]/mnt/outputs/` — `/tmp/` may have permission issues |
| `workspace_base` path using old session ID | Translate to current session mount path |
| Skipping Agent F (digital intelligence) | This drives the team profiles and niche gap section — never skip it |
| Skipping the MFP | The MFP is Step 6 of the workflow — it's part of the full audit, not optional |
