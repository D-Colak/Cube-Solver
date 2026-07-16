from cube import run, convert_notation
from solver.daisy import daisy

STAGES = (daisy,)


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

    return " ".join(solution)
