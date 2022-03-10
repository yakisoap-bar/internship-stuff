import os, shutil, math

def formatPredictions(predictions):
    msg = '\t'.join(predictions[1]['signalNames']) + '\n'
    msg += '\t'.join([str(round(pred, 3)) for pred in predictions[1]['predictions']])
	return msg

def dictToStr(content):
	'''
	Formats dictionary into readable string
	
	Parameters:
	------
	content : dict
		Dictionary to be formatted
	
	Returns:
	------
	str
		Printable string, lists dictionary items by 'key:item'
	'''
	i_type = type(info)
	msg = ""

	if i_type == dict:
		for key in info:
			msg += f"{key}: {info[key]}\n"

	elif i_type == list:
		for i in info:
			msg += f"{i}\n"

def bannerPadding(string, cols, rows, centered = True):
	'''
	How to center a div

	Parameters:
	------
	string : list
		Message to go into the box, split by newlines/if line is too long, concat at char limit
	cols : int
		Width of terminal
	rows : int
		No. of rows to fill
	centered : boolean
		If false, at the top of the box
	
	Returns:
	------
	str
		centered div
	'''
	box = ""

	padding = "*" + " " * int(cols-2) + "*\n"
	num_padding = rows - len(string)

	box += padding * (math.floor(num_padding/2))

	for line in string:
		num_spaces = (cols-len(line))/2 - 1
		spaces1 = " " * (math.floor(num_spaces))
		spaces2 = " " * (math.ceil(num_spaces))
		box += f"*{spaces1}{line}{spaces2}*"

	box += padding * (math.floor(num_padding/2))

	return box

def createBanner(section, msg = ""):
	'''
	Creates **aesthetic** banner that fills the whole terminal

	Parameters:
	------
	section : str
		Section header
	msg : str
		Content below section
	
	Returns: 
	------
	str
		Banner
	'''
	cols, rows = shutil.get_terminal_size(fallback=(80, 24))

	bannerh_border = "*" * cols
	paddingv = 5
	max_line_len = cols - paddingv*2
	header_rows = 5
	msg_rows = rows - header_rows - 3

	# Split msg into clean lines
	msg = msg.split('\n')
	for i in range(len(msg)):
		line_len = len(msg[i])
		if line_len > max_line_len:
			trunc_line = msg[i][:line_len-max_line_len]
			msg.insert(i+1, trunc_line)	

	# Section Header
	banner = f"{bannerh_border}"
	banner += bannerPadding([section], cols, header_rows)
	banner += f"{bannerh_border}"

	# Section content	
	banner += bannerPadding(msg, cols, msg_rows)
	banner += f"{bannerh_border}"

	os.system('cls' if os.name == 'nt' else 'clear')
	print(banner)