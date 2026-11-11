/* =========================================================
   CLUB NASFECO · Locales con descuento
   ---------------------------------------------------------
   >>> LOCALES Y CATEGORÍAS: EDITA SOLO AQUÍ <<<
   Cada local: nombre, categoria (id de la lista de categorías),
   descuento, sobre (a qué aplica), ciudad, condiciones.
   Si un local está en varias ciudades: ciudad: 'Quito, Cuenca'.
   Ficha del local: promocion (detalle de la promoción),
   descripcion (sobre el local), direccion (calle y número, para
   el mapa), imagen y logo (rutas, por ejemplo
   'assets/club/mi-local.jpg') y web (enlace). Opcional: mapa, si
   Google lo encuentra mejor con otro texto o con coordenadas.
   Quita "demo: true" cuando el local sea real: mientras exista
   uno de ejemplo, la página muestra el aviso de vista previa.
   ========================================================= */
const CLUB = {
  ciudades: ['Quito', 'Guayaquil', 'Cuenca', 'Loja'],
  categorias: [
    { id: 'gastronomia', nombre: 'Gastronomía',       icono: 'M4 3v7a3 3 0 006 0V3M7 3v18M17 3c-2 1.5-3 4-3 7s1 4 3 4v7' },
    { id: 'salud',       nombre: 'Salud',             icono: 'M12 21s-8-4.8-8-11a4.5 4.5 0 018-2.8A4.5 4.5 0 0120 10c0 6.2-8 11-8 11zM12 9v5M9.5 11.5h5' },
    { id: 'belleza',     nombre: 'Belleza y spa',     icono: 'M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z' },
    { id: 'deporte',     nombre: 'Deporte',           icono: 'M4 9v6M7 6v12M17 6v12M20 9v6M7 12h10' },
    { id: 'hogar',       nombre: 'Hogar',             icono: 'M3 11l9-8 9 8M5 9.5V21h14V9.5M10 21v-6h4v6' },
    { id: 'automotriz',  nombre: 'Automotriz',        icono: 'M4 16v-3l2-6h12l2 6v3M4 16h16M4 16v3M20 16v3M7.5 13h.01M16.5 13h.01' },
    { id: 'mascotas',    nombre: 'Mascotas',          icono: 'M12 12c-3 0-5.5 2.6-5.5 5 0 2 1.6 3 3.2 3 1 0 1.5-.5 2.3-.5s1.3.5 2.3.5c1.6 0 3.2-1 3.2-3 0-2.4-2.5-5-5.5-5zM6 10.5a1.8 2.3 0 100-.01zM18 10.5a1.8 2.3 0 100-.01zM9.5 6.5a1.8 2.4 0 100-.01zM14.5 6.5a1.8 2.4 0 100-.01z' },
    { id: 'educacion',   nombre: 'Educación',         icono: 'M2 9l10-5 10 5-10 5zM6 11.5V16c2 2 10 2 12 0v-4.5M22 9v6' },
    { id: 'turismo',     nombre: 'Hoteles y turismo', icono: 'M3 20V6M3 16h18v4M21 16v-3a3 3 0 00-3-3h-8v6M7 12.5a1.5 1.5 0 100-.01z' },
    { id: 'moda',        nombre: 'Moda',              icono: 'M9 3L3 7l2.5 4L8 9.5V21h8V9.5l2.5 1.5L21 7l-6-4c-.5 2-1.5 3-3 3s-2.5-1-3-3z' }
  ],
  locales: [
    { nombre: 'Restaurante de ejemplo', categoria: 'gastronomia', descuento: '15%', sobre: 'en toda la carta',        ciudad: 'Quito',     promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Cafetería de ejemplo',   categoria: 'gastronomia', descuento: '10%', sobre: 'en bebidas y postres',    ciudad: 'Cuenca',    promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Clínica de ejemplo',     categoria: 'salud',       descuento: '20%', sobre: 'en consultas',            ciudad: 'Guayaquil', promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Óptica de ejemplo',      categoria: 'salud',       descuento: '15%', sobre: 'en lentes',               ciudad: 'Quito',     promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Spa de ejemplo',         categoria: 'belleza',     descuento: '25%', sobre: 'en masajes',              ciudad: 'Loja',      promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Gimnasio de ejemplo',    categoria: 'deporte',     descuento: '30%', sobre: 'en la inscripción',       ciudad: 'Quito',     promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Ferretería de ejemplo',  categoria: 'hogar',       descuento: '10%', sobre: 'en toda la tienda',       ciudad: 'Cuenca',    promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Taller de ejemplo',      categoria: 'automotriz',  descuento: '15%', sobre: 'en mantenimiento',        ciudad: 'Guayaquil', promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Veterinaria de ejemplo', categoria: 'mascotas',    descuento: '20%', sobre: 'en consultas',            ciudad: 'Quito',     promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Academia de ejemplo',    categoria: 'educacion',   descuento: '15%', sobre: 'en cursos',               ciudad: 'Loja',      promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Hotel de ejemplo',       categoria: 'turismo',     descuento: '20%', sobre: 'en hospedaje',            ciudad: 'Cuenca',    promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true },
    { nombre: 'Boutique de ejemplo',    categoria: 'moda',        descuento: '10%', sobre: 'en nueva colección',      ciudad: 'Guayaquil', promocion: 'Aquí va el detalle de la promoción para los miembros del Club.', descripcion: 'Aquí va la descripción del local: qué ofrece y qué lo hace especial.', condiciones: 'Aquí van las condiciones del local.', direccion: '', imagen: '', logo: '', demo: true }
  ]
};

