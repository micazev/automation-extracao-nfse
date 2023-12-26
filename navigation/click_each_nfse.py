from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from navigation.extract_nota_data import extract_nota_data
from navigation.extracao_pdf import extrair_dados_pdf
from utils import retry_with_logging
import logging

def click_each_nfse(nav, nota_number):
    main_window_url_pattern = "https://nfse.campinas.sp.gov.br/NotaFiscal/index.php?"
    nota_window_url_pattern = "NotaFiscal/notaFiscal.php?id_nota_fiscal="
    current_window = nav.current_window_handle

    try:
        nota_link = nav.find_element(By.XPATH, f'//a[b[text()="{nota_number}"]]')
        retry_with_logging(try_extract, nav, current_window, nota_window_url_pattern, nota_link, nota_number, main_window_url_pattern)

    except Exception as e:
        logging.error(f"Error in click_each_nfse: {e}")

def process_new_window(nav, current_window, nota_window_url_pattern):
    try:
        WebDriverWait(nav, 2).until(EC.number_of_windows_to_be(2))  # Wait for two windows to be available
        logging.info("duas janelas")
        window_handles = nav.window_handles
        new_window_handle = [handle for handle in window_handles if handle != current_window][0]
        logging.info("vai trocar de janela")
        nav.switch_to.window(new_window_handle)
        logging.info("trocou")

    except (TimeoutException, NoSuchElementException) as e:
        logging.info("Switching back to the main window.")
        nav.switch_to.window(current_window)

def click_nota(nav, nota_link):
    nav.execute_script("arguments[0].click();", nota_link)

def try_extract(nav, current_window, nota_window_url_pattern, nota_link, nota_number, main_window_url_pattern):

    retry_with_logging(click_nota, nav, nota_link)
    # Switch to the new window
    process_new_window(nav, current_window, nota_window_url_pattern)
    extract_nota_data(nav, nota_number)
    # extrair_dados_pdf(nav, nota_number)
    process_new_window(nav, current_window, main_window_url_pattern)
    # Switch to the 'principal' frame - o site é encapsulado em um frame
    nav.switch_to.frame("principal")

