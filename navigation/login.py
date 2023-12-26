# navigation/login.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
import logging


def insert_credentials(nav, username, password, captchaKey):
    try:
        wait_and_fill(nav, By.ID, 'rLogin', username)
        wait_and_fill(nav, By.ID, 'rSenha', password)

        captcha_image = nav.find_element(By.ID, "captcha_image")
        captcha = automated_captcha(captchaKey, captcha_image)  
        if captcha == "":
            captcha = input("Please enter the captcha manually: ")
        wait_and_fill(nav, By.ID, 'cap_text', captcha)
        nav.find_element(By.ID, 'btnEntrar').send_keys(Keys.RETURN)
        WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
        logging.info("login efetuado com sucesso.")
        
    except Exception as e:
        logging.error(f"Error inserting credentials.")
        box_mensagem = nav.find_element_by_class_name("colunaboxMensagemB")
        if box_mensagem:
            logging.error(box_mensagem.text)
        else:
            logging.error("Erro no Login, mas a página não exibe nenhum erro.")

def wait_and_log(nav, by, identifier, timeout):
    WebDriverWait(nav, timeout).until(EC.visibility_of_element_located((by, identifier)))

def automated_captcha(captchaKey, captcha_image):
    logging.info(f"Ativando o solucionador de captcha.")
    print(f"Ativando o solucionador de captcha.")
    solver = TwoCaptcha(captchaKey)
    
    try:
        captcha = solver.normal(captcha_image)
        logging.info(f"resultado 2captcha: {captcha}")
        return captcha
    except Exception as e:
        logging.error(f"Erro ao resolver o captcha automaticamente: {e}")
        print(f"Erro ao resolver o captcha automaticamente. Tente inserir manualmente.")
        return ""

def wait_and_fill(nav, by, identifier, value):
    element = WebDriverWait(nav, 10).until(EC.visibility_of_element_located((by, identifier)))
    element.clear()
    element.send_keys(value)
