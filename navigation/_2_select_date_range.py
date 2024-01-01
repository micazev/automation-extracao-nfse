import logging
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import select_dropdown, wait_and_fill

def select_date_range(nav, periodo):
    data_inicio, data_fim = periodo
    try:
        # Aguarda até que o elemento 'NFSe Recebidas' esteja visível e o seleciona
        elemento = WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NFSe Recebidas')))
        elemento.click()
        
        # Divide as datas em partes (ano e mês)
        valores_datas = dividir_strings(data_inicio, data_fim)

        if valores_datas is not None:
            ano_inicio, mes_inicio, ano_final, mes_final = valores_datas
            # Insere as datas nos campos do formulário
            inserir_datas(nav, mes_inicio, ano_inicio, mes_final, ano_final)
            print(f"Navegação do período: {mes_inicio}-{ano_inicio} a {mes_final}-{ano_final}")

        else:
            logging.error("Erro ao obter valores de data.")

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Erro no carregamento da página: {e}")

def dividir_strings(data_inicio, data_fim):
    try:
        # Divide as strings das datas em partes (ano e mês)
        ano_inicio, mes_inicio = data_inicio.split('-')
        ano_final, mes_final = data_fim.split('-')
        return ano_inicio, mes_inicio, ano_final, mes_final
    except Exception as e:
        logging.error(f"Erro ao dividir strings: {e}")
        return None

def inserir_datas(nav, mes_inicial, ano_inicial, mes_final, ano_final):
    try:
        # Seleciona as opções nos dropdowns de mês e ano
        select_dropdown(nav, 'rMesCompetenciaCN', mes_inicial)
        select_dropdown(nav, 'rAnoCompetenciaCN', ano_inicial)
        select_dropdown(nav, 'rMesCompetenciaCN2', mes_final)
        select_dropdown(nav, 'rAnoCompetenciaCN2', ano_final)
        # Submete o formulário de consulta
        nav.find_element(By.ID, 'btnConsultar').send_keys(Keys.RETURN)

    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Erro ao selecionar datas no dropdown. {e}")

def baixar_captcha(nav):
    try:
        # Aguarda a presença do elemento "captcha_image" e realiza o download da imagem
        captcha_image = WebDriverWait(nav, 10).until(
            EC.presence_of_element_located((By.ID, "captcha_image"))
        )
        captcha_image_data = captcha_image.screenshot_as_png
        image = Image.open(BytesIO(captcha_image_data))
        image.save("config/captcha.png")
    except:
        logging.error("Erro ao baixar imagem do captcha.")

def resolver_captcha_automatizado(captchaKey):
    try:
        # Cria um solver de captcha e tenta resolver a imagem
        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key(captchaKey)
        solver.set_soft_id(0)
        captcha_text = solver.solve_and_return_solution("config/captcha.png")
    except Exception as e:
        logging.error(f"Erro ao resolver o captcha: {e}")
        captcha_text = None
    return captcha_text

def inserir_credenciais(nav, usuario, senha, captchaKey):
    try:
        # Preenche os campos de usuário e senha
        wait_and_fill(nav, By.ID, 'rLogin', usuario)
        wait_and_fill(nav, By.ID, 'rSenha', senha)
        
        # Baixa a imagem do captcha e a resolve automaticamente
        retry_with_logging(baixar_captcha, nav)
        captcha = resolver_captcha_automatizado(captchaKey)

        # Preenche o campo de captcha com a solução obtida
        wait_and_fill(nav, By.ID, 'cap_text', captcha)
        nav.find_element(By.ID, 'btnEntrar').send_keys(Keys.RETURN)
        
    except:
        logging.error(f"Erro no login.")
