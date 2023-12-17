# navigation/login.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

def insert_credentials(nav, username, password, captchaKey):
    try:
        wait_and_fill(nav, By.ID, 'rLogin', username)
        wait_and_fill(nav, By.ID, 'rSenha', password)

        # Ask the user to manually enter the captcha
        manual_captcha = input("Please enter the captcha manually: ")

        wait_and_fill(nav, By.ID, 'cap_text', manual_captcha)
        
        # Press Enter after filling the captcha
        nav.find_element(By.ID, 'btnEntrar').send_keys(Keys.RETURN)
        time.sleep(20)
        
        # Check if the 'NFSe Recebidas' link is visible, indicating successful login
        element = WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
        
        if element:
            element.click()
            logging.info("Login efetuado com sucesso.")
        else:
            logging.error("Erro no login.")

    except Exception as e:
        logging.error(f"Error inserting credentials: {e}")

def wait_and_fill(nav, by, identifier, value):
    element = WebDriverWait(nav, 10).until(EC.visibility_of_element_located((by, identifier)))
    element.clear()
    element.send_keys(value)

def wait_and_log(nav, by, identifier, timeout):
    WebDriverWait(nav, timeout).until(EC.visibility_of_element_located((by, identifier)))
