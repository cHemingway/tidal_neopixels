import tidal
from colorsys import hsv_to_rgb
from neopixel import NeoPixel

from app import TextApp

NUM_LEDS = 80
MAX_BRIGHTNESS = 0.5

TICK_MS = 25


class RaveApp(TextApp):

    TITLE = "Neopixel Rave"
    BG = tidal.st7789.BLACK
    FG = tidal.st7789.WHITE

    def rainbow(self):
        for i in range(NUM_LEDS):
            hue = ((i + self.rainbow_state) % NUM_LEDS) / NUM_LEDS
            self.leds[i] = hsv_to_rgb(hue, 1, MAX_BRIGHTNESS)
        self.leds.write()
        self.rainbow_state += 2
        if self.rainbow_state > NUM_LEDS:
            self.rainbow_state = 0

    def all_on(self):
        v = int(255 * MAX_BRIGHTNESS)
        self.leds.fill((v, v, v))
        self.leds.write()

    def all_off(self):
        v = (0, 0, 0)
        self.leds.fill(v)
        self.leds.write()

    def setup_leds(self):
        tidal.led_power_on(True)
        self.leds = NeoPixel(tidal.LED_DATA, NUM_LEDS)
        self.leds.fill((0, 0, 0))
        self.leds.write()

    def next_mode(self):
        self.current_mode = (self.current_mode + 1) % len(self.MODES)

    def update_leds(self):
        self.MODES[self.current_mode]()

    def on_start(self):
        super().on_start()
        self.MODES = [self.rainbow, self.all_on, self.all_off]
        self.rainbow_state = 0
        self.current_mode = 0
        self.buttons.on_press(tidal.JOY_LEFT, self.next_mode)
        self.buttons.on_press(tidal.JOY_RIGHT, self.next_mode)

    def on_activate(self):
        super().on_activate()
        self.setup_leds()
        tidal.led_power_on(True)
        # Timer needs to be here
        self.timer = self.periodic(TICK_MS, self.update_leds)
        # Screen writing needs to be here
        self.window.cls()
        self.window.println("L/R = Mode")
        self.window.println("U/D = Brightness")

    def on_deactivate(self):
        super().on_deactivate()
        self.all_off()
        tidal.led_power_on(False)
        self.timer.cancel()


main = RaveApp
