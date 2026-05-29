# -*- coding: utf-8 -*-
"""Build the full seller-facing BOV site for 613 Westbourne Dr, West Hollywood.
Institutional/advisory listing proposal for Ian Lee & family. Full standard BOV: track record ->
marketing -> property -> location -> market -> buyer profile -> sale comps ->
rent comps -> rent roll -> operating statement -> financial summary ->
price reveal ($2,150,000) + pricing matrix + trade range.
All financials from Glen's pricing model. All maps via Google Maps JS API."""
import json
from collections import Counter
from statistics import mean, median

md = json.load(open(r"C:\Users\gscher\Downloads\map_data.json", encoding="utf-8"))
SUBJ = md["subject"]
MARKERS = md["markers"]
MAPS_KEY = "AIzaSyB1FbBfb4q0FVpiMSHBhjERp_R2lP3wDE8"

# ---------------------------------------------------------------------------
# SUBJECT FINANCIALS (source: 613 Westbourne Model.pdf - Glen's pricing model)
# ---------------------------------------------------------------------------
LIST = 2_150_000
UNITS = 8
SF = 7442
YEAR = 1949

GSR_CUR, GSR_PF = 181_020, 197_388
VAC_CUR, VAC_PF = 5_431, 5_922          # 3% vacancy
EGI_CUR, EGI_PF = 175_589, 191_466

# (label, current, pro_forma, note_number)
EXPENSES = [
    ("Real Estate Taxes",  26_875, 26_875, 1),
    ("Insurance",           9_042,  9_042, 2),
    ("Utilities",           9_000,  9_000, 3),
    ("Repairs & Maintenance", 6_000, 6_000, 4),
    ("Contract Services",   4_800,  4_800, 5),
    ("General & Admin",     1_600,  1_600, 6),
    ("Operating Reserves",  2_000,  2_000, 7),
    ("Management Fee (5%)", 8_779,  9_573, 8),
]
EXP_CUR = sum(e[1] for e in EXPENSES)   # 68,096
EXP_PF  = sum(e[2] for e in EXPENSES)   # 68,890
NOI_CUR, NOI_PF = EGI_CUR - EXP_CUR, EGI_PF - EXP_PF   # 107,493 / 122,576

# Financing
LOAN = 1_182_500            # 55% LTV
RATE = 0.06
AMORT = 30
DOWN = LIST - LOAN          # 967,500 (45%)
DS = 85_076                 # annual debt service (model)
CONSTANT = DS / LOAN        # 0.071945
PRIN_CUR, PRIN_PF = 14_521, 15_417

# Rent roll: (unit, type, sf, current, pro_forma)
RENT_ROLL = [
    ("1", "2BR / 2BA", 950, 2_400, 2_729),
    ("2", "1BR / 1BA", 800, 1_995, 1_995),
    ("3", "1BR / 1BA", 800, 1_000, 1_066),
    ("4", "2BR / 2BA", 950, 1_650, 2_066),
    ("5", "2BR / 2BA", 950, 1_850, 2_238),
    ("6", "1BR / 1BA", 800, 1_400, 1_371),
    ("7", "1BR / 1BA", 800, 1_995, 2_040),
    ("8", "2BR / 2BA", 950, 2_795, 2_944),
]

# Rentometer market survey (0.5 mi radius) - 02_Extracted_Data evidence 2026-05-28
RENTO = {
    "1BR": {"n": 44, "median": 2974, "mean": 3002, "p25": 2448, "p75": 3555},
    "2BR": {"n": 42, "median": 3875, "mean": 4079, "p25": 3443, "p75": 4714},
}
MKT_1BR, MKT_2BR = 1_618, 2_494   # model pro-forma market rents

# ---------------------------------------------------------------------------
# SALE COMPS (source: Agent-Detail-Full (39).pdf - Glen-pulled TheMLS)
# ---------------------------------------------------------------------------
# addr, units, built, sf, closed, price, ppu, psf, cap(None), grm, lat, lng
COMPS = [
    ("1027 N Ogden Dr",    10, 1963,  9303, "Mar 2026", 2_038_234, 203_823, 219.09, 5.22, 11.83, 34.089201, -118.359554),
    ("525 N Sweetzer Ave",  6, 1959,  6120, "Jan 2026", 1_950_000, 325_000, 318.63, 5.39, 12.12, 34.080835, -118.370363),
    ("948 Palm Ave",        8, 1909,  4904, "Jan 2026", 2_400_000, 300_000, 489.40, None, 13.01, 34.088951, -118.382805),
    ("1036 N Genesee Ave", 10, 1960,  8190, "Apr 2026", 2_850_000, 285_000, 347.99, 5.65, 12.26, 34.089349, -118.358363),
    ("1425 N Hayworth Ave",11, 1951, 10235, "May 2026", 2_820_000, 256_364, 275.53, 5.16, 12.48, 34.096130, -118.363066),
    ("1241 N Fairfax Ave", 14, 1958, 10378, "Apr 2026", 3_076_000, 219_714, 296.40, None, 12.13, 34.092912, -118.361588),
]
COMP_NARR = [
    ("1027 N Ogden Dr", "A 10-unit 1963 building that closed March 2026 at $2,038,234, or $203,823 per unit and $219/SF on a 5.22% cap and 11.83 GRM. It is the lowest per-unit and per-foot data point in the set, reflecting a larger, less-renovated asset further east. The subject's smaller unit count and prime Westbourne location support pricing above Ogden's per-unit basis."),
    ("525 N Sweetzer Ave", "The closest match in size: 6 units, built 1959, closed January 2026 at $1,950,000, or $325,000 per unit and $319/SF on a 5.39% cap and 12.12 GRM. With a Walk Score of 93 it sets the high end on a per-unit basis. The subject's $268,750 per unit sits comfortably below Sweetzer despite a comparable location, underscoring achievable upside."),
    ("948 Palm Ave", "An 8-unit building in the Norma Triangle that closed January 2026 at $2,400,000, or $300,000 per unit and a 13.01 GRM. Built in 1909 on a tight 4,904 SF footprint, its high $489/SF reflects small units and land value. It matches the subject's unit count exactly and trades at $300,000 per unit, well above the subject's suggested $268,750."),
    ("1036 N Genesee Ave", "A fully RSO 10-unit that closed April 2026 at $2,850,000, or $285,000 per unit and $348/SF on a 5.65% cap and 12.26 GRM, seismic retrofit complete. It sits on the same block as our own January 2025 closing at 1046 N Genesee. A strong, recent, professionally marketed Westside trade that brackets the subject above on per-unit pricing."),
    ("1425 N Hayworth Ave", "An 11-unit, separately metered 1951 building with on-site laundry, closed May 2026 at $2,820,000, or $256,364 per unit and $276/SF on a 5.16% cap and 12.48 GRM. The most recent sale in the set and a close fundamental comp; its per-unit figure and sub-5.2% cap closely frame the subject's pricing on the most current data available."),
    ("1241 N Fairfax Ave", "A 14-unit all-2BR/2BA RSO building that closed April 2026 at $3,076,000, or $219,714 per unit and $296/SF on a 12.13 GRM. Its lower per-unit figure reflects scale and a 263-day marketing period. The subject's smaller, mixed-unit profile in a quieter prime-residential pocket supports a higher per-unit basis than Fairfax's larger-building discount."),
]

# Subject metrics at list
SUB_PPU = LIST / UNITS
SUB_PSF = LIST / SF
SUB_CAP = NOI_CUR / LIST * 100
SUB_GRM = LIST / GSR_CUR

# Comp summary stats
caps = [c[8] for c in COMPS if c[8] is not None]
grms = [c[9] for c in COMPS]
ppus = [c[6] for c in COMPS]
psfs = [c[7] for c in COMPS]

# ---------------------------------------------------------------------------
# PRICING MATRIX
# ---------------------------------------------------------------------------
TRADE_LOW, TRADE_HIGH = 2_000_000, 2_200_000
gap = LIST - TRADE_LOW                       # 150,000
INCREMENT = 50_000                            # in [gap/4=37.5K, gap/3=50K]; clean & bottom row 2 inc below trade low
TOP = LIST + 5 * INCREMENT                     # 2,400,000
BOTTOM = LIST - 5 * INCREMENT                  # 1,900,000
MATRIX_PRICES = list(range(TOP, BOTTOM - 1, -INCREMENT))   # 11 rows

def calc_metrics(p):
    loan = 0.55 * p
    down = 0.45 * p
    ds = loan * CONSTANT
    return {
        "price": p,
        "cur_cap": NOI_CUR / p * 100,
        "pf_cap": NOI_PF / p * 100,
        "coc": (NOI_CUR - ds) / down * 100,
        "psf": p / SF,
        "ppu": p / UNITS,
        "pf_grm": p / GSR_PF,
    }

# ===========================================================================
# BUILD GENERATED HTML FRAGMENTS
# ===========================================================================
def usd(n):  return f"${n:,.0f}"

# ---- Rent roll rows ----
rr = ""
for u, t, sf, cur, pf in RENT_ROLL:
    rr += (f"<tr><td>{u}</td><td>{t}</td><td>{sf:,}</td>"
           f"<td>{usd(cur)}</td><td>${cur/sf:.2f}</td>"
           f"<td>{usd(pf)}</td><td>${pf/sf:.2f}</td></tr>\n")
tot_cur = sum(r[3] for r in RENT_ROLL); tot_pf = sum(r[4] for r in RENT_ROLL)
rr += (f'<tr class="totrow"><td colspan="2"><strong>Totals / Mo.</strong></td>'
       f'<td><strong>{SF:,}</strong></td>'
       f'<td><strong>{usd(tot_cur)}</strong></td><td></td>'
       f'<td><strong>{usd(tot_pf)}</strong></td><td></td></tr>')

# ---- Operating statement (Current, 5 cols) ----
def os_row(label, val, ref="", summary=False, neg=False):
    cls = ' class="totrow"' if summary else ""
    pu = f"${val/UNITS:,.0f}"; ps = f"${val/SF:.2f}"; pe = f"{val/EGI_CUR*100:.1f}%"
    disp = f"(${abs(val):,.0f})" if neg else f"${val:,.0f}"
    return (f"<tr{cls}><td>{label}{ref}</td><td>{disp}</td>"
            f"<td>{pu}</td><td>{ps}</td><td>{pe}</td></tr>\n")

