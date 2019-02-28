import csv


def get_identity(seq):
     return seq[0:4]
def split_element(seq, length):
      return [seq[i:i+length] for i in range(0, len(seq), length)]
def check_sum_verify(seq):
    sum = 0
    del seq[0:3]
    for x in range(len(seq)):
        sum = sum + seq[x]
    check = sum & 0xff
    return check == 0xff

with open("filetest.csv", mode='r') as csvfile:
    my_list = []
    reader = csv.reader(csvfile)
    for row in reader:
        my_list.append(row)

lists = [my_list[x][0] for x in range(0, len(my_list))]
#list = [splitCount(lists[x]) for x in range(len(lists))]
for x in range(len(lists)):
    ident = get_identity(lists[x])
    if (ident == 'Xbee'):
        temp_list = split_element(lists[x], 2)
        del temp_list[0:2]
        del temp_list[-1]
        temp_list.insert(0, '7e')
        list_2 = [int(temp_list[x], 16) for x in range(0, len(temp_list))]
        immut_list = (list_2)
        check_sum_verify(list_2)
        print(immut_list)
        #print([hex(list_2[x]) for x in range(len(list_2))])
    elif (ident == 'GPS1'):
        print(lists[x])
    elif (ident == 'Imag'):
        print(lists[x])

#del list[0:9]
#del list[101:103]
#list_1 = [ ''.join(x) for x in zip(list[0::2], list[1::2]) ]
#list_2 = [int(list_1[x], 16) for x in range(0, len(list_1)) ]
#list_3 = [list_2[x]/2048 for x in range(0, len(list_2))]
print(list)
#print(len(list_1))
csvfile.close()
