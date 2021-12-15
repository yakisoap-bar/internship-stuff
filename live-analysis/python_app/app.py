# Libraries
import argparse

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

# program
def doStuff(args):
	config_block_iq(args.centerFreq, args.refLevel, args.bandwidth, 1024)
	data = acquire_block_iq(1024, args.numRecords).tolist()
	print(predict_post('http://localhost:3000/predict', data))

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

	args = parser.parse_args()

	device_connect()
	if args.battery:
		print(getBatteryStatus()[])
	else:
		doStuff(args)

if __name__ == '__main__':
	main()