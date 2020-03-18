from dataclasses import dataclass

TEXT_1ST_ROW_1ST_COL = 'Inward code'
TEXT_1ST_ROW_2ND_COL = 'Name + Time'

IWCODE = 0
LOGSTRING = 1
# how the data is formatted:
# mr.A 1:00, mr.A 1:01, mr.B 1:02
# mr.A 1:00, mr.B 1:02
# mr.A 1:00, 1:01, mr.B 1.02
@dataclass
class LogData:
    name: str
    loggedTime: str