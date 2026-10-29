# Roteiro: entregar a migração sem esperar pelo final

## O que já está resolvido e o que falta fazer

As duas aplicações, seus testes e o executor de validação estão implementados. As duas pipelines iniciais funcionam, mas repetem a orquestração. Sua tarefa é escrever o workflow reutilizável e adaptar suas chamadas. Este roteiro apresenta os estados que devem funcionar; não contém o YAML final da solução.

Se estiver estudando individualmente, faça revisão própria identificada como tal. Não é necessário produzir aprovações fictícias. Os PRs podem usar uma descrição curta: mudança, verificação e o que ainda não migrou.

## 0. Reconhecer a base

Na raiz do projeto, execute:

```sh
python tools/verify_service.py --project-path services/catalogo --test-path tests
python tools/verify_service.py --project-path services/supervisao --test-path verificacoes
```

Leia os JSONs em `outputs/catalogo/validacao.json` e `outputs/supervisao/validacao.json`. Compare projeto, testes, Python e código de saída. A revisão Git aparece depois que o projeto está em um clone com commits. Os relatórios são temporários, não arquivos a commitar.

Abra as duas definições em `.github/workflows/` e marque mentalmente o que se repete. Note as diferenças que não podem desaparecer: matriz do catálogo e caminho das verificações da supervisão.

Na interface do GitHub, confirme as execuções normais de **CI · Catálogo** e **CI · Supervisão**. Pushes em uma branch disparam os dois workflows; PRs também podem gerar outras execuções. Compare resultados da mesma revisão, sem misturar uma execução antiga com outra nova.

## 1. Escolher o tronco ativo

A `main` guarda a base e `main-resolucao` será o tronco desta prática. Se essa branch ainda não existe, partindo da principal atualizada e com o diretório limpo:

```sh
git switch main
git pull --ff-only
git switch -c main-resolucao
git push -u origin main-resolucao
```

Se já existir, use `git switch main-resolucao` e atualize-a; não recrie ou sobrescreva a branch. A tag opcional `lab03-inicio` deve identificar a base, sem mover uma tag já publicada. Nenhuma aplicação é implantada por esses comandos.

Ao criar o próximo PR, selecione base `main-resolucao`. A `main` preservada não deve receber os incrementos. O nome main-resolucao é uma adaptação didática: há um único tronco ativo, sem develop ou linha de release paralela.

## 2. Primeiro incremento: padrão exercitado sem migrar ninguém

Crie uma branch curta a partir do tronco atualizado, por exemplo `feat/padrao-validacao`.

Antes de escrever, leia [o contrato](contrato-da-automacao.md). Crie `.github/workflows/_verificacao-python.yml` com o evento `workflow_call`. Declare as entradas do contrato e um job que reutilize a sequência já conhecida. Mantenha as permissões de leitura; não precisamos de secrets ou escrita no repositório.

A matriz não ficará nesse padrão. Ele recebe uma única versão por chamada e prepara o Python solicitado. Os caminhos devem chegar ao comando como parâmetros, não ficar fixos em services/catalogo. Preserve a falha como falha e o registro do diagnóstico.

Crie uma chamada de teste temporária, por exemplo `.github/workflows/ensaio-reuso.yml`, disparada por push e pull_request. Ela deve chamar o padrão com catálogo, tests, Python 3.11 e cenário normal. O disparo por push/PR permite exercitá-la enquanto é um arquivo novo na branch; um botão manual pode não aparecer para um workflow que ainda não existe na branch padrão.

Observe a diferença entre chamar action dentro de steps e chamar workflow no nível do job. Antes do PR, confira que a chamada de teste e os dois consumidores iniciais passam. O GitHub precisa conseguir localizar e interpretar o arquivo reutilizável. Testar apenas o comando Python localmente não demonstra isso.

Faça um commit coerente, envie e abra o PR para main-resolucao. Revise o diff e as execuções. Depois de integrar, confira o tronco. Não comece a segunda etapa empilhando uma branch sobre um PR ainda não integrado.

