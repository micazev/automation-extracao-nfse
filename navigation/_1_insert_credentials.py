import logging
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.imagecaptcha import *

from utils import wait_and_fill, retry_with_logging, is_window_open
from config.config import delete_old_captcha


def insert_credentials(nav, usuario, senha, chaveCaptcha):
    try:
        # Preenche os campos de usuário e senha
        wait_and_fill(nav, By.ID, 'rLogin', usuario)
        wait_and_fill(nav, By.ID, 'rSenha', senha)
        # Tenta baixar o captcha
        retry_with_logging(baixar_captcha, nav)
        # Resolve o captcha automaticamente
        captcha = resolver_captcha_automatizado(chaveCaptcha)

        # Descomente as linhas abaixo se quiser inserir o captcha manualmente
        # captcha = ""
        # if captcha == "":
        #     captcha = input("Por favor, insira o captcha manualmente: ")

        # Preenche o campo de texto do captcha
        wait_and_fill(nav, By.ID, 'cap_text', captcha)
        delete_old_captcha()

        # Submete o formulário de login
        nav.find_element(By.ID, 'btnEntrar').send_keys(Keys.RETURN)
        
    except:
        # Registra um erro em caso de falha no login
        logging.error(f"Erro no login.")
        raise

def baixar_captcha(nav):
    try:
        # Aguarda a presença do elemento da imagem do captcha
        imagem_captcha = WebDriverWait(nav, 10).until(
            EC.presence_of_element_located((By.ID, "captcha_image"))
        )
        # Captura a imagem do captcha e salva no arquivo
        dados_imagem_captcha = imagem_captcha.screenshot_as_png
        imagem = Image.open(BytesIO(dados_imagem_captcha))
        imagem.save("config/captcha.png")
    except:
        # Registra um erro em caso de falha ao baixar a imagem do captcha
        logging.error("Erro ao baixar imagem do captcha.")
        raise

def resolver_captcha_automatizado(chaveCaptcha):
    # Resolução via anti-captcha.com
    try:
        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key(chaveCaptcha)
        solver.set_soft_id(0)
        # Resolve o captcha e retorna o texto
        texto_captcha = solver.solve_and_return_solution("config/captcha.png")
    except Exception as e:
        # Registra um erro em caso de falha na resolução do captcha
        logging.error(f"Erro ao resolver o captcha: {e}")
        texto_captcha = None
        raise
    return texto_captcha
