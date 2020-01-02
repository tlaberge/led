from argparse import ArgumentParser
from gpiozero import LED, PWMLED
from time import sleep
import logging


class AbstractDimmer:
    DEFAULT_BRIGHTNESS = 50

    def __init__(self, pin, brightness=DEFAULT_BRIGHTNESS):
        self.pin = pin
        if not (0 <= brightness <= 100):
            raise ValueError("Brightness must be between 0 and 100, inclusive")

        self.brightness = brightness
        self.running = False

    def run(self):
        raise NotImplementedError("Override run() in the derived class")

    def stop(self):
        raise NotImplementedError("Override stop() in the derived clss")


class LedDimmer(AbstractDimmer):
    DEFAULT_CYCLE = 0.01

    def __init__(self, pin, brightness=AbstractDimmer.DEFAULT_BRIGHTNESS, cycle=DEFAULT_CYCLE):
        super().__init__(pin, brightness)
        self.led = LED(self.pin)
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


class PwmDimmer(AbstractDimmer):

    def __init__(self, pin, brightness=AbstractDimmer.DEFAULT_BRIGHTNESS, active_high=True):
        super().__init__(pin, brightness)
        self.led = PWMLED(self.pin, active_high=active_high)
        self.running = False

    def run(self):
        logging.info("PwmDimmer runs")
        self.running = True
        self.led.value = self.brightness / 100.0
        while self.running:
            sleep(0.1)
        self.led.value = 0

    def stop(self):
        self.running = False
        logging.info("PwmDimmer Stops")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--brightness', action='store', type=float, default=50.0)
    args = parser.parse_args()

    if args.brightness < 0 or args.brightness > 100:
        raise ValueError("Brightness needs to be between 0 and 100 inclusive")

    dimmer = LedDimmer(18, args.brightness)
    dimmer.run()
