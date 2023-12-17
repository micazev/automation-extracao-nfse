# navigation/click_each_nfse.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
import time

def click_each_nfse(nav):
    try:
        # Switch to the main window
        main_window_handle = nav.window_handles[0]
        nav.switch_to.window(main_window_handle)

        # Locate the table rows
        table_rows = nav.find_elements(By.XPATH, '//table[@border="0"]/tbody/tr[contains(@class, "gridResultado")]')

        # Count the number of rows
        row_count = len(table_rows)
        print(f"Number of rows to click: {row_count}")
        logging.info(f"Number of rows to click: {row_count}")

        # Iterate through each row and click on the first column item
        for row in table_rows:
            first_column_item = row.find_element(By.XPATH, './td[@align="left" and contains(@class, "right")]/a')
            first_column_item_text = first_column_item.text
            first_column_item.click()
            time.sleep(50)
            nota_number = extract_nota_number(nav, first_column_item_text)

            # Perform actions on the details page
            # extract_nota_fiscal_details(nav, nota_number)

            # After processing the details page, close the current window and go back to the main table page
            nav.close()
            nav.switch_to.window(main_window_handle)

    except Exception as e:
        logging.error(f"Error in click_each_nfse: {e}")

def extract_nota_number(nav, item_text):
    try:
        # Extracting details from the nota fiscal details page
        page_source = nav.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the element with the specified class
        nota_element = soup.find('td', {'class': 'impressaoTitulo'})

        if nota_element:
            nota_value = nota_element.text.strip()
            print(f"Numero da Nota: {nota_value}")
            logging.info(f"Numero da Nota: {nota_value}")
        else:
            logging.warning("Element with class 'impressaoTitulo' not found.")

        return nota_value

    except Exception as e:
        logging.error(f"Error in extract_nota_fiscal_details: {e}")