os_income = ""
os_income += os_row("Gross Scheduled Rent", GSR_CUR)
os_income += os_row("Less: Vacancy (3%)", -VAC_CUR, neg=True)
os_income += os_row("Effective Gross Income", EGI_CUR, summary=True)

os_exp = ""
for label, cur, pf, n in EXPENSES:
    os_exp += os_row(label, cur, ref=f' <sup class="nr">[{n}]</sup>')
os_exp += os_row("Total Operating Expenses", EXP_CUR, summary=True)
os_exp += os_row("Net Operating Income", NOI_CUR, summary=True)

OS_NOTES = [
    "Reassessed at the suggested list price under Prop 13 (approx. 1.25% of value). A new buyer should budget to this reassessed basis, not the seller's lower legacy assessment.",
    "(Units x $200) plus building square footage at $1.00/SF, the LAAA benchmark for a building of this vintage and size.",
    "Owner-paid common-area utilities (water, sewer, trash, common electric). Units are individually metered for in-unit gas and electric.",
    "Routine repairs, turnover, and ongoing maintenance for an 8-unit building of this age in West Hollywood.",
    "On-site services including landscaping, pest control, and periodic vendor work.",
    "Licenses, the West Hollywood rental registration, bookkeeping, and miscellaneous administrative costs.",
    "A prudent capital reserve carried at the property level for components and deferred items.",
    "Professional management at 5% of collected income, in line with full-service management for a building of this size.",
]
os_notes_html = "".join(
    f'<p><strong>[{i+1}] {EXPENSES[i][0]}:</strong> {t}</p>'
    for i, t in enumerate(OS_NOTES)
)

# ---- Sale comp table ----
sc = ""
for i, c in enumerate(COMPS, 1):
    addr, un, blt, sf, cl, pr, ppu, psf, cap, grm = c[:10]
    capd = f"{cap:.2f}%" if cap is not None else "&ndash;"
    sc += (f"<tr><td>{i}</td><td>{addr}</td><td>{un}</td><td>{blt}</td>"
           f"<td>{sf:,}</td><td>{cl}</td><td>{usd(pr)}</td>"
           f"<td>{usd(ppu)}</td><td>${psf:.0f}</td><td>{capd}</td><td>{grm:.2f}</td></tr>\n")
# subject highlight
sc += (f'<tr class="hl"><td>&#9733;</td><td>613 Westbourne Dr (Subject)</td><td>{UNITS}</td>'
       f'<td>{YEAR}</td><td>{SF:,}</td><td>List</td><td>{usd(LIST)}</td>'
       f'<td>{usd(SUB_PPU)}</td><td>${SUB_PSF:.0f}</td><td>{SUB_CAP:.2f}%</td><td>{SUB_GRM:.2f}</td></tr>\n')
# average / median summary rows
sc += (f'<tr class="totrow"><td colspan="6">Comp Average</td>'
       f'<td>{usd(mean([c[5] for c in COMPS]))}</td><td>{usd(mean(ppus))}</td>'
       f'<td>${mean(psfs):.0f}</td><td>{mean(caps):.2f}%</td><td>{mean(grms):.2f}</td></tr>\n')
sc += (f'<tr class="totrow"><td colspan="6">Comp Median</td>'
       f'<td>{usd(median([c[5] for c in COMPS]))}</td><td>{usd(median(ppus))}</td>'
       f'<td>${median(psfs):.0f}</td><td>{median(caps):.2f}%</td><td>{median(grms):.2f}</td></tr>\n')

sc_narr = "".join(
    f'<p class="narr"><strong>{i+1}. {a}</strong> &nbsp;{txt}</p>'
    for i, (a, txt) in enumerate(COMP_NARR)
)

COMPS_JSON = json.dumps([
    {"a": c[0], "u": c[1], "y": c[4], "p": f"{c[5]:,}", "lat": c[10], "lng": c[11]}
    for c in COMPS
])

# ---- Rent comps table ----
def rc_row(name, mkt, d):
    return (f"<tr><td>{name}</td><td>{usd(mkt)}</td><td>{usd(d['p25'])} &ndash; {usd(d['p75'])}</td>"
            f"<td>{usd(d['median'])}</td><td>{usd(d['mean'])}</td><td>{d['n']}</td></tr>\n")
rent_comp_rows = rc_row("1 Bed / 1 Bath", MKT_1BR, RENTO["1BR"]) + rc_row("2 Bed / 2 Bath", MKT_2BR, RENTO["2BR"])

# ---- Pricing matrix ----
matrix = ""
for p in MATRIX_PRICES:
    m = calc_metrics(p)
    cls = ' class="hl"' if p == LIST else ""
    matrix += (f'<tr{cls}><td>{usd(m["price"])}</td><td>{m["cur_cap"]:.2f}%</td>'
               f'<td>{m["pf_cap"]:.2f}%</td><td>{m["coc"]:.2f}%</td>'
               f'<td>${m["psf"]:.0f}</td><td>{usd(m["ppu"])}</td><td>{m["pf_grm"]:.2f}x</td></tr>\n')

# ---- Financial summary two columns ----
def two(cur, pf, money=True, suf=""):
    f = (lambda v: usd(v)) if money else (lambda v: f"{v}{suf}")
    return f"<td>{f(cur)}</td><td>{f(pf)}</td>"

coc_cur = (NOI_CUR - DS) / DOWN * 100
coc_pf = (NOI_PF - DS) / DOWN * 100
tr_cur = (NOI_CUR - DS + PRIN_CUR) / DOWN * 100
tr_pf = (NOI_PF - DS + PRIN_PF) / DOWN * 100

summary_left = f"""
<table class="sm"><thead><tr><th colspan="2">Operating Data</th></tr></thead><tbody>
<tr><td>Suggested List Price</td><td>{usd(LIST)}</td></tr>
<tr><td>Down Payment (45%)</td><td>{usd(DOWN)}</td></tr>
<tr><td>Number of Units</td><td>{UNITS}</td></tr>
<tr><td>Price / Unit</td><td>{usd(SUB_PPU)}</td></tr>
<tr><td>Price / SF</td><td>${SUB_PSF:.0f}</td></tr>
<tr><td>Gross Building SF</td><td>{SF:,}</td></tr>
<tr><td>Year Built</td><td>{YEAR}</td></tr>
</tbody></table>
<table class="sm"><thead><tr><th>Returns</th><th>Current</th><th>Pro Forma</th></tr></thead><tbody>
<tr><td>Cap Rate</td>{two(f"{SUB_CAP:.2f}",f"{NOI_PF/LIST*100:.2f}",money=False,suf="%")}</tr>
<tr><td>GRM</td>{two(f"{SUB_GRM:.2f}",f"{LIST/GSR_PF:.2f}",money=False,suf="x")}</tr>
<tr><td>Cash-on-Cash</td>{two(f"{coc_cur:.2f}",f"{coc_pf:.2f}",money=False,suf="%")}</tr>
<tr><td>DCR</td>{two(f"{NOI_CUR/DS:.2f}",f"{NOI_PF/DS:.2f}",money=False)}</tr>
</tbody></table>
<table class="sm"><thead><tr><th colspan="2">Financing</th></tr></thead><tbody>
<tr><td>Loan Amount</td><td>{usd(LOAN)}</td></tr>
<tr><td>Loan Type</td><td>Fixed, Amortizing</td></tr>
<tr><td>Interest Rate</td><td>{RATE*100:.2f}%</td></tr>
<tr><td>Amortization</td><td>{AMORT} years</td></tr>
<tr><td>Loan Constant</td><td>{CONSTANT*100:.2f}%</td></tr>
<tr><td>Loan-to-Value</td><td>55%</td></tr>
</tbody></table>
"""

summary_right = f"""
<table class="sm"><thead><tr><th>Income</th><th>Current</th><th>Pro Forma</th></tr></thead><tbody>
<tr><td>Gross Scheduled Rent</td>{two(GSR_CUR,GSR_PF)}</tr>
<tr><td>Less: Vacancy (3%)</td>{two(-VAC_CUR,-VAC_PF)}</tr>
<tr class="totrow"><td>Effective Gross Income</td>{two(EGI_CUR,EGI_PF)}</tr>
</tbody></table>
<table class="sm"><thead><tr><th>Cash Flow</th><th>Current</th><th>Pro Forma</th></tr></thead><tbody>
<tr><td>Net Operating Income</td>{two(NOI_CUR,NOI_PF)}</tr>
<tr><td>Debt Service</td>{two(-DS,-DS)}</tr>
<tr><td>Net Cash Flow</td>{two(NOI_CUR-DS,NOI_PF-DS)}</tr>
<tr><td>Principal Reduction (Yr 1)</td>{two(PRIN_CUR,PRIN_PF)}</tr>
<tr class="totrow"><td>Total Return</td>{two(f"{tr_cur:.2f}",f"{tr_pf:.2f}",money=False,suf="%")}</tr>
</tbody></table>
<table class="sm"><thead><tr><th>Expenses</th><th>Current</th><th>Pro Forma</th></tr></thead><tbody>
"""
for label, cur, pf, n in EXPENSES:
    summary_right += f"<tr><td>{label}</td>{two(cur,pf)}</tr>\n"
summary_right += (f'<tr class="totrow"><td>Total Expenses</td>{two(EXP_CUR,EXP_PF)}</tr>\n'
                  f'<tr><td>Expense Ratio (% EGI)</td>'
                  f'<td>{EXP_CUR/EGI_CUR*100:.1f}%</td><td>{EXP_PF/EGI_PF*100:.1f}%</td></tr>\n'
                  f'</tbody></table>')

# ---- Resume card counts (from markers) ----
NAVY = "#1B3A5C"; GOLD = "#C5A258"
cnt = Counter(m["city"] for m in MARKERS); un = Counter()
for m in MARKERS: un[m["city"]] += (m.get("u") or 0)
weho_b, weho_u = cnt["West Hollywood"], un["West Hollywood"]
corr_b, corr_u = cnt["WeHo Corridor (Fairfax/Melrose)"], un["WeHo Corridor (Fairfax/Melrose)"]
bh_b, bh_u = cnt["Beverly Hills"], un["Beverly Hills"]
sm_b, sm_u = cnt["Santa Monica"], un["Santa Monica"]
wla_b, wla_u = cnt["Westwood / Brentwood / West LA"], un["Westwood / Brentwood / West LA"]
al_b = weho_b + corr_b + bh_b + sm_b
al_u = weho_u + corr_u + bh_u + sm_u
# Combined prime-Westside total across all five submarkets (lead with this, not the WeHo breakout)
prime_b = weho_b + corr_b + bh_b + sm_b + wla_b
prime_u = weho_u + corr_u + bh_u + sm_u + wla_u

