# Contrato da validação compartilhada

Um contrato de automação descreve o que o workflow consumidor fornece e o que pode esperar. Aqui não estamos alterando respostas HTTP. Estamos definindo a interface usada por outras pipelines.

## Entradas da chamada

Use estes nomes para manter o roteiro e as evidências comparáveis:

| Entrada | Tipo no workflow_call | Obrigatória | Significado |
|---|---|---|---|
| `project-path` | string | Sim | Caminho do serviço relativo à raiz do checkout |
| `test-path` | string | Sim | Diretório dos testes relativo à pasta do serviço |
| `python-version` | string | Sim | Uma versão de Python para esta chamada |
| `cenario` | string | Não; padrão normal | `normal` ou `falha` |

O tipo da entrada não verifica sozinho se um caminho existe. A ferramenta Python faz essa conferência e rejeita uma entrada inválida. A entrada de cenário em `workflow_call` é string; a lista de opções da tela manual pertence ao `workflow_dispatch` do consumidor.

Valores esperados:

| Consumidor | project-path | test-path | python-version |
|---|---|---|---|
| Catálogo, primeira execução | services/catalogo | tests | 3.11 |
| Catálogo, segunda execução | services/catalogo | tests | 3.12 |
| Supervisão | services/supervisao | verificacoes | 3.12 |

A matriz permanece no catálogo. Cada variação chama o mesmo padrão com uma versão. O workflow compartilhado não precisa criar outra matriz nem conhecer os nomes catálogo e supervisão.

## Responsabilidades

**Consumidor:** define eventos, matriz quando necessária, caminhos e cenário. Mantém a descrição clara do serviço que está sendo verificado.

**Padrão compartilhado:** prepara um runner, obtém os arquivos, prepara a versão pedida de Python, invoca o executor e preserva seu código de saída. O resultado deve identificar serviço, revisão, versão de Python e cenário. O resumo do Actions pode complementar os logs; ele não determina se a verificação foi aprovada.

**Executor Python, já fornecido:** valida caminhos, descobre e executa testes, rejeita descoberta vazia, aplica a falha controlada e grava o relatório. Não é tarefa do laboratório reescrever esse programa.

## Como ler a nova sintaxe

Você já conhece um step com `uses: actions/setup-python@v5`: ele chama uma action dentro de um job. Um workflow reutilizável é chamado em `jobs.NOME.uses`. O job chamador não possui seus próprios `steps` ou `runs-on`: esses elementos pertencem ao workflow chamado.

Um fragmento ilustrativo de chamada, ainda incompleto, é:

```yaml
jobs:
  verificar:
    uses: ./.github/workflows/_verificacao-python.yml
    with:
      project-path: services/catalogo
```

Ele mostra a posição do `uses`, mas ainda faltam as outras entradas e a matriz do catálogo. Não é o workflow final.

Na declaração do padrão, `on.workflow_call.inputs` define os nomes aceitos. Durante a execução, `inputs.project-path` consulta o valor recebido. A expressão não percorre uma pasta chamada inputs.

Há três nomes que podem ser parecidos, mas têm papéis diferentes: a chave `python-version` da nossa interface; a expressão `matrix.python-version`, que fornece um valor no consumidor; e o parâmetro `python-version` esperado pela action setup-python dentro do padrão.

## Passar valores ao comando

Prefira entregar os inputs como variáveis de ambiente do step e usar variáveis citadas no shell, como `"$PROJECT_PATH"`. Isso mantém o valor como argumento do comando em vez de misturá-lo ao texto de um script. O cenário pode ser entregue por `LAB_CENARIO`, que o executor já entende, ou pelo argumento `--cenario`.

Os argumentos `--project-path` e `--test-path` continuam obrigatórios no comando Python. Declarar um input no YAML não o transmite automaticamente ao programa. Confira o relatório para demonstrar que o valor atravessou a chamada inteira.

## Resultado esperado

- Normal: código 0 quando os testes passam.
- Falha controlada: código 1, mesmo quando a suíte real passa.
- Teste real reprovado: código não zero, sem depender da sonda.
- Caminho inválido ou diretório sem testes: código não zero e diagnóstico.

Não utilize `continue-on-error: true`, `|| true` nem outro mecanismo que transforme uma reprovação obrigatória em sucesso. Um step de relatório pode rodar com `always()` sem recuperar a aprovação da verificação.

O contrato desta prática usa o estado de aprovação/reprovação e o relatório. Não exige outputs nomeados de workflow, publicação de artefatos ou passagem de arquivos entre jobs. Esses recursos podem ser estudados depois de a reutilização estar compreendida.

## Estabilidade da referência

Use `./.github/workflows/_verificacao-python.yml` nesta prática para chamar o arquivo da mesma revisão. Não se acrescenta `@branch` a essa sintaxe local. Para compartilhar entre repositórios, a referência passa a incluir proprietário, repositório e uma revisão, com decisões adicionais de versão e acesso. Isso fica fora da implementação atual.

[Documentação de reutilização](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).
