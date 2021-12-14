from API.RSA_API import *
from ctypes import *
from Functions.Collect import err_check

rsa = cdll.LoadLibrary('./API/win/RSA_API.dll')

def getBatteryStatus():
    # define struct
    power_info = POWER_INFO()

    # get power info from SA
    err_check(rsa.POWER_GetStatus(byref(power_info)))

    return power_info

def rebootDevice(id):
    err_check(rsa.DEVICE_Reset(c_int(id)))