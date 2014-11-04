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
            response = {'is_exception': False,
                         'result': {'commandstring': {'archimedes1': {'level': str(random.randint(0, 10000) / 100.0),
                                                                      'load' : str(random.randint(0, 10000) / 100.0)},
                                                      'archimedes2': {'level': str(random.randint(0, 10000) / 100.0),
                                                                      'load' : str(random.randint(0, 10000) / 100.0)},
                                                      'archimedes3': {'level': str(random.randint(0, 10000) / 100.0),
                                                                      'load' : str(random.randint(0, 10000) / 100.0)},
                                                      'archimedes4': {'level': str(random.randint(0, 10000) / 100.0),
                                                                      'load' : str(random.randint(0, 10000) / 100.0)},
                                                      'archimedes5': {'level': str(random.randint(0, 10000) / 100.0),
                                                                      'load' : str(random.randint(0, 10000) / 100.0)},
                                                      'archimedes6': {'level': str(random.randint(0, 10000) / 100.0),
                                                                      'load' : str(random.randint(0, 10000) / 100.0)},
                                                      'archimedes7': {'level': str(random.randint(0, 10000) / 100.0),
                                                                      'load' : str(random.randint(0, 10000) / 100.0)}}}}
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

