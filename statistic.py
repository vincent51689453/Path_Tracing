import numpy as np
from scipy.signal import argrelextrema

def find_local_min(patient,wash_bin,hand_rub):
    #Neighbour elements for comparsion to find local extrema
    compare_neighbour = 20

    #Input of this function should be the result of LPF
    patient_index_list = argrelextrema(patient,np.less,order=compare_neighbour)
    bin_index_list = argrelextrema(wash_bin,np.less,order=compare_neighbour)
    hand_index_list = argrelextrema(hand_rub,np.less,order=compare_neighbour)

    return patient_index_list,bin_index_list,hand_index_list

def global_thresholding(data_list,thresh,index_list,orientation_list):
    #Find out the True minima based on thresholding approach
    n = len(index_list[0])
    a = index_list[0]
    local_minima = []
    output_index = []
    #Measured theta limit
    theta_1, theta_2 = 160,200
    #Get all the minima based on the index list
    for counter in range(0,n):
        index = a[counter]
        #Thresholding
        if(data_list[index]<= thresh):
            #Orientation limit
            if((orientation_list[index]<=theta_1)or(orientation_list[index]>=theta_2)):
                local_minima.append(data_list[index])
                output_index.append(index)

    local_minima = np.array(local_minima)
    return local_minima,output_index

def serach_wash_record(contact_index,clean_record,merge):
    #Assume there will not be more than 3 contacts
    contact_index = np.array(contact_index)
    n = contact_index.shape[0]
    print("Contact Vector:",contact_index)

    contact_ok = 0
    contact_fail = 0

    buffer = []
    i = 0

    #One contact
    if(n == 1):
        while(i<contact_index[0]):
            buffer.append(clean_record[i])
            i+=1
        if(max(buffer)==1):
            contact_ok += 1
        else:
            contact_fail += 1
        buffer = []
    
    #Two contacts
    if(n == 2):
        #1
        while(i<contact_index[0]):
            buffer.append(clean_record[i])
            i+=1
        if(max(buffer)==1):
            contact_ok += 1
        else:
            contact_fail += 1

        #2
        i = contact_index[0]
        buffer = []
        while(i<contact_index[1]):
            buffer.append(clean_record[i])
            i+=1
        #Consider consecutive contacts
        diff = contact_index[1] - contact_index[0]
        if(diff >= merge):
            if(max(buffer)==1):
                contact_ok += 1
            else:
                contact_fail += 1
        i = 0
        buffer = []
    
    #Three contacts
    if(n == 3):
        #1
        while(i<contact_index[0]):
            buffer.append(clean_record[i])
            i+=1
        if(max(buffer)==1):
            contact_ok += 1
        else:
            contact_fail += 1

        #2
        i = contact_index[0]
        buffer = []
        while(i<contact_index[1]):
            buffer.append(clean_record[i])
            i+=1
        #Consider consecutive contacts
        diff = contact_index[1] - contact_index[0]
        if(diff >= merge):
            if(max(buffer)==1):
                contact_ok += 1
            else:
                contact_fail += 1

        #3
        i = contact_index[1]
        buffer = []
        while(i<contact_index[2]):
            buffer.append(clean_record[i])
            i+=1
        #Consider consecutive contacts
        diff = contact_index[2] - contact_index[1]
        if(diff >= merge):
            if(max(buffer)==1):
                contact_ok += 1
            else:
                contact_fail += 1
        i = 0
        buffer = []
    
    return contact_ok,contact_fail

def search_leave_record(contact_index,clean_record,total_sample):
    contact_index = np.array(contact_index)
    n = contact_index.shape[0]
    ok = 0
    fail = 0
    last_contact_index = 0
    buffer = []
    #If there is contact
    if(n > 0):
        last_contact_index = contact_index[-1]
        #Second wash record between last contact and last data
        for i in range(last_contact_index,total_sample):
            buffer.append(clean_record[i])
        #Check handwash record
        if(max(buffer)==1):
            ok += 1
        else:
            fail += 1

    return ok,fail
        

        
