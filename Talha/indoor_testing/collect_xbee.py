import serial
import threading
import queue
import time
import csv
millis = time.ctime()
start_time = time.time()
def serial_read(s):
	seq = []
	while True:
		e = s.read()
		if(e.hex() == '7e'):
			line = s.read(108)
			#print(line.hex())
			queue.put('Xbee'+line.hex())

def gps_read():
    while True:
        queue.put("hello")
        time.sleep(1)


queue = queue.Queue(0)
serial0 = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)
send_1 = [0x42]
serial0.write(serial.to_bytes(send_1))
thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
#thread2 = threading.Thread(target=gps_read).start()

with open("test_2_16.csv", mode='w', buffering=1) as csvfile:
	while True:
		line = queue.get()
		#print(line)
		csvfile.write(line)
		csvfile.write("\n")
		elapsed_time = time.time() - start_time
		print(elapsed_time)
