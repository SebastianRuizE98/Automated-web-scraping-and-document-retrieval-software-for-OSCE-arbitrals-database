from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import pandas as pd
import time

# Inicializar el driver
driver = webdriver.Chrome()

def print_element_info(element, name):
    if element:
        print(f"{name} HTML: {element.get_attribute('outerHTML')}")
    else:
        print(f"{name} no encontrado.")

try:
    # Cargar la página
    url = "https://prodapp1.osce.gob.pe/sda-pub/documentos/public/busquedaArbitraje.xhtml"
    driver.get(url)

    datos_totales = []
    time.sleep(10)  # Esperar a que cargue la página

    # Esperar a que desaparezca el modal de carga
    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located((By.ID, "formBusqueda:windowprocesandoDialog_modal"))
    )

    # Seleccionar el año 2024
    campo_año = driver.find_element(By.XPATH, '//*[@id="formBusqueda:j_idt29:idAnioLaudo_label"]')
    campo_año.click()
    año_2024 = driver.find_element(By.XPATH, '//*[@id="formBusqueda:j_idt29:idAnioLaudo_panel"]/div/ul/li[3]')
    año_2024.click()

    # Clic en el botón de búsqueda
    boton_buscar = driver.find_element(By.XPATH, '//*[@id="formBusqueda:j_idt29:j_idt135"]/span[2]')
    print_element_info(boton_buscar, "Botón de búsqueda")  # Verificar si el botón es el correcto
    
    try:
        boton_buscar.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].scrollIntoView();", boton_buscar)
        boton_buscar.click()

        

    time.sleep(5)  # Esperar a que carguen los datos

    last_key_value = None  # Almacena el valor clave de la última página

    # Iterar en las páginas para extraer datos
    while True:
        try:
            # Esperar a que desaparezca el modal de carga
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "formBusqueda:windowprocesandoDialog_modal"))
            )

            tabla = driver.find_element(By.XPATH, '//*[@id="formBusqueda:j_idt29:tablaLaudos"]/div[2]')
            filas = tabla.find_elements(By.TAG_NAME, "tr")

            if len(filas) > 1:
                # Obtener la clave de la primera fila
                nueva_key_value = filas[1].find_elements(By.TAG_NAME, "td")[0].text
                print(f"Clave de primera fila: {nueva_key_value}")

                if nueva_key_value == last_key_value:
                    print("La clave no cambió, probablemente sea la última página.")
                    break
                last_key_value = nueva_key_value

                # Extraer los datos de la tabla
                for fila in filas[1:]:
                    celdas = fila.find_elements(By.TAG_NAME, "td")
                    datos_totales.append([celda.text for celda in celdas])

                print(f"Página procesada: {len(filas) - 1} filas.")

            else:
                print("No se encontraron filas de datos.")
                break

            # Intentar ir a la siguiente página
            siguiente_pagina_btn = driver.find_element(By.XPATH, '//*[@id="formBusqueda:j_idt29:tablaLaudos_paginator_bottom"]/span[5]/span')
            print_element_info(siguiente_pagina_btn, "Botón de siguiente página")  # Verificar si es el botón correcto
            
            try:
                siguiente_pagina_btn.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].scrollIntoView();", siguiente_pagina_btn)
                driver.execute_script("arguments[0].click();", siguiente_pagina_btn)

            time.sleep(5)  # Esperar carga de nueva página

        except (NoSuchElementException, TimeoutException) as e:
            print(f"No se pudo continuar: {e}")
            break

except NoSuchElementException:
    print("No se pudo encontrar la tabla de resultados.")

finally:
    # Guardar los datos en un archivo Excel
    df = pd.DataFrame(datos_totales)
    if df.empty:
        print("El DataFrame está vacío.")
    else:
        df.to_excel("resultados_arbitraje.xlsx", index=False)
        print("Datos guardados exitosamente en 'resultados_arbitraje.xlsx'")

    driver.quit()
