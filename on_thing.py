import board
import neopixel
import time

leds = neopixel.NeoPixel(board.NEOPIXEL,10)
print("hi")

for i in range(3):
    leds.fill((0,0,255))
    time.sleep(.05)
    leds.fill((0,0,0))
    time.sleep(.05)


while True:
    foo = input()
    print(foo)
    try:
        color = [int(i) for i in foo.split(',')]
        leds.fill(color)
    except:
        for i in range(5):
            leds.fill((255,0,0))
            time.sleep(.05)
            leds.fill((0,0,0))
            time.sleep(.05)
