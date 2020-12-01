import cv2
import numpy as np
import matplotlib.pyplot as plt
#pip install mplcursors
import mplcursors

#Visualized pixel size
pixel_offset = 5
start_pixel_offset = 20
end_pixel_offset = 20

#Multiple color pixels for label
label_pixel_color = [(0,255,0),(255,0,0),(0,0,255),(204,255,204),(255,102,102)]
#White pixel for label (starting)
start_pixel_color = (255,255,255)
#Red pixel for label (ending)
end_pixel_color = (0,0,255)
#Purple pixel for label (hand wash)
handwash_pixel_color = (255,153,153)

#Boundary boxes definition
zone_x_min_patient,zone_y_min_patient,zone_x_max_patient,zone_y_max_patient = 366,369,521,667
zone_x_min_clean,zone_y_min_clean,zone_x_max_clean,zone_y_max_clean = 194,300,330,420
zone_x_min_door,zone_y_min_door,zone_x_max_door,zone_y_max_door = 631,308,674,414
zone_x_min_alchol,zone_y_min_alchol,zone_x_max_alchol,zone_y_max_alchol = 430,329,470,356
zone_x_min_roi,zone_y_min_roi,zone_x_max_roi,zone_y_max_roi = 160,130,697,721

#Mid points of different zones
mid_x_patient = int((zone_x_min_patient+zone_x_max_patient)/2.0)
mid_y_patient = int((zone_y_min_patient+zone_y_max_patient)/2.0)

mid_x_clean = int((zone_x_min_clean+zone_x_max_clean)/2.0)
mid_y_clean = int((zone_y_min_clean+zone_y_max_clean)/2.0)

mid_x_door = int((zone_x_min_door+zone_x_max_door)/2.0)
mid_y_door = int((zone_y_min_door+zone_y_max_door)/2.0)

mid_x_alchol = int((zone_x_min_alchol+zone_x_max_alchol)/2.0)
mid_y_alchol = int((zone_y_min_alchol+zone_y_max_alchol)/2.0)

def background_creation(image_width,image_height):
    #Create black background
    background = np.zeros((image_height,image_width,3), np.uint8)

    #Draw Paitent Zone
    color_patient = (255,102,255)
    cv2.rectangle(background,(zone_x_min_patient,zone_y_min_patient),(zone_x_max_patient,zone_y_max_patient),color_patient,2)
    cv2.circle(background,(mid_x_patient,mid_y_patient),4,color_patient,-1)
    cv2.putText(background,"Patient",(mid_x_patient-40,mid_y_patient-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,color_patient,1)

    #Draw Cleaning Zone
    color_clean = (255,255,51)
    cv2.rectangle(background,(zone_x_min_clean,zone_y_min_clean),(zone_x_max_clean,zone_y_max_clean),color_clean,2)
    cv2.circle(background,(mid_x_clean,mid_y_clean),4,color_clean,-1)
    cv2.putText(background,"Cleaning Zone",(mid_x_clean-50,mid_y_clean-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,color_clean,1)

    #Drawing Entrence 
    color_door = (127,0,255)
    cv2.rectangle(background,(zone_x_min_door,zone_y_min_door),(zone_x_max_door,zone_y_max_door),color_door,2)
    cv2.circle(background,(mid_x_door,mid_y_door),4,color_door,-1)
    cv2.putText(background,"Entrance",(mid_x_door-30,mid_y_door-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,color_door,2) 

    #Drawing Alchohol
    cv2.rectangle(background, (zone_x_min_alchol,zone_y_min_alchol),(zone_x_max_alchol,zone_y_max_alchol),(255,255,51),2)            
    cv2.circle(background, (mid_x_alchol, mid_y_alchol), 4, (255,255,51), -1)
    cv2.putText(background, "CLEANING ZONE", (mid_x_alchol-30, mid_y_alchol-20),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,51), 1)

    #Drawing ROI
    cv2.rectangle(background, (zone_x_min_roi,zone_y_min_roi),(zone_x_max_roi,zone_y_max_roi),(0,255,255),2)               

    return background

def plot_all_distance(dist_patient,dist_rub,dist_wash):
    #It only plot distance

    plt.subplots_adjust(wspace=0.4,hspace=0.4)

    plt.subplot(2,2,1)
    line1 = plt.plot(dist_patient)
    plt.title("Self_2_Patient")
    plt.xlabel("Data sequence")
    plt.ylabel("Distance")
    plt.grid()

    plt.subplot(2,2,2)
    line2 = plt.plot(dist_rub)
    plt.title("Self_2_Hand Rub")
    plt.xlabel("Data sequence")
    plt.ylabel("Distance")
    plt.grid()

    plt.subplot(2,2,3)
    line3 = plt.plot(dist_wash)
    plt.title("Self_2_Wash Bin")
    plt.xlabel("Data sequence")
    plt.ylabel("Distance")
    plt.grid()

    #Interative marker on graph
    mplcursors.cursor(line1)
    mplcursors.cursor(line2)
    mplcursors.cursor(line3)

    plt.show()

def plot_all_distance_gradient(dist_patient,dist_rub,dist_wash,\
                                grad_patient,grad_rub,grad_wash,\
                                LPF_patient,LPF_rub,LPF_wash):

    #It plot distances and gradients (including LPF)                      
    plt.subplots_adjust(wspace=0.4,hspace=0.4)

    plt.figure(1)
    plt.subplot(2,2,1)
    line1 = plt.plot(dist_patient)
    line4 = plt.plot(grad_patient)
    line7 = plt.plot(LPF_patient)
    plt.title("Self_2_Patient")
    plt.xlabel("Data sequence")
    plt.legend(['distance','gradient','LPF'])
    plt.grid()

    plt.subplot(2,2,2)
    line2 = plt.plot(dist_rub)
    line5 = plt.plot(grad_rub)
    line8 = plt.plot(LPF_rub)
    plt.title("Self_2_Hand Rub")
    plt.xlabel("Data sequence")
    plt.legend(['distance','gradient','LPF'])
    plt.grid()

    plt.subplot(2,2,3)
    line3 = plt.plot(dist_wash)
    line6 = plt.plot(grad_wash)
    line9 = plt.plot(LPF_wash)
    plt.title("Self_2_Wash Bin")
    plt.xlabel("Data sequence")
    plt.legend(['distance','gradient','LPF'])
    plt.grid()

    #Interative marker on graph
    mplcursors.cursor(line1)
    mplcursors.cursor(line2)
    mplcursors.cursor(line3)
    mplcursors.cursor(line4)
    mplcursors.cursor(line5)
    mplcursors.cursor(line6)
    mplcursors.cursor(line7)
    mplcursors.cursor(line8)
    mplcursors.cursor(line9)

    plt.show()