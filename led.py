from argparse import ArgumentParser
from gpiozero import LED 
from time import sleep

parser = ArgumentParser()
parser.add_argument('--delay', action='store', type=float, default=1.0)
args = parser.parse_args()


led = LED(18)
while True:
    led.on()
    sleep(args.delay)
    led.off()
    sleep(args.delay)
