"""
Author: Talha Alvi
Capstone Project 2019
"""
import os
#os.environ['PYQTGRAPH_QT_LIB'] = 'PySide'
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process, Manager, Queue
from time import sleep


"""
Function: display()
Parameters:
    accel - queue containing raw acceleration values to be plotted
    iri - queue containing roughness index values to be plotted
Return type: None
Requirements: Requires roughness index to have been computed and put into the queue before being called
Description: Uses pyqtgraph and QT graphics framework to create a live plot. In a while loop the update function is
             called which constantly takes the acceleration and roughness values being put into the queue and plots them
             on the graph.
"""

def display(accel, iri):

    app2 = QtGui.QApplication([])
    pg.setConfigOption('background', 'w')
    view = pg.GraphicsView()
    layout = pg.GraphicsLayout()
    win2 = pg.GraphicsWindow(title="Basic plotting examples")
#    win2.resize(1000,600)
#    win2.setWindowTitle('pyqtgraph example: Plotting')
    p2 = win2.addPlot(row=1, col=1, title="Acceleration Mov Avg")
    p3 = win2.addPlot(row=2, col=1, title='Roughness Index')
    #p2.setRange()
    curves = [[] for x in range(5)]
    curves[0] = p2.plot(pen='r')
    curves[1] = p2.plot(pen='b')
    curves[2] = p2.plot(pen='c')
    curves[3] = p3.plot(pen='b')
    data = [[] for x in range(5)]
    len = [[] for x in range(2)]
    global c_accel
    global c_iri
    while True:
        update(curves, accel, data, len, iri)
        if c_accel > 4000:
            p2.clear()
            p3.clear()
            p4.clear()
            curves[0] = p2.plot(pen='r')
            curves[1] = p2.plot(pen='b')
            curves[2] = p2.plot(pen='c')
            curves[3] = p3.plot(pen='b')
            data = [[] for x in range(5)]
            len = [[] for x in range(2)]
            c_accel = 0
            c_iri = 0
            QtGui.QApplication.processEvents()

c_accel = 0
c_iri = 0

"""
Function: update()
Parameters:
    curves - List containing the various curves to be plotted on the live graph
    accel - Queue of raw acceleration values
    data - empty list used to put the data into for plotting
    len - empty list used to track the length of data being plotted
    iri - Queue pf roughness index values to be plotted
Return type: None
Requirements: Must be called inside a while loop to continously plot data
Description: Checks if queues aren't empty, and if they aren't it gets the data in the queue for both acceleration and roughness
             which is them appended to the empty list, which is then added to the curve using curves[x].setData() function. The
             information is then process in the for loop allowing the plot to update in real time
"""
def update(curves , accel, data, len, iri):
        global c_accel
        global c_iri
        if accel.qsize() > 1:
            for x in range(50):
                c_accel += 1
                item = accel.get()
                data[0].append(item[0])
                data[1].append(item[1])
                data[2].append(item[2])
                len[0].append(c_accel)
            curves[0].setData(len[0], data[0])
            curves[1].setData(len[0], data[1])
            curves[2].setData(len[0], data[2])
            QtGui.QApplication.processEvents()

        if iri.qsize() > 1:
            roughness = iri.get()
            for x in range(40):
                c_iri += 1
                len[1].append(c_iri)
                data[3].append(roughness[x])
            curves[3].setData(len[1], data[3])
            QtGui.QApplication.processEvents()
