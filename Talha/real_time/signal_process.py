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
def process_signal(accel_list):
    global counts
    counts = counts + 1
    dc_block_0 = dc_blocker(accel_list[0])
    dc_block_1 = dc_blocker(accel_list[1])
    dc_block_2 = dc_blocker(accel_list[2])
    mov_avg_0 = moving_average(dc_block_0, 33)
    mov_avg_1 = moving_average(dc_block_1, 33)
    mov_avg_2 = moving_average(dc_block_2, 33)
    plt.plot(dc_block_0)
    proc_parse = Process(target=plot_figure, args=(counts,))
    proc_parse.start()
    

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