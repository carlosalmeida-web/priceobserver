from funcoes_auxiliares import validar_nome, extrair_numero, verifica_mudanca, registrar_log

import time 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def iniciar_driver():
    """
    Inicia o Chrome com Selenium.
    O driver é responsável por controlar o navegador.
    """
    service = Service(ChromeDriverManager().install()) # Aqui já instala o driver certo automaticamente e usa ele em Service()
    driver = webdriver.Chrome(service=service) # Conecta o navegador com o sellenium
    driver.maximize_window() # Abre o navegador em tela cheia
    return driver

def ler_valor_pagina(driver, url, xpath_campo, usuario):
    """
    Abre a página e lê o texto do elemento informado por XPath.
    Depois extrai o número do texto.
    """
    driver.get(url)
    time.sleep(2)

    elemento = driver.find_element(By.XPATH, xpath_campo) # Colocamos como parametro o tipo de busca que sera utilizada para encontrar o elemento e expressão XPath inteira que queremos encontrar
    texto = elemento.text.strip()

    registrar_log(usuario, f"Campo localizado com XPath: {xpath_campo}")
    registrar_log(usuario, f"Texto encontrado no campo: {texto}")

    valor = extrair_numero(texto)

    return valor, texto

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
        valor, texto = ler_valor_pagina(driver_monitor, url, xpath_campo, nome_usuario)
        registrar_log(nome_usuario, f"Valor '{valor}' encontrado no texto: '{texto}'")
    except Exception as e:
        registrar_log(nome_usuario, f"Erro ao tentar ler valor da página: {e}")

if __name__ == "__main__":
    monitorar_preco()