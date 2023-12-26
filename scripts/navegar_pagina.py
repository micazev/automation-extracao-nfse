import logging 
from utils import write_recover_file

def navegar_pagina(driver, nota_numbers):
    from navigation._4_click_each_nfse import click_each_nfse
    notas_processadas = []

    for nota_number in nota_numbers:
        click_each_nfse(driver, nota_number)
        logging.info(f"Processada nota {nota_number}")
        notas_processadas.append(nota_number)
        # write_recover_file("nota_number",nota_number)
    return notas_processadas