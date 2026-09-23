"""
delivery.py

Camada de mais alto nível do projeto: junta a rotulagem de zonas
(bitmap_holes.label_zones) com a busca do caminho mais curto
(pathfinder.shortest_path) para responder à pergunta que interessa ao
negócio: "existe uma rota de entrega entre o restaurante e o cliente e,
se existir, qual é ela?"

Decisão de arquitetura: antes de rodar BFS (O(linhas*colunas) no pior
caso), fazemos uma checagem O(1) usando o mapa de zonas pré-calculado.
Se restaurante e cliente já nascem em zonas diferentes, sabemos
imediatamente que não há rota possível, sem gastar tempo procurando um
caminho que sabemos que não existe. Num mapa de cidade real, com rios e
vias cortadas criando várias zonas isoladas, essa checagem evita buscas
caras e desnecessárias.
"""

from dataclasses import dataclass
from typing import List

from .bitmap_holes import label_zones
from .grid import CityMap, Coordinate
from .pathfinder import UnreachableDestinationError, shortest_path


@dataclass
class DeliveryRoute:
    """Resultado de uma consulta de rota de entrega."""

    path: List[Coordinate]

    @property
    def distance(self) -> int:
        """Número de passos até o destino (não conta a célula de partida)."""
        return len(self.path) - 1


def find_delivery_route(
    city_map: CityMap, restaurant: Coordinate, client: Coordinate
) -> DeliveryRoute:
    """
    Calcula a rota de entrega mais curta entre `restaurant` e `client`.

    Raises:
        ValueError: se alguma das coordenadas não for navegável.
        UnreachableDestinationError: se restaurante e cliente estiverem em
            zonas desconectadas do mapa.
    """
    if not city_map.is_navigable(restaurant):
        raise ValueError(f"Restaurante em {restaurant} não é uma posição navegável.")
    if not city_map.is_navigable(client):
        raise ValueError(f"Cliente em {client} não é uma posição navegável.")

    label_grid, _ = label_zones(city_map.grid)

    if not _same_zone(label_grid, restaurant, client):
        raise UnreachableDestinationError(
            f"Restaurante {restaurant} e cliente {client} estão em zonas "
            "desconectadas do mapa — não existe rota possível."
        )

    path = shortest_path(city_map, restaurant, client)
    return DeliveryRoute(path=path)


def _same_zone(label_grid: List[List[int]], a: Coordinate, b: Coordinate) -> bool:
    ra, ca = a
    rb, cb = b
    label_a = label_grid[ra][ca]
    label_b = label_grid[rb][cb]
    return label_a != -1 and label_a == label_b
