import os
import json
import random
import logging
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from config.config import configure_webdriver

driver = configure_webdriver()

def is_window_open(driver):
    try:
        # Tenta alternar para a primeira janela encontrada
        WebDriverWait(driver, 2).until(EC.number_of_windows_to_be(1))
        return True
    except NoSuchWindowException:
        return False

def save_to_file(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except:
        logging.error(f"Erro ao escrever o arquivo {filename}")

def generate_random_number():
    return random.randint(2, 6)

def retry_with_logging(function, driver, *args, **kwargs):
    attempt = 0
    max_attempts = 3
    delay = 0
    while attempt < max_attempts:
        try:
            # Adiciona a verificação da janela antes de cada tentativa
            if not is_window_open(driver):
                # Se a janela não estiver aberta, reinicie a automação
                logging.info("Não janelas abertas.")
                driver = restart_automation(driver)
            
            return function(driver, *args, **kwargs)
        except Exception as e:
            logging.warning(f"Error on attempt {attempt + 1}: {str(e)}")
            attempt += 1
            if attempt < max_attempts:
                logging.info(f"{attempt} Retrying...")
                sleep(delay)
            else:
                logging.error("Max attempts reached. Unable to complete operation.")
                raise Exception("Erro. Tentativas esgotadas.")

def wait_and_click(nav, by, value):
    try:
        element = WebDriverWait(nav, 3).until(EC.visibility_of_element_located((by, value)))
        element.click()
        return True
    except Exception as e:
        logging.error(f"Error clicking on {by}: {value}: {e}")
        return False

def select_dropdown(nav, control_id, value):
    try:
        drop_down_select = Select(nav.find_element(By.ID, f'{control_id}'))
        drop_down_select.select_by_visible_text(value)
    except NoSuchElementException as e:
        logging.error(f"Error selecting dropdown {control_id}: {e}")

def find_page(nav, url_pattern, url_atual):
    try:
        if url_pattern not in url_atual:
            # nav.close()
            abas = nav.window_handles
            for aba in abas:
                nav.switch_to.window(aba)
                if url_atual != nav.current_url:
                    return False
                else:
                    return True
        else:
            return True
    except:
        logging.error("A página desejada não foi encontrada.")
        return False

def wait_and_fill(nav, by, identifier, value):
    element = WebDriverWait(nav, 10).until(EC.visibility_of_element_located((by, identifier)))
    element.clear()
    element.send_keys(value)

def write_recover_file(label, data):
    file_path = "config/recover.json"
    
    # Check if the file exists or is empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        except json.JSONDecodeError:
            # Handle the case when the file is not in valid JSON format
            existing_data = {}
    else:
        existing_data = {}

    # Update the existing data with the new label and data
    existing_data[label] = data

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=2)

def restart_automation(driver):
    # Adicione aqui as operações necessárias para reiniciar a automação, como abrir a janela, fazer login, etc.
    logging.info("Restarting automation...")
    driver.quit()  # Fecha o WebDriver atual
    driver = configure_webdriver()  # Configura um novo WebDriver
    return driver

def retry_with_logging(function, *args, **kwargs):
    attempt = 0
    max_attempts = 3
    delay = 0
    while attempt < max_attempts:
        try:
            if is_window_open(driver):
                return function(*args, **kwargs)
            else:
                logging.info("Window is not open. Restarting automation...")
                # Adicione aqui a lógica para reabrir a janela e fazer o login novamente, se necessário
        except Exception as e:
            logging.warning(f"Error on attempt {attempt + 1}: {str(e)}")
            attempt += 1
            if attempt < max_attempts:
                logging.info(f"{attempt} Retrying...")
                sleep(delay)
            else:
                logging.error("Max attempts reached. Unable to complete operation.")
                raise Exception("Erro. Tentativas esgotadas.")
