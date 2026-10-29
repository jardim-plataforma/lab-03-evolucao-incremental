# Operação e diagnóstico

## Executar localmente pela raiz

```sh
python tools/verify_service.py --project-path services/catalogo --test-path tests
python tools/verify_service.py --project-path services/supervisao --test-path verificacoes
```

O executor muda para a pasta do serviço antes de iniciar os testes. Por isso, test-path é relativo ao projeto, não à raiz do repositório. Ele não precisa de um servidor previamente iniciado. Os testes abrem e encerram servidores em portas locais livres.

O Python local pode ser 3.11 ou 3.12. Para exercitar as duas versões localmente, elas precisam estar instaladas. Não é necessário fazer essa instalação para começar: o runner prepara as versões configuradas no workflow. Não declare uma versão testada apenas porque ela aparece no YAML; confira a execução e o relatório.

## Conferir o retorno e o relatório

PowerShell: imediatamente depois de um comando, use `$LASTEXITCODE`. Bash: use `echo $?`. Um retorno zero indica aprovação; diferente de zero indica reprovação ou erro de configuração.

`outputs/SERVICO/validacao.json` registra serviço, caminhos recebidos, Python, revisão Git, cenário e retornos. O relatório é reescrito em cada execução local daquele serviço. Ele não é uma prova de integridade nem substitui o log dos testes. Em runners separados, cada execução tem seu próprio disco.

O executor recusa caminho de projeto fora de services/ e caminho de testes fora do próprio projeto. Um diretório existente que não contenha testes é erro, não sucesso. A configuração de cenário é validada antes da execução.

## Cenário controlado de falha

```sh
python tools/verify_service.py --project-path services/catalogo --test-path tests --cenario falha
python tools/verify_service.py --project-path services/supervisao --test-path verificacoes --cenario falha
```

Os dois comandos devem reprovar. Eles executam os testes e depois acrescentam uma falha controlada. Isso comprova que o workflow não esconde uma reprovação; não demonstra um defeito no serviço.

No GitHub, use **Actions → CI · Catálogo ou CI · Supervisão → Run workflow**. Selecione explicitamente a branch e o cenário. O workflow com execução manual deve existir na branch padrão. A base já possui os dois arquivos; mantenha seus nomes durante a migração. Execute normal e falha separadamente. Não faça merge para conseguir testar uma feature já enviada.

## Erro de caminho, sem modificar a aplicação

```sh
python tools/verify_service.py --project-path services/supervisao --test-path tests-inexistentes
```

O erro esperado é de configuração do caminho, não um teste reprovado. Compare com o diretório correto verificacoes. Se o workflow compartilha um caminho fixo, o teste do catálogo pode passar enquanto o da supervisão falha. Corrija o repasse da entrada, não a aplicação.

## Cópia limpa

Depois de enviar a revisão que deseja conferir, use uma pasta nova, fora do clone atual:

```sh
git clone --branch main-resolucao https://github.com/jardim-plataforma/lab-03-evolucao-incremental.git lab03-copia-limpa
cd lab03-copia-limpa
git rev-parse HEAD
python tools/verify_service.py --project-path services/catalogo --test-path tests
python tools/verify_service.py --project-path services/supervisao --test-path verificacoes
```

Se estiver conferindo um PR ainda aberto, clone a branch real do PR no lugar de main-resolucao. Registre o SHA para não comparar resultados de revisões diferentes. Esses comandos só leem o remoto e criam uma nova cópia; não alteram a resolução original.

## Diagnosticar por camadas

| Observação | Onde investigar primeiro |
|---|---|
| GitHub não interpreta a chamada | Posição de jobs.NOME.uses, nome do arquivo e entradas declaradas |
| Arquivo reutilizável não encontrado | Caminho direto em .github/workflows e referência local da mesma revisão |
| Checkout existe, mas o programa não é encontrado | Caminho de tools/ e diretório de trabalho do step |
| Supervisão tenta abrir tests | Entrada test-path e seu repasse ao comando |
| Zero testes encontrados | Caminho/padrão de descoberta; não aceite aprovação vazia |
| Cenário falha termina verde | Código de saída, tolerância indevida ou cenário não repassado |
| Só funciona na máquina local | Arquivo não versionado, pasta de trabalho ou dependência implícita |
| Job fica aguardando runner | Disponibilidade/política de execução; não é um teste executado com falha |

## Aplicações para consulta manual

Catálogo: na pasta services/catalogo, `python -m backend.server`; portal em http://127.0.0.1:8080 e saúde em /health. As APIs v1 e v2 seguem disponíveis.

Supervisão: na pasta services/supervisao, `python -m app.server`; relatório em http://127.0.0.1:8090/estado e saúde em /health. Ela resume o arquivo local config/checks.json, sem sondagem de rede externa. O nome catalogo presente nesse arquivo é somente um registro de demonstração, não uma conexão entre serviços.

Ctrl+C encerra o servidor manual. Executar servidores é opcional para a migração, mas ajuda a reconhecer que as cargas de trabalho são aplicações reais executáveis, não arquivos de mensagem.

## Conclusão das evidências

Anote referência Git, consumidor, Python, cenário, resultado e link da execução. Para o cenário normal, confirme os testes do serviço certo. Para falha, a reprovação é esperada. A página do jardim deve distinguir o que foi observado localmente do que foi executado no GitHub.
