import pandas as pd
from db_classes import *
from openpyxl import Workbook
from openpyxl import load_workbook
import random, math
from datetime import datetime


SHEET_NAME = "Log Datasheet"
def GetLogDataSheet(file, wb):
    try:
        ws = wb[SHEET_NAME]
    except KeyError:
        print(f'No existed sheet. Creating new one as {SHEET_NAME}')
        ws = wb.create_sheet(SHEET_NAME)
        ws.append([TEXT_1ST_ROW_1ST_COL, TEXT_1ST_ROW_2ND_COL])
    finally:
        ws = wb[SHEET_NAME]
    
    wb.save(file)
    return ws

def ReadFile(file):
    df = pd.read_excel(file, sheet_name = SHEET_NAME)
    return df

def ParseFileAndCheckDuplicated(file):
    try:
        workbook = load_workbook(filename=file)
    except Exception as e:
        if(isinstance(e,FileNotFoundError)):
            print("File not existed, new one will be created")
            workbook = CreateNew(file)
        else:
            print(f'{e} ------> exitting')
            return

    datadict = {}
    sheet = GetLogDataSheet(file,workbook)
    isKeyDuplicated = False
    for row in sheet.values:
        if(row[0] == TEXT_1ST_ROW_1ST_COL):
            continue

        if(row[IWCODE_IDX] in datadict):
            isKeyDuplicated = True
            #TODO: log error

        datadict[row[IWCODE_IDX]] = row[DATA_IDX]
        col = DATA_IDX + 1
        while(col < len(row) and row[col] != None):
            datadict[row[IWCODE_IDX]] += f',{row[col]}'
            col += 1

    return datadict, isKeyDuplicated, workbook

def FindBlankCellByRow(ws, row):
    col = 1
    while(ws.cell(row = row, column = col).value != None):
        col = col + 1

    return row, col

def Log(file, wb, code, user, datalist):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ws = GetLogDataSheet(file, wb)
    FoundExisting = False
    for i in range(0, len(datalist)):
        if code == datalist[i][IWCODE_IDX]:
            row, userCol = FindBlankCellByRow(ws, i+2)
            FoundExisting = True
            break

    if(FoundExisting):
        timeCol = userCol + 1 
    else:
        row = len(datalist) + 2
        codeCol = IWCODE_COL
        ws.cell(row,codeCol).value = code

        userCol = USER_COL
        timeCol = TIME_COL

    ws.cell(row,userCol).value = user
    ws.cell(row,timeCol).value = time
    print(f'Wrote {user} to [{row}][{userCol}] and {time} to [{row}][{timeCol}]')
    wb.save(file)

def CreateNew(file):
    workbook = Workbook()
    sheet = GetLogDataSheet(file,workbook)
    workbook.save(filename=file)
    return workbook
