"""
Gera uma imagem estática (PNG) ilustrando o mapa de exemplo e a rota
calculada, para usar no README.

Rode com:
    python examples/generate_preview_image.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import matplotlib
matplotlib.use("Agg")  # backend sem display, necessário em ambiente headless
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from delivery_zone_mapper import CityMap, find_delivery_route
from example_run import CLIENTE, MAPA_DO_BAIRRO, RESTAURANTE

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "assets" / "example_route.png"

CORES = {
    "restaurante": "#FF7A45",
    "cliente": "#2DD4BF",
    "rota": "#FFC857",
    "obstaculo": "#0B0F14",
    "livre": "#1E2A38",
}


def main() -> None:
    mapa = CityMap(grid=MAPA_DO_BAIRRO)
    rota = find_delivery_route(mapa, RESTAURANTE, CLIENTE)
    path_cells = set(rota.path)

    rows, cols = mapa.rows, mapa.cols
    fig, ax = plt.subplots(figsize=(cols / 1.6, rows / 1.6))
    fig.patch.set_facecolor("#0F1620")

    for r in range(rows):
        for c in range(cols):
            if (r, c) == RESTAURANTE:
                cor = CORES["restaurante"]
            elif (r, c) == CLIENTE:
                cor = CORES["cliente"]
            elif (r, c) in path_cells:
                cor = CORES["rota"]
            elif not mapa.is_navigable((r, c)):
                cor = CORES["obstaculo"]
            else:
                cor = CORES["livre"]
            ax.add_patch(
                patches.FancyBboxPatch(
                    (c + 0.06, rows - r - 1 + 0.06),
                    0.88,
                    0.88,
                    boxstyle="round,pad=0,rounding_size=0.08",
                    facecolor=cor,
                    edgecolor="#0F1620",
                    linewidth=1.5,
                )
            )

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        f"Rota calculada com BFS — {rota.distance} passos",
        fontsize=12,
        color="#E7EDF5",
        family="monospace",
        pad=12,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight", facecolor="#0F1620")
    print(f"Imagem salva em {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
