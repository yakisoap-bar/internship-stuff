from API.RSA_API import *
from ctypes import *
from platform import system

import numpy as np

def loadTektronixDLL():
    # load dll
    CURRENT_OS = system()
    
    if CURRENT_OS == 'Windows':
        rsa = cdll.LoadLibrary('./API/win/RSA_API.dll')
    elif CURRENT_OS == 'Linux':
        RTLD_LAZY = 0x0001
        LAZYLOAD = RTLD_LAZY | RTLD_GLOBAL
        rsa = CDLL('./API/linux/libRSA_API.so', LAZYLOAD)
        usbapi = CDLL("./API/linux/libcyusb_shared.so",LAZYLOAD)
    else:
        print('OS not supported!')
        exit()

# functions
def err_check(rs):
    if ReturnStatus(rs) != ReturnStatus.noError:
        raise RSAError(ReturnStatus(rs).name)

def device_connect():
    numFound = c_int(0)
    intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
    deviceIDs = intArray()
    deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
    deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)
    apiVersion = create_string_buffer(DEVINFO_MAX_STRLEN)

    rsa.DEVICE_GetAPIVersion(apiVersion)

    output = {
            'message' : None,
            'api_version' : apiVersion.value.decode(),
            'device_type' : None,
            'device_serial' : None
        }

    err_check(rsa.DEVICE_Search(byref(numFound), deviceIDs,
                                deviceSerial, deviceType))

    if numFound.value < 1:
        # rsa.DEVICE_Reset(c_int(0))
        output['message'] = 'No Device Found.'

    elif numFound.value == 1:
        output['device_type'] = deviceType.value.decode()
        output['device_serial'] = deviceSerial.value.decode()

        err_check(rsa.DEVICE_Connect(deviceIDs[0]))
        rsa.CONFIG_Preset()
        rsa.DEVICE_PrepareForRun()

        output['message'] = 'Connection Success.'
    else:
        # corner case
        output['message'] = 'Too Many Devices Connected.'

    return output

def config_block_iq(cf=1e9, refLevel=0, iqBw=40e6, recordLength=10e3, sampleRate=0):
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

    iqSampleRate = c_double(sampleRate)
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

    return np.array(collected_data).tolist()