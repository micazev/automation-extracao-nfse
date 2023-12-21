# config.py
import os
import json 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

logs_folder = 'logs'
os.makedirs(logs_folder, exist_ok=True)
log_file_path = os.path.join(logs_folder, f'navigation_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_log_file_path():
    return log_file_path

def load_config_data():
    config_file_path = os.path.join(os.path.dirname(__file__), 'input.json')
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
