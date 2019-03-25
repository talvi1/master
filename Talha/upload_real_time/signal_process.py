import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from numpy import exp, pi, abs, angle, linspace
import scipy.fftpack
from scipy import signal
from multiprocessing import Process, Queue

"""
Function: dc_blocker()
Parameters: 
    list - 1-D list of arbitrary size containing floats
Return type: 1-D Numpy array, same size as input
Requirements:
Description: Implements a dc blocking filter using a first difference with an added
             recursive element. Results are stored in a numpy array initialized with zeros.
"""


def dc_blocker(list):
    out = np.zeros(len(list))
    for x in range(1, len(list)):
        out[x] = list[x] - list[x-1] + 0.9995*out[x-1]
    return out
"""
Function: moving_average()
Parameters: 
    list - 1-D list of arbitrary size containing floats
    N - An odd integer, representing size of moving average window
Return type: 1-D Numpy array, same size as input
Requirements: Requires input data to have been filtered by the dc_blocker() function
Description: Implements a symmetric general moving average algorithm for any window of size N, granted N is odd.
             Results are stored in a numpy array initialized with zeros.
"""
    
def moving_average(list, N):
    size = len(list)
    p = int((N-1)/2)
    q = int(p + 1)
    out = np.zeros(size)
    sum = 0
    for x in range(0, N-1):
        sum = sum + list[x]
    out[p] = sum/N #calculates average for initial values, size of N - 1 by summing them and dividing by N 
    for x in range(q , len(list)):
        out[x] = out[x-1] + (1/N)*(list[x] - list[x-N])
    return out
"""
Function: low_pass()
Parameters: 
    list - 1-D list of arbitrary size containing floats
Return type: 1-D Numpy array, same size as input
Requirements: Requires input data to have been filtered by the dc_blocker() function
Description: Implements a FIR low pass filter of order 10. Filter coefficients computed
             using Matlab filterdesigner tool. Filter output computed using scipy signal.lfilter function,
             which uses the filter coefficients to computer the output of the filter based on the input list.
"""
        
    
def low_pass(list):
    out = np.zeros(len(list))
    coeff = [0, -0.0044665638786995504, 0.011327879152762059, 0.099069904958781679,
    0.2329273163231553, 0.29999999999999999, 0.2329273163231553, 0.099069904958781679,
    0.011327879152762059, -0.0044665638786995504, 0]
    z = [1.0]
    out = signal.lfilter(coeff, z, list)
    return out
    
"""
Function: band_pass()
Parameters: 
    list - 1-D list of arbitrary size containing floats
Return type: 1-D Numpy array, same size as input
Requirements: Requires input data to have been filtered by the dc_blocker() function
Description: Implements an IIR band pass butterworth filter of order 10. Filter coefficients computed
             using Matlab filterdesigner tool. Filter output computed using scipy signal.lfilter function,
             which uses the filter coefficients to computer the output of the filter based on the input list.
"""
            
def band_pass(list):
    out = np.zeros(len(list))
    num = [0.0045068899518683932, 0, -0.022534449759341966, 0, 0.045068899518683932,
    0, -0.045068899518683932, 0, 0.022534449759341966, 0, -0.0045068899518683932]
    denom = [1, -6.9333187505764933, 21.865640509227923, -41.507632081885859, 52.72557966974199,
    -46.929213459865323, 29.653343115559892, -13.128105143013805, 3.8957144658539424,
    -0.69966421553011993, 0.057657639882063405]
    out = signal.lfilter(num, denom, list)
    return out
    
"""
Function: roughness()
Parameters: 
    list - 3-D list of floats, where each length of each list is the same so list[0] == list[1] == list[2] 
Return type: 1-D Numpy array of where length = size
Requirements: Requires input data to have been filtered by dc_blocker(), filtered by one of moving_average(), low_pass() or band_pass()
              and integrated using simpsons_method() or trapezoidal method
Description: Computes a roughness index by using a algorithm to sum the absolute of the difference between list[1]/list[2] and list[0] 
             for n values. The summation represents the roughness over some section of the road in meters for both left and right side 
             of the road. Both sides are averaged to give an overall roughness index for the road profile.  
"""    
    
