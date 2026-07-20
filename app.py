import io
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import matplotlib
matplotlib.use("Agg")  # no gui on the server
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from cube import SOLVED, convert_notation, record, run
from scramble_reader import random_scramble
from solver.solve import solve
from visualize import COLORS, cell_coords, setup

INTERVAL = 120


def render_png(frames, stages, scramble, i):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    setup(ax)
    patches = np.empty((6, 3, 3), dtype=object)
    for face, row, col, xy in cell_coords():
        rect = plt.Rectangle(xy, 1, 1, edgecolor="black", linewidth=0.5)
        ax.add_patch(rect)
        patches[face, row, col] = rect

    cube, move = frames[i]
    for patch, side in zip(patches.ravel(), cube.ravel()):
        patch.set_facecolor(COLORS[side])

    ax.text(6, 10.1, scramble, ha="center", fontsize=9, family="monospace")
    ax.text(3, 9.25, f"{i}/{len(frames) - 1}    {move}",
            fontsize=13, family="monospace")
    if stages:  # move i lands the cube in frame i, so it names the stage there
        ax.text(9.5, 1.5, stages[max(i - 1, 0)], ha="center",
                fontsize=18, family="monospace", fontweight="bold")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    return buf.getvalue()


def new_solve():
    cube = SOLVED.copy()
    scramble = random_scramble()
    run(cube, convert_notation(scramble))
    solution, stages = solve(cube)
    frames = record(cube, convert_notation(solution))
    st.session_state.update(scramble=scramble, solution=solution,
                            stages=stages, idx=0, playing=False)
    with st.spinner("Rendering..."):
        st.session_state.images = [
            render_png(frames, stages, scramble, i) for i in range(len(frames))]


st.set_page_config(page_title="Rubik's Cube Solver")
st.title("Rubik's Cube Solver")

if "images" not in st.session_state:
    new_solve()

if st.button("New scramble"):
    new_solve()

st.markdown(f"**Scramble:** `{st.session_state.scramble}`")
st.markdown(f"**Solution ({len(st.session_state.images) - 1} moves):** "
            f"`{st.session_state.solution}`")

last = len(st.session_state.images) - 1
prev, play, nxt, restart = st.columns(4)
if prev.button("Prev"):
    st.session_state.idx = max(0, st.session_state.idx - 1)
    st.session_state.playing = False
if play.button("Play / Pause"):
    if st.session_state.idx >= last:  # replay from the top
        st.session_state.idx = 0
    st.session_state.playing = not st.session_state.playing
if nxt.button("Next"):
    st.session_state.idx = min(last, st.session_state.idx + 1)
    st.session_state.playing = False
if restart.button("Restart"):
    st.session_state.idx = 0
    st.session_state.playing = False

st.caption("Controls: Play / Pause, Prev, Next, Restart")
st.image(st.session_state.images[st.session_state.idx])

# autoplay brrrra braa bra
if st.session_state.playing:
    if st.session_state.idx < last:
        time.sleep(INTERVAL / 1000)
        st.session_state.idx += 1
        st.rerun()
    else:
        st.session_state.playing = False
