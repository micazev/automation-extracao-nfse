# main.py
import logging
from config.config import load_config_data, configure_webdriver
from navigation.login import insert_credentials
from navigation.select_date_range import select_date_range
from utils import processar_datas, retry_with_logging, abrir_notas
    
# Main
if __name__ == "__main__":
    try:
        config_data = load_config_data()
        driver = configure_webdriver()

        if driver:
            try:
                logging.info("Início da automação")
                driver.get('https://nfse.campinas.sp.gov.br/NotaFiscal/acessoSistema.php')

                # Switch to the 'principal' frame - o site é encapsulado em um frame
                driver.switch_to.frame("principal")
                # Login
                retry_with_logging(insert_credentials, driver, config_data['usuario'], config_data['senha'], config_data["captchaKey"])
                # time.sleep(800)
                datas = processar_datas(config_data['dataInicio'], config_data['dataFim'])
                
                for periodo in datas:
                    logging.info(f"Começando a extração do período: {periodo}")
                    data_inicio, data_fim = periodo
                    retry_with_logging(select_date_range, driver, data_inicio, data_fim)
                    retry_with_logging(abrir_notas, driver)
                    logging.info(f"Finalizada a extração do período: {periodo}")

            finally:
                driver.quit()
                logging.info("operação finalizada.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
