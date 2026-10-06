# -*- coding: utf-8 -*-
"""Edita las escenas de cocina y dormitorio con los equipos que vende Nasfeco."""
from PIL import Image, ImageFilter, ImageDraw
A = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))), "assets") + "/"
SP = os.path.dirname(os.path.abspath(__file__)) + "/"

def soft_mask(w, h, f=10):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rectangle([f, f, w - f, h - f], fill=255)
    return m.filter(ImageFilter.GaussianBlur(f / 2))

def clone(img, box, dx):
    """Tapa box copiando el bloque desplazado dx en horizontal (bordes difuminados)."""
    x0, y0, x1, y1 = box
    src = img.crop((x0 + dx, y0, x1 + dx, y1))
    img.paste(src, (x0, y0), soft_mask(x1 - x0, y1 - y0, 8))

def fill_rows(img, box, lx, rx):
    """Rellena box interpolando por fila entre columnas limpias a la izquierda y derecha."""
    x0, y0, x1, y1 = box
    Lc = img.crop((lx[0], y0, lx[1], y1)).resize((1, y1 - y0), Image.BOX)
    Rc = img.crop((rx[0], y0, rx[1], y1)).resize((1, y1 - y0), Image.BOX)
    two = Image.new("RGB", (2, y1 - y0)); two.paste(Lc, (0, 0)); two.paste(Rc, (1, 0))
    # estirar 2 columnas al ancho: interpolación lineal por fila
    big = two.resize((4, y1 - y0), Image.NEAREST).resize((x1 - x0 + 2 * (x1 - x0) // 2, y1 - y0), Image.BILINEAR)
    off = (big.width - (x1 - x0)) // 2
    patch = big.crop((off, 0, off + x1 - x0, y1 - y0))
    img.paste(patch, (x0, y0), soft_mask(x1 - x0, y1 - y0, 6))

def cutout(path, height):
    im = Image.open(path).convert("RGBA"); im = im.crop(im.split()[3].getbbox())
    w = round(im.width * height / im.height)
    return im.resize((w, height), Image.LANCZOS)

def tone(item, k=0.86):
    from PIL import ImageEnhance
    a = item.split()[3]; rgb = ImageEnhance.Brightness(item.convert("RGB")).enhance(k)
    warm = Image.new("RGB", item.size, (120, 100, 80)); rgb = Image.blend(rgb, warm, 0.05)
    out = rgb.convert("RGBA"); out.putalpha(a); return out

def place(img, item, cx, bottom, shadow=0.35):
    x = round(cx - item.width / 2); y = bottom - item.height
    sh = Image.new("L", img.size, 0)
    ImageDraw.Draw(sh).ellipse([x - 10, bottom - 14, x + item.width + 10, bottom + 10], fill=int(255 * shadow))
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    dark = Image.new("RGB", img.size, (60, 50, 40))
    img.paste(dark, (0, 0), sh)
    img.paste(item, (x, y), item)
    return (x, y, x + item.width, bottom)

# ------------------------------------------------------------- COCINA
k = Image.open(A + "home/ui-wd-vis-shop-by-kitchen-PC.jpg").convert("RGB")
clone(k, (880, 280, 1065, 580), 190)          # filtro de mesa de acero
clone(k, (1598, 355, 1682, 566), -95)          # grifo negro (X16)
fill_rows(k, (1262, 662, 1752, 1100), (1216, 1252), (1756, 1786))   # K6 y X16 bajo el fregadero
floor = 1088
uf = place(k, tone(cutout(A + "uf/WD-RF10-UF-NSF.png", 215)), 1292, floor, 0.3)
x12 = place(k, tone(cutout(A + "x12/wd-product-1016-page-in-the-box-img1.webp", 255)), 1445, floor)
g5 = place(k, tone(cutout(A + "g5/ui-wd-g5p700a-system.png", 255)), 1652, floor)
X0, X1 = 90, 1905                               # recorte: sin el dispensador de la derecha
k = k.crop((X0, 0, X1, k.height))
k.save(A + "home/escena-cocina.jpg", quality=86, optimize=True, progressive=True)
W, H = k.size
pct = lambda b: (round(((b[0] + b[2]) / 2 - X0) / W * 100, 1), round((b[1] + (b[3] - b[1]) * 0.45) / H * 100, 1))
print("cocina", W, H, "uf", pct(uf), "x12", pct(x12), "g5", pct(g5), "ed01", pct((480, 370, 625, 560)))

# ------------------------------------------------------------- DORMITORIO
b = Image.open(A + "home/ui-wd-vis-shop-by-Bedroom-PC.jpg").convert("RGB")
BX0, BX1 = 0, 1255
b = b.crop((BX0, 0, BX1, b.height))
b.save(A + "home/escena-dormitorio.jpg", quality=86, optimize=True, progressive=True)
print("dormitorio", b.size, "ed01", (round((1010 - BX0) / b.width * 100, 1), round(560 / b.height * 100, 1)))

prev = Image.new("RGB", (W // 2 + b.width // 2 + 10, H // 2), "#888")
prev.paste(k.resize((W // 2, H // 2)), (0, 0)); prev.paste(b.resize((b.width // 2, H // 2)), (W // 2 + 10, 0))
prev.save(SP + "scene_prev.png")
k.crop((1150 - X0, 560, 1860 - X0, 1130)).save(SP + "scene_zoom.png")
