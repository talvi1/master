from multiprocessing import Process, Queue
import multiprocessing
from time import sleep
import time

def f(x):
    start_time = time.time()
    count = 0
    while True:
        elapsed_time = time.time() - start_time
        count = count + 1
        x.put(count)
        sleep(0.02)

def j(local, status):

    while True:
        list = []
        if (local.qsize() >= 50):
            for x in range(50):
                list.append(local.get())
            print(list)
            sleep(3)
def z(glob, local):
    while True:
        local.put(glob.get())
        print(glob.qsize())
        print(local.qsize())

queue = Queue()
local = Queue()
status = Queue()
proc1 = Process(target=f, args=(queue,))
proc2 = Process(target=z, args=(queue,local))
proc3 = Process(target=j, args=(local, status,))
proc1.start()
proc2.start()
proc3.start()
while True:
    #print(queue.qsize())
    if (status.get() == 'Finished'):
        proc1.join()
        proc2.join()
        proc3.join()
    sleep(0.01)
