import json
from pathlib import Path
BASE = Path(__file__).resolve().parent / "dados"
horarios = [
    {"data": "10/11/2026", "horario": "09:00", "disponivel": True},
    {"data": "10/11/2026", "horario": "13:00", "disponivel": True},
    {"data": "10/11/2026", "horario": "15:00", "disponivel": True},
    {"data": "11/11/2026", "horario": "09:00", "disponivel": True},
    {"data": "11/11/2026", "horario": "14:00", "disponivel": True},
    {"data": "12/11/2026", "horario": "10:00", "disponivel": True}
]
(BASE / "horarios.json").write_text(json.dumps(horarios, ensure_ascii=False, indent=2), encoding="utf-8")
(BASE / "agendamentos.json").write_text("[]", encoding="utf-8")
print("Dados de demonstração restaurados.")
