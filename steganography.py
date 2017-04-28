	
def is_encoding(char):
	return not ((char.isalpha()) | (char.isdigit()) | (char == ' ') | (char == '<') | (char == '>') | (char == '\r') | (char == '\n'))

def decode(message):
	bin_string = get_binary(message)
	split = [bin_string[8*i:8*(i+1)] for i in range(len(bin_string)//8)]
	bytes = [int(i, 2) for i in split]
	decoded = ''.join(chr(i) for i in bytes)
	return decoded

def get_binary(message):
	secret = get_encoded(message)
					
	bin_string = ""
	x = 2
	while(x<len(secret)):
		if secret[x] != '\\':
			bin_string+='0'
			x+=1
		elif secret[x] == '\\':
			bin_string+='1'
			x+=2
	return bin_string

def get_encoded(message):
	secret = ""
	for char in message:
				if is_encoding(char):
					secret += char
	return secret
	
	
def get_binary_from_plaintext(message):
    bin_message = ''.join(format(ord(x), 'b').zfill(8) for x in message)
    return bin_message

def get_space(text):
    count = 0
    for char in text:
        if is_encoding(char):
            count+=1
    return count//8

def hide_message(message,text):
	space = get_space(text)
	if len(message) > space:
		raise SpaceError(space,len(message))
	else:
		binary_string = get_binary_from_plaintext(message)
		x=0
		new_message = ''
		for char in text:
			if is_encoding(char) & (x<len(binary_string)):
				if binary_string[x]=='1':
					new_message = new_message + "\\" + char
				else:
					new_message += char
				x+=1
			else:
				new_message += char
		return new_message

class SpaceError(Exception):
	def __init__(self,space,size):
		self.space = space
		self.size = size
	def __str__(self):
		return "Secret is %d bytes long. Message can only hide %d bytes." % (self.size, self.space)
