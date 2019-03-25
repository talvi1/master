import serial
import threading
import queue
import time
import csv
import board
import busio
import adafruit_gps

millis = time.ctime()
start_time = time.time()
def serial_read(s):
	while True:
		e = s.read()
		if (e.hex() == '7e'):
			line = s.read(109)
			print(line.hex())
			queue.put('Xbee'+line.hex())
		
def gps_read(gps):
	timestamp = time.monotonic()
	while True:
		gps.update()
		current = time.monotonic()
		if current - timestamp >= 1.0:
			timestamp = current
		if not gps.has_fix:
			print ('Waiting for fix...')
			time.sleep(1)
			continue
		x = 'Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
      gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
      gps.timestamp_utc.tm_mday,  # struct_time object that holds
      gps.timestamp_utc.tm_year,  # the fix time.  Note you might
      gps.timestamp_utc.tm_hour,  # not get all data like year, day,
      gps.timestamp_utc.tm_min,   # month!
      gps.timestamp_utc.tm_sec)
		sat = gps.satellites
		speed = gps.speed_knots
		latitude = gps.latitude
		longitude = gps.longitude 
		queue.put(x)
		queue.put(sat)
		queue.put(speed)
		queue.put(latitude)
		queue.put(longitude)
		time.sleep(0.5)
		
		

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)

gps = adafruit_gps.GPS(uart)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')

timestamp = time.monotonic()
queue = queue.Queue(0)
#serial0 = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)

send_1 = [0x42]
#serial0.write(serial.to_bytes(send_1))

#thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
thread2 = threading.Thread(target=gps_read, args=(gps,),).start()

with open("file_gps.csv", mode='w', buffering=1) as csvfile:
	while True:
		line = queue.get()
		#print(line)
		csvfile.write(str(line))
		csvfile.write("\n")
		elapsed_time = time.time() - start_time
		print(elapsed_time)
