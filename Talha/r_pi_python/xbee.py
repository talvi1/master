import time
import serial
from timeit import default_timer as timer

start = timer()


ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, bytesize=8, parity='N', stopbits=1)

to_send1 = [0x42];
#to_send = [0x7E, 0x00, 0x04, 0x08, 0x01, 0x48, 0x56, 0x58]
ser.write(serial.to_bytes(to_send1))
#ser.write(serial.to_bytes(to_send))

while True:
   data = ser.read()
   #print(hex(ord(data)))
   print(data)
   print(timer())
