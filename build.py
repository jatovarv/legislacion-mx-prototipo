#!/usr/bin/env python3
"""Genera el sitio a partir de cpeum.json (sin dependencias, compatible con GitHub Pages).

    python3 build.py                                   # todo, con la URL base por defecto
    python3 build.py --site-url https://midominio.mx   # URL base para canonical, sitemap y robots

Además de la CPEUM, genera las páginas del Código Civil para el Distrito Federal (ccdf.json) mediante build_ccdf.py:
ccdf/index.html (índice) y ccdf/articulos/N.html; sólo los artículos con texto cotejado entran al sitemap.

Salida:
  index.html        navegador interactivo (SPA): se le inyecta cpeum.json entre los marcadores
                    <!-- DATA:START --> y <!-- DATA:END -->, para que funcione en local (file://)
                    y publicado.
  articulos/N.html  una página estática por cada artículo con "estado": "verificado" (hoy, el 1o.):
                    texto vigente íntegro, fechas, enlace al DOF y versiones anteriores, legible sin
                    JavaScript e indexable. Los artículos de prototipo (texto simulado) nunca se
                    publican como página estática.
  sitemap.xml       portada + páginas estáticas.
  robots.txt        permite todo y apunta al sitemap.
"""
import argparse
import datetime as dt
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "cpeum.json"
INDEX = ROOT / "index.html"
ARTICULOS_DIR = ROOT / "articulos"

# URL pública por defecto (GitHub Pages del repositorio). Cámbiala con --site-url o SITE_URL.
SITE_URL_DEFAULT = "https://jatovarv.github.io/legislacion-mx-prototipo"

START = "<!-- DATA:START -->"
END = "<!-- DATA:END -->"

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
ROMANOS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


# ----------------------------------------------------------------------------- utilidades
def esc(s):
    return html.escape(str(s), quote=True)


def fmt_fecha(iso, corto=False):
    if not iso:
        return ""
    y, m, d = (int(x) for x in iso.split("-"))
    if corto:
        return f"{d} {MESES[m - 1][:3]} {y}"
    return f"{d} de {MESES[m - 1]} de {y}"


def numero_art(n):
    n = int(n)
    return f"{n}o." if n <= 9 else str(n)


def rango_vigencia(v):
    if not v.get("vigencia_desde"):
        return "Fecha de publicación pendiente de cotejo" + (f" (pista: DOF {fmt_fecha(v['fecha_sugerida'])})" if v.get("fecha_sugerida") else "")
    if v.get("vigencia_nunca_rigio"):
        return f"Publicado el {fmt_fecha(v['publicacion'])}, corregido antes de entrar en vigor"
    if v.get("vigencia_hasta_indeterminada"):
        return f"Desde el {fmt_fecha(v['vigencia_desde'])} hasta fecha por determinar"
    if not v.get("vigencia_hasta"):
        return f"Vigente desde el {fmt_fecha(v['vigencia_desde'])}"
    return f"Del {fmt_fecha(v['vigencia_desde'])} al {fmt_fecha(v['vigencia_hasta'])}"


def vigencia_marca(v):
    if v.get("vigencia_verificada") is not False:
        return ""
    return (f' <span class="por-cotejar" title="{esc(v.get("vigencia_nota") or "Entrada en vigor pendiente de cotejo con el decreto")}">'
            f"vigencia por cotejar</span>")


def extraccion_marca(v):
    """Cuerpo pendiente de cotejo con el PDF de la SCJN (bloque fusionado, limpieza de corte de página)."""
    if not v.get("extraccion_pendiente"):
        return ""
    return (f' <span class="por-cotejar" title="{esc(v.get("nota_extraccion") or "Texto pendiente de cotejo con el PDF de la SCJN")}">'
            f"extracción por cotejar</span>")


def valor_romano(s):
    total = 0
    for i, ch in enumerate(s):
        v = ROMANOS[ch]
        w = ROMANOS.get(s[i + 1]) if i + 1 < len(s) else 0
        total += -v if v < (w or 0) else v
    return total


