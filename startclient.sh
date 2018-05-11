#!/bin/sh

nohup /home/pi/temperature-provider.py "$@" > temperature-provider.log 2>&1 &
