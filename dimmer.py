from argparse import ArgumentParser
from gpiozero import LED 
from time import sleep

parser = ArgumentParser()
parser.add_argument('--brightness', action='store', type=float, default=1.0)
args = parser.parse_args()


brightness = args.brightness
if brightness < 0 or brightness > 1:
    raise ValueError("Brightness needs to be between 0 and 1 inclusive")

led = LED(18)

on = brightness
off = 1 - brightness
cycle = 0.01

while True:
    led.on()
    sleep(cycle * on)
    led.off()
    sleep(cycle * off)