def clasificar_parrafos(parrafos):
    """Misma lógica que index.html: apartados (A.), fracciones (I.) e incisos (a)) en secuencia."""
    sig_frac, sig_ap = 1, "A"
    clases = []
    for p in parrafos:
        rom = re.match(r"^([IVXLCDM]+)\.\s", p)
        ap = re.match(r"^([A-Z])\.\s", p)
        if rom and valor_romano(rom.group(1)) == sig_frac:
            sig_frac += 1
            clases.append("fraccion")
        elif ap and ap.group(1) == sig_ap:
            sig_ap = chr(ord(sig_ap) + 1)
            sig_frac = 1
            clases.append("apartado")
        elif rom:
            sig_frac = valor_romano(rom.group(1)) + 1
            clases.append("fraccion")
        elif ap:
            sig_ap = chr(ord(ap.group(1)) + 1)
            sig_frac = 1
            clases.append("apartado")
        elif re.match(r"^[a-z]\)\s", p):
            clases.append("inciso")
        elif re.match(r"^(Art(ículo|\.)\s+\d+)", p) and len(p) < 40:
            clases.append("encabezado")
        else:
            clases.append("")
    return clases


def texto_html(texto):
    parrafos = re.split(r"\n\s*\n", texto)
    clases = clasificar_parrafos(parrafos)
    out = []
    for p, c in zip(parrafos, clases):
        attr = f' class="{c}"' if c else ""
        out.append(f"<p{attr}>{esc(p).replace(chr(10), '<br>')}</p>")
    return "\n".join(out)


def dof_link_html(v):
    url = v.get("dof_url")
    if not isinstance(url, str) or not re.match(r"^https?://", url, re.I):
        return ""
    texto = v.get("dof_etiqueta") or "Ver decreto en el DOF"
    return (f'<a class="dof-link" href="{esc(url)}" target="_blank" rel="noopener noreferrer" '
            f'title="Abre la publicación oficial en una pestaña nueva">{esc(texto)} ↗</a>')


def fuente_link_html(v):
    url = v.get("fuente_url")
    if not isinstance(url, str) or not re.match(r"^https?://", url, re.I):
        return ""
    return (f'<a class="dof-link" href="{esc(url)}" target="_blank" rel="noopener noreferrer" '
            f'title="Abre el texto consolidado oficial en una pestaña nueva">{esc(v.get("fuente_etiqueta") or "Ver fuente oficial")} ↗</a>')


def ruta_estructura(estructura, num):
    """Devuelve la lista de nodos (Título > Capítulo > Sección) que contienen el artículo."""
    def visitar(nodo, camino):
        camino = camino + [nodo]
        rango = nodo.get("articulos")
        if rango and rango["desde"] <= num <= rango["hasta"]:
            return camino
        for hijo in nodo.get("hijos", []):
            r = visitar(hijo, camino)
            if r:
                return r
        return None
    for t in estructura:
        r = visitar(t, [])
        if r:
            return r
    return []


