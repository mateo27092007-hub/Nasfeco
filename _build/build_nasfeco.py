import itertools
# -*- coding: utf-8 -*-
"""Genera nasfeco.html (B2B) e index.html (portal) con la nueva marca."""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nf_wow import DAY, CALC, JS as WOWJS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
WA_PATH = re.sub(r'^<path d="|"$', "", open(os.path.join(HERE, "wa_path.txt"), encoding="utf-8").read().strip())
WA = f'<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="{WA_PATH}"/></svg>'
V = "?v=34"

def svg(d, w=24, sw=1.8):
    return f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>'
I_RIGHT = "M9 6l6 6-6 6"; I_MENU = "M4 7h16M4 12h16M4 17h16"; I_X = "M6 6l12 12M18 6L6 18"
I_SHIELD = "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM9 12l2 2 4-4"
I_GLOBE = "M12 22a10 10 0 100-20 10 10 0 000 20zM2 12h20M12 2a15 15 0 010 20M12 2a15 15 0 000 20"
I_CHART = "M3 3v18h18M7 15l4-4 3 3 5-6"
I_PIN = "M12 22s7-6.2 7-12a7 7 0 10-14 0c0 5.8 7 12 7 12zM12 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z"
I_MAIL = "M4 5h16v14H4zM4 6l8 7 8-7"

LOGO_SVG = '<svg viewBox="0 0 200 40" width="{w}" height="{h}" aria-label="Nasfeco S.A." role="img"><g transform="translate(5,5)"><path d="M5 5 L25 15 L5 25 Z" stroke="url(#lg{uid})" stroke-width="4.5" stroke-linejoin="round" fill="none"/><circle cx="5" cy="5" r="5" fill="#10B981"/><circle cx="25" cy="15" r="5" fill="#059669"/><circle cx="5" cy="25" r="5" fill="#00B4D8"/></g><text x="45" y="26" font-family="Times New Roman, serif" font-weight="bold" font-size="22" fill="currentColor" letter-spacing="1">NASFECO S.A</text><defs><linearGradient id="lg{uid}" x1="5" y1="5" x2="25" y2="25" gradientUnits="userSpaceOnUse"><stop offset="0%" stop-color="#10B981"/><stop offset="100%" stop-color="#00B4D8"/></linearGradient></defs></svg>'
_LG = itertools.count()
def nf_logo(color="#0A192F", sub=True, size=30):
    w, h = (150, 30) if sub else (120, 24)
    return '<span class="nf-logo" style="color:' + color + '">' + LOGO_SVG.format(w=w, h=h, uid=next(_LG)) + '</span>'


FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">'''

