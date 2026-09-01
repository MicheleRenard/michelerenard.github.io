#!/usr/bin/env python3
"""
Draw every original pixel-art asset for the RPG page (rpg/assets/).

All art is generated from this file — the character from pixel-string grids
(reviewable in a text diff), the tiles and buildings procedurally — so the
whole look of Renard Village is reproducible and editable without an image
editor. Safe to re-run at any time; prints every file it writes.

    python3 tools/build-rpg-sprites.py

Outputs:
    rpg/assets/sprites/michele-walk.png   48x96  (3 frames x 4 directions, 16x24)
    rpg/assets/sprites/crier.png          32x24  (2 frames)
    rpg/assets/sprites/cat.png            32x16  (2 frames)
    rpg/assets/sprites/sign.png           16x16
    rpg/assets/tiles/tiles.png            16x16 ground tiles in one row
    rpg/assets/tiles/{lab,library,guild,inn,shop,fountain}.png
"""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT_SPRITES = ROOT / "rpg" / "assets" / "sprites"
OUT_TILES = ROOT / "rpg" / "assets" / "tiles"

# ---------------------------------------------------------------------------
# Palette. Site identity: ink #1B2432, ember #B4552B, night #2F5A69.
# ---------------------------------------------------------------------------
PAL = {
    ".": None,                # transparent
    "H": (54, 38, 27),        # hair, dark brown
    "h": (84, 60, 40),        # hair highlight
    "S": (236, 188, 152),     # skin
    "s": (204, 152, 118),     # skin shadow
    "E": (27, 36, 50),        # eyes / outlines (site ink)
    "J": (43, 58, 84),        # jacket (brightened ink for readability)
    "j": (64, 84, 116),       # jacket highlight
    "W": (245, 243, 238),     # collar / shirt (site paper)
    "R": (180, 85, 43),       # ember accent (scarf)
    "P": (70, 74, 82),        # trousers
    "B": (38, 30, 24),        # boots
}

# ---------------------------------------------------------------------------
# Michèle — 16x24, three frames per direction (stand, step A, step B).
# Short dark hair, dark jacket, ember scarf: the likeness brief.
# ---------------------------------------------------------------------------

DOWN_STAND = [
    "................",
    ".....HHHHHH.....",
    "....HHHHHHHH....",
    "...HHhHHHHhHH...",
    "...HHSSSSSSHH...",
    "...HSSSSSSSSH...",
    "...HSESSSSESH...",
    "....SSSSSSSS....",
    "....sSSSSSSs....",
    ".....SssssS.....",
    "....JRRRRRRJ....",
    "...JJJWWWWJJJ...",
    "...JJJJWWJJJJ...",
    "..SJJJJJJJJJJS..",
    "..SJJJJJJJJJJS..",
    "..sJJJJJJJJJJs..",
    "...JjJJJJJJjJ...",
    "....PPPPPPPP....",
    "....PPP..PPP....",
    "....PPP..PPP....",
    "....PPP..PPP....",
    "....BBB..BBB....",
    "....BBB..BBB....",
    "................",
]

DOWN_A = [
    "................",
    ".....HHHHHH.....",
    "....HHHHHHHH....",
    "...HHhHHHHhHH...",
    "...HHSSSSSSHH...",
    "...HSSSSSSSSH...",
    "...HSESSSSESH...",
    "....SSSSSSSS....",
    "....sSSSSSSs....",
    ".....SssssS.....",
    "....JRRRRRRJ....",
    "...JJJWWWWJJJ...",
    "...JJJJWWJJJJ...",
    "..SJJJJJJJJJJ...",
    "..SJJJJJJJJJJS..",
    "...JJJJJJJJJJs..",
    "...JjJJJJJJjJ...",
    "....PPPPPPPP....",
    "....PPP..PPP....",
    "...PPP...PPP....",
    "...PPP....PP....",
    "...BBB...BBB....",
    ".........BBB....",
    "................",
]

