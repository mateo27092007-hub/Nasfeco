/* =========================================================
   NASFECO · Cookies
   Solo almacenamiento imprescindible. YouTube y Google Ads esperan a que la persona acepte.
   Rechazar es igual de fácil que aceptar. La elección se guarda en localStorage ("nf-consent": "yes" | "no").
   ========================================================= */
(function () {
  const ADS = 'AW-18496630945';
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  const root = document.documentElement, ck = document.getElementById('ck');
  let consent = store.get('nf-consent');   // 'yes' | 'no' | null

  const showBar = on => { if (!ck) return; ck.hidden = !on; root.classList.toggle('ck-on', on); };

  // Google Ads (medición de conversiones): solo se carga con consentimiento
  let adsLoaded = false;
  function adsOn() {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    if (adsLoaded) { gtag('consent', 'update', { ad_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted', analytics_storage: 'granted' }); return; }
    adsLoaded = true;
    gtag('js', new Date()); gtag('config', ADS);
    const s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ADS; document.head.appendChild(s);
  }
  function adsOff() {
    if (adsLoaded && typeof window.gtag === 'function') gtag('consent', 'update', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied' });
    window.gtag = undefined;   // x.js comprueba "typeof gtag" antes de enviar conversiones
    // borra las cookies propias que hubiera dejado Google Ads
    document.cookie.split(';').map(c => c.split('=')[0].trim()).filter(n => /^_gcl_|^_ga/.test(n)).forEach(n => {
      [location.hostname, '.' + location.hostname.replace(/^www\./, '')].forEach(d => { document.cookie = `${n}=; Max-Age=0; path=/; domain=${d}`; });
      document.cookie = `${n}=; Max-Age=0; path=/`;
    });
  }

  function apply(v) {
    root.classList.toggle('yt-ok', v === 'yes');
    if (v === 'yes') adsOn();
    else { adsOff(); document.querySelectorAll('iframe[src*="youtube"]').forEach(f => f.remove()); }
    document.dispatchEvent(new CustomEvent('nf-consent', { detail: v }));
  }
  function set(v) { consent = v; store.set('nf-consent', v); showBar(false); apply(v); }

  window.NFConsent = { ok: () => consent === 'yes', open: () => showBar(true) };

  // se registra antes que x.js: "Aceptar y ver" acepta y, a continuación, x.js carga ese video
  document.addEventListener('click', e => {
    const c = e.target.closest('[data-consent]'); if (c) { set(c.dataset.consent); return; }
    if (e.target.closest('[data-cookie-settings]')) { e.preventDefault(); showBar(true); ck && ck.querySelector('button')?.focus({ preventScroll: true }); }
  });

  if (consent === 'yes') apply('yes');
  else if (consent !== 'no') showBar(true);
})();
