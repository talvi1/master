from multiprocessing import Process, Queue
import multiprocessing
from time import sleep
import time
import data_collect
import data_parse
import plot



queue = Queue()
status = Queue()
accel_0 = Queue()
accel_1 = Queue()
accel_2 = Queue()

process_queue = Queue()
data_collect.start_collection(queue, status, process_queue)



graph = Process(target=plot.display, args=('bob',accel_0, accel_1, accel_2))
graph.start()
#sleep(10)
proc_parse = Process(target=data_parse.extract_queue, args=(queue, status, accel_0, accel_1, accel_2))
proc_parse.start()
#for x in range(10000):
   # graph_queue.put([x, 1])
start_time = time.time()
while True:
    elapsed_time = time.time() - start_time
    if (not status.empty()):
        msg = status.get()
        print(msg)
        print(queue.qsize())
        if msg == "Processes Exited":
            quit()

   # if (not queue.empty()):
      # print(queue.get())
      #  print(elapsed_time)

   # print(elapsed_time)
    #sleep(0.1)
    if (elapsed_time > 60.0 and elapsed_time < 60.05):
        data_collect.finish_collection(status)
        proc_parse.terminate()
        proc_parse.join()
        graph.terminate()
        graph.join()
        status.put("Processes Exited")
