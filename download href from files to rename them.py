from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

# Configurar Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# URL de la página
url = "https://prodapp1.osce.gob.pe/sda-pub/documentos/public/busquedaArbitraje.xhtml"
driver.get(url)

# Esperar a que desaparezca el modal de carga inicial
wait.until(EC.invisibility_of_element_located((By.ID, "formBusqueda:windowprocesandoDialog_modal")))

# Seleccionar el año 2024
campo_año = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formBusqueda:j_idt29:idAnioLaudo_label"]')))
campo_año.click()
año_2024 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formBusqueda:j_idt29:idAnioLaudo_panel"]/div/ul/li[3]')))
año_2024.click()

# Esperar que desaparezca el modal antes de buscar
wait.until(EC.invisibility_of_element_located((By.ID, "formBusqueda:windowprocesandoDialog_modal")))

# Clic en el botón de búsqueda
boton_buscar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formBusqueda:j_idt29:j_idt135"]/span[2]')))
driver.execute_script("arguments[0].click();", boton_buscar)

# Esperar a que carguen los resultados
wait.until(EC.invisibility_of_element_located((By.ID, "formBusqueda:windowprocesandoDialog_modal")))

# Diccionario para almacenar los datos
datos = {}

fila_global = 1  # Contador de filas global

while True:
    # Esperar a que la tabla esté disponible
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="formBusqueda:j_idt29:tablaLaudos_data"]')))
    
    # Obtener todas las filas de la tabla
    filas = driver.find_elements(By.XPATH, '//*[@id="formBusqueda:j_idt29:tablaLaudos_data"]/tr')

    for i in range(1, len(filas) + 1):
        try:
            boton_descarga = wait.until(EC.presence_of_element_located(
                (By.XPATH, f'//*[@id="formBusqueda:j_idt29:tablaLaudos_data"]/tr[{i}]/td[10]/a')
            ))
            
            # Obtener el href del botón de descarga
            href = boton_descarga.get_attribute("href")
            if href:
                match = re.search(r'/(\d+)_Documento', href)  # Extrae solo el número
                if match:
                    numero = match.group(1)
                    
                    # Guardar datos en diccionario
                    datos[fila_global] = numero

                    print(f"Fila {fila_global}: {numero}")
                    fila_global += 1  # Incrementar el contador global
        except Exception as e:
            print(f"Error procesando la fila {fila_global}: {e}")

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

# Cerrar el navegador
driver.quit()

print(datos)

# Ruta de la carpeta con los documentos
carpeta_docs = r"G:\Mi unidad\Proyectos\Lector de Docs de SEACE\DOCS LAUDOS"

# Recorrer los archivos en la carpeta
import os
for archivo in os.listdir(carpeta_docs):
    ruta_original = os.path.join(carpeta_docs, archivo)

    # Extraer el número inicial del nombre del archivo
    match = re.match(r"^(\d+)_", archivo)
    if match:
        numero_archivo = match.group(1)

        # Buscar si el número está en los valores del diccionario
        for clave, valor in datos.items():
            if valor == numero_archivo:
                # Nueva ruta con el nombre cambiado
                nuevo_nombre = f"{clave}.pdf"  # Asegura la extensión correcta
                ruta_nueva = os.path.join(carpeta_docs, nuevo_nombre)

                # Renombrar el archivo
                os.rename(ruta_original, ruta_nueva)
                print(f'Renombrado: "{archivo}" → "{nuevo_nombre}"')
                break  # Evita múltiples cambios en un mismo archivo