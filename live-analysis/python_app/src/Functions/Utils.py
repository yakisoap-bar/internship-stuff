import os, shutil

def printStatus(info):
	# Clears screan after printing information
	# info can be dict or list
	os.system('cls' if os.name == 'nt' else 'clear')

	i_type = type(info)
	msg = ""

	if i_type == dict:
		for key in info:
			msg += f"{key}: {info[key]}\n"

	elif i_type == list:
		for i in info:
			msg += f"{i}\n"
	
	print(msg)

def printPrediction(predictions):
	os.system('cls' if os.name == 'nt' else 'clear')
	# for name, pred in zip(predictions[1]['signalNames'], predictions[1]['predictions']):
	# 	print(f'{name}: {pred}')

	msg = '\t'.join(predictions[1]['signalNames']) + '\n'
	msg += '\t'.join([str(round(pred, 3)) for pred in predictions[1]['predictions']])

	print(msg)

def createBanner(section = "", msg = ""):
	columns, rows = shutil.get_terminal_size(fallback=(80, 24))
	header = "*"*columns

	section_spaces = " " * (int(columns/2-len(section)/2))

	if msg != "":
		msg_spaces = " " * (int(columns/2 - len(msg)/2))
		header_name = f"{section}\n\n{msg_spaces}{msg}"

	banner = f"{header}\n\n{header_spaces}{section_name}\n\n{header}"

	return banner