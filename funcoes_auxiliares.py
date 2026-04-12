# Arquivo com as funções auxiliares

import re

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

def verifica_mudanca(valor_antigo, valor_novo):
    """
    Retorna True se o valor mudou.
    """
    return valor_antigo != valor_novo
