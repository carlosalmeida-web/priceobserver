from funcoes_auxiliares import validar_nome, extrair_numero, verifica_mudanca, registrar_log

import time 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def iniciar_driver():
    """
    Inicia o Chrome com selenium.
    O driver é responsável por controlar o navegador.
    """
    service = Service(ChromeDriverManager().install()) # Instala o driver certo automaticamente e o uso no Service
    driver = webdriver.Chrome(service=service) # Conecta o navegador com o Selenium
    driver.maximize_window() # Abre o navegador em tela cheia
    return driver

def monitorar_preco():
    print("<<<< MONITOR DE PRECO >>>>")

    nome_usuario = input("Digite seu nome: ").strip()
    while not validar_nome(nome_usuario):
        nome_usuario = input("Nome invalido. Digite novamente: ").strip()

    url = input("Digite a URL para monitorar: ").strip()
    xpath_campo = input("Digite o XPath do campo: ").strip()

    registrar_log(nome_usuario, "Sistema iniciado!")
    registrar_log(nome_usuario, f"Usuario informado: {nome_usuario}")
    registrar_log(nome_usuario, f"URL informada: {url}")
    registrar_log(nome_usuario, f"XPath informado: {xpath_campo}")

    driver_monitor = iniciar_driver()

    try:
        registrar_log(nome_usuario, f"Acessando a URL: {url}")
        driver_monitor.get(url)
        time.sleep(2)
        registrar_log(nome_usuario, f"URL acessada com sucesso: {url}")
    
    except Exception as e:
        registrar_log(nome_usuario, f"Erro ao acessar a URL: {e}")

if __name__ == "__main__":
    monitorar_preco()
