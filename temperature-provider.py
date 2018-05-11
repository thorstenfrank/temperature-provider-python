#!/usr/bin/python3

# #############################################################################
# This script is meant to be run on a raspberry pi, reading values from a
# DS18B20 temperature sensor and posting them to a temperature server.
# #############################################################################

import argparse
import datetime
import glob
import os
import requests
import sys
import time

# Base settings
measurement_name = None
measurement_interval = 60

# Sensor (device) settings
device_base_folder = '/sys/bus/w1/devices'
device_folder_name = '28*'
device_base_filename = '/w1_slave'
device_fullpath = None

# Server Settings
post_to_server = True
server_base_url = 'http://localhost:8080'
post_path = '/temperature/'
post_request_param= '?value='
complete_url = None
force_post = False

# Debug output settings
verbose = False

# Dummy value used when no vale could be read from the Sensor
no_value = 999999999

# Debug output
def print_verbose(message):
    if verbose:
        print(message)

# Parse script arguments and set properties
def parse_args():
    parser = argparse.ArgumentParser(description='Read temperature measurements and publish them')
    parser.add_argument('name', help='Measurement name')
    parser.add_argument('-i', '--interval', type=int, help='Seconds between measurement readings (default: 60)')
    parser.add_argument('-d', '--dry-run', action="store_true", help="Read the measurement but don't actually contact the server")
    parser.add_argument('-v', '--verbose', action="store_true", help="Write debug output")
    parser.add_argument('-u', '--url', help='Base server URL (default: localhost:8080)')
    parser.add_argument('-n', '--devicename', help='Sensor devide name, e.g. 28-123456. If not specified, automatically detected if possible')
    parser.add_argument('-f', '--forcepost', action='store_true', help='Post reading to server even if there was no change (default: false)')

    args = parser.parse_args()

    global measurement_name
    measurement_name = args.name

    if args.dry_run:
        global post_to_server
        post_to_server = False

    if args.interval:
        global measurement_interval
        measurement_interval = args.interval

    if args.verbose:
        global verbose
        verbose = args.verbose

    if args.url:
        global server_base_url
        server_base_url = args.url

    if args.devicename:
        global device_fullpath
        device_fullpath = device_base_folder + '/' + args.devicename + device_base_filename

    if args.forcepost:
        global force_post
        force_post = args.forcepost

# Debug output of all properties
def print_properties():
    print("--- PROPERTIES ---")
    print("Name: {}".format(measurement_name))
    print("Device File: {}".format(device_fullpath))
    print("Post to Server? {}".format(post_to_server))
    print("Interval: {} seconds".format(measurement_interval))
    print("Server URL: {}".format(complete_url))
    print("Force posting to server? {}".format(force_post))

# If the device name wasn't specified, attempt to automatically determine it
def determine_devide_folder():
    global device_fullpath
    if device_fullpath is None:
        print_verbose("Auto-determining path")
        base_pattern = device_base_folder + device_folder_name
        for path in glob.glob(base_pattern):
            if os.path.isdir(path):
                device_fullpath = path + device_base_filename
                break

    if not os.path.exists(device_fullpath):
        print("Device file does not exist! Check your 1-wire setup")
        print("Missing device file: {}".format(device_fullpath))
        sys.exit(1)

# create the complete URL pattern
def build_complete_server_url():
    global complete_url
    complete_url = server_base_url + post_path + measurement_name + post_request_param

# open file and get temperature reading
def read_temperature():
    return_value = no_value
    with open(device_fullpath, 'r') as file:
        for line in file:
            index = line.find('t=')
            if index >= 0:
                return_value = float(line[index+2:])
                break

    return return_value

# Take the value and post it to the server, or just print if we're doing a dry-run
def post_reading(value):
    post_url = complete_url + str(value)
    if post_to_server:
        try:
            requests.post(complete_url)
        except OSError as err:
            print(datetime.datetime.now())
            print("Error ocurred while posting to server: {0}".format(err))
    else:
        print_verbose("DRY-RUN: would POST to: " + post_url)

# Read the temperature from the sensor, post it to the server, sleep some and do it all over again
def loop_read_and_post():
    temp_last = 0.0
    while True:
        temp_now = read_temperature()
        if temp_now != no_value and (force_post or temp_now != temp_last):
            post_reading(temp_now)
            temp_last = temp_now
        time.sleep(measurement_interval)

# MAIN script control
parse_args()
determine_devide_folder()
build_complete_server_url()

# debug output
if verbose:
    print_properties()
    print("--- STARTING LOOP ---")

# and run the loop
loop_read_and_post()
