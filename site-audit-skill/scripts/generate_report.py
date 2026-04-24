#!/usr/bin/env python3
"""
CountingFive Site Audit Report Generator
Generates a branded HTML and Markdown report from audit JSON data.

Usage:
    python3 generate_report.py --data /tmp/audit_results.json --config /path/to/config.json \
        --output-html /path/to/output.html --output-md /path/to/output.md
"""

import json
import sys
import os
import argparse
import base64
from datetime import datetime


# ── Section metadata (shared by HTML, Markdown, and MFP builders) ─────────────
SECTION_META = [
    ("target_market_clarity",  "Target Market Clarity"),
    ("competitive_visibility", "Competitive Search Visibility"),
    ("niche_intelligence",     "Niche & Services Intelligence"),
    ("seo_health",             "SEO / AIO / GEO Health"),
    ("mobile_responsiveness",  "Mobile Responsiveness"),
    ("site_speed",             "Site Speed & Performance"),
    ("technology_stack",       "Technology Stack"),
    ("site_health",            "Site Age, Health & Errors"),
]

SECTION_ICONS = {
    "mobile_responsiveness":  "",
    "site_speed":             "",
    "seo_health":             "",
    "target_market_clarity":  "",
    "niche_intelligence":     "",
    "competitive_visibility": "",
    "technology_stack":       "",
    "site_health":            "",
}


# ── Utility helpers ───────────────────────────────────────────────────────────
def logo_b64(path):
    """Return a base64 data URI for an image file, or empty string on failure."""
    if not path or not os.path.exists(path):
        return ""
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = os.path.splitext(path)[1].lstrip(".").lower()
        mime = {"png": "image/png", "jpg": "image/jpeg",
                "jpeg": "image/jpeg", "svg": "image/svg+xml"}.get(ext, "image/png")
        return f"data:{mime};base64,{data}"
    except Exception:
        return ""


def esc(text):
    """HTML-escape a value."""
    if not isinstance(text, str):
        text = str(text) if text is not None else ""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))


def grade_class(grade):
    """Return CSS class suffix for a letter grade."""
    if not grade or grade == "N/A":
        return "na"
    return {"A": "a", "B": "b", "C": "c", "D": "d", "F": "f"}.get(grade[0].upper(), "na")


def score_bar_color(score):
    """Return a hex color for a 1–10 score."""
    try:
        s = float(score)
        if s >= 7.5:
            return "#10B981"
        elif s >= 5.5:
            return "#F59E0B"
        else:
            return "#DC2626"
    except (TypeError, ValueError):
        return "#9CA3AF"


def ring_degrees(score, max_score=10):
    """Convert a 1–10 score to conic-gradient degrees."""
    try:
        return round((float(score) / float(max_score)) * 360, 1)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0


def fmt_score(score):
    """Format a score for display."""
    if score is None:
        return "N/A"
    if isinstance(score, str):
        return score
    if isinstance(score, float):
        return f"{score:.1f}"
    return str(score)


# ── Staff & Expertise HTML builder ────────────────────────────────────────────
def build_staff_expertise_html(staff_expertise: dict) -> str:
    """Render the Staff & Expertise Profile section HTML."""
    if not staff_expertise:
        return ""

    staff_list  = staff_expertise.get("staff", [])
    collective  = staff_expertise.get("collective_analysis", {})

    if not staff_list and not collective:
        return ""

    html = ""

    # ── Collective summary box ────────────────────────────────────────────
    if collective:
        creds_list = ", ".join(collective.get("combined_credentials", []))
        summary    = collective.get("summary", "")
        top_gaps   = collective.get("top_3_gaps", [])
        unlev      = collective.get("high_value_unleveraged_niches", [])

        gap_items = "".join(
            f'<li>{esc(g)}</li>' for g in top_gaps[:3])
        unlev_text = ", ".join(unlev) if unlev else "None identified"

        html += f"""
  <div class="staff-summary-box">
    <h4>Team Credentials</h4>
    <p>{esc(creds_list) if creds_list else "See individual profiles below."}</p>
    {(f'<h4 style="margin-top:10px">Collective Summary</h4><p>{esc(summary)}</p>') if summary else ''}
    {(f'<h4 style="margin-top:10px">High-Value Unleveraged Niches</h4><p style="color:#FCD34D">{esc(unlev_text)}</p>') if unlev else ''}
    {(f'<h4 style="margin-top:10px">Top Gaps</h4><ul class="staff-gaps-list">{gap_items}</ul>') if gap_items else ''}
  </div>"""

    # ── Per-person cards ──────────────────────────────────────────────────
    if staff_list:
        cards_html = ""
        for person in staff_list:
            name    = person.get("name", "")
            title_p = person.get("title", "")
            creds   = person.get("credentials", [])
            summary_p = person.get("summary", "")
            leverage  = person.get("overall_leverage", "partially_leveraged")
            top_gaps_p = person.get("top_gaps", [])
            cred_opps  = person.get("credential_opportunities", [])
            linkedin   = person.get("linkedin", {})

            # Credential badges
            cred_badges = "".join(
                f'<span class="cred-badge">{esc(c)}</span>' for c in creds)

            # Leverage indicator
            lev_map = {
                "fully_leveraged":    ("leverage-full",    "Fully Leveraged"),
                "partially_leveraged":("leverage-partial", "Partially Leveraged"),
                "not_leveraged":      ("leverage-none",    "Not Leveraged"),
            }
            lev_class, lev_label = lev_map.get(leverage, ("leverage-partial", "Partially Leveraged"))

            # LinkedIn line
            li_html = ""
            if linkedin.get("found") and linkedin.get("headline"):
                li_html = (f'<div style="font-size:11px;color:var(--gray);margin:4px 0 8px">'
                           f'LinkedIn: {esc(linkedin["headline"])}</div>')

            # Opportunity rows
            opp_rows = ""
            for opp in cred_opps:
                cred_name  = opp.get("credential", "")
                niches_str = ", ".join(opp.get("niche_opportunities", []))
                on_site    = opp.get("site_mentions_this", False)
                gap_note   = opp.get("gap_note", "")
                site_class = "td-pass" if on_site else "td-fail"
                site_txt   = "Yes" if on_site else "No"
                opp_rows += f"""
            <tr>
              <td><strong>{esc(cred_name)}</strong></td>
              <td style="font-size:11px">{esc(niches_str)}
                {(f'<div class="gap-note-text">{esc(gap_note)}</div>') if gap_note else ''}
              </td>
              <td class="{site_class}" style="text-align:center;white-space:nowrap">{site_txt}</td>
            </tr>"""

            opp_table = ""
            if opp_rows:
                opp_table = f"""
          <table class="opp-table">
            <thead><tr>
              <th>Credential</th>
              <th>Niche Opportunities</th>
              <th>On Site</th>
            </tr></thead>
            <tbody>{opp_rows}</tbody>
          </table>"""

            # Top gaps list
            gaps_html = ""
            if top_gaps_p:
                items = "".join(f'<li>{esc(g)}</li>' for g in top_gaps_p[:3])
                gaps_html = f'<ul class="staff-gaps-list" style="margin-top:10px">{items}</ul>'

            cards_html += f"""
        <div class="staff-card">
          <div class="staff-name">{esc(name)}</div>
          <div class="staff-title">{esc(title_p)}</div>
          <div style="margin-bottom:8px">{cred_badges}</div>
          <div style="margin-bottom:8px"><span class="{lev_class}">{lev_label}</span></div>
          {li_html}
          {opp_table}
          {gaps_html}
          {(f'<div style="font-size:12px;color:var(--gray);margin-top:10px;line-height:1.5">{esc(summary_p)}</div>') if summary_p else ''}
        </div>"""

        html += f'<div class="staff-grid">{cards_html}</div>'

    return html


