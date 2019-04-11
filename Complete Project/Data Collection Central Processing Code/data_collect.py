"""
Author: Talha Alvi
Capstone Project 2019
Description: All the funtions that are used to collect data from each of the hardware devices. 
"""
import serial
import board
import busio
import adafruit_gps
from picamera import PiCamera
from multiprocessing import Process, Queue
import datetime
from time import sleep
import time

"""
Function: serial_read()
Parameters:
    data_queue - Queue to store data(xbee, image name, gps coordinates) as it arrives real time, shared among all processes
    speed_queue - Queue to store speed data from GPS to be shared among other processes to adjust rate at which data is captured/processed
    s - Serial port object, initialized in start_collection()
Return type: None
Requirements: Requires serial port to be initialized before being called. Must be called inside a separate process/thread to insure data can be collected from
			  multiple devices concurrently
Description: Based on speed condition, reads invididual byte to see if it sees start of a Xbee frame, if frame is seen, it reads the whole frame length.
			 Frame is then put into the data queue with a identifier as to what device the data is from. Data collection is continuous
"""
def serial_read(data_queue, speed_queue, s):
	frame_length = 108
	while True:
		speed = 0
		if (speed < 5.0):
			e = s.read()
			if (e.hex() == '7e'):
				line = s.read(frame_length)
				data_queue.put('Xbee'+line.hex())
"""
Function: gps_read()
Parameters:
    data_queue - Queue to store data(xbee, image name, gps coordinates) as it arrives real time, shared among all processes
    speed_queue - Queue to store speed data from GPS to be shared among other processes to adjust rate at which data is captured/processed
    gps - Serial port object, initialized in start_collection()
Return type: None
Requirements: Requires serial port to be initialized before being called. Must be called inside a separate process/thread to insure data can be collected from
			  multiple devices concurrently
Description: Initialized GPS update rate is set to 1 Hz in start_collection(), continuously gets new data from GPS after a second has elapsed. Uses time.monotonic() to see if a second has elapsed
			 and gets GPS data. Checks if GPS has a fix, if GPS doesn't have a fix to a satellite, waits in a while loop. If fix is found, gets speed, latitude and longitude data from
			 the GPS. Adds latitude and longitude data to data_queue with a GPS0 identifier. Speed data is stored in speed_queue. Both queues are shared among multiple processes.

"""
def gps_read(data_queue, speed_queue, gps):
	timestamp = time.monotonic()
	while True:
		gps.update()
		current = time.monotonic()
		if current - timestamp >= 1.0:
			timestamp = current
			if not gps.has_fix:
				print ('Waiting for GPS')
				continue
			speed = gps.speed_knots
			speed_km = 1.852*float(speed)
			for x in range(15):
				speed_queue.put(0)
			latitude = gps.latitude
			longitude = gps.longitude
			data_queue.put('GPS0'+str(latitude) + "|" + str(longitude))
			time.sleep(1)
"""
Function: capture_image()
Parameters:
    data_queue - Queue to store data(xbee, image name, gps coordinates) as it arrives real time, shared among all processes
    speed_queue - Queue to store speed data from GPS to be shared among other processes to adjust rate at which data is captured/processed
Return type: None
Requirements: Must be called inside a separate process.
Description: Initializes camera settings. Continuously captures images based on specified sleep time, which effectively sets the sample rate of the camera.
			 Images are stored based on date and time stamp. The image name is put into data_queue to be able to identify, where and which image was captured.
"""
def capture_image(data_queue, speed_queue):
	 camera = PiCamera()
	 camera.rotation = 0
	 camera.resolution = (1920, 1080)
	 camera.framerate = 60
	 camera.brightness = 50
	 while True:
		 speed = speed_queue.get()
		 if (speed < 5.0):
			 fileName = 'Image_' + str(datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S")) + '.jpg'
			 data_queue.put(fileName)
			 camera.capture(fileName, use_video_port=True)
			 sleep(0.75)
"""
Function: start_collection()
Parameters:
    data_queue - Queue to store data(xbee, image name, gps coordinates) as it arrives real time, shared among all processes
    status_queue - Queue to store status messages about program errors and to show program state in real time
    speed_queue - Queue to store speed data from GPS to be shared among other processes to adjust rate at which data is captured/processed
Return type: None
Requirements: None
Description: Initializes serial ports for GPS and Xbee. Sends command to GPS to read only necessary data in specified format and set sample rate. Wakes up Xbee device
			 by getting it out of boot loader mode by sending 0x42. Creates new processes and starts them for each of xbee, gps and camera to get data concurrently.
"""
def start_collection(data_queue, status_queue, speed_queue):
	gps = 0
	uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
	gps = adafruit_gps.GPS(uart)
	gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
	gps.send_command(b'PMTK220,1000')

	serial0 = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)
	send_1 = [0x42]
	serial0.write(serial.to_bytes(send_1))

	global proc_xbee
	global proc_gps
	global proc_camera

	proc_xbee = Process(target=serial_read, args=(data_queue, speed_queue, serial0,))
	proc_gps = Process(target=gps_read, args=(data_queue, speed_queue, gps,))
	proc_camera = Process(target=capture_image, args=(data_queue, speed_queue,))
	proc_xbee.start()
	proc_gps.start()
	proc_camera.start()
	status_queue.put([1, "Data Collection Started"])
"""
Function: finish_collection()
Parameters: None
Return type: None
Requirements: None
Description: Terminates and joins the processes started for gps, camera and xbee safely, when program execution is finished
"""
def finish_collection():

	proc_gps.terminate()
	proc_xbee.terminate()
	proc_camera.terminate()

	proc_gps.join()
	proc_xbee.join()
	proc_camera.join()
