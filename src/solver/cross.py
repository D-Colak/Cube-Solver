# cross: drop the daisy's yellow petals down onto the yellow center

from cube import U, YELLOW
from solver.geometry import (
    EDGES,
    TOP_EDGES,
    SIDE_FACES,
    FACE_CHAR,
    DOWN_STICKER,
    notation,
    turns_to,
    cost,
)
from solver.cube_reader import sc, edges_with

GUARD = 100  # safety net; the loop should finish well before this


def side_sticker(name):
    return EDGES[name][1]


def solved(cube):
    for face in SIDE_FACES:
        if sc(cube, DOWN_STICKER[face]) != YELLOW:
            return False
        if sc(cube, side_sticker("D" + FACE_CHAR[face])) != face:
            return False
    return True


def cross(work, do):
    def petals():
        # (edge, the face it belongs on) for every yellow edge still up top
        out = []
        for name, face in edges_with(work, YELLOW):
            if name in TOP_EDGES and face == U:
                out.append((name, sc(work, side_sticker(name))))
        return out

    for _ in range(GUARD):
        if solved(work):
            return

        left = petals()
        if not left:
            break  # nothing to place

        # drop any petal lined up
        ready = [h for n, h in left if turns_to(U, n, h) == 0]
        if ready:
            do(notation(ready[0], 2))
            continue

        # else spin U to bring the closest petal to home face
        name, home = min(left, key=lambda p: cost(turns_to(U, *p)))
        do(notation(U, turns_to(U, name, home)))
