# Arquivo com as funções auxiliares

def validar_nome(nome):
    
    nome = nome.strip()

    if len(nome) < 3:
        return False

    for caractere in nome:
        if not (caractere.isalpha() or caractere.isspace()):
            return False

    return True
