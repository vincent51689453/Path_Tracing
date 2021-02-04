#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import datetime
from datetime import timedelta
import visualization as vs
import os
from shutil import copyfile
# 0 :IDLE
# 1 :START COUNTING
# 2 :START ANALYZE 
door_status = 0
in_time = 34
out_time = 2
start_time_in = 'x'
start_time_out = 'x'
inside = 0
data_index = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("MDSSCC/POINTS")

def on_message(client, userdata, msg):
    global start_time_in,door_status,start_time_out,inside
    global data_index
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    x = msg.payload.decode()
    message_dict = json.loads(x)
    now = datetime.datetime.now()
    loc_x = int(message_dict["x"])
    loc_y = int(message_dict["y"])
    print("[{}]x: {} y:{}".format(data_index,loc_x,loc_y))

    if(((loc_x>=vs.zone_x_min_door)and(loc_x<=vs.zone_x_max_door))\
        and ((loc_y>=vs.zone_y_min_door)and(loc_y<=vs.zone_y_max_door))):
        inside = 10
    else:
        inside = 30
    if((loc_x == 9999)and(loc_y == 9999)):
        #{"x":"9999","y":"9999"}
        inside = 99


    if(inside == 10):
        if(door_status == 0):
            # START COUNTING
            door_status = 1
            start_time_in = now 
            print("[INFO] System start counting at index {}\r\n".format(data_index))
            copyfile('path_emp.csv','path_log.csv')

        elif(door_status == 1):
            diff = datetime.datetime.strptime(str(now), datetimeFormat)\
                - datetime.datetime.strptime(str(start_time_in), datetimeFormat)
            total_diff = diff.seconds+(diff.microseconds/1000000)

            print("Diff Time [IN]in {}s\r\n".format(total_diff))
            if(total_diff>=in_time):
                print("[INFO] System start analyzing at index {}\r\n".format(data_index))
                os.system('python single_id_counter3.py')
                # START ANALYZE
                door_status = 2
                start_time_out = now
        
        else:
            diff = datetime.datetime.strptime(str(now), datetimeFormat)\
                - datetime.datetime.strptime(str(start_time_out), datetimeFormat)
            total_diff = diff.seconds+(diff.microseconds/1000000)
            print("Diff Time [OUT]in {}s\r\n".format(total_diff))
            if(total_diff>=out_time):
                # START ANALYZE
                door_status = 0

    elif(inside == 99):
        print("[INFO] Status Reset\r\n")
        door_status = 0
        start_time_out = 'x'
        start_time_in = 'x'
        data_index = 0
    else:
        z = 0
    
    data_index += 1

    
client = mqtt.Client()
client.connect("ia.ic.polyu.edu.hk",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
