# -*- coding: utf-8 -*-

import os
os.environ['PYQTGRAPH_QT_LIB'] = 'PySide'
from pyqtgraph.Qt import QtGui, QtCore

import numpy as np

import pyqtgraph as pg

from multiprocessing import Process, Manager, Queue

import sched, time, threading
from time import sleep




# Displaying the data
def display(name, accel_0, accel_1, accel_2):

    app2 = QtGui.QApplication([])
    win2 = pg.GraphicsWindow(title="Basic plotting examples")
    win2.resize(1000,600)
    win2.setWindowTitle('pyqtgraph example: Plotting')
    p2 = win2.addPlot(title="Updating plot")
    p2.setRange(yRange=[-5, 5])
    curve0 = p2.plot(pen='y')
    curve1 = p2.plot(pen='g')
    curve2 = p2.plot(pen='c')
    Xm0 = np.linspace(0, 0, 100)
    Xm1 = np.linspace(0, 0, 100)
    Xm2 = np.linspace(0, 0, 100)
    count = 0
    while True:
        update(curve0, curve1, curve2, accel_0, accel_1, accel_2, Xm0, Xm1, Xm2, count)
        #pg.QtGui.QApplication.exec_()

# Setting timer and appending input data
def update(curve0, curve1, curve2 , accel_0, accel_1, accel_2, Xm0, Xm1, Xm2, count):   
        #Xm[:-1] = Xm[1:]
        if accel_0.qsize() >= 100:
            for i in range(100):
                Xm0[i] = accel_0.get()
                Xm1[i] = accel_1.get()
                Xm2[i] = accel_2.get()
                count += 1
            curve0.setData(Xm0)
            curve1.setData(Xm1)
            curve2.setData(Xm2)
            curve0.setPos(count, 0)
            curve1.setPos(count, 0)
            curve2.setPos(count, 0)
            QtGui.QApplication.processEvents()
            #print(count)
        #print(Xm)

# Reading data and displaying in a thread
def io(running,q):

    t = 0
    while running.is_set():
        s = np.sin(2 * np.pi * t)
        t += 0.01
        print(s)
        print(t)
        q.put([t,s])
        time.sleep(0.001)
    print("Done")

if __name__ == '__main__':

    q = Queue()
    # Event for stopping the IO thread
    run = threading.Event()
    run.set()
    # Running in thread
    t = threading.Thread(target=io, args=(run,q))
    t.start()
    # Display
    p = Process(target=display, args=('bob',q))
    p.start()
    input("See ? Main process immediately free ! Type any key to quit.")
    run.clear()
    print("Waiting for scheduler to join thread..")
    t.join()
    p.join()
    
    
