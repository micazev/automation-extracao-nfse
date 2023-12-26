import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from navigation._5_extract_nota_data import extract_nota_data
from utils import retry_with_logging, generate_random_number


def click_each_nfse(nav, nota_number):
    main_window = nav.current_window_handle
    nota_window_url_pattern = "NotaFiscal/notaFiscal.php?id_nota_fiscal="
    main_window_url_pattern = "https://nfse.campinas.sp.gov.br/NotaFiscal/index.php?"
    retry_with_logging(try_extract, nav, main_window, nota_number, main_window_url_pattern)

def try_extract(nav, main_window, nota_number, main_window_url_pattern):
    try:
        prosseguir = False
        dados_nao_extraidos = True
        while dados_nao_extraidos:
            rdm = generate_random_number()
            time.sleep(rdm)
            prosseguir = retry_with_logging(click_nota, nav, nota_number, main_window_url_pattern, main_window)
            if prosseguir:
                prosseguir = process_new_window(nav, main_window)
                if prosseguir:
                    url_atual = nav.current_url
                    dados_nao_extraidos = extract_nota_data(nav, nota_number, dados_nao_extraidos)
        nav.switch_to.window(main_window)
        nav.switch_to.frame("principal")
    except Exception as e:
        logging.error(f"Erro ao clicar em cada nota: {e}")


def click_nota(nav, nota_number, main_window_url_pattern, main_window):
    try:
        if main_window_url_pattern not in url_atual:
            nav.close()
            abas = nav.window_handles
            for aba in abas:
                nav.switch_to.window(aba)
                url_atual = nav.current_url
                if main_window_url_pattern in url_atual:
                    logging.info(f"Página principal encontrada.")
   
        else:
            logging.info("Já estou na página principal.")
        nav.switch_to.frame("principal")
        nav.find_element(By.XPATH, f'//a[b[text()="{nota_number}"]]').click()
        prosseguir = True

    except:
        logging.warning(f"Erro ao clicar na nota {nota_number}.")
        
        try:
            nota_link = nav.find_element(By.XPATH, f'//a[b[text()="{nota_number}"]]')
            nav.execute_script("arguments[0].click();", nota_link)
            prosseguir = True

        except:
            logging.error(f"Erro ao clicar no link da nota {nota_number}")
        
    return prosseguir

def process_new_window(nav, main_window):
    prosseguir = False
    try:
        WebDriverWait(nav, 2).until(EC.number_of_windows_to_be(2))  # Wait for two windows to be available
        window_handles = nav.window_handles
        new_window_handle = [handle for handle in window_handles if handle != main_window][0]
        nav.switch_to.window(new_window_handle)
        prosseguir = True

    except (TimeoutException, NoSuchElementException) as e:
        logging.error("Erro ao encontrar a janela, voltando a janela inicial.")
        for handle in nav.window_handles:
            if handle != main_window:
                logging.info("fechando janelas excedentes.")
                nav.switch_to.window(handle)
                nav.close()
        nav.switch_to.window(main_window)

    return prosseguir