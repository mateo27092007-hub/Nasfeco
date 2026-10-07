from urllib.parse import quote as quote_url
import itertools
# -*- coding: utf-8 -*-
"""Genera las páginas Waterdrop Ecuador con la estructura de waterdropfilter.com (Serie X)."""
import os, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
WA_PATH = re.sub(r'^<path d="|"$', "", open(os.path.join(HERE, "wa_path.txt"), encoding="utf-8").read().strip())
SITE = "https://nasfeco.com/"
PRICES = {"x12": (1099, 1299), "x16": (1599, 1999), "x8": (699, 799), "uf": (189, 249), "smart": (99, 129)}
PROMO_END = "2026-10-31"

def A(name):
    """Ruta a un recurso en assets/x (usa .webp si se optimizó)."""
    base = os.path.join(ROOT, "assets", "x")
    if os.path.exists(os.path.join(base, name)): return "assets/x/" + name
    w = re.sub(r"\.(png|jpg)$", ".webp", name)
    if os.path.exists(os.path.join(base, w)): return "assets/x/" + w
    raise FileNotFoundError(name)

V = lambda vid: f"assets/x/video/{vid}.mp4"
VP = lambda vid: f"assets/x/video/{vid}-poster.jpg"

def svg(d, w=24, sw=2, fill=False):
    f = 'fill="currentColor"' if fill else f'fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    return f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" {f} aria-hidden="true"><path d="{d}"/></svg>'
I_CART = "M3 4h2l2.4 11.2a1 1 0 001 .8h9.2a1 1 0 001-.8L20 8H6.2M9 20.5a.5.5 0 11-1 0 .5.5 0 011 0zm9 0a.5.5 0 11-1 0 .5.5 0 011 0z"
I_DOWN = "M6 9l6 6 6-6"
I_RIGHT = "M9 6l6 6-6 6"
I_LEFT = "M15 6l-6 6 6 6"
I_MENU = "M4 7h16M4 12h16M4 17h16"
I_X = "M6 6l12 12M18 6L6 18"
I_COPY = "M9 9h10v10H9zM5 15V5h10"
I_PLAY = "M8 5v14l11-7z"
I_ARROW_DOWN = "M12 5v14M6 13l6 6 6-6"
I_TRUCK = "M1 4h14v12H1zM15 9h4l4 4v3h-8M5.5 20a2 2 0 100-4 2 2 0 000 4zm13 0a2 2 0 100-4 2 2 0 000 4z"
I_TOOL = "M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.8-3.8a6 6 0 01-7.9 7.9l-6.9 6.9a2.1 2.1 0 01-3-3l6.9-6.9a6 6 0 017.9-7.9z"
I_SHIELD = "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM9 12l2 2 4-4"
I_CHAT = "M21 12a8.5 8.5 0 01-12.4 7.5L3 21l1.5-5.6A8.5 8.5 0 1121 12z"
I_PIN = "M12 22s7-6.2 7-12a7 7 0 10-14 0c0 5.8 7 12 7 12zM12 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z"
WA = f'<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="{WA_PATH}"/></svg>'

# Productos sin precio publicado: se cotizan por WhatsApp.
QUOTE = {}
def wa_quote(pid):
    return "https://wa.me/593997312362?text=" + quote_url(f"Hola Nasfeco, quiero cotizar el {QUOTE[pid]}. ¿Me ayudan con el precio?")
def price(pid, cls=""):
    if pid in QUOTE: return f'<div class="x-price {cls}">{price_in(pid)}</div>'
    return f'<div class="x-price {cls}"><span class="now" data-price="{pid}"></span><span class="was" data-was="{pid}"></span><small class="x-pnote" data-note="{pid}"></small></div>'
def price_in(pid):
    if pid in QUOTE: return '<span class="now" style="font-size:22px">Consulta el precio</span><small class="x-pnote">Cotiza por WhatsApp: te respondemos al momento</small>'
    return f'<span class="now" data-price="{pid}"></span><span class="was" data-was="{pid}"></span><small class="x-pnote" data-note="{pid}"></small>'
def code(pid):
    if pid in QUOTE: return ""
    return f'<button class="x-code" data-copy="{pid}" data-promo>Código: <b data-code="{pid}"></b>{svg(I_COPY, 14)}</button>'
def buttons(pid, buy_label="Comprar ahora"):
    if pid in QUOTE: return f'<div class="x-btns"><a class="x-btn x-btn-p" href="{wa_quote(pid)}" target="_blank" rel="noopener">Cotizar por WhatsApp</a></div>'
    return f'<div class="x-btns"><button class="x-btn x-btn-p" data-add="{pid}">Agregar al carrito</button><button class="x-btn x-btn-o" data-buy="{pid}">{buy_label}</button></div>'
def cd():
    return '<span class="x-cd" data-cd data-promo>' + "".join(f'<span><b data-{k}>00</b><small>{l}</small></span>' for k, l in [("d", "Días"), ("h", "Horas"), ("m", "Min"), ("s", "Seg")]) + "</span>"
def pic(pc, mo, alt, cls="", lazy=True, w=None, h=None):
    dims = f' width="{w}" height="{h}"' if w else ""
    ld = ' loading="lazy"' if lazy else ""
    return f'<picture><source media="(max-width:767px)" srcset="{mo}"><img src="{pc}" alt="{alt}" class="{cls}"{dims}{ld}></picture>'

# =========================================================== CABECERA / PIE
def head(title, desc, canonical, og, ld):
    canonical = canonical.replace(".html", "")
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18496630945"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','AW-18496630945');</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/x.css?v=32">
</head>
<body>
'''

def offer_ld(pid, name, desc, imgs, url):
    if pid in QUOTE:
        return {"@type": "Product", "name": name, "description": desc, "brand": {"@type": "Brand", "name": "Waterdrop"}, "image": [SITE + i for i in imgs]}
    now, was = PRICES[pid]
    return {"@type": "Product", "name": name, "description": desc, "brand": {"@type": "Brand", "name": "Waterdrop"},
            "image": [SITE + i for i in imgs],
            "offers": {"@type": "Offer", "url": SITE + url.replace(".html", ""), "priceCurrency": "USD", "price": f"{now:.2f}",
                       "priceValidUntil": PROMO_END, "availability": "https://schema.org/InStock",
                       "seller": {"@type": "Organization", "name": "Nasfeco S.A."}}}

MEGA = [
    ("product-x12.html", "assets/x12/ui-wd-x12-new-vis-pr-logo.webp", "Waterdrop X12", "1200 GPD, el más completo"),
    ("product-g5p700a.html", "assets/g5/ui-wd-g5p700a-product.webp", "Waterdrop G5P700A", "700 GPD, alcalino"),
    ("product-g2p600.html", "assets/g2/WD-G2P600-W-NSF.webp", "Waterdrop G2P600", "600 GPD, mejor precio"),
    ("product-uf.html", "assets/uf/10UB-UF-NSF.png", "Ultrafiltración UF", "Sin electricidad"),
    ("product-smart.html", "assets/ed01/1_33c5e044-eb97-4485-ae99-684bc658886e.webp", "Dispensador ED01", "Sin instalación"),
]

LOGO_SVG = '<svg viewBox="0 0 200 40" width="{w}" height="{h}" aria-label="Nasfeco S.A." role="img"><g transform="translate(5,5)"><path d="M5 5 L25 15 L5 25 Z" stroke="url(#lg{uid})" stroke-width="4.5" stroke-linejoin="round" fill="none"/><circle cx="5" cy="5" r="5" fill="#10B981"/><circle cx="25" cy="15" r="5" fill="#059669"/><circle cx="5" cy="25" r="5" fill="#00B4D8"/></g><text x="45" y="26" font-family="Times New Roman, serif" font-weight="bold" font-size="22" fill="currentColor" letter-spacing="1">NASFECO S.A</text><defs><linearGradient id="lg{uid}" x1="5" y1="5" x2="25" y2="25" gradientUnits="userSpaceOnUse"><stop offset="0%" stop-color="#10B981"/><stop offset="100%" stop-color="#00B4D8"/></linearGradient></defs></svg>'
_LG = itertools.count()
_SEAL = itertools.count()
def seal(where):
    """Sello giratorio de NASFECO. where: 'hero' (portada de la tienda) o 'gal' (foto principal de un producto)."""
    k = next(_SEAL)
    mark = ('<svg class="s-mark" viewBox="0 0 40 40" aria-hidden="true"><g transform="translate(5,5)">'
            f'<path d="M5 5 L25 15 L5 25 Z" stroke="url(#sg{k})" stroke-width="4.5" stroke-linejoin="round" fill="none"/>'
            '<circle cx="5" cy="5" r="5" fill="#10B981"/><circle cx="25" cy="15" r="5" fill="#059669"/><circle cx="5" cy="25" r="5" fill="#00B4D8"/></g>'
            f'<defs><linearGradient id="sg{k}" x1="5" y1="5" x2="25" y2="25" gradientUnits="userSpaceOnUse"><stop offset="0%" stop-color="#10B981"/><stop offset="100%" stop-color="#00B4D8"/></linearGradient></defs></svg>')
    # El anillo con el texto es un <svg> propio y gira entero (animación en la GPU, no depende del resto de la página).
    return (f'<div class="seal-n hw-seal hw-seal-{where}" aria-hidden="true"><svg class="s-ring" viewBox="0 0 200 200">'
            f'<defs><path id="sp{k}" d="M100,100 m-80,0 a80,80 0 1,1 160,0 a80,80 0 1,1 -160,0"/></defs>'
            '<circle cx="100" cy="100" r="64" class="s-in"/>'
            f'<text><textPath href="#sp{k}" textLength="498">NASFECO · DISTRIBUIDOR EXCLUSIVO OFICIAL · WATERDROP ECUADOR · </textPath></text>'
            f'</svg>{mark}</div>')

def nf_logo(sub=True):
    w, h = (150, 30) if sub else (120, 24)
    return '<span class="nf-logo">' + LOGO_SVG.format(w=w, h=h, uid=next(_LG)) + '</span>'


def wd_brand():
    return '<a href="waterdrop.html" class="wd-brand"><img class="wd-logo" src="assets/brand/waterdrop-logo.png" alt="Waterdrop" width="140" height="27"><em><b>ECUADOR</b>Distribuidor exclusivo oficial</em></a>'

I_TRUCK2 = I_TRUCK
def trust():
    items = [(I_SHIELD, "Distribuidor exclusivo oficial", "Waterdrop Filter en Ecuador"), (I_TOOL, "Instalación profesional", "Quito, Guayaquil, Cuenca y Loja"),
             (I_CHAT, "Garantía local", "Respaldo de Nasfeco S.A."), (I_TRUCK2, "Ecuador y Miami, Florida", "Presencia en Ecuador y EE. UU.")]
    it = "".join(f"<div><i>{svg(i, 20, 1.8)}</i><p><b>{t}</b><span>{d}</span></p></div>" for i, t, d in items)
    return f'<section class="x-trust"><div class="x-wrap">{it}</div></section>'

def top(subnav=None, side=None):
    mega = "".join(f'<a href="{u}"><img src="{i}" alt="" loading="lazy">{t}<small>{s}</small></a>' for u, i, t, s in MEGA)
    mega += '<button type="button" class="x-mega-side" data-quiz><small>¿No sabes cuál elegir?</small><b>Responde 3 preguntas y te recomendamos uno →</b></button>'
    mnav = "".join(f'<a href="{u}"><img src="{i}" alt="" loading="lazy">{t}</a>' for u, i, t, s in MEGA)
    out = f'''
<div class="x-group">
  <div class="x-wrap">
    <div class="x-group-l">
      <a href="index.html">{nf_logo(False)}</a>
      <a href="nasfeco.html">Empresas</a>
      <a href="waterdrop.html" class="on">Waterdrop Hogar</a>
    </div>
    <div class="x-group-r"><b style="color:var(--gold-d)">Distribuidor exclusivo oficial de Waterdrop Filter</b> · Ecuador y Miami, Florida (EE. UU.) · WhatsApp +593 99 731 2362</div>
  </div>
</div>
<div class="x-ann" data-promo>
  <div class="x-wrap">
    <span class="tag" data-promo-name></span>
    <span>Purificadores con hasta <b data-maxoff></b> de descuento</span>
    <a href="waterdrop.html#ofertas">Ver ofertas {svg(I_RIGHT, 14)}</a>
    {cd()}
  </div>
</div>
<header class="x-header">
  <div class="x-wrap">
    {wd_brand()}
    <ul class="x-nav">
      <li><a href="waterdrop.html#ofertas">Purificadores {svg(I_DOWN, 12)}</a><div class="x-mega">{mega}</div></li>
      <li><a href="waterdrop.html#ahorro">Calcula tu ahorro</a></li>
      <li><a href="repuestos">Repuestos</a></li>
      <li><a href="waterdrop.html#contacto">Contacto</a></li>
      <li><a href="#" data-quiz class="cta" onclick="return false">Encuentra tu purificador</a></li>
    </ul>
    <div class="x-icons">
      <button class="x-icon" data-open-cart aria-label="Carrito">{svg(I_CART, 22, 1.6)}<span class="x-count">0</span></button>
      <button class="x-icon x-burger" data-menu aria-label="Menú">{svg(I_MENU, 22, 1.8)}</button>
    </div>
  </div>
</header>
<nav class="x-mnav" id="x-mnav" aria-label="Menú móvil">
  <div class="x-mnav-top">{wd_brand()}<button class="x-icon" data-menu-close aria-label="Cerrar">{svg(I_X, 22)}</button></div>
  {mnav}
  <a href="repuestos">Filtros de repuesto</a>
  <a href="#" data-quiz onclick="return false">Encuentra tu purificador</a>
  <a href="waterdrop.html#ahorro">Calcula tu ahorro</a>
  <a href="waterdrop.html#servicio">Servicio Nasfeco</a>
  <a href="waterdrop.html#contacto">Contacto</a>
  <a href="nasfeco.html">Nasfeco Empresas →</a>
  <a href="index.html">← Inicio Nasfeco</a>
</nav>'''
    if subnav:
        name, links, pid = subnav
        ls = "".join(f'<a href="{h}">{t}</a>' for h, t in links)
        out += f'''
<div class="x-subnav"><div class="x-wrap"><b>{name}</b><nav>{ls}{f'<a href="{wa_quote(pid)}" target="_blank" rel="noopener" class="x-btn x-btn-p x-btn-sm">Cotizar</a>' if pid in QUOTE else '<a href="#comparar" class="x-btn x-btn-p x-btn-sm">Comprar ahora</a>'}</nav></div></div>'''
    if side:
        out += '<aside class="x-side" aria-label="Secciones"><div class="x-side-rail">' + "".join("<i></i>" for _ in side) + '</div><ul>' + \
               "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in side) + '</ul></aside>'
    return out

def bottom(extra=""):
    return f'''
<footer class="x-foot">
  <div class="x-wrap">
    <div class="x-foot-g">
      <div>{nf_logo()}
        <p>Nasfeco es una empresa de servicios en agua y energía para hogares y empresas, y <b style="color:#fff">distribuidor exclusivo oficial de Waterdrop Filter en Ecuador</b>: equipos originales, garantía y repuestos con respaldo local.</p></div>
      <div><h4>Purificadores</h4>
        <a href="product-x12.html">Waterdrop X12</a><a href="product-g5p700a.html">Waterdrop G5P700A</a><a href="product-g2p600.html">Waterdrop G2P600</a><a href="product-uf.html">Ultrafiltración UF</a><a href="product-smart.html">Dispensador ED01</a><a href="waterdrop.html#comparar">Comparar modelos</a></div>
      <div><h4>Servicio Nasfeco</h4>
        <a href="repuestos">Filtros de repuesto</a><a href="waterdrop.html#faq">Preguntas frecuentes</a><a href="waterdrop.html#contacto">Agendar instalación</a>
        <a href="https://wa.me/593997312362?text=Hola%2C%20necesito%20soporte%20t%C3%A9cnico%20con%20mi%20equipo%20Waterdrop" target="_blank" rel="noopener">Soporte técnico</a><a href="nasfeco.html">Soluciones para empresas</a></div>
      <div><h4>Contacto</h4><p style="margin-bottom:10px"><a href="purificadores-agua-quito">Quito</a> · <a href="purificadores-agua-guayaquil">Guayaquil</a> · <a href="purificadores-agua-cuenca">Cuenca</a> · <a href="purificadores-agua-loja">Loja</a></p><p style="margin-bottom:8px">Miami, Florida (EE. UU.)</p><p style="margin-bottom:8px">Ecuador: Quito, Guayaquil, Cuenca y Loja · Trabajamos en todo el país</p><p>WhatsApp: +593 99 731 2362</p></div>
    </div>
    <div class="x-foot-b"><span>&copy; 2026 Nasfeco · Ecuador. Nasfeco, distribuidor exclusivo oficial de Waterdrop Filter en Ecuador. Waterdrop es una marca registrada de su fabricante.</span><span>Creado por <strong>Mateo Perez</strong></span></div>
  </div>
</footer>
<a href="https://wa.me/593997312362?text=Hola%20Nasfeco%2C%20quiero%20informaci%C3%B3n%20sobre%20los%20purificadores" target="_blank" rel="noopener" class="x-wa" aria-label="Escríbenos por WhatsApp">{WA}</a>
<div class="x-cart-ov" id="x-cart-ov"></div>
<aside class="x-cart" id="x-cart" aria-label="Carrito">
  <div class="x-cart-h"><h3>Tu carrito</h3><button class="x-icon" data-close-cart aria-label="Cerrar">{svg(I_X, 20)}</button></div>
  <div class="x-cart-promo" data-promo><span data-promo-name></span>{cd()}</div>
  <div class="x-cart-items" id="x-cart-items"></div>
  <div class="x-cart-f">
    <div class="x-cart-row"><span>Precio normal</span><span id="x-cart-sub">$0.00</span></div>
    <div class="x-cart-row save" id="x-cart-save-row"><span>Descuento</span><span id="x-cart-save">$0.00</span></div>
    <div class="x-cart-row tot"><span>Total</span><span id="x-cart-tot">$0.00</span></div>
    <button class="x-btn x-btn-wa x-btn-block" id="x-checkout">{WA} Finalizar pedido por WhatsApp</button>
    <p class="x-cart-note">Precios finales: incluyen IVA e instalación (el ED01 no incluye envío). Recibimos tu pedido por WhatsApp y confirmamos disponibilidad, envío, instalación y forma de pago.</p>
  </div>
</aside>
<div class="x-quiz-ov" id="x-quiz-ov" role="dialog" aria-modal="true" aria-label="Encuentra tu purificador">
  <div class="x-quiz"><button class="x-icon" data-quiz-close aria-label="Cerrar">{svg(I_X, 20)}</button><div id="x-quiz-body"></div></div>
</div>
<script src="js/vendor/gsap.min.js"></script>
<script src="js/vendor/ScrollTrigger.min.js"></script>
<script src="js/x.js?v=32"></script>
{extra}
</body>
</html>
'''

# =========================================================== SECCIONES
def banner(title, sub, metrics, bg=None, prod=None, btns="", card=False, extra=""):
    m = "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in metrics)
    bgh = f'<div class="x-banner-bg">{pic(bg[0], bg[1], "", lazy=False)}</div>' if bg else '<div class="x-banner-bg"></div>'
    ph = f'<div class="x-banner-prod{" card" if card else ""}"><img src="{prod}" alt=""></div>' if prod else ""
    return f'''
<section class="x-banner">
  <div class="x-banner-in">
    {bgh}{ph}{extra}
    <div class="x-wrap"><div class="x-banner-c">
      <h1>{title}</h1><p>{sub}</p>
      <div class="x-metrics">{m}</div>{btns}
    </div></div>
  </div>
</section>''' + trust()

PICKS = {
    "x12": ("1200 GPD", "Sistema RO X12", "El equilibrio perfecto para la mayoría de familias", A("X__X12-pc.jpg"), A("X__X12-mo.jpg")),
    "x16": ("1600 GPD", "Sistema RO X16", "Máximo caudal para familias grandes y cocinas que no paran", A("X__X16-_1164x760_76074c3c-2a99-401c-8fef-8f18a43a5ce3.jpg"), A("X__X16-_900x1200_e6fe65b9-20d5-47cc-a243-bde6337ad1f2.jpg")),
    "x8": ("800 GPD", "Sistema RO X8", "La forma más accesible de tener ósmosis inversa en casa", A("X__X8-pc.jpg"), A("X__X8-mo.jpg")),
    "uf": ("Sin electricidad", "Ultrafiltración UF", "Agua limpia que conserva sus minerales, sin gastar luz", "assets/uf-gal-1.png.png", None),
    "smart": ("Sin instalación", "Dispensador ED01", "Ideal para departamentos y arriendos: cero instalación", "assets/smart-gal-1.png.jpg", None),
}
def pick(pid):
    gpd, name, tag, pc, mo = PICKS[pid]
    img = pic(pc, mo, name) if mo else f'<img src="{pc}" alt="{name}" loading="lazy">'
    return f'''<article class="x-pick{'' if mo else ' plain'}">{img}
      <div class="x-pick-c"><span class="gpd">{gpd}</span><h3>{name}</h3><p>{tag}</p>
        <div class="x-price">{price_in(pid)}{code(pid)}</div>{buttons(pid)}</div></article>'''
def picks(ids, title="Ofertas de la temporada", sub="Precios finales en dólares: incluyen IVA e instalación. Trabajamos en todo el Ecuador, con instalación en Quito, Guayaquil, Cuenca y Loja.", sid="ofertas"):
    return f'''
<section class="x-sec" id="{sid}">
  <div class="x-wrap">
    <div class="x-head x-rv"><h2 class="x-h2">{title}</h2><p class="x-lead">{sub}</p></div>
    <div class="x-car x-rv" data-car>
      <button class="x-arrow prev" aria-label="Anterior">{svg(I_LEFT, 16)}</button>
      <div class="x-car-track">{"".join(pick(i) for i in ids)}</div>
      <button class="x-arrow next" aria-label="Siguiente">{svg(I_RIGHT, 16)}</button>
    </div>
  </div>
</section>'''

def hl_card(href, pc, mo, title):
    return f'<a href="{href}" class="x-hl-card x-rv">{pic(pc, mo, title.replace("<br>", " "))}<h3>{title}</h3><span class="go">{svg(I_ARROW_DOWN, 14, 2.5)}</span></a>'

def problems(items, title="¿Te preocupan estos problemas?"):
    cards = "".join(f'<div class="x-prob x-rv"><img src="{img}" alt="{h}" loading="lazy"><div><h3>{h}</h3><p>{p}</p></div></div>' for img, h, p in items)
    return f'''
<section class="x-sec">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">{title}</h2></div><div class="x-probs">{cards}</div></div>
</section>'''

def flow(title, sub, pc_vid, mo_vid, sid="", cap=""):
    return f'''
<section class="x-flow" data-flow{f' id="{sid}"' if sid else ""}>
  <div class="x-flow-stage">
    <div class="x-flow-head"><h2>{title}</h2><p>{sub}</p></div>
    <div class="x-flow-media">
      <video class="pc" data-auto muted loop playsinline preload="none" poster="{VP(pc_vid)}"><source src="{V(pc_vid)}" type="video/mp4"></video>
      <video class="mo" data-auto muted loop playsinline preload="none" poster="{VP(mo_vid)}"><source src="{V(mo_vid)}" type="video/mp4"></video>
      {f'<div class="x-flow-cap">{cap}</div>' if cap else ""}
    </div>
  </div>
</section>'''

def speed(title, sub, items):
    f = "".join(f'<figure class="x-rv"><img src="{A(img)}" alt="{t}" loading="lazy"><figcaption><b>{n}</b><span>{t}</span></figcaption></figure>' for img, n, t in items)
    return f'''
<section class="x-sec">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">{title}</h2><p class="x-lead">{sub}</p></div><div class="x-speed">{f}</div></div>
</section>'''

def press():
    Q = [
        ("Bob Vila", A("wd-product-1016-page-media-icon-5.png"), 'El sistema de filtración <a href="https://www.bobvila.com/articles/waterdrop-x-series-launch/" target="_blank" rel="noopener">Waterdrop Serie X</a> tiene una eficiente relación de agua 3:1 que ayuda a conservar los recursos hídricos. (En comparación, otros RO sin tanque suelen rondar 1.5:1 o 2:1).'),
        ("WIRED", A("WIRED_logo_vector_-_Download_logo_WIRED_magazine_vector_logoeps.png"), '<a href="https://www.wired.com/live/amazon-prime-day-deals-october-25/?id=686cfc2328c790229f9020bf" target="_blank" rel="noopener">Este sistema</a> va un paso más allá con esterilización UV, un medidor de TDS integrado en el propio grifo y un cartucho de remineralización que asegura un agua perfectamente alcalina de pH 7.5.'),
        ("House Digest", A("Tempaper_in_the_Press.png"), 'Mientras la mayoría de filtros RO abastecen un solo grifo, <a href="https://www.housedigest.com/1982178/waterdrop-x12-pro-reverse-osmosis-filter-review/" target="_blank" rel="noopener">el X12 Pro</a> también puede llevar agua filtrada al lavavajillas, al suministro de agua fría del fregadero o a una máquina de hielo.'),
        ("New York Post", A("New_York_Post.png"), 'Entre el grifo inteligente, el pH equilibrado, la esterilización UV y su diseño elegante, <a href="https://nypost.com/shopping/waterdrop-water-filter-review/" target="_blank" rel="noopener">el Waterdrop X12</a> se siente como el futuro de la hidratación en casa.'),
        ("Wirecutter", A("Wirecutter3.png"), 'El Waterdrop X12 es un sistema bajo fregadero sin tanque y de alta capacidad, de uno de los fabricantes de filtros de ósmosis inversa más conocidos. Su gran capacidad diaria le permite entregar agua más rápido que los sistemas de menor capacidad.'),
    ]
    qs = "".join(f'<p class="{"on" if i == 0 else ""}">“{q}”</p>' for i, (_, _, q) in enumerate(Q))
    ls = "".join(f'<button class="{"on" if i == 0 else ""}" data-q="{i}" aria-label="{n}"><img src="{l}" alt="{n}" loading="lazy"></button>' for i, (n, l, _) in enumerate(Q))
    return f'''
