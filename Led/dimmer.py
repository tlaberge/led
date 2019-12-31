from argparse import ArgumentParser
from gpiozero import LED 
from time import sleep, time
import logging

from queue import Queue


class Dimmer:
    DEFAULT_BRIGHTNESS = 50
    DEFAULT_CYCLE = 0.01

    def __init__(self, pin, brightness=DEFAULT_BRIGHTNESS, cycle=DEFAULT_CYCLE):
        self.led = LED(pin)
        if not (0 <= brightness <= 100):
            raise ValueError("Brightness must be between 0 and 100, inclusive")

        self.brightness = brightness
        self.cycle = cycle
        self.running = False

    @property
    def on_time(self):
        return self.brightness / 100.0 * self.cycle

    @property
    def off_time(self):
        return self.cycle - self.on_time

    def run(self):
        logging.info("Dimmer runs")
        self.running = True
        while self.running:
            self.led.on()
            sleep(self.on_time)
            self.led.off()
            sleep(self.off_time)


    def stop(self):
        self.running = False
        logging.info("Dimmer Stops")


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--brightness', action='store', type=float, default=50.0)
    args = parser.parse_args()

    brightness = args.brightness
    if brightness < 0 or brightness > 100:
        raise ValueError("Brightness needs to be between 0 and 1 inclusive")

    dimmer = Dimmer(18, args.brightness)
    dimmer.run()
