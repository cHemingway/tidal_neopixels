import tidal
from colorsys import hsv_to_rgb
from neopixel import NeoPixel

from app import TextApp

NUM_LEDS = 80
MAX_BRIGHTNESS = 0.5

TICK_MS = 25

tidal.led_power_on(True)
leds = NeoPixel(tidal.LED_DATA, NUM_LEDS)
leds.fill((50, 50, 50))
leds.write()

rainbow_state = 0


def rainbow():
    global rainbow_state
    for i in range(NUM_LEDS):
        hue = ((i + rainbow_state) % NUM_LEDS) / NUM_LEDS
        leds[i] = hsv_to_rgb(hue, 1, MAX_BRIGHTNESS)
    leds.write()
    rainbow_state += 3
    if rainbow_state > NUM_LEDS:
        rainbow_state = 0


def all_on():
    v = (255, 255, 255) * MAX_BRIGHTNESS
    leds.fill(v)
    leds.write()


def all_off():
    v = (0, 0, 0)
    leds.fill(v)
    leds.write()


MODES = [
    rainbow,
    all_on,
    all_off
]

current_mode = 0

def toggle_mode():
    global current_mode
    current_mode = (current_mode + 1) % len(MODES)

def update_leds():
    MODES[current_mode]()

class MyApp(TextApp):

    TITLE = "Neopixel Rave"
    
    def on_start(self):
        super().on_start()
        self.buttons.on_press(tidal.JOY_UP, toggle_mode)
        self.timer = self.periodic(TICK_MS, update_leds)
        self.window.println("Press Joy Left to change mode!")
        self.window.println("Press Joy up/down to change LEDs")

    def on_activate(self):
        super().on_activate()

    def on_deactivate(self):
        super().on_deactivate()
        self.timer.cancel()

main = MyApp
