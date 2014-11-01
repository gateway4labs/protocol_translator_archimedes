import urlparse

import redis
import time
from flask import Flask, request
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

redis_client = redis.Redis()

@sockets.route('/devices/sensors')
def echo_socket(ws):
    arguments = urlparse.parse_qs(ws.environ['QUERY_STRING'])
    # { 'reservation_id' : ['foo'] }
    reservation_ids = arguments.get('reservation_id', [])
    if reservation_ids:
        reservation_id = reservation_ids[0]
    else:
        ws.send("ERROR: Reservation missing identifier")
        ws.close()
        return
    
    # 
    # Now we should:
    # 1. Add this reservation_id to redis
    # 2. While the reservation_id is in Redis (otherwise other process has removed it), take the results
    #    and convert them to the desired format (e.g., one for archimedes)
    # 
    
    while True:
        time.sleep(1)
        ws.send("Sensor data for %s: %s" % (reservation_id, time.asctime()))

print "hola"

@app.route('/')
def hello():
    return 'Hello World!'
