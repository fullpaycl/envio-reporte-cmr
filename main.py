import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime

# 📅 Obtener el mes actual en formato YYYYMM
fecha_actual = datetime.now().strftime("%Y%m")

# 📂 Carpeta donde se guardarán los archivos
carpeta_descargas = "archivos_descargados"
if not os.path.exists(carpeta_descargas):
    os.makedirs(carpeta_descargas)

# Configuración del navegador
chrome_options = Options()
chrome_options.add_argument("--headless")  # Sin interfaz gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# Inicializar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL con autenticación
usuario = "COB_ABO00082"
contraseña = "Og575Oi8"
url_login = f"https://{usuario}:{contraseña}@wp.falabella.cl/ftpsrv/main.jsp"


# 1️⃣ Acceder a la página principal y autenticarse con Selenium
driver.get(url_login)
time.sleep(3)

# 2️⃣ Cambiar al Frame Principal
try:
    driver.switch_to.frame("main")
    print("✅ Cambio al frame 'main' exitoso.")

    # 3️⃣ Hacer clic en "Login Basic"
    boton_login = driver.find_element(By.LINK_TEXT, "Login Basic")
    boton_login.click()
    print("✅ Click en 'Login Basic' exitoso")
    time.sleep(3)

    # 4️⃣ Hacer clic en "Browse"
    boton_browse = driver.find_element(By.LINK_TEXT, "Browse")
    boton_browse.click()
    print("✅ Click en 'Browse' exitoso")
    time.sleep(3)

    # 5️⃣ Hacer clic en "CYBUCLPR2"
    boton_cybuclpr2 = driver.find_element(By.LINK_TEXT, "CYBUCLPR2")
    boton_cybuclpr2.click()
    print("✅ Click en 'CYBUCLPR2' exitoso")
    time.sleep(3)

    # 6️⃣ Hacer clic en "PD-ABO"
    boton_pd_abo = driver.find_element(By.LINK_TEXT, "PD-ABO")
    boton_pd_abo.click()
    print("✅ Click en 'PD-ABO' exitoso")
    time.sleep(3)

    # 7️⃣ Buscar los archivos con la fecha actual en la carpeta "PD-ABO"
    archivos_descargar = []
    enlaces = driver.find_elements(By.TAG_NAME, "a")

    for enlace in enlaces:
        archivo_nombre = enlace.text.strip()
        archivo_url = enlace.get_attribute("href")

        # Filtrar archivos TXT con la fecha actual
        if archivo_nombre.endswith(".TXT") and fecha_actual in archivo_nombre:
            archivos_descargar.append((archivo_nombre, archivo_url))

    print(f"📂 Se encontraron {len(archivos_descargar)} archivos para descargar en {fecha_actual}")

    # 8️⃣ Obtener cookies de sesión de Selenium
    cookies = driver.get_cookies()
    session = requests.Session()

    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # 9️⃣ Descargar los archivos usando `requests` con las cookies de sesión
    for archivo_nombre, archivo_url in archivos_descargar:
        try:
            print(f"⬇️ Descargando: {archivo_nombre} ...")

            response = session.get(archivo_url, stream=True)

            if response.status_code == 200:
                ruta_guardado = os.path.join(carpeta_descargas, archivo_nombre)
                with open(ruta_guardado, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)

                print(f"✅ Archivo guardado: {ruta_guardado}")
            else:
                print(f"❌ Error al descargar {archivo_nombre}: Código {response.status_code}")

        except Exception as e:
            print(f"❌ Error al descargar {archivo_nombre}: {e}")

except Exception as e:
    print("❌ Error en la navegación:", e)

# 🔚 Cerrar el navegador
driver.quit()
