# Monitor de Preco

Projeto de Analise de Algoritmos para monitorar um valor numerico em uma pagina web e, quando houver alteracao, enviar uma mensagem para outra pagina publica.

## Instalacao

```bash
pip install -r requirements.txt
```

## Como executar

Antes de rodar o sistema, abra o Google Chrome pelo Prompt de Comando com a porta de depuracao remota:

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9333 --user-data-dir="C:\chrome_debug_test"
```

Nesse Chrome aberto, carregue as duas paginas:

1. Pagina monitorada:
   ```text
   https://coinmarketcap.com/pt-br/currencies/bitcoin/
   ```
2. Pagina de destino:
   ```text
   Link do gmail com a aba de escrever email aberta
   ```

Depois execute:

```bash
python main.py
```

Durante a execucao, o sistema solicita apenas o nome do usuario. As URLs, XPaths, intervalo e timeout ficam configurados diretamente no arquivo `main.py` para facilitar a demonstracao.

## Configuracoes principais

As principais configuracoes estao dentro da funcao `monitorar_preco` em `main.py`:

```python
intervalo = 10
timeout = 50
url_monitorada = "https://coinmarketcap.com/pt-br/currencies/bitcoin/"
xpath_campo = "//span[@data-test='text-cdp-price-display']"
url_destino = "https://mail.google.com/mail/u/0/#inbox?compose="
xpath_campo_destino = "//div[@role='textbox' and @aria-label='Corpo da mensagem' and @contenteditable='true']"
xpath_botao_destino = "//td[contains(@class, 'gU') and contains(@class, 'Up')]//div[@role='button' and contains(@aria-label, 'Enviar') and normalize-space()='Enviar']"
xpath_botao_ok = "//button[@data-mdc-dialog-action='ok' and .//span[normalize-space()='OK']]"
```

O sistema conecta no Chrome ja aberto em `127.0.0.1:9333`, encontra as abas pela URL, monitora o preco do Bitcoin no CoinMarketCap e envia uma mensagem pelo Gmail quando identifica uma alteracao de valor.

## Funcionamento

1. O usuario informa o nome.
2. O sistema valida o nome com `validar_nome`.
3. O Selenium conecta no Chrome ja aberto.
4. O sistema encontra a aba do CoinMarketCap.
5. O sistema encontra a aba do Gmail.
6. O primeiro preco lido vira o valor inicial.
7. A cada `intervalo`, o sistema le novamente o preco.
8. Se o valor mudou, o sistema monta uma mensagem com o valor antigo e o novo.
9. O sistema troca para a aba do Gmail, limpa o corpo da mensagem, digita o texto e clica no botao Enviar.
10. Se o aviso de OK do Gmail aparecer, o sistema tenta clicar nele; se nao aparecer, continua o monitoramento.

## Logs

As acoes sao registradas no arquivo `logs.txt`.

Formato dos logs:

```text
[22/04/2026 19:15:53] [USUARIO: Joao] Nome de usuário informado: Joao
[22/04/2026 19:15:54] [SISTEMA] Sistema iniciado!
```

Logs de `USUARIO` sao usados apenas para a entrada do nome e para encerramento manual com `Ctrl + C`. Todas as outras acoes sao registradas como `SISTEMA`.

## Testes automatizados

```bash
python -m unittest teste.py
```

Os testes cobrem:

- Validacao de nome.
- Extracao de numeros em textos com formato brasileiro.
- Retorno `None` quando nao existe numero no texto.

## Documentacao do codigo

A documentacao pode ser consultada com `pydoc`, usando as docstrings dos modulos:

```bash
python -m pydoc main
python -m pydoc funcoes_auxiliares
```

Tambem e possivel gerar HTML local:

```bash
python -m pydoc -w main funcoes_auxiliares
```

Esse comando gera arquivos HTML com a documentacao das funcoes.

## Analise Big O

- `n`: tamanho do texto lido no campo monitorado.
- `k`: quantidade de ciclos de monitoramento executados.

### Validacao do nome

A funcao `validar_nome(nome)` percorre cada caractere do nome uma vez para verificar se todos sao letras ou espacos.

Complexidade: `O(n)`.

### Localizacao das abas abertas

A funcao `encontrar_aba_por_url(driver, trecho_url)` percorre a lista de abas abertas ate encontrar uma URL que contenha o trecho informado.

Complexidade: `O(n)`, considerando `n` como a quantidade de abas abertas.

### Leitura e extracao do preco

A funcao `ler_valor_pagina` espera o elemento do preco aparecer, le o texto e chama `extrair_numero`.

`extrair_numero(texto)` usa expressao regular sobre o texto lido.

Complexidade: `O(n)`, onde `n` e o tamanho do texto do campo monitorado.

### Envio da mensagem

A funcao `enviar_para_outra_pagina` localiza o campo de texto do Gmail, limpa o campo, digita a mensagem, clica no botao Enviar e tenta clicar no botao OK do aviso.

Complexidade: `O(1)`.

### Comparacao dos valores

A comparacao entre o valor antigo e o valor atual usa apenas dois numeros:

```python
if valor_anterior != valor_atual:
```

Complexidade: `O(1)`.

### Monitoramento completo

Em cada ciclo, o sistema:

- Le e extrai o preco.
- Compara com o valor anterior.
- Se houver mudanca, alterna para o Gmail e envia a mensagem.

Em um unico ciclo, a operacao mais importante e a leitura/extracao do numero, que e `O(n)`.

Complexidade de um ciclo: `O(n)`.

Como o monitoramento repete esse ciclo varias vezes, para `k` ciclos a complexidade total e:

```text
O(k * n)
```

Mas se for para considerar apenas uma execucao monitoramento:

```text
O(n)
```
