# main.py
import os
import json
import logging
from config.config import get_log_file_path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from navigation.login import insert_credentials
from navigation.select_date_range import select_date_range
from navigation.click_each_nfse import click_each_nfse

# Configure the logging
log_file_path = get_log_file_path()
logging.basicConfig(filename=log_file_path, level=logging.INFO)
# Load data from config.json
def load_config_data():
    config_dir = os.path.join(os.path.dirname(__file__), 'config')
    config_file_path = os.path.join(config_dir, 'input.json')
    with open(config_file_path, 'r') as json_file:
        return json.load(json_file)

# Configure webdriver
def configure_webdriver():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome()
        return driver
    except Exception as e:
        logging.error(f"Error configuring WebDriver: {e}")
        return None
    
# Main
if __name__ == "__main__":
    config_data = load_config_data()
    driver = configure_webdriver()

    if driver:
        try:
            logging.info("Início da automação")
            driver.get('https://nfse.campinas.sp.gov.br/NotaFiscal/acessoSistema.php')

            # Switch to the 'principal' frame - o site é encapsulado em um frame
            driver.switch_to.frame("principal")

            # Login
            insert_credentials(driver, config_data['usuario'], config_data['senha'], config_data["captchaKey"])

            # Filter data range
            select_date_range(driver, config_data['dataInicio'], config_data['dataFim'])

            # click each nfse
            click_each_nfse(driver)

        finally:
            driver.quit()
    else:
        logging.error("WebDriver not initialized. Exiting.")