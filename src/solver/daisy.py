# daisy: build the yellow petals -- four yellow edges around the white U center

from cube import U, D, YELLOW, WHITE, FACE_OF
from solver.geometry import (
    TOP_EDGES,
    BOTTOM_EDGES,
    MIDDLE_EDGES,
    SIDE_FACES,
    UP_STICKER,
    notation,
    turns_to,
    cost,
)
from solver.cube_reader import sc, compile_mask, matches, edges_with, turns_until

FLOWER_MASK = [
    [-1, YELLOW, -1],
    [YELLOW, WHITE, YELLOW],
    [-1, YELLOW, -1],
]

FLOWER = compile_mask(FLOWER_MASK)

GUARD = 500  # safety net; the loop should finish well before this


def solved(cube):
    return matches(cube[U].flatten(), FLOWER)


def daisy(work, do):
    def spin_until(face, ok):
        do(notation(face, turns_until(work, face, ok)))

    def empty_slot(face):
        # spin U until this side face's petal slot is empty (not yellow)
        spin_until(U, lambda c: sc(c, UP_STICKER[face]) != YELLOW)

    def empty_petals():
        return [face for face in SIDE_FACES if sc(work, UP_STICKER[face]) != YELLOW]

    for _ in range(GUARD):
        if solved(work):
            return

        edges = edges_with(work, YELLOW)

        # if a yellow edge is facing down on D layer,
        downs = [n for n, f in edges if n in BOTTOM_EDGES and f == D]
        if downs:
            # find combinations of edge and empty petal slot that require fewest D turns
            edge, empty_face = min(
                ((e, f) for e in downs for f in empty_petals()),
                key=lambda pair: cost(turns_to(D, *pair)),
            )
            # spin that edge round to the bottom of the empty slot
            do(notation(D, turns_to(D, edge, empty_face)))
            # flip up to top layer to form the petal
            do(notation(empty_face, 2))
            continue

        # if a yellow is in the middle layer
        mids = [(n, f) for n, f in edges if n in MIDDLE_EDGES]
        if mids:
            name, empty_face = mids[0]

            # find correct move needed to place edge into U face
            a, b = name
            if FACE_OF[a] == empty_face:
                move = notation(FACE_OF[b], 1)
            else:
                move = notation(FACE_OF[a], -1)

            # spin U face until petal slot is empty
            empty_slot(FACE_OF[move[0]])
            # perform move
            do(move)
            continue

        # if a yellow edge is on D face but yellow sticker is facing sideways
        downs_sideways = [(n, f) for n, f in edges if n in BOTTOM_EDGES and f != D]
        if downs_sideways:
            _, empty_face = downs_sideways[0]
            # empty petal slot on that face
            empty_slot(empty_face)
            # spin that face so the edge goes to middle layer
            do(notation(empty_face, 1))
            continue

        # if a yellow edge is in a petal slot but facing sideways
        tops_sideways = [(n, f) for n, f in edges if n in TOP_EDGES and f != U]
        if tops_sideways:
            _, yellow_face = tops_sideways[0]
            # spin that face so the edge goes to middle layer
            do(notation(yellow_face, 1))
            continue

        break  # no movable yellow edge left