# ----------------------------------------------------------------------------- página estática
CSS = """
  :root { --brand:#0f2a4d; --accent:#1a5fb4; --bg:#f3f4f6; --surface:#fff; --text:#1f2937; --muted:#6b7280;
          --border:#e2e6ea; --ok:#1f7a4d; --ok-bg:#e6f4ec; --gold:#b8862b;
          --sans: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
          --serif: Georgia,"Charter","Iowan Old Style","Times New Roman",serif; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--text); font-family:var(--sans); line-height:1.5; -webkit-font-smoothing:antialiased; }
  a { color:var(--accent); }
  .topbar { background:var(--brand); color:#fff; padding:.8rem 1rem; display:flex; align-items:center; gap:.75rem; flex-wrap:wrap; }
  .topbar .brand { color:#fff; text-decoration:none; font-weight:700; font-size:1.05rem; display:inline-flex; align-items:baseline; gap:.5rem; }
  .topbar .pill { font-size:.62rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; background:var(--gold); color:#1f1300; padding:.15rem .45rem; border-radius:999px; }
  .topbar nav { margin-left:auto; font-size:.85rem; }
  .topbar nav a { color:#fff; opacity:.9; text-decoration:none; border-bottom:1px solid rgba(255,255,255,.4); }
  main { max-width: 820px; margin: 0 auto; padding: 1.25rem 1rem 3rem; }
  .breadcrumb { font-size:.8rem; color:var(--muted); display:flex; flex-wrap:wrap; gap:.35rem; margin-bottom:.9rem; }
  .breadcrumb a { color:var(--muted); text-decoration:none; }
  .breadcrumb a:hover { color:var(--accent); text-decoration:underline; }
  .breadcrumb b { color:var(--text); font-weight:600; }
  article { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:1.6rem 1.8rem 1.5rem; box-shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.08); }
  h1 { font-family:var(--serif); color:var(--brand); font-size:1.75rem; line-height:1.25; margin:0; }
  h1 .num { white-space:nowrap; }
  .badges { margin:.6rem 0 0; display:flex; flex-wrap:wrap; gap:.4rem; }
  .badge { font-size:.7rem; font-weight:700; letter-spacing:.04em; text-transform:uppercase; padding:.2rem .5rem; border-radius:999px; border:1px solid transparent; }
  .badge.vigente { background:var(--ok-bg); color:var(--ok); border-color:#b7e0c8; }
  .badge.verificado { background:#eef2f7; color:#334155; border-color:#d6dde6; }
  .badge.historial { background:#eaf2fc; color:#1e4e8c; border-color:#bfd3ee; }
  .aviso-historial { margin:.9rem 0 0; padding:.6rem .9rem; border-radius:8px; background:#eaf2fc; border:1px solid #bfd3ee; color:#163a6a; font-size:.85rem; }
  .tema { margin:.6rem 0 0; color:var(--muted); font-size:.92rem; }
  .meta { margin:.9rem 0 0; padding:.75rem .9rem; background:#f8fafc; border:1px solid var(--border); border-radius:8px; font-size:.85rem; color:var(--muted); display:grid; grid-template-columns:max-content 1fr; gap:.3rem .8rem; }
  .meta dt { font-weight:500; }
  .meta dd { margin:0; color:var(--text); font-weight:600; }
  .dof-link { font-weight:600; text-decoration:none; border-bottom:1px solid transparent; }
  .por-cotejar { font-size:.68rem; font-weight:700; letter-spacing:.03em; text-transform:uppercase; color:#92400e; background:#fff6e5; border:1px solid #f2c879; border-radius:999px; padding:.05rem .4rem; cursor:help; white-space:nowrap; }
  .dof-link:hover { border-bottom-color:var(--accent); }
  .texto { font-family:var(--serif); font-size:1.08rem; line-height:1.75; margin-top:1.2rem; color:#111827; }
  .texto p { margin:0 0 1em; }
  .texto p:last-child { margin-bottom:0; }
  .texto p.apartado { font-weight:700; margin-top:1.2em; }
  .texto p.fraccion { padding-left:2.2em; text-indent:-2.2em; }
  .texto p.inciso { padding-left:3.6em; text-indent:-1.4em; }
  .texto p.encabezado { font-weight:700; }
  .acciones { margin-top:1.4rem; padding-top:1rem; border-top:1px solid var(--border); display:flex; flex-wrap:wrap; gap:.6rem; }
  .btn { display:inline-flex; align-items:center; gap:.4rem; background:var(--brand); color:#fff; text-decoration:none; padding:.55rem 1rem; border-radius:8px; font-weight:600; font-size:.9rem; }
  .btn.secondary { background:#fff; color:var(--brand); border:1px solid #cfd5dc; font-weight:500; }
  h2 { font-size:1.15rem; color:var(--brand); margin:2rem 0 .6rem; }
  details.version { border:1px solid var(--border); border-radius:8px; background:#fbfcfd; margin:.6rem 0; }
  details.version summary { cursor:pointer; padding:.7rem .9rem; font-weight:600; color:var(--brand); list-style:none; display:block; line-height:1.4; }
  details.version summary::-webkit-details-marker { display:none; }
  details.version summary::before { content:"▸"; color:var(--muted); font-size:.9em; margin-right:.45rem; }
  details.version[open] summary::before { content:"▾"; }
  details.version summary small { font-weight:400; color:var(--muted); white-space:nowrap; margin-left:.35rem; }
  details.version .cuerpo { padding:0 .9rem 1rem; border-top:1px dashed var(--border); }
  details.version .meta { margin-top:.8rem; }
  details.version .texto { font-size:1.02rem; }
  .fuentes { font-size:.85rem; color:var(--muted); }
  .fuentes ul { padding-left:1.2rem; margin:.3rem 0; }
  footer { max-width:820px; margin:0 auto; padding:0 1rem 2.5rem; font-size:.78rem; color:var(--muted); line-height:1.5; }
  footer p { margin:.3rem 0; }
  @media (max-width:640px) {
    main { padding:1rem .9rem 2.5rem; }
    article { padding:1.2rem 1rem 1.1rem; }
    h1 { font-size:1.45rem; }
    .texto { font-size:1.02rem; line-height:1.7; }
    .meta { grid-template-columns:1fr; gap:.1rem; }
    .meta dt { margin-top:.4rem; }
    .topbar nav { margin-left:0; }
  }
  @media print { .topbar, .acciones { display:none; } article { border:none; box-shadow:none; padding:0; } }
"""


