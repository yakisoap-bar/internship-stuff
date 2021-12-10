from RSAAPI.RSA_API import *
from ctypes import *

import numpy as np
import matplotlib.pyplot as plt

# load dll
rsa = cdll.LoadLibrary('./RSAAPI/win/RSA_API.dll')

# functions
def err_check(rs):
    if ReturnStatus(rs) != ReturnStatus.noError:
        raise RSAError(ReturnStatus(rs).name)

def search_connect():
    numFound = c_int(0)
    intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
    deviceIDs = intArray()
    deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
    deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)
    apiVersion = create_string_buffer(DEVINFO_MAX_STRLEN)

    rsa.DEVICE_GetAPIVersion(apiVersion)
    print('API Version {}'.format(apiVersion.value.decode()))

    err_check(rsa.DEVICE_Search(byref(numFound), deviceIDs,
                                deviceSerial, deviceType))

    if numFound.value < 1:
        # rsa.DEVICE_Reset(c_int(0))
        print('No instruments found. Exiting script.')
        exit()
    elif numFound.value == 1:
        print('One device found.')
        print('Device type: {}'.format(deviceType.value.decode()))
        print('Device serial number: {}'.format(deviceSerial.value.decode()))
        err_check(rsa.DEVICE_Connect(deviceIDs[0]))
    else:
        # corner case
        print('2 or more instruments found. Enumerating instruments, please wait.')
        for inst in deviceIDs:
            rsa.DEVICE_Connect(inst)
            rsa.DEVICE_GetSerialNumber(deviceSerial)
            rsa.DEVICE_GetNomenclature(deviceType)
            print('Device {}'.format(inst))
            print('Device Type: {}'.format(deviceType.value))
            print('Device serial number: {}'.format(deviceSerial.value))
            rsa.DEVICE_Disconnect()
        # note: the API can only currently access one at a time
        selection = 1024
        while (selection > numFound.value - 1) or (selection < 0):
            selection = int(input('Select device between 0 and {}\n> '.format(numFound.value - 1)))
        err_check(rsa.DEVICE_Connect(deviceIDs[selection]))
    rsa.CONFIG_Preset()

def config_block_iq(cf=1e9, refLevel=0, iqBw=40e6, recordLength=10e3):
    recordLength = int(recordLength)
    rsa.CONFIG_SetCenterFreq(c_double(cf))
    rsa.CONFIG_SetReferenceLevel(c_double(refLevel))

    rsa.IQBLK_SetIQBandwidth(c_double(iqBw))
    rsa.IQBLK_SetIQRecordLength(c_int(recordLength))

    iqSampleRate = c_double(0)
    rsa.IQBLK_GetIQSampleRate(byref(iqSampleRate))
    # Create array of time data for plotting IQ vs time
    time = np.linspace(0, recordLength / iqSampleRate.value, recordLength)
    time1 = []
    step = recordLength / iqSampleRate.value / (recordLength - 1)
    for i in range(recordLength):
        time1.append(i * step)
    return time


def acquire_block_iq(recordLength=10e3):
    recordLength = int(recordLength)
    ready = c_bool(False)
    iqArray = c_float * recordLength
    iData = iqArray()
    qData = iqArray()
    outLength = 0
    rsa.DEVICE_Run()
    rsa.IQBLK_AcquireIQData()
    while not ready.value:
        rsa.IQBLK_WaitForIQDataReady(c_int(100), byref(ready))
    rsa.IQBLK_GetIQDataDeinterleaved(byref(iData), byref(qData),
                                     byref(c_int(outLength)), c_int(recordLength))
    rsa.DEVICE_Stop()

    return np.array([iData, qData])


def block_iq_example():
    print('\n\n########Block IQ Example########')
    search_connect()
    cf = 1e9
    refLevel = 0
    iqBw = 40e6
    recordLength = 1e3

    time = config_block_iq(cf, refLevel, iqBw, recordLength)
    IQ = acquire_block_iq(recordLength)

    fig = plt.figure(1, figsize=(15, 10))
    fig.suptitle('I and Q vs Time', fontsize='20')
    ax1 = plt.subplot(211, facecolor='k')
    ax1.plot(time * 1000, np.real(IQ), color='y')
    ax1.set_ylabel('I (V)')
    ax1.set_xlim([time[0] * 1e3, time[-1] * 1e3])
    ax2 = plt.subplot(212, facecolor='k')
    ax2.plot(time * 1000, np.imag(IQ), color='c')
    ax2.set_ylabel('I (V)')
    ax2.set_xlabel('Time (msec)')
    ax2.set_xlim([time[0] * 1e3, time[-1] * 1e3])
    plt.tight_layout()
    plt.show()
    rsa.DEVICE_Disconnect()

# program
search_connect()
config_block_iq(1e9, 0, 40e6, 1024)
print(acquire_block_iq(1024))

# block_iq_example()