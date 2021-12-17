from kivy.app import App
from k

# Libraries
from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

# program
def doStuff(args):
	config_block_iq(args.centerFreq, args.refLevel, args.bandwidth, 1024)

	while True:
		data = acquire_block_iq(1024, args.numRecords)
		predictions = predict_post('http://localhost:3000/predict', data)
		print(predictions)
		# print([predictions["signalNames"], predictions["predictions"]])

def main():
	device_connect()
	if args.battery:
		print(getBatteryStatus())
	else:
		doStuff(args)

if __name__ == '__main__':
	main()