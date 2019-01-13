from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180
camera.resolution = (1920, 1080)
camera.framerate = 5
camera.brightness = 50

sleep(2)
for i in range(30):
    camera.capture('image{0:04d}.jpg'.format(i))