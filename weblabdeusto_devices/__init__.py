import urlparse

import redis
import time
import json
from flask import Flask, request, render_template, render_template_string
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

import weblabdeusto_devices.status as status
from weblabdeusto_devices.ext import LABS

@sockets.route('/devices/sensors')
def echo_socket(ws):
    arguments = urlparse.parse_qs(ws.environ['QUERY_STRING'])
    # { 'reservation_id' : ['foo'] }
    reservation_ids = arguments.get('reservation_id', [])
    lab_ids = arguments.get('lab_id', [])

    if reservation_ids and lab_ids:
        reservation_id = reservation_ids[0]
        lab_id = lab_ids[0]
    else:
        ws.send(json.dumps({ 'error' : True, 'message' : "fields missing (check reservation_id and lab_id)" }))
        ws.close()
        return

    if lab_id not in LABS:
        ws.send(json.dumps({ 'error' : True, 'message' : "invalid lab (not found in list)" }))
        ws.close()
        return

    current_lab = LABS[lab_id]

    status.new_reservation(reservation_id, current_lab)

    while True:
        txtmsg = ws.receive()
        message = json.loads(txtmsg)
        method = message.get('method')
        if method == 'getSensorMetadata':
            metadata = current_lab.get_sensor_metadata(reservation_id, message)
            ws.send(json.dumps(metadata))
        elif method == 'getSensorData':
            pass
        else:
            ws.send(json.dumps({ 'error' : True, 'message' : 'Message without method'}))

#     previous_data = {}
#     for new_data in status.get_notifications(reservation_id):
#         ws.send(new_data)
# 
    ws.close()

@app.route('/')
def index():
    return render_template_string('''<html><body>Try the <a href="{{ url_for('static', filename='testing.html') }}">testing tool</a></body></html>''')
