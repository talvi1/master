import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from numpy import exp, pi, abs, angle, linspace
import scipy.fftpack
from multiprocessing import Process, Queue

def dc_blocker(accel):
    out = np.zeros(len(accel))
    for x in range(1, len(accel)):
        out[x] = accel[x] - accel[x-1] + 0.9995*out[x-1]
    return out
def moving_average(accel, N):
    size = len(accel)
    p = int((N-1)/2)
    q = int(p + 1)
    out = np.zeros(size)
    sum = 0
    for x in range(0, N-1):
        sum = sum + accel[x]
    out[p] = sum/N
    for x in range(q , len(accel)):
        out[x] = out[x-1] + (1/N)*(accel[x] - accel[x-N])
    return out
def low_pass(list):
    out = np.zeros(len(list))
    coeff = [0, -0.0044665638786995504, 0.011327879152762059, 0.099069904958781679,
    0.2329273163231553, 0.29999999999999999, 0.2329273163231553, 0.099069904958781679,
    0.011327879152762059, -0.0044665638786995504, 0]
    z = [1.0]
    out = signal.lfilter(coeff, z, list)
    return out
def band_pass(list):
    out = np.zeros(len(list))
    num = [0.0045068899518683932, 0, -0.022534449759341966, 0, 0.045068899518683932,
    0, -0.045068899518683932, 0, 0.022534449759341966, 0, -0.0045068899518683932]
    denom = [1, -6.9333187505764933, 21.865640509227923, -41.507632081885859, 52.72557966974199,
    -46.929213459865323, 29.653343115559892, -13.128105143013805, 3.8957144658539424,
    -0.69966421553011993, 0.057657639882063405]
    out = signal.lfilter(num, denom, list)
    return out
def roughness(list):
    sample_speed = 200.0
    i = 0
    n = 10
    m = 40
    iri_right = np.zeros(m)
    iri_left = np.zeros(m)
    iri = np.zeros(m)
    if len(list[0]) == 400:
        for x in range(m):
            for z in range(n):
                iri_left[x] += abs(list[2][z+i][0] - list[0][z+i][0])
                iri_right[x] += abs(list[1][z+i][0] - list[0][z+i][0])
            iri[x] = (iri_left[x] + iri_right[x])/2
            i += n
    return iri

def simpsons_method(list):
    d_t = 0.005
    size = len(list)
    out = np.zeros(shape=(size,1))
    for x in range(2, size):
        out[x] = out[x-1] + ((list[x-2]+4*list[x-1]+list[x])*(d_t))/6
    return out
def trapezoidal_method(list):
    fs = 200
    size = len(list)
    out = np.zeros(size)
    for x in range(1, size):
        out[x] = out[x-1] + (list[x-1]+list[x])/(2*fs)
    return out
def plot_fft(data, fig):
    N = len(data)
    T = 1.0/100.0 #1/sample rate of device
    x = linspace(0.0, N*T, N)
    yf = scipy.fftpack.fft(data)
    xf = linspace(0.0, 1.0/(2.0*T), N/2)
    plt.figure(fig)
    plt.plot(xf, 2.0/N*abs(yf[:N//2]))
    if (fig == 2):
        plt.ylim(0, 0.4)
    else:
        plt.ylim(0, 0.005)
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



def process_signal(list, status, accel, speed, iri):
    dc_block = [dc_blocker(list[x]) for x in range(len(list))]
    mov_avg = [moving_average(dc_block[x], 15) for x in range(len(dc_block))]
    integ = [simpsons_method(mov_avg[x]) for x in range(len(mov_avg))]
    for x in range(len(mov_avg[0])):
        accel.put([mov_avg[0][x], mov_avg[1][x], mov_avg[2][x]])
    r_index = roughness(integ)
    #print(r_index)
    iri.put(r_index)
    return r_index
