from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from navigation.extract_nota_data import extract_nota_data
import logging
from bs4 import BeautifulSoup
import re


def process_new_window(nav, current_window, nota_window_url_pattern):
    try:
        WebDriverWait(nav, 10).until(EC.number_of_windows_to_be(2))  # Wait for two windows to be available
        window_handles = nav.window_handles
        new_window_handle = [handle for handle in window_handles if handle != current_window][0]
        nav.switch_to.window(new_window_handle)

        # Continue with the rest of your code for the new window

    except (TimeoutException, NoSuchElementException) as e:
        logging.info("Switching back to the main window.")
        nav.switch_to.window(current_window)

def click_each_nfse(nav):
    main_window_url_pattern = "https://nfse.campinas.sp.gov.br/NotaFiscal/index.php?"
    nota_window_url_pattern = "NotaFiscal/notaFiscal.php?id_nota_fiscal="

    try:
        table_rows = nav.find_elements(By.XPATH, '//table[@border="0"]/tbody/tr[contains(@class, "gridResultado")]')
        row_count = len(table_rows)
        logging.info(f"Number of nfse: {row_count}")

        current_window = nav.current_window_handle
        
        # Se houver notas
        if row_count > 0:
            nota_numbers = []
            for row in table_rows:
                nota_link = row.find_element(By.XPATH, './/td[@class="right"]/a[b]')
                nota_number = re.search(r'\b(\d+)\b', nota_link.find_element(By.TAG_NAME, 'b').text)
                if nota_number:
                    nota_numbers.append(nota_number.group(1))

            logging.info(f"Nota Numbers: {nota_numbers}")

            # Extrair dados de cada nota
            for nota_number in nota_numbers:
                logging.info(f"Processing nota {nota_number}")
                nota_link = nav.find_element(By.XPATH, f'//a[b[text()="{nota_number}"]]')
                max_attempts = 3
                attempt = 0
                while attempt < max_attempts:
                    try:
                        nav.execute_script("arguments[0].click();", nota_link)
                        # Switch to the new window
                        process_new_window(nav, current_window, nota_window_url_pattern)
                        extract_nota_data(nav, nota_number)
                        process_new_window(nav, current_window, main_window_url_pattern)
                        # Switch to the 'principal' frame - o site é encapsulado em um frame
                        nav.switch_to.frame("principal")
                        break
                    except Exception as e:
                        logging.warning(f"Erro na tentativa {attempt + 1}: {str(e)}")
                        attempt += 1
                        if attempt < max_attempts:
                            logging.info(f"{attempt} Tentativa de extrair dados.")
                        else:
                            logging.error("Dados da nota não foram extraídos após várias tentativas")


    except Exception as e:
        logging.error(f"Error in click_each_nfse: {e}")