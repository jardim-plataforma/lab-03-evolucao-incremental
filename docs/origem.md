# Origem e limites da base

O catálogo foi preservado a partir da revisão pública `ae2716910bbc75b6209fcff3a50a07b6546b069d` do [Lab 1](https://github.com/jardim-plataforma/lab-01-entrega-compativel/tree/ae2716910bbc75b6209fcff3a50a07b6546b069d). Backend, frontend, consumidores de demonstração e 13 testes mantêm os comportamentos daquela revisão. A pasta foi colocada em services/catalogo. Seu VERSION local identifica o serviço demonstrativo; não é necessário alterá-lo para migrar o CI.

A supervisão, seus 7 testes e o executor operacional foram criados para este laboratório. Ela é uma aplicação HTTP de leitura de relatório local, sem acesso a infraestrutura externa. Seus dados são fictícios e suas funcionalidades já estão implementadas.

O Lab 3 não importa automaticamente o histórico, as tags ou a política Git Flow do Lab 2. Ele retoma o aprendizado de Actions, matrizes e falhas obrigatórias, mas inicia uma migração independente. Não contém a solução do workflow reutilizável nem as pipelines já migradas.

Os dois consumidores permanecem no mesmo repositório para reduzir requisitos de acesso. Uma adoção distribuída entre repositórios teria decisões adicionais de referência, versão e permissão. A prática demonstra os mecanismos locais e a migração incremental, não uma governança organizacional completa.
