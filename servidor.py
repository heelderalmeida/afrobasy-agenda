import json
import os
import secrets
from datetime import datetime
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, request

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dados"
API_KEY = os.getenv("AFROBASY_API_KEY", "afrobasy-chave-2026")
lock = Lock()


def carregar_json(nome_arquivo):
    caminho = DATA_DIR / nome_arquivo
    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_json(nome_arquivo, dados):
    caminho = DATA_DIR / nome_arquivo
    temporario = caminho.with_suffix(".tmp")
    with temporario.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    temporario.replace(caminho)


@app.before_request
def validar_chave_api():
    # Permite a rota inicial sem chave, apenas para teste de disponibilidade.
    if request.path == "/":
        return None
    chave_recebida = request.headers.get("X-API-KEY", "")
    if not secrets.compare_digest(chave_recebida, API_KEY):
        return jsonify({"erro": "Acesso não autorizado. Chave de API inválida."}), 401
    return None


@app.get("/")
def inicio():
    return jsonify({"sistema": "Afrobasy Agenda", "status": "online"})


@app.get("/servicos")
def listar_servicos():
    return jsonify(carregar_json("servicos.json"))


@app.get("/horarios")
def listar_horarios():
    data = request.args.get("data", "").strip()
    horarios = carregar_json("horarios.json")
    if data:
        horarios = [item for item in horarios if item["data"] == data]
    disponiveis = [item for item in horarios if item["disponivel"]]
    return jsonify(disponiveis)


def validar_agendamento(dados):
    obrigatorios = ["nome", "telefone", "servico_id", "data", "horario"]
    ausentes = [campo for campo in obrigatorios if str(dados.get(campo, "")).strip() == ""]
    if ausentes:
        return f"Campos obrigatórios ausentes: {', '.join(ausentes)}"
    nome = str(dados["nome"]).strip()
    telefone = "".join(c for c in str(dados["telefone"]) if c.isdigit())
    if len(nome) < 3:
        return "O nome deve ter pelo menos 3 caracteres."
    if len(telefone) not in (10, 11):
        return "O telefone deve conter 10 ou 11 números."
    try:
        datetime.strptime(str(dados["data"]), "%d/%m/%Y")
        datetime.strptime(str(dados["horario"]), "%H:%M")
        int(dados["servico_id"])
    except ValueError:
        return "Serviço, data ou horário em formato inválido. Use DD/MM/AAAA e HH:MM."
    return None


@app.post("/agendamentos")
def criar_agendamento():
    dados = request.get_json(silent=True) or {}
    erro = validar_agendamento(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    servicos = carregar_json("servicos.json")
    servico = next((s for s in servicos if s["id"] == int(dados["servico_id"])), None)
    if not servico:
        return jsonify({"erro": "Serviço não encontrado."}), 404

    with lock:
        horarios = carregar_json("horarios.json")
        vaga = next((h for h in horarios if h["data"] == dados["data"] and h["horario"] == dados["horario"]), None)
        if not vaga:
            return jsonify({"erro": "Data e horário não cadastrados."}), 404
        if not vaga["disponivel"]:
            return jsonify({"erro": "Esse horário já está ocupado."}), 409

        agendamentos = carregar_json("agendamentos.json")
        codigo = "AFB-" + secrets.token_hex(3).upper()
        telefone = "".join(c for c in str(dados["telefone"]) if c.isdigit())
        novo = {
            "codigo": codigo,
            "nome": str(dados["nome"]).strip(),
            "telefone": telefone,
            "servico_id": servico["id"],
            "servico": servico["nome"],
            "data": dados["data"],
            "horario": dados["horario"],
            "status": "Pendente",
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        agendamentos.append(novo)
        vaga["disponivel"] = False
        salvar_json("agendamentos.json", agendamentos)
        salvar_json("horarios.json", horarios)

    return jsonify(novo), 201


@app.get("/agendamentos/<codigo>")
def consultar_agendamento(codigo):
    agendamentos = carregar_json("agendamentos.json")
    item = next((a for a in agendamentos if a["codigo"].upper() == codigo.upper()), None)
    if not item:
        return jsonify({"erro": "Agendamento não encontrado."}), 404
    return jsonify(item)


@app.delete("/agendamentos/<codigo>")
def cancelar_agendamento(codigo):
    with lock:
        agendamentos = carregar_json("agendamentos.json")
        item = next((a for a in agendamentos if a["codigo"].upper() == codigo.upper()), None)
        if not item:
            return jsonify({"erro": "Agendamento não encontrado."}), 404
        if item["status"] == "Cancelado":
            return jsonify({"erro": "O agendamento já está cancelado."}), 409
        item["status"] = "Cancelado"
        horarios = carregar_json("horarios.json")
        vaga = next((h for h in horarios if h["data"] == item["data"] and h["horario"] == item["horario"]), None)
        if vaga:
            vaga["disponivel"] = True
        salvar_json("agendamentos.json", agendamentos)
        salvar_json("horarios.json", horarios)
    return jsonify({"mensagem": "Agendamento cancelado com sucesso.", "agendamento": item})


if __name__ == "__main__":
    print("Servidor Afrobasy iniciado em https://127.0.0.1:5000")
    print("Mantenha esta janela aberta enquanto usar o cliente.")
    app.run(host="127.0.0.1", port=5000, debug=False, ssl_context="adhoc")
