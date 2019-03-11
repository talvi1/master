import serial
import board
import busio
import adafruit_gps
from picamera import PiCamera
from multiprocessing import Process, Queue
import datetime
from time import sleep
import time


millis = time.ctime()
start_time = time.time()
def serial_read(queue, speed_queue, s):
	while True:
		speed = 0
		if (speed < 5.0):
			e = s.read()
			if (e.hex() == '7e'):
				line = s.read(108)
				queue.put('Xbee'+line.hex())
		
def gps_read(queue, speed_queue, gps):
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
			for x in range(70):
				speed_queue.put(0)
			latitude = gps.latitude
			longitude = gps.longitude
			queue.put('GPS0'+str(50.45332) + "|" + str(-104.5432))
			queue.put("time" + str(datetime.datetime.now().strftime("%d %b,%Y %H:%M:%S")))
		time.sleep(1)
		
def capture_image(queue, speed_queue):
	camera = PiCamera()
	camera.rotation = 180
	camera.resolution = (1920, 1080)
	camera.framerate = 60
	camera.brightness = 55
	while True:
		speed = speed_queue.get()
		if (speed < 5.0):
			fileName = 'image_' + str(datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S")) + '.jpg'
			queue.put(fileName)
			#camera.capture(fileName, use_video_port=True)
		sleep(1)
				
def start_collection(queue, status, process_queue):
	uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
	gps = adafruit_gps.GPS(uart)
	gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
	gps.send_command(b'PMTK220,500')
	
	serial0 = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)
	send_1 = [0x42]
	serial0.write(serial.to_bytes(send_1))
	
	speed_queue = Queue()
	
	global proc_xbee 
	global proc_gps
	global proc_camera
	
	proc_xbee = Process(target=serial_read, args=(queue, speed_queue, serial0,))
	proc_gps = Process(target=gps_read, args=(queue, speed_queue, gps,))
	proc_camera = Process(target=capture_image, args=(queue, speed_queue,))
	proc_xbee.start()
	proc_gps.start()
	proc_camera.start()
	status.put("Data Collection Started")

def finish_collection(status):
	
	proc_gps.terminate()
	proc_xbee.terminate()
	proc_camera.terminate()
	
	proc_gps.join()
	proc_xbee.join()
	proc_camera.join()
	
	
	
	
	



