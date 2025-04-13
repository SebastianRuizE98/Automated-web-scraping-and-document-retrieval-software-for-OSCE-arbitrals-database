from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Configurar el driver de Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": r"G:\Mi unidad\Proyectos\Lector de Docs de SEACE\DOCS LAUDOS",  # Ruta de descarga
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Evitar detección de Selenium y bloqueos de pop-ups
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Iniciar WebDriver
driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
wait = WebDriverWait(driver, 20)

# Ruta de descarga
download_path = r"G:\Mi unidad\Proyectos\Lector de Docs de SEACE\DOCS LAUDOS"

def esperar_descarga():
    timeout = 30
    tiempo_inicial = time.time()
    while time.time() - tiempo_inicial < timeout:
        archivos = os.listdir(download_path)
        if any(archivo.endswith(".crdownload") for archivo in archivos):
            time.sleep(1)  # Esperar a que termine la descarga
        else:
            return True
    return False

try:
    # Cargar la página
    url = "https://prodapp1.osce.gob.pe/sda-pub/documentos/public/busquedaArbitraje.xhtml"
    driver.get(url)

    # Esperar a que desaparezca el modal de carga inicial
    wait.until(EC.invisibility_of_element_located((By.ID, "formBusqueda:windowprocesandoDialog_modal")))

    # Seleccionar el año 2024
    campo_año = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formBusqueda:j_idt29:idAnioLaudo_label"]')))
    campo_año.click()
    año_2024 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formBusqueda:j_idt29:idAnioLaudo_panel"]/div/ul/li[3]')))
    año_2024.click()

    # Esperar a que desaparezca el modal antes de buscar
    wait.until(EC.invisibility_of_element_located((By.ID, "formBusqueda:windowprocesandoDialog_modal")))

    # Clic en el botón de búsqueda
    boton_buscar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formBusqueda:j_idt29:j_idt135"]/span[2]')))
    driver.execute_script("arguments[0].click();", boton_buscar)

    # Esperar a que carguen los resultados
    wait.until(EC.invisibility_of_element_located((By.ID, "formBusqueda:windowprocesandoDialog_modal")))
    
    while True:
        # Esperar a que la tabla esté disponible
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="formBusqueda:j_idt29:tablaLaudos_data"]')))
        
        # Obtener todas las filas de la tabla
        filas = driver.find_elements(By.XPATH, '//*[@id="formBusqueda:j_idt29:tablaLaudos_data"]/tr')

        for i in range(1, len(filas) + 1):
            try:
                boton_descarga = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="formBusqueda:j_idt29:tablaLaudos_data"]/tr[{i}]/td[10]/a/img')))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_descarga)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", boton_descarga)
                esperar_descarga()  # Esperar a que termine la descarga antes de continuar
            except Exception as e:
                print(f"Error al descargar en fila {i}: {e}")

        # Intentar avanzar a la siguiente página
        try:
            boton_siguiente = driver.find_element(By.XPATH, '//*[@id="formBusqueda:j_idt29:tablaLaudos_paginator_bottom"]/span[5]')
            
            if "ui-state-disabled" not in boton_siguiente.get_attribute("class"):
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_siguiente)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", boton_siguiente)
                
                # Esperar a que carguen los nuevos datos
                wait.until(EC.invisibility_of_element_located((By.ID, "formBusqueda:windowprocesandoDialog_modal")))
            else:
                print("No hay más páginas disponibles.")
                break
        except Exception as e:
            print(f"Error en la paginación: {e}")
            break

except Exception as e:
    print(f"Error general: {e}")
finally:
    driver.quit()

