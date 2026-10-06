# -*- coding: utf-8 -*-
"""Imágenes para Google Business Profile de Nasfeco."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))), "assets") + "/"
OUT = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))), "marketing", "google-business") + "/"
os.makedirs(OUT, exist_ok=True)
F = "C:/Windows/Fonts/"
def font(name, size): return ImageFont.truetype(F + name, size)
NAVY, NAVY2, GREEN, GREEN_D, CYAN, WHITE = (10, 25, 47), (17, 34, 64), (16, 185, 129), (5, 150, 105), (0, 180, 216), (255, 255, 255)

def mark(size):
    """Logo NASFECO (triángulo con 3 puntos) en alta resolución."""
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    s = S / 30.0
    pts = [(5 * s, 5 * s), (25 * s, 15 * s), (5 * s, 25 * s)]
    # trazo con degradado aproximado: verde -> cian
    for i, (a, b, col) in enumerate([(pts[0], pts[1], GREEN), (pts[1], pts[2], (8, 182, 172)), (pts[2], pts[0], CYAN)]):
        d.line([a, b], fill=col, width=int(4.5 * s))
    for (x, y), col in zip(pts, [GREEN, GREEN_D, CYAN]):
        r = 5 * s; d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    return im.resize((size, size), Image.LANCZOS)

def logo_full(width, color=WHITE):
    m = mark(int(width * 0.2))
    f = font("timesbd.ttf", int(width * 0.11))
    txt = "NASFECO S.A"
    tw = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), txt, font=f)
    h = max(m.height, tw[3]) + 10
    im = Image.new("RGBA", (m.width + 20 + tw[2], h), (0, 0, 0, 0))
    im.paste(m, (0, (h - m.height) // 2), m)
    ImageDraw.Draw(im).text((m.width + 20, (h - tw[3]) // 2 - tw[1] // 2), txt, font=f, fill=color)
    return im

def cover_crop(img, w, h):
    r = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def shade(img, alpha=170, side="left"):
    g = Image.new("L", (img.width, 1))
    for x in range(img.width):
        t = x / img.width if side == "left" else 1 - x / img.width
        g.putpixel((x, 0), int(min(250, 95 + 160 * max(0, 1 - t * 1.25))))
    g = g.resize(img.size)
    dark = Image.new("RGB", img.size, NAVY)
    out = img.copy(); out.paste(dark, (0, 0), g); return out

def text(d, xy, s, f, fill=WHITE, maxw=None):
    if not maxw: d.text(xy, s, font=f, fill=fill); return xy[1] + f.size * 1.25
    words, line, y = s.split(), "", xy[1]
    for w in words:
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) > maxw and line:
            d.text((xy[0], y), line, font=f, fill=fill); y += f.size * 1.25; line = w
        else: line = t
    d.text((xy[0], y), line, font=f, fill=fill); return y + f.size * 1.25

def pill(d, x, y, s, f, bg=GREEN, fg=WHITE):
    w = d.textlength(s, font=f) + f.size * 1.4; h = f.size * 1.9
    d.rounded_rectangle([x, y, x + w, y + h], radius=h / 2, fill=bg)
    d.text((x + f.size * 0.7, y + h / 2), s, font=f, fill=fg, anchor="lm"); return x + w

def product(path, height):
    im = Image.open(path).convert("RGBA"); im = im.crop(im.split()[3].getbbox())
    return im.resize((round(im.width * height / im.height), height), Image.LANCZOS)

def save(img, name):
    img.convert("RGB").save(OUT + name, "JPEG", quality=90, optimize=True, progressive=True); print("ok", name)

# 1) LOGO cuadrado 720x720 ----------------------------------------------
lg = Image.new("RGB", (720, 720), NAVY); d = ImageDraw.Draw(lg)
m = mark(330); lg.paste(m, ((720 - 330) // 2, 120), m)
f = font("timesbd.ttf", 92); d.text((360, 535), "NASFECO", font=f, fill=WHITE, anchor="mm")
d.text((360, 615), "S.A.", font=font("timesbd.ttf", 48), fill=GREEN, anchor="mm")
save(lg, "01-logo-720x720.jpg")

# 2) PORTADA 1080x608 (16:9) --------------------------------------------
bg = cover_crop(Image.open(A + "x/wd-page-1016-new-2-pc.jpg").convert("RGB"), 1080, 608)
cv = shade(bg, 235); d = ImageDraw.Draw(cv)
L = logo_full(300); cv.paste(L, (60, 60), L)
y = text(d, (60, 190), "Agua pura para tu hogar", font("segoeuib.ttf", 56), maxw=560)
y = text(d, (60, y + 6), "Distribuidor exclusivo oficial de Waterdrop Filter en Ecuador", font("segoeui.ttf", 26), fill=(205, 220, 235), maxw=520)
x = pill(d, 60, y + 24, "Instalación incluida", font("seguisb.ttf", 22))
pill(d, x + 12, y + 24, "Quito · Guayaquil · Cuenca · Loja", font("seguisb.ttf", 22), bg=NAVY2)
save(cv, "02-portada-1080x608.jpg")

# 3) PRODUCTOS 1080x1080 -----------------------------------------------
PRODS = [("03-producto-x12.jpg", A + "x12/wd-product-1016-page-in-the-box-img1.webp", "Waterdrop X12", "Ósmosis inversa · 1200 GPD · 11 etapas", "$1,999", "$2,200", "Incluye IVA e instalación"),
         ("04-producto-g5p700a.jpg", A + "g5/ui-wd-g5p700a-system.png", "Waterdrop G5P700A", "Ósmosis inversa alcalina · 700 GPD", "$1,399", "$1,699", "Incluye IVA e instalación"),
         ("05-producto-ultrafiltracion.jpg", A + "uf/10UB-UF-NSF.png", "Ultrafiltración UF", "Sin electricidad · 0% desperdicio", "$299", "$380", "Incluye IVA e instalación"),
         ("06-producto-dispensador-ed01.jpg", A + "ed01/1_33c5e044-eb97-4485-ae99-684bc658886e.webp", "Dispensador ED01", "Portátil · sin instalación", "$99", "$129", "Precio con IVA · envío no incluido")]
for name, path, title, sub, price, was, note in PRODS:
    im = Image.new("RGB", (1080, 1080), (246, 249, 248)); d = ImageDraw.Draw(im)
    d.ellipse([140, 120, 940, 760], fill=(231, 248, 241))
    p = product(path, 560); im.paste(p, ((1080 - p.width) // 2, 130), p)
    d.rectangle([0, 760, 1080, 1080], fill=NAVY)
    d.text((70, 800), title, font=font("segoeuib.ttf", 58), fill=WHITE)
    d.text((70, 880), sub, font=font("segoeui.ttf", 30), fill=(190, 205, 222))
    d.text((70, 925), price, font=font("segoeuib.ttf", 72), fill=GREEN)
    pw = d.textlength(price, font=font("segoeuib.ttf", 72))
    wf = font("segoeui.ttf", 34); d.text((90 + pw, 958), was, font=wf, fill=(140, 155, 175))
    ww = d.textlength(was, font=wf); d.line([90 + pw, 978, 90 + pw + ww, 978], fill=(140, 155, 175), width=3)
    d.text((70, 1050), note, font=font("seguisb.ttf", 24), fill=(170, 235, 210), anchor="ls")
    L = logo_full(220); im.paste(L, (1080 - L.width - 40, 40), L) if False else None
    m = mark(70); im.paste(m, (980, 40), m)
    save(im, name)

# 4) PUBLICACIONES 1200x900 (4:3) ---------------------------------------
def post(name, photo, kicker, title, sub, chip):
    bg = cover_crop(Image.open(photo).convert("RGB"), 1200, 900); im = shade(bg, 230); d = ImageDraw.Draw(im)
    L = logo_full(280); im.paste(L, (64, 60), L)
    d.text((64, 240), kicker.upper(), font=font("seguisb.ttf", 26), fill=GREEN)
    y = text(d, (64, 285), title, font("segoeuib.ttf", 66), maxw=640)
    y = text(d, (64, y + 10), sub, font("segoeui.ttf", 30), fill=(210, 222, 236), maxw=600)
    pill(d, 64, y + 30, chip, font("seguisb.ttf", 26))
    d.text((64, 840), "nasfeco.com  ·  WhatsApp +593 99 731 2362", font=font("segoeui.ttf", 24), fill=(200, 215, 230))
    save(im, name)

post("07-post-oferta-octubre.jpg", A + "x/wd-page-1016-new-2-pc.jpg", "Oferta de Octubre", "Hasta $300 de descuento en purificadores",
     "Precio final con IVA e instalación incluida en Quito, Guayaquil, Cuenca y Loja.", "Válido hasta el 31 de octubre")
post("08-post-distribuidor-oficial.jpg", A + "home/escena-cocina.jpg", "Distribuidor exclusivo oficial", "Waterdrop Filter en Ecuador",
     "Equipos originales, garantía, repuestos e instalación con técnicos de Nasfeco.", "Asesoría gratis por WhatsApp")
post("09-post-adios-botellones.jpg", A + "x/wd-x_seri-5.jpg", "Agua pura en casa", "Dile adiós a los botellones",
     "Agua purificada ilimitada directo del grifo. Calcula tu ahorro en nasfeco.com", "Desde $99")
post("10-post-empresas-solar.jpg", A + "nf/hero.jpg", "Nasfeco Empresas", "Energía solar y agua para tu empresa",
     "Diseñamos, instalamos y mantenemos soluciones para industrias, minería y comercios.", "Calcula tu ahorro solar")

# 5) FOTOS DE PRODUCTO / AMBIENTE en 1080x1080 (sin texto) ---------------
for i, (src) in enumerate([A + "home/escena-cocina.jpg", A + "home/escena-dormitorio.jpg", A + "g5/wd-g5p700a-product_6.jpg", A + "uf/UB-UF_6.jpg",
                           A + "x12/X12_3.jpg", A + "nf/solar.jpg"], start=11):
    im = cover_crop(Image.open(src).convert("RGB"), 1080, 1080); save(im, f"{i:02d}-foto-{os.path.basename(src).split('.')[0][:20]}.jpg")