def pagina_articulo(data, num, art, site_url, fecha_build):
    norma = data["norma"]
    verificado = art.get("estado") == "verificado"
    vers = list(art["versiones"])  # ya en orden cronológico en cpeum.json
    vig = vers[-1]
    anteriores = list(reversed(vers[:-1]))
    camino = ruta_estructura(data["estructura"], int(num))
    cap = camino[-1] if camino else {}
    n_label = numero_art(num)
    url = f"{site_url}/articulos/{num}.html"
    titulo = f"Artículo {n_label} de la {norma['nombre']} — texto vigente"
    primer_parrafo = re.split(r"\n\s*\n", vig["texto"])[0].replace("\n", " ")
    if verificado:
        descripcion = (f"Texto vigente íntegro del Artículo {n_label} de la {norma['siglas']} "
                       f"({rango_vigencia(vig).lower()}, DOF {fmt_fecha(vig['publicacion'])}), con fechas de vigencia, "
                       f"{'enlace al decreto en el Diario Oficial de la Federación y ' if vig.get('dof_url') else ''}{len(anteriores)} versiones anteriores" + (f" desde {fmt_fecha(vers[0]['vigencia_desde'])}" if vers[0].get('vigencia_desde') else "") + ".")
    else:
        descripcion = (f"Texto vigente íntegro del Artículo {n_label} de la {norma['siglas']}, conforme al texto consolidado de la Cámara de Diputados "
                       f"(última reforma del artículo: DOF {fmt_fecha(vig['publicacion'])}). Historial de versiones en construcción.")

    migas = [f'<a href="../index.html">{esc(norma["siglas"])}</a>']
    for nodo in camino:
        et = nodo["nombre"] + (f" — {nodo['subtitulo']}" if nodo.get("subtitulo") and nodo["tipo"] != "titulo" else "")
        migas.append(f'<span title="{esc(nodo.get("subtitulo", ""))}">{esc(et)}</span>')
    migas.append(f"<b>Artículo {esc(n_label)}</b>")

    meta_vig = [
        ("Vigencia", esc(rango_vigencia(vig)) + vigencia_marca(vig) + extraccion_marca(vig)),
        ("Publicación en el DOF", esc(fmt_fecha(vig["publicacion"])) if vig.get("publicacion") else "pendiente de cotejo"),
    ]
    if vig.get("capitulo"):
        meta_vig.append(("Capítulo", esc(vig["capitulo"])))
    if vig.get("nota_extraccion"):
        meta_vig.append(("Nota de extracción", esc(vig["nota_extraccion"])))
    n_fe = sum(1 for v in vers if v.get("tipo") == "fe_de_erratas")
    n_ref = len(anteriores) - n_fe
    detalle = (f"texto original de {fmt_fecha(vers[0]['publicacion'])}, " if vers[0].get("publicacion") else "") + f"{n_ref} {'reforma' if n_ref == 1 else 'reformas'}" + (f" y {n_fe} fe de erratas" if n_fe else "")
    n_pend = sum(1 for v in vers if not v.get("publicacion"))
    meta_vig.append(("Versiones", (f"{len(vers)} ({detalle})" if len(vers) > 1 else "1") + (f"; {n_pend} con fecha pendiente de cotejo" if n_pend else "")))
    if dof_link_html(vig):
        meta_vig.append(("Fuente oficial", dof_link_html(vig)))
    elif fuente_link_html(vig):
        meta_vig.append(("Fuente oficial", fuente_link_html(vig)))
    meta_html = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in meta_vig)

    hist = []
    for v in anteriores:
        es_original = v is vers[0]
        meta_v = [("Vigencia", esc(rango_vigencia(v)) + vigencia_marca(v) + extraccion_marca(v)), ("Publicación en el DOF", esc(fmt_fecha(v["publicacion"])) if v.get("publicacion") else "pendiente de cotejo")]
        if v.get("capitulo"):
            meta_v.append(("Capítulo", esc(v["capitulo"])))
        if v.get("nota_extraccion"):
            meta_v.append(("Nota de extracción", esc(v["nota_extraccion"])))
        if dof_link_html(v):
            meta_v.append(("Fuente oficial", dof_link_html(v)))
        hist.append(
            f'<details class="version" id="version-{esc(v["id"])}">'
            f'<summary>{"Fe de erratas" if v.get("tipo") == "fe_de_erratas" else "Aclaración" if v.get("tipo") == "aclaracion" else "Texto original" if es_original else "Reforma"} · {esc(rango_vigencia(v).lower())} '
            f'<small>{("DOF " + esc(fmt_fecha(v["publicacion"], corto=True))) if v.get("publicacion") else "fecha pendiente"}</small></summary>'
            f'<div class="cuerpo"><dl class="meta">{"".join(f"<dt>{k}</dt><dd>{val}</dd>" for k, val in meta_v)}</dl>'
            f'<div class="texto">{texto_html(v["texto"])}</div></div></details>'
        )
    historial_html = ""
    if anteriores:
        historial_html = (
            f'<section id="historial" aria-labelledby="h-historial"><h2 id="h-historial">Versiones anteriores del Artículo {esc(n_label)}</h2>'
            f'<p class="fuentes">Texto íntegro de cada versión, de la más reciente a la original. Para comparar los cambios palabra por palabra, '
            f'usa el <a href="../index.html#/art/{num}/v/{esc(anteriores[0]["id"])}">historial interactivo</a>.</p>'
            + "".join(hist) + "</section>"
        )

    fuentes = "".join(f'<li><a href="{esc(f["url"])}" target="_blank" rel="noopener noreferrer">{esc(f["nombre"])}</a></li>'
                      for f in norma.get("fuentes", []))

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Legislation",
                "@id": url,
                "url": url,
                "name": f"Artículo {n_label} de la {norma['nombre']}",
                "alternateName": f"Artículo {n_label} constitucional",
                "inLanguage": "es-MX",
                "legislationType": "Constitución",
                "legislationIdentifier": f"{norma['siglas']}, artículo {n_label}",
                "legislationJurisdiction": {"@type": "AdministrativeArea", "name": "Estados Unidos Mexicanos"},
                **({"legislationDateVersion": vig["vigencia_desde"]} if vig.get("vigencia_desde") else {}),
                **({"datePublished": vig["publicacion"]} if vig.get("publicacion") else {}),
                "isPartOf": {"@type": "Legislation", "name": norma["nombre"], "legislationDate": norma["publicacion"]},
                **({"sameAs": vig["dof_url"]} if vig.get("dof_url") else {}),
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": norma["nombre"], "item": f"{site_url}/"},
                    {"@type": "ListItem", "position": 2, "name": f"Artículo {n_label}", "item": url},
                ],
            },
        ],
    }
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(titulo)} | Legislación MX</title>
<meta name="description" content="{esc(descripcion)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:locale" content="es_MX">
<meta name="theme-color" content="#0f2a4d">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230f2a4d'/%3E%3Ctext x='16' y='23' font-size='20' font-family='Georgia,serif' fill='%23fff' text-anchor='middle'%3E%C2%A7%3C/text%3E%3C/svg%3E">
<script type="application/ld+json">{ld_json}</script>
<style>{CSS}</style>
</head>
<body>
<header class="topbar">
  <a class="brand" href="../index.html">Legislación MX <span class="pill">Prototipo</span></a>
  <nav aria-label="Navegación"><a href="../index.html#/art/{num}">Navegador interactivo de la Constitución</a></nav>