def roughness(list):
    list_size = 500
    i = 0
    n = 10
    size = 50
    iri_right = np.zeros(size)
    iri_left = np.zeros(size)
    iri = np.zeros(size)
    if len(list[0]) == list_size:
        for x in range(size):
            for z in range(n):
                iri_left[x] += abs(list[2][z+i][0] - list[0][z+i][0])
                iri_right[x] += abs(list[1][z+i][0] - list[0][z+i][0])
            iri[x] = (iri_left[x] + iri_right[x])/2
            i += n
    return iri
"""
Function: simpsons_method()
Parameters: 
    list - 1-D list of arbitrary size containing floats
Return type: 1-D Numpy array same size as input
Requirements: Requires input data to have been filtered by dc_blocker(), filtered by one of moving_average(), low_pass() or band_pass()

Description: Performs numerical integration on data using simpsons weighted 1, 4, 1 to get velocity from acceleration.   
"""  
def simpsons_method(list):
    d_t = 0.005
    size = len(list)
    out = np.zeros(shape=(size,1))
    for x in range(2, size):
        out[x] = out[x-1] + ((list[x-2]+4*list[x-1]+list[x])*(d_t))/6
    return out
"""
Function: trapezoidal_method()
Parameters: 
    list - 1-D list of arbitrary size containing floats
Return type: 1-D Numpy array same size as input
Requirements: Requires input data to have been filtered by dc_blocker(), filtered by one of moving_average(), low_pass() or band_pass()

Description: Performs numerical integration using trapezoidal method on acceleration samples to get velocity
"""      
def trapezoidal_method(list):
    fs = 200
    size = len(list)
    out = np.zeros(size)
    for x in range(1, size):
        out[x] = out[x-1] + (list[x-1]+list[x])/(2*fs)
    return out
"""
Function: plot_fft()
Parameters: 
    data - 1-D list of arbitrary size containing floats
    fig - number of figure
Return type: None
Requirements: Requires data be of a length of power of 2

Description: Plots a one sided discrete fourier transform of the data using scipy library
"""     
def plot_fft(data, fig):
    N = len(data)
    T = 1.0/100.0 #1/sample rate of device
    x = linspace(0.0, N*T, N)
    yf = scipy.fftpack.fft(data)
    xf = linspace(0.0, 1.0/(2.0*T), N/2)
    plt.figure(fig)
    plt.plot(xf, 2.0/N*abs(yf[:N//2]))
"""
Function: plot_mag_response()
Parameters: 
    None
Return type: 
    None
Requirements:
    None 
Description: Plots the absolute magnitude and phase response of the function given in G from 0 to pi
""" 
def plot_mag_response():
    t = linspace(0, pi, 1000)
    G = (1-exp(-1*1j*t))/(1-0.99951171875*exp(-1*1j*t))
    plt.figure(5)
    plt.plot(t, abs(G))
    plt.xlabel('Frequency (w)')
    plt.ylabel('Magnitude')
    plt.title('Magnitude Response of DC Block Filter')
    plt.figure(6)
    plt.plot(t, angle(G))
    plt.xlabel('Frequency (w)')
    plt.ylabel('Phase (rad)')
    plt.title('Phase Response of DC Block Filter')
    #plt.xticks(np.arange(0, pi, step=0.0001))

"""
Function: process_signal()
Parameters: 
    list - 3D list containing raw accelerometer values from 3 difference accelerometers in float
    status - Queue containing the status of the program
    accel - Queue for putting in acceleration values to be plotted live
    speed - Queue containing the real time speed of the car
    iri - Queue for putting in roughness index to be plotted live
Return type: List containing roughness values
Requirements: Requires acceleration data to have been parsed and converted into raw acceleration values in m/s^2
Description: Uses dc blocker to remove 0 Hz components from the data. Uses band pass filter to filter the unwanted parts of the signal. Uses simpsons 
             integration method to get velocity from acceleration. Filtered acceleration data is put into a queue to be plotted in a separate process. 
             Roughness is computed using the integrated data. Roughness is put in iri queue to be plotted in a separate process. Roughness returned to caller  
""" 

def process_signal(list, status, accel, speed, iri):
    dc_block = [dc_blocker(list[x]) for x in range(len(list))]
    band_p = [band_pass(dc_block[x]) for x in range(len(dc_block))]
    integ = [simpsons_method(band_p[x]) for x in range(len(band_p))]
    for x in range(len(band_p[0])):
        accel.put([band_p[0][x], band_p[1][x], band_p[2][x]])
    r_index = roughness(integ)
    iri.put(r_index)
    return r_index
