from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from navigation.extract_nota_data import extract_nota_data
import logging
import time

def is_table_page(url):
    return "NotaFiscal/index.php?codCidIni=" in url

def is_data_extraction_page(url):
    return "NotaFiscal/notaFiscal.php?id_nota_fiscal=" in url

def click_each_nfse(nav):
    current_page_url = None  

    try:
        table_rows = nav.find_elements(By.XPATH, '//table[@border="0"]/tbody/tr[contains(@class, "gridResultado")]')

        row_count = len(table_rows)
        logging.info(f"Number of nfse: {row_count}")

        # Get the main page URL
        main_page_url = nav.current_url

        # Iterate through each row and click on the first column item
        for row in table_rows:
            first_column_item = row.find_element(By.XPATH, './td[@align="left" and contains(@class, "right")]/a')
            first_column_item_text = first_column_item.text
            logging.info(f"Current Page URL: {current_page_url}")

            # Get the page URL before the click
            before_url = nav.current_url
            first_column_item.click()

            try:
                # Wait for the new window to appear
                WebDriverWait(nav, 10).until(
                    lambda driver: driver.current_url != before_url
                )

                # Print information about the page URL
                print(f"Current Page URL: {nav.current_url}")

                # Perform actions on the new page (extract nota number, etc.)
                if is_data_extraction_page(nav.current_url):
                    extract_nota_data(nav)

            except (TimeoutException, StaleElementReferenceException, NoSuchElementException) as e:
                logging.error(f"Error switching to new page: {e}")

            finally:
                current_page_url = nav.current_url
                logging.info(f"Current Page URL: {current_page_url}")

                logging.info(f"First Column Item Text: {first_column_item_text}")

                # Close the new window
                if is_data_extraction_page(nav.current_url):
                    nav.back()

    except Exception as e:
        logging.error(f"Error in click_each_nfse: {e}")

    finally:
        try:
            # Check if the window is still open before switching back
            if current_page_url is not None:
                # Switch back to the main page
                nav.get(main_page_url)
                nav.switch_to.frame("principal")
                logging.info(f"Current Page URL: {current_page_url}")

        except Exception as e:
            logging.error(f"Error in finally block: {e}")