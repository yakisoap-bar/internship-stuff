import os, shutil, math

def splitLines(line_string, length):
    '''
    function to split lines into defined lengths

    PARAMETERS:
    line_string: a string with the lines that are to be split
    length: the length of which to split long lines into
    '''
    lines = line_string.split('\n')
    for i, line in enumerate(lines):
        if len(line) < length:
            continue

        # split long lines into separate lines
        line_split = line.split(' ')
        temp = []
        current_line = ''
        buffer_line = ''

        for word in line_split:
            buffer_line += word + ' '
            if len(buffer_line) < length:
                current_line += word + ' '
                continue

            temp.append(current_line)
            current_line = word + ' '
            buffer_line = word + ' '

        # flush rest of buffer into temp list
        temp.append(current_line)

        del lines[i]
        lines[i:i] = temp

    return lines

def formatPrediction(predictions):
	msg = '\t'.join(predictions['signalNames']) + '\n'
	msg += '\t'.join([str(round(pred, 3)) for pred in predictions['predictions']])
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
	i_type = type(content)
	msg = ""

	if i_type == dict:
		for key in content:
			msg += f"{key}: {content[key]}\n"

	elif i_type == list:
		for i in content:
			msg += f"{i}\n"
	
	return msg

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

	padding = "|" + " " * int(cols-2) + "|\n"
	num_padding = rows - len(string)

	box += padding * (math.floor(num_padding/2))

	for line in string:
		num_spaces = (cols-len(line))/2 - 1
		spaces1 = " " * (math.floor(num_spaces))
		spaces2 = " " * (math.ceil(num_spaces))
		box += f"|{spaces1}{line}{spaces2}|"

	box += padding * (math.floor(num_padding/2))

	return box

<<<<<<< HEAD
def createBanner(section, msg=''):
    '''
    function to create a banner according to terminal window size.

    PARAMETERS:
    section: section header text
    msg: additional message to insert
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

    # get terminal window size
    cols, rows = shutil.get_terminal_size(fallback=(80, 24))

    # define printing parameters and templates
    full_lines = '-' * cols
    
    # split strings into separate lines
    section = splitLines(section, cols-4)
    msg = splitLines(msg, cols-4)

    # print section header
    print(full_lines, '\n', sep='')
    for line in section:
        print(line.center(cols))
    print('\n', full_lines, sep='')

    # calculate remaining space for message
    msg_space = rows - 4 - len(section) - 1
    msg_pad_top = (msg_space - len(msg)) // 2
    msg_pad_btm = msg_space - msg_pad_top - len(msg) - 1

    # print message section
    print('\n'*msg_pad_top)
    for line in msg:
        print(line.center(cols))
    print('\n'*msg_pad_btm, full_lines, sep='')
=======
def createBanner(section, msg = ""):
	'''
	Prints **aesthetic** banner that fills the whole terminal

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

	# Build the banner
	banner = "\n"
	# Section Header
	banner += f"{bannerh_border}"
	banner += bannerPadding([section], cols, header_rows)
	banner += f"{bannerh_border}"

	# Section content	
	banner += bannerPadding(msg, cols, msg_rows)
	banner += f"{bannerh_border}".strip()

	os.system('cls' if os.name == 'nt' else 'clear')
	print(banner)
>>>>>>> 5ce744d9622e03b994e931dc6c341d5d14540935