DOWN_B = [
    "................",
    ".....HHHHHH.....",
    "....HHHHHHHH....",
    "...HHhHHHHhHH...",
    "...HHSSSSSSHH...",
    "...HSSSSSSSSH...",
    "...HSESSSSESH...",
    "....SSSSSSSS....",
    "....sSSSSSSs....",
    ".....SssssS.....",
    "....JRRRRRRJ....",
    "...JJJWWWWJJJ...",
    "...JJJJWWJJJJ...",
    "...JJJJJJJJJJS..",
    "..SJJJJJJJJJJS..",
    "..sJJJJJJJJJJ...",
    "...JjJJJJJJjJ...",
    "....PPPPPPPP....",
    "....PPP..PPP....",
    "....PPP...PPP...",
    "....PP....PPP...",
    "....BBB...BBB...",
    "....BBB.........",
    "................",
]

UP_STAND = [
    "................",
    ".....HHHHHH.....",
    "....HHHHHHHH....",
    "...HHHHHHHHHH...",
    "...HHHHHHHHHH...",
    "...HHHhHHhHHH...",
    "...HHHHHHHHHH...",
    "....HHHHHHHH....",
    "....sHHHHHHs....",
    ".....SHHHHS.....",
    "....JJJJJJJJ....",
    "...JJJJJJJJJJ...",
    "...JJJJJJJJJJ...",
    "..SJJJJJJJJJJS..",
    "..SJJJjJJjJJJS..",
    "..sJJJjJJjJJJs..",
    "...JjJJJJJJjJ...",
    "....PPPPPPPP....",
    "....PPP..PPP....",
    "....PPP..PPP....",
    "....PPP..PPP....",
    "....BBB..BBB....",
    "....BBB..BBB....",
    "................",
]

UP_A = [
    "................",
    ".....HHHHHH.....",
    "....HHHHHHHH....",
    "...HHHHHHHHHH...",
    "...HHHHHHHHHH...",
    "...HHHhHHhHHH...",
    "...HHHHHHHHHH...",
    "....HHHHHHHH....",
    "....sHHHHHHs....",
    ".....SHHHHS.....",
    "....JJJJJJJJ....",
    "...JJJJJJJJJJ...",
    "...JJJJJJJJJJ...",
    "..SJJJJJJJJJJ...",
    "..SJJJjJJjJJJS..",
    "...JJJjJJjJJJs..",
    "...JjJJJJJJjJ...",
    "....PPPPPPPP....",
    "....PPP..PPP....",
    "...PPP...PPP....",
    "...PPP....PP....",
    "...BBB...BBB....",
    ".........BBB....",
    "................",
]

UP_B = [
    "................",
    ".....HHHHHH.....",
    "....HHHHHHHH....",
    "...HHHHHHHHHH...",
    "...HHHHHHHHHH...",
    "...HHHhHHhHHH...",
    "...HHHHHHHHHH...",
    "....HHHHHHHH....",
    "....sHHHHHHs....",
    ".....SHHHHS.....",
    "....JJJJJJJJ....",
    "...JJJJJJJJJJ...",
    "...JJJJJJJJJJ...",
    "...JJJJJJJJJJS..",
    "..SJJJjJJjJJJS..",
    "..sJJJjJJjJJJ...",
    "...JjJJJJJJjJ...",
    "....PPPPPPPP....",
    "....PPP..PPP....",
    "....PPP...PPP...",
    "....PP....PPP...",
    "....BBB...BBB...",
    "....BBB.........",
    "................",
]

RIGHT_STAND = [
    "................",
    ".....HHHHHH.....",
    "....HHHHHHHH....",
    "....HHHHHHHH....",
    "....HHHSSSSH....",
    "....HHSSSSSS....",
    "....HHSSESSs....",
    "....HHSSSSSs....",
    "....HhSSSSs.....",
    ".....HSsss......",
    ".....JRRRRJ.....",
    "....JJJRRJJJ....",
    "....JJJJJJJJ....",
    "....JJJJJJJJS...",
    "....JJJJJJJJS...",
    "....JJJJJJJJs...",
    "....JjJJJJjJ....",
    ".....PPPPPP.....",
    ".....PPPPPP.....",
    ".....PP.PPP.....",
    ".....PP.PPP.....",
    ".....BB.BBB.....",
    ".....BB.BBB.....",
    "................",
]

