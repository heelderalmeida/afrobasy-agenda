import os
import requests
import urllib3

# O certificado HTTPS é local e autoassinado. O aviso é ocultado apenas neste protótipo acadêmico.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL_BASE = "https://127.0.0.1:5000"
API_KEY = os.getenv("AFROBASY_API_KEY", "afrobasy-chave-2026")
CABECALHOS = {"X-API-KEY": API_KEY}


def requisicao(metodo, rota, **kwargs):
    try:
        resposta = requests.request(
            metodo,
            URL_BASE + rota,
            headers=CABECALHOS,
            verify=False,
            timeout=10,
            **kwargs
        )
        try:
            dados = resposta.json()
        except ValueError:
            dados = {"erro": "O servidor retornou uma resposta inválida."}
        return resposta.status_code, dados
    except requests.exceptions.ConnectionError:
        return 0, {"erro": "Não foi possível conectar. Abra outro terminal e execute servidor.py primeiro."}
    except requests.exceptions.RequestException as erro:
        return 0, {"erro": f"Falha de comunicação: {erro}"}


def titulo(texto):
    print("\n" + "=" * 52)
    print(texto.center(52))
    print("=" * 52)


def mostrar_erro(dados):
    print(f"\nERRO: {dados.get('erro', 'Operação não concluída.')}")


def consultar_servicos():
    titulo("SERVIÇOS AFROBASY")
    status, dados = requisicao("GET", "/servicos")
    if status != 200:
        return mostrar_erro(dados)
    for servico in dados:
        print(f"\nCódigo: {servico['id']}")
        print(f"Serviço: {servico['nome']}")
        print(f"Duração: {servico['duracao']}")
        print(f"Valor: R$ {servico['valor']:.2f}".replace(".", ","))


def consultar_horarios():
    titulo("HORÁRIOS DISPONÍVEIS")
    data = input("Informe a data (DD/MM/AAAA) ou Enter para todas: ").strip()
    rota = "/horarios"
    params = {"data": data} if data else None
    status, dados = requisicao("GET", rota, params=params)
    if status != 200:
        return mostrar_erro(dados)
    if not dados:
        print("\nNenhum horário disponível.")
        return
    for vaga in dados:
        print(f"- {vaga['data']} às {vaga['horario']}")


def solicitar_agendamento():
    titulo("SOLICITAR AGENDAMENTO")
    print("Consulte os serviços e horários antes de continuar.\n")
    dados = {
        "nome": input("Nome da cliente: ").strip(),
        "telefone": input("Telefone com DDD: ").strip(),
        "servico_id": input("Código do serviço: ").strip(),
        "data": input("Data (DD/MM/AAAA): ").strip(),
        "horario": input("Horário (HH:MM): ").strip()
    }
    status, resposta = requisicao("POST", "/agendamentos", json=dados)
    if status != 201:
        return mostrar_erro(resposta)
    print("\nAGENDAMENTO SOLICITADO COM SUCESSO")
    print(f"Código: {resposta['codigo']}")
    print(f"Serviço: {resposta['servico']}")
    print(f"Data: {resposta['data']} às {resposta['horario']}")
    print(f"Status: {resposta['status']}")
    print("Guarde o código para consultar ou cancelar.")


def consultar_agendamento():
    titulo("CONSULTAR AGENDAMENTO")
    codigo = input("Código do agendamento: ").strip()
    status, dados = requisicao("GET", f"/agendamentos/{codigo}")
    if status != 200:
        return mostrar_erro(dados)
    print(f"\nCódigo: {dados['codigo']}")
    print(f"Cliente: {dados['nome']}")
    print(f"Serviço: {dados['servico']}")
    print(f"Data: {dados['data']} às {dados['horario']}")
    print(f"Status: {dados['status']}")


def cancelar_agendamento():
    titulo("CANCELAR AGENDAMENTO")
    codigo = input("Código do agendamento: ").strip()
    confirmacao = input("Confirma o cancelamento? (S/N): ").strip().upper()
    if confirmacao != "S":
        print("Cancelamento interrompido.")
        return
    status, dados = requisicao("DELETE", f"/agendamentos/{codigo}")
    if status != 200:
        return mostrar_erro(dados)
    print("\nAgendamento cancelado com sucesso.")


def menu():
    while True:
        titulo("AFROBASY AGENDA")
        print("1 - Consultar serviços")
        print("2 - Consultar horários disponíveis")
        print("3 - Solicitar agendamento")
        print("4 - Consultar meu agendamento")
        print("5 - Cancelar agendamento")
        print("0 - Sair")
        opcao = input("\nEscolha uma opção: ").strip()
        acoes = {
            "1": consultar_servicos,
            "2": consultar_horarios,
            "3": solicitar_agendamento,
            "4": consultar_agendamento,
            "5": cancelar_agendamento,
        }
        if opcao == "0":
            print("Até logo!")
            break
        acao = acoes.get(opcao)
        if acao:
            acao()
        else:
            print("Opção inválida.")
        input("\nPressione Enter para voltar ao menu...")


if __name__ == "__main__":
    menu()
