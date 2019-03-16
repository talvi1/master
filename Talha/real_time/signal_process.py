import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from numpy import exp, pi, abs, angle, linspace
import scipy.fftpack
from multiprocessing import Process, Queue

def dc_blocker(accel):
    out = np.zeros(shape =(len(accel), 1))
    for x in range(1, len(accel)):
        out[x] = accel[x] - accel[x-1] + 0.9995*out[x-1]
    return out
counts = 0
def moving_average(accel, N):
    size = len(accel)
    p = int((N-1)/2)
    q = int(p + 1)
    out = np.zeros(shape=(size,1))
    sum = 0
    for x in range(0, N-1):
        sum = sum + accel[x]
    out[p] = sum/N
    for x in range(q , len(accel)):
        out[x] = out[x-1] + (1/N)*(accel[x] - accel[x-N])
    return out
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
    out = np.zeros(shape=(size,1))
    for x in range(1, size):
        out[x] = out[x-1] + (list[x-1]+list[x])/(2*fs)
    return out
def roughness_right(list, speed):
    car_speed = speed.get()
    sample_speed = 200.0
    i = 0
    iri_right = np.zeros(shape=(10, 1))
    for x in range(10):
        for z in range(10):
            iri_right[x] += abs(list[2][z+i] - list[0][z+i])
        iri_right[x] = iri_right[x]/10
        i += 10

    return iri_right
def roughness_left(list, speed):
    car_speed = speed.get()
    sample_speed = 200.0
    i = 0
    iri_left = np.zeros(shape=(10, 1))
    for x in range(10):
        for z in range(10):
            iri_left[x] += abs(list[1][z+i] - list[0][z+i])
        iri_left[x] = iri_left[x]/10
        i += 10
    return iri_left  

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

def plot_figure(count):
    plt.figure(count)
    plt.show()
def process_signal(accel_list, accel_0, accel_1, accel_2, speed, iri):
    global counts
    accel = np.zeros(shape=(len(accel_list[0]), 1))
    for x in range(len(accel_list[0])):
        accel[x] = accel_list[0][x]
    dc_block = [[] for i in range(3)]
    mov_avg = [[] for i in range(3)]
    integ = [[] for i in range(3)]
    dc_block[0] = dc_blocker(accel_list[0])
    dc_block[1]= dc_blocker(accel_list[1])
    dc_block[2] = dc_blocker(accel_list[2])
    mov_avg[0] = moving_average(dc_block[0], 15)
    mov_avg[1] = moving_average(dc_block[1], 15)
    mov_avg[2] = moving_average(dc_block[2], 15)
    integ[0] = simpsons_method(mov_avg[0])
    integ[1] = simpsons_method(mov_avg[1])
    integ[2] = simpsons_method(mov_avg[2])
    for x in range(len(mov_avg[0])):
        accel_0.put(mov_avg[0][x][0])
    for x in range(len(mov_avg[1])):
        accel_1.put(mov_avg[1][x][0])
    for x in range(len(mov_avg[2])):
        accel_2.put(mov_avg[2][x][0])
    y0 = roughness_right(integ, speed)
    y1 = roughness_left(integ, speed)
    for x in range(len(y0)):
        iri.put([y0[x][0], y1[x][0]])
        
    #print(len(mov_avg[0]))
    #print(len(mov_avg[1]))
    #print(len(mov_avg[2]))
    #print(len(mov_avg[0]))
        #counts = counts + 1
       # print(mov_avg[0][x][0])
       # print(x)
    #print(counts)
    #print(len(integ[0]))
   # print(len(integ[1]))
    #print(len(integ[2]))
    #for v in zip(*integ):
    #   print(*v)


#print(mov_avg_accel)
#plt.figure(1)
#plt.plot(mov_avg_accel)
#plt.figure(2)
#plt.plot(accel_z_0)
# plot_fft(accel_z_0, 1)
# plot_fft(Accel_Z_Device0, 2)
#plot_mag_response()
# plt.figure(3)
# plt.plot(Accel_Z_Device0)
# plt.figure(4)
# plt.plot(accel_z_0)
#plt.show()

# out = np.zeros(shape=(len(Accel_Z_Device2), 1))
# for x in range(1, len(Accel_Z_Device1)):
#     out[x] = Accel_Z_Device2[x] - Accel_Z_Device2[x-1] + 0.995*out[x-1]
# print(out)
# N = len(Accel_Z_Device1)
# T = 1.0/100.0
# x = np.linspace(0.0, N*T, N)
# yf = scipy.fftpack.fft(out)
# xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
# fig, ax = plt.subplots()
# ax.plot(xf, 2.0/N*np.abs(yf[:N//2]))
# plt.show()
# f = plt.figure(1)
# plt.plot(Accel_Z_Device2)
# f.show()
# g = plt.figure(2)
# plt.plot(out)
# g.show()
