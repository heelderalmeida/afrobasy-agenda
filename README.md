Afrobasy Agenda
Sistema cliente-servidor desenvolvido em Python para o gerenciamento de agendamentos de um salão de beleza.

Projeto desenvolvido para a disciplina Projeto Integrador III-A, com o objetivo de aplicar na prática os conceitos de arquitetura cliente-servidor, comunicação em rede e segurança básica.

Objetivo
O Afrobasy Agenda foi desenvolvido para permitir que clientes consultem serviços e horários disponíveis e realizem solicitações de agendamento de forma simples.

O projeto utiliza uma arquitetura cliente-servidor, na qual o cliente realiza as solicitações e o servidor é responsável pelo processamento e armazenamento das informações.

Funcionalidades
Consultar serviços disponíveis
Consultar horários disponíveis
Solicitar um agendamento
Gerar código de identificação do agendamento
Consultar agendamento pelo código
Cancelar agendamento
Liberar novamente o horário após cancelamento
Validar informações enviadas pelo cliente
Arquitetura
O projeto é dividido em duas aplicações:

CLIENTE.PY
    |
    | Requisições HTTPS
    | GET / POST / DELETE
    v
SERVIDOR.PY
    |
    | Processamento e validações
    v
ARQUIVOS JSON
    |
    |-- servicos.json
    |-- horarios.json
    |-- agendamentos.json
O programa cliente não acessa diretamente os arquivos de dados. Todas as operações são enviadas ao servidor, que processa a solicitação e retorna uma resposta.

Tecnologias utilizadas
Python 3
Flask
Requests
JSON
HTTPS
Chave de API
Estrutura do projeto
afrobasy-agenda/
|
|-- dados/
|   |-- agendamentos.json
|   |-- horarios.json
|   `-- servicos.json
|
|-- cliente.py
|-- servidor.py
|-- resetar_dados.py
|-- requirements.txt
|-- README.md
`-- .gitignore

Segurança
O protótipo utiliza dois mecanismos básicos de proteção:

HTTPS local
A comunicação entre cliente e servidor utiliza HTTPS com certificado local autoassinado.

Chave de API
As requisições protegidas enviam uma chave através do cabeçalho:

X-API-KEY
O servidor verifica a chave antes de processar a solicitação.

Armazenamento
Para manter o projeto simples e focado na arquitetura cliente-servidor, foi utilizado armazenamento em arquivos JSON em vez de banco de dados.

Os dados são divididos em:

servicos.json: serviços cadastrados
horarios.json: horários disponíveis
agendamentos.json: solicitações realizadas
Possíveis melhorias futuras
Banco de dados SQLite ou PostgreSQL
Autenticação de usuários
Painel administrativo
Interface gráfica
Certificado HTTPS válido
Controle automático da agenda
Integração com serviços de mensagens


Autor:
Helder Santos

Projeto Integrador III-A
Análise e Desenvolvimento de Sistemas - PUC Goiás
2026

