import os, time
LOCKFILE = r'.mutex.locked'

RETRY_INTERVAL = 0.1

def TryLockAccess(timeout = 0):
    try:
        lock = open(LOCKFILE, 'x')
        return lock
    except IOError:
        None

    start = time.time()
    retries = 0
    while (time.time() - start < timeout):
        try:
            lock = open(LOCKFILE, 'x')
            return lock
        except IOError:
            retries += 1
            print(f'File is locked, waiting and retry#{retries} in {RETRY_INTERVAL}')
            time.sleep(RETRY_INTERVAL)

    return None 

def UnlockAccess(lock):
    lock.close()
    os.remove(LOCKFILE)