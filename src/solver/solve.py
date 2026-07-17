from cube import run, convert_notation
from solver.geometry import cancel
from solver.daisy import daisy
from solver.cross import cross
from solver.f2l import f2l
from solver.oll import oll
from solver.pll import pll

STAGES = (daisy, cross, f2l, oll, pll)


def solve(cube):
    work = cube.copy()
    solution = []

    def do(notation):
        if not notation:  # a zero-turn alignment is a no-op, not a move
            return
        run(work, convert_notation(notation))
        solution.append(notation)

    for stage in STAGES:
        stage(work, do)

    tokens = [token for move in solution for token in move.split()]
    return " ".join(cancel(tokens))
