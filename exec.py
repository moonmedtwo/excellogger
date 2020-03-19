
import pandas as pd
from db_classes import IWCODE, LOGSTRING
from excellogger import ParseFileAndCheckDuplicated, RefactorWorkbook, ReadFile
import random, math
from datetime import datetime

IWCODELIST = ['12378','123162','21321','26452','953251']
USERLIST = ['avu', 'bce', 'def', 'tof', 'iphone']
tf ='demo.xlsx'

def LogEntry():
    code = IWCODELIST[int(math.floor(random.uniform(0,len(IWCODELIST))))]
    user = USERLIST[int(math.floor(random.uniform(0,len(USERLIST))))]
    print(f'{code}, {user}')
    datadict, isDuplicated, workbook = ParseFileAndCheckDuplicated(tf)

    if(isDuplicated):
        RefactorWorkbook(workbook,datadict, tf)

    datalist = list(datadict.items())
    sheet = workbook.active
    for i in range(0, len(datalist)):
        if code == datalist[i][IWCODE]:
           tmp = datalist[i][LOGSTRING]
           time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
           tmp = f'{tmp}, {user}---{time}'
           cell = f'B{i+2}'
           print(f'Editting cell[{cell}] with {tmp}')
           sheet[cell] = tmp
           workbook.save(tf)
           return

    sheet.append([code, user])
    workbook.save(tf)
    return

if __name__ == '__main__':
    for i in range(0,10):
        LogEntry()