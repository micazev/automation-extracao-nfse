# main.py
import os
import json
import time
import logging 
from selenium.webdriver.common.by import By
from config.config import get_log_file_path, load_config_data, configure_webdriver
from selenium.webdriver.chrome.options import Options
from navigation.login import insert_credentials
from navigation.select_date_range import select_date_range
from navigation.click_each_nfse import click_each_nfse
from utils import processar_datas, verifica_paginacao
    
# Main
if __name__ == "__main__":
    try:
        print("Before loading config data")
        config_data = load_config_data()
        print("After loading config data")
        driver = configure_webdriver()
        print("After configuring webdriver")

        if driver:
            try:
                logging.info("Início da automação")
                driver.get('https://nfse.campinas.sp.gov.br/NotaFiscal/acessoSistema.php')

                # Switch to the 'principal' frame - o site é encapsulado em um frame
                driver.switch_to.frame("principal")

                # Login
                insert_credentials(driver, config_data['usuario'], config_data['senha'], config_data["captchaKey"])
                # time.sleep(800)
                datas = processar_datas(config_data['dataInicio'], config_data['dataFim'])
                for periodo in datas:
                    logging.info(periodo)
                    data_inicio, data_fim = periodo
                    select_date_range(driver, data_inicio, data_fim)
                    click_each_nfse(driver)
                    while verifica_paginacao(driver):
                        driver.find_element(By.XPATH, '//a[text()="Próximo"]').click()
                        click_each_nfse(driver)

            finally:
                driver.quit()
                logging.info("operação finalizada.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")
