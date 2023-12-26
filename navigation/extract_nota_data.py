from bs4 import BeautifulSoup
import logging
import json


def save_to_file(data, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write('\n') 

def extract_data_from_table(table, labels_to_extract):
    data_dict = {}

    if len(labels_to_extract) == 3:
        cell_iterator = iter(table.find_all('td', class_='impressaoTitulo'))
        for cell in cell_iterator:
            cell_text = cell.get_text().strip()
            matching_label = next((label for label in labels_to_extract if cell_text.startswith(label)), None)
            if matching_label:
                value = cell_text[len(matching_label) + 1:].strip()
                data_dict[matching_label] = value

    else:
        cell_iterator = iter(table.find_all('td'))
        for cell in cell_iterator:
            cell_text = cell.get_text().strip()

            # Find a matching label from labels_to_extract
            matching_label = next((label for label in labels_to_extract if cell_text.startswith(label)), None)

            if matching_label:
                value = cell_text[len(matching_label) + 1:].strip()
                data_dict[matching_label] = value

    return data_dict


def extract_nota_data(nav, column_item_text):
    combined_filename = f"extracts/nota_{column_item_text}.txt"

    try:
        # Extracting details from the nota fiscal details page
        page_source = nav.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        target_text = "PRESTADOR DE SERVIÇOS"
        nota_text = "Número da Nota"

        labels_to_extract = ['Nome/Razão Social', 'CPF/CNPJ', 'Inscrição Municipal', 'Endereço', 'Município', 'UF', 'Telefone']
        labels_nota = ['Número da Nota', 'Data e Hora de Emissão', 'Código de Verificação']

        tables = soup.find_all('table', class_=['impressaoTabela', 'tamTab100'])

        try:
            tabela_prestador = next((table for table in tables if any(target_text in cell.get_text() for row in table.find_all('tr') for cell in row.find_all('td'))), None)

            data_dict_prestador = extract_data_from_table(tabela_prestador, labels_to_extract)
            save_to_file(data_dict_prestador, combined_filename)
        except:
            logging.error(f"erro ao extrair os dados do prestador: {e}")

        try:
            tabela_nota = next((table for table in tables if any(nota_text in cell.get_text() for row in table.find_all('tr') for cell in row.find_all('td'))), None)

            data_dict_nota = extract_data_from_table(tabela_nota, labels_nota)
            save_to_file(data_dict_nota, combined_filename)
        except:
            logging.error(f"erro ao extrair os dados da nota: {e}")

    except Exception as e:
        logging.error(f"Error in extract_nota_data: {e}")

    finally:
        nav.close()
