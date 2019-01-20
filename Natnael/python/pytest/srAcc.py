import serial


ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3000, bytesize=8, parity='N')


def serialValue():
    if(ser.isOpen()):
        try:
            return ser.readline()
        except Exception:
            return 0
    else:
         return 1

f = open("serialValue.txt", "a")

for i in range(10):
    f.write("This is line %d\r\n" % (i+1))
f.close()

"""
def yax():
    y_axis[]

    

    return y_axis[]
"""

#
#if(ser.isOpen()):
#    try:
#        while(1):
#            print(ser.readline())
#    except Exception:
#         print("error1")
#else:
#    print("Cannot print  serail port")
