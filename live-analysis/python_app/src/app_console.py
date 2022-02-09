# Libraries
import argparse, configparser
from mimetypes import init

from Functions.plutoSDR import PlutoSDR
from Functions.Request import predict_post

class TerminalApp():
	def __init__(self) -> None:
		self.globalVars()
		
		# Parse args
		self.args = self.parseArgs()
		self.checkArgs()

		self.params = self.readConf()
		self.initSDR()
	
	def globalVars(self):
		'''Init vars'''
		self.run_count = 0
		self.backendURL = 'http://localhost:3000/predict'
	
	def run(self):
		self.predict()
		self.genBarChart()
		
		if self.run_count != 1:
			self.run_count -= 1
			self.run()
		
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

		# Read default configs
		config = configparser.ConfigParser()
		config.read(config, self.args.conf_file)
		params = self.parseConfig(config, 'DEFAULT')
		
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
		intParams = ["ref_level", "num_records", "sampling_rate", "center_freq", "rx_bandwidth"]
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
		
	def predict(self):
		'''
		Send signals and return predictions
		'''
		self.updateConfigs()
		data = self.SDR.collect_iq()
		predictions = predict_post(self.backendURL, data, self.params['centerFreq'], self.params['filter_check'])
		
		return predictions
	
	def genBarChart(self):
		# TODO visualise predictions
		pass

	def initSDR(self):
		'''Init SDR'''
		self.SDR = PlutoSDR()
		self.SDR.initConfig(self.params['centerFreq'], self.params['bandwidth'], self.params['numRecords'])
	
	def updateConfigs(self):
		'''Update SDR configs, if empty, no change'''
		params = self.readConf()
		if params != self.params():
			self.params = params
			self.SDR.config(self.params)

def main():
	app = TerminalApp()
	app.run()
	exit()

if __name__ == '__main__':
	main()