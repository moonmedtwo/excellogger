
import pandas as pd
from excellogger import Log, ParseFileAndCheckDuplicated, ReadFile
import random, math
from lock import TryLockAccess, UnlockAccess, LOCKFILE
import sys
import os

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

if __name__ == '__main__':
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
    # lock here
    lock = TryLockAccess()
    if(lock != None):
        try:
            for i in range(0,20):
                LogEntry()
            print(ReadFile(tf))
        finally:
            # unlock here
            UnlockAccess(lock)
    else:
        print(f'Cannot create lock file. Please try to manually remove {LOCKFILE}')
