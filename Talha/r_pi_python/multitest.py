import serial
import queue
from threading import Timer, Thread, Event
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

def GPS_collect(gps):
    timestamp = time.monotonic()
    while True:
        gps.update()
        current = time.monotonic()
        if current - timestamp >= 1.0:
            timestamp = current
       # line = gps.timestamp
        x = 'Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
        gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
        gps.timestamp_utc.tm_mday,  # struct_time object that holds
        gps.timestamp_utc.tm_year,  # the fix time.  Note you might
        gps.timestamp_utc.tm_hour,  # not get all data like year, day,
        gps.timestamp_utc.tm_min,   # month!
        gps.timestamp_utc.tm_sec)
        queue.put(x)
    
class RepeatEvery(threading.Thread):
    def __init__(self, interval, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self.interval = interval 
        self.func = func       
        self.args = args         
        self.kwargs = kwargs     
        self.runable = True
    def run(self):
        while self.runable:
            self.func(*self.args, **self.kwargs)
            sleep(self.interval)
    def stop(self):
        self.runable = False

def camera_capture():
    global count
    count = count + 1
    camera.capture('image{0:04d}.jpg'.format(count))
    

#Queue setup
queue = queue.Queue(1000)

#GPS initialization
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
gps = adafruit_gps.GPS(uart)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')
timestamp = time.monotonic()

# Camera initialization
camera = PiCamera()
camera.rotation = 180
camera.resolution = (1920, 1080)
camera.framerate = 5
camera.brightness = 50

count = 0

serial0 = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)

thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
thread2 = threading.Thread(target=GPS_collect, args=(gps,),).start()
thread3 = RepeatEvery(1, camera_capture).start()

while True:
    line = queue.get(True, 10)
    print(line)
