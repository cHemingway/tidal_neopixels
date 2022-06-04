from tidal import *
from textwindow import TextWindow
from colorsys import hsv_to_rgb
from neopixel import NeoPixel
from scheduler import get_scheduler
from buttons import Buttons

buttons = Buttons()

NUM_LEDS = 80
MAX_BRIGHTNESS = 0.5

TICK_MS = 25

led_power_on(True)
leds = NeoPixel(LED_DATA, NUM_LEDS)
leds.fill((50,50,50))
leds.write()

rainbow_state = 0

def rainbow():
    global rainbow_state
    for i in range(NUM_LEDS):
        hue = ((i + rainbow_state)%NUM_LEDS) / NUM_LEDS
        leds[i] = hsv_to_rgb(hue, 1, MAX_BRIGHTNESS)
    leds.write()
    rainbow_state+=3
    if rainbow_state > NUM_LEDS:
        rainbow_state = 0

def all_on():
    v = (255,255,255) * MAX_BRIGHTNESS
    leds.fill(v)
    leds.write()
    
def all_off():
    v = (0,0,0)
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


def start():
    win = TextWindow(bg=BLACK, fg=WHITE)
    win.cls()
    win.println("Press A to toggle LED mode")
    my_timer = get_scheduler().periodic(TICK_MS, update_leds)
    buttons.on_press(BUTTON_A, toggle_mode)
    buttons.on_press(BUTTON_B, toggle_mode)
    buttons.on_press(JOY_UP, toggle_mode)
    
    
main = start
