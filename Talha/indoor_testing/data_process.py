import csv


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

with open("test_2_16.csv", mode='r') as csvfile:
    my_list = []
    reader = csv.reader(csvfile)
    for row in reader:
        my_list.append(row)

lists = [my_list[x][0] for x in range(0, len(my_list))]
#list = [splitCount(lists[x]) for x in range(len(lists))]
f = 0
t = 0
with open("data_processed_09_march.csv", mode='a', buffering=1) as csvfile2:
    csvwrite = csv.writer(csvfile2, delimiter='|')
    csvwrite.writerow(['GPS_Coordinates'] + ['Accel_Z_Device0'] + ['Accel_Z_Device1'] + ['Accel_Z_Device2'] + ['Image_Index'])
    count = 0
    multi_list = [[] for i in range(3)]
    for x in range(len(lists)):
        ident = get_identity(lists[x])
        if (ident == 'Xbee'):
            temp_list = split_element(lists[x], 2)
            del temp_list[0:2]
            temp_list.insert(0, '7e')
            list_2 = [int(temp_list[x], 16) for x in range(0, len(temp_list))]
            ver = check_sum_verify(tuple(list_2))
            if (ver):
                t = t+1
            else :
                f = f+1

            #print('\n')
            address = list_2[5]
            del list_2[0:8]
            del list_2[-1]
            #print(list_2)
            #print(temp_list)
            #print([hex(list_2[x]) for x in range(len(list_2))])
            data = shift_add(list_2)
            #print(data)
            if (address == 0x00 and ver):
                multi_list[0] = data
                count += 1
            elif (address == 0x01 and ver):
                multi_list[1] = data
                count += 1
            elif (address == 0x02 and ver):
                multi_list[2] = data
                count += 1

            if (count == 3):
                count = 0
                for i in range(len(multi_list)):
                    for j in range(0, 50):
                        if (len(multi_list[i]) < 50):
                            multi_list[i].append(0)
                for i in range(len(multi_list)):
                    for j in range(0, 50):
                        csvwrite.writerow(['         '] + [multi_list[0][j]] + [multi_list[1][j]] + [multi_list[2][j]] + [''])
        elif (ident == 'GPS1'):
            print(lists[x])
            csvwrite.writerow([lists[x]] + [''] + [''] + [''] + [''])
        elif (ident == 'Imag'):
            print(lists[x])
print(t)
print(f)
csvfile.close()
csvfile2.close()