RIGHT_A = [
    "................",
    ".....HHHHHH.....",
    "....HHHHHHHH....",
    "....HHHHHHHH....",
    "....HHHSSSSH....",
    "....HHSSSSSS....",
    "....HHSSESSs....",
    "....HHSSSSSs....",
    "....HhSSSSs.....",
    ".....HSsss......",
    ".....JRRRRJ.....",
    "....JJJRRJJJ....",
    "....JJJJJJJJ....",
    "....JJJJJJJJS...",
    "...SJJJJJJJJ....",
    "....JJJJJJJJ....",
    "....JjJJJJjJ....",
    ".....PPPPPP.....",
    "....PPP.PPP.....",
    "....PPP..PPP....",
    "....PP....PP....",
    "....BB...BBB....",
    "....BB..........",
    "................",
]

RIGHT_B = [
    "................",
    ".....HHHHHH.....",
    "....HHHHHHHH....",
    "....HHHHHHHH....",
    "....HHHSSSSH....",
    "....HHSSSSSS....",
    "....HHSSESSs....",
    "....HHSSSSSs....",
    "....HhSSSSs.....",
    ".....HSsss......",
    ".....JRRRRJ.....",
    "....JJJRRJJJ....",
    "....JJJJJJJJ....",
    "....JJJJJJJJS...",
    "....JJJJJJJJ....",
    "...sJJJJJJJJ....",
    "....JjJJJJjJ....",
    ".....PPPPPP.....",
    ".....PPPPPP.....",
    "....PPP..PP.....",
    "....PPP..PP.....",
    "....BBB..BB.....",
    ".........BB.....",
    "................",
]


def grid_to_img(grid, palette=PAL):
    h = len(grid)
    w = len(grid[0])
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(grid):
        assert len(row) == w, f"row {y} has width {len(row)}, expected {w}"
        for x, ch in enumerate(row):
            color = palette[ch]
            if color is not None:
                px[x, y] = (*color, 255)
    return img


def sheet(frames_by_row, frame_w, frame_h):
    """frames_by_row: list of rows, each row a list of PIL images."""
    rows = len(frames_by_row)
    cols = max(len(r) for r in frames_by_row)
    img = Image.new("RGBA", (cols * frame_w, rows * frame_h), (0, 0, 0, 0))
    for ry, row in enumerate(frames_by_row):
        for cx, frame in enumerate(row):
            img.paste(frame, (cx * frame_w, ry * frame_h))
    return img


def save(img, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    print(f"wrote {path.relative_to(ROOT)}  ({img.width}x{img.height})")


def build_michele():
    down = [grid_to_img(g) for g in (DOWN_STAND, DOWN_A, DOWN_B)]
    up = [grid_to_img(g) for g in (UP_STAND, UP_A, UP_B)]
    right = [grid_to_img(g) for g in (RIGHT_STAND, RIGHT_A, RIGHT_B)]
    left = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in right]
    # rows: down, up, right, left  -> 48x96
    save(sheet([down, up, right, left], 16, 24), OUT_SPRITES / "michele-walk.png")


# ---------------------------------------------------------------------------
# NPCs: town crier (16x24, 2 frames), cat (16x16, 2 frames), signpost (16x16)
# ---------------------------------------------------------------------------

CRIER_PAL = dict(PAL)
CRIER_PAL.update({
    "G": (47, 90, 105),       # tunic — site night
    "g": (70, 120, 138),      # tunic highlight
    "Y": (222, 186, 92),      # trim / bell
})

CRIER_A = [
    "................",
    ".....hhhhhh.....",
    "....hhhhhhhh....",
    "....hSSSSSSh....",
    "....SSESSESS....",
    "....SSSSSSSS....",
    ".....SssssS.....",
    "....GGGGGGGG....",
    "...GGGYYYYGGG...",
    "...GGGGGGGGGG...",
    "..SGGGGGGGGGGS..",
    "..SGGGGGGGGGGY..",
    "..sGGGGGGGGGGY..",
    "...GgGGGGGGgG...",
    "...GGGGGGGGGG...",
    "....GGGGGGGG....",
    "....PPPPPPPP....",
    "....PPP..PPP....",
    "....PPP..PPP....",
    "....PPP..PPP....",
    "....BBB..BBB....",
    "....BBB..BBB....",
    "................",
    "................",
]

