"""
cli.py

Interface de linha de comando do Delivery Zone Mapper. Gera um mapa
aleatório e mostra, direto no terminal, a rota calculada entre o
restaurante e o cliente.

Exemplo de uso:
    python -m delivery_zone_mapper.cli --rows 10 --cols 20 --obstacle-rate 0.25 --seed 42
"""

import argparse
import random
from typing import List

from .bitmap_holes import FREE, OBSTACLE
from .delivery import find_delivery_route
from .grid import CityMap, Coordinate
from .pathfinder import UnreachableDestinationError


def generate_random_grid(
    rows: int, cols: int, obstacle_rate: float, rng: random.Random
) -> List[List[int]]:
    """Gera uma matriz aleatória, respeitando a proporção de obstáculos pedida."""
    return [
        [OBSTACLE if rng.random() < obstacle_rate else FREE for _ in range(cols)]
        for _ in range(rows)
    ]


def _random_navigable_cell(city_map: CityMap, rng: random.Random) -> Coordinate:
    livres = [
        (r, c)
        for r in range(city_map.rows)
        for c in range(city_map.cols)
        if city_map.is_navigable((r, c))
    ]
    if not livres:
        raise ValueError("O mapa gerado não tem nenhuma célula navegável.")
    return rng.choice(livres)


def render_map(
    city_map: CityMap, path: List[Coordinate], restaurant: Coordinate, client: Coordinate
) -> str:
    """Renderiza o mapa em ASCII, marcando obstáculos, rota, restaurante e cliente."""
    path_cells = set(path)
    linhas = []
    for r in range(city_map.rows):
        linha = []
        for c in range(city_map.cols):
            pos = (r, c)
            if pos == restaurant:
                simbolo = "R"
            elif pos == client:
                simbolo = "C"
            elif pos in path_cells:
                simbolo = "*"
            elif not city_map.is_navigable(pos):
                simbolo = "#"
            else:
                simbolo = "."
            linha.append(simbolo)
        linhas.append(" ".join(linha))
    return "\n".join(linhas)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera um mapa aleatório e calcula a rota de entrega mais curta (BFS)."
    )
    parser.add_argument("--rows", type=int, default=10, help="Número de linhas do mapa.")
    parser.add_argument("--cols", type=int, default=15, help="Número de colunas do mapa.")
    parser.add_argument(
        "--obstacle-rate",
        type=float,
        default=0.2,
        help="Proporção de células que viram obstáculo (0.0 a 1.0).",
    )
    parser.add_argument("--seed", type=int, default=None, help="Seed para reprodutibilidade.")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    grid = generate_random_grid(args.rows, args.cols, args.obstacle_rate, rng)

    try:
        city_map = CityMap(grid=grid)
        restaurant = _random_navigable_cell(city_map, rng)
        client = _random_navigable_cell(city_map, rng)
    except ValueError as erro:
        print(f"Não foi possível gerar um mapa válido: {erro}")
        return

    print(f"Restaurante em {restaurant}, cliente em {client}\n")

    try:
        rota = find_delivery_route(city_map, restaurant, client)
        print(render_map(city_map, rota.path, restaurant, client))
        print(f"\nRota encontrada! Distância: {rota.distance} passos.")
    except UnreachableDestinationError as erro:
        print(render_map(city_map, [], restaurant, client))
        print(f"\n{erro}")


if __name__ == "__main__":
    main()
