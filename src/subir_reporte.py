import os
import time
import requests
from datetime import datetime
from selenium.webdriver.common.by import By


# Configuración API
api_url = "https://meta.fullpay.cl/api/informe-reg200"
api_token = "7|3NuAmzTOoj39dG8jhSxCGeoJSQAeU7JhDvWH4dzq8123a50b"

# Datos de acceso al portal FTP
usuario = "COB_ABO00082"
contraseña = "Og575Oi8"
url_login = f"https://{usuario}:{contraseña}@wp.falabella.cl/ftpsrv/main.jsp"

# Carpeta para guardar archivos descargados
carpeta_local = "archivos_descargados"
if not os.path.exists(carpeta_local):
    os.makedirs(carpeta_local)

def obtener_archivo_desde_api(mandante):
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    if mandante == 17:
        nombre_archivo = f"C5_200_abo00082_{fecha_actual.replace('-', '')}.txt"
    elif mandante == 14:
        nombre_archivo = f"C_200_abo00082_{fecha_actual.replace('-', '')}.txt"
    else:
        print(f"❌ Mandante {mandante} no reconocido.")
        return None, None

    ruta_archivo = os.path.join(carpeta_local, nombre_archivo)

    form_data = {"mandante": mandante, "fecha": fecha_actual}
    headers = {"Authorization": f"Bearer {api_token}"}

    print(f"✅ Solicitando archivo para la fecha {fecha_actual} y mandante {mandante}...")
    response = requests.post(api_url, data=form_data, headers=headers)

    if response.status_code == 200:
        with open(ruta_archivo, "wb") as file:
            file.write(response.content)
        print(f"✅ Archivo recibido y guardado como {ruta_archivo}")
        return ruta_archivo, nombre_archivo
    else:
        print(f"❌ Error al obtener el archivo desde la API: {response.status_code}")
        return None, None

def navegar_a_carga_200_ext(driver):
    driver.get(url_login)
    time.sleep(3)
    driver.switch_to.frame("main")
    driver.find_element(By.LINK_TEXT, "Login Basic").click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "Browse").click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "CYBUCLPR2").click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "CARGA_200_EXT").click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "Gestiones_Entrada").click()
    time.sleep(3)
    print("✅ Navegación completa hasta Gestiones_Entrada")

def subir_archivo(driver, ruta_archivo, nombre_definitivo):
    """Sube un archivo al portal desde Gestiones_Entrada"""
    try:
        boton_subir = driver.find_element(By.XPATH, "//a[contains(@href, 'FsrPutFile.jsp')]")
        boton_subir.click()
        time.sleep(2)

        driver.switch_to.window(driver.window_handles[-1])
        print("✅ Cambiado a ventana de subida")

        # Convertir a ruta absoluta
        ruta_absoluta = os.path.abspath(ruta_archivo)

        input_file = driver.find_element(By.NAME, "filenameOrig")
        input_file.send_keys(ruta_absoluta)
        print(f"✅ Archivo adjuntado: {ruta_absoluta}")

        campo_nombre_definitivo = driver.find_element(By.NAME, "filenameDest")
        campo_nombre_definitivo.clear()
        campo_nombre_definitivo.send_keys(nombre_definitivo)
        print(f"✅ Nombre definitivo asignado: {nombre_definitivo}")

        boton_confirmar = driver.find_element(By.XPATH, "//a[contains(@onclick, 'doUploadFile')]")
        boton_confirmar.click()
        print(f"✅ Archivo '{nombre_definitivo}' enviado correctamente.")

        time.sleep(5)
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"❌ Error al subir el archivo: {e}")
