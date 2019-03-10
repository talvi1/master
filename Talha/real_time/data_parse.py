from multiprocessing import Process, Queue
import time

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

def extract_queue(queue, status):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        list = []
        if (queue.qsize() >= 50):
            #print("Elapsed Time: " + str(elapsed_time)) 
            for x in range(50):
                list.append(queue.get())
               
            parse_data(list)      
            #print("Elapsed Time: " + str(elapsed_time))
            
def parse_data(list):
    f = 0
    t = 0
    count = 0
    multi_list = [[] for i in range(5)]
    for x in range(len(list)):
        ident = get_identity(list[x])
        if (ident == 'Xbee'):
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
            if (address == 0x00 and ver):
                multi_list[2] = data
                count += 1
            elif (address == 0x01 and ver):
                multi_list[3] = data
                count += 1
            elif (address == 0x02 and ver):
                multi_list[4] = data
                count += 1

            if (count == 3):
                count = 0
                for i in range(0, 2):
                    for j in range(0, 50):
                        if (len(multi_list[i+2]) < 50):
                            multi_list[i].append(0)
    for x in range(len(list)):
        ident = get_identity(list[x])
        if (ident == 'GPS0'):
            temp_list = list[x]
            s = temp_list[4:].split('|')
            multi_list[0].append(s[0])
            multi_list[1].append(s[1])
        else:
            multi_list[0].append(0)
            multi_list[1].append(0)                                   
    for v in zip(*multi_list):
        print(*v)
    #print(multi_list)        
    #print(multi_list)        
    #print("Frames Processed Correctly: " + str(t))
    #print("Frames Processed Incorrectly: " + str(f))

