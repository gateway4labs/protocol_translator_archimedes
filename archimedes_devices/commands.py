import json

import requests

from flask.ext.script import Manager
from archimedes_devices import app
import archimedes_devices.status as status


manager = Manager(app)

import redis

@manager.command
def update_status():
    reservations = status.get_reservations()
    print "Reservations: %s" % reservations
    for reservation_id in reservations:
        command = reservations[reservation_id]['command']
        base_url = reservations[reservation_id]['url']
        
        request = json.dumps({
            'method' : 'send_command', 
            'params' : {
                'reservation_id' : { 'id' : reservation_id },
                'command' : { 'commandstring' : command },
            }
        })
        cookies = {
            'weblabsessionid' : reservation_id.split('-')[-1]
        }
        response = requests.post('%sjson/' % base_url, data = request, cookies = cookies).json()
        if response.get('is_exception', True):
            print "Removing..."
            status.remove_reservation(reservation_id)
        print 
        print reservation_id
        print request
        print response
        # Obtain from redis the current reservations
        # one by one, do the following:
        # a) run the required command
        # b) get the results. If the reservation is wrong or whatever, simply remove it from the system
        # c) sleep for the next loop (which is sleeping X seconds - current, if > 0)
        

