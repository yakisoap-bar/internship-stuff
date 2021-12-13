from API.RSA_API import *
from ctypes import *

import numpy as np

# load dll
rsa = cdll.LoadLibrary('./API/win/RSA_API.dll')

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
    '''
    Configure IQ collection parameters for the connected Spectrum Analyser.

    PARAMETERS
    cf: centre frequency of the collection (hz)
    refLevel: dB reference level
    iqBw: acquisition bandwidth of the collection (hz)
    recordLength: number of samples to collect per record
    '''

    recordLength = int(recordLength)
    rsa.CONFIG_SetCenterFreq(c_double(cf))
    rsa.CONFIG_SetReferenceLevel(c_double(refLevel))

    rsa.IQBLK_SetIQBandwidth(c_double(iqBw))
    rsa.IQBLK_SetIQRecordLength(c_int(recordLength))

    iqSampleRate = c_double(0)
    rsa.IQBLK_GetIQSampleRate(byref(iqSampleRate))


def acquire_block_iq(recordLength=10e3, n_records=1):
    '''
    Acquires IQ records using connected Spectrum Analyser.

    PARAMETERS
    recordLength: number of samples per IQ record to pull
    n_records: number of records to collect

    Returns a Numpy array with `n_records` of records.
    '''

    recordLength = int(recordLength)
    ready = c_bool(False)
    iqArray = c_float * recordLength
    iData = iqArray()
    qData = iqArray()
    outLength = 0

    rsa.DEVICE_Run()

    collected_data = []
    for _ in range(n_records):
        rsa.IQBLK_AcquireIQData()
        while not ready.value:
            rsa.IQBLK_WaitForIQDataReady(c_int(100), byref(ready))
        rsa.IQBLK_GetIQDataDeinterleaved(byref(iData), byref(qData),
                                        byref(c_int(outLength)), c_int(recordLength))
        ready = c_bool(False)

        collected_data.append(np.array([iData, qData]))
        
    rsa.DEVICE_Stop()

    return np.array(collected_data)