<section class="x-sec">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Reconocido por la prensa internacional</h2><p class="x-lead">Medios de Estados Unidos que probaron los equipos Waterdrop que distribuimos en Ecuador.</p></div>
    <div class="x-press x-rv" data-press><div class="x-quote">{qs}</div><div class="x-logos">{ls}</div><small>Fragmentos traducidos del inglés. Toca el enlace para leer cada artículo original.</small></div>
  </div>
</section>'''

def faq(items, title="Preguntas frecuentes", lead="Lo que más nos preguntan antes de comprar. Si tu duda no está aquí, escríbenos por WhatsApp y te respondemos.", sid="faq"):
    q = "".join(f'<details><summary>{a}<i></i></summary><p>{b}</p></details>' for a, b in items)
    return f'''
<section class="x-sec pb" id="{sid}">
  <div class="x-wrap x-faq">
    <div class="x-faq-l x-rv"><h2>{title}</h2><p>{lead}</p>
      <a href="https://wa.me/593997312362?text=Hola%2C%20tengo%20una%20pregunta%20sobre%20los%20purificadores%20Waterdrop" target="_blank" rel="noopener" class="x-btn x-btn-k">Contáctanos</a></div>
    <div class="x-rv">{q}</div>
  </div>
</section>'''

def cmp_cats(hl):
    cols = [("x12", "assets/x12/ui-wd-x12-new-vis-pr-logo.webp", "Waterdrop X12", "product-x12.html",
             [("Tecnología", "Ósmosis inversa + remineralización"), ("Filtrado", "0.0001 μm · 11 etapas"), ("Instalación", "Bajo el fregadero, sin tanque"), ("Ideal para", "Familias que quieren máxima pureza y caudal")]),
            ("g5", "assets/g5/ui-wd-g5p700a-product.webp", "Waterdrop G5P700A", "product-g5p700a.html",
             [("Tecnología", "Ósmosis inversa + minerales alcalinos"), ("Filtrado", "0.0001 μm · 8 etapas"), ("Instalación", "Bajo el fregadero, sin tanque"), ("Ideal para", "Agua alcalina a mejor precio")]),
            ("g2", "assets/g2/WD-G2P600-W-NSF.webp", "Waterdrop G2P600", "product-g2p600.html",
             [("Tecnología", "Ósmosis inversa"), ("Filtrado", "0.0001 μm · 7 etapas"), ("Instalación", "Bajo el fregadero, sin tanque"), ("Ideal para", "Ósmosis inversa al mejor precio")]),
            ("uf", "assets/uf/10UB-UF-NSF.png", "Ultrafiltración UF", "product-uf.html",
             [("Tecnología", "Membrana de ultrafiltración"), ("Filtrado", "0.01 μm · conserva minerales"), ("Instalación", "Bajo el fregadero, sin electricidad"), ("Ideal para", "Agua de red en buen estado")]),
            ("smart", "assets/smart-gal-1.png.jpg", "Dispensador ED01", "product-smart.html",
             [("Tecnología", "Filtración eléctrica de alta densidad"), ("Filtrado", "5 μm · 35+ contaminantes"), ("Instalación", "Ninguna: sobre la mesa"), ("Ideal para", "Departamentos, oficinas y arriendos")])]
    out = ""
    for pid, img, name, url, rows in cols:
        r = "".join(f'<div class="x-row" style="min-height:0"><label>{a}</label><b>{b}</b></div>' for a, b in rows)
        out += f'''<div class="x-cmp-col{' hl' if pid == hl else ''}"><a href="{url}"><img src="{img}" alt="{name}" loading="lazy"><h3>{name}</h3></a>
          {price(pid)}<span class="x-off" data-off="{pid}"></span>{buttons(pid)}{r}
          <a href="{url}" class="x-btn x-btn-k x-btn-sm" style="margin-top:20px">Ver detalles</a></div>'''
    return f'''
<section class="x-sec" id="comparar">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Cinco equipos, uno para cada hogar</h2><p class="x-lead">Todos quitan el cloro y el mal sabor. Cambia cuánto purifican, dónde van y si necesitan instalación.</p></div>
    <div class="x-cmp x-rv"><div class="x-cmp-g" style="--n:5">{out}</div></div></div>
</section>'''

def nature():
    return f'''
<section class="x-sec" id="sostenible">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Menos plástico en Ecuador</h2><p class="x-lead">Una familia que deja los botellones evita cientos de envases al año. Y la Serie X aprovecha 3 litros de agua pura por cada litro que desecha.</p></div>
  <div class="x-nature x-rv">
    <img class="pc" src="{A("huanbaobankuai-1.jpg")}" alt="Relación 3:1 de agua pura" loading="lazy">
    <img class="mo" src="{A("Nature_s_Friend_Your_Choice-mo_1.jpg")}" alt="Relación 3:1 de agua pura" loading="lazy">
  </div></div>
</section>'''

PERKS = f'''<div class="x-perks">
  <div>{svg(I_TRUCK, 18, 1.8)} Envío a todo Ecuador</div><div>{svg(I_TOOL, 18, 1.8)} Instalación en 4 ciudades</div>
  <div>{svg(I_SHIELD, 18, 1.8)} Garantía y soporte local</div><div>{svg(I_CHAT, 18, 1.8)} Asesoría gratuita</div></div>
<p class="x-excl">{svg(I_SHIELD, 16, 2)} Equipo original vendido por Nasfeco, distribuidor exclusivo oficial de Waterdrop Filter en Ecuador.</p>'''

# ---- Secciones propias de Nasfeco ----
I_SEARCH = "M11 19a8 8 0 100-16 8 8 0 000 16zM21 21l-4.3-4.3"
I_BELL = "M18 8a6 6 0 00-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 01-3.4 0"

def calc(default="x12", options=("x8", "x12", "x16", "uf")):
    labels = {"x8": "X8", "x12": "X12", "x16": "X16", "g5": "G5P700A", "g2": "G2P600", "uf": "UF", "smart": "ED01"}
    seg = "".join(f'<button type="button" class="{"on" if o == default else ""}" data-cp="{o}">{labels[o]}</button>' for o in options)
    return f'''
<section class="x-sec" id="ahorro">
  <div class="x-wrap">
    <div class="x-head x-rv"><h2 class="x-h2">¿Cuánto gastas hoy en botellones?</h2><p class="x-lead">Haz la cuenta en 10 segundos y compara lo que gastas hoy con lo que cuesta tener agua pura en tu propia cocina.</p></div>
    <div class="x-calc x-rv" data-calc data-default="{default}">
      <div class="x-calc-in">
        <h3>Tu consumo actual</h3><p>Ajusta los valores a lo que compras normalmente.</p>
        <div class="x-cf"><label for="c-ppl">Personas en casa <output data-o="ppl"></output></label><input type="range" id="c-ppl" min="1" max="10" value="4"></div>
        <div class="x-cf"><label for="c-bot">Botellones de 20 L por semana <output data-o="bot"></output></label><input type="number" id="c-bot" min="0" max="30" step="1" value="3"></div>
        <div class="x-cf"><label for="c-price">Precio por botellón (USD)</label><input type="number" id="c-price" min="0" max="20" step="0.25" value="2.50"></div>
        <div class="x-cf"><label>Compararlo con</label><div class="x-seg">{seg}</div></div>
      </div>
      <div class="x-calc-out">
        <div><small>Gastas en botellones al año</small><b data-o="year">$0</b></div>
        <div class="row"><div><small>Al mes</small><b data-o="month">$0</b></div><div><small>Botellones de plástico al año</small><b data-o="jugs">0</b></div></div>
        <p data-o="msg"></p>
        <button class="x-btn" data-o="buy" data-add="{default}">Agregar al carrito</button>
      </div>
    </div>
    <p class="x-calc-note">Cálculo referencial. No incluye el costo de los filtros de repuesto, que dependen del modelo y del consumo.</p>
  </div>
</section>'''

def servicio(video=True):
    items = [(I_CHAT, "Te asesoramos antes de comprar", "Nos cuentas cómo es tu casa y tu consumo, y te recomendamos el equipo que realmente necesitas. Sin compromiso."),
             (I_TOOL, "Instalamos en tu casa", "Técnicos de Nasfeco instalan el equipo en Quito, Guayaquil, Cuenca y Loja, revisan conexiones y te enseñan a usarlo."),
             (I_SHIELD, "Soporte local de verdad", "Si algo pasa, hablas con una empresa ecuatoriana, no con un call center en otro país. Garantía gestionada por Nasfeco.")]
    cards = "".join(f'<div class="x-rv"><i>{svg(ic, 24, 1.8)}</i><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in items)
    vid = f'''
    <div class="x-mt" style="margin-top:64px">
      <div class="x-yt x-rv" data-yt="Po-mlA68pKI" role="button" tabindex="0" aria-label="Ver video de instalación"><img src="https://i.ytimg.com/vi/Po-mlA68pKI/hqdefault.jpg" alt="Video de instalación de la Serie X" loading="lazy"><span class="play">{svg(I_PLAY, 22, 2, True)}</span></div>
      <div class="x-rv"><p class="x-eyebrow">Instalación</p><h2>Sin obras, sin perforar paredes</h2>
        <p>La Serie X se conecta a la toma de agua fría del fregadero. Nuestros técnicos la dejan funcionando en una visita y, si estás en otra ciudad, te acompañamos por WhatsApp para que la instales tú mismo con la guía incluida.</p></div>
    </div>''' if video else ""
    return f'''
<section class="x-sec" id="servicio">
  <div class="x-wrap">
    <div class="x-head x-rv"><p class="x-eyebrow" style="text-align:center">Servicio Nasfeco</p><h2 class="x-h2">Comprar es solo el comienzo</h2><p class="x-lead">Como distribuidor exclusivo oficial de Waterdrop Filter en Ecuador, Nasfeco se encarga de que tu equipo funcione en casa durante años.</p></div>
    <div class="x-svc">{cards}</div>{vid}
  </div>
</section>'''

def b2b():
    return f'''
<section class="x-sec">
  <div class="x-wrap">
    <div class="x-b2b x-rv">
      <div><p class="x-eyebrow">Para empresas</p><h2>¿Oficina, consultorio o restaurante?</h2>
        <p>Nasfeco también diseña soluciones de agua y energía para negocios: varios puntos de agua purificada, mantenimiento programado y facturación para tu empresa.</p>
        <div class="x-btns"><a href="https://wa.me/593997312362?text=Hola%20Nasfeco%2C%20quiero%20una%20cotizaci%C3%B3n%20de%20purificadores%20para%20mi%20empresa" target="_blank" rel="noopener" class="x-btn x-btn-p">Cotizar para mi empresa</a><a href="nasfeco.html" class="x-btn x-btn-o">Conocer Nasfeco</a></div></div>
      <ul><li>Oficinas y espacios de coworking</li><li>Consultorios y clínicas</li><li>Restaurantes y cafeterías</li><li>Colegios y conjuntos residenciales</li></ul>
    </div>
  </div>
</section>'''

# =========================================================== PÁGINA: SERIE X (RO)
def page_ro():
    desc = "Purificadores de ósmosis inversa sin tanque Waterdrop Serie X (X8, X12, X16) en Ecuador, con instalación y soporte de Nasfeco en Quito. Agua pura al instante, con minerales y grifo inteligente."
    ld = {"@context": "https://schema.org", "@graph": [
        offer_ld("x12", "Waterdrop X12 Ósmosis Inversa 1200 GPD", desc, [A("ui-wd-x12-new-vis-pr-logo.png")], "product-ro.html"),
        offer_ld("x16", "Waterdrop X16 Ósmosis Inversa 1600 GPD", desc, [A("X16-LOGO-2.png")], "product-ro.html"),
        offer_ld("x8", "Waterdrop X8 Ósmosis Inversa 800 GPD", desc, [A("ui-X8-NSF.png")], "product-ro.html")]}
    h = head("Serie X Ósmosis Inversa | Waterdrop Ecuador · Nasfeco", desc, SITE + "product-ro", SITE + A("wd-page-1016-new-2-pc.jpg"), ld)
    side = [("destacados", "Por qué la Serie X"), ("ahorro", "Tu ahorro"), ("capacidad", "Velocidad"), ("filtracion", "Filtración"), ("salud", "Minerales"),
            ("servicio", "Servicio Nasfeco"), ("inteligente", "Grifo inteligente"), ("caja", "Qué incluye")]
    body = top(("Serie X · Ósmosis Inversa", [("#destacados", "Resumen"), ("#ahorro", "Ahorro"), ("#comparar", "Comparar"), ("#faq", "Preguntas")], "x12"), side)

    body += banner("Agua pura,<br>directo de tu grifo", "Ósmosis inversa sin tanque Waterdrop Serie X. Instalada y respaldada en Ecuador por Nasfeco.",
                   [("Hasta 1600", "Galones por día"), ("11", "Etapas de filtración"), ("pH 7.5", "Con minerales")],
                   bg=(A("wd-page-1016-new-2-pc.jpg"), A("wd-page-1016-new-2-mo.jpg")),
                   btns='<div class="x-btns"><a href="#ofertas" class="x-btn x-btn-p">Ver precios</a><a href="#ahorro" class="x-btn x-btn-o">Calcular mi ahorro</a></div>')

    body += picks(["x12", "x16", "x8"], title="Elige tu Serie X",
                  sub="Tres capacidades, la misma tecnología. Precios finales en dólares: incluyen IVA e instalación. Trabajamos en todo el Ecuador, con instalación en Quito, Guayaquil, Cuenca y Loja.", sid="ofertas")

    body += f'''
<section class="x-sec" id="destacados">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Por qué la Serie X</h2><p class="x-lead">Seis razones por las que es el purificador que más recomendamos para hogares en Ecuador.</p></div>
    <div class="x-hl">
      <div class="x-hl-col">{hl_card("#capacidad", A("wd-x-series-highlights-img1.jpg"), A("wd-Get_the_highlights-mo-1.jpg"), "Un vaso<br>en 2 segundos")}{hl_card("#filtracion", A("wd-x-series-highlights-img2.jpg"), A("wd-Get_the_highlights-mo-2.jpg"), "11 etapas<br>de limpieza")}</div>
      <div class="x-hl-col">{hl_card("#salud", A("d5ea80df3286a317f75c8784d9f21034.jpg"), A("b517e9b03b64d6d98a0528d4a47ef022.jpg"), "Agua con<br>minerales")}{hl_card("#inteligente", A("wd-x-series-highlights-img4.jpg"), A("wd-Get_the_highlights-mo-4.jpg"), "Grifo que te<br>dice cómo está tu agua")}</div>
      <div class="x-hl-col">{hl_card("#certificacion", A("wd-x-series-highlights-img5.jpg"), A("wd-Get_the_highlights-mo-5.jpg"), "Certificación<br>NSF/ANSI")}{hl_card("#sostenible", A("wd-x-series-highlights-img6.jpg"), A("wd-Get_the_highlights-mo-6.jpg"), "Menos agua<br>desperdiciada")}</div>
    </div></div>
</section>'''

    body += problems([
        (A("e58138043c3bf3914a737c6178db46ed264df1f8.jpg"), "El filtro se demora", "Purificadores con tanque que se vacían justo cuando estás cocinando."),
        (A("1013-_page___1_38.jpg"), "Sabe a cloro", "El agua de la red llega segura, pero con cloro, sarro y un sabor que no provoca."),
        (A("1013-_page___1_36.jpg"), "Tanques y bacterias", "El agua quieta en un tanque bajo el fregadero no es la mejor idea."),
        (A("1013-_page___1_39.jpg"), "Instalaciones eternas", "Visitas, perforaciones y mangueras por todos lados antes del primer vaso."),
    ], title="¿Te pasa algo de esto en casa?")

    body += calc("x12", ("x8", "x12", "x16"))

    body += flow("Sin tanque. Sin esperas.",
                 "El agua pasa directo por los filtros y sale lista para tomar. Con la Serie X, una taza se llena en 2 a 3 segundos.",
                 "77c38a7052694b8783f1ed958242d847", "cdf34b274a4f4038a953a7e2414abac0", sid="capacidad", cap="<span><b>Izquierda:</b> Waterdrop X12 de 1200 GPD</span><span><b>Derecha:</b> purificador común de 600 GPD</span>")

    body += speed("Lo que antes tomaba minutos", "Tiempos medidos con la X16 de 1600 galones por día", [
        ("wd-product-1016-page-banner-flux-1.jpg", "2 s", "Una taza para el café de la mañana"),
        ("wd-product-1016-page-banner-flux-2.jpg", "10 s", "Una jarra para el almuerzo"),
        ("wd-product-1016-page-banner-flux-3.jpg", "20 s", "Una olla para la sopa"),
    ])

    body += f'''
<section class="x-seq" data-seq id="filtracion">
  <div class="x-seq-stage">
    <h2>Así limpia cada gota</h2>
    <p class="x-seq-sub">Pensado para el agua de la red: reduce cloro, sarro, plomo, arsénico, flúor, PFAS, sedimentos, sales disueltas y olores.</p>
    <img class="x-seq-img" src="{A("wd-product-page-1016-filter2024-img199.png")}" alt="Las 11 etapas de filtración de la Serie X" width="1920" height="960" loading="lazy">
    <div class="x-seq-copy">
      <p class="intro on">11 etapas en un solo equipo</p>
      <div><b>Membrana de 0.0001 micras</b><span>Retiene lo que no se ve a simple vista</span></div>
      <div><b>Remineralización alcalina</b><span>Le devuelve calcio y magnesio al agua</span></div>
      <div><b>Luz UV en el grifo</b><span>La última barrera antes de tu vaso</span></div>
    </div>
  </div>
</section>'''

    mins = [("wd-x_seri-3.jpg", "wd-x_seri-2.jpg", "Para los que entrenan", "Calcio y magnesio en cada botella que llenas antes del gimnasio."),
            ("wd-x_seri-5.jpg", "wd-x_seri-4.jpg", "Para cocinar", "Lava frutas y verduras y prepara tus sopas con agua limpia."),
            ("wd-x_seri-7.jpg", "wd-x_seri-6.jpg", "Para el día a día", "Agua suave y agradable que dan ganas de tomar más."),
            ("wd-x_seri-9.jpg", "wd-x_seri-8.jpg", "Para el café", "Un café de altura merece agua sin cloro ni sarro.")]
    mp = "".join(f'<div class="x-min-p{" on" if i == 0 else ""}"><img class="pc" src="{A(pc)}" alt="{t}" loading="lazy"><img class="mo" src="{A(mo)}" alt="{t}" loading="lazy"><p>{d}</p><h3>{t}</h3></div>' for i, (pc, mo, t, d) in enumerate(mins))
    body += f'''
<section class="x-sec" id="salud">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Pura, pero no vacía</h2><p class="x-lead">La Serie X le devuelve minerales al agua después de purificarla. Así se nota en cada momento del día.</p></div>
    <div class="x-min x-rv">{mp}</div></div>
</section>'''

    body += f'''
<section class="x-sec" id="certificacion">
  <div class="x-wrap x-cert">
    <div class="x-rv">
      <p class="x-eyebrow">Calidad comprobada</p>
      <h2>No es promesa: está certificado</h2>
      <p style="margin-bottom:20px">La Serie X cuenta con certificación NSF/ANSI 42, 58 y 372, las normas internacionales de referencia para equipos de tratamiento de agua potable.</p>
      <h4>Qué reduce</h4>
      <p>Sales disueltas (TDS), PFOA, PFOS, cloro, flúor, bario, arsénico, sedimentos, cromo VI, plomo, microplásticos y olores, entre otros.</p>
      <small>Certificación emitida por IAPMO R&amp;T: NSF/ANSI 58 para las sustancias indicadas en la hoja de rendimiento del equipo y NSF/ANSI 372 para materiales bajos en plomo (≤0.25%).</small>
      <div class="x-btns" style="margin-top:22px"><button type="button" class="x-btn x-btn-p" data-cv-open>{svg(I_DOC, 18, 1.8)} Ver certificados NSF/ANSI</button></div>
    </div>
    <div class="x-cert-img x-rv x-cert-click" data-cv-open role="button" tabindex="0">{pic(A("wd-product-x16-wd-new-vis-authentication-img-pc.jpg"), A("wd-product-x16-wd-new-vis-authentication-img-mo.jpg"), "Certificados NSF/ANSI e IAPMO de la Serie X")}<span class="x-cert-zoom">{svg(I_DOC, 18, 1.8)} Ver certificados</span></div>
  </div>
</section>''' + cert_modal("serie", "Certificados · Serie X")[0]

    body += servicio()

    body += flow("Tú decides cuánta agua sale",
                 "Elige el volumen en el grifo y despreocúpate: se detiene solo cuando el vaso, la jarra o la olla está lista.",
                 "b200f21761264e5fa04a64cfa2b8be9f", "f7aeddd6691a469c99ff06eed96e5bc0", sid="inteligente")

    body += '''
<section class="x-fau dark" data-fau data-frames="224" data-base="assets/x/frames/f" data-thresholds="0,75,150">
  <div class="x-fau-stage">
    <div>
      <div class="x-fau-copy">
        <div class="on"><h3>Volumen a tu medida</h3><p>Vaso, jarra u olla con un toque</p></div>
        <div><h3>Calidad a la vista</h3><p>El TDS de tu agua en la pantalla, en tiempo real</p></div>
        <div><h3>Aviso de cambio de filtro</h3><p>El grifo te avisa cuándo cambiarlo</p></div>
      </div>
      <div class="x-fau-steps"><i class="on"></i><i></i><i></i></div>
    </div>
    <canvas width="1000" height="1000" aria-label="Grifo inteligente de la Serie X"></canvas>
  </div>
</section>'''

    body += f'''
<section class="x-us" data-us>
  <div class="x-us-pin">
    <img class="x-us-img" src="{A("3840x1600.jpg")}" alt="Serie X instalada bajo el fregadero de una cocina" loading="lazy">
    <div class="x-us-copy"><h2>Cabe en tu cocina,<br>y te sobra espacio</h2><p>Al no tener tanque, ocupa hasta un 70% menos que un purificador tradicional. Tus productos de limpieza siguen teniendo su lugar bajo el fregadero.</p></div>
  </div>
  <div class="x-us-mo x-sec"><div><h2 class="x-h2">Cabe en tu cocina, y te sobra espacio</h2><p>Al no tener tanque, ocupa hasta un 70% menos que un purificador tradicional.</p></div>
    <img src="{A("1170x1368.jpg")}" alt="Serie X bajo el fregadero" loading="lazy"></div>
</section>'''

    feats = [
        ("v", "f953ad540a8948e1abe4c8eace3ec53c", "Diseño premiado", "Su diseño ganó el reddot 2024. Se ve bien en la cocina y bajo el fregadero."),
        ("i", A("wd-product-1016-page-material-safety.jpg"), "Materiales seguros", "Componentes de grado alimenticio, pensados para durar muchos años de uso diario."),
        ("v", "68715b3969014c8891c777f98ea62602", "Menos uniones, menos fugas", "Los canales de agua van integrados dentro del equipo, así hay menos mangueras que puedan gotear."),
        ("i", A("wd-product-1016-page-waterproof.jpg"), "Enchufe resistente al agua", "Pensado para el lugar donde va: bajo el fregadero, donde siempre hay humedad."),
    ]
    fc = ""
    for kind, src, t, d in feats:
        m = (f'<video data-auto muted loop playsinline preload="none" poster="{VP(src)}"><source src="{V(src)}" type="video/mp4"></video>' if kind == "v"
             else f'<img src="{src}" alt="{t}" loading="lazy">')
        fc += f'<article class="x-feat"><div class="x-feat-m">{m}</div><h3>{t}</h3><p>{d}</p></article>'
    body += f'''
<section class="x-sec">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Hecho para durar años</h2></div>
    <div class="x-car x-rv" data-car><button class="x-arrow prev" aria-label="Anterior">{svg(I_LEFT, 16)}</button><div class="x-car-track">{fc}</div><button class="x-arrow next" aria-label="Siguiente">{svg(I_RIGHT, 16)}</button><div class="x-prog"><i></i></div></div></div>
