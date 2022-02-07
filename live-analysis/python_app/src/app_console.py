# Libraries
import argparse, configparser
from mimetypes import init

class TerminalApp():
	def __init__(self) -> None:
		self.args = self.parseArgs()
		self.checkArgs()

	def parseArgs(self):
		parser = argparse.ArgumentParser(description='Do the application')
		parser.add_argument('-v', '--verbose',
							action='store_true', dest="verbose",
							help='Display additional output and current configurations')
		parser.add_argument('--battery',
							action='store_true', dest="battery",
							help='Check battery level')
		parser.add_argument('-f', '--centerfreq',
							dest="cf", metavar="centerFreq",
							nargs='?', default=2.44e9, type=int,
							help="Set center frequency")
		parser.add_argument('-r', '--reflevel',
							dest="refLevel", metavar="refLevel",
							nargs='?', default=0, type=int,
							help="Set reference level")
		parser.add_argument('-b', '--bandwidth',
							dest="bw", metavar="bandwidth",
							nargs='?', default=40e6, type=int,
							help="Set bandwidth")
		parser.add_argument('-n', '--records',
							dest="numRecords", metavar="numRecords",
							nargs='?', default=10, type=int,
							help="Determine number of records")
		parser.add_argument('-s', '--sampfreq',
							dest="sampFreq", metavar="samplingFrequency",
							nargs='?', default=40, type=int,
							help="Set sampling frequency")
		parser.add_argument('--conf',
							dest="conFile", metavar="configFile",
							nargs='?', default='parameters.conf', type=str,
							help="Specify configuration file.")
	
		return parser.parse_args()
	
	def checkArgs(args):
		if args.configFile:
			pass
		else:
			pass
		
	def readConf(self):
		with open(self.args.filename, 'r') as f:
			conf = str(f)
		conf.split()
	
	def run():
		pass

def main():
	app = TerminalApp()
	app.run()
	exit()

if __name__ == '__main__':
	main()