</header>
<main>
  <nav class="breadcrumb" aria-label="Ubicación">{' <span aria-hidden="true">›</span> '.join(migas)}</nav>
  <article>
    <h1><span class="num">Artículo {esc(n_label)}</span> de la {esc(norma['nombre'])}</h1>
    <div class="badges"><span class="badge vigente">Texto vigente</span>{'<span class="badge verificado" title="Cotejado con las publicaciones oficiales">Verificado</span>' if verificado else '<span class="badge historial" title="El historial de la SCJN no coincide todavía con el texto vigente del consolidado">Historial por cotejar</span>' if art.get("estado") == "historial_parcial" else '<span class="badge historial" title="Las versiones anteriores se cargarán desde el DOF">Historial en construcción</span>'}</div>
    {f'<p class="tema">Tema: {esc(art["tema"])}</p>' if art.get("tema") else ''}
    <dl class="meta">{meta_html}</dl>
    {'' if verificado else '<p class="aviso-historial">Texto vigente. ' + (esc(art.get("nota", "")) if art.get("estado") == "historial_parcial" else 'Historial en construcción.') + '</p>'}
    <!-- espacio reservado para publicidad (fuera de alcance por ahora) -->
    <div class="texto" id="texto-vigente">
{texto_html(vig['texto'])}
    </div>
    <div class="acciones">
      <a class="btn" href="../index.html#/art/{num}{('/v/' + anteriores[0]['id']) if anteriores else ''}">Ver historial interactivo</a>
      <a class="btn secondary" href="../index.html">Explorar toda la Constitución</a>
    </div>
    {historial_html}
    <section id="fuentes" class="fuentes" aria-labelledby="h-fuentes">
      <h2 id="h-fuentes">Fuentes oficiales</h2>
      <p>{'Texto cotejado con las publicaciones del Diario Oficial de la Federación enlazadas en cada versión y con la compilación histórica de la Suprema Corte de Justicia de la Nación.' if verificado else f'Texto tomado del texto consolidado vigente de la Cámara de Diputados (última reforma de la Constitución: DOF {fmt_fecha(norma.get("ultima_reforma_consolidado", ""))}). Las versiones anteriores y los enlaces a cada decreto se cargarán desde el DOF y la compilación de la SCJN.'}</p>
      <ul>{fuentes}</ul>
    </section>
  </article>
