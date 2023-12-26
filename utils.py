import logging
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import time


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
                raise  

def processar_datas(data_inicio, data_fim):
    intervalo_meses = 6
    formato_data = "%Y-%m"
    data_inicio = datetime.strptime(data_inicio, formato_data)
    data_fim = datetime.strptime(data_fim, formato_data)
    
    datas_processadas = []

    while data_inicio < data_fim:
        proxima_data = data_inicio + timedelta(days=30 * intervalo_meses)
        
        if proxima_data < data_fim:
            datas_processadas.append((data_inicio.strftime(formato_data), proxima_data.strftime(formato_data)))
        else:
            datas_processadas.append((data_inicio.strftime(formato_data), data_fim.strftime(formato_data)))

        data_inicio = proxima_data

    return datas_processadas

def verifica_paginacao(nav):
    try:    
        nav.find_element(By.XPATH, '//a[text()="Próximo"]').click()
        logging.info(f'Passando para a próxima página.')
        return True
    except:
        logging.info('Há apenas uma página de notas para o período.')
        return False

def navegar_notas_periodo(driver):
    nota_numbers = verifica_notas(driver)
    navegar_pagina(driver, nota_numbers)
    i = 2
    while verifica_paginacao(driver): # se houver, ele já clica
        logging.info(f"Processando página {i}")
        navegar_pagina(driver, nota_numbers)
        i =+ 1
    logging.info("")

def navegar_pagina(driver, nota_numbers):
    from navigation.click_each_nfse import click_each_nfse
    for nota_number in nota_numbers:
        logging.info(f"Processing nota {nota_number}")
        click_each_nfse(driver, nota_number)

def wait_and_click(nav, by, value):
    try:
        element = WebDriverWait(nav, 3).until(EC.visibility_of_element_located((by, value)))
        element.click()
        time.sleep(3)  # Sleep for 3 seconds after clicking
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error waiting and clicking on {by}: {value}: {e}")

def select_dropdown(nav, control_id, value):
    try:
        drop_down_select = Select(nav.find_element(By.ID, f'{control_id}'))
        drop_down_select.select_by_visible_text(value)
    except NoSuchElementException as e:
        logging.error(f"Error selecting dropdown {control_id}: {e}")

def verifica_notas(nav):
    # Wait for the "Nenhuma NFSe localizada" text to disappear
    notas_carregaram = WebDriverWait(nav, 5).until(
        EC.invisibility_of_element_located((By.XPATH, '//tr[@class="gridResultado1"]/td[contains(text(), "Nenhuma NFSe localizada.")]'))
    )
    # Se carregaram notas - primeira checagem
    if notas_carregaram:
        table_rows = nav.find_elements(By.XPATH, '//table[@border="0"]/tbody/tr[contains(@class, "gridResultado")]')
        row_count = len(table_rows)
        logging.info(f"Número de notas a serem processadas na página: {row_count}")

        # Se houver notas - checagem dupla
        if row_count > 0:
            nota_numbers = []
            for row in table_rows:
                nota_link = row.find_element(By.XPATH, './/td[@class="right"]/a[b]')
                WebDriverWait(nav, 2).until(lambda nav: nota_link.text.strip())
                nota_number = re.search(r'\b(\d+)\b', nota_link.find_element(By.TAG_NAME, 'b').text)
                if nota_number:
                    nota_numbers.append(nota_number.group(1))

        logging.info(f"Notas a serem processdas: {nota_numbers}")
    else:
        logging.info("Não há notas para o período.")
    return nota_numbers
