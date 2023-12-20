import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By


def processar_datas(data_inicio, data_fim):
    intervalo_meses = 5
    formato_data = "%Y-%m"
    data_inicio = datetime.strptime(data_inicio, formato_data)
    data_fim = datetime.strptime(data_fim, formato_data)
    datas_processadas = []

    while data_inicio < data_fim:
        proxima_data = data_inicio + relativedelta(months=intervalo_meses)
        if proxima_data < data_fim:
            datas_processadas.append((data_inicio.strftime(formato_data), proxima_data.strftime(formato_data)))
            data_inicio = proxima_data
        else:
            datas_processadas.append((data_inicio.strftime(formato_data), data_fim.strftime(formato_data)))
            break

    return datas_processadas

def verifica_paginacao(nav):
    elemento_paginacao = nav.find_elements(By.XPATH, '//a[contains(@href, "consultarNfseRecebida.php?pagina=")]')
    if len(elemento_paginacao) > 0:
        logging.info(f'Há paginação {len(elemento_paginacao)}')
    else: 
        logging.info(f'Há apenas uma página de notas para o período.')
    return len(elemento_paginacao) > 0