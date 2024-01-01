import logging
from navigation._3_verifica_notas import verifica_notas_na_pagina
from navigation._5_navegar_pagina import navegar_pagina 
from utils import wait_and_click
from selenium.webdriver.common.by import By

def navegar_notas_periodo(nav, recover_nota_number): 
    notas_processadas = []
    nota_numbers = verifica_notas_na_pagina(nav)
    notas_processadas = navegar_pagina(nav, nota_numbers, recover_nota_number)
    recover_nota_number = ""
    i = 2
    if notas_processadas == nota_numbers:
        logging.info("todas as notas da página foram processadas.")
    else:
        notas_nao_processadas = [nota for nota in nota_numbers if nota not in notas_processadas]
        logging.info(f"Nem todas as  as notas foram processadas. Notas não processadas: {notas_nao_processadas}. Tentando processar eles novamente:")

    while verifica_paginacao(nav):
        logging.info(f"Processando página {i}")
        if notas_processadas != nota_numbers:
            notas_processadas = []
            notas_processadas = navegar_pagina(nav, nota_numbers, recover_nota_number)
            i =+ 1
        else:
            logging.info("As notas dessa página já foram processadas.")
            break

def verifica_paginacao(nav):
    try:    
        wait_and_click(nav, By.XPATH, '//a[text()="Próximo"]')
        logging.info(f'Passando para a próxima página.')
        return True
    except:
        logging.info('Não há mais páginas para o período ou elemento de passar a página não encontrado.')
        return False