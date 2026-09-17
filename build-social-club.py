#!/usr/bin/env python3
"""/events/social-club — The Grassy Issue Social Club sign-up, 17 September 2026.

WHAT IT IS. Small groups playing good courses in and around Austin. An interest
list, not a ticketed event: names come in, groups get built, dates get set.

BUILT ON THE LONG WALK CHASSIS, as asked. Same structure in the same order:
poster-hero (poster left, copy + stats right), event-details with event-body and
event-sidebar, a format-strip of badges, the interest-section form, back-section.
Every class used here already exists in that page's stylesheet, so nothing new
needs styling and nothing renders unstyled.

THE FORM ENDPOINT IS LIVE as of 17 Sept 2026. Lenny deployed a separate Apps
Script and sheet so Social Club names do not mix with Long Walk names, and
pasted the /exec URL in below. It is NOT the Long Walk deployment — the guard in
this file checks that, because pointing both forms at one script would silently
merge two interest lists and nobody would notice until the first outing.

The submit handler keeps its unset-endpoint branch. It is dead code while the
URL is set, and it is the thing that stops a future rebuild-with-placeholder from
showing people a success panel while posting into the void. Leave it in.
Setup steps and the Apps Script itself: social-club-sheets-setup.md.

THE FORM FIELDS differ from The Long Walk's on purpose. The Long Walk is one
event on one date, so it asks name/email/handicap. The Social Club is recurring
and group-based, so it asks name, email, how far you will drive, and whether you
walk or ride — the two things that actually decide which group someone fits in.

"WORTH THE DRIVE". The poster carries that line and TGI's own rule bans the word
in copy. The poster is artwork and ships as-is; the page's own prose does not use
it, and the guard at the bottom enforces that on the HTML text.

NOT ASSERTED: no dates, no course commitments, no fees, no group sizes presented
as decided. The courses named under "Where we are looking" are described as
candidates, and all of them are places the site has already covered.
"""
import re, os, sys, json, html as H

apply_ = "--apply" in sys.argv
SRC = "events/the-long-walk.html"
OUT = "events/social-club.html"
URL = "/events/social-club"
PLAIN = "The Grassy Issue Social Club — Small Groups, Good Courses"
DESC = ("An interest list for The Grassy Issue Social Club: small groups playing good courses in and "
        "around Austin. Tell us how far you'll drive and whether you walk or ride.")
POSTER = "/images/social-club-poster.jpg"

# Live endpoint, deployed by Lenny 17 Sept 2026. Its own sheet, not the Long Walk's.
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyx5uBp5eQpGGhqRSfG7V2zUjFQEh3adgHLUIQFT-_ldfcqHmlQfnv8sCSBQ03eCjlr/exec"

