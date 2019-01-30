import serial
import Queue
import threading

queue = Queue.Queue(1000)

def serial_read(s):
    while True:
        line = s.readline()
        queue.put(line)

serial0 = serial.Serial('/dev/ttyUSB0')
serial1 = serial.Serial('/dev/ttyUSB1')

thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
thread2 = threading.Thread(target=serial_read, args=(serial1,),).start()

while True:
    line = queue.get(True, 1)
    print line
