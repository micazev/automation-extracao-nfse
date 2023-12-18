from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from navigation.extract_nota_data import extract_nota_data
from bs4 import BeautifulSoup
import logging
import time

def click_each_nfse(nav):
    try:
        # Locate the table rows
        table_rows = nav.find_elements(By.XPATH, '//table[@border="0"]/tbody/tr[contains(@class, "gridResultado")]')

        # Count the number of rows
        row_count = len(table_rows)
        logging.info(f"Number of nfse: {row_count}")

        # Get the main window handle
        main_window_handle = nav.current_window_handle

        # Iterate through each row and click on the first column item
        for row in table_rows:
            first_column_item = row.find_element(By.XPATH, './td[@align="left" and contains(@class, "right")]/a')
            first_column_item_text = first_column_item.text
            first_column_item.click()

            try:
                # Wait for the new window to appear
                WebDriverWait(nav, 10).until(
                    lambda driver: len(driver.window_handles) > 1
                )

                # Switch to the new window
                new_window_handle = nav.window_handles[-1]
                nav.switch_to.window(new_window_handle)

                # Perform actions on the new window (extract nota number, etc.)
                extract_nota_data(nav)

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
