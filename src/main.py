import os
import logging
from flask import Flask, jsonify, request
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import EMAIL_CONFIG
from mailer import send_email
from subir_reporte import obtener_archivo_desde_api, navegar_a_carga_200_ext, subir_archivo

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
Logger = logging.getLogger(__name__)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.binary_location = "/usr/bin/google-chrome"  # Ruta binario Chrome


def generar_contenido_html(mensaje, nombre_archivo_definitivo=None, mandante=None, estado=True):
    fecha_hora_ejecucion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if mandante == 17:
        mandante = "CMR"
    if mandante == 14:
        mandante = "BANCO FALABELLA"

    contenido = f"""
    <html>
    <body>
        <p>{mensaje}</p>
        <p>Fecha y hora de ejecución: {fecha_hora_ejecucion}</p>
    """
    if nombre_archivo_definitivo:
        contenido += f"<p>Archivo usado por el proceso: {nombre_archivo_definitivo}</p>"
    if mandante:
        contenido += f"<p>Mandante: {mandante}</p>"

    if estado:
        contenido += "<p>Estado: ✅ Proceso exitoso</p></body></html>"
    else:
        contenido += "<p>Estado: ❌ Proceso fallido</p></body></html>"

    return contenido


@app.route("/", methods=["POST"])
def subir_reporte():
    data = request.get_json()
    mandante = data.get("mandante")

    if not mandante:
        return jsonify({"error": "Mandante no proporcionado"}), 400

    # 🆕 Crear driver dentro del request
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Paso 1: Obtener archivo desde la API
        ruta_archivo_local, nombre_archivo_definitivo = obtener_archivo_desde_api(mandante)

        if not ruta_archivo_local:
            subject = "Error en el proceso de subida de archivo ❌"
            content = generar_contenido_html(f"❌ No se obtuvo archivo desde la API para mandante {mandante}")
            send_email(subject, content, recipients=EMAIL_CONFIG["recipients"], estado=False)
            return jsonify({"error": f" ❌ No se obtuvo archivo desde la API para mandante {mandante}"}), 500

        try:
            # Paso 2: Subir archivo al FTP
            navegar_a_carga_200_ext(driver)
            subir_archivo(driver, ruta_archivo_local, nombre_archivo_definitivo)

            Logger.info(
                f"{datetime.now()} - Archivo {nombre_archivo_definitivo} descargado y subido con éxito para mandante {mandante}.")

            if mandante == 17:
                mandante = "CMR"
            if mandante == 14:
                mandante = "BANCO FALABELLA"

            subject = f"✅Proceso carga reporte {mandante},  completado con éxito 📋"
            content = generar_contenido_html("El proceso de subida de archivo se ejecutó correctamente.",
                                             nombre_archivo_definitivo, mandante)
            send_email(subject, content, recipients=EMAIL_CONFIG["recipients"], attachment_path=ruta_archivo_local)

            os.remove(ruta_archivo_local)
            print(f"✅ Archivo {ruta_archivo_local} eliminado después de subirlo.")
            return jsonify({"message": "Proceso completado con éxito"}), 200
        except Exception as e:
            subject = "Error en el proceso de subida de archivo ❌"
            content = generar_contenido_html(f" ❌ Error al subir el archivo al FTP: {e}", nombre_archivo_definitivo,
                                             mandante)
            send_email(subject, content, recipients=EMAIL_CONFIG["recipients"], attachment_path=ruta_archivo_local,
                       estado=False)
            return jsonify({"error": f"Error al subir el archivo al FTP: {e}"}), 500

    finally:
        driver.quit()


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0", debug=False)
