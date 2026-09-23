import pytest

from delivery_zone_mapper.grid import CityMap, InvalidGridError


def test_mapa_vazio_gera_erro():
    with pytest.raises(InvalidGridError):
        CityMap(grid=[])


def test_linhas_com_tamanhos_diferentes_gera_erro():
    with pytest.raises(InvalidGridError):
        CityMap(grid=[[0, 0], [0]])


def test_is_navigable_retorna_false_fora_do_mapa():
    mapa = CityMap(grid=[[0, 0], [0, 0]])
    assert mapa.is_navigable((-1, 0)) is False
    assert mapa.is_navigable((0, 5)) is False


def test_is_navigable_respeita_obstaculos():
    mapa = CityMap(grid=[[0, 1], [0, 0]])
    assert mapa.is_navigable((0, 0)) is True
    assert mapa.is_navigable((0, 1)) is False


def test_neighbors_ignora_obstaculos_e_bordas():
    mapa = CityMap(grid=[
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 1],
    ])
    vizinhos = set(mapa.neighbors((1, 1)))
    assert vizinhos == {(1, 0), (1, 2), (2, 1)}


def test_rows_e_cols():
    mapa = CityMap(grid=[[0, 0, 0], [0, 0, 0]])
    assert mapa.rows == 2
    assert mapa.cols == 3
