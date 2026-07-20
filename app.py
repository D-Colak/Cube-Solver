import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import streamlit as st

from cube import SOLVED, convert_notation, record, run
from scramble_reader import random_scramble
from solver.solve import solve
from visualize import COLORS, cell_coords, setup


def new_solve():
    """Scramble a fresh cube, solve it, and stash the frames in the session."""
    cube = SOLVED.copy()
    scramble = random_scramble()
    run(cube, convert_notation(scramble))
    solution, stages = solve(cube)
    frames = record(cube, convert_notation(solution))
    st.session_state.update(
        scramble=scramble, solution=solution, stages=stages,
        frames=frames, gif=None,
    )


def make_net(figsize=(7, 5.5)):
    # one rectangle per facelet in the unfolded net, same layout as visualize.py
    fig, ax = plt.subplots(figsize=figsize)
    setup(ax)
    patches = np.empty((6, 3, 3), dtype=object)
    for face, row, col, xy in cell_coords():
        rect = plt.Rectangle(xy, 1, 1, edgecolor="black", linewidth=0.5)
        ax.add_patch(rect)
        patches[face, row, col] = rect
    ax.text(6, 10.1, st.session_state.scramble, ha="center",
            fontsize=9, family="monospace")
    return fig, ax, patches


def paint(patches, cube):
    for patch, side in zip(patches.ravel(), cube.ravel()):
        patch.set_facecolor(COLORS[side])


def frame_figure(i):
    """A static figure of solution frame i, for the slider view."""
    frames, stages = st.session_state.frames, st.session_state.stages
    fig, ax, patches = make_net()
    cube, move = frames[i]
    paint(patches, cube)
    ax.text(3, 9.25, f"{i}/{len(frames) - 1}    {move}",
            fontsize=13, family="monospace")
    if stages:  # move i lands the cube in frame i, so it names the stage there
        ax.text(9.5, 1.5, stages[max(i - 1, 0)], ha="center",
                fontsize=18, family="monospace", fontweight="bold")
    return fig


def build_gif(interval_ms):
    """Render the whole solve to animated-GIF bytes."""
    frames, stages = st.session_state.frames, st.session_state.stages
    fig, ax, patches = make_net()
    label = ax.text(3, 9.25, "", fontsize=13, family="monospace")
    stage_label = ax.text(9.5, 1.5, "", ha="center", fontsize=18,
                          family="monospace", fontweight="bold")

    def update(i):
        cube, move = frames[i]
        paint(patches, cube)
        label.set_text(f"{i}/{len(frames) - 1}    {move}")
        stage_label.set_text(stages[max(i - 1, 0)] if stages else "")
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=interval_ms)
    # PillowWriter needs a real path, not a buffer, so round-trip a temp file
    fd, path = tempfile.mkstemp(suffix=".gif")
    os.close(fd)
    try:
        ani.save(path, writer=PillowWriter(fps=max(1, round(1000 / interval_ms))))
        return Path(path).read_bytes()
    finally:
        plt.close(fig)
        os.unlink(path)


st.set_page_config(page_title="Rubik's Cube Solver", page_icon="🧩")
st.title("🧩 Rubik's Cube Solver")

if "frames" not in st.session_state:
    new_solve()

if st.button("🎲 New scramble"):
    new_solve()

st.markdown(f"**Scramble:** `{st.session_state.scramble}`")
st.markdown(f"**Solution ({len(st.session_state.frames) - 1} moves):** "
            f"`{st.session_state.solution}`")

mode = st.radio("View", ["Step through", "Autoplay"], horizontal=True)

if mode == "Step through":
    last = len(st.session_state.frames) - 1
    i = st.slider("Move", 0, last, 0)
    st.pyplot(frame_figure(i))
    plt.close("all")
else:
    speed = st.select_slider(
        "Speed (ms per move)", options=[80, 120, 200, 350, 600], value=120)
    if st.session_state.get("gif") is None or st.session_state.get("gif_speed") != speed:
        with st.spinner("Rendering animation…"):
            st.session_state.gif = build_gif(speed)
            st.session_state.gif_speed = speed
    st.image(st.session_state.gif)
