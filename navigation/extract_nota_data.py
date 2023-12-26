import json
import logging
from bs4 import BeautifulSoup


def extract_nota_data(nav, column_item_text, dados_nao_extraidos):
    combined_filename = f"extracts/nota_{column_item_text}.txt"
    logging.info("Início da extração de dados.")

    try:
        page_source = nav.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        target_text = "PRESTADOR DE SERVIÇOS"
        nota_text = "Número da Nota"

        labels_to_extract = ['Nome/Razão Social', 'CPF/CNPJ', 'Inscrição Municipal', 'Endereço', 'Município', 'UF', 'Telefone']
        labels_nota = ['Número da Nota', 'Data e Hora de Emissão', 'Código de Verificação']

        tables = soup.find_all('table', class_=['impressaoTabela', 'tamTab100'])

        tabela_prestador = next((table for table in tables if any(target_text in cell.get_text() for row in table.find_all('tr') for cell in row.find_all('td'))), None)
        tabela_nota = next((table for table in tables if any(nota_text in cell.get_text() for row in table.find_all('tr') for cell in row.find_all('td'))), None)

        extract_and_save_data(tabela_prestador, labels_to_extract, combined_filename, "prestador")
        extract_and_save_data(tabela_nota, labels_nota, combined_filename, "nota")
        dados_nao_extraidos =  False

    except Exception as e:
        logging.error(f"Erro ao extrair dados da nota. {e} - fechar e abrir a nota novamente.")

    finally:
        nav.close()
    return dados_nao_extraidos


def extract_and_save_data(table, labels_to_extract, combined_filename, data_type):
    try:
        data_dict = extract_data_from_table(table, labels_to_extract)
        save_to_file(data_dict, combined_filename, data_type)
    except Exception as e:
       logging.error(f"Table for {data_type} not found.")

def save_to_file(data, filename, data_type):
    with open(filename, 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write(f'\n{"="*20} {data_type.upper()} {"="*20}\n')

def extract_data_from_table(table, labels_to_extract):
    data_dict = {}

    cell_iterator = iter(table.find_all('td', class_='impressaoTitulo')) if len(labels_to_extract) == 3 else iter(table.find_all('td'))

    for cell in cell_iterator:
        cell_text = cell.get_text().strip()
        matching_label = next((label for label in labels_to_extract if cell_text.startswith(label)), None)
        if matching_label:
            value = cell_text[len(matching_label) + 1:].strip()
            data_dict[matching_label] = value

    return data_dict
