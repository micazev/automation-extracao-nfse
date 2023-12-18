from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import logging
import time

def click_each_nfse(nav):
    try:
        # Locate the table rows
        table_rows = nav.find_elements(By.XPATH, '//table[@border="0"]/tbody/tr[contains(@class, "gridResultado")]')

        # Count the number of rows
        row_count = len(table_rows)
        print(f"Number of rows to click: {row_count}")
        logging.info(f"Number of rows to click: {row_count}")

        # Get the main window handle
        main_window_handle = nav.current_window_handle

        # Iterate through each row and click on the first column item
        for row in table_rows:
            first_column_item = row.find_element(By.XPATH, './td[@align="left" and contains(@class, "right")]/a')
            first_column_item_text = first_column_item.text
            first_column_item.click()
            print("estou aqui!")
            time.sleep(5)

            try:
                # Wait for the new window to appear
                WebDriverWait(nav, 10).until(
                    lambda driver: len(driver.window_handles) > 1
                )

                # Switch to the new window
                new_window_handle = nav.window_handles[-1]
                nav.switch_to.window(new_window_handle)

                # Perform actions on the new window (extract nota number, etc.)
                extract_nota_number(nav, first_column_item_text)

            except (TimeoutException, StaleElementReferenceException, NoSuchElementException) as e:
                logging.error(f"Error switching to new window: {e}")
                # Handle any exception and continue with the next row

            finally:
                # Close the new window
                if len(nav.window_handles) > 1:
                    nav.close()

                # Switch back to the main window
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

    except Exception as e:
        logging.error(f"Error in extract_nota_fiscal_details: {e}")
