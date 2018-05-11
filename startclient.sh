#!/bin/sh

# add additional arguments or place them directly in the python script
nohup /home/pi/temperature-provider.py "My Measurement Name" > temperature-provider.log 2>&1 &
