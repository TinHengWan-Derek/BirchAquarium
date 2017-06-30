import sys
import numpy
import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#CONST
MAX_A = 8
MIN_A = 0
WAVE_BALL = 1

#WINDOW_SIZE
SIZE_X = 10
SIZE_Y = 5
SIZE_Z = MAX_A+2
INIT_HEIGHT = SIZE_Z/2

#Color
COLOR = 'blue'

#global variable
exit = False
delay = 10
amplitude = 1
ball_size = 1

plt.ion()

def initializeWorld():
    world = numpy.zeros((SIZE_X,SIZE_Y,SIZE_Z))
    #initializing wave ball
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            world[x][y][INIT_HEIGHT] = WAVE_BALL
    return world

def initializemMyPlt():
    fig = plt.figure()
    fig.canvas.mpl_connect('key_press_event', press)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, SIZE_X-1)
    ax.set_ylim(0, SIZE_Y-1)
    ax.set_zlim(0, SIZE_Z-1)
    ax.set_autoscale_on(False)
    return plt,ax

def displayWorld(world):
    x,y,z = world.nonzero()
    locationX = []
    locationY = []
    locationZ = []
    plt,ax = initializemMyPlt()

    for i in range(0,len(x)):
        if world[x[i]][y[i]][z[i]] == WAVE_BALL:
            locationX.append(x[i])
            locationY.append(y[i])
            locationZ.append(z[i])

    fig = ax.scatter(locationX, locationY, locationZ, zdir='z', c=COLOR, s=ball_size*200)
    plt.draw()
    plt.pause(delay/100.0)
    return plt,ax,fig

def updateWorld(world,plt,ax,fig):
    x,y,z = world.nonzero()
    locationX = []
    locationY = []
    locationZ = []
    for i in range(0,len(x)):
        if world[x[i]][y[i]][z[i]] == WAVE_BALL:
            locationX.append(x[i])
            locationY.append(y[i])
            locationZ.append(z[i])

    fig.remove()
    fig = ax.scatter(locationX, locationY, locationZ, zdir='z', c=COLOR, s=ball_size*200)
    plt.draw()
    plt.pause(delay/100.0)
    return plt,ax,fig

def moveUP(row,world,step,z):
    before = z[row]
    after = z[row]+step
    for y in range(SIZE_Y):
        world[row][y][before] = 0
        world[row][y][after] = WAVE_BALL
    z[row] = after

def moveDown(row,world,step,z):
    before = z[row]
    after = z[row]-step
    for y in range(SIZE_Y):
        world[row][y][before] = 0
        world[row][y][after] = WAVE_BALL
    z[row] = after

def moveTo(row,world,location,z):
    before = z[row]
    after = location
    for y in range(SIZE_Y):
        world[row][y][before] = 0
        world[row][y][after] = WAVE_BALL
    z[row] = after

def followRowBefore(world,z):
    # x = 0 is the master row
    # follow the height
    # row1 follow row0,row2 follow row3, ..., row8 follow row9
    temp = z[:]
    for row in range(1,SIZE_X):
        moveTo(row,world,temp[row-1],z)

def press(event):
    global delay
    global exit
    global amplitude
    global ball_size
    print('press', event.key)
    if event.key == ' ':
        exit = True
    if event.key == '=':
        ball_size += 1
    if event.key == '-':
        ball_size -= 1
    if event.key == 'right':
        delay -= 1
    if event.key == 'left':
        delay += 1
    if event.key == 'up':
        if(amplitude+1<MAX_A):
            amplitude += 1
    if event.key == 'down':
        if(amplitude-1>MIN_A):
            amplitude -= 1
    sys.stdout.flush()

def main():
    global amplitude
    z = [INIT_HEIGHT]*SIZE_X
    world = initializeWorld()
    plt,ax,fig = displayWorld(world)

    try:
        while not exit:
            currentAmp = amplitude
            for x in range(0,currentAmp):
                moveUP(0,world,1,z)
                plt,ax,fig = updateWorld(world,plt,ax,fig)
                followRowBefore(world,z)
                plt,ax,fig = updateWorld(world,plt,ax,fig)
            for x in range(0,currentAmp*2):
                moveDown(0,world,1,z)
                plt,ax,fig = updateWorld(world,plt,ax,fig)
                followRowBefore(world,z)
                plt,ax,fig = updateWorld(world,plt,ax,fig)
            for x in range(0,currentAmp):
                moveUP(0,world,1,z)
                plt,ax,fig = updateWorld(world,plt,ax,fig)
                followRowBefore(world,z)
                plt,ax,fig = updateWorld(world,plt,ax,fig)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
