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
def display(name, accel_0, accel_1, accel_2, iri):

    app2 = QtGui.QApplication([])
    pg.setConfigOption('background', 'w')
    view = pg.GraphicsView()
    layout = pg.GraphicsLayout()
    win2 = pg.GraphicsWindow(title="Basic plotting examples")
#    win2.resize(1000,600)
#    win2.setWindowTitle('pyqtgraph example: Plotting')
    p2 = win2.addPlot(row=1, col=1, title="Acceleration Mov Avg")
    p3 = win2.addPlot(row=2, col=1, title='IRI Right')
    p4 = win2.addPlot(row=3, col=1, title='IRI Left')
    #p2.setRange()
    curves = [[] for x in range(5)]
    curves[0] = p2.plot(pen='r')
    curves[1] = p2.plot(pen='b')
    curves[2] = p2.plot(pen='c')
    curves[3] = p3.plot(pen='b')
    curves[4] = p4.plot(pen='r')

    Xm = [[] for x in range(5)]
    len = []
    clen = []
    global counts
    global c
    while True:
        update(curves, accel_0, accel_1, accel_2, Xm, len, clen, iri)
        if counts > 4000:
            p2.clear()
            p3.clear()
            p4.clear()
            curves[0] = p2.plot(pen='r')
            curves[1] = p2.plot(pen='b')
            curves[2] = p2.plot(pen='c')
            curves[3] = p3.plot(pen='b')
            curves[4] = p4.plot(pen='r')
            Xm = [[] for x in range(5)]
            len = []

            clen = []
            counts = 0
            c = 0
            QtGui.QApplication.processEvents()
        #pg.QtGui.QApplication.exec_()

# Setting timer and appending input data
counts = 0
c = 0
def update(curves , accel_0, accel_1, accel_2, Xm, len, clen, iri):
        global counts
        global c
        if accel_0.qsize() > 50 and accel_1.qsize() > 50:
            for x in range(50):
                counts += 1
                item = accel_0.get()
                item1 = accel_1.get()
                item2 = accel_2.get()
                Xm[0].append(item)
                Xm[1].append(item1)
                Xm[2].append(item2)
                len.append(counts)
            curves[0].setData(len, Xm[0])
            curves[1].setData(len, Xm[1])
            curves[2].setData(len, Xm[2])
            QtGui.QApplication.processEvents()
        if iri.qsize() > 5:
            for x in range(5):
                c += 1
                item3 = iri.get()
                clen.append(c)
                Xm[3].append(item3[0])
                Xm[4].append(item3[1])
            curves[3].setData(clen, Xm[3])
            curves[4].setData(clen, Xm[4])
            QtGui.QApplication.processEvents()

            # if counts > 100000:
            #     len = []
            #     Xm0 = []
            #     Xm1 = []
            #     Xm2 = []
            #     counts = 0


        #print(accel_0.qsize())

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
