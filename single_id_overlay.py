import cv2
import csv
import numpy as nps
import visualization as vs
import math 

#Camera setting
camera_width,camera_height = 800,800
#Log file path
log_file_path_1 = "./log_file_"
log_file_path_2 = "/path_log.csv"

#Number of csv file
num_csv = 2
i = 1

#Create image template
image = vs.background_creation(camera_width,camera_height)

while(i<=num_csv):
    #Location record
    locations = []
    #Total number of record
    max_num_record = 0

    #Change log file
    log_file_path = log_file_path_1 + str(i) + log_file_path_2

    #Read log file (x,y)
    with open(log_file_path) as log_file:
        log_analyzer = csv.reader(log_file)
        for row in log_analyzer:
            #Consider all IDs are mentioning one person
            loc_x, loc_y, clean = row[1],row[2],row[6]
            #Store every (x,y,clean) for every ID
            locations.append((loc_x,loc_y,clean))
            max_num_record += 1

    #Visualize on an image
    for counter in range(0,max_num_record):
        location = locations[counter]
        loc_x,loc_y,clean = location
        loc_x,loc_y = int(loc_x),int(loc_y)

        #Indicating the starting point
        if(counter == 0):
            image[loc_y:(loc_y+vs.pixel_offset),loc_x:(loc_x+vs.start_pixel_offset)] = vs.start_pixel_color
        #Indicating the ending point
        if(counter == (max_num_record-1)):
            image[loc_y:(loc_y+vs.pixel_offset),loc_x:(loc_x+vs.end_pixel_offset)] = vs.end_pixel_color

        #Indicating other points
        image[loc_y:(loc_y+vs.pixel_offset),loc_x:(loc_x+vs.pixel_offset)] = vs.label_pixel_color[i-1]


        window_title = 'Path Overlay Tracking [' + str(i) + ']'
        cv2.imshow(window_title,image)
        cv2.waitKey(50)
    
    i+=1

cv2.waitKey(0)
cv2.destroyAllWindows