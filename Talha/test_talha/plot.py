# -*- coding: utf-8 -*-

import os
#os.environ['PYQTGRAPH_QT_LIB'] = 'PySide'
from pyqtgraph.Qt import QtGui, QtCore

import numpy as np

import pyqtgraph as pg

from multiprocessing import Process, Manager, Queue

import sched, time, threading
from time import sleep




# Displaying the data
def display(name, accel_0, accel_1, accel_2):

    app2 = QtGui.QApplication([])
    pg.setConfigOption('background', 'w')
    view = pg.GraphicsView()
    layout = pg.GraphicsLayout()
    win2 = pg.GraphicsWindow(title="Basic plotting examples")
#    win2.resize(1000,600)
#    win2.setWindowTitle('pyqtgraph example: Plotting')
    p2 = win2.addPlot(row=1, col=1, title="Unfiltered")
    p3 = win2.addPlot(row=2, col=1, title='Moving Average')
    #p2.setRange()
    curve0 = p2.plot(pen='r')
    curve1 = p2.plot(pen='b')
    curve2 = p3.plot(pen='b')
    Xm0 = []
    len = []
    Xm1 = []
    Xm2 = []
    clen = []
    global counts
    global c
    while True:
        update(curve0, curve1, curve2, accel_0, accel_1, accel_2, Xm0, Xm1, Xm2, len, clen)
        if counts > 5000:
            p2.clear()
            p3.clear()
            curve0 = p2.plot(pen='r')
            curve1 = p2.plot(pen='b')
            curve2 = p3.plot(pen='b')
            Xm0 = []
            len = []
            Xm1 = []
            Xm2 = []
            clen = []
            counts = 0
            c = 0
            QtGui.QApplication.processEvents()
        #pg.QtGui.QApplication.exec_()

# Setting timer and appending input data
counts = 0
c = 0
def update(curve0, curve1, curve2 , accel_0, accel_1, accel_2, Xm0, Xm1, Xm2, len, clen):
        global counts
        global c


        if accel_0.qsize() > 30 and accel_1.qsize() > 30:
            for x in range(25):
                counts += 1
                item = accel_0.get()
                item1 = accel_1.get()

                Xm0.append(item)
                Xm1.append(item1)
                len.append(counts)
            curve0.setData(len, Xm0)
            curve1.setData(len, Xm1)
            QtGui.QApplication.processEvents()
        if accel_2.qsize() > 3:
            for x in range(3):
                c += 1
                item2 = accel_2.get()
                clen.append(c)
                Xm2.append(item2)
            curve2.setData(clen, Xm2)
            QtGui.QApplication.processEvents()

            # if counts > 100000:
            #     len = []
            #     Xm0 = []
            #     Xm1 = []
            #     Xm2 = []
            #     counts = 0


        print(accel_0.qsize())

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