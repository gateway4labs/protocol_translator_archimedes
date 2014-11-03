import urlparse

import redis
import time
from flask import Flask, request
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

import archimedes_devices.status as status

@sockets.route('/devices/sensors')
def echo_socket(ws):
    arguments = urlparse.parse_qs(ws.environ['QUERY_STRING'])
    # { 'reservation_id' : ['foo'] }
    reservation_ids = arguments.get('reservation_id', [])
    sensor_ids = arguments.get('sensor_id', [])
    lab_ids = arguments.get('lab_id', [])

    if reservation_ids and sensor_ids and lab_ids:
        reservation_id = reservation_ids[0]
        sensor_id = sensor_ids[0]
        lab_id = lab_ids[0]
    else:
        ws.send("ERROR: fields missing (check reservation_id, sensor_id and lab_id)")
        ws.close()
        return

    status.new_reservation(reservation_id)

    previous_data = {}
    for new_data in status.get_notifications():
        ws.send("Sensor data for %s: %s" % (reservation_id, time.asctime()))

    ws.close()

@app.route('/')
def hello():
    return 'Hello World!'
