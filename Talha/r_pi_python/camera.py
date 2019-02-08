# from picamera import PiCamera
# from time import sleep
#
# camera = PiCamera()
# camera.rotation = 180
# camera.resolution = (1920, 1080)
# camera.framerate = 5
# camera.brightness = 50
#
# sleep(2)
# for i in range(30):
#     camera.capture('image{0:04d}.jpg'.format(i))

from threading import Timer, Thread, Event
import threading
from datetime import datetime

class PT():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

def printer():
    tempo = datetime.today()
    h,m,s = tempo.hour, tempo.minute, tempo.second
    print(f"{h}:{m}:{s}")
    print(threading.active_count())


t = PT(1, printer).start()
