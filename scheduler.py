#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import datetime
from datetime import timedelta

# 0 :IDLE
# 1 :START COUNTING
# 2 :START ANALYZE 
door_status = 0
in_time = 5
out_time = 2
start_time_in = 'x'
start_time_out = 'x'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("MDSSCC/STATUS")

def on_message(client, userdata, msg):
    global start_time_in,door_status,start_time_out
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    x = msg.payload.decode()
    message_dict = json.loads(x)
    now = datetime.datetime.now()

    if(message_dict["sys_status"]=="10"):
        if(door_status == 0):
            # START COUNTING
            door_status = 1
            start_time_in = now 
            print("[INFO] System start counting\r\n")

        elif(door_status == 1):
            diff = datetime.datetime.strptime(str(now), datetimeFormat)\
                - datetime.datetime.strptime(str(start_time_in), datetimeFormat)
            print("Diff Time [IN]in {}s".format(diff.seconds))
            if(int(diff.seconds)>=in_time):
                print("[INFO] System start analyzing\r\n")
                # START ANALYZE
                door_status = 2
                start_time_out = now
        
        else:
            diff = datetime.datetime.strptime(str(now), datetimeFormat)\
                - datetime.datetime.strptime(str(start_time_out), datetimeFormat)
            print("Diff Time [OUT]in {}s".format(diff.seconds))
            if(int(diff.seconds)>=out_time):
                # START ANALYZE
                door_status = 0

    elif(message_dict["sys_status"]=="30"):
        print("[INFO] IDLE\r\n")
    
    else:
        print("[INFO] Status Reset\r\n")
        door_status = 0
        start_time_out = 'x'
        start_time_in = 'x'


    
client = mqtt.Client()
client.connect("ia.ic.polyu.edu.hk",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
