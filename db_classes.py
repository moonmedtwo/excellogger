from dataclasses import dataclass

TEXT_1ST_ROW_1ST_COL = 'Inward code'
TEXT_1ST_ROW_2ND_COL = 'Name + Time'

IWCODE_COL = 1
USER_COL = 2
TIME_COL = 3

IWCODE_IDX = 0
DATA_IDX = 1

@dataclass
class LogData:
    name: str
    loggedTime: str