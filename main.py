from funcoes_auxiliares import (
    validar_nome,
    extrair_numero,
    registrar_log
)

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEBUGGER_ADDRESS = "127.0.0.1:9333"

def conectar_chrome_aberto(debugger_address):
    """
    Conecta o Selenium em um Chrome ja aberto.
    """
    opcoes = webdriver.ChromeOptions()
    opcoes.add_experimental_option("debuggerAddress", debugger_address)

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opcoes)

def encontrar_aba_por_url(driver, trecho_url):
    """
    Procura uma aba aberta cuja URL contenha o trecho informado.
    """
    for handle in driver.window_handles:
        driver.switch_to.window(handle)

        if trecho_url in driver.current_url:
            return handle

    raise ValueError(f"Nenhuma aba aberta contem a URL: {trecho_url}")

def ler_valor_pagina(driver, xpath_campo, usuario, timeout):
    """
    Localiza o elemento informado por XPath e extrai o numero.
    """
    registrar_log(usuario, f"Buscando texto pelo XPath: {xpath_campo}", "SISTEMA")

    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath_campo))
        )
    except TimeoutException:
        raise ValueError("Elemento não encontrado dentro do tempo")

    texto = elemento.text.strip()

    registrar_log(usuario, f"Texto encontrado no campo ({xpath_campo}): {texto}", "SISTEMA")

    valor = extrair_numero(texto)
    if valor is None:
        raise ValueError("Nenhum numero foi encontrado no campo informado.")

    return valor

def clicar_por_xpath(driver, xpath, timeout, usuario, descricao):

    def clicar():
        try:
            elemento = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except TimeoutException:
            raise ValueError("Elemento não encontrado dentro do tempo")

        try:
            elemento.click()
        except ElementClickInterceptedException:
            registrar_log(usuario, f"Clique normal em {descricao} interceptado. Tentando clique via JavaScript.", "SISTEMA")
            driver.execute_script("arguments[0].click();", elemento)

    clicar()
    registrar_log(usuario, f"{descricao} clicado com sucesso.", "SISTEMA")

def enviar_para_outra_pagina(
    driver,
    xpath_campo_destino,
    xpath_botao_destino,
    xpath_botao_ok,
    mensagem,
    usuario,
    timeout,
):

    registrar_log(usuario, "Iniciando envio para a pagina de destino.", "SISTEMA")
    registrar_log(usuario, f"Buscando campo para limpar pelo XPath: {xpath_campo_destino}", "SISTEMA")

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath_campo_destino))
    ).clear()

    registrar_log(usuario, "Campo limpo com sucesso.", "SISTEMA")
    registrar_log(usuario, f"Buscando campo para digitar pelo XPath: {xpath_campo_destino}", "SISTEMA")

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath_campo_destino))
    ).send_keys(mensagem)

    registrar_log(usuario, "Mensagem DIGITADA com sucesso.", "SISTEMA")

    clicar_por_xpath(driver, xpath_botao_destino, timeout, usuario, "Botao Enviar do Gmail")

    registrar_log(usuario, "Mensagem ENVIADA com sucesso.", "SISTEMA")

    try:
        clicar_por_xpath(driver, xpath_botao_ok, 5, usuario, "Botao OK do aviso do Gmail")
    except (TimeoutException, ValueError):
        registrar_log(usuario, "Botao OK do Gmail nao apareceu. Continuando monitoramento.", "SISTEMA")


def monitorar_preco():
    """
    Executa o fluxo principal de monitoramento de preco.
    """
    print("<<<< MONITOR DE PRECO >>>>")

    driver = None
    aba_monitor = None
    aba_destino = None

    intervalo = 10
    timeout = 50
    url_monitorada = "https://coinmarketcap.com/pt-br/currencies/bitcoin/"
    xpath_campo = "//span[@data-test='text-cdp-price-display']"
    url_destino = "https://mail.google.com/mail/u/0/#inbox?compose="
    xpath_campo_destino = "//div[@role='textbox' and @aria-label='Corpo da mensagem' and @contenteditable='true']"
    xpath_botao_destino = "//td[contains(@class, 'gU') and contains(@class, 'Up')]//div[@role='button' and contains(@aria-label, 'Enviar') and normalize-space()='Enviar']"
    xpath_botao_ok = "//button[@data-mdc-dialog-action='ok' and .//span[normalize-space()='OK']]"

    nome_usuario = input("Digite seu nome: ").strip()

    while not validar_nome(nome_usuario):
        nome_usuario = input("Nome invalido. Use apenas letras e espacos, com ao menos 3 caracteres: ").strip()

    registrar_log(nome_usuario, f"Nome de usuário informado: {nome_usuario}", "USUARIO")
    registrar_log(nome_usuario, "Sistema iniciado!", "SISTEMA")

    try:
        driver = conectar_chrome_aberto(DEBUGGER_ADDRESS)
        aba_monitor = encontrar_aba_por_url(driver, url_monitorada)
        aba_destino = encontrar_aba_por_url(driver, url_destino)
        registrar_log(nome_usuario, "Conectado ao Chrome ja aberto.", "SISTEMA")

        driver.switch_to.window(aba_monitor)
        valor_anterior = ler_valor_pagina(driver, xpath_campo, nome_usuario, timeout)
        registrar_log(nome_usuario, f"Valor inicial encontrado: {valor_anterior}", "SISTEMA")

        while True:
            time.sleep(intervalo)
            driver.switch_to.window(aba_monitor)

            valor_atual = ler_valor_pagina(driver, xpath_campo, nome_usuario, timeout)

            if valor_anterior != valor_atual:
                print("\nALTERACAO DETECTADA!")
                print(f"Valor antigo: {valor_anterior}")
                print(f"Valor novo: {valor_atual}")

                mensagem_mudanca = f"Preco alterado de {valor_anterior} para {valor_atual}"

                registrar_log(
                    nome_usuario,
                    f"Alteracao detectada. {mensagem_mudanca}",
                    "SISTEMA"
                )

                driver.switch_to.window(aba_destino)
                enviar_para_outra_pagina(
                    driver,
                    xpath_campo_destino,
                    xpath_botao_destino,
                    xpath_botao_ok,
                    mensagem_mudanca,
                    nome_usuario,
                    timeout,
                )

                valor_anterior = valor_atual
            else:
                registrar_log(nome_usuario, f"Nenhuma alteracao detectada. Valor atual continua: {valor_atual}", "SISTEMA")

    except KeyboardInterrupt:
        registrar_log(nome_usuario, "Monitoramento encerrado pelo usuario.", "USUARIO")
    except Exception as e:
        registrar_log(nome_usuario, f"Erro encontrado: {e}", "SISTEMA")
    finally:
        registrar_log(nome_usuario, "Sistema finalizado.", "SISTEMA")


if __name__ == "__main__":
    monitorar_preco()
