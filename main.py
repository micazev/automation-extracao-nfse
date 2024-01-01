import ast
import time
import logging
from utils import retry_with_logging, write_recover_file
from navigation._2_select_date_range import select_date_range
from navigation._4_navegar_notas_periodo import navegar_notas_periodo
from navigation._1_insert_credentials import insert_credentials
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config.config import load_config_data, configure_webdriver, processar_datas, load_recover_data, limpar_json

driver = None


if __name__ == "__main__":
    tentativas = 0
    max_tentativas = 3

    while tentativas < max_tentativas:
        try:
            config_data = load_config_data()
            driver = configure_webdriver()
            recover_data = load_recover_data()

            if recover_data and recover_data != "{}":
                recover_nota_number = recover_data['nota_number']
                data_inicio = ast.literal_eval(recover_data['periodo'])
                data_inicio = data_inicio[0]
            else:
                data_inicio = config_data['dataInicio']
                recover_nota_number = ""

            if driver:
                try:
                    logging.info("Início da automação")
                    driver.get('https://nfse.campinas.sp.gov.br/NotaFiscal/acessoSistema.php')
                    # Switch to the 'principal' frame - O site é encapsulado em um frame
                    driver.switch_to.frame("principal")
                    retry_with_logging(insert_credentials, driver, config_data['usuario'], config_data['senha'], config_data["captchaKey"])
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
                    logging.info("Login efetuado com sucesso")
                    logging.info(data_inicio)
                    datas_processadas = processar_datas(data_inicio, config_data['dataFim'])
                    for periodo in datas_processadas:
                        logging.info(f"Início da extração do período: {periodo}")
                        write_recover_file("periodo", str(periodo))
                        retry_with_logging(select_date_range, driver, periodo)
                        retry_with_logging(navegar_notas_periodo, driver, recover_nota_number)
                        logging.info(f"Fim da extração do período: {periodo}")
                    limpar_json()
                except Exception as e:
                    logging.error(f"An error occurred: {e}")
                finally:
                    driver.quit()
                    logging.info("Operação finalizada.")
            break  # Se chegar aqui sem exceção, saia do loop
        except Exception as e:
            logging.error(f"Tentativa {tentativas + 1} falhou. Erro: {e}")
            write_recover_file("nota_number", recover_nota_number)
            write_recover_file("periodo", str(periodo))
            tentativas += 1

    logging.info("Operação finalizada com sucesso.")
