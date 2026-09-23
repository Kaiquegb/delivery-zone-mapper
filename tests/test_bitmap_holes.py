from delivery_zone_mapper.bitmap_holes import count_navigable_zones


def test_mapa_totalmente_livre_eh_uma_unica_zona():
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    assert count_navigable_zones(grid) == 1


def test_mapa_totalmente_bloqueado_nao_tem_zonas():
    grid = [
        [1, 1],
        [1, 1],
    ]
    assert count_navigable_zones(grid) == 0


def test_conta_zonas_separadas_por_obstaculos():
    grid = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]
    # quatro cantos livres, todos isolados entre si pelos obstáculos
    assert count_navigable_zones(grid) == 4


def test_zona_em_formato_de_l_conta_como_uma_so():
    grid = [
        [0, 0, 1],
        [1, 0, 1],
        [1, 0, 0],
    ]
    assert count_navigable_zones(grid) == 1


def test_mapa_vazio():
    assert count_navigable_zones([]) == 0
