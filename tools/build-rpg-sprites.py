#!/usr/bin/env python3
"""
Draw every original pixel-art asset for the RPG page (rpg/assets/).

All art is generated from this file — the character from pixel-string grids
(reviewable in a text diff), the tiles and buildings procedurally — so the
whole look of Emberrest is reproducible and editable without an image
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


INK = (27, 36, 50)


def outline(img, color=INK):
    """1px dark outline around every opaque region — the SNES sprite look."""
    w, h = img.size
    src = img.load()
    out = img.copy()
    dst = out.load()
    for y in range(h):
        for x in range(w):
            if src[x, y][3] == 0 and any(
                0 <= x + dx < w and 0 <= y + dy < h and src[x + dx, y + dy][3] > 0
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            ):
                dst[x, y] = (*color, 255)
    return out


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
    down = [outline(grid_to_img(g)) for g in (DOWN_STAND, DOWN_A, DOWN_B)]
    up = [outline(grid_to_img(g)) for g in (UP_STAND, UP_A, UP_B)]
    right = [outline(grid_to_img(g)) for g in (RIGHT_STAND, RIGHT_A, RIGHT_B)]
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
    crier = [outline(grid_to_img(g, CRIER_PAL)) for g in (CRIER_A, CRIER_B)]
    cat = [outline(grid_to_img(g, CAT_PAL)) for g in (CAT_SIT, CAT_TAIL)]
    save(sheet([crier], 16, 24), OUT_SPRITES / "crier.png")
    save(sheet([cat], 16, 16), OUT_SPRITES / "cat.png")
    save(grid_to_img(SIGN, SIGN_PAL), OUT_SPRITES / "sign.png")


# ---------------------------------------------------------------------------
# Ground tiles (16x16), procedural. Order in tiles.png (one row):
#   0 grass  1 grass-speckle  2 flowers  3 path  4 path-stones
#   5 tree   6 water  7 fence  8 cobble-plaza
# ---------------------------------------------------------------------------

GRASS = (88, 152, 64)
GRASS_D = (68, 124, 50)
GRASS_L = (110, 176, 80)
PATH = (204, 176, 124)
PATH_D = (172, 142, 96)
PATH_L = (222, 198, 152)
WATER = (52, 96, 192)
WATER_L = (96, 144, 236)
WATER_W = (196, 220, 252)
TRUNK = (107, 74, 43)
TRUNK_D = (78, 52, 30)
LEAF = (38, 96, 44)
LEAF_M = (52, 126, 56)
LEAF_L = (84, 160, 76)
FENCE = (139, 100, 60)
FENCE_D = (100, 70, 40)
PLAZA = (196, 186, 168)
PLAZA_D = (166, 156, 138)
PLAZA_L = (214, 205, 189)


def tile(fill):
    img = Image.new("RGBA", (16, 16), (*fill, 255))
    return img, ImageDraw.Draw(img)


# deterministic textures — no RNG, so re-runs are byte-identical
GRASS_DARK_DASHES = [(2, 3), (11, 2), (6, 7), (13, 9), (3, 12), (9, 14), (14, 5)]
GRASS_LIGHT_DOTS = [(5, 1), (1, 8), (8, 10), (12, 13), (4, 6)]


def t_grass(speckled=False, flowers=False):
    img, d = tile(GRASS)
    for x, y in GRASS_DARK_DASHES:
        d.rectangle([x, y, min(15, x + 1), y], fill=GRASS_D)
    for x, y in GRASS_LIGHT_DOTS:
        d.point((x, y), GRASS_L)
    if speckled:
        for x, y in [(7, 4), (2, 10), (12, 7), (5, 13), (10, 1)]:
            d.rectangle([x, y, min(15, x + 1), y], fill=GRASS_D)
    if flowers:
        for x, y, c in [(3, 4, (240, 224, 120)), (11, 6, (230, 148, 148)), (6, 11, (245, 243, 238))]:
            d.point((x, y - 1), c)
            d.rectangle([x - 1, y, x + 1, y], fill=c)
            d.point((x, y + 1), c)
            d.point((x, y), (222, 186, 92))
    return img


def t_path(stones=False):
    img, d = tile(PATH)
    for x, y in [(3, 3), (12, 5), (6, 9), (10, 13), (2, 12), (14, 10)]:
        d.point((x, y), PATH_D)
    for x, y in [(8, 2), (4, 7), (13, 14)]:
        d.point((x, y), PATH_L)
    if stones:
        for x, y in [(3, 5), (10, 3), (6, 12), (12, 9)]:
            d.rectangle([x, y, x + 1, y + 1], fill=PATH_D)
            d.point((x, y), PATH_L)
    return img


def t_tree():
    img, d = tile(GRASS)
    for x, y in [(1, 14), (14, 13)]:
        d.point((x, y), GRASS_D)
    # canopy: dark base, mid body, light crown, ink rim
    d.ellipse([0, 0, 15, 11], fill=INK)
    d.ellipse([1, 1, 14, 10], fill=LEAF)
    d.ellipse([2, 1, 13, 8], fill=LEAF_M)
    d.ellipse([4, 2, 11, 6], fill=LEAF_L)
    # trunk below the canopy, with shadow edge
    d.rectangle([6, 11, 9, 15], fill=TRUNK)
    d.rectangle([6, 11, 6, 15], fill=TRUNK_D)
    d.rectangle([5, 15, 10, 15], fill=TRUNK_D)
    for x, y in [(5, 3), (9, 2), (7, 5)]:
        d.point((x, y), (200, 230, 190))
    for x, y in [(3, 8), (11, 8), (7, 10)]:
        d.point((x, y), LEAF)
    return img


def t_water():
    img, d = tile(WATER)
    for i, y in enumerate((2, 7, 12)):
        for x0 in (1, 9):
            xo = (x0 + i * 3) % 12
            d.rectangle([xo, y, xo + 3, y], fill=WATER_L)
            d.point((xo, y), WATER_W)
    d.point((13, 4), WATER_W)
    d.point((5, 10), WATER_W)
    return img


def t_fence():
    img, d = tile(GRASS)
    d.rectangle([0, 6, 15, 8], fill=FENCE)
    d.rectangle([0, 8, 15, 8], fill=FENCE_D)
    for x in (2, 8, 14):
        d.rectangle([x - 1, 3, min(15, x + 1), 12], fill=FENCE)
        d.rectangle([x - 1, 12, min(15, x + 1), 12], fill=FENCE_D)
        d.point((x, 3), (170, 130, 85))
    return img


def t_plaza():
    img, d = tile(PLAZA)
    # 8x8 flagstones with light top-left edges and dark grout
    d.line([(0, 7), (15, 7)], fill=PLAZA_D)
    d.line([(0, 15), (15, 15)], fill=PLAZA_D)
    d.line([(7, 0), (7, 7)], fill=PLAZA_D)
    d.line([(11, 8), (11, 15)], fill=PLAZA_D)
    for x, y in [(0, 0), (8, 0), (0, 8), (12, 8)]:
        d.line([(x, y), (min(15, x + 5), y)], fill=PLAZA_L)
    d.point((4, 4), PLAZA_D)
    d.point((13, 12), PLAZA_D)
    return img


def build_tiles():
    tiles = [
        t_grass(),
        t_grass(speckled=True),
        t_grass(flowers=True),
        t_path(),
        t_path(stones=True),
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
# Buildings, procedural, one PNG each. FF town look: steep outlined roofs,
# plaster + timber walls, arched doors — and each building announces its
# trade with a hanging sign (bed, book, shield, flask, potion), so an inn
# reads as an inn from across the square.
# Sprite bottoms are what main.js aligns to; heights differ per building.
# ---------------------------------------------------------------------------

PLASTER = (236, 224, 196)
PLASTER_D = (208, 192, 160)
PLASTER_L = (246, 238, 218)
TIMBER = (110, 78, 48)
TIMBER_D = (82, 56, 32)
ROOF_BLUE = (54, 88, 208)
ROOF_BLUE_L = (86, 120, 232)
ROOF_BLUE_D = (38, 62, 158)
ROOF_EMBER = (188, 92, 46)
ROOF_EMBER_L = (214, 122, 74)
ROOF_EMBER_D = (146, 66, 32)
ROOF_NIGHT = (52, 100, 116)
ROOF_NIGHT_L = (76, 128, 146)
ROOF_NIGHT_D = (36, 72, 84)
ROOF_PLUM = (108, 72, 152)
ROOF_PLUM_L = (134, 96, 180)
ROOF_PLUM_D = (80, 50, 116)
DOOR = (96, 64, 36)
DOOR_L = (126, 90, 56)
GLASS = (130, 205, 235)
GLASS_D = (86, 156, 194)
GOLD = (222, 186, 92)
EMBER = (180, 85, 43)
NIGHT = (47, 90, 105)
WHITE = (245, 243, 238)

ICON_COLS = {".": None, "K": INK, "W": WHITE, "E": EMBER, "N": NIGHT, "Y": GOLD}

ICON_BED = [
    ".......",
    ".K.....",
    ".KKKKK.",
    ".KWWEE.",
    ".KKKKK.",
    ".K...K.",
    ".......",
]

ICON_BOOK = [
    ".......",
    ".KKKKK.",
    ".KWKWK.",
    ".KWKWK.",
    ".KWKWK.",
    ".KKKKK.",
    ".......",
]

ICON_SHIELD = [
    ".KKKKK.",
    ".KNNNK.",
    ".KNENK.",
    ".KNNNK.",
    "..KNK..",
    "...K...",
    ".......",
]

ICON_FLASK = [
    "..KKK..",
    "..KWK..",
    "..KWK..",
    ".KWWWK.",
    ".KEEEK.",
    ".KKKKK.",
    ".......",
]

ICON_POTION = [
    "..KKK..",
    "..KWK..",
    ".KWWWK.",
    ".KYYYK.",
    ".KYYYK.",
    ".KKKKK.",
    ".......",
]


def draw_icon(d, icon, ox, oy):
    for y, row in enumerate(icon):
        for x, ch in enumerate(row):
            c = ICON_COLS[ch]
            if c is not None:
                d.point((ox + x, oy + y), c)


def hanging_sign(d, icon, x, y):
    """A 9x11 wooden sign board hanging from a bracket at (x, y) topleft."""
    d.rectangle([x + 3, y, x + 8, y], fill=TIMBER_D)         # bracket arm
    d.point((x + 4, y + 1), TIMBER_D)                        # chain
    d.point((x + 7, y + 1), TIMBER_D)
    d.rectangle([x + 1, y + 2, x + 9, y + 10], fill=TIMBER)  # board
    d.rectangle([x + 1, y + 2, x + 9, y + 2], fill=TIMBER_D)
    d.rectangle([x + 1, y + 10, x + 9, y + 10], fill=TIMBER_D)
    draw_icon(d, icon, x + 2, y + 3)


def roof_trapezoid(d, w, roof_h, cols):
    """Steep FF gable: the ridge is ~40% of the width, edges trimmed light."""
    rc, rl, rd = cols
    half_span = w * 0.30                      # total inset per side at the ridge
    for y in range(roof_h):
        inset = int((roof_h - 1 - y) * half_span / max(1, roof_h - 1))
        d.rectangle([inset, y, w - 1 - inset, y], fill=rc)
        if 1 <= y < roof_h - 3 and y % 3 == 1:
            d.line([(inset + 1, y), (w - 2 - inset, y)], fill=rl)
        if 0 < y < roof_h - 2:                # slanted edge trim
            d.point((inset, y), rl)
            d.point((w - 1 - inset, y), rd)
    top_inset = int(half_span)
    d.rectangle([top_inset, 0, w - 1 - top_inset, 0], fill=rd)   # ridge cap
    d.rectangle([0, roof_h - 3, w - 1, roof_h - 2], fill=rd)     # eave shadow
    d.rectangle([0, roof_h - 1, w - 1, roof_h - 1], fill=INK)    # eave line


def window(d, x, y, w=7, h=7):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=INK)
    d.rectangle([x + 1, y + 1, x + w - 2, y + h - 2], fill=GLASS)
    d.line([(x + w // 2, y + 1), (x + w // 2, y + h - 2)], fill=GLASS_D)
    d.line([(x + 1, y + h // 2), (x + w - 2, y + h // 2)], fill=GLASS_D)
    d.point((x + 1, y + 1), (200, 235, 248))
    d.rectangle([x, y + h, x + w - 1, y + h], fill=PLASTER_D)    # sill


def arched_door(d, x, y_bottom, dw=10, dh=14):
    y0 = y_bottom - dh + 1
    d.rectangle([x, y0 + 2, x + dw - 1, y_bottom], fill=INK)
    d.rectangle([x + 1, y0, x + dw - 2, y_bottom], fill=INK)
    d.rectangle([x + 1, y0 + 3, x + dw - 2, y_bottom], fill=DOOR)
    d.rectangle([x + 2, y0 + 1, x + dw - 3, y_bottom], fill=DOOR)
    for px in range(x + 2, x + dw - 2, 2):                       # planks
        d.line([(px, y0 + 2), (px, y_bottom - 1)], fill=DOOR_L)
    d.point((x + dw - 3, y_bottom - 6), GOLD)                    # handle


def house(w, h, roof_h, roof_cols, sign_icon=None, stories=1,
          awning=False, chimney=False, pennant=False):
    """FF-style house. The sign, door and windows share the ground floor on a
    fixed grid that never overlaps: [sign] [door] [window] on narrow walls,
    [window] [sign] [door] [window] on wide (>=64) ones."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    roof_trapezoid(d, w, roof_h, roof_cols)
    # walls: 2px inset from the roof edges
    d.rectangle([2, roof_h, w - 3, h - 1], fill=PLASTER)
    d.rectangle([3, roof_h, w - 4, roof_h + 1], fill=PLASTER_L)  # light under eave
    # timber frame: corner posts, base, beam under eave
    d.rectangle([2, roof_h, 3, h - 1], fill=TIMBER)
    d.rectangle([w - 4, roof_h, w - 3, h - 1], fill=TIMBER)
    d.rectangle([2, h - 2, w - 3, h - 1], fill=TIMBER)
    d.rectangle([2, h - 1, w - 3, h - 1], fill=TIMBER_D)
    if stories == 2:
        mid = roof_h + (h - roof_h) // 2 - 2
        d.rectangle([2, mid, w - 3, mid + 1], fill=TIMBER)       # storey beam
        window(d, 8, roof_h + 4)                                 # upper windows
        window(d, w - 15, roof_h + 4)
    # ground floor layout — door centred on the sprite
    dw = 10
    dx = (w - dw) // 2
    arched_door(d, dx, h - 3)
    wy = h - 15
    sign_x = dx - 14
    if sign_icon is not None and sign_x >= 19:
        # wide wall: window, then sign, then door — all clear of each other
        window(d, 6, wy)
    elif sign_icon is not None:
        sign_x = 6                                               # sign replaces the left window
    else:
        window(d, 6, wy)
    window(d, w - 13, wy)                                        # right window always fits
    if sign_icon is not None:
        hanging_sign(d, sign_icon, sign_x, h - 18)
    if awning:
        ax0, ax1 = dx - 5, dx + dw + 4
        ay = h - 19
        for i, x in enumerate(range(ax0, ax1 + 1)):
            c = EMBER if (i // 3) % 2 == 0 else WHITE
            d.line([(x, ay), (x, ay + 4)], fill=c)
            if (i // 3) % 2 == 0 and i % 3 == 1:
                d.point((x, ay + 5), EMBER)                      # scalloped edge
        d.rectangle([ax0, ay, ax1, ay], fill=INK)
        d.rectangle([ax0, ay - 1, ax1, ay - 1], fill=TIMBER_D)
    if chimney:
        d.rectangle([w - 16, 3, w - 11, roof_h - 2], fill=PLASTER_D)
        d.rectangle([w - 17, 3, w - 10, 5], fill=INK)
        d.point((w - 14, 1), (210, 210, 210))                    # smoke
    if pennant:
        px = w // 2
        d.rectangle([px, 0, px, 6], fill=TIMBER_D)
        d.polygon([(px + 1, 0), (px + 7, 2), (px + 1, 4)], fill=EMBER)
    return outline(img)


def b_fountain():
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([1, 8, 30, 30], fill=PLAZA_D)
    d.ellipse([3, 10, 28, 28], fill=PLAZA)
    d.ellipse([4, 11, 27, 20], fill=PLAZA_L)
    d.ellipse([6, 12, 25, 26], fill=WATER)
    d.ellipse([9, 14, 22, 22], fill=WATER_L)
    d.point((12, 16), WATER_W)
    d.point((19, 19), WATER_W)
    d.rectangle([13, 4, 18, 18], fill=PLAZA)
    d.rectangle([13, 4, 14, 18], fill=PLAZA_L)
    d.rectangle([12, 3, 19, 4], fill=PLAZA_D)
    d.point((15, 1), WATER_L)
    d.point((16, 0), WATER_W)
    d.point((14, 2), WATER_W)
    return outline(img)


# Squarer proportions than the first pass — main.js aligns each sprite's
# bottom to the paths and keeps the door centres on the interact zones.
def build_buildings():
    save(house(72, 68, 26, (ROOF_EMBER, ROOF_EMBER_L, ROOF_EMBER_D),
               sign_icon=ICON_FLASK, chimney=True), OUT_TILES / "lab.png")
    save(house(56, 58, 22, (ROOF_BLUE, ROOF_BLUE_L, ROOF_BLUE_D),
               sign_icon=ICON_BOOK), OUT_TILES / "library.png")
    save(house(56, 58, 22, (ROOF_PLUM, ROOF_PLUM_L, ROOF_PLUM_D),
               sign_icon=ICON_SHIELD, pennant=True), OUT_TILES / "guild.png")
    save(house(64, 72, 24, (ROOF_NIGHT, ROOF_NIGHT_L, ROOF_NIGHT_D),
               sign_icon=ICON_BED, stories=2), OUT_TILES / "inn.png")
    save(house(56, 58, 22, (ROOF_EMBER, ROOF_EMBER_L, ROOF_EMBER_D),
               sign_icon=ICON_POTION, awning=True), OUT_TILES / "shop.png")
    save(b_fountain(), OUT_TILES / "fountain.png")



if __name__ == "__main__":
    build_michele()
    build_npcs()
    build_tiles()
    build_buildings()
    print("done.")