BODY = f"""
<div class="breadcrumb"><a href="/">Feed</a><span>/</span><a href="/events/">Events</a><span>/</span>Social Club</div>

<header class="poster-hero">
  <div class="poster-hero-inner">
    <div class="poster-image-wrap">
      <img src="{POSTER}" alt="The Grassy Issue Social Club poster — a green over a wide Hill Country horizon, with the words Good golf, Good people" />
    </div>
    <div class="poster-content">
      <span class="event-tag">TGI Event</span>
      <h1>The Grassy Issue<br/>Social Club</h1>
      <p class="poster-sub">Small groups playing good courses in and around Austin. Not a tournament, not a league &mdash; a handful of people, a tee sheet, and somewhere you have probably been meaning to play.</p>
      <div class="poster-stats">
        <div class="poster-stat">
          <div class="poster-stat-value">8&ndash;12</div>
          <div class="poster-stat-label">Per Outing</div>
        </div>
        <div class="poster-stat">
          <div class="poster-stat-value">90</div>
          <div class="poster-stat-label">Minutes Out</div>
        </div>
        <div class="poster-stat">
          <div class="poster-stat-value">0</div>
          <div class="poster-stat-label">Dues</div>
        </div>
      </div>
    </div>
  </div>
</header>

<section class="event-details">
  <div class="event-grid">
    <div class="event-body">
      <h2>Good golf. Good people.</h2>
      <p>Austin has more golf inside ninety minutes of it than most people get around to playing. Some of it is municipal and five miles from downtown. Some of it is an hour into the Hill Country on a road you would not otherwise drive. The problem is almost never the golf &mdash; it is finding three other people free on the same Saturday who also want to go.</p>

      <p>The Social Club exists to solve that specific problem. We put together a small group, book a tee sheet somewhere good, and send round the details. You show up. That is the whole mechanism.</p>

      <div class="format-strip">
        <span class="format-badge">Small Groups</span>
        <span class="format-badge">In &amp; Around Austin</span>
        <span class="format-badge">Walkers Welcome</span>
        <span class="format-badge">No Dues</span>
      </div>

      <h2>How it works.</h2>
      <p>You join the interest list below. When an outing comes together we email the people it fits &mdash; matched on how far you said you would drive and whether you walk or ride, because those two answers decide more about a good group than a handicap does.</p>

      <p>Groups run eight to twelve people, which is two or three tee times. Small enough that you will actually meet everyone, big enough that a couple of drop-outs do not kill it. Everyone pays their own green fee direct to the course. There are no dues, no membership, and no obligation to come to any given one.</p>

      <h2>Where we are looking.</h2>
      <p>Nothing is booked yet, so treat this as the shape of it rather than a schedule. Close in, the Austin municipal courses do most of the work &mdash; <a href="/drops/lions-municipal-golf-course-austin">Lions</a>, <a href="/drops/hancock-golf-course-austin">Hancock</a>, Morris Williams, Jimmy Clay and Roy Kizer. They are cheap, they are walkable, and they are the reason this city&rsquo;s golf culture looks the way it does.</p>

      <p>Further out is where the drive starts to earn itself: Grey Rock in the south, Falconhead and Avery Ranch to the north and west, Star Ranch out toward Hutto, Wolfdancer at Lost Pines, Kissing Tree down in San Marcos, Vaaler Creek in Blanco. Ninety minutes is roughly the limit &mdash; far enough for the landscape to change, close enough to be home for dinner.</p>

      <h2>Who it is for.</h2>
      <p>Anyone who plays. There is no handicap requirement and no vetting, because a group sorted by ability is a competition and this is not one. If you are new to Austin, new to golf, or just tired of texting the same two people, this is aimed squarely at you.</p>

      <p>The one thing we do ask is that you turn up when you say you will. A small group only works if the people in it show.</p>

      <p>Drop your details below and we will be in touch when the first one takes shape.</p>
    </div>

    <aside class="event-sidebar">
      <div class="sidebar-label">The Details</div>

      <div class="sidebar-item">
        <div class="sidebar-item-label">Status</div>
        <div class="sidebar-item-value">Building the list</div>
      </div>

      <div class="sidebar-item">
        <div class="sidebar-item-label">Group size</div>
        <div class="sidebar-item-value">8&ndash;12 players<br/>(2&ndash;3 tee times)</div>
      </div>

      <div class="sidebar-item">
        <div class="sidebar-item-label">Range</div>
        <div class="sidebar-item-value">Austin and roughly<br/>90 minutes around it</div>
      </div>

      <div class="sidebar-item">
        <div class="sidebar-item-label">Cost</div>
        <div class="sidebar-item-value">Your own green fee<br/>No dues, no membership</div>
      </div>

      <div class="sidebar-item">
        <div class="sidebar-item-label">Carts</div>
        <div class="sidebar-item-value">Walk or ride<br/>Both are fine</div>
      </div>

      <div class="sidebar-item">
        <div class="sidebar-item-label">Presented by</div>
        <div class="sidebar-item-value">The Grassy Issue</div>
      </div>

      <a href="#interest" class="sidebar-cta" style="display:block; text-align:center; padding:14px 24px; background:var(--ink); color:var(--paper); font-family:var(--mono); font-size:11px; letter-spacing:0.14em; text-transform:uppercase; margin-top:28px; transition:background 0.2s;">Join The List &darr;</a>
    </aside>
  </div>
</section>

<section class="interest-section" id="interest">
  <div class="interest-box">
    <div class="interest-left">
      <h2>Join the interest list.</h2>
      <p>Name, email, and two questions that help us put you in the right group. No spam, no newsletter by stealth &mdash; you will hear from us when there is an outing that fits.</p>
    </div>
    <div class="interest-right">
      <form class="interest-form" id="interestForm">
        <div class="form-field">
          <label for="name">Name</label>
          <input type="text" id="name" name="name" placeholder="Ben Crenshaw" required />
        </div>
        <div class="form-field">
          <label for="email">Email</label>
          <input type="email" id="email" name="email" placeholder="you@example.com" required />
        </div>
        <div class="form-field">
          <label for="range">How far will you drive?</label>
          <select id="range" name="range">
            <option value="">Optional</option>
            <option value="austin-only">Austin city limits</option>
            <option value="45">Up to 45 minutes</option>
            <option value="90">Up to 90 minutes</option>
            <option value="anywhere">Anywhere, I like a road trip</option>
          </select>
        </div>
        <div class="form-field">
          <label for="mode">Walk or ride?</label>
          <select id="mode" name="mode">
            <option value="">Optional</option>
            <option value="walk">Walker, always</option>
            <option value="ride">Rider, always</option>
            <option value="either">Either is fine</option>
          </select>
        </div>
        <button type="submit" class="form-submit">Join The List</button>
        <div class="form-note">We&rsquo;ll only email you about Social Club outings.</div>
      </form>
      <div class="form-success" id="formSuccess">
        <h3>You&rsquo;re on the list.</h3>
        <p>We&rsquo;ll be in touch when an outing comes together that fits how you play.</p>
      </div>
    </div>
  </div>
</section>

<div class="back-section">
  <a href="/events/" class="back-link">&larr; All events</a>
</div>
"""

