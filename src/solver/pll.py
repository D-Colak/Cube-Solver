# PLL: permute the last layer in two looks -- corners, then edges

from cube import U, F, R, B, L, SOLVED, convert_notation, run, turn
from solver.geometry import notation, invert, rotate_alg
from solver.cube_reader import turns_until
from solver.algorithms import PLL_PHASE1, PLL_PHASE2

# corner look reads the 8 corner stickers; edge look reads the whole 12-strip
SIDE_CORNERS = tuple((face, 0, col) for face in (F, R, B, L) for col in (0, 2))
STRIP = tuple((face, 0, col) for face in (F, R, B, L) for col in range(3))


def relative(coords):
    def read(cube):
        label = {}
        return tuple(label.setdefault(int(cube[c]), len(label)) for c in coords)

    return read


read_corners = relative(SIDE_CORNERS)
read_edges = relative(STRIP)


def mask_of(alg, read):
    cube = SOLVED.copy()
    run(cube, convert_notation(invert(alg)))
    return read(cube)


CORNERS = {mask_of(alg, read_corners): alg for alg in PLL_PHASE1.values()}
EDGES = {mask_of(alg, read_edges): alg for alg in PLL_PHASE2.values()}


def recognize(cube, table, read):
    probe = cube.copy()
    for k in range(4):
        alg = table.get(read(probe))
        if alg is not None:
            return k, alg
        turn(probe, U)
    return None


def solved(cube):
    return all(int(cube[c]) == c[0] for c in STRIP)


def pll(work, do):
    def look(table, read):
        found = recognize(work, table, read)
        if found is None:
            return  # already done, or a mask the table is missing
        k, alg = found
        do(rotate_alg(alg, k))  # no AUF needed

    look(CORNERS, read_corners)  # place the corners
    look(EDGES, read_edges)  # place the edges
    do(notation(U, turns_until(work, U, solved)))  # final AUF to seat the layer