def head(title, desc, canonical, og, ld, css):
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
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A192F">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{FONTS}
{css}
</head>
<body>
'''

# ===================================================================== NASFECO
SOL = [
    ("nf/solar.jpg", "01", "Energía solar", "Sistemas fotovoltaicos para empresas: diseño, instalación y monitoreo para bajar tu factura eléctrica con energía limpia.",
     ["Estudio de consumo", "Paneles y estructura", "Instalación", "Monitoreo y mantenimiento"]),
    ("nf/agua.jpg", "02", "Purificación de agua", "Agua segura para tu operación y tu equipo: sistemas de ósmosis inversa, ultrafiltración y puntos de agua para oficinas, plantas y comercios.",
     ["Ósmosis inversa", "Ultrafiltración", "Puntos de agua", "Planes de cambio de filtros"]),
    ("nf/quimico.jpg", "03", "Tratamiento químico", "Tratamiento de agua para procesos industriales y mineros, con productos y dosificación según el análisis de cada planta.",
     ["Análisis de agua", "Dosificación", "Procesos industriales", "Minería"]),
    ("nf/consultoria.jpg", "04", "Consultoría técnica", "Te acompañamos desde el diagnóstico hasta la puesta en marcha: elegimos la solución que tiene sentido para tu operación y tu presupuesto.",
     ["Diagnóstico", "Diseño del proyecto", "Implementación", "Soporte postventa"]),
]
STEPS = [
    ("01", "Diagnóstico", "Visitamos tu operación, revisamos consumo de energía, calidad de agua y necesidades del equipo.", "nf/tecnico.jpg"),
    ("02", "Propuesta a medida", "Diseñamos la solución, con tiempos, costos y el retorno esperado de la inversión.", "nf/planos.jpg"),
    ("03", "Implementación", "Nuestro equipo técnico instala, prueba y deja todo funcionando sin frenar tu operación.", "nf/consultoria.jpg"),
    ("04", "Acompañamiento", "Mantenimiento, monitoreo y soporte local para que la solución rinda durante años.", "nf/solar2.jpg"),
]
IND = [("nf/manufactura.jpg", "Manufactura", "Energía y agua para procesos productivos"),
       ("nf/mineria.jpg", "Minería", "Tratamiento químico y agua para operación"),
       ("nf/agro.jpg", "Agroindustria", "Bombeo solar y agua para riego y procesos"),
       ("nf/agua.jpg", "Alimentos y bebidas", "Agua purificada para producción"),
       ("nf/oficinas.jpg", "Oficinas y comercio", "Paneles solares y puntos de agua"),
       ("nf/tecnico.jpg", "Construcción e inmobiliario", "Soluciones para proyectos nuevos")]
FAQ = [("¿En qué ciudades trabajan?", "Trabajamos en todo el Ecuador, con presencia en Quito, Guayaquil, Cuenca y Loja. Coordinamos la visita técnica según la ubicación de tu operación."),
       ("¿Cómo empieza un proyecto?", "Con una conversación y una visita técnica para entender tu consumo y tus necesidades. Con eso preparamos una propuesta a medida."),
       ("¿Ofrecen mantenimiento?", "Sí. Acompañamos cada proyecto con mantenimiento, monitoreo y soporte técnico local."),
       ("¿También atienden hogares?", "Sí. Nasfeco es el distribuidor exclusivo oficial de Waterdrop Filter en Ecuador: vendemos sus purificadores para el hogar con instalación y soporte de Nasfeco.")]

def group(active):
    return f'''
<div class="x-group"><div class="x-wrap">
  <div class="x-group-l"><a href="index.html">{nf_logo(sub=False)}</a>
    <a href="nasfeco.html"{' class="on"' if active == "nf" else ""}>Empresas</a><a href="waterdrop.html"{' class="on"' if active == "wd" else ""}>Waterdrop Hogar</a></div>
  <div class="x-group-r"><b style="color:var(--gold-d)">Distribuidor exclusivo oficial de Waterdrop Filter</b> · Ecuador y Miami, Florida (EE. UU.) · WhatsApp +593 99 731 2362</div>
</div></div>'''

def page_nf():
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Nasfeco", "url": "https://nasfeco.com/nasfeco",
          "email": "nasfeco@gmail.com", "telephone": "+593 99 731 2362",
          "address": {"@type": "PostalAddress", "addressLocality": "Quito", "addressCountry": "EC"},
          "description": "Soluciones de energía solar, purificación y tratamiento de agua para empresas e industrias en Ecuador. Distribuidor exclusivo oficial de Waterdrop Filter en Ecuador."}
    css = f'<link rel="stylesheet" href="css/x.css{V}"><link rel="stylesheet" href="css/nf.css{V}">'
    h = head("Nasfeco | Energía Solar y Soluciones de Agua para Empresas en Ecuador",
             "Nasfeco diseña e instala soluciones de energía solar, purificación y tratamiento de agua para empresas, industrias y minería en Ecuador. Presentes en Quito, Guayaquil, Cuenca y Loja, con proyectos en todo el Ecuador.",
             "https://nasfeco.com/nasfeco", "https://nasfeco.com/assets/nf/hero.jpg", ld, css)
    sol = "".join(f'''<div class="nf-sp{" on" if i == 0 else ""}"><img src="assets/{img}" alt="{t}" loading="lazy">
      <div class="nf-sp-c"><small>{n}</small><h3>{t}</h3><div class="nf-sp-more"><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in tags)}</ul>
      <a href="#contacto">Cotizar {t.lower()} {svg(I_RIGHT, 14, 2)}</a></div></div></div>''' for i, (img, n, t, d, tags) in enumerate(SOL))
    steps = "".join(f'<div class="nf-step{" on" if i == 0 else ""}" data-step="{i}"><b>{n}</b><div><h3>{t}</h3><p>{d}</p><img src="assets/{img}" alt="{t}" loading="lazy"></div></div>' for i, (n, t, d, img) in enumerate(STEPS))
    ind = "".join(f'<a href="#contacto" class="nf-ic x-rv"><img src="assets/{img}" alt="{t}" loading="lazy"><div><h3>{t}</h3><p>{d}</p></div></a>' for img, t, d in IND)
    faq = "".join(f'<details><summary>{q}<i></i></summary><p>{a}</p></details>' for q, a in FAQ)
    tick = "".join(f"<span>{t}</span>" for t in ["Energía solar", "Purificación de agua", "Tratamiento químico", "Consultoría técnica", "Minería", "Industria", "Agroindustria", "Comercio"] * 2)
    body = group("nf") + f'''
