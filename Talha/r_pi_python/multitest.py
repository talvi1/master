import serial
import queue
import threading
import time
import board
import busio
import adafruit_gps
from picamera import PiCamera
from time import sleep


def serial_read(s):
    while True:
        line = s.readline()
        queue.put(line)

def GPS_collect(s):
    while True:
        s.update()
        line = s.satellites
        queue.put(line)
def camera(s):
    camera.capture('image{0:04d}.jpg'.format(i))

#Queue setup
queue = queue.Queue(0)

#GPS initialization
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
gps = adafruit_gps.GPS(uart)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')
timestamp = time.monotonic()

# Cameraa initialization
camera = PiCamera()
camera.rotation = 180
camera.resolution = (1920, 1080)
camera.framerate = 5
camera.brightness = 50

serial0 = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)

thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
thread2 = threading.Thread(target=GPS_collect, args=(gps,),).start()
thread3 = threading.Thread(target=camera, args=()).start()

while True:
    line = queue.get(True, 1)
    print(line)
