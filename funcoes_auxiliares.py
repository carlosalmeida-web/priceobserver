# Arquivo com as funções auxiliares

import re
from datetime import datetime

def validar_nome(nome):
    """
    Função que valida o nome do usuario

    Regras:
    - pelo menos 3 caracteres
    - apenas letras e espaços
    """
    nome = nome.strip()

    if len(nome) < 3:
        return False

    for caractere in nome:
        if not (caractere.isalpha() or caractere.isspace()):
            return False

    return True


def extrair_numero(texto):
    """
    Extrai o primeiro número encontrado em um texto.
    """
    texto = texto.strip()
    texto = texto.replace(" ", "")

    padrao = r"\d[\d.,]*"

    # Objeto da busca
    resultado = re.search(padrao, texto)

    if resultado:
        numero = resultado.group() # Extrai a string do texto encontrado
        
        # 1.299,90 -> 1299.90
        if "." in numero and "," in numero:
            numero = numero.replace(".", "").replace(",", ".")

        # 1299,90 -> 1299.90
        elif "," in numero:
            numero = numero.replace(",", ".")

        else:
            numero = numero

        return float(numero)

    return None

def registrar_log(usuario, mensagem, origem):
    """
    Registra uma mensagem de log em um arquivo .txt e imprime a mensagem no terminal.

    Origem:
    - USUARIO: entradas e acoes feitas pelo usuario.
    - SISTEMA: acoes automaticas do monitoramento.
    """
    timestamp_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if origem == "SISTEMA":
        linha = f"[{timestamp_atual}] [SISTEMA] {mensagem}\n"
    else:
        linha = f"[{timestamp_atual}] [{origem}: {usuario}] {mensagem}\n"

    with open("logs.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)

    print(linha)
