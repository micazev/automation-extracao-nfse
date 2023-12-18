from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import get_log_file_path
import logging
import logging
import time

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
        prestador_elements = soup.find('tbody', {'class': 'impressaoTabela tamTab100'})

        if prestador_elements:
            prestador_data['dados_prestador'] = str(prestador_elements)

        # Print extracted data on the console
        print("Dados da Nota:")
        print(nota_data)

        print("\nDados do Prestador:")
        print(prestador_data)

        return nota_data, prestador_data

    except Exception as e:
        logging.error(f"Error in extract_nota_data: {e}")
        return {}, {}
