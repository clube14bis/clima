#!/usr/bin/env python3
"""Converte a resposta autenticada da REDEMET em um arquivo público seguro."""

import json
import sys
from pathlib import Path


entrada, saida = map(Path, sys.argv[1:3])
resposta = json.loads(entrada.read_text())
itens = resposta.get("data", {}).get("data", [])
if not resposta.get("status") or not itens:
    raise SystemExit("A REDEMET não retornou um METAR para o aeroporto solicitado.")

mais_recente = max(itens, key=lambda item: item.get("recebimento", ""))
resultado = {
    "aeroporto": "São José do Rio Preto — SP",
    "validade": mais_recente.get("validade_inicial"),
    "recebimento": mais_recente.get("recebimento"),
    "metar": mais_recente.get("mens", "").strip(),
    "fonte": "REDEMET · DECEA",
}
saida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n")
