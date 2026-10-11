import requests
from bs4 import BeautifulSoup
import re
import json
import os
import sys
import argparse
import time
from datetime import datetime
from zoneinfo import ZoneInfo

parser = argparse.ArgumentParser(description="Vigilancia DOF Fase 1")
parser.add_argument('--fecha', type=str, help="Fecha a consultar en formato YYYY-MM-DD", default=None)
args = parser.parse_args()

if args.fecha:
    fecha_busqueda = args.fecha
    dt = datetime.strptime(fecha_busqueda, "%Y-%m-%d")
else:
    dt = datetime.now(ZoneInfo("America/Mexico_City"))
    fecha_busqueda = dt.strftime("%Y-%m-%d")

year, month, day = dt.strftime("%Y"), dt.strftime("%m"), dt.strftime("%d")

patron_cpeum = re.compile(
    r'^decreto por el que se.*?Constituci[oó]n Pol[ií]tica de los Estados Unidos Mexicanos',
    re.IGNORECASE | re.DOTALL
)

def extraer_candidatos(edicion):
    url_dof = f"https://www.dof.gob.mx/index.php?year={year}&month={month}&day={day}&edicion={edicion}"
    candidatos = []

    headers = {'User-Agent': 'Mozilla/5.0'}
    max_reintentos = 3
    exito = False

    for intento in range(max_reintentos):
        try:
            respuesta = requests.get(url_dof, headers=headers, timeout=15)
            respuesta.raise_for_status()
            exito = True
            break
        except requests.RequestException as e:
            print(f"Error de conexión (Intento {intento + 1}/{max_reintentos}) para edición {edicion}: {e}")
            time.sleep(3)

    if not exito:
        raise ConnectionError(f"Fallo persistente al conectar con el DOF para la edición {edicion}.")

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

    return candidatos

def ejecutar_vigilancia():
    resultados = []
    error_conexion = False

    try:
        for edicion in ['MAT', 'VES']:
            resultados.extend(extraer_candidatos(edicion))
    except ConnectionError as e:
        print(f"Error Crítico: {e}")
        error_conexion = True

    print("Nota: Edición extraordinaria documentada como no resuelta.")

    os.makedirs('vigilancia', exist_ok=True)
    datos_log = {
        "fecha": fecha_busqueda,
        "cobertura": "MAT y VES (Extraordinaria no resuelta)",
        "candidatos_cpeum": resultados
    }

    if error_conexion:
        datos_log["error_conexion"] = True

    with open(f"vigilancia/{fecha_busqueda}.json", 'w', encoding='utf-8') as f:
        json.dump(datos_log, f, ensure_ascii=False, indent=2)

    if error_conexion:
        sys.exit(1)

if __name__ == "__main__":
    ejecutar_vigilancia()
