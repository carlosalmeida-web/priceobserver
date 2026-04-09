def validar_nome(nome):
    nome = nome.strip()

    if len(nome) < 3:
        return False

    for caractere in nome:
        if not (caractere.isalpha() or caractere.isspace()):
            return False

    return True

def monitorar_preco():
    print("<<<< MONITOR DE PRECO >>>>")

    nome_usuario = input("Digite seu nome: ").strip()
    while not validar_nome(nome_usuario):
        nome_usuario = input("Nome invalido. Digite novamente: ").strip()

    url = input("Digite a URL para monitorar: ").strip()
    xpath_campo = input("Digite o XPath do campo: ").strip()

    print(f"Usuario: {nome_usuario}")
    print(f"URL informada: {url}")
    print(f"XPath informado: {xpath_campo}")

if __name__ == "__main__":
    monitorar_preco()
