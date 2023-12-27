import re
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def verifica_notas(nav):
    # Wait for the "Nenhuma NFSe localizada" text to disappear
    notas_carregaram = WebDriverWait(nav, 5).until(
        EC.invisibility_of_element_located((By.XPATH, '//tr[@class="gridResultado1"]/td[contains(text(), "Nenhuma NFSe localizada.")]'))
    )
    # Se carregaram notas - primeira checagem
    if notas_carregaram:
        table_rows = nav.find_elements(By.XPATH, '//table[@border="0"]/tbody/tr[contains(@class, "gridResultado")]')
        row_count = len(table_rows)
        logging.info(f"Número de notas a serem processadas na página: {row_count}")

        # Se houver notas - checagem dupla
        if row_count > 0:
            nota_numbers = []
            for row in table_rows:
                nota_link = row.find_element(By.XPATH, './/td[@class="right"]/a[b]')
                WebDriverWait(nav, 2).until(lambda nav: nota_link.text.strip())
                nota_number = re.search(r'\b(\d+)\b', nota_link.find_element(By.TAG_NAME, 'b').text)
                if nota_number:
                    nota_numbers.append(nota_number.group(1))

        logging.info(f"Notas a serem processdas: {nota_numbers}")
    else:
        logging.info("Não há notas para o período.")
    return nota_numbers