</section>'''

    body += nature()

    ivs = [("b9KVEgJwv9A", "Instalación y pruebas de la Serie X", "Una familia la instala, mide el agua antes y después, y cuenta su experiencia."),
           ("ALPRzx091G0", "La Serie X en una casa fuera de la ciudad", "Cómo funciona en una vivienda alejada que depende de su propia fuente de agua."),
           ("6kYBhODz7p8", "Agua pura para las reuniones familiares", "La Serie X en una cocina real, en un día con toda la familia en casa."),
           ("GW_j40kIjBw", "Conoce el X12 en dos minutos", "Presentación oficial de Waterdrop del modelo X12 y sus funciones.")]
    iv = "".join(f'<article class="x-iv"><div class="x-yt" data-yt="{i}" role="button" tabindex="0" aria-label="Ver video"><img src="https://i.ytimg.com/vi/{i}/hqdefault.jpg" alt="" loading="lazy"><span class="play">{svg(I_PLAY, 22, 2, True)}</span></div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in ivs)
    body += f'''
<section class="x-sec">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Míralo funcionando en casas reales</h2></div><span class="x-note">Videos en inglés de usuarios y de Waterdrop.</span>
    <div class="x-car x-rv" data-car><button class="x-arrow prev" aria-label="Anterior">{svg(I_LEFT, 16)}</button><div class="x-car-track">{iv}</div><button class="x-arrow next" aria-label="Siguiente">{svg(I_RIGHT, 16)}</button><div class="x-prog"><i></i></div></div></div>
</section>'''


    acc = [("wd-product-1016-page-in-the-box-img10.png", "Adaptador de corriente"), ("wd-product-1016-page-in-the-box-img2.png", "Conector y manguera de entrada"),
           ("wd-product-1016-page-in-the-box-img3.png", "Manguera de desagüe"), ("wd-product-1016-page-in-the-box-img4.png", "Plantilla para el grifo"),
           ("wd-product-1016-page-in-the-box-img5.png", "Abrazadera de desagüe"), ("wd-product-1016-page-in-the-box-product-1.png", "Cinta de teflón ×2"),
           ("wd-product-1016-page-in-the-box-img7.png", "Seguros de conexión ×6")]
    accs = "".join(f'<div class="x-bi"><img src="{A(i)}" alt="" loading="lazy"><span>{t}</span></div>' for i, t in acc)
    boxes = {"x12": ("wd-product-1016-page-in-the-box-img1.png", "wd-product-1016-page-in-the-box-img8.png", "wd-page-1016-collection-x12-inthebox-img10.png"),
             "x16": ("wd-product-1016-page-in-the-box-img1-1.png", "wd-product-1016-page-in-the-box-img8-16.png", "wd-product-1016-page-in-the-box-product-3-x16.png"),
             "x8": ("wd-product-1016-page-product-x8-inthebox-img1.png", "wd-product-1016-page-product-x8-inthebox-img2.png", "wd-product-1016-page-product-x8-inthebox-img3.png")}
    tabs = "".join(f'<button class="x-tab{" on" if k == "x12" else ""}" data-tab="box-{k}">{l}</button>' for k, l in [("x12", "X12"), ("x16", "X16"), ("x8", "X8")])
    panes = "".join(f'<div class="x-pane{" on" if k == "x12" else ""}" id="box-{k}"><div class="x-box-main">' +
                    "".join(f'<div class="x-bi"><img src="{A(i)}" alt="" loading="lazy"><span>{t}</span></div>' for i, t in zip(v, ["Equipo purificador", "Juego de filtros", "Grifo inteligente"])) +
                    f'</div><div class="x-box-acc">{accs}</div></div>' for k, v in boxes.items())
    body += f'''
<section class="x-sec" id="caja">
  <div class="x-wrap" data-tabs><div class="x-head x-rv"><h2 class="x-h2">Todo lo que llega a tu casa</h2><p class="x-lead">Cada equipo trae lo necesario para instalarlo. No tienes que comprar nada aparte.</p></div><div class="x-tabs">{tabs}</div><div class="x-rv">{panes}</div></div>
</section>'''

    cols = [("x12", "ui-wd-x12-new-vis-pr-logo.png", "X12 · 1200 GPD", "wd-product-1016-advance-img-2024-7-2.png", "3:1",
             ("wd-product-1016-advance-img-2024-7-12.png", "Familias de 3 a 5 personas", "El que más recomendamos", "Con minerales alcalinos"),
             ("wd-product-1016-advance-img-2024-7-9.png", "Grifo con volumen programable", "Vaso, jarra u olla con un toque")),
            ("x16", "X16-LOGO-2.png", "X16 · 1600 GPD", "wd-product-1016-advance-img-2024-7-2.png", "3:1",
             ("wd-product-1016-advance-img-2024-7-13.png", "Familias grandes", "El de mayor caudal", "Una taza en 2 segundos"),
             ("wd-product-1016-advance-img-2024-7-9.png", "Grifo con volumen programable", "Vaso, jarra u olla con un toque")),
            ("x8", "ui-X8-NSF.png", "X8 · 800 GPD", "wd-product-1016-advance-img-2024-7-1.png", "2:1",
             ("wd-product-1016-advance-img-2024-7-11.png", "Parejas y familias pequeñas", "La forma más accesible de empezar", "Misma membrana de 0.0001 μm"),
             ("wd-product-1016-advance-img-2024-7-8.png", "Grifo con pantalla", "Muestra el TDS y la vida del filtro"))]
    cc = ""
    for pid, img, name, ratio_img, ratio, ideal, faucet in cols:
        cc += f'''<div class="x-cmp-col{' hl' if pid == 'x12' else ''}"><img src="{A(img)}" alt="Waterdrop {name}" loading="lazy"><h3>{name}</h3>{price(pid)}<span class="x-off" data-off="{pid}" data-promo></span>{buttons(pid)}
          <div class="x-row ratio"><label>Agua pura por cada litro desechado</label><img src="{A(ratio_img)}" alt="{ratio}"><b>{ratio}</b></div>
          <div class="x-row"><img src="{A(ideal[0])}" alt=""><b>{ideal[1]}</b><span>{ideal[2]}</span><span>{ideal[3]}</span></div>
          <div class="x-row"><img src="{A("wd-product-1016-advance-img-2024-7-6.png")}" alt=""><b>Incluye servicio Nasfeco</b><span>Asesoría, garantía y soporte local</span><span>Repuestos originales</span></div>
          <div class="x-row"><img src="{A(faucet[0])}" alt=""><b>{faucet[1]}</b><span>{faucet[2]}</span></div></div>'''
    body += f'''
<section class="x-sec" id="comparar">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">¿Cuál es para tu casa?</h2><p class="x-lead">Si dudas entre dos, escríbenos: te ayudamos a elegir según cuántos son en casa y cuánta agua usan.</p></div><div class="x-cmp x-rv"><div class="x-cmp-g" style="--n:3">{cc}</div></div></div>
</section>'''

    body += bubbles()
    body += b2b()

    body += faq([
        ("¿Por qué necesito un purificador si el agua de mi ciudad es potable?", "El agua de la red llega potabilizada, pero en el camino puede recoger sedimentos y sarro de las tuberías, y lleva cloro, que se nota en el sabor. La Serie X elimina todo eso y además le agrega minerales."),
        ("¿Cada cuánto se cambian los filtros y cuánto cuesta?", "El filtro F2 se cambia cada 6 meses, el F1A cada año y el F3 cada 2 años, según el uso. El grifo te avisa cuándo cambiarlos. Escríbenos para conocer el precio actual de los repuestos."),
        ("¿Necesito un enchufe bajo el fregadero?", "Sí, la Serie X necesita un tomacorriente cerca para funcionar sin tanque y alimentar el grifo inteligente y la luz UV. Si no tienes uno, te lo indicamos en la asesoría previa."),
        ("¿Puedo usar mi propio grifo?", "No. El grifo de la Serie X es parte del sistema: tiene el monitor de calidad, la luz UV y el aviso de cambio de filtros."),
        ("¿Quita los minerales del agua?", "La ósmosis inversa retiene casi todo, pero la Serie X tiene una etapa que le devuelve calcio y magnesio y deja el pH alrededor de 7.5."),
        ("¿Quién responde por la garantía?", "Nasfeco S.A. La gestionamos aquí en Ecuador: si algo falla, nos escribes y lo resolvemos sin que tengas que tratar con el exterior."),
        ("¿En qué ciudades instalan?", "Instalamos con técnicos de Nasfeco en Quito, Guayaquil, Cuenca y Loja, y trabajamos en todo el Ecuador. En otras ciudades te acompañamos por WhatsApp durante la instalación, que es sencilla y trae guía paso a paso."),
        ("¿Cómo pago?", "Arma tu pedido en el carrito y envíalo por WhatsApp. Un asesor confirma disponibilidad, costo de envío o instalación y te indica las formas de pago."),
    ], lead="Lo que más nos preguntan las familias antes de comprar. Si tu duda no está aquí, escríbenos.")

    return h + body + bottom()


I_PLUS = "M12 5v14M5 12h14"
I_BOTTLE = "M10 2h4v3l2 3v12a2 2 0 01-2 2h-4a2 2 0 01-2-2V8l2-3zM8 12h8"
I_HOME = "M3 10l9-7 9 7v10a2 2 0 01-2 2H5a2 2 0 01-2-2zM9 22V12h6v10"
I_SUN = "M12 17a5 5 0 100-10 5 5 0 000 10zM12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"
I_ARROWS = "M8 7l-5 5 5 5M16 7l5 5-5 5"

HOT_PROD = {"x16": ("assets/home/ui-wd-x16-ph-product.webp", "Waterdrop X16 · Ósmosis inversa sin tanque, 1600 GPD", "product-x16.html"),
            "smart": ("assets/ed01/1_33c5e044-eb97-4485-ae99-684bc658886e.webp", "Waterdrop ED01 · Dispensador purificador portátil", "product-smart.html")}

def hot(pid, x, y, xm=None, ym=None, side=""):
    img, name, url = HOT_PROD[pid]
    mo = f"--xm:{xm}%;--ym:{ym}%;" if xm is not None else ""
    cls = (" " + side if side else "") + ("" if xm is not None else " hide-mo")
    return f'''<div class="x-hot{cls}" style="--x:{x}%;--y:{y}%;{mo}"><button type="button" aria-label="Ver {name}">{svg(I_PLUS, 18, 2.4)}</button>
      <div class="x-pop"><img src="{img}" alt=""><div><b>{name}</b>{price(pid)}<div class="x-btns" style="gap:8px"><a href="{url}" class="x-btn x-btn-p x-btn-sm">Ver equipo</a><button class="x-btn x-btn-o x-btn-sm" data-add="{pid}">Agregar</button></div></div></div></div>'''

def scene():
    return f'''
<section class="x-sec" id="en-casa">
  <div class="x-wrap">
    <div class="x-head x-rv"><h2 class="x-h2">Agua pura en cada rincón de tu casa</h2><p class="x-lead">Toca los puntos para ver qué purificador va en cada lugar.</p></div>
    <div class="x-scene-wrap x-rv" data-scene-wrap>
      <div class="x-scene on" id="sc-cocina">
        <img class="bg" src="assets/home/escena-cocina.jpg" alt="Cocina con purificadores Waterdrop X12, G5P700A, Ultrafiltración y Dispensador ED01" loading="lazy">
        {hot("smart", 25.5, 38, 25.5, 38, "l")}
        {hot("uf", 66.3, 74, 66.3, 74, "r")}
        {hot("x12", 74.6, 70, 74.6, 70, "r")}
        {hot("g5", 86, 70, 86, 70, "r")}
      </div>
      <div class="x-scene" id="sc-dorm">
        <img class="bg" src="assets/home/escena-dormitorio.jpg" alt="Dormitorio con Dispensador Waterdrop ED01" loading="lazy">
        {hot("smart", 80.5, 46, 80.5, 46, "r")}
      </div>
      <div class="x-scene-tabs"><button class="on" data-scene-tab="sc-cocina">Cocina</button><button data-scene-tab="sc-dorm">Dormitorio</button></div>
    </div>
  </div>
</section>'''

def brandcards():
    cards = [("assets/home/wd-new-vis-index-sustaninability-img1.webp", I_BOTTLE, "Sostenibilidad", "Menos plástico",
              "Una familia que deja los botellones evita cientos de envases de plástico al año.", "#ahorro", "Calcula tu impacto"),
             ("assets/home/wd-new-vis-index-sustaninability-img2.jpg", I_HOME, "Nuestra misión", "Agua segura en casa",
              "Que cada familia ecuatoriana tome agua pura sin depender de botellones, con tecnología certificada y soporte local.", "#ofertas", "Ver purificadores"),
             ("assets/nasfeco-bg.png", I_SUN, "Nasfeco Empresas", "Agua y energía",
              "Nasfeco, la empresa detrás de Waterdrop Ecuador, también lleva soluciones de agua y energía solar a negocios e industrias.", "nasfeco.html", "Conocer Nasfeco")]
    c = "".join(f'''<article class="x-bc x-rv"><img src="{img}" alt="" loading="lazy"><i>{svg(ic, 48, 1.4)}</i><small>{k}</small><h3>{h}</h3><p>{p}</p><a href="{u}">{l} {svg(I_RIGHT, 14)}</a></article>''' for img, ic, k, h, p, u, l in cards)
    return f'''
<section class="x-sec"><div class="x-wrap"><div class="x-brandcards">{c}</div></div></section>'''

def fullvid(title, sub, pc, mo):
    return f'''
<section class="x-fullvid" style="margin-top:var(--sec)">
  <video class="pc" data-auto muted loop playsinline preload="none" poster="assets/home/{pc}-poster.jpg"><source src="assets/home/{pc}.mp4" type="video/mp4"></video>
  <video class="mo" data-auto muted loop playsinline preload="none" poster="assets/home/{mo}-poster.jpg"><source src="assets/home/{mo}.mp4" type="video/mp4"></video>
  <div class="x-fullvid-c x-rv"><h2>{title}</h2><p>{sub}</p></div>
</section>'''

def bubbles():
    imgs = "".join(f'<img class="b{i+1}" src="assets/home/bubble{n}.png" alt="" aria-hidden="true">' for i, n in enumerate([1, 2, 4, 6, 7]))
    return f'''
<section class="x-bub">
  {imgs}
  <div class="x-wrap x-rv">
    <h2>Despídete<span>de los botellones</span></h2>
    <p>¿No sabes qué purificador va con tu casa? Responde 3 preguntas y te recomendamos uno en menos de un minuto.</p>
    <div class="x-btns"><button class="x-btn x-btn-p" data-quiz>Encuentra tu purificador</button><a class="x-btn x-btn-o" href="https://wa.me/593997312362?text=Hola%20Nasfeco%2C%20quiero%20asesor%C3%ADa%20para%20elegir%20mi%20purificador" target="_blank" rel="noopener">Habla con un asesor</a></div>
  </div>
</section>'''

def xcompare(hl):
    cols = [("x16", "assets/x16/X16-LOGO-2.webp", "X16 · 1600 GPD", "wd-product-1016-advance-img-2024-7-2.png", "3:1",
             ("wd-product-1016-advance-img-2024-7-13.png", "Familias grandes", "El de mayor caudal", "Una taza en 2 segundos"),
             ("wd-product-1016-advance-img-2024-7-9.png", "Grifo con volumen programable", "Vaso, jarra u olla con un toque")),
            ("x12", A("ui-wd-x12-new-vis-pr-logo.png"), "X12 · 1200 GPD", "wd-product-1016-advance-img-2024-7-2.png", "3:1",
             ("wd-product-1016-advance-img-2024-7-12.png", "Familias de 3 a 5 personas", "El que más recomendamos", "Con minerales alcalinos"),
             ("wd-product-1016-advance-img-2024-7-9.png", "Grifo con volumen programable", "Vaso, jarra u olla con un toque")),
            ("x8", "assets/x8/ui-wd-x8-a-new-vis-main.webp", "X8 · 800 GPD", "wd-product-1016-advance-img-2024-7-1.png", "2:1",
             ("wd-product-1016-advance-img-2024-7-11.png", "Parejas y familias pequeñas", "La forma más accesible de empezar", "Misma membrana de 0.0001 μm"),
             ("wd-product-1016-advance-img-2024-7-8.png", "Grifo con pantalla", "Muestra el TDS y la vida del filtro"))]
    cc = ""
    for pid, img, name, ratio_img, ratio, ideal, faucet in cols:
        cc += f'''<div class="x-cmp-col{' hl' if pid == hl else ''}"><img src="{img}" alt="Waterdrop {name}" loading="lazy"><h3>{name}</h3>{price(pid)}<span class="x-off" data-off="{pid}" data-promo></span>{buttons(pid)}
          <div class="x-row ratio"><label>Agua pura por cada litro desechado</label><img src="{A(ratio_img)}" alt="{ratio}"><b>{ratio}</b></div>
          <div class="x-row"><img src="{A(ideal[0])}" alt=""><b>{ideal[1]}</b><span>{ideal[2]}</span><span>{ideal[3]}</span></div>
          <div class="x-row"><img src="{A("wd-product-1016-advance-img-2024-7-6.png")}" alt=""><b>Incluye servicio Nasfeco</b><span>Asesoría, garantía y soporte local</span><span>Repuestos originales</span></div>
          <div class="x-row"><img src="{A(faucet[0])}" alt=""><b>{faucet[1]}</b><span>{faucet[2]}</span></div></div>'''
    return f'''
<section class="x-sec" id="comparar">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Compara la Serie X</h2><p class="x-lead">Misma tecnología de 11 etapas. Cambia el caudal y el grifo.</p></div><div class="x-cmp x-rv"><div class="x-cmp-g" style="--n:3">{cc}</div></div></div>
</section>'''

# =========================================================== PÁGINA: X16
def page_x16():
    G = "assets/x16/"
    gallery = [G + f for f in ["X16-LOGO-2.webp", "ui-wd-x16-s-new-vis-main.webp", "ui-wd-x16-new-vis-main-white.jpg", "X16_system.png", "X16_2.jpg", "X16_3.jpg",
                               "X16_5.jpg", "X16_6.jpg", "X16_714501c9-eaa2-49d0-8078-8e9c3cdddb90.jpg", "X16-NSF_ANTI-4258372.jpg", "RO_reduce_lead.jpg", "X16-Spec.jpg"]]
    desc = "Waterdrop X16 en Ecuador: ósmosis inversa sin tanque de 1600 GPD, 11 etapas, pH 7.5 con minerales y grifo digital. Instalación y soporte de Nasfeco en Quito, Guayaquil, Cuenca y Loja."
    ld = {"@context": "https://schema.org", **offer_ld("x16", "Waterdrop X16 Ósmosis Inversa 1600 GPD", desc, gallery[:3], "product-x16.html")}
    h = head("Waterdrop X16 · 1600 GPD | Waterdrop Ecuador · Nasfeco", desc, SITE + "product-x16", SITE + gallery[0], ld)
    body = top(("Waterdrop X16", [("#resumen", "Resumen"), ("#comparar", "Comparar"), ("#faq", "Preguntas")], "x16"))
    thumbs = "".join(f'<button class="{"on" if i == 0 else ""}" data-thumb="{g}" aria-label="Imagen {i+1}"><img src="{g}" alt="" loading="lazy"></button>' for i, g in enumerate(gallery))
    filters = [("ui-wd-f1a-product.png", "F1A", "Hasta 12 meses"), ("ui-wd-f2_FILTER.webp", "F2", "Hasta 6 meses"), ("ui-wd-x16-f3-filter.webp", "X16-F3", "Hasta 24 meses")]
    fl = "".join(f'<div class="x-bi" style="padding:10px"><img src="{G}{i}" alt="" loading="lazy"><span>{n}<br><small style="font-weight:400;color:#888">{d}</small></span></div>' for i, n, d in filters)
    body += f'''
<section class="x-sec" id="ofertas" style="padding-top:40px">
  <div class="x-wrap x-pbuy">
    <div><div class="x-gal-main"><img id="x-gal-main" src="{gallery[0]}" alt="Waterdrop X16"></div><div class="x-gal-th">{thumbs}</div></div>
    <div class="x-pinfo">
      <p class="x-eyebrow">Serie X · El más rápido</p><h1>Waterdrop X16 · Ósmosis inversa sin tanque</h1>
      <p>1600 galones por día: agua pura al instante para familias grandes, con minerales alcalinos y grifo digital.</p>
      <div class="x-metrics"><div><b>1600</b><span>GPD</span></div><div><b>3:1</b><span>Agua pura / desecho</span></div><div><b>pH 7.5</b><span>Con minerales</span></div></div>
      <div class="x-price">{price_in("x16")}<span class="x-off" data-off="x16" data-promo></span></div>
      <div style="margin-top:12px">{code("x16")}</div>
      <div class="x-pcd" data-promo><span><span data-promo-name></span> · termina en</span>{cd()}</div>
      {buttons("x16")}
      {PERKS}
      <p class="x-eyebrow" style="margin-top:28px">Filtros de repuesto</p>
      <div class="x-box-main" style="grid-template-columns:repeat(3,1fr);gap:10px;margin:0">{fl}</div>
    </div>
  </div>
</section>'''
    sp = [("wide", "v", "9ac939bc5196472ab8f19a9a11f1fc87", "1600 GPD", "Una taza en 2 segundos"),
          ("", "i", "wd-new-vis-product-overview-smart-img1.jpg", "3:1", "3 litros puros por cada litro desechado"),
          ("", "i", "wd-new-vis-X16-Set_of_selling_points-img2.jpg", "Flujo directo", "Sin tanque, sin esperas"),
          ("", "i", "wd-new-vis-X16-Set_of_selling_points-img4.jpg", "11 etapas", "Membrana de 0.0001 μm"),
          ("", "i", "wd-new-vis-X16-Set_of_selling_points-img5.jpg", "Minerales", "pH equilibrado 7.5±"),
          ("", "i", "wd-new-vis-X16-Set_of_selling_points-img6.jpg", "Grifo digital", "TDS y vida del filtro"),
          ("", "i", "wd-new-vis-product-UV-Sterilization-img1.jpg", "Protección LED", "Barrera extra en el circuito de agua")]
    spc = ""
    for cls, k, src, t, d in sp:
        m = (f'<video data-auto muted loop playsinline preload="none" poster="{G}{src}-poster.jpg"><source src="{G}{src}.mp4" type="video/mp4"></video>' if k == "v"
             else f'<img src="{G}{src}" alt="{t}" loading="lazy">')
        spc += f'<div class="{cls} x-rv">{m}<div class="t"><b>{t}</b><span>{d}</span></div></div>'
    body += f'''
<section class="x-sec" id="resumen">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Todo lo que hace la X16</h2></div><div class="x-sp">{spc}</div></div>
</section>'''
    pairs = [("Rápido", 1, "Purificador tradicional", "Waterdrop X16"), ("Compacto", 3, "Sistema con tanque", "Waterdrop X16"),
             ("Saludable", 5, "Agua sin tratar", "Agua X16 con minerales"), ("Inteligente", 7, "Grifo común", "Grifo digital X16")]
    tabs = "".join(f'<button class="x-tab{" on" if i == 0 else ""}" data-ba-tab="ba{i}">{t}</button>' for i, (t, *_ ) in enumerate(pairs))
    knob = svg(I_ARROWS, 20, 2.2)
    bas = "".join(f'''<div class="x-ba{" on" if i == 0 else ""}" id="ba{i}"><img src="{G}wd-new-vis-product-x16-12.11-Comparison{n}.webp" alt="{a}"><img class="after" src="{G}wd-new-vis-product-x16-12.11-Comparison{n+1}.webp" alt="{b}"><span class="bar"></span><span class="knob">{knob}</span><span class="lab a">{a}</span><span class="lab b">{b}</span></div>''' for i, (t, n, a, b) in enumerate(pairs))
    body += f'''
<section class="x-sec" data-ba>
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Pásate a la X16</h2><p class="x-lead">Desliza para comparar con lo que tienes hoy.</p></div>
    <div class="x-ba-tabs">{tabs}</div><div class="x-rv">{bas}</div></div>
</section>'''
    body += flow("El flujo más rápido de la Serie X", "Con 1600 galones por día, la X16 llena un vaso, una tetera o una olla casi tan rápido como lo pides.",
                 "ddda58eee82c4baaa6c44b59f87beb9d", "9ac939bc5196472ab8f19a9a11f1fc87", sid="velocidad").replace("assets/x/video/ddda58eee82c4baaa6c44b59f87beb9d", G + "ddda58eee82c4baaa6c44b59f87beb9d").replace("assets/x/video/9ac939bc5196472ab8f19a9a11f1fc87", G + "9ac939bc5196472ab8f19a9a11f1fc87")
    body += f'''
