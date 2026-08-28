#!/usr/bin/env python3
"""Seleciona a observação METAR mais próxima do Clube 14 BIS."""

import json
import math
import sys
from pathlib import Path

CLUBE_LAT = -20.784833
CLUBE_LON = -49.508769


def distancia_km(observacao):
    raio = 6371
    lat1, lon1 = math.radians(CLUBE_LAT), math.radians(CLUBE_LON)
    lat2, lon2 = math.radians(observacao["lat"]), math.radians(observacao["lon"])
    a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return raio * 2 * math.asin(math.sqrt(a))


entrada, saida = map(Path, sys.argv[1:3])
observacoes = json.loads(entrada.read_text())
mais_recentes = {}
for item in observacoes:
    if item.get("lat") is None or item.get("lon") is None:
        continue
    codigo = item.get("icaoId", "sem-codigo")
    if codigo not in mais_recentes or item.get("obsTime", 0) > mais_recentes[codigo].get("obsTime", 0):
        mais_recentes[codigo] = item

candidatas = list(mais_recentes.values())
if not candidatas:
    raise SystemExit("Nenhuma observação com coordenadas foi recebida.")

metar = min(candidatas, key=distancia_km)
metar["distanceKm"] = round(distancia_km(metar), 1)
metar["source"] = "AviationWeather.gov"
saida.write_text(json.dumps(metar, ensure_ascii=False, indent=2) + "\n")
