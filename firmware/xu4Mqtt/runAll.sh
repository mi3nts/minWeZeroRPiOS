#!/bin/bash
#
sleep 60
kill $(pgrep -f 'ips7100ReaderV1.py')
sleep 5
python3 ips7100ReaderV1.py &
sleep 5

kill $(pgrep -f 'i2cReader.py')
sleep 5
python3 i2cReader.py &
sleep 5

kill $(pgrep -f 'gpsReader.py')
sleep 5
python3 gpsReader.py &
sleep 5

kill $(pgrep -f 'batteryReader.py')
sleep 5
python3 batteryReader.py &
sleep 5


python3 ipReader.py
sleep 5
