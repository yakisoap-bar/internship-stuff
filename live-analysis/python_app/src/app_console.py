# Libraries
import argparse, configparser
from mimetypes import init

class TerminalApp():
	def __init__(self) -> None:
		self.globalVars()
		self.args = self.parseArgs()
		self.checkArgs()
	
	def globalVars(self):
		# Init vars
		self.parameters = {}

	def parseArgs(self):
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
		pass
	
	def checkArgs(self):
		self.readConf()
		
	def readConf(self):
		# Read default configs
		config = configparser.ConfigParser()
		config.read(self.args.conf_file)
		for setting in config['DEFAULT']:
			self.parameters[setting] = config['DEFAULT'][setting]
		
		if self.args.signal != None:
			signal_name = (self.args.signal).upper()
			for setting in config[signal_name]:
				self.parameters[setting] = config[signal_name][setting]
	
	def getSignals():
		pass

	def sendSignals():
		pass
	
	def displayPredictions():
		pass

def main():
	app = TerminalApp()
	app.run()
	exit()

if __name__ == '__main__':
	main()