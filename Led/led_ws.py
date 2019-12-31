import logging
import threading
from Led.dimmer import Dimmer

from flask import Flask, request, render_template
from flask_socketio import SocketIO, disconnect


led_lock = threading.Lock()
client_id = None
led_dimmer: Dimmer = Dimmer(pin=18)


def run_led(dimmer):
    print(dimmer)
    dimmer.run()

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

    client = request.sid
    logging.info("New dimmer client: " + str(client))
    with led_lock:
        if client_id is not None:
            logging.info("Already connected, force disconnect")
            disconnect(client)
            return
        client_id = client

    socketio.start_background_task(run_led, led_dimmer)

    logging.info("New dimmer client: " + str(client))


@socketio.on('brightness', namespace='/brightness')
def process_brightness_message(brightness):
    logging.info("Setting brightness {}".format(brightness))
    led_dimmer.brightness = float(brightness)


@socketio.on('disconnect', namespace='/brightness')
def on_disconnect():
    global client_id

    client = request.sid
    with led_lock:
        if client_id != client:
            return
        led_dimmer.stop()
        client_id = None
