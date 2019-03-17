from multiprocessing import Process, Queue
import multiprocessing
from time import sleep
import time
import data_collect
import data_parse
import plot



data_queue = Queue()
status_queue = Queue()
accel = Queue()
car_speed = Queue()
iri = Queue()

data_collect.start_collection(data_queue, status_queue, car_speed)

graph = Process(target=plot.display, args=(accel, iri))
# graph.start()

proc_parse = Process(target=data_parse.extract_queue, args=(data_queue, status_queue, accel, car_speed, iri))
proc_parse.start()

start_time = time.time()
while True:
    elapsed_time = time.time() - start_time
    if (not status_queue.empty()):
        msg = status_queue.get()
        print(msg[1])
        if msg[0] == 0:
            data_collect.finish_collection()
            proc_parse.terminate()
            proc_parse.join()
            graph.terminate()
            graph.join()
            quit()

   # if (not queue.empty()):
      #  print(queue.get())
      #  print(elapsed_time)

   # print(elapsed_time)
    #sleep(0.1)
    if (elapsed_time > 180.0 and elapsed_time < 180.05):
        data_collect.finish_collection()
        proc_parse.terminate()
        proc_parse.join()
        #pg.QtGui.QApplication.exec_()
        graph.terminate()
        graph.join()
        status.put("Processes Exited")
