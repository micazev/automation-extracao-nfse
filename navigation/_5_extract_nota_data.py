import os
import time
import logging
from bs4 import BeautifulSoup
from utils import save_to_file
from selenium.webdriver.common.by import By


def extract_nota_data(nav, nota_number, extrair_dados):
    filename = f"extracts/nota_{nota_number}.txt"
    if os.path.exists(filename):
        os.remove(filename)
    try:
        # Dados Prestador
        target_prestador = "PRESTADOR DE SERVIÇOS"
        labels_prestador = ['Nome/Razão Social', 'CPF/CNPJ', 'Inscrição Municipal', 'Endereço', 'Município', 'UF', 'Telefone']
        extract_and_save(nav, "prestador", target_prestador, labels_prestador, filename)

        # Dados da nota
        target_nota = "Número da Nota"
        labels_nota = ['Número da Nota', 'Data e Hora de Emissão', 'Código de Verificação']
        extract_and_save(nav, "nota", target_nota, labels_nota, filename)
        extrair_dados =  False

    except Exception as e:
        logging.error(f"Erro ao extrair dados da nota. {e} - fechar e abrir a nota novamente.")

    finally:
        nav.close()
    return extrair_dados

def extract_and_save(nav, data_type, target, labels, filename):
    try:
        page_source = nav.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        tables = soup.find_all('table', class_=['impressaoTabela', 'tamTab100'])

        if data_type == "prestador":
            tabela_prestador = next((table for table in tables if any(target in cell.get_text() for row in table.find_all('tr') for cell in row.find_all('td'))), None)
            extracted_data = extract_prestador(tabela_prestador, labels)
        else:
            extracted_data = extract_nota(tables, target, labels)

    except Exception as e:
       logging.error(f"Table for {data_type} not found.")
    finally:
        save_to_file(extracted_data, filename)

def extract_prestador(table, labels_to_extract):
    extracted_data = {}

    cell_iterator = iter(table.find_all('td', class_='impressaoTitulo')) if len(labels_to_extract) == 3 else iter(table.find_all('td'))

    for cell in cell_iterator:
        cell_text = cell.get_text().strip()
        matching_label = next((label for label in labels_to_extract if cell_text.startswith(label)), None)
        if matching_label:
            value = cell_text[len(matching_label) + 1:].strip()
            extracted_data[matching_label] = value
    return extracted_data

def extract_nota(driver, target_nota, labels_nota):
    extracted_data = {}

    # Encontrar a tabela que contém target_nota
    target_table = None
    for table in driver.find_elements(By.TAG_NAME, 'table'):
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            cells = row.find_elements(By.TAG_NAME, 'td')

            # Verificar se há pelo menos dois elementos (rótulo e valor)
            if len(cells) >= 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()

                # Verificar se o rótulo está na lista de labels desejados
                if target_nota in label:
                    target_table = table
                    break

    if target_table:
        for row in target_table.find_elements(By.TAG_NAME, 'tr'):
            cells = row.find_elements(By.TAG_NAME, 'td')

            if len(cells) >= 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()

                if label in labels_nota:
                    extracted_data[label] = value

    print(f"dados do nota {extracted_data}")
    time.sleep(1200)
    return extracted_data

