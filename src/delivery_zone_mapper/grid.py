"""
grid.py

Abstração do mapa da cidade usada pelo restante do projeto.

Decisão de arquitetura: CityMap é um dataclass imutável (frozen=True). Um
mapa de entregas não deveria mudar "por baixo dos panos" depois de criado —
se uma via for cortada ou um novo obstáculo aparecer, o correto é construir
um novo CityMap, e não mutar o existente. Isso evita uma classe inteira de
bugs sutis em que uma parte do código altera o mapa e outra, que guardou
uma referência antiga, passa a operar sobre dados inconsistentes.

(Nota: frozen=True impede reatribuir `city_map.grid`, mas não impede mutar
os elementos internos da lista. Para imutabilidade completa seria preciso
converter para tuplas de tuplas — optei por não fazer isso para manter a
interface simples de usar com listas comuns.)
"""

from dataclasses import dataclass
from typing import Iterator, List, Tuple

from .bitmap_holes import FREE, OBSTACLE

Grid = List[List[int]]
Coordinate = Tuple[int, int]

_FOUR_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class InvalidGridError(ValueError):
    """Mapa inválido: vazio ou com linhas de tamanhos diferentes."""


@dataclass(frozen=True)
class CityMap:
    """Mapa da cidade representado como matriz binária (0 = livre, 1 = obstáculo)."""

    grid: Grid

    def __post_init__(self) -> None:
        if not self.grid or not self.grid[0]:
            raise InvalidGridError("O mapa não pode estar vazio.")
        largura = len(self.grid[0])
        if any(len(linha) != largura for linha in self.grid):
            raise InvalidGridError("Todas as linhas do mapa devem ter o mesmo tamanho.")

    @property
    def rows(self) -> int:
        return len(self.grid)

    @property
    def cols(self) -> int:
        return len(self.grid[0])

    def is_inside(self, pos: Coordinate) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_navigable(self, pos: Coordinate) -> bool:
        if not self.is_inside(pos):
            return False
        r, c = pos
        return self.grid[r][c] == FREE

    def neighbors(self, pos: Coordinate) -> Iterator[Coordinate]:
        """Vizinhos navegáveis em 4 direções (cima, baixo, esquerda, direita)."""
        r, c = pos
        for dr, dc in _FOUR_DIRECTIONS:
            candidate = (r + dr, c + dc)
            if self.is_navigable(candidate):
                yield candidate
