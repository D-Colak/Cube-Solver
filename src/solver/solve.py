from cube import run, convert_notation, SUFFIX
from solver.geometry import TURN_CHAR
from solver.daisy import daisy
from solver.cross import cross
from solver.f2l import f2l
from solver.oll import oll
from solver.pll import pll

STAGES = (daisy, cross, f2l, oll, pll)


def solve(cube):
    work = cube.copy()
    tagged = []  # (stage, token) for every turn, before cancellation

    for stage in STAGES:
        name = stage.__name__.upper()

        def do(notation, name=name):
            if not notation:  # a zero-turn alignment is a no-op, not a move
                return
            run(work, convert_notation(notation))
            tagged.extend((name, token) for token in notation.split())

        stage(work, do)

    moves, stages = cancel_stages(tagged)
    return " ".join(moves), stages


def cancel_stages(tagged):
    # geometry.cancel, but keeping which stage each surviving move belongs to
    moves, stages = [], []
    for name, move in tagged:
        if moves and moves[-1][0] == move[0]:
            n = (SUFFIX[moves[-1][1:]] + SUFFIX[move[1:]]) % 4
            moves.pop()
            name = stages.pop()  # the merged run began in an earlier stage
            if n:
                moves.append(move[0] + TURN_CHAR[n])
                stages.append(name)
        else:
            moves.append(move)
            stages.append(name)
    return moves, stages
