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
# 2:07pm

#Camera setting
camera_width,camera_height = 800,800
#Log file path
#log_file_path = "path_log.csv"
log_path = "log/"
log_file_path= log_path+"199.csv"
#log_path = "log/162.csv"
Plotting_enable = True # True/False
MQTT_Enable = False
#%%
#log_file_path = "./dataset/log_file_42/path_log.csv"
record_file_path = "result_buffer.csv"
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

MQTT_Dashboard_Topic = "MDSSCC/AIHH/gui_dashboard"
MQTT_Server = "ia.ic.polyu.edu.hk"

#low pass filter
T = 5.0       #Sample period
fs = 30.0     #Sample Rate (Hz)
cutoff = 2    #Cutoff frequency of the filter (Hz)
nyq = 0.5*fs  #Nyquist rate
order = 2     #order of LPF
n = int(T*fs) #Total number of samples

#Global thresholding
patient_thresh = 250

#Contact record merge
contact_diff = 40

#Visualization Control


def butter_lowpass_filter(data,cutoff,fs,order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data,axis=0)
    return y    

def distance_calculation(self_x,self_y):
    self_2_patient = math.sqrt((self_x-vs.mid_x_patient)**2+(self_y-vs.mid_y_patient)**2)
    self_2_wash = math.sqrt((self_x-vs.mid_x_clean)**2+(self_y-vs.mid_y_clean)**2)
    self_2_rub = math.sqrt((self_x-vs.mid_x_alchol)**2+(self_y-vs.mid_y_alchol)**2)
    return self_2_patient,self_2_rub,self_2_wash

def orientation(self_x,self_y,zone_x,zone_y):
    #Remember it is based on opencv image coordinates system
    theta = 0
    x = abs(self_x-zone_x)
    y = abs(self_y-zone_y)
    #Quadrant I (0-90)
    if((self_x<=zone_x)and(self_y>zone_y)):
        if(y!=0):
            theta = np.rad2deg(math.atan(x/y))
        else:
            theta = 0
    #Quadrant II (90-180)
    if((self_x<zone_x)and(self_y<=zone_y)):
        if(x!=0):
            theta = np.rad2deg(math.atan(y/x))+90
        else:
            theta = 0
    #Quadrant III (180-270)
    if((self_x>zone_x)and(self_y<=zone_y)):
        if(y!=0):
            theta = np.rad2deg(math.atan(x/y))+180
        else:
            theta = 0
    #Quadrant IV (270-360)
    if((self_x>zone_x)and(self_y>=zone_y)):
        if(x!=0):
            theta = np.rad2deg(math.atan(y/x))+270
        else:
            theta = 0

    return theta


def gradient_calculation(self_x,self_y):
    #Calculate orientations of each zone with respect to each point
    self_2_patient = orientation(self_x,self_y,vs.mid_x_patient,vs.mid_y_patient)
    self_2_rub = orientation(self_x,self_y,vs.mid_x_alchol,vs.mid_y_alchol)
    self_2_wash = orientation(self_x,self_y,vs.mid_x_clean,vs.mid_y_clean)

    return self_2_patient,self_2_rub,self_2_wash    

def color_info(event,x,y,flag,param):
    #When Left is clicked in the mouse
    if event == cv2.EVENT_LBUTTONDOWN:  
        a,b,c = gradient_calculation(x,y)
        d,e,f = distance_calculation(x,y)
        print("Chosen Pixel: X->{} Y->{}".format(x,y))
        print("Gradients -> Patient = {} | -> Wash Bin = {} | -> Hand Rub = {}".format(a,c,b))
        print("Distnaces -> Patient = {} | -> Wash Bin = {} | -> Hand Rub = {}\r\n".format(d,f,e))


def find_exit(data,num_of_data):
    last_index = False
    leave = 0
    i = 100
    while((not(last_index))and(i<num_of_data)):
        x = int(data[i][0])
        y = int(data[i][1])
        if((x >= 680)and(y <= 240)):
            print("Last point: X:{} Y:{} i:{}".format(x,y,i))
            leave = i
            last_index = True
        i += 1
    print("Last index:",leave)
    return leave

#1. Read log file (x,y)
with open(log_file_path) as log_file:
    log_analyzer = csv.reader(log_file)
    df_list=[]
    for row in log_analyzer:
        #Consider all IDs are mentioning one person
#        if ((row[0] == '322') or (row[0] == '323')): 
#        if (row[0] == '424'): 
        if True:
            loc_x, loc_y, clean = row[1],row[2],row[6]
            df_list.append((int(row[0]),int(row[1]),int(row[2]),int(row[6])))
        #Store every (x,y,clean) for every ID
            locations.append((loc_x,loc_y,clean))
            max_num_record += 1

    # find_exit by Vincent 8 Dec
    last = find_exit(locations,max_num_record)
    #Update max_num_record to last
    if(last > 0):
        max_num_record = last+1
    df=pd.DataFrame(df_list)
    
    
    
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

    #Distance analyze
    a,b,c = distance_calculation(loc_x,loc_y)
    d,e,f = gradient_calculation(loc_x,loc_y)

    dist_patient.append(a)
    dist_rub.append(b)
    dist_wash.append(c)

    grad_patient.append(d)
    grad_rub.append(e)
    grad_wash.append(f)

    clean_hist.append(clean)

    if(Plotting_enable):
        cv2.imshow('Path Tracking:',image)
        cv2.setMouseCallback('Path Tracking:',color_info)  
        cv2.waitKey(50)


