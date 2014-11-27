#!/bin/bash
nohup python loop.py --fake > nohup_loop.out &
nohup ./run.sh > nohup_gunicorn.out &
