#!/usr/bin/env python3
"""Inyecta cpeum.json dentro de index.html (sin dependencias).

index.html es autocontenido: lleva los datos embebidos entre los marcadores
<!-- DATA:START --> y <!-- DATA:END --> para que funcione igual abriendo el
archivo en local (file://) que publicado en GitHub Pages.

Uso:  python3 build.py        (edita cpeum.json y vuelve a ejecutar)
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "cpeum.json"
HTML = ROOT / "index.html"

START = "<!-- DATA:START -->"
END = "<!-- DATA:END -->"


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))  # valida el JSON
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Evita cerrar el <script> por accidente si un texto contiene "</script>".
    payload = payload.replace("</", "<\\/")
    block = (
        f'{START}\n<script id="cpeum-data" type="application/json">\n'
        f"{payload}\n</script>\n{END}"
    )
    html = HTML.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(html):
        print("No se encontraron los marcadores DATA:START / DATA:END en index.html", file=sys.stderr)
        return 1
    HTML.write_text(pattern.sub(lambda _: block, html), encoding="utf-8")
    n = len(data["articulos"])
    print(f"OK: {n} artículos embebidos en index.html ({len(payload):,} bytes de datos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
