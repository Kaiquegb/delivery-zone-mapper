"""
pathfinder.py

Busca do caminho mais curto entre dois pontos navegáveis do mapa, usando
Busca em Largura (BFS).

Decisão de arquitetura: BFS, e não DFS, é o algoritmo certo aqui. O mapa é
um grafo não-ponderado — mover para qualquer célula vizinha custa sempre
"1 passo". Nesse cenário, BFS garante que a primeira vez que o algoritmo
alcança o destino, ele o alcança pelo caminho mais curto possível. DFS
encontraria *um* caminho, mas sem essa garantia.

Decisão de arquitetura: a fila é um collections.deque, não uma list.
list.pop(0) é O(n), porque o Python precisa realocar todos os elementos
restantes; deque.popleft() é O(1). Em mapas grandes, com filas de milhares
de células, essa troca muda a complexidade total da busca de O(n²) para O(n).
"""

from collections import deque
from typing import Dict, List, Optional

from .grid import CityMap, Coordinate


class UnreachableDestinationError(Exception):
    """Não existe caminho navegável entre origem e destino."""


def shortest_path(city_map: CityMap, start: Coordinate, goal: Coordinate) -> List[Coordinate]:
    """
    Retorna o caminho mais curto (lista de coordenadas, incluindo start e
    goal) entre `start` e `goal`, usando BFS.

    Raises:
        ValueError: se `start` ou `goal` não forem células navegáveis.
        UnreachableDestinationError: se não existir caminho entre os dois pontos.
    """
    if not city_map.is_navigable(start):
        raise ValueError(f"Ponto de partida {start} não é navegável.")
    if not city_map.is_navigable(goal):
        raise ValueError(f"Destino {goal} não é navegável.")

    if start == goal:
        return [start]

    queue: deque = deque([start])
    came_from: Dict[Coordinate, Optional[Coordinate]] = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            return _reconstruct_path(came_from, goal)

        for neighbor in city_map.neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    raise UnreachableDestinationError(
        f"Não existe caminho navegável entre {start} e {goal}."
    )


def _reconstruct_path(
    came_from: Dict[Coordinate, Optional[Coordinate]], goal: Coordinate
) -> List[Coordinate]:
    path = [goal]
    while came_from[path[-1]] is not None:
        path.append(came_from[path[-1]])
    path.reverse()
    return path
