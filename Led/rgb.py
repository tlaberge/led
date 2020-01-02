from argparse import ArgumentParser
from gpiozero import RGBLED
from time import sleep
import logging


class RGB:
    DEFAULT_RED = 0
    DEFAULT_GREEN = 0
    DEFAULT_BLUE = 0

    def __init__(self, red_pin=18, green_pin=23, blue_pin=24, common_cathod=True):
        self.rgb_led = RGBLED(
            red_pin, green_pin, blue_pin,
            initial_value=(RGB.DEFAULT_RED, RGB.DEFAULT_GREEN, RGB.DEFAULT_BLUE),
            active_high=common_cathod  # If you're using common anode. Otherwise, set this to false.
        )
        self.running = False
        self.rgb_led.color = (RGB.DEFAULT_RED / 100.0, RGB.DEFAULT_GREEN / 100.0, RGB.DEFAULT_BLUE / 100.0)

    def run(self):
        logging.info("RGB runs")
        self.running = True
        while self.running:
            sleep(0.1)

    def stop(self):
        self.running = False
        logging.info("RGB Stops")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--red', action='store', type=float, default=0.0)
    parser.add_argument('--green', action='store', type=float, default=0.0)
    parser.add_argument('--blue', action='store',  type=float, default=0.0)
    args = parser.parse_args()

    if args.red < 0 or args.red > 100:
        raise ValueError("Parameter 'red' needs to be between 0 and 100 inclusive")

    if args.green < 0 or args.green > 100:
        raise ValueError("Parameter 'green' needs to be between 0 and 100 inclusive")

    if args.blue < 0 or args.blue > 100:
        raise ValueError("Parameter 'blue' needs to be between 0 and 100 inclusive")

    rgb = RGB(common_cathod=False)
    rgb.rgb_led.color = (args.red / 100.0, args.green / 100.0, args.blue / 100.0)
    print("Color: ", rgb.rgb_led.color, rgb.rgb_led)
    rgb.run()
    print("Done!")