# ── HTML builder ──────────────────────────────────────────────────────────────
def build_html(data: dict, config: dict, output_path: str,
               logo_path: str, logo_path_reversed: str = ""):

    firm        = config["firm"]
    url         = data.get("url", "")
    domain      = data.get("domain", "")
    audit_date  = data.get("audit_date", datetime.now().strftime("%Y-%m-%d"))
    sections    = data.get("sections", {})
    overall_grade = data.get("overall_grade", "N/A")
    overall_score = data.get("overall_score", 0)
    exec_summary  = data.get("executive_summary", "")
    recommendations = data.get("recommendations", [])
    intelligence    = data.get("intelligence_brief")
    staff_expertise = data.get("staff_expertise")

    logo_src    = logo_b64(logo_path_reversed) or logo_b64(logo_path)
    firm_name   = esc(firm.get("name", "CountingFive"))
    firm_url    = esc(firm.get("url", ""))
    firm_tagline = esc(firm.get("tagline", ""))

    deg     = ring_degrees(overall_score)
    r_color = score_bar_color(overall_score)
    gc      = grade_class(overall_grade)

    # ── CSS ────────────────────────────────────────────────────────────────────
    css = """
  :root {
    --dark:   #1A1A2E;
    --accent: #E94560;
    --mid:    #16213E;
    --gray:   #6B7280;
    --green:  #10B981;
    --yellow: #F59E0B;
    --red:    #DC2626;
    --light:  #F9FAFB;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         background: #F3F4F6; color: #1F2937; font-size: 14px; line-height: 1.6; }
  a { color: var(--mid); }

  /* ── Header ── */
  .site-header { background: var(--dark); padding: 16px 32px;
                 display: flex; align-items: center; justify-content: space-between; }
  .logo { height: 36px; }
  .logo-text { color: white; font-size: 18px; font-weight: bold; }
  .header-meta { color: #9CA3AF; font-size: 12px; text-align: right; }
  .header-meta strong { color: white; }

  /* ── Hero ── */
  .hero { background: linear-gradient(135deg, var(--dark) 0%, var(--mid) 100%); padding: 48px 32px; }
  .hero-inner { max-width: 960px; margin: 0 auto; display: grid;
                grid-template-columns: auto 1fr; gap: 48px; align-items: center; }
  .score-ring { width: 140px; height: 140px; border-radius: 50%;
                display: flex; align-items: center; justify-content: center; }
  .score-ring-inner { width: 110px; height: 110px; border-radius: 50%; background: var(--mid);
                      display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .score-number { font-size: 38px; font-weight: 900; line-height: 1; }
  .score-label  { font-size: 11px; color: #9CA3AF; margin-top: 2px; }
  .score-grade  { font-size: 14px; color: #9CA3AF; margin-top: 2px; }
  .hero-text h1 { font-size: 28px; color: white; font-weight: 800; }
  .hero-text .site-url { color: #9CA3AF; font-size: 13px; margin-top: 4px; }
  .hero-text .verdict  { color: #D1D5DB; margin-top: 12px; font-size: 15px; line-height: 1.65; }
  .hero-pills { display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
  .pill { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
          color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
  .pill.red   { background: rgba(220,38,38,0.2);  border-color: rgba(220,38,38,0.4); }
  .pill.green { background: rgba(16,185,129,0.2); border-color: rgba(16,185,129,0.4); }

  /* ── Top findings box ── */
  .top-findings { background: rgba(233,69,96,0.1); border: 1px solid rgba(233,69,96,0.3);
                  border-radius: 8px; padding: 16px 20px; margin-top: 24px; }
  .top-findings h3 { color: var(--accent); font-size: 12px; text-transform: uppercase;
                     letter-spacing: 1px; margin-bottom: 10px; }
  .top-rec { color: #D1D5DB; font-size: 13px; margin-bottom: 6px;
             display: flex; align-items: flex-start; gap: 8px; }
  .rec-dot { width: 8px; height: 8px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
  .rec-dot.red    { background: var(--red); }
  .rec-dot.yellow { background: var(--yellow); }
  .rec-dot.green  { background: var(--green); }

  /* ── Layout ── */
  .main { max-width: 960px; margin: 0 auto; padding: 32px 16px; }
  .section-title { font-size: 20px; font-weight: 700; color: var(--dark);
                   margin: 32px 0 16px; padding-bottom: 8px; border-bottom: 2px solid var(--accent); }

  /* ── Dashboard ── */
  .dashboard { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
               gap: 12px; margin-bottom: 32px; }
  .dash-card  { background: white; border-radius: 8px; padding: 16px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  .dash-label { font-size: 11px; color: var(--gray); text-transform: uppercase;
                letter-spacing: 0.5px; margin-bottom: 8px; }
  .dash-score { margin-bottom: 8px; }
  .dash-bar   { height: 4px; background: #E5E7EB; border-radius: 2px; margin-bottom: 6px; }
  .dash-bar-fill { height: 4px; border-radius: 2px; }

  /* ── Category sections ── */
  .cat-section { background: white; border-radius: 8px; margin-bottom: 16px;
                 overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  .cat-header  { display: flex; align-items: center; justify-content: space-between;
                 padding: 16px 20px; background: var(--dark); cursor: pointer; user-select: none; }
  .cat-header:hover { background: var(--mid); }
  .cat-header h3 { color: white; font-size: 15px; }
  .cat-body       { padding: 20px; display: none; }
  .cat-body.open  { display: block; }
  .chevron        { color: #9CA3AF; font-size: 12px; transition: transform 0.2s; display: inline-block; }
  .chevron.open   { transform: rotate(180deg); }

  /* ── Narrative callout ── */
  .narrative-label { font-size: 11px; font-weight: 700; color: var(--gray);
                     text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
  .narrative { color: #374151; font-size: 14px; line-height: 1.65; margin-bottom: 20px;
               padding: 14px 16px; background: #F8FAFC;
               border-left: 3px solid var(--accent); border-radius: 0 6px 6px 0; }

  /* ── Sub-score table ── */
  .check-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 16px; }
  .check-table th { background: var(--dark); color: white; padding: 8px 12px;
                    text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
  .check-table tr:nth-child(even) { background: #F9FAFB; }
  .check-table td { padding: 8px 12px; border-bottom: 1px solid #E5E7EB; vertical-align: middle; }
  .check-label { font-weight: 500; width: 40%; }
  .td-pass { color: var(--green); }
  .td-warn { color: #92400E; }
  .td-fail { color: var(--red); font-weight: 600; }

  /* ── Badges ── */
  .badge    { display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px;
              border-radius: 4px; font-size: 13px; font-weight: 700; }
  .badge-a  { background: #D1FAE5; color: #065F46; }
  .badge-b  { background: #DBEAFE; color: #1E3A5F; }
  .badge-c  { background: #FEF3C7; color: #78350F; }
  .badge-d  { background: #FEE2E2; color: #7F1D1D; }
  .badge-f  { background: #FEE2E2; color: #7F1D1D; }
  .badge-na { background: #F3F4F6; color: #6B7280; }

  /* ── Score bars ── */
  .bar-wrap  { display: inline-block; width: 80px; height: 8px; background: #E5E7EB;
               border-radius: 4px; vertical-align: middle; margin-right: 6px; }
  .bar-fill  { display: block; height: 8px; border-radius: 4px; }
  .bar-label { font-size: 12px; color: var(--gray); }

  /* ── Priority tags ── */
  .priority-high   { background: #FEE2E2; color: var(--red);  padding: 2px 8px;
                     border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
  .priority-medium { background: #FEF3C7; color: #78350F;    padding: 2px 8px;
                     border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
  .priority-low    { background: #D1FAE5; color: #065F46;    padding: 2px 8px;
                     border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; }

  /* ── Recommendations table ── */
  .rec-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .rec-table th { background: var(--dark); color: white; padding: 10px 14px;
                  text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
  .rec-table td { padding: 10px 14px; border-bottom: 1px solid #E5E7EB; vertical-align: top; }
  .rec-table tr:nth-child(even) { background: #F9FAFB; }
  .detail-text { color: var(--gray); line-height: 1.5; margin-top: 4px; font-size: 12px; }

  /* ── Services table ── */
  .svc-table { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 12px; }
  .svc-table th { background: var(--dark); color: white; padding: 7px 10px;
                  text-align: left; font-size: 11px; text-transform: uppercase; }
  .svc-table td { padding: 7px 10px; border-bottom: 1px solid #E5E7EB; vertical-align: top; }
  .svc-table tr:nth-child(even) { background: #F9FAFB; }
  .tag-green  { background: #D1FAE5; color: #065F46; padding: 2px 7px;
                border-radius: 4px; font-size: 11px; font-weight: 600; white-space: nowrap; }
  .tag-yellow { background: #FEF3C7; color: #92400E; padding: 2px 7px;
                border-radius: 4px; font-size: 11px; font-weight: 600; white-space: nowrap; }
  .tag-red    { background: #FEE2E2; color: #7F1D1D; padding: 2px 7px;
                border-radius: 4px; font-size: 11px; font-weight: 600; white-space: nowrap; }

  /* ── Niche pills ── */
  .niche-pill           { display: inline-block; background: rgba(233,69,96,0.08);
                          border: 1px solid rgba(233,69,96,0.25); color: var(--dark);
                          padding: 3px 10px; border-radius: 12px; font-size: 12px;
                          margin: 3px 4px 3px 0; cursor: default; }
  .niche-pill.confirmed { background: #D1FAE5; border-color: #6EE7B7; color: #065F46; }
  .niche-pill.weak      { background: #FEF3C7; border-color: #FCD34D; color: #78350F; }
  .niche-pill.invisible { background: #EFF6FF; border-color: #BFDBFE; color: #1E3A5F; }

  /* ── CTA box ── */
  .cta-box    { background: var(--dark); color: white; padding: 28px 32px;
                border-radius: 8px; margin-top: 32px; text-align: center; }
  .cta-box h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
  .cta-box p  { color: #9CA3AF; font-size: 14px; line-height: 1.6; }
  .cta-box a  { color: var(--accent); text-decoration: none; }

  /* ── Digital Intelligence Brief ── */
  .intel-wrapper { border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                   margin-bottom: 16px; }
  .intel-header  { background: var(--dark); color: white; padding: 14px 20px;
                   display: flex; align-items: center; justify-content: space-between; }
  .intel-tag     { background: rgba(233,69,96,0.2); border: 1px solid rgba(233,69,96,0.4);
                   color: var(--accent); padding: 2px 10px; border-radius: 12px; font-size: 11px; }
  .intel-body    { background: white; padding: 20px; }
  .intel-sub     { font-size: 12px; font-weight: 700; color: var(--gray);
                   text-transform: uppercase; letter-spacing: 0.5px;
                   margin: 20px 0 10px; border-bottom: 1px solid #E5E7EB; padding-bottom: 4px; }
  .intel-sub:first-child { margin-top: 0; }

  /* ── Staff & Expertise Profile ── */
  .staff-grid    { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                   gap: 16px; margin: 16px 0; }
  .staff-card    { background: white; border-radius: 8px; border: 1px solid #E5E7EB;
                   padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
  .staff-name    { font-size: 15px; font-weight: 700; color: var(--dark); }
  .staff-title   { font-size: 12px; color: var(--gray); margin: 2px 0 8px; }
  .cred-badge    { display: inline-block; background: var(--dark); color: white;
                   font-size: 10px; font-weight: 700; padding: 2px 7px;
                   border-radius: 3px; margin: 0 3px 3px 0; letter-spacing: 0.5px; }
  .leverage-full    { background: #D1FAE5; color: #065F46; padding: 3px 10px;
                      border-radius: 12px; font-size: 11px; font-weight: 700; }
  .leverage-partial { background: #FEF3C7; color: #78350F; padding: 3px 10px;
                      border-radius: 12px; font-size: 11px; font-weight: 700; }
  .leverage-none    { background: #FEE2E2; color: #7F1D1D; padding: 3px 10px;
                      border-radius: 12px; font-size: 11px; font-weight: 700; }
  .opp-table     { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 10px; }
  .opp-table th  { background: #F3F4F6; color: #374151; padding: 6px 10px;
                   text-align: left; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
  .opp-table td  { padding: 7px 10px; border-bottom: 1px solid #F3F4F6; vertical-align: top; }
  .gap-note-text { font-size: 11px; color: var(--gray); font-style: italic; margin-top: 3px; }
  .staff-summary-box { background: var(--dark); color: white; border-radius: 8px;
                       padding: 16px 20px; margin-bottom: 16px; }
  .staff-summary-box h4 { margin: 0 0 8px; font-size: 13px; font-weight: 700;
                          color: var(--accent); text-transform: uppercase; letter-spacing: 0.5px; }
  .staff-summary-box p  { font-size: 13px; line-height: 1.6; margin: 0 0 8px; color: #D1D5DB; }
  .staff-gaps-list { list-style: none; padding: 10px 0 0; margin: 0; }
  .staff-gaps-list li { font-size: 12px; color: #374151; padding: 4px 0;
                        padding-left: 16px; position: relative; }
  .staff-gaps-list li::before { content: "›"; position: absolute; left: 0;
                                 color: var(--accent); font-weight: 700; }
  .staff-summary-box .staff-gaps-list li { color: #D1D5DB; }
  .staff-summary-box .staff-gaps-list li::before { color: #FCD34D; }
  @media print {
    .staff-card { page-break-inside: avoid; box-shadow: none; border: 1px solid #E5E7EB; }
    .staff-summary-box { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }

  /* ── Personnel cards ── */
  .person-card  { border: 1px solid #E5E7EB; border-radius: 6px; padding: 14px 16px; margin-bottom: 12px; }
  .person-name  { font-size: 15px; font-weight: 700; color: var(--dark); }
  .person-title { font-size: 12px; color: var(--gray); margin-top: 2px; }
  .person-creds { font-size: 11px; font-weight: 600; color: var(--accent); margin-top: 2px; }
  .person-grid  { display: grid; grid-template-columns: 120px 1fr; gap: 4px 12px;
                  margin-top: 10px; font-size: 12px; }
  .person-lbl   { color: var(--gray); font-weight: 600; }
  .person-val   { color: #374151; }
  .person-summary { font-size: 12px; color: #4B5563; font-style: italic; margin-top: 10px;
                    padding: 8px 12px; background: #F9FAFB; border-radius: 4px; line-height: 1.5; }
  .footprint-strong   { color: var(--green); font-weight: 700; }
  .footprint-moderate { color: var(--yellow); font-weight: 700; }
  .footprint-minimal  { color: var(--gray); font-weight: 700; }

  /* ── Reputation ── */
  .rating-row   { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 10px; }
  .rating-item  { background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 8px 14px; }
  .rating-stars { font-weight: 700; color: var(--dark); font-size: 14px; }
  .rating-src   { font-size: 11px; color: var(--gray); margin-top: 2px; }
  .theme-tag    { display: inline-block; background: #F0FDF4; border: 1px solid #BBF7D0;
                  color: #065F46; padding: 2px 8px; border-radius: 12px;
                  font-size: 12px; margin: 2px 3px 2px 0; }
  .concern-tag  { display: inline-block; background: #FEF2F2; border: 1px solid #FECACA;
                  color: #7F1D1D; padding: 2px 8px; border-radius: 12px;
                  font-size: 12px; margin: 2px 3px 2px 0; }
  .review-quote { font-size: 13px; color: #4B5563; font-style: italic;
                  border-left: 3px solid #E5E7EB; padding: 6px 12px;
                  margin: 6px 0; line-height: 1.5; }

  /* ── Social accounts ── */
  .social-row    { display: flex; gap: 12px; flex-wrap: wrap; }
  .social-card   { border: 1px solid #E5E7EB; border-radius: 6px; padding: 10px 14px; font-size: 12px; }
  .social-plat   { font-weight: 700; color: var(--dark); font-size: 13px; }
  .social-active  { color: var(--green); font-weight: 600; font-size: 11px; }
  .social-low     { color: var(--yellow); font-weight: 600; font-size: 11px; }
  .social-dormant { color: var(--gray); font-weight: 600; font-size: 11px; }

  /* ── Niche gap ── */
  .gap-grid      { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
  .gap-box       { background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 12px 14px; }
  .gap-box-label { font-size: 11px; font-weight: 700; color: var(--gray);
                   text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
  .gap-summary   { font-size: 13px; color: #374151; font-style: italic;
                   background: #EFF6FF; border: 1px solid #BFDBFE;
                   border-radius: 6px; padding: 12px 16px; line-height: 1.6; }

  /* ── Note ── */
  .note { font-size: 12px; color: var(--gray); margin-top: 12px; padding: 8px 12px;
          background: #F9FAFB; border-left: 3px solid #E5E7EB; border-radius: 0 4px 4px 0; }

  /* ── Footer ── */
  .site-footer  { background: var(--dark); padding: 24px 32px; margin-top: 48px;
                  display: flex; align-items: center; justify-content: space-between; }
  .logo-footer  { height: 28px; }
  .footer-text  { color: #6B7280; font-size: 12px; text-align: right; }
  .footer-text a { color: #9CA3AF; text-decoration: none; }

  /* ── Responsive ── */
  @media (max-width: 600px) {
    .hero-inner { grid-template-columns: 1fr; gap: 24px; }
    .score-ring { margin: 0 auto; }
    .gap-grid   { grid-template-columns: 1fr; }
  }

  /* ── Print ── */
  @media print {
    .cat-body       { display: block !important; }
    .cat-header     { cursor: default; background: #1A1A2E !important;
                      -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .chevron        { display: none; }
    .hero           { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .intel-header   { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    body            { background: white; }
    .cat-section    { page-break-inside: avoid; box-shadow: none; border: 1px solid #E5E7EB; }
    .site-footer    { margin-top: 24px; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .dashboard      { page-break-inside: avoid; }
    .intel-wrapper  { page-break-inside: avoid; }
  }
"""

    # ── Hero pills ────────────────────────────────────────────────────────────
    grades = [sections.get(k, {}).get("grade", "N/A") for k, _ in SECTION_META]
    high_count = sum(1 for g in grades if g.startswith("A"))
    ok_count   = sum(1 for g in grades if g.startswith("B"))
    warn_count = sum(1 for g in grades if g.startswith(("C", "D", "F")))

    pills_html = ""
    if high_count:
        pills_html += f'<span class="pill green">{high_count} Strong</span>'
    if ok_count:
        pills_html += f'<span class="pill">{ok_count} Passing</span>'
    if warn_count:
        pills_html += f'<span class="pill red">{warn_count} Need Work</span>'

    # ── Top recommendations in hero ───────────────────────────────────────────
    top_recs_html = ""
    if recommendations:
        recs_items = ""
        for rec in recommendations[:3]:
            priority  = rec.get("priority", "Medium")
            dot_class = "red" if priority == "High" else ("yellow" if priority == "Medium" else "green")
            recs_items += f"""
            <div class="top-rec">
              <span class="rec-dot {dot_class}"></span>
              <span>{esc(rec.get("issue", ""))}</span>
            </div>"""
        top_recs_html = f"""
        <div class="top-findings">
          <h3>Top Recommendations</h3>
          {recs_items}
        </div>"""

    # ── Dashboard cards ───────────────────────────────────────────────────────
    dashboard_html = ""
    for key, label in SECTION_META:
        sec   = sections.get(key, {})
        grade = sec.get("grade", "N/A")
        avg   = sec.get("average_score", "N/A")
        icon  = SECTION_ICONS.get(key, "")
        gc_d  = grade_class(grade)
        short_label = label.replace(icon + " ", "").strip() if icon else label.strip()

        if avg not in (None, "N/A") and isinstance(avg, (int, float)):
            bar_pct   = min(100, max(0, float(avg) / 10 * 100))
            bar_color = score_bar_color(avg)
            bar_html  = (f'<div class="dash-bar">'
                         f'<div class="dash-bar-fill" style="width:{bar_pct:.0f}%;background:{bar_color}"></div>'
                         f'</div>')
            score_txt = fmt_score(avg)
        else:
            bar_html  = '<div class="dash-bar"><div class="dash-bar-fill" style="width:0%"></div></div>'
            score_txt = "N/A"

        dashboard_html += f"""
    <div class="dash-card">
      <div class="dash-label">{esc(short_label)}</div>
      <div class="dash-score">
        <span class="badge badge-{gc_d}">{esc(grade)}&nbsp;&nbsp;{esc(score_txt)}</span>
      </div>
      {bar_html}
    </div>"""

    staff_expertise_html = build_staff_expertise_html(staff_expertise) if staff_expertise else ""

    # ── Digital Intelligence Brief (built early so it can be injected inline) ──
    intel_html = ""
    if intelligence:
        intel_body = ""

        # Personnel
        personnel = intelligence.get("personnel", [])
        if personnel:
            persons_html = ""
            for p in personnel:
                name      = p.get("name", "")
                title_p   = p.get("title", "")
                creds     = ", ".join(p.get("credentials", []))
                footprint = p.get("footprint_strength", "minimal").lower()
                fp_class  = (f"footprint-{footprint}"
                             if footprint in ("strong", "moderate", "minimal")
                             else "footprint-minimal")
                linkedin  = p.get("linkedin_signals", "")
                twitter   = p.get("twitter_presence", "")
                assocs    = ", ".join(p.get("associations_found", []))
                niches    = ", ".join(p.get("niche_signals", []))
                cf_items  = " | ".join(p.get("content_found", [])[:3])
                summary   = p.get("summary", "")

                detail_rows = ""
                for lbl, val in [("LinkedIn", linkedin), ("Twitter/X", twitter),
                                  ("Associations", assocs), ("Niche Signals", niches)]:
                    if val:
                        detail_rows += (f'<div class="person-lbl">{esc(lbl)}</div>'
                                        f'<div class="person-val">{esc(val)}</div>')
                if cf_items:
                    detail_rows += (f'<div class="person-lbl">Content Found</div>'
                                    f'<div class="person-val">{esc(cf_items)}</div>')

                persons_html += f"""
          <div class="person-card">
            <div class="person-name">{esc(name)}</div>
            {('<div class="person-title">' + esc(title_p) + '</div>') if title_p else ''}
            {('<div class="person-creds">' + esc(creds) + '</div>') if creds else ''}
            <div style="margin-top:6px">
              <span class="{fp_class}">{esc(footprint.title())} Online Footprint</span>
            </div>
            {('<div class="person-grid">' + detail_rows + '</div>') if detail_rows else ''}
            {('<div class="person-summary">' + esc(summary) + '</div>') if summary else ''}
          </div>"""
            intel_body += f'<div class="intel-sub">Key Personnel</div>{persons_html}'

        # Reputation
        rep = intelligence.get("reputation_signals", {})
        if rep:
            sentiment  = rep.get("overall_sentiment", "not found")
            sent_color = ("#10B981" if sentiment == "positive"
                          else "#F59E0B" if sentiment == "mixed"
                          else "#DC2626" if sentiment == "negative"
                          else "#9CA3AF")
            ratings_html = ""
            for src, rk, ck in [("Google", "google_business_rating", "google_review_count"),
                                  ("Yelp",   "yelp_rating",           None),
                                  ("Clutch", "clutch_rating",         None)]:
                rating = rep.get(rk)
                if rating:
                    count     = rep.get(ck, "") if ck else ""
                    count_txt = f" ({count} reviews)" if count else ""
                    ratings_html += (f'<div class="rating-item">'
                                     f'<div class="rating-stars">&#9733; {esc(str(rating))}'
                                     f'{esc(count_txt)}</div>'
                                     f'<div class="rating-src">{src}</div></div>')
            if rep.get("bbb_rating"):
                ratings_html += (f'<div class="rating-item">'
                                  f'<div class="rating-stars">{esc(rep["bbb_rating"])}</div>'
                                  f'<div class="rating-src">BBB</div></div>')

            praise_tags  = "".join(
                f'<span class="theme-tag">{esc(t)}</span>' for t in rep.get("praise_themes", []))
            concern_tags = "".join(
                f'<span class="concern-tag">{esc(t)}</span>' for t in rep.get("concern_themes", []))
            reviews_html = "".join(
                f'<div class="review-quote">&ldquo;{esc(r)}&rdquo;</div>'
                for r in rep.get("notable_reviews", rep.get("representative_reviews", []))[:3])

            intel_body += f"""
        <div class="intel-sub">Firm Reputation</div>
        <div style="margin-bottom:8px">Overall Sentiment:
          <strong style="color:{sent_color}">{esc(sentiment.title())}</strong>
        </div>
        {('<div class="rating-row">' + ratings_html + '</div>') if ratings_html else ''}
        {('<div style="margin:8px 0">' + praise_tags + '</div>') if praise_tags else ''}
        {('<div style="margin:4px 0">' + concern_tags + '</div>') if concern_tags else ''}
        {reviews_html}"""

        # Associations
        assocs = intelligence.get("associations", [])
        if assocs:
            assoc_items = "".join(
                f'<li style="margin-bottom:4px;font-size:13px">'
                f'<strong>{esc(a.get("name",""))}</strong> &mdash; {esc(a.get("evidence",""))}'
                f'</li>'
                for a in assocs)
            intel_body += (f'<div class="intel-sub">Associations &amp; Affiliations</div>'
                           f'<ul style="list-style:none;padding:0">{assoc_items}</ul>')

        # Content footprint
        cf = intelligence.get("content_footprint", [])
        if cf:
            cf_rows = "".join(
                f'<tr>'
                f'<td>{esc(item.get("type","").title())}</td>'
                f'<td>{esc(item.get("title",""))}</td>'
                f'<td>{esc(item.get("source",""))}</td>'
                f'<td style="color:var(--accent);font-style:italic">'
                f'{esc(item.get("niche_relevance",""))}</td>'
                f'</tr>'
                for item in cf)
            intel_body += (f'<div class="intel-sub">Content Footprint</div>'
                           f'<table class="svc-table">'
                           f'<thead><tr><th>Type</th><th>Title</th>'
                           f'<th>Source</th><th>Niche</th></tr></thead>'
                           f'<tbody>{cf_rows}</tbody></table>')

        # Social accounts
        social = intelligence.get("social_accounts", [])
        if social:
            soc_cards = ""
            for acc in social:
                activity  = acc.get("activity_level", "not found").lower()
                act_class = (f"social-{activity}"
                             if activity in ("active", "low", "dormant")
                             else "social-dormant")
                followers = f" &middot; {acc['followers_approx']}" if acc.get("followers_approx") else ""
                soc_cards += (f'<div class="social-card">'
                              f'<div class="social-plat">{esc(acc.get("platform",""))}</div>'
                              f'<div class="{act_class}">'
                              f'{esc(activity.title())}{followers}</div>'
                              f'</div>')
            intel_body += (f'<div class="intel-sub">Social Presence</div>'
                           f'<div class="social-row">{soc_cards}</div>')

        # Niche gap analysis
        gap     = intelligence.get("niche_gap_analysis", {})
        ext     = gap.get("external_niches_found", [])
        web     = gap.get("website_niches", [])
        unlev   = gap.get("unleveraged_credibility", [])
        gap_sum = gap.get("gap_summary", "")
        if ext or unlev or gap_sum:
            ext_text  = ", ".join(ext) if ext else "None detected"
            web_text  = ", ".join(web) if web else "None detected"
            unlev_html = "".join(
                f'<li style="margin-bottom:4px;font-size:13px">&#9670; {esc(u)}</li>'
                for u in unlev)
            intel_body += f"""
        <div class="intel-sub">External vs. Website Niche Gap</div>
        <div class="gap-grid">
          <div class="gap-box">
            <div class="gap-box-label">Found Externally</div>
            <div style="font-size:13px">{esc(ext_text)}</div>
          </div>
          <div class="gap-box">
            <div class="gap-box-label">On Website</div>
            <div style="font-size:13px">{esc(web_text)}</div>
          </div>
        </div>
        {('<ul style="list-style:none;padding:0;margin-bottom:12px">' + unlev_html + '</ul>') if unlev_html else ''}
        {('<div class="gap-summary">' + esc(gap_sum) + '</div>') if gap_sum else ''}"""

        intel_html = f"""
  <div class="intel-wrapper">
    <div class="intel-header">
      <span style="font-size:15px;font-weight:700">&#128269; Digital Intelligence Brief</span>
      <span class="intel-tag">External Research &mdash; Not Scored</span>
    </div>
    <div class="intel-body">
      {intel_body}
    </div>
  </div>"""

    # ── Collapsible category sections ─────────────────────────────────────────
    section_order = [
        ("target_market_clarity",  "Target Market Clarity"),
        ("competitive_visibility", "Competitive Search Visibility"),
        ("niche_intelligence",     "Niche & Services Intelligence"),
        ("seo_health",             "SEO / AIO / GEO Health"),
        ("mobile_responsiveness",  "Mobile Responsiveness"),
        ("site_speed",             "Site Speed & Performance"),
        ("technology_stack",       "Technology Stack"),
        ("site_health",            "Site Age, Health & Errors"),
    ]

    cat_sections_html = ""
    for i, (key, title) in enumerate(section_order):
        sec = sections.get(key)
        if not sec:
            continue

        # Section-group divider before the technical sections
        if key == "seo_health":
            cat_sections_html += """
  <h2 class="section-title" style="margin-top:40px">Technical Site Health</h2>
  <p style="color:var(--gray);font-size:13px;margin-bottom:16px">
    Infrastructure, search optimization, and platform performance findings.
  </p>"""

        grade     = sec.get("grade", "N/A")
        avg       = sec.get("average_score", "N/A")
        gc_c      = grade_class(grade)
        sub_scores = sec.get("sub_scores", {})
        narrative  = sec.get("narrative", "")
        score_disp = fmt_score(avg)

        badge_html = (f'<span class="badge badge-{gc_c}">'
                      f'{esc(grade)}&nbsp;&nbsp;{esc(score_disp)}</span>')

        body_content = ""

        # Narrative
        if narrative:
            body_content += f"""
      <p class="narrative-label">What This Means</p>
      <div class="narrative">{esc(narrative)}</div>"""

        # Sub-score table
        if sub_scores:
            rows = ""
            for name, score in sub_scores.items():
                label_nice = name.replace("_", " ")
                is_na = isinstance(score, str) and score.upper().startswith("N/A")
                if is_na or score is None:
                    bar_html  = ('<span class="bar-wrap">'
                                 '<span class="bar-fill" style="width:0%;background:#9CA3AF"></span>'
                                 '</span>')
                    score_txt = "N/A"
                    td_class  = ""
                else:
                    try:
                        s    = float(score)
                        pct  = min(100, max(0, s / 10 * 100))
                        col  = score_bar_color(s)
                        bar_html = (f'<span class="bar-wrap">'
                                    f'<span class="bar-fill" style="width:{pct:.0f}%;background:{col}"></span>'
                                    f'</span>')
                        score_txt = f"{score}/10"
                        td_class  = ("td-pass" if s >= 7.5
                                     else ("td-warn" if s >= 5.5
                                     else "td-fail"))
                    except (TypeError, ValueError):
                        bar_html  = '<span class="bar-wrap"><span class="bar-fill" style="width:0%"></span></span>'
                        score_txt = str(score)
                        td_class  = ""

                rows += f"""
        <tr>
          <td class="check-label">{esc(label_nice)}</td>
          <td class="{td_class}">{bar_html}<span class="bar-label">{esc(score_txt)}</span></td>
        </tr>"""

            body_content += f"""
      <table class="check-table">
        <thead><tr>
          <th>Metric</th>
          <th>Score</th>
        </tr></thead>
        <tbody>{rows}
        </tbody>
      </table>"""

        # Niche Intelligence extras
        if key == "niche_intelligence":
            services = sec.get("services_analysis", [])
            detected = sec.get("niches_detected", [])
            invisible = sec.get("niches_invisible", [])
            top3      = sec.get("top_3_improvements", [])

            if services:
                svc_rows = ""
                for svc in services:
                    clarity  = svc.get("clarity_to_non_accountant", "—")
                    framing  = svc.get("framing", "—")
                    audience = svc.get("audience", "—")
                    rewrite  = svc.get("rewrite_direction", "—")
                    c_class  = ("tag-green" if clarity  == "Clear"
                                else ("tag-yellow" if clarity  == "Moderate"   else "tag-red"))
                    f_class  = ("tag-green" if "Outcome" in framing
                                else ("tag-yellow" if "Mixed" in framing       else "tag-red"))
                    a_class  = "tag-green" if "Niche" in audience else "tag-yellow"
                    svc_rows += f"""
          <tr>
            <td><strong>{esc(svc.get("service_name","—"))}</strong></td>
            <td><span class="{c_class}">{esc(clarity)}</span></td>
            <td><span class="{f_class}">{esc(framing)}</span></td>
            <td><span class="{a_class}">{esc(audience)}</span></td>
            <td style="font-style:italic;color:#6B7280;font-size:12px">{esc(rewrite)}</td>
          </tr>"""
                body_content += f"""
      <p class="narrative-label" style="margin-top:16px">Services Communication Analysis</p>
      <div style="overflow-x:auto">
        <table class="svc-table">
          <thead><tr>
            <th>Service</th><th>Clarity</th><th>Framing</th><th>Audience</th><th>Rewrite Direction</th>
          </tr></thead>
          <tbody>{svc_rows}</tbody>
        </table>
      </div>"""

            if detected:
                det_pills = ""
                for item in detected:
                    conf       = item.get("confidence", "weak signal")
                    pill_class = "confirmed" if conf == "confirmed" else "weak"
                    evidence   = item.get("evidence", "")
                    det_pills += (f'<span class="niche-pill {pill_class}" title="{esc(evidence)}">'
                                  f'{esc(item.get("niche",""))} '
                                  f'<small>({esc(conf)})</small></span>')
                body_content += f"""
      <p class="narrative-label" style="margin-top:16px">Detected Niches</p>
      <div style="margin-bottom:8px">{det_pills}</div>"""

            if invisible:
                inv_pills = ""
                for item in invisible:
                    rationale = item.get("rationale", "")
                    inv_pills += (f'<span class="niche-pill invisible" title="{esc(rationale)}">'
                                  f'{esc(item.get("niche",""))}</span>')
                body_content += f"""
      <p class="narrative-label" style="margin-top:8px">High-Opportunity Niches (Currently Invisible)</p>
      <div style="margin-bottom:8px">{inv_pills}</div>"""

            if top3:
                items_html = "".join(
                    f'<li style="margin-bottom:6px;font-size:13px">{j}. {esc(imp)}</li>'
                    for j, imp in enumerate(top3[:3], 1)
                )
                body_content += f"""
      <p class="narrative-label" style="margin-top:16px">Top 3 Highest-Impact Improvements</p>
      <ul style="list-style:none;padding:12px 16px;background:#F0FDF4;
                 border:1px solid #BBF7D0;border-radius:6px;margin-bottom:12px">
        {items_html}
      </ul>"""

        # First section starts open
        body_class   = " open" if i == 0 else ""
        chevron_class = " open" if i == 0 else ""

        cat_sections_html += f"""
  <div class="cat-section">
    <div class="cat-header" onclick="toggleSection(this)">
      <h3>{esc(title)}</h3>
      <div style="display:flex;align-items:center;gap:12px">
        {badge_html}
        <span class="chevron{chevron_class}">&#9660;</span>
      </div>
    </div>
    <div class="cat-body{body_class}">
      {body_content}
    </div>
  </div>"""

        # Inject Staff & Expertise Profile, then Digital Intelligence Brief
        if key == "niche_intelligence":
            if staff_expertise_html:
                cat_sections_html += f"""
  <h2 class="section-title" style="margin-top:32px">Staff &amp; Expertise Profile</h2>
  <p style="color:var(--gray);font-size:13px;margin-bottom:16px">
    External research &mdash; not scored. Credential-to-niche gap analysis.
  </p>
  {staff_expertise_html}"""
            if intel_html:
                cat_sections_html += f"""
  <h2 class="section-title" style="margin-top:40px">Digital Intelligence Brief</h2>
  {intel_html}"""

    # ── Recommendations ───────────────────────────────────────────────────────
    recs_html = ""
    if recommendations:
        rec_rows = ""
        for rec in recommendations:
            priority     = rec.get("priority", "Medium")
            issue        = rec.get("issue", "")
            impact       = rec.get("impact", "")
            service      = rec.get("countingfive_service", "")
            section_name = rec.get("section", "")
            p_lc         = priority.lower()
            p_class      = (f"priority-{p_lc}" if p_lc in ("high", "medium", "low")
                            else "priority-medium")
            rec_rows += f"""
        <tr>
          <td><span class="{p_class}">{esc(priority)}</span></td>
          <td>
            <strong>{esc(issue)}</strong>
            {(f'<div class="detail-text">{esc(impact)}</div>') if impact else ''}
          </td>
          <td style="font-size:12px;color:#374151">{esc(section_name)}</td>
          <td style="font-size:12px;color:#374151">{esc(service)}</td>
        </tr>"""

        recs_html = f"""
  <h2 class="section-title">Recommendations &amp; Next Steps</h2>
  <div style="overflow-x:auto">
    <table class="rec-table">
      <thead><tr>
        <th>Priority</th>
        <th>Issue &amp; Impact</th>
        <th>Section</th>
        <th>CountingFive Service</th>
      </tr></thead>
      <tbody>{rec_rows}</tbody>
    </table>
  </div>"""

    # ── CTA box ───────────────────────────────────────────────────────────────
    cta_html = f"""
  <div class="cta-box">
    <h3>Ready to Turn These Findings Into Results?</h3>
    <p>{firm_name} specializes in web design, development, hosting, and targeted content
       for accounting and tax professionals.<br>
       Visit <a href="{firm_url}">{firm_url}</a> to start a conversation.</p>
  </div>"""

    # ── Logo img tags ─────────────────────────────────────────────────────────
    logo_img = (f'<img src="{logo_src}" class="logo" alt="{firm_name}">'
                if logo_src else f'<span class="logo-text">{firm_name}</span>')
    logo_footer_img = (f'<img src="{logo_src}" class="logo-footer" alt="{firm_name}">'
                       if logo_src else f'<span style="color:white;font-weight:bold">{firm_name}</span>')

    score_display = fmt_score(overall_score)

    # ── Assemble final HTML ───────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Site Audit &mdash; {esc(domain)} &mdash; {esc(audit_date)}</title>