<header class="x-header"><div class="x-wrap">
  <a href="nasfeco.html">{nf_logo()}</a>
  <ul class="x-nav">
    <li><a href="#soluciones">Soluciones</a></li><li><a href="#calculadora">Calculadora solar</a></li><li><a href="#proceso">Cómo trabajamos</a></li><li><a href="#industrias">Industrias</a></li><li><a href="#nosotros">Nosotros</a></li>
    <li><a href="#contacto" class="cta">Cotizar proyecto</a></li>
  </ul>
  <div class="x-icons"><button class="x-icon x-burger" data-menu aria-label="Menú">{svg(I_MENU, 22)}</button></div>
</div></header>
<nav class="x-mnav" id="x-mnav" aria-label="Menú móvil">
  <div class="x-mnav-top">{nf_logo()}<button class="x-icon" data-menu-close aria-label="Cerrar">{svg(I_X, 22)}</button></div>
  <a href="#soluciones">Soluciones</a><a href="#calculadora">Calculadora solar</a><a href="#proceso">Cómo trabajamos</a><a href="#industrias">Industrias</a><a href="#nosotros">Nosotros</a>
  <a href="#contacto">Cotizar proyecto</a><a href="waterdrop.html">Waterdrop Hogar →</a><a href="index.html">← Inicio</a>
</nav>

<section class="nf-hero">
  <img src="assets/nf/hero.jpg" alt="Planta solar al atardecer">
  <div class="x-wrap">
    <p class="x-eyebrow">Nasfeco · Ecuador y Miami, Florida</p>
    <h1>Energía y agua <b>para la industria</b> que mueve al Ecuador</h1>
    <p class="lead">Diseñamos, instalamos y mantenemos soluciones de energía solar, purificación y tratamiento de agua para empresas, plantas y operaciones mineras.</p>
    <div class="x-btns"><a href="#calculadora" class="x-btn x-btn-g">Calcula tu ahorro solar</a><a href="#contacto" class="x-btn nf-btn-w">Cotizar proyecto</a></div>
    <div class="nf-hero-m"><div><b data-count="3" data-pre="+">+3</b><span>Años de experiencia</span></div><div><b data-count="500" data-suf="+">500+</b><span>Proyectos ejecutados</span></div><div><b data-count="99" data-suf="%">99%</b><span>Satisfacción operativa</span></div></div>
  </div>
</section>
<div class="nf-tick" aria-hidden="true"><div>{tick}</div></div>

<section class="x-sec" id="soluciones">
  <div class="x-wrap">
    <div class="x-head x-rv"><p class="x-eyebrow" style="text-align:center">Soluciones</p><h2 class="x-h2">Un solo aliado para tu energía y tu agua</h2><p class="x-lead">Toca cada solución para ver qué incluye.</p></div>
    <div class="nf-sol x-rv">{sol}</div>
  </div>
</section>

{DAY}
{CALC}
<section class="x-sec" id="proceso">
  <div class="x-wrap nf-proc">
    <div class="nf-proc-l"><p class="x-eyebrow">Cómo trabajamos</p><h2>Del diagnóstico a la operación, sin sorpresas</h2>
      <p>Un mismo equipo te acompaña en cada etapa del proyecto, con respaldo técnico aquí en Ecuador.</p><div class="nf-proc-bar"><i></i></div>
      <div class="x-btns" style="margin-top:28px"><a href="#contacto" class="x-btn x-btn-p">Agendar visita técnica</a></div></div>
    <div>{steps}</div>
  </div>
</section>

<section class="x-sec" id="industrias">
  <div class="x-wrap"><div class="x-head x-rv"><p class="x-eyebrow" style="text-align:center">Industrias</p><h2 class="x-h2">Soluciones para cada sector</h2></div><div class="nf-ind">{ind}</div></div>
