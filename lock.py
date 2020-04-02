import os, time


class SimpleLock:
    EXTENSION = r'.mutex.locked'
    RETRY_INTERVAL = 0.1

    def __init__(self, filepath):
        folder = os.path.dirname(filepath)
        file = os.path.basename(filepath)
        self.lockpath = fr'{folder}\{self.EXTENSION}{file}'
        self.__lock = None

    def TryLockAccess(self, timeout = 0):
        try:
            self.__lock = open(self.lockpath, 'x')
            return True
        except IOError:
            None

        start = time.time()
        retries = 0
        while (time.time() - start < timeout):
            try:
                self.__lock = open(self.lockpath, 'x')
                return True
            except IOError:
                retries += 1
                print(f'File is locked, waiting and retry#{retries} in {self.RETRY_INTERVAL}')
                time.sleep(self.RETRY_INTERVAL)

        return  False

    def UnlockAccess(self):
        self.__lock.close()
        os.remove(self.lockpath)