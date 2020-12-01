import cv2
import csv
import numpy as np
import visualization as vs
import math 
from scipy.signal import butter,filtfilt

#Camera setting
camera_width,camera_height = 800,800
#Log file path
log_file_path = "./log_file_1/path_log.csv"
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

#Staff status
self_hygiene = False
contact_compliance = 0
contact_incompliance = 0
leave_compliance = 0
leave_incompliance = 0

#low pass filter
T = 5.0       #Sample period
fs = 30.0     #Sample Rate (Hz)
cutoff = 2    #Cutoff frequency of the filter (Hz)
nyq = 0.5*fs  #Nyquist rate
order = 2     #order of LPF
n = int(T*fs) #Total number of samples

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

def gradient_calculation(self_x,self_y):
    #factor is a scaling factor
    factor = 5
    if(self_x!=vs.mid_x_patient):
        self_2_patient = (self_y-vs.mid_y_patient)/(self_x-vs.mid_x_patient)*factor
    else:
        self_2_patient = 0

    if(self_x!=vs.mid_x_clean):
        self_2_wash = (self_y-vs.mid_y_clean)/(self_x-vs.mid_x_clean)*factor
    else:
        self_2_wash = 0

    if(self_x!=vs.mid_x_alchol):
        self_2_rub = (self_y-vs.mid_y_alchol)/(self_x-vs.mid_x_alchol)*factor
    else:
        self_2_rub = 0
    return self_2_patient,self_2_rub,self_2_wash    

def color_info(event,x,y,flag,param):
    #When Left is clicked in the mouse
    if event == cv2.EVENT_LBUTTONDOWN:  
        a,b,c = gradient_calculation(x,y)
        d,e,f = distance_calculation(x,y)
        print("Chosen Pixel: X->{} Y->{}".format(x,y))
        print("Gradients -> Patient = {} | -> Wash Bin = {} | -> Hand Rub = {}".format(a,c,b))
        print("Distnaces -> Patient = {} | -> Wash Bin = {} | -> Hand Rub = {}\r\n".format(d,f,e))

#1. Read log file (x,y)
with open(log_file_path) as log_file:
    log_analyzer = csv.reader(log_file)
    for row in log_analyzer:
        #Consider all IDs are mentioning one person
        loc_x, loc_y, clean = row[1],row[2],row[6]
        #Store every (x,y,clean) for every ID
        locations.append((loc_x,loc_y,clean))
        max_num_record += 1

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

LPF_patient = butter_lowpass_filter(dist_patient_np,cutoff,fs,order)
LPF_rub = butter_lowpass_filter(dist_rub_np,cutoff,fs,order)
LPF_wash = butter_lowpass_filter(dist_wash_np,cutoff,fs,order)

LPF_G_patient = butter_lowpass_filter(grad_patient_np,cutoff,fs,order)
LPF_G_rub = butter_lowpass_filter(grad_rub_np,cutoff,fs,order)
LPF_G_wash = butter_lowpass_filter(grad_rub_np,cutoff,fs,order)


#Plot distances
#vs.plot_all_distance(dist_patient,dist_rub,dist_wash)

#4. Plot distances / gradients / LPF
vs.plot_all_distance_gradient(dist_patient,dist_rub,dist_wash,\
                            grad_patient,grad_rub,grad_wash,\
                            LPF_patient,LPF_rub,LPF_wash,\
                            LPF_G_patient,LPF_G_rub,LPF_G_wash)


print("Done!")
cv2.waitKey(0)
cv2.destroyAllWindows

