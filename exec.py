
import pandas as pd
from excellogger import Log, ParseFileAndCheckDuplicated, ReadFile
import random, math
from lock import TryLockAccess, UnlockAccess, LOCKFILE
import sys
import os
from comm import comm_thread
import time, threading, datetime
from interthread import *
from user import UserInfo

def LogNewEntry(user, code, file):
    lock = TryLockAccess()
    if(lock != None):
        try:
            print(f'{code}, {user}')
            datadict, isDuplicated, workbook = ParseFileAndCheckDuplicated(file)

            if(isDuplicated): 
                raise('There is duplicate entry of IWCODE. Please remove the file or the entry')

            datalist = list(datadict.items())
            Log(file, workbook, code, user, datalist)
        finally:
            UnlockAccess(lock)
    else:
        print(f'Cannot create lock file. Please try to manually remove {LOCKFILE}')


def logging_thread(barrier):
    filepath = 'filetosave.txt'
    try:    
        file = open(filepath, 'r') 
    except Exception:
        print('Cannot read filetosave.txt.')
        exit()

    Lines = file.readlines() 
    tf = Lines[0]
    print(f"Logged data will be saved into {tf}")

    outFPath = os.path.dirname(tf)
    os.chdir(outFPath)

    userinfo = UserInfo()
    barrier.wait()
    while(True):
        data = DataQueue.get(block=True)        
        data = data.decode('utf8')
        LogNewEntry(userinfo.GetUserName(), data, tf)

NBR_OF_THREAD = 2
barrier = threading.Barrier(2)
if __name__ == '__main__':
    commThread = threading.Thread(target=comm_thread, args=(barrier,), daemon=True)
    loggingThread = threading.Thread(target=logging_thread, args=(barrier,), daemon=True)

    commThread.start()
    loggingThread.start()

    while(True):
        time.sleep(1)
