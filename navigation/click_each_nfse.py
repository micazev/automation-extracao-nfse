from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navigation.extract_nota_data import extract_nota_data
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# def switch_to_window_with_pattern(driver, url_pattern):
#     for handle in driver.window_handles:
#         driver.switch_to.window(handle)
#         if url_pattern in driver.current_url:
#             return True  # Encontrou a janela com o padrão desejado
#     return False  # Não encontrou nenhuma janela com o padrão
    
def switch_to_window_with_pattern(driver, url_pattern):
    while url_pattern not in driver.current_url:
            for window_handle in driver.window_handles:
                driver.switch_to.window(window_handle)

    for window_handle in driver.window_handles:
        driver.switch_to.window(window_handle)
        if url_pattern in driver.current_url:
            return True  # Encontrou a janela com o padrão desejado

    # Se não encontrar a janela, volta para a janela principal
    driver.switch_to.window(main_window_handle)
    driver.get(main_window_url)
    return False  # Não encontrou nenhuma janela com o padrão



def click_each_nfse(nav):
    main_window_url_pattern = "https://nfse.campinas.sp.gov.br/NotaFiscal/index.php?"
    nota_window_url_pattern = "NotaFiscal/notaFiscal.php?id_nota_fiscal="

    try:
        table_rows = nav.find_elements(By.XPATH, '//table[@border="0"]/tbody/tr[contains(@class, "gridResultado")]')
        row_count = len(table_rows)
        logging.info(f"Number of nfse: {row_count}")

        # Iterate through each row and click on the first column item
        for index, row in enumerate(table_rows, start=1):
            logging.info(f"Processing nota {index} of {row_count}")

            # Clica no link da nota
            column_item = row.find_element(By.XPATH, f'./td[@align="left" and contains(@class, "right")]/a[{index}]')
            column_item_text = column_item.text
            logging.info(f"Início extração da nota: {column_item_text}")
            column_item.click()

            # Verifica se a nova janela foi aberta
            try:
                switch_to_window_with_pattern(nav, nota_window_url_pattern)
                WebDriverWait(nav, 10).until(EC.url_contains(nota_window_url_pattern))
                extract_nota_data(nav, column_item_text)

            except (TimeoutException, NoSuchElementException) as e:
                logging.error(f"A janela da nota não foi encontrada. Error processing new window: {e}")

            finally:
                # if len(nav.window_handles) > 1:
                    # logging.info("fechando janelas excedentes.")
                #     nav.close()
                logging.info("voltando a janela principal.")
                switch_to_window_with_pattern(nav, main_window_url_pattern)
                WebDriverWait(nav, 10).until(EC.url_contains(main_window_url_pattern))
                logging.info("voltou.")


    except Exception as e:
        logging.error(f"Tabela não encontrada. Error in click_each_nfse: {e}")
