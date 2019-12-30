from argparse import ArgumentParser
from gpiozero import LED 
from time import sleep

parser = ArgumentParser()
parser.add_argument('--brightness', action='store', type=float, default=1.0)
parser.add_argument('--pulse', action='store', type=float, default=0)
args = parser.parse_args()

pulse = args.pulse
if pulse < 0:
    raise ValueError("Pulse length can't be negative")

brightness = args.brightness
if brightness < 0 or brightness > 1:
    raise ValueError("Brightness needs to be between 0 and 1 inclusive")

led = LED(18)

on = brightness
off = 1 - brightness
cycle = 0.01

while True:

    while pulse_tick < pulse:

        led.on()
        sleep(cycle * on)
        led.off()
        sleep(cycle * off)
        pulse_tick = pulse_tick + cycle

    pulse_tick = 0
    led.off()
    sleep(pulse)
