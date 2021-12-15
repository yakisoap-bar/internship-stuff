# Libraries
import argparse

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

# program
def doStuff(args):
	search_connect()
	config_block_iq(args.centerFreq, args.refLevel, args.bandwidth, 1024)
	data = acquire_block_iq(1024, args.numrecords).tolist()
	print(getBatteryStatus())
	print(predict_post('http://localhost:3000/predict', data))

def main():
	parser = argparse.ArgumentParser(description='Do the application')
	parser.add_argument('-v', '--verbose',
						action='store_true', dest="verbose",
						help='Display additional output and current configurations')
	parser.add_argument('-f', '--centerfreq',
						nargs='?', default=2.44e9, metavar="centerFreq", type=int,
						help="Set center frequency")
	parser.add_argument('-r', '--reflevel',
						nargs='?', default=0, metavar="refLevel", type=int,
						help="Set reference level")
	parser.add_argument('-b', '--bandwidth',
						nargs='?', default=40e6, metavar="bandwidth", type=int,
						help="Set bandwidth")
	parser.add_argument('-n', '--numrecords',
						nargs='?', default=10, metavar="numRecords", type=int,
						help="Determine number of records")

	args = parser.parse_args()
	checkStuff(args)

if __name__ == '__main__':
	main()