(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = t => String(t == null ? '' : t).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const norm = t => String(t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ico = (d, w = 22) => `<svg viewBox="0 0 24 24" width="${w}" height="${w}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${d}"/></svg>`;
  const ALL = 'M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z';

  const rail = $('#cl-rail'), out = $('#cl-out'), count = $('#cl-count'), search = $('#cl-q'), cities = $('#cl-cities');
  const cats = CLUB.categorias.filter(c => CLUB.locales.some(l => l.categoria === c.id));
  const state = { cat: 'all', q: '', city: 'all' };
  const inCity = l => state.city === 'all' || String(l.ciudad).split(',').some(c => c.trim() === state.city);
  const plural = n => `${n} ${n === 1 ? 'local' : 'locales'}`;

  /* ---------- AVISO DE VISTA PREVIA ---------- */
  if (CLUB.locales.some(l => l.demo)) $('#cl-demo').hidden = false;

  /* ---------- CATEGORÍAS ---------- */
  const chip = (id, name, d, n) => `<button type="button" class="cl-chip" data-cat="${id}" aria-pressed="false"><span class="cl-chip-i">${ico(d)}</span><span class="cl-chip-t">${esc(name)}<small>${plural(n)}</small></span></button>`;
  rail.innerHTML = chip('all', 'Todas', ALL, CLUB.locales.length) +
    cats.map(c => chip(c.id, c.nombre, c.icono, CLUB.locales.filter(l => l.categoria === c.id).length)).join('');

  /* ---------- CIUDADES ---------- */
  const cityBtn = (id, name) => `<button type="button" class="cl-city" data-city="${esc(id)}" aria-pressed="false">${esc(name)}</button>`;
  cities.innerHTML = '<span class="cl-city-ind" aria-hidden="true"></span>' + cityBtn('all', 'Todas') + CLUB.ciudades.map(c => cityBtn(c, c)).join('');
  const ind = $('.cl-city-ind', cities);
  const moveInd = () => {
    const b = $('.cl-city.on', cities);
    if (!b) return;
    ind.style.width = b.offsetWidth + 'px';
    ind.style.transform = `translateX(${b.offsetLeft}px)`;
  };

  /* ---------- TARJETAS ---------- */
  const slug = l => norm(l.nombre).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const catOf = l => CLUB.categorias.find(x => x.id === l.categoria) || {};
  const face = l => l.logo ? `<img src="${esc(l.logo)}" alt="" loading="lazy">` : `<span>${esc(l.nombre.charAt(0))}</span>`;
  const card = (l, i) => {
    const c = catOf(l);
    return `<article class="cl-loc" style="--i:${Math.min(i, 12)}">
      <div class="cl-loc-top"><div class="cl-loc-m">${face(l)}</div>${l.demo ? '<span class="cl-loc-demo">Ejemplo</span>' : ''}</div>
      <div class="cl-loc-off"><b>${esc(l.descuento)}</b><span>${esc(l.sobre)}</span></div>
      <h3>${esc(l.nombre)}</h3>
      <p class="cl-loc-meta">${ico(c.icono || ALL, 14)} ${esc(c.nombre)}<i aria-hidden="true">·</i>${esc(l.ciudad)}</p>
      <button type="button" class="cl-loc-more" data-local="${slug(l)}" aria-label="Ver el local ${esc(l.nombre)}">Ver local <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
    </article>`;
  };

  function render() {
    const q = norm(state.q).trim();
    const list = CLUB.locales.filter(l => {
      const c = CLUB.categorias.find(x => x.id === l.categoria) || {};
      return inCity(l) && (state.cat === 'all' || l.categoria === state.cat) &&
        (!q || norm([l.nombre, l.sobre, l.ciudad, c.nombre].join(' ')).includes(q));
    });
    $$('.cl-chip', rail).forEach(b => {
      const on = b.dataset.cat === state.cat;
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', on);
      const n = CLUB.locales.filter(l => inCity(l) && (b.dataset.cat === 'all' || l.categoria === b.dataset.cat)).length;
      $('small', b).textContent = plural(n);
      b.disabled = !n && !on;
    });
    $$('.cl-city', cities).forEach(b => {
      const on = b.dataset.city === state.city;
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', on);
    });
    moveInd();
    count.textContent = plural(list.length) + (state.city === 'all' ? '' : ` en ${state.city}`);
    if (!list.length) {
      out.innerHTML = `<div class="cl-empty"><h3>No encontramos locales aquí</h3><p>Prueba con otra ciudad, categoría o palabra.</p><button type="button" class="cl-btn cl-btn-o" data-reset>Ver todos los locales</button></div>`;
      return;
    }
    let n = 0;
    out.classList.toggle('one', state.cat !== 'all');
    out.innerHTML = cats.map(c => {
      const items = list.filter(l => l.categoria === c.id);
      if (!items.length) return '';
      return `<section class="cl-group" data-n="${Math.min(items.length, 4)}"><header><span>${ico(c.icono, 20)}</span><h3>${esc(c.nombre)}</h3><i aria-hidden="true"></i><small>${items.length}</small></header>
        <div class="cl-grid">${items.map(l => card(l, n++)).join('')}</div></section>`;
    }).join('');
  }

  function pick(id) {
    state.cat = id;
    render();
    const b = $(`.cl-chip[data-cat="${id}"]`, rail);
    if (b) rail.scrollTo({ left: b.offsetLeft - (rail.clientWidth - b.offsetWidth) / 2, behavior: reduce ? 'auto' : 'smooth' });
    toResults();
  }

  function toResults() {
    const bar = $('#cl-bar'), y = $('#cl-res').getBoundingClientRect().top + scrollY - bar.offsetHeight - 12;
    if (scrollY > y) scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' });
  }

  cities.addEventListener('click', e => {
    const b = e.target.closest('.cl-city');
    if (!b) return;
    state.city = b.dataset.city;
    render();
    cities.scrollTo({ left: b.offsetLeft - (cities.clientWidth - b.offsetWidth) / 2, behavior: reduce ? 'auto' : 'smooth' });
    toResults();
  });

  /* ---------- MOVER LAS CATEGORÍAS (arrastre y flechas) ---------- */
  let down = false, sx = 0, sl = 0, moved = false;
  rail.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = rail.scrollLeft; });
  addEventListener('pointermove', e => {
    if (!down) return;
    const dx = e.clientX - sx;
    if (Math.abs(dx) > 5) { moved = true; rail.classList.add('drag'); }
    if (moved) rail.scrollLeft = sl - dx;
  });
  addEventListener('pointerup', () => { down = false; rail.classList.remove('drag'); });
  rail.addEventListener('click', e => {
    if (moved) { moved = false; return; }
    const b = e.target.closest('.cl-chip');
    if (b) pick(b.dataset.cat);
  });
  $$('[data-rail]').forEach(b => b.addEventListener('click', () => rail.scrollBy({ left: +b.dataset.rail * rail.clientWidth * .7, behavior: reduce ? 'auto' : 'smooth' })));
  const edges = () => {
    const max = rail.scrollWidth - rail.clientWidth - 2;
    $('[data-rail="-1"]').disabled = rail.scrollLeft <= 2;
    $('[data-rail="1"]').disabled = rail.scrollLeft >= max;
  };
  rail.addEventListener('scroll', edges, { passive: true });
  addEventListener('resize', () => { edges(); moveInd(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(moveInd);

  /* ---------- BUSCADOR Y CONDICIONES ---------- */
  search.addEventListener('input', () => { state.q = search.value; render(); });
  out.addEventListener('click', e => {
    if (e.target.closest('[data-reset]')) { state.q = ''; state.city = 'all'; search.value = ''; pick('all'); return; }
    const m = e.target.closest('.cl-loc-more');
    if (m) openLocal(CLUB.locales.find(l => slug(l) === m.dataset.local));
  });

  /* ---------- FICHA DEL LOCAL ---------- */
  const dlg = $('#cl-d'), dBody = $('#cl-d-b');
  let cur = null;
  const PIN = 'M12 22s7-6.2 7-12a7 7 0 10-14 0c0 5.8 7 12 7 12zM12 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z';
  const mapQ = l => l.mapa || [l.direccion, l.ciudad, 'Ecuador'].filter(Boolean).join(', ');
  const mapsUrl = l => 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(mapQ(l));
  const embedUrl = l => `https://www.google.com/maps?q=${encodeURIComponent(mapQ(l))}&z=${l.direccion || l.mapa ? 16 : 12}&output=embed`;

  // El mapa es de Google y coloca cookies: igual que YouTube, solo se carga si la persona acepta (js/consent.js)
  function paintMap(l) {
    const w = $('#cl-d-mapw', dBody);
    if (!w) return;
    w.innerHTML = window.NFConsent && NFConsent.ok()
      ? `<iframe src="${esc(embedUrl(l))}" title="Mapa de ${esc(l.nombre)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
         <a class="cl-d-mapa" href="${esc(mapsUrl(l))}" target="_blank" rel="noopener" aria-label="Abrir ${esc(l.nombre)} en Google Maps"><span>${ico(PIN, 16)} Abrir en Google Maps</span></a>`
      : `<div class="cl-d-gate">${ico(PIN, 30)}<p>El mapa es de Google Maps, que usa cookies.</p><button type="button" class="cl-btn cl-btn-o" data-consent="yes">Aceptar y ver el mapa</button></div>`;
  }

  function paintLocal(l) {
    const c = catOf(l);
    dBody.innerHTML = `
      <div class="cl-d-hero">${l.imagen ? `<img src="${esc(l.imagen)}" alt="${esc(l.nombre)}">` : `<div class="cl-d-art">${ico(c.icono || ALL, 120)}</div>`}
        <span class="cl-d-cat">${ico(c.icono || ALL, 16)} ${esc(c.nombre)}</span>${l.demo ? '<span class="cl-loc-demo">Ejemplo</span>' : ''}</div>
      <div class="cl-d-in">
        <header class="cl-d-h"><div class="cl-d-logo">${face(l)}</div><div><h2 id="cl-d-t">${esc(l.nombre)}</h2><p>${ico(PIN, 15)} ${esc(l.ciudad)}</p></div></header>
        <div class="cl-d-g">
          <section class="cl-d-promo"><small>Tu promoción como miembro</small><b>${esc(l.descuento)}</b><span>${esc(l.sobre)}</span>
            ${l.promocion ? `<p>${esc(l.promocion)}</p>` : ''}${l.condiciones ? `<div class="cl-d-cond"><h3>Condiciones</h3><p>${esc(l.condiciones)}</p></div>` : ''}</section>
          <section class="cl-d-about"><h3>Sobre el local</h3>${l.descripcion ? `<p>${esc(l.descripcion)}</p>` : ''}${l.web ? `<a class="cl-d-web" href="${esc(l.web)}" target="_blank" rel="noopener">Visitar su sitio ↗</a>` : ''}</section>
        </div>
        <section class="cl-d-map"><div class="cl-d-maph"><div><h3>Dónde está</h3><p>${esc(l.direccion ? `${l.direccion}, ${l.ciudad}` : (l.demo ? `${l.ciudad} (ubicación de ejemplo)` : l.ciudad))}</p></div>
          <a class="cl-btn cl-btn-g" href="${esc(mapsUrl(l))}" target="_blank" rel="noopener">Cómo llegar</a></div>
          <div class="cl-d-mapw" id="cl-d-mapw"></div></section>
      </div>`;
    paintMap(l);
  }

  function openLocal(l) {
    if (!l) return;
    cur = l;
    paintLocal(l);
    if (!dlg.open) dlg.showModal();
    dlg.scrollTop = 0;
    history.pushState(null, '', '#local=' + slug(l));
  }

  dlg.addEventListener('close', () => {
    cur = null;
    dBody.innerHTML = '';
    if (location.hash.startsWith('#local=')) history.back();
  });
  dlg.addEventListener('click', e => { if (e.target === dlg || e.target.closest('[data-d-close]')) dlg.close(); });
  addEventListener('popstate', () => { if (dlg.open && !location.hash.startsWith('#local=')) dlg.close(); });
  document.addEventListener('nf-consent', () => { if (cur) paintMap(cur); });

  /* ---------- TARJETA DE MEMBRESÍA (se mueve con el cursor) ---------- */
  const tilt = $('[data-tilt]');
  if (tilt && !reduce && matchMedia('(hover: hover)').matches) {
    const c = $('.cl-mcard', tilt);
    tilt.addEventListener('pointermove', e => {
      const r = tilt.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      c.style.setProperty('--ry', ((x - .5) * 22).toFixed(2) + 'deg');
      c.style.setProperty('--rx', ((.5 - y) * 18).toFixed(2) + 'deg');
      c.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
      c.style.setProperty('--my', (y * 100).toFixed(1) + '%');
      tilt.classList.add('on');
    });
    tilt.addEventListener('pointerleave', () => {
      tilt.classList.remove('on');
      ['--rx', '--ry', '--mx', '--my'].forEach(p => c.style.removeProperty(p));
    });
  }

  /* ---------- APARICIÓN ---------- */
  const reveal = $$('.cl-rv');
  if (reduce || !('IntersectionObserver' in window)) reveal.forEach(e => e.classList.add('in'));
  else {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .15 });
    reveal.forEach(e => io.observe(e));
  }

  render();
  edges();

  // Enlace directo a un local: club-nasfeco#local=nombre-del-local
  const direct = location.hash.startsWith('#local=') && CLUB.locales.find(l => slug(l) === location.hash.slice(7));
  if (direct) {
    history.replaceState(null, '', location.pathname + location.search);
    openLocal(direct);
  }
})();