<style>{css}</style>
</head>
<body>

<header class="site-header">
  {logo_img}
  <div class="header-meta">
    <strong>{esc(domain)}</strong><br>
    Audit Date: {esc(audit_date)}
  </div>
</header>

<div class="hero">
  <div class="hero-inner">
    <div class="score-ring"
         style="background:conic-gradient({r_color} {deg}deg, rgba(255,255,255,0.1) 0deg)">
      <div class="score-ring-inner">
        <span class="score-number" style="color:{r_color}">{esc(score_display)}</span>
        <span class="score-label">out of 10</span>
        <span class="score-grade">{esc(overall_grade)}</span>
      </div>
    </div>
    <div class="hero-text">
      <h1>Site Audit Report</h1>
      <div class="site-url">
        <a href="{esc(url)}" style="color:#9CA3AF">{esc(url)}</a>
      </div>
      {(f'<div class="verdict">{esc(exec_summary)}</div>') if exec_summary else ''}
      <div class="hero-pills">{pills_html}</div>
      {top_recs_html}
    </div>
  </div>
</div>

<div class="main">

  <h2 class="section-title">Score Dashboard</h2>
  <div class="dashboard">
    {dashboard_html}
  </div>

  <h2 class="section-title">Section Details</h2>
  <p style="color:var(--gray);font-size:13px;margin-bottom:16px">
    Click any section to expand its findings.
  </p>
  {cat_sections_html}

  {recs_html}

  {cta_html}


