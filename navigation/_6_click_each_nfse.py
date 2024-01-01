import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from navigation._7_extract_nota_data import extract_nota_data
from utils import retry_with_logging, generate_random_number

def click_each_nfse(nav, numero_nota):
    # Obtém a janela principal atual
    janela_principal = nav.current_window_handle
    # Padrões de URLs para a janela da nota e janela principal
    padrao_url_janela_nota = "NotaFiscal/notaFiscal.php?id_nota_fiscal="
    padrao_url_janela_principal = "https://nfse.campinas.sp.gov.br/NotaFiscal/index.php?"
    prosseguir = False
    extrair_dados = True
    try:
        # Loop para tentar extrair dados enquanto a condição 'extrair_dados' for verdadeira
        while extrair_dados:
            # Gera um número aleatório e aguarda por esse período
            tempo_aleatorio = generate_random_number()
            time.sleep(tempo_aleatorio)
            # Clicar na nota
            prosseguir = retry_with_logging(clicar_nota, nav, numero_nota, padrao_url_janela_principal, janela_principal)
            if prosseguir:
                # Identificar a nova janela
                prosseguir = processar_nova_janela(nav, janela_principal)
                if prosseguir:
                    # Obtém a URL atual após o processamento da nova janela
                    url_atual = nav.current_url
                    # Tenta extrair dados da nota
                    extrair_dados = extract_nota_data(nav, numero_nota, extrair_dados)
        # Retorna para a janela principal após a extração de dados
        nav.switch_to.window(janela_principal)
        nav.switch_to.frame("principal")
    except Exception as e:
        # Registra um erro caso ocorra uma exceção
        logging.error(f"Erro ao clicar em cada nota: {e}")

def clicar_nota(nav, numero_nota, padrao_url_janela_principal, janela_principal):
    try:
        # Verifica se a URL da janela principal está presente na URL atual
        if padrao_url_janela_principal not in url_atual:
            # Fecha a janela atual
            nav.close()
            # Obtém todas as abas (janelas) abertas
            abas = nav.window_handles
            for aba in abas:
                # Alterna para cada aba
                nav.switch_to.window(aba)
                # Obtém a URL atual da aba
                url_atual = nav.current_url
                # Se a URL da janela principal estiver presente, registra uma mensagem e encerra o loop
                if padrao_url_janela_principal in url_atual:
                    logging.info(f"Página principal encontrada.")
   
        else:
            # Se a URL da janela principal já estiver presente, registra uma mensagem
            logging.info("Já estou na página principal.")
        # Alterna para o frame "principal"
        nav.switch_to.frame("principal")
        # Clica no link da nota usando XPath
        nav.find_element(By.XPATH, f'//a[b[text()="{numero_nota}"]]').click()
        # Executa o clique no link da nota usando JavaScript
        nav.execute_script("arguments[0].click();", nota_link)
        # Define 'prosseguir' como verdadeiro, indicando sucesso
        prosseguir = True

    except:
        # Se ocorrer uma exceção durante o clique na nota, tenta uma abordagem alternativa
        prosseguir = False
        
        try:
            # Tenta encontrar novamente o link da nota
            nota_link = nav.find_element(By.XPATH, f'//a[b[text()="{numero_nota}"]]')
            # Executa o clique no link da nota usando JavaScript
            nav.execute_script("arguments[0].click();", nota_link)
            # Aguarda até que haja duas janelas abertas (principal e nova janela)
            WebDriverWait(nav, 10).until(EC.number_of_windows_to_be(2))
            # Define 'prosseguir' como verdadeiro, indicando sucesso
            prosseguir = True
        except:
            # Se ainda ocorrer uma exceção, registra um aviso
            logging.warning(f"Erro ao clicar no link da nota {numero_nota}")
            raise
        
    return prosseguir

def processar_nova_janela(nav, janela_principal):
    # Inicialização de variável
    prosseguir = False
    try:
        # Aguarda até que haja duas janelas abertas
        WebDriverWait(nav, 2).until(EC.number_of_windows_to_be(2))
        # Obtém todos os identificadores de janelas
        identificadores_janelas = nav.window_handles
        # Obtém o identificador da nova janela (diferente da janela principal)
        nova_janela_identificador = [identificador for identificador in identificadores_janelas if identificador != janela_principal][0]
        # Alterna para a nova janela
        nav.switch_to.window(nova_janela_identificador)
        # Define 'prosseguir' como verdadeiro
        prosseguir = True

    except (TimeoutException, NoSuchElementException) as e:
        # Registra um erro se encontrar uma exceção ao processar a nova janela
        logging.error("Erro ao encontrar a janela, voltando à janela principal.")
        for identificador in nav.window_handles:
            if identificador != janela_principal:
                logging.info("Fechando janelas excedentes.")
                nav.switch_to.window(identificador)
                nav.close()
        nav.switch_to.window(janela_principal)

    return prosseguir
