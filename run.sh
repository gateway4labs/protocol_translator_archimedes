#!/bin/bash
gunicorn -k flask_sockets.worker weblabdeusto_devices:app
