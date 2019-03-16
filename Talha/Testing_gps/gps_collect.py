import serial
import threading
import queue
import time
import csv
import board
import busio
import adafruit_gps
from time import sleep
from picamera import PiCamera
import datetime

millis = time.ctime()
start_time = time.time()
def serial_read(s):
	while True:
		e = s.read()
		if (e.hex() == '7e'):
			line = s.read(108)
			queue.put('Xbee'+line.hex())
		
def gps_read(gps):
	timestamp = time.monotonic()
	while True:
		if (gps.update()):
			fix = gps.fix_quality
			speed = gps.speed_knots
			#while fix == 0 or fix == None or speed == None:
				#print ('Waiting for fix...')
				#fix = gps.fix_quality
				#speed = gps.speed_knots
				#time.sleep(1)
				#continue
			speed = gps.speed_knots
			#speed_km = 1.852*speed
			speed_queue.put(0)
			latitude = gps.latitude
			longitude = gps.longitude
			queue.put('GPS0'+str(50.45332))
			queue.put('GPS1'+str(-104.5432))
			queue.put(str(datetime.datetime.now().strftime("%d %b,%Y %H:%M:%S")))
		time.sleep(1)
		
def capture_image():
	while True:
		speed = 0
		if (speed < 5.0):
			fileName = 'image_' + str(datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S")) + '.jpg'
			queue.put(fileName)
			#camera.capture(fileName, use_video_port=True)
		sleep(1)
				

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)

gps = adafruit_gps.GPS(uart)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,500')

timestamp = time.monotonic()

#camera = PiCamera()
#camera.rotation = 180
#camera.resolution = (1920, 1080)
#camera.framerate = 60
#camera.brightness = 55


speed_queue = queue.Queue(0)
queue = queue.Queue(0)

serial0 = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)

send_1 = [0x42]
serial0.write(serial.to_bytes(send_1))

thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
thread2 = threading.Thread(target=gps_read, args=(gps,),).start()
thread2 = threading.Thread(target=capture_image,).start()
with open("40km_right_wheel.csv", mode='w', buffering=1) as csvfile:
	elapsed_time = time.time() - start_time
	while elapsed_time < 60.0:
		elapsed_time = time.time() - start_time
		line = queue.get()
		#print(line)
		csvfile.write(str(line))
		csvfile.write("\n")
		print(elapsed_time)
