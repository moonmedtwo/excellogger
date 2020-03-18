import pandas as pd
from db_classes import LogData, TEXT_1ST_COL, TEXT_2ND_COL
from openpyxl import Workbook
from openpyxl import load_workbook
import random

FILE = 'Book1.xlsx'

def ReadFile(file):
    df = pd.read_excel(file)
    return df

def CreateNew(file):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append([TEXT_1ST_COL, TEXT_2ND_COL])
    workbook.save(filename=file)
    return workbook

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

def EditFile(file, cell, value):
    workbook = load_workbook(filename=file)
    sheet = workbook.active
    sheet[cell] = value
    workbook.save(filename=file)

tf ='test.xlsx'
textList = ['test1', 'test2']
AppendFile(tf,textList)