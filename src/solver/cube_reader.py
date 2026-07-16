from cube import turn
from solver.geometry import EDGES, cost


def sc(cube, coord):
    # color of a single facelet
    return int(cube[coord])


def colors(cube, coords):
    # stickers in slot
    return tuple(sc(cube, c) for c in coords)


def facing(cube, coords, color):
    # which face is this color on
    for c in coords:
        if sc(cube, c) == color:
            return c[0]
    return None


def compile_mask(mask):
    # 3x3 grid to tuple(coord, color)
    flat = [c for row in mask for c in row]
    return tuple((i, v) for i, v in enumerate(flat) if v != -1)


def matches(flat_grid, compiled):
    return all(flat_grid[i] == v for i, v in compiled)


def edges_with(cube, color):
    # (edge name, face that color points at) for every edge carrying color
    found = []
    for name, coords in EDGES.items():
        if color in colors(cube, coords):
            found.append((name, facing(cube, coords, color)))
    return found


def turns_until(cube, face, ok):
    # cheapest rotation of face that satisfies ok
    probe = cube.copy()
    hits = []
    for n in range(4):
        if ok(probe):
            hits.append(n)
        turn(probe, face)
    return min(hits, key=cost, default=0)
