"""
Author: Talha Alvi
Capstone Project 2019
Description: Main process that starts all the other processes used for data collection, processing and uploading
"""

from multiprocessing import Process, Queue
import multiprocessing
from time import sleep
import time
import data_collect
import data_parse
import plot
import upload



#Queues used to access data across multiple processing are initialized
data_queue = Queue()
status_queue = Queue()
accel = Queue()
car_speed = Queue()
iri = Queue()



data_collect.start_collection(data_queue, status_queue, car_speed)


graph = Process(target=plot.display, args=(accel, iri))
#graph.start()

proc_parse = Process(target=data_parse.extract_queue, args=(data_queue, status_queue, accel, car_speed, iri))
proc_parse.start()

#Various processes are started to start data collection, create live plot of data and to process the data being collected

start_time = time.time()
#while loop just keeps track of program and if program is terminated, it closes all the processes safely
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

  #  if (not data_queue.empty()):
   #     print(data_queue.get())
    #    print(elapsed_time)

   # print(elapsed_time)
    #sleep(0.1)
    if (elapsed_time > 1000.0 and elapsed_time < 1000.05):
        data_collect.finish_collection()
        upload.close_connection()
        proc_parse.terminate()
        proc_parse.join()
        #pg.QtGui.QApplication.exec_()
        graph.terminate()
        graph.join()
        status.put("Processes Exited")
