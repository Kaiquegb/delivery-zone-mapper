from delivery_zone_mapper.bitmap_holes import count_navigable_zones, label_zones


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


def test_label_zones_rotula_obstaculos_com_menos_um():
    grid = [
        [0, 1],
        [0, 0],
    ]
    label_grid, num_zonas = label_zones(grid)
    assert num_zonas == 1
    assert label_grid[0][1] == -1


def test_label_zones_da_rotulos_diferentes_a_zonas_diferentes():
    grid = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]
    label_grid, num_zonas = label_zones(grid)
    assert num_zonas == 4
    rotulos = {label_grid[0][0], label_grid[0][2], label_grid[2][0], label_grid[2][2]}
    assert len(rotulos) == 4  # os quatro cantos pertencem a zonas distintas


def test_label_zones_da_mesmo_rotulo_para_mesma_zona():
    grid = [
        [0, 0, 1],
        [1, 0, 1],
        [1, 0, 0],
    ]
    label_grid, _ = label_zones(grid)
    assert label_grid[0][0] == label_grid[2][2]  # zona em L: mesmo rótulo do início ao fim
