import pytest

from delivery_zone_mapper.grid import CityMap
from delivery_zone_mapper.pathfinder import UnreachableDestinationError, shortest_path


def test_caminho_em_linha_reta():
    mapa = CityMap(grid=[[0, 0, 0, 0]])
    caminho = shortest_path(mapa, start=(0, 0), goal=(0, 3))
    assert caminho == [(0, 0), (0, 1), (0, 2), (0, 3)]


def test_caminho_contorna_obstaculo():
    mapa = CityMap(grid=[
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ])
    caminho = shortest_path(mapa, start=(0, 0), goal=(0, 2))
    assert caminho[0] == (0, 0)
    assert caminho[-1] == (0, 2)
    assert len(caminho) == 7  # única forma de contornar o "rio" é descer até a linha 2


def test_origem_igual_ao_destino():
    mapa = CityMap(grid=[[0, 0], [0, 0]])
    assert shortest_path(mapa, start=(0, 0), goal=(0, 0)) == [(0, 0)]


def test_destino_inalcancavel_gera_erro():
    mapa = CityMap(grid=[
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ])
    with pytest.raises(UnreachableDestinationError):
        shortest_path(mapa, start=(0, 0), goal=(2, 2))


def test_partida_em_obstaculo_gera_erro():
    mapa = CityMap(grid=[[1, 0], [0, 0]])
    with pytest.raises(ValueError):
        shortest_path(mapa, start=(0, 0), goal=(1, 1))


def test_caminho_e_realmente_o_mais_curto():
    # duas rotas possíveis: uma direta (mais curta) e um desvio mais longo
    mapa = CityMap(grid=[
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
    ])
    caminho = shortest_path(mapa, start=(0, 0), goal=(2, 0))
    # única passagem entre as duas metades do mapa é a coluna 2 (linha 1 = [1, 1, 0])
    assert len(caminho) == 7
    assert (1, 2) in caminho