CRIER_B = [
    "................",
    ".....hhhhhh.....",
    "....hhhhhhhh....",
    "....hSSSSSSh....",
    "....SSESSESS....",
    "....SSSSSSSS....",
    ".....SssssS.....",
    "....GGGGGGGG....",
    "...GGGYYYYGGG...",
    "...GGGGGGGGGG...",
    "..YGGGGGGGGGGS..",
    "..YGGGGGGGGGGS..",
    "..YGGGGGGGGGGs..",
    "...GgGGGGGGgG...",
    "...GGGGGGGGGG...",
    "....GGGGGGGG....",
    "....PPPPPPPP....",
    "....PPP..PPP....",
    "....PPP..PPP....",
    "....PPP..PPP....",
    "....BBB..BBB....",
    "....BBB..BBB....",
    "................",
    "................",
]

CAT_PAL = {
    ".": None,
    "O": (216, 150, 70),      # orange coat
    "o": (238, 180, 104),     # light coat
    "W": (245, 243, 238),     # chest / paws
    "E": (27, 36, 50),        # eyes / outline
    "P": (222, 140, 140),     # nose / inner ear
}

CAT_SIT = [
    "................",
    "................",
    "....E..E........",
    "...EOEEOE.......",
    "...EOPOOPE......",
    "...EOOOOOE......",
    "...EOEOEOE......",
    "...EOOPOOE......",
    "....EOOOE.......",
    "....EOOOOEE.....",
    "...EOOOOOOOE....",
    "...EOOOOOOOE.E..",
    "...EoOOOOOOEOE..",
    "...EoOOOOOOOE...",
    "...EWWE.EWWE....",
    "................",
]

CAT_TAIL = [
    "................",
    "................",
    "....E..E........",
    "...EOEEOE.......",
    "...EOPOOPE......",
    "...EOOOOOE......",
    "...EOEOEOE......",
    "...EOOPOOE......",
    "....EOOOE.......",
    "....EOOOOEE.....",
    "...EOOOOOOOE....",
    "...EOOOOOOOE....",
    "...EoOOOOOOE.E..",
    "...EoOOOOOOEOE..",
    "...EWWE.EWWEE...",
    "................",
]

SIGN_PAL = {
    ".": None,
    "T": (107, 74, 43),       # post
    "t": (139, 100, 60),      # board light
    "e": (110, 78, 46),       # board shade
    "E": (27, 36, 50),
}

SIGN = [
    "................",
    ".EEEEEEEEEEEEE..",
    ".EttttttttttteE.",
    ".EtEEtEEEtEEteE.",
    ".EttttttttttteE.",
    ".EtEEEtEEtEtteE.",
    ".EttttttttttteE.",
    ".EEEEEEEEEEEEE..",
    "......TT........",
    "......TT........",
    "......TT........",
    "......TT........",
    "......TT........",
    "......TT........",
    ".....TTTT.......",
    "................",
]


def build_npcs():
    crier = [grid_to_img(g, CRIER_PAL) for g in (CRIER_A, CRIER_B)]
    cat = [grid_to_img(g, CAT_PAL) for g in (CAT_SIT, CAT_TAIL)]
    save(sheet([crier], 16, 24), OUT_SPRITES / "crier.png")
    save(sheet([cat], 16, 16), OUT_SPRITES / "cat.png")
    save(grid_to_img(SIGN, SIGN_PAL), OUT_SPRITES / "sign.png")


# ---------------------------------------------------------------------------
# Ground tiles (16x16), procedural. Order in tiles.png (one row):
#   0 grass  1 grass-speckle  2 flowers  3 path  4 path-edge-n
#   5 tree   6 water  7 fence  8 cobble-plaza
# ---------------------------------------------------------------------------

GRASS = (74, 143, 60)
GRASS_D = (58, 115, 48)
GRASS_L = (90, 163, 72)
PATH = (201, 178, 133)
PATH_D = (172, 148, 105)
WATER = (58, 102, 200)
WATER_L = (90, 134, 232)
TRUNK = (107, 74, 43)
LEAF = (45, 107, 45)
LEAF_L = (61, 143, 61)
FENCE = (139, 100, 60)
FENCE_D = (100, 70, 40)
PLAZA = (188, 178, 160)
PLAZA_D = (160, 150, 132)


def tile(fill):
    img = Image.new("RGBA", (16, 16), (*fill, 255))
    return img, ImageDraw.Draw(img)


