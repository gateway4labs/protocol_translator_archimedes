Protocol translator
-------------------

This is a simple protocol translator for WebLab-Deusto (supporting existing services using the Go-Lab Smart Device specifications). It should be fine for most migrated labs.

How it works
------------

There are two services:

* A background service which periodically checks the status and stores them in Redis, using pubsub.
* A Flask app which receives sockets, obtains a reservation_id, adds it to redis, and starts listening through Redis pubsub to see when to notify the server.


