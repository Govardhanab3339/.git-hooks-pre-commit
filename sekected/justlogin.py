import pandas as pd
from datetime import datetime, timedelta
from NorenApi import NorenApi
import pyotp

# Initialize API
api = NorenApi()

user_id    = 'FA108224'
user_pwd     = 'Ram39#Kils'
factor2 = pyotp.TOTP('EETL2QPZ63D25PBN4564T6526R34I77Q').now()  # This should be TOTP
vc      = 'FA108224_U'
app_key = 'df41b1771499934e366634c53f19ac3f'
imei    = 'abc1234'
accesstoken = ''


def Shoonya_login():
    #cpass redentials
    ret=api.login(userid=user_id, password=user_pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    return ret['susertoken']

Shoonya_login()