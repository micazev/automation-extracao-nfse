import sys
import logging
from PIL import Image
from io import BytesIO
from utils import wait_and_fill
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from anticaptchaofficial.imagecaptcha import *


def insert_credentials(nav, username, password, captchaKey):
    try:
        wait_and_fill(nav, By.ID, 'rLogin', username)
        wait_and_fill(nav, By.ID, 'rSenha', password)
        
        download_captcha(nav)
        captcha = automated_captcha(captchaKey)

        # captcha = ""
        # if captcha == "":
        #     captcha = input("Please enter the captcha manually: ")

        wait_and_fill(nav, By.ID, 'cap_text', captcha)
        nav.find_element(By.ID, 'btnEntrar').send_keys(Keys.RETURN)
        WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
        logging.info("login efetuado com sucesso.")
        
    except Exception as e:
        logging.error(f"Error inserting credentials.")
        sys.exit(1)

def download_captcha(nav):
    captcha_image = WebDriverWait(nav, 10).until(
        EC.presence_of_element_located((By.ID, "captcha_image"))
    )
    captcha_image_data = captcha_image.screenshot_as_png
    image = Image.open(BytesIO(captcha_image_data))
    image.save("config/captcha.png")

def automated_captcha(captchaKey):
    try:
        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key(captchaKey)
        solver.set_soft_id(0)
        captcha_text = solver.solve_and_return_solution("config/captcha.png")
    except Exception as e:
        logging.error(f"Erro ao resolver o captcha: {e}")
        captcha_text = None
    return captcha_text


