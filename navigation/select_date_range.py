import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import select_dropdown

def select_date_range(nav, periodo):
    data_inicio, data_fim = periodo
    try:
        element = WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
        element.click()
        date_values = split_strings(data_inicio, data_fim)

        if date_values is not None:
            anoInicio, mesInicio, anoFinal, mesFinal = date_values
            insert_dates(nav, mesInicio, anoInicio, mesFinal, anoFinal)
            print(f"Navegação do período: {mesInicio}-{anoInicio} a {mesFinal}-{anoFinal}")

        else:
            logging.error("Error getting date values.")

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error on page loading: {e}")

def split_strings(data_inicio, data_fim):
    try:
        anoInicio, mesInicio = data_inicio.split('-')
        anoFinal, mesFinal = data_fim.split('-')
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

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error inserting dates: {e}")



