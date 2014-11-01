Protocol translator
-------------------

Introduction
------------


Requirements
------------

* Redis
* RabbitMQ


How it works
------------

There are different services:

* A background service which periodically checks the status and stores them in Redis, using pubsub.
* A Flask app which receives sockets, obtains a reservation_id, adds it to redis, and starts listening through Redis pubsub to see when to notify the server.