def t_grass(speckled=False, flowers=False):
    img, d = tile(GRASS)
    # deterministic speckle pattern, no RNG so re-runs are identical
    for i, (x, y) in enumerate([(2, 3), (12, 2), (7, 7), (3, 12), (13, 11), (9, 14)]):
        d.point((x, y), GRASS_D if i % 2 else GRASS_L)
    if speckled:
        for x, y in [(5, 5), (11, 8), (2, 9), (14, 6), (8, 12)]:
            d.rectangle([x, y, x + 1, y], fill=GRASS_D)
    if flowers:
        for x, y, c in [(3, 4, (232, 220, 120)), (11, 6, (224, 148, 148)), (6, 11, (240, 240, 240))]:
            d.point((x, y - 1), c)
            d.rectangle([x - 1, y, x + 1, y], fill=c)
            d.point((x, y + 1), c)
            d.point((x, y), (222, 186, 92))
    return img


def t_path(edge_n=False):
    img, d = tile(PATH)
    for x, y in [(3, 3), (12, 5), (6, 9), (10, 13), (2, 12)]:
        d.point((x, y), PATH_D)
    if edge_n:
        d.rectangle([0, 0, 15, 1], fill=GRASS)
        d.rectangle([0, 2, 15, 2], fill=PATH_D)
    return img


def t_tree():
    img, d = tile(GRASS)
    for i, (x, y) in enumerate([(2, 13), (13, 14)]):
        d.point((x, y), GRASS_D if i % 2 else GRASS_L)
    d.rectangle([6, 10, 9, 15], fill=TRUNK)
    d.ellipse([1, 0, 14, 11], fill=LEAF)
    d.ellipse([3, 1, 10, 7], fill=LEAF_L)
    d.point((5, 3), (200, 230, 200))
    return img


def t_water():
    img, d = tile(WATER)
    for y in (3, 8, 13):
        for x0 in (1, 9):
            d.rectangle([x0, y, x0 + 4, y], fill=WATER_L)
    return img


def t_fence():
    img, d = tile(GRASS)
    d.rectangle([0, 6, 15, 8], fill=FENCE)
    d.rectangle([0, 8, 15, 8], fill=FENCE_D)
    for x in (2, 8, 14):
        d.rectangle([x - 1, 3, x + 1, 12], fill=FENCE)
        d.rectangle([x - 1, 12, x + 1, 12], fill=FENCE_D)
        d.point((x, 3), (170, 130, 85))
    return img


def t_plaza():
    img, d = tile(PLAZA)
    d.line([(0, 7), (15, 7)], fill=PLAZA_D)
    d.line([(7, 0), (7, 7)], fill=PLAZA_D)
    d.line([(11, 8), (11, 15)], fill=PLAZA_D)
    return img


def build_tiles():
    tiles = [
        t_grass(),
        t_grass(speckled=True),
        t_grass(flowers=True),
        t_path(),
        t_path(edge_n=True),
        t_tree(),
        t_water(),
        t_fence(),
        t_plaza(),
    ]
    img = Image.new("RGBA", (16 * len(tiles), 16), (0, 0, 0, 0))
    for i, t in enumerate(tiles):
        img.paste(t, (i * 16, 0))
    save(img, OUT_TILES / "tiles.png")


# ---------------------------------------------------------------------------
# Buildings, procedural. FF town look: white plaster, timber, steep blue roofs.
# One PNG per building so main.js can place them without slicing arithmetic.
# ---------------------------------------------------------------------------

PLASTER = (232, 220, 192)
PLASTER_D = (205, 190, 160)
TIMBER = (122, 88, 56)
ROOF = (48, 80, 200)
ROOF_L = (74, 106, 224)
ROOF_D = (36, 60, 160)
ROOF_EMBER = (180, 85, 43)
ROOF_EMBER_L = (208, 116, 72)
ROOF_EMBER_D = (143, 65, 31)
DOOR = (94, 62, 34)
DOOR_L = (122, 88, 56)
GLASS = (120, 200, 232)
GLASS_D = (80, 150, 190)
INK = (27, 36, 50)


