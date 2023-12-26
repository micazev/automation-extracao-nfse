import logging
from utils import wait_and_click
from selenium.webdriver.common.by import By

def verifica_paginacao(nav):
    try:    
        wait_and_click(nav, By.XPATH, '//a[text()="Próximo"]')
        logging.info(f'Passando para a próxima página.')
        return True
    except:
        logging.info('Não há mais páginas para o período.')
        return False