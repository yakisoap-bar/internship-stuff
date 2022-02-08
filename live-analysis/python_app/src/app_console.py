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
		self.params = {}
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
		signal = self.SDR.collect_iq()
		predict_post(self.backendURL, signal, self.params['centerFreq'], self.params['filter_check'])
	
	def checkArgs(self):
		'''Additional check for argparser arguments'''
		self.readConf()
		
	def readConf(self):
		'''Load and parse config file'''
		# Read default configs
		config = configparser.ConfigParser()
		config.read(config, self.args.conf_file)
		self.parseConfig('DEFAULT')
		
		if self.args.signal in self.config.sections():
			signal_name = (self.args.signal).upper()
			self.parseConfig(config, signal_name)
	
	def parseConfig(self, config, key):
		'''
		Parses config file items into proper types and add them to self.params	

		PARAMETERS:
		config: Loaded config file
		key: key to load from config file
		'''
		# Define types
		intParams = ["RefLevel", "numRecords", "samplingFreq", "centerFreq", "bandwidth"]
		boolParams = ["filterCheck"]

		for setting in config[key]:
			item = config[key][setting]

			# type conversion
			if key in intParams:
				item = float(item)
			elif key in boolParams:
				item = bool(item)
			
			self.params[setting] = item
		
	def initSDR(self):
		'''Init SDR'''
		self.SDR = PlutoSDR()
		self.SDR.initConfig(self.params['centerFreq'], self.params['bandwidth'], self.params['numRecords'])
	
def main():
	app = TerminalApp()
	exit()

if __name__ == '__main__':
	main()