#3. Low pass filter after go through all the data
dist_patient_np = np.array(dist_patient)
dist_rub_np = np.array(dist_rub)
dist_wash_np = np.array(dist_wash)
grad_patient_np = np.array(grad_patient)
grad_rub_np = np.array(grad_rub)
grad_wash_np = np.array(grad_wash)

#Distance after LPF
LPF_patient = butter_lowpass_filter(dist_patient_np,cutoff,fs,order)
LPF_rub = butter_lowpass_filter(dist_rub_np,cutoff,fs,order)
LPF_wash = butter_lowpass_filter(dist_wash_np,cutoff,fs,order)

#Gradients after LPF
LPF_G_patient = butter_lowpass_filter(grad_patient_np,cutoff,fs,order)
LPF_G_rub = butter_lowpass_filter(grad_rub_np,cutoff,fs,order)
LPF_G_wash = butter_lowpass_filter(grad_rub_np,cutoff,fs,order)


#Plot distances
#vs.plot_all_distance(dist_patient,dist_rub,dist_wash)

#4. Plot distances / gradients / LPF
if(Plotting_enable):
    vs.plot_all_distance_gradient(dist_patient,dist_rub,dist_wash,\
                                grad_patient,grad_rub,grad_wash,\
                                LPF_patient,LPF_rub,LPF_wash,\
                                LPF_G_patient,LPF_G_rub,LPF_G_wash)

#%%5. Start counting
#min_paient, rub_wash, min_wash = stat.find_local_min(LPF_patient,LPF_rub,LPF_wash)
#5A Find number of patient contacts
#patient_contact,patient_index = stat.global_thresholding(LPF_patient,patient_thresh,min_paient,LPF_G_patient)
#5A Determine compliance of patient contacts
ok_patient,fail_patient = 0,0
#ok_patient,fail_patient = stat.serach_wash_record(patient_index,clean_hist,contact_diff)

#5B Determine compliance of staff leaving
ok_leave,fail_leave = 0,0
#ok_leave,fail_leave = stat.search_leave_record(patient_index,clean_hist,max_num_record)

#6. Terminal Result display
status="X"
Touch = 0
P_Min =min(LPF_patient)*1.05
#P_Min =min(dist_patient_np)*1.05
#if (P_Min >240 ):
#    P_Min =240
if (P_Min*1.2 > 350):
    BR=P_Min*1.2
else:
    BR=350

for count in range(0,max_num_record):
    if (locations[count][2]=='1'):
        if (status != "G"):
            status="G"
            Touch=0

            print("WH:{}. {}-{}".format(count,LPF_patient[count],LPF_G_patient[count]))
    elif ((LPF_patient[count] < P_Min) and ((grad_patient_np[count]<160) or (grad_patient_np[count]>210))):
        if (Touch == 0):
            if (status=="G"):
                status ="Y"
                ok_patient = ok_patient +1
                print("C:{}. {}-{}".format(count,LPF_patient[count],LPF_G_patient[count]))
            else:
                fail_patient =fail_patient +1
                print("F:{}. {}-{}".format(count,LPF_patient[count],LPF_G_patient[count]))   
        Touch=1
    elif (LPF_patient[count] > BR):
        if (Touch == 1):
            print("T:{}. {}-{}".format(count,LPF_patient[count],LPF_G_patient[count]))
            Touch = 0
            status="R"

print("P_Min {} count{} Last:{}".format(P_Min,count,status))
if (status != "G"):
    fail_leave=1
else:            
    ok_leave=1            
    
print("Report of this iteration:")
print("Compliance [Patient]:{}   Incompliance [Patient]:{}".format(ok_patient,fail_patient))
print("Compliance [Leave]  :{}   Incompliance [Leave]  :{}".format(ok_leave,fail_leave))
print("\r\n")

#7. Read previous history
with open(record_file_path) as history_file:
    dummy = []
    old_ok_p = 0
    old_fail_p = 0
    old_ok_leave = 0
    old_fail_leave = 0
    log_history = csv.reader(history_file)
    for row_record in log_history:
        old_ok_p += int(row_record[0])
        old_fail_p +=  int(row_record[1])
        old_ok_leave +=  int(row_record[2])
        old_fail_leave +=  int(row_record[3])


#8. MQTT Publish to dashboard
if(MQTT_Enable == True):
    #Publish
    a = int(old_ok_p) + ok_patient
    b = int(old_fail_p) + fail_patient
    c = int(old_ok_leave) + ok_leave
    d = int(old_fail_leave) + fail_leave

    mqtt_node = mqttsetup.mqtt_client_setup(MQTT_Server)
    message = mqttsetup.mqtt_message_generator(a,b,c,d)
    mqttsetup.mqtt_publish_record(mqtt_node,MQTT_Dashboard_Topic,message)
    print("MQTT Message Published")
    print(message)

#9. Save to CSV
with open(record_file_path,'a',newline='') as log_result:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    log_writer = csv.writer(log_result)
    log_writer.writerow([ok_patient,fail_patient,ok_leave,fail_leave,current_time])

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows

plt.plot(LPF_patient,label="P")
plt.plot(LPF_rub,label="R")
plt.plot(grad_patient_np,label="G")
plt.legend(loc="upper left")
plt.show()
#plt.plot(LPF_rub)
#plt.plot(LPF_G_rub)
#plt.show()
