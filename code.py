import time
import random
import board
import neopixel
from adafruit_circuitplayground import cp

PIXEL_PIN = board.A1
NUM_PIXELS = 240
BRIGHTNESS = 0.01

# ----------------------------
# GRID & BOUNDS (8 rows x 14 cols)
# Top-left is 218, bottom-right is 14
# ----------------------------
# Too memory hungry
# GRID = [
#     [218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231],
#     [187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200],
#     [156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169],
#     [125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138],
#     [94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107],
#     [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76],
#     [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45],
#     [1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14],
# ]
# VALID = {idx for row in GRID for idx in row}

# ----------------------------
# SHAPES
# ----------------------------
C = (158, 188, 156, 125, 94, 63, 33, 65)
M = (36, 67, 98, 129, 160, 191, 161, 131, 163, 195, 164, 133, 102, 71, 40)
P = (42, 73, 104, 135, 166, 197, 198, 168, 136)
letters = (C, M, P)

# Arrow described column-by-column (left-to-right). Last one must be a 1-tuple.
arrow = (
    (168, 137, 106),
    (167, 136, 105),
    (166, 135, 104),
    (165, 134, 103),
    (164, 133, 102),
    (163, 132, 101),
    (162, 131, 100),
    (161, 130, 99),
    (222, 191, 160, 129, 98, 67, 36),
    (190, 159, 128, 97, 66),
    (158, 127, 96),
    (126,)   # <- 1-tuple so it's iterable
)

pellets = (
    (136, ),

    (134, ),

    (132, ),

    (130, ),
    (129,),
    (159, 128, 97),
    (127, )
)

pac_path = (
    (136, ),
    (135, ),
    (134, ),
    (133, ),
    (132, ),
    (131, ),
    (130,),
    (129,),
    (128, 97, 128, 159, 128),
    (127,)
    # <- 1-tuple so it's iterable
)

pac_runaway = ((139,), (138,), (137,)) + pac_path
# ----------------------------
# NeoPixel setup (RGBW strip)
# NOTE: pixel_order=neopixel.GRBW means tuple is (G,R,B,W)
# So "yellow" is (G=255, R=255, B=0, W=0)
# ----------------------------
pixels = neopixel.NeoPixel(
    PIXEL_PIN, NUM_PIXELS,
    brightness=BRIGHTNESS, auto_write=False,
    bpp=4, pixel_order=neopixel.GRBW
)


def safe_set(idx, color):
    """Set pixel only if idx is inside the 8x14 grid and valid for the strip."""
    # if idx in VALID and 0 <= idx < NUM_PIXELS:
    pixels[idx] = color


def show_and_wait(t=0.05):
    pixels.show()
    time.sleep(t)


def move_pac(path=pac_path, color=(255, 255, 0, 0), delay=0.05):
    last = None
    for move in path:
        for pellet in move:
            safe_set(pellet, color)
            if last:
                safe_set(last, (0, 0, 0, 0))
            show_and_wait(delay)
            last = pellet


def draw_pellets(color=(0, 0, 0, 150), delay=0.05):
    for pellet in pellets:
        for px in pellet:
            safe_set(px, color)
            show_and_wait(delay)


def draw_letters(color=(255, 0, 0, 0), delay=0.05):
    """Draw CMP one pixel at a time."""
    for letter in letters:
        for px in letter:
            safe_set(px, color)
            show_and_wait(delay)


def clear_all():
    pixels.fill((0, 0, 0, 0))
    pixels.show()


def draw_arrow(color=(255, 0, 0, 0), col_delay=0.05, px_delay=0.02):
    """Draw the arrow column-by-column (left to right)."""
    for i, col in enumerate(arrow):
        if i in [0, 8]:
            for val in col:
                safe_set(val, color)
        else:
            px = col[0]
            safe_set(px, color)
            px = col[-1]
            safe_set(px, color)
        show_and_wait(px_delay)
        time.sleep(col_delay)


# ----------------------------
# MAIN LOOP
# ----------------------------
while True:
    # 1) Draw CMP
    # (G,R,B,W) -> bright red in GRBW is (0,255,0,0)
    draw_letters(color=(0, 255, 0, 0), delay=0.05)
    time.sleep(0.3)

    # 2) Clear
    clear_all()
    time.sleep(0.05)

    # 3) Draw arrow
    draw_arrow(color=(0, 255, 0, 0), col_delay=0.05,
               px_delay=0.01)  # red (in GRBW)
    time.sleep(0.2)

    draw_arrow(color=(0, 0, 255, 0), col_delay=0.05,
               px_delay=0.01)  # red (in GRBW)
    time.sleep(0.2)

    draw_pellets()
    time.sleep(0.2)

    move_pac(delay=.2)
    time.sleep(0.2)
    draw_arrow(color=(0, 0, 0, 0))
    time.sleep(0.2)

    move_pac(tuple(reversed(pac_runaway)))
    # Tiny pause and reset
    time.sleep(0.2)
    clear_all()
    time.sleep(0.2)
