For Tidal V6 Badge for EMFCamp 2022

Wire up some WS2812/Neopixels to your badge and display some simple patterns. 

## Features
- Joystick adjusts patterns and brightness
- Patterns: Rainbow, slower rainbow, all on, all off, 3Hz flash
- Currently up to 80 supported, easy to change by editing the code.
- Adjustable (in code) max brightness to save power

## Wiring
There is probably some issue with this wiring, the LEDs often come on dimly after powering up. 

### Data
I soldered to the input pin of the Torch LED D1 (see the [schematics](https://github.com/emfcamp/tidal-docs/blob/main/schematics/tidal-bot.pdf)) but J3 pin 1 would also work (and be a bit easier)

I initially tried just using the expansion pins, but without a level shifter (already present for the torch) the WS2812 won't work.

### Power
An LED strip requires quite a bit more power than the badge battery can likely take, and 5V rather than 3.3V. I have the power line connected to the 5V pad on the top board.
I also soldered a USB cable to the pads on the top board, so I can power the strip (and the badge) from a USB power bank. If you have a USB-C power bank, this isn't needed.