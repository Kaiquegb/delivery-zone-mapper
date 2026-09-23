"""
Exemplo de uso ponta-a-ponta do Delivery Zone Mapper.

Rode com:
    python examples/example_run.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from delivery_zone_mapper import CityMap, find_delivery_route
from delivery_zone_mapper.pathfinder import UnreachableDestinationError

# 0 = zona navegável | 1 = obstáculo (rio, via cortada etc.)
MAPA_DO_BAIRRO = [
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 1, 0],
    [1, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

RESTAURANTE = (0, 0)
CLIENTE = (5, 7)


def main() -> None:
    mapa = CityMap(grid=MAPA_DO_BAIRRO)

    try:
        rota = find_delivery_route(mapa, RESTAURANTE, CLIENTE)
    except UnreachableDestinationError as erro:
        print(erro)
        return

    print(f"Restaurante: {RESTAURANTE}")
    print(f"Cliente: {CLIENTE}")
    print(f"Distância da rota: {rota.distance} passos")
    print(f"Caminho: {rota.path}")


if __name__ == "__main__":
    main()
