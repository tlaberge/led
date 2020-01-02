import logging
import threading
from Led.dimmer import PwmDimmer
from Led.rgb import RGB

from flask import Flask, request, render_template
from flask_socketio import SocketIO, disconnect


led_lock = threading.Lock()
client_id = None
led_dimmer = None
rgb_led = None


def run_led(dimmer):
    print(dimmer)
    dimmer.run()


def run_rgb(rgb):
    rgb.run()

# This strangeness handles the case where Flask reloads when started
# under the debug flag.


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')


@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.j2')


@socketio.on('connect', namespace='/brightness')
def on_connect():
    global client_id
    global led_dimmer

    client = request.sid
    logging.info("New dimmer client: " + str(client))
    with led_lock:
        if client_id is not None:
            logging.info("Already connected, force disconnect")
            disconnect(client)
            return
        client_id = client

    led_dimmer = PwmDimmer(18, active_high=False)
    socketio.start_background_task(run_led, led_dimmer)

    logging.info("New dimmer client: " + str(client))


@socketio.on('brightness', namespace='/brightness')
def process_brightness_message(brightness):
    logging.info("Setting brightness {}".format(brightness))
    led_dimmer.led.value = float(brightness) / 100.0


@socketio.on('disconnect', namespace='/brightness')
def on_disconnect():
    global client_id
    global led_dimmer

    client = request.sid
    with led_lock:
        if client_id != client:
            return
        led_dimmer.stop()
        led_dimmer = None
        client_id = None


@app.route('/rgb')
def rgb():
    return render_template('rgb.j2')


@socketio.on('connect', namespace='/rgb_socket')
def on_rgb_connect():
    global client_id
    global rgb_led

    client = request.sid
    logging.info("New rgb client: " + str(client))
    with led_lock:
        if client_id is not None:
            logging.info("Already connected, force disconnect")
            disconnect(client)
            return
        client_id = client

    rgb_led = RGB(common_cathod=False)
    socketio.start_background_task(run_led, rgb_led)

    logging.info("New rgb client: " + str(client))


@socketio.on('rgb', namespace='/rgb_socket')
def process_rgb_message(rgb_values):
    logging.info("Setting rgb {}".format(rgb_values))
    rgb_led.rgb_led.color = tuple(int(val) / 100.0 for val in rgb_values)


@socketio.on('disconnect', namespace='/rgb_socket')
def on_rgb_disconnect():
    global rgb_led
    global client_id

    client = request.sid
    with led_lock:
        if client_id != client:
            return
        rgb_led.stop()
        rgb_led = None
        client_id = None

