# from network import Bluetooth

# bluetooth = Bluetooth()
# bluetooth.start_scan(-1)    # start scanning with no timeout

# while True:
#     print(bluetooth.get_adv())
import struct

import time
from collections import OrderedDict
# Protocol defined here:
#     https://github.com/zh2x/BCI_Protocol
# Thanks as well to:
#     https://github.com/ehborisov/BerryMed-Pulse-Oximeter-tool
#     https://github.com/ScheindorfHyenetics/berrymedBluetoothOxymeter
#
# The sensor updates the readings at 100Hz.
import datetime
import _bleio
import adafruit_ble
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble.services.nordic import UARTService 
uart = UARTService()
uart_connection = None
from mintsXU4 import mintsSensorReader as mSR

# from adafruit_ble_berrymed_pulse_oximeter import BerryMedPulseOximeterService

# CircuitPython <6 uses its own ConnectionError type. So, is it if available. Otherwise,
# the built in ConnectionError is used.
connection_error = ConnectionError
if hasattr(_bleio, "ConnectionError"):
    connection_error = _bleio.ConnectionError

# PyLint can't find BLERadio for some reason so special case it here.
ble = adafruit_ble.BLERadio()  # pylint: disable=no-member

wrist_band_connection = None

while True:
    print("Scanning...")
    for adv in ble.start_scan(Advertisement, timeout=5):
        name = adv.complete_name
        print(adv)
        print(name)
        if not name:
            continue
        if name.strip("\x00") == "MINTSWearable001":
            wrist_band_connection = ble.connect(adv)
            print(wrist_band_connection)
            print("Connected")
            break
    # Stop scanning whether or not we are connected.
    ble.stop_scan()
    print("Stopped scan")
    # time.sleep(5)
    # print(wrist_band_connection)
    # print(wrist_band_connection.connected)
    # time.sleep(5)
    try:
        if wrist_band_connection and wrist_band_connection.connected:
            print("Fetch connection")
            print(wrist_band_connection)
            uart_service = wrist_band_connection[UARTService]
            while wrist_band_connection.connected:    
                #byteArrayReceived = uart_service.read(4)
                byteArrayReceived    = uart_service.read(24)
                byteArrayReceivedHex = byteArrayReceived.hex()
                    # print(len(byteArrayReceivedHex))
                if byteArrayReceived:
                    dateTime = datetime.datetime.now()
                    red         = struct.unpack('<L',bytes.fromhex(byteArrayReceivedHex[0:8]))[0]   
                    ir          = struct.unpack('<L',bytes.fromhex(byteArrayReceivedHex[8:16]))[0]   
                    green       = struct.unpack('<L',bytes.fromhex(byteArrayReceivedHex[16:24]))[0]   
                    hr          = struct.unpack('<i',bytes.fromhex(byteArrayReceivedHex[24:32]))[0]   
                    spo2        = struct.unpack('<i',bytes.fromhex(byteArrayReceivedHex[32:40]))[0]   
                    temperature = struct.unpack('<f',bytes.fromhex(byteArrayReceivedHex[40:48]))[0]                                                    
       
                    sensorDictionary =  OrderedDict([
                                                    ("dateTime"    ,str(dateTime)),
                                                    ("red"         ,str(red)),
                                                    ("ir"          ,str(ir)),
                                                    ("green"       ,str(green)),
                                                    ("hr"          ,str(hr)),
                                                    ("spo2"        ,str(spo2)),
                                                    ("temperature" ,str(temperature)),
                                                    # ("frequency"   ,str(frequency)),
                                            ])

                    print(sensorDictionary)                
                    mSR.sensorFinisher(dateTime,"MWB002",sensorDictionary)
                    time.sleep(1/30)
    except connection_error:
        try:
            pulse_ox_connection.disconnect()
        except connection_error:
            pass
        pulse_ox_connection = None