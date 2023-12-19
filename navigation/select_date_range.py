import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from config.config import get_log_file_path

# Configure the logging
log_file_path = get_log_file_path()
logging.basicConfig(filename=log_file_path, level=logging.INFO)

def select_date_range(nav, dataInicio, dataFinal):
    try:
        element = WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
        element.click()
        date_values = split_strings(dataInicio, dataFinal)

        if date_values is not None:
            anoInicio, mesInicio, anoFinal, mesFinal = date_values
            print(anoInicio, mesInicio, anoFinal, mesFinal)
            insert_dates(nav, mesInicio, anoInicio, mesFinal, anoFinal)
        else:
            logging.error("Error getting date values.")

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error on page loading: {e}")


def split_strings(dataInicio, dataFinal):
    try:
        anoInicio, mesInicio = dataInicio.split('-')
        anoFinal, mesFinal = dataFinal.split('-')
        return anoInicio, mesInicio, anoFinal, mesFinal
    except Exception as e:
        logging.error(f"Error splitting strings: {e}")
        return None

def insert_dates(nav, initial_month, initial_year, final_month, final_year):
    try:
        logging.info("Start Filter Data Range and extraction")
        select_dropdown(nav, 'rMesCompetenciaCN', initial_month)
        select_dropdown(nav, 'rAnoCompetenciaCN', initial_year)
        select_dropdown(nav, 'rMesCompetenciaCN2', final_month)
        select_dropdown(nav, 'rAnoCompetenciaCN2', final_year)
        nav.find_element(By.ID, 'btnConsultar').send_keys(Keys.RETURN)
        
        # Wait for the "Nenhuma NFSe localizada" text to disappear
        WebDriverWait(nav, 10).until(
            EC.invisibility_of_element_located((By.XPATH, '//tr[@class="gridResultado1"]/td[contains(text(), "Nenhuma NFSe localizada.")]'))
        )

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error inserting dates and waiting: {e}")



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
