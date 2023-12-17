# config.py
import os
from datetime import datetime
import logging

logs_folder = 'logs'
os.makedirs(logs_folder, exist_ok=True)
log_file_path = os.path.join(logs_folder, f'navigation_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO)

def get_log_file_path():
    return log_file_path
