# Libraries
import argparse

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

def checkArgs(args):
	if args.configFile:
		pass
		return True

	else:
		return False

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
	parser = argparse.ArgumentParser(description='Do the application')
	parser.add_argument('-v', '--verbose',
						action='store_true', dest="verbose",
						help='Display additional output and current configurations')
	parser.add_argument('--battery',
						action='store_true', dest="battery",
						help='Check battery level')
	parser.add_argument('-f', '--centerfreq',
						dest="centerFreq", metavar="centerFreq",
						nargs='?', default=2.44e9, type=int,
						help="Set center frequency")
	parser.add_argument('-r', '--reflevel',
						dest="refLevel", metavar="refLevel",
						nargs='?', default=0, type=int,
						help="Set reference level")
	parser.add_argument('-b', '--bandwidth',
						dest="bandwidth", metavar="bandwidth",
						nargs='?', default=40e6, type=int,
						help="Set bandwidth")
	parser.add_argument('-n', '--numrecords',
						dest="numRecords", metavar="numRecords",
						nargs='?', default=10, type=int,
						help="Determine number of records")
	parser.add_argument('-s', '--samplingfrequency',
						dest="samplingFrequency", metavar="samplingFrequency",
						nargs='?', default=40, type=int,
						help="Set sampling frequency")
	parser.add_argument('--file',
						dest="configFile", metavar="configFile",
						nargs='?', type=str,
						help="Specify configuration file.")

	# args = parser.parse_args()

	device_connect()
	doStuff()
	# print(getBatteryStatus())

	# # Check parsed arguments
	# if args.battery:
	# 	print(getBatteryStatus())
	# 	exit()
	
	# if checkArgs():
	# 	doStuff(args)
	
	exit()

if __name__ == '__main__':
	main()