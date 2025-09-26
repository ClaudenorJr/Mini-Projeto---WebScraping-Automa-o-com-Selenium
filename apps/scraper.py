from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
import json
import time

G1_URL = "https://g1.globo.com/"
OUTPUT_FILENAME = "manchetes.json"

def extrair_manchetes(url: str, num_scrolls: int = 5, delay: int = 3) -> list[dict[str, str]]:
    driver = None
    manchetes = []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")

    try:
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        driver.set_page_load_timeout(30)
        driver.get(url)

        print(f"-> Rolando a página {num_scrolls} vezes com {delay}s de espera...")
        for _ in range(num_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)

        itens = driver.find_elements(By.CSS_SELECTOR, "a.feed-post-link")
        print(f"-> Encontrados {len(itens)} possíveis manchetes.")

        for item in itens:
            titulo = item.text.strip() or "Título não encontrado"
            link = item.get_attribute("href")
            if link:
                 manchetes.append({
                    "titulo": titulo,
                    "link": link
                 })

    except (WebDriverException, TimeoutException) as e:
        print(f"❌ Erro de WebDriver/Timeout durante a extração: {e}")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

    finally:
        if driver:
            driver.quit()

    return manchetes

def salvar_json(dados: list[dict[str, str]], nome_arquivo: str) -> None:
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"✅ {len(dados)} manchetes salvas em '{nome_arquivo}'.")
    except IOError as e:
        print(f"❌ Erro ao salvar arquivo '{nome_arquivo}': {e}")

# Função que o Main.py vai chamar
def run():
    print(f"Iniciando extração do {G1_URL} com Selenium...")
    
    # Pergunta ao usuário parâmetros opcionais
    try:
        num_scrolls = int(input("Quantas vezes rolar a página? [padrão=8]: ") or 8)
        delay = int(input("Segundos de espera entre scrolls? [padrão=4]: ") or 4)
    except ValueError:
        num_scrolls = 8
        delay = 4

    manchetes = extrair_manchetes(G1_URL, num_scrolls=num_scrolls, delay=delay)

    if manchetes:
        salvar_json(manchetes, OUTPUT_FILENAME)
    else:
        print("🛑 Nenhuma manchete encontrada ou houve um erro grave na extração.")
