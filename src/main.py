import matplotlib.pyplot as plt

from cube import SOLVED, convert_notation, record, run
from scramble_reader import random_scramble
from solver.solve import solve
from visualize import animate

INTERVAL = 100  # ms per move


def main():
    cube = SOLVED.copy()

    scramble = random_scramble()
    run(cube, convert_notation(scramble))

    solution, stages = solve(cube)
    frames = record(cube, convert_notation(solution))  # instant
    ani = animate(frames, INTERVAL, scramble, stages)  # drawn with delay
    plt.show()  # ani stays bound until this returns, so it survives


if __name__ == "__main__":
    main()
