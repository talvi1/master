"""
Author: Talha Alvi
Capstone Project 2019
Description: All the funtions that are used for parsing and processing the data so it is in a usable form
"""
from multiprocessing import Process, Queue
import time
import signal_process
import numpy as np
import upload

"""
Function: get_identity()
Parameters:
    seq - list containing any data
Return type: Returns first four elements of the list
Requirements: None
Description: Returns identifier for showing what device data in list is from (Xbee, gps, camera)
"""
def get_identity(seq):
     return seq[0:4]
"""
Function: split_element()
Parameters:
    seq - list containing xbee data frame
    length - Length to split the list elements into
Return type: List with xbee data frame split into bytes of length parameter
Requirements: None
Description: Takes an xbee frame and splits it into a list with elements of different lengths based on size of length passed to function
"""
def split_element(seq, length):
      return [seq[i:i+length] for i in range(0, len(seq), length)]
"""
Function: check_sum_verify()
Parameters:
    seq - list containing Xbee frames data as bytes
Return type: Returns true or false based on if check sum of xbee frame is verified
Requirements: None
Description: Sums the xbee frame without the preamble and checks if the lower 8 bits of the sum are 0xff, if they are that means that the integrity of the data in the frame is intact
"""
def check_sum_verify(seq):
    seq = list(seq)
    sum = 0
    del seq[0:3]
    for x in range(len(seq)):
        sum = sum + seq[x]
    check = sum & 0xff
    return check == 0xff
"""
Function: shift_add()
Parameters:
    seq - list containing accelerometer data as raw hex bytes, each accelerometer value is 16 bits or 2 bytes
Return type: Returns list containing signed float values of accelereration in m/s^2
Requirements: None
Description: Shifts the upper bits into a list. Upper and lower bits are added to get raw acceleration value in bytes. Raw hex value is converted into a signed number using twos_complement().
             The result from the twos_complement() is divided by the range of accelerometer and multiplied by gravitational acceleration to get acceleration in m/s^2.
"""
def shift_add(seq):
    list_top = [seq[x]<<8 for x in range(0, len(seq), 2)]
    list_bottom = [seq[x+1] for x in range(0, len(seq), 2)]
    list = [(list_top[x] + list_bottom[x]) for x in range(0, len(list_top))]
    list_signed = [(twos_complement(list[x])/2048)*9.83285 for x in range(len(list))]
    return list_signed
"""
Function: twos_complement()
Parameters:
    value - hex value to be converted into a signed value
Return type: Signed value of hex value
Requirements: Input to the function must be 16 bits
Description: Checks if there is a leading one (if number is supposed to be negative), if it is, it does twos complement operation on it, and returns the value
"""
def twos_complement(value):
    if ((value & 0x8000)>>15):
        value = -1*((~value & 0xFFFF) + 1)
    return value
"""
Function: get_count_frames()
Parameters:
    list - list containing many xbee frames from various devices
Return type: List with 3 elements showing the number of frames received from each of the three devices transmitting data
Requirements: None
Description: Loops over list and if xbee frame is found, it gets the device id of the xbee frame (address). Increments counters depending on which device id is seen. Returns list
             showing number of frames received from each of the three devices being used.
"""
def get_count_frames(list):
    device_0 = 0
    device_1 = 0
    device_2 = 0
    for x in range(len(list)):
        ident = get_identity(list[x])
        if (ident =='Xbee'):
            temp_list = split_element(list[x], 2)
            del temp_list[0:2]
            temp_list.insert(0, '7e')
            list_2 = [int(temp_list[x], 16) for x in range(0, len(temp_list))]
            address = list_2[5]
            if (address == 0x00):
                device_0 = device_0 + 1
            elif (address == 0x01):
                device_1 = device_1 + 1
            elif (address == 0x02):
                device_2 = device_2 + 1
    return [device_0, device_1, device_2]

