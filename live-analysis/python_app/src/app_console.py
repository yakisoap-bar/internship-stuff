# Libraries
import argparse, configparser

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

def parseArgs():
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

def readConf():
	with open(args.filename, 'r') as f:
		conf = str(f)
	conf.split()

# program
def doStuff():
	# config_block_iq(args.centerFreq, args.refLevel, args.bandwidth, 1024)
	# config_block_iq(2.44e9, 0, 40e6, 1024)
	config_block_iq(5.18e9, 0, 40e6, 1024)

	while True:
		data = acquire_block_iq(1024, 10)
		predictions = predict_post('http://localhost:3000/predict', data)
		print(predictions)

		# print([predictions["signalNames"], predictions["predictions"]])

def main():
	args = parseArgs()
	device_connect()
	print(getBatteryStatus())
	exit()

if __name__ == '__main__':
	main()