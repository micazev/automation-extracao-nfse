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
        logging.info("Start Filter Data Range and extraction")
        wait_and_log(nav, "Waiting for the element to appear: CONSULTA DE NFSE RECEBIDAS")
        initial_month, initial_year, final_month, final_year = split_strings(dataInicio, dataFinal)
        print(anoInicio, mesInicio, anoFinal, mesFinal)
        insert_dates(nav, initial_month, initial_year, final_month, final_year)
        time.sleep(20)

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error on page loading: {e}")

def split_strings(dataInicio, dataFinal):
    try:
        global anoInicio, mesInicio, anoFinal, mesFinal
        anoInicio, mesInicio = dataInicio.split('-')
        anoFinal, mesFinal = dataFinal.split('-')
    except Exception as e:
        logging.error(f"Error splitting strings: {e}")

def wait_and_click(nav, by, value):
    try:
        element = WebDriverWait(nav, 3).until(EC.visibility_of_element_located((by, value)))
        element.click()
        time.sleep(3)  # Sleep for 3 seconds after clicking
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error waiting and clicking on {by}: {value}: {e}")

def wait_and_log(nav, message):
    try:
        element = nav.find_element(By.XPATH, "//td[normalize-space()='CONSULTA DE NFSE RECEBIDAS']")
        logging.info(element.text)
    except TimeoutException as e:
        logging.error(f"Error waiting and logging: {e}")

def insert_dates(nav, initial_month, initial_year, final_month, final_year):
    try:
        logging.info("insertion of dates")
        select_dropdown(nav, 'ControlID-1', initial_month)
        select_dropdown(nav, 'ControlID-2', initial_year)
        select_dropdown(nav, 'ControlID-3', final_month)
        select_dropdown(nav, 'ControlID-4', final_year)

        nav.find_element(By.ID, 'btnConsultar').send_keys(Keys.RETURN)
        time.sleep(3) 
        # Use WebDriverWait to wait for the results to load
        # WebDriverWait(nav, 10).until(EC.presence_of_element_located((By.XPATH, "//your/result/locator")))

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error inserting dates and waiting: {e}")

def select_dropdown(nav, control_id, value):
    try:
        drop_down_select = Select(nav.find_element(By.XPATH, f'//select[@control-id="{control_id}"]'))
        drop_down_select.select_by_visible_text(value)
    except NoSuchElementException as e:
        logging.error(f"Error selecting dropdown {control_id}: {e}")
