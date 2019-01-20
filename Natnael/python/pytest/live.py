import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial
import numpy as np
import srAcc


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
plt.yticks(np.arange(-5, 5+1, 1.0))
ax1.set_xlim([0,100])
ax1.set_ylim([-5,5])



def animate(i):

    


    

    pullData = open("bump.txt","r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.set_xlim([0,100])
    ax1.set_ylim([-6,6])
    plt.yticks(np.arange(-5, 5+1, 1.0))
    ax1.plot(xar,yar)



ani = animation.FuncAnimation(fig, animate, interval=1)

plt.show()