</section>

<section class="nf-band" id="nosotros">
  <img src="assets/nf/solar2.jpg" alt="" data-par>
  <div class="x-wrap">
    <p class="x-eyebrow" style="color:var(--gold)">Nosotros</p>
    <h2 class="x-rv">Transformamos la forma en que Ecuador <b>consume energía y agua</b>.</h2>
    <p class="x-rv" style="margin-top:18px;max-width:640px;color:#C9D2E3;font-size:16px">No solo distribuimos equipos: diseñamos soluciones eficientes que optimizan recursos, reducen costos y cuidan el entorno, con tecnología certificada y un equipo técnico propio.</p>
    <div class="nf-nums"><div><b data-count="3" data-pre="+">+3</b><span>Años de experiencia</span></div><div><b data-count="500" data-suf="+">500+</b><span>Proyectos ejecutados</span></div><div><b data-count="99" data-suf="%">99%</b><span>Satisfacción operativa</span></div></div>
  </div>
</section>

<section class="x-sec">
  <div class="x-wrap"><div class="x-head x-rv"><p class="x-eyebrow" style="text-align:center">Por qué Nasfeco</p><h2 class="x-h2">Lo que nos diferencia</h2></div>
    <div class="nf-why">
      <div class="x-rv"><i>{svg(I_SHIELD)}</i><h3>Respaldo técnico local</h3><p>Equipo propio en Ecuador para instalación, mantenimiento y soporte inmediato.</p></div>
      <div class="x-rv"><i>{svg(I_GLOBE)}</i><h3>Distribuidor exclusivo oficial</h3><p>Representamos de forma exclusiva a Waterdrop Filter en Ecuador, con tecnología certificada a nivel internacional.</p></div>
      <div class="x-rv"><i>{svg(I_CHART)}</i><h3>Rentabilidad real</h3><p>Soluciones que reducen costos fijos y aportan a la sostenibilidad de tu empresa.</p></div>
    </div></div>
</section>

<section class="x-sec">
  <div class="x-wrap"><div class="nf-wd x-rv">
    <img src="assets/x/wd-page-1016-new-2-pc.jpg" alt="Purificadores Waterdrop" loading="lazy">
    <div class="nf-wd-c"><p class="x-eyebrow">Distribuidor exclusivo oficial</p><h2>Somos los distribuidores exclusivos de Waterdrop Filter en Ecuador</h2>
      <p>Purificadores Waterdrop originales para casas, departamentos y oficinas, con garantía, repuestos e instalación de Nasfeco.</p>
      <div class="x-btns"><a href="waterdrop.html" class="x-btn x-btn-p">Ver purificadores</a><a href="waterdrop.html#ahorro" class="x-btn x-btn-o">Calcular mi ahorro</a></div></div>
  </div></div>
</section>

<section class="x-sec pb" id="faq">
  <div class="x-wrap x-faq"><div class="x-faq-l x-rv"><h2>Preguntas frecuentes</h2><p>Lo que más nos preguntan las empresas antes de empezar un proyecto.</p></div><div class="x-rv">{faq}</div></div>
</section>

<section class="x-sec gray" id="contacto">
  <div class="x-wrap x-ct">
    <div class="x-rv"><p class="x-eyebrow">Contacto</p><h2>Potenciemos juntos tu proyecto</h2>
      <p>Cuéntanos qué necesitas y un especialista de Nasfeco te contactará para agendar el diagnóstico.</p>
      <div class="x-ct-line">{WA} +593 99 731 2362</div><div class="x-ct-line">{svg(I_MAIL, 22)} nasfeco@gmail.com</div><div class="x-ct-line">{svg(I_PIN, 22)} Quito, Guayaquil, Cuenca y Loja · Proyectos en todo el Ecuador</div><div class="x-ct-line">{svg(I_PIN, 22)} También en Miami, Florida (EE. UU.)</div>
      <div class="x-btns" style="margin-top:20px"><a class="x-btn x-btn-wa" href="https://wa.me/593997312362?text=Hola%20Nasfeco%2C%20quiero%20cotizar%20un%20proyecto%20para%20mi%20empresa" target="_blank" rel="noopener">{WA} Escribir por WhatsApp</a></div></div>
    <form class="x-form x-rv" id="nf">
      <div class="x-fg"><label for="n_name">Nombre</label><input id="n_name" required placeholder="Ej. Juan Pérez"></div>
      <div class="x-fg"><label for="n_company">Empresa</label><input id="n_company" required placeholder="Empresa S.A."></div>
      <div class="x-fg"><label for="n_email">Correo</label><input id="n_email" type="email" required placeholder="contacto@empresa.com"></div>
      <div class="x-fg"><label for="n_phone">Teléfono / WhatsApp</label><input id="n_phone" type="tel" required placeholder="Ej. 0999999999"></div>
      <div class="x-fg"><label for="n_service">Solución</label><select id="n_service"><option>Energía solar</option><option>Purificación de agua</option><option>Tratamiento químico</option><option>Consultoría técnica</option><option>Otro</option></select></div>
      <div class="x-fg"><label for="n_details">Cuéntanos del proyecto</label><textarea id="n_details" required placeholder="Ubicación, tipo de operación, consumo aproximado..."></textarea></div>
      <button type="submit" class="x-btn x-btn-p x-btn-block">Solicitar contacto</button>
    </form>
  </div>
