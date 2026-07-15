import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from cube import U, L, F, R, B, D

DRAW_OFFSETS = {
    U: (3, 6),
    L: (0, 3),
    F: (3, 3),
    R: (6, 3),
    B: (9, 3),
    D: (3, 0),
}


def draw(cube, colors):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal")
    ax.axis("off")

    for face in range(6):
        off_x, off_y = DRAW_OFFSETS[face]
        for row in range(3):
            for col in range(3):
                # here is draw
                ax.add_patch(
                    plt.Rectangle(
                        (off_x + col, off_y + (2 - row)),
                        1,
                        1,
                        facecolor=colors[cube[face, row, col]],
                        edgecolor="black",
                        linewidth=0.5,
                    )
                )

    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-0.5, 9.5)
    return fig


def animate_frame(i, frames, colors, patches, label):
    cube, move = frames[i]
    # match patches and cube sides
    for patch, side in zip(patches.ravel(), cube.ravel()):
        patch.set_facecolor(colors[side])
    label.set_text(f"{i}/{len(frames) - 1}    {move}")
    return [*patches.ravel(), label]


def animate(frames, colors, interval=400):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal")
    ax.axis("off")

    # build the patches
    patches = np.empty((6, 3, 3), dtype=object)
    for face in range(6):
        off_x, off_y = DRAW_OFFSETS[face]
        for row in range(3):
            for col in range(3):
                rect = plt.Rectangle(
                    (off_x + col, off_y + (2 - row)),
                    1,
                    1,
                    edgecolor="black",
                    linewidth=0.5,
                )
                ax.add_patch(rect)
                patches[face, row, col] = rect

    label = ax.text(3, 9.25, "", fontsize=14, family="monospace")

    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-0.5, 9.5)

    ani = animation.FuncAnimation(
        fig,
        animate_frame,
        frames=len(frames),
        fargs=(frames, colors, patches, label),
        interval=interval,
        repeat=False,
    )
    return ani
