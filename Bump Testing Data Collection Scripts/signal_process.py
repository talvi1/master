"""
Author: Talha Alvi
Capstone Project 2019
Description: Similar to the signal_process.py in the real time data collection script, however, here the data being processed is
             from a csv file. The data is read from a csv file into a pandas frame. The pandas frame is then parsed and the various
             filters, integration methods and the roughness index algorithm are implemented on the data. The data is then used to
             generate various plots using matplotlib. The graphs are used to make sure that data fits expectation and see what filters
             work best for the application. 
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import exp, pi, abs, angle, linspace
import scipy.fftpack
from scipy import signal

def dc_blocker(accel):
    out = np.zeros(len(accel))
    for x in range(1, len(accel)):
        out[x] = accel[x] - accel[x-1] + 0.9995*out[x-1]
    return out

def moving_average(accel, N):
    size = len(accel)
    p = int((N-1)/2)
    q = int(p + 1)
    out = np.zeros(len(accel))
    sum = 0
    for x in range(0, N-1):
        sum = sum + accel[x]
    out[p] = sum/N
    for x in range(q , size):
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
def roughness(list2, list1):
    sample_speed = 200.0
    i = 0
    iri = np.zeros(shape=(8, 1))
    if len(list2) == 200:
        for x in range(8):
            for z in range(25):
                iri[x] += abs(list2[z+i] - list1[z+i])
            iri[x] = iri[x]/25
            i += 8

    return iri
def simpsons_method(list):
    d_t = 0.005
    size = len(list)
    np.append(list,[0,0,0])
  #  print(list)
    out = np.zeros(len(list))
    for x in range(2, size):
        out[x] = out[x-1] + ((list[x-2]+4*list[x-1]+list[x])*(d_t))/6
    return out
def trapezoidal_method(list):
    fs = 200
    size = len(list)
    np.append(list,[0,0,0])
    print(list)
    out = np.zeros(len(list))
    for x in range(1, size):
        out[x] = out[x-1] + (list[x-1]+list[x])/(2*fs)
    return out
def plot_fft(data, fig):
    N = len(data)
    T = 1.0/200.0 #1/sample rate of device
    x = linspace(0.0, N*T, N)
    yf = scipy.fftpack.fft(data)
    xf = linspace(0.0, 1.0/(2.0*T), N/2)
    plt.figure(fig)
    plt.plot(xf, 2.0/N*abs(yf[:N//2]))


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

def convert():
    return 0

df = pd.read_csv('parsed_data_2in/30km_both_wheels_accelerometer_signal.csv', sep='|')

Accel_Z_Device0 = df['Accel_Z_Device0']
Accel_Z_Device1 = df['Accel_Z_Device1']
Accel_Z_Device2 = df['Accel_Z_Device2']

Device0 = Accel_Z_Device0.values.tolist()
Device1 = Accel_Z_Device1.values.tolist()
Device2 = Accel_Z_Device2.values.tolist()

#Accel_Z_Device0.reset_index(inplace=True)

n = 200


a_0 = [Device0[i:i+n] for i in range(0, len(Device0), n)]
a_1 = [Device1[i:i+n] for i in range(0, len(Device1), n)]
a_2 = [Device2[i:i+n] for i in range(0, len(Device2), n)]

accel_z_0 = [dc_blocker(a_0[i]) for i in range(len(a_0))]
accel_z_1 = [dc_blocker(a_1[i]) for i in range(len(a_1))]
accel_z_2 = [dc_blocker(a_2[i]) for i in range(len(a_2))]

low_pass_0 = [low_pass(accel_z_0[i]) for i in range(len(accel_z_0))]
low_pass_1 = [low_pass(accel_z_1[i]) for i in range(len(accel_z_1))]
low_pass_2 = [low_pass(accel_z_2[i]) for i in range(len(accel_z_2))]

band_pass_0 = [band_pass(accel_z_0[i]) for i in range(len(accel_z_0))]
band_pass_1 = [band_pass(accel_z_1[i]) for i in range(len(accel_z_1))]
band_pass_2 = [band_pass(accel_z_2[i]) for i in range(len(accel_z_2))]
mov_avg_accel_0 = [moving_average(accel_z_0[i], 9) for i in range(len(accel_z_0))]
mov_avg_accel_1 = [moving_average(accel_z_1[i], 9) for i in range(len(accel_z_1))]
mov_avg_accel_2 = [moving_average(accel_z_2[i], 9) for i in range(len(accel_z_2))]

# integ_0 = [simpsons_method(mov_avg_accel_0[i]) for i in range(len(mov_avg_accel_0))]
# integ_1 = [simpsons_method(mov_avg_accel_1[i]) for i in range(len(mov_avg_accel_1))]
# integ_2 = [simpsons_method(mov_avg_accel_2[i]) for i in range(len(mov_avg_accel_2))]

# integ_0 = [simpsons_method(low_pass_0[i]) for i in range(len(low_pass_0))]
# integ_1 = [simpsons_method(low_pass_1[i]) for i in range(len(low_pass_1))]
# integ_2 = [simpsons_method(low_pass_2[i]) for i in range(len(low_pass_2))]

integ_0 = [simpsons_method(band_pass_0[i]) for i in range(len(band_pass_0))]
integ_1 = [simpsons_method(band_pass_1[i]) for i in range(len(band_pass_1))]
integ_2 = [simpsons_method(band_pass_2[i]) for i in range(len(band_pass_2))]

iri_1 = [roughness(integ_1[i], integ_0[i]) for i in range(len(integ_1))]
iri_2 = [roughness(integ_2[i], integ_0[i]) for i in range(len(integ_2))]
avg_iri = [(iri_1[i]+iri_2[i])/2 for i in range(len(iri_1))]


a_0 = [j for i in a_0 for j in i]
a_1 = [j for i in a_1 for j in i]
a_2 = [j for i in a_2 for j in i]
accel_z_0 = [j for i in accel_z_0 for j in i]
accel_z_1 = [j for i in accel_z_1 for j in i]

accel_z_2 = [j for i in accel_z_2 for j in i]
low_pass_0 = [j for i in low_pass_0 for j in i]
low_pass_1 = [j for i in low_pass_1 for j in i]
low_pass_2 = [j for i in low_pass_2 for j in i]
band_pass_0 = [j for i in band_pass_0 for j in i]
band_pass_1 = [j for i in band_pass_1 for j in i]
band_pass_2 = [j for i in band_pass_2 for j in i]
mov_avg_accel_0 = [j for i in mov_avg_accel_0 for j in i]
mov_avg_accel_1 = [j for i in mov_avg_accel_1 for j in i]
mov_avg_accel_2 = [j for i in mov_avg_accel_2 for j in i]
integ_0 = [j for i in integ_0 for j in i]
integ_1 = [j for i in integ_1 for j in i]
integ_2 = [j for i in integ_2 for j in i]

iri_1 = [j for i in iri_1 for j in i]
iri_2 = [j for i in iri_2 for j in i]
avg_iri = [j for i in avg_iri for j in i]
y = np.ones(200)
# z = signal.firwin(11, 0.3, window='hann')
# print(y)
# print(accel_z_2[15])
# l = signal.lfilter(z, [1.0], accel_z_2[15])band_pass
fig = plt.figure()
plt.subplot(1, 1 ,1)
plt.plot(avg_iri)
plt.xlabel('Samples')
plt.ylabel('Roughness Index')
plt.title('Average Roughness')

# plt.ylabel('Roughness(m/m)')
# plt.xlabel('Samples (k)')
# plt.title('Roughness Left Wheel at 30 km/h using Band Pass')
# plt.subplot(2, 1, 1)
# plt.plot(iri_2)
# plt.ylabel('Roughness(m/m)')
# plt.xlabel('Samples (k)')
# plt.title('Roughness Right Wheel at 30 km/h using Band Pass')
# plt.ylim(0, 10)

plt.show()

#plt.savefig('Roughness_30_kmh_right_wheel_low_pass.png', dpi=1200)

# plt.plot(band_pass_1)
#
# plt.figure(2)
# plt.plot(iri_2)

# plt.figure(3)
# plt.plot(accel_z_1)
#
# plt.figure(4)
# plt.plot(a_1)

# plt.figure(2)
# plt.plot(a_0)
# #plt.ylim((-15, 15))
# plt.figure(3)
# plt.plot(mov_avg_accel_2)
# plt.ylim((-15, 15))
# plt.figure(4)
# plt.plot(integ_0)
# plt.ylim((-15, 15))
# plt.figure(5)
# plt.plot(integ_1)
# plt.ylim((-15, 15))
# plt.figure(6)
# plt.plot(integ_2)
# plt.ylim((-15, 15))

#plot_fft(Accel_Z_Device2, 1)

# plot_fft(accel_z_0, 1)
# plot_fft(Accel_Z_Device0, 2)
#plot_mag_response()
# plt.figure(3)
# plt.plot(Accel_Z_Device0)
# plt.figure(4)
# plt.plot(accel_z_0)


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
