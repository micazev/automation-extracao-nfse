import sys
import time
import json
import random
import logging
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import json
import os

def save_to_file(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except:
        logging.error(f"Erro ao escrever o arquivo {filename}")

def write_recover_file(label, data):
    file_path = "config/recover.json"

    # Carrega os dados existentes, se o arquivo existir
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Procura por um objeto existente com a mesma label e o atualiza ou adiciona um novo
    found = False
    for entry in existing_data:
        if entry.get("label") == label:
            entry["data"] = data
            found = True
            break

    if not found:
        # Se a label não foi encontrada, adiciona um novo objeto ao final da lista
        entry = {"label": label, "data": data}
        existing_data.append(entry)

    # Escreve todos os dados no arquivo
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file)

def generate_random_number():
    return random.randint(2, 6)

def retry_with_logging(function, *args, **kwargs):
    attempt = 0
    max_attempts = 3
    delay= 0
    while attempt < max_attempts:
        try:
            return function(*args, **kwargs)
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