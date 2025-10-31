import time
import board
import neopixel

PIXEL_PIN = board.A1
NUM_PIXELS = 256
BRIGHTNESS = 0.1
BASIC_DELAY = 0.2
WIDTH = 16
HEIGHT = 16

# ----------------------------
pixels = neopixel.NeoPixel(
    PIXEL_PIN, NUM_PIXELS,
    brightness=BRIGHTNESS, auto_write=False,
    bpp=4, pixel_order=neopixel.GRBW
)


def xy_to_index(x, y):
    """Map (x,y) to 1D index for a zigzag-wired matrix (row 0 at top, x left→right)."""
    if y % 2 == 0:        # even row: left -> right
        return y * WIDTH + x
    else:                 # odd row: right -> left
        return y * WIDTH + (WIDTH - 1 - x)


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


# ---- RAINBOW SWEEP ----
# Adjust these to change look/feel:
X_SPREAD = 10   # larger = slower color change across X
Y_SPREAD = 20   # larger = slower color change across Y
SPEED = 3    # higher = faster motion

t = 0
while True:
    # Compute colors for all pixels for the current frame
    for y in range(HEIGHT):
        for x in range(WIDTH):
            hue = (t + x * X_SPREAD + y * Y_SPREAD) & 255
            pixels[xy_to_index(x, y)] = colorwheel(hue)
    pixels.show()
    t = (t + SPEED) & 255
    time.sleep(0.02)