<section class="x-ph" data-ph>
  <div class="x-ph-stage">
    <video muted playsinline preload="metadata" loop poster="{G}62b310e01b534bf98c5bca01f40a5a06-poster.jpg"><source src="{G}62b310e01b534bf98c5bca01f40a5a06.mp4" type="video/mp4"></video>
    <div class="x-ph-c"><p class="x-eyebrow">Agua alcalina</p><h2>Más saludable en cada vaso</h2><p>La X16 ajusta el agua purificada a un pH de 7.5± y le suma calcio y magnesio para un sabor más suave.</p>
      <b class="num">pH 7.5</b><div class="x-ph-bar"><i></i></div><div class="x-ph-scale"><span>0 · Ácida</span><span>7 · Neutra</span><span>14 · Alcalina</span></div></div>
  </div>
</section>
<section class="x-sec">
  <div class="x-wrap x-mt">
    <video class="x-rv" data-auto muted loop playsinline preload="none" poster="{G}38fc560a5a7b46c2b2d5d6b2549e4ceb-poster.jpg"><source src="{G}38fc560a5a7b46c2b2d5d6b2549e4ceb.mp4" type="video/mp4"></video>
    <div class="x-rv"><p class="x-eyebrow">Filtración</p><h2>Más pura con 11 etapas</h2><p>Membrana de ósmosis inversa de 0.0001 μm y protección LED que reducen TDS, PFOA, PFOS, cloro, flúor, arsénico, plomo y más. Al final, una capa mineral le devuelve calcio y magnesio al agua.</p></div>
  </div>
</section>'''
    feats = [("v", "6461bec2afa04e249094b1830110110b", "Volumen a tu medida", "Programa el volumen para un vaso, una botella o la olla y el grifo se detiene solo."),
             ("i", "wd-new-vis-product-X16-Image_and_text-img2.jpg", "Grifo inteligente", "Control táctil, monitor de TDS en tiempo real y aviso de cambio de filtro."),
             ("i", "wd-new-vis-product-X16-Image_and_text-img3.jpg", "Filtros de larga duración", "El filtro RO dura hasta 24 meses y se cambia en 3 segundos, sin herramientas."),
             ("i", "wd-new-vis-product-X16-Image_and_text-img4.jpg", "Canales integrados", "Menos mangueras y uniones: más eficiencia y menos riesgo de fugas.")]
    fc = ""
    for k, src, t, d in feats:
        m = (f'<video data-auto muted loop playsinline preload="none" poster="{G}{src}-poster.jpg"><source src="{G}{src}.mp4" type="video/mp4"></video>' if k == "v"
             else f'<img src="{G}{src}" alt="{t}" loading="lazy">')
        fc += f'<article class="x-feat"><div class="x-feat-m">{m}</div><h3>{t}</h3><p>{d}</p></article>'
    body += f'''
<section class="x-sec">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Pensada para el día a día</h2></div>
    <div class="x-car x-rv" data-car><button class="x-arrow prev" aria-label="Anterior">{svg(I_LEFT, 16)}</button><div class="x-car-track">{fc}</div><button class="x-arrow next" aria-label="Siguiente">{svg(I_RIGHT, 16)}</button><div class="x-prog"><i></i></div></div></div>
</section>
<section class="x-sec">
  <div class="x-wrap x-mt">
    <div class="x-rv" style="border-radius:var(--r-card);overflow:hidden"><img src="{G}wd-new-vis-x16-save_1200_water-pc.png" alt="Relación 3:1 de agua pura" loading="lazy" style="width:100%"></div>
    <div class="x-rv"><p class="x-eyebrow">Sostenibilidad</p><h2>Desperdicia mucho menos agua</h2><p>Por cada litro que va al desagüe, la X16 entrega 3 litros de agua pura. Muchos purificadores tradicionales hacen exactamente lo contrario.</p></div>
  </div>
</section>'''
    body += servicio(video=False)
    body += f'''
<section class="x-sec" id="certificacion">
  <div class="x-wrap x-cert">
    <div class="x-rv"><p class="x-eyebrow">Calidad comprobada</p><h2>Certificada NSF/ANSI 42, 58 y 372</h2>
      <h4>Qué reduce</h4><p>TDS, PFOA, PFOS, cloro, flúor, bario, arsénico, sal, sedimentos, cromo VI, plomo, microplásticos y olores, entre otros.</p>
      <small>Certificación emitida por IAPMO R&amp;T: NSF/ANSI 58 para las sustancias indicadas en la hoja de rendimiento y NSF/ANSI 372 para materiales bajos en plomo (≤0.25%).</small></div>
    <div class="x-cert-img x-rv">{pic(G + "wd-product-x16-wd-new-vis-authentication-img-pc.jpg", G + "wd-product-x16-wd-new-vis-authentication-img-mo.jpg", "Certificados de la X16")}</div>
  </div>
</section>'''
    specs = [("Modelo", "WD-X16"), ("Capacidad", "1600 GPD"), ("Agua pura / desecho", "3:1"), ("Filtración", "11 etapas"),
             ("Certificación", "NSF/ANSI 42, 58 y 372"), ("Grifo", "Digital inteligente"), ("Medidas", "46 × 16 × 42 cm"), ("Peso", "17.8 kg"),
             ("Electricidad", "Sí, tomacorriente bajo el fregadero"), ("Uso", "Interior")]
    rows = "".join(f'<details open style="border:0"><summary style="cursor:default;padding:14px 0;border-bottom:1px solid #eee;font-weight:500"><span style="color:#888">{a}</span><span>{b}</span></summary></details>' for a, b in specs)
    rows = "".join(f'<div style="display:flex;justify-content:space-between;gap:16px;padding:14px 0;border-bottom:1px solid #eee;font-size:15px"><span style="color:#777">{a}</span><b style="font-weight:600;text-align:right">{b}</b></div>' for a, b in specs)
    box = [("X16_system.png", "Equipo X16"), ("wd-product-1016-page-in-the-box-product-2-x16.png", "Juego de filtros"), ("wd-product-1016-page-in-the-box-product-3-x16.png", "Grifo inteligente"),
           ("X_Power_adapter.png", "Adaptador de corriente"), ("X_Red_14_PE_tubing60.png", "Manguera de desagüe"), ("Feed_water_adapter_inlet_water_tubing.png", "Conector y manguera de entrada"),
           ("X_Drain_saddle.png", "Abrazadera de desagüe"), ("X_Reference_sticker.webp", "Plantilla para el grifo"), ("X_Teflon_tape.png", "Cinta de teflón ×2"), ("X_Lock_clip.png", "Seguros ×4")]
    bx = "".join(f'<div class="x-bi"><img src="{G}{i}" alt="" loading="lazy"><span>{t}</span></div>' for i, t in box)
    body += f'''
<section class="x-sec">
  <div class="x-wrap x-mt" style="align-items:start">
    <div class="x-rv" style="border-radius:var(--r-card);overflow:hidden;background:var(--s2)"><img src="{G}X16-Spec.jpg" alt="Medidas de la X16" loading="lazy" style="width:100%"></div>
    <div class="x-rv"><p class="x-eyebrow">Ficha técnica</p><h2>Especificaciones</h2>{rows}</div>
  </div>
</section>
<section class="x-sec" id="caja">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Todo lo que llega a tu casa</h2><p class="x-lead">Incluye todo para instalarla. Manual de usuario incluido.</p></div>
    <div class="x-box-acc x-rv" style="grid-template-columns:repeat(5,minmax(0,1fr))">{bx}</div></div>
</section>'''
    body += xcompare("x16")
    body += bubbles()
    body += b2b()
    body += faq([
        ("¿Cada cuánto se cambian los filtros?", "F1A cada 12 meses (hasta 1100 galones), F2 cada 6 meses (hasta 550 galones) y X16-F3 cada 24 meses (hasta 2200 galones), según el uso. El grifo te avisa cuándo cambiarlos."),
        ("¿Qué diferencia hay con la X12?", "La X16 tiene más caudal (1600 vs 1200 galones por día) y está pensada para familias grandes o cocinas con mucho uso. La filtración de 11 etapas y los minerales son los mismos."),
        ("¿Necesita electricidad?", "Sí. Necesita un tomacorriente bajo el fregadero para la bomba sin tanque, el grifo digital y la protección LED."),
        ("¿Cuánto espacio ocupa?", "Unos 46 × 16 × 42 cm. Al no tener tanque, ocupa mucho menos que un purificador tradicional."),
        ("¿Quién responde por la garantía?", "Nasfeco. La gestionamos aquí en Ecuador: si algo falla, nos escribes y lo resolvemos."),
        ("¿En qué ciudades instalan?", "Instalamos con técnicos de Nasfeco en Quito, Guayaquil, Cuenca y Loja, y trabajamos en todo el Ecuador. En otras ciudades te acompañamos por WhatsApp durante la instalación, que trae guía paso a paso."),
    ])
    return h + body + bottom()


# =====================================================================
#  v7 · Visor de certificados (se abre al instante)
# =====================================================================
I_DOC = "M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8zM14 2v6h6M9 13h6M9 17h6"
I_IMG = "M4 4h16v16H4zM4 16l5-5 4 4 3-3 4 4M15 9a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"
CERT_DOCS = {
    "g2": [("img", "assets/g2/wd-product-g2p600-vis-img17.jpg", "Certificación NSF/ANSI 372"),
           ("img", "assets/g2/wd-product-g2p600-vis-img18.jpg", "Pruebas SGS y CSA según NSF/ANSI 42, 53, 58 y 401")],
    "x16": [("pdf", "assets/certs/x16-certificado.pdf", "Hoja oficial de reducción de contaminantes"),
            ("img", "assets/x16/X16-NSF_ANTI-4258372.jpg", "Certificación NSF/ANSI 42, 58 y 372"),
            ("img", "assets/x16/wd-product-x16-wd-new-vis-authentication-img-pc.jpg", "Certificados IAPMO R&T"),
            ("img", "assets/x16/RO_reduce_lead.jpg", "Reducción de plomo")],
    "x12": [("img", "assets/x12/X12-NSF_ANTI-4258372.jpg", "Certificación NSF/ANSI 42, 58 y 372"),
            ("img", "assets/x12/wd-new-vis-Authentication-img2-pc.jpg", "Certificados IAPMO R&T"),
            ("img", "assets/x12/RO_reduce_lead.jpg", "Reducción de plomo")],
    "x8":  [("pdf", "assets/certs/x8-certificado.pdf", "Certificado IAPMO"),
            ("img", "assets/x8/RO_reduce_lead.jpg", "Reducción de plomo")],
    "g800": [("pdf", "assets/certs/g800-certificado.pdf", "Hoja oficial de reducción de contaminantes"),
             ("img", "assets/g800/G3P800-NSF-feed.webp", "Certificación NSF/ANSI 42, 53, 58 y 372"),
             ("img", "assets/g800/wd-product-g3p800-new-vis-img25.jpg", "Certificados IAPMO R&T"),
             ("img", "assets/g800/RO_reduce_lead.jpg", "Reducción de plomo")],
    "g600": [("pdf", "assets/certs/g600-certificado.pdf", "Hoja oficial de reducción de contaminantes"),
             ("img", "assets/g600/WD-G3P600-NSF.webp", "Certificación NSF/ANSI 42, 58 y 372"),
             ("img", "assets/g600/wd-product-new-vis-G3P600-Certification_report-pad.jpg", "Certificados IAPMO R&T")],
    "k6":  [("pdf", "assets/certs/k6-certificado.pdf", "Certificado IAPMO"),
            ("img", "assets/k6/k6-nsf32.jpg", "Certificación NSF/ANSI 372"),
            ("img", "assets/k6/wd-product-k6-vis-img33.jpg", "Reporte de laboratorio"),
            ("img", "assets/k6/RO_reduce_lead.jpg", "Reducción de plomo")],
    "smart": [("img", "assets/ed01/White-AlkalineAlkaline-02.jpg", "Certificación NSF/ANSI 42 y 372")],
    "all": [("pdf", "assets/certs/g5-certificado.pdf", "G5P700A · Certificado IAPMO"),
            ("img", "assets/g5/ui-wd-g5p700a-nsf-vis.jpg", "G5P700A · Certificación NSF/ANSI 58 y 372"),
            ("img", "assets/x12/X12-NSF_ANTI-4258372.jpg", "X12 · Certificación NSF/ANSI 42, 58 y 372"),
            ("img", "assets/x12/wd-new-vis-Authentication-img2-pc.jpg", "X12 · Certificados IAPMO R&T"),
            ("img", "assets/ed01/White-AlkalineAlkaline-02.jpg", "ED01 · Certificación NSF/ANSI 42 y 372")],
    "g5": [("pdf", "assets/certs/g5-certificado.pdf", "Certificado IAPMO"),
           ("img", "assets/g5/ui-wd-g5p700a-nsf-vis.jpg", "Certificación NSF/ANSI 58 y 372"),
           ("img", "assets/g5/wd-product-other-us-x8-Authentication-pc.jpg", "Certificados IAPMO R&T")],
    "serie": [("pdf", "assets/certs/x16-certificado.pdf", "X16 · Hoja oficial de reducción de contaminantes"),
              ("pdf", "assets/certs/x8-certificado.pdf", "X8-A · Certificado IAPMO"),
              ("img", "assets/x12/X12-NSF_ANTI-4258372.jpg", "X12 · Certificación NSF/ANSI"),
              ("img", "assets/x/wd-product-x16-wd-new-vis-authentication-img-pc.jpg", "Certificados IAPMO R&T")],
}

def cert_modal(key, title):
    docs = [d for d in CERT_DOCS.get(key, []) if os.path.exists(os.path.join(ROOT, d[1]))]
    if not docs: return "", ""
    items = "".join(f'<button type="button" class="x-cv-i{" on" if i == 0 else ""}" data-cv="{i}" data-type="{t}" data-src="{src}">{svg(I_DOC if t == "pdf" else I_IMG, 18, 1.8)}<span>{lab}<small>{"Documento PDF" if t == "pdf" else "Imagen"}</small></span></button>' for i, (t, src, lab) in enumerate(docs))
    modal = f'''
<div class="x-cv-ov" id="x-cv" role="dialog" aria-modal="true" aria-label="Certificados">
  <div class="x-cv">
    <div class="x-cv-h"><div><p class="x-eyebrow">Documentos oficiales</p><h3>{title}</h3></div><button class="x-icon" data-cv-close aria-label="Cerrar">{svg(I_X, 22)}</button></div>
    <div class="x-cv-b"><nav class="x-cv-list">{items}</nav><div class="x-cv-view" id="x-cv-view"></div></div>
  </div>
</div>'''
    btn = f'<div class="x-btns" style="margin-top:22px"><button type="button" class="x-btn x-btn-p" data-cv-open>{svg(I_DOC, 18, 1.8)} Ver certificados NSF/ANSI</button></div>'
    return modal, btn


# =====================================================================
#  v11 · Shorts, repuestos
# =====================================================================
SHORTS = [("x12", "26BQXx1PgIE", "Waterdrop X12"), ("g5", "TrO42mLP9z0", "Waterdrop G5P700A"), ("g2", "8OztpiA46eg", "Waterdrop G2P600"),
          ("uf", "tL_2gSpSn20", "Ultrafiltración UF"), ("smart", "Nm090TXf6oM", "Dispensador ED01")]
FID = {"F1A": "x12-f1a", "F2": "x12-f2", "X12-F3": "x12-f3", "G5P700A-CF": "g5-cf", "G5P700-RO": "g5-ro", "RF10-UF": "uf-rf10", "WD-EDF": "ed01-filtro", "G2CF": "g2-cf", "G2P6MRO": "g2-ro"}

def shorts(first=None, title="Míralos en acción", lead="Así funcionan los equipos que instalamos."):
    items = [x for x in SHORTS if x[0] == first] if first else SHORTS
    if first and not items:
        return ""
    if first and items:
        pid, vid, name = items[0]
        return f'''
<section class="x-sec" id="videos"><div class="x-wrap x-mt x-short-one">
  <div class="x-yt x-yt-v x-rv" data-ytauto="{vid}" aria-label="Video de {name}"><img src="https://i.ytimg.com/vi/{vid}/oardefault.jpg" onerror="this.onerror=null;this.src='https://i.ytimg.com/vi/{vid}/hqdefault.jpg'" alt="Video de {name}" loading="lazy"></div>
  <div class="x-rv"><p class="x-eyebrow">Video</p><h2>{title}</h2><p>{lead}</p>
    <div class="x-btns" style="margin-top:22px"><button class="x-btn x-btn-p" data-add="{pid}">Agregar al carrito</button><button class="x-btn x-btn-o" data-buy="{pid}">Comprar ahora</button></div></div>
</div></section>'''
    cards = "".join(f'''<article class="x-short x-rv"><div class="x-yt x-yt-v" data-ytauto="{vid}" aria-label="Video de {name}">
      <img src="https://i.ytimg.com/vi/{vid}/oardefault.jpg" onerror="this.onerror=null;this.src='https://i.ytimg.com/vi/{vid}/hqdefault.jpg'" alt="Video de {name}" loading="lazy"><span class="play">{svg(I_PLAY, 22, 2, True)}</span></div>'
      <h3>{name}</h3><a href="{OFFER_URL[pid]}">Ver equipo →</a></article>''' for pid, vid, name in items)
    return f'''
<section class="x-sec" id="videos"><div class="x-wrap">
  <div class="x-head x-rv"><p class="x-eyebrow" style="text-align:center">Videos</p><h2 class="x-h2">{title}</h2><p class="x-lead">{lead}</p></div>'
  <div class="x-shorts">{cards}</div></div></section>'''

FILTERS = [
    ("Waterdrop X12", "product-x12", [("x12-f1a", "F1A", "assets/x12/ui-wd-f1a-product.png", "Filtro compuesto con minerales alcalinos", "Hasta 12 meses"),
                                       ("x12-f2", "F2", "assets/x12/ui-wd-f2_FILTER.webp", "Prefiltro de sedimentos y carbón", "Hasta 6 meses"),
                                       ("x12-f3", "X12-F3", "assets/x12/ui-wd-x12-f3-fIlter.webp", "Membrana de ósmosis inversa 0.0001 μm", "Hasta 24 meses")]),
    ("Waterdrop G5P700A", "product-g5p700a", [("g5-cf", "G5P700A-CF", "assets/g5/ui-wd-g5p700a-cf-product.png", "Filtro compuesto con minerales alcalinos", "Hasta 6 meses"),
                                               ("g5-ro", "G5P700-RO", "assets/g5/ui-wd-g5p700-ro-product.png", "Membrana de ósmosis inversa 0.0001 μm", "Hasta 24 meses")]),
    ("Waterdrop G2P600", "product-g2p600", [("g2-cf", "G2CF", "assets/g2/G2CF.png", "Filtro compuesto de algodón PP y carbón activado", "Hasta 12 meses"),
                                             ("g2-ro", "G2P6MRO", "assets/g2/WD-G2P6MRO.png", "Membrana de ósmosis inversa 0.0001 μm", "Hasta 24 meses")]),
    ("Ultrafiltración UF", "product-uf", [("uf-rf10", "RF10-UF", "assets/uf/WD-RF10-UF-NSF.png", "Filtro de ultrafiltración 0.01 μm", "Hasta 12 meses")]),
    ("Dispensador ED01", "product-smart", [("ed01-filtro", "WD-EDF", "assets/filtros/wd-edf.webp", "Filtro de repuesto original para el Dispensador ED01", "Hasta 3 meses o 200 galones")]),
]

def page_repuestos():
    desc = "Filtros de repuesto originales Waterdrop en Ecuador: X12, G5P700A, G2P600, Ultrafiltración UF y Dispensador ED01. Nasfeco, distribuidor exclusivo oficial."
    h = head("Filtros de repuesto Waterdrop | Waterdrop Ecuador · Nasfeco", desc, SITE + "repuestos", SITE + "assets/x12/ui-wd-f1a-product.png",
             {"@context": "https://schema.org", "@type": "ItemList", "name": "Filtros de repuesto Waterdrop",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f"Filtro {n} para {eq}"} for i, (eq, _u, fs) in enumerate(FILTERS) for (_i, n, *_r) in fs[:1]]})
    body = top()
    groups = ""
    for eq, url, fs in FILTERS:
        cards = ""
        for fid, name, img, what, life in fs:
            msg = f"Hola Nasfeco, quiero comprar el filtro de repuesto {name} para mi {eq}. ¿Me ayudan con el precio y la disponibilidad?"
            wa = "https://wa.me/593997312362?text=" + msg.replace(" ", "%20").replace("¿", "%C2%BF").replace("?", "%3F").replace(",", "%2C")
            cards += f'''<article class="x-rep" id="{fid}"><div class="x-rep-img"><img src="{img}" alt="Filtro {name}" loading="lazy"></div>'
              <div class="x-rep-b"><span class="x-of-k">Repuesto original · {eq}</span><h3>{name}</h3><p>{what}</p><ul class="x-of-specs"><li>{life}</li><li>Original Waterdrop</li></ul>
              {price(fid)}
              <div class="x-btns"><button class="x-btn x-btn-p" data-add="{fid}">Agregar al carrito</button><button class="x-btn x-btn-wa" data-buy="{fid}">{WA} Comprar ahora</button></div>
              <a class="x-rep-eq" href="{url}">Ver equipo →</a></div></article>'''
        groups += f'<div class="x-rep-g"><h2 class="x-rep-t">Para {eq}</h2><div class="x-reps">{cards}</div></div>'
    body += f'''
<section class="x-sec" style="padding-top:48px"><div class="x-wrap">
  <div class="x-head x-rv"><p class="x-eyebrow" style="text-align:center">Repuestos originales</p><h1 class="x-h2">Filtros de repuesto Waterdrop</h1>
    <p class="x-lead">Filtros originales para tu equipo, vendidos por Nasfeco, distribuidor exclusivo oficial de Waterdrop Filter en Ecuador. Precios con IVA incluido; el envío se coordina por WhatsApp (el filtro WD-EDF incluye envío).</p></div>'
  {groups}
</div></section>'''
    return h + body + bottom()

# =========================================================== PÁGINA: TIENDA
def page_store():
    desc = "Nasfeco, distribuidor exclusivo oficial de Waterdrop Filter en Ecuador: purificadores X12, G5P700A, ultrafiltración y dispensador ED01. Trabajamos en todo el Ecuador, con instalación en Quito, Guayaquil, Cuenca y Loja."
    ld = {"@context": "https://schema.org", "@graph": [
        offer_ld("x12", "Waterdrop X12 Ósmosis Inversa", desc, [A("ui-wd-x12-new-vis-pr-logo.png")], "product-x12.html"),
        offer_ld("g5", "Waterdrop G5P700A Ósmosis Inversa Alcalina", desc, ["assets/g5/ui-wd-g5p700a-product.webp"], "product-g5p700a.html"),
        offer_ld("g2", "Waterdrop G2P600 Ósmosis Inversa 600 GPD", desc, ["assets/g2/WD-G2P600-W-NSF.webp"], "product-g2p600.html"),
        offer_ld("uf", "Waterdrop Ultrafiltración UF", desc, ["assets/uf-gal-1.png.png"], "product-uf.html"),
        offer_ld("smart", "Waterdrop Dispensador ED01", desc, ["assets/smart-gal-1.png.jpg"], "product-smart.html"),
        {"@type": "LocalBusiness", "name": "Waterdrop Ecuador · Nasfeco", "description": "Distribuidor exclusivo oficial de Waterdrop Filter en Ecuador", "telephone": "+593 99 731 2362", "url": SITE + "waterdrop",
         "address": {"@type": "PostalAddress", "addressLocality": "Quito", "addressRegion": "Pichincha", "addressCountry": "EC"}}]}
    h = head("Waterdrop Ecuador | Purificadores de Agua para tu Hogar · Nasfeco", desc, SITE + "waterdrop", SITE + A("wd-page-1016-new-2-pc.jpg"), ld)
    body = top()
    body += banner("Deja los botellones.<br>Toma agua pura.", "Nasfeco es el distribuidor exclusivo oficial de Waterdrop Filter en Ecuador, con presencia en Miami, Florida (EE. UU.): equipos originales, con instalación en Quito, Guayaquil, Cuenca y Loja y envíos a todo el país.",
                   [("Certificados", "NSF/ANSI"), ("Instalación", "En 4 ciudades"), ("Envíos", "A todo Ecuador")],
                   bg=(A("wd-page-1016-new-2-pc.jpg"), A("wd-page-1016-new-2-mo.jpg")),
                   btns='<div class="x-btns"><a href="#ofertas" class="x-btn x-btn-p">Ver ofertas</a><a href="#ahorro" class="x-btn x-btn-o">Calcular mi ahorro</a><button type="button" class="x-btn x-btn-g" data-cv-open>' + svg(I_DOC, 18, 1.8) + ' Ver certificados NSF/ANSI</button></div>', extra=seal("hero")).replace(
        '<div><b>Certificados</b><span>NSF/ANSI</span></div>',
        '<div class="x-metric-btn" data-cv-open role="button" tabindex="0" title="Ver certificados NSF/ANSI"><b>Certificados</b><span>NSF/ANSI · Ver documentos ›</span></div>', 1)
    body += cert_modal("all", "Certificaciones · Waterdrop Ecuador")[0]
    body += picks(["x12", "g5", "g2", "uf", "smart"])
    body += shorts()
    cats_items = [("product-x12.html", A("X__X12-mo.jpg"), "Waterdrop<br>X12", "Máxima pureza y caudal"),
                  ("product-g5p700a.html", "assets/g5/wd-g5p700a-product_6.jpg", "Waterdrop<br>G5P700A", "Alcalino y compacto"),
                  ("product-g2p600.html", "assets/g2/ui-wd-g2p600-product-new-vis_6.jpg", "Waterdrop<br>G2P600", "Ósmosis inversa al mejor precio"),
                  ("product-uf.html", "assets/uf/UB-UF_6.jpg", "Ultrafiltración<br>UF", "Sin luz y sin desperdicio de agua"),
                  ("product-smart.html", "assets/smart-gal-1.png.jpg", "Dispensador<br>ED01", "Para departamentos y arriendos")]
    ci = "".join(f'<a href="{u}" class="x-cat x-rv"><img src="{i}" alt="" loading="lazy"><div><h3>{t}</h3><span>{d}</span></div><span class="go">{svg(I_RIGHT, 14, 2.5)}</span></a>' for u, i, t, d in cats_items)
    body += f'''
