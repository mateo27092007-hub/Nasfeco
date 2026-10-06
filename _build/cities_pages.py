# -*- coding: utf-8 -*-
"""Páginas locales por ciudad para SEO (reutiliza las funciones del generador)."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "build_waterdrop.py"), encoding="utf-8").read()
src = src[:src.rindex("for name, fn in [")]
g = {"__file__": os.path.join(HERE, "build_waterdrop.py")}
exec(compile(src, "build10", "exec"), g)
ROOT = g["ROOT"]

CITIES = {
    "quito": ("Quito", "Pichincha", "En Quito el agua llega potabilizada, pero en el recorrido por tuberías antiguas recoge sedimentos y sarro, y mantiene un sabor a cloro que se nota en el café y la comida.",
              ["Cumbayá", "Tumbaco", "Valle de los Chillos", "Norte", "Centro", "Sur", "Calderón", "Conocoto"]),
    "guayaquil": ("Guayaquil", "Guayas", "En Guayaquil el calor hace que se tome mucha más agua, y comprar botellones cada semana sale caro. Un purificador en casa da agua pura y fría ilimitada directo del grifo.",
                  ["Samborondón", "Vía a la Costa", "Urdesa", "Kennedy", "Ceibos", "Alborada", "Daule", "Durán"]),
    "cuenca": ("Cuenca", "Azuay", "En Cuenca muchas familias ya cuidan lo que toman. Un purificador quita el cloro, el sarro y los sedimentos de las tuberías, y conserva o devuelve los minerales al agua.",
               ["El Centro", "Totoracocha", "Monay", "El Batán", "Ricaurte", "Baños", "Challuabamba"]),
    "loja": ("Loja", "Loja", "En Loja el agua de la red puede traer sedimentos y sabor a cloro. Con un purificador Waterdrop tienes agua pura para tomar y cocinar sin depender de botellones.",
             ["El Centro", "La Tebaida", "San Sebastián", "Época", "El Valle", "Sauces Norte"]),
}

def page(slug, c):
    city, prov, intro, zones = c
    title = f"Purificadores de Agua en {city} | Waterdrop Ecuador · Nasfeco"
    desc = f"Purificadores de agua Waterdrop en {city} con instalación incluida: ósmosis inversa X12 y G5P700A, ultrafiltración y dispensador ED01. Nasfeco, distribuidor exclusivo oficial en Ecuador."
    url = f"https://nasfeco.com/purificadores-agua-{slug}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "LocalBusiness", "name": f"Nasfeco · Purificadores Waterdrop {city}", "url": url, "telephone": "+593 99 731 2362",
         "description": f"Distribuidor exclusivo oficial de Waterdrop Filter en Ecuador. Venta e instalación de purificadores de agua en {city}.",
         "areaServed": {"@type": "City", "name": city}, "address": {"@type": "PostalAddress", "addressLocality": city, "addressRegion": prov, "addressCountry": "EC"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f"¿Instalan purificadores de agua en {city}?", "acceptedAnswer": {"@type": "Answer", "text": f"Sí. Los técnicos de Nasfeco instalan en {city}. El precio de la X12, el G5P700A y la Ultrafiltración incluye IVA e instalación."}},
            {"@type": "Question", "name": f"¿Cuánto cuesta un purificador de agua en {city}?", "acceptedAnswer": {"@type": "Answer", "text": "Desde $99 el Dispensador ED01, $299 la Ultrafiltración UF, $1,399 el G5P700A y $1,999 la X12, con IVA incluido."}}]}]}
    h = g["head"](title, desc, url, "https://nasfeco.com/assets/x/wd-page-1016-new-2-pc.jpg", ld)
    body = g["top"]()
    body += g["banner"](f"Purificadores de agua<br>en {city}", f"{intro} Nasfeco, distribuidor exclusivo oficial de Waterdrop Filter en Ecuador, instala en {city}.",
                        [("Instalación", f"En {city}"), ("Precio final", "IVA incluido"), ("Garantía", "Soporte local")],
                        bg=(g["A"]("wd-page-1016-new-2-pc.jpg"), g["A"]("wd-page-1016-new-2-mo.jpg")),
                        btns=f'<div class="x-btns"><a href="#ofertas" class="x-btn x-btn-p">Ver precios</a><a href="https://wa.me/593997312362?text=Hola%20Nasfeco%2C%20estoy%20en%20{city}%20y%20quiero%20informaci%C3%B3n%20sobre%20los%20purificadores" target="_blank" rel="noopener" class="x-btn x-btn-o">Cotizar por WhatsApp</a></div>')
    body += g["picks"](["x12", "g5", "uf", "smart"], title=f"Purificadores con instalación en {city}",
                       sub=f"Precios finales en dólares: incluyen IVA e instalación en {city}. El Dispensador ED01 no necesita instalación.")
    z = "".join(f"<li>{x}</li>" for x in zones)
    body += f'''
<section class="x-sec"><div class="x-wrap x-mt" style="align-items:start">
  <div class="x-rv"><p class="x-eyebrow">Cobertura</p><h2>Instalamos en {city} y alrededores</h2>
    <p>Coordinamos la instalación por WhatsApp en el día y horario que te convenga. Llevamos todo lo necesario y te enseñamos a usar el equipo.</p>
    <ul class="checks" style="margin-top:18px;display:grid;grid-template-columns:1fr 1fr;gap:8px 16px">{z}</ul></div>
  <div class="x-rv"><p class="x-eyebrow">Cómo comprar</p><h2>En 3 pasos</h2>
    <ul class="checks" style="margin-top:18px;display:grid;gap:12px"><li>Elige tu purificador o pide asesoría gratis por WhatsApp.</li><li>Agendamos la instalación en {city}.</li><li>Disfrutas agua pura desde el primer día, con garantía y soporte de Nasfeco.</li></ul>
    <div class="x-btns" style="margin-top:22px"><a class="x-btn x-btn-wa" href="https://wa.me/593997312362?text=Hola%20Nasfeco%2C%20quiero%20agendar%20una%20instalaci%C3%B3n%20en%20{city}" target="_blank" rel="noopener">Agendar en {city}</a></div></div>
</div></section>'''
    body += g["calc"]("x12", ("g5", "x12", "uf"))
    body += g["servicio"](video=False)
    body += g["cmp_cats"](None)
    body += g["faq"]([
        (f"¿Instalan purificadores de agua en {city}?", f"Sí. Los técnicos de Nasfeco instalan en {city}. El precio de la X12, el G5P700A y la Ultrafiltración UF es precio final: incluye IVA e instalación."),
        (f"¿Cuánto cuesta un purificador de agua en {city}?", "Dispensador ED01 $99 (envío no incluido), Ultrafiltración UF $299, G5P700A $1,399 y X12 $1,999. Precios finales con IVA."),
        ("¿Son equipos originales?", "Sí. Nasfeco es el distribuidor exclusivo oficial de Waterdrop Filter en Ecuador: equipos originales con garantía y repuestos."),
        (f"¿El agua de {city} necesita purificador?", "El agua de la red llega potabilizada, pero en las tuberías recoge sedimentos y sarro y conserva el cloro. Un purificador elimina todo eso y mejora el sabor."),
        ("¿Cómo pago?", "Arma tu pedido y envíalo por WhatsApp; un asesor confirma disponibilidad, fecha de instalación y formas de pago.")])
    return h + body + g["bottom"]()

for slug, c in CITIES.items():
    open(os.path.join(ROOT, f"purificadores-agua-{slug}.html"), "w", encoding="utf-8", newline="\n").write(page(slug, c))
    print("ok", slug)
