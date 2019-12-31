from argparse import ArgumentParser
from gpiozero import LED 
from time import sleep

parser = ArgumentParser()
parser.add_argument('--brightness', action='store', type=float, default=1.0)
parser.add_argument('--pulse', action='store', type=float, default=0)
args = parser.parse_args()

pulse = args.pulse / 2
if pulse < 0:
    raise ValueError("Pulse length can't be negative")
elif 0 < pulse < 0.05:
    raise ValueError("Pulse length can't be less than 0.1 seconds; set to 0 for no pulse")

brightness = args.brightness
if brightness < 0 or brightness > 1:
    raise ValueError("Brightness needs to be between 0 and 1 inclusive")

led = LED(18)

on = brightness
off = 1 - brightness
cycle = 0.01


def dimmer_cycle():

    led.on()
    sleep(cycle * on)
    led.off()
    sleep(cycle * off)


if pulse == 0:

    while True:

        dimmer_cycle()

else:

    while True:

        pulse_tick = 0

        while pulse_tick < pulse:

            dimmer_cycle()
            pulse_tick += cycle

        led.off()
        sleep(pulse)