"""
Function: extract_queue()
Parameters:
    data_queue - queue containing the data being collected from Xbee, camera, GPS
    status - queue used to communicate the status of the program among the various processes
    accel - queue used to pass acceleration values to live plot
    speed - queue used to keep track of speed of car across multiple processes
    iri - queue used to pass roughness index values to live plot

Return type: None
Requirements: Data collection has been initialized and the data_queue is constantly being updated with data from all three devices
Description: In a while loop the program checks if the main data collection queue is gotten to a certain size. After it has reached
             that size, it creates an even list the size of fr containing frames from each of the three accelerometers that are
             transmitting data. If too much time is spent trying to create the list. The program closes out as there is something wrong.
             The rest of the GPS and camera data is appended to the main data_list as well. The data_list containing the Xbee frames and
             GPS data and camera image names is then parsed using parse_data() function.
"""
def extract_queue(data_queue, status, accel, speed, iri):

    while True:
        start_time = time.time()

        temp = [[] for x in range(3)]
        data_list = []
        img_list = []
        count = 0
        fr = 10
        #print(queue.qsize())
        if (data_queue.qsize() > 35):
            while len(temp[0]) != fr or len(temp[1]) != fr or len(temp[2]) != fr:
                elapsed_time = time.time() - start_time
                item = data_queue.get()
                if item[0:4] == 'Xbee':
                    device_id = item[13]
                    #print(device_id)
                    if device_id == '0' and len(temp[0]) < fr:
                        temp[0].append(item)
                    elif device_id == '1' and len(temp[1]) < fr:
                        temp[1].append(item)
                    elif device_id == '2' and len(temp[2]) < fr:
                        temp[2].append(item)
                else:
                    data_list.append(item)

                if elapsed_time > 5.0:
                    status.put([0, 'Something is wrong...'])
        #print(temp_list)
            for x in range(fr):
                data_list.append(temp[0][x])
                data_list.append(temp[1][x])
                data_list.append(temp[2][x])
            #print(frames)
            parse_data(data_list, status, accel, speed, iri)
    #    print("Elapsed Time: " + str(elapsed_time))

"""
Function: parse_data()
Parameters:
    list - list containing raw xbee frames containing acceleration data in hex bytes, GPS coordinates, and camera image name
    status - queue used to track status of program across multiple processes
    accel - queue used to pass acceleration values to live plot process
    speed - queue used to track speed of car across multiple processes
    iri - queue used to pass roughness index values to live plot process

Return type: None
Requirements: Data is being collected and has been extracted from the main data collection queue and put into a list
Description: The function loops over a list containing the raw acceleration data, GPS coordinates and camera image names.
             The raw acceleration data is processed by first verifying the check sum of the Xbee frames. The raw hex bytes
             are then converted into signed m/s^2 values using shift_add() function. A list containing the acceleration
             values from each device transmitting is then built, which is passes to a function used to perform signal processing
             on the data. The returned filtered data is then formatted into a multi dimensionoal list containing all of the data,
             which is then uploaded to a data base by calling the upload_mysql() function.  
"""

def parse_data(list, status, accel, speed, iri):
    f = 0
    t = 0
    frame_count = 0
    #print(list)
    multi_list = [[] for i in range(3)]
    store = [[] for i in range(3)]
    for x in range(len(list)):
        ident = get_identity(list[x])
        if (ident == 'Xbee'):
            frame_count = frame_count + 1
            temp_list = split_element(list[x], 2)
            del temp_list[0:2]
            temp_list.insert(0, '7e')
            list_2 = [int(temp_list[x], 16) for x in range(0, len(temp_list))]
            ver = check_sum_verify(tuple(list_2))
            if (ver):
                t = t+1
            else:
                f = f+1
            address = list_2[5]
            del list_2[0:8]
            del list_2[-1]
            data = shift_add(list_2)
            #print(data)
            if (address == 0x00 and ver):
                for x in range(len(data)):
                    multi_list[0].append(data[x])
            elif (address == 0x01 and ver):
                for x in range(len(data)):
                    multi_list[1].append(data[x])
            elif (address == 0x02 and ver):
                for x in range(len(data)):
                    multi_list[2].append(data[x])
        elif ident == 'GPS0':
            temp = list[x]
            s = temp[4:].split('|')
            store[1].append(float(s[0]))
            store[2].append(float(s[1]))
        elif ident == 'Imag':
            store[0].append(list[x])
    roughness = signal_process.process_signal(multi_list, status, accel, speed, iri)
    lat = np.linspace(store[1][0], store[1][-1], len(roughness))
    longi = np.linspace(store[2][0], store[2][-1], len(roughness))
    z = []
    if len(store[0]) == 0:
        store[0].append(0)
    lesn = int(len(roughness)/len(store[0]))
    for i in range(len(store[0])):
        for j in range(lesn):
            z.append(store[0][i])
    if (len(z)) != len(roughness):
        for x in range(len(roughness) - len(z)):
            z.append(store[0][-1])
    list_upload = [[] for i in range(5)]
    list_upload[0] = z
    for x in range(len(roughness)):
        list_upload[1].append("Wascana_Pkway")
    list_upload[2] = roughness
    list_upload[3] = lat
    list_upload[4] = longi
   # for i in range(len(list_upload)):
   #     print(len(list_upload[i]))
   # print(list_upload[0])
    upload.upload_mysql(list_upload)
    #print(np.linspace(list_upload[1][0], list_upload[2][-1], len(roughness)))
 #   for v in zip(*list_upload):
  #       print(*v)
    #print(frame_count)
    #print(multi_list[0])
    #print(len(multi_list))

    #print(multi_list[4])
    #print(multi_list)
    #print("Frames Processed Correctly: " + str(t))
    #print("Frames Processed Incorrectly: " + str(f))
