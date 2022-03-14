from API.RSA_API import *
from ctypes import *
from platform import system
from time import sleep
import numpy as np

class Tektronix():
    def __init__(self):
        self.loadDLL()

    def loadDLL(self):
        # load dll
        CURRENT_OS = system()
    
        if CURRENT_OS == 'Windows':
            self.RSA = cdll.LoadLibrary('./API/win/RSA_API.dll')
        elif CURRENT_OS == 'Linux':
            RTLD_LAZY = 0x0001
            LAZYLOAD = RTLD_LAZY | RTLD_GLOBAL
            self.RSA = CDLL('./API/linux/libRSA_API.so', LAZYLOAD)
            usbapi = CDLL("./API/linux/libcyusb_shared.so",LAZYLOAD)
        else:
            print('OS not supported!')
            exit()

    # functions
    def err_check(self, rs):
        if ReturnStatus(rs) != ReturnStatus.noError:
            raise RSAError(ReturnStatus(rs).name)

    def device_connect(self):
        numFound = c_int(0)
        intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
        deviceIDs = intArray()
        deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
        deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)
        apiVersion = create_string_buffer(DEVINFO_MAX_STRLEN)

        self.RSA.DEVICE_GetAPIVersion(apiVersion)

        output = {
                'message' : None,
                'api_version' : apiVersion.value.decode(),
                'device_type' : None,
                'device_serial' : None
            }

        self.err_check(self.RSA.DEVICE_Search(byref(numFound), deviceIDs,
                                    deviceSerial, deviceType))

        if numFound.value < 1:
            # self.RSA.DEVICE_Reset(c_int(0))
            output['message'] = 'No Device Found.'

        elif numFound.value == 1:
            output['device_type'] = deviceType.value.decode()
            output['device_serial'] = deviceSerial.value.decode()

            self.err_check(self.RSA.DEVICE_Connect(deviceIDs[0]))
            self.RSA.CONFIG_Preset()
            self.RSA.DEVICE_PrepareForRun()

            output['message'] = 'Connection Success.'
        else:
            # corner case
            output['message'] = 'Too Many Devices Connected.'

        return output

    def config_block_iq(self, cf=1e9, refLevel=0, iqBw=40e6, recordLength=10e3, sampleRate=0):
        '''
        Configure IQ collection parameters for the connected Spectrum Analyser.

        PARAMETERS
        cf: centre frequency of the collection (hz)
        refLevel: dB reference level
        iqBw: acquisition bandwidth of the collection (hz)
        recordLength: number of samples to collect per record
        '''

        recordLength = int(recordLength)
        self.RSA.CONFIG_SetCenterFreq(c_double(cf))
        self.RSA.CONFIG_SetReferenceLevel(c_double(refLevel))

        self.RSA.IQBLK_SetIQBandwidth(c_double(iqBw))
        self.RSA.IQBLK_SetIQRecordLength(c_int(recordLength))

        iqSampleRate = c_double(sampleRate)
        self.RSA.IQBLK_GetIQSampleRate(byref(iqSampleRate))


    def acquire_block_iq(self, recordLength=10e3, n_records=1):
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

        self.RSA.DEVICE_Run()

        collected_data = []
        for _ in range(n_records):
            self.RSA.IQBLK_AcquireIQData()
            while not ready.value:
                self.RSA.IQBLK_WaitForIQDataReady(c_int(100), byref(ready))
            self.RSA.IQBLK_GetIQDataDeinterleaved(byref(iData), byref(qData),
                                            byref(c_int(outLength)), c_int(recordLength))
            ready = c_bool(False)

            collected_data.append(np.array([iData, qData]))

        self.RSA.DEVICE_Stop()

        return np.array(collected_data).tolist()

    def getBatteryStatus(self):
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
        self.err_check(self.RSA.POWER_GetStatus(byref(pInfo)))
    
        output = {
            'plugged_in' : pInfo.externalPowerPresent,
            'batt_present' : pInfo.batteryPresent,
            'charge' : pInfo.batteryChargeLevel,
            'overtemp' : pInfo.batteryOverTemperature,
            'batt_hwerror' : pInfo.batteryHardwareError
        }
    
        return output
    
    def rebootDevice(id):
        self.err_check(self.RSA.DEVICE_Reset(c_int(id)))