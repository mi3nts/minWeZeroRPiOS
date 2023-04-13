# Battery reader written for Pi Sugar 3 module
# https://github.com/PiSugar/PiSugar/wiki/PiSugar-Power-Manager-(Software)

import datetime
from subprocess import run
import time
from collections import OrderedDict
from mintsXU4 import mintsSensorReader as mSR
import os

debug  = False 

def getPiSugarOutput(command,ignoreStr):
    data = run("echo " +command + " | nc -q 1 127.0.0.1 8423",capture_output=True,shell=True)
    outValue = data.stdout.decode().replace("\n","").replace(ignoreStr,"")
    errCode  = data.stderr
    return outValue, errCode;

def main():
    

    while True:
        try:
            
            dateTime          = datetime.datetime.now()

            rtcTime,rtcErr =\
                             getPiSugarOutput("get rtc_time","battery: ")
            batteryPercentage,batteryPercentageErr =\
                             getPiSugarOutput("get battery","battery: ")
            batteryVoltage,batteryVoltageErr =\
                             getPiSugarOutput("get battery_v","battery: ")            
            batteryCurrent,batteryCurrentErr =\
                             getPiSugarOutput("get battery_i","battery: ")               
            batteryChargingState,batteryChargingErr =\
                             getPiSugarOutput("get battery_charging","battery: ")               
            batteryLedAmount,batteryChargingErr =\
                             getPiSugarOutput("get battery_led_amount","battery: ")                         
            batteryPowerPlugged,batteryChargingErr =\
                             getPiSugarOutput("get battery_power_plugged","battery: ")      



            sensorDictionary =  OrderedDict([
                    ("dateTime"               ,str(dateTime)), # always the same
                    ("batteryPercentage"      ,str(batteryPercentage)), # check with arduino code
                    ("batteryVoltage"         ,str(batteryVoltage)), # check with arduino code
                    ("batteryCurrent"         ,str(batteryCurrent)), # check with arduino code
                    ("batteryChargingState"   ,str(batteryChargingState)), # check with arduino code
                    ("batteryLedAmount"       ,str(batteryLedAmount)), # check with arduino code
                    ("batteryPowerPlugged"    ,str(batteryPowerPlugged)), # check with arduino code
                    ("rtcTime"                ,str(rtcTime)), # check with arduino code
                    ])
            print(sensorDictionary)        

            # mSR.sensorFinisher(dateTime,"MWBL002",sensorDictionary)
            # time.sleep(30)

            time.sleep(10)

        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring Battery level for Mints Wearable Node")
    main()
