from argparse import ArgumentParser
from gpiozero import LED
from time import sleep

parser = ArgumentParser()
parser.add_argument('--brightness', action='store', type=float, default=1.0)
args = parser.parse_args()


led = LED(18)
led.on()

if round(args.brightness, 2) == 1:
    led.on()
elif round(args.brightness, 2) == 0:
    led.off()
else:
    while True:
        led.on()
        sleep(.001 * args.brightness)
        led.off()
        sleep(.001 / args.brightness)  
