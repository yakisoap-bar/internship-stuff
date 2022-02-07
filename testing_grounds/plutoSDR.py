import adi
import numpy as np

class PlutoSDR():
    '''
    A class for interfacing with the ADALM-PLUTO SDR. Contains all the
    libraries needed for connecting to and controlling the SDR.

    PARAMETERS:
    ip: the ip address of the SDR
    cf: the center frequency to collect signals from
    rbw: the receiving bandwidth of the SDR to collect signals from
    n_records: the number of records to return after collecting signals
    r_length: the number of samples per record to collect
    '''

    def __init__(self, ip='192.168.2.1', cf=int(2.44e9), rbw=int(40e6), n_records=10, r_length=1024):
        self.__sdr = adi.Pluto('ip:' + ip)

        # set default parameters
        self.__r_length = r_length
        self.__n_records = n_records
        self.__sdr.rx_hardwaregain_chan0 = 'fast_attack'    # set sdr gain
        self.__sdr.sample_rate = int(56e6)                  # set sampling rate

        self.__sdr.rx_buffer_size = r_length * n_records        # set record(s) length
        self.__sdr.rx_lo = cf                               # set center frequency
        self.__sdr.rx_rf_bandwidth = rbw                    # set receiving bandwidth

    def config(self, configs={}):
        '''
        Method to configure SDR parameters. Returns current config if nothing is passed.
        
        PARAMETERS:
        configs: a dictionary containing all the possible parameters. 
        
        Possible parameters are:
        `{'sampling_rate', 'num_records, 'center_freq, 'rx_bandwidth', 'r_length}`
        '''

        possible_configs = ['sampling_rate', 'num_records', 'center_freq', 'rx_bandwidth', 'r_length']
        temp_cfg_keys = configs.keys()

        # return current configuration if nothing passed
        if len(temp_cfg_keys) == 0:
            return {
                possible_configs[0] : self.__sdr.sample_rate,
                possible_configs[1] : self.__sdr.rx_buffer_size / self.__r_length,
                possible_configs[2] : self.__sdr.rx_lo,
                possible_configs[3] : self.__sdr.rx_rf_bandwidth,
                possible_configs[4] : self.__r_length
            }

        # check if correct parameters are passed
        if sorted(temp_cfg_keys) != sorted(possible_configs):
            raise KeyError(f'Config Mismatch! Expected {possible_configs}, got {temp_cfg_keys}.')

        # set parameters to SDR
        else:
            self.__sdr.sample_rate = int(configs[possible_configs[0]])
            self.__sdr.rx_buffer_size = int(configs[possible_configs[1]]) * int(configs[possible_configs[4]])
            self.__sdr.rx_lo = int(configs[possible_configs[2]])
            self.__sdr.rx_rf_bandwidth = int(configs[possible_configs[3]])
            self.__r_length = int(configs[possible_configs[4]])

    def collect_iq(self):
        '''
        Method to collect one block of iq data.
        Returns IQ data in shape: `(n_records, 2, r_length)`
        '''

        # collect n_records of iq records
        iq_data_raw = self.__sdr.rx()

        # process complex iq records to i and q streams
        iq_data_processed = np.reshape(np.array([np.real(iq_data_raw), np.imag(iq_data_raw)]),
                            (int(self.__sdr.rx_buffer_size / self.__r_length), 2, self.__r_length))

        return iq_data_processed

sdr = PlutoSDR()

sdr.config({
    'sampling_rate' : 56e6, 
    'num_records' : 20, 
    'center_freq' : 4e9, 
    'rx_bandwidth' : 30e6,
    'r_length' : 512
    })

print(sdr.config())

print(sdr.collect_iq().shape)