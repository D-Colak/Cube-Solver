import numpy as np

# green forwards, white up
F, U, L, D, R, B = range(6)

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


INDICES = {face: tuple(np.array([p for s in STRIPS[face] for p in expand(s)]).T) for face in STRIPS}

def turn(cube, face, n=1):
    n %= 4
    # face rotation
    cube[face] = np.rot90(cube[face], -n)
    
    # strip rotation
    i = INDICES[face]
    cube[i] = np.roll(cube[i], -3 * n) # combine strip, roll by 3 (one face), add back to cube
    # no need to return


def convert_notation(notation):
    moves = []
    for move in notation.split():
        if len(move) == 1:
            moves.append((move, 1))
        elif move[1] == "'":
            moves.append((move[0], -1))
        elif move[1] == "2":
            moves.append((move[0], 2))
    return moves


def run(cube, moves):
    for move, n in moves:
        turn(cube, eval(move), n)

def main():
    cube = SOLVED.copy()
    moves = convert_notation("U2 D2 F2 B2 L2 R2")
    run(cube, moves)
    print(cube)

if __name__== "__main__":
    main()
