import urlparse
import threading
import time
import json

from flask import Flask, request, render_template_string
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

import weblabdeusto_devices.status as status
from weblabdeusto_devices.ext import LABS

class ControllerThread(threading.Thread):
    def __init__(self, ws, reservation_id, lab_controller, sensor_id):
        super(ControllerThread, self).__init__()
        self.ws = ws
        self.reservation_id = reservation_id
        self.lab_controller = lab_controller
        self.sensor_id = sensor_id
        self.notified = False

    def run(self):
        for new_data in status.get_notifications(self.reservation_id):
            response_data = self.lab_controller.extract_response_data(new_data, self.sensor_id)
            message = {
                    "method" : "getSensorData",
                    "sensorId" : self.sensor_id,
                    "accessRole" : "controller",
                    "responseData" : response_data
                }
            self.ws.send(json.dumps(message))
            if self.notified:
                break

    def notify(self):
        self.notified = True

class Controller(object):
    def __init__(self, *args):
        self.args = args
        self.thread = None

    def start(self):
        if self.thread is not None:
            self.thread.notify()

        self.thread = ControllerThread(*self.args)
        self.thread.start()

    def stop(self):
        self.thread.notify()
        self.thread = None

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
    controller = None

    while True:
        txtmsg = ws.receive()
        if txtmsg is None:
            break
        
        try:
            message = json.loads(txtmsg)
            method = message.get('method')
            if method == 'getSensorMetadata':
                metadata = current_lab.get_sensor_metadata(reservation_id, message)
                ws.send(json.dumps(metadata))
            elif method == 'getSensorData':
                if message.get('updateFrequency', -1) == 0:
                    if controller:
                        controller.stop()
                        controller = None
                else:
                    if controller:
                        controller.stop()
                    
                    sensor_id = message.get('sensorId')
                    controller = Controller(ws, reservation_id, current_lab, sensor_id)
                    controller.start()
            else:
                ws.send(json.dumps({ 'error' : True, 'message' : 'Message without method'}))
        except:
            traceback.print_exc()
            if controller:
                controller.stop()
                controller = None

            try:
                ws.send(json.dumps({ 'error' : True, 'message' : 'Unexpected server error'}))
            except:
                pass
            break
    
    if controller:
        controller.stop()
    
    status.remove_reservation(reservation_id)

    ws.close()

@app.route('/')
def index():
    return render_template_string('''<html><body>Try the <a href="{{ url_for('static', filename='testing.html') }}">testing tool</a></body></html>''')