<section class="x-sec">
  <div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">¿Cuál va con tu casa?</h2><p class="x-lead">Cinco equipos para cada forma de vivir. Si no estás seguro, te asesoramos sin costo.</p></div><div class="x-cats">{ci}</div></div>
</section>'''
    body += problems([
        (A("e58138043c3bf3914a737c6178db46ed264df1f8.jpg"), "El filtro se demora", "Purificadores con tanque que se vacían justo cuando estás cocinando."),
        (A("1013-_page___1_38.jpg"), "Sabe a cloro", "El agua de la red llega segura, pero con cloro, sarro y un sabor que no provoca."),
        (A("1013-_page___1_36.jpg"), "Tanques y bacterias", "El agua quieta en un tanque bajo el fregadero no es la mejor idea."),
        (A("1013-_page___1_39.jpg"), "Instalaciones eternas", "Visitas, perforaciones y mangueras por todos lados antes del primer vaso."),
    ], title="¿Te pasa algo de esto en casa?")
    body += calc("x12", ("g2", "g5", "x12", "uf"))
    body += flow("Sin tanque. Sin esperas.", "El agua pasa directo por los filtros y sale lista para tomar: una taza en 2 a 3 segundos.",
                 "77c38a7052694b8783f1ed958242d847", "cdf34b274a4f4038a953a7e2414abac0", cap="<span><b>Izquierda:</b> ósmosis inversa sin tanque</span><span><b>Derecha:</b> purificador común</span>")
    body += speed("Lo que antes tomaba minutos", "Tiempos aproximados con la Waterdrop X12 de 1200 galones por día", [
        ("wd-product-1016-page-banner-flux-1.jpg", "3 s", "Una taza para el café de la mañana"),
        ("wd-product-1016-page-banner-flux-2.jpg", "13 s", "Una jarra para el almuerzo"),
        ("wd-product-1016-page-banner-flux-3.jpg", "26 s", "Una olla para la sopa")])
    body += scene()
    body += cmp_cats(None)
    body += fullvid("Agua pura, <b>al instante</b>", "Del grifo a tu vaso en segundos. Así se vive con un purificador Waterdrop en casa.", "790107de19ad4d96887b0018d718590e", "5d9d093d9363400bb4c2c29d274b0a4b")
    body += servicio()
    body += brandcards()
    body += bubbles()
    body += b2b()
    body += faq([
        ("¿Por qué necesito un purificador si el agua de mi ciudad es potable?", "El agua de la red llega potabilizada, pero en el camino puede recoger sedimentos y sarro de las tuberías, y lleva cloro, que se nota en el sabor. Un purificador elimina todo eso."),
        ("¿Nasfeco es distribuidor oficial de Waterdrop?", "Sí. Nasfeco es el distribuidor exclusivo oficial de Waterdrop Filter en Ecuador. Vendemos equipos originales con garantía, repuestos y soporte técnico local."),
        ("¿Qué purificador me conviene?", "Si quieres la máxima pureza y caudal, elige la Waterdrop X12. Si buscas ósmosis inversa con minerales alcalinos, el G5P700A. Si quieres ósmosis inversa sin tanque al mejor precio, el G2P600. Si tu agua de red es de buena calidad y prefieres algo sin electricidad, la Ultrafiltración UF es ideal. Si vives en departamento o arriendo y no quieres instalar nada, el Dispensador ED01 es perfecto."),
        ("¿Hacen envíos a todo Ecuador?", "Sí. Trabajamos en todo el Ecuador. En Quito, Guayaquil, Cuenca y Loja coordinamos la instalación con nuestros técnicos; en otras ciudades te acompañamos por WhatsApp."),
        ("¿Qué incluye el precio?", "El precio que ves es el precio final, sin costos adicionales. En la X12, el G5P700A, el G2P600 y la Ultrafiltración UF incluye todo: IVA e instalación. El Dispensador ED01 no necesita instalación; su precio incluye IVA y el envío se cotiza aparte."),
        ("¿Cómo pago mi pedido?", "Agrega tus productos al carrito y finaliza el pedido por WhatsApp. Un asesor confirma disponibilidad y te indica las formas de pago."),
        ("¿Cómo uso el código de descuento?", "Los códigos se incluyen automáticamente en tu pedido de WhatsApp. El descuento es válido hasta que termine la cuenta regresiva."),
        ("¿Cada cuánto se cambian los filtros?", "Depende del modelo y de tu consumo. Todos los equipos te avisan cuándo cambiarlos y Nasfeco mantiene repuestos originales en stock."),
        ("¿Quién responde por la garantía?", "Nasfeco S.A. La gestionamos aquí en Ecuador: si algo falla, nos escribes y lo resolvemos sin que tengas que tratar con el exterior."),
    ])
    body += f'''
<section class="x-sec gray" id="contacto">
  <div class="x-wrap x-ct">
    <div class="x-rv"><p class="x-eyebrow">Asesoría gratuita</p><h2>Hablemos de tu agua</h2>
      <p>Cuéntanos cuántos son en casa y dónde viven. Un asesor de Nasfeco te recomienda el equipo ideal y coordina la instalación contigo.</p>
      <div class="x-ct-line">{WA} +593 99 731 2362</div><div class="x-ct-line">{svg(I_PIN, 22, 1.8)} Miami, Florida (EE. UU.)</div><div class="x-ct-line">{svg(I_PIN, 22, 1.8)} Ecuador: Quito, Guayaquil, Cuenca y Loja · Trabajamos en todo el país</div></div>
    <form class="x-form x-rv" id="wdf">
      <div class="x-fg"><label for="w_name">Nombre</label><input id="w_name" required placeholder="Ej. María García"></div>
      <div class="x-fg"><label for="w_email">Email</label><input id="w_email" type="email" required placeholder="maria@gmail.com"></div>
      <div class="x-fg"><label for="w_phone">Teléfono / WhatsApp</label><input id="w_phone" type="tel" required placeholder="Ej. 0999999999"></div>
      <div class="x-fg"><label for="w_interest">Me interesa</label><select id="w_interest"><option>Waterdrop X12</option><option>Waterdrop G5P700A</option><option>Waterdrop G2P600</option><option>Ultrafiltración UF</option><option>Dispensador ED01</option><option>Filtros de repuesto</option><option>No sé, quiero asesoría</option></select></div>
      <div class="x-fg"><label for="w_context">Cuéntanos de tu hogar</label><textarea id="w_context" required placeholder="Familia de 4 personas en casa, Cumbayá..."></textarea></div>
      <button type="submit" class="x-btn x-btn-p x-btn-block">Solicitar asesoría gratuita</button>
    </form>
  </div>
</section>'''
    form_js = '''<script>
document.getElementById('wdf').addEventListener('submit', async e => {
  e.preventDefault();
  const b = e.target.querySelector('button'), txt = b.textContent, v = id => document.getElementById(id).value;
  b.textContent = 'Enviando...'; b.disabled = true;
  try {
    const r = await fetch('https://guachotw1.app.n8n.cloud/webhook/727f04bc-196b-4e54-947b-70ed61e854dd', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ source: 'Waterdrop B2C', name: v('w_name'), email: v('w_email'), phone: v('w_phone'), interest: v('w_interest'), context: v('w_context') }) });
    if (r.ok || r.type === 'opaque') { b.textContent = '¡Solicitud enviada! Te contactaremos pronto'; e.target.reset(); return; }
    throw new Error();
  } catch (err) { b.textContent = 'Error al enviar. Intenta de nuevo.'; setTimeout(() => { b.textContent = txt; b.disabled = false; }, 3000); }
});
</script>'''
    return h + body.replace('</section>', '</section>', 1) + bottom(form_js).replace('<footer class="x-foot">', '<footer class="x-foot" style="margin-top:0">')

# =========================================================== PÁGINAS SIMPLES (UF / ED01)
def simple_page(pid, file, title, desc, h1, eyebrow, sub, metrics, gallery, banner_title, banner_sub, banner_img, rows, faqs):
    ld = {"@context": "https://schema.org", **offer_ld(pid, "Waterdrop " + h1, desc, gallery, file)}
    h = head(title, desc, SITE + file, SITE + gallery[0], ld)
    body = top((h1, [("#detalles", "Resumen"), ("#comparar", "Comparar"), ("#faq", "Preguntas")], pid))
    body += banner(banner_title, banner_sub, metrics, prod=banner_img, card=banner_img.endswith("uf-hero.jpg"))
    thumbs = "".join(f'<button class="{"on" if i == 0 else ""}" data-thumb="{g}" aria-label="Imagen {i+1}"><img src="{g}" alt="" loading="lazy"></button>' for i, g in enumerate(gallery))
    m = "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in metrics)
    body += f'''
<section class="x-sec" id="ofertas">
  <div class="x-wrap x-pbuy">
    <div><div class="x-gal-main"><img id="x-gal-main" src="{gallery[0]}" alt="{h1}"></div><div class="x-gal-th">{thumbs}</div></div>
    <div class="x-pinfo">
      <p class="x-eyebrow">{eyebrow}</p><h1>{h1}</h1><p>{sub}</p>
      <div class="x-metrics">{m}</div>
      <div class="x-price">{price_in(pid)}<span class="x-off" data-off="{pid}" data-promo></span></div>
      <div style="margin-top:12px">{code(pid)}</div>
      <div class="x-pcd" data-promo><span><span data-promo-name></span> · termina en</span>{cd()}</div>
      {buttons(pid)}
      {PERKS}
    </div>
  </div>
</section>'''
    rr = "".join(f'<div class="x-fr x-rv"><div class="x-fr-m"><img src="{img}" alt="{t}" loading="lazy"></div><div><p class="x-eyebrow">{e}</p><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{c}</li>" for c in cs)}</ul></div></div>' for img, e, t, d, cs in rows)
    body += f'''
<section class="x-sec" id="detalles"><div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Pensado para tu día a día</h2></div><div class="x-feat-rows">{rr}</div></div></section>'''
    body += servicio(video=False)
    body += nature()
    body += cmp_cats(pid)
    body += b2b()
    body += faq(faqs)
    return h + body + bottom()

def page_uf():
    g = [f"assets/uf-gal-{i}.png.png" for i in range(1, 6)]
    return simple_page("uf", "product-uf.html", "Ultrafiltración UF | Waterdrop Ecuador · Nasfeco",
        "Sistema de ultrafiltración Waterdrop UF en Ecuador: membrana de 0.01 μm, sin electricidad, 0% desperdicio de agua y conserva los minerales. Oferta por tiempo limitado.",
        "Ultrafiltración UF", "Bajo el fregadero · Sin electricidad",
        "Agua limpia que conserva sus minerales naturales. Sin electricidad, sin desperdicio y con mantenimiento en segundos.",
        [("0.01 μm", "Membrana UF"), ("0%", "Desperdicio"), ("12 meses", "Por filtro")], g,
        "Agua limpia,<br>sin gastar luz", "Ultrafiltración Waterdrop: conserva los minerales del agua y no desperdicia ni una gota.", "assets/x/uf-hero.jpg",
        [("assets/home/wd-product-ubuf-overviews-img3.jpg", "Diseño compacto", "Ocupa muy poco bajo el fregadero", "El filtro va directo a la tubería y deja libre casi todo el mueble para tus cosas.", ["Instalación en minutos", "Conexiones rápidas a presión", "Grifo de acero inoxidable sin plomo"]),
         ("assets/home/wd-undersink-ub-uf-img-8.png", "En la cocina", "Para cocinar y lavar alimentos", "Quita lo que no quieres y conserva los minerales: ideal para cocinar, lavar frutas y verduras y los platos.", ["Conserva los minerales", "Sin electricidad", "0% de desperdicio"]),
         ("assets/home/wd-undersink-ub-uf-img-10.png", "En la oficina", "Agua limpia para todo el equipo", "Suficiente caudal para oficinas pequeñas, sin luz ni desperdicio de agua.", ["Sin tomacorriente", "Caudal constante", "Mantenimiento mínimo"]),
         (g[0], "Filtro integrado", "Todo en un solo filtro", "Las tres etapas de filtración van en un único cartucho: menos piezas, menos fugas y nada de complicaciones.", ["Conexión giratoria en 3 s", "0 fugas", "Sin contaminación al cambiarlo"]),
         (g[2], "Mantenimiento", "Gira para quitar, gira para poner", "Cambias el filtro tú mismo en segundos, sin herramientas y sin cerrar la llave de paso.", ["3 s para quitar", "3 s para instalar", "Sin herramientas"]),
         (g[3], "Recordatorio", "Te avisa cuándo cambiar el filtro", "Un indicador con luz y sonido te recuerda el cambio en el momento justo.", ["Luz azul: filtro en buen estado", "Luz roja y pitido: hora de cambiar", "Siempre agua de calidad"]),
         (g[4], "Larga duración", "Un filtro para todo el año", "Cada cartucho dura hasta 12 meses u 8000 galones, suficiente para una familia completa.", ["Hasta 12 meses", "Hasta 8000 galones", "Ideal para familias"]),
         ("assets/home/wd-undersink-ub-uf-img-9.webp", "Cuidado personal", "Agua suave también para tu piel", "Úsala para lavarte la cara o en tu rutina de cuidado: agua filtrada que mantiene la piel fresca.", ["Sin cloro", "Conserva minerales", "Libre de BPA y plomo"])],
        [("¿La UF necesita electricidad?", "No. Funciona únicamente con la presión de agua de tu casa, así que no gasta luz y sigue funcionando aunque se vaya la energía."),
         ("¿Cuál es la diferencia con la ósmosis inversa?", "La UF retiene bacterias, óxido y sedimentos y conserva los minerales, pero no reduce las sales disueltas (TDS). Si tu agua tiene mucho sarro o metales pesados, te recomendamos la Serie X."),
         ("¿Cada cuánto se cambia el filtro?", "Hasta 12 meses u 8000 galones, según tu consumo. El indicador te avisa con luz y sonido."),
         ("¿Lo puedo instalar yo mismo?", "Sí, la instalación toma menos de 40 minutos. Si prefieres, los técnicos de Nasfeco lo instalan por ti en Quito, Guayaquil, Cuenca y Loja."),
         ("¿Tiene garantía?", "Sí. Cuenta con garantía y soporte técnico local de Nasfeco S.A.")])

def page_smart():
    g = ["assets/smart-gal-1.png.jpg"] + [f"assets/smart-gal-{i}.png.png" for i in range(2, 7)]
    return simple_page("smart", "product-smart.html", "Dispensador ED01 | Waterdrop Ecuador · Nasfeco",
        "Dispensador purificador eléctrico Waterdrop ED01 en Ecuador: 3.5 L, agua filtrada en 1 segundo, reduce 35+ contaminantes, batería de 30 días. Sin instalación.",
        "Dispensador Inteligente ED01", "Sobre la mesa · Sin instalación",
        "Agua purificada en 1 segundo, donde la necesites. Sin tuberías ni técnicos: llénalo, toca el botón y sirve.",
        [("3.5 L", "Capacidad"), ("1 s", "Agua al instante"), ("35+", "Contaminantes")], g,
        "Agua pura,<br>sin instalar nada", "Dispensador Waterdrop ED01: lo llenas, lo cargas y listo. Perfecto si vives en arriendo.", "assets/smart-gal-1.png.jpg",
        [(g[1], "Velocidad", "Purificación instantánea", "Olvídate de esperar a que el agua baje por gravedad: la bomba eléctrica entrega agua filtrada en un segundo.", ["Agua en 1 segundo", "Filtración 10X más eficiente", "Úsalo en cualquier lugar"]),
         (g[2], "Filtración", "Reduce más de 35 contaminantes", "Su filtro de 5 μm de alta densidad reduce PFOS, PFOA, plomo, microplásticos, cloro y más.", ["PFOS / PFOA", "Plomo y microplásticos", "Cloro, sabor y olor"]),
         (g[4], "Inteligente", "Siempre sabes cómo está tu filtro", "Indicadores de encendido y de vida del filtro te avisan cuándo cargar la batería y cuándo cambiar el filtro.", ["Indicador de encendido", "Indicador de vida del filtro", "Batería de 5000 mAh: hasta 30 días"]),
         (g[5], "Comparación", "Mucho mejor que una jarra tradicional", "Más capacidad, sin esperas y sin inclinar una jarra pesada para servir.", ["3.5 L vs 1.5 L", "1 s vs varios minutos", "Toca un botón en vez de verter"]),
         (g[3], "Certificación", "Certificado NSF/ANSI 42, 53, 401 y 372", "Probado por laboratorios independientes bajo las normas NSF/ANSI.", ["Grado alimenticio", "Libre de BPA", "Materiales sin plomo"])],
        [("¿Necesita instalación?", "No. Solo llénalo con agua del grifo, cárgalo y úsalo. Es ideal si vives en arriendo o no quieres modificar tu cocina."),
         ("¿Cuánto dura la batería?", "Hasta 30 días de uso normal con una sola carga gracias a su batería de 5000 mAh."),
         ("¿Reduce el TDS (sales disueltas)?", "No. El ED01 reduce cloro, plomo, PFAS, microplásticos y más de 35 contaminantes, pero conserva los minerales y no reduce el TDS. Para eso te recomendamos la Serie X de ósmosis inversa."),
         ("¿Cada cuánto se cambia el filtro?", "Depende de tu consumo. El indicador de vida del filtro te avisa cuándo cambiarlo, y el cambio toma segundos."),
         ("¿Tiene garantía?", "Sí. Cuenta con garantía y soporte técnico local de Nasfeco S.A.")])


# =====================================================================
#  v5 · Ofertas propias de Nasfeco + páginas premium para cada producto
# =====================================================================
I_CHECK = "M20 6L9 17l-5-5"
DROP_PATH = "M446 0 L835 590 A446 446 0 1 1 57 590 Z"

OFFER = {
    "x12": ("El favorito", "Serie X · 1200 GPD", "Waterdrop X12", ["1200 GPD", "11 etapas", "pH 7.5", "Grifo inteligente"]),
    "x16": ("El más rápido", "Serie X · 1600 GPD", "Waterdrop X16", ["1600 GPD", "Taza en 2 s", "pH 7.5", "Familias grandes"]),
    "x8":  ("Para empezar", "Serie X · 800 GPD", "Waterdrop X8", ["800 GPD", "10 etapas", "pH 7.5", "Grifo con pantalla"]),
    "uf":  ("Sin electricidad", "Bajo el fregadero", "Ultrafiltración UF", ["0.01 μm", "0% desperdicio", "Conserva minerales"]),
    "smart": ("Sin instalación", "Sobre la mesa", "Dispensador ED01", ["Agua en 1 s", "30+ contaminantes", "Portátil"]),
}
OFFER_IMG = {"x12": "assets/x12/ui-wd-x12-new-vis-pr-logo.webp", "x16": "assets/x16/X16-LOGO-2.webp", "x8": "assets/x8/ui-wd-x8-a-new-vis-main.webp",
             "uf": "assets/uf-gal-1.png.png", "smart": "assets/ed01/1_33c5e044-eb97-4485-ae99-684bc658886e.webp"}
OFFER_URL = {"x12": "product-x12.html", "x16": "product-x16.html", "x8": "product-x8.html", "uf": "product-uf.html", "smart": "product-smart.html"}

def pick(pid):
    badge, kick, name, specs = OFFER[pid]
    sp = "".join(f"<li>{x}</li>" for x in specs)
    return f'''<article class="x-of">
      <span class="x-of-badge">{badge}</span>{"" if pid in QUOTE else f'<span class="x-of-save" data-promo>Ahorras <b data-saveamt="{pid}"></b></span>'}
      <a class="x-of-img" href="{OFFER_URL[pid]}"><img src="{OFFER_IMG[pid]}" alt="{name}" loading="lazy"></a>
      <div class="x-of-b"><span class="x-of-k">{kick}</span><h3><a href="{OFFER_URL[pid]}">{name}</a></h3><ul class="x-of-specs">{sp}</ul>
        <div class="x-price">{price_in(pid)}</div>{code(pid)}{buttons(pid)}
        <p class="x-of-nf">{svg(I_SHIELD, 16, 1.8)} Instalación, garantía y soporte de Nasfeco</p></div>
    </article>'''

def picks(ids, title="Ofertas de la temporada", sub="Precios finales en dólares: incluyen IVA e instalación. Trabajamos en todo el Ecuador, con instalación en Quito, Guayaquil, Cuenca y Loja.", sid="ofertas"):
    return f'''
<section class="x-offers" id="{sid}">
  <div class="x-wrap">
    <div class="x-offers-head x-rv">
      <div><p class="x-eyebrow" style="text-align:left">Distribuidor exclusivo oficial · Waterdrop Filter</p><h2 class="x-h2">{title}</h2><p class="x-lead">{sub}</p></div>
      <div class="x-offers-cd" data-promo><span>La oferta termina en</span>{cd()}</div>
    </div>
    <div class="x-car x-rv" data-car>
      <button class="x-arrow prev" aria-label="Anterior">{svg(I_LEFT, 16)}</button>
      <div class="x-car-track">{"".join(pick(i) for i in ids)}</div>
      <button class="x-arrow next" aria-label="Siguiente">{svg(I_RIGHT, 16)}</button>
      <div class="x-prog"><i></i></div>
    </div>
  </div>
</section>'''

def vid(path, cls="", auto=True):
    return f'<video class="{cls}" {"data-auto " if auto else ""}muted loop playsinline preload="none" poster="{path}-poster.jpg"><source src="{path}.mp4" type="video/mp4"></video>'

def media(src, alt=""):
    return vid(src[:-4]) if src.endswith(".mp4") else f'<img src="{src}" alt="{alt}" loading="lazy">'

def flow2(title, sub, pc, mo, sid="", cap=""):
    return f'''
<section class="x-flow" data-flow{f' id="{sid}"' if sid else ""}>
  <div class="x-flow-stage">
    <div class="x-flow-head"><h2>{title}</h2><p>{sub}</p></div>
    <div class="x-flow-media">{vid(pc, "pc")}{vid(mo, "mo")}{f'<div class="x-flow-cap">{cap}</div>' if cap else ""}</div>
  </div>
</section>'''

def drop(video, title, sub, ph=7.5):
    return f'''
<section class="x-drop" data-drop data-ph="{ph}" id="minerales">
  <div class="x-drop-stage">
    <div class="x-drop-media">{vid(video)}</div>
    <svg class="x-drop-shape" viewBox="0 0 892 1252" aria-hidden="true"><path d="{DROP_PATH}" fill="#fff"/></svg>
    <div class="x-drop-c"><p class="x-eyebrow">Agua alcalina</p><h2>{title}</h2><p>{sub}</p>
      <div class="x-drop-val">pH {ph}±</div><div class="x-drop-bar"><i></i></div>
      <div class="x-drop-scale"><span>0</span><span>4</span><span>7</span><span>10</span><span>14</span></div></div>
  </div>
</section>'''

def premium(c):
    """c: dict con la configuración del producto."""
    pid = c["pid"]
    ld = {"@context": "https://schema.org", **offer_ld(pid, c["ld_name"], c["desc"], c["gallery"][:3], c["file"])}
    h = head(c["title"], c["desc"], SITE + c["file"], SITE + c["gallery"][0], ld)
    body = top((c["short"], [("#resumen", "Resumen"), ("#comparar", "Comparar"), ("#faq", "Preguntas")], pid))
    thumbs = "".join(f'<button class="{"on" if i == 0 else ""}" data-thumb="{g}" aria-label="Imagen {i+1}"><img src="{g}" alt="" loading="lazy"></button>' for i, g in enumerate(c["gallery"]))
    m = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in c["metrics"])
    fl = ""
    if c.get("filters"):
        fl = '<p class="x-eyebrow" style="margin-top:28px">Filtros de repuesto</p><div class="x-box-main" style="grid-template-columns:repeat(3,1fr);gap:10px;margin:0">' + \
             "".join(f'<a class="x-bi x-bi-link" href="repuestos#{FID.get(n, "")}" target="_blank" rel="noopener" style="padding:10px"><img src="{i}" alt="" loading="lazy"><span>{n}<br><small style="font-weight:400;color:#888">{d}</small></span><b class="x-bi-price" data-price="{FID.get(n, "")}"></b><em>Comprar →</em></a>' for i, n, d in c["filters"]) + "</div>"
    body += f'''
