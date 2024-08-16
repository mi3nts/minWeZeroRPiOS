# Import tkinter and webview libraries
# from fileinput import filename
# # from tkinter import *
# from traceback import print_stack
# import webview
import glob
import serial
import datetime
# from mintsXU4 import mintsSensorReader as mSR
# from mintsXU4 import mintsDefinitions as mD
import time
# import serial
# import pynmea2
from collections import OrderedDict
from os import listdir
from os.path import isfile, join
# import mintsLatest as mL
import csv
import os 
# import nmap, socket
import yaml
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS 

import sys
import yaml
import os
import time
import glob
from collections import defaultdict
import pandas as pd
import re
import socket

from datetime import date, timedelta, datetime
from mintsXU4 import mintsDefinitions as mD


# This will run continously - 
# Steps 
#   1) Collects all csvs it can find 
#   2) For each csv it checks if it has already synced - 
#          Do this using a nested yaml file with sensor ID @ mintsData/ID/id_influxUpdated.yaml

#   It checks if the sensor has internet 

#  With on board sensors:
    # Node ID should be updated 
    # Some means to check if connectivity is there 
    # How long should I go back to 
    # How often to send 
    # Check if already synced 



# nodeInfo           = mD.nodeInfo
# sensorInfo         = mD.sensorInfo

# nodeInfo             = pd.read_csv('https://raw.githubusercontent.com/mi3nts/AirQualityAnalysisWorkflows/main/influxdb/nodered-docker/id_lookup.csv')
# sensorInfo                = pd.read_csv('https://raw.githubusercontent.com/mi3nts/mqttSubscribersV2/main/lists/sensorIDs.csv')


dataFolder         = mD.dataFolder
nodeID             = mD.nodeID

# sensorIDs          = sensorInfo['sensorID']
credentials        = mD.credentials

influxToken        = credentials['influx']['token']  
influxOrg          = credentials['influx']['org'] 
influxBucket       = credentials['influx']['bucket'] 
influxURL          = credentials['influx']['url']

print()
print("MINTS")
print()

delta      = timedelta(days=1)

def directoryCheckV2(outputPath):
    isFile = os.path.isfile(outputPath)
    if isFile:
        return True
    if outputPath.find(".") > 0:
        directoryIn = os.path.dirname(outputPath)
    else:
        directoryIn = os.path.dirname(outputPath+"/")

    if not os.path.exists(directoryIn):
        print("Creating Folder @:" + directoryIn)
        os.makedirs(directoryIn)
        return False
    return True;


def isFloat(value):
    try:
        output = float(value)

        return output
    except ValueError:
        return value

def parse_csv_filename(filename):
    # Define a regex pattern to extract parameters
    pattern = re.compile(r'^(\w+)_(\w+)_(\w+)_(\d{4})_(\d{2})_(\d{2})\.csv$')
    # filename = os.path.basename(path)
    # Match the pattern against the filename
    match = pattern.match(os.path.basename(filename))
    if match:
        # Extract matched groups
        device_type = match.group(1)
        mac_address = match.group(2)
        sensorID  = match.group(3)
        year = match.group(4)
        month = match.group(5)
        day = match.group(6)
        fileDate = datetime(year=int(year), month=int(month), day=int(day)).date()
        return sensorID, fileDate
    else:
        raise ValueError(f"Filename {filename} does not match the expected pattern.")


def syncData2Influx(nodeID,nodeName):

    today = datetime.now().date()
    print(today)
    # print(dataFolder  + "/" + nodeID + "/" + "/*/*/*/*"+sensorID+"*.csv")
    csvDataFiles = glob.glob(\
                    dataFolder  + "/" +  nodeID + "/*/*/*/*"+nodeID+"*.csv")
    csvDataFiles.sort()

    # At this point this should check if the data is from today or not 
    # If its not today you sync it and record it 
    # If its today you record the last point - Every time the code starts 
    # again witin a while loop you check for a new time  

    for csvFile in csvDataFiles:
        print(csvFile)
        sensorID, fileDate = parse_csv_filename(csvFile)      
        if sensorID is not None:
            if fileDate != today: 
                print(fileDate)

                # print("================================================")
                # print("Syncing "+ csvFile)
                sendCSV2Influx(csvFile,nodeID,sensorID,nodeName,fileDate)
            else:
                sendCSV2InfluxToday(csvFile,nodeID,sensorID,nodeName,fileDate)

def sendCSV2InfluxToday(csvFile,nodeID,sensorID,nodeName,fileDate):
    print("Its todays data")
   

