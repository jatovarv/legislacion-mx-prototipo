import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datetime import datetime

fecha_busqueda = "2026-10-07"
dt = datetime.strptime(fecha_busqueda, "%Y-%m-%d")
year, month, day = dt.strftime("%Y"), dt.strftime("%m"), dt.strftime("%d")

patron_cpeum = re.compile(
    r'^decreto por el que se.*?Constituci[oó]n Pol[ií]tica de los Estados Unidos Mexicanos',
    re.IGNORECASE | re.DOTALL
)

def extraer_candidatos(edicion):
    url_dof = f"https://www.dof.gob.mx/index.php?year={year}&month={month}&day={day}&edicion={edicion}"
    candidatos = []

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        respuesta = requests.get(url_dof, headers=headers, timeout=15)
        respuesta.raise_for_status()
        soup = BeautifulSoup(respuesta.text, 'html.parser')

        for enlace in soup.find_all('a'):
            texto = enlace.get_text(strip=True)
            if patron_cpeum.match(texto):
                href = enlace.get('href', '')
                url_completa = href if href.startswith('http') else f"https://www.dof.gob.mx/{href}"
                candidatos.append({
                    "fuente": "DOF",
                    "edicion": edicion,
                    "titulo_decreto": texto,
                    "url": url_completa,
                    "estado": "candidato a incorporación"
                })
    except Exception as e:
        print(f"Error al procesar edición {edicion}: {e}")

    return candidatos

def ejecutar_vigilancia():
    resultados = []

    for edicion in ['MAT', 'VES']:
        resultados.extend(extraer_candidatos(edicion))

    print("Nota: Edición extraordinaria documentada como no resuelta.")

    os.makedirs('vigilancia', exist_ok=True)
    datos_log = {
        "fecha": fecha_busqueda,
        "cobertura": "MAT y VES (Extraordinaria no resuelta)",
        "candidatos_cpeum": resultados
    }

    with open(f"vigilancia/{fecha_busqueda}.json", 'w', encoding='utf-8') as f:
        json.dump(datos_log, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    ejecutar_vigilancia()
