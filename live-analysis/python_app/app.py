# Libraries
import argparse

from Functions.Collect import *
from Functions.Request import *

def configs():
	"""Check configs in here"""

def main():
	# Argument parser
	parser = argparse.ArgumentParser(description='Direct streaming of the SA to the classifier')
	parser.add_argument("configs",
						nargs="+", metavar='CONFIGS',
						action="store",
						help="Set configs for CF, refLevel, IQBandwidth, record length")
	parser.add_argument("-b", "--battery",
						action="store_true", dest="batt_level", default="False",
						help="Show current battery level")

	args = parser.parse_args()

	search_connect()
	config_block_iq(2.44e9, 0, 40e6, 1024)
	data = acquire_block_iq(1024, 10).tolist()

	print(predict_post('http://localhost:3000/predict', data))

if __name__ == '__main__':
	main()