</main>
<footer>
  <p><b>Aviso.</b> Texto reconstruido a partir de las publicaciones oficiales del Diario Oficial de la Federación. Verifica siempre contra la publicación oficial enlazada; esta página no constituye texto oficial ni asesoría jurídica.</p>
  <p>Página generada el {esc(fmt_fecha(fecha_build))} a partir de <code>cpeum.json</code>.</p>
</footer>
</body>
</html>
"""


# ----------------------------------------------------------------------------- sitemap y robots
def sitemap_xml(site_url, paginas, fecha_build, extra=()):
    """`paginas`: números de artículo de la CPEUM; `extra`: rutas relativas de otras normas, como (ruta, changefreq, priority)."""
    urls = ([(f"{site_url}/", "weekly", "0.6")] + [(f"{site_url}/articulos/{n}.html", "monthly", "0.9") for n in paginas]
            + [(f"{site_url}/{ruta}", f, pr) for ruta, f, pr in extra])
    items = "\n".join(
        f"  <url>\n    <loc>{esc(u)}</loc>\n    <lastmod>{fecha_build}</lastmod>\n    <changefreq>{f}</changefreq>\n    <priority>{p}</priority>\n  </url>"
        for u, f, p in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'


def robots_txt(site_url):
    return f"User-agent: *\nAllow: /\n\nSitemap: {site_url}/sitemap.xml\n"


# ----------------------------------------------------------------------------- index.html
HISTORIAL_DIR = ROOT / "historial"

def limpiar_version(v):
    return {k: val for k, val in v.items() if not k.startswith("notas") and k != "encabezado_scjn"}


def inyectar_index(data):
    """Embebe en index.html sólo la estructura y la versión vigente de cada artículo (~0.6 MB); el historial
    completo de cada artículo se publica en historial/N.json y el navegador lo carga al abrir «Ver historial»."""
    ligero = json.loads(json.dumps(data))
    HISTORIAL_DIR.mkdir(exist_ok=True)
    for num, art in ligero["articulos"].items():
        versiones = [limpiar_version(v) for v in art["versiones"]]
        (HISTORIAL_DIR / f"{num}.json").write_text(json.dumps({"numero": num, "versiones": versiones}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        art["total_versiones"] = len(versiones)
        art["versiones"] = [versiones[-1]]
        art["historial_url"] = f"historial/{num}.json"
    payload = json.dumps(ligero, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    block = f'{START}\n<script id="cpeum-data" type="application/json">\n{payload}\n</script>\n{END}'
    html_txt = INDEX.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(html_txt):
        raise SystemExit("No se encontraron los marcadores DATA:START / DATA:END en index.html")
    INDEX.write_text(pattern.sub(lambda _: block, html_txt), encoding="utf-8")
    return len(payload)


# ----------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site-url", default=SITE_URL_DEFAULT, help=f"URL base pública (por defecto {SITE_URL_DEFAULT})")
    ap.add_argument("--fecha", default=dt.date.today().isoformat(), help="Fecha de generación AAAA-MM-DD (por defecto, hoy)")
    args = ap.parse_args(argv)
    site_url = args.site_url.rstrip("/")

    data = json.loads(DATA.read_text(encoding="utf-8"))  # valida el JSON
    n_bytes = inyectar_index(data)
    print(f"index.html: {len(data['articulos'])} artículos embebidos ({n_bytes:,} bytes de datos); historial completo en historial/N.json")

    ARTICULOS_DIR.mkdir(exist_ok=True)
    paginas = []
    for num, art in sorted(data["articulos"].items(), key=lambda kv: int(kv[0])):
        if art.get("estado") not in ("verificado", "vigente", "historial_parcial"):
            continue  # los artículos de prototipo (texto simulado) no se publican como página estática
        destino = ARTICULOS_DIR / f"{num}.html"
        destino.write_text(pagina_articulo(data, num, art, site_url, args.fecha), encoding="utf-8")
        paginas.append(num)
        print(f"articulos/{num}.html: Artículo {numero_art(num)} ({len(art['versiones'])} {'versión' if len(art['versiones']) == 1 else 'versiones'})")
    if not paginas:
        print("Aviso: ningún artículo con estado 'verificado'; no se generaron páginas estáticas.")

    # Otras normas (sin historial todavía): cada módulo escribe sus páginas y devuelve las rutas que entran al sitemap.
    import build_ccdf
    extra = build_ccdf.generar(site_url, args.fecha)

    (ROOT / "sitemap.xml").write_text(sitemap_xml(site_url, paginas, args.fecha, extra), encoding="utf-8")
    (ROOT / "robots.txt").write_text(robots_txt(site_url), encoding="utf-8")
    print(f"sitemap.xml ({1 + len(paginas) + len(extra)} URL) y robots.txt generados para {site_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
