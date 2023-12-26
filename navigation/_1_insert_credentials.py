import sys
import logging
import urllib.request
import base64
from io import BytesIO
from PIL import Image
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
        # download_captcha(nav)
        captcha_image = nav.find_element(By.ID, "captcha_image")
        image_src = captcha_image.get_attribute("src")
        # captcha = automated_captcha(captchaKey, image_src)
        captcha = ""
        if captcha == "":
            captcha = input("Please enter the captcha manually: ")
        wait_and_fill(nav, By.ID, 'cap_text', captcha)
        time.sleep(5)
        nav.find_element(By.ID, 'btnEntrar').send_keys(Keys.RETURN)
        WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
        logging.info("login efetuado com sucesso.")
        
    except Exception as e:
        logging.error(f"Error inserting credentials.")
        sys.exit(1)

def download_captcha(nav):
    captcha_image = nav.find_element(By.ID, "captcha_image")
    # image_src = captcha_image.get_attribute("src")
    # urllib.request.urlretrieve(image_src, "config/captcha.png")
    screenshot_base64 = nav.get_screenshot_as_base64()
    image_data = base64.b64decode(screenshot_base64)
    image = Image.open(BytesIO(image_data))
    location = captcha_image.location
    size = captcha_image.size
    window_position = nav.execute_script("return window.screenLeft + ',' + window.screenTop;")
    window_left, window_top = map(int, window_position.split(','))
    adjusted_location = (location['x'] - window_left, location['y'] - window_top)
    captcha_image = image.crop((location['x'], location['y'], location['x'] + size['width'], adjusted_location['y'] + size['height']))
    captcha_image.save("config/captcha.png")

def automated_captcha(captchaKey, image_src):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(captchaKey)
    solver.set_soft_id(0)
    captcha_text = solver.solve_and_return_solution(image_src)
    if captcha_text != 0:
        logging.info(f"captcha text {captcha_text}")
    else:
        logging.error(f"task finished with error {solver.error_code}")
    return captcha_text


