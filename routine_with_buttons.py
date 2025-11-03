import board
import neopixel
import time
from adafruit_circuitplayground import cp

# ------- CONFIG -------
PIN = board.A1
WIDTH = 16
HEIGHT = 16
NUM_PIXELS = WIDTH * HEIGHT
BRIGHTNESS = 0.08
PIXEL_ORDER = neopixel.GRBW   # change to GRB for RGB strips
BK = (0, 0, 0, 0)
BL = (0, 0, 255, 0)
RD = (189, 8, 8, 0)
SK = (217, 167, 57, 0)
HR = (126, 153, 83, 0)
PR = (52, 21, 57, 0)

mario = (
    (BK, BK, BK, BK, BK, BK, RD, RD, RD, RD, RD, BK, BK, BK, BK, BK),
    (BK, BK, BK, BK, BK, RD, RD, RD, RD, RD, RD, RD, RD, BK, BK, BK),
    (BK, BK, BK, BK, BK, HR, HR, HR, SK, SK, HR, SK, BK, BK, BK, BK),
    (BK, BK, BK, BK, HR, SK, HR, SK, SK, SK, PR, SK, SK, SK, BK, BK),
    (BK, BK, BK, BK, HR, SK, HR, HR, SK, SK, SK, HR, SK, SK, SK, BK),
    (BK, BK, BK, BK, HR, HR, SK, SK, SK, SK, PR, PR, PR, PR, BK, BK),
    (BK, BK, BK, BK, BK, BK, SK, SK, SK, SK, SK, SK, SK, BK, BK, BK),
    (BK, BK, BK, BK, BK, RD, RD, BL, RD, RD, RD, BK, BK, BK, BK, BK),
    (BK, BK, BK, BK, RD, RD, RD, BL, RD, RD, BL, RD, RD, RD, BK, BK),
    (BK, BK, BK, RD, RD, RD, RD, BL, BL, BL, BL, RD, RD, RD, RD, BK),
    (BK, BK, BK, SK, SK, RD, BL, SK, BL, BL, SK, BL, RD, SK, SK, BK),
    (BK, BK, BK, SK, SK, SK, BL, BL, BL, BL, BL, BL, SK, SK, BK, BK),
    (BK, BK, BK, SK, SK, BL, BL, BL, BK, BK, BL, BL, BL, SK, SK, BK),
    (BK, BK, BK, BK, BK, BL, BL, BL, BK, BK, BL, BL, BL, BK, BK, BK),
    (BK, BK, BK, BK, HR, HR, HR, BK, BK, BK, BK, HR, HR, HR, BK, BK),
    (BK, BK, BK, HR, HR, HR, HR, BK, BK, BK, BK, HR, HR, HR, HR, BK),
)

pixels = neopixel.NeoPixel(
    PIN, NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=PIXEL_ORDER
)


def xy_to_index(x, y):
    """Map (x,y) -> index for a zigzag-wired matrix, origin at top-left."""
    return y * WIDTH + (x if y % 2 == 1 else (WIDTH - 1 - x))


def set_px(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        pixels[xy_to_index(x, y)] = color


def clear(bg=(0, 0, 0, 0)):
    pixels.fill(bg)


def draw_mario():

    for i in range(len(mario)):
        for j in range(len(mario[i])):
            set_px(j, i, mario[i][j])

    pixels.show()


def colorwheel(pos):
    """0-255 -> (R,G,B[,W]); W kept 0 for RGBW strips."""
    pos = pos & 255
    if pos < 85:
        r = 255 - pos * 3
        g = pos * 3
        b = 0
    elif pos < 170:
        pos -= 85
        r = 0
        g = 255 - pos * 3
        b = pos * 3
    else:
        pos -= 170
        r = pos * 3
        g = 0
        b = 255 - pos * 3
    # Return with W channel = 0 for RGBW strips
    return (r, g, b, 0) if len(pixels[0]) == 4 else (r, g, b)


def draw_rainbow():
    # ---- RAINBOW SWEEP ----
    # Adjust these to change look/feel:
    X_SPREAD = 10   # larger = slower color change across X
    Y_SPREAD = 20   # larger = slower color change across Y

    t = 0
    # Compute colors for all pixels for the current frame
    for y in range(HEIGHT):
        for x in range(WIDTH):
            hue = (t + x * X_SPREAD + y * Y_SPREAD) & 255
            pixels[xy_to_index(x, y)] = colorwheel(hue)
    pixels.show()


def draw_letters(color=(255, 0, 0, 0), delay=0.05):
    C = (49, 50, 64, 67, 80, 96, 112, 128, 131, 145, 146)
    M = (53, 57, 69, 70, 72, 73, 85, 87, 89,
         101, 105, 117, 121, 133, 137, 149, 153)
    P = (59, 60, 61, 75, 78, 91, 94, 107, 108, 109, 123, 139, 155)
    letters = (C, M, P)
    for letter in letters:
        for px in letter:
            pixels[to_zigzag(px)] = color
            pixels.show()
            time.sleep(delay)


def to_zigzag(idx):
    row = idx // 16
    col = idx % 16
    if row % 2 == 0:  # even row: reverse column
        col = 16 - 1 - col
    return row * 16 + col


draw_letters((0, 255, 0, 0))
current = ""
while True:
    if cp.button_a:  # Checks if Button A is pressed
        time.sleep(.1)
        if current == "mario":
            clear()
            draw_letters((0, 255, 0, 0))
        else:
            clear()
            current = "mario"
            draw_mario()
    elif cp.button_b:
        if current == "rainbow":
            clear()
            draw_letters()
        else:
            clear()
            current = "rainbow"
            draw_rainbow()
