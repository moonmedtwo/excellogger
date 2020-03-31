import queue

DataQueue = queue.Queue()

class InterthreadData:
    bytesdata = ''
    time = 0

    def __init__(self, bytesdata, time):
        self.bytesdata = bytesdata
        self.time = time