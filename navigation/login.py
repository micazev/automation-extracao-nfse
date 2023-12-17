import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from twocaptcha import TwoCaptcha
from config.config import get_log_file_path
import time

# Use the log file path
log_path = get_log_file_path()
print(f"Log file path: {log_path}")

# Configure the logging
log_file_path = get_log_file_path()
logging.basicConfig(filename=log_file_path, level=logging.INFO)

def login_with_captcha(nav, username, password, captcha_key, manual_captcha=None):
    try:
        logging.info("estou aqui")
        insert_credentials(nav, username, password)
        # captcha_code = solve_captcha(nav, captcha_key, 'path/to/captcha/image.png', manual_captcha)

        # if not captcha_code:
        #     logging.warning("Captcha solving failed.")

    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error during login: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        nav.quit()

def insert_credentials(nav, username, password):
    try:
        element = WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.ID, 'rLogin')))
        element.clear()
        element.send_keys(username)
        time.sleep(2)

        password_element = nav.find_element(By.ID, 'rSenha')
        password_element.clear()
        password_element.send_keys(password)
        time.sleep(2)
    except Exception as e:
        logging.error(f"Error inserting credentials: {e}")

def solve_captcha(nav, api_key, captcha_image_path, manual_captcha=None):
    solver = TwoCaptcha(api_key)
    try:
        result = None

        # Captcha solving
        if manual_captcha:
            captcha_solution = manual_captcha
        else:
            # If manual_captcha is not provided, prompt the user to manually enter captcha
            manual_captcha = print("Please enter the captcha manually: ")
            captcha_solution = manual_captcha.strip()

        if captcha_solution:
            # Set the captcha result in the input field
            cap_text_input = nav.find_element(By.ID, 'cap_text')
            cap_text_input.clear()
            cap_text_input.send_keys(captcha_solution)

            nav.find_element(By.ID, 'btnEntrar').send_keys(Keys.RETURN)
            WebDriverWait(nav, 30).until(EC.presence_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
            logging.info("Login efetuado com sucesso.")

            result = solver.normal(captcha_image_path)

        return result['code'] if result else None

    except Exception as e:
        logging.error(f"Error solving captcha: {e}")
        return None
