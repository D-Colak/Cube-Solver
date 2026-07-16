import numpy as np
import matplotlib.pyplot as plt

from cube import U, L, F, R, B, D

# a facelet holds a face index, so this doubles as the color lookup
# TODO - cut face colors
FACE_COLORS = {F: "green", U: "white", L: "orange", D: "yellow", R: "red", B: "blue"}
COLORS = [FACE_COLORS[face] for face in range(6)]

HELP = "space play/pause    <- -> step    r stop    q quit"

DRAW_OFFSETS = {
    U: (3, 6),
    L: (0, 3),
    F: (3, 3),
    R: (6, 3),
    B: (9, 3),
    D: (3, 0),
}


def setup(ax):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-0.5, 10.5)  # headroom above the net for the scramble


def cell_coords():
    # (face, row, col, (x, y)) for every facelet in the unfolded net
    coords = []
    for face in range(6):
        off_x, off_y = DRAW_OFFSETS[face]
        for row in range(3):
            for col in range(3):
                coords.append((face, row, col, (off_x + col, off_y + (2 - row))))

    return coords

# animation class
class Player:
    # TODO - maybe cut draw injection?
    def __init__(self, n, draw):
        self.last = n - 1
        self.i = 0
        self.playing = True
        self.draw = draw

    def seek(self, j):
        self.i = min(max(j, 0), self.last)
        self.playing = False
        self.draw()

    def tick(self): # "frame" of animation
        if not self.playing:
            return
        if self.i < self.last:
            self.i += 1
        else:
            self.playing = False  # end of loop
        self.draw()

    def on_key(self, event):
        if event.key == " ":
            if self.i >= self.last:
                self.i = 0  # replay from top
            self.playing = not self.playing
            self.draw()
        elif event.key == "right":
            self.seek(self.i + 1)
        elif event.key == "left":
            self.seek(self.i - 1)
        elif event.key == "r":
            self.seek(0)


def animate(frames, interval=400, scramble=""):
    fig, ax = plt.subplots(figsize=(8, 6))
    setup(ax)

    # build the patches
    patches = np.empty((6, 3, 3), dtype=object)
    for face, row, col, xy in cell_coords():
        rect = plt.Rectangle(xy, 1, 1, edgecolor="black", linewidth=0.5)
        ax.add_patch(rect)
        patches[face, row, col] = rect

    ax.text(6, 10.1, scramble, ha="center", fontsize=10, family="monospace")
    label = ax.text(3, 9.25, "", fontsize=14, family="monospace")
    ax.text(3, -0.35, HELP, fontsize=9, family="monospace", color="0.45")

    def draw():
        cube, move = frames[player.i]
        for patch, side in zip(patches.ravel(), cube.ravel()):
            patch.set_facecolor(COLORS[side])
        status = "" if player.playing else "[paused]"
        label.set_text(f"{player.i}/{player.last}    {move}    {status}")
        fig.canvas.draw_idle()  # repaint now, not on next tick

    player = Player(len(frames), draw)
    fig.canvas.mpl_connect("key_press_event", player.on_key)

    timer = fig.canvas.new_timer(interval)
    timer.add_callback(player.tick)
    timer.start()
    draw()
    return timer  # caller keeps this alive
