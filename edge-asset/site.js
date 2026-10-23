(() => {
  document.documentElement.classList.add('js');
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // hero slideshow (top page only)
  const slides = $$('.slide'), pager = $('#pager'), cnt = $('#cnt');
  if (slides.length > 1 && pager) {
    const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let cur = 0, timer;
    slides.forEach((_, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', '写真 ' + (i + 1));
      b.addEventListener('click', () => go(i));
      pager.appendChild(b);
    });
    const bars = $$('button', pager);
    const go = i => {
      slides[cur].classList.remove('on'); bars[cur].classList.remove('on');
      cur = i; slides[cur].classList.add('on');
      void bars[cur].offsetWidth; bars[cur].classList.add('on');
      if (cnt) cnt.textContent = String(cur + 1).padStart(2, '0');
      clearTimeout(timer);
      if (!still) timer = setTimeout(() => go((cur + 1) % slides.length), 6000);
    };
    go(0);
  }

  // reveal on scroll
  const targets = $$('.rv, .mask');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
    targets.forEach(el => io.observe(el));
  } else targets.forEach(el => el.classList.add('in'));
  // safety net: anything already scrolled past is shown even if the observer missed it
  let ticking = false;
  addEventListener('scroll', () => {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => {
      targets.forEach(el => { if (!el.classList.contains('in') && el.getBoundingClientRect().top < innerHeight) el.classList.add('in'); });
      ticking = false;
    });
  }, { passive: true });

  // contact form
  const form = $('#cf');
  if (form) {
    $$('.way').forEach(a => a.addEventListener('click', () => { const t = $('#f-topic'); if (t) t.value = a.dataset.topic; }));
    form.addEventListener('submit', e => {
      e.preventDefault();
      const mail = $('#f-mail');
      if (!mail.value || !mail.checkValidity()) { mail.focus(); mail.style.borderBottomColor = '#c0392b'; return; }
      form.hidden = true; const sent = $('#sent'); if (sent) sent.hidden = false;
    });
  }
})();
