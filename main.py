import matplotlib.pyplot as plt
import os
import random

from cube import SOLVED, record, run, convert_notation
from visualize import animate

"""
M E S are not standard notation. The centers dont move so
M = R L'
E = U D'
S = F B'
"""
ALG = "F B L U D' B' B2"
INTERVAL = 100  # ms per move

RECORD = 80

def random_scramble(path="scrambles.txt"):
    n = os.path.getsize(path) // RECORD
    with open(path, "rb") as f:
        f.seek(RECORD * random.randrange(n))
        return f.read(RECORD).decode().strip()


def main():
    cube = SOLVED.copy()

    # do scramble
    scramble = random_scramble()
    scramble_moves = convert_notation(scramble)
    run(cube, scramble_moves) 

    moves = convert_notation(ALG)
    frames = record(cube, moves)  # instant
    ani = animate(frames, INTERVAL)  # drawn with delay
    plt.show()  # ani stays bound until this returns, so it survives


if __name__ == "__main__":
    main()
