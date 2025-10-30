import time
import board
import neopixel

PIXEL_PIN = board.A1
NUM_PIXELS = 256
BRIGHTNESS = 0.1
BASIC_DELAY = 0.2
WIDTH = 16
HEIGHT = 16


pellets = (
    (125, ),
    (123, ),
    (121, ),
    (119, ),
    (117,),
    (115, 99, 131),
    (114, )
)

pac_path = (
    (125, ),
    (124, ),
    (123, ),
    (122, ),
    (121, ),
    (120, ),
    (119,),
    (118,),
    (117,),
    (116,),
    (115, 131, 115, 99, 115),
    (114,)
)

pac_runaway = {"start": pac_path[-1][-1], "end": pac_path[0][0]}

# ----------------------------
pixels = neopixel.NeoPixel(
    PIXEL_PIN, NUM_PIXELS,
    brightness=BRIGHTNESS, auto_write=False,
    bpp=4, pixel_order=neopixel.GRBW
)


def to_zigzag(idx):
    row = idx // WIDTH
    col = idx % WIDTH
    if row % 2 == 0:  # odd row: reverse column
        col = WIDTH - 1 - col
    return row * WIDTH + col


def safe_set(idx, color):
    # if idx in VALID and 0 <= idx < NUM_PIXELS:

    pixels[to_zigzag(idx)] = color


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
            # The following 3 lines cause error
            # ghost_loc = i - (j+distance_between)
            if i - (j+distance_between) < 112:  # hacky patch
                continue
            safe_set(i - (j+distance_between), ghost_color)

        show_and_wait(delay)
    # clear_all()
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
    for i in range(pac_runaway["start"], -15, -16):
        if i >= 0:
            safe_set(i, color)
        safe_set(i+16, (0, 0, 0, 0))
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
    C = (49, 50, 64, 67, 80, 96, 112, 128, 131, 145, 146)
    M = (53, 57, 69, 70, 72, 73, 85, 87, 89,
         101, 105, 117, 121, 133, 137, 149, 153)
    P = (59, 60, 61, 75, 78, 91, 94, 107, 108, 109, 123, 139, 155)
    letters = (C, M, P)
    for letter in letters:
        for px in letter:
            safe_set(px, color)
            show_and_wait(delay)


def clear_all():
    pixels.fill((0, 0, 0, 0))
    pixels.show()


def draw_arrow(color=(255, 0, 0, 0), col_delay=0.05, px_delay=0.02):
    arrow = (
        (110, 126, 142),
        (109, 125, 141),
        (108, 124, 140),
        (107, 123, 139),
        (106, 122, 138),
        (105, 121, 137),
        (104, 120, 136),
        (103, 119, 135),
        (102, 118, 134),
        (101, 117, 133),
        (68, 84, 100, 116, 132, 148, 164),
        (83, 99, 115, 131, 147),
        (98, 114, 130),
        (113,)
    )
    for i, col in enumerate(arrow):
        if i in [0, 10, len(arrow)-1]:
            for val in col:
                # patch:
                if val == 116:
                    continue
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

    # # PAC MAN MODE:
    draw_pellets()
    time.sleep(BASIC_DELAY)

    move_pac(delay=BASIC_DELAY)
    time.sleep(BASIC_DELAY)

    # Hide the arrow
    draw_arrow(color=(0, 0, 0, 0))
    time.sleep(BASIC_DELAY)

    # # run from ghosts, then get a pellet and eat them. Run away.
    pac_runaway_from_ghosts(delay=BASIC_DELAY, flee_speed=.05)
    time.sleep(BASIC_DELAY)
    clear_all()

    time.sleep(BASIC_DELAY)
