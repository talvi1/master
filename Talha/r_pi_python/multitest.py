# import serial
# import queue
# import threading
#
# queue = queue.Queue(1000)
#
# def serial_read(s):
#     while True:
#         line = s.readline()
#         queue.put(line)
#
# #serial0 = serial.Serial('/dev/ttyUSB0')
# #serial1 = serial.Serial('/dev/ttyUSB1')
#
# thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
# thread2 = threading.Thread(target=serial_read, args=(serial1,),).start()
#
# while True:
#     line = queue.get(True, 1)
#     print(line)
import threading
from time import sleep
def thread1():
    try:
        while True:
            print("Thread1 run")
            sleep(3)
    except:
        print("thread 1 ended")
        ## Insert some clean up functions
        exit()
def thread2():
    try:
        while True:
            print("thread2 running")
            sleep(3)
    except KeyboardInterrupt:
      ## Insert some cleanup functions
      exit()
t2 = threading.Thread(target=thread1, args=()).start()
t1 = threading.Thread(target=thread2, args=()).start()
exit()
