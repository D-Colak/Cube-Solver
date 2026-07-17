# F2L: fill the four bottom slots, each a yellow corner plus its middle edge

import heapq
import itertools

import numpy as np

from cube import convert_notation, run, U, D
from solver.geometry import (
    EDGES,
    CORNERS,
    MIDDLE_EDGES,
    FACE_OF,
    FACE_CHAR,
    notation,
)

GUARD = 100  # safety net; the loop should finish well before this

_PARSED = {}  # memoization


def apply(cube, move):
    parsed = _PARSED.get(move)
    if parsed is None:
        parsed = _PARSED[move] = convert_notation(move)
    run(cube, parsed)

# F2L inserts
BASIC = ("R U R'", "F' U' F", "U R U' R'", "U' F' U F")


def slot_faces(edge):
    return FACE_OF[edge[0]], FACE_OF[edge[1]]


def corner_of(edge):
    want = {"D", edge[0], edge[1]}
    return next(name for name in CORNERS if set(name) == want)


def insert(edge, alg):
    left, right = slot_faces(edge)
    swap = {"F": FACE_CHAR[left], "R": FACE_CHAR[right], "U": "U"}
    return " ".join(swap[move[0]] + move[1:] for move in alg.split())


def piece_solved(cube, coords):
    return all(int(cube[c]) == c[0] for c in coords)


def filled(cube, edge):
    return piece_solved(cube, CORNERS[corner_of(edge)]) and piece_solved(cube, EDGES[edge])


def solved(cube):
    return all(filled(cube, edge) for edge in MIDDLE_EDGES)


_PERM = {}


def macro_perm(move):
    if move not in _PERM:
        labels = np.arange(54).reshape(6, 3, 3)  # each sticker tagged by index
        apply(labels, move)
        _PERM[move] = labels.reshape(54).copy()  # perm[pos] = where pos came from
    return _PERM[move]


def _checks(edge):
    coords = CORNERS[corner_of(edge)] + EDGES[edge]
    idx = np.array([f * 9 + r * 3 + c for f, r, c in coords])
    val = np.array([f for f, r, c in coords])
    return idx, val


CHECKS = {edge: _checks(edge) for edge in MIDDLE_EDGES}


EDGE_OF_CORNER = {corner_of(edge): edge for edge in MIDDLE_EDGES}


def find_piece(cube, table, want):
    for name, coords in table.items():
        if {int(cube[c]) for c in coords} == want:
            return name
    return None


def buried_slots(cube, edge):
    corner = find_piece(cube, CORNERS, {D, FACE_OF[edge[0]], FACE_OF[edge[1]]})
    stray = find_piece(cube, EDGES, {FACE_OF[edge[0]], FACE_OF[edge[1]]})
    slots = set()
    if corner[0] != "U":
        slots.add(EDGE_OF_CORNER[corner])
    if stray in MIDDLE_EDGES:
        slots.add(stray)
    return slots


_TURN_COST = {"": 1, "'": 1, "2": 2}  # quarter turns a single move costs


def qtm(move):
    return sum(_TURN_COST[token[1:]] for token in move.split())


CAP = 14  # a slot seats in far fewer quarter turns; the cap just bounds a miss


def _search(cube, edge, keep, reach, cap):
    moves = [notation(U, n) for n in (1, 2, 3)]
    for slot in reach:
        moves += [insert(slot, alg) for alg in BASIC]
    perms = {m: macro_perm(m) for m in moves}
    costs = {m: qtm(m) for m in moves}
    keep_checks = [CHECKS[k] for k in keep]
    idx, val = CHECKS[edge]

    start = cube.reshape(54).copy()
    best = {start.tobytes(): 0}
    order = itertools.count()  # tie-breaker so arrays never get compared
    queue = [(0, next(order), start, [])]
    while queue:
        spent, _, state, sofar = heapq.heappop(queue)
        if bool((state[idx] == val).all()):
            return sofar
        if spent > best.get(state.tobytes(), spent):
            continue  # a cheaper path to this state was already settled
        for move in moves:
            step = spent + costs[move]
            if step > cap:
                continue
            nxt = state[perms[move]]
            if any(not (nxt[i] == v).all() for i, v in keep_checks):
                continue  # would break a finished slot
            key = nxt.tobytes()
            if step < best.get(key, 1 << 30):
                best[key] = step
                heapq.heappush(queue, (step, next(order), nxt, sofar + [move]))
    return None


def solve_slot(cube, edge, keep):
    reach = {edge} | (buried_slots(cube, edge) - keep)
    path = _search(cube, edge, keep, reach, CAP)
    if path is None:  # rare: open the search to every unfinished slot
        path = _search(cube, edge, keep, set(MIDDLE_EDGES) - keep, 1 << 30)
    return path


def f2l(work, do):
    keep = set()
    for _ in range(GUARD):
        if solved(work):
            return
        edge = next(e for e in MIDDLE_EDGES if e not in keep and not filled(work, e))
        path = solve_slot(work, edge, keep)
        if path is None:
            break  # no insertion keeps the finished slots; should not happen
        for move in path:
            do(move)
        keep.add(edge)
