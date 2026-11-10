# -*- coding: utf-8 -*-
"""Piezas comunes a build_waterdrop.py y build_nasfeco.py: versión de CSS/JS, tipografía local y cookies.

Cookies: solo almacenamiento imprescindible. YouTube y Google Ads se cargan únicamente si la persona acepta
(lógica en js/consent.js; estilos en css/consent.css)."""

# Súbelo cada vez que cambies un .css o .js, para que el navegador no use la versión vieja.
VER = "?v=36"

COOKIES_URL = "politica-cookies.html"

# Montserrat servida desde la propia web (assets/fonts). Antes venía de Google Fonts.
HEAD = f'''<link rel="preload" href="assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/consent.css{VER}">'''

# Banner de cookies. Rechazar y Aceptar llevan exactamente el mismo botón. Va justo antes de los scripts de la página.
BAR = f'''<div class="ck" id="ck" role="dialog" aria-modal="false" aria-labelledby="ck-t" hidden>
  <p id="ck-t"><b>Cookies</b>Solo usamos el almacenamiento imprescindible para que la web funcione. Los videos de YouTube y la medición de anuncios de Google colocan sus propias cookies, así que solo se cargan si aceptas. Puedes cambiar tu elección cuando quieras desde el pie de página. <a href="{COOKIES_URL}">Política de cookies</a></p>
  <div class="ck-b"><button type="button" class="ck-btn" data-consent="no">Rechazar</button><button type="button" class="ck-btn" data-consent="yes">Aceptar</button></div>
</div>
<script src="js/consent.js{VER}"></script>'''

# Enlaces del pie de página
FOOT = f'<a href="{COOKIES_URL}">Política de cookies</a><button type="button" class="ck-set" data-cookie-settings>Configurar cookies</button>'

# Portada guardada en la web (assets/img/yt/ID.webp) + aviso. El video se carga desde youtube-nocookie.com solo con consentimiento.
GATE = '<div class="yt-gate"><p>Este video está en YouTube, que usa cookies.</p><button type="button" data-consent="yes">Aceptar y ver</button></div>'
def yt_img(vid):
    return f"assets/img/yt/{vid}.webp"
