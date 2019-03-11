from multiprocessing import Process, Queue
import multiprocessing
from time import sleep
import time
import data_collect
import data_parse



queue = Queue()
status = Queue()
process_queue = Queue()
data_collect.start_collection(queue, status, process_queue)

proc_parse = Process(target=data_parse.extract_queue, args=(queue, status,))
proc_parse.start()


start_time = time.time()
while True:
    elapsed_time = time.time() - start_time
    if (not status.empty()):
        msg = status.get()
        print(msg)
        print(queue.qsize())
        if msg == "Processes Exited":
            quit()
        
    #if (not queue.empty()):
     #   print(queue.get())
      #  print(elapsed_time)
        
   # print(elapsed_time)
    #sleep(0.1)
    if (elapsed_time > 60.0 and elapsed_time < 60.005):
        data_collect.finish_collection(status)
        proc_parse.terminate()
        proc_parse.join()
        status.put("Processes Exited")


        

