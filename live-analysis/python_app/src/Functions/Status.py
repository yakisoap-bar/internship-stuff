from API.RSA_API import *
from ctypes import *
from Functions.Collect import err_check, rsa
from time import sleep

# rsa = cdll.LoadLibrary('./API/win/RSA_API.dll')

def getBatteryStatus():
    '''
    Returns a dictionary containing the plugged-in Spectrum Analyser's battery status.

    `plugged_in` : Whether the SA is plugged in
    `batt_present` :Whether the SA contains a battery
    `charge` : The battery charge level of the SA
    `overtemp` : Whether the SA battery is above 45 deg C
    `batt_hwerror` : Whether an error was detected in the battery hardware of the SA
    '''
    # define struct
    pInfo = POWER_INFO()

    # get power info from SA
    sleep(1)
    err_check(rsa.POWER_GetStatus(byref(pInfo)))

    output = {
        'plugged_in' : pInfo.externalPowerPresent,
        'batt_present' : pInfo.batteryPresent,
        'charge' : pInfo.batteryChargeLevel,
        'overtemp' : pInfo.batteryOverTemperature,
        'batt_hwerror' : pInfo.batteryHardwareError
    }

    return output

def rebootDevice(id):
    err_check(rsa.DEVICE_Reset(c_int(id)))