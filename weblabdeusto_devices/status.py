import redis

from weblabdeusto_devices import app


# TODO: take app.config to know the database or so
redis_client = redis.Redis()


RESERVATION_PREFIX = 'lab_reservations_'
CHANNEL_PREFIX = 'channel'
COMMAND = 'command'
BASE_URL = 'url'

def new_reservation(reservation_id, lab_module):
    command = lab_module.STATUS_COMMAND
    redis_client.hset(''.join((RESERVATION_PREFIX, reservation_id)), COMMAND, command)
    redis_client.hset(''.join((RESERVATION_PREFIX, reservation_id)), BASE_URL, 'http://www.weblab.deusto.es/weblab/')

def get_reservations():
    reservation_ids = redis_client.keys('%s*' % RESERVATION_PREFIX)
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

def notify(message, reservation_id):
    redis_client.publish('_'.join((CHANNEL_PREFIX, reservation_id)), message)

REMOVAL = 'REMOVAL'

class PubSubWrapper(object):
    def __init__(self, channels):
        self.pubsub = redis_client.pubsub()
        self.pubsub.subscribe(channels)

    def __iter__(self):
        for item in self.pubsub.listen():
            if item == REMOVAL:
                break
            yield item

        self.close()

    def close(self):
        self.pubsub.unsubscribe()

def get_notifications(reservation_id):
    channel = '_'.join((CHANNEL_PREFIX, reservation_id))
    return PubSubWrapper([channel])

def remove_reservation(reservation_id):
    redis_client.hdel(''.join((RESERVATION_PREFIX, reservation_id)), COMMAND)
    redis_client.hdel(''.join((RESERVATION_PREFIX, reservation_id)), BASE_URL)
    channel = '_'.join((CHANNEL_PREFIX, reservation_id))
    redis_client.publish(channel, REMOVAL)


