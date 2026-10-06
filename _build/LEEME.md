# Generadores del sitio

Las páginas HTML se generan con estos programas de Python (necesitan Pillow solo los de imágenes).
Ejecutar desde la carpeta del proyecto:

```
python _build/build_waterdrop.py   # waterdrop, product-*, repuestos
python _build/cities_pages.py      # purificadores-agua-quito/guayaquil/cuenca/loja
python _build/build_nasfeco.py     # nasfeco.html e index.html
```

Variable `ROOT` al inicio de cada archivo = carpeta del proyecto (cámbiala si mueves el proyecto).
Precios, códigos y fecha de la oferta: al inicio de `js/x.js` (objeto `WD`).
Esta carpeta no se publica (está en `.assetsignore`).
