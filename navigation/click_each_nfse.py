from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from navigation.extract_nota_data import extract_nota_data
from bs4 import BeautifulSoup
import logging
import time
from selenium.webdriver.common.alert import Alert

# ... (your other imports)

def click_each_nfse(nav):
    current_window_title = None  

    try:
        table_rows = nav.find_elements(By.XPATH, '//table[@border="0"]/tbody/tr[contains(@class, "gridResultado")]')

        row_count = len(table_rows)
        logging.info(f"Number of nfse: {row_count}")

        # Get the main window handle
        main_window_handle = nav.current_window_handle

        # Iterate through each row and click on the first column item
        for row in table_rows:
            first_column_item = row.find_element(By.XPATH, './td[@align="left" and contains(@class, "right")]/a')
            first_column_item_text = first_column_item.text
            logging.info(f"Current Window Title: {current_window_title}")

            # Get the window handles before the click
            before_handles = nav.window_handles
            first_column_item.click()

            try:
                # Wait for the new window to appear
                WebDriverWait(nav, 10).until(
                    lambda driver: len(driver.window_handles) > len(before_handles)
                )

                # Get all window handles
                all_handles = nav.window_handles

                # Get the new window handle
                new_window_handle = list(set(all_handles) - set(before_handles))[0]

                # Switch to the new window
                nav.switch_to.window(new_window_handle)

                # Dismiss any alert that might be present
                try:
                    Alert(nav).dismiss()
                except:
                    pass  # Ignore if no alert is present

                # Perform actions on the new window (extract nota number, etc.)
                extract_nota_data(nav)

            except (TimeoutException, StaleElementReferenceException, NoSuchElementException) as e:
                logging.error(f"Error switching to new window: {e}")

            finally:
                current_window_title = nav.title
                logging.info(f"Current Window Title: {current_window_title}")

                logging.info(f"First Column Item Text: {first_column_item_text}")

                # Close the new window
                if len(nav.window_handles) > 1:
                    nav.close()

    except Exception as e:
        logging.error(f"Error in click_each_nfse: {e}")

    finally:
        try:
            # Check if the window is still open before switching back
            if current_window_title is not None:
                # Switch back to the main window
                nav.switch_to.window(main_window_handle)
                nav.switch_to.frame("principal")
                logging.info(f"Current Window Title: {current_window_title}")

                # Close the newly opened window
                if len(nav.window_handles) > 1:
                    nav.close()

        except Exception as e:
            logging.error(f"Error in finally block: {e}")
