from cube import F, U, L, D, R, B, FACE_OF, SUFFIX

EDGES = {
    "UF": ((U, 2, 1), (F, 0, 1)),
    "UR": ((U, 1, 2), (R, 0, 1)),
    "UB": ((U, 0, 1), (B, 0, 1)),
    "UL": ((U, 1, 0), (L, 0, 1)),
    "DF": ((D, 0, 1), (F, 2, 1)),
    "DR": ((D, 1, 2), (R, 2, 1)),
    "DB": ((D, 2, 1), (B, 2, 1)),
    "DL": ((D, 1, 0), (L, 2, 1)),
    "FR": ((F, 1, 2), (R, 1, 0)),
    "RB": ((R, 1, 2), (B, 1, 0)),
    "BL": ((B, 1, 2), (L, 1, 0)),
    "LF": ((L, 1, 2), (F, 1, 0)),
}

CORNERS = {
    "UFL": ((U, 2, 0), (F, 0, 0), (L, 0, 2)),
    "UFR": ((U, 2, 2), (F, 0, 2), (R, 0, 0)),
    "UBR": ((U, 0, 2), (B, 0, 0), (R, 0, 2)),
    "UBL": ((U, 0, 0), (B, 0, 2), (L, 0, 0)),
    "DFL": ((D, 0, 0), (F, 2, 0), (L, 2, 2)),
    "DFR": ((D, 0, 2), (F, 2, 2), (R, 2, 0)),
    "DBR": ((D, 2, 2), (B, 2, 0), (R, 2, 2)),
    "DBL": ((D, 2, 0), (B, 2, 2), (L, 2, 0)),
}

TOP_EDGES = ("UF", "UR", "UB", "UL")
BOTTOM_EDGES = ("DF", "DR", "DB", "DL")
MIDDLE_EDGES = ("FR", "RB", "BL", "LF")

SIDE_FACES = (F, R, B, L)

# four edges around each face
RING = {
    U: ("UF", "UL", "UB", "UR"),
    D: ("DF", "DR", "DB", "DL"),
    F: ("UF", "FR", "DF", "LF"),
    B: ("UB", "BL", "DB", "RB"),
    R: ("UR", "RB", "DR", "FR"),
    L: ("UL", "LF", "DL", "BL"),
}

EDGE_OF = {frozenset(name): name for name in EDGES}  # {"F","R"} -> "FR"

FACE_CHAR = {face: char for char, face in FACE_OF.items()}

TURN_CHAR = {n % 4: suffix for suffix, n in SUFFIX.items()}

UP_STICKER = {face: EDGES["U" + FACE_CHAR[face]][0] for face in SIDE_FACES}
DOWN_STICKER = {face: EDGES["D" + FACE_CHAR[face]][0] for face in SIDE_FACES}


def notation(face, n):
    # shortest way to write n turns
    n %= 4
    if not n:
        return ""
    return FACE_CHAR[face] + TURN_CHAR[n]


def cost(n):
    # cost function for turns
    n %= 4
    return min(n, 4 - n)


def invert(alg):
    # reverse a sequence and flip each move
    flip = {"": "'", "'": "", "2": "2"}
    return " ".join(move[0] + flip[move[1:]] for move in reversed(alg.split()))


def cancel(moves):
    # merge consecutive or opposing turns
    out = []
    for move in moves:
        if out and out[-1][0] == move[0]:
            n = (SUFFIX[out[-1][1:]] + SUFFIX[move[1:]]) % 4
            out.pop()
            if n:
                out.append(move[0] + TURN_CHAR[n])
        else:
            out.append(move)
    return out


U_AXIS_CYCLE = "FRBL"


def rotate_alg(alg, n):
    # rotate algorithm n times around U axis
    def move(m):
        if m[0] in U_AXIS_CYCLE:
            return U_AXIS_CYCLE[(U_AXIS_CYCLE.index(m[0]) + n) % 4] + m[1:]
        return m

    return " ".join(move(m) for m in alg.split())


def turns_to(face, edge, dest):
    # turns of face that move edge to the slot it shares with dest
    ring = RING[face]
    target = EDGE_OF[frozenset(FACE_CHAR[face] + FACE_CHAR[dest])]
    return (ring.index(target) - ring.index(edge)) % 4