SCRIPT = f"""
<script>
  // ============================================================
  // GOOGLE SHEETS INTEGRATION — SOCIAL CLUB
  // This is its OWN Apps Script and sheet, separate from The Long
  // Walk, so the two interest lists do not mix.
  // Setup steps: social-club-sheets-setup.md
  // ============================================================
  var GOOGLE_SCRIPT_URL = '{SCRIPT_URL}';

  var form = document.getElementById('interestForm');
  var success = document.getElementById('formSuccess');
  var note = form.querySelector('.form-note');

  form.addEventListener('submit', function(e) {{
    e.preventDefault();
    var btn = form.querySelector('.form-submit');

    // FAIL LOUDLY, NOT SILENTLY. Until the endpoint is pasted in, a submit
    // would POST into the void and still show the success panel — the reader
    // would think they had signed up. Say so instead.
    if (GOOGLE_SCRIPT_URL.indexOf('PASTE_YOUR') === 0) {{
      note.textContent = 'Sign-ups open shortly — the list is not live yet. Email L4harrington@gmail.com to be added now.';
      note.style.opacity = '1';
      return;
    }}

    btn.disabled = true;
    btn.textContent = 'Sending…';

    var data = {{
      name: form.name.value,
      email: form.email.value,
      range: form.range.value,
      mode: form.mode.value,
      source: 'social-club',
      timestamp: new Date().toISOString()
    }};

    fetch(GOOGLE_SCRIPT_URL, {{
      method: 'POST',
      mode: 'no-cors',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(data)
    }}).then(function() {{
      form.style.display = 'none';
      success.classList.add('show');
    }}).catch(function() {{
      btn.disabled = false;
      btn.textContent = 'Try Again';
    }});
  }});
</script>
"""

SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Event",
    "name": "The Grassy Issue Social Club",
    "description": DESC,
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "url": "https://thegrassyissue.com" + URL,
    "image": "https://thegrassyissue.com" + POSTER,
    "location": {"@type": "Place", "name": "Courses in and around Austin, Texas",
                 "address": {"@type": "PostalAddress", "addressLocality": "Austin",
                             "addressRegion": "TX", "addressCountry": "US"}},
    "organizer": {"@type": "Organization", "name": "The Grassy Issue",
                  "url": "https://thegrassyissue.com"},
}

