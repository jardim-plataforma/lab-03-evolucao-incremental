# Lab 03 · Migração incremental de pipelines

Este laboratório é um projeto de estudo em engenharia de plataforma. Dois serviços já implementados possuem pipelines funcionais com orquestração duplicada. A tarefa é introduzir uma validação reutilizável e migrar os consumidores por pequenos incrementos, mantendo o tronco verificável.

**Estado inicial:** dois workflows independentes, testes aprováveis e ferramenta de validação pronta. O workflow reutilizável e sua adoção ainda não foram implementados. O trabalho será nos arquivos YAML, nos parâmetros e na documentação de operação; não é necessário desenvolver funcionalidades das aplicações.

[Enunciado](ENUNCIADO.md) · [Roteiro guiado](docs/roteiro.md) · [Contrato da automação](docs/contrato-da-automacao.md) · [Operação e diagnóstico](docs/operacao.md) · [Página no jardim](https://jardim-plataforma.github.io/jardim-plataforma/laboratorios/03-evolucao-incremental)

## A demanda

Centralizar checkout, preparação de Python, execução obrigatória e registro do resultado, sem perder as diferenças dos consumidores. O catálogo usa Python 3.11 e 3.12; a supervisão usa 3.12 e outro diretório de testes. Cada etapa da migração precisa funcionar antes da próxima.

A entrega final é o padrão utilizado pelas duas pipelines. Não há geração de ZIP, publicação de imagem nem implantação nesta prática.

## Executar as verificações

Requisitos locais: Git e Python 3.11 ou 3.12. Não é necessário instalar pacotes Python.

Na raiz do repositório:

```sh
python tools/verify_service.py --project-path services/catalogo --test-path tests
python tools/verify_service.py --project-path services/supervisao --test-path verificacoes
```

A base possui 13 testes no catálogo e 7 na supervisão. No Windows, `py -3.12` ou `py -3.11` pode substituir `python`. Os testes iniciam suas próprias instâncias temporárias; não é necessário manter o servidor aberto.

O relatório fica em `outputs/NOME/validacao.json`, ignorado pelo Git. Sem um repositório Git local, o campo de commit informa `sem-revisao-git`; num clone com commits, informa o HEAD. O SHA não comprova sozinho a ausência de alterações locais.

Para conferir uma reprovação controlada:

```sh
python tools/verify_service.py --project-path services/catalogo --test-path tests --cenario falha
```

Esse comando deve retornar código 1, mesmo com os testes da aplicação passando. Não altere a ferramenta ou os testes para esconder a reprovação. Examine `$LASTEXITCODE` no PowerShell ou `$?` no Bash imediatamente após o comando.

## Estrutura de trabalho

| Caminho | Responsabilidade |
|---|---|
| `.github/workflows/ci-catalogo.yml` | Pipeline inicial do catálogo, com matriz |
| `.github/workflows/ci-supervisao.yml` | Pipeline inicial da supervisão |
| `tools/verify_service.py` | Executor pronto, usado por ambas |
| `services/catalogo/` | API e portal de catálogo, com testes |
| `services/supervisao/` | Leitor HTTP de relatório local de supervisão, com verificações |
| `docs/` | Roteiro, contrato, comandos e critérios de diagnóstico |

Os arquivos que começam com ponto fazem parte da base: `.github/`, `.gitignore` e `.gitattributes`. Os workflows devem estar diretamente em `.github/workflows/` na raiz do repositório para serem reconhecidos pelo Actions.

## Começar sem reabrir o Git Flow

A `main` pode guardar a base didática; `main-resolucao` será o único tronco ativo. Não crie develop ou release. O roteiro apresenta uma branch curta por incremento, sempre a partir do tronco atualizado. Preserve a referência inicial; não sobrescreva uma resolução existente para repetir a prática.

Comece lendo os dois workflows e executando os dois comandos normais. Depois siga [o primeiro incremento](docs/roteiro.md). O roteiro descreve decisões e verificações, sem fornecer o YAML final para copiar.

## Executar os serviços manualmente

Para abrir o catálogo, entre em `services/catalogo` e execute `python -m backend.server`. Acesse http://127.0.0.1:8080.

Para a supervisão, entre em `services/supervisao` e execute `python -m app.server`. Acesse http://127.0.0.1:8090/estado. Ela lê dados locais fictícios; não faz chamadas ao catálogo nem monitora infraestrutura externa. Os serviços podem ser executados independentemente.

## Evidências

Registre os PRs, os commits e as execuções relevantes, principalmente o estado em que apenas um consumidor foi migrado. Uma explicação curta com resultados vale mais do que uma lista extensa de comandos. Revisão individual não deve ser apresentada como aprovação independente.

[Origem e escopo dos componentes](docs/origem.md).
