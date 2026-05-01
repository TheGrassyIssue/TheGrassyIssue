  // --- Activate feed filter from nav/footer links ---
  function activateFilter(type) {
    const pill = document.querySelector(`.pill[data-filter="${type}"]`);
    if (pill) {
      pill.click();
      setTimeout(() => {
        document.getElementById('feed').scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  }

  // --- Score form ---
  function handleUpload(input) {
    const zone = document.getElementById('uploadZone');
    const nameEl = document.getElementById('uploadFilename');
    if (input.files && input.files[0]) {
      zone.classList.add('has-file');
      nameEl.textContent = '✓ ' + input.files[0].name;
    }
  }

  // --- Google Sheets API URL (replace after deploying Apps Script) ---
  const SHEET_API = 'https://script.google.com/macros/s/AKfycbwELhdJhSk-iZxSVxIAiiW8FaEYwxmJWRBs7yODJOKf-Q2IJ0Tqm-AlPssTUoMZ4FfR/exec';

  function submitScore(e) {
    e.preventDefault();
    const btn = document.getElementById('scoreSubmitBtn');
    const form = document.getElementById('scoreForm');

    // Honeypot check
    if (form.querySelector('[name="_honey"]').value) return false;

    btn.textContent = 'Posting…';
    btn.disabled = true;

    const payload = {
      course: document.getElementById('scoreCourse').value,
      score: document.getElementById('scoreTotal').value,
      displayName: document.getElementById('scoreName').value,
      email: document.getElementById('scoreEmail').value,
      photoURL: ''
    };

    fetch(SHEET_API, {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: { 'Content-Type': 'text/plain' } // text/plain avoids CORS preflight
    }).then(r => r.json()).then(data => {
      btn.textContent = '✓ Score Posted';
      btn.classList.add('submitted');
      // Refresh the leaderboard
      loadLeaderboard();
      setTimeout(() => {
        form.reset();
        document.getElementById('uploadZone').classList.remove('has-file');
        document.getElementById('uploadFilename').textContent = '';
        btn.textContent = 'Post My Score →';
        btn.classList.remove('submitted');
        btn.disabled = false;
      }, 3000);
    }).catch(() => {
      btn.textContent = 'Error — try again';
      setTimeout(() => {
        btn.textContent = 'Post My Score →';
        btn.disabled = false;
      }, 3000);
    });
    return false;
  }
  document.getElementById('scoreForm').addEventListener('submit', submitScore);

  // --- Live Leaderboard ---
  let leaderboardData = null;
  let activeCourse = null;

  function loadLeaderboard() {
    if (SHEET_API === 'YOUR_APPS_SCRIPT_URL_HERE') {
      // Show placeholder data until Apps Script is deployed
      renderPlaceholderLeaderboard();
      return;
    }
    fetch(SHEET_API)
      .then(r => r.json())
      .then(data => {
        if (data.result === 'success') {
          leaderboardData = data;
          renderCourseTabs(data.leaderboard);
          const courses = Object.keys(data.leaderboard);
          if (courses.length > 0) {
            activeCourse = activeCourse && courses.includes(activeCourse) ? activeCourse : courses[0];
            renderLeaderboardScores(data.leaderboard[activeCourse], activeCourse);
            updateLeaderboardCta(activeCourse, data.week);
          } else {
            renderEmptyLeaderboard();
          }
        }
      })
      .catch(() => renderPlaceholderLeaderboard());
  }

  function renderCourseTabs(leaderboard) {
    const container = document.getElementById('courseTabsStrip');
    const courses = Object.keys(leaderboard);
    if (courses.length <= 1) { container.innerHTML = ''; return; }
    container.innerHTML = courses.map(course => {
      const shortName = course.replace(' Municipal', '').replace(' Pitch & Putt', ' P&P').replace(' Par 3', ' P3');
      return '<button class="scoreboard-course-tab' + (course === activeCourse ? ' active' : '') +
        '" data-course="' + course + '">' + shortName + '</button>';
    }).join('');
    container.querySelectorAll('.scoreboard-course-tab').forEach(tab => {
      tab.addEventListener('click', function() {
        activeCourse = this.dataset.course;
        container.querySelectorAll('.scoreboard-course-tab').forEach(t => t.classList.remove('active'));
        this.classList.add('active');
        renderLeaderboardScores(leaderboardData.leaderboard[activeCourse], activeCourse);
        updateLeaderboardCta(activeCourse, leaderboardData.week);
      });
    });
  }

  function renderLeaderboardScores(scores, course) {
    const container = document.getElementById('leaderboardScores');
    if (!scores || scores.length === 0) {
      container.innerHTML = '<span class="scoreboard-loading">No scores yet this week — be the first.</span>';
      return;
    }
    container.innerHTML = scores.slice(0, 7).map((s, i) =>
      '<div class="strip-score">' +
        '<span class="strip-pos">' + (i + 1) + '.</span> ' +
        '<span class="strip-name">' + escapeHtml(s.name) + '</span> ' +
        '<span class="strip-num">' + s.score + '</span>' +
      '</div>'
    ).join('');
  }

  function updateLeaderboardCta(course, week) {
    const cta = document.getElementById('leaderboardCta');
    const shortName = course.replace(' Municipal', '').replace(' Pitch & Putt', ' P&P');
    cta.textContent = shortName + ' · Week ' + week + ' →';
    cta.href = 'scoreboard.html';
  }

  function renderEmptyLeaderboard() {
    document.getElementById('leaderboardScores').innerHTML =
      '<span class="scoreboard-loading">No scores yet this week — be the first.</span>';
    document.getElementById('leaderboardCta').textContent = 'Full scoreboard →';
  }

  function renderPlaceholderLeaderboard() {
    // Fallback while API isn't connected
    const scores = [
      { name: 'slicefixer_atx', score: 74 },
      { name: 'bunkered_and_proud', score: 78 },
      { name: 'westlake_wanda', score: 81 },
      { name: 'tee_totaler', score: 83 },
      { name: 'rough_rider_78704', score: 84 },
      { name: 'dawn_patrol_dan', score: 85 },
      { name: 'hacker_mcgee', score: 87 }
    ];
    const container = document.getElementById('leaderboardScores');
    container.innerHTML = scores.map((s, i) =>
      '<div class="strip-score">' +
        '<span class="strip-pos">' + (i + 1) + '.</span> ' +
        '<span class="strip-name">' + s.name + '</span> ' +
        '<span class="strip-num">' + s.score + '</span>' +
      '</div>'
    ).join('');
    document.getElementById('leaderboardCta').textContent = 'Full scoreboard →';
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // Load leaderboard on page ready
  loadLeaderboard();

  // --- Vote bar ---
  function castVote(btn, type, evt) {
    if (evt) { evt.preventDefault(); evt.stopPropagation(); }
    const bar = btn.closest('.vote-bar');
    if (bar.classList.contains('has-voted')) return;

    const fill = bar.querySelector('.vote-bar-fill');
    const countEl = bar.querySelector('.vote-bar-count');
    const btns = bar.querySelectorAll('.vote-btn');
    const midLabel = bar.querySelector('.vote-bar-label .mid');
    const fireLabel = bar.querySelector('.vote-bar-label .fire');

    // Parse current state from the fill width and vote count
    let totalVotes = parseInt(countEl.textContent) || 100;
    let firePct = parseFloat(fill.style.width) || 50;
    let fireVotes = Math.round(totalVotes * firePct / 100);
    let midVotes = totalVotes - fireVotes;

    // Add the new vote
    if (type === 'fire') {
      fireVotes++;
    } else {
      midVotes++;
    }
    totalVotes++;

    // Calculate new percentage
    let newFirePct = Math.round((fireVotes / totalVotes) * 100);
    let newMidPct = 100 - newFirePct;

    // Animate the bar
    fill.style.width = newFirePct + '%';

    // Update count
    countEl.textContent = totalVotes + ' votes';

    // Show percentages in labels
    midLabel.innerHTML = 'Mid <span class="pct">' + newMidPct + '%</span>';
    fireLabel.innerHTML = '<span class="pct">' + newFirePct + '%</span> Fire';

    // Mark voted state
    bar.classList.add('has-voted');
    btns.forEach(b => b.classList.add('voted'));
    btn.classList.add('chosen');

    // Store vote locally for weekly digest
    const card = bar.closest('.card');
    const productName = card ? (card.querySelector('.card-title')?.textContent || 'Unknown') : 'Unknown';
    try {
      const votes = JSON.parse(localStorage.getItem('tgi_votes') || '[]');
      votes.push({
        product: productName,
        vote: type,
        firePct: newFirePct,
        midPct: newMidPct,
        total: totalVotes,
        time: new Date().toISOString()
      });
      localStorage.setItem('tgi_votes', JSON.stringify(votes));
    } catch(e) {}
  }

  // --- Mobile menu ---
  function toggleMenu() {
    const btn = document.querySelector('.nav-toggle');
    const drawer = document.getElementById('navDrawer');
    const isOpen = btn.classList.toggle('open');
    drawer.classList.toggle('open', isOpen);
    btn.setAttribute('aria-expanded', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
  }
  function closeMenu() {
    const btn = document.querySelector('.nav-toggle');
    const drawer = document.getElementById('navDrawer');
    btn.classList.remove('open');
    drawer.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  // --- Filter pills (proper reflow for masonry) ---
  const pills = document.querySelectorAll('.pill');
  const cards = document.querySelectorAll('.card');
  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => {
        p.classList.remove('active');
        p.setAttribute('aria-selected', 'false');
      });
      pill.classList.add('active');
      pill.setAttribute('aria-selected', 'true');
      const filter = pill.dataset.filter;
      cardsShown = CARDS_PER_PAGE; // reset pagination on filter change
      cards.forEach(card => {
        if (filter === 'all' || card.dataset.type === filter) {
          card.classList.remove('hidden');
          card.style.display = '';
        } else {
          card.classList.add('hidden');
          card.style.display = 'none';
        }
      });
      // Re-layout masonry and re-trigger entrance animation
      requestAnimationFrame(() => {
        layoutMasonry();
        document.querySelectorAll('.card:not(.hidden)').forEach((c, i) => {
          c.classList.remove('visible');
          setTimeout(() => c.classList.add('visible'), i * 60);
        });
      });
    });
  });

  // --- Masonry layout (left-to-right, then down, with tight vertical packing) ---
  const CARDS_PER_PAGE = 18;
  let cardsShown = CARDS_PER_PAGE;

  function layoutMasonry() {
    const feed = document.querySelector('.feed');
    const allCards = Array.from(feed.querySelectorAll('.card'));
    const filteredCards = allCards.filter(c => !c.classList.contains('hidden') && c.style.display !== 'none');
    if (!filteredCards.length) { feed.style.height = '0px'; return; }

    // Show only up to cardsShown, hide the rest as overflow
    const visibleCards = filteredCards.slice(0, cardsShown);
    const overflowCards = filteredCards.slice(cardsShown);

    overflowCards.forEach(card => {
      card.classList.add('card-overflow');
      card.style.position = 'absolute';
      card.style.left = '-9999px';
    });
    visibleCards.forEach(card => {
      card.classList.remove('card-overflow');
    });

    // Toggle load-more button visibility
    const loadMoreBtn = document.getElementById('loadMore');
    if (loadMoreBtn) {
      loadMoreBtn.style.display = overflowCards.length > 0 ? '' : 'none';
    }

    const feedWidth = feed.clientWidth;
    const firstCard = visibleCards[0];
    const cardWidth = firstCard.offsetWidth;
    const gap = 8;
    const cols = Math.max(1, Math.round(feedWidth / (cardWidth + gap)));
    const colWidth = (feedWidth - (cols - 1) * gap) / cols;
    const colHeights = new Array(cols).fill(0);

    visibleCards.forEach((card, index) => {
      const col = index % cols;
      const x = col * (colWidth + gap);
      const y = colHeights[col];
      card.style.position = 'absolute';
      card.style.left = x + 'px';
      card.style.top = y + 'px';
      card.style.width = colWidth + 'px';
      colHeights[col] += card.offsetHeight + gap;
    });

    // Hide filtered-out cards off-screen
    allCards.filter(c => c.classList.contains('hidden') || c.style.display === 'none').forEach(card => {
      card.style.position = 'absolute';
      card.style.left = '-9999px';
    });

    const maxHeight = Math.max(...colHeights);

    // Position load-more button below the cards
    const loadMoreEl = document.getElementById('loadMore');
    if (loadMoreEl && loadMoreEl.style.display !== 'none') {
      loadMoreEl.style.top = maxHeight + 'px';
      feed.style.height = (maxHeight + loadMoreEl.offsetHeight + 24) + 'px';
    } else {
      feed.style.height = maxHeight + 'px';
    }
  }

  // Run masonry on load, resize, and after images load
  layoutMasonry();
  window.addEventListener('resize', layoutMasonry);
  // Re-layout every time an image loads
  document.querySelectorAll('.feed img').forEach(img => {
    img.addEventListener('load', layoutMasonry);
    // Also handle lazy-loaded images by removing lazy and forcing load
    if (img.loading === 'lazy') {
      img.loading = 'eager';
    }
  });
  // Re-run periodically as images trickle in
  setTimeout(layoutMasonry, 300);
  setTimeout(layoutMasonry, 800);
  setTimeout(layoutMasonry, 1500);
  setTimeout(layoutMasonry, 3000);
  // Also run on window load (all resources)
  window.addEventListener('load', layoutMasonry);

  // --- Load More (global so onclick can reach it) ---
  window.loadMoreCards = function() {
    cardsShown += CARDS_PER_PAGE;
    layoutMasonry();
    document.querySelectorAll('.feed .card:not(.card-overflow):not(.hidden)').forEach((c, i) => {
      if (!c.classList.contains('visible')) {
        setTimeout(() => c.classList.add('visible'), i * 40);
      }
    });
    document.querySelectorAll('.feed img').forEach(img => {
      if (!img.complete) img.addEventListener('load', layoutMasonry, { once: true });
    });
    setTimeout(layoutMasonry, 300);
    setTimeout(layoutMasonry, 800);
  };

  // --- Entrance animations via IntersectionObserver ---
  const observerOptions = { threshold: 0.08, rootMargin: '0px 0px -40px 0px' };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  cards.forEach(card => observer.observe(card));

  // --- Email signup ---
  document.getElementById('mailingForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const input = this.querySelector('input');
    const success = document.getElementById('mailingSuccess');
    const email = input.value;

    fetch('https://formsubmit.co/ajax/l4harrington@gmail.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ email: email, _subject: 'TGI Mailing List Signup' })
    }).catch(() => {});

    input.value = '';
    success.classList.add('show');
    setTimeout(() => success.classList.remove('show'), 3000);
  });

  // --- Sticky nav shrink on scroll ---
  let lastScroll = 0;
  const nav = document.querySelector('.nav');
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (y > 100) {
      nav.style.borderBottomColor = 'rgba(20,20,20,0.12)';
    } else {
      nav.style.borderBottomColor = '';
    }
    lastScroll = y;
  }, { passive: true });

  // Slide text data for carousels with dynamic descriptions
  window._slideTexts = {
    puttercovers: [
      "Birds of Condor out of Australia. The Tokyo Country Club blade cover channels the minimalism of a Japanese country club you'll probably never visit — clean lines, dark base, subtle branding. $69.95 for something that looks like it came from a pro shop in Karuizawa.",
      "Sunday Golf's blade cover in Toasted Almond — $44.99 and the best value on this list. Magnetic closure, soft interior lining, and a warm neutral colorway that pairs with everything. Sunday built their name on lightweight bags, but the accessories hold up.",
      "Jones Golf Bags — the Block J Blade Putter Cover in Le Creme. $95, genuine leather, chenille patch, magnetic closure. Made by Tremont Sporting Co. in the USA. Jones has been making golf bags since 1971; the headcovers carry the same understated Portland sensibility.",
      "Stitch Golf's Birdie Putter Cover in Stitch Blue — $68. Clean embroidery, quality materials, and the kind of blue that reads 'tasteful' rather than 'loud.' Stitch started in premium leather goods and you can feel it in the construction. A solid mid-range pick.",
      "Cayce Golf's 'Til Death Bloom — skulls and blood-red roses on a mallet cover. $59.99 with DURA+ synthetic leather and magnetic closure. This is the one for the golfer who doesn't take the dress code too seriously. Cayce leans into bold graphics and this is their best execution of it.",
      "Dormie Workshop — the 3 Wishes Mallet Cover. $155 and the most expensive on this list, but it's handcrafted full-grain leather with an embroidered lantern appliqué and velvet liner. Made by artisans in Halifax and Los Angeles. This is the heirloom piece.",
      "Rose & Fire's A-Man Standard Putter Cover — $98, fully embroidered with UV, water, and stain resistance. The 'A-Man' branding is cheeky and self-aware. Magnetic closure, padded liner. Rose & Fire makes everything in small batches with personality baked into every stitch.",
      "Gumtree Golf & Nature Club — the Studio Collection Putter Cover at $120. Gumtree sits at the intersection of golf and nature photography, and the Studio Collection reflects that — clean design, earthy tones, premium materials. A quiet headcover for people who let their game do the talking.",
      "Fyfe Golf's Dalmore Blade Putter Cover — $110, handmade in Scotland from supple dark brown leather with cream sherpa fleece lining and magnetic closure. Named after a Highland estate. Fyfe is one of the few brands actually making headcovers in Scotland, and you can feel it in the leather.",
      "EP Headcovers — the Black Camo Putter Cover at $105. Each camo shape is individually cut from genuine leather and pieced together by hand in the USA. No two are exactly alike. EP is a headcover-only brand, which means this is all they think about. It shows.",
      "Winston Collection closes it out with the Flying Mallard — $129.99 for premium pullup leather that develops patina over time, detailed mallard embroidery, and black polar fleece lining. Available in Whiskey Brown, Forest Green, and Black. The outdoors-meets-golf crossover done right."
    ],
    whitetees: [
      "Devereux keeps it simple — the Club Toss Tee is 100% Pima cotton, soft enough to sleep in, sharp enough for the turn. White with a subtle scattered club print that says \"I golf\" without saying it too loud. $44 and built for triple-digit days.",
      "Greyson's Falcon Sport SS sits at the top of the price range ($90) but earns it — technical jersey fabric with four-way stretch and UPF protection. The Arctic colorway is a clean, bright white. If you want a tee that performs like a polo but fits like your favorite weekend shirt, this is it.",
      "Manors out of London — the MGA T-Shirt is premium 240gsm cotton with a relaxed fit and minimal branding. $61 for a tee that crosses over from the course to dinner without blinking. The weight keeps it from going translucent in the sun.",
      "Birds of Condor from Australia — the Birdies and Beats Tee mixes golf and music culture in a way that actually works. $50, white cotton, and a graphic that earns a second look. The kind of tee that starts conversations on the range.",
      "Barstool Golf's Beach Pocket Tee in Ivory — $35, the lowest price point after Kingfisher. Relaxed fit, chest pocket, subtle wave branding. No frills, no pretense. The tee you grab when you're running late and still want to look like you tried.",
      "Holderness & Bourne's Mason Tee — $55 for Peruvian cotton with a tailored fit. Clean, minimal, and the kind of shirt that looks more expensive than it is. H&B built their name on polos, but this tee carries the same quality in a quieter package.",
      "Eastside Golf's Trophy Tee in Bright White — $55 and it carries the weight of the brand's mission. Founded by Olajuwon Ajanaku and Earl Cooper to make golf culture more inclusive. The trophy graphic is iconic. This one means something beyond the fabric.",
      "Kingfisher Golf out of East Dallas — the Golfmobile Tee at $30 is the best value on this list. Small-batch, 100 pieces or fewer per run. Screen-printed illustration of a vintage golf cart. Nice things, fair prices — that's not just a tagline, it's the whole brand.",
      "Radry Golf's Fore Tee — $42, 100% cotton, relaxed fit, screen-printed art. Austin-adjacent brand that keeps it clean and understated. The kind of tee that looks like it came from a shop you'd actually want to hang out in.",
      "Malbon closes it out with the Bermuda Rooster Tee — $68 for their signature rooster graphic on white cotton. Malbon built a global golf lifestyle brand from scratch, and the Bermuda Rooster is one of their most recognizable pieces. If you know, you know."
    ],
    ztputters: [
      "The first heel-shafted putters ever built around Bettinardi's SimplyBalanced zero-torque system. The Hexperimental #7 is a mid-mallet with a plumber's neck — milled in-house, honeycomb face texture, the whole Bettinardi thing. Pre-sale started April 28. The #9 is the blade version if mallets offend you. $550 for either. The kind of putter that makes you wonder if your stroke was ever the problem.",
      "Odyssey's second pass at zero torque, and this one looks like a putter your dad would recognize. The Tri-Hot SB has a heel shaft, no shaft lean, and the Tri-Hot insert for feel. Pre-orders opened April 16, retail April 24. The whole point is that it doesn't look like a science experiment — it just quietly stops the face from rotating. $399. Odyssey finally made a zero-torque putter that won't get you chirped on the first tee.",
      "Evnroll's FaceForward ZERO line made the Golf Digest Hot List, and the Z5cs Major Edition is the limited colorway — green and black, hatchback mallet shape, the grooved face that redistributes off-center hits. $449. The ZERO system eliminates shaft lean entirely, so the face stays square through the whole stroke. If you like the idea of zero torque but want a face that also forgives your aim, this is the one.",
      "The Wilson Infinite Zero Torque 606 is the price leader on this list at $249 — and it doesn't feel like a budget putter. Mallet head, center-shaft, clean lines. Wilson has been quietly making serious putters for a while now, and the 606 is their zero-torque entry that proves you don't need to spend $550 to stop the face from twisting. For the price of two sleeves of Pro V1s more than dinner, you get a real zero-torque option.",
      "TaylorMade finally brought Spider into the zero-torque conversation. The Spider ZT takes the high-MOI stability the platform is known for and adds a balanced shaft system that keeps the face square without hand manipulation. It's TaylorMade's first entry in the category, which means the R&D budget behind it is probably larger than some brands' entire revenue. $399. The Spider that doesn't want you to think about your hands."
    ],
    postroundatx: [
      "East Austin all-day brunch with a patio and scratch cocktails. The move when you tee off at 7 and finish by noon. Order the pancake, pretend you didn't just three-putt the last four greens. Started as a food truck in 2015 — now two Austin locations and a Denver outpost.",
      "Ten minutes from Grey Rock in Driftwood. Pit-smoked brisket under a tin roof, family-style platters, BYOB. Bring a cooler with Lone Stars. The open pit has been burning since 1967 and it's one of the most photographed in Texas. Five hundred acres of Hill Country out the back door.",
      "Aaron Franklin and Tyson Cole's Asian smokehouse on South Lamar. Brisket fried rice, smoked turkey, oak-smoked salmon, and a patio that feels engineered for post-round decompression. Two of Austin's best chefs made a restaurant for people who just want to sit outside and eat smoked meat with a cold drink. They nailed it.",
      "South Austin outdoor bar with food trucks, a big screen, live music, and a dog-friendly policy. Zero pretense, cold beer, plenty of shade. Closest thing to a 20th hole in south Austin. Dale Watson plays here. That should tell you everything.",
      "Southeast Austin brewery with a massive outdoor space, food trucks, a playground, and a soccer field. Close to Jimmy Clay and Roy Kizer, which makes it the obvious stop after a links-style round at Kizer. House-brewed lagers, open seven days a week, and a view of nothing in particular that somehow works.",
      "68-degree spring-fed pool in Zilker Park. Three acres of cold, clear water. Walk straight from Butler Pitch & Putt or drive ten minutes from Lions. The most Austin thing you can do after golf — or after anything. Open year-round. Nearly 800,000 visitors a year and it never feels old.",
      "Not food, not drinks, just vibes. A vintage and antique market on South Congress that's basically a museum you can buy things from. Hunt for persimmon woods, old Masters programs, or a mid-century bar cart. Browse for 45 minutes, then get ice cream at Amy's next door."
    ],
    markerbrands: [
      "The kings of limited-edition golf accessories. CNC-milled, hand-painted, and deliberately absurd. NES cartridges, bottle caps, 8-balls — Swag treats ball markers like collectible art. Drops sell out in minutes. Most markers run $55–$90, and the aftermarket is even wilder. Based in Atlanta. If you know, you know.",
      "Portland-based and hand-forged. Seamus makes markers out of bronze, copper, and steel — the kind of thing that develops a patina and looks better after a hundred rounds. The Arnold Palmer umbrella is their signature. They also do custom club crests. Everything feels like it belongs in a leather bag from 1974.",
      "Hand-painted enamel markers from a husband-and-wife team. Every design tells a small, weird story — an old fashioned cocktail, a fire truck, a cash roll. Twenty bucks each, which makes them the most giftable markers in golf. Based in Connecticut. The kind of brand you find and then tell everyone about.",
      "Pop culture meets the green. Pins & Aces does licensed collabs — South Park, Caddyshack, Happy Gilmore — plus originals that lean funny. The Randy Marsh marker is a conversation starter on any putting green. Most markers are $14.95. Low barrier, high entertainment value. They also do headcovers and accessories.",
      "CNC-milled brass and stainless steel, hand-painted with cerakote finishes. Hatch builds markers that look like small sculptures — sugar skulls, alter egos, poker chips. Made in collaboration with Legacy Golf Goods. Most pieces are $85 and sell out on drop day. Limited runs only. Based in the Southeast.",
      "The officially licensed ball marker company. PRG holds Arnold Palmer, Ryder Cup, PGA Championship, and MLB team licenses. If it has a logo on it, PRG probably made the marker. Price range is $7.50–$24 — the most affordable on this list. Not indie in spirit, but the quality and breadth are hard to ignore.",
      "Formerly Johnston Gray Designs — now rebranded. Hand-stamped copper and brass markers made one at a time. The Secret Sauce and Birdie Juice designs have a homemade charm that CNC can't replicate. They also do custom work — your initials, your course, your dog's name. $20–$30 range. Built in a garage. Feels like it.",
      "Coin-style markers machined from exotic materials — meteorite, dinosaur bone, carbon fiber, Damascus steel. Doubloon is the luxury end of this list. The Phantom at $79 is the entry point; the top-shelf pieces run four figures. Made by Revolution Jewelry Works in Utah. Every marker comes with a story about what it's made from.",
      "One-man copper shop. Liberty hand-stamps every marker from raw copper or aluminum blanks. The designs are simple and tactile — no paint, no enamel, just metal and a hammer. Custom orders are the bread and butter. $18–$39 range. Most of the ready-made designs sell through eBay. Old school in the best way.",
      "CNC-machined from solid metal with full custom capability. Golf Life Metals does corporate logos, course crests, and personal designs at a level of detail that borders on engraving. Based in the U.S. Not a drop brand — they're a made-to-order shop. If you want your foursome's logo on a marker, this is who you call."
    ],
    malbonseoul: [
      "The hero piece. Hybrid construction — insulated body panels with stretchy woven sleeves for full range of motion. Windproof front, breathable back. The green colorway is the one that looks like it belongs on a links course in Scotland. Also comes in black. $318 and built for rounds where the weather can't make up its mind.",
      "The most technical jacket in the collection. Three-layer bonded fabric, fully seam-sealed, DWR finish. Light grey keeps it from looking like rain gear. At $448 it's the top of the line — but this is the piece that replaces your rain jacket, your wind layer, and your 'just in case' pullover. One jacket, every condition.",
      "Full seam-sealed rain protection in a clean, minimal silhouette. No logos screaming at you, no neon piping. Just a well-cut black jacket that happens to be fully waterproof. Pairs with the matching Rain Pant ($378) for a head-to-toe system. $428. The kind of rain gear you'd actually want to wear on a dry day too.",
      "Double-knit construction — heavier than a polo, lighter than a sweater. The navy pullover is the layering piece that works under a jacket or on its own in the clubhouse. Structured enough to look sharp, stretchy enough to swing in. $318. Seoul's design team clearly builds for golfers who don't want to change clothes between the course and everywhere else.",
      "The Buckets logo on a polo sweater. Cream colorway, knit construction, polo collar — this one blurs the line between golf apparel and the kind of thing you'd see at a café in Gangnam. $368. It's the most distinctly Seoul piece in the collection. Not performance wear. Not streetwear. Something else entirely.",
      "Panel-blocked mock neck in off white. Clean seams, minimal branding, the kind of mid-layer that disappears under a jacket or stands on its own. $208 makes it the most accessible layering piece in the drop. The mock neck silhouette is everywhere in Korean golf culture — this is Malbon's version of that staple.",
      "Cargo pants that somehow don't look like cargo pants. Relaxed fit, utility pockets that sit flush, tapered leg. Beige. $288. Seoul's design philosophy shows here — functional details that don't announce themselves. These work on the course and they work off it. The pintuck straight pant ($268) is the dressier alternative.",
      "Seam-sealed bucket hat in lightweight rain fabric. $112. The entry point into the collection and probably the piece that moves fastest. Fully waterproof, packable, and minimal enough to wear with anything. Also comes in white. If you buy one thing from Studio Seoul, this is the smart money pick."
    ],
    kingfisher: [
      "Started at a kitchen counter in East Dallas by a designer named Fiona. Polos, tees, and caps — nothing else. Every run is 100 pieces or fewer. No hype, no performance claims, no lifestyle fiction. Just well-designed, fairly priced golf apparel for people who care about the details but don't need to broadcast it. The tagline says it all: nice things, fair prices.",
      "The polo line is the backbone. Ten styles, all $49.99, all built on performance fabric with a clean collar. Produced by the same factories behind the big-brand polos — same materials, same construction — just without the markup or the logo tax. The Kit Polo is a good starting point. Runs of 100 mean they move fast.",
      "The Black Striped Polo is the one that looks like it costs twice what it does. Subtle texture, clean lines, no visible branding on the front. The kind of shirt that works at a muni in the morning and dinner that night. Fiona's design background shows up in the details — the collar sits right, the weight feels considered.",
      "The Cream Polo rounds out the range with a quieter option. Same $49.99 price, same performance fabric. Kingfisher doesn't do seasonal drops or trend-chasing — they make shirts they'd want to wear, produce a hundred of each, and move on. If it sells out, it's gone. No restocks, no waitlists.",
      "The graphic tee line leans into Dallas pride and self-deprecating golf humor. 'Worst Golfer in Dallas' is the signature. 100% cotton, $30–$35. The 'Getting Worse' tee and 'Dallas Original' round out the collection. These aren't performance shirts — they're what you throw on after the round or to the range on a Saturday.",
      "The cap wall is deep — 17 styles at $24.99 each. Heavy DAL branding across the line in every color you'd want. Structured and unstructured options, nylon golfers, dad caps, camo. The Logo Golfer is the cleanest silhouette. At $25 a hat, the cap line is probably the easiest entry point into the brand.",
      "Made with heart in Texas. Fiona started Kingfisher with a sewing machine and a pile of thrift store scraps. The brand grew from the overlap of her design background and her brother's golf habit. No investors, no influencer strategy, no fiction about changing your game. Just a small Dallas brand making considered clothes in small batches. Worth knowing. @kingfisher.golf"
    ],
    practiceatx: [
      "The best public practice facility in Austin, full stop. Named after the man who wrote the Little Red Book. All-grass range — no mats, no rubber tees — plus two putting greens, a practice bunker, a 3-hole short course, and a PGA Tour-designed 9-hole layout. The range faces east, so afternoon sessions dodge the sun. Buckets run $8–$14. City-owned, open to everyone, and perpetually underrated.",
      "Full-service practice complex attached to an 18-hole course in northwest Austin. Grass and mat hitting stations, Toptracer technology in the bays so you can track carry distance and ball flight, large putting green, and a short game area with bunkers. PGA pros on staff for lessons. Good warm-up spot or standalone session. Buckets around $8–$12.",
      "Yes, it's an entertainment venue. But the Toptracer data in every bay — carry, ball speed, launch angle, spin — is legitimately useful for dialing in numbers. Multi-level climate-controlled bays, open late, full bar and kitchen. Best use case: off-season sessions when you want data without the heat, or when your non-golf friends want to come along. Bays run $30–$55/hour.",
      "Austin's most beloved 9-hole par 3, tucked between Zilker Park and Lady Bird Lake. Longest hole is about 100 yards, so it's pure wedge and putter work on real greens. BYOB-friendly, zero dress code, no tee times needed. The best place in Austin to sharpen your short game without the pressure of a full round. Walk-up rate around $10–$14.",
      "The muni range that serves both Jimmy Clay and Roy Kizer on the south side. Grass tees when conditions allow, mats as backup. Big putting green, no-frills setup. Close to Kizer's links-style layout, so you can hit a bucket and play 18 in the same trip. Buckets run $6–$10 — the cheapest serious range session in Austin.",
      "The oldest municipal course in Texas, opened in 1924 on Enfield Road near downtown. The practice area is modest — putting green and a small warm-up zone — but the course itself is a 9-hole short game masterclass. Tight fairways, mature oaks, small greens. If you want to practice course management and creative shot-making on a real layout, this is your classroom. Walk-on rates are the lowest in town.",
      "Hill Country vibes with modern tech. Dripping Springs CC has a Toptracer-equipped driving range, putting green, and a laid-back bar and food setup. The range has solid target greens and the Toptracer bays give you real data on every swing. Worth the 30-minute drive from central Austin if you want a practice session that doesn't feel like a chore. They also have yard games and events.",
      "Thirty-five acres of standalone driving range in Round Rock. Full-length range, short-distance range, chipping green, putting green, and professional Musco lighting for night sessions — you can hit balls well after dark. No course attached, just pure practice. One of the few dedicated ranges left in the metro. Old school, well-maintained, and open seven days a week."
    ]
  };

  initGearCarousels();