from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
import json

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write('\n') 

def extract_nota_data(nav, column_item_text):
    combined_data = {}  # Initialize a dictionary to store the extracted data

    try:
        # Wait until the element is present on the page
        # nota_data_element_present = EC.presence_of_element_located((By.XPATH, '//td[@class="impressaoLabel" and text()="Número da Nota"]'))
        # WebDriverWait(nav, 10).until(nota_data_element_present)

        # Extracting details from the nota fiscal details page
        page_source = nav.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        labels_to_extract = ['Número da Nota', 'Data e Hora de Emissão', 'Código de Verificação',
                             'Nome/Razão Social', 'CPF/CNPJ', 'Inscrição Municipal',
                             'Endereço', 'Município', 'UF', 'Telefone']

        for label in labels_to_extract:
            logging.info(label)
            label_element = soup.find('td', class_='impressaoLabel', string=lambda text: label in text)
            logging.info(label_element)
            if label_element:
                logging.info("checando td")
                # Find the next sibling <td> with the class 'impressaoTitulo' within the same <tr>
                data_element = label_element.find_next('td', class_='impressaoTitulo')
                if not data_element:
                    logging.info("checando span")
                    # If not found, try finding the value within the same <tr>
                    data_element = label_element.find_next('span', class_='impressaoCampo')
                if data_element:
                    data_value = data_element.text.strip()
                    combined_data[label] = data_value
                else:
                    # If neither is found, try finding a <span> inside the current <td> with class 'impressaoCampo'
                    span_element = label_element.find('span', class_='impressaoCampo')
                    if span_element:
                        data_value = span_element.text.strip()
                        combined_data[label] = data_value
                    else:
                        # If neither <td class='impressaoTitulo'> nor <span class='impressaoCampo'> is found, set data_value to None
                        combined_data[label] = None

    except Exception as e:
        logging.error(f"Error in extract_nota_data: {e}")
        return {}

    finally:
        # Save extracted data for each label
        combined_filename = f"extracts/nota_{column_item_text}.txt"
        save_to_file(combined_data, combined_filename)
        logging.info(f"All data saved to {combined_filename}")
        nav.close()
