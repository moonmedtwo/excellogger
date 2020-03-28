import serial.tools.list_ports
import time, threading, datetime

CONNECTED = False
PORT_CHECKING_INTERVAL  = 0.5

import datetime, threading, time

def checkingPortThread():
    global CONNECTED, PORT_CHECKING_INTERVAL

    next_call = time.time()
    while CONNECTED == False:
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if(p.pid == 5889):
                CONNECTED = True

        print(datetime.datetime.now())
        next_call = next_call + PORT_CHECKING_INTERVAL
        time.sleep(next_call - time.time())

def comm_thread():
    timerThread = threading.Thread(target=checkingPortThread)
    timerThread.start()

    while(CONNECTED == False):
        print('Connecting ...')
        time.sleep(1)
    
    print('Connected')


comm_thread()