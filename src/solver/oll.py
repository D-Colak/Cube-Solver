# OLL: orient the last layer in two looks -- U-face edges (cross), then corners

from cube import U, F, R, B, L, SOLVED, convert_notation, run, turn
from solver.geometry import invert, rotate_alg
from solver.algorithms import OLL_PHASE1, OLL_PHASE2

U_EDGES = ((U, 0, 1), (U, 1, 0), (U, 1, 2), (U, 2, 1))
U_CORNERS = ((U, 0, 0), (U, 0, 2), (U, 2, 0), (U, 2, 2))
SIDE_CORNERS = tuple((face, 0, col) for face in (F, R, B, L) for col in (0, 2))


def read_edges(cube):
    return tuple(1 if int(cube[c]) == U else 0 for c in U_EDGES)


def read_corners(cube):
    return tuple(1 if int(cube[c]) == U else 0 for c in U_CORNERS + SIDE_CORNERS)


def mask_of(alg, read):
    cube = SOLVED.copy()
    run(cube, convert_notation(invert(alg)))
    return read(cube)


EDGES = {mask_of(alg, read_edges): alg for alg in OLL_PHASE1.values()}
CORNERS = {mask_of(alg, read_corners): alg for alg in OLL_PHASE2.values()}


def recognize(cube, table, read):
    probe = cube.copy()
    for k in range(4):
        alg = table.get(read(probe))
        if alg is not None:
            return k, alg
        turn(probe, U)
    return None


def solved(cube):
    return all(int(cube[U, r, c]) == U for r in range(3) for c in range(3))


def oll(work, do):
    def look(table, read):
        found = recognize(work, table, read)
        if found is None:
            return  # already done, or a mask the table is missing
        k, alg = found
        do(rotate_alg(alg, k))  # no AUF needed

    look(EDGES, read_edges)  # the cross
    look(CORNERS, read_corners)  # the corners
