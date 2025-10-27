import time
import random
import board
import neopixel
from adafruit_circuitplayground import cp

PIXEL_PIN = board.A1
NUM_PIXELS = 240
BRIGHTNESS = 0.01
BASIC_DELAY = 0.2

C = (158, 188, 156, 125, 94, 63, 33, 65)
M = (36, 67, 98, 129, 160, 191, 161, 131, 163, 195, 164, 133, 102, 71, 40)
P = (42, 73, 104, 135, 166, 197, 198, 168, 136)
letters = (C, M, P)

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
    (126,)
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
)

pac_runaway = {"start": pac_path[-1][-1], "end": pac_path[0][0]}

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


def pac_runaway_from_ghosts(color=(255, 255, 0, 0), delay=0.1, flee_speed=0.1):
    super_color = (0, 0, 0, 150)
    safe_set(pac_runaway["end"], super_color)
    show_and_wait(delay)
    distance_between = 2
    ghosts = (
        (255, 0, 0, 0),
        (255, 184, 255, 0),
        (0, 255, 255, 0),
        (255, 184, 82, 0)
    )

    for i in range(pac_runaway["start"], pac_runaway["end"]):
        pixels.fill((0, 0, 0, 0))
        safe_set(pac_runaway["end"], super_color)
        safe_set(i, color)
        for j, ghost_color in enumerate(ghosts):
            safe_set(i - (j+distance_between), ghost_color)

        show_and_wait(delay)
    clear_all()
    for i in range(pac_runaway["end"], pac_runaway["start"]-1, -1):
        count = 0
        for j in range(len(ghosts)-1, -1, -1):
            ghost_loc = i - (j+distance_between)
            if ghost_loc >= pac_runaway["start"] + count:
                safe_set(ghost_loc, (0, 0, 255, 0))
                safe_set(ghost_loc + 1, (0, 0, 0, 0))
            count += 1
        safe_set(i, color)
        safe_set(i+1, (0, 0, 0, 0))
        show_and_wait(delay)
    for i in range(pac_runaway["start"], pac_runaway["start"]-8, -1):
        safe_set(i, color)
        safe_set(i+1, (0, 0, 0, 0))
        show_and_wait(flee_speed)


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
    draw_letters(color=(0, 255, 0, 0), delay=0.05)
    time.sleep(0.3)

    # 2) Clear
    clear_all()
    time.sleep(0.05)

    # 3) Draw arrow
    draw_arrow(color=(0, 255, 0, 0), col_delay=0.05,
               px_delay=0.01)  # green
    time.sleep(BASIC_DELAY)

    draw_arrow(color=(0, 0, 255, 0), col_delay=0.05,
               px_delay=0.01)  # blue
    time.sleep(BASIC_DELAY)
    # PAC MAN MODE:
    draw_pellets()
    time.sleep(BASIC_DELAY)

    move_pac(delay=BASIC_DELAY)
    time.sleep(BASIC_DELAY)

    # Hide the arrow
    draw_arrow(color=(0, 0, 0, 0))
    time.sleep(BASIC_DELAY)

    # run from ghosts, then get a pellet and eat them. Run away.
    pac_runaway_from_ghosts(delay=BASIC_DELAY, flee_speed=.05)
    time.sleep(BASIC_DELAY)
    clear_all()

    time.sleep(BASIC_DELAY)
