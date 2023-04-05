import time
import board
import busio
import adafruit_gps

from adafruit_extended_bus import ExtendedI2C as I2C


try:  
# Detecting if the GPS is Connected
    i2c = I2C(4)
    gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False) # Use I2C interface
    print("GPS found")
except Exception as e:
    time.sleep(.5)
    print("No GPS found")
    print ("Error and type: %s - %s." % (e,type(e)))
    quit()

# Turn on everything (not all of it is parsed!)
print("Sending GPS Command")
gps.send_command(b"PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0")

print("Changing Update Frequency")
gps.send_command(b"PMTK220,1000")


def format_dop(dop):
    # https://en.wikipedia.org/wiki/Dilution_of_precision_(navigation)
    if dop > 20:
        msg = "Poor"
    elif dop > 10:
        msg = "Fair"
    elif dop > 5:
        msg = "Moderate"
    elif dop > 2:
        msg = "Good"
    elif dop > 1:
        msg = "Excellent"
    else:
        msg = "Ideal"
    return f"{dop} - {msg}"


talkers = {
    "GA": "Galileo",
    "GB": "BeiDou",
    "GI": "NavIC",
    "GL": "GLONASS",
    "GP": "GPS",
    "GQ": "QZSS",
    "GN": "GNSS",
}

last_print = time.monotonic()

while True:

    if not gps.update() or not gps.has_fix:
       time.sleep(0.1)
       print("No Coordinates found")
       print(gps.nmea_sentence) 
       continue

       

