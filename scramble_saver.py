# run this if you want to fill scrambles.txt yourself. It takes over 20 minutes.

import os
import random
import sys
from multiprocessing import Pool

import twophase.solver as sv
from twophase.cubie import CubieCube

from cubesolver.scrambles import PATH as OUTPUT, RECORD

N_SCRAMBLES = 10000
MAX_LENGTH = 21
TIMEOUT = 2

SUFFIX = {1: "", 2: "2", 3: "'"}


def invert(solution):
    moves = solution.split("(")[0].split()
    return " ".join(m[0] + SUFFIX[4 - int(m[1])] for m in reversed(moves))


def wca_scramble(_=None):
    cc = CubieCube()
    cc.randomize()
    facelets = cc.to_facelet_cube().to_string()
    return invert(sv.solve(facelets, MAX_LENGTH, TIMEOUT))


def init_worker():
    random.seed(os.urandom(16))


def main():
    print("building/loading tables (once)...", file=sys.stderr)
    wca_scramble()

    workers = max(1, (os.cpu_count() or 2) - 1)
    print(f"generating {N_SCRAMBLES} on {workers} workers...", file=sys.stderr)

    with (
        Pool(workers, initializer=init_worker) as pool,
        open(OUTPUT, "w", newline="") as f,
    ):
        results = pool.imap_unordered(wca_scramble, range(N_SCRAMBLES), chunksize=16)
        for i, s in enumerate(results, 1):
            if len(s) > RECORD - 1:
                raise ValueError(f"scramble exceeds record width: {len(s)} chars")
            f.write(s.ljust(RECORD - 1) + "\n")
            if i % 250 == 0:
                print(f"  {i}/{N_SCRAMBLES}", file=sys.stderr)

    size = os.path.getsize(OUTPUT)
    expected = RECORD * N_SCRAMBLES
    if size != expected:
        raise ValueError(f"bad file size: {size} != {expected} (CRLF leak?)")
    print(f"wrote {OUTPUT} ({size} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
