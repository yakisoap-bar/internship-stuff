# Libraries
import argparse, configparser
import matplotlib.pyplot as plt
import numpy as np

# SA
from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

# Plotting
from Functions.Request import predict_post
from Functions.Plot import Plotter

# Misc
from Functions.Utils import createBanner

class TerminalApp():
    def __init__(self) -> None:
        self.globalVars()
        
        # Parse args
        self.args = self.parseArgs()
        self.checkArgs()

        self.params = self.readConf()
        self.initSDR()

        # bar chart variables
        self.__barStarted = False
    
    def globalVars(self):
        '''Init vars'''
        self.run_count = 0
        self.Plot = Plotter()
    
    def start(self):
        if self.args.battery:
            print(self.getBatt())
        elif self.args.check_params:
            print(self.readConf())
        else:
            self.runPredictions()
        
    def getBatt(self):
        batt = getBatteryStatus()
        return batt

    def runPredictions(self):
        predictions = self.predict()
        self.genBarChart(predictions)
        
        if self.run_count != 1:
            self.run_count -= 1
            self.runPredictions()()
        
    def parseArgs(self):
        '''argparse'''
        parser = argparse.ArgumentParser(description='Do the application')
        parser.add_argument('-v', '--verbose',
                            action='store_true', dest="verbose",
                            help='Display additional output and current configurations')
        parser.add_argument('-b', '--batt',
                            action='store_true', dest="battery",
                            help='Check battery level')
        parser.add_argument('-p', '--params',
                            action='store_true', dest="check_params",
                            help='Check current params')
        parser.add_argument('-c', '--conf',
                            dest="conf_file", metavar="configFile",
                            nargs='?', default='params.conf', type=str,
                            help="Specify configuration file.")
        parser.add_argument('-s', '--signal',
                            dest="signal",
                            nargs='?', type=str,
                            help="Select default signal parameters")
        parser.add_argument('-r', '--run',
                            dest="run_count", metavar="configFile",
                            nargs='?', type=int,
                            help="Select default signal parameters")
        # TODO: List saved signals
    
        return parser.parse_args()

    def checkArgs(self):
        '''Additional check for argparser arguments'''
        if self.args.run_count != None:
            self.run_count = self.args.run_count

    def readConf(self):
        '''
        Load and parse config file
        returns params
        '''
        try:
            # Read default configs
            config = configparser.ConfigParser()
            config.read(self.args.conf_file)
            params = self.parseConfig(config, 'DEFAULT')
        
            if self.args.signal in config.sections():
                signal_name = (self.args.signal).upper()
                params = self.parseConfig(config, signal_name, params)
        
            return params

        except: # When the file is still writing
            return self.params
    
    def parseConfig(self, config, key, params={}):
        '''
        Parses config file items into proper types
        returns dict of params

        PARAMETERS:
        config: Loaded config file
        key: key to load from config file
        params: if given, updates params
        '''
        # Define types
        intParams = ["ref_level", "num_records", "sampling_rate", "center_freq", "rx_bandwidth"]
        boolParams = ["filter_check"]

        for setting in config[key]:
            item = config[key][setting]

            # type conversion
            if setting in intParams:
                item = int(float(item))
            elif setting in boolParams:
                item = bool(item)

            params[setting] = item

        return params

    def predict(self):
        '''
        Send signals and return predictions
        '''
        self.updateConfigs()
        data = acquire_block_iq(1024, self.params['num_records'])
        url = 'http://' + self.params['server_ip'] + ':3000/predict'
        predictions = predict_post(url, data, self.params['center_freq'], self.params['filter_check'])
        results = {"data": data,
					"predictions": predictions}
        return results
    
    def genBarChart(self, predictions):
        self.Plot.drawChart(predictions)

    def initSDR(self):
        '''Init SDR'''
        device_connect()
    
    def updateConfigs(self):
        '''Update SDR configs, if empty, no change'''
        params = self.readConf()
        if params != self.params:
            self.params = params
            config_block_iq(self.params['center_freq'], self.params['ref_level'], self.params['rx_bandwidth'], 1024)

def main():
    app = TerminalApp()
    app.start()
    exit()

if __name__ == '__main__':
    main()