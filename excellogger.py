import pandas as pd
from db_classes import IWCODE, LOGSTRING, TEXT_1ST_ROW_1ST_COL, TEXT_1ST_ROW_2ND_COL
from openpyxl import Workbook
from openpyxl import load_workbook
import random

FILE = 'Book1.xlsx'

def ReadFile(file):
    df = pd.read_excel(file)
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
    sheet = workbook.active
    isKeyDuplicated = False
    for row in sheet.values:
        if(row[0] == TEXT_1ST_ROW_1ST_COL):
            continue

        if(row[IWCODE] in datadict):
            isKeyDuplicated = True
            #TODO: log error

        datadict[row[IWCODE]] = row[LOGSTRING]

    return datadict, isKeyDuplicated

def AppendFile(file, textList):
    try:
        workbook = load_workbook(filename=file)
    except Exception as e:
        if(isinstance(e,FileNotFoundError)):
            print("File not existed, new one will be created")
            workbook = CreateNew(file)
        else:
            print(f'{e} ------> exitting')
            return

    sheet = workbook.active
    sheet.append(textList)
    workbook.save(filename=file)

def CreateNew(file):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append([TEXT_1ST_ROW_1ST_COL, TEXT_1ST_ROW_2ND_COL])
    workbook.save(filename=file)
    return workbook

def EditFile(file, cell, value):
    workbook = load_workbook(filename=file)
    sheet = workbook.active
    sheet[cell] = value
    workbook.save(filename=file)

tf ='test.xlsx'
textList = ['test1', 'test2']