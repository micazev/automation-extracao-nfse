import os
import time
import logging
from bs4 import BeautifulSoup
from utils import save_to_file

def extract_nota_data(nav, nota_number, extrair_dados):
    filename = f"extracts/nota_{nota_number}.txt"
    if os.path.exists(filename):
        os.remove(filename)
    
    try:
        page_source = nav.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        tables = soup.find_all('table', class_=['impressaoTabela', 'tamTab100'])
        extracted_data = {}

        # Dados Prestador
        labels_prestador = ['Nome/Razão Social', 'CPF/CNPJ', 'Inscrição Municipal', 'Endereço', 'Município', 'UF', 'Telefone']
        tabela_prestador = tables[4]
        prestador_data = extract_prestador(tabela_prestador, labels_prestador)
        extracted_data.update(prestador_data)

        # Dados da nota
        labels_nota = ['Número da Nota', 'Data e Hora de Emissão', 'Código de Verificação']
        tabela_nota = tables[3]
        print("estou aqui")
        nota_data = extract_nota(tabela_nota, labels_nota)
        extracted_data.update(nota_data)
        print(nota_data)

        save_to_file(extracted_data, filename)
        extrair_dados =  False

    except Exception as e:
        logging.error(f"Erro ao extrair dados. {e} - Fechar e abrir a nota novamente.")

    finally:
        nav.close()
    return extrair_dados

def extract_prestador(table, labels_to_extract):
    prestador_data = {}

    cell_iterator = iter(table.find_all('td', class_='impressaoTitulo')) if len(labels_to_extract) == 3 else iter(table.find_all('td'))

    for cell in cell_iterator:
        cell_text = cell.get_text().strip()
        matching_label = next((label for label in labels_to_extract if cell_text.startswith(label)), None)
        if matching_label:
            value = cell_text[len(matching_label) + 1:].strip()
            prestador_data[matching_label] = value
    return prestador_data

def extract_nota(tabela_nota, labels_nota):
    nota_data = {}
    print("estou aqui")
    linhas_tabela = tabela_nota.find_all('tr')
    print(f"linhas tabela {linhas_tabela}")
    for i in range(0, len(linhas_tabela), 2):
        chave = linhas_tabela[i].text.strip()
        valor = linhas_tabela[i + 1].text.strip()
        nota_data[chave] = valor
    print(f"nota data {nota_data}")
    time.sleep(1200)
    return nota_data

