(() => {
  document.documentElement.classList.add('js');
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // hamburger menu
  const burger = $('#burger'), menu = $('#menu');
  if (burger && menu) {
    const set = open => {
      document.body.classList.toggle('menu-open', open);
      burger.setAttribute('aria-expanded', open);
      burger.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
      menu.setAttribute('aria-hidden', !open);
    };
    burger.addEventListener('click', () => set(!document.body.classList.contains('menu-open')));
    $$('a', menu).forEach(a => a.addEventListener('click', () => set(false)));
    addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
    addEventListener('scroll', () => burger.classList.toggle('scrolled', scrollY > 80), { passive: true });
  }
  {
    const hd = () => document.body.classList.toggle('hd-s', scrollY > 40);
    hd(); addEventListener('scroll', hd, { passive: true });
  }

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

  // re-apply #anchor after late layout (htmlpreview writes the page after the browser's own jump)
  const id = decodeURIComponent(location.hash.slice(1));
  if (id) {
    let moved = false;
    addEventListener('wheel', () => moved = true, { passive: true, once: true });
    addEventListener('touchstart', () => moved = true, { passive: true, once: true });
    const go = () => { const t = document.getElementById(id); if (t && !moved) t.scrollIntoView(); };
    [50, 400, 1200, 2500].forEach(ms => setTimeout(go, ms));
    addEventListener('load', go);
  }

  // chapter rail on the top page
  const rail = $('.rail');
  if (rail) {
    const items = $$('li', rail), secs = $$('section[data-ch]');
    const upd = () => {
      const mid = innerHeight * 0.45; let cur = null, dark = false;
      secs.forEach(s => { const r = s.getBoundingClientRect(); if (r.top <= mid && r.bottom > mid) { cur = s.dataset.ch; dark = s.classList.contains('dark') || s.classList.contains('stance'); } });
      rail.classList.toggle('on', !!cur); rail.classList.toggle('dk', dark);
      items.forEach(li => li.classList.toggle('cur', li.dataset.ch === cur));
    };
    upd(); addEventListener('scroll', upd, { passive: true });
  }

  // reading progress + stat counters
  const prog = $('.prog');
  if (prog) {
    const up = () => { const h = document.documentElement; const max = h.scrollHeight - innerHeight; prog.style.setProperty('--p', max > 0 ? Math.min(1, scrollY / max).toFixed(4) : 0); };
    up(); addEventListener('scroll', up, { passive: true }); addEventListener('resize', up);
  }
  const market = $('.market');
  if (market && 'IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const nums = $$('.num strong', market).map(el => ({ el, node: el.firstChild, to: parseFloat(el.firstChild.textContent), dec: (el.firstChild.textContent.split('.')[1] || '').length }));
    const io2 = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return; io2.disconnect(); market.classList.add('in');
      const t0 = performance.now(), dur = 1600;
      const tick = now => { const k = Math.min(1, (now - t0) / dur), ease = 1 - Math.pow(1 - k, 3);
        nums.forEach(n => n.node.textContent = (n.to * ease).toFixed(n.dec)); if (k < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
    }), { threshold: .3 });
    io2.observe(market);
  } else if (market) market.classList.add('in');
})();
