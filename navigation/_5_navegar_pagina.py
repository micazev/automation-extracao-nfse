import logging 
from utils import write_recover_file

def navegar_pagina(driver, nota_numbers, recover_nota_number):
    from navigation._6_click_each_nfse import click_each_nfse
    notas_processadas = []
    
    if recover_nota_number != "":
        logging.info(f"numero recuperado {recover_nota_number}")
        nota_number = recover_nota_number
        if nota_number in nota_numbers:
            index_nota_number = nota_numbers.index(nota_number)

            # Mover notas antes de nota_number para notas_processadas
            notas_processadas = nota_numbers[:index_nota_number].copy()
            logging.info(f"notas numbers {nota_numbers}")

            # Remover notas antes de nota_number de nota_numbers
            nota_numbers = nota_numbers[index_nota_number:]
            logging.info(f"notas que já tinham sido processadas {notas_processadas}")
            logging.info(f"notas numbers {nota_numbers} agora")

    for nota_number in nota_numbers:
        click_each_nfse(driver, nota_number)
        logging.info(f"Processada nota {nota_number}")
        notas_processadas.append(nota_number)
        write_recover_file("nota_number", nota_number)
    return notas_processadas