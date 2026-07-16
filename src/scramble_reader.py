from random import randrange
from pathlib import Path

RECORD = 80  # bytes per scramble line, padded; lets us seek instead of scan
PATH = Path(__file__).resolve().parent.parent / "scrambles.txt"


def random_scramble(path=PATH):
    n = path.stat().st_size // RECORD
    with open(path, "rb") as f:
        f.seek(RECORD * randrange(n))
        return f.read(RECORD).decode().strip()
