from multiprocessing import Process, Queue
import time
import signal_process
import numpy as np
import upload

def get_identity(seq):
     return seq[0:4]

def split_element(seq, length):
      return [seq[i:i+length] for i in range(0, len(seq), length)]

def check_sum_verify(seq):
    seq = list(seq)
    sum = 0
    del seq[0:3]
    for x in range(len(seq)):
        sum = sum + seq[x]
    check = sum & 0xff
    return check == 0xff

def shift_add(seq):
    list_top = [seq[x]<<8 for x in range(0, len(seq), 2)]
    list_bottom = [seq[x+1] for x in range(0, len(seq), 2)]
    list = [(list_top[x] + list_bottom[x]) for x in range(0, len(list_top))]
    list_signed = [(twos_complement(list[x])/2048)*9.83285 for x in range(len(list))]
    return list_signed

def twos_complement(value):
    if ((value & 0x8000)>>15):
        value = -1*((~value & 0xFFFF) + 1)
    return value

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
    list_upload[1] = z
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
