import time
from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/sensors')
def echo_socket(ws):
    while True:
        time.sleep(1)
        ws.send("Sensor data: %s" % time.asctime())

@app.route('/')
def hello():
    return 'Hello World!'
