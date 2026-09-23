import pytest

from delivery_zone_mapper.delivery import find_delivery_route
from delivery_zone_mapper.grid import CityMap
from delivery_zone_mapper.pathfinder import UnreachableDestinationError


def test_rota_encontrada_com_sucesso():
    mapa = CityMap(grid=[
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ])
    rota = find_delivery_route(mapa, restaurant=(0, 0), client=(2, 2))
    assert rota.path[0] == (0, 0)
    assert rota.path[-1] == (2, 2)
    assert rota.distance == len(rota.path) - 1


def test_rota_impossivel_entre_zonas_diferentes():
    mapa = CityMap(grid=[
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ])
    with pytest.raises(UnreachableDestinationError):
        find_delivery_route(mapa, restaurant=(0, 0), client=(2, 2))


def test_restaurante_fora_do_mapa_gera_erro():
    mapa = CityMap(grid=[[0, 0], [0, 0]])
    with pytest.raises(ValueError):
        find_delivery_route(mapa, restaurant=(5, 5), client=(0, 0))


def test_cliente_em_obstaculo_gera_erro():
    mapa = CityMap(grid=[[0, 1], [0, 0]])
    with pytest.raises(ValueError):
        find_delivery_route(mapa, restaurant=(0, 0), client=(0, 1))
