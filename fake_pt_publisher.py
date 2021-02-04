import cv2
import csv
import numpy as np
import visualization as vs
import math 
from scipy.signal import butter,filtfilt
import statistic as stat
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import mqttsetup
from datetime import datetime
import pandas as pd
import time
# 2:07pm

#Camera setting
camera_width,camera_height = 1200,980
#Log file path
log_file_path= "path_log.csv"
Plotting_enable = True # True/False
MQTT_Enable = True
#Location record
locations = []
#Total number of record
max_num_record = 0

#Plot the record
dist_patient = []
dist_wash = []
dist_rub = []
grad_patient = []
grad_wash = []
grad_rub = []
clean_hist = []

#MQTT Control
MQTT_Dashboard_Topic = "MDSSCC/POINTS"
MQTT_Server = "ia.ic.polyu.edu.hk"
packet_index = 0


#Visualization Control
def color_info(event,x,y,flag,param):
    #When Left is clicked in the mouse
    if event == cv2.EVENT_LBUTTONDOWN:  
        print("Chosen Pixel: X->{} Y->{}".format(x,y))


#1. Read log file (x,y)
with open(log_file_path) as log_file:
    log_analyzer = csv.reader(log_file)
    df_list=[]
    for row in log_analyzer:
        #Set visulization range for testing
        if(max_num_record <= 120):
            loc_x, loc_y, clean = row[1],row[2],row[6]
            df_list.append((int(row[0]),int(row[1]),int(row[2]),int(row[6])))
            #Store every (x,y,clean) for every ID
            locations.append((loc_x,loc_y,clean))
            max_num_record += 1
    print("All data are loaded...")
   
    
#2. Visualize on an image
image = vs.background_creation(camera_width,camera_height)
for counter in range(0,max_num_record):
    #Get data one by one
    location = locations[counter]
    loc_x,loc_y,clean = location
    loc_x,loc_y = int(loc_x),int(loc_y)
    clean = int(clean)

    #Indicating the starting point
    if(counter == 0):
        image[loc_y:(loc_y+vs.pixel_offset),loc_x:(loc_x+vs.start_pixel_offset)] = vs.start_pixel_color
    if ((counter %50) ==0) and (counter >0):
        cv2.putText(image,"{}".format(counter),(loc_x-vs.pixel_offset,loc_y-vs.pixel_offset),cv2.FONT_HERSHEY_SIMPLEX,0.5,vs.handwash_pixel_color,1)
        image[loc_y:(loc_y+vs.pixel_offset),loc_x:(loc_x+vs.pixel_offset)] = vs.handwash_pixel_color
        
    #Indicating the ending point
    if(counter == (max_num_record-1)):
        image[loc_y:(loc_y+vs.pixel_offset),loc_x:(loc_x+vs.end_pixel_offset)] = vs.end_pixel_color
    #Indicating the handwash point
    if(clean == 1):
        cv2.putText(image,"1",(loc_x-vs.pixel_offset,loc_y-vs.pixel_offset),cv2.FONT_HERSHEY_SIMPLEX,0.5,vs.handwash_pixel_color,1)
        image[loc_y:(loc_y+vs.pixel_offset),loc_x:(loc_x+vs.pixel_offset)] = vs.handwash_pixel_color
    #Indicating other points (Green)
    image[loc_y:(loc_y+vs.pixel_offset),loc_x:(loc_x+vs.pixel_offset)] = vs.label_pixel_color[0]

    if(MQTT_Enable == True):
        #Publish locations
        mqtt_node = mqttsetup.mqtt_client_setup(MQTT_Server)
        message = "{\"x\":\""+str(loc_x)+"\",\"y\":\""+str(loc_y)+"\"}"
        mqttsetup.mqtt_publish_record(mqtt_node,MQTT_Dashboard_Topic,message)
        print("MQTT Message Published [{}]".format(packet_index))
        packet_index+=1
        print(message)

    if(Plotting_enable):
        cv2.imshow('Path Tracking:',image)
        cv2.setMouseCallback('Path Tracking:',color_info)  
        time.sleep(1)
        cv2.waitKey(50)


cv2.waitKey(0)
cv2.destroyAllWindows

