"""Delivery Zone Mapper - algoritmos de grafos aplicados a logística de entregas."""

from .bitmap_holes import count_navigable_zones, label_zones
from .delivery import DeliveryRoute, find_delivery_route
from .grid import CityMap, InvalidGridError
from .pathfinder import UnreachableDestinationError, shortest_path

__version__ = "0.1.0"

__all__ = [
    "CityMap",
    "InvalidGridError",
    "DeliveryRoute",
    "find_delivery_route",
    "UnreachableDestinationError",
    "shortest_path",
    "count_navigable_zones",
    "label_zones",
]
