import matplotlib.pyplot as plt

from cube import COLORS, SOLVED, convert_notation, record
from visualize import animate

"""
M E S are not standard notation. The centers dont move so
M = R L'
E = U D'
S = F B'
"""
ALG = "R M' L'"
INTERVAL = 400  # ms per move


def main():
    cube = SOLVED.copy()
    colors = COLORS.copy()

    moves = convert_notation(ALG)
    frames = record(cube, moves)  # instant
    ani = animate(frames, colors, INTERVAL)  # drawn with delay
    plt.show()  # ani stays bound until this returns, so it survives


if __name__ == "__main__":
    main()
