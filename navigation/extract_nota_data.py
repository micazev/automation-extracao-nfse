from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import get_log_file_path
import logging
import time
import json

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def extract_nota_data(nav):
    try:
        # Extracting details from the nota fiscal details page
        page_source = nav.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extracting dados_da_nota
        nota_data = {}
        nota_data_elements = soup.find_all('td', {'class': ['impressaoLabel', 'impressaoTitulo']})

        for i in range(0, len(nota_data_elements), 2):
            if i + 1 < len(nota_data_elements):  # Check if the index is within the bounds
                label = nota_data_elements[i].text.strip()
                value = nota_data_elements[i + 1].text.strip()

                if label == 'Número da Nota' or label == 'Data e Hora de Emissão' or label == 'Código de Verificação':
                    nota_data[label] = value

        # Extracting dados_prestador
        prestador_data = {}
        prestador_table = soup.find('tbody', {'class': 'impressaoTabela tamTab100'})

        if prestador_table:
            prestador_rows = prestador_table.find_all('tr')
            for row in prestador_rows:
                label = row.find('td', {'class': 'impressaoLabel'})
                value = row.find('span', {'class': 'impressaoCampo'})
                if label and value:
                    prestador_data[label.text.strip()] = value.text.strip()

        # Merge nota_data and prestador_data
        combined_data = {**nota_data, **prestador_data}

        # Save combined_data to a file
        filename = f"extracts/nota_{nota_data['Número da Nota']}.json"
        save_to_file(combined_data, filename)
        logging.info(f"Dados da Nota e do Prestador saved to {filename}")

        return combined_data

    except Exception as e:
        logging.error(f"Error in extract_nota_data: {e}")
        return {}
