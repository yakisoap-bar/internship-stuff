import os

def printStatus(info):
	# Clears screan after printing information
	# info can be dict or list
	os.system('cls' if os.name == 'nt' else 'clear')

	i_type = type(info)

	if i_type == dict:
		for key in info:
			print(f"{key}: {info[key]}")

	elif i_type == list:
		for i in info:
			print(i)

def printPrediction(predictions):
	os.system('cls' if os.name == 'nt' else 'clear')
	# for name, pred in zip(predictions[1]['signalNames'], predictions[1]['predictions']):
	# 	print(f'{name}: {pred}')

	print(*predictions[1]['signalNames'], sep='\t')
	print(*[round(pred, 3) for pred in predictions[1]['predictions']], sep='\t')