# ------------------------------------------------------------------ chassis
t = open(SRC, encoding="utf-8").read()
head = t[:t.find("</head>")]
# The Long Walk keeps its footer, search JS, mobile drawer AND both analytics
# tags in the BODY above </body> — the same trap that bit build-work-with-us.py.
# Slice the tail from <footer, not from </body>.
_f = t.find("<footer", t.find('class="back-section"'))
if _f == -1:
    raise SystemExit("could not find the footer in the chassis")
tail = t[_f:]
# drop the chassis's own Long Walk form script out of the tail
tail = re.sub(r"<script>\s*//\s*=+\s*//\s*GOOGLE SHEETS INTEGRATION.*?</script>", "", tail, flags=re.S)
nav = re.search(r'<nav class="nav".*?</nav>', t, re.S).group(0)

head = re.sub(r"<title>[^<]*</title>", f"<title>{PLAIN} — The Grassy Issue</title>", head)
for k, attr in [("description", "name"), ("og:title", "property"), ("og:description", "property"),
                ("twitter:title", "name"), ("twitter:description", "name")]:
    v = PLAIN if k.endswith("title") else DESC
    head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                  lambda m, _v=v: m.group(1) + _v + m.group(2), head)
head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
              lambda m: m.group(1) + "https://thegrassyissue.com" + URL + m.group(2), head)
head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
              lambda m: m.group(1) + "https://thegrassyissue.com" + URL + m.group(2), head)
for k, attr in [("og:image", "property"), ("twitter:image", "name")]:
    head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + "https://thegrassyissue.com" + POSTER + m.group(2), head)
# lambda, not a literal: json.dumps emits \u and \" that re.sub reads as escapes
_ld = '<script type="application/ld+json">' + json.dumps(SCHEMA) + "</script>"
if "application/ld+json" in head:
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _m: _ld, head, flags=re.S)
else:
    head += "\n" + _ld

out = head + "</head>\n<body>\n" + nav + "\n" + BODY + "\n" + tail.replace("</body>", SCRIPT + "\n</body>")

# ------------------------------------------------------------------- guards
plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", H.unescape(
    re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", out, flags=re.S))))
words = len(re.findall(r"[A-Za-z0-9']+", plain))
problems = []
if re.search(r"\bworth\b", plain, re.I):
    problems.append("banned word 'worth' in the page text")
if words < 500:
    problems.append(f"only {words} words")
if out.count("<h1") != 1:
    problems.append(f"{out.count('<h1')} h1 tags")
for tag in ("<div", "<section", "<a "):
    if out.count(tag) != out.count(tag.replace("<", "</").strip() + ">"):
        problems.append(f"unbalanced {tag.strip()}")
if "G-G89M4116SB" not in out:
    problems.append("GA4 tag did not come across from the chassis")
if "goatcounter" not in out.lower():
    problems.append("GoatCounter tag did not come across")
if 'id="tgi-search-input"' not in out:
    problems.append("search box missing")
if not os.path.exists(POSTER.lstrip("/")):
    problems.append("poster image missing on disk")
if out.count("GOOGLE_SCRIPT_URL") < 2:
    problems.append("the form script did not land")
if out.count("interestForm") != 2:
    problems.append("form id count wrong — the chassis script may have survived")
_LONGWALK = "AKfycbyYo9NOfhXF-jOdrrD0GzYSiEGLJ66_Srn0cYOlt22b1bTwiT7UmqALaSdyfMXAXw4R"
if _LONGWALK in out:
    problems.append("this page points at the LONG WALK Apps Script — the two lists would merge")
if "script.google.com/macros/s/" not in out:
    problems.append("no Apps Script endpoint in the page")
if "/exec'" not in out and '/exec"' not in out:
    problems.append("endpoint is not a /exec URL — /dev only works while signed in as the owner")
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', out, re.S):
    json.loads(b)
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(OUT, "w", encoding="utf-8").write(out)

print(("wrote" if apply_ else "DRY RUN") + f" {URL}  ({words} words)")
print("  · built on the Long Walk chassis — poster hero, body + sidebar, format strip, interest form")
print("  · form posts to the live Social Club Apps Script (its own sheet, not the Long Walk's)")
print("  · GA4 + GoatCounter + search inherited; Event schema written")
if not apply_:
    print("\npass --apply to write")