</section>

<footer class="x-foot" style="margin-top:0"><div class="x-wrap">
  <div class="x-foot-g">
    <div>{nf_logo("#ffffff")}<p style="margin-top:14px">Energía solar, purificación y tratamiento de agua para empresas e industrias en Ecuador. Distribuidor exclusivo oficial de Waterdrop Filter en Ecuador.</p></div>
    <div><h4>Soluciones</h4><a href="#soluciones">Energía solar</a><a href="#soluciones">Purificación de agua</a><a href="#soluciones">Tratamiento químico</a><a href="#soluciones">Consultoría técnica</a></div>
    <div><h4>Nasfeco</h4><a href="#nosotros">Nosotros</a><a href="#proceso">Cómo trabajamos</a><a href="waterdrop.html">Waterdrop Hogar</a><a href="index.html">Inicio</a></div>
    <div><h4>Contacto</h4><p style="margin-bottom:8px">nasfeco@gmail.com</p><p style="margin-bottom:8px">Ecuador · Miami (EE. UU.)</p><p style="margin-bottom:8px">WhatsApp +593 99 731 2362</p><p>Quito, Ecuador</p></div>
  </div>
  <div class="x-foot-b"><span>&copy; 2026 Nasfeco · Ecuador. Todos los derechos reservados.</span><span>Creado por <strong>Mateo Perez</strong></span></div>
</div></footer>
<a href="https://wa.me/593997312362?text=Hola%20Nasfeco%2C%20quiero%20informaci%C3%B3n%20para%20mi%20empresa" target="_blank" rel="noopener" class="x-wa" aria-label="Escríbenos por WhatsApp">{WA}</a>
<script src="js/vendor/gsap.min.js"></script>
<script src="js/vendor/ScrollTrigger.min.js"></script>
<script src="js/x.js{V}"></script>
{WOWJS}
<script>
(function(){{
  const $$=(s,r=document)=>[...r.querySelectorAll(s)];
  // Soluciones: expandir al pasar el mouse o tocar
  $$('.nf-sp').forEach(p=>{{const on=()=>$$('.nf-sp').forEach(x=>x.classList.toggle('on',x===p));p.addEventListener('mouseenter',on);p.addEventListener('click',on);}});
  // Proceso: el paso visible se ilumina
  const steps=$$('.nf-step'),bar=document.querySelector('.nf-proc-bar i');
  const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{const i=+e.target.dataset.step;steps.forEach((s,k)=>s.classList.toggle('on',k===i));bar.style.width=((i+1)/steps.length*100)+'%';}}}}),{{rootMargin:'-45% 0px -45% 0px'}});
  steps.forEach(s=>io.observe(s));
  // Contadores
  const cio=new IntersectionObserver(es=>es.forEach(e=>{{if(!e.isIntersecting)return;const el=e.target,to=+el.dataset.count,pre=el.dataset.pre||'',suf=el.dataset.suf||'',t0=performance.now();
    (function st(n){{const k=Math.max(0,Math.min(1,(n-t0)/1400));el.textContent=pre+Math.round(to*(1-Math.pow(1-k,3)))+suf;if(k<1)requestAnimationFrame(st);}})(t0);cio.unobserve(el);}}),{{threshold:.6}});
  $$('[data-count]').forEach(el=>cio.observe(el));
  // Parallax de la banda
  if(window.gsap&&window.ScrollTrigger&&!matchMedia('(prefers-reduced-motion: reduce)').matches){{
    $$('[data-par]').forEach(img=>gsap.fromTo(img,{{yPercent:-8}},{{yPercent:8,ease:'none',scrollTrigger:{{trigger:img.parentElement,start:'top bottom',end:'bottom top',scrub:true}}}}));
  }}
  // Formulario
  document.getElementById('nf').addEventListener('submit',async e=>{{
    e.preventDefault();const b=e.target.querySelector('button'),txt=b.textContent,v=id=>document.getElementById(id).value;
    b.textContent='Enviando...';b.disabled=true;
    try{{const r=await fetch('https://guachotw1.app.n8n.cloud/webhook/727f04bc-196b-4e54-947b-70ed61e854dd',{{method:'POST',headers:{{'Content-Type':'application/x-www-form-urlencoded'}},
      body:new URLSearchParams({{source:'Nasfeco B2B',name:v('n_name'),company:v('n_company'),email:v('n_email'),phone:v('n_phone'),service:v('n_service'),details:v('n_details')}})}});
      if(r.ok||r.type==='opaque'){{b.textContent='¡Solicitud enviada! Te contactaremos pronto';e.target.reset();return;}}throw new Error();
    }}catch(err){{b.textContent='Error al enviar. Intenta de nuevo.';setTimeout(()=>{{b.textContent=txt;b.disabled=false;}},3000);}}
  }});
}})();
</script>
</body>
</html>
'''
    return h + body

# ===================================================================== PORTAL
def page_index():
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Nasfeco", "url": "https://nasfeco.com/", "telephone": "+593 99 731 2362",
          "address": {"@type": "PostalAddress", "addressLocality": "Quito", "addressCountry": "EC"}}
    css = '''<style>
