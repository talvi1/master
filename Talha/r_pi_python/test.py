#import csv
#with open('data.csv', 'wb') as csvfile:
  #  spamwriter = csv.writer(csvfile, delimiter='|')
  #  spamwriter.writerow(['GPS_Coordinates'] + ['Accel_Z'] + ['Image_index'])
 #   for i in range(1000):
#        spamwriter.writerow([i] + [i+1000] + [i+500])

print("hello")
import serial
import threading
import queue
import time
import csv
millis = time.ctime()
start_time = time.time()
def serial_read(s):
    line = b'\x03'
    print(line.decode('utf8'))
    time.sleep(1)
def gps_read():
    while True:
        queue.put("hello")
        time.sleep(1)


queue = queue.Queue(0)
serial0 = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)
send_1 = [0x42]
serial0.write(serial.to_bytes(send_1))
thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
thread2 = threading.Thread(target=gps_read).start()

with open("filetest.csv", mode='wb', buffering=1) as csvfile:
	while True:
		line = queue.get()
		print(line)
		#csvfile.write(line)
		#csvfile.write("\n")
		elapsed_time = time.time() - start_time
		print(elapsed_time)
