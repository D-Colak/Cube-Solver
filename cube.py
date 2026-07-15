import numpy as np

# green forwards, white up
F, U, L, D, R, B = range(6)
M, E, S = range(6, 9) # middle slices
COLORS = ["green", "white", "orange", "yellow", "red", "blue"]

SOLVED = np.array([np.full((3, 3), side) for side in range(6)])

STRIPS = {
    # (face, row, col, dir)
    U: [(F, 0, None, 1), (R, 0, None, 1), (B, 0, None, 1), (L, 0, None, 1)],
    D: [(F, 2, None, 1), (L, 2, None, 1), (B, 2, None, 1), (R, 2, None, 1)],
    F: [(U, 2, None, 1), (L, None, 2, -1), (D, 0, None, -1), (R, None, 0, 1)],
    B: [(U, 0, None, 1), (R, None, 2, 1), (D, 2, None, -1), (L, None, 0, -1)],
    R: [(U, None, 2, 1), (F, None, 2, 1), (D, None, 2, 1), (B, None, 0, -1)],
    L: [(U, None, 0, 1), (B, None, 2, -1), (D, None, 0, 1), (F, None, 0, 1)],
}

PAIRS = {
    M: (R, L),
    E: (U, D),
    S: (B, F),
}


# turn strips into coords
def expand(s):
    face, row, col, dir = s
    axis = range(3)
    if dir == -1:
        axis = reversed(axis)

    if row is None:
        return [(face, r, col) for r in axis]
    else:
        return [(face, row, c) for c in axis]


INDICES = {
    face: tuple(np.array([p for s in STRIPS[face] for p in expand(s)]).T)
    for face in STRIPS
}


def turn(cube, face, n=1):
    # slices are two opposite faces at once, so centers never move
    if face in PAIRS:
        a, b = PAIRS[face]
        turn(cube, a, n)
        turn(cube, b, -n)
        return # early

    n %= 4
    # face rotation
    cube[face] = np.rot90(cube[face], -n)

    # strip rotation
    i = INDICES[face]
    cube[i] = np.roll(
        cube[i], -3 * n
    )  # combine strip, roll by 3 (one face), add back to cube
    # no need to return


FACE_OF = {"F": F, "U": U, "L": L, "D": D, "R": R, "B": B, "M": M, "E": E, "S": S}
SUFFIX = {"": 1, "'": -1, "2": 2}


def convert_notation(notation):
    moves = []
    for move in notation.split():
        face, suffix = move[0], move[1:]
        if face not in FACE_OF or suffix not in SUFFIX:
            raise ValueError(f"bad move {move!r}")
        moves.append((FACE_OF[face], SUFFIX[suffix], move))  # keep move for labels
    return moves


def run(cube, moves):
    for face, n, _ in moves:
        turn(cube, face, n)


def record(cube, moves):
    frames = [(cube.copy(), "start")]
    for face, n, move in moves:
        turn(cube, face, n)
        frames.append((cube.copy(), move))
    return frames
