#!/usr/local/bin/python3
# coding: utf-8
import sys
import curses
import time
import numpy as np

toggle = 0
debug = False
step = False
delay = 0

def main(stdscr):
    global toggle
    global debug
    global step
    global delay
    
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()
    rows = curses.LINES
    cols = curses.COLS
    cells = np.zeros((2, rows + 2, cols + 2))
    
    cross = 1
    gliders = 0

    cells[ toggle, rows//2, cols//2 - cols//4 : cols//2 + cols//4 + 1 ] = cross
    cells[ toggle, rows//2 - rows//4 : rows//2 + rows//4 + 1, cols//2 ] = cross

    #gliders
    for x, y, lr, ud in [ (2,2,1,1), (cols-2,8,-1,1),\
                          (10,rows-2,1,-1), (cols-8, rows-8,-1,-1) ]:
        cells[ toggle, y   , x-lr ] = gliders
        cells[ toggle, y+ud, x    ] = gliders
        cells[ toggle, y-ud, x+lr ] = gliders
        cells[ toggle, y   , x+lr ] = gliders
        cells[ toggle, y+ud, x+lr ] = gliders
        
    def drawScreen():
        for y in range(1, rows):
            for x in range(1, cols):
                if cells[ toggle, y, x ] == 1:
                    stdscr.addch(y-1, x-1, ' ', curses.A_REVERSE)
                else:
                    stdscr.addch(y-1, x-1, ' ', curses.A_NORMAL)

    def wrapAround():
        cells[ toggle, 0, : ] = cells[ toggle, rows-1, : ]
        cells[ toggle, rows, : ] = cells[ toggle, 1, : ]
        cells[ toggle, :, 0 ] = cells[ toggle, :, cols - 1 ]
        cells[ toggle, :, cols ] = cells[ toggle, :, 1 ]

    def updateCells():
        for y in range(1, rows):
            for x in range(1, cols):
                neighbours = np.sum(cells[ toggle, y-1 : y+2, x-1 : x+2 ])
                cell = cells[ toggle, y, x ]
                neighbours = neighbours - cell
                if cell:
                    cells[ 1 - toggle, y, x ] = 1 < neighbours < 4
                else:
                    cells[ 1 - toggle, y ,x ] = neighbours == 3

    def toggleLast():
        global toggle
        try:
            while True:
                try:
                    stdscr.getkey()
                except KeyboardInterrupt:
                    break
                except:
                    pass
                toggle = 1 - toggle
                drawScreen()
        except KeyboardInterrupt:
            pass

    try:
        while True:
            drawScreen()
            stdscr.refresh()
            if step:
                stdscr.getkey()
            elif delay != 0:
                time.sleep(delay)
            wrapAround()
            updateCells()
            toggle = 1 - toggle
    except KeyboardInterrupt:
        if debug: toggleLast() 
        pass

def help():
    print('^C : while running, enters debug mode or exits')
    print('-d : debug - toggles between last two generations on key press')
    print('-h : print this help and exit')
    print('-s : single step between generations with key press')
    print('-t : time in seconds between generations (default 0)')
    exit()
    
argc = 1
while argc < len(sys.argv):
    argv = sys.argv[argc]
    argc += 1
    if argv == '-h': help()
    if argv == '-d': debug = True
    if argv == '-s': step = True
    if argv == '-t':
        if argc < len(sys.argv):
            try:
                delay = float(sys.argv[argc])
            except ValueError:
                delay = 1
            else:
                argc += 1
        else:
            delay = 1
            
curses.wrapper(main)

