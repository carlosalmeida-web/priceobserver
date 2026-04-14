from funcoes_auxiliares import validar_nome, extrair_numero, verifica_mudanca, registrar_log

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

if __name__ == "__main__":
    monitorar_preco()
