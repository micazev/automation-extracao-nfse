import time
import logging
from utils import retry_with_logging, write_recover_file
from navigation._2_select_date_range import select_date_range
from scripts.navegar_notas_periodo import navegar_notas_periodo
from navigation._1_insert_credentials import insert_credentials
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config.config import load_config_data, delete_old_captcha, configure_webdriver, processar_datas, load_recover_data

if __name__ == "__main__":
    try:
        delete_old_captcha()
        config_data = load_config_data()
        driver = configure_webdriver()
        recover_data = load_recover_data()

        if driver:
            try:
                logging.info("Início da automação")
                driver.get('https://nfse.campinas.sp.gov.br/NotaFiscal/acessoSistema.php')
                # Switch to the 'principal' frame - O site é encapsulado em um frame
                driver.switch_to.frame("principal")
                retry_with_logging(insert_credentials, driver, config_data['usuario'], config_data['senha'], config_data["captchaKey"])
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
                logging.info("Login efetuado com sucesso")

                if len(recover_data) > 0:
                    datas_processadas = processar_datas(recover_data['periodo'][1], config_data['dataFim'])
                else:
                    datas_processadas = processar_datas(config_data['dataInicio'], config_data['dataFim'])
                for periodo in datas_processadas:
                    logging.info(f"Início da extração do período: {periodo}")
                    write_recover_file("periodo", str(periodo))
                    retry_with_logging(select_date_range, driver, periodo)
                    retry_with_logging(navegar_notas_periodo, driver)
                    logging.info(f"Fim da extração do período: {periodo}")
                with open("config/recover.txt", 'w') as arquivo:
                    pass
            except Exception as e:
                logging.error(f"An error occurred: {e}")
            finally:
                driver.quit()
                logging.info("Operação finalizada.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        #limpar recovery data
        logging.info("Operação finalizada com sucesso.")
