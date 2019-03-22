from picamera import PiCamera
from time import sleep
from threading import Timer, Thread, Event
import threading
from datetime import datetime

camera = PiCamera()
camera.rotation = 0
camera.resolution = (1920, 1080)
camera.framerate = 5
camera.brightness = 50

sleep(2)
for i in range(30):
     camera.capture('image{0:04d}.jpg'.format(i))