<section class="x-sec" id="ofertas" style="padding-top:40px">
  <div class="x-wrap x-pbuy">
    <div><div class="x-gal-main"><img id="x-gal-main" src="{c["gallery"][0]}" alt="{c["h1"]}">{seal("gal") if c.get("seal") else ""}</div><div class="x-gal-th">{thumbs}</div></div>
    <div class="x-pinfo">
      <p class="x-eyebrow">{c["eyebrow"]}</p><h1>{c["h1"]}</h1><p>{c["sub"]}</p>
      <div class="x-metrics">{m}</div>
      <div class="x-price">{price_in(pid)}{"" if pid in QUOTE else f'<span class="x-off" data-off="{pid}" data-promo></span>'}</div>
      {"" if pid in QUOTE else f'<div style="margin-top:12px">{code(pid)}</div><div class="x-pcd" data-promo><span><span data-promo-name></span> · termina en</span>{cd()}</div>'}
      {buttons(pid)}
      {PERKS}
      {fl}
    </div>
  </div>
</section>'''
    body += shorts(pid, title="Míralo en acción", lead=f"Así funciona {c.get('art', 'la')} {c['short']} en una casa real: instalación, uso del grifo y agua pura al instante. En Ecuador la instalan los técnicos de Nasfeco.")
    if c.get("sp"):
        spc = "".join(f'<div class="{cls} x-rv">{media(src, t)}<div class="t"><b>{t}</b><span>{d}</span></div></div>' for cls, src, t, d in c["sp"])
        body += f'''
<section class="x-sec" id="resumen"><div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">{c["sp_title"]}</h2></div><div class="x-sp">{spc}</div></div></section>'''
    else:
        body += '<span id="resumen"></span>'
    if c.get("ba"):
        tabs = "".join(f'<button class="x-tab{" on" if i == 0 else ""}" data-ba-tab="ba{i}">{t}</button>' for i, (t, *_r) in enumerate(c["ba"]))
        knob = svg(I_ARROWS, 20, 2.2)
        bas = "".join(f'<div class="x-ba{" on" if i == 0 else ""}" id="ba{i}"><img src="{i1}" alt="{a}" loading="lazy"><img class="after" src="{i2}" alt="{b}" loading="lazy"><span class="bar"></span><span class="knob">{knob}</span><span class="lab a">{a}</span><span class="lab b">{b}</span></div>'
                      for i, (t, i1, i2, a, b) in enumerate(c["ba"]))
        body += f'''
<section class="x-sec" data-ba><div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">{c["ba_title"]}</h2><p class="x-lead">Desliza para comparar con lo que tienes hoy.</p></div>
  <div class="x-ba-tabs">{tabs}</div><div class="x-rv">{bas}</div></div></section>'''
    if c.get("flow"):
        body += flow2(*c["flow"])
    if c.get("drop"):
        body += drop(*c["drop"])
    for mt in c.get("mt", []):
        src, eb, t, d, rev = mt
        ml = f'<div class="x-rv" style="border-radius:var(--r-card);overflow:hidden">{media(src, t)}</div>'
        tx = f'<div class="x-rv"><p class="x-eyebrow">{eb}</p><h2>{t}</h2><p>{d}</p></div>'
        body += f'<section class="x-sec"><div class="x-wrap x-mt">{tx + ml if rev else ml + tx}</div></section>'
    if c.get("feats"):
        fc = "".join(f'<article class="x-feat"><div class="x-feat-m">{media(src, t)}</div><h3>{t}</h3><p>{d}</p></article>' for src, t, d in c["feats"])
        body += f'''
<section class="x-sec"><div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">{c["feats_title"]}</h2></div>
  <div class="x-car x-rv" data-car><button class="x-arrow prev" aria-label="Anterior">{svg(I_LEFT, 16)}</button><div class="x-car-track">{fc}</div><button class="x-arrow next" aria-label="Siguiente">{svg(I_RIGHT, 16)}</button><div class="x-prog"><i></i></div></div></div></section>'''
    if c.get("rows"):
        rr = "".join(f'<div class="x-fr x-rv"><div class="x-fr-m"><img src="{img}" alt="{t}" loading="lazy"></div><div><p class="x-eyebrow">{e}</p><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in cs)}</ul></div></div>' for img, e, t, d, cs in c["rows"])
        body += f'<section class="x-sec"><div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">{c.get("rows_title", "Pensado para tu día a día")}</h2></div><div class="x-feat-rows">{rr}</div></div></section>'
    if c.get("detail"):
        imgs = "".join(f'<img class="x-rv" src="{i}" alt="" loading="lazy">' for i in c["detail"])
        body += f'<section class="x-sec"><div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">{c.get("detail_title", "Más detalles del producto")}</h2></div><div class="x-detail{" two" if c.get("detail_two") else ""}">{imgs}</div></div></section>'
    body += servicio(video=False)
    if c.get("cert"):
        pc, mo, t, d = c["cert"]
        modal, btn = cert_modal(pid, "Certificados · " + c["short"])
        zoom = '<span class="x-cert-zoom">' + svg(I_DOC, 18, 1.8) + ' Ver certificados NSF/ANSI</span>' if modal else ""
        body += f'''
<section class="x-sec" id="certificacion"><div class="x-wrap x-cert">
  <div class="x-rv"><p class="x-eyebrow">Calidad comprobada</p><h2>{t}</h2><p>{d}</p>{btn}</div>
  <div class="x-cert-img x-rv{" x-cert-click" if modal else ""}"{" data-cv-open role='button' tabindex='0'" if modal else ""}>{pic(pc, mo, t)}{zoom}</div></div></section>{modal}'''
    if c.get("specs"):
        rows = "".join(f'<div style="display:flex;justify-content:space-between;gap:16px;padding:14px 0;border-bottom:1px solid #eee;font-size:15px"><span style="color:#777">{a}</span><b style="font-weight:600;text-align:right">{b}</b></div>' for a, b in c["specs"])
        simg = f'<div class="x-rv" style="border-radius:var(--r-card);overflow:hidden;background:var(--s2)"><img src="{c["spec_img"]}" alt="Medidas" loading="lazy" style="width:100%"></div>' if c.get("spec_img") else "<div></div>"
        body += f'<section class="x-sec"><div class="x-wrap x-mt" style="align-items:start">{simg}<div class="x-rv"><p class="x-eyebrow">Ficha técnica</p><h2>Especificaciones</h2>{rows}</div></div></section>'
    if c.get("box"):
        bx = "".join(f'<div class="x-bi"><img src="{i}" alt="" loading="lazy"><span>{t}</span></div>' for i, t in c["box"])
        body += f'''
<section class="x-sec" id="caja"><div class="x-wrap"><div class="x-head x-rv"><h2 class="x-h2">Todo lo que llega a tu casa</h2><p class="x-lead">Trae lo necesario para instalarlo. Manual de usuario incluido.</p></div>
  <div class="x-box-acc x-rv" style="grid-template-columns:repeat(5,minmax(0,1fr))">{bx}</div></div></section>'''
    body += cmp_cats(pid)
    body += bubbles()
    body += b2b()
    body += faq(c["faq"])
    return h + body + bottom()

# --------------------------------------------------------------- X16
G16 = "assets/x16/"
X16 = dict(pid="x16", file="product-x16.html", short="Waterdrop X16", ld_name="Waterdrop X16 Ósmosis Inversa 1600 GPD",
    title="Waterdrop X16 · 1600 GPD | Waterdrop Ecuador · Nasfeco",
    desc="Waterdrop X16 en Ecuador: ósmosis inversa sin tanque de 1600 GPD, 11 etapas, pH 7.5 con minerales y grifo digital. Instalación y soporte de Nasfeco en Quito, Guayaquil, Cuenca y Loja.",
    gallery=[G16 + f for f in ["X16-LOGO-2.webp", "ui-wd-x16-s-new-vis-main.webp", "ui-wd-x16-new-vis-main-white.jpg", "X16_system.png", "X16_2.jpg", "X16_3.jpg",
                               "X16_5.jpg", "X16_6.jpg", "X16_714501c9-eaa2-49d0-8078-8e9c3cdddb90.jpg", "X16-NSF_ANTI-4258372.jpg", "RO_reduce_lead.jpg", "X16-Spec.jpg"]],
    eyebrow="Serie X · El más rápido", h1="Waterdrop X16 · Ósmosis inversa sin tanque",
    sub="1600 galones por día: agua pura al instante para familias grandes, con minerales alcalinos y grifo digital.",
    metrics=[("1600", "GPD"), ("3:1", "Agua pura / desecho"), ("pH 7.5", "Con minerales")],
    filters=[(G16 + "ui-wd-f1a-product.png", "F1A", "Hasta 12 meses"), (G16 + "ui-wd-f2_FILTER.webp", "F2", "Hasta 6 meses"), (G16 + "ui-wd-x16-f3-filter.webp", "X16-F3", "Hasta 24 meses")],
    sp_title="Todo lo que hace la X16",
    sp=[("wide", G16 + "9ac939bc5196472ab8f19a9a11f1fc87.mp4", "1600 GPD", "Una taza en 2 segundos"),
        ("", G16 + "wd-new-vis-product-overview-smart-img1.jpg", "3:1", "3 litros puros por cada litro desechado"),
        ("", G16 + "wd-new-vis-X16-Set_of_selling_points-img2.jpg", "Flujo directo", "Sin tanque, sin esperas"),
        ("", G16 + "wd-new-vis-X16-Set_of_selling_points-img4.jpg", "11 etapas", "Membrana de 0.0001 μm"),
        ("", G16 + "wd-new-vis-X16-Set_of_selling_points-img5.jpg", "Minerales", "pH equilibrado 7.5±"),
        ("", G16 + "wd-new-vis-X16-Set_of_selling_points-img6.jpg", "Grifo digital", "TDS y vida del filtro"),
        ("", G16 + "wd-new-vis-product-UV-Sterilization-img1.jpg", "Protección LED", "Barrera extra en el circuito de agua")],
    ba_title="Pásate a la X16",
    ba=[(t, f"{G16}wd-new-vis-product-x16-12.11-Comparison{n}.webp", f"{G16}wd-new-vis-product-x16-12.11-Comparison{n+1}.webp", a, b) for t, n, a, b in
        [("Rápido", 1, "Purificador tradicional", "Waterdrop X16"), ("Compacto", 3, "Sistema con tanque", "Waterdrop X16"), ("Saludable", 5, "Agua sin tratar", "Agua X16 con minerales"), ("Inteligente", 7, "Grifo común", "Grifo digital X16")]],
    flow=("El flujo más rápido de la Serie X", "Con 1600 galones por día, la X16 llena un vaso, una tetera o una olla casi tan rápido como lo pides.",
          G16 + "ddda58eee82c4baaa6c44b59f87beb9d", G16 + "9ac939bc5196472ab8f19a9a11f1fc87", "velocidad"),
    drop=(G16 + "62b310e01b534bf98c5bca01f40a5a06", "Más saludable en cada vaso", "La X16 ajusta el agua purificada a un pH de 7.5± y le suma calcio y magnesio para un sabor más suave."),
    mt=[(G16 + "38fc560a5a7b46c2b2d5d6b2549e4ceb.mp4", "Filtración", "Más pura con 11 etapas", "Membrana de ósmosis inversa de 0.0001 μm y protección LED que reducen TDS, PFOA, PFOS, cloro, flúor, arsénico, plomo y más. Al final, una capa mineral le devuelve calcio y magnesio.", False),
        (G16 + "wd-new-vis-x16-save_1200_water-pc.png", "Sostenibilidad", "Desperdicia mucho menos agua", "Por cada litro que va al desagüe, la X16 entrega 3 litros de agua pura. Muchos purificadores tradicionales hacen exactamente lo contrario.", True)],
    feats_title="Pensada para el día a día",
    feats=[(G16 + "6461bec2afa04e249094b1830110110b.mp4", "Volumen a tu medida", "Programa el volumen para un vaso, una botella o la olla y el grifo se detiene solo."),
           (G16 + "wd-new-vis-product-X16-Image_and_text-img2.jpg", "Grifo inteligente", "Control táctil, monitor de TDS en tiempo real y aviso de cambio de filtro."),
           (G16 + "wd-new-vis-product-X16-Image_and_text-img3.jpg", "Filtros de larga duración", "El filtro RO dura hasta 24 meses y se cambia en 3 segundos, sin herramientas."),
           (G16 + "wd-new-vis-product-X16-Image_and_text-img4.jpg", "Canales integrados", "Menos mangueras y uniones: más eficiencia y menos riesgo de fugas.")],
    cert=(G16 + "wd-product-x16-wd-new-vis-authentication-img-pc.jpg", G16 + "wd-product-x16-wd-new-vis-authentication-img-mo.jpg", "Certificada NSF/ANSI 42, 58 y 372",
          "Probada por IAPMO R&amp;T: reduce TDS, PFOA, PFOS, cloro, flúor, bario, arsénico, sedimentos, cromo VI, plomo, microplásticos y olores, entre otros."),
    specs=[("Modelo", "WD-X16"), ("Capacidad", "1600 GPD"), ("Agua pura / desecho", "3:1"), ("Filtración", "11 etapas"), ("Certificación", "NSF/ANSI 42, 58 y 372"),
           ("Grifo", "Digital inteligente"), ("Medidas", "46 × 16 × 42 cm"), ("Peso", "17.8 kg"), ("Electricidad", "Sí, tomacorriente bajo el fregadero")],
    spec_img=G16 + "X16-Spec.jpg",
    box=[(G16 + i, t) for i, t in [("X16_system.png", "Equipo X16"), ("wd-product-1016-page-in-the-box-product-2-x16.png", "Juego de filtros"), ("wd-product-1016-page-in-the-box-product-3-x16.png", "Grifo inteligente"),
         ("X_Power_adapter.png", "Adaptador de corriente"), ("X_Red_14_PE_tubing60.png", "Manguera de desagüe"), ("Feed_water_adapter_inlet_water_tubing.png", "Conector de entrada"),
         ("X_Drain_saddle.png", "Abrazadera de desagüe"), ("X_Reference_sticker.webp", "Plantilla para el grifo"), ("X_Teflon_tape.png", "Cinta de teflón ×2"), ("X_Lock_clip.png", "Seguros ×4")]],
    faq=[("¿Cada cuánto se cambian los filtros?", "F1A cada 12 meses, F2 cada 6 meses y X16-F3 cada 24 meses, según el uso. El grifo te avisa cuándo cambiarlos."),
         ("¿Qué diferencia hay con la X12?", "La X16 tiene más caudal (1600 vs 1200 galones por día) y está pensada para familias grandes. La filtración de 11 etapas y los minerales son los mismos."),
         ("¿Necesita electricidad?", "Sí. Necesita un tomacorriente bajo el fregadero para la bomba sin tanque, el grifo digital y la protección LED."),
         ("¿Quién responde por la garantía?", "Nasfeco. La gestionamos aquí en Ecuador: si algo falla, nos escribes y lo resolvemos."),
         ("¿En qué ciudades instalan?", "Instalamos con técnicos de Nasfeco en Quito, Guayaquil, Cuenca y Loja, y trabajamos en todo el Ecuador. En otras ciudades te acompañamos por WhatsApp durante la instalación, que trae guía paso a paso.")])

# --------------------------------------------------------------- X12
G12 = "assets/x12/"
X12 = dict(pid="x12", seal=True, file="product-x12.html", short="Waterdrop X12", ld_name="Waterdrop X12 Ósmosis Inversa 1200 GPD",
    title="Waterdrop X12 · 1200 GPD | Waterdrop Ecuador · Nasfeco",
    desc="Waterdrop X12 en Ecuador: ósmosis inversa sin tanque de 1200 GPD, 11 etapas, minerales alcalinos y grifo inteligente. Instalación y soporte de Nasfeco en Quito, Guayaquil, Cuenca y Loja.",
    gallery=[G12 + f for f in ["ui-wd-x12-main-sello.webp", "ui-wd-x12-b-new-vis-main.webp", "ui-wd-x12-new-vis-pr-logo-white.jpg", "WD_X12_new.webp", "1226-WD-_1016-1200g__2.jpg",
                               "1226-WD-_1016-1200g__3.jpg", "X12_3.jpg", "X12_4.jpg", "1226-WD-_1016-1200g__7.jpg", "X12_8.jpg", "X12-NSF_ANTI-4258372.jpg", "RO_reduce_lead.jpg", "X12-Spec.jpg"]],
    eyebrow="Serie X · El más vendido", h1="Waterdrop X12 · Ósmosis inversa sin tanque",
    sub="El equilibrio perfecto para la mayoría de familias: agua pura al instante, minerales alcalinos y grifo inteligente.",
    metrics=[("1200", "GPD"), ("3:1", "Agua pura / desecho"), ("pH 7.5", "Con minerales")],
    filters=[(G12 + "ui-wd-f1a-product.png", "F1A", "Hasta 12 meses"), (G12 + "ui-wd-f2_FILTER.webp", "F2", "Hasta 6 meses"), (G12 + "ui-wd-x12-f3-fIlter.webp", "X12-F3", "Hasta 24 meses")],
    sp_title="Todo lo que hace la X12",
    sp=[("wide", G12 + "fd1e33f5b69e4a4e9c566a669b921a1f.mp4", "1200 GPD", "Una taza en 3 segundos"),
        ("", G12 + "wd-new-vis-product-overview-smart-img1.jpg", "3:1", "3 litros puros por cada litro desechado"),
        ("", G12 + "wd-new-vis-product-overview-smart-img2.jpg", "11 etapas", "Membrana de 0.0001 μm"),
        ("", G12 + "wd-new-vis-product-overview-smart-img3.jpg", "Minerales", "pH equilibrado 7.5±"),
        ("", G12 + "wd-new-vis-product-overview-smart-img4.jpg", "Grifo digital", "TDS y vida del filtro")],
    ba_title="Pásate a la X12",
    ba=[("Sabor", G12 + "wd-new-vis-product-x12-12.11-Comparison1-12.12.webp", G12 + "wd-new-vis-product-x12-12.11-Comparison2-12.12.webp", "Agua con mal sabor", "Agua X12"),
        ("Seguridad", G12 + "wd-new-vis-product-x16-12.11-Comparison3.webp", G12 + "wd-new-vis-product-x12-12.11-Comparison4.png", "Sistema tradicional", "Waterdrop X12"),
        ("Saludable", G12 + "wd-new-vis-product-x16-12.11-Comparison5.webp", G12 + "wd-new-vis-product-x16-12.11-Comparison6.webp", "Agua sin tratar", "Agua X12 con minerales"),
        ("Ecológico", G12 + "wd-new-vis-product-x12-Comparison7.jpg", G12 + "wd-new-vis-product-x12-Comparison8.jpg", "Botellones", "Waterdrop X12")],
    flow=("Una taza en 3 segundos", "Con 1200 galones por día, la X12 te da agua pura apenas abres el grifo. Sin tanque y sin esperas.",
          G12 + "b86901cd108444c0bd0205e76b91a3f7", G12 + "88d751e9916e4e4b96ac3fca31cf7c6c", "velocidad"),
    drop=(G12 + "7f24c79c8deb40ad8173c66aa62464a8", "Más saludable con minerales alcalinos", "La X12 ajusta el pH del agua a 7.5± y le suma calcio y magnesio: mejor para ti y mejor para el sabor de tus comidas y bebidas."),
    mt=[(G16 + "38fc560a5a7b46c2b2d5d6b2549e4ceb.mp4", "Filtración", "Más pura con 11 etapas", "Membrana de 0.0001 μm y protección LED que reducen TDS, PFOA, PFOS, cloro, flúor, arsénico, plomo y más.", False),
        (G12 + "56261930927b4e0d81d011c35a1c8059.mp4", "Instalación", "Lista en unos 30 minutos", "Su diseño sin tanque libera hasta un 70% del espacio bajo el fregadero y se instala fácil. En Quito, Guayaquil, Cuenca y Loja, los técnicos de Nasfeco la dejan funcionando.", True),
        (G12 + "wd-new-vis-product-1200_-pc.png", "Sostenibilidad", "Desperdicia mucho menos agua", "Por cada litro que va al desagüe, la X12 entrega 3 litros de agua pura.", False)],
    feats_title="Detalles que marcan la diferencia",
    feats=[(G12 + "wd-new-vis-product-Take_apart-img2.jpg", "Protección LED", "Una luz LED en el circuito de agua agrega una barrera extra para que cada vaso sea más seguro."),
           (G12 + "wd-product-new-vis-X12W-Take_apart-img3.jpg", "Filtro de larga duración", "El filtro RO dura hasta 24 meses: menos cambios y menos gasto."),
           (G12 + "wd-product-new-vis-X12W-Take_apart-img2.jpg", "Sin tanque", "Ahorra hasta un 70% del espacio bajo el fregadero."),
           (G12 + "wd-new-vis-product-Take_apart-img3.jpg", "Materiales seguros", "Libre de BPA y de plomo, pensado para años de uso diario.")],
    detail_title="Más detalles", detail=[G12 + "wd-product-X12-2025-2-21-PC.jpg"],
    cert=(G12 + "wd-new-vis-Authentication-img2-pc.jpg", G12 + "wd-new-vis-Authentication-img2-mo.jpg", "Certificada NSF/ANSI 42, 58 y 372",
          "Probada por IAPMO R&amp;T según NSF/ANSI 58 para las sustancias de su hoja de rendimiento y NSF/ANSI 372 para materiales bajos en plomo."),
    specs=[("Modelo", "WD-X12"), ("Capacidad", "1200 GPD"), ("Agua pura / desecho", "3:1"), ("Filtración", "11 etapas"), ("Certificación", "NSF/ANSI 42, 58 y 372"),
           ("Grifo", "Inteligente"), ("Medidas", "46 × 16 × 42 cm"), ("Peso", "17.7 kg"), ("Electricidad", "Sí, tomacorriente bajo el fregadero")],
    spec_img=G12 + "X12-Spec.jpg",
    box=[(G12 + i, t) for i, t in [("wd-product-1016-page-in-the-box-img1.webp", "Equipo X12"), ("wd-product-1016-page-in-the-box-img8.webp", "3 filtros"), ("X12_Smart_faucet.png", "Grifo inteligente"),
         ("X_Power_adapter.png", "Adaptador de corriente"), ("X_Red_14_PE_tubing60.png", "Manguera de desagüe"), ("Feed_water_adapter_inlet_water_tubing.png", "Conector de entrada"),
         ("X_Drain_saddle.png", "Abrazadera de desagüe"), ("X_Reference_sticker.webp", "Plantilla para el grifo"), ("X_Teflon_tape.png", "Cinta de teflón ×2"), ("X_Lock_clip.png", "Seguros ×4")]],
    faq=[("¿Por qué la X12 es la más recomendada?", "Tiene el caudal suficiente para una familia de 3 a 5 personas, 11 etapas de filtración, minerales alcalinos y grifo con volumen programable."),
         ("¿Cada cuánto se cambian los filtros?", "F1A cada 12 meses, F2 cada 6 meses y X12-F3 cada 24 meses, según el uso. El grifo te avisa cuándo cambiarlos."),
         ("¿Necesita electricidad?", "Sí, un tomacorriente bajo el fregadero para la bomba sin tanque, el grifo y la protección LED."),
         ("¿Quién responde por la garantía?", "Nasfeco. La gestionamos aquí en Ecuador."),
         ("¿En qué ciudades instalan?", "Instalamos con técnicos de Nasfeco en Quito, Guayaquil, Cuenca y Loja, y trabajamos en todo el Ecuador. En otras ciudades te acompañamos por WhatsApp durante la instalación.")])