</div>

<footer class="site-footer">
  {logo_footer_img}
  <div class="footer-text">
    {firm_name} &mdash; {firm_tagline}<br>
    <a href="{firm_url}">{firm_url}</a>
  </div>
</footer>

<script>
function toggleSection(header) {{
  const body    = header.nextElementSibling;
  const chevron = header.querySelector('.chevron');
  body.classList.toggle('open');
  if (chevron) chevron.classList.toggle('open');
}}
</script>

</body>
</html>"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML generated: {output_path}")


# ── Markdown builder (unchanged) ──────────────────────────────────────────────
def build_markdown(data: dict, config: dict, output_path: str):
    firm = config["firm"]
    url = data.get("url", "")
    domain = data.get("domain", "")
    audit_date = data.get("audit_date", datetime.now().strftime("%B %d, %Y"))
    sections = data.get("sections", {})
    overall_grade = data.get("overall_grade", "N/A")
    overall_score = data.get("overall_score", 0)
    exec_summary = data.get("executive_summary", "")
    recommendations = data.get("recommendations", [])

    lines = []
    lines.append(f"# Website Audit Report: {url}")
    lines.append(f"**Prepared by:** {firm['name']}  ")
    lines.append(f"**Date:** {audit_date}  ")
    lines.append(f"**Overall Grade:** {overall_grade} ({overall_score}/10)")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Executive Summary")
    lines.append("")
    if exec_summary:
        lines.append(exec_summary)
    lines.append("")

    lines.append("| Section | Score | Grade |")
    lines.append("|---------|-------|-------|")
    for key, label in SECTION_META:
        sec = sections.get(key, {})
        grade = sec.get("grade", "N/A")
        avg = sec.get("average_score", "N/A")
        lines.append(f"| {label} | {avg}/10 | **{grade}** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    section_configs = [
        ("target_market_clarity",  "Target Market Clarity"),
        ("competitive_visibility", "Competitive Search Visibility"),
        ("niche_intelligence",     "Niche & Services Intelligence"),
        ("seo_health",             "SEO / AIO / GEO Health"),
        ("mobile_responsiveness",  "Mobile Responsiveness"),
        ("site_speed",             "Site Speed & Performance"),
        ("technology_stack",       "Technology Stack"),
        ("site_health",            "Site Age, Health & Errors"),
    ]

    for key, title in section_configs:
        sec = sections.get(key)
        if not sec:
            continue
        grade = sec.get("grade", "N/A")
        avg = sec.get("average_score", "N/A")
        sub_scores = sec.get("sub_scores", {})
        narrative = sec.get("narrative", "")

        lines.append(f"## {title}")
        lines.append(f"**Grade: {grade}** | **Average Score: {avg}/10**")
        lines.append("")

        if sub_scores:
            lines.append("**Sub-Scores:**")
            lines.append("")
            for name, score in sub_scores.items():
                label = name.replace("_", " ").title()
                lines.append(f"- {label}: {score}/10")
            lines.append("")

        if narrative:
            lines.append(narrative)
        lines.append("")
        lines.append("---")
        lines.append("")

    niche = sections.get("niche_intelligence")
    if niche:
        grade = niche.get("grade", "N/A")
        avg   = niche.get("average_score", "N/A")
        lines.append("## 🏷 Niche & Services Intelligence")
        lines.append(f"**Grade: {grade}** | **Average Score: {avg}/10**")
        lines.append("")

        sub_scores = niche.get("sub_scores", {})
        if sub_scores:
            lines.append("**Niche Clarity Sub-Scores:**")
            lines.append("")
            for name, score in sub_scores.items():
                label = name.replace("_", " ").title()
                lines.append(f"- {label}: {score}/10")
            lines.append("")

        if niche.get("narrative"):
            lines.append(niche["narrative"])
            lines.append("")

        services = niche.get("services_analysis", [])
        if services:
            lines.append("### Services Communication Analysis")
            lines.append("")
            lines.append("| Service | Clarity | Framing | Audience | Rewrite Direction |")
            lines.append("|---------|---------|---------|----------|-------------------|")
            for svc in services:
                lines.append(
                    f"| {svc.get('service_name','—')} "
                    f"| {svc.get('clarity_to_non_accountant','—')} "
                    f"| {svc.get('framing','—')} "
                    f"| {svc.get('audience','—')} "
                    f"| {svc.get('rewrite_direction','—')} |"
                )
            lines.append("")

        detected = niche.get("niches_detected", [])
        if detected:
            lines.append("### Detected Niches")
            lines.append("")
            for item in detected:
                lines.append(f"- **{item.get('niche','')}** ({item.get('confidence','')}) — {item.get('evidence','')}")
            lines.append("")

        invisible = niche.get("niches_invisible", [])
        if invisible:
            lines.append("### Invisible but High-Opportunity Niches")
            lines.append("")
            for item in invisible:
                lines.append(f"- **{item.get('niche','')}** — {item.get('rationale','')}")
            lines.append("")

        top3 = niche.get("top_3_improvements", [])
        if top3:
            lines.append("### Top 3 Highest-Impact Improvements")
            lines.append("")
            for i, imp in enumerate(top3[:3], 1):
                lines.append(f"{i}. {imp}")
            lines.append("")

        lines.append("---")
        lines.append("")

    lines.append("## 💡 Recommendations & Next Steps")
    lines.append("")
    for i, rec in enumerate(recommendations, 1):
        lines.append(f"### {i}. {rec.get('issue', '')} ({rec.get('priority', '')} Priority)")
        if rec.get("impact"):
            lines.append(f"**Business Impact:** {rec['impact']}")
            lines.append("")
        if rec.get("countingfive_service"):
            lines.append(f"**CountingFive Can Help:** {rec['countingfive_service']}")
        lines.append("")

    brief = data.get("intelligence_brief")
    if brief:
        lines.append("## 🔎 Digital Intelligence Brief")
        lines.append("*External research — not scored*")
        lines.append("")

        personnel = brief.get("personnel", [])
        if personnel:
            lines.append("### Key Personnel Profiles")
            lines.append("")
            for p in personnel:
                creds = ", ".join(p.get("credentials", []))
                lines.append(f"#### {p.get('name','')} — {p.get('title','')} {('· ' + creds) if creds else ''}")
                lines.append(f"**Footprint Strength:** {p.get('footprint_strength','').title()}")
                if p.get("linkedin_signals"):
                    lines.append(f"**LinkedIn:** {p['linkedin_signals']}")
                if p.get("twitter_presence"):
                    lines.append(f"**Twitter/X:** {p['twitter_presence']}")
                if p.get("associations_found"):
                    lines.append(f"**Associations:** {', '.join(p['associations_found'])}")
                if p.get("niche_signals"):
                    lines.append(f"**Niche Signals:** {', '.join(p['niche_signals'])}")
                if p.get("content_found"):
                    lines.append(f"**Content Found:** {' | '.join(p['content_found'][:3])}")
                if p.get("summary"):
                    lines.append(f"")
                    lines.append(p["summary"])
                lines.append("")

        rep = brief.get("reputation_signals", {})
        if rep:
            lines.append("### Firm Reputation Signals")
            lines.append(f"**Overall Sentiment:** {rep.get('overall_sentiment','not found').title()}")
            ratings = []
            if rep.get("google_business_rating"):
                ratings.append(f"Google ★ {rep['google_business_rating']}" +
                               (f" ({rep['google_review_count']} reviews)" if rep.get("google_review_count") else ""))
            if rep.get("yelp_rating"):
                ratings.append(f"Yelp ★ {rep['yelp_rating']}")
            if rep.get("bbb_rating"):
                ratings.append(f"BBB: {rep['bbb_rating']}")
            if ratings:
                lines.append(f"**Ratings:** {' · '.join(ratings)}")
            if rep.get("praise_themes"):
                lines.append(f"**Praise Themes:** {', '.join(rep['praise_themes'])}")
            if rep.get("concern_themes"):
                lines.append(f"**Concern Themes:** {', '.join(rep['concern_themes'])}")
            if rep.get("representative_reviews"):
                lines.append("")
                lines.append("**Representative Reviews:**")
                for r in rep["representative_reviews"][:3]:
                    lines.append(f"> {r}")
            lines.append("")

        assoc = brief.get("associations", [])
        if assoc:
            lines.append("### Industry & Association Affiliations")
            lines.append("")
            for a in assoc:
                lines.append(f"- **{a.get('name','')}** — {a.get('evidence','')}")
            lines.append("")

        cf = brief.get("content_footprint", [])
        if cf:
            lines.append("### Content Footprint")
            lines.append("")
            lines.append("| Type | Title | Source | Niche |")
            lines.append("|------|-------|--------|-------|")
            for item in cf:
                lines.append(f"| {item.get('type','').title()} | {item.get('title','')} "
                             f"| {item.get('source','')} | {item.get('niche_relevance','')} |")
            lines.append("")

        soc = brief.get("social_accounts", [])
        if soc:
            lines.append("### Social Media Presence")
            lines.append("")
            for acc in soc:
                followers = f" · {acc['followers_approx']} followers" if acc.get("followers_approx") else ""
                lines.append(f"- **{acc.get('platform','')}**: {acc.get('activity_level','').title()}{followers}")
            lines.append("")

        gap = brief.get("niche_gap_analysis", {})
        ext = gap.get("external_niches_found", [])
        web = gap.get("website_niches", [])
        unlev = gap.get("unleveraged_credibility", [])
        gap_sum = gap.get("gap_summary", "")
        if ext or unlev or gap_sum:
            lines.append("### External vs. Website Niche Gap Analysis")
            lines.append("")
            if ext:
                lines.append(f"**Niches Found Externally:** {', '.join(ext)}")
            if web:
                lines.append(f"**Niches on Website:** {', '.join(web)}")
            if unlev:
                lines.append("")
                lines.append("**Unleveraged Credibility:**")
                for u in unlev:
                    lines.append(f"- {u}")
            if gap_sum:
                lines.append("")
                lines.append(f"> {gap_sum}")
            lines.append("")

        lines.append("---")
        lines.append("")

    lines.append(f"*{firm['name']} — {firm['tagline']}*  ")
    lines.append(f"*{firm['url']}*")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"✅ Markdown generated: {output_path}")


