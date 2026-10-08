/* More from TGI — redraw the four cards on every page view, favouring newer posts.
   Pool: /data/more-pool.json (built on deploy by rotate-more-from-tgi.py).
   Static cards stay in the HTML for crawlers and no-JS readers. */
(function () {
  var grid = document.querySelector('.more-grid');
  if (!grid || !window.fetch) return;
  var here = location.pathname.replace(/\.html$/, '').replace(/\/$/, '');
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  fetch('/data/more-pool.json', {cache: 'no-cache'}).then(function (r) { return r.ok ? r.json() : null; }).then(function (P) {
    if (!P || P.length < 6) return;
    var now = Date.now();
    var skip = (grid.getAttribute('data-exclude') || '').split(',').filter(Boolean);
    var cand = P.filter(function (p) { return p.u !== here && skip.indexOf(p.u) < 0; });
    function age(p) { return Math.max(0, (now - Date.parse(p.d + 'T12:00:00Z')) / 864e5); }
    function w(p, kinds) { return (0.04 + Math.pow(0.5, age(p) / 21)) / (1 + (kinds[p.k] || 0) * 0.6); }
    var pin = (grid.getAttribute('data-pin') || '').split(',').filter(Boolean);
    var out = [], kinds = {};
    pin.forEach(function (u) { cand.forEach(function (p) { if (p.u === u && out.indexOf(p) < 0) { out.push(p); kinds[p.k] = (kinds[p.k] || 0) + 1; } }); });
    var fresh = cand.filter(function (p) { return age(p) <= 14 && out.indexOf(p) < 0; });
    if (fresh.length && out.length < 4) { var f = fresh[Math.floor(Math.random() * fresh.length)]; out.push(f); kinds[f.k] = 1; }
    while (out.length < 4 && out.length < cand.length) {
      var rest = cand.filter(function (p) { return out.indexOf(p) < 0; });
      var tot = 0, ws = rest.map(function (p) { var x = w(p, kinds); tot += x; return x; });
      var r = Math.random() * tot, i = 0;
      for (; i < rest.length - 1; i++) { r -= ws[i]; if (r <= 0) break; }
      out.push(rest[i]); kinds[rest[i].k] = (kinds[rest[i].k] || 0) + 1;
    }
    grid.innerHTML = out.map(function (p) {
      return '<a href="' + esc(p.u) + '" class="more-card"><div class="more-card-img"><img src="' + esc(p.i) +
        '" alt="' + esc(p.t) + '" loading="lazy" /></div><div class="more-card-body"><div class="more-card-name">' +
        esc(p.t) + '</div><div class="more-card-tag">' + p.k + '</div></div></a>';
    }).join('');
  }).catch(function () {});
})();
