# Python Temperature Sensor Client

A python script that is meant to run on a Raspberry Pi, reading values from a
DS18B20 temperature sensor and posting them to the [temperature-server](https://github.com/thorstenfrank/temperature-server).

# Prerequisites

This script assumes that the sensor is properly set up and values can be read from
`/sys/bus/w1/devices/<sensor-id>/w1_slave`.

There a numerous tutorials out there for setting up the hardware.

The script depends on the `requests` module, if you don't have that installed yet:

```
sudo apt-get install python3-pip
sudo pip3 install requests
```
This script is meant to continuously read temperature readings and upload them - so you will need to get the
[temperature-server](https://github.com/thorstenfrank/temperature-server) up and running as well.

# Running

Open the `temperature-provider.py` script and edit the properties as needed, namely

* `measurement_name`: the label you want to give to the reading - the name or location of the sensor, or whatever you want it to be
* `device_id`: the physical address of the sensor - check your Raspi's `/sys/bus/w1/devices/` directory, there will probably be a subdirectory starting with `28-` or similar there. If not, your sensor isn't set up properly
* `server_url`: base URL (hostname and port) of the temperature server
* `measurement_interval`: by default, the script checks for temperature changes every 60 seconds. Change this to your liking

Save the file and run it.

The shell script `startclient.sh` can be used to start the script in the background and keep it running.