# --------------------------------------------------------------- X8
G8 = "assets/x8/"
D8 = lambda n: f"{G8}wd-x-series-alkaline-detail-img{n}.jpg"
X8 = dict(pid="x8", file="product-x8.html", short="Waterdrop X8", ld_name="Waterdrop X8 Ósmosis Inversa 800 GPD",
    title="Waterdrop X8 · 800 GPD | Waterdrop Ecuador · Nasfeco",
    desc="Waterdrop X8 en Ecuador: ósmosis inversa sin tanque de 800 GPD, 10 etapas, minerales alcalinos y grifo con pantalla. Instalación y soporte de Nasfeco en Quito, Guayaquil, Cuenca y Loja.",
    gallery=[G8 + f for f in ["ui-wd-x8-a-new-vis-main.webp", "ui-wd-x8-a-new-vis-main-white.jpg", "WD-X8_3.jpg", "WD-X8_4.jpg", "WD-X8_5.jpg", "WD-X8_6.jpg",
                              "ui-wd-x8-a-product_1.jpg", "ui-wd-x8-a-product_3.jpg", "ui-wd-x8-a-product_4.jpg", "ui-wd-x8-a-product_5.jpg", "ui-wd-x8-a-product_6.jpg", "wd-x8-spec.jpg"]],
    eyebrow="Serie X · Para empezar", h1="Waterdrop X8 · Ósmosis inversa sin tanque",
    sub="La forma más accesible de tener ósmosis inversa en casa: agua pura y alcalina, sin tanque y con grifo que te muestra la calidad del agua.",
    metrics=[("800", "GPD"), ("2:1", "Agua pura / desecho"), ("10", "Etapas")],
    filters=[(G8 + "ui-wd-f1a-product.png", "F1A", "Hasta 12 meses"), (G8 + "ui-wd-f2_FILTER.webp", "F2", "Hasta 6 meses"), (G8 + "ui-wd-x8-f3-filter.webp", "X8-F3", "Hasta 24 meses")],
    drop=(G12 + "7f24c79c8deb40ad8173c66aa62464a8", "Pura y con minerales", "La X8 purifica con ósmosis inversa y luego le devuelve minerales alcalinos al agua para un pH equilibrado."),
    rows_title="Por qué elegir la X8",
    rows=[(D8(12), "Para toda la familia", "Mejor agua, mejor sabor", "Agua más rica para tomar, preparar café o té y cocinar tus comidas.", ["Agua más saludable", "Mejor sabor en bebidas", "Comidas más ricas"]),
          (D8(15), "Filtración", "10 etapas con minerales", "Membrana de ósmosis inversa de 0.0001 μm y una etapa final que agrega minerales alcalinos.", ["Membrana de 0.0001 μm", "Minerales alcalinos", "Certificada NSF/ANSI"]),
          (D8(16), "Velocidad", "800 galones por día", "Flujo constante e inmediato, sin tanque que se vacíe a mitad de la cocina.", ["Sin tanque", "Flujo estable", "Agua al instante"]),
          (D8(20), "Instalación", "Sin tanque, sin complicaciones", "Ocupa hasta un 70% menos espacio y se instala en unos 30 minutos.", ["70% menos espacio", "Instalación rápida", "Técnicos Nasfeco en Quito, Guayaquil, Cuenca y Loja"]),
          (D8(21), "Mantenimiento", "Cambia el filtro en 3 segundos", "Giras, sacas y pones el nuevo. Sin herramientas ni mover el equipo.", ["Sin herramientas", "Sin goteos", "En segundos"]),
          (D8(23), "Grifo con pantalla", "Calidad del agua a la vista", "El grifo muestra el TDS en tiempo real, el estado de los filtros y alertas.", ["Monitor de TDS", "Aviso de cambio de filtro", "Alertas de falla"]),
          (D8(24), "Sostenibilidad", "Menos agua desperdiciada", "Por cada litro que va al desagüe, entrega 2 litros de agua pura.", ["Relación 2:1", "Menos botellones", "Menos plástico"]),
          (D8(25), "Larga duración", "Filtros de hasta 24 meses", "Menos cambios de filtro y un costo de mantenimiento más bajo.", ["F1A: 12 meses", "F2: 6 meses", "X8-F3: 24 meses"])],
    detail_title="Comparado con un RO tradicional", detail=[D8(22)],
    cert=(G8 + "RO_reduce_lead.jpg", G8 + "RO_reduce_lead.jpg", "Certificada NSF/ANSI 42, 58 y 372", "Certificada por IAPMO R&amp;T. Reduce plomo, PFOA/PFOS, flúor, cloro, sabor y olor, entre otros contaminantes."),
    specs=[("Modelo", "WD-X8-A"), ("Capacidad", "800 GPD"), ("Agua pura / desecho", "2:1"), ("Filtración", "10 etapas"), ("Certificación", "NSF/ANSI 42, 58 y 372"),
           ("Grifo", "Con pantalla (TDS y vida del filtro)"), ("Medidas", "46 × 16 × 42 cm"), ("Peso", "16.1 kg"), ("Electricidad", "Sí, tomacorriente bajo el fregadero")],
    spec_img=G8 + "wd-x8-spec.jpg",
    box=[(G8 + i, t) for i, t in [("x8-in_the_box-system.png", "Equipo X8"), ("ui-wd-x8-a-in_the_box-filters.png", "Juego de filtros"), ("x8-pro-inthebox-smartfaucet.png", "Grifo con pantalla"),
         ("X_Power_adapter.png", "Adaptador de corriente"), ("X_Red_14_PE_tubing60.png", "Manguera de desagüe"), ("Feed_water_adapter_inlet_water_tubing.png", "Conector de entrada"),
         ("x8-in_the_box-Drain_saddle.png", "Abrazadera de desagüe"), ("wd-page-1016-collection-x8-a-inthebox-img7.webp", "Plantilla para el grifo"), ("X_Teflon_tape.png", "Cinta de teflón"), ("X_Lock_clip.png", "Seguros")]],
    faq=[("¿Qué diferencia hay entre la X8 y la X12?", "La X8 tiene 800 galones por día, 10 etapas y relación 2:1. La X12 tiene 1200 galones, 11 etapas, relación 3:1 y grifo con volumen programable."),
         ("¿Para cuántas personas alcanza?", "Ideal para parejas y familias pequeñas de 1 a 3 personas."),
         ("¿Cada cuánto se cambian los filtros?", "F1A cada 12 meses, F2 cada 6 meses y X8-F3 cada 24 meses, según el uso."),
         ("¿Necesita electricidad?", "Sí, un tomacorriente bajo el fregadero."),
         ("¿Quién responde por la garantía?", "Nasfeco, aquí en Ecuador.")])

# --------------------------------------------------------------- UF
UF = dict(pid="uf", file="product-uf.html", short="Ultrafiltración UF", ld_name="Waterdrop Ultrafiltración UF 10UB",
    title="Ultrafiltración UF | Waterdrop Ecuador · Nasfeco",
    desc="Sistema de ultrafiltración Waterdrop 10UB-UF en Ecuador: membrana de 0.01 μm, sin electricidad, sin desperdicio y conserva los minerales. Incluye grifo de acero inoxidable e instalación.",
    gallery=["assets/uf/10UB-UF-NSF-feed.jpg", "assets/uf/10UB-UF-NSF.png", "assets/uf/UB-UF_6.jpg", "assets/uf/UB-UF_7.jpg", "assets/uf/UB-UF_4.jpg", "assets/uf/UB-UF_3.jpg", "assets/uf/UB-UF_9.jpg", "assets/uf/UB-UF_8.jpg", "assets/uf/WD-RF10-UF-NSF.png", "assets/uf/dedicated-faucet-ultrafiltration.png"],
    eyebrow="Bajo el fregadero · Sin electricidad", h1="Waterdrop Ultrafiltración UF",
    sub="Agua limpia que conserva sus minerales naturales. Sin electricidad, sin desperdicio de agua y con grifo de acero inoxidable incluido.",
    metrics=[("0.01 μm", "Membrana UF"), ("0%", "Desperdicio"), ("12 meses", "Por filtro")],
    filters=[("assets/uf/WD-RF10-UF-NSF.png", "RF10-UF", "Hasta 12 meses")],
    rows_title="Pensado para tu día a día",
    rows=[("assets/uf/wd-undersink-ub-uf-img-1.webp", "Membrana UF", "Retiene lo que no se ve", "Todo lo que mida más de 0.01 micras se queda en la membrana: óxido, bacterias, quistes y sedimentos.", ["Membrana de 0.01 μm", "Retiene bacterias", "Conserva minerales"]),
          ("assets/uf/UB-UF_6.jpg", "Larga duración", "Un filtro para todo el año", "Cada filtro dura hasta 12 meses u 8000 galones: suficiente para toda la familia.", ["Hasta 12 meses", "Hasta 8000 galones", "Ideal para familias"]),
          ("assets/uf/UB-UF_7.jpg", "Filtro integrado", "Se cambia en 3 segundos", "Conexión giratoria sin herramientas, sin fugas y sin ensuciar el mueble.", ["Cambio en 3 s", "0 fugas", "Sin contaminación"]),
          ("assets/uf/UB-UF_4.jpg", "Mayor eficiencia", "Más área de filtración", "Su estructura plisada tiene mucha más superficie: filtra mejor y se tapa menos.", ["20× más área", "Menos obstrucciones", "Caudal estable"]),
          ("assets/uf/UB-UF_3.jpg", "Recordatorio", "Te avisa cuándo cambiar el filtro", "Un indicador con luz te dice cuándo toca el cambio.", ["Luz azul: todo bien", "Luz roja: hora de cambiar", "Siempre agua de calidad"]),
          ("assets/uf/UB-UF_9.jpg", "Grifo incluido", "Grifo de acero inoxidable 304", "Grifo dedicado con acabado cepillado, sin plomo, que combina con cualquier cocina.", ["Acero inoxidable 304", "Sin plomo", "Incluido en la caja"]),
          ("assets/uf/wd-undersink-ub-uf-img-8.png", "En la cocina", "Para tomar, cocinar y lavar alimentos", "Quita lo que no quieres y conserva los minerales.", ["Conserva los minerales", "Sin electricidad", "0% de desperdicio"])],
    feats_title="Agua limpia en cada momento",
    feats=[("assets/uf/wd-undersink-ub-uf-img-10.png", "En la oficina", "Agua limpia para todo el equipo, sin luz ni desperdicio."),
           ("assets/uf/wd-undersink-ub-uf-img-9.webp", "Cuidado personal", "Agua filtrada que mantiene la piel fresca."),
           ("assets/uf/wd-product-ubuf-overviews-img3.jpg", "Diseño compacto", "Ocupa muy poco bajo el fregadero."),
           ("assets/uf/wd-product-ubuf-overviews-img1.jpg", "Instalación rápida", "Conexiones a presión: queda lista en minutos.")],
    detail_title="Más detalles", detail=["assets/uf/UB-UF_8.jpg"],
    specs=[("Modelo", "WD-10UB-UF"), ("Filtración", "Membrana UF de 0.01 μm"), ("Caudal", "2.8 L/min"), ("Vida del filtro", "12 meses / 30 000 L"),
           ("Medidas", "9 × 10 × 31 cm"), ("Peso", "1.7 kg"), ("Temperatura del agua", "2 a 38 °C"), ("Electricidad", "No necesita"), ("Grifo", "Acero inoxidable 304 sin plomo, incluido")],
    spec_img="assets/uf/10UB-UF-NSF.png",
    faq=[("¿La UF necesita electricidad?", "No. Funciona con la presión de agua de tu casa, así que no gasta luz."),
         ("¿Cuál es la diferencia con la ósmosis inversa?", "La UF retiene bacterias, óxido y sedimentos y conserva los minerales, pero no reduce las sales disueltas (TDS). Para eso te recomendamos la X12 o el G5P700A."),
         ("¿Cada cuánto se cambia el filtro?", "Hasta 12 meses u 8000 galones, según tu consumo."),
         ("¿El precio incluye instalación?", "Sí. Es el precio final: incluye IVA e instalación, sin costos adicionales."),
         ("¿Quién responde por la garantía?", "Nasfeco, distribuidor exclusivo oficial de Waterdrop Filter en Ecuador.")])

# --------------------------------------------------------------- ED01
GE = "assets/ed01/"
EB = lambda n: f"{GE}wd-product-countertop-electric-water-pitcher-ed01a-pc-img{n}.jpg"
ED = dict(pid="smart", file="product-smart.html", short="Dispensador ED01", ld_name="Waterdrop Dispensador ED01",
    title="Dispensador ED01 | Waterdrop Ecuador · Nasfeco",
    desc="Dispensador purificador eléctrico Waterdrop ED01 en Ecuador: agua filtrada en 1 segundo, reduce más de 30 contaminantes, portátil y sin instalación.",
    gallery=[GE + f for f in ["1_33c5e044-eb97-4485-ae99-684bc658886e.webp", "319IZ2UmO8L.jpg", "41Au5hMvngL.jpg", "51ii-WXfo8L.jpg",
                             "White-AlkalineAlkaline-02.jpg", "White-AlkalineAlkaline-08.jpg", "White-AlkalineAlkaline-09.jpg"]],
    eyebrow="Sobre la mesa · Sin instalación", h1="Dispensador Inteligente ED01", filters=[("assets/filtros/wd-edf.webp", "WD-EDF", "Hasta 3 meses")],
    sub="Agua filtrada en 1 segundo, donde la necesites. Sin tuberías ni técnicos: lo llenas, tocas el botón y sirves.",
    metrics=[("1 s", "Agua al instante"), ("30+", "Contaminantes"), ("15", "Tazas de capacidad")],
    detail_title="Conócelo en detalle",
    detail=[EB(3), EB(10), EB(11), EB(6), EB(7), EB(8), EB(9)], detail_two=True,
    cert=(GE + "White-AlkalineAlkaline-02.jpg", GE + "White-AlkalineAlkaline-02.jpg", "Certificado NSF/ANSI 42 y 372",
          "Probado por laboratorios independientes: reduce cloro, PFOA/PFOS, plomo, sabor y olor, entre más de 30 contaminantes."),
    specs=[("Modelo", "WD-ED01A"), ("Caudal", "Hasta 0.8 L/min"), ("Capacidad", "15 tazas"), ("Vida del filtro", "Filtro WD-EDF: 3 meses o 200 galones"), ("Medidas", "18 × 25 × 26 cm"),
           ("Instalación", "No necesita"), ("Alimentación", "Batería recargable")],
    spec_img=GE + "1_33c5e044-eb97-4485-ae99-684bc658886e.webp",
    faq=[("¿Necesita instalación?", "No. Solo llénalo con agua del grifo, cárgalo y úsalo. Ideal si vives en arriendo."),
         ("¿Cuándo cambio el filtro?", "Cuando el indicador parpadee en rojo y suene. Cada filtro WD-EDF dura hasta 3 meses o 200 galones."),
         ("¿Reduce el TDS?", "No. Para reducir sales disueltas te recomendamos la Serie X de ósmosis inversa."),
         ("¿Quién responde por la garantía?", "Nasfeco, aquí en Ecuador.")])

def page_x16(): return premium(X16)
def page_x12(): return premium(X12)
def page_x8(): return premium(X8)
def page_uf(): return premium(UF)
def page_smart(): return premium(ED)


# =====================================================================
#  v6 · G3P800, G3P600 y K6
# =====================================================================
PRICES.update({"g800": (849, 999), "g600": (439, 539), "k6": (599, 799)})
OFFER.update({
    "g800": ("Más vendido", "Serie G · 800 GPD", "Waterdrop G3P800", ["800 GPD", "10 etapas", "UV incluido", "Grifo con pantalla"]),
    "g600": ("Nuevo", "Serie G · 600 GPD", "Waterdrop G3P600", ["600 GPD", "8 etapas", "Sin tanque", "Grifo con pantalla"]),
    "k6":   ("Agua caliente", "Serie K · 600 GPD", "Waterdrop K6", ["Agua caliente al instante", "40–95 °C", "600 GPD", "Doble pantalla"]),
})
OFFER["x8"] = ("Accesible", "Serie X · 800 GPD", "Waterdrop X8-A", ["800 GPD", "10 etapas", "pH 7.5", "Grifo con pantalla"])
PRICES["g5"] = (1399, 1699)
PRICES.update({"x12": (1999, 2200), "uf": (299, 380), "smart": (99, 129)})
OFFER["g5"] = ("Alcalino", "Serie G5 · 700 GPD", "Waterdrop G5P700A", ["700 GPD", "8 etapas", "Minerales alcalinos", "Grifo con pantalla"])
OFFER["x12"] = ("El más completo", "Serie X · 1200 GPD", "Waterdrop X12", ["1200 GPD", "11 etapas", "pH 7.5", "Grifo inteligente"])
OFFER_IMG["g5"] = "assets/g5/ui-wd-g5p700a-product.webp"
OFFER_URL["g5"] = "product-g5p700a.html"
HOT_PROD["x12"] = ("assets/x12/ui-wd-x12-new-vis-pr-logo.webp", "Waterdrop X12 · Ósmosis inversa sin tanque, 1200 GPD", "product-x12.html")
HOT_PROD["uf"] = ("assets/uf/10UB-UF-NSF.png", "Waterdrop Ultrafiltración UF · Sin electricidad", "product-uf.html")
HOT_PROD["smart"] = ("assets/ed01/1_33c5e044-eb97-4485-ae99-684bc658886e.webp", "Waterdrop ED01 · Dispensador purificador portátil", "product-smart.html")
HOT_PROD["g5"] = ("assets/g5/ui-wd-g5p700a-product.webp", "Waterdrop G5P700A · Ósmosis inversa alcalina, 700 GPD", "product-g5p700a.html")
OFFER_IMG["uf"] = "assets/uf/10UB-UF-NSF.png"
OFFER_IMG.update({"g800": "assets/g800/G3P800-LOGO-2.webp", "g600": "assets/g600/ui-wd-g3p600-product_1.png", "k6": "assets/k6/ui-wd-k6-product_3.webp"})
OFFER_URL.update({"g800": "product-g3p800.html", "g600": "product-g3p600.html", "k6": "product-k6.html"})
HOT_PROD.update({"x16": ("assets/home/ui-wd-x16-ph-product.webp", "Waterdrop X16 · Ósmosis inversa sin tanque, 1600 GPD", "product-x16.html")})

# ---------- G3P800
GG = "assets/g800/"
G8B = lambda n: f"{GG}US-WD-G3P800-W_ERS-1001D___20241010_V2_{n}.jpg"
GG8 = lambda n, e="jpg": f"{GG}wd-product-g3p800-new-vis-img{n}.{e}"
G3P800 = dict(pid="g800", file="product-g3p800.html", short="Waterdrop G3P800", ld_name="Waterdrop G3P800 Ósmosis Inversa 800 GPD",
    title="Waterdrop G3P800 · 800 GPD | Waterdrop Ecuador · Nasfeco",
    desc="Waterdrop G3P800 en Ecuador: ósmosis inversa sin tanque de 800 GPD, 10 etapas, esterilización UV y grifo con pantalla TDS. Instalación y soporte de Nasfeco en Quito, Guayaquil, Cuenca y Loja.",
    gallery=[GG + "G3P800-LOGO-2.webp", GG + "ui-wd-G3P800-new-vis-PR.jpg", G8B(2), G8B(3), G8B(7), G8B(8), G8B(6), G8B(9), G8B(4), GG + "RO_reduce_lead.jpg", GG + "G3P800-NSF-feed.webp", GG + "G3P800-LOGO-1.jpg"],
    eyebrow="Serie G · El más vendido", h1="Waterdrop G3P800 · Ósmosis inversa sin tanque",
    sub="800 galones por día, 10 etapas de filtración y esterilización UV. El purificador más vendido de Waterdrop, ahora con instalación de Nasfeco.",
    metrics=[("800", "GPD"), ("3:1", "Agua pura / desecho"), ("10", "Etapas")],
    filters=[(GG + "ui-wd-g3-n1cf-new.png", "CF", "Hasta 6 meses"), (GG + "ui-wd-g3-n3cb-new.png", "CB", "Hasta 12 meses"), (GG + "800.webp", "G3P800-RO", "Hasta 24 meses")],
    sp_title="Todo lo que hace la G3P800",
    sp=[("wide", GG + "7ce60e95236b4a8ca91ec3967028c5db.mp4", "800 GPD", "Una taza en 5 segundos"),
        ("", GG8(2), "10 etapas", "Membrana de 0.0001 μm"),
        ("", GG8(4), "Grifo inteligente", "Calidad del agua en la pantalla"),
        ("", GG8(6), "Esterilización UV", "Protección extra en la salida"),
        ("", GG8(22), "Sin tanque", "Hasta 70% menos espacio")],
    ba_title="Pásate a la G3P800",
    ba=[("Sabor", GG8(9, "webp"), GG8(10, "webp"), "Agua con mal sabor", "Agua G3P800"),
        ("Seguridad", GG + "wd-new-vis-product-x16-12.11-Comparison3.webp", GG8(12, "webp"), "Sistema tradicional", "Waterdrop G3P800"),
        ("Caudal", GG8(13, "webp"), GG8(14, "webp"), "Flujo lento", "800 GPD al instante"),
        ("Ambiente", GG8(15, "webp"), GG8(16, "webp"), "Botellones", "Waterdrop G3P800")],
    mt=[(GG + "ec076240d21344cfad036003dd4b539d.mp4", "Grifo con pantalla", "Sabes cómo está tu agua", "El grifo muestra el TDS en tiempo real y te avisa cuándo cambiar cada filtro.", False),
        (GG8(24), "Sostenibilidad", "Desperdicia mucho menos agua", "Por cada litro que va al desagüe, la G3P800 entrega 3 litros de agua pura.", True)],
    feats_title="Detalles que marcan la diferencia",
    feats=[(GG + "US-WD-G3P800-W_ERS-1001D___20250410-V3-32_2.jpg", "Filtros de larga duración", "El filtro RO dura hasta 24 meses: equivale a miles de botellones que ya no compras."),
           (GG8(3), "Expertos en agua", "Filtración probada en laboratorio con los estándares NSF/ANSI."),
           (GG8(5), "Membrana de 0.0001 μm", "Retiene metales pesados, sales disueltas y más de 1000 contaminantes.")],
    detail_title="Más detalles", detail=[GG8(18), GG8(26)], detail_two=True,
    cert=(GG8(25), GG8("25-mo"), "Certificada NSF/ANSI 42, 53, 58 y 372",
          "Probada por IAPMO R&amp;T: reduce flúor, PFOA/PFOS, TDS, cromo, cloro, plomo, sabor, olor, metales pesados y sedimentos, entre otros."),
    specs=[("Modelo", "WD-G3P800-W"), ("Capacidad", "800 GPD"), ("Agua pura / desecho", "3:1"), ("Filtración", "10 etapas"), ("Certificación", "NSF/ANSI 42, 53, 58 y 372"),
           ("Grifo", "Con pantalla TDS"), ("Medidas", "46 × 14 × 45 cm"), ("Peso", "14.7 kg"), ("Electricidad", "Sí, tomacorriente bajo el fregadero")],
    spec_img=GG + "wd-g3p800-spec-new.webp",
    box=[(GG + i, t) for i, t in [("ui-wd-g3p800-in_the_box-system.png", "Equipo G3P800"), ("ui-wd-g3p800-in_the_box-filters.png", "Juego de filtros"), ("ui-wd-g3p800-in_the_box-faucet.png", "Grifo"),
         ("wd-g3p600-product-img_10.png", "Adaptador de corriente"), ("ui-wd-g3p800-in_the_box-UV_Sterilizer.png", "Esterilizador UV"), ("ui-wd-g3p800-in_the_box-Feed_water_adapter.png", "Conector de entrada"),
         ("wd-g3p600-product-img_8.png", "Abrazadera de desagüe"), ("wd-g3p600-product-img_4.png", "Manguera"), ("wd-g3p600-product-img_7.png", "Cinta de teflón"), ("ui-wd-g3p800-in_the_box-Lock_Clip.png", "Seguros")]],
    faq=[("¿Qué contaminantes reduce?", "Con 10 etapas reduce PFOA, PFOS, flúor, metales pesados (plomo, cromo, arsénico), sales y partículas grandes."),
         ("¿Cada cuánto se cambian los filtros?", "CF cada 6 meses, CB cada 12 meses y G3P800-RO cada 24 meses, según el uso. El grifo te avisa cuándo cambiarlos."),
         ("¿Qué diferencia hay con la X12?", "La X12 tiene más caudal (1200 GPD), minerales alcalinos y grifo con volumen programable. La G3P800 es la opción más vendida con muy buena relación precio-calidad."),
         ("¿Necesita electricidad?", "Sí, un tomacorriente bajo el fregadero."),
         ("¿Quién responde por la garantía?", "Nasfeco, aquí en Ecuador.")])

