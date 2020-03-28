
import pandas as pd
from excellogger import Log, ParseFileAndCheckDuplicated, ReadFile
import random, math
from lock import TryLockAccess, UnlockAccess, LOCKFILE
import sys
import os
from comm import comm_thread
import time, threading, datetime

IWCODELIST = ['1','2','3','4','5', '6', '7' , '8' , '9' , '0']
USERLIST = ['avu', 'bce', 'def', 'tof', 'iphone']
tf ='demo.xlsx'
        
def LogEntry():
    code = IWCODELIST[int(math.floor(random.uniform(0,len(IWCODELIST))))]
    user = USERLIST[int(math.floor(random.uniform(0,len(USERLIST))))]
    print(f'{code}, {user}')
    datadict, isDuplicated, workbook = ParseFileAndCheckDuplicated(tf)

    if(isDuplicated): 
        raise('There is duplicate entry of IWCODE. Please remove the file or the entry')

    datalist = list(datadict.items())

    Log(tf, workbook, code, user, datalist)

    return

def LogNewEntry(user, code, file):
    lock = TryLockAccess()
    if(lock != None):
        try:
            print(f'{code}, {user}')
            datadict, isDuplicated, workbook = ParseFileAndCheckDuplicated(tf)

            if(isDuplicated): 
                raise('There is duplicate entry of IWCODE. Please remove the file or the entry')

            datalist = list(datadict.items())
            Log(tf, workbook, code, user, datalist)
        finally:
            UnlockAccess(lock)
    else:
        print(f'Cannot create lock file. Please try to manually remove {LOCKFILE}')


def logging_thread(barrier):
    filepath = 'filetosave.txt'
    try:    
        file = open(filepath, 'r') 
    except Exception as e:
        print('cannot open file')
        exit()

    Lines = file.readlines() 
    tf = Lines[0]

    outFPath = os.path.dirname(tf)
    os.chdir(outFPath)

    barrier.wait()
    while(True):
        print('logging thread')
        time.sleep(3)

NBR_OF_THREAD = 2
barrier = threading.Barrier(2)
if __name__ == '__main__':
    commThread = threading.Thread(target=comm_thread, args=(barrier,))
    loggingThread = threading.Thread(target=logging_thread, args=(barrier,))

    commThread.start()
    loggingThread.start()
