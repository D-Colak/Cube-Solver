import matplotlib.pyplot as plt

from cube import COLORS, SOLVED, convert_notation, record
from visualize import animate

ALG = "U B D' F2 D B' U' R2 D F2 D' R2 D F2 D' R2"
INTERVAL = 100  # ms per move


def main():
    cube = SOLVED.copy()
    colors = COLORS.copy()

    moves = convert_notation(ALG)
    frames = record(cube, moves)  # instant
    ani = animate(frames, colors, INTERVAL)  # drawn with delay
    plt.show()  # ani stays bound until this returns, so it survives


if __name__ == "__main__":
    main()
