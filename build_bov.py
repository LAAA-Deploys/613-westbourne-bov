# -*- coding: utf-8 -*-
"""Build price-free BOV site for 613 Westbourne Dr, West Hollywood.
Seller-facing win-the-listing pitch for Ian Lee & family. NO price anywhere.
All maps via Google Maps JS API (hard requirement)."""
import json

md = json.load(open(r"C:\Users\gscher\Downloads\map_data.json", encoding="utf-8"))
SUBJ = md["subject"]
MARKERS = md["markers"]
MAPS_KEY = "AIzaSyB1FbBfb4q0FVpiMSHBhjERp_R2lP3wDE8"

NAVY = "#1B3A5C"; GOLD = "#C5A258"

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>613 Westbourne Drive | Broker Opinion of Value | LAAA Team</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="images/logo-blue.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{ --navy:#1B3A5C; --gold:#C5A258; --ink:#1a1a1a; --gray:#5b6470; --line:#e4e7ec; --bg:#f7f8fa; }
  *{ box-sizing:border-box; margin:0; padding:0; }
  html{ scroll-behavior:smooth; }
  body{ font-family:'Inter',-apple-system,sans-serif; color:var(--ink); line-height:1.65; background:#fff; -webkit-font-smoothing:antialiased; }
  h1,h2,h3,h4{ line-height:1.2; font-weight:700; color:var(--navy); }
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
  nav .links{ display:flex; gap:24px; }
  nav .links a{ color:#cdd7e3; text-decoration:none; font-size:13px; font-weight:500; letter-spacing:.02em; }
  nav .links a:hover{ color:#fff; }
  @media(max-width:880px){ nav .links{ display:none; } }

  /* COVER */
  .cover{ background:linear-gradient(160deg,#15314f 0%,#1B3A5C 55%,#24496f 100%); color:#fff; padding:0; border:none; }
  .cover .wrap{ padding-top:70px; padding-bottom:0; }
  .cover .logo{ height:54px; margin-bottom:48px; }
  .cover .label{ display:inline-block; border:1px solid rgba(197,162,88,.6); color:var(--gold); text-transform:uppercase; letter-spacing:.18em; font-size:11px; font-weight:700; padding:7px 16px; border-radius:3px; margin-bottom:26px; }
  .cover h1{ color:#fff; font-size:58px; font-weight:800; letter-spacing:-.02em; }
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
  .stats .s .n{ font-size:34px; font-weight:800; color:var(--navy); letter-spacing:-.02em; }
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
  .rc .big{ font-size:30px; font-weight:800; color:var(--navy); margin-top:10px; }
  .rc .det{ font-size:13px; color:var(--gray); margin-top:4px; }
  @media(max-width:780px){ .resume-cards{ grid-template-columns:1fr 1fr; } }

  /* MAP */
  .map{ width:100%; height:480px; border-radius:12px; border:1px solid var(--line); margin-top:18px; background:#eef1f4; }
  .map-controls{ display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; }
  .map-controls button{ font-family:inherit; font-size:13px; font-weight:600; padding:8px 16px; border:1px solid var(--navy); background:#fff; color:var(--navy); border-radius:30px; cursor:pointer; transition:all .15s; }
  .map-controls button.active,.map-controls button:hover{ background:var(--navy); color:#fff; }
  .maptip{ font-size:12px; color:var(--gray); margin-top:10px; }

  /* TABLE */
  table{ width:100%; border-collapse:collapse; margin-top:18px; font-size:14px; }
  th{ background:var(--navy); color:#fff; text-align:left; padding:11px 14px; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:.04em; }
  td{ padding:11px 14px; border-bottom:1px solid var(--line); color:#33404f; }
  tr:nth-child(even) td{ background:#fafbfc; }
  .hl td{ background:#fdf8ee !important; font-weight:600; }

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
  footer .legal{ border-top:1px solid #2c4a6b; padding-top:24px; font-size:11.5px; color:#7e94ad; line-height:1.7; }
  @media(max-width:780px){ footer .fteam{ grid-template-columns:1fr; } }
</style>
</head>
<body>

<nav id="nav">
  <div class="wrap">
    <img src="images/logo-white.png" alt="LAAA Team">
    <div class="links">
      <a href="#team">Team</a>
      <a href="#resume">Track Record</a>
      <a href="#weho">West Hollywood</a>
      <a href="#market">Market</a>
      <a href="#marketing">Marketing</a>
      <a href="#process">Process</a>
      <a href="#exchange">1031</a>
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
<div class="prepared">The most qualified team to sell an 8-unit apartment building in an A-level Los Angeles location.</div>

<!-- INTRO -->
<section id="intro">
  <div class="wrap">
    <div class="eyebrow">A Note to the Lee Family</div>
    <h2 style="font-size:32px;max-width:760px">You told us what matters most: broker competence, a flawless 1031, and moving quickly. That is exactly what we do.</h2>
    <p class="lead" style="margin-top:20px;max-width:820px">For over a decade, the only thing we have sold is apartment buildings in Los Angeles &mdash; and our strongest markets are the A-level Westside cities like West Hollywood, Beverly Hills, and Santa Monica. Since 2018, no team has sold more apartment buildings in the 5 to 25-unit range in Los Angeles than we have. This proposal lays out who we are, what we have closed on your doorstep, how we read the West Hollywood market today, and the precise marketing machine we will run to get you the highest price in the timeframe you need.</p>
    <p style="max-width:820px">We have intentionally not put a price on this page. Pricing is a strategy conversation we want to have with you and your father directly &mdash; with the full analysis in front of us &mdash; not a headline number designed to win a beauty contest. What follows is the evidence that we are the right team to trust with that conversation.</p>
  </div>
</section>

<!-- TEAM -->
<section id="team" class="alt">
  <div class="wrap">
    <div class="eyebrow">Your Advisors</div>
    <h2 style="font-size:30px;margin-bottom:8px">Two senior partners &mdash; not a junior hand-off</h2>
    <p style="max-width:780px;margin-bottom:28px">You will work directly with both founding partners of the LAAA Team. Between us we carry 26 years in the business and a team of ten supporting every listing.</p>
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
    <div class="eyebrow">The Resume</div>
    <h2 style="font-size:32px;max-width:820px">Sold more LA apartment buildings in the 5&ndash;25 unit range than any other team since 2018</h2>
    <p style="max-width:820px;margin-top:14px">This is not a brag &mdash; it is the single most important qualification for selling your building. We price apartment buildings every single day, we know who the buyers are, and we know how to run the process. The numbers below are our firm-wide career record.</p>

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

    <h3 style="font-size:22px;margin-top:48px">Where we win: the A-level Westside</h3>
    <p style="max-width:820px;margin-top:8px">Our closed transactions are concentrated in exactly the markets that matter for your building &mdash; the prime, supply-constrained Westside cities. Here is a snapshot of our closings in these submarkets.</p>
    <div class="resume-cards">
      <div class="rc"><div class="city">West Hollywood</div><div class="big">__WEHO_B__</div><div class="det">buildings &middot; __WEHO_U__ units</div></div>
      <div class="rc"><div class="city">WeHo / Fairfax&ndash;Melrose Corridor</div><div class="big">__CORR_B__</div><div class="det">buildings &middot; __CORR_U__ units</div></div>
      <div class="rc"><div class="city">Beverly Hills</div><div class="big">__BH_B__</div><div class="det">buildings &middot; __BH_U__ units</div></div>
      <div class="rc"><div class="city">Santa Monica</div><div class="big">__SM_B__</div><div class="det">buildings &middot; __SM_U__ units</div></div>
      <div class="rc"><div class="city">Westwood / Brentwood / West LA</div><div class="big">__WLA_B__</div><div class="det">buildings &middot; __WLA_U__ units</div></div>
      <div class="rc" style="border-top-color:var(--navy);background:#f4f7fb"><div class="city">A-Level Westside Total</div><div class="big">__AL_B__</div><div class="det">buildings &middot; __AL_U__ units</div></div>
    </div>

    <h3 style="font-size:22px;margin-top:48px">Our closings across prime Los Angeles</h3>
    <p style="max-width:820px;margin-top:8px">Every pin is an apartment building we have closed in these A-level submarkets. Filter by city, or zoom to West Hollywood to see how close we have transacted to your building.</p>
    <div class="map-controls" id="resumeControls"></div>
    <div id="resumeMap" class="map"></div>
    <div class="maptip">Click any pin for the address, unit count, and year closed.</div>

    <div class="callout">
      <div class="eyebrow">On your doorstep</div>
      <h3>We closed a 5-unit building on North Genesee &mdash; the same block as your best comparable</h3>
      <p>In January 2025 we closed two West Hollywood apartment buildings within weeks of each other, including 1046 N Genesee Ave. That is the same block as one of the most relevant recent sales to your property. When we tell you what 613 Westbourne is worth, it comes from deals we actually closed nearby &mdash; not a database guess.</p>
    </div>

    <h3 style="font-size:20px;margin-top:44px">Recent West Hollywood closings</h3>
    <table>
      <thead><tr><th>Property</th><th>Units</th><th>Closed</th><th>Notes</th></tr></thead>
      <tbody>
        <tr class="hl"><td>1046 N Genesee Ave</td><td>5</td><td>Jan 2025</td><td>Same block as your top comparable</td></tr>
        <tr><td>1052 N Martel Ave</td><td>5</td><td>Jan 2025</td><td>Prime WeHo, closed alongside Genesee</td></tr>
        <tr><td>9005 Keith Ave</td><td>5</td><td>2020</td><td>Heart of West Hollywood, 90069</td></tr>
      </tbody>
    </table>
    <p class="maptip">Plus additional closings throughout the Fairfax / Melrose corridor and the adjacent Beverly Hills and Hollywood submarkets. A full deal-by-deal history is available at LAAA.com.</p>
  </div>
</section>

<!-- WEST HOLLYWOOD -->
<section id="weho" class="alt">
  <div class="wrap">
    <div class="eyebrow">We Know West Hollywood</div>
    <h2 style="font-size:32px;max-width:820px">A 1.9-square-mile city with its own rules &mdash; and we know all of them</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">West Hollywood is one of the most desirable and resilient multifamily submarkets in all of Greater Los Angeles. It is also one of the most unique &mdash; WeHo and Santa Monica do not play by the City of LA's rules. That distinction is exactly why you need a specialist who sells here, not a generalist.</p>

    <div class="twocol" style="margin-top:30px">
      <div>
        <p>Dubbed &ldquo;The Creative City,&rdquo; West Hollywood sits between Beverly Hills and Hollywood, anchored by the Sunset Strip, the West Hollywood Design District, the Pacific Design Center, and the boutiques of Robertson and Melrose. It is consistently ranked among the most walkable cities in California, drawing a dense, affluent base of young professionals and creatives.</p>
        <p>For an apartment owner, what matters is the fundamentals beneath that lifestyle: roughly 80% of WeHo housing is renter-occupied, vacancy is historically low, and limited land plus strict zoning keep supply tight. Development demand remains strong &mdash; from The Harland's luxury residences to the $71M-financed 8850 Sunset project &mdash; which continues to support rising values and durable rental demand. This is a market where well-marketed, well-priced buildings still trade.</p>
        <ul class="clean">
          <li><strong>No Measure ULA transfer tax</strong> &mdash; unlike the City of LA, WeHo is exempt, a real advantage for sellers at this price point.</li>
          <li><strong>West Hollywood Rent Stabilization</strong> &mdash; among the strictest in the region. We underwrite and market to it correctly so buyers price the building accurately and do not retrade.</li>
          <li><strong>Investor-driven buyer pool</strong> &mdash; the WeHo buyer is buying income and location, and we know precisely who they are.</li>
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
    <p style="max-width:820px;margin-top:8px">Your building sits in the heart of prime West Hollywood, walkable to Santa Monica Boulevard, the Design District, and the Beverly Hills border. The map below shows the subject property alongside our nearby closings.</p>
    <div id="subjectMap" class="map" style="height:440px"></div>
    <div class="maptip">Gold marker: 613 Westbourne Drive. Navy markers: LAAA closings nearby.</div>
  </div>
</section>

<!-- MARKET -->
<section id="market">
  <div class="wrap">
    <div class="eyebrow">The Market Right Now</div>
    <h2 style="font-size:30px;max-width:820px">An honest read: healthy and active, fair to both sides</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">You asked how we see the market and where it is heading. Here is the straight answer, with no spin.</p>
    <div class="feat" style="margin-top:24px">
      <div class="f"><h4><span class="ico">1</span> Where we are vs. the peak</h4><p>The all-time peak was the end of 2022, when money was nearly free and deals traded at 4% cap rates. The market corrected 15&ndash;25% depending on submarket. West Hollywood, as an A-location, sits at the lower end of that correction &mdash; closer to 15%.</p></div>
      <div class="f"><h4><span class="ico">2</span> The recovery is real</h4><p>2024 and the first half of 2025 were genuinely tough. Since then the market has recovered meaningfully. We are not just listing deals &mdash; we are opening escrows and closing them. Right now we have 11 deals in escrow and 15 closed this year.</p></div>
      <div class="f"><h4><span class="ico">3</span> What to expect ahead</h4><p>We expect status quo for the foreseeable future. There are no signs from our boots on the ground, or from Marcus &amp; Millichap's national research, of a major move up or down. We do not have a crystal ball, and we will not pretend to.</p></div>
      <div class="f"><h4><span class="ico">4</span> It is a per-deal market</h4><p>It is more of a buyer's market than 2022, but it almost feels like a fair fight. Whether you are in the driver's seat comes down to execution: price it right, expose it fully, and get multiple offers on the table at the same time. That is what we control.</p></div>
    </div>
  </div>
</section>

<!-- MARKETING -->
<section id="marketing" class="alt">
  <div class="wrap">
    <div class="eyebrow">The Marketing Machine</div>
    <h2 style="font-size:32px;max-width:820px">How we put 613 Westbourne in front of every qualified buyer &mdash; at the same time</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">Generating real demand is not luck. It is a system we have built and run across 460+ closings. The goal is simple: create an auction-like atmosphere by getting multiple qualified buyers to the table simultaneously.</p>

    <div class="feat" style="margin-top:26px">
      <div class="f"><h4><span class="ico">&#9742;</span> The right people, by name</h4><p>The most probable buyer owns a similar building nearby. We have the first name, last name, cell phone, and email &mdash; confirmed &mdash; for essentially every apartment owner in West Hollywood, with roughly 95% accuracy. A full-time analyst keeps the database current on every LA County apartment sale.</p></div>
      <div class="f"><h4><span class="ico">&#128231;</span> A database that converts</h4><p>10,000+ principals and 15,000+ brokers. Every 1031 buyer we uncover goes onto a tracked exchange list. With 26 active listings, we are in constant contact with today's most active buyers &mdash; not the buyers of two years ago.</p></div>
      <div class="f"><h4><span class="ico">&#127758;</span> The M&amp;M platform</h4><p>Marcus &amp; Millichap dominates the $1&ndash;25M private-capital market with offices in every state and Canada, plus international reach. For an A-location like WeHo, that national and international exposure matters.</p></div>
      <div class="f"><h4><span class="ico">&#129309;</span> We share the deal</h4><p>We actively co-broke. We pursue outside brokers rather than hoard the listing, because the goal is finding every needle in the haystack &mdash; including the buyer from out of market we would never reach alone.</p></div>
    </div>

    <h3 style="font-size:20px;margin-top:40px">Launch sequence &mdash; live within 7 days</h3>
    <ul class="clean" style="max-width:840px">
      <li><strong>Within 7 calendar days</strong> of signing, we are 100% live online. The only thing that adds time is professional photography, which adds about three days.</li>
      <li><strong>Full offering memorandum</strong> drafted and sent to you for review and edits. We launch only once you approve it.</li>
      <li><strong>Simultaneous blast</strong> &mdash; emails, every major online platform, and physical postcards to mailboxes all hit at the same time to maximize same-time offers.</li>
      <li><strong>Due-diligence folder prepared up front</strong> so a buyer can move fast and cannot manufacture reasons to retrade.</li>
    </ul>
  </div>
</section>

<!-- PROCESS / PRICING / TIMELINE -->
<section id="process">
  <div class="wrap">
    <div class="eyebrow">Pricing Strategy &amp; Execution</div>
    <h2 style="font-size:32px;max-width:820px">Priced right, exposed fully, and built to close on your timeline</h2>

    <div class="twocol" style="margin-top:26px">
      <div>
        <h3 style="font-size:19px">How we price &mdash; and why no number is on this page</h3>
        <p>This is an investment sale, not a home sale. There is no emotional bidding war that drives a home 10% over asking. The buyer is solving for return &mdash; price per unit, price per square foot, cap rate, GRM, and cash-on-cash at today's low-6% interest rates. We value your building against the right comps: rent-controlled, pre-October 1978, 5&ndash;15 units, and the most recent sales possible, because the market has moved.</p>
        <p>Our recommendation is to establish the number we are confident it will sell at, then list 3&ndash;5% above that to create room for negotiation. Where exactly to list is a strategy conversation for you, your father, and us &mdash; which is why we are bringing the analysis to that call rather than printing a headline here.</p>
        <h3 style="font-size:19px;margin-top:24px">Vetting the buyer</h3>
        <p>Terms matter as much as price in a 1031. We ask every buyer a simple question &mdash; why do you want to buy it? &mdash; and we almost always know the buyer or broker and their reputation. You will get our honest read on whether they will actually close.</p>
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
        <div class="callout" style="margin-top:18px">
          <div class="eyebrow">Built for your timeline</div>
          <h3 style="font-size:19px">List now, close before August</h3>
          <p>Live next week, offers in the first two to three weeks, escrow opened by week four, and a 45&ndash;60 day escrow. That path closes well ahead of the late-summer slowdown you want to avoid.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- 1031 -->
<section id="exchange" class="alt">
  <div class="wrap">
    <div class="eyebrow">1031 Exchange Expertise</div>
    <h2 style="font-size:32px;max-width:820px">The exchange is not a complication for us &mdash; it is our core business</h2>
    <p class="lead" style="margin-top:14px;max-width:840px">The vast majority of our deals involve a 1031 exchange on the buy side, the sell side, or both. We have navigated well over 100 of them, and every one is documented as a case study on LAAA.com.</p>
    <div class="feat" style="margin-top:24px">
      <div class="f"><h4><span class="ico">&#8644;</span> Selling into your San Francisco purchase</h4><p>Exchanging from Westbourne into a Bay Area home is fully doable &mdash; the replacement simply has to be held for investment. We will make sure your timeline and documentation line up so the exchange holds.</p></div>
      <div class="f"><h4><span class="ico">&#9201;</span> The reverse-exchange option</h4><p>If you find the new property first, a reverse exchange lets you acquire before you sell. It is only nominally more expensive &mdash; often just a few thousand dollars that blend into closing costs &mdash; and it removes the pressure of a fire sale. A real option worth keeping open.</p></div>
      <div class="f"><h4><span class="ico">&#128221;</span> Get the structure right</h4><p>Renting the replacement home to family can work, but the details matter. We will point you to the right 1031 accommodator and counsel so it is structured cleanly from day one. (We coordinate the real estate; your tax and legal advisors confirm the structure.)</p></div>
      <div class="f"><h4><span class="ico">&#9989;</span> Terms that protect the exchange</h4><p>We structure timelines, deposits, and contingencies specifically to protect your exchange windows &mdash; something a residential agent simply is not set up to do.</p></div>
    </div>
  </div>
</section>

<!-- REFERENCES / NEXT STEPS -->
<section id="next">
  <div class="wrap">
    <div class="eyebrow">References &amp; Next Steps</div>
    <h2 style="font-size:30px;max-width:820px">Call our clients. Then let's price it together.</h2>
    <div class="twocol" style="margin-top:22px">
      <div>
        <p>You said broker competence is what matters most &mdash; we agree, and we welcome the scrutiny. We are happy to connect you with current and recently-closed clients, including sellers who just completed their own 1031 exchanges, so you can ask the questions that matter: is this team trustworthy, are they good at the job, and what is it like working with them day to day.</p>
        <ul class="clean">
          <li>Direct references from active and recently-closed clients, on request.</li>
          <li>A full pricing analysis and listing strategy, turned around fast &mdash; ready for a follow-up call with you and your father early to mid next week.</li>
          <li>Sample offering memoranda so you can see exactly what your marketing package will look like.</li>
        </ul>
      </div>
      <div class="callout">
        <div class="eyebrow">One housekeeping item</div>
        <h3 style="font-size:19px">Clear the title before you sell</h3>
        <p>Public records currently show an erroneous conveyance against the property (a January 2025 recording to an unrelated party that does not reflect your ownership). It is almost certainly a clerical recording error, but it must be cleaned up before a sale. Our title partner can investigate and resolve it &mdash; we have already flagged it.</p>
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
      This Broker Opinion of Value and marketing proposal has been prepared exclusively for Ian Lee and the Lee family for the purpose of evaluating brokerage representation for 613 Westbourne Drive, West Hollywood, CA 90069. It is confidential and is not an appraisal. Track-record figures reflect the career production of the LAAA Team. Statements regarding market conditions represent the opinion of the LAAA Team and are not guarantees of future results. The LAAA Team does not provide tax or legal advice; consult your own 1031 accommodator, accountant, and attorney regarding exchange structure. &copy; 2026 The LAAA Team at Marcus &amp; Millichap.
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
  var CITY_COLORS = {
    'West Hollywood':'#C5A258',
    'WeHo Corridor (Fairfax/Melrose)':'#1B3A5C',
    'Beverly Hills':'#2e6b8f',
    'Santa Monica':'#3d8168',
    'Westwood / Brentwood / West LA':'#7a5ea0'
  };
  var resumeMap, subjectMap, resumeMarkers=[], info;

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
      mk.addListener('click',function(){
        info.setContent('<div style="font-family:Inter,sans-serif;padding:2px 4px"><strong style="color:#1B3A5C">'+m.a+'</strong><br><span style="color:#5b6470;font-size:13px">'+m.city+' &middot; '+(m.u||'&ndash;')+' units &middot; closed '+m.y+'</span></div>');
        info.open(resumeMap, mk);
      });
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
    subjMk.addListener('click',function(){
      info.setContent('<div style="font-family:Inter,sans-serif;padding:2px 4px"><strong style="color:#1B3A5C">613 Westbourne Drive</strong><br><span style="color:#5b6470;font-size:13px">West Hollywood, CA 90069 &middot; 8 units</span></div>');
      info.open(subjectMap, subjMk);
    });
    // nearby LAAA closings (WeHo + corridor) on the subject map
    MARKERS.filter(function(m){ return m.city.indexOf('Hollywood')>-1 || m.city.indexOf('WeHo')>-1; }).forEach(function(m){
      var mk=new google.maps.Marker({ position:{lat:m.lat,lng:m.lng}, map:subjectMap, icon:pin('#1B3A5C'), title:m.a });
      mk.addListener('click',function(){
        info.setContent('<div style="font-family:Inter,sans-serif;padding:2px 4px"><strong style="color:#1B3A5C">'+m.a+'</strong><br><span style="color:#5b6470;font-size:13px">LAAA closing &middot; '+(m.u||'&ndash;')+' units &middot; '+m.y+'</span></div>');
        info.open(subjectMap, mk);
      });
    });

    // Offscreen-init guard: Google Maps can paint gray until the container
    // gets a resize once it scrolls into view. Trigger resize + recenter on reveal.
    setupResizeGuard(resumeMap, document.getElementById('resumeMap'), function(){
      var b=new google.maps.LatLngBounds();
      resumeMarkers.forEach(function(mk){ if(mk.getVisible()) b.extend(mk.getPosition()); });
      if(!b.isEmpty()){ resumeMap.fitBounds(b); } else { resumeMap.setCenter({lat:34.05,lng:-118.41}); }
    });
    setupResizeGuard(subjectMap, document.getElementById('subjectMap'), function(){
      subjectMap.setCenter({lat:SUBJECT.lat,lng:SUBJECT.lng});
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

from collections import Counter
cnt = Counter(m["city"] for m in MARKERS); un = Counter()
for m in MARKERS: un[m["city"]] += (m.get("u") or 0)
weho_b, weho_u = cnt["West Hollywood"], un["West Hollywood"]
corr_b, corr_u = cnt["WeHo Corridor (Fairfax/Melrose)"], un["WeHo Corridor (Fairfax/Melrose)"]
bh_b, bh_u = cnt["Beverly Hills"], un["Beverly Hills"]
sm_b, sm_u = cnt["Santa Monica"], un["Santa Monica"]
wla_b, wla_u = cnt["Westwood / Brentwood / West LA"], un["Westwood / Brentwood / West LA"]
# A-level westside = WeHo + corridor + BH + SM
al_b = weho_b + corr_b + bh_b + sm_b
al_u = weho_u + corr_u + bh_u + sm_u

repl = {
  "__SUBJECT_JSON__": json.dumps(SUBJ),
  "__MARKERS_JSON__": json.dumps(MARKERS),
  "__MAPS_KEY__": MAPS_KEY,
  "__WEHO_B__": str(weho_b), "__WEHO_U__": str(weho_u),
  "__CORR_B__": str(corr_b), "__CORR_U__": str(corr_u),
  "__BH_B__": str(bh_b), "__BH_U__": str(bh_u),
  "__SM_B__": str(sm_b), "__SM_U__": str(sm_u),
  "__WLA_B__": str(wla_b), "__WLA_U__": str(wla_u),
  "__AL_B__": str(al_b), "__AL_U__": str(al_u),
}
out = HTML
for k, v in repl.items():
    out = out.replace(k, v)

open(r"C:\Users\gscher\613-westbourne-bov\index.html", "w", encoding="utf-8").write(out)
print("WROTE index.html", len(out), "chars")
print(f"WeHo {weho_b}/{weho_u}  Corr {corr_b}/{corr_u}  BH {bh_b}/{bh_u}  SM {sm_b}/{sm_u}  WLA {wla_b}/{wla_u}  ALevel {al_b}/{al_u}")
