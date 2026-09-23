"""
bitmap_holes.py

Algoritmo base do projeto: dado um mapa binário (matriz de 0s e 1s), conta
quantas zonas navegáveis (regiões conectadas de células livres) existem.

Esta é a evolução direta do desafio "Bitmap Holes": em vez de apenas contar
"buracos" numa imagem binária, aqui cada região conectada de zeros vira uma
zona de entrega isolada do resto do mapa.

Decisão de arquitetura: a DFS é iterativa, com uma pilha explícita (uma
`list` usada como stack), em vez de recursiva. Uma DFS recursiva usa a pilha
de chamadas do próprio Python, que tem um limite padrão de 1000 níveis
(sys.getrecursionlimit()). Um mapa de cidade real — por exemplo 200x200
células — estouraria esse limite com facilidade numa zona grande e serpenteada.
Uma pilha manual evita esse problema por completo, ao custo de um código
levemente mais verboso do que a versão recursiva.
"""

from typing import List, Set, Tuple

Grid = List[List[int]]
Coordinate = Tuple[int, int]

FREE = 0
OBSTACLE = 1


def count_navigable_zones(grid: Grid) -> int:
    """
    Conta quantas zonas navegáveis (regiões 4-conectadas de células livres)
    existem no mapa.

    Args:
        grid: matriz onde 0 = célula navegável e 1 = obstáculo.

    Returns:
        Número de zonas navegáveis desconectadas entre si.
    """
    return len(_find_all_zones(grid))


def _find_all_zones(grid: Grid) -> List[Set[Coordinate]]:
    """Retorna a lista de zonas do mapa, cada uma como um conjunto de coordenadas."""
    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])
    visited: Set[Coordinate] = set()
    zones: List[Set[Coordinate]] = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == FREE and (r, c) not in visited:
                zone = _flood_fill(grid, (r, c))
                visited |= zone
                zones.append(zone)

    return zones


def _flood_fill(grid: Grid, start: Coordinate) -> Set[Coordinate]:
    """DFS iterativa (com pilha) que retorna todas as células conectadas a `start`."""
    rows, cols = len(grid), len(grid[0])
    stack = [start]
    zone: Set[Coordinate] = set()

    while stack:
        r, c = stack.pop()
        if (r, c) in zone:
            continue
        if not (0 <= r < rows and 0 <= c < cols):
            continue
        if grid[r][c] != FREE:
            continue

        zone.add((r, c))
        stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])

    return zone
