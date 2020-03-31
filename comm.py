import serial.tools.list_ports
import time, threading, datetime
import serial
import re

CONNECTED = False
PORT_CHECKING_INTERVAL  = 0.1

import datetime, threading, time

PORTS = []
TIMEOUT = 0.1

def doRead(ser,term, tout):
    matcher = re.compile(term)    #gives you the ability to search for anything
    tic     = time.time()
    buff    = ser.read(1)
    # you can use if not ('\n' in buff) too if you don't like re
    while ((time.time() - tic) < tout) and (not matcher.search(buff.decode('utf-8'))): 
        ch = ser.read(1)
        if(len(ch) != 0): 
            tic = time.time()
        buff += ch
    return buff 

def checkingPortThread():
    global CONNECTED, PORT_CHECKING_INTERVAL

    next_call = time.time()
    while CONNECTED == False:
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if(p.pid == 5889):
                CONNECTED = True
                PORTS.append(p)

        # print(datetime.datetime.now())
        next_call = next_call + PORT_CHECKING_INTERVAL
        
        curTime = time.time()
        if(next_call < curTime):
            time.sleep(PORT_CHECKING_INTERVAL)
        else:
            time.sleep(next_call - curTime)

def comm_thread(barrier):
    from interthread import InterthreadData, DataQueue
    timerThread = threading.Thread(target=checkingPortThread)
    timerThread.start()

    i = 1
    while(CONNECTED == False):
        print('Connecting ' + '.' * i)
        if(i > 5):
            i = 1
        else:
            i += 1
        time.sleep(PORT_CHECKING_INTERVAL * 10)
    
    print('Connected')

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port=PORTS[-1].device,
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS,
        timeout = TIMEOUT
    )
    ser.isOpen()
    barrier.wait()
    while(True):
        line = doRead(ser, '\n', TIMEOUT * 3)
        if(len(line)):
            data = InterthreadData(line, time.time())
            DataQueue.put(data)
            #TODO: handle when hardware is disconnected

def comm_thread_test(barrier):
    from interthread import InterthreadData, DataQueue
    print('Connected')
    attempt = 0
    n = 0
    barrier.wait()
    while(True):
        line = f'FakeIWCode-{attempt}'
        line = line.encode('utf-8')
        data = InterthreadData(line, time.time())
        DataQueue.put(data)
        n += 1
        if(n > 5):
            n = 0
            attempt += 1
        time.sleep(1)