# ===========================================================================
# HTML
# ===========================================================================
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>613 Westbourne Drive | Broker Opinion of Value | LAAA Team</title>
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Broker Opinion of Value and marketing proposal for 613 Westbourne Drive, West Hollywood. Prepared by the LAAA Team at Marcus &amp; Millichap.">
<meta property="og:type" content="website">
<meta property="og:title" content="613 Westbourne Drive | Broker Opinion of Value">
<meta property="og:description" content="Confidential Broker Opinion of Value and marketing proposal. The LAAA Team at Marcus &amp; Millichap.">
<meta property="og:image" content="https://613-westbourne.laaa.com/preview.png">
<meta property="og:url" content="https://613-westbourne.laaa.com/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="613 Westbourne Drive | Broker Opinion of Value">
<meta name="twitter:description" content="Confidential Broker Opinion of Value and marketing proposal. The LAAA Team at Marcus &amp; Millichap.">
<meta name="twitter:image" content="https://613-westbourne.laaa.com/preview.png">
<link rel="icon" href="images/logo-blue.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap" rel="stylesheet">
<style>
  :root{ --navy:#1B3A5C; --gold:#C5A258; --ink:#1a1a1a; --gray:#5b6470; --line:#e4e7ec; --bg:#f7f8fa; --serif:'DM Serif Display',Georgia,serif; }
  *{ box-sizing:border-box; margin:0; padding:0; }
  html{ scroll-behavior:smooth; }
  body{ font-family:'Inter',-apple-system,sans-serif; color:var(--ink); line-height:1.65; background:#fff; -webkit-font-smoothing:antialiased; }
  h1,h2,h3,h4{ font-family:var(--serif); line-height:1.18; font-weight:400; color:var(--navy); letter-spacing:.005em; }
  a{ color:var(--gold); }
  .wrap{ max-width:1100px; margin:0 auto; padding:0 28px; }
  .eyebrow{ text-transform:uppercase; letter-spacing:.16em; font-size:12px; font-weight:700; color:var(--gold); margin-bottom:14px; }
  section{ padding:76px 0; border-bottom:1px solid var(--line); }
  section.alt{ background:var(--bg); }
  p.lead{ font-size:19px; color:#33404f; }
  p{ margin-bottom:15px; color:#33404f; }

  /* NAV */
  nav{ position:sticky; top:0; z-index:50; background:rgba(27,58,92,.97); backdrop-filter:blur(8px); transition:transform .3s; }
  nav .wrap{ display:flex; align-items:center; justify-content:space-between; height:60px; }
  nav img{ height:30px; }
  nav .links{ display:flex; gap:17px; }
  nav .links a{ color:#cdd7e3; text-decoration:none; font-size:13px; font-weight:500; letter-spacing:.02em; }
  nav .links a:hover{ color:#fff; }
  @media(max-width:980px){ nav .links{ display:none; } }

  /* COVER */
  .cover{ background:linear-gradient(160deg,#15314f 0%,#1B3A5C 55%,#24496f 100%); color:#fff; padding:0; border:none; }
  .cover .wrap{ padding-top:70px; padding-bottom:0; }
  .cover .logo{ height:54px; margin-bottom:48px; }
  .cover .label{ display:inline-block; border:1px solid rgba(197,162,88,.6); color:var(--gold); text-transform:uppercase; letter-spacing:.18em; font-size:11px; font-weight:700; padding:7px 16px; border-radius:3px; margin-bottom:26px; }
  .cover h1{ color:#fff; font-size:56px; font-weight:400; letter-spacing:.01em; text-shadow:0 2px 12px rgba(0,0,0,.3); }
  .cover .sub{ font-size:21px; color:#bccbdc; font-weight:400; margin-top:10px; }
  .cover .meta{ margin-top:34px; display:flex; gap:40px; flex-wrap:wrap; padding-bottom:46px; }
  .cover .meta div span{ display:block; font-size:11px; text-transform:uppercase; letter-spacing:.12em; color:#8fa6c0; margin-bottom:4px; }
  .cover .meta div strong{ font-size:17px; font-weight:600; color:#fff; }
  .cover .heroimg{ width:100%; height:340px; object-fit:cover; object-position:center 35%; display:block; }
  @media(max-width:880px){ .cover h1{ font-size:40px; } .cover .heroimg{ height:220px; } }
  .prepared{ background:var(--gold); color:#3a2f12; text-align:center; padding:13px; font-size:13px; font-weight:600; letter-spacing:.04em; }

  /* STAT BAND */
  .stats{ display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--line); border:1px solid var(--line); border-radius:10px; overflow:hidden; }
  .stats .s{ background:#fff; padding:26px 18px; text-align:center; }
  .stats .s .n{ font-family:var(--serif); font-size:38px; font-weight:400; color:var(--navy); letter-spacing:.005em; }
  .stats .s .l{ font-size:12px; color:var(--gray); margin-top:6px; line-height:1.4; }
  .stats.dark .s{ background:var(--navy); }
  .stats.dark .s .n{ color:#fff; }
  .stats.dark .s .l{ color:#9fb3c9; }
  @media(max-width:780px){ .stats{ grid-template-columns:repeat(2,1fr); } }

  /* TEAM */
  .team{ display:grid; grid-template-columns:1fr 1fr; gap:30px; }
  .advisor{ display:flex; gap:20px; align-items:flex-start; background:#fff; border:1px solid var(--line); border-radius:12px; padding:24px; }
  .advisor img{ width:96px; height:96px; border-radius:50%; object-fit:cover; flex-shrink:0; border:3px solid var(--gold); }
  .advisor h3{ font-size:20px; }
  .advisor .ttl{ color:var(--gold); font-weight:600; font-size:13px; margin:2px 0 8px; }
  .advisor .lic{ font-size:12px; color:var(--gray); }
  .advisor .ct{ font-size:13px; margin-top:8px; color:#33404f; }
  @media(max-width:780px){ .team{ grid-template-columns:1fr; } }

  /* RESUME CARDS */
  .resume-cards{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:8px; }
  .rc{ background:#fff; border:1px solid var(--line); border-top:3px solid var(--gold); border-radius:10px; padding:22px; }
  .rc .city{ font-size:15px; font-weight:700; color:var(--navy); }
  .rc .big{ font-family:var(--serif); font-size:34px; font-weight:400; color:var(--navy); margin-top:10px; }
  .rc .det{ font-size:13px; color:var(--gray); margin-top:4px; }
  @media(max-width:780px){ .resume-cards{ grid-template-columns:1fr 1fr; } }

  /* MAP */
  .map{ width:100%; height:480px; border-radius:12px; border:1px solid var(--line); margin-top:18px; background:#eef1f4; }
  .map-controls{ display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; }
  .map-controls button{ font-family:inherit; font-size:13px; font-weight:600; padding:8px 16px; border:1px solid var(--navy); background:#fff; color:var(--navy); border-radius:30px; cursor:pointer; transition:all .15s; }
  .map-controls button.active,.map-controls button:hover{ background:var(--navy); color:#fff; }
  .maptip{ font-size:12px; color:var(--gray); margin-top:10px; }

  /* TABLE */
  .table-scroll{ overflow-x:auto; -webkit-overflow-scrolling:touch; }
  .table-scroll table{ min-width:680px; }
  table{ width:100%; border-collapse:collapse; margin-top:18px; font-size:14px; }
  th{ background:var(--navy); color:#fff; text-align:left; padding:11px 14px; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:.04em; }
  td{ padding:11px 14px; border-bottom:1px solid var(--line); color:#33404f; }
  tr:nth-child(even) td{ background:#fafbfc; }
  .hl td{ background:#fdf8ee !important; font-weight:700; }
  tr.totrow td{ background:var(--navy) !important; color:#fff; font-weight:600; border-bottom:1px solid var(--navy); }
  tr.totrow td strong{ color:#fff; }
  table.fin td+td, table.fin th+th{ text-align:right; }
  sup.nr{ color:var(--gold); font-weight:700; font-size:10px; }

  /* OPERATING STATEMENT */
  .os{ display:grid; grid-template-columns:1.5fr 1fr; gap:30px; align-items:start; margin-top:8px; }
  .os .notes{ background:#f8f9fb; border:1px solid var(--line); border-radius:10px; padding:22px; font-size:12.5px; color:#33404f; }
  .os .notes h3{ font-size:15px; margin-bottom:12px; }
  .os .notes p{ margin-bottom:10px; font-size:12.5px; line-height:1.5; }
  @media(max-width:880px){ .os{ grid-template-columns:1fr; } }

  /* FINANCIAL SUMMARY */
  .sm-cols{ display:grid; grid-template-columns:1fr 1fr; gap:26px; align-items:start; margin-top:8px; }
  table.sm{ font-size:12.5px; margin-top:14px; }
  table.sm th{ font-size:11px; padding:8px 10px; }
  table.sm td{ padding:7px 10px; }
  table.sm td+td{ text-align:right; }
  @media(max-width:780px){ .sm-cols{ grid-template-columns:1fr; } }

  /* PRICE REVEAL */
  .pricewrap{ text-align:center; margin-bottom:30px; }
  .pricewrap .lbl{ font-size:13px; text-transform:uppercase; letter-spacing:.18em; color:var(--gold); font-weight:700; margin-bottom:10px; }
  .bigprice{ font-family:var(--serif); font-size:64px; font-weight:400; color:var(--navy); line-height:1; letter-spacing:.01em; }
  .trade{ text-align:center; background:linear-gradient(135deg,#1B3A5C,#24496f); color:#fff; border-radius:14px; padding:28px; margin-top:26px; }
  .trade .lbl{ color:var(--gold); letter-spacing:.12em; font-size:12px; text-transform:uppercase; font-weight:700; }
  .trade .px{ font-family:var(--serif); font-size:34px; font-weight:400; color:#fff; margin-top:10px; }

  .narr{ font-size:14px; max-width:900px; margin-top:14px; color:#33404f; }

  /* CALLOUT */
  .callout{ background:linear-gradient(135deg,#1B3A5C,#24496f); color:#fff; border-radius:14px; padding:34px 38px; margin-top:24px; }
  .callout .eyebrow{ color:var(--gold); }
  .callout h3{ color:#fff; font-size:24px; }
  .callout p{ color:#cfdcea; margin-top:8px; margin-bottom:0; }

  /* GRID FEATURES */
  .feat{ display:grid; grid-template-columns:1fr 1fr; gap:22px; margin-top:10px; }
  .feat .f{ background:#fff; border:1px solid var(--line); border-radius:10px; padding:22px; }
  .feat .f h4{ font-size:16px; display:flex; align-items:center; gap:10px; }
  .feat .f .ico{ width:34px; height:34px; border-radius:8px; background:#fdf3df; color:var(--gold); display:grid; place-items:center; font-weight:800; flex-shrink:0; }
  .feat .f p{ font-size:14px; margin:10px 0 0; }
  @media(max-width:780px){ .feat{ grid-template-columns:1fr; } }

  ul.clean{ list-style:none; margin-top:8px; }
  ul.clean li{ padding-left:26px; position:relative; margin-bottom:11px; color:#33404f; }
  ul.clean li:before{ content:"\2713"; position:absolute; left:0; top:0; color:var(--gold); font-weight:800; }

  .twocol{ display:grid; grid-template-columns:1.3fr 1fr; gap:40px; align-items:start; }
  @media(max-width:880px){ .twocol{ grid-template-columns:1fr; } }
  .demo{ background:#fff; border:1px solid var(--line); border-radius:12px; overflow:hidden; }
  .demo .row{ display:flex; justify-content:space-between; padding:13px 18px; border-bottom:1px solid var(--line); font-size:14px; }
  .demo .row:last-child{ border-bottom:none; }
  .demo .row span{ color:var(--gray); }
  .demo .row strong{ color:var(--navy); font-weight:700; }
  .demo .hd{ background:var(--navy); color:#fff; padding:13px 18px; font-weight:700; font-size:14px; }

  /* FOOTER */
  footer{ background:var(--navy); color:#cdd7e3; padding:60px 0 40px; border:none; }
  footer .logo{ height:40px; margin-bottom:30px; }
  footer .fteam{ display:grid; grid-template-columns:1fr 1fr; gap:30px; margin-bottom:36px; }
  footer h4{ color:#fff; font-size:18px; }
  footer .ttl{ color:var(--gold); font-size:13px; font-weight:600; margin:2px 0 10px; }
  footer .ct{ font-size:14px; line-height:1.9; }
  footer .ct a{ color:#cdd7e3; text-decoration:none; }
  footer .legal{ border-top:1px solid #2c4a6b; padding-top:24px; font-size:11.5px; color:rgba(255,255,255,.35); line-height:1.7; max-width:860px; }
  @media(max-width:780px){ footer .fteam{ grid-template-columns:1fr; } }

  /* PDF DOWNLOAD BUTTON */
  .pdf-float-btn{ position:fixed; bottom:24px; right:24px; z-index:90; display:inline-flex; align-items:center; gap:9px;
    background:var(--gold); color:#3a2f12; font-family:'Inter',sans-serif; font-size:14px; font-weight:700; letter-spacing:.02em;
    text-decoration:none; padding:13px 20px; border-radius:40px; box-shadow:0 6px 20px rgba(27,58,92,.28); transition:transform .15s, box-shadow .15s; }
  .pdf-float-btn:hover{ transform:translateY(-2px); box-shadow:0 10px 26px rgba(27,58,92,.34); color:#3a2f12; }
  .pdf-float-btn svg{ width:17px; height:17px; }
  @media(max-width:560px){ .pdf-float-btn span{ display:none; } .pdf-float-btn{ padding:14px; } }

  /* PRINT / PDF */
  @media print{
    *{ -webkit-print-color-adjust:exact !important; print-color-adjust:exact !important; }
    html{ scroll-behavior:auto; }
    body{ font-size:11px; line-height:1.5; }
    nav, .pdf-float-btn, .map-controls{ display:none !important; }
    .map, #resumeMap, #subjectMap, #compMap{ display:none !important; }
    .print-map-note{ display:block !important; }
    section{ padding:26px 0; border-bottom:none; page-break-inside:avoid; }
    .cover{ page-break-after:avoid; }
    #intro, #team, #resume, #marketing, #property, #weho, #market, #buyer, #comps, #rentcomps, #financials, #pricing, #process, #exchange, #next{ page-break-before:always; }
    #intro{ page-break-before:avoid; }
    .callout, .trade, .demo, .advisor, .feat .f, .rc, .stats{ page-break-inside:avoid; }
    .table-scroll{ overflow:visible !important; }
    .table-scroll table{ min-width:0 !important; }
    table, tr, td, th{ page-break-inside:avoid; }
    h2,h3{ page-break-after:avoid; }
    a{ color:var(--navy); text-decoration:none; }
    footer{ page-break-before:always; }
    @page{ margin:14mm 12mm; }
  }
  .print-map-note{ display:none; font-size:12px; color:var(--gray); margin-top:14px; font-style:italic; }
</style>
</head>
<body>

<a class="pdf-float-btn" href="613-westbourne-bov.pdf" download aria-label="Download PDF">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
  <span>Download PDF</span>
</a>

<nav id="nav">
  <div class="wrap">
    <img src="images/logo-white.png" alt="LAAA Team">
    <div class="links">
      <a href="#team">Team</a>
      <a href="#resume">Track Record</a>
      <a href="#marketing">Marketing</a>
      <a href="#property">Property</a>
      <a href="#weho">Location</a>
      <a href="#buyer">Buyer Profile</a>
      <a href="#comps">Sale Comps</a>
      <a href="#rentcomps">Rent Comps</a>
      <a href="#financials">Financials</a>
      <a href="#pricing">Pricing</a>
      <a href="#contact">Contact</a>
    </div>
  </div>
</nav>

<!-- COVER -->
<header class="cover">
  <div class="wrap">
    <img class="logo" src="images/logo-white.png" alt="LAAA Team">
    <span class="label">Confidential Broker Opinion of Value &amp; Marketing Proposal</span>
    <h1>613 Westbourne Drive</h1>
    <div class="sub">West Hollywood, CA 90069 &nbsp;|&nbsp; 8-Unit Multifamily Investment</div>
    <div class="meta">
      <div><span>Prepared exclusively for</span><strong>Ian Lee &amp; the Lee Family</strong></div>
      <div><span>Submarket</span><strong>Prime West Hollywood</strong></div>
      <div><span>Presented by</span><strong>Glen Scher &amp; Filip Niculete</strong></div>
    </div>
  </div>
  <img class="heroimg" src="images/hero.jpg" alt="613 Westbourne Drive, West Hollywood">
</header>
<div class="prepared">An opinion of value and recommended go-to-market strategy for an 8-unit West Hollywood multifamily asset.</div>

<!-- GREETING -->
<section id="intro">
  <div class="wrap">
    <div class="eyebrow">Prepared for Ian Lee and the Lee Family</div>
    <h2 style="font-size:32px;max-width:780px">An advisory opinion of value for 613 Westbourne Drive</h2>
    <p class="lead" style="margin-top:20px;max-width:820px">Ian, thank you for the opportunity to be considered. Your stated priorities, drawn from our conversation, shape the recommendation that follows: speed to a clean close, a fully covered 1031 exchange, and senior-level execution from the broker you hire.</p>
    <p style="max-width:820px">The LAAA Team focuses exclusively on Los Angeles apartment buildings, concentrated in the A-level Westside cities of West Hollywood, Beverly Hills, and Santa Monica. This document is structured as a professional broker opinion of value. It covers the engagement team and our recent closings in this submarket, our reading of the West Hollywood market today, the marketing process we would run, the most relevant recent sale and rent comparables, a full financial analysis of the building, and a pricing recommendation. The valuation appears at the end, supported by the evidence that precedes it.</p>
  </div>
</section>

<!-- TEAM -->
<section id="team" class="alt">
  <div class="wrap">
    <div class="eyebrow">Engagement Team</div>
    <h2 style="font-size:30px;margin-bottom:8px">Two senior partners, directly accountable</h2>
    <p style="max-width:780px;margin-bottom:28px">Glen and Filip personally run this engagement end to end. There is no associate hand-off. The two founding partners of the LAAA Team carry a combined 26 years in the business, supported by a team of ten on every listing.</p>
    <div class="team">
      <div class="advisor">
        <img src="images/glen.png" alt="Glen Scher">
        <div>
          <h3>Glen Scher</h3>
          <div class="ttl">Senior Managing Director Investments</div>
          <div class="lic">CA DRE #01962976 &nbsp;|&nbsp; (818) 212-2808</div>
          <div class="ct">12th year at Marcus &amp; Millichap. One of the top multifamily brokers in Los Angeles, specializing exclusively in 5+ unit apartment buildings across the Westside and San Fernando Valley. Author of widely-read analysis on Measure ULA and the LA rent-controlled market.</div>
        </div>
      </div>
      <div class="advisor">
        <img src="images/filip.png" alt="Filip Niculete">
        <div>
          <h3>Filip Niculete</h3>
          <div class="ttl">Senior Managing Director Investments</div>
          <div class="lic">CA DRE #01905352 &nbsp;|&nbsp; (818) 212-2748</div>
          <div class="ct">14th year at Marcus &amp; Millichap and co-founder of the LAAA Team. Known for execution, integrity, and a relentless work ethic, Filip and the team consistently lead the Los Angeles market in active multifamily inventory.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- RESUME -->
<section id="resume">
  <div class="wrap">
    <div class="eyebrow">Track Record</div>
    <h2 style="font-size:32px;max-width:820px">The most active team in the Los Angeles 5 to 25-unit apartment market since 2018</h2>
    <p style="max-width:820px;margin-top:14px">Transaction volume in this size range is the most relevant qualification for pricing and selling an asset like 613 Westbourne. The figures below reflect the firm-wide career record of the LAAA Team. The submarket detail that follows shows where that volume is concentrated.</p>

    <div class="stats dark" style="margin-top:28px">
      <div class="s"><div class="n">460+</div><div class="l">Apartment buildings sold</div></div>
      <div class="s"><div class="n">$1.5B+</div><div class="l">In closed apartment sales</div></div>
      <div class="s"><div class="n">#1</div><div class="l">LA team, 5&ndash;25 units, since 2018</div></div>
      <div class="s"><div class="n">100+</div><div class="l">1031 exchanges navigated</div></div>
    </div>
    <div class="stats" style="margin-top:16px">
      <div class="s"><div class="n">26</div><div class="l">Apartment listings active right now</div></div>
      <div class="s"><div class="n">11</div><div class="l">Currently in escrow</div></div>
      <div class="s"><div class="n">15</div><div class="l">Closed so far this year</div></div>
      <div class="s"><div class="n">10</div><div class="l">Team members behind your listing</div></div>
    </div>

    <h3 style="font-size:22px;margin-top:48px">Concentration: the prime Westside</h3>
    <p style="max-width:820px;margin-top:8px">The team's work is concentrated in the prime, supply-constrained Westside cities most relevant to 613 Westbourne, West Hollywood, the Fairfax&ndash;Melrose corridor, Beverly Hills, Santa Monica, and the wider West LA / Brentwood / Westwood market. Across these submarkets the team has closed:</p>
    <div class="resume-cards">
      <div class="rc" style="grid-column:1/-1;border-top-width:4px;background:#f4f7fb;text-align:center;padding:30px 22px">
        <div class="big" style="font-size:54px;line-height:1">__PRIME_B__ buildings &middot; __PRIME_U__ units</div>
        <div class="det" style="font-size:14px;margin-top:8px">Apartment buildings the team has closed across the prime Westside</div>
      </div>
    </div>

    <h3 style="font-size:22px;margin-top:48px">Closings across prime Los Angeles</h3>
    <p style="max-width:820px;margin-top:8px">Each pin is an apartment building the team has closed in these A-level submarkets. The map filters by city; the West Hollywood view shows the proximity of recent LAAA transactions to the subject.</p>
    <div class="map-controls" id="resumeControls"></div>
    <div id="resumeMap" class="map"></div>
    <div class="maptip">Click any pin for the address, unit count, and year closed.</div>
    <div class="print-map-note">Interactive map of LAAA closings available at 613-westbourne.laaa.com.</div>

    <div class="callout">
      <div class="eyebrow">Proximity to the subject</div>
      <h3>A recent LAAA closing on the same block as one of the strongest comparables</h3>
      <p>In January 2025 the team closed 1046 N Genesee Ave in prime West Hollywood, the same block as 1036 N Genesee, which traded in April 2026 at $2.85M and is one of the most relevant comparables in this report. Recent closings within blocks of the subject reflect direct, current relationships with the buyer pool active in this submarket, rather than a database estimate.</p>
    </div>
  </div>
</section>

<!-- MARKETING -->
<section id="marketing" class="alt">
  <div class="wrap">
    <div class="eyebrow">Marketing Process</div>
    <h2 style="font-size:32px;max-width:820px">Full, simultaneous exposure to every qualified buyer</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">Demand is generated through a repeatable process the team has run across more than 460 closings. The objective is competitive tension: multiple qualified buyers evaluating the asset on the same timeline, which is what supports price.</p>

    <div class="feat" style="margin-top:26px">
      <div class="f"><h4><span class="ico">&#9742;</span> Direct access to the buyer pool</h4><p>The most probable buyer owns a similar building nearby. The team maintains confirmed contact records, name, mobile, and email, for essentially every apartment owner in West Hollywood, at roughly 95% accuracy. A full-time analyst keeps the database current on every LA County apartment sale.</p></div>
      <div class="f"><h4><span class="ico">&#128231;</span> A database that converts</h4><p>10,000+ principals and 15,000+ brokers. Every 1031 buyer we uncover goes onto a tracked exchange list. With 26 active listings, we are in constant contact with today's most active buyers, not the buyers of two years ago.</p></div>
      <div class="f"><h4><span class="ico">&#127758;</span> The M&amp;M platform</h4><p>Marcus &amp; Millichap dominates the $1&ndash;25M private-capital market with offices in every state and Canada, plus international reach. For an A-location like WeHo, that national and international exposure matters.</p></div>
      <div class="f"><h4><span class="ico">&#129309;</span> We share the deal</h4><p>We actively co-broke. We pursue outside brokers rather than hoard the listing, because the goal is finding every needle in the haystack, including the buyer from out of market we would never reach alone.</p></div>
    </div>

    <h3 style="font-size:20px;margin-top:40px">Launch sequence: live within 7 days</h3>
    <ul class="clean" style="max-width:840px">
      <li><strong>Within 7 calendar days</strong> of signing, we are 100% live online. The only thing that adds time is professional photography, which adds about three days.</li>
      <li><strong>Full offering memorandum</strong> drafted and sent to you for review and edits. We launch only once you approve it.</li>
      <li><strong>Simultaneous blast</strong>: emails, every major online platform, and physical postcards to mailboxes all hit at the same time to maximize same-time offers.</li>
      <li><strong>Due-diligence folder prepared up front</strong> so a buyer can move fast and cannot manufacture reasons to retrade.</li>
    </ul>
  </div>
</section>

<!-- INVESTMENT OVERVIEW -->
<section id="property">
  <div class="wrap">
    <div class="eyebrow">Investment Overview</div>
    <h2 style="font-size:32px;max-width:820px">A well-located 8-unit building with in-place income and measured upside</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">613 Westbourne Drive is a 1949-vintage, 8-unit apartment building in the heart of prime West Hollywood, walkable to Santa Monica Boulevard, the Design District, and the Beverly Hills border. The unit mix is split evenly between four one-bedroom and four two-bedroom homes, and the rent roll shows clear room to grow within the rules of West Hollywood rent stabilization.</p>
    <div class="twocol" style="margin-top:28px">
      <div>
        <h3 style="font-size:19px">The opportunity</h3>
        <ul class="clean">
          <li><strong>Prime, irreplaceable location</strong> in a 1.9-square-mile city where land is scarce and demand is durable.</li>
          <li><strong>Eight units, evenly split</strong> 1BR and 2BR, the size and mix today's private-capital buyers want most.</li>
          <li><strong>In-place income with upside.</strong> Several units sit below where the rest of the building is already achieving, leaving a clear path to higher income over time.</li>
          <li><strong>Strong financing math</strong>: the building debt-service-covers comfortably at today's rates, which keeps the buyer pool wide and offers credible.</li>
          <li><strong>No Measure ULA transfer tax</strong>: West Hollywood is exempt, a real advantage at this price point.</li>
        </ul>
      </div>
      <div class="demo">
        <div class="hd">Property snapshot</div>
        <div class="row"><span>Units</span><strong>8</strong></div>
        <div class="row"><span>Unit mix</span><strong>4 x 1BR &middot; 4 x 2BR</strong></div>
        <div class="row"><span>Gross building SF</span><strong>__SF__</strong></div>
        <div class="row"><span>Year built</span><strong>__YEAR__</strong></div>
        <div class="row"><span>Rent control</span><strong>WeHo RSO</strong></div>
        <div class="row"><span>In-place GRM</span><strong>__GRM__</strong></div>
        <div class="row"><span>In-place cap rate</span><strong>__CAP__</strong></div>
      </div>
    </div>
  </div>
</section>

<!-- PROPERTY DETAILS -->
<section id="details" class="alt">
  <div class="wrap">
    <div class="eyebrow">Property Details</div>
    <h2 style="font-size:30px;max-width:820px">The building at a glance</h2>
    <div class="twocol" style="margin-top:24px">
      <div class="demo">
        <div class="hd">Building &amp; site</div>
        <div class="row"><span>Address</span><strong>613 Westbourne Dr</strong></div>
        <div class="row"><span>City / ZIP</span><strong>West Hollywood, 90069</strong></div>
        <div class="row"><span>Property type</span><strong>Multifamily (apartments)</strong></div>
        <div class="row"><span>Number of units</span><strong>8</strong></div>
        <div class="row"><span>Year built</span><strong>__YEAR__</strong></div>
        <div class="row"><span>Gross building SF</span><strong>__SF__</strong></div>
      </div>
      <div class="demo">
        <div class="hd">Unit mix &amp; metering</div>
        <div class="row"><span>One-bedroom / one-bath</span><strong>4 units &middot; ~800 SF</strong></div>
        <div class="row"><span>Two-bedroom / two-bath</span><strong>4 units &middot; ~950 SF</strong></div>
        <div class="row"><span>In-unit gas &amp; electric</span><strong>Tenant paid</strong></div>
        <div class="row"><span>Water / sewer / trash</span><strong>Owner paid</strong></div>
        <div class="row"><span>Rent stabilization</span><strong>West Hollywood RSO</strong></div>
        <div class="row"><span>Transfer tax (Measure ULA)</span><strong>Exempt</strong></div>
      </div>
    </div>
    <p class="maptip" style="margin-top:18px">Figures reflect the current pricing model and should be verified in due diligence.</p>
  </div>
</section>

<!-- WEST HOLLYWOOD / LOCATION -->
<section id="weho">
  <div class="wrap">
    <div class="eyebrow">West Hollywood Market Context</div>
    <h2 style="font-size:32px;max-width:820px">A 1.9-square-mile city with its own regulatory framework</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">West Hollywood is among the most desirable and resilient multifamily submarkets in Greater Los Angeles, and one of the most distinct. WeHo and Santa Monica operate under their own ordinances rather than the City of Los Angeles rules. Pricing and marketing the asset correctly within that framework requires a specialist who transacts here regularly.</p>

    <div class="twocol" style="margin-top:30px">
      <div>
        <p>Dubbed &ldquo;The Creative City,&rdquo; West Hollywood sits between Beverly Hills and Hollywood, anchored by the Sunset Strip, the West Hollywood Design District, the Pacific Design Center, and the boutiques of Robertson and Melrose. It is consistently ranked among the most walkable cities in California, drawing a dense, affluent base of young professionals and creatives.</p>
        <p>For an apartment owner, what matters is the fundamentals beneath that lifestyle: roughly 80% of WeHo housing is renter-occupied, vacancy is historically low, and limited land plus strict zoning keep supply tight. Development demand remains strong, from The Harland's luxury residences to the $71M-financed 8850 Sunset project, which continues to support rising values and durable rental demand. This is a market where well-marketed, well-priced buildings still trade.</p>
        <ul class="clean">
          <li><strong>No Measure ULA transfer tax</strong>: unlike the City of LA, WeHo is exempt, a real advantage for sellers at this price point.</li>
          <li><strong>West Hollywood Rent Stabilization</strong>: among the strictest in the region. We underwrite and market to it correctly so buyers price the building accurately and do not retrade.</li>
          <li><strong>Investor-driven buyer pool</strong>: the WeHo buyer is acquiring income and location, and that buyer pool is well known to the team.</li>
        </ul>
      </div>
      <div class="demo">
        <div class="hd">West Hollywood at a glance</div>
        <div class="row"><span>City footprint</span><strong>1.9 sq mi</strong></div>
        <div class="row"><span>Population</span><strong>~35,000</strong></div>
        <div class="row"><span>Renter-occupied housing</span><strong>~80%</strong></div>
        <div class="row"><span>Median household income</span><strong>~$95,000</strong></div>
        <div class="row"><span>Per-capita income</span><strong>~$88,000</strong></div>
        <div class="row"><span>Median age</span><strong>~40</strong></div>
        <div class="row"><span>Transfer tax (Measure ULA)</span><strong>Exempt</strong></div>
      </div>
    </div>

    <h3 style="font-size:20px;margin-top:44px">613 Westbourne Drive in context</h3>
    <p style="max-width:820px;margin-top:8px">The subject sits in the heart of prime West Hollywood, walkable to Santa Monica Boulevard, the Design District, and the Beverly Hills border. The map below shows the property alongside recent LAAA closings nearby.</p>
    <div id="subjectMap" class="map" style="height:440px"></div>
    <div class="maptip">Gold marker: 613 Westbourne Drive. Navy markers: LAAA closings nearby.</div>
    <div class="print-map-note">Interactive location map available at 613-westbourne.laaa.com.</div>
  </div>
</section>

<!-- MARKET -->
<section id="market" class="alt">
  <div class="wrap">
    <div class="eyebrow">Market Conditions</div>
    <h2 style="font-size:30px;max-width:820px">A candid read: healthy and active, balanced between buyer and seller</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">The team's current view of the market and its likely direction, stated plainly.</p>
    <div class="feat" style="margin-top:24px">
      <div class="f"><h4><span class="ico">1</span> Where we are vs. the peak</h4><p>The all-time peak was the end of 2022, when money was nearly free and deals traded at 4% cap rates. The market corrected 15&ndash;25% depending on submarket. West Hollywood, as an A-location, sits at the lower end of that correction, closer to 15%.</p></div>
      <div class="f"><h4><span class="ico">2</span> The recovery is real</h4><p>2024 and the first half of 2025 were genuinely tough. Since then the market has recovered meaningfully. We are not just listing deals, we are opening escrows and closing them. Right now we have 11 deals in escrow and 15 closed this year.</p></div>
      <div class="f"><h4><span class="ico">3</span> What to expect ahead</h4><p>We expect status quo for the foreseeable future. There are no signs from our boots on the ground, or from Marcus &amp; Millichap's national research, of a major move up or down. We do not have a crystal ball, and we will not pretend to.</p></div>
      <div class="f"><h4><span class="ico">4</span> It is a per-deal market</h4><p>Conditions favor buyers more than in 2022, though the balance is close. Outcome comes down to execution: correct pricing, full exposure, and multiple offers arriving on the same timeline. Those are the variables the engagement controls.</p></div>
    </div>
  </div>
</section>

<!-- BUYER PROFILE -->
<section id="buyer">
  <div class="wrap">
    <div class="eyebrow">Buyer Profile</div>
    <h2 style="font-size:30px;max-width:820px">The most probable buyer, and how the likely objections are addressed</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">The most likely buyer is a private-capital investor or 1031 exchange buyer who already owns on the Westside and is seeking a well-located, manageable building in a city that holds value. These buyers are largely known to the team. The points below anticipate where they will press, and how each is addressed before it becomes a retrade.</p>
    <div class="feat" style="margin-top:24px">
      <div class="f"><h4><span class="ico">A</span> &ldquo;The rents are under market.&rdquo;</h4><p>True, and that is the upside, not a problem. We frame the in-place income as a floor, document the achievable rents within RSO rules, and let the buyer underwrite the growth they are paying a fair price to capture.</p></div>
      <div class="f"><h4><span class="ico">B</span> &ldquo;It is rent-controlled.&rdquo;</h4><p>Every comparable building here is. We price to RSO, market to RSO-savvy buyers, and present clean, accurate financials so nobody discovers a surprise in diligence and tries to chip the price.</p></div>
      <div class="f"><h4><span class="ico">C</span> &ldquo;What about the building's age and condition?&rdquo;</h4><p>We prepare the due-diligence folder up front, reports, rent roll, and operating history, so the buyer can move quickly and cannot manufacture reasons to retrade late in escrow.</p></div>
      <div class="f"><h4><span class="ico">D</span> &ldquo;Will it appraise and finance?&rdquo;</h4><p>At the suggested price the building covers debt service at today's rates with room to spare. That keeps lenders comfortable and the buyer pool wide, which protects your price through close.</p></div>
    </div>
  </div>
</section>

<!-- SALE COMPS -->
<section id="comps" class="alt">
  <div class="wrap">
    <div class="eyebrow">Sale Comparable Analysis</div>
    <h2 style="font-size:32px;max-width:820px">The most relevant recent West Hollywood sales</h2>
    <p style="max-width:860px;margin-top:14px">Six recent closed sales of comparable rent-controlled apartment buildings in and around prime West Hollywood. The subject is shown in gold for direct comparison. On the metrics that drive value: price per unit, price per square foot, cap rate, and gross rent multiplier, 613 Westbourne at the suggested price sits squarely within the range and right at the median.</p>
    <div id="compMap" class="map" style="height:440px"></div>
    <div class="maptip">Gold marker: 613 Westbourne (subject). Navy markers: recent closed sales. Click any pin for details.</div>
    <div class="print-map-note">Interactive sale-comparable map available at 613-westbourne.laaa.com.</div>
    <div class="table-scroll">
      <table class="fin">
        <thead><tr><th>#</th><th>Address</th><th>Units</th><th>Built</th><th>SF</th><th>Closed</th><th>Sale Price</th><th>$/Unit</th><th>$/SF</th><th>Cap</th><th>GRM</th></tr></thead>
        <tbody>__SALE_COMP_ROWS__</tbody>
      </table>
    </div>
    <div style="margin-top:26px">__SALE_COMP_NARR__</div>
    <p class="maptip">Source: TheMLS closed-sale records, compiled by Glen Scher (CA DRE #01962976). Cap rate shown where reported by the listing source.</p>
  </div>
</section>

<!-- RENT COMPS -->
<section id="rentcomps">
  <div class="wrap">
    <div class="eyebrow">Rent Comparable Analysis</div>
    <h2 style="font-size:30px;max-width:820px">What one- and two-bedroom units rent for nearby</h2>
    <p style="max-width:860px;margin-top:14px">A market rent survey within a half-mile of the subject. The broad market spans new construction and non-rent-controlled product, so the medians below run well above what an RSO building like 613 Westbourne can charge a sitting tenant. We use them as context: they confirm the direction of rent growth and underscore the long-term upside, while our pro-forma rents stay conservative and defensible within rent-stabilization rules.</p>
    <div class="table-scroll">
      <table class="fin">
        <thead><tr><th>Unit Type</th><th>Subject Pro-Forma Rent</th><th>Market 25th&ndash;75th Pctile</th><th>Market Median</th><th>Market Mean</th><th>Samples</th></tr></thead>
        <tbody>__RENT_COMP_ROWS__</tbody>
      </table>
    </div>
    <p class="maptip">Source: Rentometer market survey, 0.5-mile radius, pulled 2026-05-28. Subject pro-forma rents from the LAAA pricing model.</p>
  </div>
</section>

<!-- FINANCIAL ANALYSIS: RENT ROLL -->
<section id="financials" class="alt">
  <div class="wrap">
    <div class="eyebrow">Financial Analysis</div>
    <h2 style="font-size:32px;max-width:820px">Unit mix &amp; rent roll</h2>
    <p style="max-width:860px;margin-top:14px">The current rent roll alongside achievable pro-forma rents. The spread between current and pro-forma is the income upside a buyer is acquiring, documented, unit by unit.</p>
    <div class="table-scroll">
      <table class="fin">
        <thead><tr><th>Unit</th><th>Type</th><th>SF</th><th>Current Rent</th><th>Rent/SF</th><th>Pro-Forma Rent</th><th>PF/SF</th></tr></thead>
        <tbody>__RENT_ROLL__</tbody>
      </table>
    </div>
  </div>
</section>

<!-- OPERATING STATEMENT -->
<section id="opstatement">
  <div class="wrap">
    <div class="eyebrow">Financial Analysis</div>
    <h2 style="font-size:30px;max-width:820px">Operating statement</h2>
    <div class="os">
      <div>
        <table class="fin">
          <thead><tr><th>Income</th><th>Annual</th><th>Per Unit</th><th>$/SF</th><th>% EGI</th></tr></thead>
          <tbody>__OS_INCOME__</tbody>
        </table>
        <table class="fin" style="margin-top:22px">
          <thead><tr><th>Expenses</th><th>Annual</th><th>Per Unit</th><th>$/SF</th><th>% EGI</th></tr></thead>
          <tbody>__OS_EXP__</tbody>
        </table>
      </div>
      <div class="notes">
        <h3>Notes to Operating Statement</h3>
        __OS_NOTES__
      </div>
    </div>
  </div>
</section>

<!-- FINANCIAL SUMMARY -->
<section id="summary" class="alt">
  <div class="wrap">
    <div class="eyebrow">Financial Analysis</div>
    <h2 style="font-size:30px;max-width:820px">Summary: current and pro forma</h2>
    <p style="max-width:860px;margin-top:14px">The complete picture at the suggested list price, current in-place and on a conservative pro-forma basis, with financing modeled at a 55% loan-to-value, 6.00% fixed loan amortized over 30 years.</p>
    <div class="sm-cols">
      <div>__SUMMARY_LEFT__</div>
      <div>__SUMMARY_RIGHT__</div>
    </div>
  </div>
</section>

<!-- PRICE REVEAL + PRICING MATRIX -->
<section id="pricing">
  <div class="wrap">
    <div class="eyebrow">Pricing Recommendation</div>
    <div class="pricewrap" style="margin-top:6px">
      <div class="lbl">Suggested List Price</div>
      <div class="bigprice">__LIST_FMT__</div>
    </div>
    <div class="stats" style="margin-top:8px">
      <div class="s"><div class="n">__PPU_FMT__</div><div class="l">Price per unit</div></div>
      <div class="s"><div class="n">__PSF_FMT__</div><div class="l">Price per SF</div></div>
      <div class="s"><div class="n">__CAP_FMT__</div><div class="l">In-place cap rate</div></div>
      <div class="s"><div class="n">__GRM_FMT__</div><div class="l">In-place GRM</div></div>
    </div>

    <h3 style="font-size:20px;margin-top:44px">Pricing matrix</h3>
    <p style="max-width:860px;margin-top:8px">How the key return metrics move across a range of prices. The highlighted row is our suggested list price.</p>
    <div class="table-scroll">
      <table class="fin">
        <thead><tr><th>Purchase Price</th><th>Current Cap</th><th>Pro-Forma Cap</th><th>Cash-on-Cash</th><th>$/SF</th><th>$/Unit</th><th>PF GRM</th></tr></thead>
        <tbody>__MATRIX_ROWS__</tbody>
      </table>
    </div>

    <div class="trade">
      <div class="lbl">A trade price in the current investment environment of</div>
      <div class="px">__TRADE__</div>
    </div>

    <h3 style="font-size:20px;margin-top:40px">Pricing rationale</h3>
    <p style="max-width:880px">This is an investment sale, not a home sale. The buyer is solving for return: price per unit, price per square foot, cap rate, GRM, and cash-on-cash at today's low-6% interest rates. The subject is valued against the appropriate comparable set: rent-controlled, pre-1978, comparable in size, and the most recent sales available, since the market has moved.</p>
    <p style="max-width:880px">At __LIST_FMT__, 613 Westbourne pencils to __PPU_FMT__ per unit, __PSF_FMT__ per square foot, a __CAP_FMT__ in-place cap rate, and an __GRM_FMT__ in-place GRM. Every one of those figures lands within the range of the six recent comparable sales and right at the median on price per unit and GRM. The slightly lower cap and GRM versus the comp set reflect the building's clear path to higher income, which a buyer pays a fair price today to capture. Our recommendation is to list at this number, which establishes the price we are confident the building will sell at while leaving appropriate room for negotiation. The trade range above reflects where we expect the building to transact in the current environment.</p>
    <div class="callout" style="margin-top:8px">
      <div class="eyebrow">Aligned to the timeline</div>
      <h3 style="font-size:19px">A path to close ahead of late summer</h3>
      <p>Live within a week of signing, offers in the first two to three weeks, escrow opened by week four, and a 45 to 60-day escrow. That sequence closes well ahead of the late-summer slowdown.</p>
    </div>
    <p class="maptip" style="margin-top:18px"><strong>Assumptions &amp; conditions:</strong> This Broker Opinion of Value is not an appraisal. Financial figures are based on information from the owner and the LAAA pricing model and should be verified in due diligence. Returns assume the financing terms stated above; actual terms will vary with the buyer and lender. Pro-forma rents reflect achievable income within West Hollywood rent-stabilization rules and are not guaranteed.</p>
  </div>
</section>

<!-- PROCESS / EXECUTION -->
<section id="process" class="alt">
  <div class="wrap">
    <div class="eyebrow">Execution</div>
    <h2 style="font-size:32px;max-width:820px">Priced correctly, exposed fully, and structured to close on schedule</h2>
    <div class="twocol" style="margin-top:26px">
      <div>
        <h3 style="font-size:19px">How we run the process</h3>
        <p>Our recommendation is to establish the number we are confident it will sell at, list there, and then create real competition through full, simultaneous exposure. The goal is multiple qualified offers on the table at the same time, that is what moves price, not a high asking number that sits.</p>
        <h3 style="font-size:19px;margin-top:24px">Vetting the buyer</h3>
        <p>Terms matter as much as price in a 1031. Every prospective buyer is asked a direct question: what is the rationale for the purchase. The team almost always knows the buyer or broker and their reputation, and provides a candid assessment of whether a given offer will actually close.</p>
      </div>
      <div>
        <div class="demo">
          <div class="hd">What our track record shows</div>
          <div class="row"><span>Avg. days to open escrow</span><strong>36 days</strong></div>
          <div class="row"><span>Career sale-to-list ratio</span><strong>96.5%</strong></div>
          <div class="row"><span>Avg. offers per deal</span><strong>~2.8</strong></div>
          <div class="row"><span>Time to fully live online</span><strong>7 days</strong></div>
          <div class="row"><span>Typical escrow length</span><strong>45&ndash;60 days</strong></div>
          <div class="row"><span>Loan contingencies allowed</span><strong>None</strong></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- 1031 -->
<section id="exchange">
  <div class="wrap">
    <div class="eyebrow">1031 Exchange Expertise</div>
    <h2 style="font-size:32px;max-width:820px">The exchange is not a complication for us, it is our core business</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">The vast majority of our deals involve a 1031 exchange on the buy side, the sell side, or both. We have navigated well over 100 of them, and every one is documented as a case study on LAAA.com.</p>
    <div class="feat" style="margin-top:24px">
      <div class="f"><h4><span class="ico">&#8644;</span> Selling into your San Francisco purchase</h4><p>Exchanging from Westbourne into a Bay Area home is fully doable, the replacement simply has to be held for investment. We will make sure your timeline and documentation line up so the exchange holds.</p></div>
      <div class="f"><h4><span class="ico">&#9201;</span> The reverse-exchange option</h4><p>If you find the new property first, a reverse exchange lets you acquire before you sell. It is only nominally more expensive, often just a few thousand dollars that blend into closing costs, and it removes the pressure of a fire sale. A real option worth keeping open.</p></div>
      <div class="f"><h4><span class="ico">&#128221;</span> Get the structure right</h4><p>Renting the replacement home to family can work, but the details matter. We will point you to the right 1031 accommodator and counsel so it is structured cleanly from day one. (We coordinate the real estate; your tax and legal advisors confirm the structure.)</p></div>
      <div class="f"><h4><span class="ico">&#9989;</span> Terms that protect the exchange</h4><p>We structure timelines, deposits, and contingencies specifically to protect your exchange windows, something a residential agent simply is not set up to do.</p></div>
    </div>
  </div>
</section>

<!-- REFERENCES / NEXT STEPS -->
<section id="next" class="alt">
  <div class="wrap">
    <div class="eyebrow">References &amp; Next Steps</div>
    <h2 style="font-size:30px;max-width:820px">References available on request</h2>
    <div class="twocol" style="margin-top:22px">
      <div>
        <p>Broker competence is the priority you identified, and we welcome the diligence. We are glad to connect you with current and recently-closed clients, including sellers who have completed their own 1031 exchanges, so the team can be assessed directly on reliability, capability, and the day-to-day experience of the engagement.</p>
        <ul class="clean">
          <li>Direct references from active and recently-closed clients, on request.</li>
          <li>A full offering memorandum drafted and turned around quickly, ready for launch within 7 days of signing.</li>
          <li>Sample offering memoranda that show exactly what the marketing package will look like.</li>
        </ul>
      </div>
      <div class="callout">
        <div class="eyebrow">Next Steps</div>
        <h3 style="font-size:19px">From engagement to live listing</h3>
        <p>On engagement, the offering memorandum is drafted for review and the property is fully live within roughly a week. The team coordinates photography, the due-diligence folder, and the simultaneous marketing launch so the asset reaches the full buyer pool at once.</p>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER / CONTACT -->
<footer id="contact">
  <div class="wrap">
    <img class="logo" src="images/logo-white.png" alt="LAAA Team">
    <div class="fteam">
      <div>
        <h4>Glen Scher</h4>
        <div class="ttl">Senior Managing Director Investments</div>
        <div class="ct">
          (818) 212-2808<br>
          <a href="mailto:Glen.Scher@marcusmillichap.com">Glen.Scher@marcusmillichap.com</a><br>
          CA DRE #01962976
        </div>
      </div>
      <div>
        <h4>Filip Niculete</h4>
        <div class="ttl">Senior Managing Director Investments</div>
        <div class="ct">
          (818) 212-2748<br>
          <a href="mailto:Filip.Niculete@marcusmillichap.com">Filip.Niculete@marcusmillichap.com</a><br>
          CA DRE #01905352
        </div>
      </div>
    </div>
    <div class="ct" style="margin-bottom:30px">
      The LAAA Team at Marcus &amp; Millichap &nbsp;|&nbsp; 16830 Ventura Blvd, Ste. 100, Encino, CA 91436<br>
      <a href="https://www.laaa.com">www.LAAA.com</a> &nbsp;|&nbsp; marcusmillichap.com/laaa-team
    </div>
    <div class="legal">
      This Broker Opinion of Value and marketing proposal has been prepared exclusively for Ian Lee and the Lee family for the purpose of evaluating brokerage representation for 613 Westbourne Drive, West Hollywood, CA 90069. It is confidential and is not an appraisal. Track-record figures reflect the career production of the LAAA Team. Financial figures derive from the owner-supplied information and the LAAA pricing model and must be verified in due diligence. Statements regarding market conditions and value represent the opinion of the LAAA Team and are not guarantees of future results. The LAAA Team does not provide tax or legal advice; consult your own 1031 accommodator, accountant, and attorney regarding exchange structure. &copy; 2026 The LAAA Team at Marcus &amp; Millichap.
    </div>
  </div>
</footer>

<script>
  // Hide-on-scroll-down nav
  var lastY=0, nav=document.getElementById('nav');
  window.addEventListener('scroll',function(){
    var y=window.pageYOffset;
    nav.style.transform=(y>lastY && y>120)?'translateY(-100%)':'translateY(0)';
    lastY=y;
  });

  // ---- Google Maps ----
  var SUBJECT = __SUBJECT_JSON__;
  var MARKERS = __MARKERS_JSON__;
  var COMPS = __COMPS_JSON__;
  var CITY_COLORS = {
    'West Hollywood':'#C5A258',
    'WeHo Corridor (Fairfax/Melrose)':'#1B3A5C',
    'Beverly Hills':'#2e6b8f',
    'Santa Monica':'#3d8168',
    'Westwood / Brentwood / West LA':'#7a5ea0'
  };
  var resumeMap, subjectMap, compMap, resumeMarkers=[], info;

  function pin(color){
    return {
      path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z',
      fillColor: color, fillOpacity: 1, strokeColor:'#fff', strokeWeight:1.5, scale:0.85,
      anchor: new google.maps.Point(0,0)
    };
  }
  function star(color){
    return { path: google.maps.SymbolPath.CIRCLE, fillColor:color, fillOpacity:1, strokeColor:'#fff', strokeWeight:3, scale:11 };
  }
  function iw(map, mk, html){
    mk.addListener('click', function(){ info.setContent(html); info.open(map, mk); });
  }

  function initMaps(){
    info = new google.maps.InfoWindow();

    // RESUME MAP
    resumeMap = new google.maps.Map(document.getElementById('resumeMap'),{
      center:{lat:34.05,lng:-118.41}, zoom:11, mapTypeControl:false, streetViewControl:false,
      styles:[{featureType:'poi',stylers:[{visibility:'off'}]}]
    });
    MARKERS.forEach(function(m){
      var mk = new google.maps.Marker({
        position:{lat:m.lat,lng:m.lng}, map:resumeMap,
        icon: pin(CITY_COLORS[m.city]||'#1B3A5C'), title:m.a, _city:m.city
      });
      iw(resumeMap, mk, '<div style="font-family:Inter,sans-serif;padding:2px 4px"><strong style="color:#1B3A5C">'+m.a+'</strong><br><span style="color:#5b6470;font-size:13px">'+m.city+' &middot; '+(m.u||'&ndash;')+' units &middot; closed '+m.y+'</span></div>');
      resumeMarkers.push(mk);
    });
    buildControls();

    // SUBJECT MAP
    subjectMap = new google.maps.Map(document.getElementById('subjectMap'),{
      center:{lat:SUBJECT.lat,lng:SUBJECT.lng}, zoom:14, mapTypeControl:false, streetViewControl:true,
      styles:[{featureType:'poi.business',stylers:[{visibility:'on'}]}]
    });
    var subjMk = new google.maps.Marker({
      position:{lat:SUBJECT.lat,lng:SUBJECT.lng}, map:subjectMap, icon:star('#C5A258'),
      title:'613 Westbourne Drive', zIndex:999
    });
    iw(subjectMap, subjMk, '<div style="font-family:Inter,sans-serif;padding:2px 4px"><strong style="color:#1B3A5C">613 Westbourne Drive</strong><br><span style="color:#5b6470;font-size:13px">West Hollywood, CA 90069 &middot; 8 units</span></div>');
    MARKERS.filter(function(m){ return m.city.indexOf('Hollywood')>-1 || m.city.indexOf('WeHo')>-1; }).forEach(function(m){
      var mk=new google.maps.Marker({ position:{lat:m.lat,lng:m.lng}, map:subjectMap, icon:pin('#1B3A5C'), title:m.a });
      iw(subjectMap, mk, '<div style="font-family:Inter,sans-serif;padding:2px 4px"><strong style="color:#1B3A5C">'+m.a+'</strong><br><span style="color:#5b6470;font-size:13px">LAAA closing &middot; '+(m.u||'&ndash;')+' units &middot; '+m.y+'</span></div>');
    });

    // COMP MAP
    compMap = new google.maps.Map(document.getElementById('compMap'),{
      center:{lat:SUBJECT.lat,lng:SUBJECT.lng}, zoom:14, mapTypeControl:false, streetViewControl:false,
      styles:[{featureType:'poi',stylers:[{visibility:'off'}]}]
    });
    var subjMk2 = new google.maps.Marker({
      position:{lat:SUBJECT.lat,lng:SUBJECT.lng}, map:compMap, icon:star('#C5A258'),
      title:'613 Westbourne Drive (Subject)', zIndex:999
    });
    iw(compMap, subjMk2, '<div style="font-family:Inter,sans-serif;padding:2px 4px"><strong style="color:#C5A258">613 Westbourne Drive</strong><br><span style="color:#5b6470;font-size:13px">Subject &middot; 8 units</span></div>');
    var compMarkers=[subjMk2];
    COMPS.forEach(function(c){
      var mk=new google.maps.Marker({ position:{lat:c.lat,lng:c.lng}, map:compMap, icon:pin('#1B3A5C'), title:c.a });
      iw(compMap, mk, '<div style="font-family:Inter,sans-serif;padding:2px 4px"><strong style="color:#1B3A5C">'+c.a+'</strong><br><span style="color:#5b6470;font-size:13px">'+c.u+' units &middot; $'+c.p+' &middot; closed '+c.y+'</span></div>');
      compMarkers.push(mk);
    });

    setupResizeGuard(resumeMap, document.getElementById('resumeMap'), function(){
      var b=new google.maps.LatLngBounds();
      resumeMarkers.forEach(function(mk){ if(mk.getVisible()) b.extend(mk.getPosition()); });
      if(!b.isEmpty()){ resumeMap.fitBounds(b); } else { resumeMap.setCenter({lat:34.05,lng:-118.41}); }
    });
    setupResizeGuard(subjectMap, document.getElementById('subjectMap'), function(){
      subjectMap.setCenter({lat:SUBJECT.lat,lng:SUBJECT.lng});
    });
    setupResizeGuard(compMap, document.getElementById('compMap'), function(){
      var b=new google.maps.LatLngBounds();
      compMarkers.forEach(function(mk){ b.extend(mk.getPosition()); });
      if(!b.isEmpty()) compMap.fitBounds(b);
    });
  }

  function setupResizeGuard(map, el, recenter){
    var done=false;
    function fix(){ if(done) return; done=true; google.maps.event.trigger(map,'resize'); recenter(); }
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(ents){
        ents.forEach(function(e){ if(e.isIntersecting){ fix(); io.disconnect(); } });
      }, {threshold:0.1});
      io.observe(el);
    } else {
      window.addEventListener('load', fix);
    }
  }

  function buildControls(){
    var cities = ['All'];
    MARKERS.forEach(function(m){ if(cities.indexOf(m.city)<0) cities.push(m.city); });
    var box = document.getElementById('resumeControls');
    cities.forEach(function(c,i){
      var b=document.createElement('button');
      b.textContent = c==='All' ? 'All submarkets' : c;
      if(i===0) b.className='active';
      b.onclick=function(){
        document.querySelectorAll('#resumeControls button').forEach(function(x){x.className='';});
        b.className='active';
        var bounds=new google.maps.LatLngBounds();
        resumeMarkers.forEach(function(mk){
          var show = (c==='All' || mk._city===c);
          mk.setVisible(show);
          if(show) bounds.extend(mk.getPosition());
        });
        if(!bounds.isEmpty()) resumeMap.fitBounds(bounds);
      };
      box.appendChild(b);
    });
  }
  window.initMaps = initMaps;
</script>
<script async src="https://maps.googleapis.com/maps/api/js?key=__MAPS_KEY__&callback=initMaps&loading=async"></script>
</body>
</html>"""

repl = {
  "__SUBJECT_JSON__": json.dumps(SUBJ),
  "__MARKERS_JSON__": json.dumps(MARKERS),
  "__COMPS_JSON__": COMPS_JSON,
  "__MAPS_KEY__": MAPS_KEY,
  "__WEHO_B__": str(weho_b), "__WEHO_U__": str(weho_u),
  "__CORR_B__": str(corr_b), "__CORR_U__": str(corr_u),
  "__BH_B__": str(bh_b), "__BH_U__": str(bh_u),
  "__SM_B__": str(sm_b), "__SM_U__": str(sm_u),
  "__WLA_B__": str(wla_b), "__WLA_U__": str(wla_u),
  "__AL_B__": str(al_b), "__AL_U__": str(al_u),
  "__PRIME_B__": str(prime_b), "__PRIME_U__": str(prime_u),
  "__SF__": f"{SF:,}", "__YEAR__": str(YEAR),
  "__GRM__": f"{SUB_GRM:.2f}x", "__CAP__": f"{SUB_CAP:.2f}%",
  "__RENT_ROLL__": rr,
  "__OS_INCOME__": os_income, "__OS_EXP__": os_exp, "__OS_NOTES__": os_notes_html,
  "__SALE_COMP_ROWS__": sc, "__SALE_COMP_NARR__": sc_narr,
  "__RENT_COMP_ROWS__": rent_comp_rows,
  "__MATRIX_ROWS__": matrix,
  "__SUMMARY_LEFT__": summary_left, "__SUMMARY_RIGHT__": summary_right,
  "__LIST_FMT__": usd(LIST), "__PPU_FMT__": usd(SUB_PPU),
  "__PSF_FMT__": f"${SUB_PSF:.0f}", "__CAP_FMT__": f"{SUB_CAP:.2f}%",
  "__GRM_FMT__": f"{SUB_GRM:.2f}x",
  "__TRADE__": f"{usd(TRADE_LOW)} &mdash; {usd(TRADE_HIGH)}",
}
out = HTML
for k, v in repl.items():
    out = out.replace(k, v)

open(r"C:\Users\gscher\613-westbourne-bov\index.html", "w", encoding="utf-8").write(out)
print("WROTE index.html", len(out), "chars")
print(f"List {usd(LIST)} | {usd(SUB_PPU)}/u | ${SUB_PSF:.0f}/SF | cap {SUB_CAP:.2f}% | GRM {SUB_GRM:.2f}")
print(f"NOI cur {usd(NOI_CUR)} / pf {usd(NOI_PF)} | EXP cur {usd(EXP_CUR)} ({EXP_CUR/EGI_CUR*100:.1f}%) / pf {usd(EXP_PF)} ({EXP_PF/EGI_PF*100:.1f}%)")
print(f"Matrix rows {len(MATRIX_PRICES)} | increment {usd(INCREMENT)} | trade {usd(TRADE_LOW)}-{usd(TRADE_HIGH)}")
print(f"Comp avg ppu {usd(mean(ppus))} med {usd(median(ppus))} | cap avg {mean(caps):.2f}% | grm med {median(grms):.2f}")