:root{--navy:#0A192F;--navy-d:#07111F;--gold:#10B981;--f:'Montserrat',-apple-system,'Segoe UI',Roboto,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{font-family:var(--f);background:var(--navy-d);color:#fff;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.p-top{position:fixed;top:0;left:0;right:0;z-index:20;display:flex;justify-content:center;padding:calc(22px + env(safe-area-inset-top,0px)) 24px 0;pointer-events:none}
.p-top .nf-logo{pointer-events:auto;background:rgba(10,25,47,.55);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.14);border-radius:40px;padding:10px 20px 10px 14px}
.nf-logo{display:inline-flex;align-items:center;gap:10px;line-height:1}
.nf-logo b{display:block;font-size:17px;font-weight:700;letter-spacing:.04em}
.nf-logo small{display:block;font-size:7px;font-weight:600;letter-spacing:.34em;margin-top:3px;opacity:.85}
.portal{display:flex;height:100vh;min-height:620px}
.side{position:relative;flex:1;overflow:hidden;display:flex;align-items:flex-end;transition:flex .8s cubic-bezier(.77,0,.18,1)}
.side:hover{flex:1.35}
.side>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.side:hover>img{transform:scale(1.05)}
.side::before{content:'';position:absolute;inset:0;z-index:1}
.s-nf::before{background:linear-gradient(0deg,rgba(10,25,47,.96) 0%,rgba(10,25,47,.6) 50%,rgba(10,25,47,.35) 100%)}
.s-wd{color:var(--navy)}
.s-wd::before{background:linear-gradient(0deg,rgba(244,239,233,.97) 0%,rgba(244,239,233,.7) 45%,rgba(244,239,233,0) 75%)}
.side-c{position:relative;z-index:2;width:100%;max-width:560px;padding:0 56px 110px}
.tag{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin-bottom:16px}
.tag::before{content:'';width:24px;height:1px;background:currentColor}
.s-wd .tag{color:#059669}
.side h2{font-size:clamp(40px,5vw,68px);font-weight:300;line-height:1;letter-spacing:-.02em}
.side h2 b{font-weight:600}
.s-nf h2 b{color:var(--gold)}
.s-wd h2 b{color:#0089A8}
.side p{margin-top:16px;font-size:16px;line-height:1.5;max-width:420px;opacity:.85}
.side ul{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.side li{font-size:12px;font-weight:500;padding:6px 12px;border-radius:20px;border:1px solid rgba(255,255,255,.35)}
.s-wd li{border-color:rgba(10,25,47,.25)}
.cta{display:inline-flex;align-items:center;gap:10px;margin-top:30px;height:50px;padding:0 26px;border-radius:4px;font-weight:600;font-size:15px;transition:gap .3s,background .3s}
.s-nf .cta{background:var(--gold);color:var(--navy)}
.s-wd .cta{background:var(--navy);color:#fff}
.side:hover .cta{gap:16px}
.cta svg{width:16px;height:16px}
.p-bot{position:fixed;left:0;right:0;bottom:calc(26px + env(safe-area-inset-bottom,0px));z-index:20;text-align:center;font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:rgba(255,255,255,.7);pointer-events:none}
.p-bot span{background:rgba(10,25,47,.55);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);padding:8px 16px;border-radius:20px}
.divider{position:absolute;left:50%;top:0;bottom:0;width:1px;background:linear-gradient(transparent,rgba(16,185,129,.7),transparent);z-index:5;pointer-events:none}
.side-c>*{opacity:0;transform:translateY(24px);animation:pIn .9s cubic-bezier(.2,.7,.2,1) forwards}
.side-c>*:nth-child(2){animation-delay:.1s}.side-c>*:nth-child(3){animation-delay:.2s}.side-c>*:nth-child(4){animation-delay:.3s}.side-c>*:nth-child(5){animation-delay:.4s}
.s-wd .side-c>*{animation-delay:.25s}.s-wd .side-c>*:nth-child(2){animation-delay:.35s}.s-wd .side-c>*:nth-child(3){animation-delay:.45s}.s-wd .side-c>*:nth-child(4){animation-delay:.55s}.s-wd .side-c>*:nth-child(5){animation-delay:.65s}
@keyframes pIn{to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.side-c>*{animation:none;opacity:1;transform:none}}
@media (max-width:860px){
  .portal{flex-direction:column;height:auto}
  .side,.side:hover{flex:none;min-height:88vh}
  .side-c{padding:0 24px 56px}
  .divider{display:none}
  .p-bot{display:none}
  .p-top{position:absolute}
  .side:first-child .side-c{padding-top:110px}
}
</style>'''
    h = head("Nasfeco | Energía y Agua para Empresas y Hogares en Ecuador",
             "Nasfeco: soluciones de energía solar y agua para empresas y distribuidor exclusivo oficial de Waterdrop Filter en Ecuador. Quito, Ecuador.",
             "https://nasfeco.com/", "https://nasfeco.com/assets/nf/portal.jpg", ld, css)
    arrow = svg("M5 12h14M13 6l6 6-6 6", 16, 2)
    body = f'''
<div class="p-top"><a href="index.html" aria-label="Nasfeco">{nf_logo("#ffffff")}</a></div>
<main class="portal">
  <a class="side s-nf" href="nasfeco.html">
    <img src="assets/nf/portal.jpg" alt="Planta de energía solar">
    <div class="side-c">
      <span class="tag">Nasfeco Empresas</span>
      <h2>Energía y agua <b>para tu empresa</b></h2>
      <p>Energía solar, purificación y tratamiento de agua para industrias, minería y comercios.</p>
      <ul><li>Energía solar</li><li>Tratamiento de agua</li><li>Consultoría técnica</li></ul>
      <span class="cta">Soluciones para empresas {arrow}</span>
    </div>
  </a>
  <a class="side s-wd" href="waterdrop.html">
    <img src="assets/x/wd-page-1016-new-2-pc.jpg" alt="Purificadores Waterdrop">
    <div class="side-c">
      <span class="tag">Waterdrop Hogar</span>
      <h2>Agua pura <b>para tu casa</b></h2>
      <p>Distribuidor exclusivo oficial de Waterdrop Filter en Ecuador. Purificadores originales con instalación y soporte de Nasfeco.</p>
      <ul><li>Ósmosis inversa</li><li>Ultrafiltración</li><li>Dispensadores</li></ul>
      <span class="cta">Ver purificadores {arrow}</span>
    </div>
  </a>
  <div class="divider"></div>
</main>
<div class="p-bot"><span>Elige tu destino</span></div>
</body>
</html>
'''
    return h + body

for name, fn in [("nasfeco.html", page_nf), ("index.html", page_index)]:
    open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n").write(fn())
    print("ok", name)
