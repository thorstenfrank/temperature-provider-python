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

Although the script was written for (and runs on) Python3, it will run on Python2 as well. You will need to change the
shebang.

# Running

The `temperature-provider.py` script runs with a single argument - the name of the measurement.

By default, it will look for a device folder `/sys/bus/w1/devices/<sensor-id>/w1_slave` where the `<sensor-id>` starts
with `28*`. If you have multiple one-wire interfaces connected, you will need to supply the correct one as an argument
using the `-n` option.

The other defaults are

* `server url`: http://localhost:8080. Can be changed using the `-u` option
* `interval`: the interval between measurement readings, defaults to 60 seconds. Can be changed using the `-i` option.
* `force post`: the script will only post a measurement to the server if it is different than the previous one. Posting can
be enforced using the `-f` switch

See the script for more obscure options, such as doing a dry-run without posting to the server.
