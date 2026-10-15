#!/usr/bin/env python3
"""Genera las páginas estáticas del Código Civil para el Distrito Federal (CCDF) a partir de ccdf.json.

Lo invoca build.py (no se corre solo). Produce:
  ccdf/index.html            índice navegable (Libros › Partes › Títulos) con metadatos de la norma
  ccdf/articulos/N.html      una página por artículo cargado en ccdf.json

Reglas:
- No hay historial del CCDF todavía: cada artículo tiene sólo su texto vigente (`texto`) o ninguno.
- Un artículo con `texto: null` (estado «pendiente») se publica con el marcador «pendiente de cotejo», sin texto
  normativo, con <meta name="robots" content="noindex,follow"> y NO entra en el sitemap: una página sin texto
  no debe indexarse. En cuanto se cargue el texto cotejado, la misma página pasa a indexarse sin tocar nada más.
- Los rangos y nombres de la estructura llevan `rango_por_cotejar` / `nombre_por_cotejar` hasta cotejarlos con el
  consolidado; mientras `norma.estructura_cotejada` sea false, el índice lleva noindex y no entra al sitemap.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
DATA_CCDF = ROOT / "ccdf.json"
CCDF_DIR = ROOT / "ccdf"
CCDF_ART_DIR = CCDF_DIR / "articulos"

CSS_EXTRA = """
  .badge.pendiente { background:#fff6e5; color:#92400e; border-color:#f2c879; }
  .pendiente-box { margin-top:1.2rem; padding:1rem 1.1rem; border:1px dashed #f2c879; background:#fffaf0; border-radius:8px; color:#5c3a0a; font-size:.95rem; }
  .pendiente-box b { color:#92400e; }
  .arbol { list-style:none; padding-left:0; margin:0; }
  .arbol ul { list-style:none; padding-left:1.1rem; margin:.2rem 0 .6rem; border-left:2px solid var(--border); }
  .arbol li { margin:.25rem 0; }
  .arbol .nodo { font-weight:600; color:var(--brand); }
  .arbol .nodo.seccion { font-weight:500; font-style:italic; }
  .arbol .sub { color:var(--text); font-weight:400; }
  .arbol .rango { color:var(--muted); font-size:.8rem; white-space:nowrap; }
  .arbol details > summary { cursor:pointer; list-style:none; }
  .arbol details > summary::-webkit-details-marker { display:none; }
  .arbol details > summary::before { content:"▸"; color:var(--muted); margin-right:.4rem; font-size:.9em; }
  .arbol details[open] > summary::before { content:"▾"; }
  .muestra { display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:.5rem; padding:0; list-style:none; margin:.6rem 0 0; }
  .muestra li { border:1px solid var(--border); border-radius:8px; padding:.55rem .7rem; background:#fbfcfd; font-size:.9rem; }
  .muestra a { font-weight:600; text-decoration:none; }
  .muestra .tema { margin:.15rem 0 0; font-size:.82rem; }
"""


def slug(num):
    return re.sub(r"\s+", "-", str(num).strip())


def rango_html(nodo, esc):
    r = nodo.get("articulos")
    marca = ""
    if nodo.get("rango_por_cotejar") or nodo.get("nombre_por_cotejar"):
        que = " y ".join(x for x, f in (("nombre", nodo.get("nombre_por_cotejar")), ("rango", nodo.get("rango_por_cotejar"))) if f)
        marca = f' <span class="por-cotejar" title="{esc(que.capitalize())} pendiente de cotejo con el texto consolidado oficial">por cotejar</span>'
    if not r:
        return marca
    txt = f"Arts. {r['desde']}–{r['hasta']}" if r["desde"] != r["hasta"] else f"Art. {r['desde']}"
    der = f"; {nodo['n_derogados']} derogado{'s' if nodo['n_derogados'] != 1 else ''}" if nodo.get("n_derogados") else ""
    fuente = f' title="Fuente: PDF del Congreso CDMX, p. {nodo["pagina"]}{der}"' if nodo.get("pagina") else ""
    return f' <span class="rango"{fuente}>({esc(txt)})</span>{marca}'


def arbol_html(nodos, esc, nivel=0):
    out = []
    for n in nodos:
        etiqueta = (f'<span class="nodo{" seccion" if n["tipo"] == "seccion" else ""}">{esc(n["nombre"])}</span>'
                    + (f' <span class="sub">— {esc(n["subtitulo"])}</span>' if n.get("subtitulo") else ""))
        hijos = n.get("hijos")
        if hijos:
            out.append(f'<li><details{" open" if nivel == 0 else ""}><summary>{etiqueta}{rango_html(n, esc)}</summary>'
                       f'<ul>{arbol_html(hijos, esc, nivel + 1)}</ul></details></li>')
        else:
            out.append(f"<li>{etiqueta}{rango_html(n, esc)}</li>")
    return "".join(out)


def ruta(estructura, num):
    """Camino (Libro › Parte › Título) que contiene el artículo `num`; sólo numerales enteros."""
    try:
        n = int(str(num).split()[0])
    except ValueError:
        return []

    def dentro(nodo):
        r = nodo.get("articulos")
        if not r:
            return False
        try:
            return int(str(r["desde"]).split()[0]) <= n <= int(str(r["hasta"]).split()[0])
        except ValueError:
            return False

    def visitar(nodo, camino):
        camino = camino + [nodo]
        for h in nodo.get("hijos", []):
            res = visitar(h, camino)
            if res:
                return res
        return camino if dentro(nodo) else None

    for nodo in estructura:
        res = visitar(nodo, [])
        if res:
            return res
    return []


def ld_norma(norma, site_url):
    return {
        "@type": "Legislation",
        "@id": f"{site_url}/ccdf/index.html",
        "url": f"{site_url}/ccdf/index.html",
        "name": norma["nombre"],
        "alternateName": norma.get("aliases", []),
        "inLanguage": "es-MX",
        "legislationType": norma.get("tipo", "Código"),
        "legislationIdentifier": norma["siglas"],
        "legislationJurisdiction": {"@type": "AdministrativeArea", "name": norma.get("jurisdiccion", "Ciudad de México")},
        "legislationDate": norma["publicacion_original"]["fechas"][0],
        "legislationDateVersion": norma["ultima_reforma"]["vigencia_desde"],
        "legislationLegalForce": "InForce",
    }


def cabecera(titulo, descripcion, url, ld, b, extra_head="", og_type="website"):
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{b.esc(titulo)} | Legislación MX</title>
<meta name="description" content="{b.esc(descripcion)}">
<link rel="canonical" href="{b.esc(url)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{b.esc(titulo)}">
<meta property="og:description" content="{b.esc(descripcion)}">
<meta property="og:url" content="{b.esc(url)}">
<meta property="og:locale" content="es_MX">
<meta name="theme-color" content="#0f2a4d">{extra_head}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230f2a4d'/%3E%3Ctext x='16' y='23' font-size='20' font-family='Georgia,serif' fill='%23fff' text-anchor='middle'%3E%C2%A7%3C/text%3E%3C/svg%3E">
<script type="application/ld+json">{ld_json}</script>
<style>{b.CSS}{CSS_EXTRA}</style>
</head>
"""


def pagina_indice(data, site_url, fecha_build, b):
    norma = data["norma"]
    url = f"{site_url}/ccdf/index.html"
    ur = norma["ultima_reforma"]
    titulo = f"{norma['nombre']} — índice y texto vigente"
    descripcion = (f"Índice navegable del {norma['nombre']} (Ciudad de México) por Libros, Partes y Títulos, con la última reforma verificada "
                   f"({b.fmt_fecha(ur['fecha'])}, Gaceta Oficial de la Ciudad de México {ur['edicion']}) y acceso al texto vigente artículo por artículo.")
    ld = {"@context": "https://schema.org", "@graph": [ld_norma(norma, site_url), {
        "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Legislación MX", "item": f"{site_url}/"},
            {"@type": "ListItem", "position": 2, "name": norma["nombre"], "item": url}]}]}
    arts = sorted(data["articulos"].values(), key=lambda a: int(str(a["numero"]).split()[0]))
    n_texto = sum(1 for a in arts if a.get("texto"))
    muestra = "".join(
        f'<li><a href="articulos/{slug(a["numero"])}.html">Artículo {b.esc(str(a["numero"]))}</a>'
        + (' <span class="por-cotejar">texto por cotejar</span>' if not a.get("texto") else "")
        + (f'<p class="tema">{b.esc(a["tema"])}</p>' if a.get("tema") else "") + "</li>"
        for a in arts)
    fuentes = "".join(f'<li><a href="{b.esc(f["url"])}" target="_blank" rel="noopener noreferrer">{b.esc(f["nombre"])}</a></li>' for f in norma.get("fuentes", []))
    tc = norma["texto_consolidado"]
    pub = norma["publicacion_original"]
    tc_hash_marca = "" if tc.get("sha256") else f' — <span class="por-cotejar" title="{b.esc(tc.get("nota", ""))}">hash SHA-256 pendiente</span>'
    meta = [
        ("Última reforma verificada", f"{b.esc(b.fmt_fecha(ur['fecha']))} — {b.esc(ur['medio'])}, edición {b.esc(ur['edicion'])} (arts. {b.esc(', '.join(ur['articulos_afectados']))})"),
        ("Vigencia de la última reforma", f"desde el {b.esc(b.fmt_fecha(ur['vigencia_desde']))}" + ("" if ur.get("vigencia_verificada") else ' <span class="por-cotejar">por cotejar</span>')),
        ("Publicación original", f"{b.esc(pub['medio'])}, {b.esc(', '.join(b.fmt_fecha(f, corto=True) for f in pub['fechas']))}"),
        ("Texto consolidado", f"{b.esc(tc['fuente'])}{tc_hash_marca}"),
        ("Artículos cargados", f"{len(arts)} ({n_texto} con texto vigente publicado, {len(arts) - n_texto} pendientes de cotejo)"),
    ]
    meta_html = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in meta)
    cm = norma.get("conflicto_metadatos")
    cotejada = norma.get("estructura_cotejada", True)
    robots = "" if cotejada else '\n<meta name="robots" content="noindex,follow">'
    badge_articulos = (
        f'<span class="badge historial" title="{b.esc(norma["aviso"])}">Muestra de {n_texto} artículos con texto vigente</span>'
        if n_texto == len(arts) and n_texto > 0
        else f'<span class="badge pendiente" title="{b.esc(norma["aviso"])}">Texto de los artículos por cotejar</span>'
    )
    return cabecera(titulo, descripcion, url, ld, b, extra_head=robots) + f"""<body>
<header class="topbar">
  <a class="brand" href="../index.html">Legislación MX <span class="pill">Prototipo</span></a>
  <nav aria-label="Navegación"><a href="../index.html">Constitución (CPEUM)</a></nav>
</header>
<main>
  <nav class="breadcrumb" aria-label="Ubicación"><a href="../index.html">Legislación MX</a> <span aria-hidden="true">›</span> <b>{b.esc(norma['siglas'])}</b></nav>
  <article>
    <h1>{b.esc(norma['nombre'])}</h1>
    <div class="badges"><span class="badge vigente">Texto vigente</span>{'<span class="badge verificado" title="Índice cotejado con el PDF oficial del Congreso de la Ciudad de México">Índice cotejado</span>' if norma.get('estructura_cotejada') else ''}{badge_articulos}</div>
    <p class="tema">También citado como {b.esc(' / '.join(norma.get('aliases', [])))}. Jurisdicción: {b.esc(norma.get('jurisdiccion', ''))}.</p>
    <dl class="meta">{meta_html}</dl>
    <p class="aviso-historial">{b.esc(norma['aviso'])}</p>
    <h2 id="h-indice">Índice del Código</h2>
    <p class="fuentes">{b.esc(norma.get('estructura_nota', ''))}</p>
    <ul class="arbol">{arbol_html(data['estructura'], b.esc)}</ul>
    <h2 id="h-articulos">Artículos disponibles</h2>
    <ul class="muestra">{muestra}</ul>
    <section id="fuentes" class="fuentes" aria-labelledby="h-fuentes">
      <h2 id="h-fuentes">Fuentes oficiales</h2>
      <ul>{fuentes}</ul>
      {f'<p>Conflicto de metadatos documentado: {b.esc(cm["fuente"])} reporta última reforma {b.esc(b.fmt_fecha(cm["ultima_reforma_reportada"]))}. {b.esc(cm["tratamiento"])}</p>' if cm else ''}
    </section>
  </article>
</main>
<footer>
  <p><b>Aviso.</b> {b.esc(norma['aviso'])} Verifica siempre contra la publicación oficial; esta página no constituye asesoría jurídica.</p>
  <p>Página generada el {b.esc(b.fmt_fecha(fecha_build))} a partir de <code>ccdf.json</code>.</p>
</footer>
</body>
</html>
"""


def pagina_articulo(data, art, site_url, fecha_build, b):
    norma = data["norma"]
    num = str(art["numero"])
    url = f"{site_url}/ccdf/articulos/{slug(num)}.html"
    con_texto = bool(art.get("texto"))
    camino = ruta(data["estructura"], num)
    ur = norma["ultima_reforma"]
    titulo = f"Artículo {num} del {norma['nombre']} — texto vigente"
    if con_texto:
        descripcion = f"Texto vigente íntegro del Artículo {num} del {norma['nombre']} (Ciudad de México), conforme al texto consolidado de la Consejería Jurídica (última reforma del Código: GOCDMX {b.fmt_fecha(ur['fecha'])})."
    else:
        descripcion = f"Artículo {num} del {norma['nombre']} (Ciudad de México): ficha con su ubicación en el Código y la última reforma verificada; texto vigente pendiente de cotejo con el consolidado oficial."
    migas = [f'<a href="../index.html">{b.esc(norma["siglas"])}</a>']
    for nodo in camino:
        et = nodo["nombre"] + (f" — {nodo['subtitulo']}" if nodo.get("subtitulo") else "")
        migas.append(f"<span>{b.esc(et)}</span>")
    migas.append(f"<b>Artículo {b.esc(num)}</b>")
    ld_art = {
        "@type": "Legislation", "@id": url, "url": url,
        "name": f"Artículo {num} del {norma['nombre']}",
        "inLanguage": "es-MX",
        "legislationType": norma.get("tipo", "Código"),
        "legislationIdentifier": f"{norma['siglas']}, artículo {num}",
        "legislationJurisdiction": {"@type": "AdministrativeArea", "name": norma.get("jurisdiccion", "Ciudad de México")},
        "isPartOf": {"@id": f"{site_url}/ccdf/index.html"},
    }
    ra = art.get("ultima_reforma")
    reformas = art.get("reformas", [])
    pub_orig = norma["publicacion_original"]
    if ra:
        if ra.get("vigencia_desde"):
            ld_art["legislationDateVersion"] = ra["vigencia_desde"]
        if ra.get("fecha"):
            ld_art["datePublished"] = ra["fecha"]
        if ra.get("url_oficial"):
            ld_art["sameAs"] = ra["url_oficial"]
    else:
        ld_art["legislationDateVersion"] = pub_orig["vigencia_desde"]
    ld = {"@context": "https://schema.org", "@graph": [ld_art, ld_norma(norma, site_url), {
        "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": norma["nombre"], "item": f"{site_url}/ccdf/index.html"},
            {"@type": "ListItem", "position": 2, "name": f"Artículo {num}", "item": url}]}]}
    meta = []
    if ra:
        ed_html = f", edición {b.esc(ra['edicion'])}" if ra.get("edicion") else ' (<span class="por-cotejar" title="Campo edicion: null en datos_cccdmx.json">edición pendiente</span>)'
        frac_html = f" (fracción {b.esc(ra['fraccion'])})" if ra.get("fraccion") else ""
        id_html = f" [{b.esc(ra['id_reforma'])}]" if ra.get("id_reforma") else ""
        meta.append(("Última reforma del artículo", f"{b.esc(b.fmt_fecha(ra['fecha']))} — {b.esc(ra['medio'])}{ed_html}{frac_html}{id_html}"))
        if ra.get("vigencia_desde"):
            meta.append(("Vigencia", f"desde el {b.esc(b.fmt_fecha(ra['vigencia_desde']))}" + ("" if ra.get("vigencia_verificada") else ' <span class="por-cotejar">por cotejar</span>')))
        else:
            meta.append(("Vigencia", '<span class="por-cotejar" title="Campo vigencia_desde: null en datos_cccdmx.json">fecha de inicio de vigencia pendiente</span>'))
    else:
        meta.append(("Última reforma del artículo", "Sin reformas registradas (texto original de 1928)"))
        meta.append(("Vigencia", f"desde el {b.esc(b.fmt_fecha(pub_orig['vigencia_desde']))} (entrada en vigor original)"))

    enlaces_dof = [
        f'<a class="dof-link" href="{b.esc(r["url_oficial"])}" target="_blank" rel="noopener noreferrer">DOF {b.esc(b.fmt_fecha(r["fecha"], corto=True))} ({b.esc(r["id_reforma"])}) ↗</a>'
        for r in reformas if r.get("url_oficial")
    ]
    if ra and ra.get("url_oficial") and not enlaces_dof:
        enlaces_dof.append(f'<a class="dof-link" href="{b.esc(ra["url_oficial"])}" target="_blank" rel="noopener noreferrer">Ver publicación oficial ↗</a>')
    tiene_gaceta_sin_url = any(not r.get("url_oficial") for r in reformas) or (ra is not None and not ra.get("url_oficial"))
    if enlaces_dof and tiene_gaceta_sin_url:
        pub_html = ", ".join(enlaces_dof) + ' · <span class="por-cotejar" title="Campo url_oficial: null para Gaceta Oficial en datos_cccdmx.json">enlace directo a Gaceta pendiente</span> (<a class="dof-link" href="https://www.consejeria.cdmx.gob.mx/gaceta-oficial" target="_blank" rel="noopener noreferrer">portal GOCDMX ↗</a>)'
    elif enlaces_dof:
        pub_html = ", ".join(enlaces_dof)
    elif tiene_gaceta_sin_url:
        pub_html = '<span class="por-cotejar" title="Campo url_oficial: null para Gaceta Oficial en datos_cccdmx.json">enlace directo a Gaceta Oficial pendiente</span> (<a class="dof-link" href="https://www.consejeria.cdmx.gob.mx/gaceta-oficial" target="_blank" rel="noopener noreferrer">portal GOCDMX ↗</a>)'
    else:
        pub_html = 'Diario Oficial de la Federación (publicaciones originales de 1928) · <a class="dof-link" href="https://www.dof.gob.mx/" target="_blank" rel="noopener noreferrer">DOF ↗</a>'
    meta.append(("Publicación oficial (DOF / Gaceta)", pub_html))
    meta.append(("Última reforma del Código", f"{b.esc(b.fmt_fecha(ur['fecha']))} (GOCDMX {b.esc(ur['edicion'])})"))
    if camino:
        meta.append(("Ubicación", b.esc(" › ".join(n["nombre"] + (f" — {n['subtitulo']}" if n.get("subtitulo") else "") for n in camino))))
    meta.append(("Fuente del texto vigente", f"<code>{b.esc(art.get('fuente_texto', 'data/ccdf/datos_cccdmx.json'))}</code> (pipeline Colab CCDF)" if con_texto else '<span class="por-cotejar" title="' + b.esc(art.get("nota", "")) + '">pendiente de cotejo</span>'))
    meta_html = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in meta)
    cuerpo = (f'<div class="texto" id="texto-vigente">\n{b.texto_html(art["texto"])}\n    </div>' if con_texto else
              f'<div class="pendiente-box" id="texto-vigente"><b>Texto pendiente de cotejo.</b> {b.esc(art.get("nota", ""))}</div>')
    aviso_art = f'<p class="aviso-historial">{b.esc(art["nota"])}</p>' if (con_texto and art.get("nota")) else ""

    items_ref = []
    for r in reformas:
        link_r = (f' — <a class="dof-link" href="{b.esc(r["url_oficial"])}" target="_blank" rel="noopener noreferrer">Ver en el DOF ↗</a>'
                  if r.get("url_oficial") else ' — <span class="por-cotejar" title="url_oficial: null en datos_cccdmx.json">enlace directo pendiente</span>')
        items_ref.append(
            f'<li><b>{b.esc(b.fmt_fecha(r["fecha"]))}</b> · <code>{b.esc(r["id_reforma"])}</code> — {b.esc(r["medio"])}'
            f' ({b.esc(r["nota"])}){link_r}</li>'
        )
    if ra and not any(r.get("fecha") == ra.get("fecha") for r in reformas):
        ed_r = f", edición {b.esc(ra['edicion'])}" if ra.get("edicion") else ""
        frac_r = f" (fracción {b.esc(ra['fraccion'])})" if ra.get("fraccion") else ""
        vig_r = f", en vigor desde el {b.esc(b.fmt_fecha(ra['vigencia_desde']))}" if ra.get("vigencia_desde") else ""
        items_ref.append(
            f'<li><b>{b.esc(b.fmt_fecha(ra["fecha"]))}</b> — {b.esc(ra["medio"])}{ed_r}{frac_r}{vig_r}'
            f' — <span class="por-cotejar" title="url_oficial: null">enlace directo pendiente</span></li>'
        )
    reformas_html = ""
    if items_ref:
        reformas_html = (
            f'<section id="reformas" class="fuentes" aria-labelledby="h-reformas">'
            f'<h2 id="h-reformas">Decretos de reforma registrados ({len(items_ref)})</h2>'
            f'<ul>{"".join(items_ref)}</ul></section>'
        )

    robots = "" if con_texto else '\n<meta name="robots" content="noindex,follow">'
    fuentes = "".join(f'<li><a href="{b.esc(f["url"])}" target="_blank" rel="noopener noreferrer">{b.esc(f["nombre"])}</a></li>' for f in norma.get("fuentes", []))
    return cabecera(titulo, descripcion, url, ld, b, extra_head=robots, og_type="article") + f"""<body>
<header class="topbar">
  <a class="brand" href="../../index.html">Legislación MX <span class="pill">Prototipo</span></a>
  <nav aria-label="Navegación"><a href="../index.html">Índice del Código Civil CDMX</a></nav>
</header>
<main>
  <nav class="breadcrumb" aria-label="Ubicación">{' <span aria-hidden="true">›</span> '.join(migas)}</nav>
  <article>
    <h1><span class="num">Artículo {b.esc(num)}</span> del {b.esc(norma['nombre'])}</h1>
    <div class="badges">{'<span class="badge vigente">Texto vigente</span>' if con_texto else '<span class="badge pendiente" title="' + b.esc(art.get("nota", "")) + '">Texto pendiente de cotejo</span>'}</div>
    {f'<p class="tema">Tema: {b.esc(art["tema"])}</p>' if art.get("tema") else ''}
    <dl class="meta">{meta_html}</dl>
    {aviso_art}
    {cuerpo}
    {reformas_html}
    <div class="acciones">
      <a class="btn" href="../index.html#h-indice">Índice del Código</a>
      <a class="btn secondary" href="../../index.html">Constitución (CPEUM)</a>
    </div>
    <section id="fuentes" class="fuentes" aria-labelledby="h-fuentes">
      <h2 id="h-fuentes">Fuentes oficiales</h2>
      <p>{'Texto vigente importado literalmente de <code>data/ccdf/datos_cccdmx.json</code> (extraído del texto consolidado de la Consejería Jurídica y de Servicios Legales de la Ciudad de México).' if con_texto else b.esc(norma['texto_consolidado']['nota'])} Última reforma verificada del Código: {b.esc(b.fmt_fecha(ur['fecha']))}, {b.esc(ur['medio'])} {b.esc(ur['edicion'])}.</p>
      <ul>{fuentes}</ul>
    </section>
  </article>
</main>
<footer>
  <p><b>Aviso.</b> {b.esc(norma['aviso'])} Verifica siempre contra la publicación oficial; esta página no constituye asesoría jurídica.</p>
  <p>Página generada el {b.esc(b.fmt_fecha(fecha_build))} a partir de <code>ccdf.json</code>.</p>
</footer>
</body>
</html>
"""


