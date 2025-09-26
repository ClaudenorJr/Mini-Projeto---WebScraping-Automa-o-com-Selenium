import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

def slow_type(element, text, total_seconds_for_all_chars):
    if not text:
        return
    for ch in text:
        element.send_keys(ch)
        time.sleep(total_seconds_for_all_chars)

def instagram_bot(username, password, target_user, headless=False, total_seconds_typing=30):
    options = Options()
    options.add_argument("--start-maximized")
    if headless:
        options.headless = True

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        driver.get("https://www.instagram.com/")
        wait = WebDriverWait(driver, 20)

        user_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='username'], input[aria-label='Phone number, username, or email']")))
        pass_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='password'], input[aria-label='Password']")))

        total_chars = len(username) + len(password)
        per_char_delay = total_seconds_typing / total_chars if total_chars else 0

        # digitar username devagar
        user_input.clear()
        for ch in username:
            user_input.send_keys(ch)
            jitter = random.uniform(-0.2 * per_char_delay, 0.2 * per_char_delay)
            time.sleep(max(0, per_char_delay + jitter))

        # digitar senha devagar
        pass_input.clear()
        for ch in password:
            pass_input.send_keys(ch)
            jitter = random.uniform(-0.2 * per_char_delay, 0.2 * per_char_delay)
            time.sleep(max(0, per_char_delay + jitter))

        pass_input.send_keys(Keys.RETURN)

        # Tratar telas adicionais
        try:
            save_info_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(text(), 'Agora não') or contains(text(), 'Not Now') or contains(text(), 'Não agora')]")))
            save_info_btn.click()
        except:
            pass

        try:
            not_now_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(text(), 'Agora não') or contains(text(), 'Not Now') or contains(text(), 'Não agora')]")))
            not_now_btn.click()
        except:
            pass

        driver.get(f"https://www.instagram.com/{target_user}/")

        # Extrair bio
        try:
            bio_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='user-bio']")))
            bio_text = bio_element.text
        except:
            try:
                bio_element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span._ap3a:nth-child(1)")))
                bio_text = bio_element.text
            except:
                bio_text = ""

        # Salvar em JSON
        data = {"perfil": target_user, "bio": bio_text}
        with open("bio_instagram.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("✅ Bio salva em bio_instagram.json")

    finally:
        time.sleep(3)
        driver.quit()

# Função que o Main.py vai chamar
def run():
    print("=== Instagram Bot ===")
    username = input("Digite seu usuário do Instagram: ")
    password = input("Digite sua senha do Instagram: ")
    target_user = input("Digite o perfil alvo: ")
    headless = input("Rodar em modo headless? (s/n): ").lower() == 's'

    instagram_bot(username, password, target_user, headless=headless)