def building(w, h, roof_h, roof=(ROOF, ROOF_L, ROOF_D), banner=None):
    """Generic FF-style house: steep roof, plaster walls, timber frame, door."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rc, rl, rd = roof
    # roof: trapezoid
    for y in range(roof_h):
        inset = max(0, (roof_h - 1 - y) * w // (roof_h * 3))
        d.rectangle([inset, y, w - 1 - inset, y], fill=rc)
    d.rectangle([0, roof_h - 3, w - 1, roof_h - 2], fill=rd)   # eave shadow
    for y in range(1, roof_h - 3, 3):                          # shingle lines
        inset = max(0, (roof_h - 1 - y) * w // (roof_h * 3))
        d.line([(inset + 1, y), (w - 2 - inset, y)], fill=rl)
    # walls
    d.rectangle([2, roof_h, w - 3, h - 1], fill=PLASTER)
    d.rectangle([2, roof_h, 3, h - 1], fill=PLASTER_D)
    d.rectangle([w - 4, roof_h, w - 3, h - 1], fill=PLASTER_D)
    d.rectangle([2, h - 2, w - 3, h - 1], fill=PLASTER_D)
    # timber frame
    d.rectangle([2, roof_h, w - 3, roof_h], fill=TIMBER)
    d.rectangle([2, h - 1, w - 3, h - 1], fill=TIMBER)
    # door, centred
    dw = 10
    dx = (w - dw) // 2
    d.rectangle([dx, h - 14, dx + dw - 1, h - 1], fill=DOOR)
    d.rectangle([dx + 1, h - 13, dx + dw - 2, h - 3], fill=DOOR_L)
    d.point((dx + dw - 3, h - 8), INK)  # handle
    # windows either side of the door
    wy = h - 13
    for wx in (5, w - 12):
        d.rectangle([wx, wy, wx + 6, wy + 6], fill=INK)
        d.rectangle([wx + 1, wy + 1, wx + 5, wy + 5], fill=GLASS)
        d.line([(wx + 3, wy + 1), (wx + 3, wy + 5)], fill=GLASS_D)
        d.line([(wx + 1, wy + 3), (wx + 5, wy + 3)], fill=GLASS_D)
    if banner:
        bw = len(banner) * 2 + 4
        bx = (w - bw) // 2
        d.rectangle([bx, roof_h + 2, bx + bw, roof_h + 8], fill=banner)
        d.rectangle([bx, roof_h + 2, bx + bw, roof_h + 2], fill=INK)
    return img


def b_lab():
    # the big one: ember roof (site accent), wide, a chimney-flask
    img = building(64, 64, 26, roof=(ROOF_EMBER, ROOF_EMBER_L, ROOF_EMBER_D))
    d = ImageDraw.Draw(img)
    d.rectangle([50, 2, 55, 12], fill=PLASTER_D)   # chimney
    d.rectangle([49, 2, 56, 4], fill=INK)
    # upper window band (it's a lab, it has instruments)
    for wx in (10, 27, 44):
        d.rectangle([wx, 30, wx + 8, 36], fill=INK)
        d.rectangle([wx + 1, 31, wx + 7, 35], fill=GLASS)
    return img


def b_fountain():
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([1, 8, 30, 30], fill=PLAZA_D)
    d.ellipse([3, 10, 28, 28], fill=PLAZA)
    d.ellipse([6, 12, 25, 26], fill=WATER)
    d.ellipse([9, 14, 22, 22], fill=WATER_L)
    d.rectangle([13, 4, 18, 18], fill=PLAZA)
    d.rectangle([13, 4, 18, 5], fill=PLAZA_D)
    d.point((15, 2), WATER_L)
    d.point((16, 1), WATER_L)
    return img


def build_buildings():
    save(b_lab(), OUT_TILES / "lab.png")
    save(building(48, 56, 20), OUT_TILES / "library.png")
    save(building(48, 56, 20, roof=(ROOF_D, ROOF, (24, 40, 110))), OUT_TILES / "guild.png")
    save(building(56, 56, 22, roof=((47, 90, 105), (70, 120, 138), (33, 66, 78))), OUT_TILES / "inn.png")
    save(building(48, 56, 20, roof=(ROOF_EMBER, ROOF_EMBER_L, ROOF_EMBER_D)), OUT_TILES / "shop.png")
    save(b_fountain(), OUT_TILES / "fountain.png")


if __name__ == "__main__":
    build_michele()
    build_npcs()
    build_tiles()
    build_buildings()
    print("done.")
