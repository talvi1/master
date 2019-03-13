# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore

import numpy as np

import pyqtgraph as pg

from multiprocessing import Process, Manager, Queue

import sched, time, threading




# Displaying the data
def display(name,q):

    app2 = QtGui.QApplication([])
    win2 = pg.GraphicsWindow(title="Basic plotting examples")
    win2.resize(1000,600)
    win2.setWindowTitle('pyqtgraph example: Plotting')
    p2 = win2.addPlot(title="Updating plot")
    curve = p2.plot(pen='y')

    x_np = []
    y_np = []

# Setting timer and appending input data
def updateInProc(curve,q,x,y):

    item = q.get()
    x.append(item[0])
    y.append(item[1])
    curve.setData(x,y)
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: updateInProc(curve,q,x_np,y_np))
    timer.start(50)

    QtGui.QApplication.instance().exec_()

# Reading data and displaying in a thread
def io(running,q):

    t = 0
    while running.is_set():
    s = np.sin(2 * np.pi * t)
    t += 0.01
    q.put([t,s])
    time.sleep(0.01)
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
