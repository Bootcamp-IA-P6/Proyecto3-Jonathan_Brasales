from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Para Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_website():
    # Configurar Selenium
    options = Options()
    options.add_argument('--headless=new')  # Ejecutar en modo headless (queremos ver que pasa)
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--no-sandbox')  # Requerido para algunos servidores
    #options.add_argument('--start-maximized')
    options.add_argument('--disable-dev-shm-usage')  # Para evitar errores de memoria
    options.add_argument("user-agent=WebscraperLearningBot/1.0 (learning purpose)")

    # 🔹 Aquí inicializamos correctamente `service` para navegador 
    #service = Service(ChromeDriverManager().install())

    # Para Chrome
    # Selenium Manager se encargará de descargar y gestionar el WebDriver
    service = Service()  # No es necesario especificar el ejecutable
    driver = webdriver.Chrome(service=service, options=options)

    # Navegar al sitio web
    url = "https://es.wikipedia.org/wiki/Wikipedia:Portada"
    driver.get(url)
    #time.sleep(3)   #Explícito aunque selenium ya espere

    print(driver.title)  

    # Esperar a que los elementos estén presentes
    try:

        bloque = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "main-potd"))
        )

        titulo = bloque.find_element(By.TAG_NAME, "h2").text #Siempre el mismo (Recurso del día)
        try:

            img = bloque.find_element(By.CSS_SELECTOR, "figure img")
            img_url = img.get_attribute("src")
            img_alt = img.get_attribute("alt")

        except Exception as e:
            print("Error al encontrar los elementos:", e)
            driver.quit()
            pass
        
        parrafos = bloque.find_elements(By.TAG_NAME, "p")
        texto = parrafos[-1].text

    
        return {
                "title": img_alt,
                "text": texto,
                "img_url": img_url,
                "source": "Wikipedia",
            }

    finally:
        driver.quit()
