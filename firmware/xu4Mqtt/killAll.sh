#!/bin/bash
#
sleep 1
kill $(pgrep -f 'ips7100ReaderV1.py')
sleep 2

kill $(pgrep -f 'readI2c.py')
sleep 2

kill $(pgrep -f 'GPSReader.py')
sleep 2

kill $(pgrep -f 'batteryReader.py')
sleep 2
