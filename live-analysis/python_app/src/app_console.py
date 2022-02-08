# Libraries
import argparse, configparser
from mimetypes import init

from Functions.plutoSDR import PlutoSDR
from Functions.Request import predict_post

class TerminalApp():
	def __init__(self) -> None:
		self.globalVars()
		self.args = self.parseArgs()
		self.checkArgs()
		self.initSDR()
	
	def globalVars(self):
		'''Init vars'''
		self.backendURL = 'http://localhost:3000/predict'

	def parseArgs(self):
		'''argparse'''
		parser = argparse.ArgumentParser(description='Do the application')
		parser.add_argument('-v', '--verbose',
							action='store_true', dest="verbose",
							help='Display additional output and current configurations')
		parser.add_argument('-b', '--batt',
							action='store_true', dest="battery",
							help='Check battery level')
		parser.add_argument('-c', '--conf',
							dest="conf_file", metavar="configFile",
							nargs='?', default='params.conf', type=str,
							help="Specify configuration file.")
		parser.add_argument('-s', '--signal',
							dest="signal", metavar="configFile",
							nargs='?', type=str,
							help="Select default signal parameters")
		# TODO: List saved signals
	
		return parser.parse_args()

	def run(self):
		# Check if params changed and update if yes
		params = self.readConf()
		if params != self.params():
			self.params = params
			self.SDR.config(self.params)

		data = self.SDR.collect_iq()
		predictions = predict_post(self.backendURL, data, self.params['centerFreq'], self.params['filter_check'])
	
	def checkArgs(self):
		'''Additional check for argparser arguments'''
		self.params = self.readConf()
		
	def readConf(self):
		'''
		Load and parse config file
		returns params
		'''

		# Read default configs
		config = configparser.ConfigParser()
		config.read(config, self.args.conf_file)
		params = self.parseConfig('DEFAULT')
		
		if self.args.signal in self.config.sections():
			signal_name = (self.args.signal).upper()
			params = self.parseConfig(config, signal_name, params)
		
		return params
	
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
		intParams = ["ref_level", "num_records", "sampleing_rate", "center_freq", "rx_bandwidth"]
		boolParams = ["filter_check"]

		for setting in config[key]:
			item = config[key][setting]

			# type conversion
			if key in intParams:
				item = float(item)
			elif key in boolParams:
				item = bool(item)
			
			params[setting] = item
		
		return params
		
	def initSDR(self):
		'''Init SDR'''
		self.SDR = PlutoSDR()
		self.SDR.initConfig(self.params['centerFreq'], self.params['bandwidth'], self.params['numRecords'])
	
def main():
	app = TerminalApp()
	exit()

if __name__ == '__main__':
	main()