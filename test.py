import numpy as np
from scipy.signal import argrelextrema

def find_local_min(patient):
    #Neighbour elements for comparsion to find local extrema
    compare_neighbour = 2

    #Input of this function should be the result of LPF
    patient_index_list = argrelextrema(patient,np.less,order=compare_neighbour)
    return patient_index_list
    
    
a = np.array([10,10,10,2,10,10,10,10,10,2,10,10,10,2,10,10,10,10])
b = find_local_min(a)
c = b[0]
output = []
for counter in range(0,len(c)):
    index = c[counter]
    output.append(a[index])

output = np.array(output)

print(output[output==2])