#!/bin/bash
gunicorn -k flask_sockets.worker archimedes_devices:app
