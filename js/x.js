/* =========================================================
   WATERDROP ECUADOR · Tienda + animaciones de scroll
   ---------------------------------------------------------
   >>> PRECIOS, CÓDIGOS Y FECHA DE LA OFERTA: EDITA SOLO AQUÍ <<<
   ========================================================= */
const WD = {
  whatsapp: '593997312362',
  promo: {
    name: 'Oferta de Octubre',
    end: '2026-10-31T23:59:59-05:00'   // hora de Ecuador (UTC-5)
  },
  products: {
    x12:   { name: 'Waterdrop X12 · 1200 GPD',      price: 1999, was: 2200, code: 'NASX12',  note: 'Precio final: incluye IVA e instalación', img: 'assets/x12/ui-wd-x12-new-vis-pr-logo.webp', url: 'product-x12.html' },
    g5:    { name: 'Waterdrop G5P700A · 700 GPD',   price: 1399, was: 1699, code: 'NASG5',   note: 'Precio final: incluye IVA e instalación', img: 'assets/g5/ui-wd-g5p700a-product.webp',      url: 'product-g5p700a.html' },
    g2:    { name: 'Waterdrop G2P600 · 600 GPD',    price: 900,  was: 1300, code: 'NASG2',   note: 'Precio final: incluye IVA e instalación', img: 'assets/g2/WD-G2P600-W-NSF.png', url: 'product-g2p600.html' },
    uf:    { name: 'Waterdrop Ultrafiltración UF',  price: 299,  was: 380,  code: 'NASUF',   note: 'Precio final: incluye IVA e instalación', img: 'assets/uf/10UB-UF-NSF.png',                 url: 'product-uf.html' },
    smart: { name: 'Waterdrop Dispensador ED01',    price: 99,   was: 129,  code: 'NASED01', note: 'Precio final con IVA · envío no incluido', img: 'assets/ed01/1_33c5e044-eb97-4485-ae99-684bc658886e.webp', url: 'product-smart.html' },
    // Filtros de repuesto (sin descuento)
    'x12-f1a':     { name: 'Filtro F1A · Waterdrop X12',         price: 49.99,  was: 49.99,  note: 'Incluye IVA · envío no incluido', img: 'assets/x12/ui-wd-f1a-product.png',        url: 'repuestos#x12-f1a' },
    'x12-f2':      { name: 'Filtro F2 · Waterdrop X12',          price: 39.99,  was: 39.99,  note: 'Incluye IVA · envío no incluido', img: 'assets/x12/ui-wd-f2_FILTER.webp',         url: 'repuestos#x12-f2' },
    'x12-f3':      { name: 'Filtro X12-F3 · Waterdrop X12',      price: 159.99, was: 159.99, note: 'Incluye IVA · envío no incluido', img: 'assets/x12/ui-wd-x12-f3-fIlter.webp',     url: 'repuestos#x12-f3' },
    'g5-cf':       { name: 'Filtro G5P700A-CF · Waterdrop G5',   price: 59.99,  was: 59.99,  note: 'Incluye IVA · envío no incluido', img: 'assets/g5/ui-wd-g5p700a-cf-product.png',  url: 'repuestos#g5-cf' },
    'g5-ro':       { name: 'Filtro G5P700-RO · Waterdrop G5',    price: 129.99, was: 129.99, note: 'Incluye IVA · envío no incluido', img: 'assets/g5/ui-wd-g5p700-ro-product.png',   url: 'repuestos#g5-ro' },
    'g2-cf':       { name: 'Filtro G2CF · Waterdrop G2P600',      price: 60,     was: 60,     note: 'Incluye IVA · envío no incluido', img: 'assets/g2/G2CF.png',                     url: 'repuestos#g2-cf' },
    'g2-ro':       { name: 'Filtro G2P6MRO · Waterdrop G2P600',   price: 130,    was: 130,    note: 'Incluye IVA · envío no incluido', img: 'assets/g2/WD-G2P6MRO.png',               url: 'repuestos#g2-ro' },
    'uf-rf10':     { name: 'Filtro RF10-UF · Ultrafiltración',   price: 70,     was: 70,     note: 'Incluye IVA · envío no incluido', img: 'assets/uf/WD-RF10-UF-NSF.png',            url: 'repuestos#uf-rf10' },
    'ed01-filtro': { name: 'Filtro WD-EDF · Dispensador ED01',   price: 25.99,  was: 25.99,  note: 'Incluye IVA y envío',             img: 'assets/filtros/wd-edf.webp',              url: 'repuestos#ed01-filtro' }
  }
};