# ── Master Firm Profile builder (unchanged except .html reference) ────────────
def build_mfp(data: dict, config: dict, output_path: str):
    firm        = config["firm"]
    url         = data.get("url", "")
    domain      = data.get("domain", "")
    audit_date  = data.get("audit_date", datetime.now().strftime("%Y-%m-%d"))
    sections    = data.get("sections", {})
    overall_grade = data.get("overall_grade", "N/A")
    overall_score = data.get("overall_score", 0)
    recommendations = data.get("recommendations", [])

    tech   = sections.get("technology_stack", {})
    speed  = sections.get("site_speed", {})
    mobile = sections.get("mobile_responsiveness", {})
    seo    = sections.get("seo_health", {})
    health = sections.get("site_health", {})
    vis    = sections.get("competitive_visibility", {})
    niche  = sections.get("niche_intelligence", {})
    market = sections.get("target_market_clarity", {})

    lines = []
    lines.append(f"# Master Firm Profile: {domain}")
    lines.append(f"<!-- Generated by CountingFive Site Audit Skill -->")
    lines.append(f"<!-- This file is the entry point for future client workflows. -->")
    lines.append(f"<!-- Add new sections as data is collected. Do not remove existing sections. -->")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Firm Identity")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| **Domain** | {domain} |")
    lines.append(f"| **URL** | {url} |")
    lines.append(f"| **Audit Date** | {audit_date} |")
    lines.append(f"| **Prepared By** | {firm.get('name', '')} |")
    lines.append(f"| **Firm Name** | *(to be filled — not always available from site crawl)* |")
    lines.append(f"| **Primary Location** | *(to be filled)* |")
    lines.append(f"| **Firm Size Estimate** | *(to be filled)* |")
    lines.append("")

    lines.append("## Online Presence Scorecard")
    lines.append(f"**Overall Grade:** {overall_grade} | **Overall Score:** {overall_score}/10")
    lines.append("")
    lines.append("| Section | Score | Grade |")
    lines.append("|---------|-------|-------|")
    for key, label in SECTION_META:
        sec   = sections.get(key, {})
        grade = sec.get("grade", "N/A")
        avg   = sec.get("average_score", "N/A")
        lines.append(f"| {label} | {avg}/10 | {grade} |")
    lines.append("")

    lines.append("## Niche & Services Profile")
    lines.append("*Source: Niche & Services Intelligence (Agent E)*")
    lines.append("")

    niche_score = niche.get("average_score", "N/A")
    lines.append(f"**Niche Clarity Score:** {niche_score}/10 | **Grade:** {niche.get('grade','N/A')}")
    lines.append("")

    detected = niche.get("niches_detected", [])
    if detected:
        lines.append("**Confirmed/Detected Niches:**")
        lines.append("")
        for item in detected:
            lines.append(f"- **{item.get('niche','')}** ({item.get('confidence','')}) — {item.get('evidence','')}")
        lines.append("")

    invisible = niche.get("niches_invisible", [])
    if invisible:
        lines.append("**High-Opportunity Niches (Currently Invisible):**")
        lines.append("")
        for item in invisible:
            lines.append(f"- **{item.get('niche','')}** — {item.get('rationale','')}")
        lines.append("")

    services = niche.get("services_analysis", [])
    if services:
        lines.append("**Services Inventory:**")
        lines.append("")
        lines.append("| Service | Clarity | Framing | Audience | Rewrite Direction |")
        lines.append("|---------|---------|---------|----------|-------------------|")
        for svc in services:
            lines.append(
                f"| {svc.get('service_name','—')} "
                f"| {svc.get('clarity_to_non_accountant','—')} "
                f"| {svc.get('framing','—')} "
                f"| {svc.get('audience','—')} "
                f"| {svc.get('rewrite_direction','—')} |"
            )
        lines.append("")

    top3 = niche.get("top_3_improvements", [])
    if top3:
        lines.append("**Top 3 Niche Improvements:**")
        lines.append("")
        for i, imp in enumerate(top3[:3], 1):
            lines.append(f"{i}. {imp}")
        lines.append("")

    lines.append("## Technical Footprint")
    lines.append("*Source: Technology Stack Assessment (Agent B)*")
    lines.append("")
    tech_ss = tech.get("sub_scores", {})
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| **Technology Score** | {tech.get('average_score','N/A')}/10 ({tech.get('grade','N/A')}) |")
    lines.append(f"| **CMS / Platform** | *(detected by crawl — see audit .md)* |")
    lines.append(f"| **SSL Present** | *(see audit .md)* |")
    lines.append(f"| **CDN / Hosting Signals** | *(see audit .md)* |")
    lines.append(f"| **CMS Modernity** | {tech_ss.get('cms_platform_modernity','N/A')}/10 |")
    lines.append(f"| **Accessibility Signals** | {tech_ss.get('accessibility_signals','N/A')}/10 |")
    lines.append("")

    lines.append("## Search & Visibility")
    lines.append("*Source: Competitive Search Visibility (Agent C) + Site Health (Agent D)*")
    lines.append("")
    vis_ss    = vis.get("sub_scores", {})
    health_ss = health.get("sub_scores", {})
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| **Visibility Score** | {vis.get('average_score','N/A')}/10 ({vis.get('grade','N/A')}) |")
    lines.append(f"| **Domain Age** | *(see audit .md)* |")
    lines.append(f"| **Domain Age Score** | {health_ss.get('domain_age','N/A')}/10 |")
    lines.append(f"| **Best Keyword Ranking** | *(see audit .md)* |")
    lines.append(f"| **Local SEO Signals** | {vis_ss.get('local_seo_signals','N/A')}/10 |")
    lines.append(f"| **AI Search Presence** | {vis_ss.get('ai_search_presence','N/A')}/10 |")
    lines.append("")

    lines.append("## Performance Baseline")
    lines.append("*Source: Mobile Responsiveness + Site Speed (Agent A)*")
    lines.append("")
    mobile_ss = mobile.get("sub_scores", {})
    speed_ss  = speed.get("sub_scores", {})
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| **Mobile Score** | {mobile.get('average_score','N/A')}/10 ({mobile.get('grade','N/A')}) |")
    lines.append(f"| **Desktop Score** | {speed.get('average_score','N/A')}/10 ({speed.get('grade','N/A')}) |")
    lines.append(f"| **Mobile Performance Sub-Score** | {mobile_ss.get('mobile_performance','N/A')}/10 |")
    lines.append(f"| **LCP Mobile** | {mobile_ss.get('lcp_mobile','N/A')}/10 |")
    lines.append(f"| **CLS Mobile** | {mobile_ss.get('cls_mobile','N/A')}/10 |")
    lines.append(f"| **Desktop Performance Sub-Score** | {speed_ss.get('desktop_performance_score','N/A')}/10 |")
    lines.append("")

    lines.append("## Content & Trust Signals")
    lines.append("*Source: Target Market Clarity + SEO Health (Agent B)*")
    lines.append("")
    market_ss = market.get("sub_scores", {})
    seo_ss    = seo.get("sub_scores", {})
    lines.append(f"| Signal | Score |")
    lines.append(f"|--------|-------|")
    lines.append(f"| **Market Clarity Score** | {market.get('average_score','N/A')}/10 ({market.get('grade','N/A')}) |")
    lines.append(f"| **Who They Serve** | {market_ss.get('who_they_serve','N/A')}/10 |")
    lines.append(f"| **Trust Signals** | {market_ss.get('trust_signals','N/A')}/10 |")
    lines.append(f"| **CTA Alignment** | {market_ss.get('cta_alignment','N/A')}/10 |")
    lines.append(f"| **Schema Markup** | {seo_ss.get('json_ld_schema_markup','N/A')}/10 |")
    lines.append(f"| **SEO Health Score** | {seo.get('average_score','N/A')}/10 ({seo.get('grade','N/A')}) |")
    lines.append("")

    lines.append("## Top Recommendations from Audit")
    lines.append("")
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            priority = rec.get("priority", "")
            issue    = rec.get("issue", "")
            impact   = rec.get("impact", "")
            service  = rec.get("countingfive_service", "")
            lines.append(f"### {i}. {issue} ({priority} Priority)")
            if impact:
                lines.append(f"**Impact:** {impact}")
            if service:
                lines.append(f"**CountingFive Service:** {service}")
            lines.append("")
    else:
        lines.append("*(No recommendations generated)*")
        lines.append("")

    brief = data.get("intelligence_brief", {})
    if brief:
        lines.append("## Digital Intelligence")
        lines.append("*Source: Digital Intelligence Brief (Agent F — external research)*")
        lines.append("")

        firm_name_det = brief.get("firm_name_detected", "")
        firm_city_det = brief.get("firm_city", "")
        if firm_name_det:
            lines.append(f"**Firm Name (detected):** {firm_name_det}")
        if firm_city_det:
            lines.append(f"**Primary City:** {firm_city_det}")
        lines.append("")

        personnel = brief.get("personnel", [])
        if personnel:
            lines.append("### Key Personnel")
            lines.append("")
            lines.append("| Name | Title | Credentials | Footprint | Niche Signals |")
            lines.append("|------|-------|-------------|-----------|---------------|")
            for p in personnel:
                creds  = ", ".join(p.get("credentials", [])) or "—"
                niches = ", ".join(p.get("niche_signals", [])) or "—"
                lines.append(f"| {p.get('name','')} | {p.get('title','')} "
                             f"| {creds} | {p.get('footprint_strength','').title()} | {niches} |")
            lines.append("")
            for p in personnel:
                if p.get("summary"):
                    lines.append(f"**{p.get('name','')}:** {p['summary']}")
                    lines.append("")

        rep = brief.get("reputation_signals", {})
        if rep:
            lines.append("### Reputation Signals")
            lines.append("")
            lines.append(f"**Overall Sentiment:** {rep.get('overall_sentiment','not found').title()}")
            if rep.get("google_business_rating"):
                lines.append(f"**Google Rating:** ★ {rep['google_business_rating']}" +
                             (f" ({rep['google_review_count']} reviews)" if rep.get("google_review_count") else ""))
            if rep.get("yelp_rating"):
                lines.append(f"**Yelp Rating:** ★ {rep['yelp_rating']}")
            if rep.get("bbb_rating"):
                lines.append(f"**BBB Rating:** {rep['bbb_rating']}")
            if rep.get("praise_themes"):
                lines.append(f"**Praise Themes:** {', '.join(rep['praise_themes'])}")
            if rep.get("concern_themes"):
                lines.append(f"**Concern Themes:** {', '.join(rep['concern_themes'])}")
            lines.append("")

        assoc = brief.get("associations", [])
        if assoc:
            lines.append("### Associations & Affiliations")
            lines.append("")
            for a in assoc:
                lines.append(f"- **{a.get('name','')}** — {a.get('evidence','')}")
            lines.append("")

        cf = brief.get("content_footprint", [])
        if cf:
            lines.append("### Content Footprint")
            lines.append("")
            lines.append("| Type | Title | Source | Niche |")
            lines.append("|------|-------|--------|-------|")
            for item in cf:
                lines.append(f"| {item.get('type','').title()} | {item.get('title','')} "
                             f"| {item.get('source','')} | {item.get('niche_relevance','')} |")
            lines.append("")

        soc = brief.get("social_accounts", [])
        if soc:
            lines.append("### Social Accounts")
            lines.append("")
            for acc in soc:
                followers = f" · {acc['followers_approx']} followers" if acc.get("followers_approx") else ""
                lines.append(f"- **{acc.get('platform','')}**: "
                             f"{acc.get('activity_level','').title()}{followers}"
                             + (f" — {acc.get('url','')}" if acc.get("url") else ""))
            lines.append("")

        press = brief.get("press_mentions", [])
        if press:
            lines.append("### Press & Media Mentions")
            lines.append("")
            for item in press:
                lines.append(f"- {item}")
            lines.append("")

        gap     = brief.get("niche_gap_analysis", {})
        ext     = gap.get("external_niches_found", [])
        web     = gap.get("website_niches", [])
        unlev   = gap.get("unleveraged_credibility", [])
        gap_sum = gap.get("gap_summary", "")
        if ext or unlev or gap_sum:
            lines.append("### External vs. Website Niche Gap")
            lines.append("")
            if ext:
                lines.append(f"**Externally Detected Niches:** {', '.join(ext)}")
            if web:
                lines.append(f"**Website Niches (from audit):** {', '.join(web)}")
            if unlev:
                lines.append("")
                lines.append("**Unleveraged Credibility:**")
                for u in unlev:
                    lines.append(f"- {u}")
            if gap_sum:
                lines.append("")
                lines.append(f"> **Gap Summary:** {gap_sum}")
            lines.append("")

    lines.append("## Pipeline Tracker")
    lines.append("*Update as the prospect moves through the pipeline.*")
    lines.append("")
    lines.append("| Stage | Status | Notes |")
    lines.append("|-------|--------|-------|")
    lines.append("| Audit Delivered | ✅ Complete | |")
    lines.append("| Prospect Conversation | ⬜ Pending | |")
    lines.append("| Proposal Sent | ⬜ Pending | |")
    lines.append("| Client Onboarded | ⬜ Pending | |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Master Firm Profile generated by {firm.get('name','')} — {firm.get('tagline','')}*  ")
    lines.append(f"*Audit date: {audit_date} | Source audit: audit-{domain}-{audit_date}.html*")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"✅ Master Firm Profile generated: {output_path}")


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate CountingFive Site Audit Report")
    parser.add_argument("--data",        required=True,  help="Path to audit_results.json")
    parser.add_argument("--config",      required=True,  help="Path to config.json")
    parser.add_argument("--output-html", required=True,  help="Output HTML path")
    parser.add_argument("--output-md",   required=True,  help="Output Markdown path")
    parser.add_argument("--output-mfp",  required=False, default=None,
                        help="Output Master Firm Profile .md path (optional)")
    args = parser.parse_args()

    with open(args.data) as f:
        data = json.load(f)
    with open(args.config) as f:
        config = json.load(f)

    # Resolve logo paths relative to config location
    config_dir    = os.path.dirname(os.path.abspath(args.config))
    logo_rel      = config.get("firm", {}).get("logo_path", "")
    logo_path     = os.path.join(config_dir, logo_rel) if logo_rel else ""
    logo_rev_rel  = config.get("firm", {}).get("logo_path_reversed", "")
    logo_path_rev = os.path.join(config_dir, logo_rev_rel) if logo_rev_rel else ""

    build_html(data, config, args.output_html, logo_path, logo_path_rev)
    build_markdown(data, config, args.output_md)

    if args.output_mfp:
        build_mfp(data, config, args.output_mfp)


if __name__ == "__main__":
    main()
