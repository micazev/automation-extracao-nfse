import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import select_dropdown, wait_and_fill

def select_date_range(nav, periodo):
    data_inicio, data_fim = periodo
    try:
        # Aguarda até que o elemento 'NFSe Recebidas' esteja visível e o seleciona
        elemento = WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
        elemento.click()
        
        # Divide as datas em partes (ano e mês)
        valores_datas = dividir_strings(data_inicio, data_fim)

        if valores_datas is not None:
            ano_inicio, mes_inicio, ano_final, mes_final = valores_datas
            # Insere as datas nos campos do formulário
            inserir_datas(nav, mes_inicio, ano_inicio, mes_final, ano_final)
            print(f"Navegação do período: {mes_inicio}-{ano_inicio} a {mes_final}-{ano_final}")

        else:
            logging.error("Erro ao obter valores de data.")

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Erro no carregamento da página: {e}")

def dividir_strings(data_inicio, data_fim):
    try:
        # Divide as strings das datas em partes (ano e mês)
        ano_inicio, mes_inicio = data_inicio.split('-')
        ano_final, mes_final = data_fim.split('-')
        return ano_inicio, mes_inicio, ano_final, mes_final
    except Exception as e:
        logging.error(f"Erro ao dividir strings: {e}")
        return None

def inserir_datas(nav, mes_inicial, ano_inicial, mes_final, ano_final):
    try:
        # Seleciona as opções nos dropdowns de mês e ano
        select_dropdown(nav, 'rMesCompetenciaCN', mes_inicial)
        select_dropdown(nav, 'rAnoCompetenciaCN', ano_inicial)
        select_dropdown(nav, 'rMesCompetenciaCN2', mes_final)
        select_dropdown(nav, 'rAnoCompetenciaCN2', ano_final)
        # Submete o formulário de consulta
        nav.find_element(By.ID, 'btnConsultar').send_keys(Keys.RETURN)

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Erro ao selecionar datas no dropdown. {e}")
