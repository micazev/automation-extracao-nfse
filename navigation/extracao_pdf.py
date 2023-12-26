import fitz
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyautogui
import logging

def extrair_dados_pdf(nav, nota_number):
    # Send Ctrl+S to save the PDF
    nav.find_element(By.ID, 'btnImprimir').click()
    # webdriver.ActionChains(nav).key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
    
    # Wait for the save dialog to appear (adjust the sleep time accordingly)
    time.sleep(1)

    # Input the file path and name, and press Enter to save as "nota.pdf"
    pyautogui.write(f"config/nota.pdf")
    pyautogui.press('enter')

    # Wait for the PDF to save (adjust the sleep time accordingly)
    time.sleep(5)

    # Open the saved PDF
    doc = fitz.open(f"config/nota.pdf")

    nota = {
        "Número da Nota": None,
        "Data e Hora de Emissão": None,
        "Código de Verificação": None,
    }

    prestador = {
        "Nome/Razão Social": None,
        "CPF/CNPJ": None,
        "Endereço": None,
        "Município": None,
        "Inscrição Municipal": None,
        "Telefone": None,
        "UF": None,
    }

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text("text").split("\n")

        for chave in nota:
            for index, line in enumerate(text):
                if chave in line:
                    nota[chave] = text[index + 1].strip() if index + 1 < len(text) else None
                    break

        for chave in prestador:
            for index, line in enumerate(text):
                if chave in line:
                    prestador[chave] = text[index + 1].strip() if index + 1 < len(text) else None
                    break

    doc.close()
    combined_data = nota.copy()
    combined_data.update(prestador)

    save_to_file(combined_data, nota_number)

def save_to_file(combined_data, nota_number):
    filename = f"extracts/nota_{nota_number}.txt"
    with open(filename, 'w') as file:
        file.write(combined_data)
