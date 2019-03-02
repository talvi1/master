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
    list = [(list_top[x] + list_bottom[x])/2048 for x in range(0, len(list_top))]
    return list

with open("filetest.csv", mode='r') as csvfile:
    my_list = []
    reader = csv.reader(csvfile)
    for row in reader:
        my_list.append(row)

lists = [my_list[x][0] for x in range(0, len(my_list))]
#list = [splitCount(lists[x]) for x in range(len(lists))]
with open("saved_data.csv", mode='a') as csvfile2:
    csvwrite = csv.writer(csvfile2, delimiter='|')
    csvwrite.writerow(['GPS_Coordinates'] + ['Accel_Z_Device0'] + ['Accel_Z_Device1'] + ['Accel_Z_Device2'] + ['Image_Index'])
    for x in range(len(lists)):
        ident = get_identity(lists[x])
        if (ident == 'Xbee'):
            temp_list = split_element(lists[x], 2)
            del temp_list[0:2]
            del temp_list[-1]
            temp_list.insert(0, '7e')
            list_2 = [int(temp_list[x], 16) for x in range(0, len(temp_list))]
            check_sum_verify(tuple(list_2))
            address = list_2[5]
            del list_2[0:8]
            del list_2[-1]
            data = shift_add(list_2)
            print(data)
            if (address == 0x02):
                for x in range(0, len(data)):
                    csvwrite.writerow(['                        '] + [data[x]] + [''] + [''] + [''])
            elif (address == 0x01):
                print('')
            elif (address == 0x01):
                print('')
        elif (ident == 'GPS1'):
            print(lists[x])
            csvwrite.writerow([lists[x]] + [''] + [''] + [''] + [''])
        elif (ident == 'Imag'):
            print(lists[x])

csvfile.close()
csvfile2.close()