**Resultado deste incremento:** o padrão está disponível e exercitado, mas ninguém foi obrigado a mudar sua pipeline para ele.

## 3. Segundo incremento: catálogo primeiro

Atualize o tronco e crie outra branch curta, como `refactor/catalogo-usa-padrao`:

```sh
git switch main-resolucao
git pull --ff-only
git switch -c refactor/catalogo-usa-padrao
```

Altere somente a orquestração do catálogo e o que for estritamente necessário para essa adoção. Preserve nome, eventos e campo manual de cenário. No job consumidor, a matriz continua definindo 3.11 e 3.12, e cada chamada fornece sua versão ao padrão. Checkout e setup ficam no workflow chamado.

Remova a implementação repetida que a chamada substitui; não mantenha um segundo caminho de verificação não utilizado. Execute o cenário normal, confira as duas versões e observe o serviço e os caminhos no relatório.

Envie o incremento e abra PR para o tronco. Enquanto o PR está aberto, execute manualmente **CI · Catálogo**, selecionando sua branch, com cenário falha. O workflow já existe na base; a execução selecionada deve usar o arquivo da branch. A aprovação normal e a reprovação controlada são evidências complementares. O cenário de falha é manual e não altera o cenário normal dos checks de push e PR.

Confirme também a execução normal da supervisão. Ela ainda usa a implementação original e não precisa migrar no mesmo PR. Integre o incremento depois da revisão. Registre uma evidência desse estado intermediário: consumidor catálogo compartilhado, supervisão independente.

**Resultado deste incremento:** já reduzimos um ponto de manutenção sem esperar a migração inteira.

## 4. Terceiro incremento: supervisão depois

Parta novamente do tronco atualizado e use uma branch como `refactor/supervisao-usa-padrao`. Substitua a implementação do job de supervisão pela chamada ao mesmo workflow.

Passe o diretório correto: services/supervisao com verificacoes, e Python 3.12. Não renomeie sua pasta de testes, não copie testes do catálogo e não altere o executor para criar um atalho específico.

Confira cenário normal e falha controlada na supervisão. Confira também catálogo normal nas duas versões. Examine o relatório: um job com nome Supervisão que executou testes do catálogo não atende ao contrato. Abra o PR, revise e integre.

**Resultado deste incremento:** os dois consumidores usam o padrão, preservando diferenças de configuração.

## 5. Quarto incremento: retirar apoio temporário e conferir reprodução

Crie uma última branch curta para retirar ensaio-reuso.yml, pois os consumidores oficiais já exercitam o padrão. O arquivo reutilizável permanece. Preserve as duas pipelines consumidoras; limpar a migração não significa apagá-las.

Examine a estrutura final. O comando comum de verificação, a preparação do runner e do Python devem estar centralizados. A matriz e as entradas específicas permanecem nos consumidores. Não é necessário transformar todos os textos ou todos os nomes em parâmetros.

Confira uma cópia limpa da revisão proposta ou integrada, como descrito em [operação](operacao.md). Integre a limpeza e registre os estados intermediários. As execuções normais do tronco precisam passar e as falhas controladas continuar reprovando quando acionadas.

## 6. Encerramento

O laboratório termina com adoção comprovada do padrão, parâmetros preservados e evidência da integração incremental. Não é necessário criar uma Release, anexar um ZIP ou executar um novo ensaio de recuperação.

O relatório no jardim pode reunir quatro parágrafos, um por incremento, com os links que sustentam os resultados. Explique em suas palavras por que era possível usar a principal depois da primeira migração, mesmo antes da segunda. Esse é o aprendizado central de Trunk-Based nesta prática.

Se uma verificação normal quebrar, corrija o incremento antes de avançar. Não transforme a falha em aviso para manter o cronograma. Se não conseguir executar Actions por restrição da conta, registre essa limitação: uma validação local não substitui a evidência da chamada entre workflows.
