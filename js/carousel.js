// Shared carousel logic — call initGearCarousels() after defining window._slideTexts

/* ── Gear Carousel ── */
function initGearCarousels() {
    document.querySelectorAll('.gear-carousel').forEach(carousel => {
      const id = carousel.dataset.carousel;
      const track = carousel.querySelector('.gear-carousel-track');
      const slides = track.querySelectorAll('.gear-slide');
      const total = slides.length;
      const dotsContainer = document.querySelector(`[data-dots="${id}"]`);
      const counter = document.querySelector(`[data-counter="${id}"]`);
      let current = 0;

      // Build dots
      if (dotsContainer) {
        for (let i = 0; i < total; i++) {
          const dot = document.createElement('button');
          dot.className = 'gear-dot' + (i === 0 ? ' active' : '');
          dot.setAttribute('aria-label', `Slide ${i + 1}`);
          dot.onclick = () => goTo(i);
          dotsContainer.appendChild(dot);
        }
      }

      function goTo(idx) {
        current = ((idx % total) + total) % total;
        track.style.transform = `translateX(-${current * 100}%)`;
        if (dotsContainer) {
          dotsContainer.querySelectorAll('.gear-dot').forEach((d, i) => {
            d.classList.toggle('active', i === current);
          });
        }
        if (counter) counter.textContent = `${current + 1} / ${total}`;
        // Dynamic slide text support
        var textEl = document.querySelector('[data-slidetext="' + id + '"]');
        if (textEl && window._slideTexts && window._slideTexts[id]) {
          textEl.style.transition = 'opacity 0.2s ease';
          textEl.style.opacity = '0';
          setTimeout(function(){ textEl.textContent = window._slideTexts[id][current]; textEl.style.opacity = '1'; }, 200);
        }
      }

      carousel.goTo = goTo;
      carousel.getTotal = () => total;
      carousel.getCurrent = () => current;
    });
  }

  function gearSlide(btn, dir) {
    const carousel = btn.closest('.gear-carousel');
    const current = carousel.getCurrent();
    const total = carousel.getTotal();
    carousel.goTo((current + dir + total) % total);
  }

  // Touch/swipe support for gear carousels
  document.querySelectorAll('.gear-carousel').forEach(carousel => {
    let startX = 0;
    let diff = 0;
    carousel.addEventListener('touchstart', e => { startX = e.touches[0].clientX; }, { passive: true });
    carousel.addEventListener('touchmove', e => { diff = startX - e.touches[0].clientX; }, { passive: true });
    carousel.addEventListener('touchend', () => {
      if (Math.abs(diff) > 40) {
        const cur = carousel.getCurrent();
        const tot = carousel.getTotal();
        carousel.goTo((cur + (diff > 0 ? 1 : -1) + tot) % tot);
      }
      diff = 0;
    });
  });