def sendCSV2Influx(csvFile,nodeID,sensorID,nodeName,fileDate):
    # try:
    while True:

        # print(csvFile)
        if not is_connected():
            print("No Connectivity")
            return 
        
        sequence = []
        tag_columns = ["device_id", "device_name"]
        time_column = "dateTime"

        with open(csvFile, "r") as f:
            reader            = csv.DictReader((line.replace('\0','') for line in f) )
            rowList           = list(reader)
            for rowData in rowList:
                try:
                    dateTimeRow = datetime.strptime(rowData['dateTime'],'%Y-%m-%d %H:%M:%S.%f')
                    point = Point(sensorID)  # Replace with your measurement name
                    point.tag("device_id", nodeID)
                    point.tag("device_name", nodeName)
                    point.time(dateTimeRow, WritePrecision.NS) 
                    # print(point)
                    # Dynamically add fields based on the headers
                    for header in reader.fieldnames:
                        if header not in tag_columns and header != time_column:
                            point.field(header, isFloat(rowData[header]))
                    # print(point)
                    # sequence.append(point)
                except ValueError as e:
                    print(f"-- An error occurred --: {e}")


        # with InfluxDBClient(url=influxURL, token=influxToken, org=influxOrg) as client:
        #     write_api = client.write_api(write_options=SYNCHRONOUS)
        #     write_api.write(influxBucket, influxOrg, sequence)
        if not is_connected():
            print("No Connectivity")
            return
        record_id_date(sensorID, date=str(fileDate), \
                        filename='id_date_records.yaml') # Name should be updated 


    # except Exception as e:
    #     print(rowData)
    #     print(f"An error occurred: {e}")


# Load existing records or create a new structure
def load_records(filename='id_date_records.yaml'):
    try:
        with open(filename, 'r') as file:
            records = yaml.safe_load(file) or {}
    except FileNotFoundError:
        records = {}
    return records

# Save records to the YAML file
def save_records(records, filename='id_date_records.yaml'):
    with open(filename, 'w') as file:
        yaml.safe_dump(records, file)

# Add a new date to an ID record, with an optional custom date
def record_id_date(id_value, date=None, filename='id_date_records.yaml'):
    records = load_records(filename)
    print(records)

    # Ensure the structure is a defaultdict of lists for easier management
    records = defaultdict(list, records)
    print(records)
    
    # Use the provided date or the current date (without time) if not provided
    if date is None:
        date = str(datetime.now().strftime('%Y-%m-%d'))
    
    # Check if the ID and date combination already exists
    if check_id_date_exists(id_value, date, records):
        print(f"ID={id_value} with Date={date} already exists.")
        return
    
    # Add the date to the list of dates for this ID
    records[id_value].append(date)
    
    save_records(records, filename)
    print(f"Recorded: ID={id_value}, Date={date}")


# Check if a specific ID and date combination exists
def check_id_date_exists(id_value, date, records=None, filename='id_date_records.yaml'):
    if records is None:
        records = load_records(filename)
    
    # Check if the ID exists and the date is in the list for that ID
    if id_value in records and date in records[id_value]:
        return True
    return False

# Read and print all records
def read_records(filename='id_date_records.yaml'):
    records = load_records(filename)
    for id_value, dates in records.items():
        print(f"ID: {id_value}")
        for date in dates:
            print(f"  Date: {date}")

def getNodeName(nodeID):
    try:
        nodeInfo           = pd.read_csv('https://raw.githubusercontent.com/mi3nts/AirQualityAnalysisWorkflows/main/influxdb/nodered-docker/id_lookup.csv')
        nodeIDs            = nodeInfo['mac_address']
        nodeNames          = nodeInfo['name']
        matchingIndex = list(nodeIDs).index(nodeID)
        nodeName= nodeNames[matchingIndex]
        return nodeName
    except ValueError:
        return None
    
    
def is_connected(hostname="www.google.com"):
    try:
        # Connect to the host -- tells us if the host is actually reachable
        socket.create_connection((hostname, 80), 2)
        return True
    except OSError:
        return False

if is_connected():
    print("Connected to the internet")
else:
    print("Not connected to the internet")

def main():    
    # At this point just check for the node name via internet 
    if is_connected():
        nodeName = getNodeName(nodeID)
        if nodeName is not None:
            syncData2Influx(nodeID,nodeName)
            # print(f"Index: {index}, Node ID: {nodeID}, Node Name: {nodeName}")
            # for sensorID in sensorIDs:
            #     # print("Sending data to Influx for Node ID: " + nodeID + ", Node Name: " + nodeName + ", Sensor ID: " +sensorID) 
            #     syncData2Influx(nodeID,nodeName,sensorID)
    time.sleep(5) # This should be a smarter function

if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    main()