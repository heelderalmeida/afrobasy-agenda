# Afrobasy Agenda

Sistema cliente-servidor desenvolvido em Python para o gerenciamento de agendamentos de um salão de beleza.

Projeto desenvolvido para a disciplina **Projeto Integrador III-A**, do curso de **Análise e Desenvolvimento de Sistemas da PUC Goiás**.

## Sobre o projeto

O Afrobasy Agenda foi desenvolvido com o objetivo de criar uma solução simples para consulta de serviços, horários e solicitações de agendamento.

O principal objetivo acadêmico do projeto é demonstrar, na prática, o funcionamento de uma **arquitetura cliente-servidor**.

O sistema possui duas aplicações:

- `cliente.py`: responsável pela interação com o usuário e pelo envio das solicitações.
- `servidor.py`: responsável por receber as solicitações, processar as regras e acessar os dados.

## Funcionalidades

O sistema permite:

- Consultar serviços disponíveis;
- Consultar horários disponíveis;
- Solicitar um agendamento;
- Gerar um código de identificação para o agendamento;
- Consultar um agendamento pelo código;
- Cancelar um agendamento;
- Liberar novamente o horário após o cancelamento.

## Arquitetura cliente-servidor

O funcionamento do sistema pode ser representado da seguinte forma:

```text
CLIENTE.PY
    |
    | Requisição HTTPS
    | GET / POST / DELETE
    |
    v
SERVIDOR.PY
    |
    | Processamento
    | Validação
    |
    v
ARQUIVOS JSON
    |
    +-- servicos.json
    +-- horarios.json
    +-- agendamentos.json
```

O cliente não acessa diretamente os arquivos de dados.

Todas as solicitações são enviadas ao servidor, que realiza o processamento e retorna uma resposta ao cliente.

## Tecnologias utilizadas

- Python 3
- Flask
- Requests
- JSON
- HTTPS
- Chave de API

## Estrutura do projeto

```text
afrobasy-agenda/
|
+-- dados/
|   +-- agendamentos.json
|   +-- horarios.json
|   +-- servicos.json
|
+-- cliente.py
+-- servidor.py
+-- resetar_dados.py
+-- requirements.txt
+-- README.md
+-- .gitignore
```

## Como executar o projeto

### 1. Criar o ambiente virtual

Abra o terminal na pasta do projeto e execute:

```powershell
py -m venv .venv
```

### 2. Ativar o ambiente virtual

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
py -m pip install -r requirements.txt
```

### 4. Iniciar o servidor

```powershell
py servidor.py
```

O servidor será iniciado localmente em:

```text
https://127.0.0.1:5000
```

Mantenha esse terminal aberto.

### 5. Iniciar o cliente

Abra um segundo terminal e ative novamente o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Depois execute:

```powershell
py cliente.py
```

O menu principal será exibido:

```text
AFROBASY AGENDA

1 - Consultar serviços
2 - Consultar horários disponíveis
3 - Solicitar agendamento
4 - Consultar meu agendamento
5 - Cancelar agendamento
0 - Sair
```

## Armazenamento dos dados

Para manter o projeto simples e focado na arquitetura cliente-servidor, foram utilizados arquivos JSON em vez de banco de dados.

Os arquivos utilizados são:

- `servicos.json`: serviços cadastrados;
- `horarios.json`: horários disponíveis;
- `agendamentos.json`: agendamentos realizados.

## Segurança

O projeto utiliza dois mecanismos básicos de segurança.

### HTTPS

A comunicação entre cliente e servidor é realizada por HTTPS utilizando certificado local autoassinado.

### Chave de API

O cliente envia uma chave de API no cabeçalho:

```text
X-API-KEY
```

O servidor verifica essa chave antes de processar as requisições protegidas.


## Autores

**Helder de Almeida Santos**
**// Breatriz de Freitas Ribeiro de Souza**
**// Eduardo Sales Sousa**

Projeto Integrador III-A  
Análise e Desenvolvimento de Sistemas  
PUC Goiás  
2026