# ---------- G3P600
G6 = "assets/g600/"
G6P = lambda n: f"{G6}wd-product-new-vis-G3P600-Point_of_pain-img{n}.webp"
G3P600 = dict(pid="g600", file="product-g3p600.html", short="Waterdrop G3P600", ld_name="Waterdrop G3P600 Ósmosis Inversa 600 GPD",
    title="Waterdrop G3P600 · 600 GPD | Waterdrop Ecuador · Nasfeco",
    desc="Waterdrop G3P600 en Ecuador: ósmosis inversa sin tanque de 600 GPD, 8 etapas y grifo con pantalla TDS. Distribuidor exclusivo oficial: Nasfeco, con instalación en Quito, Guayaquil, Cuenca y Loja.",
    gallery=[G6 + "ui-wd-g3p600-product_1.png"] + [G6 + f"ui-wd-g3p600-product_{n}.jpg" for n in range(1, 9)] + [G6 + "WD-G3P600-NSF.webp", G6 + "WD-G3P600-W-NSF.webp"],
    eyebrow="Serie G · Ósmosis inversa sin tanque", h1="Waterdrop G3P600 · Ósmosis inversa sin tanque",
    sub="Ósmosis inversa completa y compacta: 600 galones por día, 8 etapas y un grifo que te muestra la calidad del agua.",
    metrics=[("600", "GPD"), ("2:1", "Agua pura / desecho"), ("8", "Etapas")],
    sp_title="Todo lo que hace el G3P600",
    sp=[("wide", G6 + "c9a5a9d2f6b04f588ceed80f0810fbd3.mp4", "600 GPD", "Más rápido que un RO tradicional de 400 GPD"),
        ("", G6 + "wd-product-new-vis-G3P600-set-img1.jpg", "Certificada", "NSF/ANSI 42, 58 y 372"),
        ("", G6 + "wd-new-vis-product-overview-smart-img1.jpg", "2:1", "2 litros puros por cada litro desechado"),
        ("", G6 + "wd-new-vis-X16-Set_of_selling_points-img4.jpg", "8 etapas", "Membrana de 0.0001 μm"),
        ("", G6 + "wd-product-new-vis-G3P600-set-img4.jpg", "Sin tanque", "Cabe en casi cualquier mueble")],
    ba_title="Pásate al G3P600",
    ba=[("Pura", G6P(1), G6P(2), "Agua sin tratar", "Agua G3P600"), ("Saludable", G6P(3), G6P(4), "Antes", "Con G3P600"),
        ("Inteligente", G6P(5), G6P(6), "Grifo común", "Grifo con pantalla"), ("Fácil", G6P(7), G6P(8), "Sistema con tanque", "G3P600 sin tanque")],
    flow=("Más rápido de lo que esperas", "Con 600 galones por día, llena un vaso en unos 6.5 segundos, mucho más rápido que un purificador tradicional.",
          G6 + "63de709a824d4dc1bb7bb47c5f8970c5", G6 + "c9a5a9d2f6b04f588ceed80f0810fbd3", "velocidad"),
    mt=[(G6 + "d3c6b4513e1c4fb0b75f68aa6c8f4eb4.mp4", "Filtración", "8 etapas de filtración avanzada", "Membrana de ósmosis inversa de 0.0001 μm que reduce TDS, PFOA, PFOS, cloro, flúor, arsénico, plomo y más.", False),
        (G6 + "aa2ca2b375794b279598a2aeba3ec07f.mp4", "Instalación", "Lista en unos 30 minutos", "Instalación simple, sin plomero. En Quito, Guayaquil, Cuenca y Loja, los técnicos de Nasfeco la dejan funcionando.", True),
        (G6 + "wd-product-new-vis-G3P600-water-pc.jpg", "Sostenibilidad", "Menos agua desperdiciada", "Relación 2:1: por cada litro que va al desagüe, entrega 2 litros de agua pura.", False)],
    feats_title="Detalles que marcan la diferencia",
    feats=[(G6 + "wd-product-new-vis-G3P600-Take_apart-img2.jpg", "Grifo con pantalla", "Muestra el TDS en tiempo real y te avisa cuándo cambiar el filtro."),
           (G6 + "wd-product-new-vis-G3P600-Take_apart-img3.jpg", "Filtro de larga duración", "El filtro RO dura hasta 24 meses."),
           (G6 + "a20ee7cc9b5a4fcb835ee0465de1b6b6.mp4", "Diseño integrado", "Filtros en un solo cuerpo compacto, sin tanque ni mangueras de sobra."),
           (G6 + "db6cf19efaae4464b2b232208b124c47.mp4", "Cambio en segundos", "Cambias los filtros tú mismo, sin herramientas.")],
    cert=(G6 + "wd-product-new-vis-G3P600-Certification_report-pad.jpg", G6 + "wd-product-new-vis-G3P600-Certification_report-mo.jpg", "Certificada NSF/ANSI 42, 58 y 372",
          "Probada por IAPMO R&amp;T según NSF/ANSI 58 y NSF/ANSI 372 para materiales bajos en plomo."),
    specs=[("Modelo", "WD-G3P600"), ("Capacidad", "600 GPD"), ("Agua pura / desecho", "2:1"), ("Filtración", "8 etapas"), ("Certificación", "NSF/ANSI 42, 58 y 372"),
           ("Grifo", "Con pantalla TDS"), ("Medidas", "46 × 14 × 45 cm"), ("Peso", "14.7 kg"), ("Electricidad", "Sí, tomacorriente bajo el fregadero")],
    spec_img=G6 + "wd-g3p600-product-img_1.jpg",
    box=[(G6 + f"wd-g3p600-product-img_{n}.png", t) for n, t in [(1, "Equipo G3P600"), (2, "Juego de filtros"), (3, "Grifo"), (10, "Adaptador de corriente"), (4, "Manguera"),
         (5, "Conector de entrada"), (6, "Seguros ×5"), (7, "Cinta de teflón"), (8, "Abrazadera de desagüe"), (9, "Accesorios")]],
    faq=[("¿Por qué elegir el G3P600?", "Es ósmosis inversa sin tanque con 8 etapas, relación 2:1 y grifo con pantalla, en un equipo compacto."),
         ("¿Qué es la relación 2:1?", "Por cada 2 vasos de agua pura, solo 1 se va al desagüe. Los purificadores tradicionales desperdician mucho más."),
         ("¿Cada cuánto se cambian los filtros?", "CF cada 6 meses, CB cada 12 meses y G3P600-RO cada 24 meses, según el uso."),
         ("¿Necesita electricidad?", "Sí, un tomacorriente bajo el fregadero."),
         ("¿Quién responde por la garantía?", "Nasfeco, distribuidor exclusivo oficial de Waterdrop Filter en Ecuador.")])

# ---------- K6
GK = "assets/k6/"
KV = lambda n, e="jpg": f"{GK}wd-product-k6-vis-img{n}.{e}"
K6 = dict(pid="k6", file="product-k6.html", short="Waterdrop K6", ld_name="Waterdrop K6 Ósmosis Inversa con Agua Caliente",
    title="Waterdrop K6 · Agua Caliente al Instante | Waterdrop Ecuador · Nasfeco",
    desc="Waterdrop K6 en Ecuador: ósmosis inversa sin tanque de 600 GPD con agua caliente al instante de 40 a 95 °C. Purificador, hervidor y dispensador en un solo equipo.",
    gallery=[GK + "ui-wd-k6-product_3.webp", GK + "k6-1.jpg", GK + "4_b2235bc9-71ea-4a76-bca8-97bfc9f4de13.jpg", GK + "k6-2.jpg", GK + "6_521162bb-f036-4646-acf8-1e464d232585.jpg",
             GK + "7_f758891d-dd29-4e8a-88cb-8954d7f603b0.jpg", GK + "k6-5.jpg", GK + "k6-4.jpg", GK + "k6-7.jpg", GK + "k6-nsf32.jpg", GK + "RO_reduce_lead.jpg"],
    eyebrow="Serie K · Agua caliente al instante", h1="Waterdrop K6 · Ósmosis inversa con agua caliente",
    sub="Agua purificada al tiempo o caliente al instante, de 40 a 95 °C, desde el mismo grifo. Purificador, hervidor y dispensador en un solo equipo.",
    metrics=[("40–95 °C", "Agua caliente"), ("600", "GPD"), ("2:1", "Agua pura / desecho")],
    filters=[(GK + "KJF.webp", "KJF", "Hasta 12 meses")],
    sp_title="Todo lo que hace la K6",
    sp=[("wide", GK + "7ce46722375d4254ba5d7a048a0022d7.mp4", "5 equipos en 1", "Purificador, hervidor, tetera, dispensador y agua para el biberón"),
        ("", KV(2), "40 a 95 °C", "Agua caliente al instante"),
        ("", KV(4), "Calor o al tiempo", "Con un toque"),
        ("", KV(5), "Seguridad", "Bloqueo para niños"),
        ("", KV(6), "Doble pantalla", "Temperatura y calidad del agua")],
    ba_title="Pásate a la K6",
    ba=[("Temperatura", KV(9, "webp"), KV(10, "webp"), "Hervidor tradicional", "Agua caliente al instante"), ("Sabor", KV(11, "webp"), KV(12, "webp"), "Agua del grifo", "Agua K6"),
        ("Seguridad", KV(13, "png"), KV(14, "png"), "Sin purificar", "Purificada"), ("Sarro", KV(15, "webp"), KV(16, "webp"), "Con sarro", "Sin sarro")],
    mt=[(GK + "42cd7c057a1c4bc7818823e99c6be51f.mp4", "Filtración", "5 etapas con ósmosis inversa", "Reduce flúor, sedimentos, óxido, TDS, cromo, PFOA y PFOS, y elimina color, sabor, olor y cloro.", False),
        (KV(17), "Agua caliente", "Calor o al tiempo con un toque", "Elige la temperatura exacta para el café, el té, la sopa o el biberón, sin esperar a que hierva.", True),
        (KV(25), "Caudal", "600 GPD: pureza al instante", "Llena una taza en unos 6 segundos.", False)],
    feats_title="Detalles que marcan la diferencia",
    feats=[(KV(19), "Ósmosis inversa premium", "Agua más segura y limpia para toda la familia."),
           (KV(20), "Agua caliente al instante", "De 40 a 95 °C, lista cuando la necesitas."),
           (KV(21), "Grifo con pantalla", "Controla la temperatura y mira la calidad del agua."),
           (KV(27), "Diseño compacto", "Sin tanque, ahorra espacio bajo el fregadero."),
           (KV(28), "Doble pantalla", "Calidad del agua, temperatura y más, a la vista."),
           (KV(29), "Uso seguro", "Tanque de acero inoxidable y detección automática del punto de ebullición.")],
    detail_title="Más detalles", detail=[KV(22), KV(23)], detail_two=True,
    cert=(KV(33), KV("33-mo"), "Certificada NSF/ANSI 372",
          "Materiales bajos en plomo certificados por IAPMO R&amp;T. Reducción de contaminantes probada por laboratorio independiente."),
    specs=[("Modelo", "WD-K6-W"), ("Capacidad", "600 GPD"), ("Agua pura / desecho", "2:1"), ("Filtración", "5 etapas"), ("Agua caliente", "40 a 95 °C"),
           ("Certificación", "NSF/ANSI 372"), ("Medidas", "44 × 17 × 42 cm"), ("Peso", "15.8 kg"), ("Electricidad", "Sí, tomacorriente bajo el fregadero")],
    spec_img=GK + "ui-wd-k6-spec.jpg",
    box=[(GK + i, t) for i, t in [("k6-in_the_box-system.png", "Equipo K6"), ("k6-in_the_box-filter.png", "Filtro KJF"), ("k6-in_the_box-smart_faucet.png", "Grifo inteligente"),
         ("X_Power_adapter.png", "Adaptador de corriente"), ("Feed_water_adapter_inlet_water_tubing.png", "Conector de entrada"), ("k6-in_the_box-Drain_saddle.png", "Abrazadera de desagüe"),
         ("k6-in_the_box-Reference_sticker.png", "Plantilla para el grifo"), ("k6-in_the_box-Teflon_tape.png", "Cinta de teflón"), ("k6-in_the_box-Lock_clip.png", "Seguros"), ("Drain_water_tubing.png", "Manguera de desagüe")]],
    faq=[("¿Qué hace diferente a la K6?", "Combina 5 equipos en 1: purificador de ósmosis inversa, hervidor, tetera, dispensador de agua y agua a temperatura exacta para el biberón."),
         ("¿Qué tan rápido calienta?", "Al instante: eliges la temperatura entre 40 y 95 °C y sale lista del grifo."),
         ("¿Cada cuánto se cambia el filtro?", "El filtro KJF dura hasta 12 meses, según el uso."),
         ("¿Necesita electricidad?", "Sí, un tomacorriente bajo el fregadero para calentar y purificar."),
         ("¿Quién responde por la garantía?", "Nasfeco, aquí en Ecuador.")])

def page_g800(): return premium(G3P800)
def page_g600(): return premium(G3P600)
def page_k6(): return premium(K6)


# --------------------------------------------------------------- G5P700A
GZ = "assets/g5/"
G5P = dict(pid="g5", art="el", file="product-g5p700a.html", short="Waterdrop G5P700A", ld_name="Waterdrop G5P700A Ósmosis Inversa Alcalina 700 GPD",
    title="Waterdrop G5P700A · 700 GPD Alcalino | Waterdrop Ecuador · Nasfeco",
    desc="Waterdrop G5P700A en Ecuador: ósmosis inversa sin tanque de 700 GPD con minerales alcalinos, 8 etapas y grifo con pantalla TDS. Distribuidor exclusivo oficial: Nasfeco.",
    gallery=[GZ + "ui-wd-g5p700a-product.webp"] + [GZ + f"wd-g5p700a-product_{n}.jpg" for n in (2, 3, 1, 4, 5, 6, 7, 9)] + [GZ + "ui-wd-g5p700a-nsf-vis.jpg", GZ + "ui-wd-g5p700a-w.jpg"],
    eyebrow="Serie G5 · Ósmosis inversa alcalina", h1="Waterdrop G5P700A · Ósmosis inversa alcalina",
    sub="700 galones por día, 8 etapas y minerales alcalinos en un equipo compacto y sin tanque. Agua pura y equilibrada a un precio accesible.",
    metrics=[("700", "GPD"), ("2:1", "Agua pura / desecho"), ("pH+", "Alcalina")],
    filters=[(GZ + "ui-wd-g5p700a-cf-product.png", "G5P700A-CF", "Hasta 6 meses"), (GZ + "ui-wd-g5p700-ro-product.png", "G5P700-RO", "Hasta 24 meses")],
    rows_title="Por qué elegir el G5P700A",
    rows=[(GZ + "wd-g5p700a-product_3.jpg", "Salud", "Agua con minerales alcalinos", "Después de purificar, le devuelve minerales al agua para un sabor suave y un pH equilibrado.", ["Minerales alcalinos", "pH equilibrado", "Mejor sabor"]),
          (GZ + "wd-g5p700a-product_2.jpg", "Filtración", "8 etapas con membrana de 0.0001 μm", "Reduce PFOA, PFOS, cloro, plomo, flúor, metales pesados y sales disueltas.", ["Membrana de 0.0001 μm", "Reduce TDS", "Certificada NSF/ANSI 58"]),
          (GZ + "wd-g5p700a-product_4.jpg", "Grifo con pantalla", "Calidad del agua a la vista", "El grifo muestra el TDS en tiempo real y te avisa cuándo cambiar los filtros.", ["Monitor de TDS", "Aviso de cambio de filtro", "Giro de 360°"]),
          (GZ + "wd-g5p700a-product_5.jpg", "Eficiencia", "Mucho menos agua desperdiciada", "Relación 2:1: por cada litro que va al desagüe entrega 2 litros de agua pura.", ["Relación 2:1", "Menos desperdicio", "Ahorro en tu planilla"]),
          (GZ + "wd-g5p700a-product_6.jpg", "Diseño", "Compacto y sin tanque", "Ocupa hasta un 70% menos espacio bajo el fregadero y evita agua estancada.", ["70% menos espacio", "Sin tanque", "Flujo inmediato"]),
          (GZ + "wd-g5p700a-product_7.jpg", "Instalación", "Lista en unos 30 minutos", "No necesita plomero y los filtros se cambian en 3 segundos. En Quito, Guayaquil, Cuenca y Loja la instalan los técnicos de Nasfeco.", ["30 minutos", "Filtros en 3 s", "Cierre automático de agua"]),
          (GZ + "wd-g5p700a-product_9.jpg", "Larga duración", "Filtros de hasta 24 meses", "Menos cambios y un costo de mantenimiento bajo.", ["CF: 6 meses", "RO: 24 meses", "Bajo costo diario"])],
    feats_title="Detalles que marcan la diferencia",
    feats=[(GZ + "US-WD-RG17-BCN__-ERS-S1013DB-CN-_-20250114V1-30_1.jpg", "Flujo constante", "Agua inmediata y estable, sin esperar a que se llene un tanque."),
           (GZ + "wd-product-g5p700a-img10.jpg", "Menos conexiones", "Solo 3 puntos de conexión frente a los 26 de un RO tradicional: menos riesgo de fugas."),
           (GZ + "wd-product-g5p700a-img11.jpg", "Protección contra fugas", "Aviso de fugas, alerta de fallas y cierre automático del agua."),
           (GZ + "wd-product-g5p700a-img4.jpg", "Seguro para toda la familia", "Materiales libres de BPA y de plomo.")],
    detail_title="Más detalles", detail=[GZ + "wd-product-g5p700-new-img3.jpg", GZ + "wd-product-g5p700-new-img1.jpg"],
    cert=(GZ + "wd-product-other-us-x8-Authentication-pc.jpg", GZ + "wd-product-other-us-x8-Authentication-mo.jpg", "Certificada NSF/ANSI 58 y 372",
          "Certificada por IAPMO R&amp;T: reduce TDS, PFOA, PFOS, cloro, flúor, bario, sedimentos, cromo VI, plomo, microplásticos y olores, entre otros."),
    specs=[("Modelo", "G5P700A"), ("Capacidad", "700 GPD"), ("Agua pura / desecho", "2:1"), ("Filtración", "8 etapas"), ("Certificación", "NSF/ANSI 58 y 372"),
           ("Grifo", "Con pantalla TDS"), ("Medidas", "42 × 14 × 35 cm"), ("Peso", "11.8 kg"), ("Electricidad", "Sí, tomacorriente bajo el fregadero")],
    spec_img=GZ + "ui-wd-g5p700a-spec.jpg",
    box=[(GZ + i, t) for i, t in [("ui-wd-g5p700a-system.png", "Equipo G5P700A"), ("ui-wd-g5p700a-cf-product.png", "Filtro CF"), ("ui-wd-g5p700-ro-product.png", "Filtro RO"),
         ("wd-g5p700-faucet.png", "Grifo con pantalla"), ("X_Power_adapter.png", "Adaptador de corriente"), ("X_Red_14_PE_tubing60.png", "Manguera de desagüe"),
         ("Feed_water_adapter_inlet_water_tubing.png", "Conector de entrada"), ("x8-in_the_box-Drain_saddle.png", "Abrazadera de desagüe"),
         ("wd-page-1016-collection-x8-a-inthebox-img7.webp", "Plantilla para el grifo"), ("X_Teflon_tape.png", "Cinta de teflón ×2")]],
    faq=[("¿Qué diferencia hay con la X12?", "La X12 tiene más caudal (1200 GPD), 11 etapas y grifo con volumen programable. El G5P700A ofrece ósmosis inversa con minerales alcalinos en un equipo más compacto y a mejor precio."),
         ("¿Reduce PFOA y PFOS?", "Sí. Sus 8 etapas con membrana de ósmosis inversa reducen PFOA, PFOS, cloro, plomo, flúor y metales pesados."),
         ("¿Cada cuánto se cambian los filtros?", "El filtro CF cada 6 meses y el RO cada 24 meses, según el uso. El equipo te avisa cuando toca cambiarlos."),
         ("¿Necesita instalación profesional?", "No es obligatoria: se instala en unos 30 minutos. En Quito, Guayaquil, Cuenca y Loja, los técnicos de Nasfeco la instalan por ti."),
         ("¿Quién responde por la garantía?", "Nasfeco, distribuidor exclusivo oficial de Waterdrop Filter en Ecuador.")])

def page_g5(): return premium(G5P)

# --------------------------------------------------------------- G2P600
G2D = "assets/g2/"
G2V = lambda n, e="png": f"{G2D}wd-product-g2p600-vis-img{n}.{e}"
G2N = lambda n: f"{G2D}ui-wd-g2p600-product-new-vis_{n}.jpg"
PRICES["g2"] = (900, 1200)
OFFER["g2"] = ("Mejor precio", "Serie G · 600 GPD", "Waterdrop G2P600", ["600 GPD", "7 etapas", "Sin tanque", "Relación 2:1"])
OFFER_IMG["g2"] = G2D + "WD-G2P600-W-NSF.webp"
OFFER_URL["g2"] = "product-g2p600.html"
G2P = dict(pid="g2", art="el", file="product-g2p600.html", short="Waterdrop G2P600", ld_name="Waterdrop G2P600 Ósmosis Inversa 600 GPD",
    title="Waterdrop G2P600 · 600 GPD | Waterdrop Ecuador · Nasfeco",
    desc="Waterdrop G2P600 en Ecuador: ósmosis inversa sin tanque de 600 GPD, 7 etapas y relación 2:1. Precio final con IVA e instalación. Distribuidor exclusivo oficial: Nasfeco.",
    gallery=[G2D + "WD-G2P600-W-NSF.webp", G2N(5), G2N(6), G2N(1), G2N(4), G2N(7), G2N(2), G2N(3), G2D + "ui-wd-g2p600-w-cz-no.png"],
    eyebrow="Serie G · Ósmosis inversa al mejor precio", h1="Waterdrop G2P600 · Ósmosis inversa sin tanque",
    sub="600 galones por día, 7 etapas de filtración y relación 2:1 en un equipo compacto y sin tanque. La forma más accesible de tener ósmosis inversa en casa.",
    metrics=[("600", "GPD"), ("2:1", "Agua pura / desecho"), ("7", "Etapas")],
    filters=[(G2D + "G2CF.png", "G2CF", "Hasta 12 meses"), (G2D + "WD-G2P6MRO.png", "G2P6MRO", "Hasta 24 meses")],
    ba_title="Pásate al G2P600",
    ba=[("Sabor", G2V(10), G2V(11), "Agua del grifo", "Agua G2P600"), ("Bienestar", G2V(12), G2V(13), "Antes", "Con G2P600"),
        ("Tranquilidad", G2V(14), G2V(15), "Antes", "Con G2P600"), ("En familia", G2V(8), G2V(9), "Antes", "Con G2P600")],
    mt=[(G2D + "g2-video.mp4", "Video", "Así funciona el G2P600", "Un vaso de agua pura en unos 8 segundos, 7 etapas de filtración, filtros que se cambian girando y un diseño sin tanque que ahorra espacio bajo el fregadero.", True),
        (G2V(16, "jpg"), "Sostenibilidad", "Desperdicia mucho menos agua", "Relación 2:1: por cada litro que va al desagüe, entrega 2 litros de agua pura. Un purificador tradicional desperdicia mucho más.", False),
        (G2V(18, "jpg"), "Pruebas de laboratorio", "Probado por SGS y CSA", "Probado según las normas NSF/ANSI 42, 53, 58 y 401. Reduce PFOA, PFOS, flúor, cromo VI, arsénico, plomo, nitratos, cloro y más.", True)],
    feats_title="Detalles que marcan la diferencia",
    feats=[(G2V(1, "jpg"), "7 etapas de filtración", "Algodón PP, carbón activado, microfiltración y membrana de ósmosis inversa de 0.0001 μm."),
           (G2N(5), "Flujo rápido", "Llena un vaso en unos 8 segundos, más rápido que un purificador tradicional de 400 GPD."),
           (G2D + "G2CF.png", "Filtros de larga duración", "Filtro CF hasta 12 meses y filtro MRO hasta 24 meses, según el uso."),
           (G2N(7), "Instalación en 30 minutos", "Sin plomero. En Quito, Guayaquil, Cuenca y Loja lo instalan los técnicos de Nasfeco.")],
    cert=(G2V(17, "jpg"), G2V("17-mo", "jpg"), "Certificado NSF/ANSI 372",
          "Materiales bajos en plomo certificados por IAPMO R&amp;T. Además, probado por SGS y CSA según NSF/ANSI 42, 53, 58 y 401."),
    specs=[("Modelo", "WD-G2P600-W"), ("Capacidad", "600 GPD"), ("Agua pura / desecho", "2:1"), ("Filtración", "7 etapas"), ("Membrana", "0.0001 μm"),
           ("Certificación", "NSF/ANSI 372"), ("Pruebas", "SGS y CSA según NSF/ANSI 42, 53, 58 y 401"), ("Filtros", "CF hasta 12 meses · MRO hasta 24 meses"), ("Instalación", "Bajo el fregadero, sin tanque")],
    spec_img=G2D + "ui-wd-g2p600-w-cz-no.png",
    faq=[("¿Qué diferencia hay con el G5P700A?", "El G5P700A tiene más caudal (700 GPD), 8 etapas y minerales alcalinos. El G2P600 es la ósmosis inversa sin tanque más accesible: 600 GPD y 7 etapas."),
         ("¿Qué contaminantes reduce?", "Su membrana de ósmosis inversa de 0.0001 μm reduce TDS, PFOA, PFOS, plomo, cloro, flúor, arsénico, cromo VI, nitratos, sedimentos y más de 1000 contaminantes."),
         ("¿Cada cuánto se cambian los filtros?", "El filtro CF hasta 12 meses y el filtro MRO hasta 24 meses, según el uso. Se cambian girando y sacando, en segundos."),
         ("¿El precio incluye instalación?", "Sí. Es el precio final: incluye IVA e instalación, sin costos adicionales."),
         ("¿Quién responde por la garantía?", "Nasfeco, distribuidor exclusivo oficial de Waterdrop Filter en Ecuador.")])

def page_g2(): return premium(G2P)

for name, fn in [("product-x12.html", page_x12), ("product-g5p700a.html", page_g5), ("product-g2p600.html", page_g2), ("waterdrop.html", page_store), ("product-uf.html", page_uf), ("product-smart.html", page_smart), ("repuestos.html", page_repuestos)]:
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(fn())
    print("ok", name)
