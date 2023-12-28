import logging
from navigation._3_verifica_notas import verifica_notas
from scripts.navegar_pagina import navegar_pagina 
from scripts.verifica_paginacao import verifica_paginacao
from config import load_recover_data

def navegar_notas_periodo(driver):
    notas_processadas = []
    nota_numbers = verifica_notas(driver)
    notas_processadas = navegar_pagina(driver, nota_numbers)
    i = 2
    if notas_processadas == nota_numbers:
        logging.info("todas as notas foram processadas.")
    else:
        notas_nao_processadas = [nota for nota in nota_numbers if nota not in notas_processadas]
        logging.info(f"Nem todas as  as notas foram processadas. Notas não processadas: {notas_nao_processadas}")

    while verifica_paginacao(driver):
        logging.info(f"Processando página {i}")
        if notas_processadas != nota_numbers:
            notas_processadas = []
            notas_processadas = navegar_pagina(driver, nota_numbers)
            i =+ 1
        else:
            logging.info("As notas dessa página já foram processadas.")
            break