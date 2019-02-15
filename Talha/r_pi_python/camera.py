from picamera import PiCamera
from time import sleep
from threading import Timer, Thread, Event
import threading
from datetime import datetime

camera = PiCamera()
camera.rotation = 180
camera.resolution = (1920, 1080)
camera.framerate = 5
camera.brightness = 50

#sleep(2)
#for i in range(30):
#     camera.capture('image{0:04d}.jpg'.format(i))


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
    print(count)

count = 0
thread = RepeatEvery(3, camera_capture)
print("starting")
thread.start()




