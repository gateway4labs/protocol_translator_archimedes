import redis

from archimedes_devices import app


# TODO: take app.config to know the database or so
redis_client = redis.Redis()


RESERVATION_PREFIX = 'lab_reservations_'
COMMAND = 'command'
BASE_URL = 'url'

def new_reservation(reservation_id, command):
    redis_client.hset(''.join((RESERVATION_PREFIX, reservation_id)), COMMAND, command)
    redis_client.hset(''.join((RESERVATION_PREFIX, reservation_id)), BASE_URL, 'http://www.weblab.deusto.es/weblab/')

def get_reservations():
    reservation_ids = redis_client.keys('%s*' % RESERVATION_PREFIX)
    print reservation_ids
    commands = {}
    for long_reservation_id in reservation_ids:
        reservation_id = long_reservation_id.split('lab_reservations_')[1]
        command = redis_client.hget(long_reservation_id, COMMAND)
        url = redis_client.hget(long_reservation_id, BASE_URL)
        if command:
            commands[reservation_id] = {
                'command' : command,
                'url' : url,
            }
    return commands

def remove_reservation(reservation_id):
    redis_client.hdel(''.join((RESERVATION_PREFIX, reservation_id)), COMMAND)
    redis_client.hdel(''.join((RESERVATION_PREFIX, reservation_id)), BASE_URL)


