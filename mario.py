import board
import neopixel
import time

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

mario = (
    (BK, BK, BK, BK, BK, BK, RD, RD, RD, RD, RD, BK, BK, BK, BK, BK),
    (BK, BK, BK, BK, BK, RD, RD, RD, RD, RD, RD, RD, RD, BK, BK, BK),
    (BK, BK, BK, BK, BK, HR, HR, HR, SK, SK, HR, SK, BK, BK, BK, BK),
    (BK, BK, BK, BK, HR, SK, HR, SK, SK, SK, HR, SK, SK, SK, BK, BK),
    (BK, BK, BK, BK, HR, SK, HR, HR, SK, SK, SK, HR, SK, SK, SK, BK),
    (BK, BK, BK, BK, HR, HR, SK, SK, SK, SK, HR, HR, HR, HR, BK, BK),
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
    return y * WIDTH + (x if y % 2 == 0 else (WIDTH - 1 - x))


def set_px(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        pixels[xy_to_index(x, y)] = color


def clear(bg=BL):
    pixels.fill(bg)


def draw_mario():

    for i in range(len(mario)):
        for j in range(len(mario[i])):
            set_px(j, i, mario[i][j])

    pixels.show()


# --- Draw once (keep lit) ---
draw_mario()
