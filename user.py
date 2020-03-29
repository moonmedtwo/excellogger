import win32api
import win32net

import time
import os

class UserInfo:
    username = ''
    def __init__(self, username=''):
        if(len(username) == 0):
            # try:
            #     user_info = win32net.NetUserGetInfo(win32net.NetGetAnyDCName(), win32api.GetUserName(), 2)
            #     self.username = user_info["full_name"]
            # except Exception:
            self.username = os.getenv("USERNAME")
        print(f'{self.username} is being used')

    def GetUserName(self):
        ret = self.username
        return ret