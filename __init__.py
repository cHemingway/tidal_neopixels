import tidal
from colorsys import hsv_to_rgb
from neopixel import NeoPixel

from app import TextApp

NUM_LEDS = 80
MAX_BRIGHTNESS = 0.7 # From 0 to 1, Adjust this to what your power supply can handle!

TICK_MS = 25

STROBE_HZ = 3 # 180 beats to win it
STROBE_MS = int((1/STROBE_HZ) * 1000)
STROBE_TICKS = int(STROBE_MS / TICK_MS + 0.5)

class RaveApp(TextApp):

    TITLE = "Neopixel Rave"
    BG = tidal.st7789.BLACK
    FG = tidal.st7789.WHITE

    def rainbow(self):
        for i in range(NUM_LEDS):
            hue = ((i + self.rainbow_state) % NUM_LEDS) / NUM_LEDS
            self.leds[i] = hsv_to_rgb(hue, 1, self.brightness)
        self.leds.write()
        self.rainbow_state += 2
        if self.rainbow_state > NUM_LEDS:
            self.rainbow_state = 0

    def rainbow_slow(self):
        for i in range(NUM_LEDS):
            hue = ((i + self.rainbow_state) % NUM_LEDS) / NUM_LEDS
            self.leds[i] = hsv_to_rgb(hue, 1, self.brightness)
        self.leds.write()
        self.rainbow_state += 1
        if self.rainbow_state > NUM_LEDS:
            self.rainbow_state = 0

    def all_on(self):
        v = int(255 * self.brightness)
        self.leds.fill((v, v, v))
        self.leds.write()

    def all_off(self):
        v = (0, 0, 0)
        self.leds.fill(v)
        self.leds.write()

    def strobe(self):
        # Add variables first pass
        if not hasattr(self, "strobe_counter"):
            self.strobe_counter = 0
        
        self.strobe_counter += 1
        if self.strobe_counter > STROBE_TICKS:
            v = int(255 * self.brightness)
            self.leds.fill((v,v,v))
            self.strobe_counter = 0
        else:
            self.leds.fill((0,0,0))
        
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

    def brightness_up(self):
        self.brightness = min(self.brightness+0.1, MAX_BRIGHTNESS)

    def brightness_down(self):
        self.brightness = max(self.brightness-0.1, 0)

    def on_start(self):
        super().on_start()
        self.MODES = [self.rainbow, self.rainbow_slow, self.all_on, self.all_off, self.strobe]
        self.rainbow_state = 0
        self.current_mode = 0
        self.brightness = 0.5
        self.buttons.on_press(tidal.JOY_LEFT, self.next_mode)
        self.buttons.on_press(tidal.JOY_RIGHT, self.next_mode)
        self.buttons.on_press(tidal.JOY_UP, self.brightness_up)
        self.buttons.on_press(tidal.JOY_DOWN, self.brightness_down)

    def on_activate(self):
        super().on_activate()
        self.setup_leds()
        tidal.led_power_on(True)
        # Timer needs to be here
        self.timer = self.periodic(TICK_MS, self.update_leds)
        # Screen writing needs to be here
        self.window.cls()
        self.window.println("Solder to J3 Pin 1")
        self.window.println("L/R = Mode")
        self.window.println("U/D = Brightness")

    def on_deactivate(self):
        super().on_deactivate()
        self.all_off()
        tidal.led_power_on(False)
        self.timer.cancel()


main = RaveApp
