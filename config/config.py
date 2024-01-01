# config.py
import os
import json 
import logging
from datetime import datetime
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options


logs_folder = 'logs'
os.makedirs(logs_folder, exist_ok=True)
log_file_path = os.path.join(logs_folder, f'navigation_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%H:%M:%S'
)

def get_log_file_path():
    return log_file_path

def load_config_data():
    config_file_path = os.path.join(os.path.dirname(__file__), 'input.json')
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as json_file:
            return json.load(json_file)
    else:
        return {}

def load_recover_data():
    file_path = "config/recover.json"
    if os.path.getsize(file_path) > 0:
        config_file_path = os.path.join(os.path.dirname(__file__), 'recover.json')
        with open(config_file_path, 'r') as json_file:
            return json.load(json_file)
    else:
        logging.info("Nada consta no arquivo de recuperação.")
    
def delete_old_captcha():
    try:
        os.remove("config/captcha.png")
    except:
        logging.warning(f"Erro ao deletar o arquivo de captcha.")

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

def processar_datas(data_inicio, data_fim):
    intervalo_meses = 3
    formato_data = "%Y-%m"
    data_inicio = datetime.strptime(data_inicio, formato_data)
    data_fim = datetime.strptime(data_fim, formato_data)
    
    datas_processadas = []

    while data_inicio < data_fim:
        proxima_data = data_inicio + timedelta(days=30 * intervalo_meses)
        
        if proxima_data < data_fim:
            datas_processadas.append((data_inicio.strftime(formato_data), proxima_data.strftime(formato_data)))
        else:
            datas_processadas.append((data_inicio.strftime(formato_data), data_fim.strftime(formato_data)))

        data_inicio = proxima_data

    return datas_processadas

def limpar_json():
    try:
        with open('config/recover.json', 'w') as file:
            json.dump({}, file, indent=2)
        print(f'O arquivo config/recover.json foi limpo com sucesso.')

    except Exception as e:
        print(f'Ocorreu um erro ao limpar o arquivo JSON: {e}')
