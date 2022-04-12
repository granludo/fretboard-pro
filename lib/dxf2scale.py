# Copyright (c) 2022, Manfred Moitzi
# License: MIT License
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt

import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.math import Vec2
from ezdxf.enums import TextEntityAlignment, MTextEntityAlignment







def render_limits(
    origin: tuple[float, float],
    size_in_inches: tuple[float, float],
    scale: float,
) -> tuple[float, float, float, float]:
    """Returns the render limits in drawing units. """
    min_x, min_y = origin
    max_x = min_x + size_in_inches[0] * scale
    max_y = min_y + size_in_inches[1] * scale
    return min_x, min_y, max_x, max_y


def save_to_scale(
    size_in_inches: tuple[float, float] = (8.5, 11),
    origin: tuple[float, float] = (0, 0),  # of modelspace area to render
    scale: float = 1,
    dpi: int = 300,
    filename="filename.pdf"
):
    doc = make_doc(offset=(1, 2), size=(6.5, 8))
    msp = doc.modelspace()
    msp.add_mtext(
        f"scale = 1:{scale}\n"
        f"canvas = {size_in_inches[0]:.1f} inch x {size_in_inches[1]:.1f} inch ",
        dxfattribs={"style": "OpenSans", "char_height": 0.25},
    ).set_location(
        (0.2, 0.2), attachment_point=MTextEntityAlignment.BOTTOM_LEFT
    )

    ctx = RenderContext(doc)
    fig = plt.figure(dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])

    # Get render limits in drawing units:
    min_x, min_y, max_x, max_y = render_limits(
        origin, size_in_inches, scale
    )

    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    out = MatplotlibBackend(ax)
    # Finalizing invokes auto-scaling by default!
    Frontend(ctx, out).draw_layout(msp, finalize=False)

    # Set output size in inches:
    fig.set_size_inches(size_in_inches[0], size_in_inches[1], forward=True)
    fig.savefig(filename, dpi=dpi)
    plt.close(fig)


if __name__ == "__main__":
    save_to_scale(scale=1)
