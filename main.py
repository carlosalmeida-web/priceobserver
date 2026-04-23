from funcoes_auxiliares import (
    validar_nome,
    extrair_numero,
    limpar_logs,
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

def ler_valor_pagina(driver, xpath, usuario, timeout):
    """
    Localiza o elemento informado por XPath e extrai o numero.
    """
    registrar_log(usuario, f"Buscando texto na página COINMARKETCAP... (xPATH: {xpath})", "SISTEMA")

    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        raise ValueError("Elemento não encontrado dentro do tempo.")

    texto = elemento.text.strip()

    registrar_log(usuario, f"Texto encontrado na página COINMARKETCAP: {texto}", "SISTEMA")

    valor = extrair_numero(texto)
    if valor is None:
        raise ValueError("Nenhum número foi encontrado no campo informado.")

    return valor

def clicar_botao(driver, xpath, timeout, usuario, descricao):
    """
    Localiza o elemento informado por XPath e clica nele.
    """

    registrar_log(usuario, f"Buscando botão de {descricao} na página GMAIL... (xPATH: {xpath})", "SISTEMA")

    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
    except TimeoutException:
        raise ValueError("Elemento não encontrado dentro do tempo")
    
    try:
        elemento.click()
    except ElementClickInterceptedException:
        # Esse except acontece quando uma mensagem de aviso sem destinatário aparece e estamos fora do email.
        registrar_log(usuario, f"O botão de {descricao} na página GMAIL foi interceptado. Evite sair da página do GMAIL, para não acumular avisos. Tentando clique via JavaScript.", "SISTEMA")
        driver.execute_script("arguments[0].click();", elemento)
        registrar_log(usuario, f"O botão de {descricao} na página GMAIL foi clicado via JavaScript.", "SISTEMA")

    registrar_log(usuario, f"Botão de {descricao} clicado com sucesso na página GMAIL.", "SISTEMA")

def enviar_para_outra_pagina(
    driver,
    xpath_campo_preencher,
    xpath_botao_envio,
    xpath_botao_ok,
    mensagem,
    usuario,
    timeout,
):
    """
    Controla o preenchimendo da mensagem no campo e os botões.
    """

    registrar_log(usuario, f"Buscando campo para preencher na página GMAIL... (xPATH: {xpath_campo_preencher})", "SISTEMA")

    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath_campo_preencher))
        )
        elemento.clear()
        elemento.send_keys(mensagem)
    except TimeoutException:
        raise ValueError("Elemento não encontrado dentro do tempo")

    registrar_log(usuario, "Mensagem preenchida com sucesso na página GMAIL...", "SISTEMA")

    clicar_botao(driver, xpath_botao_envio, timeout, usuario, 'envio')

    try:
        clicar_botao(driver, xpath_botao_ok, 10, usuario, 'OK para fechar aviso')
    except (TimeoutException, ValueError):
        registrar_log(usuario, f"Botão de OK para fechar aviso não foi encontrado na página GMAIL. Lembre de permanecer com o Chrome em primeiro plano.", "SISTEMA")

def monitorar_preco():
    """
    Executa o fluxo principal de monitoramento de preco.
    """
    limpar_logs()

    print("<<<< MONITOR DE PRECO >>>>")

    intervalo = 10
    timeout = 50
    url_monitorada = "https://coinmarketcap.com/pt-br/currencies/bitcoin/"
    xpath_campo = "//span[@data-test='text-cdp-price-display']"
    url_envio = "https://mail.google.com/mail/u/0/#inbox?compose="
    xpath_campo_preencher = "//div[@role='textbox' and @aria-label='Corpo da mensagem' and @contenteditable='true']"
    xpath_botao_envio = "//td[contains(@class, 'gU') and contains(@class, 'Up')]//div[@role='button' and contains(@aria-label, 'Enviar') and normalize-space()='Enviar']"
    xpath_botao_ok = "//button[@data-mdc-dialog-action='ok' and .//span[normalize-space()='OK']]"

    nome_usuario = input("Digite seu nome: ").strip()

    while not validar_nome(nome_usuario):
        nome_usuario = input("Nome invalido. Use apenas letras e espacos, com ao menos 3 caracteres: ").strip()

    registrar_log(nome_usuario, f"Nome de usuário informado: {nome_usuario}", "USUARIO")
    registrar_log(nome_usuario, "Sistema iniciado!", "SISTEMA")

    try:
        driver = conectar_chrome_aberto(DEBUGGER_ADDRESS)
        aba_monitor = encontrar_aba_por_url(driver, url_monitorada)
        aba_destino = encontrar_aba_por_url(driver, url_envio)
        registrar_log(nome_usuario, "Conectado ao Chrome aberto.", "SISTEMA")

        driver.switch_to.window(aba_monitor)
        registrar_log(nome_usuario, f"Aba da página COINMARKETCAP aberta ({url_monitorada}).", "SISTEMA")
        valor_anterior = ler_valor_pagina(driver, xpath_campo, nome_usuario, timeout)
        registrar_log(nome_usuario, f"Valor inicial encontrado na pagina monitorada: {valor_anterior}", "SISTEMA")

        while True:
            time.sleep(intervalo)
            driver.switch_to.window(aba_monitor)
            registrar_log(nome_usuario, f"Aba da página COINMARKETCAP aberta ({url_monitorada}).", "SISTEMA")
            valor_atual = ler_valor_pagina(driver, xpath_campo, nome_usuario, timeout)

            if valor_anterior != valor_atual:
                mensagem_mudanca = f"Preco alterado de {valor_anterior} para {valor_atual}"
                registrar_log(nome_usuario, f"ALTERACAO DETECTADA! {mensagem_mudanca}", "SISTEMA")

                driver.switch_to.window(aba_destino)
                registrar_log(nome_usuario, f"Aba com link da página GMAIL aberta ({url_envio}).", "SISTEMA")
                enviar_para_outra_pagina(
                    driver,
                    xpath_campo_preencher,
                    xpath_botao_envio,
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