def generar(site_url, fecha_build):
    """Escribe ccdf/index.html y ccdf/articulos/N.html. Devuelve las rutas (relativas al sitio) que deben entrar al sitemap."""
    import build as b  # helpers compartidos (CSS, esc, fmt_fecha, texto_html); importación tardía para evitar el ciclo
    if not DATA_CCDF.exists():
        return []
    data = json.loads(DATA_CCDF.read_text(encoding="utf-8"))
    CCDF_ART_DIR.mkdir(parents=True, exist_ok=True)
    (CCDF_DIR / "index.html").write_text(pagina_indice(data, site_url, fecha_build, b), encoding="utf-8")
    rutas = [("ccdf/index.html", "weekly", "0.7")] if data["norma"].get("estructura_cotejada", True) else []  # índice sin cotejar: noindex y fuera del sitemap
    n_texto = 0
    for art in sorted(data["articulos"].values(), key=lambda a: int(str(a["numero"]).split()[0])):
        destino = CCDF_ART_DIR / f"{slug(art['numero'])}.html"
        destino.write_text(pagina_articulo(data, art, site_url, fecha_build, b), encoding="utf-8")
        if art.get("texto"):
            rutas.append((f"ccdf/articulos/{slug(art['numero'])}.html", "monthly", "0.8"))
            n_texto += 1
    print(f"ccdf/index.html{'' if rutas else ' (índice sin cotejar: noindex, fuera del sitemap)'} + {len(data['articulos'])} artículos del CCDF ({n_texto} con texto, {len(data['articulos']) - n_texto} pendientes de cotejo, excluidos del sitemap)")
    return rutas
