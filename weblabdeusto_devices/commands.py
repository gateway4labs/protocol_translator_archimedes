import json

import requests

from flask.ext.script import Manager
from weblabdeusto_devices import app
import weblabdeusto_devices.status as status


manager = Manager(app)

@manager.command
def update_status(fake = False):
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
        if fake:
            import random
            response = { 'result' : { 'commandstring' : {"archimedes1": {"load": str(random.randint(0,100)), "level": "18.1"}, "archimedes2": {"load": "41.0", "level": "18.9"}, "archimedes3": {"load": "3.04", "level": "18.4"}, "archimedes4": {"load": "31.07", "level": "18.5"}, "archimedes5": {"load": "620.01", "level": "11.4"}, "archimedes6": {"load": "89.59", "level": "18.4"}, "archimedes7": {"load": "43.59", "level": "16.7"}} }, 'is_exception' : False }
            response = { 'result' : { 'commandstring' : {"archimedes1": {"load": "41.07", "level": "18.1"}, "archimedes2": {"load": "41.0", "level": "18.9"}, "archimedes3": {"load": "3.04", "level": "18.4"}, "archimedes4": {"load": "31.07", "level": "18.5"}, "archimedes5": {"load": "620.01", "level": "11.4"}, "archimedes6": {"load": "89.59", "level": "18.4"}, "archimedes7": {"load": "43.59", "level": "16.7"}} }, 'is_exception' : False }
        else:
            response = requests.post('%sjson/' % base_url, data = request, cookies = cookies).json()

        result = response.get('result', {}).get('commandstring')
        if response.get('is_exception', True):
            print "Removing..."
            status.remove_reservation(reservation_id)
        else:
            print reservation_id
            print result
            status.notify(result, reservation_id)
        # Obtain from redis the current reservations
        # one by one, do the following:
        # a) run the required command
        # b) get the results. If the reservation is wrong or whatever, simply remove it from the system
        # c) sleep for the next loop (which is sleeping X seconds - current, if > 0)
        