(function () {
  const P = WD.products;
  const END = new Date(WD.promo.end).getTime();
  let promoOn = Date.now() < END;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const money = n => '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const priceOf = id => promoOn ? P[id].price : P[id].was;
  const wa = t => `https://wa.me/${WD.whatsapp}?text=${encodeURIComponent(t)}`;
  // Google Ads: conversión "Contacto WhatsApp" (enlaces wa.me y pedidos por WhatsApp)
  const waConv = () => { if (typeof gtag === 'function') gtag('event', 'conversion', { send_to: 'AW-18496630945/Aj2XCIyswpMdEKHh8PNE', transport_type: 'beacon' }); };
  document.addEventListener('click', e => { if (e.target.closest?.('a[href*="wa.me/"], a[href*="whatsapp.com/"]')) waConv(); }, true);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- PRECIOS ---------- */
  function paint() {
    document.documentElement.classList.toggle('promo-ended', !promoOn);
    const $$ = (q, r) => [...(r || document).querySelectorAll(q)].filter(e => { const k = Object.keys(e.dataset).find(x => /^(price|was|off|code|note|saveamt)$/.test(x)); return !k || P[e.dataset[k]]; });
    $$('[data-price]').forEach(e => e.textContent = money(priceOf(e.dataset.price)));
    $$('[data-was]').forEach(e => { const q = P[e.dataset.was]; e.textContent = q.was > q.price ? money(q.was) : ''; });
    $$('[data-off]').forEach(e => e.textContent = `${money(P[e.dataset.off].was - P[e.dataset.off].price).replace('.00', '')} de descuento`);
    $$('[data-code]').forEach(e => e.textContent = P[e.dataset.code].code);
    $$('[data-note]').forEach(e => e.textContent = P[e.dataset.note].note || '');
    $$('[data-saveamt]').forEach(e => e.textContent = money(P[e.dataset.saveamt].was - P[e.dataset.saveamt].price).replace('.00', ''));
    $$('[data-promo-name]').forEach(e => e.textContent = WD.promo.name);
    $$('[data-maxoff]').forEach(e => e.textContent = money(Math.max(...Object.values(P).map(p => p.was - p.price))).replace('.00', ''));
  }

  /* ---------- CUENTA REGRESIVA ---------- */
  const pad = n => String(n).padStart(2, '0');
  function tick() {
    const left = Math.max(0, END - Date.now());
    if (!left && promoOn) { promoOn = false; paint(); renderCart(); }
    const v = { d: Math.floor(left / 864e5), h: Math.floor(left / 36e5) % 24, m: Math.floor(left / 6e4) % 60, s: Math.floor(left / 1e3) % 60 };
    $$('[data-cd]').forEach(b => ['d', 'h', 'm', 's'].forEach(k => { const e = $(`[data-${k}]`, b); if (e) e.textContent = pad(v[k]); }));
  }

  /* ---------- CARRITO ---------- */
  const KEY = 'wd_cart_v2';
  let cart = {};
  try { cart = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
  Object.keys(cart).forEach(k => { if (!P[k]) delete cart[k]; });
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {} };

  function add(id, q = 1) { cart[id] = Math.min(20, (cart[id] || 0) + q); save(); renderCart(); toast(`${P[id].name} se agregó al carrito`);
    if (typeof gtag === 'function') gtag('event', 'conversion', { send_to: 'AW-18496630945/ZtMkCOPkvpIdEKHh8PNE', value: P[id].price * q, currency: 'USD' }); }
  function setQ(id, q) { if (q <= 0) delete cart[id]; else cart[id] = Math.min(20, q); save(); renderCart(); }

  function renderCart() {
    const ids = Object.keys(cart), n = ids.reduce((a, k) => a + cart[k], 0);
    $$('.x-count').forEach(e => { e.textContent = n; e.classList.toggle('show', n > 0); });
    const list = $('#x-cart-items'); if (!list) return;
    list.innerHTML = ids.length ? ids.map(id => `
      <div class="x-ci">
        <img src="${P[id].img}" alt="">
        <div><b>${P[id].name}</b>
          <div class="x-price"><span class="now">${money(priceOf(id))}</span>${promoOn && P[id].was > P[id].price ? `<span class="was">${money(P[id].was)}</span>` : ''}</div>
          <div class="x-qty"><button data-cq="${id}" data-d="-1" aria-label="Quitar uno">−</button><span>${cart[id]}</span><button data-cq="${id}" data-d="1" aria-label="Agregar uno">+</button></div>
        </div>
        <button class="x-ci-rm" data-crm="${id}">Quitar</button>
      </div>`).join('') : '<p class="x-cart-empty">Tu carrito está vacío.</p>';
    const sub = ids.reduce((a, k) => a + P[k].was * cart[k], 0), tot = ids.reduce((a, k) => a + priceOf(k) * cart[k], 0);
    $('#x-cart-sub').textContent = money(sub);
    $('#x-cart-save').textContent = '−' + money(sub - tot);
    $('#x-cart-save-row').hidden = !promoOn || sub === tot;
    $('#x-cart-tot').textContent = money(tot);
    $('#x-checkout').hidden = !ids.length;
  }
  function checkout() {
    const ids = Object.keys(cart); if (!ids.length) return;
    const lines = ids.map(k => `• ${cart[k]} x ${P[k].name} — ${money(priceOf(k) * cart[k])}${promoOn && P[k].code ? ` (código ${P[k].code})` : ''}`);
    const tot = ids.reduce((a, k) => a + priceOf(k) * cart[k], 0);
    waConv(); window.open(wa(`Hola Nasfeco, quiero hacer este pedido${promoOn ? ' con la ' + WD.promo.name : ''}:\n\n${lines.join('\n')}\n\nTotal: ${money(tot)}\n\nNombre:\nCiudad:`), '_blank');
  }
  function buy(id) {
    waConv(); window.open(wa(`Hola Nasfeco, quiero comprar el ${P[id].name} a ${money(priceOf(id))}${promoOn && P[id].code ? ` con el código ${P[id].code} (${WD.promo.name})` : ''}. ¿Me ayudan con el pedido?`), '_blank');
  }
  const openCart = () => { $('#x-cart')?.classList.add('open'); $('#x-cart-ov')?.classList.add('open'); };
  const closeCart = () => { $('#x-cart')?.classList.remove('open'); $('#x-cart-ov')?.classList.remove('open'); };

  let tt;
  function toast(msg) {
    let t = $('#x-toast');
    if (!t) { t = document.createElement('div'); t.id = 'x-toast'; t.className = 'x-toast'; document.body.appendChild(t); }
    t.innerHTML = `<span></span><button type="button">Ver carrito</button>`;
    t.firstChild.textContent = msg;
    t.lastChild.onclick = () => { t.classList.remove('show'); openCart(); };
    t.classList.add('show'); clearTimeout(tt); tt = setTimeout(() => t.classList.remove('show'), 3200);
  }

  /* ---------- CLICS (delegados) ---------- */
  document.addEventListener('click', e => {
    const t = e.target.closest('[data-add],[data-buy],[data-cq],[data-crm],[data-open-cart],[data-close-cart],#x-checkout,[data-copy],[data-tab],[data-thumb],[data-yt],[data-q],[data-menu],[data-menu-close],.x-arrow');
    if (!t) return;
    const d = t.dataset;
    if (d.add) add(d.add);
    else if (d.buy) buy(d.buy);
    else if (d.cq) setQ(d.cq, cart[d.cq] + +d.d);
    else if (d.crm) setQ(d.crm, 0);
    else if ('openCart' in d) openCart();
    else if ('closeCart' in d) closeCart();
    else if (t.id === 'x-checkout') checkout();
    else if (d.copy) {
      try { navigator.clipboard.writeText(P[d.copy].code); } catch (err) {}
      t.classList.add('copied'); setTimeout(() => t.classList.remove('copied'), 1500);
      toast(`Código ${P[d.copy].code} copiado`);
    }
    else if (d.tab) {
      const g = t.closest('[data-tabs]');
      $$('[data-tab]', g).forEach(b => b.classList.toggle('on', b === t));
      $$('.x-pane', g).forEach(p => p.classList.toggle('on', p.id === d.tab));
    }
    else if (d.thumb) {
      const m = $('#x-gal-main'); $$('[data-thumb]').forEach(b => b.classList.toggle('on', b === t));
      m.style.opacity = 0; setTimeout(() => { m.src = d.thumb; m.style.opacity = 1; }, 150);
    }
    else if (d.yt && !t.querySelector('iframe')) {
      t.insertAdjacentHTML('beforeend', `<iframe src="https://www.youtube-nocookie.com/embed/${d.yt}?autoplay=1&rel=0" title="Video" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>`);
    }
    else if (d.q !== undefined) { pressGo(+d.q); pressStop(); }
    else if ('menu' in d) $('#x-mnav')?.classList.add('open');
    else if ('menuClose' in d) $('#x-mnav')?.classList.remove('open');
    else if (t.classList.contains('x-arrow')) {
      const tr = $('.x-car-track', t.closest('[data-car]'));
      const card = tr.firstElementChild; const step = card ? card.getBoundingClientRect().width + 20 : tr.clientWidth;
      tr.scrollBy({ left: t.classList.contains('next') ? step : -step });
    }
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeCart(); $('#x-mnav')?.classList.remove('open'); } });
  $('#x-cart-ov')?.addEventListener('click', closeCart);
  $$('#x-mnav a').forEach(a => a.addEventListener('click', () => $('#x-mnav').classList.remove('open')));

  /* ---------- CARRUSELES ---------- */
  $$('[data-car]').forEach(c => {
    const tr = $('.x-car-track', c), pv = $('.x-arrow.prev', c), nx = $('.x-arrow.next', c), bar = $('.x-prog i', c);
    const up = () => {
      const max = tr.scrollWidth - tr.clientWidth;
      if (pv) pv.disabled = tr.scrollLeft < 5;
      if (nx) nx.disabled = tr.scrollLeft > max - 5;
      if (bar) { const w = Math.min(1, tr.clientWidth / tr.scrollWidth); bar.style.width = w * 100 + '%'; bar.style.left = (max > 0 ? tr.scrollLeft / max : 0) * (1 - w) * 100 + '%'; }
    };
    tr.addEventListener('scroll', up, { passive: true }); addEventListener('resize', up); up();
  });

  /* ---------- MINERALES (acordeón) ---------- */
  $$('.x-min-p').forEach(p => {
    const on = () => $$('.x-min-p', p.parentElement).forEach(x => x.classList.toggle('on', x === p));
    p.addEventListener('mouseenter', on); p.addEventListener('click', on);
  });

  /* ---------- PRENSA ---------- */
  const press = $('[data-press]'); let pi = 0, pt;
  function pressGo(i) {
    if (!press) return; pi = i;
    $$('.x-quote>p', press).forEach((q, k) => q.classList.toggle('on', k === i));
    $$('[data-q]', press).forEach((b, k) => b.classList.toggle('on', k === i));
  }
  function pressStop() { clearInterval(pt); }
  if (press) { const n = $$('[data-q]', press).length; pt = setInterval(() => pressGo((pi + 1) % n), 5000); }

  /* ---------- VIDEOS: reproducir solo cuando se ven ---------- */
  const vio = new IntersectionObserver(es => es.forEach(en => {
    const v = en.target;
    if (en.isIntersecting) { if (v.preload === 'none') v.preload = 'auto'; v.play().catch(() => {}); } else v.pause();
  }), { threshold: .15 });
  $$('video[data-auto]').forEach(v => vio.observe(v));

  /* ---------- APARICIÓN ---------- */
  let pending = $$('.x-rv'), rq = 0;
  const reveal = () => {
    rq = 0;
    const lim = innerHeight * .92;
    pending = pending.filter(e => {
      const r = e.getBoundingClientRect();
      if (r.top < lim && r.bottom > 0 || r.bottom < 0) { e.classList.add('in'); return false; }
      return true;
    });
  };
  const queueReveal = () => { if (!rq) rq = setTimeout(reveal, 40); };
  addEventListener('scroll', queueReveal, { passive: true });
  addEventListener('resize', queueReveal);
  reveal();
  const rvi = setInterval(() => { reveal(); if (!pending.length) clearInterval(rvi); }, 300);

  /* ---------- SUB-NAV + NAV LATERAL ---------- */
  const sub = $('.x-subnav'), side = $('.x-side'), banner = $('.x-banner');
  const onScroll = () => {
    const past = banner ? banner.getBoundingClientRect().bottom < 0 : scrollY > 600;
    sub?.classList.toggle('show', past);
    side?.classList.toggle('show', past);
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll(); setInterval(onScroll, 500);
  if (side) {
    const links = $$('a', side), bars = $$('.x-side-rail i', side);
    const map = links.map(a => $(a.getAttribute('href'))).filter(Boolean);
    const sio = new IntersectionObserver(es => es.forEach(en => {
      if (!en.isIntersecting) return;
      const i = map.indexOf(en.target);
      links.forEach((a, k) => a.classList.toggle('on', k === i)); bars.forEach((b, k) => b.classList.toggle('on', k === i));
    }), { rootMargin: '-45% 0px -50% 0px' });
    map.forEach(s => sio.observe(s));
  }

  /* =========================================================
     ANIMACIONES DE SCROLL (GSAP + ScrollTrigger)
     ========================================================= */
  function scroll() {
    const G = window.gsap, ST = window.ScrollTrigger;
    if (!G || !ST || reduce) { staticFau(); $$('[data-drop]').forEach(d => d.classList.add('static')); return; }
    G.registerPlugin(ST);
    ST.config({ ignoreMobileResize: true });
    const mm = G.matchMedia();
    // Orden en la página: las secciones de arriba se calculan primero (como en waterdropfilter.com)
    const pinned = $$('[data-flow],[data-seq],[data-fau],[data-us],[data-drop]');
    const prio = el => -pinned.indexOf(el);

    /* 1) Video que se expande a pantalla completa */
    mm.add('(min-width: 768px)', () => {
      $$('[data-flow]').forEach(sec => {
        const stage = $('.x-flow-stage', sec), head = $('.x-flow-head', sec), media = $('.x-flow-media', sec);
        const start = () => {
          const vw = stage.clientWidth, vh = stage.clientHeight, top = head.offsetHeight + 40;
          const w = Math.min(1280, vw - 96), h = Math.max(240, Math.min(720, vh - top - 48));
          const s = (vw - w) / 2;
          return `inset(${top}px ${s}px ${Math.max(0, vh - top - h)}px ${s}px round 24px)`;
        };
        G.set(media, { clipPath: start });
        const tl = G.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: sec, start: 'top top', end: '+=140%', scrub: .5, pin: stage, invalidateOnRefresh: true, refreshPriority: prio(sec) } });
        tl.to(head, { autoAlpha: 0, y: -80, duration: .35 }, 0)
          .fromTo(media, { clipPath: start }, { clipPath: 'inset(0px 0px 0px 0px round 0px)', duration: .7 }, 0)
          .to({}, { duration: .3 });
      });
    });

    /* 2) Filtro de 11 etapas: textos que cambian con el scroll */
    $$('[data-seq]').forEach(sec => {
      const stage = $('.x-seq-stage', sec), slides = $$('.x-seq-copy>*', sec);
      slides.forEach(s => s.classList.remove('on'));
      G.set(slides, { autoAlpha: 0, y: 22 });
      const per = () => Math.max(420, Math.round(innerHeight * .55));
      const tl = G.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: stage, start: 'center center', end: () => '+=' + per() * slides.length, pin: stage, scrub: .65, invalidateOnRefresh: true, refreshPriority: prio(sec) } });
      slides.forEach((s, i) => {
        tl.fromTo(s, { autoAlpha: 0, y: 22 }, { autoAlpha: 1, y: 0, duration: .22, ease: 'power2.out' }, i);
        if (i < slides.length - 1) tl.to(s, { autoAlpha: 0, y: -22, duration: .22, ease: 'power2.in' }, i + 1 - .22);
      });
      tl.set({}, {}, slides.length);
    });

    /* 3) Grifo inteligente: secuencia de 224 cuadros */
    $$('[data-fau]').forEach(sec => {
      const f = fau(sec); if (!f) return;
      const state = { frame: 0 };
      G.timeline({ scrollTrigger: { trigger: sec, start: 'top top', end: '+=260%', pin: $('.x-fau-stage', sec), scrub: .5, invalidateOnRefresh: true, refreshPriority: prio(sec) } })
        .to(state, { frame: f.count - 1, ease: 'none', snap: 'frame', onUpdate: () => f.draw(Math.round(state.frame)) });
    });

    /* 4) Bajo el fregadero: la escena aparece y luego el texto */
    mm.add('(min-width: 1025px)', () => {
      $$('[data-us]').forEach(sec => {
        const img = $('.x-us-img', sec), copy = $('.x-us-copy', sec);
        G.set(img, { yPercent: 10, scale: 1.08, autoAlpha: .35 });
        G.set(copy, { top: '50%', autoAlpha: 0 });
        G.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: sec, start: 'top top', end: '+=120%', scrub: 1, pin: true, anticipatePin: 1, invalidateOnRefresh: true, refreshPriority: prio(sec) } })
          .to(img, { yPercent: 0, scale: 1, autoAlpha: 1, duration: .5 }, 0)
          .to(copy, { top: '30%', autoAlpha: 1, duration: 1 }, .5);
      });
    });

    /* 5) Gota que crece sobre el video y revela el pH (como waterdropfilter.com) */
    mm.add('(min-width: 1025px)', () => {
      $$('[data-drop]').forEach(sec => {
        const stage = $('.x-drop-stage', sec), shape = $('.x-drop-shape', sec), c = $('.x-drop-c', sec), fill = $('.x-drop-bar i', sec), val = $('.x-drop-val', sec);
        const target = +(sec.dataset.ph || 7.5), st = { v: 0 };
        G.set(shape, { width: 0 }); G.set(c, { autoAlpha: 0, y: 30 }); G.set(fill, { width: 0 });
        G.timeline({ scrollTrigger: { trigger: sec, start: 'top top', end: '+=200%', pin: stage, scrub: .6, invalidateOnRefresh: true, refreshPriority: prio(sec) } })
          .to(shape, { width: () => innerWidth * 1.6, duration: 3, ease: 'power2.inOut' })
          .to(c, { autoAlpha: 1, y: 0, duration: 1, ease: 'power2.out' }, '-=0.9')
          .to(fill, { width: (target / 14 * 100) + '%', duration: 1, ease: 'power1.out' }, '<0.2')
          .to(st, { v: target, duration: 1, ease: 'power1.out', onUpdate: () => { if (val) val.textContent = 'pH ' + st.v.toFixed(1) + '±'; } }, '<');
      });
    });

    /* 6) Burbujas que flotan a distinta velocidad */
    $$('.x-bub img').forEach((b, i) => {
      G.to(b, { yPercent: [-60, 40, -30, 70, -45][i % 5], rotate: [8, -10, 6, -6, 12][i % 5], ease: 'none',
        scrollTrigger: { trigger: b.closest('.x-bub'), start: 'top bottom', end: 'bottom top', scrub: 1 } });
    });

    ST.sort(); ST.refresh();
    addEventListener('load', () => ST.refresh());
  }

  /* Cuadros del grifo (carga diferida) */
  function fau(sec) {
    const cv = $('canvas', sec); if (!cv) return null;
    const ctx = cv.getContext('2d'), count = +sec.dataset.frames, base = sec.dataset.base;
    const th = (sec.dataset.thresholds || '0').split(',').map(Number);
    const copies = $$('.x-fau-copy>div', sec), steps = $$('.x-fau-steps i', sec);
    const imgs = new Array(count); let cur = 0, started = false;
    const src = i => `${base}${String(i).padStart(3, '0')}.webp`;
    const draw = i => {
      cur = i;
      let k = i; while (k > 0 && !(imgs[k] && imgs[k].complete && imgs[k].naturalWidth)) k--;
      const im = imgs[k];
      if (im && im.complete && im.naturalWidth) { ctx.clearRect(0, 0, cv.width, cv.height); ctx.drawImage(im, 0, 0, cv.width, cv.height); }
      let c = 0; th.forEach((t, n) => { if (i >= t) c = n; });
      copies.forEach((d, n) => d.classList.toggle('on', n === c)); steps.forEach((d, n) => d.classList.toggle('on', n === c));
    };
    const load = () => {
      if (started) return; started = true;
      const order = [];
      for (let s = 16; s >= 1; s = s / 2 | 0) { for (let i = 0; i < count; i += s) if (!order.includes(i)) order.push(i); if (s === 1) break; }
      let q = 0;
      const next = () => {
        if (q >= order.length) return;
        const i = order[q++], im = new Image();
        im.decoding = 'async';
        im.onload = im.onerror = () => { if (i === 0 || Math.abs(i - cur) < 16) draw(cur); next(); };
        im.src = src(i); imgs[i] = im;
      };
      for (let p = 0; p < 6; p++) next();
    };
    new IntersectionObserver((es, o) => es.forEach(en => { if (en.isIntersecting) { load(); o.disconnect(); } }), { rootMargin: '1500px 0px' }).observe(sec);
    return { count, draw };
  }
  function staticFau() { $$('[data-fau]').forEach(sec => fau(sec)); }

  /* ---------- CALCULADORA DE BOTELLONES ---------- */
  $$('[data-calc]').forEach(c => {
    const ppl = $('#c-ppl', c), bot = $('#c-bot', c), pr = $('#c-price', c);
    let prod = c.dataset.default || 'x12', botTouched = false;
    const out = k => $(`[data-o="${k}"]`, c);
    const run = () => {
      const p = +ppl.value;
      if (!botTouched) bot.value = Math.max(1, Math.round(p * .75));
      const b = Math.max(0, +bot.value || 0), price = Math.max(0, +pr.value || 0);
      const month = b * price * 52 / 12, year = b * price * 52;
      const cost = priceOf(prod), months = month > 0 ? cost / month : 0;
      out('ppl').textContent = p + (p === 1 ? ' persona' : ' personas');
      out('bot').textContent = b;
      out('year').textContent = money(year).replace('.00', '');
      out('month').textContent = money(month);
      out('jugs').textContent = Math.round(b * 52);
      out('msg').textContent = month > 0
        ? `Con lo que hoy gastas en botellones, el ${P[prod].name.replace('Waterdrop ', '')} se paga solo en unos ${months < 1 ? 'menos de 1' : Math.ceil(months)} ${months < 1 || Math.ceil(months) === 1 ? 'mes' : 'meses'}. Después, el agua pura te cuesta mucho menos.`
        : 'Ingresa cuántos botellones compran a la semana.';
      const btn = out('buy'); if (btn) { btn.dataset.add = prod; btn.textContent = `Agregar ${P[prod].name.replace('Waterdrop ', '').split(' ·')[0]} al carrito`; }
    };
    $$('[data-cp]', c).forEach(b => b.addEventListener('click', () => {
      prod = b.dataset.cp; $$('[data-cp]', c).forEach(x => x.classList.toggle('on', x === b)); run();
    }));
    ppl.addEventListener('input', run);
    bot.addEventListener('input', () => { botTouched = true; run(); });
    pr.addEventListener('input', run);
    run();
  });


  /* ---------- ESCENA INTERACTIVA (puntos sobre la cocina) ---------- */
  $$('[data-scene-wrap]').forEach(w => {
    $$('[data-scene-tab]', w).forEach(b => b.addEventListener('click', () => {
      $$('[data-scene-tab]', w).forEach(x => x.classList.toggle('on', x === b));
      $$('.x-scene', w).forEach(sc => sc.classList.toggle('on', sc.id === b.dataset.sceneTab));
      $$('.x-hot', w).forEach(h => h.classList.remove('open'));
    }));
    $$('.x-hot>button', w).forEach(b => b.addEventListener('click', e => {
      e.stopPropagation();
      const h = b.parentElement, was = h.classList.contains('open');
      $$('.x-hot', w).forEach(x => x.classList.remove('open'));
      if (!was) h.classList.add('open');
    }));
  });
  document.addEventListener('click', e => { if (!e.target.closest('.x-hot')) $$('.x-hot.open').forEach(h => h.classList.remove('open')); });

  /* ---------- ANTES / DESPUÉS ---------- */
  $$('.x-ba').forEach(ba => {
    let drag = false;
    const set = x => { const r = ba.getBoundingClientRect(); ba.style.setProperty('--p', Math.max(2, Math.min(98, (x - r.left) / r.width * 100)) + '%'); };
    ba.addEventListener('pointerdown', e => { drag = true; set(e.clientX); });
    addEventListener('pointermove', e => { if (drag) set(e.clientX); });
    addEventListener('pointerup', () => { drag = false; });
  });
  $$('[data-ba-tab]').forEach(b => b.addEventListener('click', () => {
    const g = b.closest('[data-ba]');
    $$('[data-ba-tab]', g).forEach(x => x.classList.toggle('on', x === b));
    $$('.x-ba', g).forEach(x => x.classList.toggle('on', x.id === b.dataset.baTab));
  }));

  /* ---------- BUSCADOR DE PURIFICADOR ---------- */
  const quizOv = $('#x-quiz-ov');
  if (quizOv) {
    const Q = [
      { q: '¿Dónde vives?', o: [['casa', 'Casa o departamento propio', 'Puedo instalar algo bajo el fregadero'], ['arriendo', 'Arriendo o no quiero instalar nada', 'Prefiero algo que se ponga sobre la mesa']] },
      { q: '¿Qué te preocupa más del agua?', o: [['sabor', 'El sabor y el olor a cloro', 'Quiero agua más rica para tomar y cocinar'], ['todo', 'Sarro, metales y todo lo que no se ve', 'Quiero la máxima pureza posible']] },
      { q: '¿Cuántos son en casa?', o: [['1', '1 o 2 personas', ''], ['3', '3 a 5 personas', ''], ['6', '6 o más personas', '']] }
    ];
    const box = $('#x-quiz-body', quizOv); let step = 0, ans = {};
    const pick = () => {
      if (ans[0] === 'arriendo') return ['smart', 'Sin obras ni técnicos: lo llenas, lo cargas y tienes agua filtrada en 1 segundo.'];
      if (ans[1] === 'sabor') return ['uf', 'Quita el cloro y el mal sabor conservando los minerales, sin electricidad ni desperdicio.'];
      if (ans[2] === '1') return ['g2', 'Ósmosis inversa sin tanque al mejor precio: 7 etapas y 600 GPD, ideal para hogares pequeños.'];
      if (ans[2] === '3') return ['g5', 'Ósmosis inversa con minerales alcalinos en un equipo compacto, con 700 GPD para toda la familia.'];
      return ['x12', 'El equilibrio perfecto: máxima pureza, minerales y grifo inteligente para la familia.'];
    };
    const render = () => {
      if (step < Q.length) {
        const it = Q[step];
        box.innerHTML = '<div class="x-qbar"><i style="width:' + (step / Q.length * 100) + '%"></i></div><small>Pregunta ' + (step + 1) + ' de ' + Q.length + '</small><h3>' + it.q + '</h3><div class="x-qopts">' +
          it.o.map(o => '<button type="button" data-qa="' + o[0] + '">' + o[1] + (o[2] ? '<span>' + o[2] + '</span>' : '') + '</button>').join('') + '</div>';
        $$('[data-qa]', box).forEach(b => b.addEventListener('click', () => { ans[step] = b.dataset.qa; step++; render(); }));
      } else {
        const r = pick(), id = r[0], p = P[id];
        box.innerHTML = '<div class="x-qbar"><i style="width:100%"></i></div><small>Te recomendamos</small><div class="x-qres"><img src="' + p.img + '" alt=""><div><h3 style="margin:0">' + p.name.replace('Waterdrop ', '') + '</h3><p>' + r[1] + '</p>' +
          '<div class="x-price"><span class="now">' + money(priceOf(id)) + '</span>' + (promoOn ? '<span class="was">' + money(p.was) + '</span>' : '') + '</div>' +
          '<div class="x-btns" style="margin-top:12px"><button class="x-btn x-btn-p" data-add="' + id + '">Agregar al carrito</button><a class="x-btn x-btn-o" href="' + p.url + '">Ver detalles</a></div></div></div>' +
          '<p style="margin-top:16px;font-size:13px;color:#888">¿Dudas? <a href="https://wa.me/' + WD.whatsapp + '" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline">Escríbenos por WhatsApp</a> y te asesoramos.</p>';
      }
    };
    const open = () => { step = 0; ans = {}; render(); quizOv.classList.add('open'); };
    $$('[data-quiz]').forEach(b => b.addEventListener('click', open));
    $('[data-quiz-close]', quizOv).addEventListener('click', () => quizOv.classList.remove('open'));
    quizOv.addEventListener('click', e => { if (e.target === quizOv) quizOv.classList.remove('open'); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') quizOv.classList.remove('open'); });
  }

  /* ---------- VISOR DE CERTIFICADOS ---------- */
  const cv = $('#x-cv');
  if (cv) {
    const view = $('#x-cv-view'), items = $$('.x-cv-i', cv), mobile = () => matchMedia('(max-width: 767px)').matches;
    const show = i => {
      const b = items[i]; items.forEach(x => x.classList.toggle('on', x === b));
      const src = b.dataset.src, label = b.querySelector('span').firstChild.textContent;
      if (b.dataset.type === 'pdf') {
        view.innerHTML = mobile()
          ? '<div style="text-align:center;padding:32px"><p style="margin-bottom:16px;color:#555">' + label + '</p><a class="x-btn x-btn-p" href="' + src + '" target="_blank" rel="noopener">Abrir documento PDF</a></div>'
          : '<iframe src="' + src + '#view=FitH" title="' + label + '"></iframe><a class="x-btn x-btn-p x-btn-sm x-cv-open" href="' + src + '" target="_blank" rel="noopener">Abrir en otra pestaña</a>';
      } else {
        view.innerHTML = '<img src="' + src + '" alt="' + label + '">';
      }
    };
    const open = () => { cv.classList.add('open'); document.documentElement.style.overflow = 'hidden'; if (!view.firstChild) show(0); };
    const close = () => { cv.classList.remove('open'); document.documentElement.style.overflow = ''; };
    items.forEach((b, i) => b.addEventListener('click', () => show(i)));
    $$('[data-cv-open], a[href="#certificacion"]').forEach(t => {
      t.addEventListener('click', e => { e.preventDefault(); open(); });
      t.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); open(); } });
    });
    $('[data-cv-close]', cv).addEventListener('click', close);
    cv.addEventListener('click', e => { if (e.target === cv) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
    // precarga las imágenes para que abran al instante
    addEventListener('load', () => items.forEach(b => { if (b.dataset.type === 'img') { const im = new Image(); im.src = b.dataset.src; } }));
  }

  /* ---------- SHORTS: reproducción automática silenciada ---------- */
  const ytSrc = id => 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&mute=1&loop=1&playlist=' + id + '&controls=1&playsinline=1&rel=0&modestbranding=1&enablejsapi=1';
  const ytCmd = (f, cmd) => { try { f.contentWindow.postMessage(JSON.stringify({ event: 'command', func: cmd, args: [] }), '*'); } catch (e) {} };
  const yio = new IntersectionObserver(es => es.forEach(en => {
    const box = en.target; let f = box.querySelector('iframe');
    if (en.isIntersecting) {
      if (!f) { f = document.createElement('iframe'); f.src = ytSrc(box.dataset.ytauto); f.title = box.getAttribute('aria-label') || 'Video';
        f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.setAttribute('allowfullscreen', ''); box.appendChild(f); }
      else ytCmd(f, 'playVideo');
    } else if (f) ytCmd(f, 'pauseVideo');
  }), { threshold: .35 });
  $$('[data-ytauto]').forEach(b => yio.observe(b));
  const ytCheck = () => $$('[data-ytauto]').forEach(box => {
    if (box.querySelector('iframe')) return;
    const r = box.getBoundingClientRect();
    if (r.top < innerHeight * .9 && r.bottom > innerHeight * .1) yio.unobserve(box), yio.observe(box), (box.querySelector('iframe') || (() => {
      const f = document.createElement('iframe'); f.src = ytSrc(box.dataset.ytauto); f.title = box.getAttribute('aria-label') || 'Video';
      f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.setAttribute('allowfullscreen', ''); box.appendChild(f); })());
  });
  addEventListener('scroll', () => setTimeout(ytCheck, 60), { passive: true }); setInterval(ytCheck, 800);

  /* ---------- INICIO ---------- */
  paint(); tick(); renderCart();
  setInterval(tick, 1000);
  scroll();
})();
